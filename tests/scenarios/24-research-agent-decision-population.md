# Scenario 24: Research Agent Populates Decision Records

Verify that the research agent correctly investigates options, populates decision records, and respects the authority boundary (populates evidence but does not make selections).

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
- research-agent spawned via Task tool with `model: "opus"`, `max_turns: 25`
- Spawn prompt includes: decision record path, spec file, related task paths

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

### R4: Produce Artifacts

- Writes `.claude/support/decisions/.archive/YYYY-MM-DD_authentication-strategy.md`
- Updates DEC-001:
  - Comparison matrix populated with criteria × options
  - Option Details filled in for each option
  - Research Notes link to archive document
  - Recommendation stated (clearly labeled, not a selection)
- Status updated from `draft` to `proposed`
- Selection checkbox NOT checked

### R5: Report

- Returns summary: options found, recommendation, confidence level
- Decision record path and research archive path reported

### Expected

```
Research complete: Authentication Strategy

Options identified: 3
  - Session-based auth: Traditional server-side sessions with Express middleware
  - JWT tokens: Stateless auth with signed tokens
  - OAuth2 + sessions: Delegated auth with session persistence

Recommendation: JWT tokens — best fit for Express ecosystem per project learnings
Confidence: moderate

Decision record: .claude/support/decisions/decision-001-authentication-strategy.md
Research archive: .claude/support/decisions/.archive/YYYY-MM-DD_authentication-strategy.md
```

## Trace: Post-research flow in `/work`

- `/work` re-presents DEC-001 (now with populated options)
- User can review decision record and check selection
- After selection: frontmatter auto-updated to `approved`, Tasks 3/4/5 unblock

### Expected

- Decision status transitions: draft → proposed (by research-agent) → approved (by /work after user checks box)
- Tasks 3/4/5 become eligible for dispatch after decision approved

## Pass criteria

- [ ] Research-agent spawned with correct model and context
- [ ] DEC-001 comparison matrix populated with real criteria and scores
- [ ] Option details filled in (description, strengths, weaknesses, research notes)
- [ ] Research archive document created in `.archive/`
- [ ] DEC-001 status updated to `proposed` (not `approved`)
- [ ] Selection checkbox NOT checked by research-agent
- [ ] Recommendation stated but clearly labeled as recommendation
- [ ] Project learnings consulted (Node.js/Express constraint applied)
- [ ] After user selects, tasks 3/4/5 unblock normally

## Fail indicators

- Research-agent checks the selection checkbox (authority violation)
- Research-agent sets status directly to `approved` or `implemented`
- Options fabricated without considering project constraints
- Research archive not created
- Decision record left in `draft` status despite options being complete
- Research-agent modifies task files or spec files
