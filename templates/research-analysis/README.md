# Research/Analysis Template

## Overview

The Research/Analysis template provides a structured environment for conducting research projects, including literature reviews, hypothesis development, experiment design, data collection and analysis, and findings documentation. It includes workflows for systematic research, hypothesis tracking patterns, and data analysis standards.

## When to Use This Template

Choose this template for projects focused on:

1. **Academic Research Projects**
   - Thesis and dissertation work
   - Journal article research
   - Conference paper preparation
   - Grant proposal development

2. **Data Analysis and Statistical Studies**
   - Quantitative research studies
   - Qualitative research projects
   - Mixed methods research
   - Exploratory data analysis

3. **Systematic Reviews and Meta-Analysis**
   - Literature reviews
   - Systematic reviews
   - Meta-analysis projects
   - Evidence synthesis

4. **Experimental Research**
   - Laboratory experiments
   - Field studies
   - A/B testing and experimentation
   - Observational studies

## What This Template Provides

### Core Components

- **Task Management**: Hierarchical task tracking for research planning (from components/task-management/)
- **Literature Review Workflow**: Structured approach to searching, evaluating, and synthesizing research
- **Hypothesis Tracking**: Patterns for formulating, testing, and validating hypotheses
- **Experiment Design**: Templates for designing rigorous experiments
- **Data Analysis Workflow**: Step-by-step process for analyzing research data
- **Citation Management**: Standards for managing references and bibliographies

### File Structure

```
project/
├── CLAUDE.md                    # Router file
├── README.md                    # Project overview
├── .claude/
│   ├── commands/
│   │   ├── complete-task.md          # Task management
│   │   ├── breakdown.md              # Task breakdown
│   │   ├── sync-tasks.md             # Task synchronization
│   │   ├── update-tasks.md           # Task validation
│   │   ├── literature-review.md      # Literature review workflow
│   │   └── data-analysis.md          # Data analysis workflow
│   ├── context/
│   │   ├── overview.md               # Project overview
│   │   ├── standards/
│   │   │   ├── citation-management.md    # Citation standards
│   │   │   ├── research-methodology.md   # Methodology standards
│   │   │   └── data-quality.md           # Data quality standards
│   │   └── validation-rules.md       # Research validation rules
│   ├── tasks/                        # Task tracking
│   │   ├── task-overview.md
│   │   └── task-*.json
│   └── reference/                    # Supporting documentation
│       ├── difficulty-guide.md
│       ├── breakdown-workflow.md
│       ├── hypothesis-tracking.md    # Hypothesis patterns
│       └── experiment-design.md      # Experiment templates
└── research/                         # Your research files
    ├── literature/                   # Literature review notes
    ├── hypotheses/                   # Hypothesis documentation
    ├── experiments/                  # Experiment designs
    ├── data/
    │   ├── raw/                      # Raw data files
    │   ├── processed/                # Cleaned data
    │   └── analysis/                 # Analysis outputs
    └── findings/                     # Research findings
```

## Getting Started

### 1. Initialize Project Structure

```bash
# Create the base directories
mkdir -p .claude/{commands,context/standards,tasks,reference}
mkdir -p research/{literature,hypotheses,experiments,data/{raw,processed,analysis},findings}
```

### 2. Copy Template Files

From this template directory, copy:
- Commands from `customizations/workflows/` to `.claude/commands/`
- Standards from `customizations/standards/` to `.claude/context/standards/`
- Reference docs from `customizations/reference/` to `.claude/reference/`

### 3. Customize for Your Project

Update `.claude/context/overview.md` with:
- Research questions and objectives
- Research methodology (quantitative, qualitative, mixed)
- Domain and field of study
- Timeline and milestones
- Team members and roles
- Ethics review requirements (if applicable)

Update `.claude/context/standards/citation-management.md` with:
- Required citation style (APA, MLA, Chicago, etc.)
- Reference management tool
- Bibliography organization approach
- In-text citation conventions

### 4. Create Initial Tasks

Create task JSON files for your research phases:
- Literature review tasks
- Hypothesis formulation tasks
- Experiment design tasks
- Data collection tasks
- Analysis tasks
- Writing and publication tasks

## Typical Workflows

### Literature Review Workflow

1. **Define Scope**: Establish search terms, databases, inclusion/exclusion criteria
2. **Search**: Systematic search across relevant databases and sources
3. **Screen**: Review titles and abstracts for relevance
4. **Evaluate**: Read full texts and assess quality
5. **Extract**: Pull key information, findings, and citations
6. **Synthesize**: Organize findings, identify patterns and gaps
7. **Document**: Write literature review section

### Hypothesis Development Workflow

1. **Background Research**: Review existing literature and theory
2. **Formulate**: Write clear, testable hypotheses
3. **Define Variables**: Identify independent, dependent, and control variables
4. **Predict**: Specify expected relationships and outcomes
5. **Document**: Record hypotheses with supporting rationale
6. **Track**: Monitor hypothesis status through research process

### Experiment Design Workflow

1. **Research Question**: Define what you want to learn
2. **Variables**: Identify and operationalize all variables
3. **Design**: Choose experimental design (randomized, factorial, etc.)
4. **Controls**: Plan control groups and conditions
5. **Protocol**: Write detailed experimental procedures
6. **Ethics**: Complete IRB/ethics review if needed
7. **Pilot**: Run small-scale test of procedures
8. **Refine**: Adjust protocol based on pilot results

### Data Analysis Workflow

1. **Preparation**: Clean and validate data
2. **Exploration**: Exploratory data analysis (EDA)
3. **Visualization**: Create initial plots and charts
4. **Testing**: Apply appropriate statistical tests
5. **Validation**: Check assumptions and robustness
6. **Interpretation**: Draw conclusions from results
7. **Documentation**: Record analysis process and findings

## Key Features

### 1. Systematic Approach

- Structured workflows ensure rigorous methodology
- Hypothesis tracking maintains research focus
- Experiment templates promote reproducibility
- Citation management ensures proper attribution

### 2. Research Quality

- Literature review patterns ensure comprehensive coverage
- Experiment design templates reduce methodology gaps
- Data analysis workflows promote statistical rigor
- Validation rules catch common research errors

### 3. Reproducibility

- Detailed documentation of methods and procedures
- Version control for data processing scripts
- Clear data lineage from raw to processed to analysis
- Experiment protocols for exact replication

### 4. Collaboration Support

- Task management for team coordination
- Clear roles and responsibilities
- Shared citation library
- Review processes for quality assurance

## Customization Points

### Literature Review Workflow

Customize `customizations/workflows/literature-review.md` for your field:
- Relevant databases and search engines
- Screening criteria specific to your domain
- Quality assessment frameworks
- Synthesis approaches (narrative, thematic, meta-analysis)

### Hypothesis Tracking

Customize `customizations/reference/hypothesis-tracking.md` for your methodology:
- Hypothesis formulation guidelines
- Evidence collection standards
- Validation criteria
- Status tracking approach (supported, refuted, inconclusive)

### Experiment Design

Customize `customizations/reference/experiment-design.md` for your research type:
- Experimental design patterns (RCT, factorial, quasi-experimental)
- Sample size calculations
- Randomization procedures
- Control condition specifications

### Data Analysis

Customize `customizations/workflows/data-analysis.md` for your tools:
- Statistical software (Python, R, SPSS, etc.)
- Standard analysis pipelines
- Visualization approaches
- Result reporting formats

### Citation Management

Customize `customizations/standards/citation-management.md` for your requirements:
- Citation style (APA, MLA, Chicago, IEEE, etc.)
- Reference manager integration (Zotero, Mendeley, EndNote)
- Bibliography organization
- In-text citation conventions

## Integration with Other Components

### Task Management Component

This template uses the task-management component for:
- Breaking down complex research projects into phases
- Tracking progress across multiple research activities
- Managing dependencies between research tasks
- Coordinating collaborative research efforts

### Version Control

Research projects benefit from:
- Data versioning for reproducibility
- Script versioning for analysis code
- Document versioning for writing
- Protocol versioning for experiments

## Common Use Cases

### 1. Academic Research Project

**Initial Setup**:
- Define research questions and hypotheses
- Conduct literature review
- Design study methodology
- Obtain ethics approval if needed

**Data Collection Phase**:
- Recruit participants or gather data sources
- Execute data collection procedures
- Monitor data quality
- Store raw data securely

**Analysis Phase**:
- Clean and validate data
- Perform statistical analysis
- Create visualizations
- Validate findings

**Writing Phase**:
- Draft manuscript sections
- Prepare figures and tables
- Compile references
- Submit for publication

### 2. Data Analysis Study

**Initial Setup**:
- Identify data sources
- Define analysis questions
- Plan analysis approach
- Set up analysis environment

**Data Preparation**:
- Obtain and import data
- Clean and validate
- Transform and engineer features
- Explore initial patterns

**Analysis**:
- Apply statistical methods
- Create visualizations
- Test hypotheses
- Validate results

**Reporting**:
- Document findings
- Create presentation materials
- Write technical report
- Share reproducible code

### 3. Literature Review/Meta-Analysis

**Initial Setup**:
- Define review scope and questions
- Identify search strategy
- Create screening criteria
- Set up reference management

**Search Phase**:
- Search databases systematically
- Track search results
- Remove duplicates
- Screen by title/abstract

**Review Phase**:
- Full-text review
- Extract data
- Assess quality
- Synthesize findings

**Writing Phase**:
- Write review sections
- Create synthesis tables
- Generate flow diagrams
- Compile comprehensive bibliography

### 4. Experimental Study

**Design Phase**:
- Formulate hypotheses
- Design experiment protocol
- Plan statistical analysis
- Create materials and procedures

**Pilot Phase**:
- Run pilot study
- Refine procedures
- Validate measures
- Adjust protocol

**Execution Phase**:
- Recruit participants
- Run experiment sessions
- Collect data
- Monitor quality

**Analysis Phase**:
- Analyze results
- Test hypotheses
- Interpret findings
- Write research report

## Best Practices

1. **Document Everything**: Record decisions, procedures, and rationale throughout
2. **Version Your Data**: Keep raw data untouched, version all transformations
3. **Test Assumptions**: Validate statistical assumptions before analysis
4. **Preregister When Possible**: Preregister hypotheses and analysis plans
5. **Use Reproducible Code**: Write scripts for all data processing and analysis
6. **Organize References**: Maintain systematic citation management from the start
7. **Validate Early**: Check data quality and analysis correctness frequently
8. **Backup Regularly**: Protect research data and materials
9. **Follow Ethics Guidelines**: Maintain ethical standards throughout research
10. **Share When Appropriate**: Make data and code available for reproducibility

## Tools and Technology

Common tools used with this template:

### Data Analysis
- **Python**: pandas, numpy, scipy, statsmodels, scikit-learn
- **R**: tidyverse, ggplot2, dplyr, statistical packages
- **SPSS**: Commercial statistical software
- **Excel**: Spreadsheet analysis for smaller datasets

### Reference Management
- **Zotero**: Free, open-source reference manager
- **Mendeley**: Reference manager with PDF annotation
- **EndNote**: Commercial reference management software
- **BibTeX**: LaTeX-based citation management

### Notebook Environments
- **Jupyter**: Interactive Python notebooks
- **R Markdown**: Reproducible R analysis documents
- **Quarto**: Next-generation scientific publishing

### Visualization
- **matplotlib/seaborn**: Python visualization libraries
- **ggplot2**: R visualization package
- **Tableau**: Interactive dashboard creation
- **D3.js**: Web-based custom visualizations

### Version Control and Collaboration
- **Git**: Version control for code and documents
- **GitHub/GitLab**: Collaboration and sharing platform
- **OSF (Open Science Framework)**: Research project management

## Success Metrics

Track these metrics to measure research progress:

1. **Literature Coverage**: Number of papers reviewed, synthesis completeness
2. **Hypothesis Status**: Hypotheses tested, supported, refuted
3. **Data Quality**: Completeness, accuracy, validation checks passed
4. **Analysis Progress**: Analyses completed, results validated
5. **Documentation**: Procedures documented, code commented, findings recorded
6. **Publication**: Manuscripts drafted, submitted, accepted
7. **Reproducibility**: Code runnable, data accessible, methods documented

## Getting Help

For questions about this template:
1. Review the customization files in `customizations/`
2. Check the task-management component documentation
3. Consult the reference documentation in `.claude/reference/`
4. Review methodology guides for your specific research type

## Benefits

1. **Rigorous Methodology**: Structured workflows ensure research quality
2. **Better Organization**: Clear structure for all research materials
3. **Reproducibility**: Documentation and version control enable replication
4. **Efficient Collaboration**: Task management and standards enable teamwork
5. **Comprehensive Documentation**: Nothing gets lost or forgotten
6. **Quality Assurance**: Validation rules and review processes catch errors
7. **Publication Ready**: Organized materials make writing and sharing easier
