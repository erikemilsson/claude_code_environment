# Task Schema

This document defines the standard JSON structure for task tracking.

## Purpose

Tasks represent discrete units of work in the project. The task schema provides:
- Clear definition of what needs to be done
- Status tracking through the task lifecycle
- Difficulty scoring for complexity management
- Links to phases, decisions, and other tasks
- Agent integration for complex tasks

## Schema Structure

```json
{
  "id": "task-NNN",
  "title": "Brief task description (5-10 words)",
  "description": "Detailed description of what needs to be done, acceptance criteria, and context",
  "status": "pending | in_progress | blocked | broken_down | finished",
  "difficulty": 1-10,
  "priority": "critical | high | medium | low",
  "created": "YYYY-MM-DD",
  "updated": "YYYY-MM-DD",
  "parent_task": "task-XXX | null",
  "subtasks": ["task-NNN-1", "task-NNN-2"],
  "related_phases": ["phase-N"],
  "related_decisions": ["decision-NNN"],
  "assigned_agent": "specification-architect | implementation-architect | test-generator | null",
  "agent_context": {
    "specification_refs": ["planning/specification.md:45-67"],
    "phase_refs": ["phase-1"],
    "decision_refs": ["decision-001"],
    "additional_context": "Any other relevant information for the agent"
  },
  "blockers": [
    {
      "description": "Description of what is blocking this task",
      "status": "unresolved | resolved",
      "resolution": "How the blocker was resolved (if applicable)"
    }
  ],
  "validation": {
    "criteria": [
      "Criterion 1 (how to verify task is complete)",
      "Criterion 2"
    ],
    "completed": false
  },
  "notes": "Additional context, observations, or lessons learned"
}
```

## Field Definitions

### id
- **Format**: `task-NNN` where NNN is a number
- **Uniqueness**: Must be unique across all tasks
- **Subtask Format**: `task-NNN-M` where NNN is parent task ID, M is subtask number
- **File Name**: Task stored in `.claude/tasks/task-NNN.json`

### title
- **Length**: 5-10 words (brief summary)
- **Format**: Imperative tense (e.g., "Implement user authentication", not "Implementing...")
- **Purpose**: Quick reference in task lists

### description
- **Format**: Markdown supported
- **Content**: Should include:
  - What needs to be done (detailed)
  - Why it's needed (context)
  - Acceptance criteria (how to know it's done)
  - Any constraints or requirements

**Example:**
```
Implement JWT-based authentication for the API.

Context: Decision 002 selected JWT over session-based auth for stateless API design.

Requirements:
- Generate JWT tokens on successful login
- Validate tokens on protected endpoints
- Implement token refresh mechanism
- Tokens expire after 1 hour, refresh tokens after 7 days

Acceptance Criteria:
- /login endpoint returns JWT token
- Protected endpoints verify token
- Invalid/expired tokens return 401 error
- Token refresh works without re-authentication
```

### status
**Values:**
- `pending`: Task defined but not started
- `in_progress`: Currently being worked on
- `blocked`: Cannot proceed due to blockers (see blockers field)
- `broken_down`: Task was split into subtasks (not workable directly)
- `finished`: Task completed and validated

**Flow:**
```
pending → in_progress → finished
            ↓
          blocked (if blocker encountered)
            ↓
        in_progress (when blocker resolved)

OR for difficulty ≥7:
pending → broken_down
            ↓
        [subtasks created]
            ↓
        auto-completes when all subtasks finished
```

**Rules:**
- Only ONE task should be `in_progress` at a time (focus)
- Tasks with `status: broken_down` cannot be worked on directly (work on subtasks instead)
- Parent tasks auto-complete when all subtasks have `status: finished`

### difficulty
**Scale**: 1-10 (LLM error risk scoring)

**Guidelines:**
- **1-2 (Trivial)**: Fix typo, update text, simple config change
- **3-4 (Low)**: Basic CRUD operation, simple UI component, straightforward function
- **5-6 (Moderate)**: Form validation, API integration, moderate business logic
- **7-8 (High)**: **Must break down** - Authentication system, complex state management, database migration
- **9-10 (Extreme)**: **Must break down** - Architecture changes, distributed systems, major refactoring

**CRITICAL RULE**: Tasks with difficulty ≥7 MUST be broken down before starting work.

### priority
**Values:**
- `critical`: Blocks other work, must be done immediately
- `high`: Important, should be done soon
- `medium`: Normal priority
- `low`: Nice to have, can be deferred

**Not the same as difficulty**: A trivial task (difficulty 2) can be critical priority (blocks deployment).

### created / updated
- **Format**: YYYY-MM-DD (ISO 8601 date format)
- **created**: When task was first defined
- **updated**: Last modification date (updated whenever task is changed)

### parent_task
- **Format**: `task-XXX` or `null`
- **Purpose**: Links subtasks to parent task
- **Usage**: If this task was created by breaking down task-050, then `"parent_task": "task-050"`
- **Null**: Top-level tasks have `null` parent

### subtasks
- **Format**: Array of task IDs `["task-NNN-1", "task-NNN-2"]`
- **Purpose**: Links parent to its subtasks
- **Auto-Completion**: Parent task automatically gets `status: finished` when all subtasks are `finished`
- **Empty Array**: Tasks with no subtasks have `[]`

### related_phases
- **Format**: Array of phase IDs `["phase-1", "phase-2"]`
- **Purpose**: Links task to project phases
- **Bidirectional**: Should match `phases.md` "Related Tasks" field
- **Usage**: Helps understand which phase(s) this task implements

### related_decisions
- **Format**: Array of decision IDs `["decision-001", "decision-003"]`
- **Purpose**: Links task to architectural decisions
- **Bidirectional**: Should match `decisions.md` "Related Tasks" field
- **Usage**: Provides context for why task is structured this way

### assigned_agent
- **Format**: Agent name or `null`
- **Values**:
  - `specification-architect`: For spec validation tasks
  - `implementation-architect`: For complex implementation tasks
  - `test-generator`: For test creation tasks
  - `null`: Human-completed task (default)
- **Purpose**: Indicates task should be executed by specialized agent

### agent_context
**Only populate if `assigned_agent` is not null**

**Fields:**
- `specification_refs`: Array of references to specification sections (e.g., `["planning/specification.md:45-67"]`)
- `phase_refs`: Array of phase IDs relevant to this task
- `decision_refs`: Array of decision IDs relevant to this task
- `additional_context`: Any other information the agent needs

**Example:**
```json
{
  "specification_refs": [
    "planning/specification.md:45-67",
    "planning/specification.md:102-115"
  ],
  "phase_refs": ["phase-1", "phase-2"],
  "decision_refs": ["decision-001"],
  "additional_context": "Focus on error handling and edge cases"
}
```

### blockers
**Format**: Array of blocker objects

**Each blocker:**
```json
{
  "description": "What is blocking this task",
  "status": "unresolved | resolved",
  "resolution": "How it was resolved (if status is resolved)"
}
```

**Usage:**
- When task becomes `blocked`, add entry to `blockers` array with `status: unresolved`
- When blocker is resolved, update to `status: resolved` and add `resolution` description
- Task can return to `in_progress` after blocker resolved

**Example:**
```json
"blockers": [
  {
    "description": "Waiting for API credentials from third-party provider",
    "status": "resolved",
    "resolution": "Credentials received via email on 2025-12-20"
  }
]
```

### validation
**Purpose**: Define how to verify task completion

**Fields:**
- `criteria`: Array of strings describing validation checks
- `completed`: Boolean (false until all criteria met)

**Example:**
```json
"validation": {
  "criteria": [
    "Unit tests pass for authentication module",
    "Manual test: login with valid credentials succeeds",
    "Manual test: login with invalid credentials fails",
    "Code reviewed by team member"
  ],
  "completed": false
}
```

**Usage:**
- Define criteria when creating task
- Before marking task as `finished`, verify all criteria met
- Set `completed: true` when validation passes

### notes
- **Format**: Plain text or markdown
- **Purpose**: Capture additional context, observations, or lessons learned
- **Usage**: Add notes as work progresses

**Example:**
```
"notes": "Initially tried using bcrypt for password hashing but switched to argon2 based on OWASP recommendations (decision-015). Encountered rate limiting issues during testing - resolved by adjusting throttle settings."
```

## Task Lifecycle

### 1. Task Creation
```json
{
  "id": "task-042",
  "title": "Implement user authentication",
  "description": "...",
  "status": "pending",
  "difficulty": 8,
  "priority": "high",
  "created": "2025-12-15",
  "updated": "2025-12-15",
  "parent_task": null,
  "subtasks": [],
  "related_phases": ["phase-1"],
  "related_decisions": ["decision-002"],
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

### 2. Breakdown (if difficulty ≥7)
User runs `/breakdown task-042`

Result:
```json
// task-042.json (parent)
{
  "id": "task-042",
  "status": "broken_down",
  "subtasks": ["task-042-1", "task-042-2", "task-042-3"],
  ...
}

// task-042-1.json (subtask)
{
  "id": "task-042-1",
  "title": "Implement JWT token generation",
  "status": "pending",
  "difficulty": 5,
  "parent_task": "task-042",
  ...
}
```

### 3. Starting Work
User runs `/complete-task task-042-1 start`

Result:
```json
{
  "id": "task-042-1",
  "status": "in_progress",
  "updated": "2025-12-16",
  ...
}
```

### 4. Encountering Blocker
```json
{
  "id": "task-042-1",
  "status": "blocked",
  "blockers": [
    {
      "description": "Need security review of JWT configuration",
      "status": "unresolved"
    }
  ],
  "updated": "2025-12-17",
  ...
}
```

### 5. Resolving Blocker and Resuming
```json
{
  "id": "task-042-1",
  "status": "in_progress",
  "blockers": [
    {
      "description": "Need security review of JWT configuration",
      "status": "resolved",
      "resolution": "Security team approved config on 2025-12-18"
    }
  ],
  "updated": "2025-12-18",
  ...
}
```

### 6. Completing Task
User runs `/complete-task task-042-1 finish`

Result:
```json
{
  "id": "task-042-1",
  "status": "finished",
  "validation": {
    "criteria": ["..."],
    "completed": true
  },
  "updated": "2025-12-19",
  ...
}
```

### 7. Auto-Completion of Parent
When all subtasks (task-042-1, task-042-2, task-042-3) are finished:

```json
// task-042.json (parent auto-completes)
{
  "id": "task-042",
  "status": "finished",
  "updated": "2025-12-20",
  ...
}
```

## Examples

### Example 1: Simple Implementation Task
```json
{
  "id": "task-025",
  "title": "Add user profile page",
  "description": "Create a user profile page that displays user information (name, email, avatar) and allows users to edit their profile.\n\nRequirements:\n- Display current user info from API\n- Form for editing name and email\n- Image upload for avatar\n- Save changes via PUT /api/users/:id\n\nAcceptance Criteria:\n- Page renders at /profile route\n- User data loads correctly\n- Form validation works (email format, required fields)\n- Save button updates user and shows success message\n- Navigation link to profile added to header",
  "status": "pending",
  "difficulty": 5,
  "priority": "medium",
  "created": "2025-12-15",
  "updated": "2025-12-15",
  "parent_task": null,
  "subtasks": [],
  "related_phases": ["phase-2"],
  "related_decisions": ["decision-009"],
  "assigned_agent": null,
  "agent_context": {},
  "blockers": [],
  "validation": {
    "criteria": [
      "Profile page accessible at /profile",
      "User data displays correctly",
      "Edit form validation works",
      "Save functionality updates user",
      "Manual test: upload avatar image"
    ],
    "completed": false
  },
  "notes": ""
}
```

### Example 2: Parent Task (Broken Down)
```json
{
  "id": "task-050",
  "title": "Implement payment processing system",
  "description": "Build complete payment processing system with Stripe integration, order management, and transaction logging.\n\nThis is a high-difficulty task that needs to be broken down into subtasks.\n\nKey Requirements:\n- Stripe API integration\n- Order creation and tracking\n- Payment status webhooks\n- Transaction logging\n- Error handling and retries",
  "status": "broken_down",
  "difficulty": 9,
  "priority": "critical",
  "created": "2025-12-10",
  "updated": "2025-12-12",
  "parent_task": null,
  "subtasks": ["task-050-1", "task-050-2", "task-050-3", "task-050-4"],
  "related_phases": ["phase-2"],
  "related_decisions": ["decision-007", "decision-012"],
  "assigned_agent": null,
  "agent_context": {},
  "blockers": [],
  "validation": {
    "criteria": [
      "All subtasks completed",
      "End-to-end payment flow tested",
      "Webhook handling verified",
      "Error scenarios tested"
    ],
    "completed": false
  },
  "notes": "Broken down into subtasks on 2025-12-12 using /breakdown command"
}
```

### Example 3: Subtask
```json
{
  "id": "task-050-1",
  "title": "Set up Stripe API integration",
  "description": "Configure Stripe SDK and implement basic API connection.\n\nSteps:\n1. Install Stripe SDK\n2. Configure API keys (test and production)\n3. Create Stripe client wrapper module\n4. Implement basic health check (verify API connectivity)\n\nAcceptance Criteria:\n- Stripe SDK installed and configured\n- API keys stored securely (environment variables)\n- Client wrapper module created with error handling\n- Health check endpoint returns Stripe connection status",
  "status": "finished",
  "difficulty": 4,
  "priority": "critical",
  "created": "2025-12-12",
  "updated": "2025-12-14",
  "parent_task": "task-050",
  "subtasks": [],
  "related_phases": ["phase-2"],
  "related_decisions": ["decision-007"],
  "assigned_agent": null,
  "agent_context": {},
  "blockers": [],
  "validation": {
    "criteria": [
      "Stripe SDK installed (check package.json)",
      "API keys in .env file",
      "Client wrapper module created",
      "Health check returns 200 OK"
    ],
    "completed": true
  },
  "notes": "Used test API keys for development. Production keys will be added during deployment (task-055)."
}
```

### Example 4: Agent-Assigned Task
```json
{
  "id": "task-101",
  "title": "Fix duplicate email error handling in spec",
  "description": "Update specification Section 3.2.1 to define behavior when user attempts to register with an email that's already in the system.\n\nIssue: Current specification only covers happy path registration. Missing error handling for duplicate email scenario.\n\nLocation: planning/specification.md Section 3.2.1\nSeverity: major\nTest: spec-test-001\n\nSuggested Fix:\nAdd subsection '3.2.1.2 Duplicate Email Handling' specifying:\n- System checks if email exists before creating account\n- If exists, show error 'This email is already registered. Try logging in or reset your password.'\n- Do not reveal whether email exists (to prevent enumeration attacks)",
  "status": "pending",
  "difficulty": 5,
  "priority": "high",
  "created": "2025-12-15",
  "updated": "2025-12-15",
  "parent_task": null,
  "subtasks": [],
  "related_phases": ["phase-1"],
  "related_decisions": [],
  "assigned_agent": "specification-architect",
  "agent_context": {
    "specification_refs": ["planning/specification.md:85-120"],
    "phase_refs": ["phase-1"],
    "decision_refs": [],
    "additional_context": "This issue was found during specification testing. Focus on security implications (email enumeration)."
  },
  "blockers": [],
  "validation": {
    "criteria": [
      "Update planning/specification.md per suggested fix",
      "Re-run spec-test-001 and verify it passes"
    ],
    "completed": false
  },
  "notes": "Generated by /test-specification from spec-test-001"
}
```

## Best Practices

### Task Granularity
- **Too Small**: "Fix typo on line 42" (combine multiple small fixes into one task)
- **Too Large**: "Build entire frontend" (break down into features/pages)
- **Just Right**: "Implement user profile page" (one feature/component)

### Task Descriptions
- **Bad**: "Add authentication" (too vague)
- **Good**: "Implement JWT-based authentication with login endpoint, token validation middleware, and refresh mechanism"

### Difficulty Scoring
- **Consider complexity**: How many moving parts?
- **Consider risk**: How likely are mistakes?
- **Consider unknowns**: Are requirements clear?
- **When in doubt**: Score higher and break down if needed

### Priority vs Difficulty
- Priority = Importance/urgency
- Difficulty = Complexity/effort
- They're independent: Can have critical/trivial tasks or low-priority/complex tasks

### Related Phases/Decisions
- Always link tasks to phases (helps track phase completion)
- Link to decisions when task implements or depends on a decision
- Run `/update-executive-summary` to keep bidirectional links current

## Troubleshooting

### Problem: Task keeps growing in scope
**Solution**: Create new tasks for additional scope, don't expand original task

### Problem: Unsure if task is complete
**Solution**: Check validation criteria - if all criteria met, task is done

### Problem: Task blocked indefinitely
**Solution**: Create separate task to resolve the blocker, mark blocker with resolution plan

### Problem: Parent task not auto-completing
**Solution**: Check that ALL subtasks have `status: finished` - even one pending/in_progress will block parent completion

### Problem: Task difficulty changed after breakdown
**Solution**: This is normal - initial estimate may have been wrong. Document in notes why estimate changed.
