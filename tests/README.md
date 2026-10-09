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
| 06 | Dashboard Structure and Actionability | Full project skeleton visible, action items complete with their command, section toggles in the sidecar, critical path in the Flow graph |
| 07 | Dashboard Communication and Feedback | Attention-to-resolution loop, feedback kept in `user_feedback` across regeneration, decision detection, stale dashboard |

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
| 19 | Agent Crash and Timeout Recovery | Agent timeout/crash handling, partial work preservation, the open sentinel after a cutoff (19F), a lost delta re-check in a batch (19G) |
| 20 | Corrupted Task JSON | Malformed files, missing fields, dangling dependencies |

### Spec Lifecycle (21-23, 44)

| # | Name | Tests |
|---|------|-------|
| 21 | Spec Drift During Execution | Per-task drift check, batch prompt and per-section options, regen after reconciliation, drift budget |
| 22 | Spec Version Transition | v1 to v2 archival, task migration, when NOT to bump |
| 23 | Iterate Distill | Vision doc to spec transformation, suggest-only boundary |
| 44 | Drift Detection Reaches User | Drift found after a dashboard regen, reconciliation before the Step 1d fast exit, decision-gated tasks, `[K]` Keep all, `[V]` Re-verify, quiet rules |

### Research and Review (24-26)

| # | Name | Tests |
|---|------|-------|
| 24 | Research Agent Decision Population | `/research` populates decision options, respects authority boundary |
| 25 | Research from Iterate | `/iterate` implicit decision detection triggers research workflow |
| 26 | Review Command | `/review` assesses implementation quality, stays advisory |

### Context Transitions (27-31)

| # | Name | Tests |
|---|------|-------|
| 27 | Proactive Handoff (User-Initiated) | `/work pause` wind-down, handoff file creation, next-session restoration |
| 28 | PreCompact Hook Handoff | Auto-compaction safety net, hook-only handoff, equivalent restoration path |
| 29 | Handoff During Verification | Wind-down mid-verify, no partial verification written, fresh verify-agent on resume |
| 30 | Handoff During Parallel Batch | Multi-agent wind-down, batch state preservation, correct parallel resumption |
| 31 | Handoff at Phase Boundary | Cross-phase knowledge preservation, strategic context bridging phases |

### Later Additions (32-43, 45-52)

| # | Name | Tests |
|---|------|-------|
| 32 | /diagnose Visual Recipe | Measured-value contracts for browser-rendering bugs; screenshots never decide pass/fail |
| 33 | Waiting-on-You Queue | Human-gated coverage invariant: every user-blocked item reaches the Needs-you card |
| 34 | Evidence-Carrying Verification | Positive controls, the Empirical Evidence Gate, phase UI smoke |
| 35 | Lazy-Rule Triggers | Lazy rule files load when their trigger fires |
| 36 | Audit-Family Core Delegation | Audit commands delegate shared mechanics to `audit-family-core.md` |
| 37 | /work Procedure Stubs | STOP-gated stubs load their `work-procedures.md` bodies |
| 38 | /iterate Batch Approval | Single-response resolution of a proposal's decisions |
| 39 | /health-check Batch Fix Triage | Collect-don't-prompt fix queue; Part 5 commit offer |
| 40 | Handoff Schema Cap | Bounded handoff index; total measured after the write; overflow file named to the minute (FB-131); the PreCompact hook's cut (40D); overflow file read, then deleted with its handoff (40E) |
| 41 | Script-First Dashboard Regeneration | The renderer produces the whole dashboard |
| 42 | Section-Scoped Spec Reading | Spec index, scoped reads, freshness guard (DEC-021) |
| 43 | Acceptance Reconciliation Lens | Spec boxes vs `verification-result.json` criteria (DEC-022) |
| 45 | Template Sync Removes Retired Files | Retired sync patterns and files, `⚠ deletes` rows, commit offer (FB-126) |
| 46 | Notes History and Friction Close | Notes are newest-first history; a fixing task closes its friction entries (FB-134) |
| 47 | Uncommitted-Work Check | Step 0e counts finished tasks by their uncommitted files (FB-134) |
| 48 | Restoring a Retired Feature | Revert or scoped diff of the retirement commit, pin check, no spec edits through git (FB-134) |
| 49 | Agent Decisions Recorded and Ratified | Choices held until the verify pass, one `recorded` record per task, `/work ratify` and `/work reconsider`, `/health-check` legacy rows (FB-129) |
| 50 | Template Sync Classification | Unchanged template copies apply under bare `[A]`, not-a-variant rows, shallow history and the sidecar, manifest-list and `.gitignore` rows, non-git projects (FB-136) |
| 51 | Task Provenance Baseline | Every creation path stamps section provenance (`fingerprint.py --provenance`), `spec_unmapped`, `/health-check` baseline from the spec's git history, `confirm_current` and `needs_section` rows, `same_day_edit` (FB-135) |
| 52 | Post-Verify Delta and Residue | Same-verifier delta re-check (recorded, not counted) and when there is none, counter reset when a passed task is reopened, residue check against a pre-dispatch baseline (in context or on disk) after an agent returns or is killed, browser and build verifications and queued gates one at a time, inline bound after a cutoff (FB-130, FB-132, FB-133, FB-119) |

## Example Project

All scenarios use a "data analysis pipeline" with:
- **Phase 1**: Data collection and cleaning
- **Phase 2**: Statistical analysis (blocked by DEC-001: analysis method, inflection point)
- **Phase 3**: Visualization and reporting (blocked by DEC-002: charting library, pick-and-go)
