# Template Customization Guide

This guide explains how to customize environment templates for specific use cases, from choosing the right starting point to adding domain-specific enhancements.

---

## Quick Decision Tree

```
Start Here
    |
    ├─ Need task tracking only?
    │  └─> Use Minimal Setup (5 minutes)
    |
    ├─ Standard web/data/BI project?
    │  └─> Use corresponding Full Template
    |
    └─ Specialized domain (regulatory, medical, financial)?
       └─> Start with Base Template + Domain Customizations
```

---

## Part 1: Choosing Your Starting Point

### Option A: Minimal Setup (5 minutes)

**Use when**:
- Project has < 10 tasks
- Learning or experimental work
- Single-file scripts or utilities
- Solo developer, no shared context needed
- Quick prototyping

**What you get**:
```
project/
├── CLAUDE.md (minimal router)
└── .claude/
    └── tasks/
        ├── task-overview.md
        └── task-*.json files
```

**Upgrade path**: Add folders as needed (see Part 3)

---

### Option B: Base Template (Full)

**Use when**:
- Project has 10+ tasks
- Multiple technologies to track
- Need reusable command patterns
- Team collaboration
- Production systems

**What you get**:
```
project/
├── CLAUDE.md
├── README.md
└── .claude/
    ├── commands/
    │   ├── complete-task.md
    │   ├── breakdown.md
    │   ├── sync-tasks.md
    │   └── update-tasks.md
    ├── context/
    │   ├── overview.md
    │   ├── validation-rules.md
    │   └── standards/
    ├── tasks/
    │   ├── task-overview.md
    │   └── task-*.json
    └── reference/
        ├── difficulty-guide.md
        └── breakdown-workflow.md
```

---

### Option C: Domain-Specific Template

**Available templates**:
1. **Data Engineering** - ETL pipelines, data transformation
2. **BI/Dashboard** - Analytics, reporting, visualization
3. **Hybrid** - Combined data + BI workflows
4. **Power Query** - Regulatory calculations, Excel integration

**Use when**:
- Project fits one of these domains
- Need domain-specific commands and patterns
- Want pre-configured difficulty scoring for domain
- Benefit from domain-specific pitfalls checklist

**What you get**: Base Template + domain enhancements (see Part 2)

---

## Part 2: Domain-Specific Customizations

### Adding Domain Context Files

#### Standard Context Files (All Templates)
- `overview.md` - Project description and goals
- `validation-rules.md` - Task validation criteria
- `standards/` folder - Technology-specific conventions

#### Domain-Specific Context Files

**For Regulatory/Compliance Projects** (like Power Query):
- `glossary.md` - Definitive term/variable definitions
- `assumptions.md` - All interpretation decisions
- `llm-pitfalls.md` - Domain-specific mistake checklist
- `critical_rules.md` - DO/DON'T rules for technology

**For Data Engineering**:
- `data-architecture.md` - Pipeline patterns (Bronze-Silver-Gold)
- `naming.md` - Naming conventions for datasets/tables
- `error-handling.md` - Retry/recovery patterns
- `schema-evolution.md` - How to handle schema changes

**For BI/Dashboard**:
- `visualization-standards.md` - Chart types, color palettes
- `data-refresh.md` - Refresh schedules and dependencies
- `performance.md` - Query optimization guidelines
- `security.md` - Row-level security patterns

**For Web Development**:
- `component-patterns.md` - React/Vue/Angular patterns
- `state-management.md` - Redux/Context/Zustand conventions
- `api-integration.md` - REST/GraphQL patterns
- `accessibility.md` - WCAG compliance checklist

**For DevOps/Infrastructure**:
- `deployment-process.md` - CI/CD pipeline steps
- `monitoring-standards.md` - Metrics, logs, alerts
- `security-checklist.md` - Security review requirements
- `rollback-procedures.md` - How to revert changes

---

### Customizing Difficulty Scoring

#### Default Scoring (1-10 scale)

Base templates use simple 1-10 difficulty scoring:
- **1-2**: Trivial (fix typo, update text)
- **3-4**: Low (basic CRUD, simple UI)
- **5-6**: Moderate (form validation, API integration)
- **7-8**: High (auth setup, database migration) - **Must break down**
- **9-10**: Extreme (architecture changes) - **Must break down**

**Rule**: Tasks ≥7 must be broken down before starting work.

---

#### Multi-Dimension Scoring (Advanced)

For specialized domains, use multi-dimension scoring for more accurate assessment.

**Pattern**: Score across 5 domain-relevant dimensions (1-10 each), then average and round.

**Example Dimension Sets**:

**Power Query/Regulatory**:
1. Query Dependency Depth
2. Formula Complexity
3. Error Surface
4. Regulatory Precision
5. Performance Impact

**Web Frontend**:
1. UI Component Complexity
2. State Management Scope
3. API Integration
4. Performance Impact
5. Accessibility Requirements

**Data Engineering**:
1. Data Volume
2. Transformation Complexity
3. Pipeline Dependencies
4. Error Recovery Needs
5. Performance SLA

**DevOps/Infrastructure**:
1. Infrastructure Scope
2. Security Impact
3. Rollback Complexity
4. Monitoring Requirements
5. Cross-Team Dependencies

**Machine Learning**:
1. Data Complexity
2. Model Complexity
3. Training Time
4. Interpretability Requirements
5. Deployment Complexity

---

#### How to Implement Custom Scoring

**Step 1**: Create `reference/difficulty-guide-[domain].md`

```markdown
# Difficulty Scoring Guide for [Domain]

## Scoring System

This project uses 5-dimension difficulty scoring.

### Dimension 1: [Name] (1-10)
- **1-2**: [Low criteria]
- **3-4**: [Low-moderate criteria]
- **5-6**: [Moderate criteria]
- **7-8**: [High criteria]
- **9-10**: [Extreme criteria]

### Dimension 2: [Name] (1-10)
...

### Dimension 3: [Name] (1-10)
...

### Dimension 4: [Name] (1-10)
...

### Dimension 5: [Name] (1-10)
...

## Final Score Calculation

**Final Difficulty = ROUND(AVERAGE(Dim1, Dim2, Dim3, Dim4, Dim5))**

## Breakdown Rule

Tasks with final difficulty ≥7 MUST be broken down using `breakdown.md` before work begins.

## Examples

### Example Task: [Description]
- Dimension 1: 6 - [Reasoning]
- Dimension 2: 8 - [Reasoning]
- Dimension 3: 5 - [Reasoning]
- Dimension 4: 7 - [Reasoning]
- Dimension 5: 4 - [Reasoning]
- **Final: ROUND((6+8+5+7+4)/5) = ROUND(6) = 6**
```

**Step 2**: Reference in `breakdown.md` command

Update the difficulty assessment section to reference your custom guide.

**Step 3**: Document in `context/overview.md`

Mention that this project uses custom difficulty scoring and link to the guide.

---

### Creating Domain-Specific Commands

Commands are reusable workflow patterns stored in `.claude/commands/`.

#### Standard Commands (All Templates)

- `complete-task.md` - Start/finish tasks with status tracking
- `breakdown.md` - Split high-difficulty tasks into subtasks
- `sync-tasks.md` - Update task-overview.md from JSON files
- `update-tasks.md` - Validate task system health

#### When to Add Custom Commands

Add custom commands when you have:
1. **Repeated workflows** - Same process done multiple times
2. **Complex procedures** - Multi-step processes that need documentation
3. **Domain patterns** - Industry-specific workflows
4. **Quality gates** - Validation steps before proceeding

---

#### Custom Command Examples by Domain

**Power Query**:
- `initialize-project.md` - Phase 0: Analyze regulatory documents
- `resolve-ambiguities.md` - Phase 0: Interactive resolution
- `generate-artifacts.md` - Phase 0: Create glossary/contracts
- `extract-queries.md` - Phase 0: Extract .m files from Excel
- `validate-query.md` - Schema validation

**Data Engineering**:
- `create-pipeline.md` - Scaffold new data pipeline
- `test-pipeline.md` - Run data quality tests
- `deploy-pipeline.md` - Deploy to staging/production
- `backfill-data.md` - Historical data loading procedure

**BI/Dashboard**:
- `create-dashboard.md` - Initialize new dashboard
- `validate-metrics.md` - Check calculations against source
- `optimize-queries.md` - Performance tuning workflow
- `deploy-report.md` - Publish to production

**Web Development**:
- `create-component.md` - Scaffold new component with tests
- `create-api-endpoint.md` - Add new API route
- `run-e2e-tests.md` - Execute end-to-end test suite
- `deploy-preview.md` - Create preview deployment

**DevOps**:
- `create-service.md` - Scaffold new microservice
- `add-monitoring.md` - Add metrics/alerts for service
- `create-runbook.md` - Document operational procedures
- `plan-migration.md` - Plan infrastructure migration

---

#### Command File Template

```markdown
# [Command Name]

## Purpose
[1-2 sentence description of what this command does]

## Context Required
[What files/information Claude needs to read before running this command]
- file-1.md
- file-2.json
- Understanding of [concept]

## Process

### Step 1: [First Action]
[Detailed instructions]

### Step 2: [Second Action]
[Detailed instructions]

### Step 3: [Third Action]
[Detailed instructions]

## Output Location
[Where results should be written]
- `.claude/context/[file].md`
- `.claude/reference/[file].md`

## Critical Rules
[Important constraints or gotchas]
- Rule 1
- Rule 2

## Example

[Optional: Show example input/output]
```

---

### Adding Domain-Specific Pitfalls Checklist

If your domain has predictable LLM mistakes, create `context/llm-pitfalls.md`:

```markdown
# LLM Pitfalls for [Domain]

This checklist catalogs common mistakes LLMs make when working with [domain] materials.

IMPORTANT: Review this checklist before implementing tasks in this domain.

## Category 1: [e.g., Security]

**Pattern**: [Description of mistake pattern]
**Example**: [Specific example]
**Correct Approach**: [How to do it right]

### Common Mistakes:
- [ ] [Specific mistake 1]
- [ ] [Specific mistake 2]
- [ ] [Specific mistake 3]

## Category 2: [e.g., Performance]

**Pattern**: [Description of mistake pattern]
**Example**: [Specific example]
**Correct Approach**: [How to do it right]

### Common Mistakes:
- [ ] [Specific mistake 4]
- [ ] [Specific mistake 5]

[Add 3-6 categories based on domain]
```

**Refer to**: `.claude/reference/reusable-template-patterns.md` section 2 for examples across domains.

---

### Adding Critical Rules File

If your technology has "footguns" or common mistakes with severe consequences, create `context/critical_rules.md`:

```markdown
# Critical Rules for [Technology]

These rules MUST be followed. Violations lead to [security issues / data loss / compliance failures].

## Rule 1: [Category - e.g., Input Validation]

**DO**: [Correct approach]
**DON'T**: [What to avoid]
**WHY**: [Consequence of violation]

**Example**:
```[language]
// CORRECT
[code example]

// INCORRECT
[code example showing mistake]
```

## Rule 2: [Category]
[Same format]

[Add 5-10 critical rules]
```

**Refer to**: `.claude/reference/reusable-template-patterns.md` section 4 for examples.

---

## Part 3: Progressive Enhancement (Upgrade Path)

Start minimal and add components as needed:

### From Minimal to Basic Full Template

**When**: Project scope expands beyond 10 tasks

**Add**:
1. `.claude/context/overview.md` - Document project goals
2. `.claude/commands/` folder with standard commands
3. `.claude/reference/` folder for decisions/guides

### From Basic to Domain-Specific

**When**: Domain-specific patterns emerge

**Add**:
1. Domain-specific context files (glossary, pitfalls, critical rules)
2. Custom difficulty scoring guide
3. Domain-specific commands
4. Domain reference materials

### From Simple to Multi-Dimension Scoring

**When**: Simple difficulty scoring proves inadequate

**Add**:
1. `.claude/reference/difficulty-guide-[domain].md`
2. Update `breakdown.md` to reference new guide
3. Document in `context/overview.md`
4. Re-score existing tasks using new system

### Adding Phase 0 Workflow

**When**: Source requirements are ambiguous or need interpretation

**Add**:
1. `.claude/tasks/_phase-0-status.md` - Progress tracker
2. Phase 0 commands:
   - `initialize-project.md`
   - `resolve-ambiguities.md`
   - `generate-artifacts.md`
3. Phase 0 artifacts (generated during execution):
   - `context/glossary.md`
   - `context/assumptions.md`
   - `reference/ambiguity-report.md`
   - Domain-specific contracts/manifests

**Refer to**: `.claude/reference/reusable-template-patterns.md` section 1 for complete Phase 0 pattern.

---

## Part 4: Customization Workflow

### For New Projects

**Step 1: Choose Starting Point**
- Review "Part 1: Choosing Your Starting Point"
- Select minimal, base, or domain-specific template

**Step 2: Initialize Structure**
- Create directory structure for chosen template
- Copy standard files (CLAUDE.md, README.md)
- Initialize `.claude/` folders

**Step 3: Add Domain Customizations** (if needed)
- Review "Part 2: Domain-Specific Customizations"
- Add relevant context files
- Choose scoring system
- Create custom commands if needed
- Add pitfalls checklist
- Add critical rules

**Step 4: Populate Initial Content**
- Write `context/overview.md` with project description
- Create initial tasks in `.claude/tasks/`
- Run `sync-tasks.md` to generate overview

**Step 5: Iterate**
- Start working on tasks
- Add context files as patterns emerge
- Refine difficulty scoring as you learn
- Create commands for repeated workflows

---

### For Existing Projects

**Step 1: Assess Current State**
- How many tasks? (Minimal vs Full)
- What technologies? (Domain-specific needs?)
- Team size? (Collaboration features needed?)
- What patterns repeat? (Custom commands?)

**Step 2: Choose Target Template**
- Based on assessment, select appropriate template level
- Identify which components to add

**Step 3: Incremental Migration**
- Start with `.claude/tasks/` if not present
- Add `.claude/context/overview.md`
- Add commands one at a time as needed
- Add domain-specific files based on pain points

**Step 4: Backfill Documentation**
- Document existing patterns in context files
- Create commands for established workflows
- Score existing tasks using chosen system

---

## Part 5: Decision Matrices

### Should I Use Multi-Dimension Scoring?

| Criteria | Use Simple (1-10) | Use Multi-Dimension |
|----------|-------------------|---------------------|
| Team size | Solo or small (<3) | Medium/Large (3+) |
| Domain complexity | General purpose | Specialized (regulatory, medical, finance) |
| Risk tolerance | Can iterate on mistakes | Zero tolerance for errors |
| Task heterogeneity | Similar task types | Diverse risk profiles |
| Estimation accuracy needs | Rough estimates OK | Need precise effort estimates |

---

### Should I Add Phase 0 Workflow?

| Criteria | Skip Phase 0 | Add Phase 0 |
|----------|--------------|-------------|
| Requirements clarity | Clear, unambiguous | Ambiguous, open to interpretation |
| Source material | Technical specs | Legal/regulatory documents |
| Iteration tolerance | Can clarify during work | Need decisions upfront |
| Audit requirements | No audit trail needed | Need documented decisions |
| Team alignment | Solo or aligned | Need shared definitions |

---

### Should I Create Custom Commands?

| Criteria | Use Standard Commands | Create Custom Commands |
|----------|----------------------|------------------------|
| Workflow repetition | Each task is unique | Repeated patterns exist |
| Process complexity | Simple, self-explanatory | Multi-step, needs documentation |
| Team size | Solo developer | Team needs consistency |
| Domain specificity | General purpose | Industry-specific workflows |
| Onboarding needs | No new team members | Need to train others |

---

## Part 6: Examples

### Example 1: Medical Research Project

**Starting Point**: Base Template

**Customizations Added**:

1. **Context Files**:
   - `clinical-terminology.md` - Medical term definitions
   - `llm-pitfalls.md` - Common medical AI mistakes (dosage, drug names)
   - `privacy-requirements.md` - HIPAA compliance checklist
   - `critical_rules.md` - PHI handling rules

2. **Custom Difficulty Dimensions**:
   - Clinical Complexity
   - Privacy Risk
   - Regulatory Impact
   - Data Sensitivity
   - Validation Requirements

3. **Custom Commands**:
   - `validate-phi-removal.md` - Check for PHI in outputs
   - `clinical-review.md` - Medical expert review workflow
   - `compliance-check.md` - HIPAA validation

---

### Example 2: E-commerce Platform

**Starting Point**: Base Template

**Customizations Added**:

1. **Context Files**:
   - `api-standards.md` - REST conventions
   - `component-patterns.md` - React component guidelines
   - `performance.md` - Page load budgets
   - `security.md` - Payment processing rules

2. **Difficulty Scoring**: Simple 1-10 (works well for web dev)

3. **Custom Commands**:
   - `create-api-endpoint.md` - Scaffold endpoint with tests
   - `create-component.md` - React component with Storybook
   - `run-lighthouse.md` - Performance testing
   - `deploy-preview.md` - Vercel preview deployment

---

### Example 3: Financial Reporting System

**Starting Point**: Base Template + Phase 0

**Customizations Added**:

1. **Phase 0 Workflow** (due to ambiguous GAAP interpretations):
   - `initialize-project.md` - Extract accounting rule ambiguities
   - `resolve-ambiguities.md` - Interactive resolution with accountant
   - `generate-artifacts.md` - Create calculation glossary
   - Output: `glossary.md`, `gaap-interpretations.md`, `calculation-contracts.md`

2. **Context Files**:
   - `accounting-standards.md` - GAAP/IFRS rules
   - `llm-pitfalls.md` - Common financial calculation mistakes
   - `audit-requirements.md` - What auditors will check
   - `critical_rules.md` - Rounding, precision, currency handling

3. **Custom Difficulty Dimensions**:
   - Calculation Complexity
   - Regulatory Precision
   - Audit Criticality
   - Data Volume
   - Cross-Entity Dependencies

---

## Part 7: Quick Reference

### Template Complexity Ladder

1. **Minimal** - Tasks only
2. **Basic** - Tasks + Commands + Context
3. **Domain** - Basic + Domain files + Custom scoring
4. **Phase 0** - Domain + Ambiguity resolution workflow
5. **Full Custom** - All features + Custom dimensions + Multi-phase

**Recommendation**: Start one level below what you think you need, upgrade as patterns emerge.

---

### File Addition Checklist

When adding a new component, ensure:

- [ ] File follows naming convention (lowercase, hyphens)
- [ ] File is referenced in `CLAUDE.md` if core to project
- [ ] Related files are updated (e.g., overview.md mentions new context file)
- [ ] Commands reference context files in "Context Required" section
- [ ] Examples provided for non-obvious patterns
- [ ] Validation rules updated if adding new task criteria

---

### Common Customization Mistakes

1. **Over-engineering early** - Don't add Phase 0 for simple projects
2. **Under-documenting domains** - Specialized domains need context files
3. **Inconsistent naming** - Follow existing conventions
4. **Orphaned files** - Every file should be referenced somewhere
5. **Skipping examples** - Custom patterns need examples
6. **Not updating CLAUDE.md** - Keep router file in sync
7. **Forgetting validation** - New components need validation rules

---

## Next Steps

1. **Review** `.claude/reference/reusable-template-patterns.md` for pattern details
2. **Choose** your starting template using Part 1
3. **Customize** using Part 2 guidance
4. **Iterate** as project evolves
5. **Document** patterns that emerge for future projects

---

**Related Documentation**:
- `reusable-template-patterns.md` - Pattern library
- `templates/[name]/README.md` - Current template specifications
- `legacy-template-reference.md` - Historical comprehensive reference (frozen)
- `breakdown-workflow.md` - Task hierarchy guide
- `difficulty-guide.md` - Scoring system details
