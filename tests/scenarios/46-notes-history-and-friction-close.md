# Scenario 46 — Task notes keep their history; a fixing task closes its friction entries (FB-134 b, e)

Conceptual trace test for v5.10.0. Task `notes` are newest first: every write prepends to the existing notes and none replaces them, so a re-implementation after a verification fail keeps the `[VERIFICATION FAIL #N]` trail the verifier reads, and session recovery reads a task's state from its newest state tag. A new optional task field, `resolves_friction`, lists the friction-register entries a task was created to fix; when the task is Finished with no user review pending, `/work` closes the ones still open with `resolved_by.kind: "task"`.

## Setup / State

- Prepend means `notes` becomes `new_text + " " + notes`, or just `new_text` when `notes` is empty (`work-procedures.md § "State Persistence Protocol"`). Every `notes` write does this, drift notes and `/breakdown`'s note included.
- `.claude/support/friction.jsonl` holds three entries (other fields omitted):
  ```
  {"id": "FR-012", "kind": "path_drift", "source_anchor": "spec_v2.md § Export", "status": "open"}
  {"id": "FR-013", "kind": "vocab_drift", "source_anchor": "spec_v2.md § Reports", "status": "resolved", "resolved_by": {"kind": "iterate", "ref": "spec_v2", "at": "2026-09-30T10:00:00Z"}}
  {"id": "FR-014", "kind": "terminology_mismatch", "source_anchor": "docs/guide.md", "status": "open", "captured_in": {"agent": "verify-agent", "task": "33", "command": "/work"}}
  ```
  There is no FR-099.
- Each trace starts from this state and lists the tasks it relies on.

## Trace A — fail → re-implement → pass keeps the trail

Command path: `commands/work.md § "If Verifying (Per-Task)"` → `work-procedures.md § "State Persistence Protocol"`: "After verify-agent returns (per-task mode)" step 4 (`fail`), "After implement-agent returns" step 1 (`completed`), then step 4 (`pass`).

State: Task 30 "Add CSV export" (`owner: claude`, Awaiting Verification, `verification_attempts: 0`, no `resolves_friction`), `notes: "Added CSV export for the orders table."`.

1. verify-agent returns `fail`: the header row is missing. The orchestrator sets `verification_attempts: 1`, status In Progress, clears `completion_date`, and prepends the fail note: `notes` = `[VERIFICATION FAIL #1] Header row missing from the CSV. Added CSV export for the orders table.`
2. `/work` routes Task 30 to implement-agent, which reads the `[VERIFICATION FAIL #1]` note, adds the header row and returns `completed` with `notes: "Added the header row. Ran tests/test_export.py: pass."`.
3. The orchestrator writes `status: "Awaiting Verification"`, `completion_date` and `updated_date`, and prepends the report's notes: `notes` = `Added the header row. Ran tests/test_export.py: pass. [VERIFICATION FAIL #1] Header row missing from the CSV. Added CSV export for the orders table.`
4. verify-agent reads those notes, the earlier fail included, and returns `pass`. Task 30 → Finished; the pass doesn't touch `notes`. `verification_history` holds both attempts.

Variants (step 2 returns a different report, or a later write lands; `{report notes}` stands for the report's `notes`):
- `partial`: the report's notes are plain, e.g. `Header row half done.` (implement-agent's Wind-Down Protocol adds no tag). The orchestrator adds the tag once: `notes` = `[PARTIAL] Header row half done. [VERIFICATION FAIL #1] Header row missing …`. Status stays In Progress.
- `partial_resume_pending`: `partial_completion` is written, status stays In Progress; `notes` = `[PARTIAL_RESUME_PENDING] {report notes} [VERIFICATION FAIL #1] …`.
- `blocked`: status → Blocked; `notes` = `[BLOCKED] {report notes} [VERIFICATION FAIL #1] …`.
- Inline fix: the orchestrator does the small fix itself and prepends an `[INLINE]` note naming the files touched and checks run (`rules/agents.md § "Dispatch Invariants vs Efficiency Defaults"`); the trail stays the same way.
- Drift note: a later `[K]` Keep on the task's section prepends `[DRIFT KEPT 2026-10-05] …` ahead of everything else (`drift-reconciliation.md`).
- Empty notes: a task whose `notes` is `""` gets the new text alone, with no trailing space.

**Expected:** after every write, the earlier notes are still there under the new text, newest first, so the verifier of attempt 2 sees what attempt 1 failed on. Before v5.10.0, step 3 wrote `"notes": report.notes`, which erased the `[VERIFICATION FAIL #1]` entry.

**Pass criteria:** the writes in steps 1 and 3 and in every variant prepend, joined by one space; after the re-implementation, `notes` still holds the `[VERIFICATION FAIL #1]` entry and the original notes; a partial return carries exactly one `[PARTIAL]` tag; no write replaces `notes`; empty notes get the new text alone.

## Trace B — a fixing task passes: open entry closed, others skipped

Command path: `work-procedures.md § "State Persistence Protocol"` ("Friction entries a task fixes"; "After verify-agent returns (per-task mode)" step 4, `pass`) → `friction-register.md § "Status update protocol"`.

State: Task 31 "Fix the export path in spec and code" (`owner: claude`, Awaiting Verification), filed from an audit finding with `resolves_friction: ["FR-012", "FR-013", "FR-099"]`.

1. verify-agent returns `pass` with no `user_review_pending`. Task 31 → Finished.
2. No review is pending, so `/work` closes the task's entries through the Status update protocol (read the whole register, update by id, rewrite it atomically):
   - FR-012 is `open` → `status: "resolved"`, `resolved_by: {"kind": "task", "ref": "31", "at": "2026-10-05T14:20:00Z"}`.
   - FR-013 is already `resolved` → skipped; its `resolved_by` still names `iterate`.
   - FR-099 is not in the register → skipped; no line is added.
3. FR-014 isn't listed → stays `open`.

Variant, review pending: the pass carries `user_review_pending: true` (an `owner: both` task with a guided test). Task 31 is Finished with the review flag, and the register is untouched until `/work complete 31` (as in Trace C's variant).

Variant, fail: verify-agent returns `fail` instead. Task 31 goes back to In Progress and the register is untouched; FR-012 closes only when the task is Finished.

**Expected:** the register afterwards:
```
{"id": "FR-012", …, "status": "resolved", "resolved_by": {"kind": "task", "ref": "31", "at": "2026-10-05T14:20:00Z"}}
{"id": "FR-013", …, "status": "resolved", "resolved_by": {"kind": "iterate", "ref": "spec_v2", "at": "2026-09-30T10:00:00Z"}}
{"id": "FR-014", …, "status": "open", …}
```
The friction-register lens of the next `/audit-coherence` reads only `open` entries, so FR-012 no longer resurfaces.

**Pass criteria:** only the listed `open` entry changes; its `resolved_by` has `kind: "task"`, the task id as `ref` and an ISO timestamp as `at`; an already resolved (or dismissed) entry is left as it was; an id missing from the register is skipped without error and without a new line; unlisted entries are untouched; nothing closes on a fail or on a pass with a review pending.

## Trace C — `/work complete` prepends its notes and closes entries

Command path: `commands/work.md` (`/work complete` stub) → `work-procedures.md § "Task Completion (/work complete)"` steps 3, 3c and 5.

State: Task 32 "Rename the 'Reference surface' heading in the user guide" (`owner: human`, In Progress, no `task_verification`), `notes: "Waiting on the docs owner."`, `resolves_friction: ["FR-014"]`.

1. `/work complete 32`: step 3 auto-generates the `self_attested` verification (human task); step 3c stores the user's project notes in `user_feedback`.
2. Step 5 writes Finished, `completion_date` and `updated_date`, and prepends what was done: `notes` = `User renamed the heading in docs/guide.md. Waiting on the docs owner.`
3. Step 5 closes FR-014, which is `open`: `status: "resolved"`, `resolved_by: {"kind": "task", "ref": "32", "at": "<ISO timestamp>"}`.

Variant, review pending: Task 35 (`owner: both`, `resolves_friction: ["FR-012"]`) passed verification with `user_review_pending: true`, so the pass closed nothing and FR-012 is still `open`. The user finishes the guided test and runs `/work complete 35`: step 5 prepends its notes, clears `user_review_pending` and closes FR-012 with `ref: "35"`.

**Expected:** `/work complete` prepends its notes and closes the listed open entries, including those a review-pending pass left open.

**Pass criteria:** the step 5 notes write prepends and the earlier notes survive; FR-014 is closed with `kind: "task"` and `ref: "32"`; in the variant, FR-012 stays `open` after the pass and is closed by `/work complete 35` with `ref: "35"`.

## Trace D — a task without the field closes nothing

Command path: as Trace B.

State: Task 33 "Wire the export button" (`owner: claude`, Awaiting Verification, no `resolves_friction`). An earlier verify-agent report on it raised FR-014 (`captured_in.task: "33"`), and its notes mention `See FR-012.`.

1. verify-agent returns `pass`. Task 33 → Finished.
2. Task 33 has no `resolves_friction`, so the register isn't read or rewritten. FR-012 and FR-014 stay `open`, although Task 33 cites one and raised the other.

**Expected:** only an explicit `resolves_friction` closes entries. A citation in `notes`, or `captured_in.task`, never does.

**Pass criteria:** no `friction.jsonl` rewrite; FR-012 and FR-014 unchanged.

## Trace E — parent auto-completion closes the parent's entries

Command path: `commands/breakdown.md` step 3 → `work-procedures.md § "State Persistence Protocol"`: "After verify-agent returns (per-task mode)" steps 4 and 7. Variant: `§ "Task Completion (/work complete)"` step 6.

State: Task 34 "Rework the export module" was filed to fix FR-012 (`resolves_friction: ["FR-012"]`), `notes: "Filed from audit finding C-02."`, difficulty 8.

1. `/breakdown 34` creates 34_1 and 34_2 (subtasks don't copy `resolves_friction`) and prepends its note: Task 34 is Broken Down with `notes` = `Broken down into 2 subtasks. Filed from audit finding C-02.`
2. 34_1 is later Finished. verify-agent passes 34_2 with no review pending → Finished. 34_2 has no `resolves_friction`, so its own pass closes nothing.
3. Step 7: every subtask of Task 34 is now Finished, so Task 34 → Finished and its entries close: FR-012 → `status: "resolved"`, `resolved_by: {"kind": "task", "ref": "34", "at": "<ISO timestamp>"}`. FR-013 and FR-014 are untouched.

Variant, `/work complete`: 34_2 is `owner: human` and the user completes it with `/work complete 34_2`; step 6 sets Task 34 Finished and closes FR-012 the same way.

**Expected:** a broken-down fixing task closes its entries when it auto-completes, with its own id as `ref`. Without this path it never would: it isn't verified itself, and its subtasks don't carry the field.

**Pass criteria:** `/breakdown` prepends its note and keeps the parent's earlier notes; the subtask's pass closes nothing; parent auto-completion (step 7, or `/work complete` step 6) closes the parent's open entries with the parent's id as `ref`.

## Trace F — session recovery reads the newest state tag

Command path: `session-recovery.md § "Full Recovery Scan"` (newest state tag; Cases 2–5).

State: no `.last-clean-exit.json`, so the full scan runs. Three Blocked tasks, all `owner: claude`:
- Task 36 timed out in a parallel batch (`[AGENT TIMEOUT] Parallel agent ended without a report.`). At the next scan, Case 4 offered its options and the user picked `[R]` Retry (→ Pending). Re-dispatched, implement-agent returned `blocked`, so `notes` = `[BLOCKED] Needs the vendor API key in .env. [AGENT TIMEOUT] Parallel agent ended without a report. Added the export client.`
- Task 37: `verification_attempts: 1`; after its verification timed out, a `[K]` Keep on its section prepended a drift note: `notes` = `[DRIFT KEPT 2026-10-05] ## Export changed; user kept verification: wording only. [VERIFICATION TIMEOUT] No valid report after two asks. Added CSV export for the orders table.`
- Task 38: `verification_attempts: 3`, `notes` = `[VERIFICATION TIMEOUT] No valid report after two asks. Added the import screen.`

1. Task 36: reading from the start, the first state tag is `[BLOCKED]`, so none of Cases 2–5 match and no timeout prompt appears. The task stays Blocked on its real blocker. (Matching "notes containing `[AGENT TIMEOUT]`" would have offered Retry / Break down / Skip for a timeout that is no longer the problem.)
2. Task 37: `[DRIFT KEPT …]` isn't a state tag, so the newest state tag is `[VERIFICATION TIMEOUT]`, with attempts below 3 → Case 2: status → Awaiting Verification and verify-agent is dispatched with the extended turn budget. No note is cleared; the status change is enough. If the retry passes, Task 37 is Finished and the old timeout note stays as history.
3. Task 38: Case 3 prepends `[VERIFICATION ESCALATED] 3 verification attempts exhausted — requires human review`. At the next scan its newest state tag is `[VERIFICATION ESCALATED]` → Case 5, report only; Case 3 doesn't fire again.

**Expected:** each Blocked task is matched on its current state, read from its newest state tag; older tags further down are history.

**Pass criteria:** Task 36 gets no timeout prompt; tags that aren't state tags (`[DRIFT …]`, `[INLINE]`) and untagged text are skipped when finding the newest state tag; Case 2 clears no note; Case 3 prepends its note, so the next scan routes Task 38 to Case 5.

## Invariant checks

- Notes are newest first. No `notes` write replaces them: reports (`completed`, `partial`, `partial_resume_pending`, `blocked`), inline work, verification notes, drift notes, `/breakdown` and `/work complete` all prepend (`new_text + " " + notes`, or `new_text` alone when `notes` is empty).
- A `[VERIFICATION FAIL #N]` entry survives every later write, so each verification attempt can see the earlier failures.
- A partial return gets exactly one `[PARTIAL]` tag: implement-agent returns plain notes and the orchestrator adds the tag.
- Session recovery's Cases 2–5 match the newest state tag, never an older tag further down.
- Register entries close only when a task that lists them is Finished with no user review pending (a per-task pass without `user_review_pending`, `/work complete`, or parent auto-completion), never on a fail, `partial`, `blocked`, a review-pending pass or the move to Awaiting Verification.
- Closing is idempotent: only `open` entries change; `resolved` and `dismissed` entries keep their `resolved_by` or `dismiss_reason`; ids missing from the register add nothing.
- A task close always writes `status: "resolved"` with `resolved_by: {"kind": "task", "ref": "<task id>", "at": "<ISO timestamp>"}`.
