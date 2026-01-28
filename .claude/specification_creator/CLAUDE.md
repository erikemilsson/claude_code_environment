# Specification Creator

> **Redirect Notice:** The `/iterate` command has moved to the project root.
> Run `/iterate` from the main project directory instead of starting a separate Claude Code session here.

## What Moved

- **`/iterate` command** → Available at project root (`.claude/commands/iterate.md`)
- **Spec checklist** → `.claude/support/reference/spec-checklist.md`

## Why

Running `/iterate` from the project root eliminates the need for a separate Claude Code instance. All spec-building rules (suggest-only mode, max 4 questions, etc.) are embedded in the command file itself.

## Quick Reference

```bash
# From project root:
/iterate                    # Continue building the spec
/iterate {topic}            # Focus on a specific area
/iterate distill            # Extract buildable spec from vision document
```

The spec lives at `.claude/spec_v{N}.md`. Claude suggests changes; you make edits.
