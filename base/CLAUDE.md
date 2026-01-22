# CLAUDE.md
<!-- Target: <80 lines. Run /health-check --claude-md to check -->

Instructions for Claude Code when working in this project.

## Project Overview

[Brief description of what this project does]

## Task Management

See `.claude/reference/shared-definitions.md` for:
- Difficulty scale (1-10) with breakdown rules
- Status values and their meanings
- Mandatory task workflow rules

**Key rule**: Break down tasks with difficulty >= 7 before starting.

## Commands

- `/complete-task {id}` - Start and finish tasks (includes work check)
- `/breakdown {id}` - Split complex tasks into subtasks
- `/sync-tasks` - Update task-overview.md from JSON files
- `/health-check` - Combined task system and CLAUDE.md health check
- `/archive-tasks` - Archive old finished tasks (for large projects)
- `/restore-task {id}` - Restore a task from archive
- `/generate-workflow-diagram` - Visual Claude/Human task diagram
- `/check-work` - Review session changes for issues and fix them

## Project Structure

```
.claude/
├── commands/          # Task management commands
├── context/
│   └── overview.md    # Project context and notes
├── tasks/
│   ├── task-*.json        # Individual task files
│   ├── task-overview.md   # Auto-generated summary
│   └── workflow-diagram.md # Visual diagram (if 20+ tasks)
└── reference/
    ├── task-schema.md     # Task JSON format
    ├── difficulty-guide.md # Scoring guide
    └── claude-md-guide.md  # CLAUDE.md best practices
```

## Technology Stack

[List key technologies, frameworks, languages]

## Conventions

[Project-specific coding conventions, naming patterns, etc.]
