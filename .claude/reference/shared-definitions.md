# Shared Definitions

Single source of truth for task management definitions.

## Difficulty Scale (1-10)

| Level | Category | Action | Examples |
|-------|----------|--------|----------|
| 1-2 | Routine | Just do it | Fix typo, add field, update config |
| 3-4 | Standard | May take multiple steps | CRUD for entity, API endpoint, OAuth integration |
| 5-6 | Substantial | Design decisions needed | New module, real-time features, RBAC |
| 7-8 | Large scope | **MUST break down first** | Microservice migration, replace database |
| 9-10 | Multi-phase | **MUST break down into phases** | Architecture redesign, security overhaul |

### When to Break Down

Ask: "Can this be completed in one focused session?"
- **Yes** → Difficulty 1-6, just do it
- **No, too much scope** → Difficulty 7-8, break into chunks
- **No, need discovery** → Difficulty 9-10, break into phases

## Status Values

| Status | Meaning | Rules |
|--------|---------|-------|
| Pending | Not started | Ready to work on |
| In Progress | Currently working | Only ONE at a time |
| Blocked | Cannot proceed | Document blocker in notes |
| Broken Down | Split into subtasks | Work on subtasks, not this |
| Finished | Complete | Auto-set when subtasks done |

## Phase Values (Standard Environment)

| Phase | Purpose | Typical Tasks |
|-------|---------|---------------|
| spec | Define what to build | Requirements, acceptance criteria |
| plan | Design how to build | Architecture, task breakdown |
| execute | Build the implementation | Coding, file creation |
| verify | Confirm it works | Testing, validation |

## Task JSON Structure

### Minimal Task
```json
{
  "id": "1",
  "title": "Brief description",
  "status": "Pending",
  "difficulty": 3
}
```

### Full Task
```json
{
  "id": "1",
  "title": "Brief description",
  "description": "Detailed explanation",
  "status": "Pending",
  "difficulty": 3,
  "phase": "execute",
  "owner": "claude",
  "dependencies": [],
  "subtasks": [],
  "parent_task": null,
  "notes": ""
}
```

See `task-schema.md` for complete field definitions.

## Mandatory Rules

**ALWAYS:**
1. Break down tasks with difficulty >= 7 before starting
2. Only one task "In Progress" at a time
3. Run `/sync-tasks` after completing any task
4. Parent tasks auto-complete when all subtasks finish

**NEVER:**
- Work on "Broken Down" tasks directly (work on subtasks instead)
- Skip status updates
- Work on multiple tasks simultaneously

## Owner Field

Tasks can have an `owner` field:
- `claude` - Claude will do this task (default when not specified)
- `human` - Requires human action
- `both` - Collaborative task
