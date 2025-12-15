# Check Risks Command

## Purpose
Scan all tasks for risk indicators and generate alerts for tasks requiring intervention.

## Context Required
- Task files with belief tracking fields
- Risk indicator definitions
- Intervention thresholds

## Process

### 1. Load and Analyze Tasks

```python
def check_all_task_risks():
    risks = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': []
    }

    for task in load_all_tasks():
        risk_level = assess_task_risk(task)
        if risk_level != 'none':
            risks[risk_level].append({
                'task': task,
                'indicators': identify_risk_indicators(task),
                'recommendations': generate_recommendations(task)
            })

    return risks
```

### 2. Risk Assessment Criteria

#### Momentum Risk Assessment
```python
def assess_momentum_risk(task):
    if task.status == "In Progress":
        if task.momentum.velocity == 0:
            return 'critical', 'Task completely stopped'
        elif task.momentum.velocity < 10:
            return 'high', 'Task nearly stopped'
        elif task.momentum.phase == 'stalling':
            return 'high', 'Task is stalling'
        elif task.momentum.velocity < 30:
            return 'medium', 'Task momentum low'

    # Check trend
    if velocity_declining(task, days=3):
        return 'medium', 'Velocity declining trend'

    return 'none', ''
```

#### Confidence Risk Assessment
```python
def assess_confidence_risk(task):
    confidence = task.get('confidence', 75)

    if confidence < 25:
        return 'critical', f'Extreme uncertainty ({confidence}%)'
    elif confidence < 50:
        return 'high', f'Low confidence ({confidence}%)'
    elif confidence < 60 and task.status == "In Progress":
        return 'medium', f'Moderate uncertainty ({confidence}%)'

    # Check trend
    if confidence_dropped(task, amount=30, days=3):
        return 'high', 'Rapid confidence decline'

    return 'none', ''
```

#### Assumption Risk Assessment
```python
def assess_assumption_risk(task):
    if not task.get('assumptions'):
        return 'none', ''

    critical_invalid = [a for a in task.assumptions
                       if a.impact == 'critical' and a.status == 'invalidated']
    high_invalid = [a for a in task.assumptions
                   if a.impact == 'high' and a.status == 'invalidated']
    pending = [a for a in task.assumptions if a.status == 'pending']

    if critical_invalid:
        return 'critical', f'{len(critical_invalid)} critical assumptions invalidated'
    elif high_invalid:
        return 'high', f'{len(high_invalid)} high-impact assumptions invalidated'
    elif len(pending) > 5:
        return 'medium', f'{len(pending)} assumptions unvalidated'

    return 'none', ''
```

#### Timeline Risk Assessment
```python
def assess_timeline_risk(task):
    if task.status != "In Progress":
        return 'none', ''

    # Check for staleness
    last_activity = parse_date(task.momentum.last_activity)
    days_inactive = (today - last_activity).days

    if days_inactive > 14:
        return 'critical', f'No activity for {days_inactive} days'
    elif days_inactive > 7:
        return 'high', f'Inactive for {days_inactive} days'
    elif days_inactive > 3:
        return 'medium', f'No recent activity ({days_inactive} days)'

    return 'none', ''
```

### 3. Composite Risk Calculation

```python
def calculate_composite_risk(task):
    risk_assessments = [
        assess_momentum_risk(task),
        assess_confidence_risk(task),
        assess_assumption_risk(task),
        assess_timeline_risk(task),
        assess_dependency_risk(task),
        assess_quality_risk(task)
    ]

    # Take highest risk level found
    risk_levels = ['critical', 'high', 'medium', 'low', 'none']
    for level in risk_levels:
        if any(r[0] == level for r in risk_assessments):
            indicators = [r[1] for r in risk_assessments if r[1]]
            return level, indicators

    return 'none', []
```

### 4. Generate Risk Report

```markdown
# Task Risk Alert Report
Generated: [timestamp]

## 🔴 CRITICAL RISKS (Immediate Action Required)
[List of critical risk tasks with details]

## 🟠 HIGH RISKS (Same Day Action Required)
[List of high risk tasks with details]

## 🟡 MEDIUM RISKS (Next Day Review)
[List of medium risk tasks with details]

## 🟢 LOW RISKS (Monitor)
[List of low risk tasks with details]

## Summary Statistics
- Total Tasks Analyzed: X
- Tasks at Risk: Y
- Critical/High Risks: Z

## Recommended Actions
[Prioritized intervention list]
```

### 5. Risk Alert Format

For each at-risk task, generate:

```markdown
### Task [ID]: [Title]
**Risk Level**: [Critical/High/Medium/Low]
**Status**: [Current Status]
**Momentum**: Phase=[phase], Velocity=[velocity]
**Confidence**: [confidence]%

**Risk Indicators**:
- [Indicator 1]
- [Indicator 2]
- [Indicator 3]

**Recommended Actions**:
1. [Primary action]
2. [Secondary action]
3. [Follow-up action]

**Intervention Priority**: [Immediate/Today/Tomorrow/This Week]
```

### 6. Intervention Recommendations

```python
def generate_recommendations(task, risk_level, indicators):
    recommendations = []

    # Critical risks
    if risk_level == 'critical':
        if 'stopped' in str(indicators):
            recommendations.append('Immediate intervention meeting required')
            recommendations.append('Identify and remove all blockers')
            recommendations.append('Consider task reassignment')
        elif 'assumption' in str(indicators):
            recommendations.append('Stop work and reassess approach')
            recommendations.append('Execute fallback plan immediately')
            recommendations.append('Update all dependent tasks')

    # High risks
    elif risk_level == 'high':
        if 'stalling' in str(indicators):
            recommendations.append('Schedule intervention today')
            recommendations.append('Identify root cause of stalling')
            recommendations.append('Apply momentum boost strategy')
        elif 'confidence' in str(indicators):
            recommendations.append('Clarify requirements and approach')
            recommendations.append('Validate key assumptions')
            recommendations.append('Consider breaking down task')

    # Medium risks
    elif risk_level == 'medium':
        if 'declining' in str(indicators):
            recommendations.append('Check in with task owner')
            recommendations.append('Review blockers and dependencies')
            recommendations.append('Adjust approach if needed')
        elif 'inactive' in str(indicators):
            recommendations.append('Confirm task is still relevant')
            recommendations.append('Re-energize with clear next steps')
            recommendations.append('Set near-term milestone')

    return recommendations
```

## Output Location
- Risk report: `.claude/reports/risk-alert-YYYY-MM-DD.md`
- Console output: Summary and critical alerts
- Task updates: Risk level added to task notes

## Command Usage

### Check All Tasks
```bash
check-risks --all
```

### Check Specific Task
```bash
check-risks --task 42
```

### Check by Status
```bash
check-risks --status "In Progress"
```

### Check with Threshold
```bash
check-risks --min-level high
```

### Continuous Monitoring
```bash
check-risks --watch --interval 3600
```

## Integration Points

### With Momentum Tracker
```python
from momentum_tracker import MomentumTracker

tracker = MomentumTracker()
for task_id in at_risk_tasks:
    velocity = tracker.calculate_velocity(task)
    risks = tracker.detect_momentum_risks(task)
    # Include in risk assessment
```

### With Assumption Validator
```python
from validate_assumptions import validate_task_assumptions

for task in at_risk_tasks:
    if has_pending_assumptions(task):
        validation_priority = 'high' if risk_level >= 'high' else 'normal'
        schedule_validation(task, priority=validation_priority)
```

### With Complete Task Command
When completing tasks, check for risk impacts:
- Completing task may reduce risk for dependents
- Failed completion may increase risk for dependents
- Update risk assessments after status changes

## Alert Distribution

### Console Output (Immediate)
```
🔴 CRITICAL ALERT: Task 42 has stopped completely
   - Velocity: 0
   - Last activity: 10 days ago
   - Action required: Immediate intervention

🟠 HIGH ALERT: Task 43 is stalling
   - Velocity: 8 (declining)
   - Confidence: 35%
   - Action required: Intervention today
```

### Report File (Detailed)
Full risk assessment saved to `.claude/reports/` with:
- Complete risk analysis
- Historical trends
- Intervention recommendations
- Success metrics

### Task Updates (Persistent)
Add risk indicators to task JSON:
```json
{
  "risk_assessment": {
    "level": "high",
    "indicators": ["stalling", "low confidence"],
    "last_checked": "2025-12-15",
    "recommendations": ["intervention meeting", "clarify requirements"]
  }
}
```

## Automation Rules

### Scheduled Checks
```yaml
schedule:
  continuous:
    - Critical tasks: Every hour
    - Active tasks: Every 4 hours
  daily:
    - All "In Progress": Morning check
    - Previously at-risk: Follow-up check
  weekly:
    - Full portfolio: Comprehensive scan
```

### Trigger-Based Checks
Run risk check when:
- Task status changes
- Confidence drops >20 points
- Assumption invalidated
- Velocity drops >30 points
- Task blocked
- Dependency delayed

## Success Metrics

Track effectiveness of risk management:

```python
risk_metrics = {
    'early_detection_rate': risks_caught_early / total_risks,
    'intervention_success': risks_resolved / risks_identified,
    'false_positive_rate': false_alarms / total_alerts,
    'mean_time_to_resolve': average(resolution_times),
    'escalation_effectiveness': resolved_after_escalation / escalated
}
```

## Critical Rules

- **Never Ignore Critical**: Always act on critical risks immediately
- **Document Interventions**: Record what was done and why
- **Learn from Patterns**: Track recurring risks for process improvement
- **Prevent > Correct**: Focus on early detection
- **Communicate Clearly**: Ensure alerts reach the right people

## Quick Reference

### Risk Level Actions
- 🔴 **Critical**: Stop, escalate, intervene immediately
- 🟠 **High**: Address today, may escalate
- 🟡 **Medium**: Plan intervention, monitor closely
- 🟢 **Low**: Track trends, address if convenient

### Common Risk Patterns
1. **Momentum Loss**: Velocity < 20 → Intervention
2. **Confidence Crisis**: Confidence < 50 → Clarification
3. **Assumption Failure**: Invalid critical → Pivot
4. **Time Pressure**: Behind schedule → Resource adjustment
5. **Quality Degradation**: Validation failures → Review standards