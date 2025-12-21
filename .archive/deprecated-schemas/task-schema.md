# Task JSON Schema with Belief Tracking

**DEPRECATED** - This document has been superseded by task-schema-consolidated.md

See: .claude/reference/task-schema-consolidated.md (Created: 2025-12-17)

---

## Schema Definition

All task JSON files follow this schema structure with integrated belief tracking capabilities:

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "difficulty": "number (1-10)",
  "status": "string",
  "created_date": "string (YYYY-MM-DD)",
  "updated_date": "string (YYYY-MM-DD)",
  "dependencies": ["array of task IDs"],
  "subtasks": ["array of task IDs"],
  "parent_task": "string (task ID) or null",
  "files_affected": ["array of file paths"],
  "notes": "string",

  // Belief Tracking Fields
  "confidence": "number (0-100)",
  "assumptions": ["array of assumption objects"],
  "validation_status": "string",
  "momentum": {
    "phase": "string",
    "velocity": "number",
    "last_activity": "string (YYYY-MM-DD)"
  },
  "decision_rationale": "string"
}
```

## Field Descriptions

### Core Fields

- **id**: Unique task identifier (typically sequential number as string)
- **title**: Brief descriptive title of the task
- **description**: Detailed explanation of what needs to be done
- **difficulty**: LLM error risk score (1-10)
  - 1-2: Trivial changes
  - 3-4: Low complexity
  - 5-6: Moderate complexity
  - 7-8: High complexity (must break down)
  - 9-10: Extreme complexity (must break down)
- **status**: Current task state
  - `Pending`: Not yet started
  - `In Progress`: Currently being worked on
  - `Blocked`: Cannot proceed
  - `Broken Down`: Decomposed into subtasks
  - `Finished`: Completed
- **created_date**: When task was created (YYYY-MM-DD)
- **updated_date**: Last modification date (YYYY-MM-DD)
- **dependencies**: Task IDs that must complete before this task
- **subtasks**: Child task IDs (for broken down tasks)
- **parent_task**: Parent task ID if this is a subtask
- **files_affected**: Files that will be created/modified
- **notes**: Additional context or completion details

### Belief Tracking Fields

#### confidence (0-100)
Confidence score representing certainty in task completion approach and estimates.

- **90-100**: Very high confidence, clear path, proven approach
- **75-89**: High confidence, standard patterns apply
- **50-74**: Medium confidence, some unknowns exist
- **25-49**: Low confidence, significant unknowns
- **0-24**: Very low confidence, experimental/unclear

#### assumptions (array)
Array of assumption objects tracking beliefs about the task:

```json
{
  "id": "string",
  "description": "string",
  "confidence": "number (0-100)",
  "status": "pending|validated|invalidated",
  "impact": "low|medium|high|critical",
  "validation_method": "string",
  "validated_date": "string (YYYY-MM-DD) or null"
}
```

#### validation_status
Overall validation state of the task:

- **pending**: Not yet validated
- **validated**: Approach/assumptions confirmed correct
- **invalidated**: Approach/assumptions proven incorrect
- **partial**: Some aspects validated, others not

#### momentum
Tracks task execution velocity and energy:

```json
{
  "phase": "string",
  "velocity": "number (0-100)",
  "last_activity": "string (YYYY-MM-DD)"
}
```

**Phases:**
- **pending**: Task not started
- **ignition**: Initial work beginning (velocity 0-20)
- **building**: Momentum increasing (velocity 20-50)
- **cruising**: Steady progress (velocity 50-80)
- **coasting**: Progress slowing (velocity 30-60)
- **stalling**: Near stop (velocity 10-30)
- **stopped**: No progress (velocity 0)

**Velocity Calculation:**
- Based on activity frequency and progress rate
- Higher for regular commits/updates
- Lower for long gaps between activities
- Factors in blockers and dependencies

#### decision_rationale
Text field documenting key decisions made during task execution:

- Why specific approaches were chosen
- Trade-offs considered
- Alternative solutions rejected and why
- Lessons learned during implementation

## Example Task with Belief Tracking

```json
{
  "id": "42",
  "title": "Implement authentication system",
  "description": "Add JWT-based authentication with refresh tokens",
  "difficulty": 7,
  "status": "In Progress",
  "created_date": "2025-12-15",
  "updated_date": "2025-12-15",
  "dependencies": ["41"],
  "subtasks": ["43", "44", "45"],
  "parent_task": null,
  "files_affected": [
    "src/auth/jwt.service.ts",
    "src/auth/auth.controller.ts"
  ],
  "notes": "Using JWT with RS256 for enhanced security",
  "confidence": 85,
  "assumptions": [
    {
      "id": "a1",
      "description": "JWT library supports RS256 algorithm",
      "confidence": 95,
      "status": "validated",
      "impact": "high",
      "validation_method": "Library documentation review",
      "validated_date": "2025-12-15"
    },
    {
      "id": "a2",
      "description": "Redis available for refresh token storage",
      "confidence": 70,
      "status": "pending",
      "impact": "medium",
      "validation_method": "Infrastructure check",
      "validated_date": null
    }
  ],
  "validation_status": "partial",
  "momentum": {
    "phase": "building",
    "velocity": 45,
    "last_activity": "2025-12-15"
  },
  "decision_rationale": "Chose JWT over sessions for stateless architecture. RS256 over HS256 for asymmetric signing allowing secure token validation by services without sharing secrets."
}
```

## Usage Guidelines

1. **Confidence Scoring**: Update confidence as understanding improves
2. **Assumption Tracking**: Document all assumptions, validate during execution
3. **Momentum Monitoring**: Check velocity regularly, intervene if stalling
4. **Decision Documentation**: Record rationale for future reference
5. **Validation Checkpoints**: Validate assumptions at natural breakpoints

## Integration Points

- **complete-task.md**: Updates these fields during task completion
- **check-risks.md**: Monitors low confidence and stalling momentum
- **validate-assumptions.md**: Systematically validates pending assumptions
- **sync-tasks.md**: Includes belief tracking in overview generation