# Pension Calculator Example

This example demonstrates how the **Power Query template** is automatically selected and configured for Power BI/Excel projects.

## What This Example Shows

### Template Detection
When the specification was provided to Claude Code's smart-bootstrap system, it automatically selected the **Power Query template** because it detected:
- Keywords: "Power Query", "DAX", "M Code"
- Power BI/Excel context
- Data transformation requirements
- Business intelligence patterns

### Generated Structure
The `.claude/` environment was specifically configured for Power Query development with:

1. **Phase 0 Workflow** - Ambiguity resolution before coding
2. **5-Dimension Difficulty Scoring** - M complexity, DAX complexity, data volume, performance, query folding
3. **Power Query Standards** - M code conventions, DAX patterns
4. **LLM Pitfall Checklist** - Common AI mistakes with Power Query

### Key Benefits Demonstrated

#### 1. Phase 0: Ambiguity Resolution
Before any code is written, the template enforces:
- Stakeholder interviews
- Edge case documentation
- Data quality standards
- Regulatory requirement clarification

This prevents the common problem of building the wrong solution.

#### 2. Multi-Dimensional Difficulty Scoring
Tasks are scored on 5 dimensions specific to Power Query:
```
Task: "Implement pension calculation function"
- M Complexity: 7 (iterative logic)
- DAX Complexity: 5 (time intelligence)
- Data Volume: 6 (10,000+ records)
- Performance: 8 (query folding issues)
- Integration: 4 (standard sources)
Overall Difficulty: 8 (requires breakdown)
```

#### 3. LLM-Specific Guardrails
The template includes warnings about common AI mistakes:
- Not understanding query folding
- Incorrect DAX context transitions
- Mixing M and DAX inappropriately
- Performance anti-patterns

## How It Was Created

### 1. User Provided Specification
```bash
# User created original-spec.md with Power Query requirements
```

### 2. Bootstrap Command
```
"Create environment from claude_code_environment repo using spec: original-spec.md"
```

### 3. Automatic Processing
Claude Code:
1. Read the specification
2. **Detected Power Query keywords** → Selected Power Query template
3. Generated `.claude/` with domain-specific features
4. Created Phase 0 tasks for ambiguity resolution
5. Set up 5-dimension scoring system
6. Added Power Query-specific commands

### 4. Ready for Power Query Development
The project is now ready with:
- Phase 0 ambiguity tasks
- Multi-dimensional difficulty scoring
- M code and DAX standards
- Performance optimization guides
- Query folding checklist

## Compare With Other Templates

The **Power Query template** provides:
- Phase 0 ambiguity resolution workflow
- 5-dimension difficulty scoring
- M code formatting standards
- DAX best practices
- Query folding optimization guides
- Common pitfall warnings

Compare with:
- **simple-todo-app/** - Base template for general development
- **research-project/** - Research template for academic work

## Files in This Example

```
pension-calculator/
├── original-spec.md           # The input specification
├── generated-environment/     # What was generated
│   └── .claude/
│       ├── commands/         # Including validate-m-code.md
│       ├── context/          # With Power Query standards
│       ├── tasks/           # Phase 0 tasks first
│       └── reference/       # 5-dimension scoring guide
└── README.md                # This explanation
```

## Power Query Template Features

### Phase 0 Workflow
All projects start with ambiguity resolution:
1. Stakeholder interviews
2. Edge case documentation
3. Data quality standards
4. Success criteria definition

### 5-Dimension Difficulty Scoring
Every task is evaluated on:
1. **M Complexity** - Language features, recursion, custom functions
2. **DAX Complexity** - Context transitions, time intelligence, relationships
3. **Data Volume** - Row counts, refresh frequency
4. **Performance** - Query folding, incremental refresh
5. **Integration** - Data sources, APIs, authentication

### LLM Pitfall Warnings
Common mistakes to avoid:
- Confusing M and DAX syntax
- Ignoring query folding
- Creating cartesian products
- Misunderstanding evaluation contexts
- Using inefficient iterators

## Using This Pattern

To create your own Power Query project:

1. Write a specification mentioning Power Query/DAX/Power BI
2. Open VS Code in new project directory
3. Tell Claude Code: "Create environment using spec: [path]"
4. Complete Phase 0 tasks first
5. Use 5-dimension scoring for task planning

The Power Query template works well for:
- Power BI reports
- Excel Power Query solutions
- Data transformation projects
- Financial modeling
- Business intelligence dashboards