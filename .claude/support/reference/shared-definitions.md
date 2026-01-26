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

## Priority Values

See `task-schema.md` for full priority definitions. Summary:

| Value | Emoji | Meaning |
|-------|-------|---------|
| critical | 🔴 | Blocking other work, immediate attention |
| high | 🟠 | Important, should be done soon |
| medium | (none) | Normal priority (default) |
| low | (none) | Nice to have, do when time permits |

Priority affects sorting in Ready sections (critical → high → medium → low).
Only critical and high show emoji prefixes in the dashboard.

## Task JSON Structure

See `task-schema.md` for complete field definitions including timeline fields (priority, due_date, milestone, external_dependency).

### Minimal Task
```json
{
  "id": "1",
  "title": "Brief description",
  "status": "Pending",
  "difficulty": 3
}
```

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

Tasks have an `owner` field that determines responsibility and dashboard placement:

| Value | Emoji | Dashboard Section | When to Use |
|-------|-------|-------------------|-------------|
| `claude` | 🤖 | Claude Status | Autonomous work (default when omitted) |
| `human` | ❗ | Your Actions | Requires human action |
| `both` | 👥 | Both sections | Collaborative work |

**Human tasks** - Configure secrets, make decisions, external actions, review/approve
**Claude tasks** - Write code, implement features, tests, docs, research
**Both tasks** - Human provides direction, Claude implements (appears in BOTH dashboard sections with 👥)

## Task ID Conventions

| Pattern | Meaning | Example |
|---------|---------|---------|
| `N` | Top-level task | `1`, `2`, `3` |
| `N_M` | Sequential subtask | `1_1`, `1_2` (must do in order) |
| `N_Ma` | Parallel subtask | `1_1a`, `1_1b` (can do simultaneously) |

Use underscores for sequential dependencies, letters for parallel work within a sequence.
