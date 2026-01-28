# Update Template

Compares local `.claude/` files against the template repository, shows differences, and offers to update.

## Usage
```
/update-template            # Check for template updates and offer to apply
```

## Purpose

Keeps your project's workflow files (commands, agents, reference docs) in sync with the latest template version. Only affects files in the `sync` category — your customizations and project data are never touched.

---

## Requirements

- `.claude/version.json` - Contains `template_repo` and `template_version`
- `.claude/sync-manifest.json` - Lists files in `sync` category
- `gh` CLI installed and authenticated (or use GitHub MCP tools)

## Safety Principles

1. **No silent deletions** - Files are never removed without explicit user confirmation
2. **Preview before apply** - Shows all changes before making them
3. **Sync category only** - Never touches `customize` or `ignore` category files
4. **Preserves local additions** - Files that exist locally but not in template are kept

---

## Process

### Step 1: Gather Information

Read local configuration:
```json
// .claude/version.json
{
  "template_version": "1.0.0",
  "template_repo": "https://github.com/user/claude_code_environment"
}

// .claude/sync-manifest.json
{
  "categories": {
    "sync": [".claude/commands/*.md", ".claude/agents/*.md", ...]
  }
}
```

Fetch template from remote:
```bash
git clone --depth 1 {template_repo} /tmp/template
```

### Step 2: Compare and Report

Categorize all files in the `sync` category:

| Category | Meaning |
|----------|---------|
| **Up to date** | Local matches template |
| **Modified** | Template has changes |
| **New in template** | File added in template |
| **Local only** | File exists locally but not in template |

### Step 3: Show Results and Offer Update

```
### Template Sync Check

Source: https://github.com/user/claude_code_environment
Version: v1.0.0 (local) → v1.1.0 (template)

## Status

✓ Up to date (3 files)
  .claude/commands/status.md
  .claude/commands/breakdown.md
  .claude/support/reference/task-schema.md

⚠️ Modified in template (3 files)
  .claude/commands/work.md (+15 -8 lines)
  .claude/agents/implement-agent.md (+23 -5 lines)
  .claude/commands/health-check.md (+45 -12 lines)

+ New in template (1 file)
  .claude/commands/new-feature.md

• Local only (1 file)
  .claude/commands/my-custom.md

---

[U] Update all modified/new files
[P] Preview diffs first
[S] Select files individually
[K] Keep current (no changes)
```

---

## Preview Diffs

When `[P]` is selected, show diffs for each modified file:

```
## Diff: .claude/commands/work.md

@@ -19,7 +19,7 @@ What It Does
-5. **Routes to specialists** - Invokes implement-agent
+5. **Routes to specialists** - Reads and follows implement-agent workflow

@@ -212,8 +212,12 @@ If Executing
-Invoke implement-agent with:
+**CRITICAL:** You must read implement-agent.md and follow its workflow.
...

[N] Next file  [U] Update this file  [S] Skip this file  [Q] Quit preview
```

## Individual File Selection

When `[S]` is selected:

```
## Select Files to Update

Modified:
  [1] .claude/commands/work.md (+15 -8)
  [2] .claude/agents/implement-agent.md (+23 -5)
  [3] .claude/commands/health-check.md (+45 -12)

New:
  [4] .claude/commands/new-feature.md

Enter numbers (comma-separated), or:
  [A] All  [N] None  [B] Back

Selection: _
```

---

## Handling Local-Only Files

Files that exist locally but not in the template are **never automatically deleted**.

If local-only files exist in the `sync` category:

```
## Local-Only Files

These files exist locally but not in the template:
  • .claude/commands/custom-workflow.md
  • .claude/agents/custom-agent.md

These may be intentional customizations. What would you like to do?

[K] Keep all (recommended)
[R] Review individually

Selection: _
```

If `[R]` is selected:

```
## Review: .claude/commands/custom-workflow.md

This file exists locally but not in the template.

[K] Keep - Intentional local customization
[D] Delete - No longer needed
[S] Skip - Decide later

Selection: _
```

---

## Applying Updates

Before any modifications:
1. Create backup in `.claude/support/workspace/sync-backup-{timestamp}/`
2. Show confirmation of what will change

```
## Confirm Update

Will update:
  • .claude/commands/work.md
  • .claude/agents/implement-agent.md
  • .claude/commands/health-check.md

Will add:
  • .claude/commands/new-feature.md

Will keep (local-only):
  • .claude/commands/my-custom.md

Backup location: .claude/support/workspace/sync-backup-20260127-143022/

[Y] Yes, apply updates  [N] Cancel

Selection: _
```

## Post-Update Summary

```
### Sync Complete ✓

Updated:
  ✓ .claude/commands/work.md
  ✓ .claude/agents/implement-agent.md
  ✓ .claude/commands/health-check.md

Added:
  + .claude/commands/new-feature.md

Kept (local-only):
  • .claude/commands/my-custom.md

Version: v1.0.0 → v1.1.0

Backup saved to: .claude/support/workspace/sync-backup-20260127-143022/
(Auto-deleted after 7 days)

Next steps:
  1. Review the updated files
  2. Run /health-check to verify system health
  3. Test your workflows
```

---

## Conflict Handling

If a sync file has local modifications that differ from the expected template version:

```
## Conflict: .claude/commands/work.md

This file has local changes that aren't in the template.
Updating will overwrite your modifications.

[O] Overwrite with template
[K] Keep local version
[D] Show diff
[M] Merge manually

Selection: _
```

## Error Recovery

If sync is interrupted:

```
[Warning] Previous sync was interrupted

  - 2 files updated before interruption
  - Backup exists at: .claude/support/workspace/sync-backup-20260127-143022/

[R] Resume from where it stopped
[S] Start fresh
[X] Restore backup and cancel

Selection: _
```

## Offline Mode

If GitHub is unavailable:
```
[Warning] Cannot reach template repository
  - Check network connection
  - Verify gh CLI: gh auth status
  - Try again later
```

## Up-to-Date Response

If everything matches:
```
### Template Sync Check ✓

Source: https://github.com/user/claude_code_environment
Version: v1.1.0

All 12 sync files are up to date.
No action needed.
```

---

## Edge Cases

**Missing version.json:** Skipped with note: "Create .claude/version.json to enable template sync"

**Missing sync-manifest.json:** Skipped with note: "Create .claude/sync-manifest.json to enable template sync"

## When to Run

- Periodically (monthly recommended)
- After cloning a new project from the template
- When you hear about template improvements
- Before starting a new project phase

## Reference

Version info: `.claude/version.json`
Sync manifest: `.claude/sync-manifest.json`
