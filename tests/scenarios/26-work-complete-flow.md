# Scenario 26: Work Complete Flow

Verify that `/work complete` correctly handles manual task completion for human-owned tasks, validates preconditions, triggers parent auto-completion, and regenerates the dashboard.

## Context

`/work complete` is the primary mechanism for users to signal that they've finished a task — especially human-owned tasks that Claude cannot implement. It also handles edge cases like completing tasks outside the normal agent workflow, invalid IDs, and subtask parent auto-completion. This scenario tests the full `/work complete` lifecycle.

## State (Base)

- Phase 1: 5 tasks
  - Task 1: "Set up cloud credentials" (owner: human, status: "Pending")
  - Task 2: "Configure database schema" (owner: claude, status: "Finished", task_verification.result: "pass")
  - Task 3: "Build API endpoints" (owner: claude, status: "In Progress", depends on [1, 2])
  - Task 4: "Review data model" (owner: human, status: "In Progress")
  - Task 5: "Write integration tests" (owner: both, status: "Pending", depends on [3, 4])
- Parent Task 10: "Complete procurement" (status: "Broken Down", subtasks: ["10_1", "10_2"])
  - Task 10_1: status: "Finished"
  - Task 10_2: status: "In Progress" (owner: human)

---

## Trace 26A: Complete a human-owned "In Progress" task

- **Path:** work.md § "Task Completion" → Steps 1-8

### Scenario

User runs `/work complete 4` to mark Task 4 (human-owned, "In Progress") as done.

### Expected

1. Task identified by ID (Step 1)
2. Validation passes: status is "In Progress", deps satisfied (Step 2)
3. Work check — reviews changes (Step 3)
4. Task JSON updated (Step 4):
   - `status: "Finished"`
   - `completion_date` set
   - `updated_date` set
   - `notes` include what was done
5. Parent auto-completion checked (Step 5) — Task 4 has no parent, skip
6. Dashboard regenerated (Step 6)
7. Auto-archive check (Step 7) — count < 100, skip
8. Lightweight health check (Step 8)

### Pass criteria

- [ ] Task 4 status changes from "In Progress" to "Finished"
- [ ] `completion_date` and `updated_date` populated
- [ ] Dashboard regenerated with updated task status
- [ ] Health check runs after completion
- [ ] Task 5 dependency status recalculated (Task 4 now satisfied, still waiting on Task 3)

### Fail indicators

- Task completed without validation checks
- Dashboard not regenerated
- No health check after completion
- Task 5 incorrectly unblocked (Task 3 still "In Progress")

---

## Trace 26B: Reject completion of "Pending" task

- **Path:** work.md § "Task Completion" → Step 2

### Scenario

User runs `/work complete 1`. Task 1 is "Pending" (never started).

### Expected

- Step 2 validation fails: status must be "In Progress"
- For quick tasks, the process should first set status to "In Progress", then complete
- User informed of the issue

### Pass criteria

- [ ] "Pending" task not silently completed without passing through "In Progress"
- [ ] Process offers to set "In Progress" first for quick tasks, or instructs user to start the task
- [ ] Task status not changed to "Finished" directly from "Pending"

### Fail indicators

- Task jumps from "Pending" to "Finished" (bypasses "In Progress" checkpoint)
- No validation error or guidance provided
- Workflow compliance check (Step 6 of main process) can't verify the task went through "In Progress"

---

## Trace 26C: Parent auto-completion on last subtask

- **Path:** work.md § "Task Completion" → Step 5

### Scenario

User runs `/work complete 10_2`. Task 10_1 is already "Finished". This is the last subtask.

### Expected

1. Task 10_2 set to "Finished"
2. Step 5: Check parent auto-completion
   - Parent Task 10 has subtasks ["10_1", "10_2"]
   - 10_1: "Finished", 10_2: now "Finished"
   - All subtasks finished → parent auto-completes
3. Parent Task 10 status set to "Finished"
4. Dashboard regenerated showing both completions
5. Any tasks depending on Task 10 become unblocked

### Pass criteria

- [ ] Task 10_2 marked "Finished"
- [ ] Parent Task 10 auto-completes to "Finished" (all subtasks done)
- [ ] Dashboard shows parent as "Finished"
- [ ] Auto-completion is triggered automatically, not requiring a separate user action
- [ ] Downstream tasks depending on parent Task 10 become eligible

### Fail indicators

- Parent stays "Broken Down" despite all subtasks being finished
- User must manually run `/work complete 10` to finish the parent
- Dashboard shows parent as "Broken Down" while all subtasks are "Finished"

---

## Trace 26D: `/work complete` with no ID finds current task

- **Path:** work.md § "Task Completion" → Step 1

### Scenario

User runs `/work complete` (no ID). Task 3 is the only task with status "In Progress".

### Expected

- Step 1: No ID provided → scan for current "In Progress" task
- Task 3 identified as the in-progress task
- Completion proceeds on Task 3

### Pass criteria

- [ ] Current "In Progress" task detected when no ID is provided
- [ ] Correct task identified (Task 3)
- [ ] Completion proceeds normally

### Fail indicators

- Error: "No task ID provided" without attempting auto-detection
- Wrong task selected
- Ambiguity not handled if multiple tasks are "In Progress" (parallel mode)

---

## Trace 26E: Reject completion of already-finished task

- **Path:** work.md § "Task Completion" → Step 2

### Scenario

User runs `/work complete 2`. Task 2 is already "Finished".

### Expected

- Step 2 validation: status is "Finished", not "In Progress"
- Reports: "Task 2 is already finished"
- No state changes

### Pass criteria

- [ ] Already-finished task not re-completed
- [ ] No redundant status changes or date updates
- [ ] User informed task is already done

### Fail indicators

- Task re-processed (completion_date overwritten, dashboard regenerated for no reason)
- Error message unclear about what happened
