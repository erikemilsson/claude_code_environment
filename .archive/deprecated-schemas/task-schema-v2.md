# Task Schema v2.0 - With Structured Progress Tracking

**DEPRECATED** - This document has been superseded by task-schema-consolidated.md

See: .claude/reference/task-schema-consolidated.md (Created: 2025-12-17)

The progress tracking features from this document have been integrated into the consolidated schema as an optional field.

---

*Version: 2.0 | Created: 2025-12-16*

## Overview

Enhanced task JSON schema with structured progress tracking for multi-step tasks. This schema extends the base task model with detailed progress fields for better visibility and state management.

## Complete Schema Definition

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "difficulty": "number (1-10)",
  "status": "Pending | In Progress | Blocked | Broken Down | Finished",
  "created_date": "YYYY-MM-DD",
  "updated_date": "YYYY-MM-DD",
  "dependencies": ["array of task IDs"],
  "subtasks": ["array of subtask IDs"],
  "parent_task": "task ID or null",
  "files_affected": ["array of file paths"],
  "notes": "string",

  "belief_tracking": {
    "confidence": "number (0-100)",
    "assumptions": ["array or structured array"],
    "validation_status": "pending | validated | invalidated | partial",
    "momentum": {
      "phase": "pending | ignition | building | cruising | coasting | stalling | stopped",
      "velocity": "number (0-100)",
      "last_activity": "YYYY-MM-DD"
    },
    "decision_rationale": "string"
  },

  "progress": {
    "type": "simple | milestone | percentage | step_counter",
    "current_step": "number",
    "total_steps": "number",
    "completion_percentage": "number (0-100)",
    "current_phase": "string",
    "

    "milestones": [
      {
        "id": "number",
        "name": "string",
        "status": "pending | in_progress | complete | skipped",
        "started_at": "ISO 8601 timestamp",
        "completed_at": "ISO 8601 timestamp",
        "notes": "string"
      }
    ],

    "step_history": [
      {
        "step_number": "number",
        "description": "string",
        "status": "complete | failed | skipped",
        "timestamp": "ISO 8601 timestamp",
        "duration_minutes": "number",
        "output": "string (summary of results)"
      }
    ],

    "blocking_step": {
      "step_number": "number",
      "description": "string",
      "blocker_type": "dependency | error | waiting_for_input | resource_unavailable",
      "blocker_details": "string",
      "blocked_since": "ISO 8601 timestamp"
    },

    "checkpoints": [
      {
        "checkpoint_id": "string",
        "step_number": "number",
        "state_file": "path to checkpoint JSON",
        "created_at": "ISO 8601 timestamp",
        "can_resume": "boolean"
      }
    ],

    "metrics": {
      "estimated_time_minutes": "number",
      "actual_time_minutes": "number",
      "steps_completed": "number",
      "steps_failed": "number",
      "steps_skipped": "number",
      "retry_count": "number"
    }
  }
}
```

## Progress Type Patterns

### 1. Simple Progress (Default)

For basic tasks without detailed tracking:

```json
{
  "progress": {
    "type": "simple",
    "completion_percentage": 0
  }
}
```

### 2. Step Counter Progress

For tasks with discrete, sequential steps:

```json
{
  "progress": {
    "type": "step_counter",
    "current_step": 3,
    "total_steps": 10,
    "completion_percentage": 30,
    "current_phase": "Implementing core functionality",
    "step_history": [
      {
        "step_number": 1,
        "description": "Set up project structure",
        "status": "complete",
        "timestamp": "2025-12-16T10:00:00Z",
        "duration_minutes": 15,
        "output": "Created directories and initial files"
      },
      {
        "step_number": 2,
        "description": "Install dependencies",
        "status": "complete",
        "timestamp": "2025-12-16T10:15:00Z",
        "duration_minutes": 5,
        "output": "Installed 42 packages"
      }
    ]
  }
}
```

### 3. Milestone-Based Progress

For tasks organized around key deliverables:

```json
{
  "progress": {
    "type": "milestone",
    "completion_percentage": 60,
    "current_phase": "Testing",
    "milestones": [
      {
        "id": 1,
        "name": "Environment Setup",
        "status": "complete",
        "started_at": "2025-12-16T09:00:00Z",
        "completed_at": "2025-12-16T09:30:00Z",
        "notes": "Docker containers configured"
      },
      {
        "id": 2,
        "name": "Core Implementation",
        "status": "complete",
        "started_at": "2025-12-16T09:30:00Z",
        "completed_at": "2025-12-16T11:00:00Z",
        "notes": "All endpoints implemented"
      },
      {
        "id": 3,
        "name": "Testing",
        "status": "in_progress",
        "started_at": "2025-12-16T11:00:00Z",
        "notes": "Running integration tests"
      },
      {
        "id": 4,
        "name": "Documentation",
        "status": "pending"
      }
    ]
  }
}
```

### 4. Percentage-Based Progress

For tasks with continuous progress:

```json
{
  "progress": {
    "type": "percentage",
    "completion_percentage": 75,
    "current_phase": "Final optimization",
    "metrics": {
      "files_processed": 150,
      "total_files": 200,
      "estimated_time_remaining_minutes": 30
    }
  }
}
```

## Blocking State Documentation

When a task is blocked, document it thoroughly:

```json
{
  "status": "Blocked",
  "progress": {
    "blocking_step": {
      "step_number": 5,
      "description": "Database migration",
      "blocker_type": "dependency",
      "blocker_details": "Waiting for DBA approval for schema changes",
      "blocked_since": "2025-12-16T14:00:00Z"
    }
  }
}
```

## Checkpoint Management

For long-running tasks requiring state preservation:

```json
{
  "progress": {
    "checkpoints": [
      {
        "checkpoint_id": "cp_001",
        "step_number": 3,
        "state_file": ".claude/tasks/checkpoints/78_cp_001.json",
        "created_at": "2025-12-16T10:30:00Z",
        "can_resume": true
      },
      {
        "checkpoint_id": "cp_002",
        "step_number": 6,
        "state_file": ".claude/tasks/checkpoints/78_cp_002.json",
        "created_at": "2025-12-16T11:30:00Z",
        "can_resume": true
      }
    ]
  }
}
```

## Integration with Complete-Task Command

### Starting a Task with Progress Tracking

```markdown
WHEN STARTING A TASK:
1. READ task file
2. INITIALIZE progress structure based on task complexity:
   - Simple tasks (difficulty 1-3): Use simple progress
   - Multi-step tasks (difficulty 4-6): Use step_counter
   - Complex tasks (difficulty 7-10): Use milestone or percentage
3. SET initial values:
   - current_step: 1
   - total_steps: (estimated based on description)
   - completion_percentage: 0
   - current_phase: "Initialization"
4. CREATE first checkpoint if total_steps > 10
```

### Updating Progress During Work

```markdown
AFTER EACH SIGNIFICANT ACTION:
1. INCREMENT current_step
2. CALCULATE completion_percentage = (current_step / total_steps) * 100
3. ADD entry to step_history with:
   - What was done
   - How long it took
   - Key output/results
4. UPDATE current_phase to reflect work focus
5. CREATE checkpoint if:
   - current_step % 3 == 0 (every 3 steps)
   - Before risky operation
   - Context exceeds 50% budget
```

### Handling Blockers

```markdown
WHEN BLOCKED:
1. SET status to "Blocked"
2. POPULATE blocking_step with:
   - Current step number
   - Clear description of blocker
   - Type of blocker
   - Detailed explanation
   - Timestamp
3. PRESERVE current progress state
4. CREATE checkpoint for resumption
```

## Example: Complete Task with Progress

```json
{
  "id": "78_4",
  "title": "Enhance command files with explicit execution steps",
  "difficulty": 6,
  "status": "In Progress",
  "progress": {
    "type": "step_counter",
    "current_step": 4,
    "total_steps": 12,
    "completion_percentage": 33,
    "current_phase": "Updating breakdown.md",
    "step_history": [
      {
        "step_number": 1,
        "description": "Audit existing command files",
        "status": "complete",
        "timestamp": "2025-12-16T10:00:00Z",
        "duration_minutes": 10,
        "output": "Found 12 command files needing updates"
      },
      {
        "step_number": 2,
        "description": "Create update plan",
        "status": "complete",
        "timestamp": "2025-12-16T10:10:00Z",
        "duration_minutes": 5,
        "output": "Prioritized files by usage frequency"
      },
      {
        "step_number": 3,
        "description": "Update complete-task.md",
        "status": "complete",
        "timestamp": "2025-12-16T10:15:00Z",
        "duration_minutes": 20,
        "output": "Converted to imperative voice, added parallel hints"
      },
      {
        "step_number": 4,
        "description": "Update breakdown.md",
        "status": "in_progress",
        "timestamp": "2025-12-16T10:35:00Z"
      }
    ],
    "metrics": {
      "estimated_time_minutes": 120,
      "actual_time_minutes": 35,
      "steps_completed": 3,
      "steps_failed": 0,
      "steps_skipped": 0,
      "retry_count": 0
    }
  }
}
```

## Progress Calculation Formulas

### Completion Percentage Calculation

```javascript
// For step_counter type
completion_percentage = (steps_completed / total_steps) * 100

// For milestone type
completed_milestones = milestones.filter(m => m.status === 'complete').length
completion_percentage = (completed_milestones / milestones.length) * 100

// For percentage type
completion_percentage = directly set based on work estimate

// For broken down tasks
completed_subtasks = subtasks.filter(t => t.status === 'Finished').length
completion_percentage = (completed_subtasks / subtasks.length) * 100
```

### Time Estimation

```javascript
// Based on historical data
average_step_duration = sum(step_history.duration_minutes) / step_history.length
estimated_remaining = (total_steps - current_step) * average_step_duration

// With variance consideration
variance_factor = 1.2  // 20% buffer
estimated_remaining = estimated_remaining * variance_factor
```

## Migration from v1 to v2

### Backward Compatibility

Tasks without progress field continue to work:
```json
{
  "id": "old_task",
  "status": "In Progress"
  // No progress field - treated as simple progress at 0%
}
```

### Auto-Enhancement

When updating old tasks, add basic progress:
```json
{
  "progress": {
    "type": "simple",
    "completion_percentage": 0
  }
}
```

## Best Practices

### DO:
✅ Update progress after each significant step
✅ Create checkpoints for tasks with >10 steps
✅ Document blockers immediately when encountered
✅ Use appropriate progress type for task complexity
✅ Include meaningful output summaries in step_history
✅ Calculate realistic time estimates with buffers

### DON'T:
❌ Update progress for trivial actions
❌ Create checkpoints in tight loops
❌ Leave blocking_step empty when blocked
❌ Mix progress types within a task
❌ Forget to update completion_percentage
❌ Store large outputs in step_history (summarize instead)

## Usage Examples

### Command Integration

```markdown
# In complete-task.md

EXECUTE:
1. READ task-{id}.json
2. IF no progress field:
   ADD progress structure based on difficulty
3. SET progress.current_step += 1
4. ADD to progress.step_history
5. CALCULATE progress.completion_percentage
6. IF current_step % 3 == 0:
   CREATE checkpoint
7. WRITE updated task file
```

### Status Display

```markdown
# In sync-tasks.md

DISPLAY:
Task 78_4: Enhance command files [████░░░░░░] 33% (Step 4/12)
Current: Updating breakdown.md
Time: 35min elapsed, ~85min remaining
```

## Conclusion

The structured progress tracking enhancement provides:
- Clear visibility into task progress
- Ability to resume from checkpoints
- Detailed history of steps taken
- Accurate time estimations
- Blocker documentation
- Metrics for process improvement

This schema enables Claude 4 to maintain state effectively across long-running tasks while providing transparency to users about ongoing work.