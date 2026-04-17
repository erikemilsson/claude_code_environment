# Archived Feedback

All resolved feedback items. Each entry preserves its final status and reason.

- **promoted** — Incorporated into the spec via `/iterate`
- **absorbed** — Combined into another item (has `absorbed_into` pointer)
- **closed** — Investigated but decided against
- **archived** — Not relevant (quick triage)

---

## FB-001: /work must check memory for known dangerous operations before executing

**Status:** absorbed
**Captured:** 2026-04-02
**Absorbed:** 2026-04-02 — Combined into FB-008
**Absorbed Into:** FB-008

When `/work` routes to actions that involve running processes, it proceeds without checking whether previous sessions flagged those operations as dangerous.

## FB-002: /work session continuity fails across conversation boundaries

**Status:** absorbed
**Captured:** 2026-04-02
**Absorbed:** 2026-04-02 — Combined into FB-008
**Absorbed Into:** FB-008

`/work` re-derives project state from task files alone in new sessions, missing blocked tasks and promises from previous sessions.

## FB-004: Plan mode workflow changed — template should guide the new "plan to file" pattern

**Status:** absorbed
**Captured:** 2026-04-02
**Absorbed:** 2026-04-02 — Combined into FB-009
**Absorbed Into:** FB-009

The old "compact with plan" feature no longer exists. The template should guide users toward the write-to-file replacement workflow.

## FB-006: Exiting plan mode should prompt to persist the plan to a file

**Status:** absorbed
**Captured:** 2026-04-02
**Absorbed:** 2026-04-02 — Combined into FB-009, then FB-009 absorbed into FB-007
**Absorbed Into:** FB-007

When the user exits plan mode, there's no prompt to save the plan to a durable file. The exit moment is the natural trigger point for persistence.

## FB-009: Plan persistence workflow — guide users and prompt at exit

**Status:** absorbed
**Captured:** 2026-04-02
**Absorbed:** 2026-04-02 — Collapses into FB-007 once persistence guidance is clear enough
**Absorbed Into:** FB-007

The old "compact with plan" is gone. The replacement (write plan to workspace, clear, read and execute) works but is non-obvious. Users need guidance at the right moment. Collapsed into FB-007 because clear persistence guidance resolves both items.

## FB-010: Subagents spawned by /work cannot write `.claude/tasks/` or spawn nested Task tools

**Status:** absorbed
**Captured:** 2026-04-07
**Absorbed:** 2026-04-17
**Absorbed Into:** DEC-004
**Reason:** DEC-004 (subagent capability contract, approved 2026-04-14, implemented 2026-04-17) adopted Option B — orchestrator owns all `.claude/` state transitions; subagents return structured reports. This resolves the documented workflow-violation by making the report-returning pattern the contract rather than a workaround.

**Refined:** 2026-04-14 — Reconcile the subagent-capability contract. First investigate what subagents are actually allowed to do in the current harness (writes to `.claude/tasks/`, nested `Task` tool). Then align either the permissions/sandbox or the agent-definition docs so the documented workflow matches execution reality. Preference: if subagents can be given the capability, let them own Steps 6a/6b as documented — orchestrator fallback only if the harness genuinely can't allow it. Primary concern is the workflow-contract violation.
**Assessed:** 2026-04-14 — Affects `.claude/agents/implement-agent.md` (Steps 3, 6a, 6b, 6c), `.claude/agents/verify-agent.md` (T6, T7), `.claude/commands/work.md` (Step 4 dispatch), `.claude/rules/agents.md` (Context Separation), `system-overview.md` (atomic implement→verify contract). Scope: corrective. Conflict: current docs assert atomic agent-owned contract; if harness can't be fixed, orchestrator becomes co-owner — a non-trivial architectural shift. Best routed to a decision record (store at root `decisions/`, ephemeral) rather than a direct template edit, since "fix sandbox" vs "formalize orchestrator ownership" lead to different architectures.

When `/work` dispatches implement-agents and verify-agents via the `Task` tool (both in parallel batches and sequentially), the spawned subagents run in a sandbox that:

1. **Denies write access to `.claude/tasks/`** — Edit, Write, and even `Bash` (with `dangerouslyDisableSandbox: true`) all return permission-denied for any path under `.claude/tasks/`, despite the additional working directories listed in the agent env. Reads work; only writes are blocked. The implementation file edits inside `app/` succeed — only writes outside `app/` (the project's primary cwd) are blocked.

2. **Does not expose the `Task` tool** — implement-agents cannot spawn the verify-agent subagent that Step 6b of `implement-agent.md` mandates. `Task` is not in the agent's tool list and `ToolSearch` cannot find it.

The implement-agent and verify-agent workflows in `.claude/agents/*.md` both assume the agent can:
- Step 6a: write `task.status = "Awaiting Verification"` and notes back to `task-{id}.json`
- Step 6b: spawn verify-agent as a separate subagent
- Verify-agent T-steps: write `task_verification` block back to the task JSON

None of these are possible from within a spawned subagent in the current harness. Every parallel implement-agent returns a structured "I'm done, here's what I did, the coordinator needs to handle 6a/6b" report, and the orchestrator (parent `/work` agent) has to manually:
1. Read the modified task file
2. Edit status `In Progress → Awaiting Verification` + write notes
3. Spawn verify-agent itself
4. Read the verify-agent's structured report
5. Manually persist the `task_verification` block + status `Awaiting Verification → Finished`

This worked but added significant orchestrator overhead per task. In a recent Phase 10 session (7 tasks across 3 dispatch rounds), the coordinator handled 14 manual JSON edits + 7 verify-agent dispatches + 7 manual verification persistences. The cost is real: extra context window pressure on the coordinator, slower parallel batches (because re-serialization at the orchestrator), and a workflow contract violation (Steps 6a/6b are nominally the implement-agent's responsibility, not the coordinator's).

## FB-012: Standardized base allowedTools set in template with merge-aware health-check

**Status:** absorbed
**Captured:** 2026-04-08
**Absorbed:** 2026-04-17
**Absorbed Into:** DEC-005
**Reason:** DEC-005 (base allowedTools shipping policy, approved 2026-04-14, implemented 2026-04-17) adopted Option E — template ships `.claude/settings.json` with 15-entry base `permissions.allow`; additions layer via `settings.local.json`; health-check enforces the boundary. All four concerns from this item (base set shape, merge strategy, file ownership, health-check behavior) are resolved by the decision record and its implementation. FB-026 (auto-mode reevaluation) may revisit the permissions model, but that is a new decision, not a reopening of this item.

**Refined:** 2026-04-14 — Promoted without Q&A; capture text is the refined insight. Add a conservative template-owned "base" `allowedTools` set (safe for any project) to reduce permission prompts in `acceptEdits` mode. Projects extend via their own `.claude/settings.json` / `.claude/settings.local.json`. Health-check must merge the base set into existing projects without clobbering project-specific additions.
**Assessed:** 2026-04-14 — Requires a new shipped `.claude/settings.json` (doesn't exist today — template policy is currently "doesn't ship settings"), reclassifying it in `.claude/sync-manifest.json` (probably to a new `merge` category), flipping `health-check.md` Part 5c (which currently asserts the opposite), adding key-granular merge logic to Part 5 Template Sync, and updating `system-overview.md` and root `CLAUDE.md` file-boundary table. Scope: additive + corrective. Open policy questions (merge strategy add-only vs remove-on-update, which Bash commands belong in base set, whole-file vs key-granular merge) warrant a decision record at root `decisions/` before implementation. Note: the reversal should be scoped to `allowedTools` only — hooks/env/theme stay user-owned, which forces key-granular merge logic.

Add a standardized set of accepted permissions (`allowedTools`) to the Claude Code environment template. Goal: reduce permission prompts (especially in `acceptEdits` mode, since Max plan can't use auto mode) while keeping things safe and maintainable.

## FB-013: Revisit hard phase transition dependencies for cross-phase parallel tasks

**Status:** absorbed
**Captured:** 2026-04-10
**Absorbed:** 2026-04-17
**Absorbed Into:** DEC-006
**Reason:** DEC-006 (phase gate flexibility, approved 2026-04-14, implemented 2026-04-17) adopted Option A — optional `cross_phase: true` boolean on individual tasks exempts them from the phase gate on eligibility while preserving phase membership for verification. Directly resolves the SIREN recruitment case that surfaced this item; schema, eligibility, dashboard annotation, breakdown inheritance, and health-check boolean validation all landed in the same pass.

**Refined:** 2026-04-14 — The hard phase gate is a software-centric assumption that breaks for research/procurement/stakeholder-engagement domains where long-running activities (often `owner: human`) must start before prior phases close. SIREN is representative, not a one-off, so a schema change is justified. Two viable mechanisms remain open and should go to a decision record: (a) add optional `cross_phase: true` on individual tasks, or (b) weaken the phase gate to only block on `owner: claude` / `owner: both`, letting `owner: human` tasks float. Other directions (spec-level phase-overlap declarations, document-the-workaround) are disfavored.
**Assessed:** 2026-04-14 — Affects `task-schema.md` (`phase` field definition line 122), `phase-decision-gates.md` (enforcement procedure), `commands/work.md` Step 4, `rules/task-management.md` + `rules/spec-workflow.md`, `commands/health-check.md` Part 1, `commands/breakdown.md` (subtask inheritance under option a), `dashboard-regeneration.md` (cross-phase rendering), `system-overview.md` (invariant description). Scope: additive (option a) or corrective (option b reverses a documented invariant). Note: parallel-execution rules in `task-management.md` already use dependency+file-conflict eligibility without referencing phase — FB-013 is consistent with that model. Decision record at root `decisions/` (ephemeral) should resolve (a) vs (b); once decided, implementation is bounded.

Original capture: phase gate blocks Phase N+1 tasks until all Phase N complete — breaks for research/procurement/stakeholder work with long-running activities that naturally span phases. SIREN workshop recruitment was the surfacing case.

## FB-020: Research Skills architectural limitations before template adoption

**Status:** absorbed
**Captured:** 2026-04-17
**Absorbed:** 2026-04-17
**Absorbed Into:** DEC-007
**Reason:** DEC-007 (Skills adoption scope, approved 2026-04-17 Option B — reference-only adoption) resolved the user's blocking concern. Research finding: Skills inject into the caller's message stream (shared context), so orchestration/verify flows cannot live in Skills, but subagents spawned from within a Skill still get fresh context. DEC-004 isolation is preserved. Template will adopt Skills only for on-demand reference content; orchestration and verify flows stay in commands and subagents. Also resolves FB-033's Skill-vs-subagent sub-question: spec-auditor must be a subagent.

**Assessed:** 2026-04-17 — Affects potentially new `.claude/skills/` dir, `.claude/CLAUDE.md`, `.claude/rules/agents.md`, commands, and subagent/skill context-window architecture. Scope: exploratory. Research-first: must resolve subagent-vs-skill context-window semantics (user's primary concern — would affect DEC-004 guarantees) plus distribution/override semantics and permissions inheritance before any migration. FB-033 depends on this outcome (subagent vs skill for spec-auditor). Route: Phase 3 research (candidate DEC-007). Do not begin any implementation.

Source: Claude Code best-practices doc (fetched 2026-04-17) — presents Skills as the on-demand alternative to CLAUDE.md for "domain knowledge or workflows that are only relevant sometimes." User flagged adoption as research-first, not implementation. Primary concern: subagent context-window behavior when spawned from a Skill.

## FB-026: Reevaluate permissions story given auto-mode maturity

**Status:** absorbed
**Captured:** 2026-04-17
**Absorbed:** 2026-04-17
**Absorbed Into:** DEC-008
**Reason:** DEC-008 (auto-mode reevaluation, approved 2026-04-17 Option D — narrow to 8 entries + document auto mode) resolved the inflection question. Research finding: `permissions.allow` rules short-circuit the auto-mode classifier — the shipped allowlist is not dead code (saves latency, covers dontAsk/CI, supports hooks). Full reversal would break hooks and non-Opus-4.7 users. Option D narrows the shipped list from 15 to 8 essential entries and adds auto-mode documentation. The layered two-file model from DEC-005 stays intact. Unblocks FB-037.

**Assessed:** 2026-04-17 — Affects `.claude/settings.json`, `.claude/sync-manifest.json`, `.claude/commands/health-check.md` Part 5c, `.claude/CLAUDE.md` Critical Invariants, `system-overview.md`, `.claude/README.md` Settings section. Scope: corrective — may reverse portions of DEC-005. Inflection-point candidate DEC-008. Blocks FB-037 (hook recipe shape depends on outcome). Research can start immediately — no upstream dependencies. Route: Phase 3 research (candidate DEC-008).

Source: Claude Code best-practices doc (fetched 2026-04-17) mentioned auto mode (`--permission-mode auto`) as alternative to explicit allowlists. Auto mode became available on Max plan ~2026-04-13, post-dating DEC-005's assumptions. User flagged the potential inflection: if auto mode covers most of the base allowlist at runtime, the shipped file may be unnecessary complexity.

## FB-003: Template's subdirectory layout causes Turbopack CSS resolution failure in Next.js 16

**Status:** promoted
**Captured:** 2026-04-02
**Promoted:** 2026-04-02 — Incorporated into template: `.claude/support/reference/known-issues.md` (KI-001), `commands/work.md` § Step 0 Preamble + Step 4 Safety Gate

Template ships contextual advisory about Turbopack/subdirectory bug, surfaced via `/work` hazard check when dev servers are relevant. Subdirectory vs. flat layout research deferred to a separate decision record.

## FB-005: Template files changed — system-overview.md needs updating

**Status:** promoted
**Captured:** 2026-04-02
**Promoted:** 2026-04-02 — Incorporated into `system-overview.md` § Instruction Architecture (rules inventory) and § Proactive Context Transitions (authoritative files)

Updated system-overview.md to reflect session-management.md and Session Management section in CLAUDE.md.

## FB-007: Handoff, plan, and memory overlap — streamline into a coherent workflow

**Status:** promoted
**Captured:** 2026-04-02
**Promoted:** 2026-04-02 — Incorporated into `system-overview.md` § Three Persistence Mechanisms, `commands/work.md` § Step 0a2, `rules/session-management.md` § Which Persistence Mechanism When

Three-lane model (handoff/plan/memory) with clear decision table, explore→plan→execute named workflow, and `/work` Step 0 plan file auto-discovery.

## FB-008: /work fails to restore context at session boundaries

**Status:** promoted
**Captured:** 2026-04-02
**Promoted:** 2026-04-02 — Incorporated into `system-overview.md` § Dangerous Operations Require Safety Checks, `commands/work.md` § Step 0 Preamble + Step 4 Safety Gate

New design principle: never auto-execute flagged-dangerous operations. `/work` Step 0 consults auto-memory and known-issues before execution, Step 4 gates dangerous processes behind user confirmation.

## FB-014: Dashboard Mermaid diagrams are unreadable at scale — need diagram rules overhaul

**Status:** promoted
**Captured:** 2026-04-10
**Refined:** 2026-04-14 — Reframe the dashboard diagram's purpose from "project overview" to "orientation snapshot": show where the user is now and what's next in line, with dependency detail on upcoming tasks. It does not need uniformly-sized boxes for every task or phase. The current approach works up to ~10 tasks and breaks beyond that. Mermaid is preferred but not mandatory. Scope: diagram-generation rules in `dashboard-regeneration.md` and `rules/dashboard.md`. Large-project rendering should zoom in on the active frontier rather than fitting the whole project on one canvas.
**Assessed:** 2026-04-14 — Primary rewrite target: `dashboard-regeneration.md` § "Project Overview Diagram" — remove `graph LR` as hard rule, drop the ">15 nodes" critical-path-only threshold, revisit the 4-task render threshold, switch labeling model to frontier-vs-context, and shift scaling from "fit everything" to "show the frontier". Direct template edit — no decision record needed.
**Promoted:** 2026-04-14 — Incorporated into `system-overview.md` § Communication: Dashboard and CLI-Direct → "Dashboard visualization features" (Orientation diagram bullet). Follow-up work targets `dashboard-regeneration.md` § "Project Overview Diagram" and `rules/dashboard.md` § Scaling.

## FB-016: Feedback review should persist review notes for /iterate handoff

**Status:** promoted
**Captured:** 2026-04-13
**Refined:** 2026-04-14 — Phase 2 refinement Q&A and Phase 3 impact assessment Q&A both generate context (scoping decisions, motivation, priority signals, "explicitly not X" boundaries) that is lost after the one-line `**Refined:**` / `**Assessed:**` summaries. Add a `**Review notes:**` section captured at both trigger points (end of Phase 2 refinement, and on `[Y] Approve` in Phase 3). The command must explicitly prompt the user for review notes — do not auto-generate from the conversation (fabrication risk). Prefer noisier UX over silent drift. Scope: `commands/feedback.md` Phase 2 and Phase 3 flow.
**Assessed:** 2026-04-14 — Isolated to `commands/feedback.md`. `commands/iterate.md` already reads ready items — no logic change, just benefits from richer source. Dependency: FB-018 also edits Phase 2 flow — bundle implementation. Review notes apply after `[R] Refine` Q&A only, not after `[P] Promote`.
**Promoted:** 2026-04-14 — Incorporated into `system-overview.md` § Feature Catalog → Feedback System (Review notes persistence). Follow-up work targets `commands/feedback.md` Phase 2 Refine flow and Phase 3 Approve flow.

## FB-018: /feedback review Phase 2 options need clarification and a "proceed without refining" path

**Status:** promoted
**Captured:** 2026-04-14
**Refined:** 2026-04-14 — Two UX gaps: (1) inline option prompts like `[R] / [C] / [N] / [S]` need a short one-line gloss on every letter; a single legend printed once is not enough — the gloss must ride with every prompt. (2) Add `[P] Promote — mark refined using current text` in Phase 2 that skips Q&A refinement and sets status to `refined` using the capture text. Phase 2 only — Phase 3 keeps its `[Y] Approve` gate. Scope: `commands/feedback.md` Phase 2 prompts and option handling.
**Assessed:** 2026-04-14 — Isolated to `commands/feedback.md`: add glosses everywhere option menus appear and add a `[P] Promote` action handler. Dependency: FB-016 (Review notes) — bundle implementation since both edit Phase 2; Review notes apply after `[R] Refine` Q&A only, not after `[P] Promote`.
**Promoted:** 2026-04-14 — Incorporated into `system-overview.md` § Feature Catalog → Feedback System (Promote path). Follow-up work targets `commands/feedback.md` Phase 2 prompts (glosses on every option menu) and the new `[P] Promote` action handler.

