# Repository Context

## What This Repository Is

A **template repository** for bootstrapping new Claude Code project environments. Contains two copy-paste-ready environments optimized for Claude Opus 4.5.

## Repository Structure

```
claude_code_environment/
├── CLAUDE.md                # Instructions for this repo
├── README.md                # Human documentation
├── lite/                    # Minimal environment (~11 files)
│   ├── CLAUDE.md
│   ├── README.md
│   └── .claude/
│       ├── commands/        # archive-tasks, breakdown, complete-task, restore-task, sync-tasks
│       ├── context/         # overview.md
│       ├── reference/       # shared-definitions, task-schema
│       └── tasks/           # task-overview.md
├── standard/                # Full-featured environment (~22 files)
│   ├── CLAUDE.md
│   ├── README.md
│   └── .claude/
│       ├── agents/          # orchestrator, spec, plan, implement, verify
│       ├── commands/        # + work.md
│       ├── context/         # + phases, decisions, questions
│       ├── reference/       # + agent-handoff, workflow-guide
│       └── tasks/
├── .claude/                 # This repo's own environment
│   ├── commands/            # Core 5 commands
│   ├── context/             # This file
│   ├── reference/           # Core 4 reference docs
│   └── tasks/               # Work tracking
└── .archive/                # Archived content
```

## How Users Use This

```bash
# Simple project - task management only
cp -r /path/to/claude_code_environment/lite/ /path/to/new-project/

# Complex project - full workflow with agents
cp -r /path/to/claude_code_environment/standard/ /path/to/new-project/

# Edit CLAUDE.md and .claude/context/overview.md
# Start working
```

## Two Environments

### lite/
- **Purpose**: Quick start, any project type
- **Features**: Task tracking, breakdown, completion, archiving
- **Best for**: Well-defined projects, minimal overhead

### standard/
- **Purpose**: Complex multi-phase development
- **Features**: Everything in lite/ plus Spec→Plan→Execute→Verify workflow
- **Best for**: Large projects, autonomous multi-phase work

## Working in This Repository

### Modifying lite/
Keep it minimal. Only add files essential for basic task management.

### Modifying standard/
Maintain the Spec→Plan→Execute→Verify flow. Changes should support the agent workflow.

### Archiving
Move deprecated content to `.archive/` with documentation in `.archive/README.md`.

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Instructions for Claude Code working on this repo |
| `README.md` | Human documentation for GitHub visitors |
| `.claude/reference/shared-definitions.md` | Difficulty scale, status values, rules |
| `.claude/reference/task-schema-consolidated.md` | Task JSON schema |
| `.claude/tasks/task-overview.md` | Current work tracking |
| `.archive/README.md` | Index of archived content |

## Conventions

- **No emojis** unless explicitly requested
- **Markdown format** for all documentation
- **Task files**: `task-{id}.json` with sequential IDs
- **Commands**: `{verb}-{noun}.md` format
