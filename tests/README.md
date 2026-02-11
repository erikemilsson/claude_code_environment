# Template Workflow Tests

Conceptual test scenarios for the Claude Code environment template. These verify that the command definitions (work.md, iterate.md, health-check.md) correctly handle decision gating, phase transitions, and session resilience.

## How to Run

These are **conceptual trace tests**, not automated scripts. To run a scenario:

1. Read the **State** section — this defines the starting conditions
2. Trace through the referenced **command path** (Step N in work.md, Check N in health-check.md, etc.)
3. Compare the command logic's behavior against the **Expected** outcome
4. Check off **Pass criteria**

No fixture files or project setup needed. The state description in each scenario is sufficient.

## When to Run

- After significant changes to `/work`, `/iterate`, or `/health-check`
- After modifying the decision system (decisions.md, extension-patterns.md)
- After changing dashboard format hints or regeneration procedure
- When adding new state-based features that interact with decisions or phases

## Scenarios

### Core Workflow (01-07)

| # | Name | Tests | Key Commands |
|---|------|-------|-------------|
| 01 | Decision Discovery | `/iterate` finds implicit decisions in spec text | iterate.md Step 2 |
| 02 | Decision Blocking | `/work` blocks tasks with unresolved decision deps | work.md Step 2b |
| 03 | Inflection Point Handoff | Resolved inflection point pauses `/work`, hands to `/iterate` | work.md Step 2b-post, iterate.md Post-Inflection-Point |
| 04 | Dashboard Skeleton | Dashboard shows full project shape including blocked areas | dashboard.md, work.md |
| 05 | Phase Transition | Pick-and-go decision unblocks without `/iterate` | work.md Step 2b-post |
| 06 | Late Decision Detection | Catches decisions created after work already started | work.md Step 2b item 5, health-check.md Check 6 |
| 07 | Session Resumption | State persists across session boundaries | All commands |

### Dashboard Deep Dive (08-14)

Tests the dashboard as a communication hub across project lifecycle stages. Focus areas: information hierarchy, action item completeness, verification gate integrity, feedback persistence, and phase-appropriate content.

| # | Name | Tests | Key Files |
|---|------|-------|-----------|
| 08 | Dashboard First Impression | Section relevance and hierarchy at project start | dashboard.md, work.md |
| 09 | Dashboard Actionability | Every attention item has link, action, and completion signal | dashboard.md, work.md |
| 10 | Verification Gate Integrity | Claude cannot bypass user verification/approval gates | implement-agent.md, work.md |
| 11 | Feedback Flow and Persistence | User feedback has a destination, persists, and is retrievable | dashboard.md, decisions.md |
| 12 | Dashboard Phase Relevance | Sections provide value appropriate to current phase | work.md (toggles) |
| 13 | Critical Path Visualization | Dependency chain communicated effectively for complex projects | dashboard.md, extension-patterns.md |
| 14 | Dashboard Communication Loop | Complete attention → action → resolution loop doesn't break | All dashboard-related files |

**Design gaps surfaced by 08-14:**
- Inline feedback areas in "Tasks Ready for You" are lost on dashboard regeneration (11B, 14B)
- No designated place for user constraints/notes in decision docs (11B)
- Section toggle system is static — no phase-aware defaults (12D)
- Critical Path text format doesn't convey parallel branches (13A)
- Decision resolution doesn't explicitly update frontmatter status (14C)
- `questions.md` not linked from dashboard (11C)

## Example Project

All scenarios use a "data analysis pipeline" with:
- **Phase 1**: Data collection and cleaning
- **Phase 2**: Statistical analysis (blocked by DEC-001: analysis method, inflection point)
- **Phase 3**: Visualization and reporting (blocked by DEC-002: charting library, pick-and-go)
