# Belief Tracking Framework

*Consolidated guidance for confidence scoring and assumption management.*

## Confidence Scoring

### Score Ranges

| Score | Level | Description | Action |
|-------|-------|-------------|--------|
| 90-100 | Very High | Proven approach | Proceed automatically |
| 75-89 | High | Standard patterns | Proceed with monitoring |
| 50-74 | Medium | Some unknowns | Proceed with validation |
| 25-49 | Low | Significant uncertainty | Prototype/research first |
| 0-24 | Very Low | Highly uncertain | Full research required |

### Base Scores by Task Type

| Task Type | Base Score |
|-----------|------------|
| Documentation | 85 |
| Refactoring | 75 |
| Bug fix | 70 |
| New feature | 60 |
| Integration | 55 |
| Architecture | 50 |
| Research | 40 |
| Experimental | 25 |

### Adjustments

**Increase confidence (+5 to +20)**
- Clear, detailed requirements
- Prior successful experience
- Good documentation available
- Proven patterns/tools
- Automated tests possible

**Decrease confidence (-5 to -20)**
- Cross-system dependencies
- Unclear requirements
- External API reliance
- Legacy system interaction
- Tight deadlines
- Security/compliance requirements

## Assumption Management

### Assumption Structure

```json
{
  "id": "assumption-id",
  "description": "Clear statement of assumption",
  "category": "requirement|technical|dependency|resource|timeline",
  "confidence": 80,
  "status": "pending|validated|invalidated",
  "impact": "low|medium|high|critical",
  "validation_method": "How to verify",
  "fallback_plan": "What to do if false",
  "affected_tasks": ["task-ids"]
}
```

### Impact Levels

| Level | Definition | Response |
|-------|------------|----------|
| Critical | Project fails if wrong | Validate immediately |
| High | Significant rework if wrong | Validate early |
| Medium | Moderate adjustments needed | Validate during implementation |
| Low | Minor tweaks only | Validate as convenient |

### Validation Methods
- **Code testing**: Direct validation through tests
- **Documentation review**: Check official specs
- **Prototype/spike**: Build minimal POC
- **Expert consultation**: Ask domain expert
- **Production testing**: Deploy to staging

### When to Validate
- Before critical decisions
- At project milestones
- When confidence drops
- When related assumption fails
- Before major commits

## Momentum Tracking

### Phases

| Phase | Velocity | Description |
|-------|----------|-------------|
| pending | 0 | Not started |
| ignition | 10-20 | Just starting |
| building | 20-50 | Gaining speed |
| cruising | 50-80 | Steady progress |
| coasting | 30-60 | Slowing down |
| stalling | 10-30 | Major slowdown |
| stopped | 0 | No progress |

### Transitions

```
Starting work → ignition
Making progress → building
Steady progress → cruising
Slowing down → coasting
Major issues → stalling
Blocked → stopped
```

## Integration

### In Task JSON

```json
{
  "confidence": 75,
  "assumptions": [
    {"description": "...", "status": "pending", "impact": "high"}
  ],
  "validation_status": "pending|partial|validated",
  "momentum": {
    "phase": "building",
    "velocity": 35,
    "last_activity": "2025-12-17"
  }
}
```

### Confidence-Momentum Correlation

| Confidence | Typical Phase |
|-----------|---------------|
| 80-100 | Cruising |
| 60-79 | Building |
| 40-59 | Ignition/Coasting |
| 20-39 | Stalling |
| 0-19 | Stopped |

## Risk Indicators

### Warning Signs
- Multiple assumptions at "pending" status
- Confidence < 50% on high-priority task
- Assumptions invalidated but no fallback
- Momentum stalling for > 2 checkpoints
- Related assumptions failing in pattern

### Response Actions
1. **Break down** into smaller pieces
2. **Prototype** to validate approach
3. **Research** unknowns
4. **Consult** domain experts
5. **Prepare** parallel approaches

## Quick Reference

### Confidence Quick Scoring
Start at 50, then adjust:
- **Big boosts (+10-20)**: Done before, clear requirements, good docs
- **Big risks (-10-20)**: Never done, vague requirements, external dependencies

### Assumption Priority
1. Validate critical/high impact first
2. Every high-impact assumption needs fallback plan
3. Review daily during active work
4. Escalate failures immediately
