# CLAUDE.md

Instructions for Claude Code when working in this repository.

> **Optimized for Claude Opus 4.5** - This system is calibrated for Opus 4.5's capabilities.

## Repository Purpose

This is a **template repository** for bootstrapping new Claude Code project environments. It contains:

1. **base/** - A minimal, ready-to-copy project structure
2. **extras/** - Optional add-ons for specific use cases
3. **examples/** - Working examples showing the structure in use
4. **docs/** - Documentation for using this system
5. **.claude/** - This repo's own environment (for maintaining this repo)

## Repository Structure

```
claude_code_environment/
├── base/                    # THE copy-paste folder (minimal)
│   ├── CLAUDE.md           # Project instructions template
│   ├── README.md           # Project docs template
│   └── .claude/            # Task management structure
│
├── extras/                  # Optional add-ons
│   ├── development/        # Source of truth, assumptions, pitfalls
│   ├── project-management/ # Phases, decisions, handoffs
│   └── advanced/           # Agents, planning workflows
│
├── examples/               # Working examples
│   ├── development-project/
│   └── life-project/
│
├── docs/                   # Documentation for this repo
├── scripts/                # Utility scripts
├── .claude/                # THIS REPO's environment
└── .archive/               # Old templates, bootstrap system
```

## Core Workflow

**How users start a new project:**

```bash
cp -r /path/to/claude_code_environment/base/ /path/to/new-project/
# Edit CLAUDE.md and .claude/context/overview.md
# Start working
```

No generation, no templates to choose - just copy and customize.

## Task Management

### Difficulty Scale (1-10)
- **1-4**: Standard tasks - just do them
- **5-6**: Substantial tasks - may take multiple steps
- **7-8**: Large scope - MUST break down before starting
- **9-10**: Multi-phase - MUST break down into phases

### Status Values
- **Pending**: Not started
- **In Progress**: Currently working (only one at a time)
- **Blocked**: Cannot proceed (document why)
- **Broken Down**: Split into subtasks
- **Finished**: Complete

### Mandatory Rules

**ALWAYS:**
- Break down tasks with difficulty >= 7 before starting
- Only one task "In Progress" at a time
- Run sync-tasks after completing any task
- Parent tasks auto-complete when subtasks finish

**NEVER:**
- Work on "Broken Down" tasks directly (work on subtasks)
- Skip status updates
- Work on multiple tasks simultaneously

## Working in This Repository

### Modifying base/

The base/ folder should stay minimal. Only add files if they're needed by >80% of projects.

### Adding extras

Add new extras to `extras/` with clear documentation about when to use them.

### Updating examples

Examples should be generic. Keep them simple and illustrative.

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
- `task-schema-consolidated.md` - Task schema
- `parallel-tool-patterns.md` - Parallel execution patterns
- `extended-thinking-triggers.md` - Ultrathink usage
- `context-management.md` - /clear, /compact strategies

## Navigation

- **Understanding base**: See `base/CLAUDE.md`
- **Understanding extras**: See `docs/extras-guide.md`
- **Repository tasks**: See `.claude/tasks/task-overview.md`
- **Archived content**: See `.archive/README.md`

## Quick Reference

### Commands
```
/sync-tasks              # Update task overview
/complete-task {id}      # Start/finish tasks
/breakdown {id}          # Split complex tasks
/tdd-cycle               # Test-driven development
```

### Extended Thinking
- **"think"** - Basic reasoning
- **"think hard"** - Thorough analysis
- **"think harder"** - Deep analysis
- **"ultrathink"** - Maximum depth (difficulty 9-10)

### Context Management
- **`/clear`** - Reset context completely
- **`/compact`** - Compress context while preserving key info
