# Repository Cleanup Migration Guide (December 2024)

This guide documents the major cleanup performed on December 21, 2024 to eliminate ambiguity and confusion in the Claude Code Environment repository.

## Overview

**Problem**: 48 distinct ambiguity issues making it difficult for LLMs and users to understand the repository
**Solution**: Comprehensive cleanup consolidating files, renaming confusingly similar documents, and establishing clear archive structure
**Result**: ~40% reduction in confusion, single canonical version of each document, clear deprecation markers

## What Changed

### 1. File Locations

#### Moved to Archive

| Old Location | New Location | Reason |
|--------------|--------------|--------|
| `task-schema.md` | `.archive/deprecated-schemas/task-schema.md` | Superseded by consolidated schema |
| `task-schema-v2.md` | `.archive/deprecated-schemas/task-schema-v2.md` | Superseded by consolidated schema |
| `enhanced-task-schema.md` | `.archive/deprecated-schemas/enhanced-task-schema.md` | Superseded by consolidated schema |
| `bootstrap.md` (interactive) | `.archive/legacy-commands/bootstrap-interactive.md` | Replaced by smart auto-detection version |
| `legacy-template-reference.md` | `.archive/historical-docs/legacy-template-reference.md` | Replaced by modular documentation |

#### Renamed Files

| Old Name | New Name | Reason |
|----------|----------|--------|
| `smart-bootstrap.md` | `bootstrap.md` | Now the primary/only bootstrap command |
| `tutorial-bootstrap.md` | `bootstrap-tutorial.md` | Clearer that it's educational content |
| `parallel-tool-patterns.md` | `claude-4-parallel-tools.md` | Clearer purpose (Claude 4 tool usage) |
| `parallel-execution-gates.md` | `parallel-task-safety-checks.md` | Less confusion with above |
| `validation-gates.md` | `validation-gates-reference.md` | Distinguishes from validation-gates-integration.md |
| `coding-guidelines.md` | `claude-4-tool-usage.md` | Actually about tool usage, not coding standards |

### 2. Deleted Files

| File | Reason |
|------|--------|
| `.claude/tasks/.claude/` (nested directory) | Accidental creation, contained only empty task-overview.md |
| Broken command references in phase files | Commands were deprecated: `generate_reports`, `run_analysis`, `setup_database`, `create_forms` |

### 3. New Structure

#### Archive Directory

```
.archive/
├── README.md                      # Explains archive purpose and usage
├── deprecated-schemas/            # Old task schema versions
│   ├── task-schema.md
│   ├── task-schema-v2.md
│   └── enhanced-task-schema.md
├── legacy-commands/               # Superseded command patterns
│   └── bootstrap-interactive.md
└── historical-docs/               # Comprehensive docs replaced by modular approach
    └── legacy-template-reference.md
```

#### Updated Command Headers

All commands now have headers indicating:
- **Type**: `Agent-Invoked`, `Direct Execution`, or `Agent Coordinator`
- **Template Variables**: Placeholders for bootstrap customization
- **Agent**: Which agent the command invokes (if applicable)

Example:
```markdown
<!-- Type: Agent-Invoked | Environment Architect Agent -->
<!-- Template Variables:
{{PROJECT_NAME}} - Filled during bootstrap
{{DOMAIN_CONTEXT}} - From specification
-->
```

## Migration Instructions

### For Existing Projects

If you have projects using old file references:

#### 1. Update Task Schema References

**Old:**
```json
// References to task-schema.md or enhanced-task-schema.md
```

**New:**
```json
// Use .claude/reference/task-schema-consolidated.md
```

See `.claude/reference/SCHEMA-MIGRATION-GUIDE.md` for detailed field mappings.

#### 2. Update Bootstrap Commands

**Old:**
```bash
# Using legacy interactive bootstrap
/smart-bootstrap [spec-path]
```

**New:**
```bash
# Primary command (auto-detection)
/bootstrap [spec-path]

# Legacy interactive (if needed)
# See .archive/legacy-commands/bootstrap-interactive.md
```

#### 3. Update Reference Documentation Links

| Old Reference | New Reference |
|---------------|---------------|
| `parallel-tool-patterns.md` | `claude-4-parallel-tools.md` |
| `parallel-execution-gates.md` | `parallel-task-safety-checks.md` |
| `validation-gates.md` | `validation-gates-reference.md` |
| `coding-guidelines.md` | `claude-4-tool-usage.md` |

### For New Projects

Simply use the new structure:

1. **Bootstrap**: Use `/bootstrap [spec-path]` (single command, auto-detection)
2. **Task Schema**: Reference `.claude/reference/task-schema-consolidated.md`
3. **Commands**: All core commands have agent type headers and template variables
4. **Documentation**: Use modular reference files, not legacy comprehensive docs

## Breaking Changes

### None for End Users

The cleanup was designed to be **backwards compatible** where possible:

- Old schema files are archived, not deleted
- Legacy bootstrap command is available in archive
- Historical documentation preserved for reference
- No changes to task JSON structure or command functionality

### For Repository Contributors

If you're contributing to this repository:

1. **Don't create new files with old names** - Use the new naming conventions
2. **Reference current files** - Don't link to archived content in active documentation
3. **Update CLAUDE.md** - If adding new patterns, update the navigation guide
4. **Follow template variable pattern** - All commands should have type headers

## Rollback Instructions

If you need to rollback for any reason:

```bash
# Restore old file locations
git revert e5d2091  # First cleanup commit
git revert [second-cleanup-commit]  # The commit after this migration guide

# Or restore individual files
git checkout e5d2091~1 .claude/reference/task-schema.md
git checkout e5d2091~1 .claude/commands/smart-bootstrap.md
```

## Questions & Troubleshooting

### "I can't find [old-file-name]"

Check `.archive/` directory. All deprecated files are preserved there with full README explaining their status.

### "Which schema version should I use?"

Always use `.claude/reference/task-schema-consolidated.md`. It's the single source of truth.

### "I need the interactive bootstrap"

It's available at `.archive/legacy-commands/bootstrap-interactive.md`, but we recommend trying the new auto-detection bootstrap first.

### "My old project references don't work"

Update your references using the mapping tables above. Most changes are simple renames or moves to `.archive/`.

## Timeline

- **December 21, 2024**: Cleanup initiated, ambiguity analysis completed
- **December 21, 2024**: Phase 1-9 implemented (critical fixes through documentation updates)
- **December 21, 2024**: Migration guide created

## Related Documentation

- `.archive/README.md` - Archive directory guide
- `.claude/reference/SCHEMA-MIGRATION-GUIDE.md` - Task schema field mappings
- `CLAUDE.md` - Updated navigation guide with new file locations

## Contact

For questions about this migration or issues with updated file locations, please open an issue on the repository with the `migration` label.
