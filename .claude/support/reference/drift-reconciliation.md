# Drift Detection and Reconciliation

Procedures for detecting spec drift, reconciling changes with tasks, managing version transitions, and enforcing drift budgets. These run inline during `/work` Step 1.

---

## Dashboard Freshness Check

Before using dashboard data, verify it's current (runs as `/work` Step 1a, after the `pending_decomposition[]` check):

1. **Compute current task state hash** — canonical: `python3 .claude/scripts/dashboard-render.py --task-hash`:
   ```
   task_hash = SHA-256(sorted list of: task_id + ":" + status + ":" + difficulty + ":" + owner + ":" + review
                       for each active task-*.json; review = 1 if user_review_pending else 0)
   ```

2. **Read dashboard metadata** (if present):
   ```markdown
   <!-- DASHBOARD META
   generated: 2026-01-28T14:30:00Z
   task_hash: sha256:abc123...
   spec_fingerprint: sha256:def456...
   -->
   ```

3. **Compare hashes:**
   ```
   If dashboard has no META block, task_hash differs, OR META spec_fingerprint
   differs from the current spec hash (fingerprint.py --spec .claude/spec_v{N}.md):
   ├─ Log: "Dashboard stale — regenerating"
   ├─ Regenerate dashboard from task JSON files
   └─ Continue with fresh dashboard
   ```
   User content lives in the sidecar (`dashboard-state.json`), not in the HTML, so a regen loses nothing.

   **META `spec_fingerprint`** records the spec the dashboard was rendered from. It is **not** evidence that drift was checked: every regen stamps the current spec hash, whether or not any task was reconciled. Drift is checked by Step 1b on every `/work` (§ "Spec Drift Detection").

4. **Compare template_version:**
   ```
   Read template_version from META block
   Read template_version from .claude/version.json
   If they differ OR META field is absent:
   ├─ Log: "Dashboard format stale — regenerating"
   ├─ Regenerate dashboard (will use current format rules and set new template_version in META)
   └─ Continue with fresh dashboard
   ```

A dashboard can be content-stale (task hash or spec hash mismatch) or format-stale (template_version mismatch). Either triggers full regeneration; the two checks share a single full-regen invocation when both fire. (The dashboard is read-only HTML rendered whole each time — there is no targeted-edit drift to track; the old `pending_full_regen` sentinel was retired.)

**Why this matters:** Dashboard can become stale if tasks are modified outside `/work`, if the spec is edited, or if template sync updates the format rules. This check ensures you always work from accurate data with current formatting.

---

## Spec Drift Detection (Granular)

Runs as `/work` Step 1b, on every `/work`. It compares each task's `section_fingerprint` with the current hash of the section its `spec_section` names: a `## ` section, or a `### ` subsection whose heading is unique in the spec. Detection needs no snapshot: `section_snapshot_ref` is only used to show diffs in the reconciliation UI.

**Deterministic check:** `python3 .claude/scripts/fingerprint.py --drift .claude` (the argument is the `.claude` directory). It is read-only and exits 0 on success, including when there is no spec or no tasks, and 2 when the directory doesn't exist or on a usage error. Keys are always present; lists are sorted by section heading, tasks by natural id order:

```json
{
  "spec": "spec_v3",
  "spec_fingerprint": "sha256:…",
  "checked": 42,
  "drifted": [
    {"section": "## Auth", "fingerprint": "sha256:<current section hash>", "deferred": false,
     "tasks": [{"id": "12", "title": "…", "status": "Finished", "owner": "claude",
                "deferred": false, "subsection_unchanged": false}]}
  ],
  "missing": [{"section": "## Old name",
               "tasks": [{"id": "31", "title": "…", "status": "Pending", "owner": "claude"}]}],
  "unmigrated": ["7"],
  "historical": 33,
  "unmatched": 45,
  "no_provenance": 20,
  "unmapped": 3,
  "unreadable": ["task-9.json"],
  "unreconciled_sections": 1
}
```

With no spec file, `spec` and `spec_fingerprint` are `null`, every list is empty and every count is 0.

**Unreconciled drift** means `unreconciled_sections` > 0. The number counts drifted sections with at least one non-deferred task, plus missing sections. `/work` routes it to § "Granular Reconciliation UI"; `/status` and the dashboard report the same number.

**Rules.** This is the prose fallback when the script can't run. `fingerprint.py` implements the same rules, so change both together. Candidates are `.claude/tasks/task-*.json` (not `archive/`); a file that fails to parse, or whose JSON is not an object, goes in `unreadable`. The current spec is the single `spec_v{N}.md` (the highest N if there are several). For each task, the first matching rule wins:

1. `status` is `Absorbed` or `Broken Down`, or `out_of_spec` is true → skip; not counted. Subtasks carry the provenance (`/breakdown` copies it), and an out-of-spec task has no spec section to drift from.
2. `spec_version` is a non-empty string that doesn't name the current spec → a Finished task counts as `historical` (Task Migration leaves its provenance unchanged by design); any other status goes in `unmigrated` (§ "Task Migration on Version Transition"). `spec_version` names the current spec when, after `.strip()`, it equals the current stem (`spec_v3`), its bare number (`3`) or `v3`. A `spec_version` that is missing, empty or not a string counts as current.
3. `spec_section` or `section_fingerprint` is missing or blank → never flagged. Counted in `unmapped` when `spec_unmapped` is `true` (the task declares it belongs to no single section), otherwise in `no_provenance`. A task that has both fields goes on to rule 4 whatever its `spec_unmapped` says.
4. **Heading match**, with `s = spec_section.strip()`:
   - (a) `s` matches a current `## ` heading line `h` when `h.strip() == s`, or else when `h.strip() == "## " + s`.
   - (b) If no `## ` heading matches and `s` starts with `### `, `s` matches when **exactly one** current `### ` heading line has `.strip() == s`. The task is then compared with that subsection's hash and reported under the `### ` heading. Some projects record subsection-level provenance this way.
   - (c) No match, or several `### ` matches → a Finished task adds to `unmatched` (the work shipped, and its provenance is historical or free-form, so nothing is prompted); any other status goes in `missing` under `s`.
5. Matched → counted in `checked`. If `section_fingerprint` equals the current hash of the matched section (the subsection, under 4b), the task is in sync and nothing is reported.
6. Matched and different → `drifted`, grouped under the matched heading. The task is `subsection_unchanged` only when it has `spec_subsection` and `subsection_fingerprint`, and the current hash of that `### ` subsection, looked up within the task's matched `## ` section only, equals `subsection_fingerprint` (§ "Subsection-level drift narrowing"). A task matched under 4b is never `subsection_unchanged`.

**Deferrals.** `.claude/drift-deferrals.json` is `{"deferrals": [...]}` or a bare list; ignore anything else, and any entry without a string `section`. An entry matches a drifted section when `section.strip()` equals the heading, or `"## " + section.strip()` does. An entry with a non-empty `affected_tasks` list defers only those tasks (ids are compared as strings, so `3` and `"3"` match); otherwise it defers every drifted task in the section. A section is `deferred` when all its drifted tasks are. Missing sections are never deferred.

**Tasks without a section fingerprint are never flagged.** Comparing them with the full-spec hash would flag every such task on every spec edit. Such tasks are counted in `no_provenance` instead (or in `unmapped`, when they say so with `spec_unmapped: true`). New tasks don't land in `no_provenance`: every creation path stamps provenance (`task-schema.md § "Drift Prevention Fields"`, creation contract). For tasks that already lack it, `/health-check` Part 1 check 11 offers a one-time baseline (`fingerprint.py --baseline`), which stamps the hash the section had in the spec's git history at the task's date. History-dated hashes assume the spec was edited on the line the task was built on: a side-branch edit is dated by its merge, and a fast-forwarded branch can't be told apart. A task's own `spec_fingerprint` isn't compared either, since a full-spec hash changes on any edit.

**Hash computation:**
```bash
# Use shasum (available on macOS and Linux; sha256sum is Linux-only)
shasum -a 256 .claude/spec_v{N}.md | cut -d' ' -f1
# Prefix with "sha256:" → "sha256:a1b2c3d4..."
```

**Section fingerprint computation:**
```bash
# For each ## section, hash: heading + all content until next ## or EOF
printf '%s' "## Authentication\nContent here..." | shasum -a 256 | cut -d' ' -f1
# Prefix with "sha256:" → "sha256:e5f6g7h8..."
# A ### subsection hashes the same way: heading + content until the next ###, ## or EOF
```

**Script alternative:** `.claude/scripts/fingerprint.py --spec PATH` (full spec) or `.claude/scripts/fingerprint.py --sections PATH` (JSON map of `## heading` → hash) — produces byte-identical output to the prose recipes above. Use when running in the orchestrator; the prose recipe remains authoritative if the script is absent. `--sections --depth 3` ALSO emits `### ` subsection hashes (additive — `## ` hashes are unchanged) for finer drift localization on very large sections; `--index PATH` emits the spec section index (below); `--drift DIR` runs the whole check above.

### Spec Index Freshness

The spec section index (`.claude/spec_v{N}.index.json`, generated by `fingerprint.py --index`) lets commands and agents locate a `## ` section by heading and `Read` only its line range instead of loading the whole spec — see `rules/spec-workflow.md § "Section-scoped spec reading"`. The index is a **derived, regenerable artifact** whose freshness is driven by the same full-spec fingerprint Step 1b already computes:

```
Index is stale when: the file is missing OR its top-level `spec_fingerprint` differs
from the current full-spec fingerprint.

When stale → regenerate (orchestrator owns the write):
  python3 .claude/scripts/fingerprint.py --index .claude/spec_v{N}.md  > .claude/spec_v{N}.index.json
```

`/work` Step 1b compares the index's `spec_fingerprint` with the drift JSON's `spec_fingerprint` (the current full-spec hash) and regenerates the index when they differ. Consumers reading the spec outside `/work` (audits, `/iterate`, agents) apply the same missing-or-mismatched guard before trusting the index, and fall back to a direct scoped/full read otherwise (subagents cannot write `.claude/`, so they read the index only if already fresh, else read the spec directly). The index carries **no task provenance** and is **not** fingerprinted into tasks — it never participates in drift reconciliation, so a stale index is a performance miss, never a correctness risk.

### Subsection-level drift narrowing

A one-line edit rehashes the entire `## ` section, so every task under it shows as drifted, even tasks whose own `### ` subsection is untouched. This matters most for **large** sections (the section index reports a high `char_count`, tens of KB). Narrowing spares those tasks:

1. **Per-task narrowing (`subsection_unchanged`).** A drifted task that carries `spec_subsection` + `subsection_fingerprint` (see `task-schema.md`) is marked `subsection_unchanged: true` when the current hash of that `### ` subsection, found within the task's matched `## ` section, still equals its `subsection_fingerprint`. A repeated `### ` heading elsewhere in the spec doesn't count. A task whose `spec_section` is itself a `### ` heading (rule 4b) is already compared at subsection level and is never marked. The reconciliation UI shows such tasks in a **"likely unaffected (subsection unchanged)"** group with `[K] Keep` recommended. They are never dropped; the user can still pick any option. A task without the pair (legacy, small-section or whole-section task) is flagged at `## `-level as before. **No regression.**
2. **Subsection breakdown.** For a large changed section, diff the `### ` hashes of the snapshot and of the current spec and name the changed subsections in the UI, whatever the task provenance: *"`## Phase 40` changed — specifically `### X`, `### Y` (subsections `### A`–`### F` unchanged)."* With no snapshot, skip the breakdown.
3. **On reconcile:** every option except `[S]` and `[O]` refreshes `subsection_fingerprint` along with `section_fingerprint`, when the task has one.

The `### ` hashes are additive: `--depth 3` never changes the `## ` hashes, so narrowing never alters the `## `-level comparison. It is a precision refinement on top of `## `-level drift: it can only spare tasks the user would otherwise keep by hand, and the "likely unaffected" grouping (surface, don't drop) keeps it safe.

### What fingerprints can't see

Fingerprints detect change, not wrongness. A section that was wrong when it was written stays fingerprint-current, so the drift check never flags it, even while it misdescribes shipped work. A downstream project spent eight days and four cleanup passes on such sections. The instruments for this are closure sweeps (verify-agent T2c item 4) and `/audit-coherence`.

---

## Substantial Change Detection

Before showing the reconciliation UI, evaluate the magnitude of changes and respond accordingly.

**Heuristic — changes are "substantial" when ANY of:**
- More than 50% of sections have changed fingerprints
- New sections were added (scope expansion)
- Sections were deleted (scope reduction)
- Spec has been `active` for > 7 days AND > 3 sections changed

**If changes are NOT substantial:**

Proceed directly to the Granular Reconciliation UI (below). Small edits are absorbed into the current version via normal drift reconciliation.

**If changes ARE substantial:**

Present a version bump suggestion before reconciliation:

```
Spec has changed significantly since tasks were created:
  - {X} of {Y} sections modified
  - {A} new sections added / {B} sections deleted
  - Estimated {P}% of content changed

This may warrant a new spec version.

[N] New spec version (v{N+1}) (archives current version, then reconcile)
[C] Continue as v{N} (reconcile changes in place)
```

- **If user picks [N]:** Execute the Version Transition Procedure (see `iterate.md` § "Version Transition Procedure"), then run Task Migration (below), then proceed to reconciliation against the new version.
- **If user picks [C]:** Proceed directly to the Granular Reconciliation UI. Changes are absorbed into the current version.

Either choice preserves the user's edits. The version bump is about organizational clarity, not data safety.

---

## Task Migration on Version Transition

When `/work` detects that existing tasks reference an older spec version (tasks have `spec_version: "spec_v{M}"` but current spec is `spec_v{N}` where N > M), perform task migration:

```
For each task:
  IF status == "Finished", "Absorbed" or "Broken Down":
    → Leave provenance unchanged (historical record; subtasks carry their own)
    → These tasks were verified/resolved against the old spec — that's correct

  IF any other status (the drift check's `unmigrated` list):
    → Check if task's spec_section heading still exists in new spec
    │
    ├─ Section exists, content matches:
    │  → Update task: spec_version, spec_fingerprint, section_fingerprint (and subsection_fingerprint if present)
    │  → Task continues normally
    │
    ├─ Section exists, content changed:
    │  → Update spec_version reference
    │  → Flag for reconciliation (handled by Granular Reconciliation UI)
    │
    └─ Section does not exist in new spec:
       → Present to user:
       │
       │  Task {id} "{title}" references section "{spec_section}"
       │  which no longer exists in spec v{N}.
       │
       │  [D] Delete task
       │  [O] Keep as out-of-spec
       │  [R] Reassign to different section
```

**After migration:** Update the decomposed snapshot reference. Create `spec_v{N}_decomposed.md` if decomposition runs, or update `section_snapshot_ref` on migrated tasks to point to the new spec version's snapshot. Then re-run `python3 .claude/scripts/fingerprint.py --drift .claude`: the migrated tasks now name the current spec, so a changed section among them shows up as drift in this run, not the next.

---

## Drift Budget Enforcement

To prevent drift from accumulating indefinitely, enforce a drift budget.

**Configuration (in spec frontmatter):**
```yaml
---
version: 1
status: active
drift_policy:
  max_deferred_sections: 3      # Max sections that can be deferred
  max_deferral_age_days: 14     # Max days a deferral can persist
---
```

**Default values (if not configured):** `max_deferred_sections: 3`, `max_deferral_age_days: 14`

**Tracking deferred reconciliations:**

When the user picks `[S]` Skip during reconciliation, record it (a per-task skip lists only the skipped tasks in `affected_tasks`):
```json
// In .claude/drift-deferrals.json
{
  "deferrals": [
    {
      "section": "## Authentication",
      "deferred_date": "2026-01-20",
      "affected_tasks": ["3", "4", "7"]
    }
  ]
}
```

**Enforcement logic:**
```
On each /work run:
1. Read drift-deferrals.json (if exists)
2. Count active deferrals (not yet reconciled)
3. Check for expired deferrals (older than max_deferral_age_days)

IF active_deferrals > max_deferred_sections:
  ├─ ERROR: Too many deferred sections
  │
  │  You have deferred reconciliation for N sections (max: M).
  │  Must reconcile at least {N - M} section(s) before continuing.
  │
  │  [R] Reconcile now (required)
  │
  └─ Proceed to Granular Reconciliation UI (pre-filtered to deferred sections)

IF any deferral expired (and count is within budget):
  ├─ WARNING: Deferral expired
  │
  │  Deferral for "## SectionName" has expired (deferred N days ago, max: M days).
  │
  │  [R] Reconcile now (recommended)
  │  [X] Reset deferral timers (acknowledges drift risk)
  │
  ├─ If user selects [R]: proceed to Granular Reconciliation UI
  └─ If user selects [X]:
     1. Update each expired deferral's deferred_date to today in drift-deferrals.json
        (deferrals will expire again after max_deferral_age_days)
     2. Log: "⚠️ Drift deferrals reset — {N} sections remain unreconciled. Tasks in these sections may not match the current spec."
     3. Continue with /work (unblock)
```

**Clearing deferrals:** When a section is reconciled with any option except `[S]`, remove its entry from `drift-deferrals.json`. After a per-task review, keep only the still-skipped tasks in the entry's `affected_tasks`.

**See also:**
- `.claude/support/reference/workflow.md` § "Spec Change and Feature Addition" for the end-to-end process overview.

---

## Granular Reconciliation UI

Runs after `/work` Step 1c and before Step 1d whenever the drift check reports unreconciled drift, and for deferred sections when § "Drift Budget Enforcement" requires it. Claude recommends an option; the user always picks, and nothing applies by default.

**Batch prompt** when 2+ drifted sections are unreconciled. Missing sections are never in the batch; they always go through `[D]`/`[O]`/`[R]` per task (see "Missing sections" below).

```
{N} spec sections changed since their tasks were built:
  ## Auth — 3 Finished, 1 Pending (has open tasks — reviewed separately)
  ## Billing — 2 Finished
[E] Go through each section | [K] Keep all (the edits don't change what was built)
```

`[K]` applies Keep only to sections whose drifted tasks are all Finished. A section with a drifted open task (any status but Finished) is listed with the marker `(has open tasks — reviewed separately)` and always goes through the per-section prompt, whichever option the user picks here, because an open task may need its text updated before it's built. `[E]` presents every section one at a time. When every listed section is marked, `[K]` isn't offered: the list is shown as an overview and the per-section prompts follow. There is no "defer all": a project with many changed sections would exceed the deferral budget in one step.

**Per section:** show this prompt, then the affected tasks, with any `subsection_unchanged` tasks grouped as "likely unaffected (subsection unchanged)" (§ "Subsection-level drift narrowing").

```
Section "## Auth" changed — 3 Finished, 1 Pending task(s).
  {diff, or the current section text when there is nothing to diff against}
  Recommended: [K] — {one-line reason from the diff}
  [A] Apply — reset Finished tasks to Pending (rebuild + re-verify); update open tasks
  [V] Re-verify — check the shipped work against the new text, no rebuild; update open tasks
  [K] Keep — the edit doesn't change what was built; keep verification
  [R] Review individually | [S] Skip (defer)
```

| Option | Fingerprints | Finished tasks | Open tasks |
|---|---|---|---|
| `[A]` Apply | refreshed | reset to Pending; `task_verification` + `user_review_pending` cleared; `verification_attempts` set to 0 | description or acceptance criteria updated where the new text changes them; status unchanged; `[DRIFT UPDATED]` note |
| `[V]` Re-verify | refreshed | → Awaiting Verification with `drift_reverify` set and `verification_attempts` set to 0; verify-agent checks the shipped work against the current text (`owner: human`: stays Finished with `user_review_pending: true`) | as `[A]` |
| `[K]` Keep | refreshed | status, `task_verification`, `user_review_pending` untouched | untouched |
| `[R]` Review individually | per task: `[A]` Apply, `[V]` Re-verify, `[K]` Keep, `[E]` Edit, `[S]` Skip, `[O]` Mark out-of-spec | | |
| `[S]` Skip | unchanged; deferral recorded (budget applies) | | |

**Refreshed** means `spec_fingerprint`, `section_fingerprint` and, when present, `subsection_fingerprint` are set to current values. For a task whose `spec_section` is a `### ` heading, `section_fingerprint` takes that subsection's hash. Every choice except `[S]` and `[O]` refreshes them, including per-task choices; `[O]` only sets `out_of_spec: true` and keeps the provenance fields, since the drift check skips out-of-spec tasks.

**Recommendation rule.** Claude recommends one option per section, from the diff: editorial-only edits (status, annotation, typo) → `[K]`; acceptance text changed → `[V]` (re-verifies Finished work, updates open tasks); requirements changed so the shipped work must be rebuilt → `[A]`.

**Attempt counter.** `[A]` and `[V]` set `verification_attempts` to 0 on the Finished tasks they send back to rebuild or re-verification; `verification_history` keeps the earlier record. The counter counts every dispatched verify return, passes included (a delta re-check is not counted), so a Finished task can already sit at 2, and without the reset a single failed re-check would escalate it to Blocked with no fix cycle.

**Open tasks under `[A]` and `[V]`** (any drifted task that isn't Finished): refresh the fingerprints, update the task's description or acceptance criteria where the new section text changes them, and leave the status alone. Prepend to the task's notes: `[DRIFT UPDATED {YYYY-MM-DD}] {section} changed; {what changed in the task, or "no task change needed"}`.

**`[A]` Apply.** A Finished task was verified against the old section text, so its `task_verification` is stale. When a section contains Finished tasks, warn before applying:
```
⚠️ Section "{section}" contains {N} Finished task(s) that will be reset to Pending:
  - Task {id}: "{title}"
Apply changes? [Y] Yes, reset and re-verify  [N] No, review individually instead
```
If the user selects `[N]`, fall through to `[R] Review individually` for that section (allows per-task decisions).

**On apply (confirmed):**
1. Update `spec_fingerprint` and `section_fingerprint` (and `subsection_fingerprint` if the task carries one) to current values
2. Clear `task_verification` and `user_review_pending` (remove both fields; re-verification sets the flag again where it applies)
3. Set `status` back to `"Pending"` and `verification_attempts` to 0
4. Prepend to its notes: `"Reset to Pending — spec section changed after verification. Needs re-implementation and re-verification."`

Open tasks in the section: see "Open tasks under `[A]` and `[V]`" above.

**`[V]` Re-verify:**
1. Refresh fingerprints.
2. Finished tasks not owned by `human`: set `status` to `"Awaiting Verification"`, remove `task_verification` (`verification_history` stays), set `verification_attempts` to 0 and set `drift_reverify: {"section": "{section}", "date": "{YYYY-MM-DD}"}`. There is no separate dispatch: `/work` Step 3's normal routing sends them to verify-agent (per-task), since Awaiting Verification has priority. Pass → Finished; fail → the normal fail path, starting again at attempt 1.
3. Finished `owner: human` tasks stay Finished with `user_review_pending: true`.
4. Prepend to the notes of each task in steps 2–3: `[DRIFT RE-VERIFY {YYYY-MM-DD}] {section} changed; re-verifying against the current text`. The note is the human-readable record; dispatch reads `drift_reverify`.
5. Open tasks: as under `[A]` (above), with the `[DRIFT UPDATED …]` note.

**Re-verification brief.** Every per-task verify dispatch for a task carrying `drift_reverify` adds the line `Re-verification after a spec edit: the implementation is unchanged; check it against the current section text.` That covers `/work`'s normal dispatch (`work.md § "If Verifying (Per-Task)"`), the re-dispatches in `session-recovery.md` and the timeout re-dispatch (`work-procedures.md`, "After verify-agent returns (per-task mode)" step 5). With that line, verify-agent skips its diff-based scope check (`verify-agent.md` Step T2b): the implementation was committed long ago, and the working tree may hold only the uncommitted spec edit. `drift_reverify` is removed when a per-task verification result is written for the task, pass or fail, so the fix after a failed re-check is verified as usual. It is also removed whenever the task goes back to Pending or In Progress for rework, for example a manual reset after an escalation, because the implementation then changes. A timeout keeps it for the retry.

**`[K]` Keep:** refresh fingerprints; no status or verification change. Prepend to the notes of every task in the section: `[DRIFT KEPT {YYYY-MM-DD}] {section} changed; user kept verification: {one-line reason}`

**Invariant:** no Finished task carries a verification result computed against a different section text than its current fingerprints, except in two recorded cases: the user chose `[K]`, which its notes record; or the task is `owner: human` under `[V]`, which keeps its old verification with fresh fingerprints while `user_review_pending: true` stands in until the user re-checks.

**Diff baseline.** Diffs come from the decomposition snapshot (`section_snapshot_ref`), so after a `[K]`, later diffs show changes since decomposition, not since the keep. The task's latest `[DRIFT KEPT]` note says what was already accepted. A task with no snapshot whose `notes` carry `[BASELINE] … stamped from the spec at <sha>` is diffed against that commit (`git diff <sha> -- .claude/spec_v{N}.md`, cut to the section); only a task with neither gets the current section text alone.

**Missing sections** (open tasks whose `spec_section` has no match under rule 4: no heading, or several `### ` headings) use the § "Task Migration on Version Transition" prompt: `[D]` Delete task, `[O]` Keep as out-of-spec, `[R]` Reassign to a different section. `[R]` sets `spec_section` to the chosen heading and refreshes the fingerprints (`fingerprint.py --provenance .claude --section "<heading>"` prints the values). `[O]` sets `out_of_spec: true` and keeps the provenance fields; the drift check skips out-of-spec tasks (rule 1).

**After reconciling:** clear reconciled sections from `drift-deferrals.json` (§ "Drift Budget Enforcement"). Then, if any choice wrote a task file or `drift-deferrals.json` (an `[S]`-only pass writes just the deferral file), regenerate the dashboard (Tier-1 trigger: **drift reconciliation applied**). `task_hash` covers neither fingerprints nor deferrals, so the Step 1a check wouldn't notice, and the dashboard would keep showing the old drift.

**Edge cases:** New section → suggest new tasks (`/iterate` adds it to `pending_decomposition[]`, and `/work` Step 1a offers decomposition). Section deleted or renamed → its open tasks are missing (above); its Finished tasks only add to `unmatched`. No snapshot → detection still works, because it compares task fingerprints with the current spec; what the UI shows instead is under "Diff baseline" above.
