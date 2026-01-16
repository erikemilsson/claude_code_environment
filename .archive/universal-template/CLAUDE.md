# CLAUDE.md - Universal Project Template

**CRITICAL: This file defines the Claude Code environment structure. Do not modify the structure, schemas, or command patterns documented here unless explicitly instructed by the user.**

## Environment Rules (IMMUTABLE)

### What You CANNOT Change

**Folder Structure:**
```
.claude/
├── context/           # Executive summaries (user approval required)
├── tasks/             # Task JSON files (follow task-schema.md)
├── commands/          # Command patterns (don't modify)
├── agents/            # Agent configs (don't modify)
└── reference/         # Schema docs (don't modify)
```

**Rules:**
1. **Never modify** the folder structure above
2. **Never modify** files in `.claude/commands/`, `.claude/agents/`, `.claude/reference/`
3. **Never modify** `.claude/context/phases.md` or `.claude/context/decisions.md` without explicit user approval
4. **Always follow** schemas in `.claude/reference/*.md` exactly
5. **Never create** implementation files inside `.claude/` folder

### What You CAN Change

**User approval NOT required:**
- Create/update task files in `.claude/tasks/` (following task-schema.md)
- Update `.claude/context/overview.md` (project status summary)
- Create implementation files OUTSIDE `.claude/` folder

**User approval REQUIRED:**
- Changes to `.claude/context/phases.md`
- Changes to `.claude/context/decisions.md`
- Use `/update-executive-summary` command and get approval

## Implementation Files Go Outside .claude/

**Correct:**
```
project/
├── .claude/                  # Environment files (structure defined here)
├── src/                      # Your implementation code
│   ├── components/
│   ├── services/
│   └── utils/
├── tests/                    # Your tests
├── docs/                     # Your documentation
└── [any other project files]
```

**The `.claude/` folder is ONLY for project management, not implementation code.**

## Single Source of Truth Hierarchy

```
CLAUDE.md (this file - environment rules & standards)
    ↓
.claude/context/phases.md + decisions.md (executive summaries - APPROVAL REQUIRED)
    ↓
.claude/tasks/*.json (implementation tasks)
    ↓
Your implementation files (src/, tests/, docs/, etc.)
```

## Quick Start

### Option 1: Direct to Building (Clear Specification)

```bash
# 1. Copy template
cp -r universal-template/ /path/to/your-project/
cd /path/to/your-project/

# 2. Remove planning/ folder (not needed)
rm -rf planning/

# 3. Customize context files
# Edit: .claude/context/overview.md
# Edit: .claude/context/phases.md
# Edit: .claude/context/decisions.md

# 4. Create initial tasks in .claude/tasks/
# Follow .claude/reference/task-schema.md

# 5. Run: /sync-tasks

# 6. Start building (implementation files go in src/, not .claude/)
```

### Option 2: Planning Phase First (Specification Development)

```bash
# 1. Copy template
cp -r universal-template/ /path/to/your-project/
cd /path/to/your-project/

# 2. Run: /init-specification
# This interactively defines decision categories

# 3. Develop planning/specification.md iteratively

# 4. Define phases in planning/.claude/context/phases.md

# 5. Run: /test-specification (when ready to validate)

# 6. Complete generated refinement tasks

# 7. Run: /sync-from-planning (pull to main .claude/)

# 8. Start building (implementation files go in src/, not .claude/)
```

## Core Commands

### /complete-task
Start or finish a task with validation.

**Usage:**
```
/complete-task task-042 start   # Begin work
/complete-task task-042 finish  # Mark complete
```

**Rules:**
- One task `in_progress` at a time
- Check parent auto-completion when finishing subtasks
- Run `/sync-tasks` after finishing

**See:** `.claude/commands/complete-task.md` for details

### /breakdown
Split difficulty ≥7 tasks into subtasks (≤6 each).

**Usage:**
```
/breakdown task-050
```

**Rules:**
- MUST break down tasks with difficulty ≥7 before starting
- Each subtask must be ≤6 difficulty
- Parent auto-completes when all subtasks finish

**See:** `.claude/commands/breakdown.md` for details

### /sync-tasks
Update task-overview.md from task JSON files.

**Usage:**
```
/sync-tasks
```

**When to use:**
- After creating/updating/completing tasks
- Before starting work session
- Automatically called by other commands

**See:** `.claude/commands/sync-tasks.md` for details

## Planning Commands (Optional)

### /init-specification
Initialize planning phase with custom decision categories.

**Usage:**
```
/init-specification
```

**Interactive process:**
1. Define decision categories (architecture, data, integration, etc.)
2. Creates planning/ structure
3. Sets up specification template

**See:** `.claude/commands/init-specification.md` for details

### /test-specification
Generate and execute specification validation tests.

**Usage:**
```
/test-specification              # Full spec
/test-specification --section 3  # Specific section
/test-specification --rerun      # Re-run existing tests
```

**Process:**
1. Generates test files in planning/tests/
2. Executes with specification-architect agent
3. Creates tasks for issues found

**See:** `.claude/commands/test-specification.md` for details

### /update-executive-summary
Refresh phases.md and decisions.md (REQUIRES APPROVAL).

**Usage:**
```
/update-executive-summary
```

**CRITICAL:**
- Shows diff of proposed changes
- MUST get user approval before applying
- Updates change logs
- Runs /sync-tasks after

**See:** `.claude/commands/update-executive-summary.md` for details

## Task Management

### Task Schema
**All tasks MUST follow:** `.claude/reference/task-schema.md`

**Key fields:**
```json
{
  "id": "task-001",
  "title": "Brief description",
  "description": "Detailed requirements",
  "status": "pending | in_progress | blocked | broken_down | finished",
  "difficulty": 1-10,
  "priority": "critical | high | medium | low",
  "parent_task": "task-000 | null",
  "subtasks": ["task-001-1", "task-001-2"],
  "related_phases": ["phase-1"],
  "related_decisions": ["decision-001"],
  "validation": {
    "criteria": ["..."],
    "completed": false
  }
}
```

**Difficulty scoring:**
- 1-2: Trivial
- 3-4: Low
- 5-6: Moderate
- 7-8: High (**MUST break down**)
- 9-10: Extreme (**MUST break down**)

**Status flow:**
```
pending → in_progress → finished
            ↓
        broken_down (difficulty ≥7)
            ↓
        [subtasks finish]
            ↓
        auto-completes
```

### Phase Tracking
**Schema:** `.claude/reference/phase-schema.md`

**Defined in:** `.claude/context/phases.md` (APPROVAL REQUIRED for changes)

**Structure:**
- Phase ID, order, status
- Inputs and outputs
- Components within phase
- Related tasks and decisions

**Use `/update-executive-summary` to propose changes (requires approval).**

### Decision Tracking
**Schema:** `.claude/reference/decision-schema.md`

**Defined in:** `.claude/context/decisions.md` (APPROVAL REQUIRED for changes)

**Track only major/architectural decisions:**
- Technology stack choices
- Architectural patterns
- Data modeling approaches
- Security strategies
- Integration methods

**Use `/update-executive-summary` to propose changes (requires approval).**

## Agents (Optional)

### specification-architect
Validates specifications for completeness and consistency.

**When to use:**
- Running `/test-specification`
- Validating spec sections
- Tasks assigned with `assigned_agent: "specification-architect"`

**See:** `.claude/agents/specification-architect.md`

### implementation-architect
Designs implementation approaches for complex tasks.

**When to use:**
- Tasks with difficulty ≥7 that need breakdown
- Complex architectural decisions
- System design questions
- Tasks assigned with `assigned_agent: "implementation-architect"`

**See:** `.claude/agents/implementation-architect.md`

### test-generator
Generates comprehensive test plans and test tasks.

**When to use:**
- After specification development
- Before implementing features
- When test coverage unclear
- Tasks assigned with `assigned_agent: "test-generator"`

**See:** `.claude/agents/test-generator.md`

## Reference Documentation

**Read these for complete schemas and examples:**

- `.claude/reference/task-schema.md` - Task JSON structure (comprehensive)
- `.claude/reference/phase-schema.md` - Phase tracking structure
- `.claude/reference/decision-schema.md` - Decision tracking structure
- `.claude/reference/test-schema.md` - Specification test structure

**Each reference includes:**
- Field definitions
- Detailed examples
- Best practices
- Troubleshooting guides

## Mandatory Rules

### Task Management
1. **ALWAYS** break down difficulty ≥7 tasks before starting
2. **ALWAYS** have exactly one task `in_progress` at a time
3. **ALWAYS** run `/sync-tasks` after completing tasks
4. **NEVER** work on parent tasks marked as `broken_down`
5. **NEVER** modify task JSON structure (follow task-schema.md)

### Folder Structure
1. **NEVER** modify `.claude/` folder structure
2. **NEVER** create implementation files in `.claude/`
3. **ALWAYS** create implementation files outside `.claude/` (src/, tests/, etc.)
4. **NEVER** modify command, agent, or reference files
5. **NEVER** modify phases.md or decisions.md without approval

### Executive Summaries
1. **ALWAYS** use `/update-executive-summary` to propose changes
2. **ALWAYS** get user approval before changing phases.md or decisions.md
3. **NEVER** directly edit executive summaries without approval process
4. **ALWAYS** update change logs when changes approved

### Schema Compliance
1. **ALWAYS** follow schemas in `.claude/reference/*.md` exactly
2. **NEVER** add custom fields to schemas without user approval
3. **ALWAYS** validate task JSON against task-schema.md
4. **NEVER** deviate from status values or field formats

## Troubleshooting

**Problem:** Can't find where to document something
→ Read relevant schema in `.claude/reference/`

**Problem:** Need to change phase structure
→ Run `/update-executive-summary` and get approval

**Problem:** Task complexity overwhelming
→ Check difficulty, use `/breakdown` if ≥7

**Problem:** Unsure if decision should be tracked
→ Only major/architectural decisions (see decision-schema.md)

**Problem:** Where do implementation files go?
→ OUTSIDE `.claude/` - create `src/`, `tests/`, `docs/`, etc.

## Version
- **Template Version:** 2.0
- **Date:** 2025-12-29
- **Changes:** Universal template with standardized schemas and protected structure
