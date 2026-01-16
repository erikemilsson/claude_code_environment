# Undo Bootstrap - Remove Generated Environment

## Purpose
Safely remove files created by bootstrap operation to allow starting over. Preserves user-created content while removing generated `.claude/` structure and related files.

## Context Required
- Current directory should have `.claude/` directory
- Understanding that this operation removes generated files

## When to Use
- Bootstrap created environment in wrong directory
- Want to switch to different template
- Template detection was incorrect
- Need to start fresh after testing
- Encountered errors during bootstrap

## Safety Features
1. **Preview Before Delete** - Shows exactly what will be removed
2. **User-Created Content Protection** - Detects and preserves custom files
3. **Confirmation Required** - Cannot accidentally delete
4. **Backup Option** - Can create backup before removal
5. **Dry Run Mode** - Can preview without actually deleting

## Process

### Step 1: Validate Environment Exists

**Check for .claude/ directory**:
```bash
# Verify environment exists
[ -d ".claude" ] && echo "Environment found" || echo "No environment to remove"
```

**If no .claude/ directory**:
```
ℹ️  No bootstrap environment found

Current directory: [path]

No .claude/ directory exists in this location.
There is nothing to undo.

Possible reasons:
  • Bootstrap was not run in this directory
  • You're in the wrong directory
  • Environment was already removed

What would you like to do?
  1. List recent directories (to find correct location)
  2. Cancel operation
```
→ Exit gracefully

**If .claude/ exists** → Continue to Step 2

### Step 2: Analyze Generated vs User-Created Content

**Scan environment for custom content**:

**Check for user modifications**:
- Task files with notes or custom fields
- Context files modified after bootstrap
- Custom commands not in template
- Files in non-standard locations

**Identify bootstrap-generated files** (typical list):
- `CLAUDE.md` (if created by bootstrap)
- `README.md` (if created by bootstrap)
- `.claude/commands/` (standard commands)
- `.claude/context/` (template files)
- `.claude/tasks/task-overview.md`
- `.claude/reference/` (template docs)

**Identify potentially user-created**:
- `.claude/tasks/task-*.json` (task files)
- `.claude/context/*.md` (modified context)
- `.claude/commands/*.md` (custom commands)
- Any files with recent modification times

**Modification Detection**:
```bash
# Check if files were modified after creation
# Look at file modification times and content
find .claude -type f -name "*.md" -o -name "*.json"
```

### Step 3: Categorize Files

**Three categories**:

1. **Safe to Delete** (definitely bootstrap-generated)
   - Standard command files (complete-task.md, breakdown.md, sync-tasks.md)
   - Template reference docs
   - Empty or unmodified template files

2. **User Content** (preserve)
   - Task JSON files with actual data
   - Modified context files
   - Custom commands not in template
   - Any file with substantial user content

3. **Ambiguous** (ask user)
   - Files that might be user-created
   - Modified template files
   - Non-standard files in .claude/

### Step 4: Present Removal Plan

**Show detailed plan**:
```
═══════════════════════════════════════════════════════════
UNDO BOOTSTRAP - REMOVAL PLAN
═══════════════════════════════════════════════════════════

DIRECTORY: [current directory]

WILL REMOVE (Bootstrap-generated files):
  ✓ CLAUDE.md (0 modifications)
  ✓ README.md (bootstrap template)
  ✓ .claude/commands/
      • complete-task.md
      • breakdown.md
      • sync-tasks.md
      • update-tasks.md
      [+ N more standard commands]
  ✓ .claude/reference/
      • difficulty-guide.md
      • breakdown-workflow.md
      [+ N more reference docs]
  ✓ .claude/context/
      • overview.md (unmodified template)
      • validation-rules.md (unmodified)

WILL PRESERVE (User content):
  ⚠️  .claude/tasks/
      • task-1.json (has user notes)
      • task-2.json (completed)
      • task-3.json (in progress)
      • task-overview.md (has custom content)
  ⚠️  .claude/context/
      • project-notes.md (custom file)
  ⚠️  .claude/commands/
      • my-custom-workflow.md (user-created)

AMBIGUOUS (Please confirm):
  ?  .claude/context/overview.md
     Modified: 2 hours ago
     Size: 3.2 KB (larger than template)
     Contains custom content?
     → Keep this file? [Y/n]

  ?  README.md
     Modified: 1 hour ago
     Might have user additions
     → Keep this file? [Y/n]

═══════════════════════════════════════════════════════════

SUMMARY:
  • Will remove: 12 files (standard bootstrap files)
  • Will preserve: 7 files (user content)
  • Need decision: 2 files (ambiguous)

Total to delete: ~12 files, ~45 KB

═══════════════════════════════════════════════════════════

Options:
  1. Proceed with removal (recommended)
  2. Create backup first, then remove
  3. Dry run (show what would happen, don't delete)
  4. Cancel operation

What would you like to do? [1/2/3/4]
```

### Step 5: Handle User Choice

**Option 1: Proceed with Removal**
```
Removing bootstrap-generated files...

Removed:
  ✓ CLAUDE.md
  ✓ .claude/commands/ (8 files)
  ✓ .claude/reference/ (3 files)
  ✓ .claude/context/ (2 files)

Preserved:
  ⚠️  .claude/tasks/ (4 files with user content)
  ⚠️  .claude/context/ (1 custom file)

Cleanup:
  • Removed empty directories
  • Preserved .claude/tasks/ (has content)
  • Preserved .claude/context/ (has 1 file)

═══════════════════════════════════════════════════════════
UNDO COMPLETE
═══════════════════════════════════════════════════════════

Bootstrap environment removed. Preserved user-created content:
  • 4 task files in .claude/tasks/
  • 1 custom context file
  • 1 custom command

You can now:
  1. Run bootstrap again with different settings
  2. Remove remaining .claude/ files manually if desired
  3. Navigate to different directory
```

**Option 2: Create Backup First**
```
Creating backup...

Backup location: .claude-backup-[timestamp]/
Copying files...

Backed up 24 files → .claude-backup-2025-12-18-143022/

Now proceeding with removal...
[Continue with standard removal]

Backup preserved at: .claude-backup-2025-12-18-143022/
You can restore by moving contents back to .claude/
```

**Option 3: Dry Run**
```
═══════════════════════════════════════════════════════════
DRY RUN - NO FILES WILL BE DELETED
═══════════════════════════════════════════════════════════

Would remove:
  • CLAUDE.md (3 KB)
  • README.md (5 KB)
  • .claude/commands/complete-task.md (2 KB)
  • .claude/commands/breakdown.md (2 KB)
  [... full list ...]

Would preserve:
  • .claude/tasks/task-1.json
  • .claude/tasks/task-2.json
  [... full list ...]

Total that would be deleted: 12 files, 45 KB
Total that would be preserved: 7 files, 23 KB

This was a DRY RUN. No files were actually deleted.

To actually remove files, run this command again and choose option 1.
```

**Option 4: Cancel**
```
Cancelled. No files were removed.
```

### Step 6: Post-Removal Cleanup

**After successful removal**:

1. **Remove Empty Directories**
   ```bash
   # Remove .claude/ if completely empty
   rmdir .claude/commands 2>/dev/null
   rmdir .claude/reference 2>/dev/null
   rmdir .claude/context 2>/dev/null
   rmdir .claude/tasks 2>/dev/null
   rmdir .claude 2>/dev/null
   ```

2. **Report Final State**
   ```
   Final directory state:
   [If .claude/ completely removed:]
     • .claude/ - Removed (was empty)
     • CLAUDE.md - Removed
     • Directory is clean ✓

   [If .claude/ has remaining content:]
     • .claude/tasks/ - Kept (4 task files)
     • .claude/context/ - Kept (1 custom file)
     • To remove manually: rm -rf .claude/
   ```

## Advanced Options

### Selective Removal

**Remove only specific components**:
```
Instead of full removal, you can remove specific parts:

  1. Remove commands only (keep context and tasks)
  2. Remove reference docs only
  3. Remove CLAUDE.md only
  4. Custom selection (choose what to remove)

What would you like to do? [1/2/3/4/full removal]
```

### Force Removal

**Remove everything (including user content)**:
```
⚠️  WARNING: Force removal mode

This will remove ALL .claude/ content including:
  • User-created tasks
  • Modified context files
  • Custom commands
  • All reference docs
  • CLAUDE.md
  • README.md (if generated by bootstrap)

This action CANNOT be undone (unless you choose backup).

Type 'DELETE EVERYTHING' to confirm force removal: ____
```

Only proceed if user types exact phrase.

## Safety Checks

### Before Any Deletion

1. **Verify not in system directory**
   - Check we're not in ~, /, /usr, etc.
   - Abort if in dangerous location

2. **Check for uncommitted git changes**
   ```bash
   git status --porcelain 2>/dev/null
   ```
   - Warn if uncommitted changes to .claude/
   - Suggest commit first

3. **Verify .claude/ is bootstrap-generated**
   - Check for standard file structure
   - Warn if structure is non-standard
   - User might have custom setup

### During Deletion

1. **Delete files individually** (not recursive rm -rf)
2. **Log each deletion**
3. **Stop on error** (don't continue if something fails)
4. **Keep count** of deleted files

### After Deletion

1. **Verify expected files gone**
2. **Verify preserved files still exist**
3. **Check directory permissions** unchanged

## Error Handling

### Permission Denied
```
❌ ERROR: Permission denied

Could not remove: .claude/commands/complete-task.md

This file may be:
  • Locked by another process
  • Have restricted permissions
  • In use by an application

Fix permissions and try again, or use:
  sudo [command] (if you have admin rights)
```

### Partial Failure
```
⚠️  WARNING: Partial removal

Successfully removed:
  ✓ CLAUDE.md
  ✓ 8 command files
  ✓ 3 reference files

Failed to remove:
  ❌ .claude/context/overview.md (permission denied)
  ❌ .claude/tasks/ (directory not empty)

Remaining files may need manual removal.
```

### Git Conflict
```
⚠️  NOTICE: Git changes detected

You have uncommitted changes in .claude/ directory:
  • .claude/tasks/task-1.json (modified)
  • .claude/context/custom.md (new file)

Removing these files will lose uncommitted changes.

Recommended: Commit changes first
  git add .claude/
  git commit -m "Save before bootstrap undo"

Proceed anyway? [y/N]
```

## Examples

### Example 1: Clean Removal
User ran bootstrap, realized wrong template, wants to start over.
→ Remove all bootstrap files, no user content to preserve
→ Fast, simple removal

### Example 2: Partial Removal
User has been working, created tasks, wants different template.
→ Preserve task files and custom content
→ Remove only generated structure
→ Can re-bootstrap with different template

### Example 3: Backup and Remove
User unsure if wants to lose content.
→ Create full backup first
→ Remove environment
→ Can restore from backup if needed

### Example 4: Dry Run First
User wants to see what would be removed.
→ Show full removal plan without deleting
→ User reviews and confirms
→ Run again to actually remove

## Recovery Options

### If Accidentally Removed User Content

**If backup was created**:
```
To restore from backup:
  cp -r .claude-backup-[timestamp]/* .claude/
```

**If no backup**:
```
User content was removed. Recovery options:
  1. Check git history: git log .claude/
  2. Restore from git: git checkout HEAD~1 .claude/
  3. Check filesystem backups (Time Machine, etc.)
  4. Recreate content from memory
```

## Validation Checklist

Before confirming removal:
- [ ] Verified .claude/ directory exists
- [ ] Identified all user-created content
- [ ] Presented clear removal plan
- [ ] Offered backup option
- [ ] Got explicit user confirmation
- [ ] Logged all operations
- [ ] Verified successful removal
- [ ] Reported final state

## Critical Rules

1. **NEVER delete without showing plan first**
2. **ALWAYS preserve user-created content** (tasks, custom files)
3. **ALWAYS offer backup option**
4. **NEVER use recursive rm -rf on .claude/** without per-file check
5. **ALWAYS verify each deletion succeeded**
6. **NEVER delete if in system directory** (/, /usr, etc.)
7. **ALWAYS check for git changes** before removing
8. **ALWAYS provide recovery information** after removal

## Related Commands

- `/bootstrap` - Create new environment
- `/smart-bootstrap` - Auto-detect and create environment
- `/update-tasks` - Validate environment health

## Output Location

Files removed from current working directory:
- Removes `./CLAUDE.md` (if bootstrap-generated)
- Removes `./README.md` (if bootstrap-generated)
- Removes `./.claude/` and contents (except preserved files)
- Creates `./.claude-backup-[timestamp]/` if backup requested