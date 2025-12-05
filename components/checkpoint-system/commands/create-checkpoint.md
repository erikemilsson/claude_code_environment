# Create Checkpoint Command

## Purpose
Capture current state before making changes to enable rollback if needed.

## Context Required
- Task ID to create checkpoint for
- Task must have files_affected defined
- Optional: checkpoint type (defaults to pre-execution)
- Optional: description

## Process

### 1. Load Task Information
- Read `.claude/tasks/task-{id}.json`
- Extract `files_affected` array
- Verify task has workable status (not "Broken Down")

### 2. Generate Checkpoint ID
- Determine next sequence number:
  - List existing checkpoints in `.claude/checkpoints/` matching `chk-{task_id}-*`
  - Find highest sequence number
  - Increment by 1 (or use 1 if no existing checkpoints)
- Format: `chk-{task_id}-{sequence}`
- Example: `chk-42-3` (3rd checkpoint for task 42)

### 3. Create Checkpoint Directory
- Create `.claude/checkpoints/{checkpoint_id}/`
- This will store backup copies of files

### 4. Process Each File
For each file in `files_affected`:

**If file exists:**
- Calculate SHA-256 hash of current contents
- Create subdirectories in checkpoint folder to match file structure
- Copy file to `.claude/checkpoints/{checkpoint_id}/{relative_path}`
- Record metadata:
  ```json
  {
    "path": "path/to/file.py",
    "hash": "abc123...",
    "backup_path": ".claude/checkpoints/chk-42-3/path/to/file.py",
    "existed": true
  }
  ```

**If file doesn't exist:**
- Record that file will be created:
  ```json
  {
    "path": "path/to/new-file.py",
    "hash": "",
    "backup_path": "",
    "existed": false
  }
  ```

### 5. Capture Task State
- Create snapshot of entire task JSON
- This enables restoring task status if rollback needed

### 6. Write Checkpoint Metadata
Create `.claude/checkpoints/{checkpoint_id}/checkpoint.json`:
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
    },
    {
      "path": "tests/test_api.py",
      "hash": "",
      "backup_path": "",
      "existed": false
    }
  ],
  "task_state": {
    "id": "42",
    "title": "Integrate payment API",
    "status": "In Progress",
    ...
  }
}
```

### 7. Report Success
Display to user:
```
✓ Checkpoint chk-42-3 created
  Type: pre-execution
  Files captured: 3 existing, 2 new
  Location: .claude/checkpoints/chk-42-3/

  Rollback available: Use rollback-to command with checkpoint ID
```

## Output Location
- `.claude/checkpoints/{checkpoint_id}/checkpoint.json` - Metadata
- `.claude/checkpoints/{checkpoint_id}/{file_paths}` - Backup copies

## Critical Rules
- Always calculate file hashes for change detection
- Preserve directory structure in backup folder
- Record whether files existed at checkpoint time
- Never overwrite existing checkpoint (increment sequence)
- Checkpoint creation should be fast (don't backup large binary files unnecessarily)

## Integration Points
- Called automatically by `complete-task.md` at step 4 (before work starts)
- Can be called manually at any time during task execution
- Used by `rollback-to.md` to restore state

## Error Handling
- If task not found: ERROR "Task {id} does not exist"
- If no files_affected: WARNING "Task has no files_affected, checkpoint will only capture task state"
- If checkpoint directory creation fails: ERROR "Cannot create checkpoint directory"
- If file copy fails: WARNING "Could not backup {file}, continuing with other files"
