# Scenario 29: On Hold and Absorbed Statuses

Verify that `/work` correctly handles `On Hold` and `Absorbed` task statuses — skipping them during routing, excluding them from completion checks, and preserving audit trails.

## Context

`On Hold` and `Absorbed` are statuses for tasks that are intentionally paused or folded into other tasks. Unlike `Blocked` (which has a specific impediment), `On Hold` is a user-initiated pause. Unlike deletion, `Absorbed` preserves the task's history while removing it from active work. Both statuses must be excluded from routing, parallel dispatch, and phase completion calculations.

## State (Base)

- Phase 1: 6 tasks
  - Task 1: "Set up data pipeline" (status: "Finished", task_verification.result: "pass")
  - Task 2: "Configure monitoring" (status: "On Hold", notes: "Deferring until infrastructure review in March")
  - Task 3: "Build ETL jobs" (status: "Pending", depends on [1])
  - Task 4: "Add data validation" (status: "Absorbed", absorbed_into: "3", notes: "Scope covered by task 3 after breakdown")
  - Task 5: "Write API layer" (status: "Pending", depends on [3])
  - Task 6: "Deploy to staging" (status: "Pending", owner: "human", depends on [3, 5])
- Parent Task 10: "Initial data setup" (status: "Broken Down", subtasks: ["10_1", "10_2", "10_3"])
  - Task 10_1: status: "Finished"
  - Task 10_2: status: "Absorbed", absorbed_into: "10_1"
  - Task 10_3: status: "Finished"

---

## Trace 29A: `/work` skips On Hold tasks during routing

- **Path:** work.md Step 3 → Explicit routing algorithm

### Scenario

User runs `/work` (auto-detect mode). Task 2 is "On Hold", Task 3 is "Pending" with satisfied deps.

### Expected

1. Step 3 routing scans for actionable tasks
2. Task 2 ("On Hold") is excluded from candidate pool — not treated as Pending, Blocked, or actionable
3. Task 3 ("Pending") is selected as next work item
4. Status summary line shows on hold count: "Tasks: 6 total (1 finished, 0 in progress, 3 pending, 1 on hold, 1 absorbed)"

### Pass criteria

- [ ] Task 2 not selected for execution despite being a non-finished task
- [ ] Task 3 correctly identified as next actionable task
- [ ] On Hold tasks excluded from parallelism eligibility (Step 2c)
- [ ] Status summary includes on hold and absorbed counts

### Fail indicators

- `/work` attempts to execute Task 2
- Task 2 treated as "Pending" or "Blocked"
- On Hold tasks included in parallel batch assessment

---

## Trace 29B: Absorbed tasks excluded from phase completion

- **Path:** work.md Step 3 → Explicit routing algorithm, Step 1

### Scenario

Phase 1 tasks: 1 (Finished), 2 (On Hold), 3 (Finished), 4 (Absorbed), 5 (Finished), 6 (Finished). User runs `/work`.

### Expected

1. Phase completion check excludes Absorbed tasks (Task 4)
2. On Hold task (Task 2) is NOT excluded from phase completion — it's still an active task that hasn't been done
3. Phase 1 is NOT complete because Task 2 is On Hold
4. `/work` reports: phase not complete, Task 2 is on hold

### Pass criteria

- [ ] Absorbed tasks excluded from phase completion calculation
- [ ] On Hold tasks still count as incomplete for phase completion (user must resume or absorb them)
- [ ] Phase correctly identified as incomplete
- [ ] User informed that Task 2 (On Hold) prevents phase completion

### Fail indicators

- Phase marked complete while Task 2 is On Hold
- Absorbed task counted as incomplete (blocking phase)
- No mention of On Hold task in phase status

---

## Trace 29C: Parent auto-completion with Absorbed subtask

- **Path:** work.md § "Task Completion" → Step 5

### Scenario

Parent Task 10 has subtasks [10_1, 10_2, 10_3]. Task 10_1: Finished, Task 10_2: Absorbed (into 10_1), Task 10_3: Finished.

### Expected

1. Parent auto-completion check runs
2. Non-Absorbed subtasks: 10_1 (Finished), 10_3 (Finished) — all done
3. Absorbed subtask 10_2 excluded from check
4. Parent Task 10 auto-completes to "Finished"

### Pass criteria

- [ ] Absorbed subtask (10_2) excluded from auto-completion check
- [ ] Parent auto-completes when all non-Absorbed subtasks are Finished
- [ ] Parent status changes from "Broken Down" to "Finished"

### Fail indicators

- Parent stays "Broken Down" because 10_2 is not "Finished"
- Absorbed subtask blocks parent completion
- Parent requires manual completion

---

## Trace 29D: Health check validates On Hold and Absorbed rules

- **Path:** health-check.md Part 1 → Status Rules (Check 5)

### Scenario

Health check runs on a project with:
- Task 2: status "On Hold", no notes field
- Task 4: status "Absorbed", no absorbed_into field
- Task 7: status "On Hold", notes: "Waiting for Q2", on hold for 45 days

### Expected

1. Task 2: Warning — "On Hold" should have notes explaining why paused
2. Task 4: Error — "Absorbed" must have `absorbed_into` field
3. Task 7: Warning — on hold > 30 days (may be forgotten)

### Pass criteria

- [ ] Missing notes on "On Hold" flagged as warning
- [ ] Missing `absorbed_into` on "Absorbed" flagged as error
- [ ] Stale "On Hold" (> 30 days) flagged as warning
- [ ] Auto-fix offered for stale On Hold: resume, absorb, or keep

### Fail indicators

- On Hold without notes passes validation silently
- Absorbed without `absorbed_into` passes validation
- Long-standing On Hold tasks not detected

---

## Trace 29E: Only user can resume On Hold tasks

- **Path:** work.md Step 3, shared-definitions.md § Mandatory Rules

### Scenario

User runs `/work`. Task 2 is "On Hold". Claude determines the hold reason is no longer valid.

### Expected

1. `/work` does NOT automatically change Task 2 from "On Hold" to "Pending"
2. Claude may note in output: "Task 2 is on hold — resume it if the hold reason no longer applies"
3. Only explicit user action can move a task out of "On Hold"

### Pass criteria

- [ ] Claude never auto-resumes On Hold tasks
- [ ] User informed about on-hold tasks when relevant
- [ ] On Hold is a "user-owns-the-transition" status

### Fail indicators

- Claude sets On Hold task back to Pending without user instruction
- On Hold tasks silently skipped with no mention to user
