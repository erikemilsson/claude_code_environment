# Scenario 35: Lazy-Rule Triggers (v4.16.0 context diet)

Verify that content moved out of the always-loaded rules payload is still read at the right moments via its trigger stubs: `feature-retirement.md` (path-scoped since v5.10.0), `mcp-patterns.md` (MCP sections), and `extension-hooks.md § Cross-Project Capture Protocol`.

## Context

v4.16.0 cut ~26K chars from the per-session auto-load: `feature-retirement.md` left the `@import` list (needed only mid-retirement), the two MCP sections and the capture protocol moved to lazy reference docs with trigger stubs left under the original section names in `rules/agents.md`. The failure mode this scenario guards: the model acts in one of these flows WITHOUT reading the moved content, because the trigger didn't fire.

Leaving the `@import` list never kept `feature-retirement.md` out of context: Claude Code loads every `.claude/rules/**/*.md` without `paths:` frontmatter at launch (`claude-code-authoring.md § "Rules loading"`), so it loaded into every session until v5.10.0. Since v5.10.0 its `paths:` frontmatter (`.claude/support/retired/**`) loads it only when Claude uses the Read, Write or Edit tool on a file under `.claude/support/retired/`; a Bash read doesn't trigger it.

## State (Base)

- Standard project on template ≥ v5.10.0; `.claude/CLAUDE.md` imports 7 rules files. `feature-retirement.md` is in `.claude/rules/`, not imported, with `paths:` frontmatter scoping it to `.claude/support/retired/**`
- A shipped feature "legacy-export" the user wants parked
- A pending parallel batch of 4 tasks, one of which requires Playwright-driven UI inspection
- The session surfaced a generally-useful rule worth promoting to the template

---

## Trace 35A: Retirement request triggers the rule read

- **Path:** user: "let's retire the legacy-export feature" → CLAUDE.md summary trigger line

### Expected

- At session start the rule's text is not in context: its `paths:` frontmatter keeps it from loading at launch
- Before ANY retirement step, Claude reads `.claude/rules/feature-retirement.md` (the summary line names it path-scoped and says to read it first: a retirement starts before any file under `.claude/support/retired/` is touched, so the path trigger alone would fire too late)
- The procedure then follows the rule: pre-retirement engine-consumer audit (4-pattern grep), snapshot, commit pin BEFORE the removal commit, manifest, spec annotation (not excision), discoverability entry

### Pass criteria

- [ ] A fresh session's launch context doesn't contain the rule's text
- [ ] The rule file is read before snapshot/manifest work begins
- [ ] No retirement step is improvised from memory of the summary line alone

### Fail indicators

- The rule's text is in a fresh session's launch context (no `paths:` frontmatter, or frontmatter that doesn't parse, which loads the rule at launch)
- Retirement proceeds straight to `git rm` or snapshotting without the rule read
- Spec section excised instead of annotated (the canonical symptom of acting without the rule)

### Variant 35A2: Restore request

- **Path:** user: "bring legacy-export back" → Claude uses the Read tool on `.claude/support/retired/legacy-export/manifest.json`
- The Read matches `.claude/support/retired/**`, so Claude Code loads the rule (frontmatter stripped) and the restore follows its `§ "Restore Path"`: retirement commit, removal check, pin check, route; never `git cherry-pick`. Had Claude read the manifest with Bash `cat`, the rule wouldn't load; the summary line's READ-first instruction covers that case.

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
