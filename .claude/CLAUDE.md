# CLAUDE.md

Instructions for Claude Code when working in this project.

## Model Requirement

This environment is designed for **Claude Opus 4.6** (`claude-opus-4-6`). The difficulty scale, task breakdown thresholds, and agent workflows are calibrated for Opus-level reasoning. All agents (implement-agent, verify-agent, research-agent) must run on Opus 4.6.

## Project Overview

[Brief description of what this project does]

> **Scope note:** "The project" and "the system" refer to what's being built. The supporting workflow infrastructure in `.claude/` is "the environment."

## Design Philosophy

This environment is domain-agnostic. It works for software development, research, procurement, renovation, event planning, or any spec-driven project. Dashboard language, task tracking, and verification adapt to the project domain — no code-specific assumptions are built in.

## How the Environment Works

**The dashboard is your navigation hub** (`.claude/dashboard.md`). During the build phase, Claude surfaces what needs your attention — decisions to make, files to review, actions to take — with links to the specific files that need it. You click through to inspect files directly, but the dashboard guides you there so you don't need to browse `.claude/` on your own. The dashboard is the primary hub during active development; post-completion activities may involve more direct interaction.

The dashboard has a **Sections** checklist at the top — check or uncheck items to control which sections Claude generates during `/work`. Custom Views is optional and defaults to unchecked.

**Note:** The dashboard ships as a populated format example (a fictional renovation project). On first `/work` run after spec decomposition, it is replaced with your actual project data. The example exists so Claude can see exactly what format to produce.

**Interaction modes:** Not everything routes through the dashboard. For synchronous tasks (testing a CLI, confirming output, quick yes/no), Claude presents them directly in the CLI conversation. For async tasks (document review, design decisions, phase gates), the dashboard remains the hub. Verify-agent also self-tests runnable outputs (CLIs, APIs, web UIs) before asking you to test — you only verify what Claude genuinely can't evaluate on its own. See `.claude/support/reference/workflow.md` § "Interaction Modes and Runtime Validation".

For full details, see `.claude/support/reference/workflow.md` § "System Overview".

## Specification

The project specification lives at `.claude/spec_v{N}.md` (exactly one file; `/work` discovers N by globbing).

**Propose-approve-apply for spec changes.** Present changes as explicit declarations (what changes, where, proposed text); apply only after user approval. You CAN perform infrastructure operations autonomously (archiving, version transitions, frontmatter updates). See `commands/iterate.md` § "Propose-Approve-Apply Boundary".

**Direct edits to the spec are always safe** — the decomposed snapshot preserves the before-state, and drift detection handles reconciliation. After a spec edit, the user runs `/work` to continue building (detects changes and reconciles affected tasks) or `/iterate` to keep refining.

To create or revise specifications, run `/iterate`.

## Vision Documents

Every project starts with ideation. A vision document is required before spec creation.

1. Brainstorm in Claude Desktop (or any tool) — explore features, phases, key decisions, constraints
2. Save the result to `.claude/vision/`
3. Run `/iterate distill` to extract a buildable spec

Vision docs capture intent and philosophy; specs capture buildable scope. Both are preserved. Vision docs can be added throughout the project lifecycle — the vision folder is a living input, not a one-time artifact.

**Starting from Claude Desktop?** See `support/reference/desktop-project-prompt.md` for project instructions that guide ideation sessions to produce well-structured vision documents aligned with this workflow.

## Workflow: Spec → Execute → Verify

Phased workflow: **Spec** (define requirements) → **Execute** (implement-agent) → **Verify** (verify-agent). Specialist agents with separated concerns ensure quality through independent validation.

**Primary command:** `/work` - Checks requests against spec, decomposes spec into tasks, routes to specialist agents.

**Core principle:** The spec is the living source of truth. All work aligns with it, or the spec is updated intentionally.

**Parallel execution** is the default: when `/work` finds multiple pending tasks with no mutual dependencies or file conflicts, it dispatches them concurrently. Each task still runs the full implement → verify cycle. Configure via `parallel_execution` in spec frontmatter.

For details on phases, agent handoffs, parallel execution, and checkpoints, see `.claude/support/reference/workflow.md`.

## Environment Commands

Commands defined in `.claude/commands/` for this workflow. Not Claude Code built-ins (`/help`, `/clear`).

### Primary
- `/work` - Start or continue work (checks spec alignment, decomposes tasks, checks gates, resolves decisions, routes to agents)
- `/work complete` - Complete current in-progress task (or `/work complete {id}`)
- `/iterate` - Structured spec review and refinement (checks gaps, asks questions, proposes spec changes)
- `/review` - Implementation quality review (architecture, integration, patterns — purely advisory)
- `/status` - Quick read-only view of project state (no modifications)
- `/research` - Investigate options for decisions (populates comparison matrices, writes research archives)
- `/feedback` - Capture and manage project improvement ideas (quick capture, review, triage)

### Task Management
- `/breakdown {id}` - Split complex tasks into subtasks
- `/health-check` - Validate tasks, decisions, CLAUDE.md health, and template sync

## Task Rules

**Important:** Always use the project's task system (`.claude/tasks/task-*.json` files) for all task management. Never use built-in TaskCreate/TaskUpdate/TaskList tools as a replacement — those are separate from this project's tracking.

Tasks are tracked in `.claude/tasks/` as JSON files. The **Project Dashboard** at `.claude/dashboard.md` is your navigation hub during the build phase — it surfaces what needs attention with links to specific files:
- 🚨 **Action Required** — everything Claude needs from you: decisions, tasks, reviews — with links and completion signals
- 📊 **Progress** — phase breakdown, critical path, timeline, and recent activity
- 📋 **Tasks** — full task list by phase
- 📋 **Decisions** — decision log with status
- 💡 **Notes** — your preserved notes section
- Optional: **Custom Views** (toggle via Sections checklist)

**Key rules:**
- Break down tasks with difficulty >= 7 before starting
- Multiple tasks "In Progress" allowed when parallel-eligible (no file conflicts, deps satisfied)
- Dashboard regenerates automatically after task changes

See `.claude/support/reference/shared-definitions.md` for difficulty scale, status values, and mandatory rules. See `.claude/support/reference/task-schema.md` for owner values, priority values, and all JSON field definitions.

## Decisions

Major decisions are documented in `.claude/support/decisions/`.

- **Dashboard tracks all decisions** - Status, pending items, and timeline in one place
- **Records:** `decision-*.md` - full analysis with comparison tables
- **Research:** `.claude/support/decisions/.archive/` - background research documents
- **Reference:** `.claude/support/reference/decisions.md`

When facing significant choices, create a decision record rather than deciding inline.

## Feedback

Fleeting ideas and improvement thoughts go in `.claude/support/feedback/`.

- **Quick capture:** `/feedback [text]` — save an idea without losing context
- **Review:** `/feedback review` — triage unreviewed items interactively
- **Spec integration:** Refined feedback surfaces in `/iterate` for incorporation
- **Archive:** Items that aren't relevant are archived with reasons in `archive.md`
- **Reference:** `.claude/support/feedback/README.md`

## Workspace

Temporary documents go in `.claude/support/workspace/` (scratch, research, drafts). Never create working documents in the project root. See `.claude/support/workspace/README.md` for directory rules and file placement guide.

## Documents

User-provided reference files (PDFs, contracts, vendor docs, permits, etc.) go in `.claude/support/documents/`. When the user provides a file path, move it there with a descriptive filename. See `.claude/support/documents/README.md` for conventions.

**Credentials and secrets:** Never commit API keys, passwords, tokens, or credentials to any tracked file. Use environment variables or a `.env` file (which must be in `.gitignore`). If a task requires secrets, set `owner: "human"` for the credential setup step.

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

## Technology Stack / Tools

[List key technologies, frameworks, tools, or services used in this project]

## Conventions

[Project-specific conventions, naming patterns, document formats, etc.]

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
