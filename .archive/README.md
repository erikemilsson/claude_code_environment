# Archive

This folder contains archived content from the repository reorganization (January 2025).

## Structure

```
.archive/
├── README.md                    # This file
├── MIGRATION-2024-12.md         # Historical context for December 2024 cleanup
├── templates-summary.md         # Summary of the old 5-template system
├── components-summary.md        # Summary of the old component library
└── deprecated-schemas/          # Old task schema versions
    ├── task-schema.md
    ├── task-schema-v2.md
    └── enhanced-task-schema.md
```

## What Was Archived

### Templates (69 files)
The old 5-template system (base, data-analytics, documentation-content, life-projects, power-query, research-analysis) was replaced by `base/` + `extras/`.

See `templates-summary.md` for details.

### Components (46 files)
The modular component library (checkpoint-system, error-catalog, pattern-library, task-management, validation-gates) was consolidated into `base/` and `extras/`.

See `components-summary.md` for details.

### Other Deletions
- `scripts/` (19 files) - Python automation, overengineered
- `test/` (24 files) - Tests for deprecated machinery
- `examples/` (51 files) - Replaced by `/examples/`
- `sample-project/` (13 files) - Replaced by `examples/development-project/`
- `universal-template/` (24 files) - Replaced by `base/` + `extras/advanced/`
- `docs/` (3 files) - Merged into root README
- `bootstrap/` (4 files) - Replaced by simple copy workflow
- `legacy-commands/` (1 file) - Obsolete bootstrap command
- `historical-docs/` - Was empty

## When to Reference

Only reference archived files if:
- Understanding historical decisions
- Looking for patterns not yet migrated
- Researching why something was changed

## Don't Use

These files are archived and not maintained. Use `base/` and `extras/` instead.
