# System Overview

Reference documentation for the environment builder system. Moved here from CLAUDE.md to keep the main instructions file focused on project-specific configuration.

## How This System Works

**Your primary interface is the dashboard** (`.claude/dashboard.md`). It shows everything you need:
- What needs your attention (decisions, reviews, blockers)
- What Claude is working on
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
