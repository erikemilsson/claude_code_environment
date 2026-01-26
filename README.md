# Claude Code Environment

A ready-to-use project structure for Claude Code with built-in task management.

> **Optimized for Claude Opus 4.5** - Task difficulty and workflow design assume Opus 4.5 capabilities.

## Quick Start

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
└── examples/              # Working examples
    ├── development-project/  # Generic coding project
    └── life-project/         # Generic PM project
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
- `/health-check` - Check health

### Rules

1. Break down tasks with difficulty >= 7 before starting
2. Only one task "In Progress" at a time
3. Run `/sync-tasks` after completing tasks
4. Parent tasks auto-complete when subtasks finish

## Daily Workflow

### Starting work
1. Review `.claude/tasks/task-overview.md` for pending tasks
2. Pick a task to work on

### Working on a task
1. Run `/complete-task {id}` to mark as In Progress
2. Do the work
3. Run `/complete-task {id}` again to mark as Finished
4. Run `/sync-tasks` to update overview

### Breaking down complex tasks
For difficulty >= 7:
1. Run `/breakdown {id}` - creates subtasks with difficulty <= 6
2. Work on subtasks instead of parent
3. Parent auto-completes when all subtasks finish

## Optional Extras

Copy from `extras/` only when needed. Start simple.

### development/
For software projects:
- **source-of-truth-template.md** - When multiple docs sources exist
- **assumptions-template.md** - Track decisions made with incomplete info
- **llm-pitfalls-template.md** - Domain-specific LLM mistakes to avoid

Copy to: `.claude/context/`

### project-management/
For tracking phases and decisions:
- **phases-template.md** - Distinct project phases with inputs/outputs
- **decisions-template.md** - Document rationale for choices
- **handoff-guide-command.md** - Tasks split between Claude and human

Copy to: `.claude/context/` or `.claude/commands/`

### advanced/
For complex projects needing agents or specification development. Most projects don't need this.

## Examples

- **development-project/** - A Todo API project showing task breakdown
- **life-project/** - A kitchen renovation showing project management

## Tips

- **Keep tasks focused** - One task = one deliverable
- **Use notes** - Track what was done, issues encountered, follow-ups
- **Sync frequently** - Run `/sync-tasks` after completing or breaking down tasks
- **Don't over-engineer** - The base/ template is sufficient for most projects

---

**License:** Provided as-is for personal use. Fork and customize as needed.
