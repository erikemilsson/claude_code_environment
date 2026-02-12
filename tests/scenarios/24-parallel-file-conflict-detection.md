# Scenario 24: Parallel Execution with File Conflict Detection

Verify that `/work` parallel dispatch correctly detects file conflicts between concurrent tasks and holds back conflicting tasks.

## Context

Parallel execution is a core template feature: when multiple tasks are eligible and have no conflicts, they run concurrently. But tasks that modify the same files must NOT run in parallel — the second write would overwrite the first. `/work` must detect file-level conflicts and serialize conflicting tasks while parallelizing non-conflicting ones.

## State

- 4 pending tasks, no decision blockers, all in the same phase:
  - **Task A**: modifies `src/database/models.py` and `src/database/queries.py`
  - **Task B**: modifies `src/api/routes.py` (no conflict with A)
  - **Task C**: modifies `src/database/models.py` and `src/api/middleware.py` (conflicts with A on `models.py`)
  - **Task D**: modifies `tests/test_api.py` (no conflict with anyone)
- Parallel execution enabled in spec frontmatter
- All tasks have no explicit dependency relationships

## Trace 24A: Conflict detection and dispatch

- **Path:** `/work` Step 4 (parallel dispatch)
- `/work` examines file lists for each eligible task
- Detects overlap: Task A and Task C both touch `src/database/models.py`

### Expected

- Tasks A, B, and D are dispatched in parallel (no file conflicts between them)
- Task C is held back until Task A completes (shared `models.py`)
- The conflict reason is logged or surfaced

### Pass criteria

- [ ] File conflict between A and C is detected
- [ ] Non-conflicting tasks (A, B, D) run in parallel
- [ ] Task C is queued, not dispatched alongside A
- [ ] Conflict detection is based on file paths, not just directory overlap

### Fail indicators

- All 4 tasks run in parallel (conflict missed)
- Only A runs, with B, C, D all held back (over-conservative)
- Conflict detection uses directory-level granularity (blocking B because it's also in `src/`)

---

## Trace 24B: Dashboard shows parallel execution status

- **Path:** dashboard.md → task status during parallel execution; work.md § "If Executing (Parallel)" Step 2

### Expected

- Dashboard shows A, B, D as "In Progress"
- Task C shown as "Pending (held: conflict with Task A)" — the `conflict_note` field drives this display
- Overall progress reflects parallel work accurately

### Mechanism

Step 2 of "If Executing (Parallel)" annotates held-back tasks with a `conflict_note` in the task JSON:
```json
{ "conflict_note": "Held: file conflict with Task A on src/database/models.py. Auto-clears when conflict resolves." }
```

The Section Display Rules render this as: `Pending (held: conflict with Task A)` in the Status column.

### Pass criteria

- [ ] Parallel task status is visible in dashboard (A, B, D as "In Progress")
- [ ] Conflict reason is visible in dashboard task status column via `conflict_note`
- [ ] Queued task shows what it's waiting for and why
- [ ] `conflict_note` is removed when the task is dispatched

### Fail indicators

- Dashboard shows C as "Pending" with no explanation of why it's not running
- No indication that A, B, D are running concurrently
- Conflict reason is only in logs, not visible to user
- `conflict_note` persists after conflict resolves

---

## Trace 24C: After conflict resolves, queued task becomes eligible

- **Path:** `/work` "If Executing (Parallel)" Step 4 → incremental re-dispatch loop
- Task A completes. Task C was waiting on it due to `src/database/models.py` conflict.
- Tasks B and D are still in progress.

### Expected

- Task C becomes eligible immediately after Task A completes (within the same polling loop iteration)
- C is dispatched in parallel with still-running B and D (no file conflicts between them)
- C's `conflict_note` is cleared when it's dispatched
- No manual intervention needed

### Mechanism

Step 4 of "If Executing (Parallel)" uses `run_in_background: true` and polls for completion. When Task A finishes:
1. A is removed from `active_agents`
2. Step 2c eligibility is re-run — Task C's conflict on `models.py` is now resolved (A is "Finished")
3. C is dispatched as a new background agent and added to `active_agents`
4. `conflict_note` is cleared from C's task JSON

This is **incremental re-dispatch** — tasks are released as soon as their specific conflicts resolve, not when the entire batch finishes.

### Pass criteria

- [ ] After A completes, C becomes eligible for dispatch within the same parallel execution cycle
- [ ] C can run in parallel with still-running B and D
- [ ] No user action required to unblock C
- [ ] The re-check happens automatically via the polling loop, not only on next `/work` invocation
- [ ] `conflict_note` is cleared from C when dispatched

### Fail indicators

- C remains blocked after A completes
- User must run `/work` again to unblock C
- C can't run until B and D also complete (over-serialization — the old "wait for entire batch" pattern)
