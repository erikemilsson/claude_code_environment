# Claude Code Environment Builder

## Purpose

This template helps create customized Claude Code project environments from initial requirements. Provide your project idea, answer clarifying questions, and receive a tailored file structure with context-aware documentation.

------

## Quick Start: Minimal Example

Don't need the full template system? Here's the absolute minimum setup for a simple project:

#### Minimal Structure (5 minutes)

```
my-project/
├── CLAUDE.md
└── .claude/
    ├── tasks/
    │   ├── task-overview.md
    │   ├── task-1.json
    │   ├── task-2.json
    │   └── task-3.json
    └── commands/
        ├── sync-tasks.md
        ├── update-tasks.md
        └── complete-task.md
```

#### CLAUDE.md

```markdown
# Project: [Name]

## What I'm Building
[2-3 sentence description]

## Current Tasks
See `.claude/tasks/task-overview.md`

## Commands
- `@.claude/commands/sync-tasks.md` - Update task overview

## Next Action
[What you're working on right now]
```

#### Task Example (task-1.json)

```json
{
  "id": "1",
  "title": "Setup project structure",
  "description": "Create basic folder layout and README",
  "difficulty": 2,
  "status": "Pending",
  "created_date": "2024-01-15",
  "dependencies": [],
  "subtasks": [],
  "parent_task": null,
  "notes": ""
}
```

### When to Use Minimal vs. Full Template

**Use Minimal Setup for:**

- ✅ Weekend projects (< 10 tasks)
- ✅ Learning/experimental work
- ✅ Single-file scripts or utilities
- ✅ When you just need task tracking

**Use Full Template for:**

- ✅ Multi-week projects (10+ tasks)
- ✅ Multiple technologies/standards to track
- ✅ Team collaboration
- ✅ Production systems
- ✅ When you need reusable command patterns

**Upgrade Path**: Start minimal, add folders as needed:

1. Add `.claude/context/overview.md` when scope grows
2. Add `.claude/commands/` when you repeat instructions
3. Add `.claude/reference/` when you need to track decisions
4. Add `.claude/context/standards/` when code consistency matters

------

## How This Works

### Step 1: Initial Input

You provide:

- **Project description** (brain dump is fine)
- **Type of work** (coding, planning, analysis, etc.)
- **Any specific requirements** (tools, constraints, deadlines)

### Step 2: Clarification

Claude Code will ask about:

- Project goals and success criteria
- Technical stack preferences
- Timeline and constraints
- Collaboration needs
- Existing resources or dependencies

### Step 3: Environment Creation

Claude Code builds your customized environment with:

- Appropriate folder structure
- Context files for Claude's memory
- Command definitions for repeated tasks
- Reference documentation
- Task management structure with hierarchical breakdown support

------

## Core Environment Pattern

Every project follows this base structure, adapted to specific needs:

```
project/
├── CLAUDE.md              # Router file (keeps context minimal)
├── README.md              # Human-readable documentation
└── .claude/               # Claude-specific context
    ├── commands/          # Reusable task patterns
    ├── context/           # Project understanding
    ├── tasks/             # Work tracking
    └── reference/         # Information storage
```

### Key Principles

1. **CLAUDE.md as Router**: Root file stays under 100 lines, points to relevant docs
2. **Separation of Concerns**: `.claude/` for AI, everything else for humans
3. **Lazy Loading**: Only load context when needed for specific tasks
4. **Progressive Enhancement**: Start simple, add complexity as needed
5. **Hierarchical Task Management**: Complex tasks automatically decompose into manageable subtasks

------

## Environment Types

### 1. Base Template (Any Project)

**Use for**: General planning, research, non-technical projects

```
project/
├── CLAUDE.md
├── README.md
└── .claude/
    ├── commands/
    │   ├── plan.md            # Break down goals into tasks
    │   ├── breakdown.md       # Split high-difficulty tasks
    │   ├── update-tasks.md    # Validate and refresh tasks
    │   ├── complete-task.md   # Work on tasks with status tracking
    │   ├── sync-tasks.md      # Update task-overview.md
    │   ├── research.md        # Investigate solutions
    │   └── status.md          # Report progress
    ├── context/
    │   ├── overview.md        # What are we building?
    │   ├── constraints.md     # Limitations & requirements
    │   ├── preferences.md     # Personal/team preferences
    │   └── validation-rules.md # Task validation rules
    ├── tasks/
    │   ├── task-overview.md   # Auto-updated task table
    │   ├── task-1.json        # Individual task files
    │   ├── task-2.json        # (sequential numbering)
    │   └── ...
    └── reference/
        ├── notes.md           # Research findings
        ├── difficulty-guide.md # Task difficulty scoring
        └── breakdown-workflow.md # Hierarchical task management guide
```

### 2. Data Engineering Template

**Use for**: ETL pipelines, data processing, analytics engineering

```
project/
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── commands/
│   │   ├── plan.md            # Feature breakdown
│   │   ├── breakdown.md       # Split high-difficulty tasks
│   │   ├── update-tasks.md    # Validate tasks
│   │   ├── complete-task.md   # Work with status tracking
│   │   ├── sync-tasks.md      # Update task-overview.md
│   │   ├── review-code.md     # Code quality checks
│   │   ├── optimize.md        # Performance tuning
│   │   └── document.md        # Generate docs
│   ├── context/
│   │   ├── overview.md        # System architecture
│   │   ├── standards/
│   │   │   ├── python.md      # Python/Polars patterns
│   │   │   ├── sql.md         # SQL conventions
│   │   │   └── testing.md     # Test requirements
│   │   ├── workflows.md       # CI/CD process
│   │   └── validation-rules.md # Task validation
│   ├── tasks/
│   │   ├── task-overview.md   # Sprint task table
│   │   ├── task-1.json        # Individual tasks
│   │   └── ...
│   └── reference/
│       ├── data-model.md      # Schema documentation
│       ├── dependencies.md    # External systems
│       ├── performance.md     # Optimization notes
│       ├── difficulty-guide.md # Task scoring
│       └── breakdown-workflow.md # Task hierarchy guide
├── src/
│   └── etl/
├── tests/
└── docs/
```

### 3. BI/Dashboard Template

**Use for**: Power BI, reporting, visualization projects

```
project/
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── commands/
│   │   ├── plan.md            # Dashboard requirements
│   │   ├── breakdown.md       # Split complex features
│   │   ├── update-tasks.md    # Validate tasks
│   │   ├── complete-task.md   # Work with status tracking
│   │   ├── sync-tasks.md      # Update task-overview.md
│   │   ├── review-dax.md      # DAX optimization
│   │   ├── validate.md        # Check calculations
│   │   └── document-kpi.md    # Explain metrics
│   ├── context/
│   │   ├── overview.md        # Dashboard purpose
│   │   ├── standards/
│   │   │   ├── powerbi.md     # Naming conventions
│   │   │   ├── dax.md         # DAX patterns
│   │   │   └── design.md      # Visual guidelines
│   │   ├── users.md           # Audience needs
│   │   └── validation-rules.md # Task validation
│   ├── tasks/
│   │   ├── task-overview.md   # Feature task table
│   │   ├── task-1.json        # Individual tasks
│   │   └── ...
│   └── reference/
│       ├── data-sources.md    # Available connections
│       ├── kpis.md            # Business metrics
│       ├── glossary.md        # Term definitions
│       ├── difficulty-guide.md # Task scoring
│       └── breakdown-workflow.md # Task hierarchy guide
├── reports/
└── queries/
```

### 4. Hybrid Template

**Use for**: Projects combining multiple technologies

Combines elements from above templates based on needs.

------

## Task Management System

### Task Structure

Tasks are stored as individual JSON files in `.claude/tasks/` with this schema:

```json
{
  "id": "1",
  "title": "Setup authentication system",
  "description": "Implement OAuth2 with Google and GitHub providers",
  "difficulty": 7,
  "status": "Pending",
  "created_date": "2024-01-15",
  "updated_date": "2024-01-15",
  "assigned_to": null,
  "estimated_hours": 8,
  "actual_hours": 0,
  "dependencies": [],
  "subtasks": [],
  "parent_task": null,
  "files_affected": ["src/auth/", "config/oauth.json"],
  "notes": "",
  "blockers": [],
  "tags": ["security", "backend"],
  "breakdown_history": null
}
```

### Difficulty Scoring (LLM Error Risk)

| Level    | Risk        | Examples                                      |
| -------- | ----------- | --------------------------------------------- |
| 1-2      | Trivial     | Fix typo, update text, add comment            |
| 3-4      | Low         | Basic CRUD, simple UI changes                 |
| 5-6      | Moderate    | Form validation, API integration              |
| **7-8**  | **High**    | **Auth setup, database migration**            |
| **9-10** | **Extreme** | **Architecture changes, distributed systems** |

**Critical Rule**: Tasks with difficulty ≥7 should be broken down into subtasks with difficulty ≤6 using the breakdown command to reduce error risk.

### Task Status Values

| Status          | Meaning                        | Can Work On? | Auto-Transitions       |
| --------------- | ------------------------------ | ------------ | ---------------------- |
| **Pending**     | Defined but not started        | ✅ Yes        | → In Progress (manual) |
| **In Progress** | Actively being worked on       | ✅ Yes        | → Finished (manual)    |
| **Blocked**     | Cannot proceed due to blockers | ❌ No         | → In Progress (manual) |
| **Broken Down** | Decomposed into subtasks       | ❌ No         | → Finished (automatic) |
| **Finished**    | Complete                       | ❌ No         | None (terminal)        |

**Key Concept**: "Broken Down" tasks are **containers** that track progress through their subtasks. They cannot be worked on directly and auto-complete when all subtasks finish.

### Task Overview Synchronization

The `task-overview.md` file is automatically updated whenever task JSON files change:

```markdown
| ID / File | Task | Difficulty | Dependencies | Status |
|-----------|------|------------|--------------|--------|
| 1. [task-1.json](task-1.json) | Setup authentication | 7 🔴 | | Pending |
| 2. [task-2.json](task-2.json) | Build dashboard | 5 | 1 | Pending |
```

**Status Indicators:**

- 🔴 High difficulty (≥7) without "Broken Down" status - needs breakdown
- 🔵 Broken Down (shows subtask progress: "Broken Down (X/Y done)")
- 🟡 Blocked
- 🟢 Finished

------

## Command Patterns

Commands are reusable instructions stored in `.claude/commands/`. They follow this structure:

```markdown
# Command: [Name]

## Purpose
[What this command does]

## Context Required
- [List of files to read first]

## Process
1. [Step-by-step instructions]
2. [What to analyze]
3. [What to output]

## Output Location
- [Where to save results]
```

### Core Commands

#### `/complete-task`

**Starts work on a task with proper status tracking.** This is the standard entry point for beginning any task. Gets user confirmation, updates status to "In Progress", performs the work, then marks as "Finished" with feedback on results. Blocks work on "Broken Down" tasks and implements automatic parent task completion.

#### `/breakdown`

**Splits tasks with difficulty ≥7 into manageable subtasks.** Automatically transitions parent task to "Broken Down" status and establishes completion dependency chain. Parent cannot be worked on directly after breakdown.

#### `/update-tasks`

Validates all task structures, checks consistency between JSON files and task-overview.md, flags any outdated or irrelevant tasks, and ensures the task system is properly synchronized.

#### `/plan`

Creates new tasks from requirements with appropriate difficulty scoring

#### `/sync-tasks`

Updates `task-overview.md` from all task JSON files. Shows subtask progress for "Broken Down" tasks.

#### `/status`

Shows current sprint progress with risk assessment

#### `/review`

Analyzes code/content against project standards

#### `/research`

Investigates solutions with pros/cons analysis

#### `/optimize`

Identifies performance improvements

------

## CLAUDE.md Router Pattern

The root CLAUDE.md should always follow this minimal structure:

```markdown
# Project: [Name]

## Quick Start
For [specific task], read:
- `.claude/context/[relevant].md`
- `.claude/reference/[relevant].md`

## Available Commands
- `.claude/commands/complete-task.md` - Start working on a task
- `.claude/commands/breakdown.md` - Split high-difficulty tasks (≥7)
- `.claude/commands/update-tasks.md` - Validate and refresh all tasks
- `.claude/commands/sync-tasks.md` - Update task overview
- `.claude/commands/status.md` - Show progress and risk assessment
- `.claude/commands/review.md` - Check quality
- [project-specific commands]

## Working on Tasks
**Always use `.claude/commands/complete-task.md` to start work on any task.** This ensures proper status tracking and prevents inconsistencies.

**For high-difficulty tasks (≥7):**
1. Run `.claude/commands/breakdown.md [task-id]` first
2. Parent task automatically becomes "Broken Down" (cannot be worked on directly)
3. Work on the created subtasks using complete-task.md
4. Parent auto-completes when all subtasks are finished

## Task Status Legend
- 🔴 Needs breakdown (difficulty ≥7, not yet broken down)
- 🔵 Broken Down (work on subtasks, shows X/Y progress)
- 🟡 Blocked
- 🟢 Finished

## Task Management
- Current tasks: `.claude/tasks/task-overview.md`
- High-risk tasks (difficulty ≥7) should be broken down using breakdown.md
- Run `/sync-tasks` after manual task updates
- See `.claude/reference/breakdown-workflow.md` for hierarchical task management guide

## Navigation Rules
- Planning work? → Start with `.claude/tasks/task-overview.md`
- Writing code? → Read `.claude/context/standards/`
- Need context? → Check `.claude/reference/`

## Current Focus
[1-2 lines about what's being worked on]
```

------

## Command File Examples

### breakdown.md

~~~markdown
# Command: Breakdown High-Difficulty Tasks

## Purpose
Split tasks with difficulty ≥7 into smaller, manageable subtasks to reduce LLM error risk. Automatically transitions parent task to "Broken Down" status and establishes completion dependency chain.

## Context Required
- `.claude/tasks/*.json` (all task files)
- `.claude/context/validation-rules.md`
- `.claude/reference/difficulty-guide.md`

## Process

### 1. Identify Breakdown Candidate
- Accept task ID as parameter: `@breakdown.md <task_id>`
- Read the specified task JSON file
- **Validate eligibility:**
  - Task difficulty MUST be ≥7
  - Task status MUST be "Pending" or "In Progress"
  - Task MUST NOT already have status "Broken Down" or "Finished"
  - If invalid, halt with clear error message

### 2. Analyze and Plan Breakdown
- Review task description, requirements, and `files_affected`
- Identify logical components that can be separated
- Design subtasks following these rules:
  - Each subtask difficulty MUST be ≤6
  - Subtasks MUST cover all original requirements
  - Subtasks SHOULD be independently testable
  - Create natural dependency order if needed
- Confirm breakdown plan with user before proceeding

### 3. Create Subtask Files
For each planned subtask:
- Generate new task ID (next sequential number)
- Create JSON file: `.claude/tasks/task-{new_id}.json`
- Set required fields:
  ```json
  {
    "id": "{new_id}",
    "title": "{subtask_title}",
    "description": "{detailed_description}",
    "difficulty": {1-6},
    "status": "Pending",
    "created_date": "{YYYY-MM-DD}",
    "updated_date": "{YYYY-MM-DD}",
    "parent_task": "{original_task_id}",
    "dependencies": [{other_subtask_ids_if_needed}],
    "subtasks": [],
    "notes": "Created from breakdown of Task {original_task_id}"
  }
~~~

### 4. Update Parent Task to "Broken Down"

This is the CRITICAL step that solves the state ambiguity problem:

- Update original task JSON file:

  ```json
  {  "status": "Broken Down",  "updated_date": "{current_date}",  "breakdown_history": "{current_date}",  "subtasks": ["{subtask_1_id}", "{subtask_2_id}", ...],  "notes": "{original_notes}\n\n[{date}] Task broken down into {N} subtasks: #{ids}. Parent task will auto-complete when all subtasks finish."}
  ```

### 5. Sync and Report

- Run `@.claude/commands/sync-tasks.md` to update overview
- Provide breakdown summary:
  - Original task ID and title
  - Number of subtasks created
  - List of subtask IDs with titles and difficulties
  - Confirmation that parent is now "Broken Down"
  - Next recommended action (start first subtask)

## Automatic Completion Logic

**IMPORTANT:** The following logic should be checked by `complete-task.md` whenever marking a subtask as "Finished":

```
When marking subtask as "Finished":
1. Read subtask's `parent_task` field
2. If parent_task exists:
   a. Load parent task JSON
   b. If parent status == "Broken Down":
      - Check ALL tasks in parent's `subtasks` array
      - If ALL subtasks have status "Finished":
        * Update parent status to "Finished"
        * Set parent updated_date to current date
        * Add note: "Auto-completed: all subtasks finished"
        * Report to user: "✅ Parent Task #{id} automatically completed!"
```

## Example Breakdown

**Input Task:**

```json
{
  "id": "12",
  "title": "Build emissions data ETL pipeline",
  "difficulty": 8,
  "status": "Pending"
}
```

**After Breakdown:**

**Parent Task (task-12.json):**

```json
{
  "id": "12",
  "title": "Build emissions data ETL pipeline",
  "difficulty": 8,
  "status": "Broken Down",
  "breakdown_history": "2024-01-15",
  "subtasks": ["13", "14", "15", "16", "17"],
  "notes": "[2024-01-15] Task broken down into 5 subtasks: #13-17. Parent will auto-complete when all subtasks finish."
}
```

**Created Subtasks:**

- Task 13: "Design pipeline architecture" (difficulty: 4, parent: "12")
- Task 14: "Build API connectors for emissions data sources" (difficulty: 5, parent: "12")
- Task 15: "Implement data transformation with Polars" (difficulty: 6, parent: "12")
- Task 16: "Create Azure SQL loader" (difficulty: 5, parent: "12")
- Task 17: "Add error handling and logging" (difficulty: 4, parent: "12")

## Output Location

- New task JSON files in `.claude/tasks/` (one per subtask)
- Updated parent task JSON file (status → "Broken Down")
- Updated `.claude/tasks/task-overview.md` (via sync-tasks)
- Console report of breakdown results

## Error Handling

- If task already "Broken Down": "Task #{id} has already been broken down into subtasks #{list}. Use update-tasks.md to modify existing subtasks."
- If task difficulty <7: "Task #{id} has difficulty {X} which is below the breakdown threshold (7). Breakdown not needed."
- If task "Finished": "Cannot break down completed task #{id}."

### sync-tasks.md

```
# Command: Sync Task Overview

## Purpose
Update task-overview.md to reflect current state of all task JSON files.

## Context Required
- `.claude/tasks/*.json` (all task files)
- `.claude/context/validation-rules.md`

## Process
1. Read all task JSON files in `.claude/tasks/` using @.claude/tasks/*.json
2. Sort by task ID (numerical order)
3. Validate each task against validation rules
4. Generate markdown table with columns:
   - ID / File (linked)
   - Task (title)
   - Difficulty
   - Dependencies (comma-separated IDs)
   - Status
5. Add status indicators:
   - 🔴 for difficulty ≥7 without "Broken Down" status
   - 🔵 for "Broken Down" tasks (show subtask progress)
   - 🟡 for blocked tasks
   - 🟢 for completed tasks
6. **For "Broken Down" tasks, calculate and show completion progress:**
   - Count finished subtasks vs total subtasks
   - Format status as: "Broken Down (X/Y done)"
   - Example: "Broken Down (3/5 done)"
7. Include summary statistics:
   - Total tasks
   - Average difficulty
   - Blocked count
   - Completion percentage

## Output Location
- `.claude/tasks/task-overview.md` (overwrite completely)

## Example Output

```markdown
# Project Tasks Overview

## Summary
- Total Tasks: 8
- Top-level Tasks: 3
- Subtasks: 5
- Average Difficulty: 5.2
- Blocked: 0
- Complete: 37%

## All Tasks

| ID / File | Task | Difficulty | Dependencies | Status |
|-----------|------|------------|--------------|--------|
| 12. [task-12.json](task-12.json) | Build emissions ETL | 8 🔵 | | Broken Down (3/5 done) |
| 13. [task-13.json](task-13.json) | ↳ Design pipeline architecture | 4 | | Finished 🟢 |
| 14. [task-14.json](task-14.json) | ↳ Build API connectors | 5 | 13 | Finished 🟢 |
| 15. [task-15.json](task-15.json) | ↳ Implement Polars transforms | 6 | 14 | In Progress |
| 16. [task-16.json](task-16.json) | ↳ Create Azure SQL loader | 5 | 15 | Pending |
| 17. [task-17.json](task-17.json) | ↳ Add error handling | 4 | 15,16 | Pending |

### Legend
- 🔴 High risk (difficulty ≥7) - needs breakdown
- 🔵 Broken Down - work on subtasks
- 🟡 Blocked - needs resolution
- 🟢 Complete
- ↳ Indicates subtask (indented under parent)

### Difficulty Scale
1-2: Trivial | 3-4: Low | 5-6: Moderate | 7-8: High | 9-10: Extreme
### update-tasks.md

```markdown
# Command: Update Tasks

## Purpose
Validate task structure, ensure tasks are still relevant, and flag any inconsistencies between task JSON files and task-overview.md. This is the main command for checking system health.

## Context Required
- `.claude/tasks/*.json` (all task files)
- `.claude/tasks/task-overview.md`
- `.claude/context/validation-rules.md`
- `.claude/reference/difficulty-guide.md`
  
## Process
1. **Read all task files** using @.claude/tasks/*.json and @.claude/tasks/task-overview.md
2. **Validate structure and rules** for each task:
   - All required fields present and valid
   - Status values are legal ("Pending", "In Progress", "Blocked", "Broken Down", "Finished")
   - Difficulty scoring is appropriate per difficulty-guide.md
   - Dates are in YYYY-MM-DD format
   - Dependencies reference existing task IDs and there are no circular dependencies
   - "Broken Down" tasks have at least one subtask in `subtasks` array
   - Subtasks have valid `parent_task` reference
3. **Check consistency** between JSON files and task-overview.md:
   - Are all tasks from JSON files present in overview?
   - Do statuses match between JSON and overview?
   - Are difficulty scores consistent?
   - Does overview correctly show subtask progress for "Broken Down" tasks?
4. **Assess relevance:**
   - Are "In Progress" tasks actually being worked on?
   - Are "Blocked" tasks listing specific blockers?
   - Are finished tasks marked with completion dates?
   - Do "Broken Down" tasks have all their subtasks created?
5. **Validate parent-child relationships:**
   - All subtasks listed in parent's `subtasks` array exist
   - All subtasks with `parent_task` reference a valid parent
   - Parent tasks with difficulty ≥7 and status "Pending" should be flagged for breakdown
6. **Update if needed:**
   - If JSON files are correct but overview is outdated: run sync-tasks
   - If JSON files need updates: update them first, then run sync-tasks
   - Flag any tasks that may be outdated or irrelevant
7. **Report findings:**
   - List any validation errors or inconsistencies found
   - Suggest corrections
   - Confirm if system is in sync

## Output Location
- Console report of findings
- Updated task JSON files (if corrections needed)
- Updated `.claude/tasks/task-overview.md` (via sync-tasks if needed)
```

### complete-task.md

```markdown
# Command: Complete Task

## Purpose
Begin working on a task with proper status tracking. This is the standard way to start any task work.

## Context Required
- Specific task JSON file (e.g., `.claude/tasks/task-X.json`)
- `.claude/tasks/task-overview.md`
- `.claude/context/validation-rules.md` 
- Any context files relevant to the task
	
## Process
1. **Load task details:**
   - Read the specified task JSON file
   - Read task-overview.md to check dependencies and current state
   - **Check if status is "Broken Down":**
     * If yes, halt with message: "❌ Task {id} has been broken down into subtasks {list}. Please work on the individual subtasks instead. Use '@.claude/commands/complete-task.md {subtask_id}' to start a subtask."
   - Verify all dependencies are marked "Finished"

2. **Confirm with user:**
   - Display task title, description, and estimated hours
   - Show any blockers or dependencies
   - If task has `parent_task`, show parent context
   - Ask: "Ready to start work on Task X: [title]? (yes/no)"
   - Wait for user confirmation before proceeding

3. **Update status to "In Progress":**
   - Update task JSON file:
     * `"status": "In Progress"`
     * `"updated_date"` to current date (YYYY-MM-DD format)
     * If not already set, add `"actual_hours": 0`

4. **Sync overview:**
   - Run @.claude/commands/sync-tasks.md to update task-overview.md

5. **Begin work:**
   - Load any standards or context files mentioned in `files_affected`
   - Perform the task work
   - Track any issues or notes

6. **Update upon completion:**
   - Update task JSON file:
     * `"status": "Finished"`
     * `"updated_date"` to completion date
     * `"actual_hours"` with time spent
     * Add any relevant notes to `"notes"` field
   
   - **Check for parent task auto-completion:**
     * Read task's `parent_task` field
     * If parent_task exists:
       - Load parent task JSON file
       - If parent status == "Broken Down":
         * Get all task IDs from parent's `subtasks` array
         * Load each subtask JSON and check status
         * If ALL subtasks are "Finished":
           - Update parent task JSON:
             * `"status": "Finished"`
             * `"updated_date"` to current date
             * Add to `"notes"`: "Auto-completed: all subtasks finished on {date}"
           - Report to user: "🎉 Completing this subtask also completed parent Task #{parent_id}: {parent_title}!"

7. **Final sync and feedback:**
   - Run @.claude/commands/sync-tasks.md again
   - Provide completion summary:
     * What was accomplished
     * Any blockers encountered
     * Estimated vs actual hours
     * Files created/modified
     * If parent was auto-completed, mention it
     * Suggested next task (lowest difficulty with no dependencies)
	
## Output Location
- Updated task JSON file in `.claude/tasks/`
- Possibly updated parent task JSON file (if auto-completion triggered)
- Updated `.claude/tasks/task-overview.md` (via sync-tasks)
- Console feedback on task progress and completion
- Any work products in their appropriate project locations

## Example: Parent Auto-Completion

User: @.claude/commands/complete-task.md 17

[Task work happens...]

✅ Task #17 "Add error handling" completed!

- Estimated: 3 hours
- Actual: 2.5 hours
- Files modified: src/etl/error_handler.py, tests/test_errors.py

🎉 Completing this subtask also completed parent Task #12: "Build emissions data ETL pipeline"! All 5 subtasks (13-17) are now finished.

Suggested next task: Task #18 "Create dashboard mockups" (difficulty: 4)
```



------

## Context File Templates

### overview.md

```markdown
# Project Overview

## Goal
[What success looks like]

## Scope
- Included: [What we're building]
- Excluded: [What we're not]

## Key Decisions
- [Technology choices]
- [Architecture patterns]
```

### standards/[technology].md

```markdown
# [Technology] Standards

## Conventions
- [Naming patterns]
- [File organization]

## Patterns
- [Preferred approaches]
- [Anti-patterns to avoid]

## Examples
[Code snippets showing correct usage]
```

### tasks/task-overview.md

```markdown
# Project Tasks Overview

## Summary
- Total Tasks: X
- Top-level Tasks: Y
- Subtasks: Z
- Average Difficulty: X.X
- Blocked: X
- Complete: X%

## All Tasks

| ID / File | Task | Difficulty | Dependencies | Status |
|-----------|------|------------|--------------|--------|
| 1. [task-1.json](task-1.json) | Setup authentication | 7 🔴 | | Pending |
| 2. [task-2.json](task-2.json) | Build dashboard | 5 | 1 | Pending |

### Legend
- 🔴 High risk (difficulty ≥7) - needs breakdown
- 🔵 Broken Down - work on subtasks (shows X/Y progress)
- 🟡 Blocked - needs resolution
- 🟢 Complete
- ↳ Indicates subtask (indented under parent)

### Difficulty Scale
1-2: Trivial | 3-4: Low | 5-6: Moderate | 7-8: High | 9-10: Extreme
```

### reference/difficulty-guide.md

```markdown
# Task Difficulty Guide

## Scoring Criteria (LLM Error Probability)

### Low Risk (1-6)
- 1: Single word/character change
- 2: Simple UI text update
- 3: Basic CRUD following pattern
- 4: Standard form with validation
- 5: API integration with docs
- 6: Component with state logic

### High Risk (7-10) - REQUIRES BREAKDOWN
- 7: Multi-provider auth setup
- 8: Database migration with backfill
- 9: Architectural refactoring
- 10: Distributed system implementation

## Breakdown Strategy

When difficulty ≥7:
1. Identify independent components
2. Create logical sequence
3. Each subtask should be ≤6
4. Add clear dependencies
5. Test each subtask independently

## Why Breakdown Matters

**Without Breakdown:**
- Task: "Implement OAuth2 authentication" (difficulty: 8)
- Status: "In Progress" (ambiguous - what part is being worked on?)
- Risk: High error probability, unclear progress

**With Breakdown**
- Parent: "Implement OAuth2 authentication" (difficulty: 8, status: "Broken Down (2/4 done)")
- Subtask 1: "Create OAuth config structure" (difficulty: 3) ✅ Finished
- Subtask 2: "Implement Google provider" (difficulty: 5) ✅ Finished
- Subtask 3: "Implement GitHub provider" (difficulty: 5) 🔄 In Progress
- Subtask 4: "Add session management" (difficulty: 4) ⏳ Pending

Result: Clear progress (50% complete), lower error risk per subtask, parent auto-completes when done.
```

### reference/validation-rules.md

```markdown
# Task Validation Rules

## Required Fields
Every task JSON file must include:
- `id` (string, unique)
- `title` (string, non-empty)
- `description` (string)
- `difficulty` (integer, 1-10)
- `status` (string, from valid statuses)
- `created_date` (string, YYYY-MM-DD format)
- `dependencies` (array of task IDs or empty)
- `subtasks` (array of task IDs or empty)
- `parent_task` (string task ID or null)
- `breakdown_history` (string YYYY-MM-DD format or null)

## Valid Status Values
- **Pending**: Task is defined but not started
- **In Progress**: Task is actively being worked on
- **Blocked**: Task cannot proceed (must have specific blockers listed)
- **Broken Down**: Task has been decomposed into subtasks; completion depends on subtask progress
- **Finished**: Task is complete

## Status-Specific Rules

### "Broken Down" Status
- MUST have at least one subtask in the `subtasks` array
- CANNOT be manually moved to "Finished" (only automatic)
- CANNOT be worked on directly (must work on subtasks)
- Original `difficulty` is preserved for reference
- Automatically transitions to "Finished" when all subtasks are "Finished"
- MUST have `breakdown_history` timestamp set

### Subtask Rules
- If `parent_task` is not null, task is a subtask
- Parent task referenced in `parent_task` must exist
- Parent task must have this subtask in its `subtasks` array
- Subtasks should have difficulty ≤6

## Legal Status Transitions
- Pending → In Progress (when work begins)
- Pending → Blocked (if blockers discovered before starting)
- Pending → **Broken Down** (when using breakdown.md command)
- In Progress → Finished (when work completes successfully)
- In Progress → Blocked (if blockers encountered during work)
- In Progress → **Broken Down** (if complexity discovered mid-work)
- Blocked → In Progress (when blockers are resolved)
- Blocked → Pending (if need to reset blocked task)
- **Broken Down → Finished** (automatic only, when all subtasks done)

## Illegal Transitions
- Finished → any other status (completed tasks don't regress)
- Direct Pending → Finished (must go through In Progress, unless parent is Broken Down)
- **Broken Down → In Progress** (cannot resume work on broken down task)
- **Manual Broken Down → Finished** (only automatic transition allowed)

## Automatic Status Updates
- When using complete-task.md: Status automatically changes Pending → In Progress → Finished
- When completing a subtask: Check if parent should auto-complete
- When using breakdown.md: Parent status automatically changes to "Broken Down"
- When using update-tasks.md: Status inconsistencies are flagged but not auto-corrected
- When using sync-tasks.md: Status is read from JSON and displayed in overview (no changes to JSON)

## Dependency Rules
- Tasks with unfinished dependencies should stay "Pending"
- Task cannot depend on itself
- No circular dependencies (A→B→C→A)
- All dependency IDs must reference existing tasks
- Subtasks can depend on other subtasks from the same parent

## Difficulty Rules
- Tasks with difficulty ≥7 should be broken down using breakdown.md
- Subtasks should each have difficulty ≤6
- Difficulty should match criteria in difficulty-guide.md
- Parent task's original difficulty is preserved even after breakdown

## Parent-Child Relationship Rules
- If task has `parent_task` set, it must be listed in parent's `subtasks` array
- If task has entries in `subtasks` array, those tasks must have `parent_task` pointing back
- A task cannot be both a parent and a subtask (no nesting beyond one level)
- All subtasks of a "Broken Down" parent must exist as valid task files
```

### reference/breakdown-workflow.md

```markdown
# Task Breakdown Workflow Guide

## When to Break Down Tasks

**Mandatory breakdown:**
- Any task with difficulty ≥7

**Optional breakdown:**
- Tasks estimated >8 hours
- Tasks with unclear requirements (break down for clarity)
- Tasks discovered to be complex during "In Progress"

## The "Broken Down" Status

### What It Means
When a task is marked "Broken Down", it becomes a **container** or **epic**:
- It is NOT a unit of work itself
- It CANNOT be worked on directly
- It tracks progress through its subtasks
- It auto-completes when all subtasks finish

### What You Can Do
- ✅ View its progress in task-overview.md
- ✅ Add notes for context
- ✅ Review its subtasks
- ❌ Cannot change status manually to "Finished"
- ❌ Cannot use complete-task.md on it
- ❌ Cannot add time tracking (track time on subtasks instead)

### Visual Indicators
In task-overview.md, Broken Down tasks show:
- 🔵 icon
- Progress: "Broken Down (X/Y done)"
- Subtasks indented with ↳ symbol
- Links to all subtasks

## Subtask Rules

### Subtask Creation
- Each subtask gets sequential ID (next available number)
- Each subtask has `parent_task` field pointing to original
- Subtasks inherit context but have own difficulty scores (≤6)
- Subtasks can have dependencies on other subtasks
- Subtasks start with status "Pending"

### Subtask Completion
When you finish the LAST subtask:
1. You mark subtask as "Finished" (normal process via complete-task.md)
2. System detects parent is "Broken Down"
3. System checks all sibling subtasks
4. If all siblings "Finished" → parent auto-completes to "Finished"
5. You receive notification: "🎉 Parent Task #{id} automatically completed!"

## Example Workflow

### Initial State

Task 7: "Implement Azure SQL integration" (difficulty: 8, status: Pending)

### Step 1: Break Down
**User:** @.claude/commands/breakdown.md 7

**Claude analyzes the task and proposes:**

I'll break down Task 7 into 4 subtasks:

1. Create connection manager (difficulty: 4)
   - Handle connection pooling
   - Manage credentials securely
   
2. Build bulk insert module (difficulty: 6)
   - Implement batch processing
   - Handle data type mapping
   
3. Add retry logic (difficulty: 4)
   - Exponential backoff
   - Error classification
   
4. Write integration tests (difficulty: 3)
   - Test connection handling
   - Test bulk operations

Proceed with breakdown? (yes/no)

### After Breakdown
Task 7: "Implement Azure SQL integration" 
  - Status: Broken Down 🔵
  - Difficulty: 8 (original preserved)
  - Subtasks: 15, 16, 17, 18
  - Progress shown in overview: "Broken Down (0/4 done)"

Task 15: "Create connection manager" (difficulty: 4, status: Pending, parent: 7)
Task 16: "Build bulk insert module" (difficulty: 6, status: Pending, parent: 7)
Task 17: "Add retry logic" (difficulty: 4, status: Pending, parent: 7, depends on: 15, 16)
Task 18: "Write integration tests" (difficulty: 3, status: Pending, parent: 7, depends on: 15, 16, 17)

### Step 2: Work on Subtasks
User: @.claude/commands/complete-task.md 15  # Start first subtask

**Claude:**
Progress updates:
Task 7: "Broken Down (1/4 done)" after completing Task 15
Task 7: "Broken Down (2/4 done)" after completing Task 16
Task 7: "Broken Down (3/4 done)" after completing Task 17

### Step 3: Complete Last Subtask
@.claude/commands/complete-task.md 18  # Finish last subtask

# Output includes:
✅ Task #18 "Write integration tests" completed!
- Estimated: 2 hours
- Actual: 2.5 hours

🎉 Completing this subtask also completed parent Task #7: "Implement Azure SQL integration"!
All 4 subtasks (15-18) are now finished.

Suggested next task: Task #19 "Configure ETL scheduling" (difficulty: 5)

### Final State
Task 7: Status changed from "Broken Down" to "Finished" (automatic)
  - All subtasks (15-18): Status = "Finished"
  - Notes updated: "Auto-completed: all subtasks finished on 2024-01-16"
  - Total actual hours: Sum of all subtask hours (11 hours)

```





## Benefits of This Approach

1. **No Ambiguity**: Clear distinction between work items (subtasks) and containers (broken down parents)
2. **Accurate Progress**: Easy to see "3 out of 4 subtasks done = 75%" in task-overview.md
3. **Prevents Errors**: Cannot accidentally complete parent with unfinished work
4. **Self-Managing**: Automatic completion reduces manual overhead and prevents inconsistencies
5. **Better Planning**: Difficulty scores reflect actual work complexity per subtask
6. **Lower Risk**: Each subtask has difficulty ≤6, reducing LLM error probability
7. **Clear Dependencies**: Subtask dependencies make work sequence explicit

## Common Questions

**Q: Can I break down a task that's already "In Progress"?** A: Yes! If you discover complexity mid-work, you can break it down. The parent will transition to "Broken Down" and you'll work on the subtasks instead.

**Q: What if I want to undo a breakdown?** A: You cannot directly undo. However, you can mark all subtasks as "Finished" individually (if the work is done), or delete the subtasks and reset the parent to "Pending" (if you made a mistake).

**Q: Can subtasks be broken down further?** A: No. The system only supports one level of hierarchy (parent → subtasks). If a subtask seems too complex, increase its difficulty score but keep it ≤6. If it's genuinely >6, consider redesigning the parent's breakdown.

**Q: How do I track time for a "Broken Down" task?** A: Don't track time on the parent. Track actual_hours on each subtask. The parent's total effort is the sum of all subtask hours.

**Q: What happens if I try to use complete-task.md on a "Broken Down" task?** A: The command will halt with an error: "❌ Task {id} has been broken down into subtasks {list}. Please work on the individual subtasks instead."

------

## Initialization Questions

When creating a new environment, Claude Code should ask:

### Essential Questions

1. **What are you building?** (project description)
2. **What type of project?** (coding/planning/analysis/other)
3. **What's your timeline?** (deadline/ongoing/exploratory)

### Technical Questions (if applicable)

1. **Technology stack?** (languages/frameworks/tools)
2. **Existing systems?** (integrations/dependencies)
3. **Team size?** (solo/collaborative)

### Context Questions

1. **Success criteria?** (how you'll know it's working)
2. **Constraints?** (budget/technical/organizational)
3. **Prior work?** (existing code/documentation)

------

## Post-Generation Instructions

After creating the environment, Claude Code should provide this guidance to the user:

"✅ **Environment created successfully!**

Here's what I've set up for you:
- Project structure in [describe what was created]
- [X] initial tasks with difficulty scoring
- [Y] command files for common workflows
- Hierarchical task management with automatic parent completion

**Next steps to start working:**

1. **Verify understanding**: Review `.claude/context/overview.md` - does it match your vision?
   
2. **Check task health**: Run `@.claude/commands/update-tasks.md` to validate task structure
   - This will flag any inconsistencies between JSON files and overview
   - Ensures all tasks are properly formatted and relevant
   - Confirms parent-child relationships are valid
   - Confirms system is ready for work

3. **Handle high-difficulty tasks**: Look for 🔴 markers in task-overview.md
   - These indicate tasks with difficulty ≥7 that need breakdown
   - Run `@.claude/commands/breakdown.md [task-id]` for each
   - Parent will automatically become "Broken Down" and cannot be worked on directly
   - Work on the created subtasks instead

4. **Start your first task**: Use `@.claude/commands/complete-task.md [task-id]`
   - **Always use this command to start task work** - it ensures proper status tracking
   - I'll ask for confirmation before starting
   - Status will automatically update from Pending → In Progress → Finished
   - If you complete the last subtask of a broken down parent, the parent auto-completes!
   - You'll get feedback on completion with next task suggestions

5. **Monitor progress**: Check `.claude/tasks/task-overview.md` anytime
   - 🔴 markers indicate tasks needing breakdown
   - 🔵 markers show "Broken Down" tasks with subtask progress (X/Y done)
   - Status updates happen automatically when using complete-task.md and breakdown.md
   - Subtasks are indented with ↳ symbol under their parent
   
6. **Maintain task system**: Run `@.claude/commands/update-tasks.md` periodically
   - Validates task structure and consistency
   - Checks parent-child relationships
   - Flags outdated or irrelevant tasks
   - Keeps task-overview.md synchronized

**Hierarchical Task Management:**

- Tasks ≥7 difficulty are automatically managed as containers
- Parent tasks show progress through their subtasks
- Parents auto-complete when all subtasks finish
- See `.claude/reference/breakdown-workflow.md` for complete guide

**Ready to begin?** Run `@.claude/commands/complete-task.md` with a task ID to start!"

------

## Usage Example

### User Input:

"I need to build an ETL pipeline that pulls carbon emissions data from various APIs, processes it with Polars, and loads it into Azure SQL Database. It needs to run daily and feed a Power BI dashboard."

### Claude Code Response:

"I'll help you set up a data engineering environment for your carbon emissions ETL pipeline. Let me ask a few clarifying questions:

1. **Data Sources**: Which specific APIs will you be pulling from?
2. **Data Volume**: Approximate daily data size?
3. **Error Handling**: How critical is this pipeline? Need alerting?
4. **Authentication**: Do you have Azure credentials set up?
5. **Testing**: Do you need automated tests?

Based on your answers, I'll create a customized environment with:

- Python/Polars code templates
- Azure SQL connection patterns
- Power BI integration setup
- Daily scheduling configuration
- Appropriate testing structure
- Hierarchical task breakdown for complex components"

### Generated Structure with Task Management:
```
carbon-emissions-etl/ └── .claude/ ├── tasks/ │ ├── task-overview.md │ ├── task-1.json # "Setup project structure" (difficulty: 3) │ ├── task-2.json # "Configure API connections" (difficulty: 8) 🔴 │ ├── task-3.json # "Build Polars pipeline" (difficulty: 7) 🔴 │ ├── task-4.json # "Implement Azure SQL loader" (difficulty: 7) 🔴 │ └── task-5.json # "Create scheduling system" (difficulty: 5) └── commands/ └── breakdown.md
```

### Task Breakdown Example:

After running `@.claude/commands/breakdown.md 2`, the high-difficulty task is split:

**Task 2: "Configure API connections" (8) becomes:**

Status: "Broken Down (0/5 done)" 🔵

Subtasks created:
- Task 6: "Create API client base class" (4, parent: 2)
- Task 7: "Implement EPA API connector" (5, parent: 2, depends on: 6)
- Task 8: "Implement EU emissions API connector" (5, parent: 2, depends on: 6)
- Task 9: "Add retry logic and error handling" (4, parent: 2, depends on: 7,8)
- Task 10: "Create API response validators" (3, parent: 2, depends on: 9)

**Task 4: "Implement Azure SQL loader" (7) becomes:**

Status: "Broken Down (0/5 done)" 🔵

Subtasks created:
- Task 11: "Set up connection string management" (3, parent: 4)
- Task 12: "Create database schema" (4, parent: 4, depends on: 11)
- Task 13: "Implement bulk insert logic" (5, parent: 4, depends on: 12)
- Task 14: "Add transaction handling" (4, parent: 4, depends on: 13)
- Task 15: "Create connection pool" (3, parent: 4, depends on: 13)

**Result**: Maximum task difficulty reduced from 8 to 5, significantly lowering error risk. Parent tasks automatically complete when all subtasks are finished.

-----



## Tool Routing & Model Selection

### When to Use Gemini API

**Research & Current Information**
- Current events, recent news, up-to-date statistics
- Regulatory changes, legal updates
- Market trends, financial data
- **Model:** `gemini-2.5-pro` with `grounding: true` (enables Google Search)
- **Tool:** `mcp__gemini__generate_text`

**Domain Knowledge & Analysis**

- Industry regulations and compliance interpretation
- Business domain expertise (sustainability, finance, healthcare)
- Data pattern analysis and statistical insights
- Document analysis and summarization (reports, papers, specifications)
- **Model:** `gemini-2.5-pro` with `grounding: true` for factual accuracy
- **Tool:** `mcp__gemini__generate_text`

**Content Generation**
- Blog posts, articles, technical documentation
- Marketing copy, product descriptions
- Executive summaries, one-pagers
- **Model:**  `gemini-2.5-pro`
- **Tool:** `mcp__gemini__generate_text`

**Image Analysis**
- Chart/graph interpretation from screenshots
- Dashboard design review
- Visual data extraction
- **Model:** `gemini-2.5-pro`
- **Tool:** `mcp__gemini__analyze_image`

**Code Review & Explanation**
- Algorithm explanation and complexity analysis
- Architecture pattern review
- Best practices validation
- **Model:** `gemini-2.5-pro`
- **Tool:** `mcp__gemini__generate_text`

### When to Use Claude's Native Capabilities

**Code Implementation & Editing**

- Writing Python, SQL, DAX, M, JavaScript
- Refactoring and optimization
- Debugging and error fixing
- File system operations

**System Architecture & Design**

- ETL pipeline design
- Database schema modeling
- Power BI data model architecture
- Integration patterns

**Project Management**

- Task breakdown and estimation
- Command execution
- File structure organization
- Status tracking and reporting

### Hybrid Workflows

For complex tasks requiring both models:

1. **Analysis → Implementation**
   - Gemini: Research regulations, analyze requirements, review documentation
   - Claude: Implement solution, create code, build artifacts

2. **Review → Refactor**
   - Gemini: Code review feedback, identify anti-patterns
   - Claude: Apply refactoring, update implementation

3. **Research → Design**
   - Gemini: Market analysis, competitive research
   - Claude: System design, technical architecture

### Usage Guidelines

**When calling Gemini:**
- Always inform the user which model you're using and why
- Use `grounding: true` for factual queries requiring current information
- Present results clearly with proper citations if search was used
- Fall back to Claude if Gemini encounters errors
- For sustainability/data analytics (your domain), prefer `gemini-2.5-pro` with grounding

**Model Selection Quick Reference:**
- **gemini-2.5-flash**: Speed-critical tasks, simple queries, image analysis
- **gemini-2.5-pro**: Complex analysis, accuracy-critical work, code review
- **Add grounding: true**: When current/factual information is needed

**Example Command Usage:**
```markdown
For current EU emissions regulations:
@gemini (model: gemini-2.5-pro, grounding: true)

For analyzing a Power BI dashboard screenshot:
@gemini analyze_image (model: gemini-2.5-flash)
```

-----

## Best Practices

1. **Start Simple**: Use base template, add complexity as needed
2. **Keep Context Focused**: Only load what's relevant to current task
3. **Document Decisions**: Capture "why" in reference files
4. **Update Regularly**: Keep tasks and context current
5. **Use Command Templates**: Create command files for repetitive instruction patterns
6. **Separate Concerns**: AI context vs human documentation

### Task Management Best Practices

1. **Always Use complete-task.md**: Start all task work with this command - manual status updates lead to inconsistencies
2. **Break Down Complexity Early**: Split tasks ≥7 difficulty using breakdown.md before starting work
3. **Trust the Automation**: Let parent tasks auto-complete; don't manually change status
4. **Work Bottom-Up**: Always work on subtasks, never on "Broken Down" parents
5. **Validate Regularly**: Run update-tasks.md before major work sessions to catch parent-child inconsistencies
6. **Sequential IDs**: Never skip task numbers (1, 2, 3... not 1, 3, 5)
7. **Track Hours on Subtasks**: Don't track time on parent tasks; sum subtask hours for total
8. **Clear Blockers**: Document specific blockers, not vague issues
9. **Shallow Dependencies**: Keep dependency depth shallow (max 2-3 levels)
10. **Review Breakdown**: Read `.claude/reference/breakdown-workflow.md` to understand the hierarchical system

### Common Pitfalls to Avoid

❌ **Don't**: Manually set parent task to "Finished"
✅ **Do**: Let it auto-complete when subtasks finish

❌ **Don't**: Try to work on a "Broken Down" task
✅ **Do**: Work on its subtasks instead

❌ **Don't**: Create subtasks with difficulty >6
✅ **Do**: Keep all subtasks at moderate complexity or below

❌ **Don't**: Nest subtasks (subtask of subtask)
✅ **Do**: Keep hierarchy flat (one level only)

❌ **Don't**: Break down tasks with difficulty <7
✅ **Do**: Only break down high-risk tasks (≥7)



## Notes

- This template is intentionally flexible - adapt as needed
- Command files provide reusable instruction templates for consistent workflows
- Reference files can include external links and resources
- Task hierarchy is limited to one level (parent → subtasks, no further nesting)
- "Broken Down" status is automatic; don't try to manage it manually
- Consider adding `.claude/logs/` for debugging complex projects