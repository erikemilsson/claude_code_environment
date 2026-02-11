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

## Model Requirement

This environment is designed for **Claude Opus 4.6** (`claude-opus-4-6`). The difficulty scale, task breakdown thresholds, and agent workflows are calibrated for Opus-level reasoning. All agents (implement-agent, verify-agent) must run on Opus 4.6.

## Project Overview

[Brief description of what this project does]

> **Scope note:** "The project" and "the system" refer to what's being built. The supporting workflow infrastructure in `.claude/` is "the environment."

## How the Environment Works

**The dashboard is your communication channel with Claude** (`.claude/dashboard.md`). During the build phase (Spec → Execute → Verify), everything Claude needs from you is surfaced there: decisions to make, files to review, actions to take. You should always be able to open the dashboard and see what your next action is.

**How it works in practice:**
- Claude tracks tasks, implements code, and runs verification autonomously
- When Claude needs your input, it appears in the dashboard — with links to the relevant files, checkboxes to confirm actions, and space for feedback
- You click through to files when needed, then signal completion back through the dashboard
- You don't need to browse `.claude/` internals to understand what's happening

**This is pragmatic, not rigid.** The dashboard is the primary communication hub during active development. Post-completion activities (testing, deployment) may involve more direct interaction. Claude should surface information through the dashboard when it makes sense, not force everything through it artificially.

For full details, see `.claude/support/reference/workflow.md` § "System Overview".

## Specification

The project specification lives at `.claude/spec_v{N}.md` (exactly one file; `/work` discovers N by globbing).

**Do not author spec content directly.** If you identify improvements:
1. Quote the relevant section
2. Explain the suggested change
3. Let the user make the edit

**You CAN perform spec infrastructure operations** — archiving, copying during version transitions, updating frontmatter version numbers and dates. The boundary is authorship (deciding what to build) vs infrastructure (managing files). See `iterate.md` § "Suggest-Only Boundary" for details.

To create or revise specifications, run `/iterate`.

## Vision Documents

If you have a vision/design document from ideation (e.g., Claude Desktop brainstorming):

1. Save it to `.claude/vision/`
2. Run `/iterate distill` to extract a buildable spec

Vision docs capture intent and philosophy; specs capture buildable scope. Both are preserved.

**Starting from Claude Desktop?** See `support/reference/desktop-project-prompt.md` for project instructions that guide ideation sessions to produce well-structured vision documents aligned with this workflow.

## Workflow: Spec → Execute → Verify

This project uses a phased workflow: **Spec** (define requirements) → **Execute** (build via implement-agent) → **Verify** (validate via verify-agent). Two specialist agents check each other's work, eliminating the blind spots of self-validation.

**Primary command:** `/work` - Checks requests against spec, decomposes spec into tasks, routes to specialist agents.

**Core principle:** The spec is the living source of truth. All work aligns with it, or the spec is updated intentionally.

**Parallel execution** is the default: when `/work` finds multiple pending tasks with no mutual dependencies or file conflicts, it dispatches them concurrently. Each task still runs the full implement → verify cycle. Configure via `parallel_execution` in spec frontmatter.

For details on phases, agent handoffs, parallel execution, and checkpoints, see `.claude/support/reference/workflow.md`.

## Environment Commands

Commands defined in `.claude/commands/` for this workflow. Not Claude Code built-ins (`/help`, `/clear`).

### Primary
- `/work` - Start or continue work (checks spec alignment, decomposes tasks, checks gates, resolves decisions, routes to agents)
- `/work complete` - Complete current in-progress task (or `/work complete {id}`)
- `/iterate` - Structured spec review (checks gaps, asks questions, suggests content, discovers project structure)
- `/status` - Quick read-only view of project state (no modifications)

### Task Management
- `/breakdown {id}` - Split complex tasks into subtasks
- `/health-check` - Validate tasks, decisions, and CLAUDE.md health
- `/update-template` - Check for and apply template updates

### Setup
- `/setup-check` - Validate template configuration (run after cloning)

## Task Rules

**Important:** Always use the project's task system (`.claude/tasks/task-*.json` files) for all task management. Never use built-in TaskCreate/TaskUpdate/TaskList tools as a replacement — those are separate from this project's tracking.

Tasks are tracked in `.claude/tasks/` as JSON files. The **Project Dashboard** at `.claude/dashboard.md` is your communication channel with Claude during the build phase:
- 🚨 **Needs Your Attention** - everything Claude needs from you: decisions, tasks, reviews — with links to relevant files and ways to respond
- 🤖 **Claude Status** - what Claude is working on
- 📊 **Progress This Week** - recent completions and activity
- 📋 **All Decisions** - decision log with status
- 📝 **All Tasks** - full task list with details
- 💡 **Notes & Ideas** - your preserved notes section

**Key rules:**
- Break down tasks with difficulty >= 7 before starting
- Multiple tasks "In Progress" allowed when parallel-eligible (no file conflicts, deps satisfied)
- Dashboard regenerates automatically after task changes

See `.claude/support/reference/shared-definitions.md` for difficulty scale, status values, and owner definitions.

## Decisions

Major decisions are documented in `.claude/support/decisions/`.

- **Dashboard tracks all decisions** - Status, pending items, and timeline in one place
- **Records:** `decision-*.md` - full analysis with comparison tables
- **Research:** `.archive/` - background research documents
- **Reference:** `.claude/support/reference/decisions.md`

When facing significant choices, create a decision record rather than deciding inline.

## Workspace

Temporary documents go in `.claude/support/workspace/` (scratch, research, drafts). Never create working documents in the project root. See `.claude/support/reference/workflow.md` § "Workspace" for details.

## Archiving Rules

Archived files have specific locations. Do not create new archive locations.

| What | Archive Location | When |
|------|------------------|------|
| Spec versions | `.claude/support/previous_specifications/spec_v{N}.md` | Before creating v{N+1} |
| Decomposed specs | `.claude/support/previous_specifications/spec_v{N}_decomposed.md` | After task decomposition |
| Completed tasks | `.claude/tasks/archive/` | When task count exceeds 100 |

See `.claude/support/reference/paths.md` for all canonical paths.

## Project Structure

See `.claude/support/reference/workflow.md` § "Project Structure" for the full directory tree and template configuration file documentation.

## Technology Stack

[List key technologies, frameworks, languages]

## Conventions

[Project-specific coding conventions, naming patterns, etc.]

## Glossary

`.claude/support/reference/shared-definitions.md` contains the glossary — canonical definitions for all environment terminology. Definitions are already present in context within the files you read during normal workflow — only reference the glossary section when explicitly working with concept definitions or aligning reference files.

## Project Structure Patterns

Patterns for organizing work in complex projects. Phases are implicit from spec structure; decisions are always available.

### Phases

Structure work into sequential stages where Phase N+1 can't begin until Phase N is complete.

- **Purpose:** Enforce natural project boundaries (prototype→production, data pipeline→visualization)
- **How it works:** Spec sections define phases. Tasks get a `phase` field during decomposition. Dashboard groups tasks by phase with per-phase progress.
- **No special configuration needed** — phases emerge from spec structure
- **Docs:** [extension-patterns.md#phases](support/reference/extension-patterns.md#phases)

### Decisions

Track choices with comparison matrices, option details, optional weighted scoring, and a checkbox selection mechanism.

- **Purpose:** Document and resolve choices that block downstream work
- **Features:** Comparison matrix, option analysis, optional weighted scoring, checkbox selection in the decision doc
- **Pick-and-go vs inflection point:** Most decisions simply unblock tasks when resolved. An **inflection point** decision changes what gets built — after resolution, `/work` pauses and suggests running `/iterate` to revisit the spec.
- **Docs:** [extension-patterns.md#decisions](support/reference/extension-patterns.md#decisions)
