# Workflow Guide

How to use the Claude Code environment in your projects.

## Setup Workflow

### 1. Copy the base

```bash
# Option A: Copy entire base folder
cp -r /path/to/claude_code_environment/base/ /path/to/your-project/

# Option B: Just copy .claude folder to existing project
cp -r /path/to/claude_code_environment/base/.claude/ /path/to/existing-project/.claude/
cp /path/to/claude_code_environment/base/CLAUDE.md /path/to/existing-project/CLAUDE.md
```

### 2. Customize CLAUDE.md

Update the template with your project details:

```markdown
# CLAUDE.md

## Project Overview
[What your project does]

## Technology Stack
- Language: [e.g., Python, TypeScript]
- Framework: [e.g., FastAPI, React]
- Database: [e.g., PostgreSQL]

## Conventions
[Your coding style, naming conventions, etc.]
```

### 3. Add context

Fill in `.claude/context/overview.md` with:
- What the project is
- Current state/phase
- Key decisions made
- Important notes

### 4. Create initial tasks

Create JSON files in `.claude/tasks/`:

```json
{
  "id": "1",
  "title": "Set up project",
  "status": "Pending",
  "difficulty": 3
}
```

Run `/sync-tasks` to generate the overview.

## Daily Workflow

### Starting work

1. Run `/health-check` to check system health
2. Review `.claude/tasks/task-overview.md` to see what's pending
3. Pick a task to work on

### Working on a task

1. Run `/complete-task {id}` to mark as In Progress
2. Do the work
3. Add notes to the task JSON
4. Run `/complete-task {id}` again to mark as Finished
5. Run `/sync-tasks` to update overview

### Breaking down complex tasks

For tasks with difficulty >= 7:

1. Run `/breakdown {id}`
2. Claude creates subtasks with difficulty <= 6
3. Work on subtasks instead of parent
4. Parent auto-completes when all subtasks finish

## Task States

```
Pending --> In Progress --> Finished
              |
              v
           Blocked (document why)

Pending --> Broken Down --> [subtasks complete] --> Finished
```

## Tips

### Keep tasks focused

- One task = one deliverable
- If a task has multiple parts, consider breaking it down
- Subtasks should be independently completable

### Use notes

Add notes to tasks to track:
- What was done
- Issues encountered
- Follow-up items
- Links to relevant commits/PRs

### Sync frequently

Run `/sync-tasks` after:
- Completing tasks
- Breaking down tasks
- Starting a session (to see current state)

### Handle blockers

When a task is blocked:
1. Set status to "Blocked"
2. Document the blocker in notes
3. Create a task to resolve the blocker if needed
