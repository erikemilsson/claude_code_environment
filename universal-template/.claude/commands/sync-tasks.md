# Command: sync-tasks

## Purpose
Update `task-overview.md` to reflect current state of all task JSON files.

## Usage
```
/sync-tasks   # Generate updated task overview
```

## Process

### 1. Scan All Task Files
- Read all `.claude/tasks/task-*.json` files
- Validate JSON structure
- Extract task data

### 2. Generate Overview

Create `task-overview.md` with:

#### Header
```markdown
# Task Overview
*Generated: 2025-12-29 10:30*
*Total: 25 | Pending: 10 | In Progress: 2 | Finished: 12 | Broken Down: 1*
```

#### Task Table
```markdown
## All Tasks

| ID | Title | Status | Difficulty | Parent | Subtasks |
|----|-------|--------|------------|--------|----------|
| 001 | Setup database | Finished | 4 | - | - |
| 002 | Build API | Broken Down | 8 | - | [002-1, 002-2, 002-3] |
| 002-1 | Design endpoints | Finished | 5 | 002 | - |
| 002-2 | Implement auth | In Progress | 6 | 002 | - |
| 002-3 | Add validation | Pending | 5 | 002 | - |
```

#### Status Sections
Group tasks by status:

```markdown
## Pending (10 tasks)
- task-003: Add user profile page (difficulty: 5, priority: medium)
- task-004: Implement search (difficulty: 7, priority: high) ⚠ Needs breakdown
...

## In Progress (2 tasks)
- task-002-2: Implement auth (difficulty: 6, priority: critical)
- task-010: Add logging (difficulty: 4, priority: low)

## Finished (12 tasks)
- task-001: Setup database (difficulty: 4)
...

## Broken Down (1 task)
- task-002: Build API (8 subtasks, 2/3 complete)
```

#### Priority Tasks
```markdown
## High Priority
- task-004: Implement search (difficulty: 7, status: pending) ⚠ Needs breakdown
- task-002-2: Implement auth (difficulty: 6, status: in_progress)
```

#### Warnings
```markdown
## Warnings
⚠ Tasks requiring breakdown (difficulty ≥7):
- task-004: Implement search (difficulty: 7)
- task-015: Migrate database (difficulty: 8)
```

### 3. Calculate Statistics

- Total tasks
- Status distribution
- Difficulty distribution
- Completion percentage
- Average difficulty

## Output Location
`.claude/tasks/task-overview.md`

## When to Use
- After creating new tasks
- After updating task status
- After breaking down tasks
- Before starting work (to see current state)
- Periodically to review progress

## Integration
- Automatically called by `/complete-task` after finishing a task
- Can be run manually anytime

## Example Output

```markdown
# Task Overview
*Generated: 2025-12-29 14:30*
*Total: 15 | Pending: 6 | In Progress: 1 | Finished: 7 | Broken Down: 1*

## Progress
Completion: 53% (8/15 tasks finished, including broken down parent)

## All Tasks

| ID | Title | Status | Difficulty | Parent | Subtasks |
|----|-------|--------|------------|--------|----------|
| 001 | Setup PostgreSQL database | Finished | 4 | - | - |
| 002 | Build REST API | Broken Down | 8 | - | [002-1, 002-2, 002-3] |
| 002-1 | Design API endpoints | Finished | 5 | 002 | - |
| 002-2 | Implement authentication | In Progress | 6 | 002 | - |
| 002-3 | Add request validation | Pending | 5 | 002 | - |
| 003 | Create user profile page | Pending | 5 | - | - |
| 004 | Implement search functionality | Pending | 7 | - | - |

## Pending (6 tasks)
- task-002-3: Add request validation (difficulty: 5, priority: critical, parent: task-002)
- task-003: Create user profile page (difficulty: 5, priority: medium)
- task-004: Implement search functionality (difficulty: 7, priority: high) ⚠ Needs breakdown
...

## In Progress (1 task)
- task-002-2: Implement authentication (difficulty: 6, priority: critical, parent: task-002)

## Finished (7 tasks)
- task-001: Setup PostgreSQL database (difficulty: 4)
- task-002-1: Design API endpoints (difficulty: 5, parent: task-002)
...

## Broken Down (1 task)
- task-002: Build REST API (3 subtasks, 1/3 complete - 33%)
  - task-002-1: Design API endpoints [Finished]
  - task-002-2: Implement authentication [In Progress]
  - task-002-3: Add request validation [Pending]

## High Priority
- task-002-2: Implement authentication (difficulty: 6, status: in_progress)
- task-004: Implement search functionality (difficulty: 7, status: pending)

## Warnings
⚠ Tasks requiring breakdown (difficulty ≥7):
- task-004: Implement search functionality (difficulty: 7, status: pending)

## Next Steps
1. Complete task-002-2 (currently in progress)
2. Break down task-004 before starting (difficulty: 7)
3. Continue with pending tasks after high-priority items
```
