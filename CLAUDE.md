# CLAUDE.md

> **Template Repository**: This file serves dual purposes.
> - Working on this repo? See "Maintaining This Template" below.
> - Using as template? Delete everything above the separator line.

## Maintaining This Template

Instructions for working on the claude_code_environment repository itself:

- **Purpose**: Template for bootstrapping Claude Code projects
- **Keep minimal**: Resist adding project-specific content
- **Test changes**: Copy to temp directory and verify workflow works
- **Placeholders**: Use `[bracketed text]` for user-customizable sections

### What NOT to do

- Don't fill in template placeholders with real content
- Don't add files that aren't essential to the template
- Don't add project-specific conventions

---
<!-- DELETE EVERYTHING ABOVE THIS LINE WHEN USING AS TEMPLATE -->

# CLAUDE.md

Instructions for Claude Code when working in this project.

## Project Overview

[Brief description of what this project does]

## Specification

The project specification lives at `.claude/spec_v{N}.md`.

**Do not edit the specification directly.** If you identify improvements:
1. Quote the relevant section
2. Explain the suggested change
3. Let the user make the edit

To create or revise specifications, start a Claude Code instance from `.claude/specification_creator/`.

## Workflow: Spec → Execute → Verify

This project uses a phased workflow for autonomous work:

1. **Spec** - Define what needs to be built (requirements, constraints, acceptance criteria, key decisions)
2. **Execute** - Build it (tasks decomposed from spec, implementation)
3. **Verify** - Confirm it works (testing, validation against spec)

**Primary command:** `/work` - Intelligent entry point that checks requests against spec, decomposes spec into tasks, and routes to specialist agents.

**Core principle:** The spec is the living source of truth. All work should align with it, or the spec should be updated intentionally.

**Human checkpoints:** At phase boundaries, quality gate failures, and when requests don't align with spec.

## Commands

### Primary
- `/work` - Start or continue work (checks spec alignment, decomposes tasks, routes to agents)

### Task Management
- `/complete-task {id}` - Start and finish tasks
- `/breakdown {id}` - Split complex tasks into subtasks
- `/sync-tasks` - Update task-overview.md from JSON files
- `/health-check` - Validate tasks, decisions, and CLAUDE.md health
- `/archive-tasks` - Archive old finished tasks
- `/restore-task {id}` - Restore a task from archive

## Task Rules

Tasks are tracked in `.claude/tasks/` as JSON files.

**Key rules:**
- Break down tasks with difficulty >= 7 before starting
- Only one task "In Progress" at a time
- Run `/sync-tasks` after completing any task

See `.claude/reference/shared-definitions.md` for difficulty scale and status values.

## Decisions

Major decisions are documented in `.claude/context/decisions/`.

- **Index:** `index.md` - all decisions with status
- **Records:** `decision-*.md` - full analysis with comparison tables
- **Research:** `.archive/` - background research documents
- **Template:** `.claude/reference/decision-template.md`

When facing significant choices, create a decision record rather than deciding inline.

## Project Structure

```
.claude/
├── spec_v{N}.md               # Project specification (source of truth)
├── previous_specifications/   # Archived spec versions
├── specification_creator/     # Start Claude Code here for spec sessions
│   ├── CLAUDE.md             # Rules for spec-building mode
│   └── README.md
├── commands/                  # /work and task commands
├── agents/                    # Specialist agents
│   ├── implement-agent.md    # Task execution
│   └── verify-agent.md       # Validation against spec
├── context/
│   ├── overview.md           # Project context
│   ├── phases.md             # Phase definitions and status
│   ├── decisions/            # Decision documentation
│   │   ├── index.md          # Decision summary and pending
│   │   ├── decision-*.md     # Individual decision records
│   │   └── .archive/         # Research documents
│   └── questions.md          # Accumulated questions for human
├── learnings/                 # Project-specific patterns (ask Claude to check)
│   └── README.md             # Usage guide
├── reference/
│   ├── task-schema.md        # Task JSON format
│   ├── shared-definitions.md
│   ├── workflow-guide.md     # Workflow explained
│   ├── agent-handoff.md      # Agent coordination
│   ├── decision-template.md  # Decision record format
│   └── decision-guide.md     # Decision documentation guide
└── tasks/
    ├── task-*.json           # Individual task files
    └── task-overview.md      # Auto-generated summary
```

## Technology Stack

[List key technologies, frameworks, languages]

## Conventions

[Project-specific coding conventions, naming patterns, etc.]
