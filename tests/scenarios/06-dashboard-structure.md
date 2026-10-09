# Scenario 06: Dashboard Structure and Actionability

Verify that the dashboard provides a complete, actionable view of the project at every stage — from first generation through active execution to completion.

## Trace A: Full project skeleton visible

### State

3 phases, 8 tasks. Phase 1: 3 ready. Phase 2: 3 blocked by DEC-001 (inflection point). Phase 3: 2 blocked by DEC-002 + Phase 2.

### Expected

All phases and decisions visible with blocking context; tasks appear as per-phase counts and as nodes in the Flow graph (the HTML dashboard has no per-task table, DEC-024).

### Pass criteria

- [ ] All phases visible in the Phase map even when most work is blocked (one heatmap cell and one active-front card each)
- [ ] Each phase shows its done/total count and status: Phase 1 `Active` 0/3, Phase 2 `Blocked (DEC-001)` 0/3, Phase 3 `Blocked (DEC-002)` 0/2
- [ ] Blocking reasons visible: the decision ID in the phase status, and each unresolved decision as a `❗` node feeding the tasks it gates in the Flow graph
- [ ] The Flow graph draws the critical path with a heavier stroke, user actions (`❗` nodes) included
- [ ] Full project journey understandable from dashboard alone

### Fail indicators

- Only Phase 1 shown (blocked phases hidden)
- A blocked phase shown without the decision that blocks it
- Dashboard requires reading task JSON to understand which phase is blocked and by what

---

## Trace B: First impression after decomposition

### State

- Spec v1 just decomposed into tasks
- 4 Claude tasks, 1 human task ("Configure API keys"), 1 pending decision
- No work started, no drift, no verification debt

### Expected

- Masthead and Pulse provide instant orientation (project name, stage, task and phase counts, completion % ring with per-status counts)
- The "Needs you" card (Action Required) appears early — after Pulse and the Phase map, plus the Flow graph when it renders
- The card shows only populated sub-sections (here Decisions and Your Tasks; empty ones omitted)
- Pending decision has a link to the decision doc file
- Human task row names the action and its command: `Configure API keys — yours to do → run /work complete 5` (task rows carry a command, not a file link)
- No "null state noise" — empty sub-sections are omitted, not shown as placeholders; the Timeline and Acceptance criteria sections are absent while they have no data

### Pass criteria

- [ ] Action Required visible without scrolling past boilerplate
- [ ] Decision listed with clickable link to decision doc
- [ ] Human task listed with what to do and the command that closes it
- [ ] Empty sub-sections omitted entirely (no placeholder text)
- [ ] Dashboard fits in a reasonable length for a fresh project

### Fail indicators

- User must scroll past empty sections to reach actionable content
- Decision listed without a link, or human task listed without its command
- Empty sub-sections rendered with "None" or similar placeholders
- Dashboard is excessively long for a project with no work done

---

## Trace C: Action item completeness

### State

- Active execution with multiple types of attention items:
  - Task with missing verification (verification debt)
  - Pending decision blocking tasks
  - Human-owned task needing action
  - Claude-owned task Finished with `user_review_pending: true` (a `test_protocol` awaits the user)
  - `owner: "both"` task Blocked on the user's A-or-B choice; the choice is in sidecar `augment_rows[]` with `task_id` set

### Expected

Every item in Action Required is fully actionable from the dashboard:
- Each item has a description of what the user needs to do
- Each decision row links to its record (path relative to `.claude/`, where `dashboard.html` lives); task rows carry no file link
- Each item names the command that resolves it (`/work`, `/work complete {id}`, `/work {id}`, or ticking an option in the decision record; `fyi` augment rows excepted)
- Items are consistent with the rest of the page (the Decisions card, the Pulse verification-debt count)
- Your Tasks lists the review-pending task whatever its owner (it is Finished; a stale flag on unfinished work gets no row), and the Blocked both-owned task; "Also Needs You" (last) carries the A-or-B question

### Pass criteria

- [ ] Verification debt lists affected tasks with instruction to run `/work`
- [ ] Pending decisions link to decision doc, with the decision's title
- [ ] Human task rows read `{title} — yours to do → run /work complete {id}`
- [ ] Review-pending row closes with `/work complete {id}`, even for a Finished, Claude-owned task
- [ ] The Blocked task's choice is answerable from the card alone
- [ ] No item requires browsing the file tree to figure out what to do

### Fail indicators

- Items listed as counts without identifying which tasks/decisions
- Decision link missing or using an absolute path
- No instruction on how to resolve or signal completion
- Action Required lists a decision the Decisions card doesn't have
- Review-pending or Blocked-on-you task missing because of its owner or status

---

## Trace D: Section toggles and phase relevance

### State

- The dashboard is read-only HTML with no in-file Sections checklist (DEC-024); the four switches (`action_required`, `decisions`, `notes`, `custom_views`) live in sidecar `section_toggles` (`dashboard-regeneration.md § "Section Toggle Configuration"`)
- User asks Claude to turn "Decisions" off (small project, few decisions), or edits `dashboard-state.json`; the orchestrator writes `section_toggles.decisions: false` (Step 2b) and regenerates

### Expected

- The Decisions card is excluded entirely from the regenerated page (no heading, no content); unresolved decisions still get their rows in the "Needs you" card
- Sections switched on are generated from source data; every other section (Pulse, Phase map, Flow, Timeline, Specification) renders from data and has no switch
- `action_required: false` is the exception: the "Needs you" card stays, with the line "Action Required section is toggled off."
- The sidecar's toggle state is preserved across regenerations (the script only reads it)
- On first generation, static toggle defaults are seeded (Decisions on even with no records; the card itself is omitted until a record exists)

### Pass criteria

- [ ] No toggle checklist in `dashboard.html`; `section_toggles` in the sidecar is the only source
- [ ] Switching a section off removes it entirely from regenerated output
- [ ] Regeneration preserves the sidecar's toggle state
- [ ] First generation seeds the static defaults

### Fail indicators

- Toggle ignored during regeneration
- Excluded sections still show a heading
- Regeneration overwrites the sidecar's toggle state
- A toggle changed by editing `dashboard.html` (gone at the next regen)

---

## Trace E: Critical path visualization

### State

- Complex project: 3 phases, parallel-eligible tasks, decision gates, human and Claude tasks interleaved

### Expected

- The Flow section's inline-SVG dependency graph communicates the dependency chain (`render_svg_graph`; there is no critical-path one-liner in the HTML dashboard)
- Owner indicators show who owns each node: `❗` you, `🤖` Claude, `👥` both, with a fill colour per owner
- Parallel branches sit in the same column, between the fork and join nodes their edges connect
- User action items stand out visually: human-owned tasks and unresolved decisions (`❗ DEC-NNN`) have their own colours
- The critical path (longest chain) has heavier node and edge strokes; the caption reads `Owners: ❗ you · 🤖 Claude · 👥 both · heavier stroke = critical path`
- Above 15 incomplete tasks the graph reduces to the critical path plus immediate neighbours, with a caption counting the omitted tasks

### Pass criteria

- [ ] Owner indicators present on every node
- [ ] Sequential flow shown with arrows, left to right
- [ ] Parallel branches visible as nodes sharing a column
- [ ] User can determine "what do I need to do" vs "what is Claude doing" at a glance
- [ ] Critical path distinguishable by its heavier stroke

### Fail indicators

- Nodes drawn without owner indicators
- Graph drawn for a degenerate case (fewer than 4 incomplete tasks, no edges, or a dependency cycle), where it should be hidden
- Parallel branches shown as sequential
- Critical path not distinguishable from the other edges
