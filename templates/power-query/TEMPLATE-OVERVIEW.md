# Power Query Template - Overview

## Purpose

This template provides a complete system for building Power Query projects with Claude Code, specializing in:

- **Regulatory/Compliance Calculations** (EU Battery Regulation, ISO standards, etc.)
- **Complex Data Pipelines** (Bronze-Silver-Gold medallion architecture)
- **Excel Power Query Projects** (with git-friendly .m file version control)

## Unified Structure Approach

This template integrates components from two original approaches:
1. **Minimal** - Quick setup for existing PQ projects (3 files)
2. **Comprehensive** - Full Phase 0 initialization for complex regulatory projects (27 files)

The repository's general structure can accommodate both use cases by selecting appropriate components.

## Core Innovation: Phase 0 Workflow

**Problem Solved**: LLMs frequently misinterpret ambiguous regulatory language, leading to inconsistent implementations across sessions.

**Solution**: Front-load ALL ambiguity resolution BEFORE coding begins.

### Phase 0 Steps
1. **initialize-project.md** - Analyze calculation documents, extract ambiguities
2. **resolve-ambiguities.md** - Interactive batch resolution (5 at a time)
3. **generate-artifacts.md** - Create glossary, data contracts, initial tasks
4. **extract-queries.md** - Extract .m files from Excel, enable watch mode

### Phase 0 Outputs
- **glossary.md** - Every variable defined (eliminates interpretation ambiguity)
- **assumptions.md** - All interpretation decisions documented
- **data-contracts.md** - Expected schemas for each query
- **query-manifest.md** - What each query does
- **dependency-graph.md** - Query execution order

After Phase 0: Claude implements queries following exact specifications with no ambiguity questions.

## Directory Structure

```
templates/power-query/
├── commands/                  # Phase 0 + Phase 1 command files
│   ├── initialize-project.md
│   ├── resolve-ambiguities.md
│   ├── generate-artifacts.md
│   ├── extract-queries.md
│   ├── complete-task.md
│   ├── breakdown.md
│   ├── validate-query.md
│   ├── sync-tasks.md
│   └── update-tasks.md
│
├── context/                   # PQ-specific context files
│   ├── overview.md            # Template for project description
│   ├── llm-pitfalls.md        # Mandatory checklist before implementing
│   ├── power-query.md         # M-code standards
│   ├── naming.md              # Naming conventions
│   ├── error-handling.md      # Error handling patterns
│   ├── data-architecture.md   # Bronze-Silver-Gold pattern
│   ├── validation-rules.md    # Task validation criteria
│   └── critical_rules.md      # Domain-specific gotchas template
│
├── reference/                 # Reference documentation
│   ├── difficulty-guide-pq.md # PQ-specific difficulty scoring
│   └── breakdown-workflow.md  # Task breakdown workflow
│
├── CLAUDE-template.md         # Comprehensive CLAUDE.md template
├── CLAUDE-minimal.md          # Minimal CLAUDE.md template
├── QUICKSTART.md              # Quick reference guide
├── SETUP-GUIDE.md             # Comprehensive setup walkthrough
├── FILE-MANIFEST.md           # Complete file listing with purposes
├── STRUCTURE.md               # Directory structure details
└── README.md                  # Human-readable overview
```

## Key Features

### 1. LLM Pitfalls Checklist
Pre-populated list of common mistakes LLMs make when interpreting regulatory documents:
- Ambiguity in legal language
- Implicit calculation steps
- Unit inconsistencies
- Circular references
- Null propagation errors
- Try/otherwise misuse

### 2. Power Query-Specific Difficulty Scoring
5-dimension scoring system:
- **Query Dependency Depth** (1-10)
- **Formula Complexity** (1-10)
- **Error Surface** (1-10)
- **Regulatory Precision** (1-10)
- **Performance Impact** (1-10)

**Rule**: Tasks ≥7 must be broken down into subtasks ≤6.

### 3. Automatic Glossary Generation
From ambiguity resolutions, creates variable dictionary:
```markdown
| Variable Name | Type | Unit | Description | Source |
|---------------|------|------|-------------|--------|
| RecycledContentShare | Decimal | % | Share of recycled content | Art. 7(1) |
```

### 4. Schema Validation Without Execution
`validate-query.md` performs static analysis to verify query schemas match contracts without running Excel.

### 5. Excel Power Query Editor Integration
- Watch mode auto-syncs .m files to Excel
- Git-friendly: .m files are source of truth
- Automatic backups before sync

## When to Use This Template

**Use Comprehensive Approach When:**
- Implementing regulatory/compliance calculations
- Source documents have ambiguous language
- Multiple calculation methods need reconciliation
- Audit trail required
- Zero error tolerance
- Team needs shared variable definitions

**Use Minimal Approach When:**
- Existing PQ project needs documentation
- Simple data transformations
- No regulatory requirements
- Solo developer, no shared context needed
- Quick prototyping

## Integration with Repository Structure

This template follows the repository's component-based approach:

1. **Commands** - Reusable workflow patterns
2. **Context** - Project understanding files
3. **Reference** - Supporting documentation
4. **Templates** - CLAUDE.md and overview.md templates

Users can:
- Use all components (comprehensive)
- Select specific components (custom)
- Reference patterns for other domains (reusable)

## Typical Workflow

### Comprehensive Project Setup
```bash
# 1. Copy template components to new project
cp -r templates/power-query/.claude/commands/ my-project/.claude/commands/
cp -r templates/power-query/.claude/context/ my-project/.claude/context/
cp -r templates/power-query/.claude/reference/ my-project/.claude/reference/
cp templates/power-query/CLAUDE-template.md my-project/CLAUDE.md

# 2. Add calculation documents
# Place PDFs in my-project/calculation-docs/

# 3. Edit overview.md
# Fill in project details

# 4. Run Phase 0
# @.claude/commands/initialize-project.md
# @.claude/commands/resolve-ambiguities.md (multiple times)
# @.claude/commands/generate-artifacts.md
# @.claude/commands/extract-queries.md

# 5. Execute tasks (Phase 1)
# @.claude/commands/complete-task.md 1
```

### Minimal Project Setup
```bash
# 1. Copy minimal CLAUDE.md
cp templates/power-query/CLAUDE-minimal.md my-project/CLAUDE.md

# 2. Copy critical_rules.md template
cp templates/power-query/context/critical_rules.md my-project/docs/

# 3. Start coding
# No Phase 0 needed for simple projects
```

## Reusable Concepts for Other Templates

Components useful beyond Power Query:

1. **Phase 0 Pattern** - Front-load ambiguity resolution
   - Applicable to: Legal document analysis, API spec implementation, requirement analysis

2. **LLM Pitfalls Checklist** - Domain-specific mistake prevention
   - Applicable to: Any domain with non-obvious rules (finance, healthcare, legal)

3. **Glossary Generation** - Variable naming dictionary
   - Applicable to: Multi-developer projects, domain-heavy projects

4. **Difficulty Scoring Dimensions** - Domain-specific complexity metrics
   - Applicable to: Custom difficulty scoring for specialized domains

5. **critical_rules.md Pattern** - Capture LLM misinterpretations
   - Applicable to: Any project where LLMs make repeated mistakes

## Files Generated During Use

When a user applies this template to their project:

**Phase 0 Generates:**
- `.claude/reference/ambiguity-report.md`
- `.claude/context/glossary.md`
- `.claude/context/assumptions.md`
- `.claude/reference/data-contracts.md`
- `.claude/reference/query-manifest.md`
- `.claude/reference/dependency-graph.md`
- `.claude/tasks/task-*.json`
- `.claude/tasks/_phase-0-status.md`

**Phase 1 Generates:**
- `power-query/*.m` files (extracted from Excel)
- Updated task statuses

## Related Documentation

- **QUICKSTART.md** - Fast 5-minute overview
- **SETUP-GUIDE.md** - Comprehensive walkthrough
- **FILE-MANIFEST.md** - Complete file listing
- **difficulty-guide-pq.md** - Detailed scoring guide
- **llm-pitfalls.md** - Complete pitfall checklist

## Example Use Case

**EU Battery Regulation Carbon Footprint Formula (CFF) Calculation**

**Challenge:**
- Delegated Act Article 7 has ambiguous language ("and/or", implicit steps)
- ISO 22628 standard conflicts with some interpretations
- Need audit trail for regulatory compliance

**Solution with This Template:**
1. Phase 0 found 23 ambiguities
2. User resolved in 5 batches (45 minutes)
3. Generated glossary with 47 terms
4. Created 15 tasks (3 at difficulty 8, broken down)
5. Claude implemented 8 queries following exact specs
6. Zero ambiguity questions during implementation
7. Full audit trail via assumptions.md

**Result:** Compliant implementation with documented decisions.

## Version History

- **Original PQ-Project-Starter 1** - Minimal approach (3 files)
- **Original PQ-Project-Starter 2** - Comprehensive approach (27 files)
- **Current Unified Template** - Component-based, supports both use cases

## Contributing

When updating this template:
1. Keep minimal/comprehensive paths viable
2. Document new components in FILE-MANIFEST.md
3. Update difficulty scoring if new dimensions added
4. Add new pitfalls to llm-pitfalls.md
5. Test both workflow paths

## Support

- Excel Power Query Editor extension: https://github.com/ewc3labs/excel-power-query-editor
- Power Query M reference: https://learn.microsoft.com/en-us/powerquery-m/
- Template issues: Check repository README.md
