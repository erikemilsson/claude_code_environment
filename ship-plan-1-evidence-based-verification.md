# Ship Plan 1 — Evidence-Based Verification (close the UI/runtime verification gap)

> **Temporary working file** — root-level by request (2026-06-10). Not template content; delete after ship or move to `template-maintenance/`. Source: cross-repo usage analysis 2026-06-10 (styler + `interaction-logs/` + `template-maintenance/ship-log.md`). Companions: `ship-plan-2-prose-diet-and-mechanization.md`, `ship-plan-3-interaction-tax-and-queue.md`. All line-number anchors are approximate as of template v4.12.1 — re-locate by section name before editing.

## Problem

Verification produces textual claims; empirical truth is currently checked by Erik. Verify-agent reads diffs, never observes the running system, and never escalates a terminal "no" — so wrong passes ship (Erik catches them) and false negatives poison state (Erik unwinds them).

## Evidence base (measured 2026-06-10)

- **styler: 806 verifications, 0 terminal failures** (718 first-pass, 24 needed 2 attempts, 4 needed 3, 1 needed 4). The verifier never says "no" to the user.
- **Dominant archived-feedback theme in styler = UI drift Erik caught post-ship:** styler-local FB-149 ("score format drifts across six+ variants, sometimes within one screen"), FB-150 (timestamps), FB-138 (category names), FB-115 (boilerplate blurbs).
- **T731** (interaction-logs): task passed verification; its page returned 500.
- **T697 / template FB-085:** implement-agent claimed a false browser premise, verify-agent confirmed it from the same docs-derived model; caught only by orchestrator-driven Playwright at user hand-off.
- **FR-040** (styler friction register): BSD/macOS grep silently returned no output → false "engine dormant" finding → propagated into handoff + dashboard + memory; a full session (2026-06-10, 0 tasks completed) spent unwinding it.
- **Manual backstop loop:** 60 task-named screenshots in styler's project root (many `-fixed`/`after-fix` re-shots), 114 `owner: both` tasks queued on Erik's review, 62 of 391 session-export friction notes verification-themed.
- **The standalone audit surface is not voluntarily used:** `/audit-ui` has produced zero artifacts in styler ever; `/audit-coherence` ran exactly twice, both 2026-05-15. Capability must live inside the loops that actually run (`/work`, `/diagnose`).

## Ship items

### S1 — Ship FB-085's locked recipe into `/diagnose` (~20 lines) — ✅ SHIPPED v4.13.0 (2026-06-10)

The design is finished and locked: `template-maintenance/feedback.md § FB-085 "Resolved design"` + `template-maintenance/visual-verify-vision.md § Resolution`. Add the `## Visual / browser-rendering bugs` recipe to `commands/diagnose.md`:

- Falsifiable assertions on **measured values** (geometry + computed style via `browser_evaluate`); no pixel-diff/golden images.
- Each iteration = one falsifiable hypothesis with a **predicted value-effect** (folds in the queued "math-check before commit-to-pixels" signal from the FB-082 signal queue).
- N=3 loop, configurable; early-exit when out of distinct hypotheses; non-convergence surfaces unmet contract + per-iteration hypothesis→prediction→result trace + before/after screenshots; **never silently declares success**.
- `browser_take_screenshot` is reporting-only (FB-087); persistence of the passing contract as a test is conditional on a harness existing (FB-064 detection, `/diagnose` Phase 5 seam).
- Runs at orchestrator level (dissolves the verify-agent Playwright-sandbox blocker — exactly why the grill folded it into `/diagnose`).

**Decision — RESOLVED 2026-06-10:** Erik approved overriding the formal 2nd-project gate. Rationale recorded: the gate predates the grill that resolved cost/uncertainty; the cost is now known (~20 lines, zero new surface, trivially reversible per FB-085's own no-DEC reasoning), and the within-styler evidence volume (62/391 verification-themed notes, T731, the shipped-UI-drift FB family) exceeds what the gate was protecting against. S1 SHIPPED v4.13.0 (2026-06-10), same session as the override. FB-085 archived (full entry in `template-maintenance/feedback-archive.md`, stub in `feedback.md`); trace test at `tests/scenarios/32-diagnose-visual-recipe.md`; ship-log entry appended.

**Files:** `commands/diagnose.md`. Ledger: FB-085 → promoted; remove the FB-082 signal-queue "math-check" item as absorbed.

### S2 — Positive-control rule for negative findings (the FR-040 class) — ✅ SHIPPED v4.15.0 (2026-06-10; authoring-doc edit deliberately dropped — OS fact lives in the rule)

New short rule (one paragraph, stated once, referenced once): any **negative finding** ("X is absent / dormant / unused / has no consumer") that will be written to durable state (friction register, handoff, dashboard, verification result, retirement proposal) must either (a) come from the dedicated `Grep` tool (ripgrep — not bash grep, which on macOS can silently emit nothing on certain files), or (b) include a **positive control**: the same probe demonstrated to find a known-present target. Findings lacking both are reported as "unverified absence", not persisted.

This generalizes FB-084's 4-pattern retirement grep (which covers *which patterns* to search; this covers *whether the probe works at all*).

**Files:** `rules/agents.md` (short sub-section near "Tool Preferences"), `agents/verify-agent.md` (one line in the check contract), `support/reference/claude-code-authoring.md` (the BSD/macOS grep silent-failure fact — DEC-017's home for "facts authors trip over").

### S3 — Evidence-carrying verification for UI-affecting tasks — ✅ SHIPPED v4.15.0 (2026-06-10; lean confirmed — `evidence[]` presence, no enum split)

Make passes carry proof on tasks where the failure mode is empirical:

- **Schema** (`support/reference/task-schema.md`): add optional `task_verification.evidence[]` — `{type: computed_style | geometry | http_status | console | screenshot | build, target, assertion, observed, result}`. Open question (lean below): also split `runtime_validation: partial` into `partial_empirical` / `partial_documented` per FB-085 Option 2, or derive that rollup from `evidence[]` presence. **Lean: derive from `evidence[]`; no enum migration.**
- **Orchestrator step** (`commands/work.md § "After verify-agent returns"` / per-task verify, ~:747): for tasks with `runtime_validation: partial|required` touching web-UI surfaces, the orchestrator runs the empirical step (navigate affected route; HTTP status; console-error scan; the task's geometry/computed-style assertions) **before** writing `result: pass`. Verify-agent (subagent — no reliable Playwright access) keeps doing static checks and *names the assertions to run*; the orchestrator executes them.
- **FB-076 mitigation 1 ships here** (cheapest of its three): when a task touches client-marked files (`'use client'` or framework equivalent), run the project's production build before pass; record as `evidence[] {type: build}`. Project declares its build command in root `./CLAUDE.md` (per FB-076 § Template-side homes).

**Files:** `support/reference/task-schema.md`, `agents/verify-agent.md § runtime_validation`, `commands/work.md`, `support/reference/root-claude-md-template.md` (build-command hook).

### S4 — Phase-gate UI smoke inside `/work` — ✅ SHIPPED v4.15.0 (2026-06-10)

At phase-level verification (`commands/work.md`, phase-level verify ~:844): if the phase's tasks touched UI routes, the orchestrator runs one lite pass over the affected routes — HTTP status, console errors, the phase's accumulated `evidence[]` assertions re-checked. Reuses S1's measurement vocabulary; full `/audit-ui` remains the deep tool (referenced from the gate as the escalation). Gating mirrors `/audit-ui`'s `applies_when` web-framework detection — non-web projects see zero change.

This puts audit-ui-class checking inside the loop that demonstrably runs, instead of waiting for a voluntary invocation that has never happened.

## Sequencing & version bumps

S2 (PATCH-ish but behavioral → MINOR-safe) → S1 (MINOR: new `/diagnose` behavior) → S3 (MINOR: schema + orchestrator) → S4 (MINOR). Each independently shippable; stop after any. Bump `template_version` per ship (pre-commit hook reminds); append `template-maintenance/ship-log.md` entries.

## Acceptance

- `tests/scenarios/` additions: (a) UI-affecting task with no `evidence[]` → orchestrator does not write `result: pass`; (b) negative finding without positive control → reported as unverified-absence, not persisted; (c) `/diagnose` visual recipe non-convergence → surfaces report, no silent success.
- Trace an FR-040-shaped scenario (probe silently empty) through S2 and confirm it dies before any state write.
- `/health-check` clean; no sync-manifest changes (no files added/removed).

## Risks / mitigations

- **Playwright MCP not in the base toolset** (styler 04-20 note: tools must be loaded via ToolSearch) — S1/S3/S4 text must include the ToolSearch load step explicitly.
- **Domain-agnostic template:** every UI item gates on web-framework detection; the schema field is optional and domain-neutral (`http_status`/`build` apply to any runnable system).
- **Dev server:** starting one for verification is sanctioned; respect-prior-kills still applies (`rules/agents.md § Behavioral Rules`).
- **Token cost:** `browser_evaluate` targeted queries only (FB-087); never `browser_snapshot` on long pages.
- **Prose-growth tension with Plan 2:** S2 adds ~15 lines total; S3/S4 add to work.md. Coordinate with Plan 2 P3 (work.md split) — see Conflicts.

## Conflicts with other plans

`commands/work.md` is edited by S3/S4 here, by Plan 2 P3 (split), and by Plan 3 T3 (queue contract). Execute plans in separate sessions, anchor by section name. Suggested global order: Plan 2 P1 (pointer sweep) → Plan 3 T3 → **Plan 1** → Plan 3 T1/T2 → Plan 2 P2/P4 → Plan 2 P3/P5.

## Ledger updates on ship

- FB-085 → promoted ✅ done in v4.13.0 (archived; root `CLAUDE.md` updated).
- FB-076 → partially shipped (mitigation 1 via S3); rewrite its defer condition to cover only mitigations 2–3 (ESLint rule, live-data cross-ref).
- FB-082 signal queue: "math-check before commit-to-pixels" → absorbed by S1 ✅ done in v4.13.0.
- `template-maintenance/ship-log.md` + `.claude/version.json` per ship (✅ done for S1).
