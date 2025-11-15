# Task Management Component

## Overview

The Task Management component provides a hierarchical task tracking system with automatic parent completion, difficulty-based breakdown requirements, and status validation. It's designed to reduce LLM error probability by enforcing breakdown of complex tasks (difficulty ≥7) into manageable subtasks (difficulty ≤6).

## Versioning Strategy

### Component Version: 1.0.0

This component uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes to schema or command interfaces
- **MINOR**: New features, new commands, or new optional fields
- **PATCH**: Bug fixes, documentation updates, clarifications

### Version History

- **1.0.0** (2025-11-15): Initial release with core task management features
  - Hierarchical task structure with parent-child relationships
  - Automatic parent completion when all subtasks finish
  - Difficulty-based breakdown requirements (≥7 must break down)
  - Four core commands (complete-task, breakdown, sync-tasks, update-tasks)
  - JSON schema with validation rules

### Updating This Component in Projects

When a new version is released, projects can update by:

1. **Review changelog**: Check version history above for breaking changes
2. **Backup current state**: Copy `.claude/tasks/` to `.claude/tasks-backup/`
3. **Update commands**: Replace command files in `.claude/commands/`
4. **Update reference docs**: Replace files in `.claude/reference/`
5. **Update schema**: Review `schema.json` for new fields
6. **Migrate tasks**: If breaking changes exist, run migration script (see Migrations section)
7. **Test**: Run `update-tasks.md` to validate all tasks still conform to schema

### Backwards Compatibility

This component maintains backwards compatibility within MINOR versions:

- New optional fields can be added without migration
- Existing fields maintain the same types and meanings
- Command interfaces remain stable
- Status values and transitions remain unchanged

### Future Migrations

If MAJOR version updates require migration, migration scripts will be provided in `migrations/` directory with step-by-step instructions.

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

### Quick Integration (5 minutes)

To use this component in a new project:

1. **Copy component files**:
   ```bash
   # From this repository to your project
   cp -r components/task-management/commands/* your-project/.claude/commands/
   cp -r components/task-management/reference/* your-project/.claude/reference/
   ```

2. **Create tasks directory**:
   ```bash
   mkdir -p your-project/.claude/tasks
   ```

3. **Create initial tasks**: Create `task-1.json`, `task-2.json`, etc. following the schema

4. **Generate overview**:
   ```
   @.claude/commands/sync-tasks.md
   ```

5. **Reference in CLAUDE.md**:
   ```markdown
   ## Task Management

   Uses Task Management Component v1.0.0
   See `.claude/reference/breakdown-workflow.md` for task hierarchy rules.
   ```

### Integration Example: Data Engineering Project

For a typical data engineering project integrating this component:

**File structure**:
```
data-pipeline-project/
├── CLAUDE.md
├── README.md
└── .claude/
    ├── commands/
    │   ├── complete-task.md      # From component
    │   ├── breakdown.md          # From component
    │   ├── sync-tasks.md         # From component
    │   ├── update-tasks.md       # From component
    │   └── run-pipeline.md       # Project-specific command
    ├── context/
    │   ├── overview.md
    │   └── standards/
    │       └── python-style.md
    ├── reference/
    │   ├── difficulty-guide.md   # From component
    │   ├── validation-rules.md   # From component
    │   └── breakdown-workflow.md # From component
    └── tasks/
        ├── task-overview.md      # Generated by sync-tasks
        ├── task-1.json          # "Setup database schema" (difficulty: 7, broken down)
        ├── task-2.json          # "Create staging tables" (difficulty: 5)
        ├── task-3.json          # "Build transformation logic" (difficulty: 6)
        └── task-4.json          # "Implement error handling" (difficulty: 4)
```

**Example initial task** (task-1.json):
```json
{
  "id": "1",
  "title": "Setup database schema",
  "description": "Design and implement PostgreSQL schema for emissions data with proper indexing and constraints",
  "difficulty": 7,
  "status": "Pending",
  "created_date": "2025-11-15",
  "dependencies": [],
  "subtasks": [],
  "parent_task": null,
  "files_affected": ["sql/schema.sql", "migrations/001_initial.sql"],
  "tags": ["database", "infrastructure"]
}
```

**CLAUDE.md reference**:
```markdown
# CLAUDE.md

## Task Management

This project uses Task Management Component v1.0.0

### Commands
- `@.claude/commands/complete-task.md {id}` - Start/finish tasks
- `@.claude/commands/breakdown.md {id}` - Split complex tasks (difficulty ≥7)
- `@.claude/commands/sync-tasks.md` - Update task-overview.md
- `@.claude/commands/update-tasks.md` - Validate task system

### Workflow
1. High-difficulty tasks (≥7) must be broken down before starting
2. Use complete-task.md for all task work
3. Parent tasks auto-complete when subtasks finish
4. See `.claude/reference/breakdown-workflow.md` for details

## Project-Specific Context
...
```

### Integration Example: Documentation Project

For a documentation/content project:

**CLAUDE.md reference**:
```markdown
# CLAUDE.md

## Task Management

Uses Task Management Component v1.0.0

### Custom Difficulty Mapping

This documentation project adapts difficulty scoring:
- 1-2: Typo fixes, minor updates
- 3-4: Single page creation, small edits
- 5-6: Multi-page documentation, API reference generation
- 7-8: Documentation architecture, style guide creation
- 9-10: Complete documentation system overhaul

### Tags Used
- `content`: Writing/editing tasks
- `structure`: Information architecture
- `review`: Editorial review needed
- `technical`: Requires technical accuracy validation
- `api-docs`: API reference documentation

## Workflow Notes
- All `review` tagged tasks require completion checklist from `.claude/reference/content-review-checklist.md`
- Technical content tasks should reference `standards/writing-style-guide.md`
```

### Customization Options

Projects can customize this component by:

1. **Custom difficulty interpretations**: Adjust difficulty guide in `.claude/reference/difficulty-guide.md` for domain-specific complexity
2. **Additional status values**: Extend status enum in schema (requires MAJOR version bump)
3. **Project-specific fields**: Add custom fields to task JSON (use `custom_*` prefix to avoid conflicts)
4. **Tag taxonomies**: Define project-specific tag sets in CLAUDE.md
5. **Workflow variations**: Create project-specific commands that wrap core commands

### Using with Templates

Templates in this repository can declare component dependencies in their `components.json`:

```json
{
  "included_components": [
    {
      "name": "task-management",
      "version": "1.0.0",
      "files": {
        "commands": ["complete-task.md", "breakdown.md", "sync-tasks.md", "update-tasks.md"],
        "reference": ["difficulty-guide.md", "validation-rules.md", "breakdown-workflow.md"]
      },
      "customizations": {
        "difficulty_guide": "Adapted for documentation projects",
        "tags": ["content", "structure", "review", "technical"]
      }
    }
  ]
}
```

This allows templates to automatically include and configure the component during project initialization.

## Benefits

1. **No Ambiguity**: Clear distinction between work items (subtasks) and containers (broken down parents)
2. **Accurate Progress**: Easy to see "3 out of 4 subtasks done = 75%" in task-overview.md
3. **Prevents Errors**: Cannot accidentally complete parent with unfinished work
4. **Self-Managing**: Automatic completion reduces manual overhead and prevents inconsistencies
5. **Better Planning**: Difficulty scores reflect actual work complexity per subtask
6. **Lower Risk**: Each subtask has difficulty ≤6, reducing LLM error probability
7. **Clear Dependencies**: Subtask dependencies make work sequence explicit
