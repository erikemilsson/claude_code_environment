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
    ├── spec_v{N}.md               # Active project specification
    ├── previous_specifications/   # Archived spec versions
    ├── specification_creator/     # Separate environment for spec building
    │   ├── CLAUDE.md              # Rules for spec-building mode
    │   └── README.md              # How to use
    ├── agents/                    # Specialist agents
    │   ├── implement-agent.md     # Builds the solution
    │   └── verify-agent.md        # Validates against spec
    ├── commands/                  # Slash commands
    │   ├── work.md                # Main entry point
    │   ├── complete-task.md       # Task completion
    │   ├── breakdown.md           # Task decomposition
    │   ├── sync-tasks.md          # Update task overview
    │   ├── health-check.md        # System health validation
    │   ├── archive-tasks.md       # Archive old tasks
    │   └── restore-task.md        # Restore archived tasks
    ├── context/
    │   ├── overview.md            # Project context
    │   ├── phases.md              # Phase status tracking
    │   ├── decisions/             # Decision documentation
    │   │   ├── index.md           # Decision summary
    │   │   └── decision-*.md      # Individual records
    │   └── questions.md           # Questions for human
    ├── reference/
    │   ├── shared-definitions.md  # Difficulty scale, status values
    │   ├── task-schema.md         # Task JSON format
    │   ├── workflow-guide.md      # Workflow documentation
    │   ├── agent-handoff.md       # Agent coordination
    │   ├── decision-template.md   # Decision record format
    │   └── decision-guide.md      # Decision documentation guide
    └── tasks/
        └── task-overview.md       # Task summary (auto-generated)
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
- Archive old versions to `.claude/previous_specifications/`

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
