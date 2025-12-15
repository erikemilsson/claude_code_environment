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