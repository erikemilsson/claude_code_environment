# Research/Analysis Template

## Overview

The Research/Analysis template provides a structured environment for conducting research projects, academic studies, data analysis, and experimental work. It includes standards for literature reviews, hypothesis tracking, experiment design, data analysis workflows, and citation management.

## When to Use This Template

Choose this template for projects focused on:

1. **Academic Research Projects**
   - Graduate research and dissertations
   - Academic paper writing
   - Literature reviews and meta-analyses
   - Research proposal development

2. **Data Science and Analysis**
   - Exploratory data analysis
   - Statistical modeling projects
   - Machine learning experiments
   - Data-driven research studies

3. **Experimental Research**
   - Hypothesis-driven experiments
   - A/B testing and experimentation
   - Clinical trials and studies
   - Laboratory research documentation

4. **Market and Business Research**
   - Market analysis projects
   - Competitive intelligence
   - Business case development
   - Strategic research initiatives

## What This Template Provides

### Core Components

- **Task Management**: Hierarchical task tracking for research planning (from components/task-management/)
- **Literature Review Structure**: Systematic approach to reviewing and organizing research literature
- **Hypothesis Tracking**: Framework for formulating, testing, and documenting hypotheses
- **Experiment Design Patterns**: Templates for designing rigorous experiments
- **Data Analysis Workflows**: Structured processes for data exploration, cleaning, and analysis
- **Citation Management**: Standards for tracking and managing research citations

### File Structure

```
project/
├── CLAUDE.md                    # Router file
├── README.md                    # Project overview
├── .claude/
│   ├── commands/
│   │   ├── complete-task.md     # Task management
│   │   ├── breakdown.md         # Task breakdown
│   │   ├── sync-tasks.md        # Task synchronization
│   │   ├── update-tasks.md      # Task validation
│   │   ├── conduct-analysis.md  # Data analysis workflow
│   │   └── review-literature.md # Literature review workflow
│   ├── context/
│   │   ├── overview.md          # Research project overview
│   │   ├── standards/
│   │   │   ├── literature-review.md     # Literature review standards
│   │   │   ├── hypothesis-tracking.md   # Hypothesis documentation
│   │   │   ├── experiment-design.md     # Experiment design patterns
│   │   │   └── citation-format.md       # Citation standards
│   │   └── validation-rules.md  # Research validation rules
│   ├── tasks/                   # Task tracking
│   │   ├── task-overview.md
│   │   └── task-*.json
│   └── reference/               # Supporting documentation
│       ├── difficulty-guide.md
│       ├── breakdown-workflow.md
│       ├── data-analysis-checklist.md
│       └── statistical-methods.md
└── research/                    # Your research work
    ├── literature/              # Literature reviews and notes
    ├── data/                    # Raw and processed data
    ├── experiments/             # Experiment designs and results
    ├── analysis/                # Analysis scripts and notebooks
    ├── hypotheses/              # Hypothesis documentation
    └── publications/            # Papers, reports, presentations
```

## Getting Started

### 1. Initialize Project Structure

```bash
# Create the base directories
mkdir -p .claude/{commands,context/standards,tasks,reference}
mkdir -p research/{literature,data,experiments,analysis,hypotheses,publications}
```

### 2. Copy Template Files

From this template directory, copy:
- Commands from `customizations/commands/` to `.claude/commands/`
- Standards from `customizations/standards/` to `.claude/context/standards/`
- Workflows from `customizations/workflows/` to `.claude/commands/`
- Reference docs from `customizations/reference/` to `.claude/reference/`

### 3. Customize for Your Project

Update `.claude/context/overview.md` with:
- Research question or thesis
- Research methodology
- Expected outcomes
- Timeline and milestones
- Data sources and collection methods

Update `.claude/context/standards/hypothesis-tracking.md` with:
- Your hypothesis formulation approach
- Testing methodology
- Success criteria
- Documentation standards

### 4. Create Initial Tasks

Create task JSON files for your research work:
- Literature review tasks
- Data collection tasks
- Experiment design tasks
- Analysis tasks
- Publication tasks

## Typical Workflows

### Literature Review Workflow

1. **Planning**: Define search strategy, databases, keywords, inclusion/exclusion criteria
2. **Search**: Conduct systematic search across academic databases
3. **Screening**: Apply inclusion/exclusion criteria to filter papers
4. **Extraction**: Extract key information, findings, and citations
5. **Synthesis**: Organize findings thematically, identify gaps
6. **Documentation**: Write literature review section with proper citations

### Hypothesis-Driven Research Workflow

1. **Formulation**: Develop research question and testable hypotheses
2. **Background**: Conduct literature review to inform hypothesis
3. **Design**: Design experiments or studies to test hypotheses
4. **Data Collection**: Gather data according to research design
5. **Analysis**: Perform statistical analysis to test hypotheses
6. **Interpretation**: Draw conclusions, discuss implications
7. **Documentation**: Document findings and limitations

### Data Analysis Workflow

1. **Data Acquisition**: Collect or import raw data
2. **Exploration**: Initial exploration to understand data characteristics
3. **Cleaning**: Handle missing values, outliers, data quality issues
4. **Transformation**: Feature engineering, normalization, aggregation
5. **Analysis**: Apply statistical methods or machine learning models
6. **Validation**: Verify results, check assumptions, sensitivity analysis
7. **Visualization**: Create charts, graphs, and visual summaries
8. **Documentation**: Document methods, findings, and interpretations

### Experimental Design Workflow

1. **Objective**: Define clear research objective and hypothesis
2. **Variables**: Identify independent, dependent, and control variables
3. **Methodology**: Choose experimental design (RCT, factorial, etc.)
4. **Sample Size**: Calculate required sample size for statistical power
5. **Protocol**: Document detailed experimental protocol
6. **Ethics**: Address ethical considerations and approvals
7. **Execution**: Conduct experiment following protocol
8. **Analysis**: Analyze results and test hypotheses

## Key Features

### 1. Systematic Literature Review

- Search strategy templates for reproducible searches
- Citation tracking and organization
- Thematic coding and categorization
- Gap analysis and synthesis
- Reference management integration

### 2. Rigorous Hypothesis Management

- Structured hypothesis formulation templates
- Testing methodology documentation
- Results tracking against hypotheses
- Revision and iteration tracking
- Null hypothesis handling

### 3. Reproducible Research

- Data provenance tracking
- Analysis script version control
- Computational environment documentation
- Random seed and parameter tracking
- Results reproducibility validation

### 4. Data Quality Assurance

- Data validation rules and checks
- Data cleaning documentation
- Quality control workflows
- Data lineage tracking
- Audit trails for data transformations

## Customization Points

### Literature Review Standards

Customize `customizations/standards/literature-review-structure.md` for your field:
- Database search strategies (PubMed, IEEE, JSTOR, etc.)
- Citation style (APA, MLA, Chicago, Vancouver)
- Screening criteria
- Data extraction templates
- Quality assessment frameworks

### Hypothesis Tracking

Customize `customizations/standards/hypothesis-tracking.md` for your methodology:
- Hypothesis formulation format (null vs. alternative)
- Testing approach (frequentist, Bayesian)
- Significance thresholds
- Multiple hypothesis correction methods
- Documentation requirements

### Experiment Design

Customize `customizations/standards/experiment-design-patterns.md` for your research type:
- Design types (RCT, quasi-experimental, observational)
- Randomization methods
- Blinding procedures
- Sample size calculations
- Protocol templates

### Data Analysis Workflows

Customize `customizations/workflows/data-analysis-workflow.md` for your tools:
- Programming languages (Python, R, Julia, MATLAB)
- Statistical methods
- Visualization standards
- Notebook organization (Jupyter, R Markdown)
- Code review processes

## Integration with Other Components

### Task Management Component

This template uses the task-management component for:
- Breaking down research projects into phases
- Tracking literature review progress
- Managing experiment timelines
- Coordinating analysis tasks
- Planning publication milestones

### Version Control

Research projects benefit from:
- Data versioning (DVC, Git LFS)
- Code and notebook versioning
- Results snapshot tracking
- Collaboration workflows
- Reproducibility through version pinning

### Tool Integration

#### Gemini API Use Cases
- Research literature search and summarization with grounding
- Market research and competitive analysis
- Domain expertise consultation
- Research paper review and feedback
- Statistical method recommendations

#### Claude Use Cases
- Data analysis code implementation
- Statistical analysis scripting
- Experiment design development
- Research documentation writing
- Data cleaning and transformation

## Common Use Cases

### 1. Academic Research Paper

**Initial Setup**:
- Define research question and hypotheses
- Create literature review structure
- Set up data collection plan
- Design experiments or studies

**Ongoing Work**:
- Conduct systematic literature review
- Collect and clean data
- Run experiments and analyses
- Write paper sections
- Respond to peer review

### 2. Data Science Project

**Initial Setup**:
- Define business question or problem
- Identify data sources
- Set up analysis environment
- Create task breakdown for exploration, modeling, deployment

**Ongoing Work**:
- Exploratory data analysis
- Feature engineering
- Model development and validation
- Results interpretation
- Deployment and monitoring

### 3. Experimental Study

**Initial Setup**:
- Formulate hypotheses
- Design experimental protocol
- Calculate sample sizes
- Obtain ethics approval

**Ongoing Work**:
- Recruit participants
- Conduct experiments
- Record and organize data
- Perform statistical analysis
- Write research report

### 4. Market Research Analysis

**Initial Setup**:
- Define research objectives
- Identify data sources and methods
- Create survey or interview protocols
- Plan analysis approach

**Ongoing Work**:
- Collect primary/secondary data
- Clean and organize responses
- Conduct quantitative and qualitative analysis
- Synthesize findings
- Create presentation and recommendations

## Best Practices

1. **Document Everything**: Record decisions, assumptions, and methods in real-time
2. **Version Data and Code**: Track changes to datasets and analysis scripts
3. **Test Assumptions**: Validate statistical assumptions before applying methods
4. **Handle Uncertainty**: Document limitations, confounds, and alternative explanations
5. **Ensure Reproducibility**: Use seed values, document environments, script everything
6. **Peer Review**: Have others review methodology and analysis before finalizing
7. **Iterate Hypotheses**: Refine hypotheses based on preliminary findings
8. **Maintain Audit Trail**: Keep records of all data transformations
9. **Visualize Results**: Create clear visualizations to communicate findings
10. **Cite Properly**: Maintain accurate citations throughout the research process

## Tools and Technology

Common tools used with this template:

### Data Analysis
- **Python**: pandas, NumPy, scikit-learn, statsmodels
- **R**: tidyverse, ggplot2, caret, shiny
- **Julia**: DataFrames.jl, Plots.jl, MLJ.jl
- **MATLAB**: Statistics and Machine Learning Toolbox

### Statistical Software
- **SPSS**: Point-and-click statistical analysis
- **SAS**: Enterprise statistical software
- **Stata**: Econometrics and biostatistics
- **JASP / jamovi**: Open-source alternatives to SPSS

### Literature Management
- **Zotero**: Open-source reference manager
- **Mendeley**: Reference manager with PDF annotation
- **EndNote**: Professional citation management
- **BibTeX**: LaTeX citation management

### Notebooks and Documentation
- **Jupyter**: Interactive Python/R/Julia notebooks
- **R Markdown**: Reproducible R analysis documents
- **Quarto**: Next-generation R Markdown
- **Observable**: JavaScript notebooks for data viz

### Data Management
- **DVC**: Data version control
- **Git LFS**: Large file storage for Git
- **PostgreSQL / SQLite**: Structured data storage
- **Apache Arrow / Parquet**: Efficient data formats

### Experiment Management
- **MLflow**: Machine learning experiment tracking
- **Weights & Biases**: Deep learning experiment tracking
- **ClearML**: ML experiment management
- **Sacred**: Python experiment configuration

## Success Metrics

Track these metrics to measure research progress:

1. **Literature Coverage**: Number of papers reviewed, citations tracked
2. **Hypothesis Testing**: Hypotheses tested vs. planned, results documented
3. **Data Quality**: Completeness, accuracy, validation pass rates
4. **Analysis Completion**: Planned analyses completed, results validated
5. **Reproducibility**: Ability to reproduce key findings from scripts
6. **Publication Progress**: Sections drafted, reviews completed, submissions
7. **Timeline Adherence**: Tasks completed on schedule, milestone achievement

## Getting Help

For questions about this template:
1. Review the customization files in `customizations/`
2. Check the task-management component documentation
3. Consult the reference documentation in `.claude/reference/`
4. Review statistical methods guide for analysis questions

## Benefits

1. **Structured Approach**: Clear frameworks for each research phase
2. **Reproducibility**: Version control and documentation ensure repeatable results
3. **Quality Assurance**: Checklists and workflows maintain rigor
4. **Collaboration**: Clear processes for multi-researcher projects
5. **Efficiency**: Templates and patterns accelerate research work
6. **Transparency**: Comprehensive documentation of methods and decisions
