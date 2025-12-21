# Research Project Example

This example demonstrates how the **Research template** is automatically selected for academic and scientific research projects.

## What This Example Shows

### Template Detection
When the specification was provided to Claude Code's smart-bootstrap system, it automatically selected the **Research template** because it detected:
- Keywords: "research", "literature review", "meta-analysis", "hypothesis"
- Academic methodology patterns
- Statistical analysis requirements
- Publication planning

### Generated Structure
The `.claude/` environment was specifically configured for research with:

1. **Hypothesis Tracking** - Formal hypothesis management
2. **Literature Review Workflow** - Systematic review commands
3. **Statistical Standards** - Analysis best practices
4. **Citation Management** - Reference tracking system

### Key Benefits Demonstrated

#### 1. Research-Specific Commands
Pre-configured commands for academic workflows:
- `literature-search.md` - Systematic database queries
- `extract-data.md` - Standardized data extraction
- `run-analysis.md` - Statistical analysis execution
- `check-hypotheses.md` - Hypothesis validation

#### 2. Hypothesis Management
Formal tracking of research hypotheses:
```json
{
  "id": "H1",
  "hypothesis": "Temperature rise > 1.5°C correlates with >30% biodiversity loss",
  "status": "untested",
  "evidence_for": [],
  "evidence_against": [],
  "statistical_support": null,
  "conclusion": "pending"
}
```

#### 3. Literature Review Tracking
Systematic organization of sources:
- Search strategy documentation
- Inclusion/exclusion criteria
- PRISMA flow tracking
- Quality assessment scores
- Citation network analysis

## How It Was Created

### 1. User Provided Specification
```bash
# User created original-spec.md with research methodology
```

### 2. Bootstrap Command
```
"Create environment from claude_code_environment repo using spec: original-spec.md"
```

### 3. Automatic Processing
Claude Code:
1. Read the specification
2. **Detected research keywords** → Selected Research template
3. Generated `.claude/` with academic features
4. Created hypothesis tracking system
5. Set up literature review workflow
6. Added statistical analysis standards

### 4. Ready for Research
The project is now ready with:
- Hypothesis tracking files
- Literature database structure
- Analysis workflow commands
- PRISMA compliance checklist
- Statistical rigor guidelines

## Compare With Other Templates

The **Research template** provides:
- Hypothesis testing framework
- Literature review management
- Statistical analysis patterns
- Citation tracking
- Research ethics guidelines
- Reproducibility standards

Compare with:
- **simple-todo-app/** - Base template for software
- **pension-calculator/** - Power Query for BI projects

## Files in This Example

```
research-project/
├── original-spec.md           # The input specification
├── generated-environment/     # What was generated
│   └── .claude/
│       ├── commands/         # Research workflows
│       ├── context/          # Methodology & hypotheses
│       ├── tasks/           # Research phases
│       └── reference/       # Statistical guides
└── README.md                # This explanation
```

## Research Template Features

### Hypothesis Tracking System
All hypotheses are formally tracked with:
- Clear statement
- Test criteria
- Evidence collection
- Statistical validation
- Final conclusions

### Literature Management
Systematic approach to sources:
- Search strategy log
- Screening workflow
- Data extraction templates
- Quality assessment
- Citation formatting

### Statistical Rigor
Built-in best practices:
- Pre-registration reminders
- Power analysis
- Effect size reporting
- Confidence intervals
- Sensitivity analysis

### Reproducibility
Ensuring research can be replicated:
- Version control for data
- Analysis script documentation
- Environment specifications
- Raw data preservation
- Transparent reporting

## Using This Pattern

To create your own research project:

1. Write a specification with research methodology
2. Open VS Code in new project directory
3. Tell Claude Code: "Create environment using spec: [path]"
4. Follow the phased research workflow
5. Use hypothesis tracking throughout

The Research template works well for:
- Academic research papers
- Systematic literature reviews
- Meta-analyses
- PhD dissertations
- Grant proposals
- Research data management