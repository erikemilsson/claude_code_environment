# Scenario 25: Breakdown Command

Verify that `/breakdown` correctly splits high-difficulty tasks into subtasks, updates parent status, inherits spec provenance, and integrates with the `/work` routing that rejects difficulty >= 7 tasks.

## Context

Tasks with difficulty >= 7 cannot be dispatched to implement-agent (Step 1b rejects them). The `/breakdown` command is the only way to make them workable. This scenario tests the full lifecycle: detection, breakdown, provenance inheritance, parent status, and re-eligibility of subtasks.

## State (Base)

- Phase 1: 4 tasks
  - Task 1: "Set up project scaffolding" (difficulty 3, Pending)
  - Task 2: "Build authentication system" (difficulty 8, Pending, `spec_section: "## Authentication"`, `spec_fingerprint: "sha256:aaa"`, `section_fingerprint: "sha256:bbb"`, `section_snapshot_ref: "spec_v1_decomposed.md"`)
  - Task 3: "Create user profile page" (difficulty 5, Pending, depends on Task 2)
  - Task 4: "Add admin dashboard" (difficulty 4, Pending, depends on Task 2)

---

## Trace 25A: `/work` rejects high-difficulty task

- **Path:** `/work` → Step 3 routing → implement-agent.md → Step 1b Validate Task

### Scenario

Task 1 is "Finished". Task 2 (difficulty 8) is next eligible. `/work` routes to implement-agent, which validates the task.

### Expected

- implement-agent Step 1b: `difficulty >= 7` → Stop
- Reports back: "Task 2 needs breakdown first (difficulty 8). Use `/breakdown 2`."
- Task 2 stays "Pending" — not set to "In Progress"

### Pass criteria

- [ ] implement-agent rejects difficulty 8 task at Step 1b
- [ ] Task status remains "Pending" (not modified)
- [ ] User is directed to `/breakdown` with the task ID
- [ ] No implementation work begins on the high-difficulty task

### Fail indicators

- implement-agent begins implementing Task 2 despite difficulty 8
- Task 2 set to "In Progress" before breakdown
- Error message doesn't mention `/breakdown`

---

## Trace 25B: `/breakdown` creates subtasks with inherited provenance

- **Path:** breakdown.md → Process Steps 1-5

### Scenario

User runs `/breakdown 2`. The command reads Task 2 and splits it into 3 subtasks.

### Expected

- 3 subtask files created: `task-2_1.json`, `task-2_2.json`, `task-2_3.json`
- Each subtask has difficulty <= 6
- Each subtask inherits ALL spec provenance from parent:
  - `spec_fingerprint: "sha256:aaa"`
  - `spec_version: "spec_v1"`
  - `spec_section: "## Authentication"`
  - `section_fingerprint: "sha256:bbb"`
  - `section_snapshot_ref: "spec_v1_decomposed.md"`
- Parent Task 2 updated:
  - `status: "Broken Down"`
  - `subtasks: ["2_1", "2_2", "2_3"]`
- Dashboard regenerated after breakdown

### Pass criteria

- [ ] Subtask files created with `parent_task: "2"`
- [ ] All 5 spec provenance fields copied from parent to each subtask
- [ ] Each subtask has difficulty <= 6
- [ ] Parent status set to "Broken Down"
- [ ] Parent `subtasks` array lists all subtask IDs
- [ ] Dashboard regenerated (shows subtasks, parent marked "Broken Down")

### Fail indicators

- Subtasks missing spec provenance fields (breaks drift detection)
- Subtask difficulty >= 7 (recursive breakdown needed but not triggered)
- Parent status not changed to "Broken Down"
- Dashboard not regenerated after breakdown

---

## Trace 25C: Downstream dependencies transfer to subtasks

- **Path:** `/work` auto-detect after breakdown

### Scenario

Tasks 3 and 4 depend on Task 2 (`dependencies: ["2"]`). After breakdown, Task 2 is "Broken Down". `/work` needs to understand that Tasks 3 and 4 are blocked until all subtasks of Task 2 are finished.

### Expected

- Tasks 3 and 4 remain blocked — parent Task 2 is "Broken Down", not "Finished"
- Subtasks 2_1, 2_2, 2_3 are eligible for dispatch (no deps of their own, or ordered internally)
- When ALL subtasks finish → parent auto-completes to "Finished" → Tasks 3 and 4 unblock

### Pass criteria

- [ ] Tasks depending on parent remain blocked while parent is "Broken Down"
- [ ] Subtasks are dispatchable by `/work`
- [ ] Parent auto-completes when all subtasks finish
- [ ] Downstream tasks unblock after parent auto-completion

### Fail indicators

- Tasks 3 and 4 unblock immediately after breakdown (parent is "Broken Down", not "Finished")
- Subtasks not recognized as dispatchable by `/work`
- Parent doesn't auto-complete when all subtasks finish
- Manual intervention required to unblock downstream tasks

---

## Trace 25D: `/work` rejects "Broken Down" parent task

- **Path:** implement-agent.md → Step 1b Validate Task

### Scenario

User tries `/work 2` to work directly on the broken-down parent task.

### Expected

- implement-agent Step 1b: `status is "Broken Down"` → Stop
- Reports: "Task 2 has been broken down — work on subtasks 2_1, 2_2, 2_3 instead"

### Pass criteria

- [ ] implement-agent rejects "Broken Down" tasks at Step 1b
- [ ] User directed to work on subtasks instead
- [ ] Parent task status not modified

### Fail indicators

- implement-agent starts working on the parent task
- Parent task set to "In Progress" despite being "Broken Down"
