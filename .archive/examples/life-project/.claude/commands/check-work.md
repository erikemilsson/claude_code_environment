# Check Work

Review session changes for issues, then fix them.

## Usage
```
/check-work
```

## Process

### 1. Identify Changes
- Get all modified/new files in this session (use `git diff` for uncommitted changes)
- If no changes detected, report "No changes to review" and exit

### 2. Review for Issues
For each changed file, check for:
- **Bugs**: Logic errors, off-by-one, null/undefined handling
- **Edge cases**: Missing boundary checks, empty inputs, error paths
- **Inefficiencies**: Unnecessary loops, repeated work, obvious optimizations
- **Inconsistencies**: Style mismatches with surrounding code, naming conventions

### 3. Report & Fix
For each issue found:
1. **Identify**: State the file, location, and issue
2. **Suggest**: Explain the fix
3. **Implement**: Make the change

If no issues found, confirm: "Reviewed [N] files, no issues detected."
