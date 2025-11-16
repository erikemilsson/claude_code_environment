# Power Query Template - Quick Reference

One-page cheat sheet for Power Query project environments.

---

## When to Use This Template

**Use Power Query Template for**:
- Excel Power Query projects
- Regulatory/compliance calculations
- Complex data transformations with legal/financial source documents
- Projects requiring audit trails
- Zero error tolerance scenarios

**Signals you need this template**:
- Source documents contain ambiguous language
- Multiple calculation interpretations possible
- Team needs shared variable definitions
- Regulatory precision required
- Need to version control .m files from Excel

---

## Phase 0 Workflow (4 Steps)

Run BEFORE implementation when requirements are ambiguous:

### Step 1: Initialize Project
**Command**: `@.claude/commands/initialize-project.md`
- Analyze calculation documents
- Extract ambiguities and inconsistencies
- Generate initial ambiguity report

### Step 2: Resolve Ambiguities
**Command**: `@.claude/commands/resolve-ambiguities.md`
- Interactive batch resolution (5 at a time)
- User makes interpretation decisions
- Document all decisions in assumptions.md

### Step 3: Generate Artifacts
**Command**: `@.claude/commands/generate-artifacts.md`
- Create glossary.md (every variable defined)
- Create data-contracts.md (expected schemas)
- Create query-manifest.md (what each query does)
- Create dependency-graph.md (execution order)
- Generate initial tasks

### Step 4: Extract Queries
**Command**: `@.claude/commands/extract-queries.md`
- Extract .m files from Excel workbooks
- Enable version control for Power Query code
- Set up watch mode for changes

**Phase 0 Completion Criteria**:
- All ambiguities resolved
- Every variable has definition in glossary
- All interpretation decisions documented
- Data contracts established
- Initial task list created

---

## Key Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `initialize-project.md` | Phase 0 Step 1 | Start of project, analyze docs |
| `resolve-ambiguities.md` | Phase 0 Step 2 | After ambiguity extraction |
| `generate-artifacts.md` | Phase 0 Step 3 | After resolutions complete |
| `extract-queries.md` | Phase 0 Step 4 | Initialize Excel integration |
| `complete-task.md` | Start/finish tasks | Every task workflow |
| `breakdown.md` | Split high-difficulty tasks | When difficulty ≥7 |
| `validate-query.md` | Schema validation | Before deploying queries |
| `sync-tasks.md` | Update task overview | After task status changes |

---

## 5-Dimension Difficulty Scoring

**Score each task across 5 dimensions (1-10 each), then average and round.**

### Dimension 1: Query Dependency Depth (1-10)
- 1-2: Standalone query, no dependencies
- 3-4: 1-2 upstream queries
- 5-6: 3-5 upstream queries
- 7-8: 6-10 upstream queries, complex dependency chain
- 9-10: 10+ dependencies, circular risk, complex DAG

### Dimension 2: Formula Complexity (1-10)
- 1-2: Simple select/filter
- 3-4: Basic transformations (rename, add column)
- 5-6: Moderate logic (conditional columns, grouping)
- 7-8: Complex transformations (pivots, multiple joins, nested logic)
- 9-10: Advanced M code (custom functions, list operations, recursion)

### Dimension 3: Error Surface (1-10)
- 1-2: Minimal failure modes, forgiving data
- 3-4: Some edge cases, basic null handling
- 5-6: Multiple error scenarios, type coercion needed
- 7-8: Many failure modes, complex error handling
- 9-10: Extreme error risk, requires extensive try/otherwise

### Dimension 4: Regulatory Precision (1-10)
- 1-2: Informational only, no compliance impact
- 3-4: Referenced in reports, low regulatory risk
- 5-6: Used in compliance calculations, moderate oversight
- 7-8: Direct regulatory reporting, high precision required
- 9-10: Critical compliance metric, audit focus, zero tolerance

### Dimension 5: Performance Impact (1-10)
- 1-2: Tiny dataset, instant execution
- 3-4: Small data, < 1 second
- 5-6: Moderate data, 1-10 seconds
- 7-8: Large data, 10-60 seconds, optimization needed
- 9-10: Very large data, > 1 minute, performance critical

**Final Score** = ROUND(AVERAGE(Dim1, Dim2, Dim3, Dim4, Dim5))

**Breakdown Rule**: Tasks with final difficulty ≥7 MUST be broken down using `breakdown.md` before starting work.

---

## LLM Pitfalls Checklist

Review `context/llm-pitfalls.md` before implementing. Common mistakes:

### Ambiguity Pitfalls
- [ ] Assuming specific interpretation without confirming
- [ ] Not flagging vague language in source documents
- [ ] Treating "may" as "must" or vice versa

### Calculation Pitfalls
- [ ] Missing implicit calculation steps from regulatory text
- [ ] Incorrect order of operations
- [ ] Not handling edge cases mentioned in footnotes

### Technical Pitfalls
- [ ] Unit inconsistencies (days vs years, dollars vs cents)
- [ ] Null propagation errors (null in arithmetic)
- [ ] Type coercion mistakes (text to number, date formats)
- [ ] Overusing try/otherwise (masking real errors)
- [ ] Circular reference risks in dependent queries

### M-Code Specific
- [ ] Mutation attempts (M is functional, immutable)
- [ ] List vs Table confusion
- [ ] Step reference errors (using wrong previous step name)
- [ ] Missing "in" keyword in let expressions
- [ ] Incorrect error handling patterns

---

## Critical Context Files

| File | Purpose | Check Before |
|------|---------|--------------|
| `glossary.md` | Every variable definition | Implementing any calculation |
| `assumptions.md` | All interpretation decisions | Making judgment calls |
| `llm-pitfalls.md` | Common mistake checklist | Starting new task |
| `data-architecture.md` | Bronze-Silver-Gold pattern | Structuring queries |
| `power-query.md` | M-code conventions | Writing M code |
| `critical_rules.md` | DO/DON'T rules | Code review |

---

## Project Structure

```
project/
├── CLAUDE.md
├── README.md
├── calculation-docs/           # Source regulatory PDFs
├── excel-files/                # Excel workbooks with Power Query
├── power-query/                # Extracted .m files (git tracked)
└── .claude/
    ├── commands/
    │   ├── initialize-project.md
    │   ├── resolve-ambiguities.md
    │   ├── generate-artifacts.md
    │   ├── extract-queries.md
    │   ├── complete-task.md
    │   ├── breakdown.md
    │   ├── validate-query.md
    │   ├── sync-tasks.md
    │   └── update-tasks.md
    ├── context/
    │   ├── overview.md
    │   ├── glossary.md              # Phase 0 output
    │   ├── assumptions.md           # Phase 0 output
    │   ├── llm-pitfalls.md
    │   ├── data-architecture.md
    │   ├── validation-rules.md
    │   ├── power-query.md
    │   ├── naming.md
    │   ├── error-handling.md
    │   └── critical_rules.md
    ├── tasks/
    │   ├── _phase-0-status.md
    │   ├── task-overview.md
    │   └── task-*.json
    └── reference/
        ├── ambiguity-report.md      # Phase 0 output
        ├── data-contracts.md        # Phase 0 output
        ├── query-manifest.md        # Phase 0 output
        ├── dependency-graph.md      # Phase 0 output
        ├── difficulty-guide-pq.md
        └── breakdown-workflow.md
```

---

## Typical Workflow

### Initial Setup (Phase 0)
1. Create project structure
2. Add regulatory/calculation documents to `calculation-docs/`
3. Run `initialize-project.md` → extracts ambiguities
4. Run `resolve-ambiguities.md` → interactive resolution
5. Run `generate-artifacts.md` → creates glossary, contracts, tasks
6. Run `extract-queries.md` → extracts .m files from Excel
7. Review `_phase-0-status.md` for completion

### Implementation Phase
1. Read `task-overview.md` to see all tasks
2. For each task:
   - Run `complete-task.md` to start
   - If difficulty ≥7, run `breakdown.md` first
   - Check `glossary.md` for variable definitions
   - Check `llm-pitfalls.md` for common mistakes
   - Implement in Excel Power Query
   - Run `extract-queries.md` to capture .m file
   - Run `validate-query.md` for schema check
   - Mark task complete in `complete-task.md`
3. Run `sync-tasks.md` to update overview

### Maintenance
- Re-run `extract-queries.md` after Excel changes
- Update `glossary.md` if new variables added
- Update `assumptions.md` if interpretations change
- Keep `data-contracts.md` in sync with actual schemas

---

## Decision Tree

```
Do you have regulatory/compliance calculations?
│
├─ YES → Do source documents have ambiguous language?
│        │
│        ├─ YES → Use Phase 0 Workflow (full comprehensive approach)
│        │        1. initialize-project.md
│        │        2. resolve-ambiguities.md
│        │        3. generate-artifacts.md
│        │        4. extract-queries.md
│        │
│        └─ NO → Use minimal approach (skip Phase 0, start with tasks)
│
└─ NO → Consider Base Template or Data Engineering Template instead
```

---

## When to Use Comprehensive vs Minimal

### Comprehensive (with Phase 0)
- Implementing regulatory/compliance calculations
- Source documents have ambiguous language
- Multiple calculation methods need reconciliation
- Audit trail required
- Zero error tolerance
- Team needs shared variable definitions

### Minimal (skip Phase 0)
- Existing PQ project needs documentation
- Simple data transformations
- No regulatory requirements
- Solo developer, no shared context needed
- Quick prototyping
- Requirements are crystal clear

---

## Common Mistakes

1. **Skipping Phase 0** when source docs are ambiguous → leads to rework
2. **Not using glossary** → inconsistent variable interpretations
3. **Ignoring LLM pitfalls** → common M-code mistakes
4. **Not breaking down difficulty ≥7** → tasks too complex, errors increase
5. **Forgetting to extract .m files** → changes lost, no version control
6. **Not validating schemas** → runtime errors in production
7. **Skipping assumptions.md** → lose context on why decisions were made

---

## Success Metrics

**Phase 0 Success**:
- Zero ambiguities remain unresolved
- Every variable in glossary
- All assumptions documented
- Data contracts match actual query outputs

**Implementation Success**:
- Tasks with difficulty ≥7 are broken down
- All queries have validated schemas
- .m files version controlled
- No critical rule violations
- LLM pitfall checklist reviewed for each task

---

## Quick Links

**Full Documentation**:
- Template structure: `templates/power-query/README.md`
- Historical reference: `legacy-template-reference.md` (frozen snapshot)
- Customization guide: `.claude/reference/template-customization-guide.md`
- Reusable patterns: `.claude/reference/reusable-template-patterns.md`
- Breakdown workflow: `.claude/reference/breakdown-workflow.md`
- Difficulty guide: `.claude/reference/difficulty-guide-pq.md`

**Key Context Files**:
- `context/glossary.md` - Variable definitions
- `context/assumptions.md` - Interpretation decisions
- `context/llm-pitfalls.md` - Common mistakes
- `context/critical_rules.md` - DO/DON'T rules

**Task Management**:
- `tasks/task-overview.md` - All tasks summary
- `tasks/_phase-0-status.md` - Phase 0 progress

---

**Print this page and keep it visible while working on Power Query projects.**
