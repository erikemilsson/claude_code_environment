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

> **Scope note:** "The project" and "the system" refer to what's being built. The supporting workflow infrastructure in `.claude/` is "the environment."

## How the Environment Works

**Your primary interface is the dashboard** (`.claude/dashboard.md`). Claude tracks tasks in `.claude/tasks/`, implements according to spec, and surfaces decision points. You review and approve at phase boundaries.

For full details, see `.claude/support/reference/system-overview.md`.

## Specification

The project specification lives at `.claude/spec_v{N}.md`.

**Do not edit the specification directly.** If you identify improvements:
1. Quote the relevant section
2. Explain the suggested change
3. Let the user make the edit

To create or revise specifications, run `/iterate`.

## Vision Documents

If you have a vision/design document from ideation (e.g., Claude Desktop brainstorming):

1. Save it to `.claude/vision/`
2. Run `/iterate distill` to extract a buildable spec

Vision docs capture intent and philosophy; specs capture buildable scope. Both are preserved.

## Workflow: Spec → Execute → Verify

This project uses a phased workflow: **Spec** (define requirements) → **Execute** (build via implement-agent) → **Verify** (validate via verify-agent). Two specialist agents check each other's work, eliminating the blind spots of self-validation.

**Primary command:** `/work` - Checks requests against spec, decomposes spec into tasks, routes to specialist agents.

**Core principle:** The spec is the living source of truth. All work aligns with it, or the spec is updated intentionally.

For details on phases, agent handoffs, and checkpoints, see `.claude/support/reference/workflow.md`.

## Environment Commands

Commands defined in `.claude/commands/` for this workflow. Not Claude Code built-ins (`/help`, `/clear`).

### Primary
- `/work` - Start or continue work (checks spec alignment, decomposes tasks, routes to agents)
- `/work complete` - Complete current in-progress task (or `/work complete {id}`)
- `/iterate` - Structured spec review (checks gaps, asks questions, suggests content)
- `/status` - Quick read-only view of project state (no modifications)

### Task Management
- `/breakdown {id}` - Split complex tasks into subtasks
- `/health-check` - Validate tasks, decisions, and CLAUDE.md health
- `/update-template` - Check for and apply template updates

### Setup
- `/setup-check` - Validate template configuration (run after cloning)

## Task Rules

**Important:** Always use the project's task system (`.claude/tasks/task-*.json` files) for all task management. Never use built-in TaskCreate/TaskUpdate/TaskList tools as a replacement — those are separate from this project's tracking.

Tasks are tracked in `.claude/tasks/` as JSON files. The **Project Dashboard** at `.claude/dashboard.md` shows:
- 🚨 **Needs Your Attention** - decisions pending, tasks ready for you, reviews needed
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

Temporary documents go in `.claude/support/workspace/` (scratch, research, drafts). Never create working documents in the project root. See `.claude/support/reference/system-overview.md` for details.

## Project Structure

See `.claude/support/reference/system-overview.md` for the full directory tree and template configuration file documentation.

## Technology Stack

[List key technologies, frameworks, languages]

## Conventions

[Project-specific coding conventions, naming patterns, etc.]
