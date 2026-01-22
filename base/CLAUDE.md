# CLAUDE.md
<!-- Target: <80 lines. Run /health-check --claude-md to check -->

Instructions for Claude Code when working in this project.

## Project Overview

[Brief description of what this project does]

## Task Management

### Difficulty Scale (1-10)
- **1-4**: Standard tasks - just do them
- **5-6**: Substantial tasks - may take multiple steps
- **7-8**: Large scope - MUST break down before starting
- **9-10**: Multi-phase - MUST break down into phases

### Task Status
- **Pending**: Not started
- **In Progress**: Currently working (only one at a time)
- **Blocked**: Cannot proceed (document why)
- **Broken Down**: Split into subtasks (work on subtasks, not this)
- **Finished**: Complete

### Rules
1. Break down tasks with difficulty >= 7 before starting
2. Only one task "In Progress" at a time
3. Run `/sync-tasks` after completing any task
4. Parent tasks auto-complete when all subtasks finish

## Commands

- `/complete-task {id}` - Start and finish tasks (includes work check)
- `/breakdown {id}` - Split complex tasks into subtasks
- `/sync-tasks` - Update task-overview.md from JSON files
- `/health-check` - Combined task system and CLAUDE.md health check
- `/archive-tasks` - Archive old finished tasks (for large projects)
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
    └── difficulty-guide.md # Scoring guide
```

## Technology Stack

[List key technologies, frameworks, languages]

## Conventions

[Project-specific coding conventions, naming patterns, etc.]
