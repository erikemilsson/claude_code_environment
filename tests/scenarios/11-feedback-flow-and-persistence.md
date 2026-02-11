# Scenario 11: Feedback Flow and Persistence

Verify that user feedback has a clear destination, is stored structurally, and can be retrieved later. This tests the full lifecycle: dashboard surfaces the need → user provides feedback → feedback is captured → feedback influences work → feedback is retrievable.

## Context

The user wants to minimize file browsing. Feedback should flow through the dashboard (or files linked from it), not require the user to know internal file locations. For research projects, this feedback is part of the deliverable — it must be structured and durable.

## State

- Phase 1: active execution
- Task 11: "In Progress" (owner: both) — "Review auth design" — needs user feedback on approach
- Task 15: "Finished" — verify-agent flagged 2 out-of-spec recommendations
- DEC-002: proposed — user reviewing caching options, wants to note constraints
- questions.md has 2 unanswered questions (1 blocking)

---

## Trace 11A: Task feedback flow

- **Path:** dashboard.md → Your Tasks format

### Scenario

Task 11 needs user feedback on the auth design. The dashboard should make it clear WHERE to write feedback and WHAT happens after.

### Expected in dashboard

```markdown
### Your Tasks

| ID | Task | Action | Link |
|----|------|--------|------|
| 11 | Review auth design | Read doc, leave feedback below | [auth-design.md](../support/decisions/decision-003.md) |

**Task 11 — Feedback:**
<!-- Write your feedback here, then run /work complete 11 -->

```

### Feedback lifecycle

1. User reads linked file (auth-design.md)
2. User writes feedback in the designated area
3. User runs `/work complete 11`
4. `/work complete` reads the dashboard, picks up feedback from the inline area
5. Feedback is captured in task JSON notes field
6. Dashboard is regenerated, feedback area disappears (task complete)

### Gap analysis

**Where does the feedback actually persist?**
- The inline feedback area in dashboard.md is between `<!-- USER SECTION -->` markers — but it's NOT in the user section. It's in the "Your Tasks" sub-section.
- When dashboard regenerates, the "Your Tasks" table is rebuilt from source data. Feedback written there is LOST on regeneration.
- The Notes section (`## 💡 Notes`) is preserved, but task feedback isn't written there.

**Current persistence model:**
- Dashboard inline feedback → transient (lost on regen)
- Task JSON notes → durable (persists across sessions)
- Decision doc → durable (persists across sessions)
- questions.md answers → durable (persists across sessions)

### Pass criteria

- [ ] Dashboard provides a clear place to write feedback for Task 11
- [ ] Feedback area has instructions on what to do after writing
- [ ] `/work complete` captures feedback before regenerating dashboard
- [ ] Feedback persists in task JSON notes after completion
- [ ] If dashboard regenerates BEFORE user runs `/work complete`, feedback in the inline area is not silently lost

### Fail indicators

- User writes feedback in dashboard, dashboard regenerates, feedback disappears
- No clear place to write feedback (user must know to edit task JSON directly)
- Feedback written but never captured in any durable location
- `/work complete` doesn't read inline feedback before regenerating

---

## Trace 11B: Decision feedback flow

- **Path:** dashboard.md → Action Required → Decisions; decisions.md → Decision Record Format

### Scenario

User is reviewing DEC-002 (caching strategy). They want to:
1. Note constraints ("Must work with our existing Redis cluster")
2. Ask a clarifying question before selecting
3. Eventually select an option

### Expected

- Dashboard links to decision doc
- Decision doc has a structured "Select an Option" section with checkboxes
- Decision doc has space for notes/constraints

### Gap analysis

**Where does the user add constraints?**
- The decision doc template has: Background, Options Comparison, Option Details, Select an Option, Decision, Trade-offs, Impact
- There's no explicit "Your Notes" or "Constraints" section in the decision template
- The user could write in "Background" but that's meant to be Claude-authored context
- The user could write after the checkboxes but there's no designated area

**Where does the user ask a clarifying question?**
- They could add to questions.md, but that requires knowing about that file
- They could write in the decision doc, but where?
- The dashboard doesn't provide a "Ask about this decision" mechanism

### Pass criteria

- [ ] Decision doc has a clear place for user notes/constraints (not just Claude-authored sections)
- [ ] Dashboard's decision link takes user to a file where they can both READ context and WRITE their input
- [ ] If user has questions about a decision, there's a clear path to ask (linked from dashboard)
- [ ] User constraints on a decision persist in the decision record (discoverable later)

### Fail indicators

- User adds notes to decision doc, Claude regenerates it, notes are lost
- No designated area for user input in the decision template
- User has to navigate to questions.md independently (not linked from decision context)
- Constraints noted during decision-making are not part of the final decision record

---

## Trace 11C: Feedback as deliverable (research projects)

- **Path:** Cross-cutting concern — not currently addressed in dashboard.md

### Scenario

User is building a research project. During the build:
- They made 5 decisions with rationale
- They provided feedback on 3 task implementations
- They answered 8 questions that shaped the architecture
- They noted constraints and trade-offs

Later, they need to compile this into a report or reference it for a follow-up project.

### Expected feedback locations (current)

| Feedback type | Storage location | Structured? | Discoverable? |
|---------------|-----------------|-------------|---------------|
| Decision rationale | `decision-*.md` files | Yes (template) | Yes (Decisions section) |
| Task implementation feedback | Task JSON `notes` field | Partially | Requires reading JSON |
| Questions & answers | `questions.md` | Yes (table) | Yes (but file not linked from dashboard) |
| Constraints | No designated location | No | No |
| Trade-off notes | Decision doc "Trade-offs" section | Yes | Yes (in decision doc) |
| Architecture reasoning | No designated location | No | No |

### Gap analysis

- Decision records are well-structured and discoverable — good
- Task feedback in JSON notes is durable but not easily browsable
- Questions and answers are structured but questions.md isn't linked from the dashboard
- There's no single "project journal" or "feedback log" that aggregates user inputs
- For research projects, compiling these into a report requires reading multiple file types

### Pass criteria

- [ ] Decision records capture user rationale (not just the selection)
- [ ] Task feedback is stored in a format that's browsable (not buried in JSON)
- [ ] questions.md is accessible from the dashboard (linked in Notes or a dedicated section)
- [ ] A user can reconstruct the decision-making history from the file system
- [ ] Archived user inputs are structured enough to be compiled into a report

### Fail indicators

- User feedback scattered across 4 different file formats with no index
- Task feedback only exists as a JSON string in a field that's hard to read
- No way to find all user inputs without reading every file in .claude/
- questions.md exists but is never linked from anything the user sees

---

## Trace 11D: Out-of-spec recommendation feedback

- **Path:** work.md → Step 3 out-of-spec task handling; dashboard.md → Reviews sub-section

### Scenario

Task 15 finished, verify-agent created 2 out-of-spec recommendations. The user needs to Accept, Reject, or Defer each. Their reasoning should be captured.

### Expected in dashboard

```markdown
### Reviews

- [ ] **Add input validation** — verify-agent recommends adding validation to API endpoints (beyond spec) → [task-16.json](../tasks/task-16.json) — Accept / Reject / Defer
- [ ] **Add rate limiting** — verify-agent recommends rate limiting for public endpoints → [task-17.json](../tasks/task-17.json) — Accept / Reject / Defer
```

### Gap analysis

**Where does the user's reasoning go?**
- work.md Step 3 out-of-spec handling offers: `[A]` Accept, `[R]` Reject, `[D]` Defer, `[AA]` Accept all
- Accept sets `out_of_spec_approved: true` — no reason field
- Reject deletes the task — no record of why
- Defer skips — no reason captured
- The user's reasoning for accepting or rejecting is lost

### Pass criteria

- [ ] Dashboard presents out-of-spec recommendations with enough context to decide
- [ ] Each recommendation links to the source (task JSON or relevant file)
- [ ] User's Accept/Reject/Defer choice is recorded
- [ ] Reasoning for the choice has a place to be captured (even optionally)
- [ ] Rejected recommendations leave a trace (not silently deleted)

### Fail indicators

- Recommendations presented without context (user can't decide from dashboard alone)
- Rejected tasks are deleted with no record they existed
- User's reasoning is not captured anywhere
- Accept/Reject is a CLI-only interaction with no dashboard trace
