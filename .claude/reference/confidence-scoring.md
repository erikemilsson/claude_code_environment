# Confidence Scoring Methodology

## Overview

Confidence scoring quantifies certainty levels in project decisions, task estimates, and assumption validity. This 0-100 scale provides transparency about uncertainty and helps identify where additional validation or research is needed.

## Confidence Score Ranges

| Score | Level | Description | When to Use |
|-------|-------|-------------|-------------|
| 90-100 | Very High | Near certainty, proven approach | Well-documented, frequently done tasks |
| 75-89 | High | Strong confidence, standard patterns | Common patterns with minor variations |
| 50-74 | Medium | Moderate confidence, some unknowns | New combinations of known techniques |
| 25-49 | Low | Significant uncertainty | Experimental approaches, many unknowns |
| 0-24 | Very Low | Highly uncertain | Cutting-edge, unprecedented tasks |

## Calculation Methodology

### Base Score Determination

Start with a base score based on task type:

```python
base_scores = {
    'documentation': 85,      # Usually straightforward
    'bug_fix': 70,           # Depends on bug complexity
    'new_feature': 60,        # New code, some unknowns
    'refactoring': 75,        # Known code, clear goals
    'architecture': 50,       # Many decisions, trade-offs
    'integration': 55,        # External dependencies
    'research': 40,          # Exploration required
    'experimental': 25        # Uncharted territory
}
```

### Adjustment Factors

Apply these modifiers to the base score:

#### Positive Adjustments (add points)

**Requirements Clarity**
- Crystal clear, detailed specs: +15
- Well-defined acceptance criteria: +10
- Clear success metrics: +5

**Prior Experience**
- Done identical task before: +20
- Similar task completed recently: +15
- Related experience available: +10
- Team member has expertise: +8

**Documentation Quality**
- Comprehensive documentation exists: +15
- Good examples available: +10
- Active community support: +5

**Tool/Technology Maturity**
- Stable, well-tested tools: +10
- Long-term support versions: +5
- Industry standard solutions: +8

**Testing Capability**
- Automated tests possible: +10
- Quick feedback loops: +8
- Rollback capability: +5

#### Negative Adjustments (subtract points)

**Complexity Factors**
- Cross-system dependencies: -15
- Concurrent user requirements: -10
- Performance constraints: -10
- Security requirements: -8

**Unknown Variables**
- Unclear requirements: -20
- Changing specifications: -15
- Hidden dependencies: -12
- Legacy system interaction: -10

**Resource Constraints**
- Tight deadline pressure: -10
- Limited testing environment: -8
- No rollback capability: -10
- Single point of failure: -12

**External Dependencies**
- Third-party API reliance: -10
- Vendor lock-in risk: -8
- Regulatory compliance needed: -12
- Customer data involved: -10

## Context-Specific Scoring

### Template Selection Confidence

When choosing project templates:

```python
template_confidence = {
    'exact_match': 95,      # Requirements match template perfectly
    'close_match': 80,      # 80%+ requirements align
    'partial_match': 60,    # 50-80% alignment
    'adaptation_needed': 45, # Significant customization required
    'custom_build': 30      # No suitable template exists
}
```

### Task Completion Estimates

Confidence in time estimates:

```python
estimate_confidence = base_score * complexity_factor * history_factor

Where:
- complexity_factor = 1.0 - (unknowns * 0.1)
- history_factor = accuracy_of_past_estimates / 100
```

### Assumption Validity

Individual assumption confidence:

```python
assumption_confidence = {
    'documented_fact': 95,        # In official documentation
    'tested_behavior': 85,        # Verified through testing
    'common_knowledge': 75,       # Industry standard practice
    'educated_guess': 50,         # Based on similar systems
    'hypothesis': 30,             # Needs validation
    'pure_speculation': 10        # No supporting evidence
}
```

## Practical Examples

### Example 1: Simple Bug Fix

```json
{
  "task": "Fix typo in error message",
  "base_score": 70,
  "adjustments": [
    {"factor": "Clear requirement", "value": +10},
    {"factor": "Simple change", "value": +15},
    {"factor": "Easy to test", "value": +5}
  ],
  "final_confidence": 100,
  "rationale": "Trivial change with no risk"
}
```

### Example 2: API Integration

```json
{
  "task": "Integrate payment provider API",
  "base_score": 55,
  "adjustments": [
    {"factor": "Good documentation", "value": +10},
    {"factor": "Example code available", "value": +8},
    {"factor": "External dependency", "value": -10},
    {"factor": "Financial data handling", "value": -12},
    {"factor": "Regulatory compliance", "value": -10}
  ],
  "final_confidence": 41,
  "rationale": "External dependencies and compliance requirements introduce significant uncertainty"
}
```

### Example 3: Architecture Decision

```json
{
  "task": "Choose between microservices and monolith",
  "base_score": 50,
  "adjustments": [
    {"factor": "Team experience with both", "value": +10},
    {"factor": "Clear scaling requirements", "value": +8},
    {"factor": "Long-term impact", "value": -15},
    {"factor": "Difficult to reverse", "value": -12}
  ],
  "final_confidence": 41,
  "rationale": "High-impact decision with long-term consequences"
}
```

## Confidence Over Time

### Confidence Lifecycle

```
Project Start: Low confidence (many unknowns)
       ↓
Research Phase: Confidence increases (learning)
       ↓
Planning Complete: Peak planning confidence
       ↓
Implementation Start: Temporary dip (reality check)
       ↓
Mid-Implementation: Steady increase (experience)
       ↓
Testing Phase: Validation adjustments (±)
       ↓
Completion: Highest confidence (proven)
```

### When to Recalculate

Recalculate confidence when:

1. **New Information**: Requirements change or clarify
2. **Assumption Changes**: Validation or invalidation
3. **Milestone Reached**: Natural checkpoint
4. **Blocker Encountered**: Unexpected obstacle
5. **Dependency Resolved**: External factor clarified

## Using Confidence Scores

### Decision Making

| Confidence | Recommended Action |
|-----------|-------------------|
| 75-100 | Proceed with standard process |
| 50-74 | Proceed with extra validation checkpoints |
| 25-49 | Create prototype or proof of concept first |
| 0-24 | Research phase required before commitment |

### Risk Mitigation

For low confidence tasks:

1. **Break Down**: Decompose into smaller, higher-confidence pieces
2. **Prototype**: Build minimal version to validate approach
3. **Research**: Investigate unknowns before committing
4. **Expert Consultation**: Seek domain expertise
5. **Parallel Paths**: Explore multiple approaches simultaneously

### Communication

Use confidence to set expectations:

- **High confidence**: "This will take 2 days" (definitive)
- **Medium confidence**: "This should take 2-3 days" (likely range)
- **Low confidence**: "Initial estimate is 2-5 days, pending investigation" (wide range)

## Integration with Belief Tracking

### Task Confidence Evolution

Track how confidence changes:

```json
{
  "confidence_history": [
    {"date": "2025-12-01", "score": 45, "reason": "Initial assessment"},
    {"date": "2025-12-05", "score": 65, "reason": "Requirements clarified"},
    {"date": "2025-12-08", "score": 55, "reason": "Dependency issue discovered"},
    {"date": "2025-12-10", "score": 80, "reason": "Solution validated"}
  ]
}
```

### Assumption Impact on Confidence

Each assumption affects overall confidence:

```python
task_confidence = base_confidence * assumption_factor

Where assumption_factor =
  (sum of (assumption_confidence * assumption_impact)) /
  (sum of assumption_impacts)
```

### Momentum Correlation

Confidence often correlates with momentum:

| Confidence | Typical Momentum Phase |
|-----------|------------------------|
| 80-100 | Cruising |
| 60-79 | Building |
| 40-59 | Ignition/Coasting |
| 20-39 | Stalling |
| 0-19 | Stopped |

## Calibration Guidelines

### Personal Calibration

Track your estimates vs actuals:

```python
calibration_score = (
    correct_high_confidence_predictions /
    total_high_confidence_predictions
) * 100
```

Aim for:
- 90% accuracy when confidence > 90
- 75% accuracy when confidence > 75
- 50% accuracy when confidence > 50

### Team Calibration

Normalize across team members:

1. Track individual calibration scores
2. Identify over/under-confident patterns
3. Apply personal adjustment factors
4. Regular calibration reviews

## Common Pitfalls

### Overconfidence Bias

**Symptoms:**
- Consistently underestimate time
- Surprises during implementation
- Frequent scope creep

**Mitigation:**
- Apply "optimism tax" (-10 to -15 points)
- Require evidence for high scores
- Regular retrospectives

### Underconfidence Paralysis

**Symptoms:**
- Excessive research phases
- Over-engineering solutions
- Analysis paralysis

**Mitigation:**
- Set minimum confidence thresholds
- Time-box research phases
- Accept calculated risks

### False Precision

**Symptoms:**
- Arguing about 73 vs 74
- Over-analyzing small differences
- Missing the bigger picture

**Mitigation:**
- Use ranges (70-80 instead of 75)
- Focus on level changes (High→Medium)
- Round to nearest 5 or 10

## Quick Reference Card

### Confidence Quick Scoring

Start with base (50), then adjust:

**Big Boosts (+10 to +20)**
- Done before successfully
- Clear requirements
- Good documentation
- Proven patterns

**Big Risks (-10 to -20)**
- Never done before
- Vague requirements
- External dependencies
- Compliance requirements

**Result Interpretation**
- 75+ → Green light
- 50-74 → Proceed carefully
- 25-49 → Research first
- 0-24 → Reconsider approach