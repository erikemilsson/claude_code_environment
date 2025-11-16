# Task Overview

**Last Updated**: [Not generated]

---

## Phase Status

**Current Phase**: Phase 0 - Initialization

Tasks will be generated after Phase 0 completion.

See `.claude/tasks/_phase-0-status.md` for initialization progress.

---

## Instructions

1. Complete Phase 0 by running:
   - `@.claude/commands/initialize-project.md`
   - `@.claude/commands/resolve-ambiguities.md`
   - `@.claude/commands/generate-artifacts.md`
   - `@.claude/commands/extract-queries.md`

2. After Phase 0, this file will contain:
   - Task table with all planned work
   - Status indicators (🔴 high difficulty, 🔵 broken down)
   - Subtask hierarchy
   - Current sprint/focus

3. Use these commands to manage tasks:
   - `@.claude/commands/complete-task.md [id]` - Work on a task
   - `@.claude/commands/breakdown.md [id]` - Split high-difficulty tasks
   - `@.claude/commands/sync-tasks.md` - Update this overview
   - `@.claude/commands/update-tasks.md` - Validate task structure

---

## Task Format (After Generation)

Tasks will appear in this format:

| ID | Title | Difficulty | Status | Dependencies | Notes |
|----|-------|------------|--------|--------------|-------|
| 1  | Task name | 5 | Pending | - | Description |
| 2  | High-difficulty task | 8 🔴 | Pending | 1 | Needs breakdown |
| 2  | ↳ Subtask 1 | 4 | Pending | 1 | Parent: 2 |
| 2  | ↳ Subtask 2 | 5 | Pending | 2.1 | Parent: 2 |

**Markers**:
- 🔴 = Difficulty ≥7, needs breakdown before starting
- 🔵 = Status "Broken Down (X/Y done)", shows subtask progress
- ↳ = Subtask indentation

---

## Phase 0 Completion

This file will be automatically updated when `generate-artifacts.md` runs successfully.
