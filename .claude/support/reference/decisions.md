# Decisions Reference

Guide for creating, documenting, and classifying project decisions.

---

## Record Template

### Filename Format

`decision-{NNN}-{slug}.md`

Examples: `decision-001-oauth-library.md`, `decision-002-database-choice.md`

### Template

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
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
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

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: [Name]
- [ ] Option B: [Name]

*Check one box above, then fill in the Decision section below.*

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
8. Regenerate the dashboard to include the new decision

---

## When to Create Records

### Create a Record For

- Technology choices (libraries, frameworks, services)
- Architectural patterns (how components connect)
- Scope decisions (what's in/out of MVP)
- Process changes (how work gets done)
- Anything that took significant discussion to resolve

### Skip Records For

- Obvious choices with no real alternatives
- Trivial implementation details
- Decisions already documented elsewhere (e.g., in specs)
- Temporary workarounds (use code comments instead)

> **Rule of thumb:** If someone might reasonably ask "why did we do it this way?" in 3 months, create a record.

---

## Decision Lifecycle

```
draft → proposed → approved → implemented
                      ↓
                 superseded
```

- **draft**: Research phase. Gathering options, running experiments.
- **proposed**: Options documented, recommendation made. Ready for stakeholder input.
- **approved**: Decision finalized. May await implementation.
- **implemented**: Decision reflected in codebase. Common end state.
- **superseded**: Replaced by a newer decision. Link to replacement in Impact section.

### Revisiting Decisions

Decisions aren't permanent. Revisit when circumstances change, trade-offs prove worse than expected, or better options become available.

When superseding: create a new record, reference the old one, mark old as `superseded`, note the replacement in the old record's Impact section.

---

## Choice Classification: Spec vs Implementation

Complex projects benefit from separating **what** to do from **how** to do it. This prevents implementation details from driving design.

### Spec-Level Choices (What)

Define requirements, scope, and approach at a design level. Affects user-visible behavior or system architecture. Should be decided before implementation. Changes require spec revision.

**Examples:** Which features to include in MVP, authentication strategy (OAuth vs magic links), data model structure, API design patterns, user-facing workflows.

### Implementation-Level Choices (How)

Define tools, libraries, and technical details. Affects developer experience, not user-visible behavior. Can be decided during implementation. Changes don't require spec revision.

**Examples:** Which OAuth library, database engine selection, testing framework, CSS approach, build tool configuration.

### Classification Checklist

| Question | Spec-Level | Implementation-Level |
|----------|------------|---------------------|
| Does it change what the system does? | Yes | No |
| Would users notice if it changed? | Yes | No |
| Can it be swapped without redesign? | No | Yes |
| Is it about *behavior* or *tooling*? | Behavior | Tooling |

### Gray Areas

| Choice | Classification | Reasoning |
|--------|---------------|-----------|
| Database type (SQL vs NoSQL) | Spec-Level | Affects data modeling and query patterns |
| Specific database (Postgres vs MySQL) | Implementation-Level | Swappable within SQL category |
| Auth method (OAuth vs passwords) | Spec-Level | User-facing flow differs |
| OAuth library | Implementation-Level | Same OAuth flow, different code |
| Real-time strategy (WebSockets vs SSE) | Spec-Level | Different capabilities and UX |
| WebSocket library | Implementation-Level | Same protocol, different API |

**When in doubt:** If changing it would require rewriting the spec's acceptance criteria, it's spec-level.

### Integration with Decision Records

- **Spec-Level choices**: Always warrant a decision record if non-obvious
- **Implementation-Level choices**: Create records for significant choices (libraries with long-term commitment, major infrastructure tools)
- **Trivial Implementation choices**: Document inline or skip

---

## Comparison Tables

The options comparison table is the core of a decision record. It forces structured evaluation.

### Good Criteria

- **Performance**: Speed, resource usage
- **Complexity**: Learning curve, maintenance burden
- **Cost**: Licensing, infrastructure, time
- **Ecosystem**: Community, documentation, longevity
- **Fit**: How well it matches our constraints
- **Risk**: Unknowns, potential failure modes

Use qualitative ratings (Good/Moderate/Poor) or quantitative when available.

---

## Research Archives

Store significant research in `.claude/support/decisions/.archive/`:
- `YYYY-MM-DD_topic.md` - Research notes, findings
- Link from the decision record's Research Notes

This keeps decision records focused while preserving detailed findings.

---

## Optional: Weighted Scoring Matrix

For high-stakes decisions, use weighted scoring to make evaluation explicit:

```markdown
## Weighted Scoring

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| [Criterion 1] | 30% | 4/5 | 3/5 | 5/5 |
| [Criterion 2] | 25% | 5/5 | 4/5 | 3/5 |
| [Criterion 3] | 25% | 3/5 | 5/5 | 4/5 |
| [Criterion 4] | 20% | 4/5 | 3/5 | 4/5 |
| **Weighted Total** | | **4.05** | **3.75** | **4.05** |
```

**Scoring:** 5/5 = Fully meets, 4/5 = Mostly meets, 3/5 = Partial, 2/5 = Weak, 1/5 = Does not meet.

**When to use:** Decisions affecting architecture, multiple strong alternatives, need to communicate rationale to stakeholders.

**Calculating:** For each option: `(Weight1 x Score1) + (Weight2 x Score2) + ...`

---

## Optional: Fallback Plan

For decisions with uncertainty, document what happens if the primary choice doesn't work out:

```markdown
## Fallback Plan

**Trigger condition:** [When would we reconsider this decision?]
**Fallback approach:** [What's the alternative if the primary fails?]
**Migration path:**
1. [Step to transition from primary to fallback]
2. [Data migration or refactoring needed]
**Sunk cost if triggered:** [What work would be lost or need rework?]
```

**When to include:** New/unproven technology, expensive-to-reverse decisions, external dependencies, tight timelines.

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

| Field | Required | Description |
|-------|----------|-------------|
| `file` | Yes | Relative path from project root |
| `line` | No | Line number (approximate is fine) |
| `description` | Yes | Brief description of what this anchor represents |

**Why anchors matter:** Drift detection (`/health-check` validates anchor files exist), impact analysis when revisiting decisions, tracing decisions to code during refactoring.

---

## Anti-Patterns

| Anti-Pattern | Problem |
|---|---|
| **Decision Theater** | Creating elaborate records for trivial choices. Keep small decisions in code comments. |
| **Analysis Paralysis** | Researching endlessly without deciding. Set time limits for draft status. |
| **Orphan Records** | Decisions referenced nowhere, never implemented. Implement or mark superseded. |
| **Missing Trade-offs** | Every choice has costs. "No downsides" means incomplete analysis. |
| **Invisible Rationale** | "We chose X" without explaining why. The rationale is the most valuable part. |
| **Impl Choices in Spec** | "The system shall use React 18" — ties spec to libraries. Spec should state requirements; tools go in decision records. |
| **Spec Choices During Impl** | Adding features during coding without spec review. Note the idea, update spec first, then implement. |

---

## Example: Completed Decision Record

<details>
<summary>Click to expand full example</summary>

```markdown
---
id: DEC-001
title: OAuth Library Selection
status: implemented
category: technology
created: 2026-01-10
decided: 2026-01-12
related:
  tasks: [task-005]
  decisions: []
implementation_anchors:
  - file: "src/auth/oauth.ts"
    line: 1
    description: "OAuth provider setup and configuration"
  - file: "src/middleware/auth.ts"
    line: 23
    description: "Token validation middleware"
inflection_point: false
blocks: [task-005]
---

# OAuth Library Selection

## Background

The application needs OAuth 2.0 support for Google and GitHub login. We need a library that handles
the OAuth flow, token management, and provider abstraction. The choice affects authentication
architecture and long-term maintenance burden.

## Options Comparison

| Criteria | Passport.js | Auth.js (NextAuth) | Custom Implementation |
|----------|-------------|--------------------|-----------------------|
| Provider support | 500+ strategies | 80+ built-in | Manual per-provider |
| Complexity | Moderate | Low | High |
| Flexibility | High | Moderate | Full |
| Maintenance | Active | Active | On us |
| Session handling | BYO | Built-in | BYO |
| **Overall** | Good for flexibility | Best for our stack | Too much effort |

## Option Details

### Option A: Passport.js

**Description:** Express middleware with a strategy-based plugin architecture for authentication.

**Strengths:**
- Huge ecosystem of strategies
- Battle-tested in production for 10+ years
- Fine-grained control over auth flow

**Weaknesses:**
- Session management is separate concern
- Some strategies are community-maintained and may lag
- More boilerplate to set up

**Research Notes:** Reviewed docs and examples. Works well but requires more glue code for our Next.js setup.

### Option B: Auth.js (NextAuth)

**Description:** Authentication library designed for Next.js with built-in provider support and session management.

**Strengths:**
- First-class Next.js integration
- Built-in session handling with JWT or database
- Minimal configuration for common providers

**Weaknesses:**
- Less flexible for non-standard flows
- Tied to Next.js patterns
- Abstractions can be hard to customize

**Research Notes:** Tested with Google and GitHub providers in a spike. Setup took ~30 minutes vs ~2 hours for Passport.

## Select an Option

- [ ] Passport.js
- [x] Auth.js (NextAuth)
- [ ] Custom Implementation

## Decision

**Selected:** Auth.js (NextAuth)

**Rationale:**
Our stack is Next.js, and Auth.js provides the tightest integration with minimal boilerplate. The two
providers we need (Google, GitHub) are built-in. The spike demonstrated a working setup in 30 minutes.

## Trade-offs

**Gaining:**
- Fast setup with built-in provider support
- Integrated session management

**Giving Up:**
- Flexibility for non-standard auth flows (acceptable — we don't need them now)
- Framework portability (acceptable — we're committed to Next.js)

## Impact

**Implementation Notes:**
- Configure Auth.js in `src/auth/oauth.ts`
- Add token validation middleware in `src/middleware/auth.ts`

**Affected Areas:**
- `src/auth/` (new directory)
- `src/middleware/auth.ts` (new file)
- Related tasks: task-005

**Risks:**
- Auth.js major version upgrades may require migration effort
- Mitigation: Pin major version, monitor release notes
```

</details>

---

## Tips

- **Start with Background**: If you can't articulate why it matters, it might not need a record.
- **Options first**: Research before forming an opinion.
- **Comparison table**: Forces structured thinking; reveals non-obvious differences.
- **Be honest about trade-offs**: Every choice has costs.
- **Link related items**: Connect to tasks and other decisions.
