# Audit CLAUDE.md

Check CLAUDE.md for bloat and offer guided fixes.

## Usage
```
/audit-claude-md [--report-only]
```

## Purpose

CLAUDE.md files accumulate detail over time. Best practice is minimal (~60-80 lines) for quick context loading. This command detects bloat and offers guided cleanup.

By default, after showing the report, you'll be offered the chance to walk through fixes interactively. Use `--report-only` to just see the report without prompts.

## Thresholds

| Metric | Warning | Error |
|--------|---------|-------|
| Total lines | 80 | 120 |
| Section lines | 15 | 25 |
| Code blocks | 10 | 20 |
| Inline schemas | 8 | Always flag |

## Process

### Step 1: Scan CLAUDE.md
```
READ CLAUDE.md
COUNT total lines
IDENTIFY sections (## headers)
COUNT lines per section
FIND code blocks (``` delimiters)
COUNT lines per code block
```

### Step 2: Run Checks
```
CHECK total lines against thresholds
FOR each section:
  CHECK line count against thresholds
FOR each code block:
  CHECK line count against thresholds
  CHECK if looks like JSON schema (>8 lines with braces)
```

### Step 3: Report Status
```
## CLAUDE.md Audit Report

### File Metrics
- Total lines: N [✅/⚠️/❌]
- Sections: N
- Code blocks: N

### Section Sizes
| Section | Lines | Status |
|---------|-------|--------|
| Task Management | 12 | ✅ |
| Technology Stack | 18 | ⚠️ Exceeds 15 |
...

### Code Blocks
| Location | Lines | Status |
|----------|-------|--------|
| Line 45-55 | 10 | ⚠️ At threshold |
...

### Summary
✅ N checks passed
⚠️ N warnings
❌ N errors
```

### Step 4: Offer Fix Workflow

Skip this step if `--report-only` was specified.

If any warnings or errors were found, ask:

```
Would you like to walk through these issues now? (y/n): _
```

If user answers yes, for EACH flagged issue sequentially ask:

```
⚠️ Section "Technology Stack" is 18 lines (threshold: 15)

Options:
1. Move to .claude/reference/technology-stack.md
2. Keep inline (essential for quick reference)
3. Condense (rewrite to fewer lines)
4. Skip for now

Your choice: _
```

Apply fix immediately before moving to next issue.

## Fix Actions

### Move (Option 1)
1. Create `.claude/reference/{section-slug}.md` with section content
2. Replace section in CLAUDE.md with: `See .claude/reference/{section-slug}.md`
3. Confirm change made

### Keep (Option 2)
1. Note in report that section was explicitly kept
2. Move to next issue

### Condense (Option 3)
1. Show current content
2. Ask user what the essential points are
3. Rewrite section with condensed content
4. Confirm change made

### Skip (Option 4)
1. Move to next issue without changes

## Externalization Pattern

**Before (inline):**
```markdown
## Task Schema
{
  "id": "string",
  "title": "string",
  ...15 more lines...
}
```

**After (externalized):**
```markdown
## Task Schema
See `.claude/reference/task-schema.md`
```

## What Belongs Inline

Keep in CLAUDE.md:
- Project overview (2-3 sentences)
- Critical commands (one-liners)
- Key conventions (brief list)
- Navigation pointers

Move to reference/:
- Detailed schemas (>8 lines)
- Verbose examples
- Full procedure documentation
- Technology deep-dives

## When to Run

- When CLAUDE.md feels "heavy"
- After adding significant content
- Periodically (monthly recommended)
- Before sharing project with others

## Reference

Best practices: `.claude/reference/claude-md-guide.md`
