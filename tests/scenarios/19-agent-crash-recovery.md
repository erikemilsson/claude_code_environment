# Scenario 19: Agent Crash and Timeout Recovery

Verify that `/work` correctly handles agent failures — both implement-agent and verify-agent — including timeouts, unexpected exits, and partial work.

## Context

Agents run as separate `Agent` invocations with turn budgets stated in their dispatch prompts. When an agent crashes, times out, or exits without producing expected artifacts, `/work` must leave the project in a recoverable state. The user should never need to manually inspect task JSON to figure out what went wrong.

## State

- Phase 1: 3 tasks
  - Task 1: "Build authentication module" (status: "In Progress", owner: "claude")
  - Task 2: "Add rate limiting" (status: "Pending", depends on [1])
  - Task 3: "Write API docs" (status: "Pending", no dependencies)
- implement-agent dispatched for Task 1, currently mid-execution

---

## Trace 19A: Implement-agent times out (parallel)

- **Path:** /work parallel execution

### Scenario

Tasks 1 and 3 dispatched in parallel (no file conflicts, no dependencies between them). Task 1's agent runs past its turn budget and ends without a report while still implementing — verification was never reached. Files have been partially modified. Task 3's agent completes successfully. Timeout is relevant for parallel agents and verify-agents, whose prompts state a turn budget; sequential mode dispatches implement-agent without one (small tasks may run inline, per `rules/agents.md § "Dispatch Invariants vs Efficiency Defaults"`).

### Expected

1. Collection loop receives Task 1's notification: the agent ended without a report
2. Task 1 status set to "Blocked"
3. Task 1 notes updated: `[AGENT TIMEOUT]`
4. Task 3 completes normally — its results are processed independently
5. Dashboard regenerated showing Task 1 as Blocked, Task 3 as Finished
6. User informed with specific guidance: which task timed out, what to check

### Pass criteria

- [ ] Task 1 status transitions to "Blocked", not left as "In Progress"
- [ ] Timeout note added to task JSON with `[AGENT TIMEOUT]` prefix
- [ ] Task 3's successful completion is not affected by Task 1's failure
- [ ] Dependent tasks (Task 2) remain Pending, not dispatched
- [ ] User gets actionable guidance (not just "an error occurred")

### Fail indicators

- Task 1 left as "In Progress" with no indication of failure
- Entire parallel batch aborted because one agent timed out
- Task 3's results lost or ignored due to Task 1's failure
- Task 2 dispatched despite Task 1 not completing

---

## Trace 19B: Verify-agent times out (sequential)

- **Path:** /work session recovery, verify-agent timeout handling

### Scenario

implement-agent completed successfully for Task 1. verify-agent was spawned and returned prose instead of the report schema; asked once for the report, it again returned no valid report.

### Expected

1. `/work` detects the missing report and asks verify-agent once for it, without incrementing `verification_attempts`
2. The second invalid return is treated as verification failure
3. Task 1 status set to "Blocked"
4. Note added: `[VERIFICATION TIMEOUT]`
5. `verification_attempts` incremented
6. User informed: verification timed out, suggest retrying or running `/health-check`

### Pass criteria

- [ ] First invalid return re-requested once, not counted as an attempt
- [ ] Missing verification result treated as failure, not success
- [ ] `verification_attempts` counter incremented
- [ ] Task status set to "Blocked" with `[VERIFICATION TIMEOUT]` note
- [ ] If `verification_attempts < 3`, next `/work` run can retry verification
- [ ] If `verification_attempts >= 3`, escalated to user review

### Fail indicators

- Task marked "Finished" because implement-agent completed (verification skipped)
- `verification_attempts` not incremented (retry limit never triggers)
- First invalid return treated as a timeout (burns an attempt on a formatting slip)
- No distinction between verification failure and verification timeout in notes

---

## Trace 19C: Parallel agent crash — one of three agents fails

- **Path:** /work parallel execution

### Scenario

Tasks 1, 3, and a new Task 4 dispatched in parallel. Task 1's agent fails (ends without a report; no usage limit, API or harness error). Tasks 3 and 4 complete successfully.

### Expected

1. Collection loop receives Task 1's failure notification: the agent ended without a report
2. Task 1 set to "Blocked" with `[AGENT TIMEOUT]` note
3. Tasks 3 and 4 proceed normally — their results are processed
4. After batch completes: dashboard regenerated showing mixed results
5. Task 2 (depends on Task 1) remains Pending
6. Next `/work` run surfaces Task 1 as needing attention

### Pass criteria

- [ ] One agent's failure does not abort the entire parallel batch
- [ ] Successfully completed tasks are processed normally (status "Finished" if verification passed)
- [ ] Failed task is clearly marked with failure reason
- [ ] Dashboard shows mixed batch results: some completed, one blocked
- [ ] Incremental re-dispatch does NOT re-dispatch the failed task automatically

### Fail indicators

- Entire batch aborted because one agent failed
- Failed task's status is ambiguous (still "In Progress")
- Successfully completed tasks' results lost or ignored
- Failed task silently re-dispatched within the same collection loop

---

## Trace 19D: Agent produces partial work — files modified but task incomplete

- **Path:** implement-agent issue handling

### Scenario

implement-agent for Task 1 created 2 of 3 required files, then hit a blocking issue (e.g., discovered a missing dependency). Agent correctly set status to "Blocked" and documented the blocker — but files are in a half-done state.

### Expected

1. Task 1 status: "Blocked" (set by agent)
2. Task 1 notes contain the blocker description
3. Blocker flagged for human clarification (asked directly via conversation)
4. Partial files remain on disk (not reverted — they represent real work)
5. Dashboard attention section shows: blocked task, blocker reason
6. Next `/work` run does NOT re-dispatch Task 1 until blocker resolved

### Pass criteria

- [ ] Blocker documented in task notes
- [ ] Partial work preserved (not silently deleted)
- [ ] Dashboard surfaces the blocker with enough context to act on it
- [ ] `/work` routing skips Blocked tasks

### Fail indicators

- Partial files deleted or reverted without user consent
- Blocker only recorded in task notes, not surfaced in dashboard
- `/work` re-dispatches Task 1 while still Blocked
- Agent exits without documenting what went wrong

---

## Trace 19E: Verify-agent killed by a usage limit (sequential)

- **Path:** /work verify-agent timeout handling — infrastructure-termination exclusion (FB-120)

### Scenario

implement-agent completed successfully for Task 1 (`verification_attempts: 0`). verify-agent was spawned, and a platform usage limit killed it after 4 tool calls: a zero-token return (or an HTTP 429 error) with no report. Contrast with 19B, where the verifier twice returned no valid report.

### Expected

1. `/work` classifies the return as an infrastructure termination, not a timeout
2. `verification_attempts` stays 0; no `task_verification` written
3. Task 1 stays "Awaiting Verification", with no `[VERIFICATION TIMEOUT]` note
4. User told verification was interrupted; the FB-103 post-limit dispatch rule applies
5. A fresh verify-agent runs once the limit clears (Step 3 routes Awaiting Verification first)

### Pass criteria

- [ ] `verification_attempts` not incremented
- [ ] Task status stays "Awaiting Verification" (not "Blocked")
- [ ] No `[VERIFICATION TIMEOUT]` note and no partial `task_verification`
- [ ] Interruption surfaced to the user

### Fail indicators

- Treated as a timeout: attempts incremented, task Blocked with `[VERIFICATION TIMEOUT]` (burns one of three attempts on an outage)
- The cut-off verification, or a parallel batch, dispatched in the same session without the user's go-ahead (post-limit dispatch rule, `parallel-execution.md § "Pre-Dispatch Confirmation"`)
- FB-103's implement-agent recovery steps applied (e.g. a fresh implement-agent dispatched to re-confirm the work)

---

## Trace 19F: Session cut off after an earlier clean exit — the open sentinel forces the full scan

- **Path:** `commands/work.md § "Before Any Dispatch"` (open sentinel) → next session, `/work` Step 0b → `session-recovery.md`

### Scenario

At 09:10 a `/work` run ended cleanly and wrote `.claude/tasks/.last-clean-exit.json`. At 14:00 the same day a new session runs `/work`: at its first dispatch (implement-agent for Task 1) it writes the sentinel again with `"open": true`, the other keys kept. The terminal is closed while the agent is running: no pause, no clean exit. Task 1 is "In Progress" on disk and a dev server the agent started is still listening. At 15:30 a third session runs `/work`.

### Expected

1. Step 0b reads the sentinel: its timestamp is 90 minutes old, inside the 24-hour window, but it has `"open": true`
2. An open sentinel is not a clean exit, whatever its timestamp: the full recovery scan runs
3. The scan finds Task 1 "In Progress". Case 6 applies although its `updated_date` is today, because the sentinel is open
4. "Residue From a Previous Session" runs with the scan, before anything is dispatched, and reports the listener
5. One prompt for Task 1: it has been In Progress since a session that did not end cleanly, with the line that it was updated today and an agent or another session may still be working on it; `[C]` Continue, `[P]` Reset to Pending, `[H]` Put On Hold, `[L]` Leave
6. The user answers `[C]`: Task 1 stays "In Progress", `[CONTINUE {today}]` is prepended to its notes, and Step 3 routes it to implement-agent ("Continued from recovery"), with its notes and the state of its files in the brief
7. When this session ends cleanly or pauses, the sentinel is written closed

Variant, pause then more work: the 14:00 session runs `/work pause` (sentinel written closed), then keeps working in the same conversation. Its first dispatch after the pause writes `"open": true` again, so a cutoff after that point is also caught.

Variant, no dispatch: a `/work` run that dispatches nothing (a fast exit, nothing eligible) never writes `"open": true`. It still reaches Step 5, which writes the sentinel closed with a new timestamp.

Variant, the user leaves it: the 14:00 session is in fact still running in another terminal, its agent at work on Task 1. The user answers `[L]`. Nothing is written to Task 1 and nothing is dispatched for it; the run goes on with other work (Task 3) or, with nothing else dispatchable, says Task 1 is In Progress elsewhere. Step 5 writes the sentinel with `"open": true`, so this session does not close the sentinel of the one that still has an agent out. The same answer for a task whose notes begin with `[CONTINUE` from an earlier run also keeps it from being routed.

Variant, left with a closed sentinel: the sentinel is closed and three days old, and Task 1 has been In Progress for three days (case 6's over-24h arm). The user answers `[L]`. Step 5 writes the sentinel with `"open": true` although it was closed, so the next `/work` runs the full scan and asks about Task 1 again, however soon it runs.

Variant, continued tasks and a compaction: two tasks were stranded and the user answered `[C]` for both. Task 1 is dispatched, with `[RE-DISPATCHED {today}]` prepended to its notes in the write that precedes the dispatch, and the conversation is compacted while its agent is still running. Step 3 reads the task files: the second task's notes still begin with `[CONTINUE {today}]`, so it is routed; Task 1's begin with `[RE-DISPATCHED`, so it is not routed a second time, and would not be after a `misaligned` or zero-token return either. Weeks later Task 1, long Finished, is reopened to In Progress: its old `[CONTINUE]` note is no longer first in `notes` and routes nothing.

Variant, a human task: Task 5 (`owner: human`) is also In Progress. Case 6 does not ask about it, open sentinel or not.

Variant, a sub-mode first: at 15:30 the user runs `/work complete` for another task instead of `/work`, and that task needs a verify-agent. A sub-mode skips Step 0b. "Before Any Dispatch" reads the sentinel, finds it already open, and marks it again. At Step 5 the sentinel was open when this conversation first read it and no Step 0b has run, so it is written with `"open": true` kept. The next plain `/work` still runs the full scan and asks about Task 1.

Variant, same task with a closed sentinel: the 14:00 session ran `/work pause` while Task 1 was In Progress, and the 15:30 session finds the sentinel closed and 90 minutes old. Fast path; case 6 does not fire (a normal pause, under 24 hours).

### Pass criteria

- [ ] The sentinel has `"open": true` from the first dispatch until the session's clean exit or pause
- [ ] A sentinel with `"open": true` leads to the full scan even though its timestamp is recent
- [ ] Task 1 is asked about in one prompt, on the day it was stranded, and the leftover listener is reported
- [ ] After `[C]`, an implement-agent is dispatched for Task 1 in this run
- [ ] A clean exit or pause leaves the sentinel without `open` (or with `"open": false`)
- [ ] A dispatch after a mid-session pause opens the sentinel again
- [ ] A sub-mode run before any scan leaves an open sentinel open, even when it dispatched a verifier of its own
- [ ] `[L]` writes nothing to the task, dispatches nothing for it, and the sentinel is written open, whether it was open, closed, missing or stale
- [ ] A `[C]` choice is on the task (`[CONTINUE {date}]` first in `notes`) and is acted on after a compaction
- [ ] No prompt for an `owner: human` task

### Fail indicators

- Fast path taken because the sentinel is under 24 hours old (the pre-v5.14.1 behaviour: the 09:10 clean exit hid the 14:00 cutoff)
- Task 1 left In Progress with no prompt because its `updated_date` is under 24 hours old
- `[C]` chosen and nothing dispatched for Task 1 (Step 3's algorithm picks only Pending tasks)
- `"open": true` written at session start, before any dispatch, or a mark that drops the sentinel's other keys (marking again before a later dispatch is harmless)
- The sentinel deleted to mark the session open
- `/work pause` or a clean exit leaving `"open": true` behind in the session that marked it
- `/work complete` in a fresh session closing a sentinel that another session left open, because its own dispatch "marked" it
- A long `/work` session that was compacted and then paused leaving the sentinel open (it ran Step 0b: closed)
- `[L]` followed by a closed sentinel, or by a status or notes write to the left task
- A task routed by a `[CONTINUE]` note that is no longer first in its notes, or routed after `[L]` in the same run
- A continued task dispatched with `[CONTINUE]` still first in its notes
- `[C]` offered for an `owner: human` task and an implement-agent sent to do the user's work
- A paused task under 24 hours old asked about when the sentinel is closed

---

## Trace 19G: A verifier resumed for a delta re-check ends without a report (parallel)

- **Path:** `parallel-execution.md § "Parallel Dispatch"` step 4, failure branch → `work-procedures.md` "Post-verify delta" step 5

### Scenario

In a parallel batch, Task 3 passed per-task verification and a one-line fix to it went back to the same verifier as a delta re-check that uses the browser: the verifier is in `active_verifiers` marked `delta` and `exclusive`, Task 3 is "Awaiting Verification", and Task 4's exclusive verification is waiting in `exclusive_verify_queue`. The resumed verifier's notification reports a failure with no report, and no usage limit, API or harness error.

### Expected

1. The Residue check runs for it first
2. The delta rule applies in place of the timeout rule: no second ask, no `[VERIFICATION TIMEOUT]`, Task 3 is not Blocked, and nothing is appended to `verification_history[]` for the lost reply
3. Task 3 needs a fresh verify-agent, starting from `verification_attempts: 0`. Its verification is exclusive, so it joins the tail of the queue as a `verify` entry, behind Task 4
4. The verifier is removed from `active_verifiers`, the user is told, and the head of the queue is run: Task 4's verify-agent. Task 3's follows when that one ends

Variant, a usage limit killed it: an interruption. Task 3 stays "Awaiting Verification", nothing is counted, and the post-limit dispatch rule holds the queue (Task 4 included) for the user's go-ahead.

### Pass criteria

- [ ] Task 3 is "Awaiting Verification" throughout, never Blocked
- [ ] No `[VERIFICATION TIMEOUT]` note and no history entry for the lost delta reply
- [ ] The queue moves on: Task 4's verify-agent is dispatched after the failure is processed
- [ ] At no moment are two exclusive jobs running

### Fail indicators

- The delta's failure handled as case 2 of the failure branch: asked again, then `[VERIFICATION TIMEOUT]` and Blocked, with an attempt counted
- Task 4 left queued with nothing running (the failure of a `delta` entry not treated as the end of an exclusive job)
- Task 3's fresh verify-agent dispatched at once, and then Task 4's as the head of the queue, both driving the browser
- Task 3 set back to Finished because "it had already passed"
