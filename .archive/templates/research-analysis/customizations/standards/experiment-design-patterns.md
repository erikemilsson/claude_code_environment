# Experiment Design Patterns

## Overview

This document provides templates and standards for designing rigorous experiments across different research contexts. A well-designed experiment maximizes internal validity (causal inference) while maintaining practical feasibility and ethical standards.

## Core Design Principles

### Internal Validity

Confidence that the independent variable caused changes in the dependent variable.

**Threats to Internal Validity**:
- **History**: Events outside the experiment affecting results
- **Maturation**: Natural changes in participants over time
- **Testing**: Practice effects from repeated measurement
- **Instrumentation**: Changes in measurement tools or procedures
- **Regression to Mean**: Extreme scores moving toward average
- **Selection Bias**: Non-random group assignment creating differences
- **Attrition**: Differential dropout between groups

### External Validity

Generalizability of findings to other populations, settings, and times.

**Considerations**:
- Sample representativeness
- Ecological validity (realistic settings)
- Multiple populations and contexts
- Temporal validity (stability over time)

### Construct Validity

How well the operationalization captures the theoretical construct.

**Questions**:
- Does the manipulation actually manipulate the intended variable?
- Does the measure actually measure the intended construct?
- Are there confounding variables?

### Statistical Conclusion Validity

Appropriateness of statistical inferences.

**Considerations**:
- Adequate statistical power
- Appropriate statistical tests
- Assumption violations
- Multiple testing corrections
- Effect size reporting

## Experimental Design Types

### 1. Randomized Controlled Trial (RCT)

**Gold standard** for causal inference; random assignment to treatment/control.

#### Basic RCT Structure

```
Participants
    ↓ (Random Assignment)
    ├─→ Treatment Group → Outcome Measurement
    └─→ Control Group → Outcome Measurement
```

#### Design Template

```markdown
## RCT Design: [Experiment Title]

### Research Question
[What causal question does this answer?]

### Hypothesis
- **H₀**: [No treatment effect]
- **H₁**: [Expected treatment effect]

### Participants
- **Target Population**: [Who this applies to]
- **Sampling Method**: [How recruited]
- **Sample Size**: N = [number] ([power analysis justification])
- **Inclusion Criteria**: [Who can participate]
- **Exclusion Criteria**: [Who cannot participate]

### Design Type
- **Structure**: [Parallel groups / Crossover / Factorial]
- **Randomization**: [Simple / Stratified / Block / Cluster]
- **Blinding**: [None / Single-blind / Double-blind / Triple-blind]

### Intervention
- **Treatment Group**: [What they receive]
  - **Dosage/Intensity**: [Amount/frequency]
  - **Duration**: [How long]
  - **Delivery**: [How administered]
- **Control Group**: [What they receive]
  - **Type**: [No treatment / Placebo / Active control / Wait-list]

### Outcome Measures
- **Primary Outcome**: [Main outcome of interest]
  - **Measurement**: [How measured]
  - **Timing**: [When measured]
- **Secondary Outcomes**: [Additional outcomes]

### Procedure
1. [Recruitment and screening]
2. [Baseline assessment]
3. [Randomization]
4. [Intervention delivery]
5. [Post-intervention assessment]
6. [Follow-up (if applicable)]

### Statistical Analysis
- **Primary Analysis**: [Test for main effect]
- **Secondary Analyses**: [Additional tests]
- **Interim Analyses**: [Planned stopping rules, if any]

### Ethical Considerations
- **IRB Approval**: [Status]
- **Informed Consent**: [Process]
- **Risks**: [Potential harms]
- **Benefits**: [Potential benefits]
- **Withdrawal**: [Right to withdraw]
```

#### Randomization Methods

**Simple Randomization**:
- Coin flip or random number generator for each participant
- Pros: Truly random, simple
- Cons: May create unequal group sizes, especially with small N

**Block Randomization**:
- Randomize within blocks (e.g., blocks of 4: 2 treatment, 2 control)
- Pros: Ensures equal group sizes
- Cons: Allocation can become predictable

**Stratified Randomization**:
- Randomize within strata (e.g., age groups, sex)
- Pros: Ensures balanced groups on key variables
- Cons: More complex, requires knowing stratification variables upfront

**Cluster Randomization**:
- Randomize groups (schools, clinics) rather than individuals
- Pros: Practical when individual randomization not feasible
- Cons: Reduced statistical power, need cluster-adjusted analysis

#### Blinding Strategies

**Single-Blind**: Participants don't know their assignment
**Double-Blind**: Participants and experimenters don't know
**Triple-Blind**: Participants, experimenters, and data analysts don't know

**Blinding Checks**: Assess whether blinding was successful by asking participants/experimenters to guess assignments

### 2. Crossover Design

Each participant receives both treatment and control in different periods.

#### Structure

```
Group 1: Treatment → Washout → Control
Group 2: Control → Washout → Treatment
```

#### Advantages
- Each participant is their own control (higher power)
- Smaller sample size needed
- Controls for individual differences

#### Disadvantages
- Carryover effects (treatment affecting later periods)
- Not suitable if treatment has permanent effects
- Longer study duration

#### Design Considerations

**Washout Period**:
- Time between conditions to eliminate carryover
- Duration based on treatment half-life or expected duration of effects

**Order Effects**:
- Counterbalance treatment order across participants
- Include order as factor in analysis

**Carryover Assessment**:
- Test for period × treatment interaction
- May need to analyze only first period if carryover suspected

### 3. Factorial Design

Manipulates multiple independent variables simultaneously.

#### 2×2 Factorial Example

```
                Factor B (e.g., Dosage)
                Low         High
Factor A   Yes  Cell 1      Cell 2
(e.g.,     No   Cell 3      Cell 4
Training)
```

#### Advantages
- Tests multiple hypotheses in one study
- Can detect interactions between factors
- More efficient than separate studies

#### Disadvantages
- Complexity increases with more factors
- Larger sample size needed
- Interaction interpretation can be challenging

#### Analysis Approach

**Main Effects**:
- Effect of Factor A averaged across levels of B
- Effect of Factor B averaged across levels of A

**Interaction Effects**:
- Whether effect of A depends on level of B
- Visualize with interaction plots

### 4. Quasi-Experimental Designs

When random assignment is not feasible.

#### Non-Equivalent Groups Design

```
Treatment Group (pre-existing) → Intervention → Outcome
Control Group (pre-existing) → No intervention → Outcome
```

**Threats**:
- Selection bias (groups differ at baseline)
- Regression to the mean

**Mitigations**:
- Measure baseline characteristics
- Statistical control for baseline differences
- Propensity score matching

#### Interrupted Time Series

```
Multiple measurements → Intervention → Multiple measurements
O O O O → X → O O O O
```

**Advantages**:
- Strong causal inference if clear discontinuity
- Controls for ongoing trends

**Analysis**:
- Test for level change (immediate impact)
- Test for slope change (rate of change)

### 5. Within-Subjects (Repeated Measures) Design

Same participants measured multiple times under different conditions.

#### Advantages
- Higher statistical power
- Smaller sample needed
- Controls for individual differences

#### Disadvantages
- Practice effects
- Fatigue
- Carryover effects

#### Counterbalancing

Vary order of conditions across participants to control for order effects.

**Complete Counterbalancing**: All possible orders (only feasible for few conditions)

**Latin Square**: Each condition appears once in each position

Example (4 conditions):
```
Participant 1: A B C D
Participant 2: B C D A
Participant 3: C D A B
Participant 4: D A B C
```

## Sample Size and Power

### Power Analysis Components

- **Effect Size (d or f)**: Magnitude of expected difference
  - Small: d = 0.2, f = 0.1
  - Medium: d = 0.5, f = 0.25
  - Large: d = 0.8, f = 0.4
- **Alpha (α)**: Type I error rate (typically 0.05)
- **Power (1 - β)**: Probability of detecting real effect (typically 0.80 or 0.90)
- **Sample Size (N)**: Number needed to achieve desired power

### Power Analysis Template

```markdown
## Power Analysis for [Study Name]

### Expected Effect Size
- **Estimated effect**: d = [value] ([small/medium/large])
- **Justification**: [Based on prior research / pilot data / minimum meaningful effect]

### Parameters
- **Alpha (α)**: 0.05 (two-tailed)
- **Desired Power (1 - β)**: 0.80
- **Number of Groups**: [2 or more]
- **Design**: [Between / Within subjects]

### Sample Size Calculation
- **Total N required**: [number]
- **Per group**: [number per group]
- **Attrition estimate**: [expected dropout %]
- **Recruitment target**: [N + attrition buffer]

### Software Used
[G*Power / R pwr package / Python statsmodels]

### Sensitivity Analysis
If N = [available sample size], minimum detectable effect = [d value]
```

### Online Calculators and Tools

- **G*Power**: Free standalone power analysis software
- **R packages**: `pwr`, `WebPower`, `simr` (for mixed models)
- **Python**: `statsmodels.stats.power`
- **Online**: [Various online calculators for specific designs]

## Control and Comparison Groups

### No Treatment Control

Participants receive no intervention; natural baseline.

**Pros**: True control condition
**Cons**: May have high dropout; ethical concerns if treatment is beneficial

### Placebo Control

Participants receive inert intervention matching treatment in form but not content.

**Purpose**: Control for expectancy effects
**Example**: Sugar pill matching active drug

**Ethical Requirement**: Clinical equipoise (genuine uncertainty about which is better)

### Wait-List Control

Control group receives treatment after study completion.

**Pros**: Ethically preferable; reduces dropout
**Cons**: Time-limited; can't assess long-term effects

### Active Control (Treatment as Usual)

Compare new treatment to standard existing treatment.

**Pros**: Clinically relevant comparison
**Cons**: May need larger sample to detect difference between two active treatments

### Attention Control

Control group receives equal attention but not the hypothesized active ingredient.

**Purpose**: Control for non-specific therapy effects (time, attention, rapport)

## Procedure Documentation

### Standard Operating Procedure (SOP) Template

```markdown
## Experimental Procedure: [Study Title]

### Materials Needed
- [List all materials, equipment, software]
- [Include version numbers for software/instruments]

### Preparation
1. [Setup steps before participant arrives]
2. [Calibration or testing of equipment]

### Participant Arrival
1. **Greeting**: [Script for greeting participant]
2. **Consent**: [Informed consent procedure]
3. **Screening**: [Check inclusion/exclusion criteria]

### Pre-Intervention
1. **Baseline Measures**: [What to measure and how]
2. **Instructions**: [Exact wording for participant instructions]
3. **Practice Trials**: [If applicable]

### Randomization
1. **Timing**: [When to randomize]
2. **Method**: [How to assign to condition]
3. **Recording**: [How to record assignment]

### Intervention Delivery
**Treatment Condition**:
1. [Step-by-step procedure]
2. [Exact timing of each element]
3. [Standardized instructions/materials]

**Control Condition**:
1. [Step-by-step procedure]
2. [Matching elements to treatment]

### Post-Intervention
1. **Outcome Measures**: [What to measure and order]
2. **Timing**: [Immediately / After delay]
3. **Debriefing**: [Script for explaining study purpose]

### Data Recording
- **Form**: [Paper / Electronic]
- **Variables**: [List all to record]
- **Quality Checks**: [How to verify data entry]

### Adverse Events
- **Monitoring**: [What to watch for]
- **Reporting**: [Who to notify, how urgently]
- **Stopping Rules**: [Criteria for stopping study]

### End of Session
1. **Compensation**: [Payment/credit procedure]
2. **Scheduling**: [Follow-up appointments if needed]
3. **Contact Info**: [How participants can reach researchers]
```

## Common Design Challenges

### Challenge 1: Small Sample Size

**Solutions**:
- Within-subjects design (more power)
- Increase effect size (stronger manipulation)
- Use more sensitive measures
- Accept lower power; focus on effect size and confidence intervals
- Collaboration to pool samples across sites

### Challenge 2: Attrition

**Prevention**:
- Participant payment/incentives
- Regular contact/reminders
- Reduce participant burden
- Wait-list control (motivation to complete)

**Analysis**:
- Intent-to-treat analysis (include all randomized)
- Complete-case analysis (only completers)
- Multiple imputation for missing data
- Compare completers vs. dropouts on baseline characteristics

### Challenge 3: Non-Compliance

Participants don't follow protocol (e.g., don't take medication).

**Solutions**:
- Simplify protocol
- Increase monitoring (pill counts, adherence tracking)
- Motivational strategies

**Analysis**:
- Intent-to-treat (based on assignment, regardless of compliance)
- Per-protocol (only compliant participants)
- Complier average causal effect (CACE) analysis

### Challenge 4: Heterogeneous Effects

Treatment works for some but not others.

**Approaches**:
- Stratification by moderator variables
- Subgroup analyses (with caution about power)
- Personalized treatment rules using machine learning
- Report individual participant data or response distribution

## Ethical Considerations

### IRB/Ethics Review Requirements

Document for ethics board:
- Research purpose and significance
- Participant recruitment methods
- Informed consent procedure
- Risks and benefits
- Data confidentiality and security
- Compensation
- Vulnerability considerations (children, prisoners, etc.)

### Informed Consent Elements

Must include:
- Study purpose and procedures
- Duration of participation
- Voluntary nature and right to withdraw
- Risks and benefits
- Alternatives to participation
- Confidentiality protections
- Contact information for questions
- Signature (or electronic equivalent)

### Special Populations

**Children**: Parental consent + child assent
**Prisoners**: Extra protections against coercion
**Pregnant Women**: Risk assessment for fetus
**Cognitively Impaired**: Assess capacity to consent; may need surrogate

### Deception

If study requires deception:
- Justify necessity (no alternative)
- Minimize degree of deception
- Debrief thoroughly afterward
- Allow withdrawal after debriefing

## Pilot Testing

### Pilot Study Checklist

Before full study, test:
- [ ] Recruitment procedures work
- [ ] Participants understand instructions
- [ ] Manipulation is perceivable (manipulation check)
- [ ] Measures have adequate variability
- [ ] Timing is appropriate (not too long/short)
- [ ] Data recording system works
- [ ] Effect size is in expected range (refine power analysis)
- [ ] Adverse events identified
- [ ] Procedure is standardized across experimenters

## Reporting Standards

### CONSORT Statement (for RCTs)

Required elements:
- Trial design and changes to methods
- Participant flow (diagram)
- Recruitment details
- Baseline characteristics table
- Numbers analyzed
- Outcomes for each group
- Harms/adverse events
- Trial registration number

### Pre-Registration

Register experimental design before data collection:

**Include**:
- Hypotheses (primary and secondary)
- Design and procedure
- Sample size justification
- Analysis plan
- Stopping rules

**Platforms**:
- OSF (Open Science Framework)
- AsPredicted
- ClinicalTrials.gov (clinical trials)

## Resources

### Design Tools
- G*Power: Power analysis software
- Sealed Envelope: Randomization and blinding service
- REDCap: Research data capture system

### Guidelines
- CONSORT (RCTs)
- TREND (non-randomized trials)
- STROBE (observational studies)

### Further Reading
- Shadish, Cook, & Campbell (2002): Experimental and Quasi-Experimental Designs
- Maxwell, Delaney, & Kelley (2018): Designing Experiments and Analyzing Data
- Field (2018): Discovering Statistics (practical guide)
