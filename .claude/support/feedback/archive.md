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

