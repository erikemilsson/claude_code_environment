# Decision Record Template

Use this template when creating new decision records in `.claude/support/decisions/`.

---

## Filename Format

`decision-{NNN}-{slug}.md`

Examples:
- `decision-001-oauth-library.md`
- `decision-002-database-choice.md`
- `decision-003-api-versioning.md`

---

## Template

```markdown
---
id: DEC-{NNN}
title: [Short descriptive title]
status: draft
category: [architecture | technology | process | scope | methodology | vendor]
created: YYYY-MM-DD
decided:
related:
  tasks: []
  decisions: []
implementation_anchors: []
---

# [Title]

## Background

[Why does this decision need to be made? What problem are we solving?
Include enough context for someone unfamiliar to understand.]

## Options Comparison

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| [Criterion 1] | | | |
| [Criterion 2] | | | |
| [Criterion 3] | | | |
| Overall | | | |

## Option Details

### Option A: [Name]

**Description:** [What this option entails]

**Strengths:**
- [Benefit 1]
- [Benefit 2]

**Weaknesses:**
- [Drawback 1]
- [Drawback 2]

**Research Notes:** [Links, experiments, spike findings]

### Option B: [Name]

**Description:** [What this option entails]

**Strengths:**
- [Benefit 1]
- [Benefit 2]

**Weaknesses:**
- [Drawback 1]
- [Drawback 2]

**Research Notes:** [Links, experiments, spike findings]

## Decision

**Selected:** [Option name]

**Rationale:**
[Why this option was chosen. Be specific about the criteria that mattered most.]

## Trade-offs

**Gaining:**
- [What we get from this choice]

**Giving Up:**
- [What we sacrifice or defer]

## Impact

**Implementation Notes:**
[How this affects the work, any immediate actions needed]

**Affected Areas:**
- [Files, components, or systems affected]
- [Related tasks: task IDs]

**Risks:**
- [Any risks introduced by this decision]
```

---

## Status Values

| Status | Meaning |
|--------|---------|
| `draft` | Being researched, not ready for review |
| `proposed` | Ready for stakeholder review |
| `approved` | Decision made, awaiting implementation |
| `implemented` | Decision executed in codebase |
| `superseded` | Replaced by a newer decision |

---

## Categories

| Category | Use For |
|----------|---------|
| `architecture` | System structure, component design, patterns |
| `technology` | Libraries, frameworks, languages, tools |
| `process` | Workflows, team practices, conventions |
| `scope` | Feature boundaries, priorities, trade-offs |
| `methodology` | Approaches, algorithms, techniques |
| `vendor` | Third-party services, APIs, integrations |

---

## Quick Start

1. Copy the template above into a new file
2. Update frontmatter (id, title, category, created)
3. Write Background section
4. Add options to comparison table
5. Fill in Option Details
6. Once decided, complete Decision, Trade-offs, Impact
7. Update status to `approved` or `implemented`
8. Add entry to `index.md`

---

## Tips

- **Start with Background**: If you can't articulate why the decision matters, it might not need a formal record.
- **Options first**: Research options before forming an opinion.
- **Comparison table**: Forces structured thinking; reveals non-obvious differences.
- **Be honest about trade-offs**: Every choice has costs.
- **Link related items**: Connect to tasks and other decisions.

---

## Implementation Anchors

When a decision reaches `implemented` status, add anchors to track where the decision is realized in code:

```yaml
implementation_anchors:
  - file: "src/auth/oauth.ts"
    line: 45
    description: "OAuth provider configuration"
  - file: "src/middleware/auth.ts"
    line: 12
    description: "JWT validation middleware"
```

### Anchor Fields

| Field | Required | Description |
|-------|----------|-------------|
| `file` | Yes | Relative path from project root |
| `line` | No | Line number (approximate is fine) |
| `description` | Yes | Brief description of what this anchor represents |

### Why Anchors Matter

- **Drift detection**: `/health-check` validates that anchor files exist
- **Impact analysis**: When revisiting a decision, know exactly where it's implemented
- **Onboarding**: New team members can trace decisions to code
- **Refactoring**: Know which decisions are affected when files move

### When to Add Anchors

- When setting status to `implemented`
- After refactoring code that implements a decision
- When extending an implementation to new locations

### Health Check Integration

`/health-check --decisions` validates:
- All `implemented` decisions have at least one anchor
- Anchor files exist in the codebase
- Warns about missing files (suggests updating anchors or reverting status)
