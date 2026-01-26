# Archived Templates Summary

This document summarizes the old 5-template system that was replaced by the simpler `base/` + `extras/` approach in January 2025.

## Why Archived

The template system was **overengineered** for the actual use case:
- Users rarely needed domain-specific templates
- Most projects used the same core structure
- Template selection added friction to getting started
- Maintaining 5 templates meant 5x the work for updates

**Replacement**: Copy `base/` and add extras as needed.

## The Five Templates

### 1. Base Template
**Use case**: General planning, research, non-technical projects

Core structure that all other templates extended:
```
project/
├── CLAUDE.md              # Router file
├── README.md              # Human docs
└── .claude/
    ├── commands/          # plan, breakdown, complete-task, sync-tasks
    ├── context/           # overview, constraints, preferences
    ├── tasks/             # task-overview.md + task-*.json
    └── reference/         # notes, difficulty-guide
```

**Now**: This is essentially what `base/` provides.

### 2. Data Engineering Template
**Use case**: ETL pipelines, data processing, analytics engineering

Extended base with:
- `context/standards/python.md` - Python/Polars patterns
- `context/standards/sql.md` - SQL conventions
- `context/standards/testing.md` - Test requirements
- `context/workflows.md` - CI/CD process
- `reference/data-model.md` - Schema documentation
- `reference/dependencies.md` - External systems
- `reference/performance.md` - Optimization notes
- Commands: `review-code.md`, `optimize.md`, `document.md`

**Now**: Use `base/` + `extras/development/` for source of truth and standards.

### 3. BI/Dashboard Template
**Use case**: Power BI, reporting, visualization projects

Extended base with:
- `context/standards/powerbi.md` - Naming conventions
- `context/standards/dax.md` - DAX patterns
- `context/standards/design.md` - Visual guidelines
- `context/users.md` - Audience needs
- `reference/data-sources.md` - Available connections
- `reference/kpis.md` - Business metrics
- `reference/glossary.md` - Term definitions
- Commands: `review-dax.md`, `validate.md`, `document-kpi.md`

**Now**: Use `base/` and create project-specific context files as needed.

### 4. Hybrid Template
**Use case**: Projects combining multiple technologies

Merged elements from Data Engineering and BI templates based on needs. No fixed structure - generated dynamically during bootstrap.

**Now**: Same approach - use `base/` and add what you need.

### 5. Power Query Template
**Use case**: Excel Power Query, regulatory/compliance calculations

Most complex template with Phase 0 workflow for ambiguity resolution:

```
project/
├── calculation-docs/              # Source regulatory PDFs
├── excel-files/                   # Excel workbooks
├── power-query/                   # Extracted .m files
└── .claude/
    ├── commands/
    │   ├── initialize-project.md  # Phase 0 Step 1
    │   ├── resolve-ambiguities.md # Phase 0 Step 2
    │   ├── generate-artifacts.md  # Phase 0 Step 3
    │   └── extract-queries.md     # Phase 0 Step 4
    ├── context/
    │   ├── glossary.md            # Variable dictionary
    │   ├── assumptions.md         # Interpretation decisions
    │   ├── llm-pitfalls.md        # Common mistakes checklist
    │   └── data-architecture.md   # Bronze-Silver-Gold
    ├── tasks/
    │   └── _phase-0-status.md     # Phase 0 tracker
    └── reference/
        ├── ambiguity-report.md
        ├── data-contracts.md
        ├── query-manifest.md
        └── dependency-graph.md
```

**5-Dimension Difficulty Scoring**:
1. Query Dependency Depth (1-10)
2. Formula Complexity (1-10)
3. Error Surface (1-10)
4. Regulatory Precision (1-10)
5. Performance Impact (1-10)

**Now**: Phase 0 pattern documented in `extras/advanced/` for projects that need it.

## Key Patterns Worth Preserving

### Difficulty-Based Task Breakdown
Tasks with difficulty >= 7 must be broken down before work begins. Subtasks should have difficulty <= 6. This pattern is preserved in `base/`.

### Command Structure
```markdown
# Command: [Name]

## Purpose
[What this command does]

## Context Required
- [Files to read first]

## Process
1. [Step-by-step instructions]

## Output Location
- [Where to save results]
```

### CLAUDE.md as Router
Keep CLAUDE.md under 100 lines. Point to specific docs rather than duplicating content.

### Status Values
- Pending, In Progress, Blocked, Broken Down, Finished
- "Broken Down" tasks cannot be worked on directly
- Parent auto-completes when all subtasks finish

## Migration Path

If you have an old project using these templates:

1. Keep your existing structure - it still works
2. For new projects, just copy `base/`
3. Add files from `extras/` as needed
4. The task management system is unchanged

## Files Deleted

The following directories contained the template implementations:
- `templates/data-analytics/` (5 files)
- `templates/documentation-content/` (5 files)
- `templates/life-projects/` (5 files)
- `templates/power-query/` (17 files)
- `templates/research-analysis/` (5 files)

Total: ~69 files consolidated into this summary.
