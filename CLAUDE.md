# CLAUDE.md

Instructions for Claude Code when working in this project.

## Project Overview

[Brief description of what this project does]

## Workflow: Spec → Plan → Execute → Verify

This project uses a phased workflow for autonomous work:

1. **Spec** - Define what needs to be built (requirements, constraints, acceptance criteria)
2. **Plan** - Design how to build it (architecture, tasks, dependencies)
3. **Execute** - Build it (implementation, following the plan)
4. **Verify** - Confirm it works (testing, validation against spec)

**Primary command:** `/work` - Context-aware entry point that determines the current phase and routes to the appropriate agent.

**Human checkpoints:** At phase boundaries and quality gate failures.

## Commands

### Primary
- `/work` - Start or continue work (analyzes state, routes to appropriate agent)

### Task Management
- `/complete-task {id}` - Start and finish tasks
- `/breakdown {id}` - Split complex tasks into subtasks
- `/sync-tasks` - Update task-overview.md from JSON files
- `/health-check` - Validate task system, semantic drift, and CLAUDE.md health
- `/archive-tasks` - Archive old finished tasks
- `/restore-task {id}` - Restore a task from archive

## Task Rules

Tasks are tracked in `.claude/tasks/` as JSON files with phase tracking.

**Key rules:**
- Break down tasks with difficulty >= 7 before starting
- Only one task "In Progress" at a time
- Run `/sync-tasks` after completing any task

See `.claude/reference/shared-definitions.md` for difficulty scale and status values.

## Project Structure

```
.claude/
├── commands/          # /work and task commands
├── agents/            # Specialist agents
│   ├── orchestrator.md
│   ├── spec-agent.md
│   ├── plan-agent.md
│   ├── implement-agent.md
│   └── verify-agent.md
├── context/
│   ├── overview.md    # Project context
│   ├── phases.md      # Phase definitions and status
│   ├── decisions.md   # Decision log
│   └── questions.md   # Accumulated questions for human
├── reference/
│   ├── task-schema.md       # Task JSON format (with phases)
│   ├── shared-definitions.md
│   ├── workflow-guide.md    # Workflow explained
│   └── agent-handoff.md     # Agent coordination
└── tasks/
    ├── task-*.json        # Individual task files
    └── task-overview.md   # Auto-generated summary
```

## Technology Stack

[List key technologies, frameworks, languages]

## Conventions

[Project-specific coding conventions, naming patterns, etc.]
