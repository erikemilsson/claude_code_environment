# Scenario 30: Handoff During Parallel Batch

Verify that context transitions work correctly when multiple agents are running in parallel. The coordinator must capture batch-level state, and the next session must correctly recover all tasks without re-dispatching already-completed work or losing held-back task context.

## State

- Phase 2: 5 tasks
  - Task 5: "Finished"
  - Task 7: "In Progress" (parallel agent A — implement-agent mid-Step 4)
    - `files_affected: ["src/transform/mapper.py", "src/transform/aggregate.py"]`
  - Task 9: "Awaiting Verification" (parallel agent B — verify-agent mid-Step T4)
    - `files_affected: ["src/export/csv_writer.py"]`
  - Task 10: Pending, `conflict_note: "Held: file conflict with Task 7 on src/transform/mapper.py"`
    - `files_affected: ["src/transform/mapper.py", "src/transform/validator.py"]`
  - Task 11: "Finished" (completed earlier in this parallel batch by agent C)
- Parallel batch: tasks [7, 9, 11], held back: [10]

---

## Trace 30A: `/work pause` during parallel execution

- **Path:** `/work pause` triggered while coordinator is managing parallel batch

### Expected

1. Coordinator recognizes pause signal
2. Running agents (A for task 7, B for task 9) wind down:
   - Agent A (implement): writes partial notes to task 7, keeps status "In Progress"
   - Agent B (verify): does NOT write partial verification, task 9 stays "Awaiting Verification"
3. Task 11 results already processed (status "Finished" — no action needed)
4. Handoff file written with parallel context:
   ```json
   {
     "active_work": [
       {
         "task_id": "7",
         "agent": "implement",
         "agent_step": "Step 4 (implementation)",
         "partial": true,
         "partial_notes": "Mapper module complete. Aggregation not started.",
         "ready_for_verify": false
       },
       {
         "task_id": "9",
         "agent": "verify",
         "agent_step": "Step T4 (output quality)",
         "partial": true,
         "ready_for_verify": false
       }
     ],
     "parallel_state": {
       "batch_tasks": ["7", "9", "11"],
       "completed_in_batch": ["11"],
       "held_back": [
         {"task_id": "10", "conflict_with": "7", "shared_files": ["src/transform/mapper.py"]}
       ]
     }
   }
   ```
5. Task 7 notes updated with `[PARTIAL]` prefix
6. Task 10 keeps its `conflict_note` (transient, but informational for handoff context)
7. Session sentinel written

### Pass criteria

- [ ] Both in-flight tasks represented in `active_work` array
- [ ] Task 11 (already completed) NOT in `active_work` — only in `parallel_state.completed_in_batch`
- [ ] `parallel_state` captures full batch context including held-back tasks with conflict details
- [ ] Task 9 (mid-verification) has no partial `task_verification` written
- [ ] Task 7 notes updated with `[PARTIAL]` prefix
- [ ] Single handoff file captures all parallel state (not one per agent)

### Fail indicators

- Only one of the two in-flight tasks captured in handoff
- Task 11's completion lost or re-dispatched
- Held-back task 10 forgotten in handoff (would lose conflict context)
- Multiple handoff files created (one per agent)
- Partial verification result written for task 9

---

## Trace 30B: Next session resumes parallel batch

- **Path:** `/work` Step 0, handoff with parallel state exists

### State (at session start)

- `.claude/tasks/.handoff.json` exists (from 30A, with `parallel_state`)
- Task 7: "In Progress" with `[PARTIAL]` notes
- Task 9: "Awaiting Verification"
- Task 10: Pending with `conflict_note`
- Task 11: "Finished"

### Expected

1. `/work` Step 0 detects handoff, presents summary:
   ```
   Resuming from previous session (paused during parallel batch):
   - Task 7 "Build transformation engine" — implementation partial, continuing
   - Task 9 "CSV export module" — verification interrupted, will restart
   - Task 10 held back (file conflict with task 7)
   - Task 11 completed in previous batch
   ```
2. Handoff deleted
3. Session recovery runs:
   - Task 7: "In Progress" — no auto-recovery needed (implement-agent will continue)
   - Task 9: "Awaiting Verification" — Case 1: auto-recover by spawning verify-agent
4. `/work` Step 2c re-assesses parallelism with current state:
   - Task 7 needs implementation (routing to implement-agent)
   - Task 9 needs verification (recovery is spawning verify-agent)
   - Task 10 still conflicts with task 7 (held back again)
   - New parallel batch possible: task 7 implementation + task 9 verification (different files, no conflict)
5. `conflict_note` on task 10 may be refreshed or cleared based on new conflict assessment

### Pass criteria

- [ ] All four tasks correctly accounted for (no task forgotten, no task re-dispatched unnecessarily)
- [ ] Task 11 not re-dispatched (already "Finished")
- [ ] Task 9 gets fresh verify-agent via session recovery (not resumed from partial state)
- [ ] Task 10 conflict re-assessed from actual `files_affected` (not blindly trusted from handoff)
- [ ] Parallelism re-assessed fresh — handoff informs context but doesn't dictate batch composition

### Fail indicators

- Task 11 re-dispatched (ignoring completed status)
- Task 10 dispatched despite ongoing conflict with task 7
- Previous batch composition blindly replicated (should re-assess from current state)
- Task 9 verification treated as failed (it wasn't — it was interrupted)
- Sequential execution forced when parallel is still viable
