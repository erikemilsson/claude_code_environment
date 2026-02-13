# Scenario 06: Dashboard Structure and Actionability

Verify that the dashboard provides a complete, actionable view of the project at every stage — from first generation through active execution to completion.

## Trace A: Full project skeleton visible

### State

3 phases, 8 tasks. Phase 1: 3 ready. Phase 2: 3 blocked by DEC-001 (inflection point). Phase 3: 2 blocked by DEC-002 + Phase 2.

### Expected

All phases, tasks, and decisions visible with blocking context.

### Pass criteria

- [ ] All phases visible even when most work is blocked
- [ ] Tasks grouped by phase with per-phase summary
- [ ] Blocking reasons visible (decision IDs, phase dependencies)
- [ ] Critical path shows the sequence including user actions
- [ ] Full project journey understandable from dashboard alone

### Fail indicators

- Only Phase 1 tasks shown (blocked phases hidden)
- Tasks shown without dependency/blocking context
- Dashboard requires reading task JSON to understand what's blocked

---

## Trace B: First impression after decomposition

### State

- Spec v1 just decomposed into tasks
- 4 Claude tasks, 1 human task ("Configure API keys"), 1 pending decision
- No work started, no drift, no verification debt

### Expected

- Header provides instant orientation (project name, stage, completion %, counts)
- Action Required section appears early — within the first screenful
- Action Required shows only populated sub-sections (empty ones omitted)
- Pending decision has a link to the decision doc file
- Human task has an action description and a link to the relevant file
- No "null state noise" — empty sub-sections are omitted, not shown as placeholders

### Pass criteria

- [ ] Action Required visible without scrolling past boilerplate
- [ ] Decision listed with clickable link to decision doc
- [ ] Human task listed with what to do and where to go
- [ ] Empty sub-sections omitted entirely (no placeholder text)
- [ ] Dashboard fits in a reasonable length for a fresh project

### Fail indicators

- User must scroll past empty sections to reach actionable content
- Decision or human task listed without links
- Empty sub-sections rendered with "None" or similar placeholders
- Dashboard is excessively long for a project with no work done

---

## Trace C: Action item completeness

### State

- Active execution with multiple types of attention items:
  - Task with missing verification (verification debt)
  - Pending decision blocking tasks
  - Human-owned task needing action

### Expected

Every item in Action Required is fully actionable from the dashboard:
- Each item has a description of what the user needs to do
- Each item links to the relevant file (relative path from dashboard)
- Each item provides a way to signal completion
- Items are consistent with their detail sections (Tasks, Decisions)

### Pass criteria

- [ ] Verification debt lists affected tasks with instruction to run `/work`
- [ ] Pending decisions link to decision doc with question summary
- [ ] Human tasks have action descriptions and file links
- [ ] No item requires browsing the file tree to figure out what to do

### Fail indicators

- Items listed as counts without identifying which tasks/decisions
- Links missing or using absolute paths
- No instruction on how to resolve or signal completion
- Action Required references items missing from detail sections

---

## Trace D: Section toggles and phase relevance

### State

- Dashboard has a Sections checklist at the top
- User unchecks "Decisions" (small project, few decisions)

### Expected

- Unchecked sections excluded entirely from regeneration (no heading, no content)
- Checked sections generated from source data
- Section checklist preserved across regenerations (user's checkbox state is authoritative)
- On first generation, toggle defaults computed from project state (e.g., Decisions checked only if decisions exist)

### Pass criteria

- [ ] Sections checklist exists at the top of dashboard.md
- [ ] Unchecking a section removes it entirely from regenerated output
- [ ] Regeneration preserves the user's checkbox state
- [ ] First generation computes sensible defaults from project content

### Fail indicators

- Toggle ignored during regeneration
- Excluded sections still show a heading
- Regeneration overwrites user's checklist state
- Toggle requires editing config files instead of the dashboard itself

---

## Trace E: Critical path visualization

### State

- Complex project: 3 phases, parallel-eligible tasks, decision gates, human and Claude tasks interleaved

### Expected

- Critical path one-liner in the Progress section communicates the dependency chain
- Owner indicators show who owns each step
- Parallel branches use bracket notation showing fork/join points
- User action items stand out visually
- For complex projects, one-liner supplemented with an inline diagram

### Pass criteria

- [ ] Owner indicators present on every step
- [ ] Sequential flow shown with arrows
- [ ] Parallel branches visible via bracket notation
- [ ] User can determine "what do I need to do" vs "what is Claude doing" at a glance
- [ ] Step count includes parallel branches

### Fail indicators

- Steps listed without owner indicators
- One-liner wraps so many times it defeats the purpose
- Parallel branches shown as sequential
- Critical path is a numbered list instead of a one-liner
