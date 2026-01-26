# CLAUDE.md Best Practices

Guidelines for keeping CLAUDE.md minimal and effective.

## Target Size

**Ideal: 60-80 lines.** This ensures fast context loading and quick reference.

| Threshold | Lines | Meaning |
|-----------|-------|---------|
| ✅ Healthy | <80 | Good shape |
| ⚠️ Warning | 80-120 | Consider trimming |
| ❌ Bloated | >120 | Needs cleanup |

## What Belongs in CLAUDE.md

**Keep inline:**
- Project overview (2-3 sentences)
- Critical commands (one-line each)
- Key rules and conventions (brief list)
- Project structure (simple tree)
- Navigation pointers to reference docs

**Move to .claude/reference/:**
- Detailed schemas (>8 lines)
- Verbose examples or templates
- Full procedure documentation
- Technology deep-dives
- Historical context or decisions

## The Externalization Pattern

When a section grows too large, externalize it:

**Before:**
```markdown
## Task Schema
{
  "id": "string",
  "title": "string",
  "status": "Pending | In Progress | Blocked | Finished",
  ...12 more lines...
}
```

**After:**
```markdown
## Task Schema
See `.claude/reference/task-schema.md`
```

This keeps CLAUDE.md scannable while preserving detail accessibility.

## Signs of Bloat

- Sections with >15 lines
- Code blocks with >10 lines
- Inline JSON schemas
- Duplicate information
- "Just in case" content
- Historical notes that aren't actionable

## Section Guidelines

| Section Type | Target Lines |
|--------------|--------------|
| Overview | 3-5 |
| Commands | 1 per command |
| Conventions | 5-10 |
| Structure | 10-15 |
| Technology | 5-8 |

## Audit Command

Run `/health-check --claude-md` to check for bloat. After the report, you'll be offered to walk through fixes interactively.

Run `/health-check --report-only` to just see the report without fix prompts.
