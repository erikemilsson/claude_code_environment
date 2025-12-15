# Task Risk Indicators Reference

## Overview

Risk indicators are early warning signals that a task may fail, stall, or require intervention. This reference defines risk levels, detection criteria, and response protocols.

## Risk Levels

### Critical Risk (🔴)
**Definition**: Immediate threat to project success
**Response Time**: Immediate (< 1 hour)
**Escalation**: Always escalate

### High Risk (🟠)
**Definition**: Significant threat requiring urgent attention
**Response Time**: Same day (< 4 hours)
**Escalation**: Escalate if not resolved quickly

### Medium Risk (🟡)
**Definition**: Potential issues that need monitoring
**Response Time**: Next day (< 24 hours)
**Escalation**: Escalate if becomes pattern

### Low Risk (🟢)
**Definition**: Minor concerns for awareness
**Response Time**: Next review cycle
**Escalation**: Document only

## Risk Categories

### 1. Momentum Risks

#### Velocity Indicators
```python
velocity_risk_matrix = {
    'critical': velocity == 0 and status == "In Progress",
    'high': velocity < 10 and status == "In Progress",
    'medium': velocity < 30 and declining_trend,
    'low': velocity < 50
}
```

| Indicator | Condition | Risk Level | Intervention |
|-----------|-----------|------------|--------------|
| Dead Stop | Velocity = 0, Active task | 🔴 Critical | Immediate unblocking |
| Near Stop | Velocity < 10 | 🟠 High | Same-day intervention |
| Stalling | Velocity < 20 | 🟡 Medium | Next-day check-in |
| Slowing | Velocity declining 3+ days | 🟡 Medium | Review approach |

#### Phase Indicators
```python
phase_risk_matrix = {
    'critical': phase == "stopped" and status == "In Progress",
    'high': phase == "stalling",
    'medium': phase == "coasting" and velocity_declining,
    'low': phase == "ignition" and days_in_phase > 5
}
```

### 2. Confidence Risks

#### Confidence Thresholds
| Confidence | Risk Level | Indicator | Action Required |
|------------|------------|-----------|-----------------|
| 0-24 | 🔴 Critical | Extreme uncertainty | Pause and reassess |
| 25-49 | 🟠 High | Significant doubt | Research/validate |
| 50-74 | 🟡 Medium | Moderate uncertainty | Monitor closely |
| 75-100 | 🟢 Low | Normal confidence | Standard process |

#### Confidence Decline Patterns
```python
def assess_confidence_risk(task):
    if confidence_dropped(task, amount=30, days=3):
        return "high"
    elif confidence_dropped(task, amount=20, days=7):
        return "medium"
    elif confidence < initial_confidence * 0.6:
        return "medium"
    return "low"
```

### 3. Assumption Risks

#### Assumption Status Matrix
```python
assumption_risk_levels = {
    'critical': {
        'condition': 'critical assumption invalidated',
        'indicator': '🔴 Project viability threatened',
        'action': 'Stop work, reassess approach'
    },
    'high': {
        'condition': 'high impact assumption invalidated',
        'indicator': '🟠 Major rework likely',
        'action': 'Execute fallback plan'
    },
    'medium': {
        'condition': 'multiple assumptions pending validation',
        'indicator': '🟡 Uncertainty accumulating',
        'action': 'Prioritize validation'
    },
    'low': {
        'condition': 'low impact assumptions unvalidated',
        'indicator': '🟢 Minor adjustments possible',
        'action': 'Validate when convenient'
    }
}
```

#### Invalidation Impact
| Impact | Invalidations | Risk Level | Response |
|--------|---------------|------------|----------|
| Critical | Any | 🔴 Critical | Immediate pivot |
| High | 1+ | 🟠 High | Activate fallback |
| Medium | 2+ | 🟡 Medium | Adjust approach |
| Low | 3+ | 🟢 Low | Document changes |

### 4. Dependency Risks

#### Dependency Patterns
```python
dependency_risks = {
    'circular': {
        'level': 'critical',
        'indicator': 'Tasks depend on each other',
        'action': 'Restructure immediately'
    },
    'blocked_chain': {
        'level': 'high',
        'indicator': 'Multiple tasks waiting on one',
        'action': 'Prioritize blocking task'
    },
    'deep_chain': {
        'level': 'medium',
        'indicator': 'Dependency depth > 3',
        'action': 'Consider parallelization'
    },
    'external': {
        'level': 'medium',
        'indicator': 'Depends on external team/system',
        'action': 'Establish communication'
    }
}
```

### 5. Timeline Risks

#### Schedule Indicators
| Indicator | Condition | Risk Level | Action |
|-----------|-----------|------------|--------|
| Overdue | Past deadline | 🔴 Critical | Immediate escalation |
| At Risk | <20% time left, <50% complete | 🟠 High | Resource reallocation |
| Behind | Progress rate < required rate | 🟡 Medium | Adjust scope/resources |
| Tight | <10% schedule buffer | 🟢 Low | Monitor closely |

#### Burndown Analysis
```python
def calculate_timeline_risk(task):
    days_remaining = (deadline - today).days
    work_remaining = 1 - completion_percentage
    required_velocity = work_remaining / days_remaining

    if required_velocity > historical_velocity * 1.5:
        return "critical"
    elif required_velocity > historical_velocity * 1.2:
        return "high"
    elif required_velocity > historical_velocity:
        return "medium"
    return "low"
```

### 6. Resource Risks

#### Resource Availability
| Resource Issue | Impact | Risk Level | Mitigation |
|----------------|--------|------------|------------|
| Key person unavailable | Blocker | 🔴 Critical | Immediate reassignment |
| Skill gap identified | Delay | 🟠 High | Training or external help |
| Tool/system unavailable | Blocker | 🟠 High | Find alternative |
| Limited availability | Slowdown | 🟡 Medium | Adjust timeline |

### 7. Quality Risks

#### Quality Indicators
```python
quality_risk_indicators = {
    'no_tests': {
        'level': 'high',
        'indicator': 'Code without test coverage',
        'action': 'Add tests before proceeding'
    },
    'validation_failures': {
        'level': 'high',
        'indicator': 'Multiple validation checkpoint fails',
        'action': 'Review quality standards'
    },
    'tech_debt': {
        'level': 'medium',
        'indicator': 'Shortcuts accumulating',
        'action': 'Schedule refactoring'
    },
    'documentation_gap': {
        'level': 'low',
        'indicator': 'Missing/outdated docs',
        'action': 'Update documentation'
    }
}
```

## Composite Risk Score

### Risk Score Calculation

```python
def calculate_composite_risk(task):
    risk_scores = {
        'momentum': assess_momentum_risk(task) * 0.25,
        'confidence': assess_confidence_risk(task) * 0.20,
        'assumptions': assess_assumption_risk(task) * 0.20,
        'timeline': assess_timeline_risk(task) * 0.15,
        'dependencies': assess_dependency_risk(task) * 0.10,
        'quality': assess_quality_risk(task) * 0.10
    }

    composite = sum(risk_scores.values())

    if composite >= 75:
        return "critical"
    elif composite >= 50:
        return "high"
    elif composite >= 25:
        return "medium"
    return "low"
```

### Risk Factors Weighting

| Factor | Weight | Rationale |
|--------|--------|-----------|
| Momentum | 25% | Direct progress indicator |
| Confidence | 20% | Uncertainty measure |
| Assumptions | 20% | Foundation stability |
| Timeline | 15% | Deadline pressure |
| Dependencies | 10% | External factors |
| Quality | 10% | Long-term health |

## Early Warning Patterns

### Pattern Recognition

#### Death Spiral Pattern
```
Indicators:
1. Confidence drops → 2. Velocity decreases →
3. Assumptions invalidated → 4. Task stalls
```
**Risk Level**: 🔴 Critical
**Intervention**: Break cycle immediately

#### Cascade Failure Pattern
```
Indicators:
1. One task blocks → 2. Dependencies pile up →
3. Multiple tasks stall → 4. Project momentum lost
```
**Risk Level**: 🔴 Critical
**Intervention**: Unblock root cause urgently

#### Slow Burn Pattern
```
Indicators:
1. Gradual velocity decline → 2. Increasing tech debt →
3. Quality issues emerge → 4. Rework required
```
**Risk Level**: 🟠 High
**Intervention**: Address fundamentals

#### Confidence Erosion Pattern
```
Indicators:
1. Small issues accumulate → 2. Confidence drops →
3. Hesitation increases → 4. Progress slows
```
**Risk Level**: 🟡 Medium
**Intervention**: Rebuild confidence

## Risk Detection Rules

### Automated Detection

```python
risk_detection_rules = [
    # Critical Rules
    {
        'name': 'dead_stop',
        'condition': lambda t: t.velocity == 0 and t.status == "In Progress",
        'level': 'critical',
        'alert': 'Task has completely stopped'
    },
    {
        'name': 'critical_assumption_failed',
        'condition': lambda t: any(a.impact == 'critical' and a.status == 'invalidated' for a in t.assumptions),
        'level': 'critical',
        'alert': 'Critical assumption invalidated'
    },

    # High Risk Rules
    {
        'name': 'stalling_active',
        'condition': lambda t: t.momentum.phase == 'stalling' and t.status == "In Progress",
        'level': 'high',
        'alert': 'Active task is stalling'
    },
    {
        'name': 'confidence_crisis',
        'condition': lambda t: t.confidence < 30,
        'level': 'high',
        'alert': 'Confidence critically low'
    },

    # Medium Risk Rules
    {
        'name': 'velocity_decline',
        'condition': lambda t: velocity_trend(t, days=3) < -10,
        'level': 'medium',
        'alert': 'Velocity declining rapidly'
    },
    {
        'name': 'assumption_accumulation',
        'condition': lambda t: count_pending_assumptions(t) > 5,
        'level': 'medium',
        'alert': 'Too many unvalidated assumptions'
    }
]
```

## Risk Response Protocols

### By Risk Level

#### Critical Risk Response
```yaml
Timeline: Immediate (< 1 hour)
Actions:
  1. Stop affected work
  2. Notify project lead
  3. Convene emergency meeting
  4. Develop recovery plan
  5. Execute intervention
  6. Monitor hourly
Documentation: Required
Escalation: Always
```

#### High Risk Response
```yaml
Timeline: Same day (< 4 hours)
Actions:
  1. Alert task owner
  2. Assess impact
  3. Identify root cause
  4. Implement mitigation
  5. Schedule follow-up
  6. Monitor daily
Documentation: Required
Escalation: If not resolved in 24 hours
```

#### Medium Risk Response
```yaml
Timeline: Next day (< 24 hours)
Actions:
  1. Flag for review
  2. Discuss in standup
  3. Plan intervention
  4. Track progress
  5. Monitor weekly
Documentation: Recommended
Escalation: If becomes pattern
```

#### Low Risk Response
```yaml
Timeline: Next review cycle
Actions:
  1. Log observation
  2. Monitor trends
  3. Address if convenient
Documentation: Optional
Escalation: Not required
```

## Risk Mitigation Strategies

### Preventive Measures

1. **Regular Monitoring**: Daily risk scans
2. **Early Validation**: Test assumptions quickly
3. **Confidence Tracking**: Monitor sentiment
4. **Dependency Management**: Minimize chains
5. **Buffer Planning**: Build in slack time
6. **Quality Gates**: Catch issues early

### Corrective Measures

1. **Momentum Injection**: Add resources
2. **Confidence Rebuilding**: Small wins
3. **Assumption Validation**: Rapid testing
4. **Dependency Breaking**: Parallelization
5. **Scope Adjustment**: Focus on critical
6. **Team Support**: Pair programming

## Quick Reference Matrix

| Risk Type | Critical Indicator | Response Time | First Action |
|-----------|-------------------|---------------|--------------|
| Momentum | Velocity = 0 | Immediate | Unblock |
| Confidence | < 25 | Immediate | Reassess |
| Assumption | Critical invalid | Immediate | Pivot |
| Timeline | Past deadline | Immediate | Escalate |
| Dependency | Circular | Same day | Restructure |
| Quality | Security issue | Same day | Fix |
| Resource | Blocker unavailable | Same day | Reassign |