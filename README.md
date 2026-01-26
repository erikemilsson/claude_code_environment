# Claude Code Environment

Ready-to-use project structures for Claude Code with built-in task management.

> **Optimized for Claude Opus 4.5** - Task difficulty and workflow design assume Opus 4.5 capabilities.

## Quick Start

Choose an environment and copy it to your project:

```bash
# For simple projects - task management only
cp -r /path/to/claude_code_environment/lite/ /path/to/your-project/

# For complex projects - full workflow with agents
cp -r /path/to/claude_code_environment/standard/ /path/to/your-project/
```

Edit `CLAUDE.md` with your project details and start working.

## Two Environments

### lite/ (~11 files)

**Best for:** Quick start, simple projects, any project type

Task management only:
- Track work with JSON task files
- Break down complex tasks
- Sync task overview
- Archive old tasks

```
lite/
├── CLAUDE.md
├── README.md
└── .claude/
    ├── commands/     # breakdown, complete-task, sync-tasks, etc.
    ├── context/      # overview.md
    ├── reference/    # task-schema, shared-definitions
    └── tasks/        # task-overview.md
```

### standard/ (~22 files)

**Best for:** Large projects, autonomous multi-phase work, complex development

Everything in lite/ plus:
- **Spec → Plan → Execute → Verify** workflow
- `/work` command as single entry point
- Specialist agents (orchestrator, spec, plan, implement, verify)
- Phase tracking and decision logging
- Question accumulation for batch human review

```
standard/
├── CLAUDE.md
├── README.md
└── .claude/
    ├── commands/     # work, breakdown, complete-task, etc.
    ├── agents/       # orchestrator, spec, plan, implement, verify
    ├── context/      # overview, phases, decisions, questions
    ├── reference/    # workflow-guide, agent-handoff, task-schema
    └── tasks/        # task-overview.md
```

## Core Concepts

### Task Management (Both Environments)

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

**lite/ commands:**
- `/complete-task {id}` - Start and finish tasks
- `/breakdown {id}` - Split complex tasks
- `/sync-tasks` - Update overview
- `/archive-tasks` - Archive old tasks
- `/restore-task {id}` - Restore from archive

**standard/ adds:**
- `/work` - Context-aware entry point (analyzes state, routes to agents)

### Rules

1. Break down tasks with difficulty >= 7 before starting
2. Only one task "In Progress" at a time
3. Run `/sync-tasks` after completing tasks
4. Parent tasks auto-complete when subtasks finish

## Workflow

### lite/ Workflow

1. Review `task-overview.md` for pending tasks
2. Run `/complete-task {id}` to start
3. Do the work
4. Run `/complete-task {id}` to finish
5. Run `/sync-tasks` to update overview

### standard/ Workflow

1. Run `/work` - analyzes project state
2. Routes to appropriate phase (Spec → Plan → Execute → Verify)
3. Agent does focused work, accumulates questions
4. Human checkpoint at phase boundaries
5. Continue until complete

## Which to Choose?

**Use lite/ when:**
- Starting a new project quickly
- Project scope is well-defined
- Don't need phase tracking
- Want minimal overhead

**Use standard/ when:**
- Building something complex
- Requirements need refinement
- Want autonomous multi-phase work
- Need decision tracking and question batching

## Tips

- **Start with lite/** - You can always add standard/ features later
- **Keep tasks focused** - One task = one deliverable
- **Use notes** - Track what was done, issues encountered
- **Sync frequently** - Run `/sync-tasks` after completing tasks

---

**License:** Provided as-is for personal use. Fork and customize as needed.
