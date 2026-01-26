# Reusable Template Patterns

This document catalogs reusable patterns extracted from domain-specific templates (particularly Power Query) that can be adapted for other template types.

## 1. Phase 0 Ambiguity Resolution Workflow

**Origin**: Power Query template for regulatory/compliance projects

**Pattern**: Multi-step initialization workflow that resolves ambiguities before implementation begins

**Structure**:
1. **Analyze** - Examine source documents/requirements, extract ambiguities and inconsistencies
2. **Resolve** - Interactive batch resolution (present 5 ambiguities at a time, get user decisions)
3. **Generate** - Create definitive artifacts (glossary, assumptions, contracts)
4. **Initialize** - Set up project structure with resolved specifications

**Commands**:
- `initialize-project.md` - Step 1: Analyze and extract ambiguities
- `resolve-ambiguities.md` - Step 2: Interactive resolution session
- `generate-artifacts.md` - Step 3: Create documentation artifacts
- `extract-queries.md` or equivalent - Step 4: Initialize project structure

**Status Tracking**:
- `_phase-0-status.md` - Progress tracker showing which steps are complete

**Artifacts Generated**:
- `glossary.md` - Definitive term/variable definitions
- `assumptions.md` - All interpretation decisions documented
- `data-contracts.md` or equivalent - Expected interfaces/schemas
- Domain-specific manifests

**When to Adapt**:
- Legal/compliance domains (contracts, regulations)
- Medical/healthcare (clinical guidelines, protocols)
- Financial (accounting standards, tax rules)
- Any domain where source material contains:
  - Ambiguous language
  - Multiple valid interpretations
  - Implicit assumptions
  - Need for audit trail
  - Zero-tolerance for misinterpretation

**Adaptation Examples**:
- **Medical Protocol Template**: Extract drug name ambiguities, dosage interpretations, timing definitions
- **Legal Contract Template**: Extract jurisdiction-specific interpretations, defined terms, obligation mappings
- **Financial Reporting Template**: Extract calculation definitions, rounding rules, classification criteria

---

## 2. Domain-Specific Pitfalls Checklist

**Origin**: `context/llm-pitfalls.md` in Power Query template

**Pattern**: Pre-populated checklist of common LLM mistakes specific to a domain

**Structure**:
```markdown
# LLM Pitfalls for [Domain]

This checklist catalogs common mistakes LLMs make when working with [domain] materials.

## Category 1: [e.g., Terminology]
- [ ] Mistake pattern 1
- [ ] Mistake pattern 2

## Category 2: [e.g., Calculations]
- [ ] Mistake pattern 3
- [ ] Mistake pattern 4
```

**Power Query Example Categories**:
1. Ambiguity in legal language
2. Implicit calculation steps
3. Unit inconsistencies
4. Circular references
5. Null propagation errors
6. Try/otherwise misuse

**Adaptation Examples**:

**Web Development**:
- XSS vulnerability patterns
- State mutation mistakes
- Missing key props in lists
- Race conditions in async code
- Memory leaks in event handlers

**SQL/Database**:
- SQL injection vulnerabilities
- N+1 query problems
- Missing indexes on foreign keys
- Improper NULL handling
- Transaction isolation issues

**React Development**:
- Direct state mutation
- Missing dependencies in useEffect
- Infinite render loops
- Prop drilling anti-patterns
- Missing error boundaries

**DevOps/Infrastructure**:
- Hardcoded credentials
- Missing health checks
- Inadequate resource limits
- Single points of failure
- Missing rollback procedures

**When to Include**:
- Domain has specialized knowledge
- Common mistakes are predictable
- Errors have severe consequences
- Team members have varying expertise levels

---

## 3. Multi-Dimension Difficulty Scoring

**Origin**: 5-dimension scoring system in Power Query template

**Pattern**: Instead of single 1-10 difficulty score, evaluate tasks across multiple relevant dimensions, then average

**Power Query Dimensions**:
1. Query Dependency Depth (1-10)
2. Formula Complexity (1-10)
3. Error Surface (1-10)
4. Regulatory Precision (1-10)
5. Performance Impact (1-10)

**Final Score = Average of 5 dimensions, rounded to nearest integer**

**Benefits**:
- More accurate difficulty assessment
- Identifies specific risk areas
- Helps with task breakdown strategy
- Provides better context for effort estimation

**Adaptation Examples**:

**Web Frontend Template**:
1. UI Component Complexity (1-10) - Number of states, interactions
2. State Management Scope (1-10) - Local vs global, async complexity
3. API Integration (1-10) - Endpoints involved, error handling
4. Performance Impact (1-10) - Render frequency, bundle size
5. Accessibility Requirements (1-10) - WCAG level, screen reader support

**Data Engineering Template**:
1. Data Volume (1-10) - GB/TB processed
2. Transformation Complexity (1-10) - Join depth, aggregation logic
3. Pipeline Dependencies (1-10) - Upstream/downstream count
4. Error Recovery Needs (1-10) - Idempotency, retry complexity
5. Performance SLA (1-10) - Real-time vs batch, latency requirements

**DevOps/Infrastructure Template**:
1. Infrastructure Scope (1-10) - Services affected, environment count
2. Security Impact (1-10) - Blast radius, compliance requirements
3. Rollback Complexity (1-10) - State management, data migrations
4. Monitoring Requirements (1-10) - Metrics, alerts, dashboards needed
5. Cross-Team Dependencies (1-10) - Coordination overhead

**Machine Learning Template**:
1. Data Complexity (1-10) - Feature engineering needs, data quality
2. Model Complexity (1-10) - Algorithm sophistication, hyperparameter space
3. Training Time (1-10) - Computational resources needed
4. Interpretability Requirements (1-10) - Explainability needs
5. Deployment Complexity (1-10) - Serving infrastructure, monitoring

**Implementation**:
- Document dimensions in `reference/difficulty-guide-[domain].md`
- Reference in task breakdown process
- Use in `breakdown.md` command to assess when tasks need splitting

---

## 4. Critical Rules Pattern

**Origin**: `context/critical_rules.md` in Power Query template

**Pattern**: Technology or domain-specific DO/DON'T rules that prevent critical mistakes

**Structure**:
```markdown
# Critical Rules for [Technology/Domain]

These rules MUST be followed. Violations lead to [severe consequence].

## Rule 1: [Category]
**DO**: [Correct approach]
**DON'T**: [What to avoid]
**WHY**: [Consequence of violation]
**EXAMPLE**: [Code sample]

## Rule 2: [Category]
...
```

**When to Include**:
- Technology has footguns or common mistakes
- Violations have severe consequences (security, data loss, compliance)
- Pattern violations are detectable in code review
- Team has different experience levels

**Adaptation Examples**:

**React Template**:
- DO use setState/useState, DON'T mutate state directly
- DO provide keys in lists, DON'T use array index as key
- DO cleanup in useEffect return, DON'T leave subscriptions open
- DO memoize expensive computations, DON'T recalculate on every render

**SQL/Database Template**:
- DO use parameterized queries, DON'T concatenate user input
- DO explicitly list columns, DON'T use SELECT *
- DO use transactions for multi-step updates, DON'T leave partial states
- DO create indexes on foreign keys, DON'T leave unindexed joins

**Python/Data Science Template**:
- DO use virtual environments, DON'T install globally
- DO validate schemas, DON'T assume data shape
- DO handle missing data, DON'T use .dropna() blindly
- DO version datasets, DON'T overwrite production data

**Security Template**:
- DO validate all inputs, DON'T trust user data
- DO use prepared statements, DON'T build SQL strings
- DO encrypt sensitive data, DON'T store passwords in plain text
- DO rate limit APIs, DON'T allow unlimited requests

---

## 5. Artifact Generation Commands

**Origin**: `generate-artifacts.md` in Power Query template

**Pattern**: Commands that transform analysis into structured documentation artifacts

**Examples from Power Query**:
- Generate glossary from variable extraction
- Generate data contracts from schema analysis
- Generate dependency graph from query relationships
- Generate query manifest from file analysis

**Reusable Pattern**:
```markdown
# Generate [Artifact Name]

## Purpose
Transform [source] analysis into structured [artifact type]

## Context Required
- [Source file 1]
- [Source file 2]
- [Analysis results]

## Process
1. Read [source files]
2. Extract [patterns/information]
3. Structure into [format]
4. Validate [criteria]
5. Write to [output location]

## Output Location
`.claude/[context|reference]/[artifact-name].md`
```

**Adaptation Examples**:

**API Documentation Template**:
- `generate-api-docs.md` - Extract endpoints from routes, generate OpenAPI spec
- `generate-examples.md` - Create usage examples from test files

**Database Schema Template**:
- `generate-erd.md` - Create entity relationship diagram from migrations
- `generate-data-dictionary.md` - Document tables/columns from schema

**Component Library Template**:
- `generate-component-catalog.md` - Extract props/usage from component files
- `generate-storybook-index.md` - Create Storybook navigation from components

---

## 6. Phase-Based Status Tracking

**Origin**: `_phase-0-status.md` in Power Query template

**Pattern**: Dedicated progress tracker for multi-phase initialization or complex workflows

**Structure**:
```markdown
# Phase [N] Status

**Started**: [Date]
**Last Updated**: [Date]
**Status**: [Not Started | In Progress | Complete]

## Steps

- [x] Step 1: [Description] ✓ Complete
- [ ] Step 2: [Description] (In Progress)
- [ ] Step 3: [Description]
- [ ] Step 4: [Description]

## Outputs Generated

- [x] artifact-1.md
- [ ] artifact-2.md
- [ ] artifact-3.md

## Next Action

[What needs to happen next]
```

**When to Use**:
- Multi-step initialization workflows
- Gated processes (can't proceed until phase complete)
- Multiple artifacts generated across steps
- Need clear handoff between phases

**Adaptation Examples**:
- `_onboarding-status.md` - New project setup checklist
- `_migration-status.md` - Database or architecture migration progress
- `_deployment-status.md` - Production deployment checklist
- `_security-audit-status.md` - Security review progress

---

## 7. Domain-Specific Validation Patterns

**Origin**: Schema validation, data contracts in Power Query template

**Pattern**: Structured validation specific to domain requirements

**Power Query Examples**:
- `data-contracts.md` - Expected schema for each query
- `validate-query.md` - Schema validation command
- `dependency-graph.md` - Query execution order validation

**Reusable Pattern Components**:

1. **Contracts/Interfaces**: Define expected shape
2. **Validation Command**: Check actual vs expected
3. **Dependency Tracking**: Map relationships

**Adaptation Examples**:

**API Development**:
- `api-contracts.md` - Request/response schemas
- `validate-endpoint.md` - Schema validation command
- `api-dependency-graph.md` - Service dependencies

**React Components**:
- `component-contracts.md` - PropTypes/TypeScript interfaces
- `validate-component.md` - Props validation
- `component-tree.md` - Component hierarchy

**Database**:
- `schema-contracts.md` - Expected table structures
- `validate-migration.md` - Schema validation
- `table-dependencies.md` - Foreign key relationships

---

## Usage Recommendations

### When to Extract Patterns

Extract when a pattern:
1. Appears useful for 3+ other domain types
2. Solves a general class of problem
3. Can be parameterized/customized
4. Has clear adaptation guidelines

### When to Keep Domain-Specific

Keep specific when:
1. Highly specialized to one technology
2. Adaptation would lose essential value
3. No clear generalization exists
4. Coupling to domain is fundamental

### Implementation Strategy

1. **Document the pattern** (this file)
2. **Create adaptation guide** in customization workflow (task 17)
3. **Update bootstrap command** to offer pattern as option (task 15)
4. **Maintain examples** from multiple domains
5. **Version patterns** as they evolve

---

## Pattern Maturity Levels

**Level 1 - Concept**: Identified but not yet extracted
**Level 2 - Documented**: Described in this file
**Level 3 - Templated**: Available in bootstrap command
**Level 4 - Validated**: Used successfully in 3+ domains
**Level 5 - Standardized**: Recommended default for certain project types

### Current Maturity

| Pattern | Level | Domains Used |
|---------|-------|--------------|
| Phase 0 Workflow | 2 | Power Query |
| Pitfalls Checklist | 2 | Power Query |
| Multi-Dimension Scoring | 2 | Power Query |
| Critical Rules | 2 | Power Query |
| Artifact Generation | 2 | Power Query |
| Phase Status Tracking | 2 | Power Query |
| Domain Validation | 2 | Power Query |

**Goal**: Move all patterns to Level 3 through task 15 (bootstrap command)
