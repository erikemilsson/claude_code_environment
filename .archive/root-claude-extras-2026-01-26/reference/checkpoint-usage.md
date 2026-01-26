# Checkpoint System Usage Guide

*Created: 2025-12-17*

## Overview

The checkpoint system provides fast, reliable state snapshots for the task management system. Checkpoints allow you to save current task state and restore it later if needed, particularly useful for:
- Long-running task sequences
- Experimental task modifications
- Recovery from errors
- Before major changes

## Implementation

### Script Location
**Primary Tool**: `scripts/checkpoint-manager.py`

### Features
- Timestamped checkpoint creation
- SHA-256 integrity verification
- Compressed storage (gzip)
- Diff between checkpoints
- State restoration
- Metadata tracking

## When to Create Checkpoints

### Automatic Checkpoint Triggers
Checkpoints should be created automatically:
1. **Every 3 steps** during long tasks (progress.current_step % 3 == 0)
2. **Before risky operations** (major refactors, deletions)
3. **When context usage > 50%** (preserve state before potential reset)
4. **Before breaking down tasks** (preserve original structure)

### Manual Checkpoint Triggers
Create checkpoints manually:
- Before experimental changes
- At natural breakpoints (end of day, milestone)
- Before batch operations
- When task state is known-good

### DON'T Create Checkpoints
Avoid checkpoint overhead for:
- Every trivial step
- Tight loops
- Already-finished tasks
- Simple task updates

## Usage

### Creating a Checkpoint

```bash
# Python API
python3 scripts/checkpoint-manager.py create "Description of current state"

# Returns checkpoint ID: checkpoint_20251217_143022
```

```python
# In scripts or commands
from scripts.checkpoint_manager import CheckpointManager

manager = CheckpointManager()
checkpoint_id = manager.create_checkpoint("Before breaking down task 42")
print(f"Created checkpoint: {checkpoint_id}")
```

### Listing Checkpoints

```bash
# Command line
python3 scripts/checkpoint-manager.py list
```

```python
# Python API
checkpoints = manager.list_checkpoints()
for cp in checkpoints:
    print(f"{cp['id']}: {cp['description']} ({cp['files_count']} files)")
```

**Output:**
```
checkpoint_20251217_143022: Before breaking down task 42 (25 files)
checkpoint_20251217_120000: End of morning work session (23 files)
checkpoint_20251216_180000: Before validation gate changes (22 files)
```

### Comparing Checkpoints

```bash
# Show difference between checkpoint and current state
python3 scripts/checkpoint-manager.py diff checkpoint_20251217_143022
```

```python
# Python API
diffs = manager.diff_checkpoint("checkpoint_20251217_143022")
print(f"Added: {diffs['added']}")
print(f"Modified: {diffs['modified']}")
print(f"Deleted: {diffs['deleted']}")
```

**Output:**
```
Added: ['task-42_1.json', 'task-42_2.json', 'task-42_3.json']
Modified: ['task-42.json', 'task-overview.md']
Deleted: []
```

### Restoring from Checkpoint

```bash
# Restore task state from checkpoint
python3 scripts/checkpoint-manager.py restore checkpoint_20251217_143022
```

```python
# Python API
manager.restore_checkpoint("checkpoint_20251217_143022", backup_current=True)
print("State restored to checkpoint")
```

**What Happens:**
1. Current state backed up to `.claude/checkpoints/pre_restore_backup/`
2. Checkpoint files extracted from gzip
3. Task files copied to `.claude/tasks/`
4. Integrity verified via SHA-256 hash
5. Restoration confirmed

### Deleting Checkpoints

```bash
# Delete old checkpoint
python3 scripts/checkpoint-manager.py delete checkpoint_20251216_180000
```

```python
# Python API
manager.delete_checkpoint("checkpoint_20251216_180000")
```

## Checkpoint Storage Structure

```
.claude/checkpoints/
├── checkpoint_20251217_143022/
│   ├── metadata.json              # Checkpoint info
│   ├── tasks/                     # Snapshot of .claude/tasks/
│   │   ├── task-01.json
│   │   ├── task-02.json
│   │   └── task-overview.md
│   └── tasks.tar.gz               # Compressed version
├── checkpoint_20251217_120000/
│   └── ...
└── pre_restore_backup/            # Backup before restore
    └── ...
```

## Metadata Format

Each checkpoint includes metadata:

```json
{
  "id": "checkpoint_20251217_143022",
  "timestamp": "2025-12-17T14:30:22.456789",
  "description": "Before breaking down task 42",
  "files_count": 25,
  "hash": "a3f5c8...9d2e1b",
  "compressed_size_kb": 45,
  "uncompressed_size_kb": 182
}
```

## Integration with Commands

### complete-task.md Integration

**Auto-checkpoint triggers:**
```markdown
DURING TASK EXECUTION:
1. IF task has progress tracking AND current_step % 3 == 0:
   CREATE checkpoint with description: "Task {task_id} step {current_step}"

2. IF context usage > 50%:
   CREATE checkpoint with description: "Context checkpoint at {usage}%"

3. IF error encountered AND can_recover:
   CREATE checkpoint before recovery attempt
```

### breakdown.md Integration

**Before breakdown:**
```markdown
BEFORE BREAKING DOWN TASK:
1. READ task file
2. CREATE checkpoint with description: "Before breakdown of task {task_id}"
3. PERFORM breakdown
4. IF breakdown fails:
   RESTORE from checkpoint
   REPORT error
```

### Validation Gates Integration

**Recovery checkpoints:**
```markdown
BEFORE VALIDATION GATE:
1. IF gate is high-risk (major changes):
   CREATE checkpoint

AFTER VALIDATION GATE:
1. IF gate failed:
   RESTORE from checkpoint
   REPORT failure
```

## Best Practices

### Checkpoint Naming
Use descriptive names:
- ✅ "Before breakdown of task 42"
- ✅ "Completed milestone 3 of task 12"
- ✅ "End of day checkpoint - all tests passing"
- ❌ "Checkpoint"
- ❌ "Backup"
- ❌ "Test"

### Checkpoint Frequency
Balance safety and performance:
- **Too frequent**: Wasted storage, slower operations
- **Too infrequent**: More work lost if restore needed
- **Recommended**: Every 3 significant steps or at natural boundaries

### Checkpoint Retention
Manage checkpoint lifecycle:
- Keep last 5 checkpoints per task
- Keep daily checkpoints for 7 days
- Keep weekly checkpoints for 30 days
- Delete checkpoints of finished tasks after 7 days

### Storage Considerations
Monitor checkpoint disk usage:
```bash
# Check checkpoint storage
du -sh .claude/checkpoints/
```

If storage grows too large:
- Delete old checkpoints
- Increase compression level
- Archive to external storage

## Command-Line Interface

### Available Commands

```bash
# Create checkpoint
python3 scripts/checkpoint-manager.py create "Description"

# List checkpoints
python3 scripts/checkpoint-manager.py list

# Show checkpoint details
python3 scripts/checkpoint-manager.py show checkpoint_ID

# Diff checkpoint vs current
python3 scripts/checkpoint-manager.py diff checkpoint_ID

# Restore from checkpoint
python3 scripts/checkpoint-manager.py restore checkpoint_ID

# Delete checkpoint
python3 scripts/checkpoint-manager.py delete checkpoint_ID

# Cleanup old checkpoints
python3 scripts/checkpoint-manager.py cleanup --days 7
```

### Options

```bash
# Create with auto-description
python3 scripts/checkpoint-manager.py create --auto

# Restore without backup
python3 scripts/checkpoint-manager.py restore checkpoint_ID --no-backup

# Force delete (no confirmation)
python3 scripts/checkpoint-manager.py delete checkpoint_ID --force

# List with filters
python3 scripts/checkpoint-manager.py list --since "2025-12-15" --task-id 42
```

## Python API Reference

### CheckpointManager Class

```python
class CheckpointManager:
    def __init__(self, base_path: str = "."):
        """Initialize checkpoint manager

        Args:
            base_path: Root directory of project (default: current dir)
        """

    def create_checkpoint(self, description: str = "") -> str:
        """Create new checkpoint

        Args:
            description: Human-readable checkpoint description

        Returns:
            checkpoint_id: Unique identifier for checkpoint
        """

    def list_checkpoints(self) -> List[Dict]:
        """List all checkpoints

        Returns:
            List of checkpoint metadata dictionaries, newest first
        """

    def diff_checkpoint(self, checkpoint_id: str) -> Dict[str, List]:
        """Compare checkpoint to current state

        Args:
            checkpoint_id: ID of checkpoint to compare

        Returns:
            Dictionary with 'added', 'modified', 'deleted' lists
        """

    def restore_checkpoint(self, checkpoint_id: str, backup_current: bool = True):
        """Restore state from checkpoint

        Args:
            checkpoint_id: ID of checkpoint to restore
            backup_current: Create backup of current state (default: True)
        """

    def delete_checkpoint(self, checkpoint_id: str):
        """Delete checkpoint

        Args:
            checkpoint_id: ID of checkpoint to delete
        """
```

## Error Handling

### Common Errors

**Checkpoint not found:**
```
ValueError: Checkpoint checkpoint_20251217_143022 not found
```
**Solution**: Verify checkpoint ID with `list` command

**Hash mismatch during restore:**
```
IntegrityError: Checkpoint hash mismatch (corrupted)
```
**Solution**: Checkpoint file corrupted, cannot restore safely

**Insufficient disk space:**
```
OSError: No space left on device
```
**Solution**: Delete old checkpoints or free up disk space

### Recovery Strategies

**If checkpoint restore fails:**
1. Check checkpoint integrity: `python3 scripts/checkpoint-manager.py verify checkpoint_ID`
2. Try older checkpoint if available
3. Manually rebuild state from task-overview.md
4. Report corruption to prevent using bad checkpoint

**If checkpoint creation fails:**
1. Check disk space: `df -h`
2. Check permissions: `ls -la .claude/checkpoints/`
3. Verify tasks directory exists: `ls .claude/tasks/`
4. Continue without checkpoint (add note to task)

## Performance

### Checkpoint Operation Times

| Operation | Typical Time | Notes |
|-----------|-------------|-------|
| Create (20 tasks) | 50-100ms | Includes compression |
| List | <10ms | Reads metadata only |
| Diff | 20-50ms | Compares file hashes |
| Restore | 100-200ms | Includes decompression |

### Optimization Tips

1. **Use compression**: Already enabled by default (gzip)
2. **Batch creates**: Create multiple checkpoints in single script run
3. **Async creates**: Don't wait for checkpoint completion if not critical
4. **Selective restore**: Restore only specific files if needed

## Testing

### Test Checkpoint System

```python
# Test checkpoint creation
def test_create_checkpoint():
    manager = CheckpointManager()
    checkpoint_id = manager.create_checkpoint("Test checkpoint")
    assert checkpoint_id.startswith("checkpoint_")

    checkpoints = manager.list_checkpoints()
    assert checkpoint_id in [cp['id'] for cp in checkpoints]

# Test restore
def test_restore_checkpoint():
    manager = CheckpointManager()

    # Create initial state
    checkpoint_id = manager.create_checkpoint("Before changes")

    # Make changes
    # ... modify task files ...

    # Restore
    manager.restore_checkpoint(checkpoint_id)

    # Verify restoration
    # ... check task files match checkpoint ...
```

## Related Documentation

- **Checkpoint Manager Script**: `scripts/checkpoint-manager.py`
- **Task Schema**: `.claude/reference/task-schema-consolidated.md` (progress.checkpoints field)
- **Complete Task Command**: `.claude/commands/complete-task.md` (checkpoint integration)
- **Error Recovery**: `.claude/reference/error-recovery.md`

## Future Enhancements

Planned improvements:
- Incremental checkpoints (only changed files)
- Cloud backup integration
- Automatic cleanup policies
- Checkpoint diffs visualization
- Rollback preview (dry-run restore)
- Checkpoint branching (multiple states)

## Troubleshooting

### Checkpoints taking too much space?
```bash
# Compress old checkpoints more aggressively
python3 scripts/checkpoint-manager.py compress --all --level 9

# Archive old checkpoints
python3 scripts/checkpoint-manager.py archive --older-than 30d
```

### Lost checkpoints after git operations?
Add `.claude/checkpoints/` to `.gitignore`:
```
.claude/checkpoints/
```
Checkpoints are local working state, not project artifacts.

### Checkpoint restore not working?
```bash
# Verify checkpoint integrity
python3 scripts/checkpoint-manager.py verify checkpoint_ID

# If corrupted, try previous checkpoint
python3 scripts/checkpoint-manager.py list
python3 scripts/checkpoint-manager.py restore checkpoint_OLDER_ID
```

## Summary

The checkpoint system provides:
- Fast, automated state snapshots
- Safe experimentation and rollback
- Recovery from errors
- Long-task state preservation
- Minimal performance overhead

**Use checkpoints to**:
- Preserve known-good states
- Enable safe experimentation
- Recover from failures
- Track task progress milestones

**Integration points**:
- `complete-task.md`: Auto-checkpoints every 3 steps
- `breakdown.md`: Checkpoint before task breakdown
- Validation gates: Checkpoint before risky operations
- Manual: User-triggered checkpoints at any time
