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
- Parallel or heavy re-dispatch in the same session without explicit user confirmation
- FB-103's implement-agent recovery steps applied (e.g. a fresh implement-agent dispatched to re-confirm the work)
