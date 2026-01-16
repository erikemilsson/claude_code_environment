# Claude Code Environment

A ready-to-use project structure for Claude Code with built-in task management.

> **Optimized for Claude Opus 4.5** - Task difficulty and workflow design assume Opus 4.5 capabilities.

## Quick Start

**Get started in 30 seconds:**

```bash
# Copy base folder to your new project
cp -r /path/to/claude_code_environment/base/ /path/to/your-project/

# Edit CLAUDE.md with your project details
# Edit .claude/context/overview.md with project context

# Create your first task and start working
```

That's it. No generation, no templates to choose from, just copy and customize.

## What's Included

```
claude_code_environment/
├── base/                   # Copy this to start a project
│   ├── CLAUDE.md          # Project instructions for Claude
│   ├── README.md          # Project documentation template
│   └── .claude/
│       ├── settings.json  # Pre-configured permissions
│       ├── commands/      # Task management commands
│       ├── context/       # Project context
│       ├── tasks/         # Task tracking
│       └── reference/     # Schema and guides
│
├── extras/                 # Optional add-ons (copy what you need)
│   ├── development/       # Source of truth, assumptions, pitfalls
│   ├── project-management/ # Phases, decisions, handoffs
│   └── advanced/          # Agents, planning workflows
│
├── examples/              # Working examples
│   ├── development-project/  # Generic coding project
│   └── life-project/         # Generic PM project
│
└── docs/                  # Documentation
    ├── README.md          # Getting started
    ├── workflow.md        # Usage workflow
    └── extras-guide.md    # When to use extras
```

## Core Features

### Task Management

Track work with JSON task files:

```json
{
  "id": "1",
  "title": "Implement login",
  "status": "In Progress",
  "difficulty": 5
}
```

### Difficulty Scale

| Level | Description | Action |
|-------|-------------|--------|
| 1-4 | Standard | Just do it |
| 5-6 | Substantial | Multiple steps |
| 7-8 | Large scope | Must break down |
| 9-10 | Multi-phase | Must break down |

### Commands

- `/complete-task {id}` - Start and finish tasks
- `/breakdown {id}` - Split complex tasks
- `/sync-tasks` - Update overview
- `/update-tasks` - Check health

### Rules

1. Break down tasks with difficulty >= 7 before starting
2. Only one task "In Progress" at a time
3. Run `/sync-tasks` after completing tasks
4. Parent tasks auto-complete when subtasks finish

## Workflow

1. **Copy** `base/` to your project
2. **Customize** CLAUDE.md and context/overview.md
3. **Create tasks** in `.claude/tasks/`
4. **Work** using commands to track progress
5. **Add extras** from `extras/` as needed

See `docs/workflow.md` for detailed usage.

## Optional Extras

Copy from `extras/` when you need:

| Folder | Use Case |
|--------|----------|
| `development/` | Source of truth, assumptions, LLM pitfalls |
| `project-management/` | Phases, decisions, handoff guides |
| `advanced/` | Agents, planning workflows |

See `docs/extras-guide.md` for details on when to use each.

## Examples

- **development-project/** - A Todo API project showing task breakdown
- **life-project/** - A kitchen renovation showing project management

## Documentation

- `docs/README.md` - Getting started
- `docs/workflow.md` - Daily usage workflow
- `docs/extras-guide.md` - When to use extras

## Archive

Old templates and bootstrap system are in `.archive/` for reference. Use `base/` instead.

---

**License:** Provided as-is for personal use. Fork and customize as needed.
