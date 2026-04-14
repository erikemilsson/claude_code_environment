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

