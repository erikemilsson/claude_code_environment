# Validate Assumptions Command

## Purpose
Systematically validate pending assumptions across tasks and update their status based on evidence.

## Context Required
- Task files with assumption arrays
- Access to validation methods (code, documentation, etc.)
- Understanding of impact levels

## Process

### 1. Gather Pending Assumptions

```python
# Scan all task files for pending assumptions
pending = []
for task_file in task_files:
    task = load_json(task_file)
    for assumption in task.assumptions:
        if assumption.status == "pending":
            pending.append({
                'task_id': task.id,
                'assumption': assumption
            })
```

### 2. Group by Validation Method

Group assumptions that can be validated together:

```python
groups = {
    'code_test': [],      # Test via code
    'doc_review': [],     # Check documentation
    'api_call': [],       # Test API endpoints
    'performance': [],    # Run performance tests
    'user_confirm': []    # Need user input
}
```

### 3. Execute Validation

For each validation group:

#### Code Testing
```python
def validate_code_assumptions(assumptions):
    for assumption in assumptions:
        try:
            # Run specific test
            result = run_validation_test(assumption)
            assumption['status'] = 'validated' if result else 'invalidated'
            assumption['validated_date'] = today()
            assumption['validation_notes'] = str(result)
        except Exception as e:
            assumption['status'] = 'invalidated'
            assumption['validation_notes'] = str(e)
```

#### Documentation Review
```python
def validate_documentation(assumptions):
    for assumption in assumptions:
        # Check official docs
        doc_evidence = search_documentation(assumption.description)
        if doc_evidence:
            assumption['status'] = 'validated'
            assumption['validation_notes'] = f"Confirmed in: {doc_evidence.source}"
        else:
            assumption['status'] = 'pending'  # Can't invalidate without evidence
            assumption['validation_notes'] = "No documentation found"
```

#### API Testing
```python
def validate_api_assumptions(assumptions):
    for assumption in assumptions:
        response = test_api_endpoint(assumption.endpoint)
        if matches_expectation(response, assumption):
            assumption['status'] = 'validated'
        else:
            assumption['status'] = 'invalidated'
            assumption['fallback_needed'] = True
```

### 4. Update Task Files

Write validated assumptions back to tasks:

```python
for task_id, assumptions in validated_assumptions.items():
    task = load_task(task_id)
    task['assumptions'] = assumptions
    task['validation_status'] = calculate_overall_status(assumptions)
    task['confidence'] = adjust_confidence_based_on_validation(
        task['confidence'],
        assumptions
    )
    save_task(task)
```

### 5. Handle Invalidations

For each invalidated assumption:

1. **Check Impact Level**:
   - Critical: Stop work, escalate immediately
   - High: Execute fallback plan
   - Medium: Adjust approach
   - Low: Note and continue

2. **Execute Fallback**:
   ```python
   if assumption.impact in ['critical', 'high']:
       fallback = assumption.fallback_plan
       create_new_tasks(fallback.alternative_approach)
       update_timeline(fallback.timeline_impact)
       notify_stakeholders(fallback.communication_plan)
   ```

3. **Update Related Tasks**:
   ```python
   for task_id in assumption.affected_tasks:
       task = load_task(task_id)
       task['notes'] += f"\nAssumption {assumption.id} invalidated"
       task['confidence'] -= impact_confidence_penalty[assumption.impact]
       recalculate_estimates(task)
   ```

### 6. Generate Validation Report

Create summary of validation results:

```markdown
# Assumption Validation Report - [Date]

## Summary
- Total Pending: X
- Validated: Y
- Invalidated: Z
- Still Pending: W

## Critical Findings
[List any critical/high impact invalidations]

## Validated Assumptions
[List with evidence]

## Invalidated Assumptions
[List with fallback plans]

## Actions Required
[Next steps based on invalidations]
```

## Output Location
- Updated task JSON files
- Validation report in `.claude/reports/validation-YYYY-MM-DD.md`
- Updated confidence scores in affected tasks

## Command Usage

### Validate All Pending
```bash
validate-assumptions --all
```

### Validate Specific Task
```bash
validate-assumptions --task 42
```

### Validate by Category
```bash
validate-assumptions --category technical
```

### Validate by Impact
```bash
validate-assumptions --impact critical
```

## Validation Triggers

Run this command when:

1. **Natural Breakpoints**:
   - Task completion
   - Sprint end
   - Milestone reached
   - Before deployment

2. **Risk Indicators**:
   - Confidence < 50%
   - Multiple blockers
   - Unexpected behavior
   - Performance issues

3. **Time-Based**:
   - Daily for critical
   - Weekly for high
   - Sprint for medium
   - As needed for low

## Critical Rules

- **Never Skip Critical**: Always validate critical assumptions
- **Document Evidence**: Record how assumption was validated
- **Execute Fallbacks**: Don't ignore invalidated assumptions
- **Update Promptly**: Reflect validation results immediately
- **Communicate Failures**: Share invalidations with team

## Integration with Belief Tracking

### Confidence Adjustment

```python
def adjust_confidence_after_validation(task, validation_results):
    validated_count = len([a for a in validation_results if a.status == 'validated'])
    invalidated_count = len([a for a in validation_results if a.status == 'invalidated'])

    # Boost for validated assumptions
    task.confidence += validated_count * 5

    # Penalty for invalidated assumptions
    for assumption in validation_results:
        if assumption.status == 'invalidated':
            penalty = {
                'critical': 30,
                'high': 20,
                'medium': 10,
                'low': 5
            }
            task.confidence -= penalty[assumption.impact]

    # Keep within bounds
    task.confidence = max(0, min(100, task.confidence))
```

### Momentum Impact

```python
def update_momentum_after_validation(task, validation_results):
    critical_invalid = any(
        a.status == 'invalidated' and a.impact == 'critical'
        for a in validation_results
    )

    if critical_invalid:
        task.momentum.phase = 'stalling'
        task.momentum.velocity = max(0, task.momentum.velocity - 40)
    elif all(a.status == 'validated' for a in validation_results):
        task.momentum.velocity = min(100, task.momentum.velocity + 10)
```

## Example Execution

### Input State
```json
{
  "task": "42",
  "assumptions": [
    {
      "id": "a1",
      "description": "API supports batch operations",
      "status": "pending",
      "impact": "high"
    },
    {
      "id": "a2",
      "description": "Response time < 100ms",
      "status": "pending",
      "impact": "medium"
    }
  ]
}
```

### Validation Process
1. Test API batch endpoint → Success
2. Measure response time → 150ms (Failed)

### Output State
```json
{
  "task": "42",
  "assumptions": [
    {
      "id": "a1",
      "description": "API supports batch operations",
      "status": "validated",
      "impact": "high",
      "validated_date": "2025-12-15",
      "validation_notes": "Tested with 100 item batch"
    },
    {
      "id": "a2",
      "description": "Response time < 100ms",
      "status": "invalidated",
      "impact": "medium",
      "validated_date": "2025-12-15",
      "validation_notes": "Actual: 150ms average",
      "fallback_plan": "Implement caching layer"
    }
  ],
  "validation_status": "partial",
  "confidence": 65,  // Reduced from 75
  "notes": "Performance assumption invalidated - implementing cache"
}