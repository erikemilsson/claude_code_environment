# Scenario 35: Lazy-Rule Triggers (v4.16.0 context diet)

Verify that content moved out of the always-loaded rules payload is still read at the right moments via its trigger stubs: `feature-retirement.md` (un-imported), `mcp-patterns.md` (MCP sections), and `extension-hooks.md § Cross-Project Capture Protocol`.

## Context

v4.16.0 cut ~26K chars from the per-session auto-load: `feature-retirement.md` left the `@import` list (needed only mid-retirement), the two MCP sections and the capture protocol moved to lazy reference docs with trigger stubs left under the original section names in `rules/agents.md`. The failure mode this scenario guards: the model acts in one of these flows WITHOUT reading the moved content, because the trigger didn't fire.

## State (Base)

- Standard project on template ≥ v4.16.0; `.claude/CLAUDE.md` imports 7 rules files (feature-retirement absent from imports, present on disk)
- A shipped feature "legacy-export" the user wants parked
- A pending parallel batch of 4 tasks, one of which requires Playwright-driven UI inspection
- The session surfaced a generally-useful rule worth promoting to the template

---

## Trace 35A: Retirement request triggers the rule read

- **Path:** user: "let's retire the legacy-export feature" → CLAUDE.md summary trigger line

### Expected

- Before ANY retirement step, Claude reads `.claude/rules/feature-retirement.md` (the summary line marks it lazy with an explicit READ-first trigger)
- The procedure then follows the rule: pre-retirement engine-consumer audit (4-pattern grep), snapshot, commit pin BEFORE the removal commit, manifest, spec annotation (not excision), discoverability entry

### Pass criteria

- [ ] The rule file is read before snapshot/manifest work begins
- [ ] No retirement step is improvised from memory of the summary line alone

### Fail indicators

- Retirement proceeds straight to `git rm` or snapshotting without the rule read
- Spec section excised instead of annotated (the canonical symptom of acting without the rule)

---

## Trace 35B: MCP-involving parallel batch triggers mcp-patterns read

- **Path:** `/work` Step 2c parallel batch includes a Playwright-driving task → `rules/agents.md § "MCP and Parallel Execution"` stub

### Expected

- The stub's one-line rule already prevents naive fan-out (route shared-MCP work through ONE agent)
- Before finalizing the dispatch plan, Claude reads `.claude/support/reference/mcp-patterns.md` for the full pattern (single MCP agent + parallelize the rest + sequential multi-route scoping)
- Cross-refs in `/diagnose`, `/audit-ui`, `/health-check` resolve to the new path

### Pass criteria

- [ ] No parallel batch ever has two agents driving the same MCP
- [ ] The reference doc is read when the batch actually involves MCP work (not on every `/work` run)

### Fail indicators

- Two subagents dispatched with browser-MCP instructions in one batch
- mcp-patterns.md read on MCP-free batches (defeats the diet)

---

## Trace 35C: Sync recommendation triggers the capture-protocol read

- **Path:** Claude about to recommend "promote this rule to the template, then sync" → `rules/agents.md § "Cross-Project Capture Protocol"` stub

### Expected

- Before the recommendation is delivered, Claude reads `extension-hooks.md § "Cross-Project Capture Protocol"` and runs the boundary check (enumerate local additions to template-owned files; route generically-applicable → promotion-first, project-specific → migration-first)

### Pass criteria

- [ ] Boundary check runs at suggestion time, not at sync time
- [ ] Findings routed per the protocol's two branches

### Fail indicators

- Sync recommended with unreconciled local additions to template-owned files
- The stub's one-liner treated as the full protocol (no read)
