# Shared Definitions

Single source of truth for task management definitions. Referenced by CLAUDE.md and commands.

## Difficulty Scale (1-10)

| Level | Category | Action |
|-------|----------|--------|
| 1-4 | Standard | Just do it |
| 5-6 | Substantial | May take multiple steps |
| 7-8 | Large scope | MUST break down first |
| 9-10 | Multi-phase | MUST break down into phases |

> See `task-schema-consolidated.md` for detailed examples by level.

## Status Values

| Status | Meaning | Rules |
|--------|---------|-------|
| Pending | Not started | Ready to work on |
| In Progress | Currently working | Only ONE at a time |
| Blocked | Cannot proceed | Document blocker in notes |
| Broken Down | Split into subtasks | Work on subtasks, not this |
| Finished | Complete | Auto-set when subtasks done |

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

## Task JSON Structure (Minimal)

```json
{
  "id": "1",
  "title": "Brief description",
  "status": "Pending",
  "difficulty": 3
}
```

> See `task-schema-consolidated.md` for full field definitions.
