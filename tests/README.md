# Template Workflow Tests

Conceptual test scenarios for the Claude Code environment template. These verify that the command definitions (work.md, iterate.md, health-check.md) and agent workflows (implement-agent, verify-agent) correctly handle decision gating, phase transitions, verification, and session resilience.

## How to Run

These are **conceptual trace tests**, not automated scripts. To run a scenario:

1. Read the **State** section — this defines the starting conditions
2. Trace through the referenced **command behavior** in the relevant command/agent files
3. Compare the command logic's behavior against the **Expected** outcome
4. Check off **Pass criteria**

No fixture files or project setup needed. The state description in each scenario is sufficient.

## When to Run

- After significant changes to `/work`, `/iterate`, or `/health-check`
- After modifying the decision system or dashboard structure
- After changing agent workflows (implement-agent, verify-agent)
- When adding new state-based features that interact with decisions or phases

## Scenarios

### Core Workflow (01-05)

| # | Name | Tests |
|---|------|-------|
| 01 | Decision Discovery | `/iterate` finds implicit decisions in spec text |
| 02 | Decision Blocking | `/work` blocks tasks with unresolved decision deps |
| 03 | Inflection Point Handoff | Resolved inflection point pauses `/work`, hands to `/iterate` |
| 04 | Phase Transition | Pick-and-go decision unblocks without `/iterate` |
| 05 | Session Resumption | State persists across session boundaries via files |

### Dashboard (06-07)

| # | Name | Tests |
|---|------|-------|
| 06 | Dashboard Structure and Actionability | Full project skeleton visible, action items complete with links, section toggles, critical path |
| 07 | Dashboard Communication and Feedback | Attention-to-resolution loop, feedback persistence, decision detection, stale dashboard |

### Verification and Gates (08)

| # | Name | Tests |
|---|------|-------|
| 08 | Verification Gate Integrity | Claude cannot bypass user verification, human tasks, decisions, or phase boundaries |

### Real-World Adaptation (09-13)

| # | Name | Tests |
|---|------|-------|
| 09 | Tech Stack Discovery | `/iterate` detects project tech from existing files |
| 10 | Existing Test Suite | verify-agent discovers and uses existing test infrastructure |
| 11 | Non-Software Project | Template works for spec-only / documentation projects |
| 12 | Large Task History | Archival threshold and dashboard generation at scale |
| 13 | Parallel File Conflict Detection | `/work` parallel dispatch holds back tasks that touch same files |

### Workflow Lifecycle (14-18)

| # | Name | Tests |
|---|------|-------|
| 14 | Breakdown Command | `/breakdown` splits high-difficulty tasks, inherits provenance |
| 15 | Work Complete Flow | `/work complete` validates, completes, auto-completes parents |
| 16 | Verification Failure and Rework | Fail-fix-re-verify loop, re-verification limit, phase-level fix tasks |
| 17 | Task Dependency Chains | Linear chains, multi-blocker convergence, circular detection |
| 18 | On Hold and Absorbed Statuses | Special statuses excluded from routing and phase completion |

### Error Recovery (19-20)

| # | Name | Tests |
|---|------|-------|
| 19 | Agent Crash and Timeout Recovery | Agent timeout/crash handling, partial work preservation |
| 20 | Corrupted Task JSON | Malformed files, missing fields, dangling dependencies |

### Spec Lifecycle (21-23)

| # | Name | Tests |
|---|------|-------|
| 21 | Spec Drift During Execution | Section-level drift detection, reconciliation, drift budget |
| 22 | Spec Version Transition | v1 to v2 archival, task migration, when NOT to bump |
| 23 | Iterate Distill | Vision doc to spec transformation, suggest-only boundary |

### Research and Review (24-26)

| # | Name | Tests |
|---|------|-------|
| 24 | Research Agent Decision Population | `/research` populates decision options, respects authority boundary |
| 25 | Research from Iterate | `/iterate` implicit decision detection triggers research workflow |
| 26 | Review Command | `/review` assesses implementation quality, stays advisory |

## Example Project

All scenarios use a "data analysis pipeline" with:
- **Phase 1**: Data collection and cleaning
- **Phase 2**: Statistical analysis (blocked by DEC-001: analysis method, inflection point)
- **Phase 3**: Visualization and reporting (blocked by DEC-002: charting library, pick-and-go)
