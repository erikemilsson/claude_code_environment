# Reference Files

Documentation that Claude reads during workflow execution and on-demand guidance for specific situations.

## Core (read by commands/agents during execution)

| File | Purpose |
|------|---------|
| `shared-definitions.md` | Status values, difficulty scale, owner types, glossary of all terms |
| `task-schema.md` | JSON schema for task files |
| `workflow.md` | Spec→Execute→Verify process, parallel execution, verification tiers, system overview, project structure |
| `paths.md` | Canonical file locations — prevents Claude from inventing paths |
| `dashboard-regeneration.md` | Dashboard regeneration procedure, section format reference, critical path, project overview diagram |
| `drift-reconciliation.md` | Spec drift detection, reconciliation UI, drift budget, task migration |
| `parallel-execution.md` | Parallelism eligibility, file conflict algorithm, parallel dispatch |

## Guides (read on-demand for specific situations)

| File | Purpose |
|------|---------|
| `decisions.md` | Decision record template, lifecycle, choice classification (spec vs implementation) |
| `spec-checklist.md` | Spec readiness criteria, red flags, core questions |
| `extension-patterns.md` | Phases and decisions patterns for complex projects |
| `setup-checklist.md` | Template configuration checks (CLAUDE.md placeholders, version.json), run during decomposition |
| `desktop-project-prompt.md` | Instructions for Claude Desktop ideation sessions |

## Related READMEs (in sibling directories)

| File | Purpose |
|------|---------|
| `../learnings/README.md` | Categories, format, and maintenance guidelines for project-specific learnings |
| `../workspace/README.md` | Directory rules, file placement guide, and graduation process for temporary files |
