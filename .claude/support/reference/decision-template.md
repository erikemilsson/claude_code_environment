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

## Example: Completed Decision Record

Below is a realistic filled-in example showing what a completed decision record looks like.

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

### Option C: Custom Implementation

**Description:** Build OAuth flow directly using provider APIs and HTTP clients.

**Strengths:**
- Full control over every aspect
- No dependency risk

**Weaknesses:**
- Significant development effort
- Must handle token refresh, CSRF, state management manually
- Security risk from implementation bugs

## Decision

**Selected:** Auth.js (NextAuth)

**Rationale:**
Our stack is Next.js, and Auth.js provides the tightest integration with minimal boilerplate. The two
providers we need (Google, GitHub) are built-in. The spike demonstrated a working setup in 30 minutes.
Passport.js is a strong alternative but requires more glue code for our framework. Custom implementation
is ruled out — the effort and security risk aren't justified.

## Trade-offs

**Gaining:**
- Fast setup with built-in provider support
- Integrated session management
- Active maintenance aligned with Next.js releases

**Giving Up:**
- Flexibility for non-standard auth flows (acceptable — we don't need them now)
- Framework portability (acceptable — we're committed to Next.js)

## Impact

**Implementation Notes:**
- Configure Auth.js in `src/auth/oauth.ts`
- Add token validation middleware in `src/middleware/auth.ts`
- Environment variables: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`

**Affected Areas:**
- `src/auth/` (new directory)
- `src/middleware/auth.ts` (new file)
- `.env.example` (add OAuth variables)
- Related tasks: task-005

**Risks:**
- Auth.js major version upgrades may require migration effort
- Mitigation: Pin major version, monitor release notes
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
8. Regenerate the dashboard to include the new decision

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

`/health-check` validates:
- All `implemented` decisions have at least one anchor
- Anchor files exist in the codebase
- Warns about missing files (suggests updating anchors or reverting status)
