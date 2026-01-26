# Archived Components Summary

This document summarizes the modular component library that was consolidated into `base/` and `extras/` in January 2025.

## Why Archived

The component system was **overengineered**:
- Required a composition step during bootstrap
- Added complexity without proportional value
- Most users just wanted everything together
- Maintenance of separate components was tedious

**Replacement**: Essential components are now in `base/`. Optional extras in `extras/`.

## The Five Component Types

### 1. Checkpoint System
**Purpose**: Save and restore project state at specific points

Files:
- `create-checkpoint.md` - Save current state with description
- `list-checkpoints.md` - Show all saved checkpoints
- `diff-checkpoint.md` - Compare current state to checkpoint
- `rollback-to.md` - Restore state from checkpoint

**Pattern**:
```bash
# Create checkpoint before risky changes
/create-checkpoint "Before authentication refactor"

# If things go wrong
/rollback-to "Before authentication refactor"
```

**Current status**: Not migrated to base/extras. Use git branches instead.

### 2. Error Catalog
**Purpose**: Track known errors and their solutions

Provided:
- `error-log.md` - Template for logging errors
- `known-issues.md` - Catalog of known problems
- `troubleshooting.md` - Common solutions

**Pattern**: When an error occurs repeatedly, add it to the catalog with symptoms, cause, and solution for faster resolution.

**Current status**: Not essential. Create project-specific error docs if needed.

### 3. Pattern Library
**Purpose**: Reusable code patterns for common operations

Patterns included:
- `csv-transform.pattern.md` - CSV data transformations
- `excel-read.pattern.md` - Reading Excel files
- `json-parse.pattern.md` - JSON handling
- `power-query-bronze.pattern.md` - PQ bronze layer pattern
- `dax-measure.pattern.md` - DAX measure templates
- `dataflow-gen2.pattern.md` - Dataflow Gen2 patterns

**Pattern structure**:
```markdown
# Pattern: [Name]

## When to Use
[Scenarios where this applies]

## Template
[Code template with placeholders]

## Variations
[Common modifications]

## Anti-patterns
[What to avoid]
```

**Current status**: Create project-specific patterns in `.claude/reference/` as needed.

### 4. Task Management
**Purpose**: Track work with difficulty scoring and automatic completion

Files:
- `complete-task.md` - Start/finish tasks with status tracking
- `breakdown.md` - Split high-difficulty tasks
- `sync-tasks.md` - Update task overview
- `update-tasks.md` - Validate task structure
- `generate-handoff-guide.md` - Create handoff documentation
- `validation-rules.md` - Task validation criteria
- `breakdown-workflow.md` - Guide for breaking down tasks
- `difficulty-guide.md` - How to score task difficulty

**This component IS in base/**: The entire task management system is preserved in `base/.claude/`.

### 5. Validation Gates
**Purpose**: Quality checks before proceeding with work

Gates included:
- Pre-implementation validation
- Pre-commit checks
- Pre-merge validation
- Dependency validation
- Schema validation

**Pattern**:
```markdown
Before starting implementation:
1. Verify all dependencies are met
2. Check that task difficulty is appropriate
3. Confirm context files are loaded
4. Validate assumptions are documented
```

**Current status**: Embedded in command workflows rather than separate component.

## Key Patterns Worth Preserving

### Component Composition
The idea of composable pieces is good. Implementation was too complex.

Better approach: Start with `base/`, add files from `extras/` as needed. No composition step required.

### Difficulty-Based Workflow
From task-management component:
- Difficulty 1-6: Work directly
- Difficulty 7+: Must break down first
- Subtasks should be difficulty <= 6

This is preserved in `base/`.

### Validation as Process
From validation-gates:
- Always validate before starting
- Check context is loaded
- Verify dependencies are met

This is now embedded in command instructions rather than separate gates.

## Migration Path

Components are already absorbed:

| Old Component | Current Location |
|--------------|------------------|
| checkpoint-system | Use git branches |
| error-catalog | Create as needed |
| pattern-library | Create as needed |
| task-management | `base/.claude/` |
| validation-gates | In command workflows |

## Files Deleted

The following directories contained the component implementations:
- `components/checkpoint-system/` (4 command files + README)
- `components/error-catalog/` (3 files + README)
- `components/pattern-library/` (6 pattern files + README)
- `components/task-management/` (8 files)
- `components/validation-gates/` (4 files + README)

Total: ~46 files consolidated into this summary + base/.
