# Command: breakdown

## Purpose
Split high-difficulty tasks (≥7) into manageable subtasks (≤6 difficulty each).

## Usage
```
/breakdown task-050   # Break down task-050 into subtasks
```

## Context Required
- Task ID to break down
- Understanding of task scope and requirements

## Process

### 1. Validate Breakdown Need

Check:
- Task difficulty ≥ 7 (or user requested)
- Task is not already "broken_down"
- Task can be decomposed logically

### 2. Analyze Task Complexity

Read task file and identify:
- Logical components
- Dependencies between components
- Estimated difficulty for each component

### 3. Create Subtasks

For each component:
- **Generate unique ID**: `task-{parent-id}-{number}` (e.g., task-050-1, task-050-2)
- **Write task JSON file**:
  ```json
  {
    "id": "task-050-1",
    "title": "Specific subtask title",
    "description": "Clear, focused description",
    "status": "pending",
    "difficulty": 4,
    "priority": "critical",
    "created": "2025-12-29",
    "updated": "2025-12-29",
    "parent_task": "task-050",
    "subtasks": [],
    "related_phases": ["phase-2"],
    "related_decisions": ["decision-007"],
    "assigned_agent": null,
    "agent_context": {},
    "blockers": [],
    "validation": {
      "criteria": ["..."],
      "completed": false
    },
    "notes": ""
  }
  ```

### 4. Update Parent Task

- Set `status: "broken_down"`
- Set `subtasks: [array of subtask IDs]`
- Add note: "Broken down into X subtasks"
- Preserve all other parent data

### 5. Run /sync-tasks

Update task-overview.md to show new hierarchy

## Breakdown Strategies

### Functional Breakdown
Split by feature or capability:
- task-050-1: User authentication
- task-050-2: Password reset
- task-050-3: Session management

### Architectural Breakdown
Split by system layer:
- task-050-1: Database schema
- task-050-2: API endpoints
- task-050-3: Frontend components

### Temporal Breakdown
Split by implementation order:
- task-050-1: Setup and configuration
- task-050-2: Core implementation
- task-050-3: Testing and validation

## Validation Rules

**Each subtask must:**
- Have difficulty ≤ 6
- Be independently completable
- Have clear deliverable
- Not have circular dependencies

**Subtask titles must:**
- Be specific and actionable
- Use imperative tense
- Clearly describe what to do

## Output Location
- New files: `.claude/tasks/task-{new-id}.json` for each subtask
- Updated parent file: `.claude/tasks/task-{parent-id}.json`
- Updated overview: `.claude/tasks/task-overview.md`

## Example

```
User: /breakdown task-050

Claude: Analyzing task-050 (Implement payment processing system)...

Difficulty: 9 (requires breakdown)

Breaking down into subtasks:

1. task-050-1: Set up Stripe API integration (difficulty: 4)
   - Install Stripe SDK
   - Configure API keys
   - Create client wrapper

2. task-050-2: Implement payment processing (difficulty: 6)
   - Create payment endpoints
   - Handle payment flow
   - Add error handling

3. task-050-3: Add webhook handling (difficulty: 5)
   - Set up webhook endpoints
   - Verify webhook signatures
   - Process payment events

4. task-050-4: Add transaction logging (difficulty: 4)
   - Design log schema
   - Implement logging
   - Add log queries

Creating subtask files...
✓ Created task-050-1.json
✓ Created task-050-2.json
✓ Created task-050-3.json
✓ Created task-050-4.json

Updating parent task-050...
✓ Status: pending → broken_down
✓ Subtasks: [task-050-1, task-050-2, task-050-3, task-050-4]

Running /sync-tasks...
✓ Task overview updated

Breakdown complete!

Next: Start with task-050-1 (lowest difficulty)
Run: /complete-task task-050-1 start
```

## MANDATORY Rules

**ALWAYS:**
- Verify each subtask difficulty ≤ 6
- Set parent status to "broken_down"
- Create all subtask files before updating parent
- Run /sync-tasks after breakdown

**NEVER:**
- Create subtasks with difficulty > 6
- Work on parent task after breakdown
- Skip dependency mapping
- Forget to set parent_task field
