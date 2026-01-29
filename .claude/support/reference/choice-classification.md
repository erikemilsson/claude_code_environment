# Choice Classification Guide

Complex projects benefit from separating **what** to do from **how** to do it. This prevents implementation details from driving design, and ensures the spec remains stable while technical approaches can evolve.

---

## Two Types of Choices

### Spec-Level Choices (What)

Define requirements, scope, and approach at a design level.

**Examples:**
- Which features to include in MVP
- Authentication strategy (OAuth vs magic links vs passwords)
- Data model structure and relationships
- API design patterns (REST vs GraphQL vs RPC)
- Testing philosophy (TDD, integration-first, etc.)
- User-facing behavior and workflows

**Characteristics:**
- Affects user-visible behavior or system architecture
- Should be decided before implementation begins
- Changes require spec revision
- Documented in spec or as formal decisions

### Implementation-Level Choices (How)

Define tools, libraries, and technical implementation details.

**Examples:**
- Which OAuth library to use (Auth.js vs Passport.js)
- Database engine selection (Postgres vs SQLite vs MySQL)
- Testing framework choice (Jest vs Vitest vs Mocha)
- CSS approach (Tailwind vs CSS modules vs styled-components)
- Build tool configuration (Vite vs webpack vs esbuild)
- Linting and formatting rules

**Characteristics:**
- Affects developer experience, not user-visible behavior
- Can be decided during implementation
- Changes don't require spec revision
- Documented in decisions or inline comments

---

## Sequencing

**Recommended workflow:**

1. **Finalize all Spec-Level choices** in the spec
2. **Begin implementation**
3. **Make Implementation-Level choices** as needed during development
4. **Document Implementation-Level decisions** for significant choices

**Why this order matters:**
- Prevents tool selection from constraining design
- Keeps spec focused on requirements, not implementation
- Allows flexibility to change tools without spec churn
- Makes the spec readable by non-technical stakeholders

---

## Classification Checklist

Ask these questions to classify a choice:

| Question | Spec-Level | Implementation-Level |
|----------|------------|---------------------|
| Does it change what the system does? | Yes | No |
| Would users notice if it changed? | Yes | No |
| Does it constrain future features? | Yes | Sometimes |
| Can it be swapped without redesign? | No | Yes |
| Is it in the spec acceptance criteria? | Yes | No |
| Does it affect API contracts? | Yes | No |
| Is it about *behavior* or *tooling*? | Behavior | Tooling |

---

## Gray Areas

Some choices sit between spec and implementation level:

| Choice | Classification | Reasoning |
|--------|---------------|-----------|
| Database type (SQL vs NoSQL) | Spec-Level | Affects data modeling and query patterns |
| Specific database (Postgres vs MySQL) | Implementation-Level | Swappable within SQL category |
| Auth method (OAuth vs passwords) | Spec-Level | User-facing flow differs |
| OAuth library | Implementation-Level | Same OAuth flow, different code |
| Real-time strategy (WebSockets vs SSE) | Spec-Level | Different capabilities and UX |
| WebSocket library | Implementation-Level | Same protocol, different API |

**When in doubt:** If changing it would require rewriting the spec's acceptance criteria, it's spec-level.

---

## Benefits of This Separation

### For the Spec
- Stays focused on requirements and behavior
- Readable by stakeholders without technical deep-dives
- Stable even as implementation details evolve

### For Implementation
- Freedom to choose best tools for the job
- Can upgrade or swap libraries without spec changes
- Technical decisions documented separately where detail is appropriate

### For the Team
- Clear handoff points between design and build phases
- Easier to parallelize work (spec authors vs implementers)
- Reduces churn from mixing concerns

---

## Anti-Patterns

### Putting Implementation Choices in the Spec

**Problem:** "The system shall use React 18 with Zustand for state management."

**Why it's bad:** Ties the spec to specific versions and libraries. If Zustand is deprecated, the spec needs revision even though requirements haven't changed.

**Better:** "The system shall provide real-time UI updates when data changes." (Spec-level)
Then document React + Zustand choice in a decision record. (Implementation-level)

### Making Spec Choices During Implementation

**Problem:** Deciding during coding that "users should be able to sign in with Apple ID" when the spec says OAuth with Google/GitHub.

**Why it's bad:** Scope creep. Implementation is adding requirements without spec review.

**Better:** Note the idea, pause, update the spec through the proper process, then implement.

---

## Integration with Decision Records

- **Spec-Level choices**: Always warrant a decision record if non-obvious
- **Implementation-Level choices**: Create decision records for significant choices (libraries with long-term commitment, major infrastructure tools)
- **Trivial Implementation choices**: Document inline or skip (formatter config, minor dev dependencies)

See [Decision Template](decision-template.md) for the decision record format.
