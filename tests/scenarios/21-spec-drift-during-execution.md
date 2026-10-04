# Scenario 21: Spec Drift During Active Execution

Verify that `/work` detects and handles spec changes made while tasks are already decomposed and in progress.

## Context

Users frequently edit the spec after decomposition — adding detail, changing requirements, or removing sections. On every `/work`, Step 1b runs a deterministic check (`fingerprint.py --drift .claude`) that compares each task's `section_fingerprint` with the current hash of its own `## ` section and groups the changed tasks by section. Drift Reconciliation then presents them, before Step 1d. The decomposed snapshot only supplies the diff shown in each prompt. The critical invariant: no task should silently execute against a stale spec section.

## State

- `spec_v1.md` (status `active`, edited within the last week) has 10 `## ` sections; four of them have tasks
- `spec_v1.md` decomposed into 8 tasks across 2 phases
- Decomposed snapshot saved at `.claude/support/previous_specifications/spec_v1_decomposed.md`
- Tasks have `spec_version: "spec_v1"`, `spec_fingerprint`, `section_fingerprint`, `spec_section` and `section_snapshot_ref` from decomposition
- Phase 1: Tasks 1-4 (Task 1: Finished, Task 2: In Progress, Tasks 3-4: Pending)
- Phase 2: Tasks 5-8 (all Pending)
- No `drift-deferrals.json` yet
- User has since edited `spec_v1.md`:
  - **Section "## Authentication"** (maps to Tasks 2, 3): Changed from "basic auth" to "OAuth 2.0" — substantive requirement change
  - **Section "## API Endpoints"** (maps to Tasks 5, 6): Added a new endpoint — additive change
  - **Section "## Database Schema"** (maps to Tasks 1, 4): Unchanged
  - **Section "## Deployment"** (maps to Tasks 7, 8): Typo fix only

---

## Trace 21A: Deterministic drift check identifies changed sections

- **Path:** /work Step 1b (`fingerprint.py --drift .claude`) → Step 1c

### Scenario

User runs `/work` after editing the spec. Step 1b runs the drift check. It runs on every `/work`, whatever the dashboard META says.

### Expected

1. `fingerprint.py --drift .claude` compares each task's `section_fingerprint` with the current hash of its `## ` section (if the script can't run, the prose rules in `drift-reconciliation.md` give the same result)
2. Output, sections in heading order:
   - `drifted`: `## API Endpoints` (Tasks 5, 6), `## Authentication` (Tasks 2, 3), `## Deployment` (Tasks 7, 8), each `deferred: false`
   - Tasks 1 and 4 are in sync (`## Database Schema` unchanged) and not reported; `checked: 8`
   - `unreconciled_sections: 3`
3. Detection can't tell a typo from a requirement change: all three sections are reported the same way. The difference shows up in Claude's recommendation (21B)
4. Step 1c reports 3 changed sections
5. Substantial-change check: 3 of 10 sections changed, none added or deleted → not substantial, no version-bump prompt
6. Drift Reconciliation runs next (21B), before Step 1d and before any task is routed

### Pass criteria

- [ ] Each task compared against its own section's current hash (not a full-spec binary check)
- [ ] Check runs even when the dashboard META `spec_fingerprint` matches the current spec
- [ ] Each changed section identified with its affected tasks
- [ ] Unchanged sections (Database Schema) not flagged
- [ ] Tasks grouped by their source section

### Fail indicators

- All 8 tasks flagged as affected (full-spec comparison instead of per-section)
- Only the first changed section detected
- Step 1b skipped because the dashboard META matched (the FB-128 failure; see Scenario 44 Trace A)

---

## Trace 21B: Reconciliation — batch prompt, then per-section picks

- **Path:** /work Drift Reconciliation → `drift-reconciliation.md` § "Granular Reconciliation UI"

### Scenario

Three changed sections are unreconciled, so the batch list comes first. Every one of them has open tasks, so each is marked and goes through its own prompt; `[K]` Keep all isn't offered.

### Expected

1. Batch list (shown when 2+ changed sections are unreconciled):
   ```
   3 spec sections changed since their tasks were built:
     ## API Endpoints — 2 Pending (has open tasks — reviewed separately)
     ## Authentication — 1 In Progress, 1 Pending (has open tasks — reviewed separately)
     ## Deployment — 2 Pending (has open tasks — reviewed separately)
   ```
   Every listed section is marked, so there is nothing for `[K]` Keep all to keep: the list is an overview, and the per-section prompts follow.
2. Each section prompt shows the diff against `spec_v1_decomposed.md`, one recommended option with a one-line reason, and `[A]` Apply / `[V]` Re-verify / `[K]` Keep / `[R]` Review individually / `[S]` Skip (defer):
   - "## API Endpoints" (new endpoint): Claude recommends `[A]` (requirements changed). User picks `[S]`: Tasks 5 and 6 keep their old fingerprints; a deferral is recorded in `drift-deferrals.json` with `deferred_date` and `affected_tasks: ["5", "6"]`
   - "## Authentication" (basic auth → OAuth 2.0): Claude recommends `[A]`. User picks `[A]`: the section has no Finished task, so no reset warning. Tasks 2 and 3 are open, so they get the current `spec_fingerprint` and `section_fingerprint`, Claude updates their descriptions for OAuth 2.0, their statuses stay (In Progress, Pending), and each gains `[DRIFT UPDATED {YYYY-MM-DD}] ## Authentication changed; {what changed in the task}` (Task 2: see also 21C)
   - "## Deployment" (typo fix): Claude recommends `[K]` (typo-only). User picks `[K]`: Tasks 7 and 8 get the current fingerprints, keep their status, and each gains the note `[DRIFT KEPT {YYYY-MM-DD}] ## Deployment changed; user kept verification: {one-line reason}`
3. Task files and `drift-deferrals.json` were written, so the dashboard is regenerated (Tier-1 trigger "drift reconciliation applied"; either write alone would trigger it). No task's status changed, so `task_hash` alone wouldn't have caught it
4. In the regenerated dashboard, `## API Endpoints` is `deferred: true`, so `unreconciled_sections` is 0: META `drift_sections: 0` and `drift_deferrals: 1`; footer `⚠️ 0 changed spec section(s), 1 drift deferrals, 0 verification debt`; the Needs-you Spec Drift sub-section shows only the deferral row (`1 deferred spec-drift reconciliation(s) → run /work to review`)
5. `/work` continues to Step 1d and routing

### Pass criteria

- [ ] Batch list shows each changed section with task counts by status and marks each section with open tasks `(has open tasks — reviewed separately)`; with every section marked, `[K]` Keep all isn't offered, and there is never a defer-all
- [ ] Each section prompt offers the five options with one recommendation; nothing is applied without the user's pick
- [ ] Per-section picks respected independently
- [ ] `[A]` and `[K]` refresh fingerprints on every task in the section, In Progress included; `[S]` leaves them and records a dated deferral
- [ ] `[A]` updates open tasks' text in place, leaves their status, and writes the `[DRIFT UPDATED …]` note
- [ ] Typo-only section recommended `[K]`, requirement change recommended `[A]`
- [ ] `[K]` changes no status and writes the `[DRIFT KEPT …]` note
- [ ] Dashboard regenerated after reconciliation; the deferred section shows as a deferral, not as a changed section
- [ ] In Progress tasks with updated fingerprints are handled by the post-reconciliation warning (see 21C)

### Fail indicators

- All-or-nothing reconciliation (accept all or reject all)
- A "defer all" option in the batch prompt
- A section with open tasks kept by a batch `[K]` without its own prompt
- An option applied without the user's pick
- Typo-level change recommended `[A]` (task re-evaluation for a typo)
- Dashboard still lists three changed sections after reconciliation (no regen, because `task_hash` didn't change)
- In-progress task silently re-fingerprinted without warning about partial work
- Deferred sections forgotten (no tracking)

---

## Trace 21C: In-progress task affected by drift

- **Path:** /work post-reconciliation warning

### Scenario

After reconciliation (21B), Task 2 is In Progress but its spec section changed from "basic auth" to "OAuth 2.0". The user chose `[A]` for that section. `/work` runs the post-reconciliation check.

### Expected

1. `/work` detects Task 2 is In Progress with an updated section fingerprint
2. Warning displayed: `⚠️ Task 2 "Implement authentication" is In Progress but its spec section changed during reconciliation. Review the task's partial work against the updated requirements before continuing.`
3. Warning is informational, not a gate — user can proceed or manually reset the task
4. `/work` continues to routing after displaying the warning

### Pass criteria

- [ ] Warning displayed for In Progress tasks with changed section fingerprints
- [ ] Warning is specific: names the task and the fact that requirements changed
- [ ] Warning does not block work — user can proceed
- [ ] Partial work is not discarded or reset automatically

### Fail indicators

- Task 2 silently re-dispatched against new requirements with no warning
- No mention of the requirement change to the user
- Warning treated as a hard gate (blocks all work until user acts)
- Task automatically reset to Pending without user consent

---

## Trace 21D: Drift budget enforcement

- **Path:** drift budget enforcement

### Scenario

User has been deferring sections across multiple `/work` runs. Current state: 3 sections deferred, one deferred 15 days ago. The budget rules are unchanged by v5.9.0.

### Expected

1. `/work` checks drift budget on every run (no fast path skips it):
   - Max deferred sections threshold checked
   - Max deferral age threshold checked
2. If budget exceeded: `/work` pauses and requires reconciliation before continuing
3. Stale deferrals (> configured age) highlighted specifically
4. User cannot indefinitely postpone drift reconciliation
5. `[S]` (per section, or per task under `[R]`) remains the only way to defer. The batch prompt has no defer-all, because a project with several changed sections would exceed `max_deferred_sections` with one keystroke

### Pass criteria

- [ ] Drift budget checked on each `/work` run
- [ ] Exceeding max deferrals blocks further work until resolved
- [ ] Stale deferrals surfaced with age
- [ ] Budget thresholds are configurable (not hardcoded)
- [ ] No prompt defers several sections at once

### Fail indicators

- Unlimited deferrals allowed (drift accumulates silently)
- Budget enforcement skipped if tasks are available to work on
- No indication of how long sections have been deferred
- A batch "defer all" path that bypasses the budget
