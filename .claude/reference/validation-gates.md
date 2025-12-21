# Validation Gates Framework

## Core Principle

**Every critical decision point must pass through explicit validation before proceeding**

Validation gates are MANDATORY checkpoints that ensure:
1. **Pre-conditions** are met before starting
2. **Invariants** hold during execution
3. **Post-conditions** verify completion
4. **Quality** meets acceptance criteria

## Gate Types & Criteria

### 1. Pre-Execution Gates (GO/NO-GO Decisions)

#### Task Start Gate
```
GATE: Can this task be started?

CHECKS:
□ Status is "Pending" or "In Progress" (not "Broken Down" or "Finished")
□ All dependencies are "Finished"
□ No active blockers exist
□ Required resources available
□ Confidence level >= 50%

PASS CRITERIA: All checks must pass
FAIL ACTION: Stop with specific reason
```

#### Breakdown Decision Gate
```
GATE: Should this task be broken down?

CHECKS:
□ Difficulty >= 7 OR user request
□ Task is decomposable into logical parts
□ Each subtask can be <= difficulty 6
□ Clear dependency chain possible

PASS CRITERIA: First check AND all others
FAIL ACTION: Proceed without breakdown if difficulty < 7
```

#### Environment Creation Gate
```
GATE: Ready to generate environment?

CHECKS:
□ Specification successfully read
□ Template confidence >= 85%
□ No critical unknowns remain
□ Configuration validated
□ Target directory writable

PASS CRITERIA: All checks must pass
FAIL ACTION: Gather missing information
```

### 2. Mid-Execution Gates (CONTINUE/ADJUST/ABORT)

#### Progress Checkpoint Gate
```
GATE: Should execution continue as planned?

TRIGGER: Every 3 steps OR 25% progress

CHECKS:
□ Current approach still valid
□ No unexpected blockers found
□ Confidence hasn't dropped >30%
□ Time estimate still reasonable
□ Context usage < 70%

PASS CRITERIA: All checks pass
ADJUST ACTION: Modify approach if 1-2 fail
ABORT ACTION: Stop if 3+ fail
```

#### Assumption Validation Gate
```
GATE: Are working assumptions still valid?

TRIGGER: Before critical operations

CHECKS:
□ Each assumption explicitly tested
□ >70% assumptions validated
□ No critical assumptions invalidated
□ Alternative approach available if needed

PASS CRITERIA: No critical failures
FAIL ACTION: Re-evaluate approach
```

#### Resource Threshold Gate
```
GATE: Sufficient resources to continue?

CHECKS:
□ Context usage < 80%
□ Time spent < 2x estimate
□ Iteration count < max_retries
□ Error rate < 20%

PASS CRITERIA: All within thresholds
FAIL ACTION: Checkpoint and optimize
```

### 3. Completion Gates (ACCEPT/REJECT/REWORK)

#### Task Completion Gate
```
GATE: Is the task truly complete?

CHECKS:
□ All requirements addressed
□ Tests pass (if applicable)
□ Documentation updated
□ No regression introduced
□ Confidence >= initial level
□ All subtasks finished (if parent)

PASS CRITERIA: All checks must pass
FAIL ACTION: Identify and fix gaps
```

#### Quality Acceptance Gate
```
GATE: Does output meet quality standards?

CHECKS:
□ Code follows guidelines
□ No security vulnerabilities
□ Performance acceptable
□ Error handling present
□ Edge cases considered

PASS CRITERIA: No critical issues
FAIL ACTION: Rework identified issues
```

#### Parent Completion Gate
```
GATE: Can parent task be auto-completed?

CHECKS:
□ All subtasks status == "Finished"
□ No subtask has critical notes
□ Combined output satisfies parent goal
□ Integration tested (if applicable)

PASS CRITERIA: All checks must pass
FAIL ACTION: Parent remains "Broken Down"
```

## Implementation Patterns

### Explicit Gate Check Pattern
```python
def validate_gate(gate_name, checks):
    """Execute validation gate with explicit pass/fail"""
    results = {}
    passed = 0
    failed = 0

    for check_name, check_func in checks.items():
        result = check_func()
        results[check_name] = result
        if result:
            passed += 1
        else:
            failed += 1
            log(f"GATE FAIL: {gate_name} - {check_name}")

    if failed == 0:
        log(f"GATE PASS: {gate_name} - All {passed} checks passed")
        return True, results
    else:
        log(f"GATE BLOCKED: {gate_name} - {failed}/{len(checks)} checks failed")
        return False, results
```

### Progressive Gate Pattern
```python
class ProgressiveGate:
    """Gate that tracks validation history"""

    def __init__(self, name, threshold=0.8):
        self.name = name
        self.threshold = threshold
        self.history = []

    def check(self, validations):
        total = len(validations)
        passed = sum(1 for v in validations if v())
        ratio = passed / total if total > 0 else 0

        self.history.append({
            'timestamp': now(),
            'ratio': ratio,
            'passed': ratio >= self.threshold
        })

        if ratio >= self.threshold:
            return 'PASS', ratio
        elif ratio >= self.threshold * 0.7:
            return 'CONDITIONAL', ratio
        else:
            return 'FAIL', ratio
```

### Circuit Breaker Gate
```python
class CircuitBreakerGate:
    """Gate that opens after repeated failures"""

    def __init__(self, name, failure_threshold=3):
        self.name = name
        self.failure_threshold = failure_threshold
        self.consecutive_failures = 0
        self.is_open = False

    def check(self, condition):
        if self.is_open:
            return False, "Circuit breaker open"

        if condition():
            self.consecutive_failures = 0
            return True, "Check passed"
        else:
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.failure_threshold:
                self.is_open = True
                return False, "Circuit breaker triggered"
            return False, f"Check failed ({self.consecutive_failures}/{self.failure_threshold})"
```

## Gate Integration Points

### In complete-task.md

```markdown
### Pre-Execution Validation Gate [MANDATORY]

**BEFORE starting work:**
```
EXECUTE validation_gate("task_start", {
    "status_check": status in ["Pending", "In Progress"],
    "dependency_check": all_dependencies_complete(),
    "blocker_check": no_active_blockers(),
    "confidence_check": confidence >= 50
})

IF gate_fails:
    DOCUMENT failure reason
    STOP execution
    PROVIDE remediation steps
```

### During Execution [MANDATORY CHECKPOINTS]

**AFTER every 3 steps:**
```
EXECUTE validation_gate("progress_checkpoint", {
    "approach_valid": current_approach_working(),
    "confidence_stable": confidence_drop < 30,
    "time_reasonable": time_spent < estimate * 1.5,
    "context_available": context_usage < 70
})

IF gate_fails:
    CHECKPOINT current state
    EVALUATE adjustments needed
    DECIDE continue/adjust/abort
```

### Completion Validation Gate [MANDATORY]

**BEFORE marking finished:**
```
EXECUTE validation_gate("task_complete", {
    "requirements_met": all_requirements_addressed(),
    "quality_check": meets_quality_standards(),
    "tests_pass": all_tests_passing(),
    "docs_updated": documentation_current(),
    "no_regression": no_breaking_changes()
})

IF gate_fails:
    IDENTIFY specific gaps
    COMPLETE missing work
    RE-VALIDATE before finishing
```
```

### In breakdown.md

```markdown
### Pre-Breakdown Validation Gate [MANDATORY]

**BEFORE creating subtasks:**
```
EXECUTE validation_gate("breakdown_required", {
    "difficulty_check": difficulty >= 7 OR user_requested,
    "decomposable": can_split_logically(),
    "size_appropriate": each_subtask_difficulty <= 6,
    "dependencies_clear": dependency_chain_valid()
})

IF gate_fails AND difficulty < 7:
    PROCEED without breakdown
    DOCUMENT why breakdown skipped
```

### Subtask Creation Gate [MANDATORY]

**FOR each proposed subtask:**
```
EXECUTE validation_gate("subtask_valid", {
    "difficulty_limit": difficulty <= 6,
    "independently_completable": no_circular_deps(),
    "clearly_defined": has_specific_deliverable(),
    "testable": has_completion_criteria()
})

IF gate_fails:
    ADJUST subtask definition
    RE-VALIDATE before creating
```
```

## Gate Metrics & Monitoring

### Key Metrics to Track

| Metric | Description | Target |
|--------|-------------|--------|
| Gate Pass Rate | % of gates passed first try | >80% |
| False Positive Rate | Gates failed but task succeeded | <10% |
| False Negative Rate | Gates passed but task failed | <5% |
| Average Retries | Attempts before gate pass | <2 |
| Time in Gate | Duration of validation | <5 sec |

### Gate Effectiveness Review

Weekly review questions:
1. Which gates fail most frequently?
2. Are failures predictive of task problems?
3. Which checks are too strict/lenient?
4. Where do we need additional gates?
5. Can any gates be automated further?

## Quick Reference Card

### Task Execution Gates

| Gate | When | Pass Criteria | Fail Action |
|------|------|---------------|-------------|
| Start Gate | Before work | All deps complete, no blockers | Stop & fix |
| Progress Gate | Every 3 steps | Approach valid, confidence stable | Adjust/abort |
| Assumption Gate | Before critical ops | >70% validated | Re-evaluate |
| Complete Gate | Before finishing | All requirements met | Fix gaps |
| Quality Gate | At completion | Standards met, tests pass | Rework |

### Breakdown Gates

| Gate | When | Pass Criteria | Fail Action |
|------|------|---------------|-------------|
| Breakdown Required | Before split | Difficulty ≥7 or requested | Skip if <7 |
| Subtask Valid | Per subtask | Difficulty ≤6, independent | Adjust definition |
| Parent Update | After creation | All subtasks created | Retry creation |

### Environment Gates

| Gate | When | Pass Criteria | Fail Action |
|------|------|---------------|-------------|
| Spec Analysis | After read | Indicators extracted | Re-read/clarify |
| Template Selection | Before generation | Confidence ≥85% | Ask user |
| File Generation | Before writes | Paths valid, writable | Fix permissions |
| Validation Final | After creation | All files exist & valid | Regenerate |

## Gate Enforcement Levels

### Level 1: Advisory (Log Only)
- Gate executes but doesn't block
- Logs pass/fail for analysis
- Used during development

### Level 2: Soft Block (Warning)
- Gate warns on failure
- Allows override with reason
- Default for most gates

### Level 3: Hard Block (Mandatory)
- Gate must pass to proceed
- No override without escalation
- Used for critical operations

### Level 4: Multi-Gate (Consensus)
- Multiple gates must agree
- Used for high-risk operations
- Requires unanimous pass

## Implementation Priority

1. **Immediate** (implement now):
   - Task start/complete gates
   - Breakdown validation
   - Progress checkpoints

2. **High Priority**:
   - Assumption validation
   - Quality gates
   - Parent completion

3. **Medium Priority**:
   - Resource thresholds
   - Circuit breakers
   - Progressive gates

4. **Future Enhancement**:
   - ML-based gate tuning
   - Predictive gate warnings
   - Cross-project gate learning