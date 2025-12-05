# Checkpoint System

## Overview

The Checkpoint System provides state snapshots and rollback capability for task execution. When work goes wrong, checkpoints enable safe restoration to previous working states.

## Purpose

- **Safety net**: Capture state before risky changes
- **Recovery**: Rollback when implementations fail
- **Experimentation**: Try approaches knowing you can undo
- **Debugging**: Compare current state to known-good checkpoints

## Core Concepts

### Checkpoint
A snapshot of project state at a specific moment, including:
- All files affected by task (with SHA-256 hashes)
- Task JSON state (status, notes, etc.)
- Metadata (timestamp, type, description)
- Backup copies of existing files

### Checkpoint Types
- **pre-execution**: Automatic checkpoint before starting work (integrated into complete-task.md)
- **mid-execution**: Manual checkpoint during complex multi-step work
- **manual**: User-requested checkpoint at any time

### Checkpoint ID Format
`chk-{task_id}-{sequence}`

Examples:
- `chk-42-1` - First checkpoint for task 42
- `chk-42-2` - Second checkpoint for task 42
- `chk-15-5` - Fifth checkpoint for task 15

Sequence numbers auto-increment for each task.

## Directory Structure

```
components/checkpoint-system/
├── README.md                    # This file
├── schemas/
│   └── checkpoint.schema.json   # Checkpoint metadata schema
└── commands/
    ├── create-checkpoint.md     # Capture current state
    ├── rollback-to.md           # Restore previous checkpoint
    ├── list-checkpoints.md      # Display checkpoint history
    └── diff-checkpoint.md       # Compare states

.claude/checkpoints/             # Local checkpoint storage (gitignored)
├── chk-42-1/
│   ├── checkpoint.json          # Metadata
│   └── [backed up files]        # File copies preserving structure
├── chk-42-2/
│   ├── checkpoint.json
│   └── [backed up files]
└── ...
```

## Command Workflows

### Creating Checkpoints

**Automatic (via complete-task.md):**
```
/complete-task 42

Step 4: Creating checkpoint...
✓ Checkpoint chk-42-1 created
  Type: pre-execution
  Files captured: 3 existing, 2 new
  Location: .claude/checkpoints/chk-42-1/
```

**Manual:**
```
/create-checkpoint 42

✓ Checkpoint chk-42-2 created
  Type: mid-execution
  Files captured: 5 existing, 0 new
```

### Listing Checkpoints

```
/list-checkpoints 42

Checkpoint: chk-42-1
  Created: 2025-12-05T10:15:00Z (2 hours ago)
  Type: pre-execution
  Files: 3 existing, 2 new
  Task status: Pending → In Progress

Checkpoint: chk-42-2
  Created: 2025-12-05T11:30:00Z (45 minutes ago)
  Type: mid-execution
  Files: 5 existing, 0 new
  Task status: In Progress [CURRENT]

Total: 2 checkpoints for task 42
```

### Comparing States

```
/diff-checkpoint chk-42-1

Comparing current state to checkpoint chk-42-1

Summary:
  3 files modified
  1 file added
  0 files deleted

Modified Files:
  src/api/client.py (+12 lines, -5 lines)
  tests/test_api.py (+8 lines, -2 lines)
  src/config.py (+3 lines, -3 lines)

Added Files:
  src/api/auth.py (new file, 45 lines)
```

### Rolling Back

```
/rollback-to chk-42-1

Restoration Plan:
  ✓ src/api/client.py - RESTORE (changed)
  - src/config.py - UNCHANGED (skip)
  ✗ src/api/auth.py - REMOVE (created after checkpoint)

⚠ WARNING: This will modify 1 file and remove 1 file

Continue with rollback? [y/N] y

✓ Rollback to chk-42-1 complete
  Files restored: 1
  Files removed: 1
  Task status: Restored
```

## Integration with Other Components

### Task Management
- Checkpoints reference task IDs and capture task state
- Task files_affected determines which files to checkpoint
- Task notes record checkpoint creation and restoration events

### Validation Gates (complete-task.md)
- Pre-execution gate creates checkpoint before work starts (step 4)
- Post-execution gate can suggest rollback if failures detected

### Pattern Library
- Patterns can recommend checkpoints before risky operations
- Post-conditions may include "checkpoint created before X"

### Error Catalog (Future)
- Error entries can reference checkpoints where error occurred
- Recovery suggestions can include "rollback to checkpoint X"

## Checkpoint Metadata Schema

See `schemas/checkpoint.schema.json` for full schema.

**Key fields:**
```json
{
  "checkpoint_id": "chk-42-3",
  "task_id": "42",
  "timestamp": "2025-12-05T14:30:00Z",
  "type": "pre-execution",
  "description": "Before starting API integration work",
  "files": [
    {
      "path": "src/api/client.py",
      "hash": "abc123...",
      "backup_path": ".claude/checkpoints/chk-42-3/src/api/client.py",
      "existed": true
    }
  ],
  "task_state": {
    "id": "42",
    "status": "In Progress",
    ...
  }
}
```

## Best Practices

### When to Create Checkpoints

**Always:**
- Before starting any task (automatic via complete-task.md)
- Before refactoring existing code
- Before making breaking changes

**Consider:**
- After completing major milestone in multi-step task
- Before trying experimental approach
- Before batch operations (bulk renames, mass edits)

### When to Rollback

**Definitely:**
- Implementation has critical bugs that can't be quickly fixed
- Approach turns out to be fundamentally flawed
- Accidentally deleted or corrupted files

**Maybe:**
- Want to try completely different approach
- User requests reset to earlier state
- Debugging requires clean slate

### Checkpoint Management

**Do:**
- Create descriptive checkpoints (meaningful descriptions)
- Use diff-checkpoint before rollback to preview changes
- Preserve checkpoints even after rollback (may need again)

**Don't:**
- Create excessive checkpoints (clutters history)
- Delete checkpoints prematurely (disk space is cheap, recovery is valuable)
- Rollback without reviewing diff first (know what you're undoing)

## File Change Detection

Checkpoints use **SHA-256 hashing** for efficient change detection:
- Calculate hash of file contents
- Compare to checkpoint hash
- Only restore if hash differs (avoids unnecessary file operations)

**Benefits:**
- Fast comparison (hash calculation vs. full file diff)
- Accurate detection (any change affects hash)
- Handles binary files (hash works regardless of file type)

## Safety Features

### Confirmation Required
Rollback always requires explicit confirmation showing exactly what will change.

### Pre-Rollback Checkpoint
Option to create safety checkpoint before rollback (can rollback the rollback).

### Selective Restoration
Can restore individual files instead of full checkpoint.

### Preservation
Checkpoints never deleted automatically (manual cleanup if needed).

### Task State Restoration
Optional - can restore files without resetting task status.

## Storage Considerations

### What's Stored
- Full copies of files (not diffs) for reliability
- Directory structure preserved
- Only files in task files_affected

### What's Not Stored
- Files outside task scope (efficient)
- Build artifacts (should be in .gitignore anyway)
- Large binary files (may want to exclude these)

### Cleanup
`.claude/checkpoints/` excluded from git (local only).

Manual cleanup options:
- Delete old checkpoints for completed tasks
- Delete checkpoints for abandoned approaches
- Keep checkpoints for important milestones

## Error Handling

Commands handle errors gracefully:
- Missing checkpoints: Clear error messages
- Corrupted metadata: Skip invalid checkpoints with warnings
- File operation failures: Continue with other files, report issues
- User cancellation: No changes made, safe to cancel anytime

## Future Enhancements

Potential additions:
- Checkpoint expiration (auto-delete after N days)
- Compressed storage (tar.gz checkpoints)
- Checkpoint branching (multiple checkpoint paths)
- Remote checkpoint storage (backup to cloud)
- Checkpoint sharing (export/import for collaboration)
- Incremental checkpoints (store only diffs)

## Examples

### Example 1: Safe Refactoring

```
# Start task, automatic checkpoint created
/complete-task 42

# Checkpoint chk-42-1 created automatically

# Do some work, realize approach is wrong
# Check what changed
/diff-checkpoint chk-42-1

# Rollback to clean state
/rollback-to chk-42-1

# Try different approach
```

### Example 2: Multi-Step Implementation

```
# Start task
/complete-task 42
# Checkpoint chk-42-1 (pre-execution)

# Complete step 1, create checkpoint
/create-checkpoint 42
# Checkpoint chk-42-2 (mid-execution)

# Complete step 2, create checkpoint
/create-checkpoint 42
# Checkpoint chk-42-3 (mid-execution)

# Step 3 fails, rollback to after step 1
/rollback-to chk-42-2

# Try step 2 differently
```

### Example 3: Debugging with Diffs

```
# Something broke, when did it break?
/list-checkpoints 42

# Compare against checkpoints
/diff-checkpoint chk-42-1  # No issue
/diff-checkpoint chk-42-2  # Bug introduced here!

# See exactly what changed
/diff-checkpoint chk-42-2

# Rollback if needed or fix specific file
```

## See Also

- **Validation Gates**: Pre/post-execution validation (calls create-checkpoint)
- **Task Management**: Task lifecycle and status tracking
- **Pattern Library**: Reusable patterns (some recommend checkpoints)
- **Error Catalog**: Error tracking and prevention (references checkpoints)
