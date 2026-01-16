# Literature Review Structure Standards

## Overview

This document defines standards for conducting systematic and narrative literature reviews. A well-structured literature review identifies relevant research, critically evaluates findings, and synthesizes knowledge to support research questions or identify gaps.

## Literature Review Types

### Systematic Literature Review

Comprehensive, reproducible search and analysis of all available evidence on a specific research question.

**Key Characteristics**:
- Pre-defined search protocol
- Explicit inclusion/exclusion criteria
- Systematic screening process
- Quality assessment of included studies
- Structured data extraction
- Meta-analysis (if appropriate)

**When to Use**:
- Medical and health sciences research
- Evidence-based policy decisions
- Meta-analysis or quantitative synthesis
- Need for unbiased, comprehensive evidence

### Narrative Literature Review

Selective review that provides overview and critical analysis of a topic without systematic methodology.

**Key Characteristics**:
- Flexible search strategy
- Author judgment in study selection
- Thematic organization
- Critical interpretation and synthesis
- Qualitative analysis

**When to Use**:
- Broad topic overviews
- Theoretical framework development
- Identifying research trends
- Preliminary research exploration

### Scoping Review

Maps the key concepts, evidence, and gaps in a research area.

**When to Use**:
- Emerging research areas
- Clarifying concepts and definitions
- Identifying research gaps
- Informing systematic review feasibility

## Review Structure

### 1. Search Strategy

#### Define Research Question

Use PICO framework for focused questions:
- **P**opulation: Who is the study about?
- **I**ntervention/Exposure: What is being studied?
- **C**omparison: What is it compared to?
- **O**utcome: What are you measuring?

Example: "In adults with type 2 diabetes (P), does metformin (I) compared to sulfonylureas (C) reduce cardiovascular events (O)?"

#### Select Databases

**General Academic**:
- Google Scholar (broad coverage, includes grey literature)
- Web of Science (citation tracking)
- Scopus (multidisciplinary, citation metrics)

**Subject-Specific**:
- PubMed/MEDLINE (medicine, life sciences)
- IEEE Xplore (engineering, computer science)
- PsycINFO (psychology, behavioral sciences)
- EconLit (economics)
- JSTOR (humanities, social sciences)
- arXiv (physics, math, computer science preprints)

#### Develop Search Terms

**Boolean Operators**:
- AND: Narrows results (diabetes AND exercise)
- OR: Expands results (hypertension OR "high blood pressure")
- NOT: Excludes terms (medicine NOT veterinary)

**Wildcards and Truncation**:
- \* for multiple characters: child\* (child, children, childhood)
- ? for single character: wom?n (woman, women)

**Phrase Searching**:
- Use quotes for exact phrases: "machine learning"

**Example Search String**:
```
(diabetes OR "type 2 diabetes" OR T2DM) AND
(metformin OR biguanide*) AND
(cardiovascular OR "heart disease" OR CVD) AND
(outcome* OR mortality OR morbidity)
```

#### Document Search Process

Create a search log with:
- Database name and date accessed
- Search string used
- Number of results
- Filters applied (date range, language, publication type)
- Number of records exported

### 2. Screening Process

#### Inclusion Criteria

Define what studies to include:
- Publication date range
- Study design types (RCTs, cohort studies, etc.)
- Population characteristics
- Language restrictions
- Publication status (peer-reviewed only or include grey literature)

#### Exclusion Criteria

Define what to exclude:
- Non-empirical studies (opinion pieces, editorials)
- Irrelevant populations or interventions
- Low-quality studies (based on assessment criteria)
- Duplicate publications

#### Screening Workflow

1. **Title Screening**: Quick review of titles, exclude obviously irrelevant
2. **Abstract Screening**: Review abstracts of remaining papers
3. **Full-Text Screening**: Read full papers that pass abstract screening
4. **Final Inclusion**: Apply all criteria to determine final set

**Documentation**:
- Record number of papers at each stage
- Note reasons for exclusion
- Create PRISMA flow diagram for systematic reviews

### 3. Data Extraction

#### Create Extraction Template

Standard fields to extract:
- **Citation**: Author, year, title, journal
- **Study Design**: RCT, cohort, case-control, cross-sectional, etc.
- **Population**: Sample size, demographics, inclusion/exclusion criteria
- **Intervention/Exposure**: Details of what was studied
- **Comparison**: Control or comparison group
- **Outcomes**: Primary and secondary outcomes measured
- **Results**: Key findings, effect sizes, p-values
- **Quality Indicators**: Randomization, blinding, attrition, bias assessment
- **Limitations**: Author-reported and reviewer-identified limitations
- **Funding**: Funding source and potential conflicts of interest

#### Organize Extracted Data

**Tools**:
- Spreadsheet (Excel, Google Sheets) for tabular data
- Reference manager (Zotero, Mendeley) for citation details
- Qualitative analysis software (NVivo, MAXQDA) for thematic coding
- Dedicated review software (Covidence, DistillerSR)

### 4. Quality Assessment

#### Select Assessment Tool

**General**:
- GRADE (Grading of Recommendations Assessment)
- Newcastle-Ottawa Scale (observational studies)

**Study-Specific**:
- Cochrane Risk of Bias tool (RCTs)
- ROBINS-I (non-randomized interventions)
- CASP Checklists (various study types)
- JBI Critical Appraisal Tools

#### Assessment Criteria

Common quality indicators:
- Selection bias
- Performance bias
- Detection bias
- Attrition bias
- Reporting bias
- Sample size adequacy
- Confounding control
- Measurement validity

### 5. Synthesis

#### Thematic Organization

Group findings by:
- Research question or hypothesis
- Theoretical framework
- Chronology (historical development)
- Methodology
- Themes or concepts

#### Critical Analysis

For each theme or finding:
- Summarize what is known
- Identify consistencies across studies
- Highlight contradictions or controversies
- Evaluate strength of evidence
- Note methodological limitations
- Identify gaps or unanswered questions

#### Integration Approaches

**Narrative Synthesis**:
- Textual description of findings
- Grouping studies by characteristics
- Exploring relationships within/between studies
- Assessing robustness of synthesis

**Quantitative Synthesis (Meta-Analysis)**:
- Statistical combination of effect sizes
- Heterogeneity assessment (I² statistic)
- Sensitivity analysis
- Publication bias assessment (funnel plots)

### 6. Documentation Standards

#### Literature Review Document Structure

```markdown
# Literature Review: [Topic]

## Introduction
- Background and context
- Research question or objectives
- Scope and boundaries

## Methods
- Search strategy (databases, search terms)
- Inclusion/exclusion criteria
- Screening process
- Data extraction approach
- Quality assessment method
- Synthesis approach

## Results
- Search results (PRISMA diagram)
- Study characteristics (summary table)
- Quality assessment results
- Synthesis of findings (organized thematically)

## Discussion
- Summary of main findings
- Strength of evidence
- Gaps and limitations in current research
- Implications for practice/research
- Future research directions

## Conclusion
- Key takeaways
- Research question answered (if applicable)

## References
- Complete bibliography in specified citation format
```

#### Supporting Materials

- **Search Log**: Detailed record of all searches
- **Screening Record**: PRISMA flow diagram
- **Data Extraction Spreadsheet**: Full extracted data
- **Quality Assessment Forms**: Completed assessments for each study
- **Excluded Studies List**: Studies excluded at full-text stage with reasons

## Citation Management

### Reference Manager Setup

**Recommended Tools**:
- **Zotero**: Open-source, browser integration, group libraries
- **Mendeley**: PDF annotation, institutional sharing
- **EndNote**: Professional features, institutional licenses
- **BibTeX**: LaTeX integration for academic papers

### Organization Structure

**Folders/Collections**:
```
Literature Review Project
├── Search Results
│   ├── PubMed Results
│   ├── IEEE Results
│   └── Google Scholar Results
├── Screening
│   ├── Title Screen - Include
│   ├── Abstract Screen - Include
│   └── Full Text Screen - Include
├── Included Studies
│   ├── Theme 1: [Topic]
│   ├── Theme 2: [Topic]
│   └── Theme 3: [Topic]
└── Excluded Studies
```

**Tagging**:
- Study design (RCT, cohort, case-control)
- Theme categories
- Quality rating (high, medium, low)
- Relevance (primary, secondary, background)

### Citation Workflow

1. **Import**: Export from databases, import to reference manager
2. **Organize**: Sort into folders, add tags
3. **Annotate**: Add notes, highlights to PDFs
4. **Extract**: Record key information in extraction template
5. **Cite**: Use plugin to insert citations while writing
6. **Export**: Generate bibliography in required format

## Common Pitfalls to Avoid

1. **Search Too Narrow**: Missing relevant studies due to restrictive search terms
2. **Search Too Broad**: Overwhelming number of irrelevant results
3. **Publication Bias**: Only including published, positive results
4. **Cherry Picking**: Selecting studies that support preconceived conclusions
5. **Inconsistent Screening**: Applying criteria inconsistently across studies
6. **Poor Documentation**: Unable to reproduce search and screening process
7. **Inadequate Synthesis**: Simply summarizing without critical analysis
8. **Ignoring Quality**: Treating all studies equally regardless of rigor
9. **Missing Grey Literature**: Excluding dissertations, reports, preprints
10. **No Protocol**: Starting without clear plan (for systematic reviews)

## Review Timelines

Typical time estimates:

- **Systematic Review**: 6-12 months
  - Protocol development: 2-4 weeks
  - Search and screening: 2-3 months
  - Data extraction: 2-3 months
  - Quality assessment: 1-2 months
  - Synthesis and writing: 2-3 months

- **Narrative Review**: 1-3 months
  - Planning and search: 2-4 weeks
  - Reading and note-taking: 3-6 weeks
  - Synthesis and writing: 2-4 weeks

## Resources

### PRISMA Guidelines
- PRISMA 2020 Statement for reporting systematic reviews
- PRISMA-P for review protocols
- PRISMA flow diagram template

### Training
- Cochrane Interactive Learning modules
- Campbell Collaboration resources
- EQUATOR Network reporting guidelines

### Tools
- Rayyan - collaborative screening tool
- Covidence - systematic review management
- RevMan - Cochrane's review software
- GRADE Pro - evidence quality assessment
