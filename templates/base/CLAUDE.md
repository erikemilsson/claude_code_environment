# Project: [Your Project Name]

## What I'm Building
[2-3 sentence description of the project goal and scope]

## Quick Start

### Current Tasks
See `.claude/tasks/task-overview.md` for all tasks with difficulty scoring, dependencies, and status tracking.

### Available Commands
- `@.claude/commands/complete-task.md <task_id>` - Start and finish a task with proper tracking
- `@.claude/commands/breakdown.md <task_id>` - Split difficulty ≥7 tasks into manageable subtasks
- `@.claude/commands/sync-tasks.md` - Update task overview from JSON files
- `@.claude/commands/update-tasks.md` - Validate task system health

## Working on Tasks

**Before starting work:**
1. Check `.claude/tasks/task-overview.md` for available tasks
2. Look for 🔴 markers (difficulty ≥7) - these MUST be broken down first
3. Ensure dependencies are completed

**To start a task:**
Use `@.claude/commands/complete-task.md <task_id>` - this handles status tracking automatically

**For complex tasks:**
Use `@.claude/commands/breakdown.md <task_id>` to split into subtasks. Parent will auto-complete when all subtasks finish.

## Task Status Legend
- **Pending**: Not started
- **In Progress**: Currently working
- **Blocked**: Cannot proceed (needs blocker resolution)
- **Broken Down**: Split into subtasks (work on subtasks, parent auto-completes)
- **Finished**: Complete

## Task Management
Tasks are stored as individual JSON files in `.claude/tasks/`. The `task-overview.md` is auto-generated via `sync-tasks.md`.

**Key rules:**
- Tasks with difficulty ≥7 must be broken down before work begins
- "Broken Down" tasks cannot be worked on directly - work on their subtasks
- Parent tasks auto-complete when all subtasks are finished
- Always use `complete-task.md` to ensure proper status tracking

## Navigation Rules
- **Project understanding** → `.claude/context/overview.md`
- **Task details** → `.claude/tasks/task-*.json` and `task-overview.md`
- **Difficulty scoring** → `.claude/reference/difficulty-guide.md`
- **Breakdown process** → `.claude/reference/breakdown-workflow.md`
- **Validation rules** → `.claude/reference/validation-rules.md`

## Current Focus
[What you're working on right now - update as you progress]

Next task: [Specific task ID and title]
