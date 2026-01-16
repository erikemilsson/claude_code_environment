# Claude Code Environment Documentation

This repository provides a ready-to-use project structure for Claude Code with built-in task management.

## Quick Start

### 1. Copy the base folder

```bash
cp -r /path/to/claude_code_environment/base/ /path/to/your-project/
```

### 2. Customize for your project

Edit these files:
- `CLAUDE.md` - Add your project overview, tech stack, conventions
- `.claude/context/overview.md` - Add project context and notes

### 3. Start working

Create your first task:
```json
// .claude/tasks/task-1.json
{
  "id": "1",
  "title": "Your first task",
  "status": "Pending",
  "difficulty": 3
}
```

Run `/sync-tasks` to update the task overview.

## What's Included

### base/

A minimal, ready-to-use project structure:

```
base/
├── CLAUDE.md              # Project instructions for Claude Code
├── README.md              # Project documentation template
└── .claude/
    ├── settings.json      # Pre-configured permissions
    ├── commands/          # Task management commands
    │   ├── complete-task.md
    │   ├── breakdown.md
    │   ├── sync-tasks.md
    │   └── update-tasks.md
    ├── context/
    │   └── overview.md    # Project context
    ├── tasks/
    │   └── task-overview.md
    └── reference/
        ├── task-schema.md
        └── difficulty-guide.md
```

### extras/

Optional add-ons you can copy as needed:

- **development/** - Source of truth, assumptions, LLM pitfalls templates
- **project-management/** - Phases, decisions, handoff guides
- **advanced/** - Agents, planning workflows (for complex projects)

### examples/

Working examples showing the structure in use:

- **development-project/** - A generic coding project (Todo API)
- **life-project/** - A generic PM project (Kitchen renovation)

## Core Concepts

### Task Management

Tasks track what needs to be done. Each task has:
- **id**: Unique identifier
- **title**: Brief description
- **status**: Pending, In Progress, Blocked, Broken Down, Finished
- **difficulty**: 1-10 scale

### Difficulty Scale

| Level | Description | Action |
|-------|-------------|--------|
| 1-4 | Standard | Just do it |
| 5-6 | Substantial | May take multiple steps |
| 7-8 | Large scope | Must break down |
| 9-10 | Multi-phase | Must break down |

### Commands

- `/complete-task {id}` - Start and finish tasks
- `/breakdown {id}` - Split complex tasks into subtasks
- `/sync-tasks` - Update overview from JSON files
- `/update-tasks` - Check task system health

## Next Steps

- See [workflow.md](workflow.md) for detailed usage workflow
- See [extras-guide.md](extras-guide.md) for when to use extras
