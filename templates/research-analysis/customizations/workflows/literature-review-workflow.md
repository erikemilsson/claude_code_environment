# Literature Review Workflow

## Purpose

This command guides you through conducting a systematic or narrative literature review from search strategy development through synthesis and documentation.

## Context Required

- Research question or topic
- Scope of review (systematic vs. narrative)
- Databases and search terms
- Inclusion/exclusion criteria
- Reference manager setup

## Process

### Phase 1: Planning

#### 1.1 Define Review Objectives

**Questions to Answer**:
- What is the research question?
- Is this a systematic review or narrative review?
- What is the scope (broad overview vs. specific question)?
- What is the intended output (paper section, standalone review, meta-analysis)?

**Document**:
```markdown
## Literature Review Plan

**Research Question**: [Specific question to address]

**Review Type**: [Systematic / Narrative / Scoping]

**Scope**:
- **Population**: [Who/what is this about?]
- **Intervention/Exposure**: [What is being studied?]
- **Comparison**: [Compared to what?]
- **Outcome**: [What are we measuring?]

**Purpose**: [Background for study / Identify gaps / Inform hypothesis / Standalone review]

**Timeline**: [Start date - End date]
```

#### 1.2 Develop Search Strategy

**Select Databases**:
- General: Google Scholar, Web of Science, Scopus
- Subject-specific: PubMed, PsycINFO, IEEE Xplore, EconLit, etc.
- Grey literature: Dissertation databases, conference proceedings, reports

**Develop Search Terms**:
```markdown
## Search Terms

**Concept 1 (e.g., Population)**:
- Term 1: [e.g., "adolescent" OR "teenager" OR "youth"]

**Concept 2 (e.g., Intervention)**:
- Term 2: [e.g., "mindfulness" OR "meditation" OR "MBSR"]

**Concept 3 (e.g., Outcome)**:
- Term 3: [e.g., "anxiety" OR "stress" OR "mental health"]

**Combined Search String**:
(adolescent OR teenager OR youth) AND (mindfulness OR meditation OR MBSR) AND (anxiety OR stress OR "mental health")

**Filters**:
- Date range: [e.g., 2015-2025]
- Language: [e.g., English]
- Publication type: [e.g., Peer-reviewed articles]
```

**Test Search**:
- Run pilot search in one database
- Check relevance of top results
- Refine terms if too broad (too many irrelevant) or too narrow (missing key papers)

#### 1.3 Define Inclusion/Exclusion Criteria

```markdown
## Inclusion Criteria

**Population**:
- [e.g., Adolescents ages 12-18]
- [Include/exclude clinical vs. community samples]

**Study Design**:
- [e.g., RCTs, quasi-experimental, cohort studies]
- [Include/exclude case studies, reviews]

**Publication Type**:
- [Peer-reviewed journal articles]
- [Include/exclude dissertations, conference papers, books]

**Language**:
- [English only / Multiple languages]

**Date Range**:
- [e.g., Published 2015-2025]

## Exclusion Criteria

- [e.g., Non-empirical papers (editorials, opinions)]
- [e.g., Wrong population (adults, children under 12)]
- [e.g., Wrong intervention (not mindfulness-based)]
- [e.g., No relevant outcome measure]
- [e.g., Full text not available]
```

### Phase 2: Search Execution

#### 2.1 Conduct Searches

**For Each Database**:
1. Document search date
2. Record search string used
3. Note any database-specific syntax adjustments
4. Apply filters (date, language, type)
5. Record number of results
6. Export results to reference manager

**Search Log Template**:
```markdown
## Search Log

### Database: PubMed
- **Date**: 2025-11-16
- **Search String**: ("adolescent"[MeSH] OR "teenager") AND ("mindfulness"[MeSH] OR "meditation") AND ("anxiety"[MeSH])
- **Filters**: 2015-2025, English, Clinical Trial OR RCT
- **Results**: 234 records
- **Exported**: Yes (RIS format to Zotero)

### Database: PsycINFO
- **Date**: 2025-11-16
- **Search String**: (adolescent* OR teenager*) AND (mindfulness OR meditation) AND anxiety
- **Filters**: 2015-2025, English, Peer-reviewed
- **Results**: 189 records
- **Exported**: Yes (RIS format to Zotero)

[Repeat for each database]
```

#### 2.2 Import to Reference Manager

**Steps**:
1. Create new collection/folder for this review
2. Import all search results
3. Remove duplicates
4. Verify import (check random sample for completeness)

**Zotero Example**:
- Collections → New Collection → "Mindfulness Anxiety Review"
- File → Import → Select exported .ris files
- Right-click collection → "Find Duplicate Items" → Merge

### Phase 3: Screening

#### 3.1 Title Screening

**Process**:
- Read titles of all imported records
- Exclude obviously irrelevant based on inclusion/exclusion criteria
- When uncertain, include for abstract screening

**Track**:
```markdown
## Title Screening

**Starting**: 423 records (after duplicate removal)
**Excluded**: 187 (clearly irrelevant based on title)
**To abstract screening**: 236
```

**Tips**:
- Screen quickly; err on side of inclusion
- Create "Excluded - Title" tag/collection if you want to track reasons

#### 3.2 Abstract Screening

**Process**:
- Read abstracts of records that passed title screening
- Apply inclusion/exclusion criteria more strictly
- Tag reasons for exclusion (helpful for PRISMA diagram)

**Track**:
```markdown
## Abstract Screening

**Starting**: 236 records
**Excluded**: 142
  - Wrong population: 34
  - Wrong intervention: 28
  - No relevant outcome: 45
  - Study design: 22
  - Other: 13
**To full-text screening**: 94
```

#### 3.3 Full-Text Screening

**Process**:
- Obtain full-text PDFs for remaining records
- Read full text
- Apply final inclusion/exclusion criteria
- Document reasons for exclusion at this stage

**Track**:
```markdown
## Full-Text Screening

**Starting**: 94 records
**Could not obtain full text**: 6
**Excluded after full-text review**: 35
  - Wrong population: 8
  - Wrong intervention: 12
  - No relevant outcome: 7
  - Insufficient data: 5
  - Duplicate data (same sample): 3
**Included in review**: 53
```

**Create PRISMA Flow Diagram** (for systematic reviews):
```
Records identified through database searching (n = 423)
          ↓
After duplicates removed (n = 423)
          ↓
Title screening → Excluded (n = 187)
          ↓
Abstract screening (n = 236) → Excluded (n = 142)
          ↓
Full-text screening (n = 94) → Excluded (n = 35)
          ↓
Studies included (n = 53)
```

### Phase 4: Data Extraction

#### 4.1 Create Extraction Template

**Spreadsheet Template** (customize for your review):

| Study ID | Citation | Year | Country | Population | Sample Size | Design | Intervention | Control | Outcome Measure | Key Findings | Effect Size | Quality Rating | Notes |
|----------|----------|------|---------|------------|-------------|--------|--------------|---------|-----------------|--------------|-------------|----------------|-------|
| S001 | Smith et al. | 2020 | USA | Adolescents 14-17 | 120 | RCT | 8-week MBSR | Wait-list | GAD-7 | Sig reduction in anxiety | d = 0.52 | High | Well-conducted |

**Excel/Google Sheets Setup**:
- One row per study
- Freeze top row (headers)
- Use data validation for categorical fields
- Add comments for clarifications

#### 4.2 Extract Data from Each Study

**Process**:
1. Open full-text PDF
2. Extract information systematically
3. Record page numbers for key data points
4. Flag uncertainties or missing data
5. Enter into extraction template

**Tips**:
- Extract from two independent reviewers (for systematic reviews)
- Resolve discrepancies through discussion
- Contact authors if critical data missing
- Be consistent in how you code information

### Phase 5: Quality Assessment

#### 5.1 Select Assessment Tool

**Common Tools**:
- **RCTs**: Cochrane Risk of Bias tool
- **Observational studies**: Newcastle-Ottawa Scale
- **General**: GRADE, CASP checklists

#### 5.2 Assess Each Study

**Example: Cochrane Risk of Bias**

For each study, rate:
- Random sequence generation
- Allocation concealment
- Blinding of participants/personnel
- Blinding of outcome assessment
- Incomplete outcome data
- Selective reporting

**Rating**: Low risk / High risk / Unclear

**Document**:
```markdown
## Quality Assessment

| Study ID | Random Sequence | Allocation | Blinding Participants | Blinding Assessors | Attrition | Selective Reporting | Overall Quality |
|----------|----------------|------------|---------------------|-------------------|-----------|---------------------|-----------------|
| S001 | Low | Low | High | Low | Low | Low | Moderate |
| S002 | Low | Low | Low | Low | Low | Low | High |
```

### Phase 6: Synthesis

#### 6.1 Organize Findings

**Thematic Organization**:
- Group studies by theme, population, intervention type, outcome, etc.
- Create sub-collections or tags in reference manager

**Example Structure**:
```
Literature Review: Mindfulness and Adolescent Anxiety

1. Introduction
2. Methods (search strategy, inclusion/exclusion, quality assessment)
3. Results
   3.1 Study Characteristics
   3.2 School-Based Mindfulness Programs
   3.3 Clinical Mindfulness Interventions
   3.4 Online/App-Based Mindfulness
   3.5 Moderators of Effectiveness (age, baseline anxiety, dosage)
4. Discussion
5. Conclusion
```

#### 6.2 Narrative Synthesis

**For Each Theme**:
- Summarize number of studies
- Describe study characteristics (designs, samples, measures)
- Synthesize findings (what did they find?)
- Note consistencies and contradictions
- Assess quality of evidence
- Identify gaps

**Template**:
```markdown
### School-Based Mindfulness Programs

**Overview**: Fifteen studies examined school-based mindfulness interventions for adolescent anxiety.

**Study Characteristics**:
- Sample sizes ranged from 40 to 350 students (median = 120)
- Ages 12-18 years (mean = 14.5)
- 12 RCTs, 3 quasi-experimental designs
- Intervention duration: 6-12 weeks (mode = 8 weeks)
- Most used GAD-7 or STAI as outcome measure

**Findings**:
- 12 of 15 studies found significant reduction in anxiety (80%)
- Effect sizes ranged from d = 0.25 to d = 0.78 (median = 0.45)
- Effects were larger for:
  - Longer interventions (≥8 weeks)
  - Students with elevated baseline anxiety
  - Programs with home practice components

**Contradictory Findings**:
- Three studies found no significant effect
- All three had <6 weeks duration and no home practice

**Quality**:
- 8 high quality, 5 moderate, 2 low quality
- Main limitation: Lack of blinded outcome assessment

**Gaps**:
- Few studies examined long-term maintenance (>6 months)
- Limited diversity in samples (mostly white, middle-class)
- Unclear which specific mindfulness components drive effects
```

#### 6.3 Meta-Analysis (if applicable)

**When Appropriate**:
- Sufficient number of studies (generally ≥5)
- Studies are sufficiently similar (population, intervention, outcome)
- Quantitative data available (means, SDs, effect sizes)

**Software**:
- R: meta, metafor packages
- Python: statsmodels
- RevMan (Cochrane)

**Basic Process**:
1. Calculate effect size for each study
2. Weight by sample size (inverse variance method)
3. Combine weighted effect sizes
4. Assess heterogeneity (I² statistic)
5. Conduct sensitivity analyses
6. Create forest plot

### Phase 7: Documentation

#### 7.1 Write Literature Review

**Structure** (for standalone review):
```markdown
# Literature Review: [Topic]

## Abstract
[150-250 word summary]

## Introduction
- Background and context
- Importance of the topic
- Research question or objectives
- Scope of review

## Methods
- Search strategy (databases, search terms, dates)
- Inclusion/exclusion criteria
- Screening process (PRISMA diagram)
- Data extraction procedures
- Quality assessment method
- Synthesis approach

## Results
- Study selection (PRISMA flow)
- Study characteristics (summary table)
- Quality assessment results
- Synthesis of findings (organized thematically)
  - Theme 1: [Description of findings]
  - Theme 2: [Description of findings]
  - Meta-analysis results (if conducted)

## Discussion
- Summary of main findings
- Strength and quality of evidence
- Consistency across studies
- Limitations of current evidence
- Gaps in the literature
- Implications for practice
- Implications for research

## Conclusion
- Key takeaways
- Research question answered
- Future directions

## References
[Complete bibliography]

## Appendices
- Appendix A: Search Strings for Each Database
- Appendix B: Data Extraction Form
- Appendix C: Quality Assessment Forms
- Appendix D: Excluded Studies with Reasons
```

#### 7.2 Create Supporting Materials

**Summary Table**:
Create table summarizing all included studies (author, year, design, sample, intervention, outcome, findings)

**PRISMA Diagram**:
Visual flow of study selection process

**Quality Assessment Summary**:
Table showing quality ratings for each study

### Phase 8: Review and Finalize

#### 8.1 Internal Review

- Re-read for clarity and completeness
- Check that all citations in reference list
- Verify no included studies are missing from synthesis
- Check formatting consistency

#### 8.2 Peer Review (if collaborative)

- Have colleague review for:
  - Missed studies (check reference lists of key papers)
  - Interpretation accuracy
  - Clarity of writing
  - Completeness

#### 8.3 Update Search (for lengthy reviews)

If review process took >6 months, consider updating search to capture recent publications.

## Output Location

- **Reference library**: Zotero/Mendeley collection
- **Data extraction**: `research/literature/data_extraction.xlsx`
- **Search log**: `research/literature/search_log.md`
- **Quality assessment**: `research/literature/quality_assessment.xlsx`
- **Literature review document**: `research/literature/literature_review.md`
- **PRISMA diagram**: `research/literature/prisma_flow.png`

## Best Practices

1. **Be Systematic**: Document every decision and step
2. **Be Transparent**: Report what you did, including searches that didn't yield results
3. **Be Comprehensive**: Cast a wide net initially; narrow through screening
4. **Be Consistent**: Apply inclusion/exclusion criteria uniformly
5. **Be Critical**: Assess quality; don't treat all studies equally
6. **Be Honest**: Report null findings and contradictions
7. **Be Organized**: Use reference manager; tag and categorize
8. **Be Reproducible**: Someone should be able to replicate your search

## Common Pitfalls

- **Search too narrow**: Missing relevant studies
- **Search too broad**: Drowning in irrelevant results
- **Inconsistent screening**: Applying criteria differently across studies
- **Cherry-picking**: Only including studies that support your view
- **Ignoring grey literature**: Missing unpublished studies (publication bias)
- **Poor documentation**: Can't reproduce search later
- **No quality assessment**: Treating poor and good studies equally
- **Superficial synthesis**: Just listing findings without integration

## Resources

### Guidelines
- PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)
- Cochrane Handbook for Systematic Reviews
- Campbell Collaboration resources

### Tools
- Reference managers: Zotero, Mendeley, EndNote
- Screening tools: Rayyan, Covidence
- Meta-analysis: RevMan, R metafor, Comprehensive Meta-Analysis

### Training
- Cochrane Interactive Learning
- Campbell Collaboration training
- PRISMA statement and checklist
