# Scenario 31: Corrupted and Malformed Task JSON

Verify that `/work` and `/health-check` gracefully handle corrupted, malformed, or structurally invalid task JSON files.

## Context

Task JSON files can become corrupted through various means: manual editing errors, agent write failures (partial writes during crash), merge conflicts, or encoding issues. The system must detect these problems and surface them clearly rather than crashing, silently skipping tasks, or producing confusing downstream errors.

## State

- `.claude/tasks/` contains 5 task files:
  - `task-1.json`: Valid, status "Finished"
  - `task-2.json`: Invalid JSON (truncated — missing closing `}`)
  - `task-3.json`: Valid JSON but missing required `title` field
  - `task-4.json`: Valid JSON, valid schema, status "Pending"
  - `task-5.json`: Valid JSON but `status` field contains "Compleet" (typo, not a valid status)

---

## Trace 31A: `/work` encounters invalid JSON during task scan

- **Path:** work.md Step 1 → task file reading; Step 2c → routing algorithm

### Scenario

User runs `/work`. Step 1 reads all task files. `task-2.json` fails to parse.

### Expected

1. `/work` reports the parse error for `task-2.json` with filename and error description
2. Valid tasks (1, 3, 4, 5) are still loaded and processed
3. User informed: "1 task file could not be read — run `/health-check` for details"
4. `/work` continues with loadable tasks rather than aborting entirely
5. `task-2.json` excluded from routing, progress counts, and dashboard

### Pass criteria

- [ ] Parse error reported with filename (not a generic "something went wrong")
- [ ] Valid tasks still processed — one bad file doesn't halt everything
- [ ] User directed to `/health-check` for repair guidance
- [ ] Corrupted task excluded from all calculations (progress, phase completion, dependencies)

### Fail indicators

- `/work` crashes or aborts on first invalid file
- Corrupted file silently skipped with no warning
- Corrupted task counted in progress stats (e.g., "5 total" when only 4 are loadable)
- Valid tasks blocked because the scan "failed"

---

## Trace 31B: `/health-check` validates task schema

- **Path:** health-check.md Part 1 (Task Validation)

### Scenario

`/health-check` runs and encounters all 5 task files.

### Expected

1. `task-2.json`: **Error** — invalid JSON, cannot parse. Listed under Non-Fixable Issues: "Need to examine file."
2. `task-3.json`: **Error** — missing required field `title`. Listed under Non-Fixable Issues: "Need human input for values."
3. `task-5.json`: **Error** — unknown status value "Compleet". Listed under Non-Fixable Issues: "Need to determine correct status." Valid values listed for reference.
4. `task-1.json`, `task-4.json`: Pass validation.

### Pass criteria

- [ ] Invalid JSON detected and reported with specific parse error
- [ ] Missing required fields flagged as errors (not warnings)
- [ ] Invalid enum values flagged as errors with valid values listed for reference
- [ ] None of these issues offered auto-fix (all require human judgment per health-check design)
- [ ] Summary shows: "3 errors across 5 task files"

### Fail indicators

- Invalid JSON reported as "missing field" (wrong error type)
- Missing fields not caught (only JSON syntax checked)
- Auto-fix offered for truncated files (dangerous — data loss)
- No distinction between errors (must fix) and warnings (should fix)

---

## Trace 31C: Dependency references point to nonexistent tasks

- **Path:** health-check.md Part 1 → Check 2 (Relationship Integrity) and Check 5 (Status Rules); work.md Step 2c

### Scenario

`task-4.json` has `depends_on: ["2", "99"]`. Task 2 exists but is corrupted. Task 99 doesn't exist at all.

### Expected

1. `/health-check` flags two issues on Task 4:
   - Dependency on Task 2: "Referenced task file is corrupted/unreadable"
   - Dependency on Task 99: "Referenced task does not exist"
2. `/work` treats Task 4 as Blocked (unresolvable dependencies)
3. Dashboard shows Task 4 with dependency issue noted

### Pass criteria

- [ ] Dangling dependency references detected (task 99)
- [ ] Dependency on corrupted task detected (task 2)
- [ ] Task with unresolvable deps treated as Blocked, not Pending
- [ ] Both issues reported separately with specific task IDs

### Fail indicators

- Task 4 dispatched despite unresolvable dependencies
- Dangling references silently ignored
- Generic "dependency error" without specifying which dependency
- `/work` crashes when resolving dependency on corrupted task
