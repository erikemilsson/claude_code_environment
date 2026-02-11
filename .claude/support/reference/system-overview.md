# System Overview

Reference documentation for the environment builder system. Moved here from `.claude/CLAUDE.md` to keep the main instructions file focused on project-specific configuration.

## How This System Works

### Design Principle: Dashboard as Communication Hub

During the build phase, **the dashboard is how Claude communicates with you**. It's not just a status display — it's the place where Claude tells you what it needs and where you tell Claude what you've decided.

**The contract:**
- If Claude needs your input, it shows up in the dashboard — with a link to the relevant file, a description of what to do, and a way to signal back (checkbox, feedback area)
- You should always be able to open the dashboard and know your next action
- You don't need to browse `.claude/` internals to understand what's happening

**This is pragmatic, not rigid.** The dashboard is the primary channel during active development (Spec → Execute → Verify). Post-completion activities or exploration may involve more direct interaction. The goal is clarity about what needs your attention, not preventing you from looking at files.

### What you do
- Review the dashboard for your next action
- Click through to linked files when needed (review a document, configure something, test a feature)
- Signal completion back through the dashboard (checkboxes, feedback sections)
- Update the spec when requirements change
- Make decisions when Claude surfaces options

### What Claude does
- Tracks tasks and progress (in `.claude/tasks/`)
- Implements according to spec
- Surfaces everything user-facing through the dashboard — action items with links, not buried in internal files
- Validates work against acceptance criteria
- Regenerates the dashboard after every significant change

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
| `customize` | User-editable, template provides defaults | `.claude/CLAUDE.md`, README.md, questions.md |
| `ignore` | Project-specific data, never synced | Tasks, dashboard, decision records, learnings |

### settings.local.json

Pre-approved permissions for consistent Claude Code behavior. Ensures the template works the same way for everyone using it. Contains tool permissions that would otherwise require per-session approval.

## Project Structure

```
.claude/
├── CLAUDE.md                  # Instructions for Claude Code
├── dashboard.md               # Project Dashboard (auto-generated)
├── verification-result.json   # Latest verification outcome (written by verify-agent)
├── spec_v{N}.md               # Project specification (source of truth)
├── vision/                    # Vision documents from ideation
│   └── {project}-vision.md   # Design philosophy, future roadmap
├── tasks/                     # Task data
│   └── task-*.json           # Individual task files
├── commands/                  # /work and task commands
├── agents/                    # Specialist agents
│   ├── implement-agent.md    # Task execution
│   └── verify-agent.md       # Validation against spec
├── specification_creator/     # Legacy redirect (use /iterate from project root)
│   ├── CLAUDE.md             # Redirect notice
│   └── README.md
├── support/                   # Supporting documentation
│   ├── reference/            # Schemas, guides, definitions
│   │   ├── task-schema.md
│   │   ├── shared-definitions.md
│   │   ├── workflow.md
│   │   ├── spec-checklist.md
│   │   ├── decision-template.md
│   │   └── decision-guide.md
│   ├── decisions/            # Decision documentation
│   │   ├── decision-*.md     # Individual decision records
│   │   └── .archive/         # Research documents
│   ├── learnings/            # Project-specific patterns
│   │   └── README.md
│   ├── previous_specifications/  # Spec snapshots at decomposition (for drift detection)
│   ├── workspace/            # Claude's working area (gitignored)
│   │   ├── scratch/          # Temporary notes, quick analysis
│   │   ├── research/         # Web search results, reference material
│   │   └── drafts/           # WIP docs before final location
│   └── questions.md          # Accumulated questions for human
├── sync-manifest.json
├── settings.local.json
└── version.json
```
