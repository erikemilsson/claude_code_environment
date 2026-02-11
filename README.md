# Claude Code Environment Template

A ready-to-use project template for Claude Code with Spec→Execute→Verify workflow.

**Designed for Claude Opus 4.6.** The difficulty scale, task breakdown thresholds, and agent workflows are calibrated for Opus-level reasoning. Using a less capable model may result in lower quality output and incorrect difficulty assessments.

## Setup

```bash
# Clone this template
git clone https://github.com/your-username/claude_code_environment.git my-project
cd my-project
rm -rf .git && git init

# Customize for your project
# 1. Edit .claude/CLAUDE.md - Delete the meta section (everything above the ---), then customize
# 2. Create your spec: run /iterate in Claude Code
# 3. Edit this README.md - Replace with your project documentation
```

## What's Included

```
└── .claude/
    ├── CLAUDE.md                  # Instructions for Claude Code
    ├── spec_v{N}.md               # Source of truth: requirements
    ├── dashboard.md               # Project Dashboard (auto-generated)
    ├── tasks/                     # Task data
    │   └── task-*.json            # Individual task files
    ├── commands/                  # Slash commands
    │   ├── work.md                # Main entry point
    │   ├── iterate.md             # Spec review and building
    │   ├── status.md              # Read-only status view
    │   ├── breakdown.md           # Task decomposition
    │   ├── health-check.md        # System health validation
    │   ├── update-template.md     # Template sync
    │   └── setup-check.md         # Template configuration check
    ├── agents/                    # Specialist agents
    │   ├── implement-agent.md     # Builds the solution
    │   └── verify-agent.md        # Validates against spec
    ├── specification_creator/     # Legacy redirect (use /iterate from project root)
    │   ├── CLAUDE.md              # Redirect notice
    │   └── README.md              # Redirect notice
    ├── support/                   # Supporting documentation
    │   ├── reference/             # Schemas, guides, definitions
    │   ├── decisions/             # Decision documentation
    │   │   ├── index.md           # Decision summary
    │   │   ├── decision-*.md      # Individual records
    │   │   └── .archive/          # Research documents
    │   ├── learnings/             # Project-specific patterns
    │   ├── previous_specifications/  # Archived spec versions
    │   ├── workspace/             # Claude's working area (gitignored)
    │   └── questions.md           # Questions for human
    ├── sync-manifest.json
    ├── settings.local.json
    └── version.json
```

## Workflow

```mermaid
flowchart TD
    subgraph DESKTOP["Claude Desktop — Ideation"]
        D1(["Brainstorm concept"])
        D2[/"Vision Document"/]
        D1 --> D2
    end

    D2 -->|"Save to .claude/vision/"| S1

    subgraph SPEC["Claude Code — /iterate"]
        S1(["/iterate distill"])
        S2["Build spec: questions, content, structure"]
        S3{"Ready?"}
        S4[/"Spec v1"/]

        S1 --> S2 --> S3
        S3 -->|"Gaps remain"| S2
        S3 -->|"Ready"| S4
    end

    S4 --> W1

    subgraph EXEC["Claude Code — /work"]
        W1(["/work"])
        W2["Decompose spec into tasks by phase"]
        W3{"Task eligible?"}
        W4["implement-agent builds"]
        W5["verify-agent validates"]
        W6{"More tasks?"}

        W1 --> W2 --> W3
        W3 -->|"Decision unresolved"| W3B["User selects in decision doc"]
        W3B --> W3
        W3 -->|"Clear"| W4 --> W5 --> W6
        W6 -->|"Yes"| W3
        W6 -->|"Phase complete"| PHASE
    end

    PHASE{"All phase tasks done?"}
    PHASE -->|"Next phase"| W1
    PHASE -->|"Last phase"| DONE(["Project Complete"])

    classDef desktop fill:#e8d5f5,stroke:#7c3aed,stroke-width:2px,color:#1a1a1a
    classDef spec fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1a1a1a
    classDef exec fill:#d1fae5,stroke:#059669,stroke-width:2px,color:#1a1a1a
    classDef phase fill:#fef3c7,stroke:#d97706,stroke-width:3px,color:#1a1a1a
    classDef done fill:#bbf7d0,stroke:#16a34a,stroke-width:2px,color:#1a1a1a

    class DESKTOP desktop
    class SPEC spec
    class EXEC exec
    class PHASE phase
    class DONE done
```

**Core principle:** The spec is the living source of truth. All work aligns with it, or the spec is updated intentionally.

### Core Concepts

| Concept | What It Is | Example | Resolved By |
|---------|-----------|---------|-------------|
| **Phase** | Sequential project stage. Phase N+1 blocked until Phase N complete. | "Build pilot first, then production" | All phase tasks finish, next phase unlocks |
| **Decision** | Choice with multiple viable options. Blocks dependent tasks. | "Postgres or SQLite?" | User checks selection in decision doc |
| **Human Task** | Action only the user can do. `/work` skips it. | "Configure the API keys" | User completes it and marks done |
| **Inflection Point** | A decision that changes *what* gets built. | "Monolith or microservices?" | After selection, `/work` pauses and suggests `/iterate` to revisit spec |

You *identify* structure during brainstorming (Claude Desktop), *configure* it during spec building (`/iterate`), and *resolve* it during execution (`/work`). All concepts surface in the dashboard and are handled inline — no separate commands to learn.

For details: [terminology](.claude/support/reference/shared-definitions.md) | [phases & decisions](.claude/support/reference/extension-patterns.md) | [dashboard format](.claude/support/reference/dashboard-patterns.md)

## Creating Specifications

Specifications are created using the `/iterate` command from the project root:

```bash
/iterate                    # Auto-detect what's needed and build the spec
/iterate {topic}            # Focus on a specific area
/iterate distill            # Extract buildable spec from a vision document
```

The iterate command will:
- Guide you through requirement gathering
- Create versioned specs at `.claude/spec_v{N}.md`
- Archive old versions to `.claude/support/previous_specifications/`

Once your spec is ready, run `/work` to begin execution.

## Commands

| Command | Description |
|---------|-------------|
| `/work` | Main entry point - checks spec, decomposes tasks, routes to agents |
| `/work complete` | Complete current in-progress task (or `/work complete {id}`) |
| `/iterate` | Structured spec review (checks gaps, asks questions, suggests content) |
| `/status` | Quick read-only view of project state |
| `/breakdown {id}` | Split complex tasks into subtasks |
| `/health-check` | Validate system health |
| `/update-template` | Check for and apply template updates |
| `/setup-check` | Validate template configuration (run after cloning) |

## License

[Your license here]
