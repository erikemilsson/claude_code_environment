# Claude Code Environment Template

A ready-to-use project template for Claude Code with Spec→Execute→Verify workflow.

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

1. **Spec** - Create specification using `/iterate` (see below)
2. **Execute** - Implement (tasks decomposed from spec by /work)
3. **Verify** - Validate against acceptance criteria

Use `/work` to start or continue work. Claude checks requests against the spec, decomposes tasks, and routes to the appropriate agent.

**Core principle:** The spec is the living source of truth. All work aligns with it, or the spec is updated intentionally.

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
