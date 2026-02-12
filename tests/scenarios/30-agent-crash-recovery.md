# Scenario 30: Agent Crash and Timeout Recovery

Verify that `/work` correctly handles agent failures — both implement-agent and verify-agent — including timeouts, unexpected exits, and partial work.

## Context

Agents run as separate Task invocations with `max_turns` limits. When an agent crashes, times out, or exits without producing expected artifacts, `/work` must leave the project in a recoverable state. The user should never need to manually inspect task JSON to figure out what went wrong.

## State

- Phase 1: 3 tasks
  - Task 1: "Build authentication module" (status: "In Progress", owner: "claude")
  - Task 2: "Add rate limiting" (status: "Pending", depends on [1])
  - Task 3: "Write API docs" (status: "Pending", no dependencies)
- implement-agent dispatched for Task 1, currently mid-execution

---

## Trace 30A: Implement-agent times out (parallel)

- **Path:** work.md Step 4 § "If Executing (Parallel)" → one agent reaches `max_turns: 40` without completing

### Scenario

Tasks 1 and 3 dispatched in parallel (no file conflicts, no dependencies between them). Task 1's agent reaches the turn limit while still implementing — Step 6b (verify-agent spawn) was never reached. Files have been partially modified. Task 3's agent completes successfully.

### Note on sequential mode

In sequential mode, implement-agent runs inline in the `/work` conversation (not as a spawned Task agent), so there is no `max_turns` limit. Timeout is only relevant for parallel agents (spawned with `max_turns: 40`) and verify-agents (spawned with `max_turns: 30`). This trace tests the parallel case.

### Expected

1. Polling loop detects Task 1's agent exited without completion signal (60 poll iterations)
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

## Trace 30B: Verify-agent times out (sequential)

- **Path:** work.md Step 4 § "If Verifying (Per-Task)" → verify-agent reaches `max_turns: 30`; work.md Step 0 Case 2 (recovery on next run); verify-agent.md § "Timeout Handling"

### Scenario

implement-agent completed successfully for Task 1. verify-agent was spawned but exhausted its turn limit without writing `verification-result.json`.

### Expected

1. `/work` detects missing verification result after agent exits
2. Task 1 treated as verification failure
3. Task 1 status set to "Blocked"
4. Note added: `[VERIFICATION TIMEOUT]`
5. `verification_attempts` incremented
6. User informed: verification timed out, suggest retrying or running `/health-check`

### Pass criteria

- [ ] Missing verification result treated as failure, not success
- [ ] `verification_attempts` counter incremented
- [ ] Task status set to "Blocked" with `[VERIFICATION TIMEOUT]` note
- [ ] If `verification_attempts < 3`, next `/work` run can retry verification
- [ ] If `verification_attempts >= 3`, escalated to user review

### Fail indicators

- Task marked "Finished" because implement-agent completed (verification skipped)
- `verification_attempts` not incremented (retry limit never triggers)
- No distinction between verification failure and verification timeout in notes

---

## Trace 30C: Parallel agent crash — one of three agents fails

- **Path:** work.md Step 4 § "If Executing (Parallel)" → polling loop

### Scenario

Tasks 1, 3, and a new Task 4 dispatched in parallel. Task 1's agent crashes (exits without completing). Tasks 3 and 4 complete successfully.

### Expected

1. Polling loop detects Task 1's agent exited without completion signal
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
- Failed task silently re-dispatched in the same polling cycle

---

## Trace 30D: Agent produces partial work — files modified but task incomplete

- **Path:** work.md Step 4 → implement-agent.md § "Handling Issues"

### Scenario

implement-agent for Task 1 created 2 of 3 required files, then hit a blocking issue (e.g., discovered a missing dependency). Agent correctly set status to "Blocked" and documented the blocker per implement-agent.md § "Handling Issues" — but files are in a half-done state.

### Expected

1. Task 1 status: "Blocked" (set by agent)
2. Task 1 notes contain the blocker description
3. Question added to `questions.md` with date prefix
4. Partial files remain on disk (not reverted — they represent real work)
5. Dashboard attention section shows: blocked task, blocker reason, link to questions.md
6. Next `/work` run does NOT re-dispatch Task 1 until blocker resolved

### Pass criteria

- [ ] Blocker documented in task notes AND questions.md
- [ ] Partial work preserved (not silently deleted)
- [ ] Dashboard surfaces the blocker with enough context to act on it
- [ ] `/work` routing skips Blocked tasks

### Fail indicators

- Partial files deleted or reverted without user consent
- Blocker only recorded in task notes, not surfaced in dashboard
- `/work` re-dispatches Task 1 while still Blocked
- Agent exits without documenting what went wrong
