# CLAUDE.md

Instructions for Claude Code when working in this repository.

> **Optimized for Claude Opus 4.5** - This system is calibrated for Opus 4.5's capabilities.

## Repository Purpose

This is a **template repository** for bootstrapping new Claude Code project environments. It contains two complete, copy-paste-ready environments:

1. **lite/** - Minimal task management (~11 files)
2. **standard/** - Full-featured with Spec→Plan→Execute→Verify workflow (~22 files)

## Repository Structure

```
claude_code_environment/
├── lite/                    # Quick start, task management only
│   ├── CLAUDE.md           # Simple project instructions
│   ├── README.md           # Project docs template
│   └── .claude/            # Commands, context, reference, tasks
│
├── standard/               # Full-featured for complex projects
│   ├── CLAUDE.md          # Full workflow instructions
│   ├── README.md          # Project docs template
│   └── .claude/           # Commands, agents, context, reference, tasks
│
├── .claude/                # THIS REPO's own environment
└── .archive/               # Old templates, extras, examples
```

## Core Workflow

**How users start a new project:**

```bash
# Simple project
cp -r /path/to/claude_code_environment/lite/ /path/to/new-project/

# Complex project
cp -r /path/to/claude_code_environment/standard/ /path/to/new-project/

# Edit CLAUDE.md and .claude/context/overview.md
# Start working
```

## Task Management

See `.claude/reference/shared-definitions.md` for difficulty scale, status values, and mandatory rules.

**Key rules**:
- Break down tasks with difficulty >= 7 before starting
- Only one task "In Progress" at a time
- Run `/sync-tasks` after completing any task

## Working in This Repository

### Modifying lite/

The lite/ folder should stay minimal. Only add files if they're essential for basic task management.

### Modifying standard/

The standard/ folder contains the full workflow. Changes should maintain the Spec→Plan→Execute→Verify flow.

### Archiving

Move deprecated content to `.archive/` with documentation in `.archive/README.md`.

## Tool Usage

**Prefer parallel execution** when operations are independent:
- Multiple Read operations in single message
- Independent Bash commands simultaneously
- Multiple Grep/Glob searches concurrently

**Use specialized tools** instead of Bash:
- Read (not cat) for reading files
- Write (not echo) for creating files
- Edit (not sed) for modifying files
- Glob (not find) for file patterns
- Grep (not grep/rg) for content search

## Reference Documentation

Key files in `.claude/reference/`:
- `shared-definitions.md` - Difficulty scale, status values, mandatory rules
- `task-schema-consolidated.md` - Task JSON schema
- `context-management.md` - /clear, /compact strategies
- `extended-thinking-triggers.md` - Ultrathink usage

## Navigation

- **Understanding lite**: See `lite/CLAUDE.md`
- **Understanding standard**: See `standard/CLAUDE.md`
- **Repository tasks**: See `.claude/tasks/task-overview.md`
- **Archived content**: See `.archive/README.md`

## Quick Reference

### Commands
```
/sync-tasks              # Update task overview
/complete-task {id}      # Start/finish tasks
/breakdown {id}          # Split complex tasks
/archive-tasks           # Archive completed tasks
/restore-task {id}       # Restore from archive
```

### Extended Thinking
- **"think"** - Basic reasoning
- **"think hard"** - Thorough analysis
- **"think harder"** - Deep analysis
- **"ultrathink"** - Maximum depth (difficulty 9-10)

### Context Management
- **`/clear`** - Reset context completely
- **`/compact`** - Compress context while preserving key info
