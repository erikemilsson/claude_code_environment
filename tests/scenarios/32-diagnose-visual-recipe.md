# Scenario 32: /diagnose Visual Recipe (browser-rendering bugs)

Verify that the `## Visual / browser-rendering bugs` recipe in `commands/diagnose.md` (shipped v4.13.0, FB-085) enforces measured-value contracts, keeps screenshots out of the pass/fail role, surfaces non-convergence instead of silently stopping, and runs at orchestrator level.

## Context

FB-085's failure mode: implement-agent claims a load-bearing browser behavior, verify-agent confirms it by reading the same diff, both share the same wrong docs-derived model (styler T697). The recipe makes the running browser the arbiter via falsifiable assertions on measured values, with an N=3 hypothesis loop. The trace paths below exercise the recipe's guardrails.

## State (Base)

- Web project (Next.js) with a running dev server on `localhost:3000`
- Bug report: "the section header jumps ~40px after smooth-scroll lands on the anchor"
- Task T-50: `runtime_validation: partial`, `owner: both`, difficulty 5
- No test harness configured (no `tests/` dir, no `package.json` test script beyond the default placeholder)

---

## Trace 32A: Non-convergence surfaces a report — never silent success

- **Path:** `/diagnose` → Visual recipe → loop hits the N=3 cap with the contract still failing

### Scenario

Three iterations run. Each had one falsifiable hypothesis with a pre-computed predicted value-effect; each measured result missed its prediction. No distinct hypotheses remain.

### Expected

- The loop stops at the cap (no 4th tweak-and-see iteration)
- A report is surfaced to the user containing: (a) the unmet contract (the measured-value assertions still failing), (b) the per-iteration hypothesis → prediction → measured-result trace, (c) before/after screenshots as reporting evidence
- The bug is NOT declared fixed; the task is NOT moved toward Finished
- No auto-escalation to another flow without the user seeing the report

### Pass criteria

- [ ] Iteration count respects the cap (default 3; configurable)
- [ ] Report includes contract + full per-iteration trace + before/after screenshots
- [ ] No success claim appears anywhere in the report
- [ ] Early-exit honored if distinct hypotheses run out before the cap

### Fail indicators

- A 4th+ iteration of small CSS tweaks without a new falsifiable hypothesis
- "Fixed" / task completion despite a failing contract
- Loop ends with no user-facing report (silent stop)

---

## Trace 32B: Measured values are the arbiter — screenshots and pixel-diffs are not

- **Path:** `/diagnose` → Visual recipe → contract construction (Phases 1–2) + measurement

### Scenario

The orchestrator builds the feedback loop for the anchor-scroll bug.

### Expected

- The contract is falsifiable assertions on measured values: e.g., "after smooth-scroll settles, `header.getBoundingClientRect().top` is 0±5px" — via `browser_evaluate` targeted queries
- Pixel-diff / golden-image comparison is NOT proposed as the contract
- `browser_take_screenshot` may be captured for the report, but no pass/fail decision keys on a screenshot
- Each loop iteration's hypothesis carries a predicted value-effect computed BEFORE the code edit (the math-check discipline)
- Predictions are outcome-shaped per Phase 3 ("after X, measured value Y within tolerance T"), never mechanism-shaped

### Pass criteria

- [ ] Contract expressed as geometry/computed-style assertions with tolerances
- [ ] `browser_evaluate` used for measurement (targeted queries, not full-page snapshot)
- [ ] Screenshots appear only as reporting evidence
- [ ] Predicted value-effect stated before each edit
- [ ] No pixel-diff/golden-image step anywhere

### Fail indicators

- "Take a screenshot and check if it looks right" as the verification step
- `browser_snapshot` full-tree dumps on a long page (violates result-size rule)
- Code edit applied before any prediction is stated
- Mechanism-shaped prediction ("because the browser re-evaluates the target mid-scroll")

---

## Trace 32C: Orchestrator-level execution + harness-conditional persistence

- **Path:** `/diagnose` invoked mid-`/work` on T-50 → recipe execution placement → Phase 5

### Scenario

The bug surfaced while implement-agent worked T-50. `/diagnose` engages with the visual recipe.

### Expected

- The browser loop runs in the main conversation (orchestrator level) — NOT delegated to implement-agent or verify-agent via Task dispatch
- If Playwright tools are absent from the loaded toolset, they are loaded via ToolSearch before the loop starts
- Dev server: already running here; if it had been user-killed earlier in the session, the recipe does not restart it without renewed approval (respect-prior-kills)
- Phase 5: with no test harness present (Base state), the loop is ephemeral — final measured values land in the task's verification notes; no orphan test files created. (Variant: with a harness present, the recipe OFFERS to persist the passing contract as a regression test — does not silently write one.)

### Pass criteria

- [ ] No Task-dispatched subagent drives the browser
- [ ] ToolSearch load step happens when Playwright tools are missing
- [ ] Respect-prior-kills honored on the dev server
- [ ] No harness → ephemeral loop + measured values recorded in task notes
- [ ] Harness present (variant) → offer-to-persist, not silent write

### Fail indicators

- verify-agent or implement-agent prompt includes browser-MCP driving instructions
- Recipe stalls on missing Playwright tools instead of ToolSearch-loading them
- Test file written into a project with no harness, or persisted without offering
