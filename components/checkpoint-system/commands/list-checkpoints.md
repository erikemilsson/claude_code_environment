# List Checkpoints Command

## Purpose
Display all checkpoints for a task with metadata to help choose which checkpoint to restore.

## Context Required
- Task ID to list checkpoints for
- Optional: filter by checkpoint type (pre-execution, mid-execution, manual)

## Process

### 1. Find Checkpoints
- Search `.claude/checkpoints/` for directories matching `chk-{task_id}-*`
- Load `checkpoint.json` from each directory
- Sort by sequence number (oldest to newest)

### 2. Display Checkpoint List
Format each checkpoint as:
```
Checkpoint: chk-42-1
  Created: 2025-12-05T10:15:00Z (2 hours ago)
  Type: pre-execution
  Description: Before starting API integration work
  Files: 3 existing, 2 new
  Task status: Pending → In Progress

Checkpoint: chk-42-2
  Created: 2025-12-05T11:30:00Z (45 minutes ago)
  Type: mid-execution
  Description: After implementing basic authentication
  Files: 5 existing, 0 new
  Task status: In Progress

Checkpoint: chk-42-3
  Created: 2025-12-05T12:00:00Z (15 minutes ago)
  Type: manual
  Description: Before refactoring error handling
  Files: 5 existing, 1 new
  Task status: In Progress

Total: 3 checkpoints for task 42
```

### 3. Add Current State Indicator
Show which checkpoint represents current state:
```
Checkpoint: chk-42-3 [CURRENT]
  (Files match current state - no changes since checkpoint)

OR

Checkpoint: chk-42-3
  (Current state differs - 2 files changed, 1 file added)
```

### 4. Provide Restoration Guidance
At the end of the list:
```
To restore a checkpoint:
  rollback-to chk-42-{sequence}

To compare current state against checkpoint:
  diff-checkpoint chk-42-{sequence}

To create new checkpoint:
  create-checkpoint {task_id}
```

## Output Location
- Console display (no file modifications)

## Display Options

### Compact Format
One line per checkpoint:
```
chk-42-1 | 2h ago | pre-execution | 3 files | Pending→In Progress
chk-42-2 | 45m ago | mid-execution | 5 files | In Progress
chk-42-3 | 15m ago | manual | 6 files | In Progress [CURRENT]
```

### Detailed Format (Default)
Multi-line with full metadata (shown above)

### Filter by Type
```
list-checkpoints 42 --type pre-execution

Showing pre-execution checkpoints only:

Checkpoint: chk-42-1
  Created: 2025-12-05T10:15:00Z (2 hours ago)
  ...
```

## Critical Rules
- Sort by sequence number (chronological order)
- Show relative timestamps (e.g., "2 hours ago") for quick reference
- Indicate current state matches
- Never modify checkpoints (read-only operation)

## Integration Points
- Called before rollback-to to choose checkpoint
- Called after create-checkpoint to confirm creation
- Used in troubleshooting to review checkpoint history

## Error Handling
- If task not found: ERROR "Task {id} does not exist"
- If no checkpoints exist: INFO "No checkpoints found for task {id}"
- If checkpoint.json corrupted: WARNING "Checkpoint {id} metadata invalid, skipping"

## Advanced Features

### Timeline View
Show checkpoints on timeline with task events:
```
Task 42 Timeline:

10:00 - Task created
10:15 - [chk-42-1] pre-execution checkpoint
10:20 - Status: Pending → In Progress
11:30 - [chk-42-2] mid-execution checkpoint
12:00 - [chk-42-3] manual checkpoint
12:15 - [CURRENT STATE]
```

### File Change Summary
Show which files changed between checkpoints:
```
Checkpoint: chk-42-2
  Changes since chk-42-1:
    Modified: src/api/client.py
    Modified: tests/test_api.py
    Added: src/api/auth.py
```

### Storage Size
Show disk space used by each checkpoint:
```
Checkpoint: chk-42-3
  Storage: 145 KB (3 files backed up)
  Location: .claude/checkpoints/chk-42-3/
```
