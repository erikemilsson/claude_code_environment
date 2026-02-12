# Scenario 17: Task Dependency Chains

Verify that `/work` correctly resolves complex dependency relationships — linear chains, multi-blocker convergence, and circular dependency detection.

## Context

Task dependencies control execution order. Simple cases (A depends on B) are implicitly tested elsewhere, but real projects produce complex dependency graphs: chains where A → B → C, convergence where a task waits on multiple predecessors, and potential circular references. `/work` must handle all of these correctly in both sequential and parallel dispatch.

## State (Base)

- Phase 1: 7 tasks
  - Task 1: "Create database schema" (Pending, no deps)
  - Task 2: "Build data access layer" (Pending, depends on [1])
  - Task 3: "Implement business logic" (Pending, depends on [2])
  - Task 4: "Set up authentication" (Pending, no deps)
  - Task 5: "Build API endpoints" (Pending, depends on [2, 4] — both must be finished)
  - Task 6: "Create frontend components" (Pending, depends on [5])
  - Task 7: "Write integration tests" (Pending, depends on [3, 5, 6])
- Parallel execution enabled

---

## Trace 17A: Linear chain — only root tasks eligible initially

- **Path:** /work eligibility assessment → /work task routing

### Scenario

Fresh start. All tasks are "Pending". `/work` assesses eligibility.

### Expected

- Tasks 1 and 4 are eligible (no dependencies)
- Tasks 2, 3, 5, 6, 7 are blocked (unfinished dependencies)
- If parallel mode: Tasks 1 and 4 dispatched concurrently (no file conflicts assumed)
- If sequential mode: Task 1 dispatched (lower ID)

### Pass criteria

- [ ] Only tasks with ALL dependencies satisfied are eligible
- [ ] Tasks 1 and 4 correctly identified as the only unblocked tasks
- [ ] Tasks 2-7 remain "Pending" (not dispatched)
- [ ] Parallel dispatch includes both root tasks when no file conflicts

### Fail indicators

- Task 2 dispatched before Task 1 finishes
- Task 5 dispatched before both 2 AND 4 finish
- Only one root task dispatched when parallel is enabled and no conflicts exist

---

## Trace 17B: Chain propagation — completing a task unblocks the next

- **Path:** `/work` after Task 1 completes → re-assessment

### Scenario

Task 1 finishes (passes verification). Task 4 is still "In Progress". `/work` re-assesses.

### Expected

- Task 2 becomes eligible: its only dependency (Task 1) is now "Finished"
- Task 3 still blocked: depends on Task 2 (still "Pending")
- Task 5 still blocked: depends on Task 2 (Pending) AND Task 4 (In Progress)
- Task 2 dispatched

### Pass criteria

- [ ] Task 2 becomes eligible immediately after Task 1 finishes
- [ ] Task 3 does NOT become eligible (transitive dependency not short-circuited)
- [ ] Task 5 remains blocked (needs BOTH deps, not just one)
- [ ] Dependency check uses actual current status of each dependency

### Fail indicators

- Task 2 still blocked after Task 1 completes
- Task 3 becomes eligible when Task 2 hasn't started (transitive dependency leak)
- User must run `/work` manually to trigger re-assessment

---

## Trace 17C: Multi-blocker convergence — all dependencies must be satisfied

- **Path:** /work eligibility assessment for Task 5

### Scenario

Task 2 is now "Finished". Task 4 is still "In Progress". Task 5 depends on both [2, 4].

### Expected

- Task 5 remains blocked: Task 4 is not "Finished"
- Task 3 becomes eligible (depends only on Task 2, which is "Finished")
- `/work` dispatches Task 3

### Pass criteria

- [ ] Task 5 stays blocked when only one of its two dependencies is satisfied
- [ ] ALL dependencies must be "Finished" for a task to be eligible
- [ ] No partial-satisfaction shortcut exists

### Fail indicators

- Task 5 unblocks when Task 2 finishes but Task 4 hasn't
- Dependency check uses OR logic instead of AND
- Task 5 dispatched with a "partial deps satisfied" note

---

## Trace 17D: Convergence resolves — multi-dep task unblocks

- **Path:** `/work` after Task 4 completes

### Scenario

Task 4 now finishes. Task 2 was already "Finished". Task 5 depends on [2, 4].

### Expected

- Task 5 becomes eligible: both dependencies now "Finished"
- Task 3 may still be "In Progress"
- Task 5 and Task 3 can run in parallel (if no file conflicts)

### Pass criteria

- [ ] Task 5 unblocks the moment its last dependency (Task 4) finishes
- [ ] No stale dependency cache — fresh status read for each assessment
- [ ] Task 5 can run in parallel with unrelated in-progress tasks

### Fail indicators

- Task 5 still blocked after both deps finish (stale cache)
- Task 5 can't run until Task 3 also finishes (false dependency)

---

## Trace 17E: Deep convergence — task with 3+ dependencies

- **Path:** `/work` eligibility for Task 7

### Scenario

Tasks 3, 5, and 6 are all "Finished". Task 7 depends on [3, 5, 6].

### Expected

- Task 7 becomes eligible: all three dependencies satisfied
- Task 7 dispatched

### Pass criteria

- [ ] Task with 3 dependencies correctly evaluates all three
- [ ] Eligible only when ALL three are "Finished"
- [ ] No limit on number of dependencies a single task can have

### Fail indicators

- Only first N dependencies checked
- Task unblocks after 2 of 3 deps finish

---

## Trace 17F: Circular dependency detection

- **Path:** `/health-check` or `/work` dependency validation

### Scenario

Due to a manual edit error, task files contain a circular dependency:
- Task 20: depends on [21]
- Task 21: depends on [22]
- Task 22: depends on [20]

### Expected

- `/work` or `/health-check` detects the cycle during dependency resolution
- Reports: "Circular dependency detected: 20 → 21 → 22 → 20"
- No tasks in the cycle are dispatched (they'd be permanently blocked)
- User directed to fix the dependency error

### Pass criteria

- [ ] Circular dependency detected (not an infinite loop)
- [ ] Clear error message identifying the cycle
- [ ] Affected tasks not dispatched
- [ ] Non-circular tasks in the same phase still dispatchable

### Fail indicators

- Infinite loop during dependency resolution (no cycle detection)
- Tasks in cycle silently ignored (no error surfaced)
- All tasks in the phase blocked due to the cycle (over-conservative)
- `/work` crashes or hangs

---

## Trace 17G: Critical path reflects dependency chain

- **Path:** /work critical path generation

### Scenario

Current state: Tasks 1, 2, 4 finished. Task 3 in progress. Tasks 5, 6, 7 pending. The longest dependency chain is: Task 3 → (unblocks nothing directly in the longest path) vs Task 5 → Task 6 → Task 7 (3 steps).

### Expected

- Critical path identified as the longest remaining chain
- Dashboard shows: `🤖 Build API endpoints → 🤖 Create frontend components → 🤖 Write integration tests → Done *(3 steps)*`
- Human-owned steps (if any) shown with `❗` prefix

### Pass criteria

- [ ] Critical path correctly identifies the longest dependency chain
- [ ] Path includes only incomplete tasks
- [ ] Owner indicators (❗/🤖/👥) match task owners
- [ ] Path updates as tasks complete

### Fail indicators

- Critical path includes already-finished tasks
- Path shows all tasks regardless of dependencies (just a flat list)
- Critical path doesn't update after task completion
