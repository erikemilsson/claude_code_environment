# Archive

This folder contains archived content from repository reorganizations.

## Structure

```
.archive/
├── README.md                    # This file
├── root-claude-extras-2026-01-26/  # Root .claude/ simplification
│   ├── commands/               # 19 extra commands
│   ├── reference/              # 28+ extra reference docs
│   └── directories/            # 12 subsystem directories
├── deprecated-schemas/          # Old task schema versions
├── tasks/                       # Completed task JSON files (180 files)
├── phase-docs/                  # Phase planning documents
├── analysis-templates/          # Analysis templates and reports
├── extras/                      # Archived January 2026 - replaced by standard/
│   ├── development/
│   ├── project-management/
│   └── advanced/
└── examples/                    # Archived January 2026 - replaced by lite/ and standard/
    ├── development-project/
    └── life-project/
```

## January 2026 Reorganization

### Root .claude/ Simplification (2026-01-26)
The root `.claude/` directory was simplified to mirror the lite/ template:
- **Kept:** 5 core commands, 4 reference docs, tasks
- **Archived:** 19 commands, 28+ reference docs, 12 subsystem directories
- See `root-claude-extras-2026-01-26/README.md` for details

### Template Restructure (2026-01-26)
The repository was restructured from `base/` + `extras/` + `examples/` to two complete environments:
- **lite/** - Minimal task management only (~11 files)
- **standard/** - Full-featured with Spec→Plan→Execute→Verify workflow (~22 files)

### extras/ (14 files)
Optional add-ons that were complex to integrate. Now consolidated into `standard/`:
- `development/` - Source of truth, assumptions, pitfalls templates
- `project-management/` - Phases, decisions, handoffs
- `advanced/` - Agents and planning workflows

### examples/ (44 files)
Working examples that showed the old structure in use. Replaced by the copy-paste-ready environments themselves.

## January 2025 Reorganization

### Completed Tasks (180 files)
All completed task JSON files moved from `.claude/tasks/` to `tasks/`. Only active (pending/blocked) tasks remain in `.claude/tasks/`.

### Phase Documents (6 files)
Phase planning documents (phase1-4) and duplicate task-overview-observability.md archived to `phase-docs/`.

### Analysis Templates (3 files)
Analysis directory contents archived to `analysis-templates/`. These were maintenance-mode templates.

### Empty Directories Removed
- `.claude/checkpoints/` - Never used
- `.claude/locks/` - Never used
- `.claude/shared-context/` - Never used
- `.claude/tasks/archive/` - Empty

## December 2024 Reorganization

### Templates (69 files)
The old 5-template system was replaced by `base/` + `extras/`.

### Components (46 files)
The modular component library was consolidated into `base/` and `extras/`.

### Other Deletions
- `scripts/` (19 files) - Python automation
- `test/` (24 files) - Tests for deprecated machinery
- `sample-project/` (13 files)
- `universal-template/` (24 files)
- `docs/` (3 files)
- `bootstrap/` (4 files)
- `legacy-commands/` (1 file)

## When to Reference

Only reference archived files if:
- Understanding historical decisions
- Looking for patterns not yet migrated
- Researching why something was changed

## Don't Use

These files are archived and not maintained. Use `lite/` or `standard/` instead.
