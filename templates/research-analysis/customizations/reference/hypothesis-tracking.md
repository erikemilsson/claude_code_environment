# Hypothesis Tracking

## Purpose

Patterns and templates for tracking research hypotheses including formulation, testing criteria, evidence collection, validation status, and decision-making throughout the research process.

## Why Track Hypotheses?

1. **Maintains Focus**: Keeps research aligned with original questions
2. **Prevents HARKing**: Documents hypotheses before data analysis (Hypothesizing After Results Known)
3. **Shows Process**: Demonstrates scientific rigor and transparency
4. **Tracks Evolution**: Records how thinking developed through research
5. **Enables Preregistration**: Facilitates formal preregistration of studies
6. **Prevents Bias**: Reduces confirmation bias and p-hacking

---

## Hypothesis Formulation

### Components of a Good Hypothesis

1. **Testable**: Can be empirically evaluated
2. **Falsifiable**: Can be proven wrong
3. **Specific**: Clear variables and relationships
4. **Grounded**: Based on theory or prior evidence
5. **Directional** (when appropriate): Specifies expected direction of effect

### Hypothesis Structure

**Basic Format**:
```
If [independent variable], then [dependent variable] because [theoretical rationale].
```

**Example**:
```
If students receive personalized feedback, then their test scores will improve because tailored guidance addresses individual knowledge gaps.
```

**Alternative Format (Correlational)**:
```
[Variable A] is [positively/negatively/not] related to [Variable B].
```

**Example**:
```
Study time is positively related to exam performance.
```

### Types of Hypotheses

**Null Hypothesis (H₀)**:
- States no effect or no difference
- What you attempt to reject
- Example: "There is no difference in test scores between Group A and Group B"

**Alternative Hypothesis (H₁ or Hₐ)**:
- States expected effect or difference
- What you hope to support
- Example: "Group A will have higher test scores than Group B"

**Directional Hypothesis**:
- Specifies direction of effect (greater than, less than)
- Example: "Treatment A will produce faster recovery than Treatment B"
- Use when theory strongly predicts direction

**Non-Directional Hypothesis**:
- States effect exists but not direction
- Example: "There is a difference in effectiveness between Treatment A and Treatment B"
- Use when direction uncertain

---

## Hypothesis Tracking Template

### Individual Hypothesis Document

Create a file for each hypothesis: `research/hypotheses/H1_[brief-description].md`

```markdown
# Hypothesis 1: [Brief Title]

## Hypothesis Statement

**Formal Statement**:
[Full hypothesis statement]

**Null Hypothesis (H₀)**:
[Null hypothesis]

**Alternative Hypothesis (H₁)**:
[Alternative hypothesis]

**Type**: [Directional / Non-directional]

## Variables

**Independent Variable(s)**:
- Name: [Variable name]
- Operationalization: [How measured]
- Levels/Range: [Categories or range of values]

**Dependent Variable(s)**:
- Name: [Variable name]
- Operationalization: [How measured]
- Measurement: [Scale, units, instrument]

**Control Variables**:
- [Variable 1]: [Why controlled]
- [Variable 2]: [Why controlled]

## Theoretical Basis

**Background Theory**:
[Theory or framework supporting this hypothesis]

**Prior Evidence**:
- Study 1: [Citation] - [Finding]
- Study 2: [Citation] - [Finding]

**Rationale**:
[Why you expect this relationship]

## Testing Plan

**Sample**:
- Population: [Target population]
- Sample size: [Planned N, with power analysis justification]
- Sampling method: [Random, convenience, stratified, etc.]

**Procedure**:
[Brief description of data collection procedure]

**Statistical Test**:
- Primary test: [e.g., independent t-test, ANOVA, regression]
- Assumptions to check: [Normality, homogeneity of variance, etc.]
- Significance level: α = [typically 0.05]
- Effect size measure: [Cohen's d, r, eta-squared, etc.]

**Alternative Analyses**:
[Backup plan if assumptions violated, e.g., non-parametric alternatives]

## Evidence Collected

**Data Source**:
[Where data comes from]

**Date Collected**:
[When data was collected]

**Sample Characteristics**:
- Actual N: [Number of participants/observations]
- [Key demographics or characteristics]

## Results

**Statistical Results**:
- Test statistic: [e.g., t(98) = 2.45]
- p-value: [e.g., p = .016]
- Effect size: [e.g., d = 0.50]
- Confidence interval: [e.g., 95% CI [0.15, 0.85]]

**Interpretation**:
[What the statistical results mean]

**Supporting Evidence**:
- Descriptive statistics: [Means, SDs by group]
- Visualizations: [Reference to figures]
- Additional analyses: [Sensitivity analyses, subgroup analyses]

## Decision

**Status**: [Supported / Not Supported / Inconclusive]

**Decision Rationale**:
[Why you reached this conclusion]

**Confidence**:
[High / Medium / Low - based on effect size, consistency, sample size, etc.]

**Caveats**:
[Limitations affecting interpretation]

## Implications

**Theoretical Implications**:
[What this means for theory]

**Practical Implications**:
[Real-world applications or relevance]

**Future Research**:
[What questions this raises]

## Timeline

- Formulated: [Date]
- Preregistered: [Date, if applicable]
- Data collection: [Date range]
- Analysis completed: [Date]
- Decision made: [Date]

## Related Hypotheses

- Hypothesis 2: [How related]
- Hypothesis 3: [How related]

## Notes

[Any additional notes, unexpected findings, methodological issues, etc.]
```

---

## Hypothesis Tracking Spreadsheet

For quick overview, maintain a summary spreadsheet: `research/hypotheses/hypothesis_tracker.xlsx`

| ID | Hypothesis | Variables (IV → DV) | Type | Status | Result | p-value | Effect Size | Notes |
|----|------------|---------------------|------|--------|--------|---------|-------------|-------|
| H1 | Treatment improves outcomes | Treatment → Outcome | Directional | Tested | Supported | .016 | d=0.50 | As predicted |
| H2 | Age moderates effect | Age × Treatment → Outcome | Non-dir | Tested | Not Supported | .234 | η²=0.02 | Weak moderation |
| H3 | Gender differences exist | Gender → Outcome | Non-dir | Pending | - | - | - | Data collection ongoing |

**Columns Explained**:
- **ID**: Unique identifier (H1, H2, H3...)
- **Hypothesis**: Brief statement
- **Variables**: Independent → Dependent variable(s)
- **Type**: Directional, Non-directional, Exploratory
- **Status**: Formulated, Preregistered, Data Collected, Tested, Reported
- **Result**: Supported, Not Supported, Inconclusive, Mixed
- **p-value**: Statistical significance
- **Effect Size**: Magnitude of effect
- **Notes**: Brief comments

---

## Hypothesis Status Values

### Formulation Stage

**Formulated**:
- Hypothesis written
- Variables identified
- Rationale documented
- Not yet tested

**Refined**:
- Revised based on feedback
- Variables clarified
- Methods improved

**Preregistered**:
- Formally registered (OSF, AsPredicted, clinical trial registry)
- Timestamped commitment to testing
- Analysis plan specified

### Testing Stage

**Data Collection in Progress**:
- Currently gathering data
- Testing not yet performed

**Data Collection Complete**:
- All data collected
- Ready for analysis

**Under Analysis**:
- Statistical tests being performed
- Results being validated

**Tested**:
- Analysis complete
- Results available
- Decision not yet final

### Decision Stage

**Supported**:
- Results consistent with hypothesis
- Statistically significant in predicted direction
- Effect size meaningful

**Not Supported**:
- Results inconsistent with hypothesis
- Not statistically significant, or
- Significant in opposite direction

**Inconclusive**:
- Results ambiguous
- Insufficient power
- Methodological issues prevent clear conclusion

**Mixed**:
- Some evidence supporting, some contradicting
- Depends on subgroup or conditions
- Effect present but complex

**Abandoned**:
- No longer relevant
- Replaced by better formulation
- Data collection not feasible

### Reporting Stage

**Reported**:
- Included in manuscript/report
- Findings communicated

**Published**:
- Appeared in peer-reviewed publication
- Publicly available

---

## Workflow Integration

### 1. Before Data Collection

```markdown
## Hypothesis Checklist (Formulation)

- [ ] Hypothesis clearly stated
- [ ] Variables operationalized
- [ ] Theoretical basis documented
- [ ] Testing method identified
- [ ] Statistical power adequate (power analysis)
- [ ] Confounds identified and controlled
- [ ] Preregistration considered (if appropriate)
```

**Deliverables**:
- Hypothesis document created
- Added to tracking spreadsheet
- Status: "Formulated" or "Preregistered"

### 2. During Data Collection

**Monitor**:
- Track sample size progress
- Note any deviations from protocol
- Record unexpected observations
- Update status in tracker

**Update**:
- Status → "Data Collection in Progress"
- Expected completion date
- Actual N enrolled

### 3. During Analysis

**Process**:
1. Check planned analysis approach
2. Verify assumptions
3. Run statistical tests
4. Calculate effect sizes
5. Interpret results objectively

**Document**:
- Update hypothesis file with results
- Add statistical details to tracker
- Create visualizations
- Note any surprises

**Update**:
- Status → "Under Analysis" → "Tested"
- Add p-value, effect size to tracker

### 4. Making Decision

**Decision Criteria**:

1. **Statistical Significance**:
   - p < α (typically 0.05)
   - Direction matches prediction (if directional)

2. **Effect Size**:
   - Small: Supported but weak
   - Medium: Supported
   - Large: Strongly supported

3. **Confidence Interval**:
   - Does not include zero (for differences)
   - Narrow CI: Higher confidence

4. **Robustness**:
   - Consistent across sensitivity analyses
   - Assumptions met or results hold with alternatives

**Final Status Assignment**:
- Consider all evidence holistically
- Document rationale for decision
- Note confidence level
- Acknowledge limitations

**Update**:
- Status → "Supported" / "Not Supported" / etc.
- Result column in tracker
- Confidence level noted

### 5. Reporting

**Inclusion in Report/Manuscript**:
- Report all tested hypotheses (not just significant ones)
- Include effect sizes and confidence intervals
- Describe surprising or null findings
- Discuss implications

**Update**:
- Status → "Reported" or "Published"
- Add manuscript citation when published

---

## Best Practices

### Do's

1. **Formulate Before Seeing Data**: Avoid HARKing
2. **Be Specific**: Vague hypotheses are untestable
3. **Document Rationale**: Explain why you expect this result
4. **Track Everything**: Include hypotheses not supported
5. **Preregister**: When feasible, formally register predictions
6. **Update Promptly**: Keep tracker current
7. **Include Effect Sizes**: Statistical significance alone insufficient
8. **Consider Alternatives**: What if results differ from expectation?
9. **Report All Tests**: Including non-significant results
10. **Revise Thoughtfully**: If refining hypothesis, document changes

### Don'ts

1. **Don't HARK**: Don't present post-hoc findings as hypotheses
2. **Don't P-Hack**: Don't try multiple analyses until p < .05
3. **Don't Cherry-Pick**: Don't report only supported hypotheses
4. **Don't Overstate**: Supported ≠ proven
5. **Don't Ignore Effect Size**: Small effects may be statistically significant but not meaningful
6. **Don't Skip Null Results**: Non-findings are findings
7. **Don't Change Hypotheses Post-Hoc**: Revisions should be documented
8. **Don't Treat Exploratory as Confirmatory**: Label clearly
9. **Don't Forget Assumptions**: Check before interpreting results
10. **Don't Work Backward**: From data to hypothesis = HARKing

---

## Preregistration

### What is Preregistration?

Timestamped, public commitment to:
- Research questions and hypotheses
- Study design and methods
- Planned sample size
- Analysis plan

**Benefits**:
- Prevents HARKing
- Distinguishes confirmatory from exploratory
- Increases credibility
- Protects against bias

### When to Preregister

**Strongly Recommended**:
- Clinical trials (often required)
- Hypothesis-driven confirmatory research
- Studies with potential for bias
- Research with policy implications

**Less Critical**:
- Purely exploratory research
- Secondary data analysis (mark as exploratory)
- Pilot studies

### Where to Preregister

**Open Science Framework (OSF)**:
- osf.io/registries
- Free and widely used
- Embargoed option (keep private until publication)

**AsPredicted**:
- aspredicted.org
- Simple 9-question format
- Quick and easy

**Clinical Trial Registries**:
- ClinicalTrials.gov (US)
- EU Clinical Trials Register
- Required for clinical trials

**Field-Specific Registries**:
- PROSPERO (systematic reviews)
- Registered Reports (journals)

### What to Include in Preregistration

1. **Hypotheses**: All hypotheses, clearly stated
2. **Variables**: How IV and DV will be measured
3. **Sample**: Target N, inclusion/exclusion criteria
4. **Procedure**: Data collection methods
5. **Analysis Plan**: Statistical tests, handling of outliers, missing data
6. **Decision Criteria**: What results would support/refute hypothesis

---

## Exploratory vs. Confirmatory

### Confirmatory Hypotheses

**Characteristics**:
- Formulated before data collection
- Based on theory or prior research
- Specific prediction
- Hypothesis test planned in advance

**Reporting**:
- Label as "confirmatory"
- Report exact p-values
- Include effect sizes and CIs
- Strong basis for conclusions

### Exploratory Analyses

**Characteristics**:
- Emerged during or after data collection
- Not prespecified
- Data-driven observations
- Hypothesis-generating

**Reporting**:
- Clearly label as "exploratory"
- Valuable for future research
- Requires replication for confirmation
- Cannot make strong causal claims

**Both are Valuable**:
- Confirmatory: Tests existing theory
- Exploratory: Generates new ideas
- Be transparent about which is which

---

## Example Hypothesis Tracker Entry

```markdown
# Hypothesis 3: Personalized Feedback Improves Learning

## Hypothesis Statement

**Alternative Hypothesis (H₁)**:
Students who receive personalized feedback will achieve higher test scores than students who receive generic feedback.

**Null Hypothesis (H₀)**:
There is no difference in test scores between students receiving personalized versus generic feedback.

**Type**: Directional

## Variables

**Independent Variable**: Feedback Type
- Operationalization: Random assignment to personalized or generic feedback
- Levels: Personalized, Generic

**Dependent Variable**: Test Score
- Operationalization: Final exam score (0-100 scale)
- Measurement: Standardized multiple-choice exam

**Control Variables**:
- Prior knowledge: Pre-test score
- Study time: Self-reported hours
- Class section: Controlled via randomization

## Theoretical Basis

**Background Theory**:
Cognitive load theory and personalized learning theory suggest that tailored feedback reduces cognitive load and addresses individual knowledge gaps more effectively than generic feedback.

**Prior Evidence**:
- Smith et al. (2022): Found d = 0.42 effect of personalized feedback
- Jones & Lee (2021): Meta-analysis showed mean effect r = .28

**Rationale**:
Personalized feedback directly addresses each student's specific errors and misconceptions, enabling more efficient learning than generic feedback that may not address individual needs.

## Testing Plan

**Sample**:
- Population: Undergraduate students in Intro Psychology
- Sample size: N = 120 (power = .80 to detect d = 0.50 at α = .05)
- Sampling: Random assignment within class sections

**Procedure**:
Students complete pre-test, receive feedback (personalized or generic) on practice problems, then complete final exam.

**Statistical Test**:
- Primary: Independent samples t-test
- Assumptions: Normality (Shapiro-Wilk), homogeneity of variance (Levene's)
- Significance level: α = .05 (two-tailed, though directional expected)
- Effect size: Cohen's d

**Alternative Analyses**:
If assumptions violated: Mann-Whitney U test
Planned: ANCOVA controlling for pre-test scores

## Results

**Statistical Results**:
- t(118) = 2.87, p = .005, 95% CI [0.15, 0.85]
- Cohen's d = 0.53 (medium effect)
- Personalized: M = 78.3 (SD = 12.1), Generic: M = 71.9 (SD = 13.4)

**Interpretation**:
Students receiving personalized feedback scored significantly higher (6.4 points on average) than those receiving generic feedback.

**Supporting Evidence**:
- Effect consistent when controlling for pre-test scores (ANCOVA)
- Sensitivity analysis excluding outliers: similar results
- No assumption violations detected

## Decision

**Status**: Supported

**Rationale**:
Results statistically significant in predicted direction with medium effect size. Findings consistent with theory and prior research. Robust across sensitivity analyses.

**Confidence**: High

**Caveats**:
- Single course context; generalizability unclear
- Self-selection into undergraduate psychology possible
- Short-term retention only (no long-term follow-up)

## Implications

**Theoretical**: Supports personalized learning theory
**Practical**: Instructors should consider personalized feedback where feasible
**Future Research**: Test in other domains, examine long-term retention, investigate optimal personalization methods

## Timeline

- Formulated: 2024-01-15
- Preregistered: 2024-01-20 (OSF)
- Data collection: 2024-02-01 to 2024-03-15
- Analysis completed: 2024-03-20
- Decision made: 2024-03-22

## Related Hypotheses

- H4: Effect moderated by prior knowledge (tested, not supported)
- H5: Effect mediated by engagement (exploratory, positive correlation)
```

---

## Common Pitfalls

1. **Vague Hypotheses**: "X affects Y" - Be specific about direction and magnitude
2. **Untestable Hypotheses**: Cannot be empirically evaluated
3. **Too Many Hypotheses**: Increases multiple comparison problem
4. **Post-Hoc Hypotheses**: Treating exploratory findings as confirmatory
5. **Ignoring Null Results**: Only reporting supported hypotheses
6. **Confusing Association and Causation**: Observational data cannot prove causation
7. **Fishing Expeditions**: Testing everything until something is significant

---

## File Organization

```
research/
└── hypotheses/
    ├── hypothesis_tracker.xlsx       # Summary spreadsheet
    ├── preregistration.md            # Preregistration document (if used)
    ├── H1_feedback_improves_learning.md
    ├── H2_prior_knowledge_moderates.md
    ├── H3_engagement_mediates.md
    └── exploratory_findings.md       # Post-hoc findings for future testing
```

---

## Resources

### Preregistration Platforms
- Open Science Framework: https://osf.io/
- AsPredicted: https://aspredicted.org/
- ClinicalTrials.gov: https://clinicaltrials.gov/

### Guides
- Center for Open Science preregistration guide
- "Preregistration: A Plan, Not a Prison" (Nosek et al., 2019)
- JARS (Journal Article Reporting Standards) - APA

### Tools
- Power analysis: G*Power, R pwr package
- Effect size calculators: Online tools, R effectsize package
