# Rollback to Checkpoint Command

## Purpose
Restore files and task state to a previous checkpoint when work needs to be undone.

## Context Required
- Checkpoint ID to restore (format: `chk-{task_id}-{sequence}`)
- Optional: whether to restore task status (defaults to yes)
- Optional: selective file restoration (restore only specific files)

## Process

### 1. Load Checkpoint Metadata
- Read `.claude/checkpoints/{checkpoint_id}/checkpoint.json`
- Verify checkpoint exists and is valid
- Display checkpoint information:
  ```
  Checkpoint: chk-42-3
  Created: 2025-12-05T14:30:00Z
  Type: pre-execution
  Description: Before starting API integration work
  Files: 3 existing, 2 new (would be removed)
  Task status at checkpoint: In Progress
  ```

### 2. Analyze Current State
For each file in checkpoint metadata:

**Compare current state to checkpoint:**
- Calculate current file hash (if exists)
- Compare to checkpoint hash
- Determine action needed:
  - `RESTORE` - File changed, will restore from backup
  - `UNCHANGED` - File matches checkpoint, skip
  - `REMOVE` - File was created after checkpoint, will delete
  - `MISSING` - File existed at checkpoint but missing now, will restore

**Generate restoration plan:**
```
Restoration Plan:
  ✓ src/api/client.py - RESTORE (changed)
  - src/api/utils.py - UNCHANGED (skip)
  ✗ tests/test_new.py - REMOVE (created after checkpoint)
  ⚠ src/config.py - MISSING (will restore)
```

### 3. Confirm with User
Display plan and ask for confirmation:
```
⚠ WARNING: This will modify 2 files and remove 1 file

Continue with rollback? [y/N]
```

**Safety features:**
- Default to NO (require explicit confirmation)
- Show exactly what will change
- Option to create a checkpoint of current state before rollback

### 4. Restore Files
For each file requiring action:

**RESTORE (file changed):**
- Copy from `.claude/checkpoints/{checkpoint_id}/{path}` to original location
- Report: `✓ Restored src/api/client.py`

**REMOVE (file created after):**
- Delete current file
- Report: `✗ Removed tests/test_new.py (didn't exist at checkpoint)`

**MISSING (existed at checkpoint):**
- Restore from backup
- Report: `⚠ Restored src/config.py (was missing)`

**UNCHANGED (matches checkpoint):**
- Skip (no action needed)
- Report: `- Skipped src/api/utils.py (unchanged)`

### 5. Restore Task Status (Optional)
If user confirmed task status restoration:
- Load `task_state` from checkpoint metadata
- Update `.claude/tasks/task-{id}.json` with snapshot
- Add note: `"Restored from checkpoint chk-42-3 on {timestamp}"`
- Report:
  ```
  ✓ Task status restored
    Status: In Progress → In Progress
    Notes: Updated with restoration record
  ```

**If user declined task restoration:**
- Keep current task status
- Still add note about file restoration: `"Files restored from checkpoint chk-42-3 on {timestamp}"`

### 6. Report Results
Display summary:
```
✓ Rollback to chk-42-3 complete

  Files restored: 2
  Files removed: 1
  Files unchanged: 1
  Task status: Restored

  Checkpoint preserved at: .claude/checkpoints/chk-42-3/
```

### 7. Preservation
- Never delete checkpoint after rollback (may need to rollback again)
- Checkpoint remains available for future reference or re-rollback

## Output Location
- Modified files in their original locations
- Updated task JSON file
- Checkpoint directory unchanged (preserved)

## Critical Rules
- **Always confirm before modifying files** - Rollback is destructive
- **Use hash comparison** - Only restore actually changed files
- **Preserve checkpoints** - Never delete after use
- **Add restoration notes** - Document when rollback occurred
- **Safety first** - Offer to create pre-rollback checkpoint

## Selective Restoration
Allow restoring only specific files:
```
rollback-to chk-42-3 --files src/api/client.py tests/test_api.py
```

This restores only specified files, leaves others unchanged.

## Integration Points
- Called manually when work needs to be undone
- Referenced by post-execution gate when failures detected
- Can be chained (rollback to checkpoint, then rollback again to earlier checkpoint)

## Error Handling
- If checkpoint not found: ERROR "Checkpoint {id} does not exist"
- If checkpoint.json invalid: ERROR "Checkpoint metadata corrupted"
- If backup file missing: ERROR "Cannot restore {file}, backup not found"
- If file restore fails: WARNING "Could not restore {file}, continuing with others"
- If user cancels: INFO "Rollback cancelled, no changes made"

## Advanced Features

### Diff Before Rollback
Show detailed differences before confirming:
```
Show differences? [y/N] y

src/api/client.py:
  - Line 42: response = requests.post(url, json=data)
  + Line 42: response = requests.get(url, params=data)
  - Line 55: return response.json()
  + Line 55: return response.text
```

### Partial Rollback
Prompt for each file:
```
Restore src/api/client.py? [y/N/a] y  (y=yes, N=no, a=all)
Restore tests/test_api.py? [y/N/a] N
Remove tests/test_new.py? [y/N/a] y
```

### Pre-Rollback Safety Checkpoint
Before any changes:
```
Create safety checkpoint before rollback? [Y/n] y
✓ Created checkpoint chk-42-4 (current state)
  You can rollback to chk-42-4 if needed
```
