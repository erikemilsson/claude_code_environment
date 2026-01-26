# Claude Code Environment Template

A ready-to-use project template for Claude Code with Spec→Execute→Verify workflow.

## Setup

```bash
# Clone this template
git clone https://github.com/your-username/claude_code_environment.git my-project
cd my-project
rm -rf .git && git init

# Customize for your project
# 1. Edit CLAUDE.md - Delete the meta section (everything above the ---), then customize
# 2. Create your spec: cd .claude/specification_creator && claude
# 3. Edit this README.md - Replace with your project documentation
```

## What's Included

```
├── CLAUDE.md                      # Instructions for Claude Code
└── .claude/
    ├── spec_v{N}.md               # Source of truth: requirements
    ├── tasks/                     # Source of truth: work status
    │   ├── task-*.json            # Individual task files
    │   └── task-overview.md       # Project Dashboard (auto-generated)
    ├── commands/                  # Slash commands
    │   ├── work.md                # Main entry point
    │   ├── complete-task.md       # Task completion
    │   ├── breakdown.md           # Task decomposition
    │   ├── sync-tasks.md          # Update task overview
    │   ├── health-check.md        # System health validation
    │   ├── archive-tasks.md       # Archive old tasks
    │   └── restore-task.md        # Restore archived tasks
    ├── agents/                    # Specialist agents
    │   ├── implement-agent.md     # Builds the solution
    │   └── verify-agent.md        # Validates against spec
    ├── specification_creator/     # Separate environment for spec building
    │   ├── CLAUDE.md              # Rules for spec-building mode
    │   └── README.md              # How to use
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

1. **Spec** - Create specification using the specification_creator (see below)
2. **Execute** - Implement (tasks decomposed from spec by /work)
3. **Verify** - Validate against acceptance criteria

Use `/work` to start or continue work. Claude checks requests against the spec, decomposes tasks, and routes to the appropriate agent.

**Core principle:** The spec is the living source of truth. All work aligns with it, or the spec is updated intentionally.

## Creating Specifications

Specifications are created in a separate Claude Code environment to keep spec-building focused:

```bash
cd .claude/specification_creator
claude   # Start Claude Code here
```

This gives you a dedicated session for defining requirements without implementation distractions. The specification_creator will:
- Guide you through requirement gathering
- Create versioned specs at `.claude/spec_v{N}.md`
- Archive old versions to `.claude/support/previous_specifications/`

Once your spec is ready, return to the main project directory and run `/work` to begin execution.

## Commands

| Command | Description |
|---------|-------------|
| `/work` | Main entry point - analyzes state, routes to agent |
| `/complete-task {id}` | Start and finish tasks |
| `/breakdown {id}` | Split complex tasks into subtasks |
| `/sync-tasks` | Update task-overview.md |
| `/health-check` | Validate system health |
| `/archive-tasks` | Archive completed tasks |
| `/restore-task {id}` | Restore from archive |

## License

[Your license here]
