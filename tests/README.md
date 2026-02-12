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
- After changing dashboard structure, section toggles, or regeneration procedure
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
- Inline feedback areas in "Your Tasks" are lost on dashboard regeneration (11B, 14B)
- No designated place for user constraints/notes in decision docs (11B)
- Section toggle system is static — no phase-aware defaults (12D)
- Critical path one-liner doesn't convey parallel branches (13A)
- Decision resolution doesn't explicitly update frontmatter status (14C)
- `questions.md` not linked from dashboard (11C)

### Real-World Adaptation (15-24)

Tests grounded in patterns observed across real projects. All previous scenarios use a single hypothetical "data analysis pipeline"; these scenarios test how the template adapts to diverse project types, existing infrastructure, and scale.

| # | Name | Tests | Key Commands/Files |
|---|------|-------|-------------------|
| 15 | Tech Stack Discovery | `/iterate` detects project tech from existing files | iterate.md Step 1 |
| 16 | Existing Test Suite | verify-agent discovers and uses existing pytest setup | verify-agent.md |
| 17 | Migration from Custom .claude/ | Template applied to project with incompatible existing `.claude/` dir | setup-checklist, health-check Part 1 |
| 18 | Non-Software Project | Template works for spec-only / docs-only projects | implement-agent.md, verify-agent.md |
| 19 | Nested Project Structure | Agents find code in subdirectories, run builds from correct location | implement-agent.md, verify-agent.md |
| 20 | External Service Dependencies | Task decomposition surfaces API keys / DB setup as prerequisites | work.md Step 3 |
| 21 | Large Task History | Performance and archival at 100+ tasks | work.md, health-check.md |
| 22 | CI/CD-Aware Verification | verify-agent mirrors CI checks, doesn't duplicate them | verify-agent.md |
| 23 | Staged Approval Gates | User-defined gates block entire project stages until manual approval | work.md |
| 24 | Parallel File Conflict Detection | `/work` parallel dispatch holds back tasks that touch same files | work.md Step 4 |

**Key themes surfaced by 15-24:**
- Most adopters have existing projects, not greenfield — migration (17) is the common path
- verify-agent must adapt to project type: code (16), docs (18), nested (19), CI-backed (22)
- Scale is a real concern — projects reach 380+ tasks (21)
- External dependencies are common and need explicit handling (20)
- Parallel execution needs file-level conflict detection (24)

### Workflow Lifecycle (25-28)

Tests for core lifecycle operations that were previously uncovered: task breakdown, manual completion, verification rework, and dependency resolution.

| # | Name | Tests | Key Commands/Files |
|---|------|-------|-------------------|
| 25 | Breakdown Command | `/breakdown` splits high-difficulty tasks, inherits provenance, updates parent | breakdown.md, implement-agent.md Step 1b |
| 26 | Work Complete Flow | `/work complete` validates, completes, auto-completes parents, regenerates dashboard | work.md § Task Completion |
| 27 | Verification Failure and Rework | Fail → fix → re-verify loop, 2-attempt limit, phase-level fix tasks | verify-agent.md Steps T6-T7, implement-agent.md |
| 28 | Task Dependency Chains | Linear chains, multi-blocker convergence, circular detection, critical path | work.md Step 2c, Step 3 |
| 29 | On Hold and Absorbed Statuses | On Hold/Absorbed excluded from routing, phase completion, parent auto-completion | work.md Step 3, health-check.md Check 6, shared-definitions.md |

**Key behaviors surfaced by 25-29:**
- `/breakdown` is the only path for difficulty >= 7 tasks — implement-agent rejects them
- `/work complete` is the primary human action signal — parent auto-completion depends on it
- Verification failure is not terminal — the rework loop has a 2-attempt limit before human escalation
- Dependency resolution must use AND logic (all deps satisfied), not OR
- Circular dependencies must be detected and reported, not cause infinite loops
- On Hold is a user-owned transition — Claude never auto-resumes paused tasks
- Absorbed preserves audit trail while removing tasks from active work

## Example Project

All scenarios use a "data analysis pipeline" with:
- **Phase 1**: Data collection and cleaning
- **Phase 2**: Statistical analysis (blocked by DEC-001: analysis method, inflection point)
- **Phase 3**: Visualization and reporting (blocked by DEC-002: charting library, pick-and-go)
