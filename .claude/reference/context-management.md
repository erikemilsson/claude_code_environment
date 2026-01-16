# Context Management Framework for Long Tasks

*Version: 1.1 | Updated: 2025-01-16 | Based on: Anthropic Claude Code Best Practices*

## Overview

Long-running tasks in Claude Code require structured context management to maintain state, track progress, and enable resumption. This framework provides patterns for managing context efficiently across extended workflows.

## Core Principles

1. **Checkpoint Early and Often** - Save state at logical boundaries
2. **Structure Over Narrative** - Use JSON for data, markdown for documentation
3. **Progressive Summarization** - Compact context as you progress
4. **Explicit State Tracking** - Always know where you are in the process
5. **Session Hygiene** - Use /clear and /compact strategically

## Session Management: /clear vs /compact

### /clear - Full Context Reset

**What it does:** Completely clears the conversation context, starting fresh.

**When to use /clear:**
```markdown
✅ After completing a major task or milestone
✅ Before starting an unrelated task
✅ When context is confused or corrupted
✅ After complex debugging sessions
✅ When switching between different projects
✅ When conversation has accumulated irrelevant history
```

**When NOT to use /clear:**
```markdown
❌ In the middle of a multi-step task
❌ When you need continuity from previous work
❌ When recovering from an error (use checkpoint instead)
❌ When iterating on a feature
```

**Best practice pattern:**
```markdown
1. Complete current task/milestone
2. Commit any changes
3. Update task status in task JSON
4. Run sync-tasks
5. /clear
6. Start next task with fresh context
```

### /compact - Context Compression

**What it does:** Compresses the conversation context while preserving key information and continuity.

**When to use /compact:**
```markdown
✅ Mid-task when context is getting large
✅ When you need to continue but reduce noise
✅ After verbose tool outputs (large file reads, etc.)
✅ When context exceeds ~60-70% capacity
✅ Before complex operations that will add context
✅ When you want to preserve continuity but reduce bloat
```

**When NOT to use /compact:**
```markdown
❌ When you need full detail from recent operations
❌ Right before reviewing previous output
❌ When debugging requires full history
❌ At natural task boundaries (use /clear instead)
```

**Best practice pattern:**
```markdown
1. Notice context getting large
2. Ensure current step is at a good stopping point
3. /compact
4. Briefly re-state what you're working on
5. Continue with compressed context
```

### Decision Matrix

| Scenario | Use /clear | Use /compact |
|----------|-----------|--------------|
| Task completed | ✅ | ❌ |
| Mid-task, context bloated | ❌ | ✅ |
| Starting unrelated work | ✅ | ❌ |
| Need continuity but less noise | ❌ | ✅ |
| Context confused/corrupted | ✅ | ❌ |
| After large file operations | ❌ | ✅ |
| Switching projects | ✅ | ❌ |
| Iterating on same feature | ❌ | ✅ |

### Preserving State Across /clear

When you must /clear but need to preserve state:

```markdown
BEFORE /clear:
1. Update task JSON with current state
2. Write checkpoint file if needed
3. Document any in-progress work in scratchpad
4. Commit any changes

AFTER /clear:
1. Read relevant task JSON files
2. Read checkpoint if resuming
3. Briefly review scratchpad notes
4. Continue from documented state
```

### Markdown Checklists for Large Tasks

Create persistent checklists that survive /clear:

```markdown
# File: .claude/checklists/feature-auth.md

## Feature: User Authentication

### Phase 1: Setup
- [x] Create user model
- [x] Add database migration
- [x] Set up JWT utilities

### Phase 2: Implementation
- [x] Login endpoint
- [ ] Logout endpoint          ← CURRENT
- [ ] Password reset flow
- [ ] Session management

### Phase 3: Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Security audit

## Notes
- Using bcrypt for password hashing
- Token expiry: 24h access, 7d refresh
- See decision log: .claude/scratchpad/decisions/auth-approach.md
```

**Usage:**
```markdown
1. Create checklist at task start
2. Update as you progress
3. /clear when needed - checklist persists
4. After /clear, read checklist to resume
```

## Context Budget Management

### Token Allocation Strategy

```markdown
CONTEXT BUDGET (200K tokens):
- System/Instructions: ~5K tokens (2.5%)
- Task State: ~10K tokens (5%)
- Working Memory: ~50K tokens (25%)
- Code/Content: ~100K tokens (50%)
- Buffer: ~35K tokens (17.5%)

WHEN APPROACHING LIMIT:
1. Summarize completed sections
2. Archive verbose outputs
3. Extract key decisions
4. Maintain only active context
```

### Context Compaction Techniques

#### 1. Progressive Summarization

```markdown
FULL DETAIL → SUMMARY → KEY POINTS → REFERENCE

Example:
Initial: Full code review with all findings (5000 tokens)
Summary: List of issues and fixes needed (500 tokens)
Key Points: Critical issues only (100 tokens)
Reference: "Reviewed auth.js - 3 critical, 5 minor issues"
```

#### 2. State Compression

```json
{
  "checkpoint": "phase_3_complete",
  "completed": ["analysis", "design", "core_implementation"],
  "current": "testing",
  "remaining": ["documentation", "deployment"],
  "key_decisions": {
    "database": "PostgreSQL chosen for ACID compliance",
    "framework": "Next.js 14 for SSR capabilities"
  },
  "blockers": [],
  "next_action": "Run integration tests"
}
```

## Checkpoint Patterns

### 1. Bootstrap Workflow Checkpoints

```markdown
CHECKPOINT: environment_selection
{
  "stage": "template_detection",
  "detected_type": "power-query",
  "confidence": 0.85,
  "evidence": ["found DAX functions", "Power BI mentioned"],
  "user_confirmed": false,
  "next": "confirm_with_user"
}

CHECKPOINT: file_generation
{
  "stage": "creating_structure",
  "completed_files": [".claude/", "commands/", "context/"],
  "remaining_files": ["tasks/", "reference/"],
  "errors": [],
  "next": "create_task_files"
}
```

### 2. Task Breakdown Checkpoints

```markdown
CHECKPOINT: analysis_complete
{
  "parent_task": "78",
  "complexity_score": 9,
  "identified_subtasks": 17,
  "dependencies_mapped": true,
  "next": "create_subtask_files"
}

CHECKPOINT: subtasks_created
{
  "parent_task": "78",
  "subtasks_created": ["78_1", "78_2", "...", "78_17"],
  "files_written": 17,
  "parent_updated": true,
  "next": "run_sync_tasks"
}
```

### 3. Complex Analysis Checkpoints

```markdown
CHECKPOINT: codebase_scan
{
  "files_analyzed": 142,
  "patterns_found": {
    "authentication": 12,
    "database": 34,
    "api_endpoints": 28
  },
  "issues_identified": 7,
  "next": "deep_dive_issues"
}
```

## State Persistence Guidelines

### 1. JSON for Structured Data

```markdown
USE JSON WHEN:
✅ Tracking lists or arrays
✅ Maintaining counters
✅ Storing configuration
✅ Recording status/progress
✅ Preserving exact values

EXAMPLE:
{
  "tasks_completed": [1, 2, 3],
  "current_task": 4,
  "total_tasks": 10,
  "success_rate": 0.95
}
```

### 2. Markdown for Documentation

```markdown
USE MARKDOWN WHEN:
✅ Explaining decisions
✅ Documenting process
✅ Creating summaries
✅ Writing instructions
✅ Formatting output

EXAMPLE:
## Decision: Database Selection
Chose PostgreSQL because:
- ACID compliance required
- Complex queries needed
- Team expertise available
```

### 3. Hybrid Approach

```markdown
COMBINE BOTH:
1. JSON for state
2. Markdown for context
3. Reference JSON from Markdown

Example:
## Current Progress
See `checkpoint_2024_12_16.json` for detailed state.
Key highlights:
- 75% complete
- No blockers
- On schedule
```

## Resumption Protocols

### 1. Task Resumption Pattern

```markdown
RESUME TASK PROTOCOL:
1. READ last checkpoint file
2. VERIFY current file states
3. IDENTIFY last completed action
4. DETERMINE next action
5. CHECK for state changes
6. CONTINUE from checkpoint

IMPLEMENTATION:
```json
{
  "resume_from": "checkpoint_3",
  "last_action": "created_database_schema",
  "next_action": "implement_api_endpoints",
  "context_restored": true,
  "ready_to_continue": true
}
```

### 2. Conversation Resumption

```markdown
RESUME CONVERSATION PROTOCOL:
1. SCAN recent messages for context
2. IDENTIFY incomplete tasks
3. RESTORE working state
4. ACKNOWLEDGE resumption
5. CONTINUE or request clarification

MESSAGE: "I see we were working on [task].
Last completed: [action].
Shall I continue with [next action]?"
```

## Multi-Step Workflow Examples

### Example 1: Bootstrap Process

```markdown
STEP 1: Initialization
checkpoint_1.json:
{
  "step": 1,
  "action": "read_specification",
  "spec_file": "project_spec.md",
  "status": "complete"
}

STEP 2: Template Detection
checkpoint_2.json:
{
  "step": 2,
  "action": "detect_template",
  "detected": "power-query",
  "confidence": 0.92,
  "status": "complete"
}

STEP 3: File Generation
checkpoint_3.json:
{
  "step": 3,
  "action": "generate_files",
  "progress": "60%",
  "completed": ["CLAUDE.md", ".claude/commands/"],
  "remaining": [".claude/tasks/"],
  "status": "in_progress"
}
```

### Example 2: Codebase Analysis

```markdown
PHASE 1: Discovery
{
  "phase": "discovery",
  "files_found": 234,
  "directories_mapped": true,
  "techstack_identified": ["React", "Node", "PostgreSQL"],
  "checkpoint": "discovery_complete"
}

PHASE 2: Deep Analysis
{
  "phase": "analysis",
  "components_analyzed": 45,
  "dependencies_mapped": true,
  "issues_found": 12,
  "checkpoint": "analysis_complete"
}

PHASE 3: Recommendations
{
  "phase": "recommendations",
  "report_generated": true,
  "priorities_set": true,
  "checkpoint": "complete"
}
```

## Token Optimization Strategies

### 1. Selective Context Loading

```markdown
INSTEAD OF: Loading everything
DO: Load only what's needed

# Beginning of task:
Load: Task definition, requirements
Skip: Previous task history

# Middle of task:
Load: Current checkpoint, active files
Skip: Completed phase details

# End of task:
Load: Validation criteria, summary template
Skip: Intermediate states
```

### 2. Reference Instead of Inline

```markdown
INSTEAD OF:
"Here's the full code: [5000 tokens of code]"

DO:
"Code implemented in auth.js (lines 45-127)
Key features:
- JWT validation
- Role-based access
- Refresh token handling"
```

### 3. Incremental Updates

```markdown
INSTEAD OF: Rewriting full state
DO: Update only changed fields

# Initial state
state_v1.json: Full state (1000 tokens)

# Updates
update_v2.json: {"tasks_completed": append(4)}
update_v3.json: {"status": "testing"}

# Final merge for checkpoint
checkpoint_final.json: Merged state
```

## Progress Tracking Patterns

### 1. Percentage-Based Tracking

```json
{
  "overall_progress": 65,
  "phase_progress": {
    "planning": 100,
    "implementation": 80,
    "testing": 40,
    "documentation": 0
  },
  "time_estimates": {
    "elapsed": "2 hours",
    "remaining": "1 hour"
  }
}
```

### 2. Milestone-Based Tracking

```json
{
  "milestones": [
    {"id": 1, "name": "Setup", "status": "complete"},
    {"id": 2, "name": "Core Features", "status": "complete"},
    {"id": 3, "name": "Testing", "status": "in_progress"},
    {"id": 4, "name": "Deployment", "status": "pending"}
  ],
  "current_milestone": 3,
  "blockers": []
}
```

### 3. Step Counter Tracking

```json
{
  "total_steps": 25,
  "completed_steps": 18,
  "current_step": 19,
  "step_description": "Running integration tests",
  "steps_remaining": 7
}
```

## Error Recovery Patterns

### 1. Checkpoint Rollback

```markdown
ON ERROR:
1. SAVE error state
2. IDENTIFY last good checkpoint
3. ROLLBACK to checkpoint
4. LOG failure reason
5. ATTEMPT alternative approach

STRUCTURE:
{
  "error": "Database connection failed",
  "checkpoint_rollback": "checkpoint_5",
  "alternative_action": "Use SQLite instead",
  "retry_count": 1
}
```

### 2. Partial Progress Preservation

```markdown
WHEN INTERRUPTED:
1. SAVE partial progress
2. MARK incomplete items
3. CREATE resumption point
4. DOCUMENT stop reason

{
  "partial_progress": {
    "completed": ["task1", "task2"],
    "in_progress": "task3",
    "progress_on_current": "60%",
    "remaining": ["task4", "task5"]
  }
}
```

## Best Practices

### DO:
✅ Create checkpoints before long operations
✅ Use JSON for structured state
✅ Compress verbose output to summaries
✅ Track both progress and blockers
✅ Include resumption instructions
✅ Version your checkpoints
✅ Clean up old checkpoints
✅ Use /compact mid-task when context grows
✅ Use /clear between unrelated tasks
✅ Create markdown checklists for large features
✅ Update task JSON before any context reset

### DON'T:
❌ Store entire file contents in checkpoints
❌ Duplicate information across checkpoints
❌ Mix state and documentation in JSON
❌ Forget to update checkpoint after changes
❌ Include sensitive data in checkpoints
❌ Create checkpoints in tight loops
❌ Use /clear in the middle of a task (use /compact)
❌ Let context grow unbounded without /compact
❌ Forget to re-establish context after /clear

## Integration with Task System

### Task-Checkpoint Relationship

```markdown
Each task maintains:
- checkpoint/ directory for states
- Current checkpoint reference
- Checkpoint history

task-78.json:
{
  "current_checkpoint": "checkpoint_3",
  "checkpoint_history": [
    "checkpoint_1_init",
    "checkpoint_2_analysis",
    "checkpoint_3_implementation"
  ]
}
```

### Automatic Checkpoint Creation

```markdown
CREATE CHECKPOINT WHEN:
- Task status changes
- Completing major phase
- Before risky operations
- At regular intervals (every 10 steps)
- When context exceeds 50% budget
```

## Quick Reference: Session Commands

```markdown
COMMAND CHEAT SHEET:

/clear
  - Full context reset
  - Use: Between tasks, when confused
  - Preserves: Nothing (use checkpoints)

/compact
  - Compress context, keep continuity
  - Use: Mid-task, after verbose ops
  - Preserves: Key context, recent work

FREQUENCY GUIDELINES:
- /compact: Every 30-60 minutes of continuous work
- /clear: After each major milestone/task
- Checkpoints: Every 3-5 significant steps
```

## Conclusion

Effective context management enables Claude Code to handle complex, long-running tasks efficiently. By following these patterns:
- Tasks can be resumed seamlessly
- Context remains within token limits
- Progress is transparent and trackable
- Errors are recoverable
- State is preserved accurately

**Key habits:**
- Use /compact proactively during long sessions
- Use /clear at natural task boundaries
- Create markdown checklists for multi-session features
- Always update task JSON before context resets

Always prioritize structure over narrative, checkpoint frequently, and maintain clear resumption paths.