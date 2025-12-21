# Sync Tasks Command

## Purpose
Update `task-overview.md` to reflect current state of all task JSON files, including belief tracking metrics, momentum phases, confidence levels, and visual health indicators.

## Process

### 1. Data Collection
**Scan all task files** in `.claude/tasks/`
- Read each `task-*.json` file
- Validate JSON structure
- Extract all fields including belief tracking data

### 2. Metric Calculation

#### Task Information
- ID, title, status, difficulty
- Parent/subtask relationships
- Dependencies and blockers
- Files affected

#### Belief Tracking Metrics
- **Confidence scores**: Average, distribution, trends
- **Momentum phases**: Current phase distribution
- **Assumption validation**: Rates and status
- **Risk indicators**: Critical, moderate, low counts
- **Decision tracking**: Recent decisions impact

### 3. Generate Enhanced Overview

#### Header Section
```markdown
# Task Overview
*Generated: [timestamp]*
*Total Tasks: X | Active: Y | Completed: Z*

## Project Health Summary
**Overall Confidence:** [█████░░░] 75%
**Momentum:** Building ▓ | **Validation Rate:** 85% ✓
**Risk Level:** 🟡 Moderate (2 critical, 5 moderate)
```

#### Main Task Table
Include columns:
- ID (with visual status indicator)
- Title (with confidence badge)
- Status (with momentum symbol)
- Difficulty
- Dependencies
- Subtasks
- Health (composite indicator)

Example row:
```
| ✓ 61 | [85%] Enhanced Task Schema | Finished • | 6 | [] | [] | 🟢 |
```

#### Status Indicators Legend
```
Status Symbols:
✓ = Finished | ⚡ = In Progress | ⏸ = Pending | 🚫 = Blocked | 📦 = Broken Down

Momentum Phases:
█ = Initiating | ▓ = Building | ░ = Cruising | ○ = Declining | • = Stalled

Health Indicators:
🟢 = Good | 🟡 = Moderate | 🔴 = Critical | ⚪ = Unknown
```

### 4. Statistics Sections

#### Task Distribution
```markdown
### Task Status Distribution
Pending:     [████░░░░░░] 40% (10 tasks)
In Progress: [██░░░░░░░░] 20% (5 tasks)
Finished:    [██████░░░░] 60% (15 tasks)
```

#### Confidence Analysis
```markdown
### Confidence Levels
High (90-100%):    [████░░] 4 tasks
Good (75-89%):     [██████] 6 tasks
Moderate (50-74%): [████░░] 4 tasks
Low (<50%):        [██░░░░] 2 tasks
Average: 72.5%
```

#### Momentum Tracking
```markdown
### Momentum Phases
Initiating: 2 tasks █
Building:   5 tasks ▓▓▓▓▓
Cruising:   8 tasks ░░░░░░░░
Declining:  1 task  ○
Stalled:    0 tasks
```

#### Risk Summary
```markdown
### Risk Analysis
🔴 Critical Risks: 2
- Task 42: Database migration (Impact: 9, Likelihood: 0.8)
- Task 55: Authentication system (Impact: 8, Likelihood: 0.7)

🟡 Moderate Risks: 5
- [List top moderate risks]

🟢 Low Risks: 10
```

### 5. Assumption Validation Summary
```markdown
### Assumption Status
✓ Validated:     [██████░░] 60% (12 assumptions)
⚠ Needs Check:   [████░░░░] 25% (5 assumptions)
✗ Invalidated:   [█░░░░░░░] 10% (2 assumptions)
? Pending:       [█░░░░░░░] 5% (1 assumption)

Key Assumptions at Risk:
1. [assumption description] - Task 23
2. [assumption description] - Task 45
```

### 6. Pattern Insights
```markdown
### Detected Patterns
- **Velocity Trend:** ↗ Increasing (avg 2.5 days/task → 1.8 days/task)
- **Confidence Trend:** ↘ Slight decline (78% → 72.5%)
- **Common Blockers:** External dependencies (40%), Missing specs (30%)
- **Success Patterns:** Breaking down high-difficulty tasks improves completion rate by 65%
```

### 7. Recent Activity
```markdown
### Recent Updates (Last 7 days)
- 2025-12-15: Task 75 completed (Project Health Dashboard)
- 2025-12-14: Task 67 moved to Building phase
- 2025-12-13: Critical risk identified in Task 42
```

### 8. Hierarchical View
Show parent-child relationships with indentation and progress:
```markdown
### Task Hierarchy
60. Belief Tracker System [Broken Down - 85% complete]
    ├─ 61. Enhanced Task Schema [Finished ✓]
    ├─ 62. Confidence Scoring [Finished ✓]
    ├─ 75. Project Health Dashboard [Finished ✓]
    └─ 77. Test Integration [Pending ⏸]
```

## Context-Aware Next Steps

After syncing tasks, provide smart suggestions based on project state:

### Analysis Logic

After generating the overview, analyze current state to suggest next actions:

**If critical risks detected:**
```
✓ Task overview updated

⚠️  CRITICAL RISKS DETECTED ([N] tasks)
High-impact tasks need attention:

📋 PRIORITY ACTION:
   → Task [ID]: [Title] (Impact: [N]/10, Likelihood: [N]%)
   → Run: /check-risks [task-id] to analyze mitigation strategies
   → Or: Address risk before proceeding with task
```

**If high-difficulty tasks need breakdown (≥7):**
```
✓ Task overview updated

⚠️  COMPLEX TASKS REQUIRE BREAKDOWN
[N] pending tasks with difficulty ≥7 detected

📋 NEXT STEP (break down before starting):
   → Task [ID]: [Title] (difficulty: [N])
   → Run: /breakdown [task-id]

   Repository rules require breakdown for difficulty ≥7
```

**If tasks are blocked:**
```
✓ Task overview updated

🚫 BLOCKED TASKS: [N] tasks cannot proceed

📋 NEXT STEP (resolve blockers):
   → Task [ID]: [Title]
   → Blocker: [Blocker description]
   → Action: [Suggested resolution]
```

**If confidence declining (trend analysis):**
```
✓ Task overview updated

📉 CONFIDENCE TREND DECLINING
Average confidence: [X]% (down from [Y]%)

📋 SUGGESTED ACTION:
   → Run: /validate-assumptions to review pending assumptions
   → [N] assumptions need validation
   → Or: Review low-confidence tasks for clarity improvements
```

**If momentum stalled:**
```
✓ Task overview updated

⚠️  MOMENTUM STALLED: [N] tasks in declining/stalled phase

📋 NEXT STEP (restart momentum):
   → Review stalled tasks for blockers
   → Consider switching to easier tasks (difficulty ≤4) to build momentum
   → Suggested: Task [ID] - [Title] (difficulty: [N])
```

**If all systems healthy and work ready:**
```
✓ Task overview updated

✅ PROJECT HEALTH: [Status] | [X]/[Total] tasks complete ([%]%)

📋 NEXT STEP (continue work):
   → Suggested: Task [ID] - [Title]
   → Reason: [Why this task - e.g., "High priority, unblocks 3 tasks"]
   → Run: /complete-task [id]

   Other options:
   - [N] pending tasks available
   - [N] high-priority tasks
   - Review: .claude/tasks/task-overview.md
```

**If project complete:**
```
✓ Task overview updated

🎉 ALL TASKS COMPLETE!
[Total] tasks finished. No pending or blocked tasks.

📋 NEXT STEPS (project completion):
   □ Review deliverables and outcomes
   □ Run final validation tests
   □ Update documentation
   □ Create completion report
   □ Archive/tag repository
```

**If Phase 0 tasks detected but not complete:**
```
✓ Task overview updated

⏳ PHASE 0 IN PROGRESS
Initialization tasks must complete before implementation

📋 NEXT STEP (complete Phase 0):
   → Task [ID]: [Phase 0 step]
   → Run: /complete-task [id]
   → Phase 0 progress: [X]/[Y] steps complete
   → Estimated time remaining: [N] minutes
```

### Suggestion Priority Rules
When choosing which suggestion to show (if multiple apply):
1. **Critical risks** - Highest priority, show first
2. **Blocked tasks** - Must resolve before progress
3. **High-difficulty needs breakdown** - Required before work
4. **Phase 0 incomplete** - Must finish before implementation
5. **Momentum/confidence issues** - Process health concerns
6. **Standard continuation** - Normal work flow
7. **Project complete** - All done

## Output Location
`.claude/tasks/task-overview.md`

## Command Options
- `--minimal`: Basic table without metrics
- `--verbose`: Include all belief tracking details
- `--json`: Output raw data as JSON
- `--health-only`: Focus on health metrics
- `--hierarchy`: Show only hierarchical view

## When to Use
- After creating/updating any task file
- Before starting work session (to see current state)
- After completing tasks
- When task relationships change
- After updating belief tracking data
- Before project reviews or reports

## Integration
- Automatically called by `complete-task` command
- Triggers dashboard refresh if metrics change significantly
- Updates pattern detection cache
- Can trigger alerts for critical changes

## Performance Notes
- Cache calculations for 5 minutes
- Process tasks incrementally when possible
- Use parallel processing for large task sets
- Skip visualization calculations for JSON output