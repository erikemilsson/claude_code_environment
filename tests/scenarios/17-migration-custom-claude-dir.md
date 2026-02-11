# Scenario 17: Migration from Custom .claude/ Task System

Verify that the template handles being applied to a project that already has a `.claude/` directory with an incompatible task management structure.

## Context

This is the most common adoption path: a user has an existing project with a custom `.claude/` setup (different task schema, custom commands, project-specific settings) and wants to adopt the template. The template must detect conflicts, preserve user work, and suggest a migration path rather than silently overwriting.

## State

- Project has existing `.claude/tasks/` with `task-1.json` through `task-29.json` in a DIFFERENT schema:
  - Missing `difficulty` field
  - Uses `status: "Finished"` instead of `"completed"`
  - No `phase` or `decision_dependencies` fields
  - Has fields the template doesn't expect (`assignee`, `sprint`)
- Existing `.claude/commands/` with custom commands (`plan.md`, `update-tasks.md`) that overlap with or extend template commands
- Existing `.claude/settings.local.json` with project-specific permissions
- Existing `.claude/CLAUDE.md` with project-specific instructions

## Trace 17A: Schema mismatch detection

- **Path:** `/setup-check` run after template files are copied in
- `/setup-check` reads existing task files and compares against expected schema
- Finds missing required fields (`difficulty`, `phase`) and non-standard values (`"Finished"`)

### Expected

- `/setup-check` detects schema mismatches in existing task files
- Reports which fields are missing, which have unexpected values
- Does NOT attempt to auto-migrate task files
- Suggests migration steps (add missing fields, map status values)

### Pass criteria

- [ ] Existing task files are not silently overwritten or corrupted
- [ ] Schema differences are surfaced to the user with specific details
- [ ] Missing fields and non-standard values are both detected
- [ ] A clear migration path is suggested

### Fail indicators

- Task files are silently overwritten with template defaults
- `/setup-check` reports "all good" despite schema mismatches
- Task files become unreadable after template application
- Migration is attempted automatically without user consent

---

## Trace 17B: Command collision detection

- **Path:** `/setup-check` → command directory scan
- Existing `plan.md` overlaps conceptually with `/iterate`
- Existing `update-tasks.md` overlaps with `/work complete`
- Template adds `work.md`, `iterate.md`, `breakdown.md`, `health-check.md`, etc.

### Expected

- `/setup-check` reports command name collisions or functional overlaps
- Warns that existing custom commands may conflict with template commands
- Preserves existing commands (does not delete them)
- Suggests renaming or archiving conflicting commands

### Pass criteria

- [ ] Command collisions are reported
- [ ] Existing custom commands are preserved
- [ ] User is advised on how to resolve overlaps
- [ ] No commands are silently deleted or overwritten

### Fail indicators

- Custom commands are silently replaced by template commands
- `/setup-check` doesn't scan the commands directory at all
- User's custom workflow is broken without warning

---

## Trace 17C: User settings preservation

- **Path:** `/setup-check` → settings file handling
- Existing `settings.local.json` has project-specific tool permissions
- Template may ship default settings

### Expected

- Existing `settings.local.json` is preserved completely
- If template settings conflict, the conflict is reported
- User permissions are never downgraded without consent

### Pass criteria

- [ ] User settings are preserved
- [ ] Settings conflicts are reported if they exist
- [ ] No silent permission changes

### Fail indicators

- `settings.local.json` is overwritten with template defaults
- Existing permissions are lost
- User must re-configure tool permissions after template application
