# CLAUDE.md

This file provides guidance to [Claude Code](claude.ai/code) when working with code in this repository.



### Core Files

1. **CLAUDE.md** - LLM instructions and project overview
2. **[file].xlsx** - Main Excel workbook with Power Query
3. **[file].xlsx_PowerQuery.m** - Exported Power Query code (for version control)



### Documentation Files

4. **[reference_tables.md](docs/reference_tables.md)** - Quick lookup for formulas, material routing, edge cases
5. **[critical_rules.md](docs/critical_rules.md)** - Non-obvious domain rules that prevent errors (domain-specific gotchas)]



### Project Management

6. **[task_tracker.md](docs/task_tracker.md)** - Active/completed/backlog tasks



## Implementation Rules

### General  Rules

- Do not write code without me asking for it
- Do not suggest data validation changes
- Only write code strictly for the task that I have asked for help. Do not write data validation script unless that is the task you have been given.



### [critical_rules.md](docs/critical_rules.md)

[critical_rules.md](docs/critical_rules.md)  captures non-obvious implementation rules that LLMs frequently misunderstand, leading to contradictory suggestions across conversations. Red flags that indicate you should consult this document are:

- "This looks like a bug..."

- "We should simplify..."

- "Why doesn't this match..."

- "Let's make this consistent with..."

- "This hardcoded value should be..."

The rules in [critical_rules.md](docs/critical_rules.md) may be updated as new changes are implemented. The document has the following structure:  

```
## Critical Rule: [Description]

**Why this looks wrong but isn't:** 

- [Reason A for why it looks wrong]
- ...

**DO / DO NOT:** [Action to take or not take by the LLM]
```



## ARCHITECTURE

General Rules:

- No VBA
- No Array formulas
- Keep power query
- 

Table A

- Type of table (input, PQ-reference, output)
- 

Purpose

- Data validated rows?



## File & Folder Structure

```
project_name/
├── CLAUDE.md                          # Project overview, architecture, dev tasks
├── ProjectName_template.xlsx          # Main workbook (gitignored)
├── ProjectName_template.xlsx_PowerQuery.m  # Exported M code
├── docs/
├──── reference_tables.md                # Quick reference data
├──── critical_rules.md                  # Domain-specific gotchas
└──── task_tracker.md                    # Tasks
```







# Data Architecture

## Medallion Structure



## Data Validation

<Data validation rules and methods will be specificed here>

General Guidelines:

- Keep it simple
- Do not add validation scripts unless it has been agreed on with me.
