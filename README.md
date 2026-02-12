# Claude Code Environment Template

A ready-to-use project template for Claude Code with a structured Spec → Execute → Verify workflow.

**Designed for Claude Opus 4.6.** The difficulty scale, task breakdown thresholds, and agent workflows are calibrated for Opus-level reasoning.

## Using This Template

```bash
# Clone and start a new project
git clone https://github.com/your-username/claude_code_environment.git my-project
cd my-project
rm -rf .git && git init

# Customize
# 1. Fill in the placeholder sections in .claude/CLAUDE.md (Project Overview, Tech Stack, Conventions)
# 2. Delete this README.md, tests/, and root CLAUDE.md (template maintenance files)
# 3. Run /iterate in Claude Code to create your spec
```

## What Ships vs. What Doesn't

The `.claude/` directory is the environment — it ships to new projects. Everything at root level is template maintenance infrastructure that you delete when starting a project.

```
├── README.md              # Template docs (delete in projects)
├── CLAUDE.md              # Template maintenance context (delete in projects)
├── system-overview.md     # Environment design reference (delete in projects)
├── tests/                 # Command verification scenarios (delete in projects)
└── .claude/               # ← This is what ships to new projects
    ├── README.md          # Environment guide — how it works, essential files
    ├── CLAUDE.md          # Instructions for Claude Code
    ├── spec_v{N}.md       # Source of truth: requirements
    ├── dashboard.md       # Project Dashboard (auto-generated)
    ├── tasks/             # Task data
    ├── commands/          # Slash commands (/work, /iterate, etc.)
    ├── agents/            # Specialist agents (implement, verify)
    └── support/           # Reference docs, decisions, workspace
```

See `.claude/README.md` for full documentation on the environment itself — commands, concepts, workflow, and file reference.

## Maintaining This Template

See root `CLAUDE.md` for Claude-specific maintenance instructions (what to do, what not to do, file boundaries).

### Testing

Conceptual test scenarios in `tests/scenarios/` verify that command definitions handle decisions, phases, and session resilience correctly. Run them after significant changes to `/work`, `/iterate`, or `/health-check`. See `tests/README.md` for details.

## License

[Your license here]
