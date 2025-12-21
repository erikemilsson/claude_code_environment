# Archive Directory

This directory contains deprecated, historical, and legacy files from the Claude Code Environment repository. These files are preserved for reference but are **not part of the active codebase**.

## Directory Structure

### `/deprecated-schemas/`
Contains superseded task schema versions. These have been consolidated into a single authoritative schema.

**Files:**
- `task-schema.md` - Original task schema (replaced Dec 2025)
- `task-schema-v2.md` - Second iteration with progress tracking (replaced Dec 2025)
- `enhanced-task-schema.md` - Belief tracking focus (replaced Dec 2025)

**Current Version:** `.claude/reference/task-schema-consolidated.md`

### `/legacy-commands/`
Contains deprecated command patterns that have been replaced with improved versions.

**Files:**
- `bootstrap-interactive.md` - Original interactive bootstrap with manual template selection

**Current Version:** `.claude/commands/bootstrap.md` (auto-detection, agent-based)

### `/historical-docs/`
Contains comprehensive documentation that has been superseded by modular, focused guides.

**Files:**
- `legacy-template-reference.md` - Original 52KB comprehensive template guide (frozen snapshot)

**Current Documentation:** See `templates/` directory and individual reference files in `.claude/reference/`

## When to Reference Archived Files

### Use Archived Files When:
- Understanding historical design decisions
- Migrating from old schema versions
- Researching why patterns changed
- Troubleshooting legacy projects

### Do NOT Use Archived Files For:
- New project creation
- Active development guidance
- Command execution
- Schema validation

## Migration Guides

For help migrating from old to new patterns:
- Task schema migration: See `.claude/reference/SCHEMA-MIGRATION-GUIDE.md`
- Bootstrap migration: Legacy interactive → Smart auto-detect (just use new `/bootstrap` command)
- Template reference: See individual files in `templates/[name]/README.md`

## Archive Policy

**When files are added:**
- Deprecated schemas and major version changes
- Superseded command patterns
- Historical comprehensive docs replaced by modular structure

**What stays active:**
- Current canonical versions
- Active templates and components
- Working commands and reference materials

## Questions?

If you're unsure whether to use an archived file:
1. Check the current version location noted above
2. Review migration guides
3. Default to using active codebase unless specifically researching history
