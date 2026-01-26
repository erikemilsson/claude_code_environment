# Claude Code Environment Template

A ready-to-use project template for Claude Code with Spec→Plan→Execute→Verify workflow.

## Setup

```bash
# Clone this template
git clone https://github.com/your-username/claude_code_environment.git my-project
cd my-project
rm -rf .git && git init

# Customize for your project
# 1. Edit CLAUDE.md - Add project description, tech stack, conventions
# 2. Edit .claude/context/overview.md - Add specification and context
# 3. Edit this README.md - Replace with your project documentation
```

## What's Included

```
├── CLAUDE.md                 # Instructions for Claude Code
└── .claude/
    ├── agents/               # Specialist agents for each phase
    │   ├── orchestrator.md   # Routes to appropriate agent
    │   ├── spec-agent.md     # Defines requirements
    │   ├── plan-agent.md     # Designs implementation
    │   ├── implement-agent.md # Builds the solution
    │   └── verify-agent.md   # Validates against spec
    ├── commands/             # Slash commands
    │   ├── work.md           # Main entry point
    │   ├── complete-task.md  # Task completion
    │   ├── breakdown.md      # Task decomposition
    │   ├── sync-tasks.md     # Update task overview
    │   ├── archive-tasks.md  # Archive old tasks
    │   └── restore-task.md   # Restore archived tasks
    ├── context/
    │   ├── overview.md       # Project specification
    │   ├── phases.md         # Phase status tracking
    │   ├── decisions.md      # Decision log
    │   └── questions.md      # Questions for human
    ├── reference/
    │   ├── shared-definitions.md  # Difficulty scale, status values
    │   ├── task-schema.md         # Task JSON format
    │   ├── workflow-guide.md      # Workflow documentation
    │   └── agent-handoff.md       # Agent coordination
    └── tasks/
        └── task-overview.md  # Task summary (auto-generated)
```

## Workflow

1. **Spec** - Define requirements in `.claude/context/overview.md`
2. **Plan** - Design architecture and create tasks
3. **Execute** - Implement following the plan
4. **Verify** - Validate against acceptance criteria

Use `/work` to start or continue work. Claude analyzes the current state and routes to the appropriate phase.

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
