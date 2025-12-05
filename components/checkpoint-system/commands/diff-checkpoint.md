# Diff Checkpoint Command

## Purpose
Compare current state against a checkpoint to show what changed since the checkpoint was created.

## Context Required
- Checkpoint ID to compare against (format: `chk-{task_id}-{sequence}`)
- Optional: specific files to compare (compare subset)
- Optional: diff format (unified, side-by-side, summary-only)

## Process

### 1. Load Checkpoint Metadata
- Read `.claude/checkpoints/{checkpoint_id}/checkpoint.json`
- Verify checkpoint exists and is valid
- Extract file list and hashes

### 2. Compare Each File
For each file in checkpoint metadata:

**Calculate current state:**
- Check if file exists now
- Calculate current file hash
- Compare to checkpoint hash

**Determine change type:**
- `UNCHANGED` - Hash matches, no changes
- `MODIFIED` - File exists, hash differs
- `DELETED` - File existed at checkpoint, missing now
- `SAME_MISSING` - File didn't exist at checkpoint, still missing

**Find new files:**
- Look for files that exist now but weren't in checkpoint
- Mark as `ADDED` (created after checkpoint)

### 3. Display Summary
Show overview of changes:
```
Comparing current state to checkpoint chk-42-2
Created: 2025-12-05T11:30:00Z (45 minutes ago)

Summary:
  3 files modified
  1 file added
  0 files deleted
  2 files unchanged

Modified Files:
  src/api/client.py
  tests/test_api.py
  src/config.py

Added Files:
  src/api/auth.py

Unchanged Files:
  src/utils.py
  tests/conftest.py
```

### 4. Display File Diffs
For each modified file, show unified diff:

```
─────────────────────────────────────
File: src/api/client.py
─────────────────────────────────────
@@ -15,7 +15,7 @@ class APIClient:
         self.base_url = base_url
-        self.timeout = 30
+        self.timeout = 60
         self.session = requests.Session()

 @@ -42,8 +42,10 @@ def post(self, endpoint, data):
-        response = requests.post(url, json=data)
-        return response.json()
+        response = requests.post(url, json=data, timeout=self.timeout)
+        if response.status_code != 200:
+            raise APIError(f"Request failed: {response.status_code}")
+        return response.json()
```

### 5. Task State Comparison
Compare current task state to checkpoint snapshot:
```
─────────────────────────────────────
Task State Changes:
─────────────────────────────────────
  Status: In Progress (unchanged)
  Updated date: 2025-12-05T11:30:00Z → 2025-12-05T12:15:00Z
  Notes: (2 lines added)
```

### 6. Provide Rollback Suggestion
If changes found:
```
To restore checkpoint state:
  rollback-to chk-42-2

This would:
  - Revert 3 modified files
  - Remove 1 added file
  - Keep 2 unchanged files
```

If no changes:
```
✓ Current state matches checkpoint chk-42-2
  No rollback needed
```

## Output Location
- Console display (no file modifications)
- Optional: write diff to file with `--output diff.txt`

## Diff Formats

### Summary Only (--summary)
```
src/api/client.py      MODIFIED  (+12 lines, -5 lines)
tests/test_api.py      MODIFIED  (+8 lines, -2 lines)
src/api/auth.py        ADDED     (new file, 45 lines)
src/config.py          MODIFIED  (+3 lines, -3 lines)
src/utils.py           UNCHANGED
```

### Unified Diff (Default)
Standard unified diff format with context lines (shown above)

### Side-by-Side (--side-by-side)
```
Checkpoint (chk-42-2)          |  Current State
─────────────────────────────────────────────────
self.timeout = 30              |  self.timeout = 60
response = requests.post(...)  |  response = requests.post(..., timeout=self.timeout)
return response.json()         |  if response.status_code != 200:
                               |      raise APIError(...)
                               |  return response.json()
```

### Stat Only (--stat)
```
3 files changed, 23 insertions(+), 10 deletions(-)
src/api/client.py     | 15 ++++++++-------
tests/test_api.py     | 10 +++++-----
src/api/auth.py       | 45 +++++++++++++++++++++++++++++++++++++++++++++
src/config.py         |  6 +++---
```

## Critical Rules
- Never modify files (read-only comparison)
- Use actual file content for diff (not just hashes)
- Show context lines for readability
- Handle binary files gracefully (show "Binary file differs")
- Compare task state as well as files

## Integration Points
- Called before rollback-to to preview changes
- Used during troubleshooting to understand what changed
- Referenced by list-checkpoints for per-checkpoint summaries

## Error Handling
- If checkpoint not found: ERROR "Checkpoint {id} does not exist"
- If checkpoint.json invalid: ERROR "Checkpoint metadata corrupted"
- If backup file missing: WARNING "Cannot compare {file}, backup not found"
- If current file unreadable: WARNING "Cannot read {file}, skipping comparison"

## Advanced Features

### Selective Comparison
Compare only specific files:
```
diff-checkpoint chk-42-2 --files src/api/client.py tests/test_api.py

Comparing 2 files only (others ignored)
```

### Ignore Whitespace
```
diff-checkpoint chk-42-2 --ignore-whitespace

Summary:
  2 files modified (ignoring whitespace changes)
  1 file has only whitespace changes (ignored)
```

### Context Lines
Control diff context:
```
diff-checkpoint chk-42-2 --context 5

(Shows 5 lines of context instead of default 3)
```

### Export Diff
Save to file for review or sharing:
```
diff-checkpoint chk-42-2 --output changes.diff

✓ Diff written to changes.diff (1.2 KB)
  Apply with: patch -p1 < changes.diff (to undo changes)
```

### Hash-Only Mode
Quick check without full diff:
```
diff-checkpoint chk-42-2 --hash-only

Fast comparison (hash-based):
  src/api/client.py      MODIFIED  (hash differs)
  tests/test_api.py      MODIFIED  (hash differs)
  src/api/auth.py        ADDED     (not in checkpoint)
  src/config.py          MODIFIED  (hash differs)
  src/utils.py           UNCHANGED (hash matches)

Use without --hash-only to see line-by-line differences
```
