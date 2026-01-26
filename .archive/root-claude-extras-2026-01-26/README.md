# Archived Root .claude/ Extras

**Archived:** 2026-01-26

Content moved from root `.claude/` directory during simplification. The root environment now mirrors the lite/ template structure.

## What Was Archived

### commands/ (19 files)
Extra commands beyond core task management:
- analyze-patterns, apply-fix, audit-claude-md, check-risks, create-spec
- explore-plan-code-commit, log-decision, monitor, review-file, run-diagnosis
- show-commands, show-dashboard, show-health, tdd-cycle, update-tasks
- use-agent, validate-assumptions, validate-spec, view-dashboard

### reference/ (28+ files)
Extra reference docs beyond core:
- Agent integration guides
- Coding guidelines (js, python, sql, powerquery)
- Workflow guides (headless, multi-claude, visual-iteration)
- Schema migration guides
- Template customization guides

### directories/ (12 directories)
Entire subsystems:
- agents/, agent-docs/ - Agent definitions
- analyzers/ - Python analysis scripts
- dashboard/, monitor/ - Monitoring system
- decisions/, insights/ - Tracking systems
- scripts/ - Python utilities
- sop/ - Standard operating procedures
- system/ - System context files
- tests/, validation/ - Testing infrastructure

### Root files
- agent-config.json
- MONITORING.md
- settings.local.json

## Restoration

To restore any of these, copy back to `.claude/`:

```bash
cp -r .archive/root-claude-extras-2026-01-26/commands/monitor.md .claude/commands/
```
