# Hypothesis Tracking Standards

## Overview

This document defines standards for formulating, documenting, testing, and tracking research hypotheses. Proper hypothesis management ensures rigorous scientific methodology, clear testing criteria, and transparent reporting of results.

## Hypothesis Fundamentals

### What is a Hypothesis?

A hypothesis is a testable prediction about the relationship between variables, derived from theory or prior research. It must be:

- **Testable**: Can be empirically verified or falsified
- **Specific**: Clearly defines variables and expected relationships
- **Falsifiable**: Possible to prove wrong
- **Based on Theory**: Grounded in existing knowledge or logical reasoning

### Types of Hypotheses

#### Null Hypothesis (H₀)

Statement of no effect, no difference, or no relationship.

**Examples**:
- "There is no difference in test scores between the treatment and control groups"
- "The correlation between hours studied and exam scores is zero"
- "The drug has no effect on blood pressure compared to placebo"

#### Alternative Hypothesis (H₁ or Hₐ)

Statement that contradicts the null hypothesis; what you expect to find.

**Examples**:
- "The treatment group will have higher test scores than the control group" (directional)
- "There is a difference in test scores between groups" (non-directional)

#### Directional vs. Non-Directional

**Directional (One-tailed)**:
- Predicts direction of effect: "Group A will score higher than Group B"
- Used when theory strongly predicts direction
- More statistical power if correct, but inappropriate if direction uncertain

**Non-directional (Two-tailed)**:
- Predicts difference without specifying direction: "Groups will differ"
- More conservative, appropriate when direction uncertain
- Standard in most research

## Hypothesis Formulation Framework

### FINER Criteria

Good hypotheses are **FINER**:

- **Feasible**: Can be investigated with available resources, time, and subjects
- **Interesting**: Novel, relevant, or addresses important question
- **Novel**: Confirms, refutes, or extends previous findings
- **Ethical**: Can be studied without ethical violations
- **Relevant**: Advances scientific knowledge or has practical implications

### Formulation Template

```markdown
## Hypothesis [ID]: [Brief Title]

### Research Question
[What question does this hypothesis address?]

### Theoretical Basis
[What theory or prior research supports this hypothesis?]

### Variables
- **Independent Variable(s)**: [Variable(s) being manipulated or observed]
  - Levels/Categories: [Describe levels or range]
- **Dependent Variable(s)**: [Variable(s) being measured]
  - Measurement: [How will it be measured?]
  - Unit: [Units of measurement]
- **Control Variables**: [Variables held constant]
- **Confounding Variables**: [Potential confounds to address]

### Hypothesis Statement
- **Null Hypothesis (H₀)**: [Statement of no effect]
- **Alternative Hypothesis (H₁)**: [Expected finding]
- **Type**: [Directional/Non-directional]

### Operationalization
[How will abstract concepts be measured concretely?]

### Expected Effect
- **Direction**: [Positive/Negative/Non-directional]
- **Magnitude**: [Small/Medium/Large or specific effect size]
- **Statistical Significance Level**: [α = 0.05 typical, or specify]

### Testing Plan
- **Study Design**: [Experimental, observational, etc.]
- **Statistical Test**: [t-test, ANOVA, regression, etc.]
- **Sample Size**: [Planned N, with power analysis justification]
- **Data Collection Method**: [Surveys, experiments, observations, etc.]

### Success Criteria
[What results would support/reject this hypothesis?]
```

## Hypothesis Organization

### Hypothesis Registry

Maintain a central registry of all hypotheses:

```markdown
# Hypothesis Registry

| ID | Title | Status | Priority | Date Created | Date Tested | Result |
|----|-------|--------|----------|--------------|-------------|---------|
| H1 | Exercise improves cognition | Tested | High | 2025-01-15 | 2025-03-20 | Supported |
| H2 | Dosage affects response time | In Progress | High | 2025-01-20 | - | - |
| H3 | Age moderates effect | Pending | Medium | 2025-02-01 | - | - |
```

### Status Values

- **Pending**: Formulated but not yet tested
- **In Progress**: Data collection or analysis underway
- **Tested**: Analysis complete
- **Supported**: Results consistent with alternative hypothesis
- **Not Supported**: Results consistent with null hypothesis
- **Inconclusive**: Results ambiguous or insufficient data
- **Revised**: Hypothesis modified based on preliminary findings
- **Abandoned**: No longer pursuing this hypothesis

### Priority Levels

- **High**: Primary research questions, essential to project
- **Medium**: Secondary questions, interesting but not critical
- **Low**: Exploratory, opportunistic if data available

## Statistical Framework

### Frequentist Approach

Traditional null hypothesis significance testing (NHST).

#### Testing Process

1. **Formulate Hypotheses**: State H₀ and H₁
2. **Set Significance Level**: Typically α = 0.05 (5% Type I error rate)
3. **Collect Data**: Following planned methodology
4. **Calculate Test Statistic**: Based on data and chosen test
5. **Determine p-value**: Probability of observing data if H₀ is true
6. **Make Decision**:
   - If p < α: Reject H₀, support H₁
   - If p ≥ α: Fail to reject H₀

#### Reporting Template

```markdown
### Hypothesis [ID] Results

**Test**: [t-test, ANOVA, chi-square, etc.]
**Test Statistic**: [t/F/χ²/etc.] = [value], df = [degrees of freedom]
**p-value**: p = [value]
**Effect Size**: [Cohen's d, η², r, etc.] = [value]
**Confidence Interval**: [95% CI: lower, upper]

**Decision**: [Reject/Fail to reject] H₀
**Interpretation**: [Plain language explanation of what results mean]
```

### Bayesian Approach

Alternative to NHST; updates prior beliefs with data.

#### Bayes Factor

Quantifies evidence for H₁ relative to H₀:

- **BF₁₀ > 10**: Strong evidence for H₁
- **BF₁₀ = 3-10**: Moderate evidence for H₁
- **BF₁₀ = 1**: No evidence either way
- **BF₁₀ < 1/3**: Evidence for H₀

#### Reporting Template

```markdown
### Hypothesis [ID] Results (Bayesian)

**Prior Distribution**: [Description of prior beliefs]
**Posterior Distribution**: [Updated beliefs after seeing data]
**Bayes Factor (BF₁₀)**: [value]
**Posterior Probability**: P(H₁|data) = [value]
**Credible Interval**: [95% CrI: lower, upper]

**Interpretation**: [Evidence strength and updated beliefs]
```

## Multiple Hypothesis Testing

### Problem: Inflated Type I Error

Testing multiple hypotheses increases false positive rate.

**Example**:
- Single test at α = 0.05: 5% false positive rate
- 20 independent tests: P(at least one false positive) ≈ 64%

### Correction Methods

#### Bonferroni Correction

Most conservative; divides α by number of tests.

**Adjusted α**: α_adjusted = α / m (where m = number of tests)

**Example**: 10 tests, α = 0.05 → α_adjusted = 0.005

**Pros**: Simple, controls family-wise error rate
**Cons**: Very conservative, reduces power

#### Benjamini-Hochberg (False Discovery Rate)

Less conservative; controls proportion of false discoveries.

**Process**:
1. Order p-values from smallest to largest
2. Find largest i where p_i ≤ (i/m) × α
3. Reject all hypotheses with p ≤ p_i

**Pros**: More power than Bonferroni
**Cons**: Allows some false positives

#### Holm-Bonferroni (Sequential Bonferroni)

Compromise between Bonferroni and no correction.

**Process**:
1. Order p-values from smallest to largest
2. Test each at α/(m - i + 1) until one fails
3. Reject all hypotheses before first failure

### Planned vs. Post-Hoc Comparisons

**Planned Comparisons**:
- Hypotheses specified before data collection
- Based on theory or prior research
- More lenient correction appropriate

**Post-Hoc/Exploratory**:
- Hypotheses generated after seeing data
- Data-driven pattern finding
- Requires stricter correction or validation in new data

## Hypothesis Evolution

### Pre-Registration

Register hypotheses before data collection to prevent:
- HARKing (Hypothesizing After Results are Known)
- p-hacking (trying many analyses until finding significance)
- Selective reporting of significant results

**Platforms**:
- Open Science Framework (OSF)
- AsPredicted
- ClinicalTrials.gov (clinical research)

**What to Register**:
- Research hypotheses
- Study design and methods
- Sample size and power analysis
- Analysis plan
- Outcome measures

### Hypothesis Revision

Sometimes hypotheses need modification based on preliminary findings.

#### When Revision is Appropriate

- Preliminary data reveals measurement issues
- Pilot study suggests different effect than expected
- Theory development leads to refined predictions

#### Revision Documentation

```markdown
### Hypothesis Revision Log

**Original Hypothesis (H[ID]v1)**: [Original statement]
**Date**: [Date formulated]

**Revised Hypothesis (H[ID]v2)**: [Revised statement]
**Date**: [Date revised]
**Reason**: [Why revision was needed]
**Status of Original**: [Abandoned/Tested separately/Integrated]

**Impact on Analysis**: [How this affects statistical approach]
```

#### Transparency Requirements

- Clearly label exploratory vs. confirmatory analyses
- Report both original and revised hypotheses
- Acknowledge revision in publications
- Ideally test revised hypothesis in new sample

## Common Hypothesis Pitfalls

### 1. Vague Hypotheses

**Problem**: "Social media affects mental health"
**Better**: "Adolescents who spend >3 hours/day on social media will report higher depression scores (PHQ-9) than those spending <1 hour/day"

### 2. Unfalsifiable Hypotheses

**Problem**: "The universe has a purpose"
**Better**: "Patients receiving mindfulness training will show reduced cortisol levels compared to wait-list controls"

### 3. Confusing Hypothesis with Prediction

**Hypothesis**: Theoretical statement about relationships
**Prediction**: Specific expected outcome in your study

### 4. Multiple Hypotheses in One

**Problem**: "Intervention will improve test scores and attendance"
**Better**:
- H1: "Intervention will improve test scores"
- H2: "Intervention will improve attendance"

### 5. Directional Hypothesis Without Theory

Don't predict direction unless you have theoretical justification.

### 6. Ignoring Effect Size

Significance doesn't mean importance. Always consider effect size.

### 7. Not Considering Statistical Power

Under-powered studies waste resources and fail to detect real effects.

## Documentation Templates

### Individual Hypothesis File

Create `research/hypotheses/hypothesis-[ID].md`:

```markdown
# Hypothesis [ID]: [Title]

## Status
- **Current Status**: [Pending/In Progress/Tested]
- **Priority**: [High/Medium/Low]
- **Date Created**: [YYYY-MM-DD]
- **Last Updated**: [YYYY-MM-DD]

## Research Context

### Research Question
[What question does this address?]

### Background
[Relevant theory and prior research]

### Significance
[Why is this hypothesis important?]

## Hypothesis Details

### Variables
[As described in formulation template above]

### Hypotheses
- **H₀**: [Null hypothesis]
- **H₁**: [Alternative hypothesis]

### Operationalization
[How concepts will be measured]

## Testing Plan

### Study Design
[Experimental design details]

### Sample
- **Target N**: [Sample size]
- **Power Analysis**: [Justification for N]
- **Inclusion/Exclusion Criteria**: [Who qualifies]

### Procedure
[How data will be collected]

### Statistical Analysis
- **Test**: [Statistical test to use]
- **α Level**: [Significance threshold]
- **Effect Size Metric**: [d, η², r, etc.]
- **Software**: [R, Python, SPSS, etc.]

### Assumptions
[Statistical assumptions and how to check them]

## Results

### Data Collection
- **Date**: [When data were collected]
- **Actual N**: [Final sample size]
- **Deviations from Plan**: [Any changes to planned procedure]

### Analysis
[Results as per reporting template above]

### Interpretation
[What results mean for theory and practice]

### Limitations
[Threats to validity, confounds, limitations]

## Follow-Up

### Implications
[What these results suggest for future research]

### Next Steps
[Planned follow-up studies or analyses]
```

## Integration with Task Management

Link hypotheses to tasks:

```json
{
  "id": "42",
  "title": "Test hypothesis H3: Age moderates treatment effect",
  "description": "Conduct moderation analysis to test whether age moderates the relationship between treatment condition and outcome",
  "difficulty": 6,
  "status": "Pending",
  "tags": ["hypothesis-testing", "analysis", "H3"],
  "hypothesis_id": "H3",
  "dependencies": ["41"]
}
```

## Reporting Guidelines

### In Research Papers

#### Methods Section
- State all hypotheses (including those not supported)
- Describe hypothesis formulation process
- Note if pre-registered

#### Results Section
- Report test results for each hypothesis
- Include test statistics, p-values, effect sizes, confidence intervals
- Present negative results, not just significant findings

#### Discussion Section
- Interpret hypothesis test results
- Discuss implications of supported/unsupported hypotheses
- Acknowledge limitations
- Suggest future research based on findings

### Pre-Registration Report

- All hypotheses (primary and secondary)
- Justification for each
- Planned analyses
- Sample size rationale
- Stopping rules

## Resources

### Statistical Power and Sample Size
- G*Power software (free power analysis tool)
- `pwr` package in R
- Effect size conventions (Cohen, 1988)

### Pre-Registration Platforms
- Open Science Framework (osf.io)
- AsPredicted.org
- ClinicalTrials.gov

### Multiple Testing
- Benjamini & Hochberg (1995) - False Discovery Rate
- Holm (1979) - Sequential Bonferroni
- Westfall & Young (1993) - Resampling methods
