# /work Web Evidence Gates

<!-- Loaded on demand by commands/work.md: read only when the trigger line in /work points here. -->

Orchestrator-level browser checks for web-UI work (same applies-when detection as `/audit-ui`). Non-web tasks and projects without a web framework skip both gates. During a parallel batch the per-task gate takes a turn in the exclusive-verify queue (`parallel-execution.md § "Single-Instance Resources"`): it uses the browser and may run the build.

## Empirical Evidence Gate (per-task, before persisting a pass)

**Empirical Evidence Gate (before persisting a pass):** when `report.result == "pass"` AND the task's output is a web-UI route/component in a project with a web framework (same applies-when detection as `/audit-ui`) AND `checks.runtime_validation` is `"partial"` — or `"pass"` reached without browser measurement — run the evidence step at orchestrator level BEFORE applying the persistence protocol:

1. Ensure Playwright MCP tools are loaded (ToolSearch if absent) and a dev server is available (starting one for verification is sanctioned; respect-prior-kills applies).
2. Execute `report.empirical_assertions[]` (named by verify-agent per `verify-agent.md § Step T4b` item 5; if absent, default to HTTP status + console-error scan per affected route). Use `browser_evaluate` targeted queries — never full-tree snapshots on long pages.
3. **Client-bundle check:** if the task touched client-marked files (`'use client'` or framework equivalent) and root `./CLAUDE.md` declares a build command (§ Verification Hooks), run the production build; record as a `build`-type evidence entry.
4. Record each outcome into `task_verification.evidence[]` (schema: `task-schema.md § "Evidence Sub-field"`).
5. Any failing assertion → treat the verification as `fail`: route through the normal fail path with the failing evidence appended to `issues[]`. All passing → proceed to the persistence protocol with `evidence[]` included.

Non-web tasks, projects without a web framework, and `runtime_validation: "not_applicable"` tasks skip this gate entirely — zero change for non-software domains.

## Phase UI Smoke (before acting on a phase-level pass)

**Phase UI smoke (orchestrator-level, web projects only):** before acting on a phase-level `pass`, if any task in the phase touched web-UI routes/components (same applies-when detection as `/audit-ui`), run one lite pass over the affected routes: navigate each, assert HTTP status, scan console errors, and re-check that the phase's accumulated `task_verification.evidence[]` assertions still hold (`browser_evaluate` targeted queries; load Playwright tools via ToolSearch if absent). Failures create fix tasks exactly like phase-level verification failures — loop to Execute. Each fix task is written with section provenance (`task-schema.md § "Drift Prevention Fields"`, creation contract). For depth beyond the smoke (visual quality, IA, affordances), suggest `/audit-ui`; this gate is the in-loop minimum, not a replacement. Non-web projects skip.
