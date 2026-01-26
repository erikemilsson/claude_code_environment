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

## How This System Works

**Your primary interface is the dashboard** (`.claude/dashboard.md`). It shows everything you need:
- What needs your attention (decisions, reviews, blockers)
- What Claude is working on
- Timeline and upcoming deadlines
- Progress and recent activity

**What you do:**
- Write code and documentation (outside `.claude/`)
- Make decisions when Claude surfaces options
- Review and approve at phase boundaries
- Update the spec when requirements change

**What Claude does:**
- Tracks tasks and progress (in `.claude/tasks/`)
- Implements according to spec
- Surfaces decision points to you
- Validates work against acceptance criteria

**You shouldn't need to dig into `.claude/` internals** - the dashboard brings everything to you.

## Specification

The project specification lives at `.claude/spec_v{N}.md`.

**Do not edit the specification directly.** If you identify improvements:
1. Quote the relevant section
2. Explain the suggested change
3. Let the user make the edit

To create or revise specifications, start a Claude Code instance from `.claude/specification_creator/`.

## Workflow: Spec → Execute → Verify

This project uses a phased workflow: **Spec** (define requirements) → **Execute** (build via implement-agent) → **Verify** (validate via verify-agent). Two specialist agents check each other's work, eliminating the blind spots of self-validation.

**Primary command:** `/work` - Checks requests against spec, decomposes spec into tasks, routes to specialist agents.

**Core principle:** The spec is the living source of truth. All work aligns with it, or the spec is updated intentionally.

For details on phases, agent handoffs, and checkpoints, see `.claude/support/reference/workflow.md`.

## Commands

### Primary
- `/work` - Start or continue work (checks spec alignment, decomposes tasks, routes to agents)
- `/work complete` - Complete current in-progress task (or `/work complete {id}`)
- `/status` - Quick read-only view of project state (no modifications)

### Task Management
- `/breakdown {id}` - Split complex tasks into subtasks
- `/health-check` - Validate tasks, decisions, and CLAUDE.md health

### Setup
- `/setup-check` - Validate template configuration (run after cloning)

## Task Rules

Tasks are tracked in `.claude/tasks/` as JSON files. The **Project Dashboard** at `.claude/dashboard.md` shows:
- 🚨 **Needs Your Attention** - decisions pending, tasks ready for you, reviews needed
- 🎯 **Milestones** - project phase progress and targets
- ⏰ **Timeline** - upcoming deadlines and milestones
- 🤖 **Claude Status** - what Claude is working on
- 📊 **Progress This Week** - recent completions and activity
- 📋 **All Decisions** - decision log with status
- 📝 **All Tasks** - full task list with details
- 💡 **Notes & Ideas** - your preserved notes section

**Key rules:**
- Break down tasks with difficulty >= 7 before starting
- Only one task "In Progress" at a time
- Dashboard regenerates automatically after task changes

See `.claude/support/reference/shared-definitions.md` for difficulty scale, status values, and owner definitions.

## Decisions

Major decisions are documented in `.claude/support/decisions/`.

- **Dashboard tracks all decisions** - Status, pending items, and timeline in one place
- **Records:** `decision-*.md` - full analysis with comparison tables
- **Research:** `.archive/` - background research documents
- **Template:** `.claude/support/reference/decision-template.md`

When facing significant choices, create a decision record rather than deciding inline.

## Workspace

When you need to create temporary documents (research, analysis, drafts), use `.claude/support/workspace/`:

- **scratch/** - Throwaway notes, quick analysis, temporary thinking
- **research/** - Web search results, reference material, gathered context
- **drafts/** - Work-in-progress documents before they move to their final location

**Rules:**
- Never create working documents in the project root or other locations
- Use simple descriptive names (`api-comparison.md`, not `task-5-research.md`)
- When a draft is ready to become permanent, discuss where it should go

## Template Configuration Files

Two files control template behavior:

### sync-manifest.json

Defines which files sync from template updates vs stay project-specific:

| Category | Purpose | Examples |
|----------|---------|----------|
| `sync` | Updated from template | Commands, agents, reference docs |
| `customize` | User-editable, template provides defaults | CLAUDE.md, README.md, questions.md |
| `ignore` | Project-specific data, never synced | Tasks, dashboard, decision records, learnings |

### settings.local.json

Pre-approved permissions for consistent Claude Code behavior. Ensures the template works the same way for everyone using it. Contains tool permissions that would otherwise require per-session approval.

## Project Structure

```
.claude/
├── dashboard.md               # Project Dashboard (auto-generated)
├── spec_v{N}.md               # Project specification (source of truth)
├── tasks/                     # Task data
│   ├── task-*.json           # Individual task files
│   └── milestone-*.json      # Milestone definitions
├── commands/                  # /work and task commands
├── agents/                    # Specialist agents
│   ├── implement-agent.md    # Task execution
│   └── verify-agent.md       # Validation against spec
├── specification_creator/     # Start Claude Code here for spec sessions
│   ├── CLAUDE.md             # Rules for spec-building mode
│   └── README.md
├── support/                   # Supporting documentation
│   ├── reference/            # Schemas, guides, definitions
│   │   ├── task-schema.md
│   │   ├── shared-definitions.md
│   │   ├── workflow.md
│   │   ├── decision-template.md
│   │   └── decision-guide.md
│   ├── decisions/            # Decision documentation
│   │   ├── decision-*.md     # Individual decision records
│   │   └── .archive/         # Research documents
│   ├── learnings/            # Project-specific patterns
│   │   └── README.md
│   ├── previous_specifications/  # Archived spec versions
│   ├── workspace/            # Claude's working area (gitignored)
│   │   ├── scratch/          # Temporary notes, quick analysis
│   │   ├── research/         # Web search results, reference material
│   │   └── drafts/           # WIP docs before final location
│   └── questions.md          # Accumulated questions for human
├── sync-manifest.json
├── settings.local.json
└── version.json
```

## Technology Stack

[List key technologies, frameworks, languages]

## Conventions

[Project-specific coding conventions, naming patterns, etc.]
