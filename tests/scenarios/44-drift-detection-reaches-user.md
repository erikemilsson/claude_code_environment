# Scenario 44 — Detected spec drift reaches the user (FB-128)

Conceptual trace test for v5.9.0. `/work` Step 1b runs a deterministic drift check (`fingerprint.py --drift .claude`) on every run, with no META fast path to skip it. Drift Reconciliation runs before the Step 1d fast exit. Two new options, `[V]` Re-verify and `[K]` Keep, let the user keep verified work when an edit doesn't change what was built. Quiet rules keep historical and unprovenanced tasks out of the prompt. Bundled from FB-117: a task waiting on a decision counts as non-actionable in Step 1d.

## Setup / State

- `.claude/spec_v3.md`, status `active`, 12 `## ` sections, so no trace changes more than half of them. Traces D and F also delete a section; if Substantial Change Detection suggests a version bump there, the user picks `[C]` Continue as v3 and reconciliation proceeds as traced.
- Tasks decomposed against it carry `spec_version: "spec_v3"`, `spec_section`, `spec_fingerprint`, `section_fingerprint` and `section_snapshot_ref: "spec_v3_decomposed.md"`. The snapshot exists.
- No `drift-deferrals.json`, and `pending_decomposition[]` is empty, unless a trace says otherwise.
- Each trace lists the tasks it relies on. Any other task is Finished, verified and in sync with its section.

## Trace A — the FB-128 repro: an `/iterate` edit survives a pause regen

Command path: `commands/iterate.md` (post-apply step: edited sections need no marker) → `commands/work.md § "Context Transition"` (pause regen) → next session's `/work`: `§ "Step 1a"` → `§ "Step 1b"` → `§ "Drift Reconciliation"`.

State: `## Auth` has Tasks 1 and 2 (Finished, verified, `owner: claude`) and Task 3 (Pending). The dashboard is current.

1. `/iterate` rewords one of `## Auth`'s acceptance criteria and the user approves. The section already has tasks, so `/iterate` adds nothing to `pending_decomposition[]` and writes no other marker.
2. The user runs `/work pause`, which regenerates the dashboard. META `spec_fingerprint` now equals the edited spec's hash. The renderer's `compute_drift()` sees that `## Auth` no longer matches the `section_fingerprint` of Tasks 1–3, so the regen shows the drift:
   - META `drift_sections: 1`
   - footer `⚠️ 1 changed spec section(s), 0 drift deferrals, 0 verification debt`
   - Needs-you → Spec Drift: `## Auth changed since its tasks were built (2 Finished, 1 Pending) → run /work to reconcile`
3. Next session, `/work`. Step 1a: `task_hash`, `template_version` and `spec_fingerprint` all match META, so no regen. There is no fast path, so Step 1b runs anyway.
4. Step 1b: `fingerprint.py --drift .claude` returns `## Auth` under `drifted` (`deferred: false`; Tasks 1 and 2 Finished, Task 3 Pending) and `unreconciled_sections: 1`.
5. Step 1c reports one changed section. With one section there is no batch prompt; Drift Reconciliation shows the section prompt:
   ```
   Section "## Auth" changed — 2 Finished, 1 Pending task(s).
     {diff against spec_v3_decomposed.md}
     Recommended: [V] — {one-line reason from the diff}
     [A] Apply — reset Finished tasks to Pending (rebuild + re-verify); update open tasks
     [V] Re-verify — check the shipped work against the new text, no rebuild; update open tasks
     [K] Keep — the edit doesn't change what was built; keep verification
     [R] Review individually | [S] Skip (defer)
   ```
   This comes before Step 1d and before any task is routed.

Variant A2, edit outside `/iterate`: instead of step 1, the user edits `## Auth` in an editor after the pause. Step 1a finds META `spec_fingerprint` ≠ the current spec hash and regenerates, so the dashboard shows the drift rows. Step 1b detects the same drift as in step 4. Detection never depends on that regen.

**Expected:** the edit reaches the user at the next `/work`, whatever regens happened in between and whether or not the edit went through `/iterate`. Before v5.9.0, the matching META `spec_fingerprint` sent `/work` down the fast path past Steps 1a and 1b, and the edit was never reconciled.

**Pass criteria:** Step 1b runs although META matches the spec; the dashboard shows the drift (footer, Needs-you row, `drift_sections`) before the user runs `/work`; no marker is needed for an edited existing section; the prompt names one recommended option and applies nothing until the user picks; reconciliation comes before Step 1d and routing.

## Trace B — Step 1d: reconciliation is offered before the fast exit

Command path: `commands/work.md § "Step 1b"` → `§ "Drift Reconciliation"` → `§ "Step 1d: Non-Actionable State Fast Path"`.

State: auto-detect mode (`/work` with no arguments). The only unfinished tasks are Task 4 (`## Billing`, `owner: human`, Pending, dependencies met) and Task 5 (`## Reports`, Blocked). `## Billing` changed since Task 4 and Task 6 (Finished, verified, `owner: claude`) were built. Nothing is In Progress or Awaiting Verification, and there is no verification debt.

1. Step 1b: `## Billing` under `drifted` (Task 6 Finished, Task 4 Pending), `unreconciled_sections: 1`.
2. Drift Reconciliation now runs before Step 1d, so the `## Billing` prompt comes first. Before v5.9.0, Step 1d's fast exit returned first with "No Claude-actionable work", and the drift was never shown.
3. Step 1d is evaluated after the user's pick. Its new precondition is `No unreconciled spec drift (Drift Reconciliation, which now runs before Step 1d, leaves unreconciled_sections at 0)`:
   - `[K]`: fingerprints refreshed, notes written, no task becomes actionable → `unreconciled_sections` is 0 → FAST EXIT. Task 4 is listed under `Your next actions:`, Task 5 under `Blockers:`.
   - `[S]`: a deferral is recorded and `## Billing` becomes `deferred: true` → `unreconciled_sections` is 0 → FAST EXIT, as for `[K]`. Only `drift-deferrals.json` was written, which still counts as drift reconciliation applied, so the dashboard is regenerated and shows a deferral instead of a changed section.
   - `[V]`: Task 6 goes to Awaiting Verification for a verify-agent re-check. Verification takes priority (Step 1d's "no Awaiting Verification" precondition), so no fast exit fires while the re-check is outstanding.
   - `[A]`: Task 6 is reset to Pending, which Claude can act on. No fast exit; `/work` routes to it.
   - Under `[V]` and `[A]` alike, Task 4 (open) keeps its status: Claude updates its description or acceptance criteria where the new text changes them, refreshes its fingerprints and notes `[DRIFT UPDATED 2026-10-04] ## Billing changed; {what changed, or "no task change needed"}`. Under `[K]` it gets the `[DRIFT KEPT …]` note instead.

**Expected:** the reconciliation prompt always comes before the fast-exit output. The fast exit fires only when `unreconciled_sections` is 0 and no work the user's pick created is still outstanding.

**Pass criteria:** drift is shown even when nothing else is Claude-actionable; the fast exit fires after `[K]` or `[S]`; the work a pick creates (`[A]` rebuild, `[V]` re-check) comes before any fast exit; human-owned and Blocked tasks keep their usual fast-exit headings.

## Trace C — a decision-gated task waits, and the fast exit fires (FB-117)

Command path: `commands/work.md § "Step 1d: Non-Actionable State Fast Path"` (Step 2b's checkbox detection first, then the decision clause), consistent with `§ "Step 2c: Parallelism Eligibility Assessment"`.

State: auto-detect mode, no drift (`unreconciled_sections: 0`). The only unfinished tasks are Task 7 "Build CSV export" (`## Export`, Pending, `owner: both`, dependencies met, `decision_dependencies: ["DEC-004"]`; DEC-004's record has `status: proposed` and no option ticked) and Task 8 "Confirm export columns with finance" (Pending, `owner: human`, dependencies met).

1. Step 1b finds nothing to reconcile, so Step 1d's preconditions hold. Step 1d's checkbox scan finds no ticked box, so DEC-004 stays `proposed`.
2. Task 7 is Pending and not Blocked, but its decision dependency is unresolved (the record is `proposed`). It counts as non-actionable, the same as Blocked. Step 2c already leaves such tasks out of batches.
3. Every remaining task is non-actionable → FAST EXIT. Task 8 is listed under `Your next actions:`, and Task 7 under the new heading:
   ```
   Waiting on decisions:
   - Task 7: "Build CSV export" — waiting on DEC-004 → /research DEC-004
   ```
4. Variants: a missing DEC-004 record, or one in `draft`, also counts as unresolved, with the same output. Once DEC-004 is `approved`, Task 7 is actionable: no fast exit, and `/work` routes to it. The clause applies whatever the owner; `owner: claude` behaves the same.
5. Ticked-box variant: since the last `/work`, the user ticked an option in DEC-004's `## Select an Option`, and the frontmatter still says `status: proposed`. Step 1d begins by running Step 2b's checkbox detection, which finds the tick, sets DEC-004 to `approved` with `decided:` today, and logs `Decision DEC-004 resolved → status updated to 'approved' (selected: …)`. The decision clause then finds DEC-004 resolved, so Task 7 is actionable: no fast exit, and `/work` routes to it. Step 2b's own scan later finds nothing new.

**Expected:** before v5.9.0, Task 7 counted as Claude-actionable (Pending, not human-owned), so the fast exit never fired, while Step 2c kept it out of every batch. Now Step 1d and Step 2c agree, and the user is told which decision to resolve. A decision the user has already ticked never holds the task back: without the scan before Step 1d, the fast exit would fire before Step 2b could process the tick, and every `/work` would repeat the wait.

**Pass criteria:** a task with an unresolved decision dependency counts as non-actionable in Step 1d; it's listed under `Waiting on decisions:` with `/research {DEC-ID}`; a missing record or a `draft`/`proposed` status counts as unresolved; a ticked box is processed before the decision clause is evaluated, so a decision ticked while still `proposed` is approved first and its task routes; once the decision is approved, the task routes normally.

## Trace D — batch prompt with two changed sections → `[K]` Keep all

Command path: `commands/work.md § "Drift Reconciliation"` → `drift-reconciliation.md § "Granular Reconciliation UI"` (batch prompt) → `dashboard-regeneration.md § "When to Regenerate"` (Tier 1: drift reconciliation applied).

State: `## Auth` gained a status annotation, `## Billing` had a typo fixed, and `## Legacy Import` was deleted. `## Auth` has Tasks 1 and 2 (Finished, verified, `owner: claude`) and Task 3 (Pending). `## Billing` has Task 6 (Finished, verified). Task 9 (Pending, `owner: claude`) has `spec_section: "## Legacy Import"`. No deferrals.

1. Step 1b: `drifted` holds `## Auth` (Tasks 1 and 2 Finished, Task 3 Pending) and `## Billing` (Task 6 Finished); `missing` holds `## Legacy Import` (Task 9, Pending); `unreconciled_sections: 3`.
2. Two changed sections are unreconciled, so the batch prompt appears. `## Auth` has an open task (Task 3), so it carries the marker. Missing sections are never in the batch:
   ```
   2 spec sections changed since their tasks were built:
     ## Auth — 2 Finished, 1 Pending (has open tasks — reviewed separately)
     ## Billing — 1 Finished
   [E] Go through each section | [K] Keep all (the edits don't change what was built)
   ```
3. The user picks `[K]`, which keeps only `## Billing`, whose drifted tasks are all Finished. Task 6 gets the current `spec_fingerprint` and `section_fingerprint` (and `subsection_fingerprint` where present). Status, `task_verification` and `user_review_pending` are untouched. It gains the note `[DRIFT KEPT 2026-10-04] ## Billing changed; user kept verification: {one-line reason}`.
4. `## Auth` goes through its own section prompt anyway. Claude recommends `[K]` (status annotation only) and the user picks it: Tasks 1, 2 and 3 get current fingerprints and `[DRIFT KEPT …]` notes, with status and verification untouched. Task 3 stays Pending.
5. Separately, `## Legacy Import` goes through the per-task missing-section prompt for Task 9: `[D]` Delete / `[O]` Keep as out-of-spec / `[R]` Reassign. The user reassigns it to `## Auth`, so it now references that section with current fingerprints.
6. Task files changed, so the dashboard is regenerated (Tier-1 trigger "drift reconciliation applied"). Only fingerprints, notes and one `spec_section` changed, so `task_hash` is identical and Step 1a would not have caught it. The drift check now returns `drifted: []`, `missing: []` and `unreconciled_sections: 0`. The footer reads `spec aligned · 0 drift deferrals, 0 verification debt`, the Spec Drift sub-section is gone, and META shows `drift_sections: 0`.

**Expected:** `[K] Keep all` keeps the all-Finished section without a further prompt. The section with an open task gets its own prompt, because an open task may need its text updated before it's built. Each kept verification is recorded on its task. The deleted heading is handled per task, never inside the batch. The dashboard drops the drift rows right away.

**Pass criteria:** the batch prompt appears because 2+ changed sections are unreconciled, lists task counts by status, marks the section with an open task `(has open tasks — reviewed separately)`, and offers only `[E]` and `[K]` (no defer-all); `[K]` keeps only the unmarked section, refreshing fingerprints and noting each of its tasks without changing status or verification; the marked section still gets the per-section prompt; the missing section stays out of the batch; the dashboard is regenerated although `task_hash` didn't change.

## Trace E — `[V]` on a Finished claude-owned task and a Finished human-owned task

Command path: `drift-reconciliation.md § "Granular Reconciliation UI"` (`[V]`) → `commands/work.md § "If Verifying (Per-Task)"` → `agents/verify-agent.md` Step T2b → `work-procedures.md` "After verify-agent returns (per-task mode)".

State: one acceptance threshold in `## Reports` was reworded, and the spec edit is still uncommitted. Task 10 is Finished, `owner: claude`, with `task_verification.result: "pass"`, `verification_attempts: 2` and two `verification_history` entries (a fail, then a pass); its implementation was committed weeks ago. Task 11 is Finished, `owner: human`, with a self-attested `task_verification`. Only `## Reports` changed, so there is no batch prompt.

1. The prompt opens `Section "## Reports" changed — 2 Finished task(s).` and recommends `[V]`: the acceptance text changed. The user picks `[V]`.
2. Both tasks get current fingerprints and the note `[DRIFT RE-VERIFY 2026-10-04] ## Reports changed; re-verifying against the current text`.
3. Task 10 (`owner: claude`): status → Awaiting Verification, `task_verification` cleared, `verification_attempts` 2 → 0, and `drift_reverify: {"section": "## Reports", "date": "2026-10-04"}` set. `verification_history` keeps both entries. Normal routing then dispatches verify-agent (Awaiting Verification has priority); the task carries `drift_reverify`, so the brief adds `Re-verification after a spec edit: the implementation is unchanged; check it against the current section text.`
4. verify-agent, at Step T2b, skips the diff-based undeclared-file check: `git diff` holds only the uncommitted `.claude/spec_v3.md` edit, which would otherwise read as an undeclared change. It sets `scope_validation: "pass"` with the note "re-verification: no implementation diff" and judges the artifacts in Task 10's `files_affected` against the current `## Reports` text.
   - Pass → Finished with a new `task_verification` and `verification_attempts: 1`; the attempt is appended to `verification_history` after the two earlier entries; `drift_reverify` is removed.
   - Fail → the normal fail path (`task-schema.md § "Failure Handling"`), counted from 0: the task returns to In Progress at attempt 1 with `[VERIFICATION FAIL #1]` and is not escalated. `drift_reverify` is removed, so the fix is verified against its real diff. Without the reset, this fail would be attempt 3, and the task would go straight to Blocked with `[VERIFICATION ESCALATED]` and no fix cycle.
   - Two invalid returns → Blocked with `[VERIFICATION TIMEOUT]`. No result was written, so `drift_reverify` stays, and session recovery's retry (`session-recovery.md`, Case 2) sends the re-verification line again.
5. Task 11 (`owner: human`): stays Finished with `user_review_pending: true`. No verify-agent is dispatched. The Needs-you card lists it under Your Tasks until `/work complete 11` closes the review.
6. Task files changed, so the dashboard is regenerated (drift reconciliation applied).

**Expected:** nothing is rebuilt. Task 10's shipped work is checked against the new text by a fresh verify-agent that knows there is no implementation diff, with a fresh attempt count, and Task 11 goes back to its owner for review.

**Pass criteria:** neither task is reset to Pending; the claude-owned task goes to Awaiting Verification with `verification_attempts` reset to 0, `drift_reverify` set and history kept; every dispatch for it, retries included, carries the re-verification line; verify-agent passes scope validation with "re-verification: no implementation diff" rather than failing the uncommitted spec edit as undeclared; a failed re-verification takes the normal fail path at attempt 1, not escalated; `drift_reverify` is removed once a result is written, pass or fail; the human-owned task stays Finished with the review flag and no verify-agent dispatch; Task 10 is Finished again only after passing against the current text, and Task 11's earlier self-attestation stands only behind the open review.

## Trace F — quiet rules: who is never prompted

Command path: `scripts/fingerprint.py --drift .claude` (per-task rule order; the prose fallback in `drift-reconciliation.md` gives the same result).

State: the current spec is `spec_v3`. `## Auth` changed since decomposition: the edit is inside its `### Password rules` subsection, and its `### Session timeout` subsection is untouched. Each of those `### ` headings occurs once in the spec. `## Old Login` was deleted. The tasks (rule numbers as amended: 1 includes `out_of_spec`, 4(a) `## ` match, 4(b) unique `### ` match, 4(c) no match):

| Task | Status | Provenance | Rule | Result |
|---|---|---|---|---|
| 12 | Absorbed (into 2) | `## Auth`, old fingerprint | 1 | skipped, counted nowhere |
| 13 | Broken Down (13a, 13b) | `## Auth`, old fingerprint | 1 | skipped, counted nowhere |
| 13a | Finished | `## Auth` (copied by `/breakdown`), old fingerprint | 4(a), 6 | `drifted` |
| 13b | Pending | `## Auth` (copied by `/breakdown`), old fingerprint | 4(a), 6 | `drifted` |
| 14 | Finished | `spec_version: "spec_v2"`, `## Auth` | 2 | `historical` |
| 15 | Pending | `spec_version: "spec_v2"` | 2 | `unmigrated` |
| 16 | Pending | no `section_fingerprint` (created ad hoc before v5.13.0) | 3 | `no_provenance` |
| 17 | Finished | `## Old Login` | 4(c) | `unmatched` |
| 18 | Pending | `## Old Login` | 4(c) | `missing` |
| 19 | Finished | `spec_section: " Auth "` (no `## `, stray spaces), old fingerprint | 4(a), 6 | matches `## Auth` → `drifted` |
| 20 | Finished | `spec_section: "### Session timeout"`, that subsection's hash | 4(b), 5 | in sync, not reported |
| 21 | Finished | `spec_section: "### Password rules"`, that subsection's old hash | 4(b), 6 | `drifted` under `### Password rules` |
| 22 | Pending, `out_of_spec: true` (kept with `[O]` earlier) | `## Old Login`, old fingerprint | 1 | skipped, counted nowhere |
| 23 | Pending | `spec_unmapped: true`, no `spec_section` (a repo-wide lint sweep) | 3 | `unmapped` |
| `archive/task-3.json` | Finished | `## Auth`, old fingerprint | — | not scanned |

1. Output (excerpt; `spec_fingerprint`, the section `fingerprint`, and each task's `title`, `owner`, `deferred` and `subsection_unchanged` omitted):
   ```json
   {
     "spec": "spec_v3",
     "checked": 5,
     "drifted": [{"section": "## Auth", "deferred": false,
                  "tasks": [{"id": "13a", "status": "Finished"},
                            {"id": "13b", "status": "Pending"},
                            {"id": "19", "status": "Finished"}]},
                 {"section": "### Password rules", "deferred": false,
                  "tasks": [{"id": "21", "status": "Finished"}]}],
     "missing": [{"section": "## Old Login", "tasks": [{"id": "18", "status": "Pending"}]}],
     "unmigrated": ["15"],
     "historical": 1,
     "unmatched": 1,
     "no_provenance": 1,
     "unmapped": 1,
     "unreadable": [],
     "unreconciled_sections": 3
   }
   ```
2. Dashboard: three Spec Drift rows, `## Auth changed since its tasks were built (2 Finished, 1 Pending) → run /work to reconcile`, `### Password rules changed since its tasks were built (1 Finished) → run /work to reconcile` and `## Old Login is no longer in the spec (1 open task(s) reference it) → run /work to reconcile`. Footer `⚠️ 3 changed spec section(s), 0 drift deferrals, 0 verification debt`.
3. `/work`: Task 15 goes through Task Migration. Two changed sections are unreconciled, so the batch prompt lists `## Auth — 2 Finished, 1 Pending (has open tasks — reviewed separately)` and `### Password rules — 1 Finished`; `[K]` Keep all would keep only `### Password rules`. Task 18 gets the `[D]`/`[O]`/`[R]` prompt outside the batch. Tasks 12, 13, 14, 16, 17, 20, 22 and 23 never appear in a prompt.

Variant: if `### Session timeout` also appeared under another `## ` section, Task 20 would take the no-match branch (Finished → `unmatched`), the same as a `### ` heading that no longer exists.

**Expected:** only drifted and missing entries reach the user. Everything else is counted or skipped, so a project with historical, ad hoc or free-form provenance isn't prompted about it every session. A task whose provenance is the subsection itself (Task 20) isn't reported while that subsection is unchanged, even though its `## ` section changed; unlike DEC-021 narrowing, it isn't listed as "likely unaffected" either.

**Pass criteria:** Absorbed, Broken Down and out-of-spec tasks are skipped and counted nowhere, while a Broken Down task's subtasks are checked; an out-of-spec task stays quiet although its heading is gone (Task 22); a Finished task from an older spec version counts as `historical` and isn't flagged; a task without provenance is counted in `no_provenance`, never flagged (`/health-check` check 11 offers the baseline that gives it provenance; Scenario 51), and one that declares `spec_unmapped: true` is counted in `unmapped` instead; the same deleted heading gives `unmatched` for a Finished task and `missing` for a Pending one; heading matching ignores surrounding whitespace and a missing `## `; a `spec_section` naming a `### ` heading that occurs once is compared with that subsection's hash, staying quiet while it's unchanged (Task 20) and reported under the `### ` heading, with `subsection_unchanged: false`, when it changed (Task 21); `archive/` isn't scanned.

## Invariant checks

- Detection never reads dashboard META. META `spec_fingerprint` records which spec the dashboard was rendered from (Step 1a regenerates when it differs); it is not evidence that drift was checked.
- The check is read-only. `fingerprint.py --drift` writes nothing; the orchestrator makes every state change.
- `/work` and the renderer share one implementation (`compute_drift()`). If the renderer can't load it, the footer reads `drift unchecked · {d} drift deferrals, {k} verification debt` and the rest of the dashboard renders.
- Every pick except `[S]`, `[O]` and `[D]` refreshes `spec_fingerprint`, `section_fingerprint` and, when present, `subsection_fingerprint`. `[S]` records a deferral under the unchanged drift budget.
- `[A]` and `[V]` reset `verification_attempts` to 0 on the Finished tasks they send back to rebuild or re-verification (`verification_history` keeps the earlier record), and update open tasks in place with a `[DRIFT UPDATED …]` note.
- Claude recommends one option per section and never applies one without the user's pick.
- No Finished task carries a verification result computed against a different section text than its current fingerprints, unless the user chose `[K]`, which its notes record. (A human-owned task under `[V]` is covered by its open review; Trace E.)
- A missing snapshot doesn't affect detection; the prompt shows the current section text instead of a diff.
- Diffs still come from the decomposition snapshot, so after a `[K]` later diffs show changes since decomposition, not since the keep.
