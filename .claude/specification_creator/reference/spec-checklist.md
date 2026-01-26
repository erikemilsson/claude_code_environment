# Spec Readiness Checklist

Defines "complete enough" for a specification to move to task decomposition.

## Required Sections

Each section must meet its criteria before the spec is ready for `/work` decomposition.

### 1. Overview
| Criterion | Check |
|-----------|-------|
| Problem statement is specific (not generic) | |
| Target users are identified | |
| At least 2 concrete problems with solutions listed | |

**Red flags:** Placeholder text like "[Brief description]", vague statements like "make it better"

### 2. Architecture
| Criterion | Check |
|-----------|-------|
| Components are named and described | |
| Relationships between components are clear | |
| At least 1 key design decision with rationale | |

**Red flags:** No component diagram/description, decisions without rationale

### 3. Requirements
| Criterion | Check |
|-----------|-------|
| At least 3 functional requirements | |
| Requirements are behaviors, not tasks | |
| Non-functional requirements address: performance OR security OR scalability | |
| Constraints list any hard boundaries (tech, timeline, dependencies) | |

**Red flags:** Requirements that are really tasks ("Add login button"), no constraints section

### 4. Acceptance Criteria
| Criterion | Check |
|-----------|-------|
| At least 5 testable criteria | |
| Each criterion is pass/fail verifiable | |
| Criteria cover the core user journey | |
| No criterion requires subjective judgment | |

**Red flags:** Criteria like "works well", "is fast", "looks good" - these aren't testable

### 5. Open Questions
| Criterion | Check |
|-----------|-------|
| No questions that block core architecture | |
| No questions that block the critical path | |
| Remaining questions are deferrable to implementation | |

**Red flags:** Questions like "What database should we use?" or "How will auth work?" still open

---

## Readiness Levels

### Not Ready
- Any required section has placeholder text
- Architecture section is empty or vague
- Fewer than 3 acceptance criteria
- Open questions block core functionality

### Minimally Ready
- All sections have real content (no placeholders)
- Architecture describes main components
- At least 5 acceptance criteria exist
- Open questions are implementation details only

### Well-Defined
- All criteria in this checklist pass
- Acceptance criteria map clearly to requirements
- Non-functional requirements have measurable targets
- No ambiguity in scope boundaries

---

## Section-Specific Guidance

### Writing Good Acceptance Criteria

**Bad → Good:**
- "User can log in" → "User can log in with email and password; invalid credentials show error message within 2 seconds"
- "App is fast" → "Page load time < 3 seconds on 3G connection"
- "Data is secure" → "Passwords are hashed with bcrypt; API requires authentication token"

**Granularity target:** Each criterion should map to 1-3 implementation tasks.

### Writing Good Requirements

**Format:** "[User/System] can/must [behavior] when [condition]"

**Bad → Good:**
- "Add authentication" → "Users must authenticate before accessing protected resources"
- "Handle errors" → "System must display user-friendly error messages for all API failures"

### Defining Non-Functional Requirements

Always include a measurable target:

| Category | Bad | Good |
|----------|-----|------|
| Performance | "Should be fast" | "API responses < 200ms p95" |
| Security | "Must be secure" | "OWASP Top 10 vulnerabilities addressed" |
| Scalability | "Should scale" | "Support 1000 concurrent users" |

---

## Using This Checklist

The `/iterate` command checks the spec against this list and identifies gaps. You can also:

1. **Self-review:** Walk through before starting a Claude session
2. **Focus review:** Ask Claude to deep-dive on a specific section
3. **Final check:** Run before transitioning to `/work` decomposition
