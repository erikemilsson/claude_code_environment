# Task Schema - Consolidated Reference

*Version: Consolidated 2025-12-17 | Based on: task-schema.md, task-schema-v2.md, enhanced-task-schema.md*

## Status

**CURRENT SCHEMA**: This document represents the authoritative task schema for the project.

**REPLACED DOCUMENTS**:
- task-schema.md (original belief tracking schema)
- task-schema-v2.md (progress tracking extension)
- enhanced-task-schema.md (alternative belief tracking format)

## Complete Schema Definition

```json
{
  // Core Task Fields
  "id": "string",
  "title": "string",
  "description": "string",
  "difficulty": "number (1-10)",
  "status": "Pending | In Progress | Blocked | Broken Down | Finished",
  "created_date": "YYYY-MM-DD",
  "updated_date": "YYYY-MM-DD",
  "completion_date": "YYYY-MM-DD or null",
  "completion_notes": "string or null",
  "dependencies": ["array of task IDs"],
  "subtasks": ["array of subtask IDs"],
  "parent_task": "task ID or null",
  "files_affected": ["array of file paths"],
  "notes": "string",

  // Belief Tracking Fields (flat structure - currently used)
  "confidence": "number (0-100)",
  "assumptions": [
    {
      "id": "string",
      "description": "string",
      "confidence": "number (0-100)",
      "status": "pending|validated|invalidated",
      "impact": "low|medium|high|critical",
      "validation_method": "string",
      "validated_date": "YYYY-MM-DD or null"
    }
  ],
  "validation_status": "pending|validated|invalidated|partial",
  "momentum": {
    "phase": "initializing|pending|ignition|building|cruising|coasting|stalling|stopped",
    "velocity": "number (0-100)",
    "last_activity": "YYYY-MM-DD"
  },
  "decision_rationale": "string",

  // Progress Tracking (optional, for complex tasks)
  "progress": {
    "type": "simple|step_counter|milestone|percentage",
    "current_step": "number",
    "total_steps": "number",
    "completion_percentage": "number (0-100)",
    "current_phase": "string",

    "milestones": [
      {
        "id": "number",
        "name": "string",
        "status": "pending|in_progress|complete|skipped",
        "started_at": "ISO 8601 timestamp",
        "completed_at": "ISO 8601 timestamp",
        "notes": "string"
      }
    ],

    "step_history": [
      {
        "step_number": "number",
        "description": "string",
        "status": "complete|failed|skipped",
        "timestamp": "ISO 8601 timestamp",
        "duration_minutes": "number",
        "output": "string (summary of results)"
      }
    ],

    "blocking_step": {
      "step_number": "number",
      "description": "string",
      "blocker_type": "dependency|error|waiting_for_input|resource_unavailable",
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

## Field Descriptions

### Core Task Fields

#### id
- **Type**: String
- **Required**: Yes
- **Format**: Sequential number as string (e.g., "1", "42", "78_3" for subtasks)
- **Purpose**: Unique identifier for the task

#### title
- **Type**: String
- **Required**: Yes
- **Format**: Brief descriptive title (recommended <80 characters)
- **Purpose**: Quick identification of task purpose

#### description
- **Type**: String
- **Required**: Yes
- **Format**: Detailed explanation of what needs to be done
- **Purpose**: Full context for task implementation

#### difficulty
- **Type**: Number
- **Required**: Yes
- **Range**: 1-10 (LLM error risk score)
- **Scale**:
  - 1-2: Trivial (typo fixes, text updates)
  - 3-4: Low (simple CRUD, basic UI)
  - 5-6: Moderate (form validation, API integration)
  - 7-8: High (MUST break down - auth systems, migrations)
  - 9-10: Extreme (MUST break down - architecture changes, distributed systems)

#### status
- **Type**: String (enum)
- **Required**: Yes
- **Values**:
  - `Pending`: Not yet started
  - `In Progress`: Currently being worked on
  - `Blocked`: Cannot proceed (must document blocker)
  - `Broken Down`: Decomposed into subtasks (not directly workable)
  - `Finished`: Completed successfully
- **Rules**:
  - Never work on "Broken Down" tasks directly (work on subtasks instead)
  - "Broken Down" tasks auto-complete when all subtasks finish
  - Only one task should be "In Progress" at a time per workflow

#### dates
- **created_date**: When task was created (YYYY-MM-DD)
- **updated_date**: Last modification date (YYYY-MM-DD)
- **completion_date**: When task was finished (YYYY-MM-DD or null)

#### completion_notes
- **Type**: String or null
- **Required**: No (null until completion)
- **Purpose**: Document what was actually done, including:
  - Implementation approach used
  - Any deviations from original plan
  - Bugs found and fixed during work
  - New tasks created
  - Links to relevant files or commits
  - Assumption validation results

#### dependencies
- **Type**: Array of task ID strings
- **Required**: Yes (empty array if none)
- **Purpose**: Tasks that must complete before this task can start
- **Validation**: All IDs must reference existing tasks, no circular dependencies

#### subtasks
- **Type**: Array of task ID strings
- **Required**: Yes (empty array if none)
- **Purpose**: Child tasks created when breaking down this task
- **Rules**: Non-empty only when status is "Broken Down"

#### parent_task
- **Type**: String or null
- **Required**: Yes
- **Purpose**: References parent task if this is a subtask
- **Rules**: Must reference existing task with this task in its subtasks array

#### files_affected
- **Type**: Array of file path strings
- **Required**: Yes (empty array if none)
- **Purpose**: Tracks which files will be created or modified
- **Format**: Relative paths from project root

#### notes
- **Type**: String
- **Required**: Yes (can be empty string)
- **Purpose**: Additional context, warnings, or implementation hints

### Belief Tracking Fields

#### confidence
- **Type**: Number
- **Range**: 0-100
- **Required**: Yes
- **Purpose**: Confidence score representing certainty in task completion approach
- **Ranges**:
  - 90-100: Very high confidence, clear path, proven approach
  - 75-89: High confidence, standard patterns apply
  - 50-74: Medium confidence, some unknowns exist
  - 25-49: Low confidence, significant unknowns
  - 0-24: Very low confidence, experimental/unclear
- **Updates**: Adjust based on discoveries during work

#### assumptions
- **Type**: Array of assumption objects
- **Required**: Yes (empty array if none)
- **Structure**:
  ```json
  {
    "id": "a1",
    "description": "Clear statement of assumption",
    "confidence": 80,
    "status": "pending|validated|invalidated",
    "impact": "low|medium|high|critical",
    "validation_method": "How we'll verify this",
    "validated_date": "YYYY-MM-DD or null"
  }
  ```
- **Impact Levels**:
  - Critical: Project fails if wrong
  - High: Major rework required
  - Medium: Moderate adjustments needed
  - Low: Minor changes only

#### validation_status
- **Type**: String (enum)
- **Required**: Yes
- **Values**:
  - `pending`: Not yet validated
  - `validated`: All assumptions confirmed correct
  - `invalidated`: One or more assumptions proven wrong
  - `partial`: Some validated, some not
- **Calculation**: Based on status of all assumptions

#### momentum
- **Type**: Object
- **Required**: Yes
- **Structure**:
  ```json
  {
    "phase": "string",
    "velocity": "number (0-100)",
    "last_activity": "YYYY-MM-DD"
  }
  ```
- **Phases**:
  - `initializing`: Task being set up (velocity 0)
  - `pending`: Not started (velocity 0)
  - `ignition`: Initial work beginning (velocity 10-20)
  - `building`: Momentum increasing (velocity 20-50)
  - `cruising`: Steady progress (velocity 50-80)
  - `coasting`: Progress slowing (velocity 30-60)
  - `stalling`: Near stop (velocity 10-30)
  - `stopped`: No progress (velocity 0)

#### decision_rationale
- **Type**: String
- **Required**: Yes (can be empty until decisions made)
- **Purpose**: Document key decisions including:
  - Why specific approaches were chosen
  - Trade-offs considered
  - Alternative solutions rejected and why
  - Lessons learned during implementation

### Progress Tracking Fields (Optional)

The `progress` field is optional and recommended for:
- Tasks with difficulty ≥ 7
- Multi-step tasks requiring checkpoint management
- Long-running tasks (>10 steps)
- Tasks where detailed tracking provides value

See Progress Types section below for detailed usage.

## Progress Types

### Simple Progress (Default)
For basic tasks without detailed tracking:
```json
{
  "progress": {
    "type": "simple",
    "completion_percentage": 0
  }
}
```

### Step Counter Progress
For discrete, sequential steps:
```json
{
  "progress": {
    "type": "step_counter",
    "current_step": 3,
    "total_steps": 10,
    "completion_percentage": 30,
    "current_phase": "Implementing core functionality"
  }
}
```

### Milestone-Based Progress
For key deliverables:
```json
{
  "progress": {
    "type": "milestone",
    "completion_percentage": 60,
    "milestones": [
      {
        "id": 1,
        "name": "Environment Setup",
        "status": "complete",
        "started_at": "2025-12-16T09:00:00Z",
        "completed_at": "2025-12-16T09:30:00Z"
      }
    ]
  }
}
```

### Percentage-Based Progress
For continuous progress:
```json
{
  "progress": {
    "type": "percentage",
    "completion_percentage": 75,
    "current_phase": "Final optimization"
  }
}
```

## Validation Rules

### Required Fields
All tasks MUST have:
- id, title, description, difficulty, status
- created_date, updated_date
- dependencies, subtasks, parent_task (can be empty/null)
- files_affected, notes (can be empty)
- confidence, assumptions, validation_status
- momentum, decision_rationale (can be empty)

### Status Constraints
- "Broken Down" tasks MUST have non-empty subtasks array
- "Blocked" tasks SHOULD document blocker in notes or blocking_step
- "Finished" tasks MUST have completion_date and completion_notes

### Relationship Constraints
- dependencies MUST reference existing task IDs
- NO circular dependencies allowed
- subtasks MUST reference existing tasks
- parent_task MUST reference task with this ID in its subtasks array

### Date Format
All dates must be YYYY-MM-DD format (ISO 8601 date portion)

## Migration Notes

### From enhanced-task-schema.md
The flat belief tracking structure (current) is preferred over nested:
```json
// Current (correct)
{
  "confidence": 75,
  "assumptions": [],
  ...
}

// Old enhanced schema (deprecated)
{
  "belief_tracking": {
    "confidence": 75,
    "assumptions": []
  }
}
```

### Adding Progress Tracking
Existing tasks without progress field continue to work.
Add progress only when complexity warrants it:
```json
{
  "id": "old_task",
  "status": "In Progress",
  // Add this when needed:
  "progress": {
    "type": "simple",
    "completion_percentage": 0
  }
}
```

## Best Practices

### Task Creation
- Start with realistic confidence scores
- Document all assumptions upfront
- Set momentum to "initializing" initially
- Leave decision_rationale empty until decisions made

### During Execution
- Update confidence as understanding improves
- Validate assumptions at natural breakpoints
- Update momentum phase and velocity regularly
- Document decision rationale when making significant choices

### At Completion
- Mark all assumptions as validated or invalidated
- Set final confidence score based on actual experience
- Update momentum to "cruising" with high velocity if successful
- Write comprehensive completion_notes

### For Broken Down Tasks
- Create all subtasks before marking as "Broken Down"
- Subtasks inherit some context from parent
- Parent auto-completes when all subtasks finish
- Parent momentum = average of subtask velocities

## Command Integration

### complete-task.md
- Updates belief tracking fields during execution
- Validates assumptions
- Calculates new momentum
- Requires completion_notes
- Auto-completes parent tasks

### sync-tasks.md
- Generates overview from all task files
- Includes belief tracking metrics
- Shows hierarchical relationships
- Displays visual health indicators

### breakdown.md
- Creates subtasks for difficulty ≥ 7 tasks
- Distributes parent confidence to subtasks
- Sets up subtask relationships
- Marks parent as "Broken Down"

### update-tasks.md
- Validates all required fields present
- Checks relationship consistency
- Flags stalled momentum
- Reports validation errors

## Examples

See components/task-management/examples/ for complete task examples demonstrating:
- Simple task (difficulty 1-3)
- Moderate task (difficulty 4-6) with basic progress
- Complex task (difficulty 7-8) broken down with milestones
- High-confidence task with validated assumptions
- Low-confidence task with pending validations
- Blocked task with blocker documentation
