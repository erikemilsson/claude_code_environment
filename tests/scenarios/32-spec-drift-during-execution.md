# Scenario 32: Spec Drift During Active Execution

Verify that `/work` detects and handles spec changes made while tasks are already decomposed and in progress.

## Context

Users frequently edit the spec after decomposition — adding detail, changing requirements, or removing sections. The drift detection system (work.md Step 1b, drift-reconciliation.md) must compare the current spec against the decomposed snapshot using section-level fingerprints, identify what changed, and present reconciliation options. The critical invariant: no task should silently execute against a stale spec section.

## State

- `spec_v1.md` decomposed into 8 tasks across 2 phases
- Decomposed snapshot saved at `.claude/support/previous_specifications/spec_v1_decomposed.md`
- Tasks have `spec_fingerprint`, `section_fingerprint`, and `spec_section` fields from decomposition
- Phase 1: Tasks 1-4 (Task 1: Finished, Task 2: In Progress, Tasks 3-4: Pending)
- Phase 2: Tasks 5-8 (all Pending)
- User has since edited `spec_v1.md`:
  - **Section "## Authentication"** (maps to Tasks 2, 3): Changed from "basic auth" to "OAuth 2.0" — substantive requirement change
  - **Section "## API Endpoints"** (maps to Tasks 5, 6): Added a new endpoint — additive change
  - **Section "## Database Schema"** (maps to Task 1): Unchanged
  - **Section "## Deployment"** (maps to Tasks 7, 8): Typo fix only

---

## Trace 32A: Granular drift detection identifies changed sections

- **Path:** work.md Step 1b § "Spec Drift Detection (Granular)"; drift-reconciliation.md § "Spec Drift Detection"

### Scenario

User runs `/work` after editing the spec. Step 1b computes spec fingerprint, detects mismatch, performs section-level analysis.

### Expected

1. Full spec fingerprint differs from stored `spec_fingerprint` on tasks
2. Section-level analysis runs:
   - "## Authentication": fingerprint changed → Tasks 2, 3 affected
   - "## API Endpoints": fingerprint changed → Tasks 5, 6 affected
   - "## Database Schema": fingerprint matches → Task 1 unaffected
   - "## Deployment": fingerprint changed → Tasks 7, 8 affected
3. Granular reconciliation UI presented per changed section

### Pass criteria

- [ ] Section-level comparison used (not just full-spec binary check)
- [ ] Each changed section identified with its affected tasks
- [ ] Unchanged sections (Database Schema) not flagged
- [ ] Tasks grouped by their source section in the reconciliation UI

### Fail indicators

- All 8 tasks flagged as affected (full-spec fallback instead of granular)
- Only the first changed section detected
- Typo-only change (Deployment) treated identically to requirement change (Authentication)

---

## Trace 32B: Reconciliation UI — user chooses per-section actions

- **Path:** drift-reconciliation.md § "Granular Reconciliation UI"

### Scenario

Drift detected in 3 sections. User presented with options per section: `[A]` Accept (update fingerprint, re-align tasks), `[R]` Reject (revert spec section), `[S]` Skip/Defer.

### Expected

1. "## Authentication" — user selects `[A]` Accept:
   - Task 2 (In Progress): `section_fingerprint` updated (post-reconciliation warning surfaces this in 32C)
   - Task 3 (Pending): `section_fingerprint` updated, task description may need revision
2. "## API Endpoints" — user selects `[S]` Defer:
   - Tasks 5, 6 retain old fingerprints
   - Deferral recorded in `drift-deferrals.json`
3. "## Deployment" — user selects `[A]` Accept:
   - Tasks 7, 8: fingerprints updated silently (typo-level change, no task revision needed)

### Pass criteria

- [ ] Per-section actions respected independently
- [ ] Accept updates `section_fingerprint` on affected tasks (both In Progress and Pending)
- [ ] Deferred sections tracked with timestamp in `drift-deferrals.json`
- [ ] Trivial changes (typos) update fingerprints without flagging for task revision
- [ ] In Progress tasks with updated fingerprints are handled by the post-reconciliation warning (see 32C)

### Fail indicators

- All-or-nothing reconciliation (accept all or reject all)
- In-progress task silently re-fingerprinted without warning about partial work
- Deferred sections forgotten (no tracking)
- Typo-level change triggers full task re-evaluation

---

## Trace 32C: In-progress task affected by drift

- **Path:** work.md § "Post-reconciliation In Progress warning" → Step 2c routing

### Scenario

After reconciliation (32B), Task 2 is In Progress but its spec section changed from "basic auth" to "OAuth 2.0". User accepted the change. `/work` runs the post-reconciliation check.

### Expected

1. `/work` detects Task 2 is In Progress with an updated section fingerprint
2. Warning displayed: `⚠️ Task 2 "Implement authentication" is In Progress but its spec section changed during reconciliation. Review the task's partial work against the updated requirements before continuing.`
3. Warning is informational, not a gate — user can proceed or manually reset the task
4. `/work` continues to routing (Step 2c) after displaying the warning

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

## Trace 32D: Drift budget enforcement

- **Path:** drift-reconciliation.md § "Drift Budget Enforcement"

### Scenario

User has been deferring sections across multiple `/work` runs. Current state: 3 sections deferred, one deferred 15 days ago.

### Expected

1. `/work` checks drift budget before proceeding:
   - Max deferred sections threshold checked
   - Max deferral age threshold checked
2. If budget exceeded: `/work` pauses and requires reconciliation before continuing
3. Stale deferrals (> configured age) highlighted specifically
4. User cannot indefinitely postpone drift reconciliation

### Pass criteria

- [ ] Drift budget checked on each `/work` run
- [ ] Exceeding max deferrals blocks further work until resolved
- [ ] Stale deferrals surfaced with age
- [ ] Budget thresholds are configurable (not hardcoded)

### Fail indicators

- Unlimited deferrals allowed (drift accumulates silently)
- Budget enforcement skipped if tasks are available to work on
- No indication of how long sections have been deferred
