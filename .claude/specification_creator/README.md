# Specification Creator

> **Note:** The `/iterate` command has moved to the project root. You no longer need to start a separate Claude Code session here.

## How to Create Specifications

From your project root directory, run:

```bash
/iterate                    # Auto-detect what's needed and build the spec
/iterate {topic}            # Focus on a specific area
/iterate distill            # Extract buildable spec from a vision document
```

## Specification Format

```yaml
---
version: {N}
status: active | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## What Lives Here

This directory is kept for backward compatibility. The active components have moved:

| Was Here | Now At |
|----------|--------|
| `commands/iterate.md` | `.claude/commands/iterate.md` (project root commands) |
| `reference/spec-checklist.md` | `.claude/support/reference/spec-checklist.md` |

The `.archive/` directory remains available for spec-session working documents.

## Full Documentation

- **Iterate command**: `.claude/commands/iterate.md`
- **Spec readiness**: `.claude/support/reference/spec-checklist.md`
- **Workflow guide**: `.claude/support/reference/workflow.md`
