# Task Management Component (Simplified)

Lightweight task tracking for Claude Code projects. Keeps you organized without getting in the way.

## What You Get

```
.claude/
├── tasks/
│   ├── task-overview.md    # Summary of all tasks
│   └── task-*.json         # Individual task files
└── commands/
    ├── complete-task.md    # Start/finish tasks
    ├── breakdown.md        # Split complex tasks
    ├── sync-tasks.md       # Update overview
    └── update-tasks.md     # Health check
```

## Quick Start

### 1. Create a task
```json
{
  "id": "1",
  "title": "Build login page",
  "status": "Pending",
  "difficulty": 4
}
```

### 2. Work on it
```
/complete-task 1
```

### 3. See progress
```
/sync-tasks
```

## Task Schema

Only 3 required fields:

```json
{
  "id": "1",
  "title": "What needs doing",
  "status": "Pending"
}
```

Optional fields when useful:
- `description` - More detail
- `difficulty` - 1-10 scale (break down >= 7)
- `dependencies` - Task IDs that must finish first
- `subtasks` - Child task IDs
- `parent_task` - Parent task ID
- `notes` - Progress, blockers, completion summary
- `owner` - Who does this: "claude", "human", or "both"

## Core Concepts

### Status Values
| Status | Meaning |
|--------|---------|
| Pending | Not started |
| In Progress | Working on it |
| Blocked | Can't proceed (add notes explaining why) |
| Broken Down | Split into subtasks - work on those instead |
| Finished | Done |

### Difficulty (Optional)
Use difficulty to signal when a task needs breaking down:
- **1-6**: Just do it
- **7-10**: Consider breaking down first

### Parent/Child Tasks
When you break down a task:
1. Parent becomes "Broken Down"
2. Create subtask files with `parent_task` pointing to parent
3. Work on subtasks
4. Parent auto-completes when all subtasks finish

## Commands

| Command | Purpose |
|---------|---------|
| `/complete-task {id}` | Start working, then mark finished |
| `/breakdown {id}` | Split into subtasks |
| `/sync-tasks` | Regenerate task-overview.md |
| `/update-tasks` | Check for issues |
| `/generate-handoff-guide` | Create Claude/Human task overview with diagram |

## Example Workflow

**Big task:**
```json
{"id": "1", "title": "Build auth system", "status": "Pending", "difficulty": 8}
```

**After breakdown:**
```
Task 1: "Broken Down", subtasks: ["1_1", "1_2", "1_3"]
Task 1_1: "Setup OAuth" (difficulty 5)
Task 1_2: "Login flow" (difficulty 4)
Task 1_3: "Session handling" (difficulty 5)
```

**After completing all subtasks:**
```
Task 1: "Finished" (auto-completed)
Task 1_1: "Finished"
Task 1_2: "Finished"
Task 1_3: "Finished"
```

## Claude/Human Handoffs

Some tasks Claude can't do autonomously (Power BI UI, manual testing, approvals). Use the `owner` field:

```json
{"id": "1", "title": "Write M queries", "owner": "claude"}
{"id": "2", "title": "Configure PBI visuals", "owner": "human", "dependencies": ["1"]}
{"id": "3", "title": "Review together", "owner": "both", "dependencies": ["2"]}
```

Run `/generate-handoff-guide` to create:
- Mermaid diagram showing workflow
- Human task checklist
- Clear handoff points

## Philosophy

This system exists to:
1. **Show what needs doing** - task-overview.md
2. **Track what's done** - status updates
3. **Handle complexity** - break down big tasks
4. **Clarify handoffs** - who does what

It does NOT try to:
- Track your confidence levels
- Monitor your momentum
- Validate every step you take
- Create checkpoints constantly

With capable models like Claude Opus 4.5, you don't need guardrails - you need visibility.
