# Archive

This folder contains archived files from the repository reorganization (January 2025).

## What's Here

### templates/

The old template system with 5 template types:
- base
- data-analytics
- documentation-content
- life-projects
- power-query
- research-analysis

**Replaced by**: `base/` folder (single, simple template)

### components/

Modular components designed for template composition:
- checkpoint-system
- error-catalog
- pattern-library
- task-management
- validation-gates

**Replaced by**: Components moved directly into `base/` and `extras/`

### universal-template/

An attempt at a "one size fits all" template with agents, specification development, and executive summaries.

**Replaced by**: `base/` + `extras/advanced/`

### examples/

Old examples including:
- complete-projects (pension calculator)
- project-specific-commands
- specifications

**Replaced by**: `examples/` with generic development-project and life-project

### bootstrap/

The old bootstrap system for generating environments from templates:
- bootstrap.md
- bootstrap-tutorial.md
- show-bootstrap-details.md
- undo-bootstrap.md

**Replaced by**: Simple copy workflow (no generation needed)

### sample-project/

A sample generated project from the bootstrap system.

**Replaced by**: `examples/development-project/`

### Legacy Files

- `legacy-template-reference.md` - Comprehensive reference for old template system
- `PHASE-0-PATTERN.md` - Phase 0 pattern for Power Query projects
- `claude-4-tasks-summary.md` - Task summary documentation

## When to Reference

Only look at archived files if:
- You need to understand historical decisions
- Looking for patterns not yet migrated
- Debugging issues with old templates

## Don't Use

These files are archived, not maintained. Use `base/` and `extras/` instead.
