# Scenario 24: Research Agent Populates Decision Records

Verify that the research agent correctly investigates options, returns decision-record content for the orchestrator to write (DEC-004), and respects the authority boundary (populates evidence but does not make selections).

## State

- Spec v1: active, describes a web application with authentication requirement
- DEC-001: status `draft`, title "Authentication Strategy", category `architecture`
  - Background filled in, comparison matrix empty, no options listed
  - `blocks: ["3", "4", "5"]` — three tasks waiting on this decision
- Task 3, 4, 5: status `Pending`, `decision_dependencies: ["DEC-001"]`
- Task 1: status `Finished` (no decision dep)
- Task 2: status `In Progress` (no decision dep)
- `.claude/support/learnings/` contains a note: "Project uses Node.js with Express"

## Trace: `/work` encounters blocking decision

- /work decision dependency check
- DEC-001 is unresolved, blocks Tasks 3, 4, 5
- Options presented: `[R]` Research, `[S]` Skip
- User selects `[R]`

### Expected

- `/work` gathers context (decision record, spec, related tasks)
- research-agent spawned via `Agent` tool with `model: "opus"`; prompt states a turn budget of about 25 tool calls
- Spawn prompt includes: decision record path, spec file, related task paths, and the instruction to return the archive and record edits in the report rather than write files

## Trace: research-agent Steps R1-R5

### R1: Understand Investigation

- Reads DEC-001 record, notes `blocks: ["3", "4", "5"]`
- Reads spec section on authentication
- Reads learnings (discovers Node.js/Express)
- Identifies criteria: security, implementation complexity, user experience, compatibility with Express

### R2: Gather Options

- Identifies 2-4 authentication approaches (e.g., session-based, JWT, OAuth2)
- Checks compatibility with Node.js/Express ecosystem
- Discards clearly incompatible options with rationale

### R3: Evaluate Options

- Scores each option against criteria
- Checks compatibility with existing decisions (none in this case)
- Identifies risks and unknowns per option

### R4: Produce Artifacts (returned, not written)

- Writes no files (subagents can't write `.claude/` — DEC-004)
- Archive: target path `.claude/support/decisions/.archive/YYYY-MM-DD_authentication-strategy.md` + full body
- Anchored edits for DEC-001 (exact existing heading + replacement body; heading kept):
  - `## Select an Option` — placeholder labels replaced with the three option names, all boxes unchecked
  - `## Options Comparison` — comparison matrix populated with criteria × options, recommendation stated after it (clearly labeled, not a selection)
  - `## Option Details` — filled in for each option, Research Notes link to the archive path
- Frontmatter change: `status: proposed` (was `draft`)
- No edit checks the selection checkbox

### R5: Report

- Returns summary: options found, recommendation, confidence level
- Then the R4 artifacts: decision-record edits first, then the archive body

### Expected

```
Research complete: Authentication Strategy

Options identified: 3
  - Session-based auth: Traditional server-side sessions with Express middleware
  - JWT tokens: Stateless auth with signed tokens
  - OAuth2 + sessions: Delegated auth with session persistence

Recommendation: JWT tokens — best fit for Express ecosystem per project learnings
Confidence: moderate

Decision record: .claude/support/decisions/decision-001-authentication-strategy.md — edits below
Research archive: .claude/support/decisions/.archive/YYYY-MM-DD_authentication-strategy.md

Decision-record edits:
  Frontmatter: status: proposed
  Edit 1 — Anchor: ## Select an Option
           Replacement: {three unchecked boxes with the real option names}
  Edit 2 — Anchor: ## Options Comparison
           Replacement: {populated matrix + labeled recommendation}
  Edit 3 — Anchor: ## Option Details
           Replacement: {three option subsections}

Research archive body:
  {methodology, sources, findings per option, discarded options}
```

## Trace: `/work` persists the artifacts (research.md Step 4, item 1)

- Writes the archive file at the reported path
- Applies Edits 1–3 to DEC-001 (each anchor matches exactly once), then `status: draft` → `proposed`
- DEC-016 `permissions.ask` prompt fires on the `decision-001-*.md` edit; user approves (sanctioned route)
- No edit checks a selection box or touches `## Your Notes & Constraints`, so none is skipped

## Trace: Post-research flow in `/work`

- `/work` re-presents DEC-001 (now with populated options)
- User can review decision record and check selection
- After selection: frontmatter auto-updated to `approved`, Tasks 3/4/5 unblock

### Expected

- Decision status transitions: draft → proposed (written by `/work` from the research-agent's report, research.md Step 4) → approved (by /work after user checks box)
- Tasks 3/4/5 become eligible for dispatch after decision approved

## Pass criteria

- [ ] Research-agent spawned with correct model and context
- [ ] Research-agent writes no files; the orchestrator writes the archive and applies the record edits (research.md Step 4)
- [ ] DEC-001 comparison matrix populated with real criteria and scores
- [ ] Option details filled in (description, strengths, weaknesses, research notes)
- [ ] Research archive document created in `.archive/`
- [ ] DEC-001 status updated to `proposed` (not `approved`)
- [ ] `## Select an Option` lists the real option names; no box checked (no returned or applied edit checks one)
- [ ] Recommendation stated but clearly labeled as recommendation
- [ ] Project learnings consulted (Node.js/Express constraint applied)
- [ ] After user selects, tasks 3/4/5 unblock normally

## Fail indicators

- Research-agent writes (or tries to write) any file instead of returning it in its report (DEC-004)
- An edit that checks the selection checkbox is returned or applied (authority violation)
- Research-agent returns a status past `proposed`, or the orchestrator sets one
- Options fabricated without considering project constraints
- Research archive not created, or the returned edits not applied (Step 4 persist skipped)
- Decision record left in `draft` status despite options being complete
- Research-agent returns edits to task files or spec files
