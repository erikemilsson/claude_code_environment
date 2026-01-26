# Project Health Dashboard

## Overview
This dashboard provides real-time insights into project health through belief tracking metrics, task momentum analysis, and risk indicators.

## Dashboard Components

### 1. Task Momentum Overview
```
============ MOMENTUM PHASES ============
█ Initiating    ▓ Building    ░ Cruising    ○ Declining    • Stalled
```

**Current Distribution:**
- Initiating: 0 tasks
- Building: 0 tasks
- Cruising: 0 tasks
- Declining: 0 tasks
- Stalled: 0 tasks

### 2. Confidence Metrics
```
HIGH CONFIDENCE (90-100%)  [████████░░] 0%
GOOD CONFIDENCE (75-89%)   [████████░░] 0%
MODERATE (50-74%)          [████████░░] 0%
LOW CONFIDENCE (<50%)      [████████░░] 0%
```

**Average Project Confidence:** N/A

### 3. Assumption Validation Status
```
✓ VALIDATED     [████████░░] 0%
⚠ NEEDS CHECK   [████████░░] 0%
✗ INVALIDATED   [████████░░] 0%
? PENDING       [████████░░] 0%
```

**Key Assumptions at Risk:**
- None currently identified

### 4. Risk Indicators
```
🔴 Critical Risks: 0
🟡 Moderate Risks: 0
🟢 Low Risks: 0
```

**Top Risk Areas:**
1. None currently identified
2. None currently identified
3. None currently identified

### 5. Pattern Insights
```
=============== DETECTED PATTERNS ===============
```

**Velocity Trends:**
- Average task completion time: N/A
- Momentum shift patterns: None detected
- Bottleneck areas: None identified

**Quality Indicators:**
- Assumption validation rate: N/A
- Confidence improvement over time: N/A
- Decision reversal frequency: N/A

### 6. Task Status Summary
```
PENDING     [████████░░] 0 tasks
IN PROGRESS [████████░░] 0 tasks
BLOCKED     [████████░░] 0 tasks
FINISHED    [████████░░] 0 tasks
BROKEN DOWN [████████░░] 0 tasks
```

### 7. Health Score
```
PROJECT HEALTH: [?????]
├─ Task Momentum:    [?]
├─ Confidence Level: [?]
├─ Assumption Valid: [?]
├─ Risk Management:  [?]
└─ Pattern Stability:[?]

Overall: UNKNOWN (No data)
```

## Dashboard Refresh Commands
- `show-dashboard` - Display current project health
- `refresh-metrics` - Update all metrics from task data
- `analyze-trends` - Generate pattern insights

## Alert Thresholds
- **Critical Alert:** Average confidence < 50%
- **Warning Alert:** > 30% tasks stalled
- **Risk Alert:** > 3 critical risks identified
- **Pattern Alert:** Declining momentum in > 50% active tasks

## Data Sources
- Task files: `.claude/tasks/task-*.json`
- Decision log: `.claude/decisions/decision-log.md`
- Assumption tracker: `.claude/validation/assumption-tracker.md`
- Pattern analysis: `.claude/insights/patterns.md`

## Visualization Legend
```
Progress Bars:
[████████░░] - Filled portion represents percentage
█ - Complete/Active
▓ - Partial/Building
░ - Empty/Pending
○ - Declining/Warning
• - Stalled/Critical

Status Indicators:
✓ - Validated/Complete
⚠ - Warning/Needs Attention
✗ - Failed/Invalidated
? - Unknown/Pending
🔴 - Critical
🟡 - Moderate
🟢 - Good/Low Risk
```

## Update Frequency
- Real-time: Task status changes
- Hourly: Momentum calculations
- Daily: Pattern analysis
- Weekly: Trend insights

---
*Dashboard generated: 2025-12-15*
*Next refresh: On demand*