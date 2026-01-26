# Validation Gates Framework

*Mandatory checkpoints ensuring quality at critical decision points.*

## Core Principle

**Every critical decision must pass explicit validation before proceeding.**

Gates enforce:
1. **Pre-conditions** met before starting
2. **Invariants** hold during execution
3. **Post-conditions** verify completion
4. **Quality** meets acceptance criteria

## Gate Types

### 1. Pre-Execution Gates (GO/NO-GO)

#### Task Start Gate
```
CHECKS:
□ Status is "Pending" or "In Progress"
□ All dependencies are "Finished"
□ No active blockers
□ Confidence >= 50%
□ Difficulty >= 7 requires breakdown first

PASS: All checks pass → Proceed
FAIL: Stop with specific reason
```

#### Breakdown Decision Gate
```
CHECKS:
□ Difficulty >= 7 OR user request
□ Task is decomposable
□ Each subtask can be <= difficulty 6
□ Clear dependency chain possible

PASS: First check AND all others → Break down
FAIL: If difficulty < 7 → Proceed without breakdown
```

### 2. Mid-Execution Gates (CONTINUE/ADJUST/ABORT)

#### Progress Checkpoint Gate
**Trigger**: Every 3 steps or 25% progress

```
CHECKS:
□ Current approach still valid
□ No unexpected blockers
□ Confidence hasn't dropped > 30%
□ Time spent < 2x estimate
□ Context usage < 70%

PASS: Continue execution
WARN (1-2 fail): Adjust approach
FAIL (3+ fail): Checkpoint and re-evaluate
```

#### Assumption Validation Gate
**Trigger**: Before critical operations

```
CHECKS:
□ Each assumption explicitly tested
□ > 70% assumptions validated
□ No critical assumptions invalidated

PASS: Continue
FAIL: Re-evaluate approach
```

### 3. Post-Execution Gates (ACCEPT/REJECT)

#### Task Completion Gate
```
CHECKS:
□ All requirements addressed
□ Tests pass (if applicable)
□ Documentation updated
□ No regression introduced
□ Confidence >= initial level
□ All subtasks finished (if parent)

PASS: Mark as Finished
FAIL: Identify and fix gaps
```

#### Quality Acceptance Gate
```
CHECKS:
□ Code follows guidelines
□ No security vulnerabilities
□ Performance acceptable
□ Error handling present
□ Edge cases considered

PASS: Accept output
FAIL: Rework identified issues
```

## Integration Points

### In complete-task workflow

**Before starting:**
```
1. Run pre-execution gate
2. If FAIL → Stop, document reason
3. If PASS → Continue
```

**During execution (every 3 steps):**
```
1. Run progress checkpoint gate
2. If WARN → Adjust approach
3. If FAIL → Create checkpoint, evaluate
```

**Before finishing:**
```
1. Run completion gate
2. If FAIL → Fix gaps, re-run
3. If PASS → Mark finished
```

### In breakdown workflow

**Before breakdown:**
```
1. Run breakdown decision gate
2. If FAIL and difficulty < 7 → Skip breakdown
3. If PASS → Create subtasks
```

**Per subtask:**
```
1. Run subtask validation gate
2. Verify difficulty <= 6
3. Verify no circular dependencies
```

## Gate Configuration

Default thresholds (adjustable in `agent-config.json`):

```json
{
  "validation_gates": {
    "pre_execution": {
      "confidence_threshold": 50,
      "confidence_warning": 70
    },
    "mid_execution": {
      "progress_check_interval": 3,
      "confidence_drop_max": 30,
      "context_usage_max": 70
    },
    "post_execution": {
      "assumption_validation_min": 70,
      "require_completion_notes": true
    }
  }
}
```

## Enforcement Levels

| Level | Behavior | Use For |
|-------|----------|---------|
| Advisory | Log only | Development |
| Soft Block | Warn, allow override | Most gates |
| Hard Block | Must pass | Critical operations |

## Command-Line Usage

```bash
# Manual gate execution
python scripts/validation-gates.py pre-exec task-42
python scripts/validation-gates.py mid-exec task-42 --step 6
python scripts/validation-gates.py post-exec task-42
python scripts/validation-gates.py breakdown task-42
```

## Best Practices

### DO
- Run pre-execution gates before every task
- Run mid-execution gates at checkpoints
- Run post-execution gates before marking finished
- Log all gate results

### DON'T
- Skip gates "just this once"
- Ignore warnings without documenting why
- Proceed when blocking gates fail
- Modify gates to "make them pass"

### Document Overrides
If proceeding despite warnings:
```json
{
  "gate_overrides": [{
    "gate": "confidence_threshold",
    "reason": "Time constraints - risks documented",
    "approved_by": "user",
    "date": "2025-12-17"
  }]
}
```

## Quick Reference

| Gate | When | Pass Criteria | Fail Action |
|------|------|---------------|-------------|
| Start | Before work | Deps complete, no blockers | Stop & fix |
| Progress | Every 3 steps | Approach valid, confidence stable | Adjust/abort |
| Assumption | Before critical ops | >70% validated | Re-evaluate |
| Complete | Before finishing | All requirements met | Fix gaps |
| Quality | At completion | Standards met | Rework |
| Breakdown | Before split | Difficulty ≥7 | Skip if <7 |
