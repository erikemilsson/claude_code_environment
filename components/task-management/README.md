# Task Management Component

## Overview

The Task Management component provides a hierarchical task tracking system with automatic parent completion, difficulty-based breakdown requirements, and status validation. It's designed to reduce LLM error probability by enforcing breakdown of complex tasks (difficulty ≥7) into manageable subtasks (difficulty ≤6).

## Core Concepts

### Task Difficulty Scoring (LLM Error Risk)

| Level    | Risk        | Examples                                      |
| -------- | ----------- | --------------------------------------------- |
| 1-2      | Trivial     | Fix typo, update text, add comment            |
| 3-4      | Low         | Basic CRUD, simple UI changes                 |
| 5-6      | Moderate    | Form validation, API integration              |
| **7-8**  | **High**    | **Auth setup, database migration**            |
| **9-10** | **Extreme** | **Architecture changes, distributed systems** |

**Critical Rule**: Tasks with difficulty ≥7 **must** be broken down into subtasks with difficulty ≤6 using the breakdown command to reduce error risk.

### Task Status Values

| Status          | Meaning                        | Can Work On? | Auto-Transitions       |
| --------------- | ------------------------------ | ------------ | ---------------------- |
| **Pending**     | Defined but not started        | ✅ Yes        | → In Progress (manual) |
| **In Progress** | Actively being worked on       | ✅ Yes        | → Finished (manual)    |
| **Blocked**     | Cannot proceed due to blockers | ❌ No         | → In Progress (manual) |
| **Broken Down** | Decomposed into subtasks       | ❌ No         | → Finished (automatic) |
| **Finished**    | Complete                       | ❌ No         | None (terminal)        |

**Key Concept**: "Broken Down" tasks are **containers** that track progress through their subtasks. They cannot be worked on directly and auto-complete when all subtasks finish.

## File Structure

When using this component in a project:

```
project/
└── .claude/
    ├── tasks/
    │   ├── task-overview.md   # Auto-generated summary table
    │   ├── task-1.json        # Individual task files
    │   ├── task-2.json        # (sequential numbering)
    │   └── ...
    └── commands/
        ├── complete-task.md   # Start/finish tasks with status tracking
        ├── breakdown.md       # Split difficulty ≥7 tasks into subtasks
        ├── sync-tasks.md      # Update task-overview.md from JSON
        └── update-tasks.md    # Validate task system health
```

## Task Schema

Tasks are stored as individual JSON files following the schema in `schema.json`. See `schema.json` for the complete JSON Schema definition.

### Example Task

```json
{
  "id": "1",
  "title": "Setup authentication system",
  "description": "Implement OAuth2 with Google and GitHub providers",
  "difficulty": 7,
  "status": "Pending",
  "created_date": "2024-01-15",
  "updated_date": "2024-01-15",
  "assigned_to": null,
  "estimated_hours": 8,
  "actual_hours": 0,
  "dependencies": [],
  "subtasks": [],
  "parent_task": null,
  "files_affected": ["src/auth/", "config/oauth.json"],
  "notes": "",
  "blockers": [],
  "tags": ["security", "backend"],
  "breakdown_history": null
}
```

## Commands

### complete-task.md

**Purpose**: Start and finish tasks with proper status tracking.

**Process**:
1. Validates task is workable (not "Broken Down")
2. Checks dependencies are met
3. Updates status to "In Progress"
4. Performs the work
5. Updates status to "Finished"
6. Checks for parent task auto-completion
7. Updates task-overview.md

See `commands/complete-task.md` for full details.

### breakdown.md

**Purpose**: Split tasks with difficulty ≥7 into manageable subtasks.

**Process**:
1. Validates task difficulty ≥7
2. Analyzes requirements and plans subtasks (each ≤6 difficulty)
3. Creates subtask JSON files
4. Updates parent status to "Broken Down"
5. Establishes parent-child relationships
6. Updates task-overview.md

See `commands/breakdown.md` for full details.

### sync-tasks.md

**Purpose**: Update task-overview.md to reflect current state of all task JSON files.

**Process**:
1. Reads all task JSON files
2. Generates markdown table with status indicators
3. Shows subtask progress for "Broken Down" tasks
4. Includes summary statistics

See `commands/sync-tasks.md` for full details.

### update-tasks.md

**Purpose**: Validate all task structures, check consistency, and flag issues.

**Process**:
1. Validates task structure against schema
2. Checks consistency between JSON and overview
3. Validates parent-child relationships
4. Flags outdated or irrelevant tasks
5. Reports findings and suggests corrections

See `commands/update-tasks.md` for full details.

## Reference Documentation

### difficulty-guide.md

Detailed scoring criteria for task difficulty assessment and breakdown strategies.

### validation-rules.md

Comprehensive validation rules for:
- Required fields
- Status transitions (legal and illegal)
- Parent-child relationships
- Dependency rules

### breakdown-workflow.md

Complete guide to hierarchical task management including:
- When to break down tasks
- Understanding "Broken Down" status
- Subtask rules and completion logic
- Example workflows
- Common questions

## Workflow Example

### 1. Initial High-Difficulty Task

```json
{
  "id": "12",
  "title": "Build emissions data ETL pipeline",
  "difficulty": 8,
  "status": "Pending"
}
```

### 2. Break Down the Task

Run: `@.claude/commands/breakdown.md 12`

**Result**: Parent task becomes "Broken Down (0/5 done)", subtasks created:
- Task 13: "Design pipeline architecture" (difficulty: 4, parent: "12")
- Task 14: "Build API connectors" (difficulty: 5, parent: "12")
- Task 15: "Implement data transformation" (difficulty: 6, parent: "12")
- Task 16: "Create database loader" (difficulty: 5, parent: "12")
- Task 17: "Add error handling" (difficulty: 4, parent: "12")

### 3. Work on Subtasks

Run: `@.claude/commands/complete-task.md 13`

**Progress updates**:
- After Task 13: "Broken Down (1/5 done)"
- After Task 14: "Broken Down (2/5 done)"
- After Task 15: "Broken Down (3/5 done)"
- After Task 16: "Broken Down (4/5 done)"

### 4. Complete Last Subtask

Run: `@.claude/commands/complete-task.md 17`

**Result**:
- Task 17 marked "Finished"
- Parent Task 12 automatically transitions to "Finished"
- Notification: "🎉 Parent Task #12 automatically completed!"

## Best Practices

1. **Always Use complete-task.md**: Start all task work with this command - manual status updates lead to inconsistencies
2. **Break Down Complexity Early**: Split tasks ≥7 difficulty using breakdown.md before starting work
3. **Trust the Automation**: Let parent tasks auto-complete; don't manually change status
4. **Work Bottom-Up**: Always work on subtasks, never on "Broken Down" parents
5. **Validate Regularly**: Run update-tasks.md before major work sessions
6. **Sequential IDs**: Never skip task numbers (1, 2, 3... not 1, 3, 5)
7. **Track Hours on Subtasks**: Don't track time on parent tasks; sum subtask hours for total
8. **Clear Blockers**: Document specific blockers, not vague issues
9. **Shallow Dependencies**: Keep dependency depth shallow (max 2-3 levels)

## Common Pitfalls

❌ **Don't**: Manually set parent task to "Finished"
✅ **Do**: Let it auto-complete when subtasks finish

❌ **Don't**: Try to work on a "Broken Down" task
✅ **Do**: Work on its subtasks instead

❌ **Don't**: Create subtasks with difficulty >6
✅ **Do**: Keep all subtasks at moderate complexity or below

❌ **Don't**: Nest subtasks (subtask of subtask)
✅ **Do**: Keep hierarchy flat (one level only)

❌ **Don't**: Break down tasks with difficulty <7
✅ **Do**: Only break down high-risk tasks (≥7)

## Integration with Projects

To use this component in a new project:

1. Copy the task management commands to `.claude/commands/`
2. Copy reference documentation to `.claude/reference/`
3. Create `.claude/tasks/` directory
4. Create initial task JSON files following the schema
5. Run `sync-tasks.md` to generate task-overview.md
6. Reference the component in your project's CLAUDE.md

## Benefits

1. **No Ambiguity**: Clear distinction between work items (subtasks) and containers (broken down parents)
2. **Accurate Progress**: Easy to see "3 out of 4 subtasks done = 75%" in task-overview.md
3. **Prevents Errors**: Cannot accidentally complete parent with unfinished work
4. **Self-Managing**: Automatic completion reduces manual overhead and prevents inconsistencies
5. **Better Planning**: Difficulty scores reflect actual work complexity per subtask
6. **Lower Risk**: Each subtask has difficulty ≤6, reducing LLM error probability
7. **Clear Dependencies**: Subtask dependencies make work sequence explicit
