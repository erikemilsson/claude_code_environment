# Enhanced Task Schema with Belief Tracking

**DEPRECATED** - This document has been superseded by task-schema-consolidated.md

See: .claude/reference/task-schema-consolidated.md (Created: 2025-12-17)

NOTE: The nested "belief_tracking" format from this document was NOT adopted. Use flat belief tracking structure at root level.

---

## Overview

The enhanced task schema integrates belief tracking directly into the task management system, enabling confidence scoring, assumption management, momentum tracking, and decision documentation. This creates a transparent, self-aware project execution framework.

## Core Schema Structure

```json
{
  // Standard Task Fields
  "id": "string",
  "title": "string",
  "description": "string",
  "difficulty": "number (1-10)",
  "status": "Pending|In Progress|Blocked|Broken Down|Finished",
  "created_date": "YYYY-MM-DD",
  "updated_date": "YYYY-MM-DD",
  "dependencies": ["task_id"],
  "subtasks": ["task_id"],
  "parent_task": "task_id or null",
  "files_affected": ["filepath"],
  "notes": "string",

  // Belief Tracking Fields
  "confidence": 75,
  "assumptions": [
    {
      "id": "a1",
      "description": "string",
      "confidence": 80,
      "status": "pending|validated|invalidated",
      "impact": "low|medium|high|critical",
      "validation_method": "string",
      "validated_date": "YYYY-MM-DD or null"
    }
  ],
  "validation_status": "pending|validated|invalidated|partial",
  "momentum": {
    "phase": "pending|ignition|building|cruising|coasting|stalling|stopped",
    "velocity": 0,
    "last_activity": "YYYY-MM-DD"
  },
  "decision_rationale": "string"
}
```

## Confidence Scoring System (0-100)

### Score Ranges

| Range | Level | Description | Example Scenario |
|-------|-------|-------------|------------------|
| 90-100 | Very High | Clear path, proven approach, minimal unknowns | Updating a README file |
| 75-89 | High | Standard patterns apply, some minor uncertainties | Implementing CRUD operations |
| 50-74 | Medium | Significant unknowns, research needed | Integrating new API |
| 25-49 | Low | Many unknowns, experimental approach | New architecture pattern |
| 0-24 | Very Low | Highly uncertain, requires exploration | Cutting-edge technology |

### Confidence Factors

**Positive Factors (increase confidence):**
- Clear requirements (+10-20)
- Existing similar implementations (+15)
- Well-documented technology (+10)
- Team expertise available (+10-15)
- Proven patterns applicable (+10-20)

**Negative Factors (decrease confidence):**
- Ambiguous requirements (-10-20)
- New/unfamiliar technology (-15-25)
- External dependencies (-10-15)
- Limited documentation (-10-20)
- Cross-system integration (-10-15)

## Assumption Tracking

### Assumption Object Structure

```json
{
  "id": "unique_identifier",
  "description": "Clear statement of what we're assuming",
  "confidence": 80,
  "status": "pending|validated|invalidated",
  "impact": "low|medium|high|critical",
  "validation_method": "How we'll verify this assumption",
  "validated_date": null
}
```

### Impact Levels

- **Critical**: Project fails if assumption is wrong
- **High**: Major rework required if wrong
- **Medium**: Moderate adjustments needed if wrong
- **Low**: Minor changes only if wrong

### Validation Methods

- **Code Test**: Write code to verify
- **Documentation Review**: Check official docs
- **API Call**: Test actual endpoint
- **Performance Test**: Measure actual performance
- **User Feedback**: Get stakeholder confirmation
- **Prototype**: Build proof of concept

## Validation Status Types

### Task-Level Validation

- **pending**: Not yet validated, assumptions untested
- **validated**: All assumptions confirmed correct
- **invalidated**: One or more critical assumptions proven wrong
- **partial**: Some assumptions validated, others pending/failed

### Triggers for Validation

1. **Natural Breakpoints**: After completing subtasks
2. **Dependency Completion**: When dependent tasks finish
3. **Time-Based**: Daily/weekly validation checks
4. **Risk-Based**: When entering high-risk phases
5. **Change-Based**: When requirements change

## Momentum Tracking System

### Momentum Phases

| Phase | Velocity Range | Characteristics | Intervention Needed |
|-------|---------------|-----------------|---------------------|
| **pending** | 0 | Not started | Start planning |
| **ignition** | 0-20 | Just starting, gaining traction | Provide clarity, remove blockers |
| **building** | 20-50 | Accelerating progress | Maintain focus |
| **cruising** | 50-80 | Steady, optimal progress | Monitor only |
| **coasting** | 30-60 | Slowing but still moving | Check for issues |
| **stalling** | 10-30 | Nearly stopped | Urgent intervention |
| **stopped** | 0 | No progress | Escalate/reassign |

### Velocity Calculation

Velocity is calculated based on:

```python
factors = {
    'days_since_last_activity': -10 per day over 2 days,
    'completion_percentage': +1 per percent complete,
    'subtasks_completed': +20 per subtask,
    'blockers_present': -30 if blocked,
    'dependencies_met': +20 if all met,
    'confidence_level': +(confidence / 5)
}
```

### Momentum Transfer

Tasks can transfer momentum to related tasks:
- Parent tasks gain momentum when subtasks complete
- Dependent tasks gain momentum when dependencies finish
- Related tasks (same component) share momentum boosts

## Decision Rationale Documentation

### What to Document

**Architecture Decisions:**
```
"Chose microservices over monolith because:
1. Team distributed across timezones
2. Independent scaling requirements
3. Different technology stacks per service"
```

**Trade-off Decisions:**
```
"Prioritized speed over optimization:
- Deadline critical (launch in 2 weeks)
- Performance acceptable (200ms response)
- Can optimize in v2 after launch"
```

**Approach Changes:**
```
"Switched from REST to GraphQL mid-task:
- Original assumption: Simple data needs (invalidated)
- Discovered: Complex nested queries required
- GraphQL reduces API calls from 15 to 1"
```

### Decision Categories

1. **Technical**: Technology/tool selection
2. **Architectural**: System design choices
3. **Process**: Workflow/methodology decisions
4. **Trade-off**: Competing priority resolutions
5. **Pivot**: Course corrections during execution

## Usage Examples

### High Confidence Task

```json
{
  "id": "101",
  "title": "Add loading spinner to form",
  "difficulty": 2,
  "status": "In Progress",
  "confidence": 95,
  "assumptions": [
    {
      "id": "a1",
      "description": "Spinner component already exists",
      "confidence": 100,
      "status": "validated",
      "impact": "low",
      "validation_method": "Component library check",
      "validated_date": "2025-12-15"
    }
  ],
  "validation_status": "validated",
  "momentum": {
    "phase": "cruising",
    "velocity": 75,
    "last_activity": "2025-12-15"
  },
  "decision_rationale": "Using existing spinner component for consistency"
}
```

### Low Confidence Task

```json
{
  "id": "102",
  "title": "Implement real-time collaboration",
  "difficulty": 8,
  "status": "In Progress",
  "confidence": 35,
  "assumptions": [
    {
      "id": "a1",
      "description": "WebSocket library supports 1000+ concurrent users",
      "confidence": 40,
      "status": "pending",
      "impact": "critical",
      "validation_method": "Load testing",
      "validated_date": null
    },
    {
      "id": "a2",
      "description": "Conflict resolution algorithm handles all edge cases",
      "confidence": 25,
      "status": "pending",
      "impact": "high",
      "validation_method": "Prototype testing",
      "validated_date": null
    }
  ],
  "validation_status": "pending",
  "momentum": {
    "phase": "stalling",
    "velocity": 15,
    "last_activity": "2025-12-13"
  },
  "decision_rationale": "Attempting WebSocket approach first due to real-time requirements. May need to fall back to polling if performance issues arise."
}
```

## Integration with Commands

### complete-task.md Integration

When completing tasks, the command must:
1. Update confidence based on actual vs expected
2. Validate or invalidate assumptions
3. Calculate new momentum velocity
4. Require decision rationale for significant choices
5. Transfer momentum to related tasks

### check-risks.md Integration

Risk checking monitors:
1. Tasks with confidence < 50
2. Tasks in stalling/stopped momentum phase
3. Tasks with critical invalidated assumptions
4. Tasks with velocity decline > 30 points

### validate-assumptions.md Integration

Systematic validation:
1. List all pending assumptions
2. Group by validation method
3. Execute validation tests
4. Update assumption status
5. Recalculate task confidence

## Best Practices

1. **Update Confidence Regularly**: As you learn more, adjust confidence
2. **Document Assumptions Early**: Capture all assumptions at task start
3. **Monitor Momentum Daily**: Check for stalling tasks each day
4. **Validate at Breakpoints**: Test assumptions at natural pauses
5. **Explain Decisions**: Future you will thank present you
6. **Transfer Momentum**: Complete related tasks in sequence
7. **Escalate Stalls**: Don't let tasks sit in stalling phase
8. **Learn from Invalidations**: Update similar task assumptions