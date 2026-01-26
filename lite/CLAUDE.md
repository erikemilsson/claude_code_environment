# CLAUDE.md

Instructions for Claude Code when working in this project.

## Project Overview

[Brief description of what this project does]

## Task Management

Tasks are tracked in `.claude/tasks/` as JSON files.

**Key rules:**
- Break down tasks with difficulty >= 7 before starting
- Only one task "In Progress" at a time
- Run `/sync-tasks` after completing any task

See `.claude/reference/shared-definitions.md` for difficulty scale and status values.

## Commands

- `/complete-task {id}` - Start and finish tasks
- `/breakdown {id}` - Split complex tasks into subtasks
- `/sync-tasks` - Update task-overview.md from JSON files
- `/health-check` - Validate task system and CLAUDE.md health
- `/archive-tasks` - Archive old finished tasks
- `/restore-task {id}` - Restore a task from archive

## Project Structure

```
.claude/
├── commands/          # Task management commands
├── context/
│   └── overview.md    # Project context and notes
├── reference/
│   ├── task-schema.md       # Task JSON format
│   └── shared-definitions.md # Difficulty, status, rules
└── tasks/
    ├── task-*.json        # Individual task files
    └── task-overview.md   # Auto-generated summary
```

## Technology Stack

[List key technologies, frameworks, languages]

## Conventions

[Project-specific coding conventions, naming patterns, etc.]
