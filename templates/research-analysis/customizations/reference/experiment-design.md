# Experiment Design

## Purpose

Templates and patterns for designing rigorous experiments including variable identification, control strategies, methodology documentation, and experimental protocols. This guide helps ensure experiments are well-designed, replicable, and capable of testing hypotheses effectively.

## Why Good Experiment Design Matters

1. **Validity**: Ensures results actually answer your research question
2. **Reliability**: Makes findings replicable by others
3. **Efficiency**: Minimizes wasted resources on flawed studies
4. **Credibility**: Well-designed studies are more likely to be published
5. **Ethics**: Reduces unnecessary risk or burden on participants

---

## Experiment Design Fundamentals

### Key Concepts

**Independent Variable (IV)**:
- Variable manipulated by researcher
- The presumed cause
- Example: Treatment dosage, teaching method, interface design

**Dependent Variable (DV)**:
- Variable measured by researcher
- The presumed effect
- Example: Test scores, recovery time, task completion speed

**Control Variables**:
- Variables held constant across conditions
- Prevents confounding
- Example: Time of day, room temperature, participant age range

**Confounding Variables**:
- Variables that vary with IV and affect DV
- Threaten internal validity
- Must be controlled or measured

**Random Assignment**:
- Participants randomly assigned to conditions
- Ensures groups equivalent before treatment
- Gold standard for causal inference

---

## Common Experimental Designs

### 1. Randomized Controlled Trial (RCT)

**Structure**:
```
Participants → Random Assignment → Treatment Group → Measure Outcome
                                 → Control Group   → Measure Outcome
```

**When to Use**:
- Testing intervention effectiveness
- Causal questions
- Have control over assignment

**Example**:
- IV: New drug (yes/no)
- DV: Symptom severity
- Design: 100 patients randomized to drug or placebo

**Strengths**:
- Strong causal inference
- Controls for confounds
- Clear interpretation

**Limitations**:
- May not be ethical or feasible
- Limited external validity if tightly controlled
- Can be expensive

### 2. Between-Subjects Design

**Structure**:
Different participants in each condition

```
Group A: Condition 1 → Measure
Group B: Condition 2 → Measure
Group C: Condition 3 → Measure
```

**When to Use**:
- Treatment has lasting effects
- Learning/practice effects problematic
- Conditions mutually exclusive

**Example**:
Comparing three teaching methods (lecture, discussion, online) with different classes

**Strengths**:
- No carry-over effects
- Simple analysis

**Limitations**:
- Requires more participants
- Individual differences between groups
- Less statistical power than within-subjects

**Design Considerations**:
- Use random assignment
- Check baseline equivalence
- Consider blocking on key variables

### 3. Within-Subjects Design (Repeated Measures)

**Structure**:
Same participants in all conditions

```
All Participants: Condition 1 → Measure → Condition 2 → Measure → Condition 3 → Measure
```

**When to Use**:
- Limited participants available
- Want to control individual differences
- Conditions don't have lasting effects

**Example**:
Testing reaction time under three noise levels (quiet, moderate, loud) with same participants

**Strengths**:
- Controls for individual differences
- Greater statistical power
- Fewer participants needed

**Limitations**:
- Order/practice effects
- Carry-over effects
- Fatigue or boredom

**Design Considerations**:
- Counterbalance order
- Use washout periods if needed
- Check for order effects

### 4. Mixed Design

**Structure**:
Combines between- and within-subjects factors

```
Group A: Condition 1 → Measure → Condition 2 → Measure
Group B: Condition 1 → Measure → Condition 2 → Measure
```

**When to Use**:
- Multiple factors with different characteristics
- Some variables suit between, others within

**Example**:
- Between: Treatment type (therapy vs. control)
- Within: Time (pre, post, follow-up)

**Strengths**:
- Combines advantages of both designs
- Can test interactions

**Limitations**:
- More complex
- Larger sample size needed
- Complicated analysis

### 5. Factorial Design

**Structure**:
Two or more independent variables

```
2×2 Factorial:
            Factor B: Level 1    Factor B: Level 2
Factor A: 1    Cell 1             Cell 2
Factor A: 2    Cell 3             Cell 4
```

**When to Use**:
- Multiple factors of interest
- Want to test interactions
- Theory predicts interactive effects

**Example**:
- Factor A: Caffeine (yes/no)
- Factor B: Sleep (full/deprived)
- DV: Reaction time

**Strengths**:
- Tests main effects and interactions
- Efficient (two questions with one study)
- Reveals complex relationships

**Limitations**:
- Sample size grows quickly (2×2×2 = 8 cells)
- Difficult to recruit for many cells
- Interpretation complex with higher-order interactions

### 6. Quasi-Experimental Design

**Structure**:
No random assignment (use existing groups)

```
Non-Equivalent Groups:
Group A (non-random) → Treatment → Measure
Group B (non-random) → No Treatment → Measure
```

**When to Use**:
- Random assignment not feasible
- Using existing groups (classes, clinics, etc.)
- Ethical constraints prevent randomization

**Example**:
Comparing two schools using different curricula

**Strengths**:
- Feasible when RCT not possible
- Can still provide useful evidence
- More ecologically valid

**Limitations**:
- Weaker causal inference
- Selection bias possible
- Confounds not controlled

**Design Improvements**:
- Pre-test/post-test
- Matched controls
- Statistical controls
- Multiple comparison groups

### 7. Crossover Design

**Structure**:
Participants receive all treatments in sequence

```
Group A: Treatment 1 → Washout → Treatment 2 → Measure
Group B: Treatment 2 → Washout → Treatment 1 → Measure
```

**When to Use**:
- Chronic conditions where each participant can receive both treatments
- Treatments reversible
- Want within-subject control

**Example**:
Testing two pain medications with washout period between

**Strengths**:
- Each participant is own control
- Powerful
- Fewer participants needed

**Limitations**:
- Requires reversible conditions
- Carry-over effects possible
- Takes longer

---

## Experiment Design Template

Create a file for each experiment: `research/experiments/exp_[name].md`

```markdown
# Experiment: [Experiment Name]

## Research Question

**Primary Question**:
[What you want to find out]

**Secondary Questions**:
- [Additional question 1]
- [Additional question 2]

## Hypotheses

**Primary Hypothesis**:
[Main prediction, linked to research question]

**Secondary Hypotheses**:
- H1: [Hypothesis 1]
- H2: [Hypothesis 2]

## Design Overview

**Design Type**: [RCT / Between-subjects / Within-subjects / Mixed / Factorial / Quasi-experimental / Crossover]

**Design Diagram**:
```
[Visual representation of design]
```

## Variables

### Independent Variable(s)

**IV1: [Variable Name]**
- **Type**: [Manipulated / Measured]
- **Levels**: [e.g., Control, Treatment A, Treatment B]
- **Operationalization**: [How you will implement/manipulate this]
- **Justification**: [Why these levels]

**IV2: [If factorial]**
- **Type**: [Manipulated / Measured]
- **Levels**: [List levels]
- **Operationalization**: [How implemented]

### Dependent Variable(s)

**DV1: [Variable Name]**
- **Operationalization**: [How you will measure this]
- **Measurement Tool**: [Scale, instrument, device]
- **Scale**: [Continuous, ordinal, nominal; range]
- **Reliability**: [Expected reliability, if known]
- **Validity**: [Evidence for validity]

**DV2: [If multiple]**
- [Same structure as DV1]

### Control Variables

| Variable | How Controlled | Rationale |
|----------|----------------|-----------|
| Age | Restrict to 18-65 | Developmental differences |
| Time of day | All sessions 9am-12pm | Circadian effects |
| Environment | Same lab room | Standardize conditions |

### Potential Confounds

| Confound | Risk Level | Mitigation Strategy |
|----------|------------|---------------------|
| Motivation | Medium | Random assignment, measure baseline motivation |
| Prior experience | High | Screen participants, statistical control |
| Experimenter effects | Low | Single blinded procedure |

## Participants

**Population**: [Target population]

**Sample Size**:
- **Planned N**: [Number, per condition if applicable]
- **Power Analysis**: [Power, effect size expected, alpha level]
  - Expected effect size: [d = X or r = X based on prior research]
  - Power: [Typically .80]
  - Alpha: [Typically .05]
  - Required N: [From power analysis]

**Recruitment**:
- **Method**: [How you will recruit - ads, participant pool, etc.]
- **Eligibility Criteria**:
  - Inclusion: [Who can participate]
  - Exclusion: [Who cannot participate]

**Compensation**: [Payment, course credit, etc.]

## Procedure

**Timeline**:
```
Session 1 (Day 1): Consent → Pre-test → Treatment → Post-test (60 min)
Session 2 (Day 8): Follow-up measure (20 min)
```

**Detailed Steps**:

1. **Recruitment and Screening** (1 week before):
   - [Recruitment method]
   - [Screening criteria]
   - [Schedule sessions]

2. **Pre-Session Preparation**:
   - [Materials to prepare]
   - [Room setup]
   - [Randomization]

3. **Session Flow**:

   **A. Welcome and Consent** (5 min):
   - Greet participant
   - Review informed consent
   - Answer questions
   - Obtain signature

   **B. Pre-test** (10 min):
   - [Baseline measures]
   - [Instructions to participant]

   **C. Treatment/Manipulation** (30 min):
   - [Describe what happens in each condition]
   - **Control Condition**: [Exactly what participants do/receive]
   - **Treatment Condition**: [Exactly what participants do/receive]

   **D. Post-test** (10 min):
   - [Outcome measures]
   - [Same as pre-test or different?]

   **E. Debrief** (5 min):
   - [Explain purpose]
   - [Answer questions]
   - [Thank participant]

4. **Follow-up** (if applicable):
   - [When and how]

## Materials

**Equipment**:
- [List all equipment needed]

**Stimuli**:
- [Describe or link to stimuli]

**Questionnaires/Scales**:
- [List all measures]
- [Include sample items]

**Other Materials**:
- Informed consent form
- Demographic questionnaire
- Debrief form

## Randomization and Blinding

**Randomization**:
- **Method**: [Simple random, block randomization, stratified, etc.]
- **Implementation**: [Random number generator, sealed envelopes, etc.]
- **Stratification**: [If blocking on any variables]

**Blinding**:
- **Participants**: [Blinded / Not blinded - explain]
- **Experimenters**: [Blinded / Not blinded - explain]
- **Analysts**: [Blinded / Not blinded - explain]

## Data Collection

**What Will Be Collected**:
- Demographic data
- Pre-test scores
- Treatment/condition assignment
- Post-test scores
- Additional measures: [list]

**How Recorded**:
- [Paper forms / Computer / Automated device]

**Data Management**:
- **Storage**: [Where data will be stored]
- **Backup**: [Backup procedures]
- **Security**: [De-identification, encryption, access control]

**Data Quality**:
- [Real-time checks during collection]
- [Validation procedures]

## Statistical Analysis Plan

**Primary Analysis**:
- **Test**: [e.g., Independent t-test, ANOVA, regression]
- **Comparison**: [Which groups/conditions compared]
- **Assumptions**: [What you'll check]
- **Alpha level**: [Typically .05]

**Secondary Analyses**:
- [Additional tests for secondary hypotheses]

**Exploratory Analyses**:
- [Analyses not prespecified]

**Handling Missing Data**:
- [Deletion / Imputation / Other]

**Handling Outliers**:
- [Criteria for outliers]
- [How handled - kept, removed, winsorized]

**Multiple Comparisons**:
- [If testing multiple hypotheses, adjustment method]

**Effect Sizes**:
- [Which effect size measures will be reported]

## Pilot Study

**Pilot Plan**:
- **N**: [Small sample to test procedures]
- **Purpose**: [What you want to learn from pilot]
- **Modifications**: [How pilot results will inform main study]

**Pilot Results**:
[After running pilot, document what you learned and changes made]

## Ethics and Safety

**IRB Status**: [Not yet submitted / Submitted / Approved - date]

**Risks**:
- [Potential risks to participants]
- [How minimized]

**Benefits**:
- [Direct benefits to participants]
- [Societal benefits]

**Confidentiality**:
- [How participant privacy protected]

**Informed Consent**:
- [What participants will be told]
- [Deception if any, with justification]

**Debriefing**:
- [What participants will learn after study]

**Right to Withdraw**:
- [Participants can withdraw anytime without penalty]

## Timeline

| Phase | Dates | Status |
|-------|-------|--------|
| Design experiment | [dates] | [Complete/In progress] |
| IRB submission | [dates] | [Complete/Planned] |
| Pilot study | [dates] | [Complete/Planned] |
| Recruitment | [dates] | [Planned] |
| Data collection | [dates] | [Planned] |
| Data analysis | [dates] | [Planned] |
| Write-up | [dates] | [Planned] |

## Limitations and Threats to Validity

### Internal Validity Threats

| Threat | Risk | How Addressed |
|--------|------|---------------|
| Selection bias | [Low/Med/High] | [Random assignment] |
| History | [Low/Med/High] | [Control group] |
| Maturation | [Low/Med/High] | [Short study duration] |
| Testing effects | [Low/Med/High] | [Alternate forms] |
| Instrumentation | [Low/Med/High] | [Standardized measures] |
| Regression to mean | [Low/Med/High] | [No selection on extremes] |
| Attrition | [Low/Med/High] | [Short study, compensation] |

### External Validity Threats

| Threat | Risk | How Addressed |
|--------|------|---------------|
| Sample representativeness | [Low/Med/High] | [Diverse recruitment] |
| Setting artificiality | [Low/Med/High] | [Justify as acceptable] |
| Demand characteristics | [Low/Med/High] | [Deception, blinding] |
| Experimenter effects | [Low/Med/High] | [Standardized protocol] |

### Construct Validity

- **IV construct validity**: [Does manipulation capture intended construct?]
- **DV construct validity**: [Does measure capture intended construct?]

### Statistical Conclusion Validity

- **Power**: [Adequate sample size via power analysis]
- **Assumptions**: [Check and report]
- **Fishing**: [Prespecified hypotheses]

## Expected Results

**Predicted Outcome**:
[What you expect to find if hypothesis supported]

**Alternative Outcomes**:
- [What if null result?]
- [What if opposite direction?]
- [What if interaction in factorial?]

**Decision Rules**:
- [What results would lead to rejecting/accepting hypothesis]

## References

[Key references informing this design, prior similar studies]

## Appendices

- Appendix A: Informed consent form
- Appendix B: Experimental stimuli
- Appendix C: Questionnaires
- Appendix D: Debrief form

## Notes

[Any additional notes, decisions made, changes from original plan]
```

---

## Design Checklist

### Before Finalizing Design

**Conceptual**:
- [ ] Research question clearly defined
- [ ] Hypotheses testable
- [ ] Variables operationalized
- [ ] IV actually manipulates intended construct
- [ ] DV actually measures intended construct
- [ ] Confounds identified and addressed

**Methodological**:
- [ ] Design matches research question
- [ ] Adequate sample size (power analysis)
- [ ] Randomization plan specified
- [ ] Control condition appropriate
- [ ] Blinding plan specified
- [ ] Measures reliable and valid
- [ ] Procedure standardized

**Practical**:
- [ ] Feasible to recruit participants
- [ ] Materials available or obtainable
- [ ] Equipment available
- [ ] Timeline realistic
- [ ] Budget adequate
- [ ] Ethics approval plan

**Analysis**:
- [ ] Analysis plan specified
- [ ] Assumptions can be checked
- [ ] Alternative analyses planned
- [ ] Effect sizes will be reported
- [ ] Missing data plan specified

**Documentation**:
- [ ] Protocol written clearly
- [ ] Replicable by others
- [ ] Preregistration considered
- [ ] IRB materials prepared

---

## Common Pitfalls to Avoid

1. **Inadequate Power**: Pilot too small to detect meaningful effect
2. **Confounds Not Controlled**: Alternative explanations for results
3. **Weak Manipulation**: IV doesn't actually vary enough
4. **Poor Measures**: DV unreliable or invalid
5. **No Manipulation Check**: Don't verify IV worked
6. **Selection Bias**: Non-random assignment allows confounds
7. **Experimenter Bias**: Expectations influence results
8. **Demand Characteristics**: Participants guess hypothesis and comply
9. **Attrition**: Differential dropout threatens validity
10. **Fishing Expeditions**: Testing many things without plan

---

## Improving Experimental Rigor

### Manipulation Checks

**Purpose**: Verify IV manipulation worked as intended

**Example**:
- IV: Stress manipulation (high/low stress)
- Manipulation check: "How stressed do you feel?" (1-10 scale)
- Analysis: Verify high-stress group reports more stress

### Attention Checks

**Purpose**: Ensure participants paying attention

**Example**:
- Embedded items: "For this question, please select 'Strongly Agree'"
- Consistency checks: Ask same question twice
- Timing checks: Flag impossibly fast responses

### Pilot Testing

**What to Pilot**:
- Procedure clarity
- Materials comprehensibility
- Timing
- Manipulation effectiveness
- Measure sensitivity

**How**:
- Small N (5-10)
- Think-aloud protocol
- Debrief thoroughly
- Revise based on feedback

---

## Statistical Power Analysis

**Why Needed**:
- Ensure adequate sample to detect effect
- Avoid wasting resources on underpowered study
- Ethical obligation not to burden participants needlessly

**Inputs**:
1. **Expected effect size**: From prior research or smallest effect of interest
2. **Alpha level**: Typically .05
3. **Desired power**: Typically .80 (80% chance of detecting effect if it exists)
4. **Test type**: t-test, ANOVA, regression, etc.

**Example**:
```
Design: Independent t-test
Expected effect: d = 0.50 (medium)
Alpha: .05
Power: .80

Required N: 64 per group (128 total)
```

**Tools**:
- G*Power (free software)
- R: `pwr` package
- Online calculators

**What if No Prior Effect Size?**:
- Use smallest effect of practical interest
- Convention: small (d=.20), medium (d=.50), large (d=.80)
- Better to overestimate needed N than underestimate

---

## Control Strategies

### Randomization

**Simple Random Assignment**:
- Coin flip, random number generator
- Each participant has equal chance

**Block Randomization**:
- Ensure equal N across conditions
- Randomize within blocks
- Example: AABB, ABBA, BABA, ABAB

**Stratified Randomization**:
- Balance on key variable
- Randomize within strata
- Example: Randomize males and females separately

### Matching

**Purpose**: Create equivalent groups on key variable

**Types**:
- Matched pairs: Match participants 1:1, assign to different conditions
- Matched groups: Ensure groups have same distribution on variable

**Example**:
Match on baseline severity, then randomize to treatment/control

### Counterbalancing

**Purpose**: Control for order effects in within-subjects designs

**Complete Counterbalancing**:
All possible orders represented

**Example** (3 conditions):
- ABC, ACB, BAC, BCA, CAB, CBA

**Partial Counterbalancing**:
Latin square - each condition appears in each position once

**Example** (4 conditions):
- ABCD
- BCDA
- CDAB
- DABC

### Blinding

**Single-Blind**: Participants don't know condition
**Double-Blind**: Participants and experimenters don't know
**Triple-Blind**: Add data analysts

**When Blinding Not Possible**:
- Standardize procedures
- Use objective measures
- Analyze data blind to condition (coded)

---

## Reporting Experiments

**CONSORT Statement** (for RCTs):
Checklist of what to report in trial publications

**Key Elements**:
1. **Design**: Describe experimental design
2. **Participants**: Recruitment, eligibility, assignment
3. **Interventions**: Detailed description of conditions
4. **Outcomes**: All measures specified
5. **Sample Size**: Justification and power
6. **Randomization**: Sequence generation and concealment
7. **Blinding**: Who was blinded
8. **Flow**: CONSORT diagram showing participant flow
9. **Results**: For all outcomes
10. **Limitations**: Threats to validity

---

## File Organization

```
research/
└── experiments/
    ├── exp_feedback_study/
    │   ├── design.md              # This template
    │   ├── protocol.md            # Step-by-step procedure
    │   ├── materials/
    │   │   ├── consent_form.pdf
    │   │   ├── stimuli/
    │   │   ├── questionnaires/
    │   │   └── debrief.pdf
    │   ├── analysis_plan.md       # Prespecified analyses
    │   └── pilot_results.md       # Pilot findings
    └── exp_retention_study/
        └── [same structure]
```

---

## Resources

### Design Guides
- Shadish, Cook, & Campbell (2002): Experimental and Quasi-Experimental Designs
- Field & Hole (2003): How to Design and Report Experiments

### Power Analysis
- G*Power: Free power analysis software
- R `pwr` package
- Online calculators (various)

### Reporting Standards
- CONSORT: RCT reporting guidelines
- JARS: APA reporting standards
- TREND: Quasi-experimental designs

### Ethics
- Belmont Report: Ethical principles
- IRB guidelines: Institutional requirements

### Preregistration
- OSF: Open Science Framework
- AsPredicted: Quick preregistration
- ClinicalTrials.gov: Required for trials
