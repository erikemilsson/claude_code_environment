# Scenario 34: Evidence-Carrying Verification (positive controls, evidence gate, phase smoke)

Verify the v4.15.0 trio: negative findings require a positive control (S2), web-UI passes carry orchestrator-recorded `evidence[]` (S3), and phase-level passes on UI phases get a route smoke (S4).

## Context

styler evidence basis: 806 verifications with zero terminal fails while shipped UI drift was caught by the user; T731 passed verification with a 500ing page; FR-040's silent-grep false negative poisoned state for a session. Passes must carry proof; absence claims must prove the probe works. FB-114 later showed the absence rule's mechanism defeated (controls that returned nothing, no `Grep` tool in the harness, result sets that didn't match the claim), so 34A traces the tool-agnostic version.

## State (Base)

- Next.js project, dev server available, root `./CLAUDE.md § Verification Hooks` declares `npm run build`
- Task 40: "Restyle score pill" — `runtime_validation`-eligible web UI, `owner: claude`, files: `src/components/ScorePill.tsx` (`'use client'`)
- Task 41: "Document data model" — markdown deliverable (non-runnable)

---

## Trace 34A: Negative finding without a working positive control is not persisted

- **Path:** verify-agent absence claim → `agents/verify-agent.md § Tool Preferences` ("Negative findings") → `rules/agents.md § "Negative Findings Require a Positive Control"` → `support/reference/negative-findings.md`

### Scenario

During Task 40 verification, in a harness with no `Grep` tool, verify-agent searches via Bash `rg` and finds zero references to `legacyScoreFormat`. It wants to report "field unused — candidate for removal".

### Expected

- The claim qualifies as a negative finding destined for `issues[]`/`friction_markers[]`; verify-agent reads `negative-findings.md` before reporting it
- It is reported only with a positive control that returned a hit: the same command (tool, flags, root, filters) finding a known-present symbol such as `ScorePill`, with both counts in the report. No tool earns an exemption
- Variant (broken control): the control also returns 0, e.g. an unquoted glob that zsh expanded, or a repo-root `rg` that skipped the hidden or gitignored path holding the control. The probe is broken, so nothing is reported as a finding until it's fixed
- Variant (closure sweep): T2c's reference search comes back empty, which would pass `consistency_check` → the same control is required before the pass
- With no working control: phrased as "unverified absence" in `notes`, NOT written as a finding; orchestrator does not project it into friction.jsonl / handoff / dashboard

### Pass criteria

- [ ] Absence claims with a same-command control that returned a hit pass through normally, whatever tool produced them
- [ ] A control that returns nothing invalidates the probe instead of confirming the absence
- [ ] An empty T2c reference search passes `consistency_check` only with a control
- [ ] Uncontrolled claims appear only as "unverified absence" prose
- [ ] No state write (friction register, dashboard, handoff) from an uncontrolled claim

### Fail indicators

- "Unused/dormant/no consumer" finding persisted on search silence alone
- Positive control skipped because the result "looks obviously right"
- An empty control counted as "ran the control"
- A claim exempted from the control because a particular tool (e.g. the `Grep` tool) produced it

---

## Trace 34B: Web-UI pass requires evidence; failing assertion flips to fail

- **Path:** `/work` § If Verifying (Per-Task) → Empirical Evidence Gate (`work-web-evidence.md`)

### Scenario

Task 40's verify-agent returns `result: "pass"`, `runtime_validation: "partial"`, and `empirical_assertions[]` (HTTP 200 on `/outfits`, no console errors, `.score-pill` computed `font-variant-numeric: tabular-nums`).

### Expected

- Gate runs BEFORE the persistence protocol: Playwright loaded via ToolSearch if absent; assertions executed via `browser_evaluate` targeted queries (no full-tree snapshots)
- Client-bundle check: Task 40 touched a `'use client'` file + build command declared → `npm run build` runs; outcome recorded as `build`-type evidence
- All passing → `task_verification` written WITH `evidence[]`; task → Finished
- Variant: the computed-style assertion observes `normal` instead of `tabular-nums` → verification treated as `fail`, failing evidence appended to `issues[]`, normal fail path (attempts increment, status In Progress)
- Task 41 (markdown) skips the gate entirely; no evidence expected

### Pass criteria

- [ ] No `result: "pass"` persisted for Task 40 without `evidence[]`
- [ ] Build evidence present when client-marked files were touched
- [ ] Failing assertion → fail path, not pass-with-note
- [ ] Non-runnable task unaffected (no gate, no evidence requirement)

### Fail indicators

- Pass persisted on code-reading alone for a web-UI task
- Screenshot used as the pass/fail arbiter
- Gate dispatched to a subagent (must be orchestrator-level)
- Gate forced on a non-web project or document task

---

## Trace 34C: Phase-level pass on a UI phase gets a route smoke

- **Path:** `/work` § If Verifying (Phase-Level) → Phase UI smoke (`work-web-evidence.md`)

### Scenario

Phase 3 (six tasks, four touched routes `/outfits` and `/style`) gets phase-level `result: "pass"` from verify-agent.

### Expected

- Before acting on the pass: orchestrator navigates `/outfits` + `/style`, asserts HTTP status, scans console errors, re-checks the phase's accumulated `evidence[]` assertions
- A 500 on `/style` → fix task created (same mechanics as phase-level verification failures), loop to Execute — the phase does NOT complete
- All clean → proceed to "If Completing"; `/audit-ui` suggested only as the deeper option, not auto-run
- A docs-only phase (no UI routes) skips the smoke

### Pass criteria

- [ ] Smoke runs only for phases that touched web-UI surfaces
- [ ] Route failure blocks phase completion via a fix task
- [ ] Smoke stays lite (status/console/existing assertions — no new audit lenses)

### Fail indicators

- Phase completes with a route returning 500 (the T731 class)
- Smoke silently skipped on a UI phase
- Full `/audit-ui` auto-invoked as part of the gate
