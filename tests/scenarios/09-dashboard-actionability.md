# Scenario 09: Dashboard Action Item Completeness

Verify that every item in "Action Required" is fully actionable from the dashboard — the user should never need to browse the file tree to figure out what to do or where to go.

## Context

The user has `dashboard.md` open in a split pane next to Claude Code CLI. The project is in active execution. Multiple types of attention items exist simultaneously. The test verifies the "action item contract" from dashboard.md: every item must be actionable, linked, and provide a way to signal completion.

## State

- Phase 1: active execution
- Task 3: "Finished" (owner: claude) — missing `task_verification` field (verification debt)
- Task 5: "Pending" (owner: human) — "Configure API keys" — action: add keys to `.env`
- Task 7: "Awaiting Verification" (owner: claude) — just completed, needs verification
- Task 11: "In Progress" (owner: both) — "Review auth design" — needs user feedback
- DEC-002: proposed, blocks tasks 8-9
- Blocking question in questions.md: "[BLOCKING] What caching solution to use?"

## Trace 09A: Verification debt action item

- **Path:** dashboard.md → Sub-Section Structure → Verification Debt

### Expected

```markdown
### Verification Debt

⛔ **Verification Debt: 2 tasks** — Project cannot complete until resolved

| Task | Title | Issue |
|------|-------|-------|
| 3 | Setup database | Missing verification |
| 7 | Auth middleware | Awaiting verification |

*Run `/work` to trigger verification for these tasks.*
```

### Pass criteria

- [ ] Debt table lists BOTH tasks (missing verification + awaiting verification)
- [ ] Clear instruction on what to do: "Run `/work`"
- [ ] User doesn't need to open task JSON files to understand the issue

### Fail indicators

- Debt shown as a count without listing which tasks
- No instruction on how to resolve
- User must read task JSON to understand what "missing verification" means

---

## Trace 09B: Decision pending action item

- **Path:** dashboard.md → Sub-Section Structure → Decisions

### Expected

```markdown
### Decisions

| ID | Decision | Question | Options Doc |
|----|----------|----------|-------------|
| D-002 | Caching strategy | Redis vs Memcached vs in-memory? | [decision-002.md](../support/decisions/decision-002-caching.md) |

*Open the decision doc, review options, and check your selection.*
```

### Pass criteria

- [ ] Link to decision doc is a relative path that works from dashboard.md location
- [ ] Question column summarizes the choice (user doesn't need to open doc just to know what it's about)
- [ ] Instruction tells user what to DO: open doc, review, check selection
- [ ] After checking selection in the doc, user knows to run `/work` again

### Fail indicators

- Decision ID shown without a link to the file
- Question column is empty or says "See decision doc"
- No instruction on how to signal completion (user doesn't know to run /work after selecting)

---

## Trace 09C: Human task action item

- **Path:** dashboard.md → Sub-Section Structure → Your Tasks

### Expected

```markdown
### Your Tasks

| ID | Task | Action | Link |
|----|------|--------|------|
| 5 | Configure API keys | Add keys to `.env` and check off | [.env.example](../../.env.example) |
| 11 | Review auth design | Read doc, leave feedback below | [auth-design.md](../support/decisions/decision-003.md) |

**Task 11 — Feedback:**
<!-- Write your feedback here, then run /work complete 11 -->

```

### Pass criteria

- [ ] Each task has an Action column that says what to DO (not just what the task IS)
- [ ] Each task has a Link column with a relative path to the relevant file
- [ ] Links use relative paths from `.claude/dashboard.md` to target files
- [ ] Task 11 has an inline feedback area with clear instructions
- [ ] Feedback area tells user what command to run after writing feedback
- [ ] Task 5 makes clear what "check off" means (how to signal completion)

### Fail indicators

- Tasks listed without links (user must find files in explorer)
- Action column restates the task title instead of describing the action
- Feedback area is missing for tasks that need it
- No instruction on how to signal task completion
- Links are absolute paths or don't work from dashboard location

---

## Trace 09D: Reviews action item

- **Path:** dashboard.md → Sub-Section Structure → Reviews

### Expected

```markdown
### Reviews

- [ ] **Resolve caching question** — [BLOCKING] What caching solution to use? → [questions.md](../support/questions/questions.md)
```

### Pass criteria

- [ ] Blocking question from questions.md appears as a review item
- [ ] Link goes to questions.md where the question lives
- [ ] Checkbox provides a way to track completion
- [ ] User understands this is blocking all work

### Fail indicators

- Blocking question not surfaced in dashboard at all
- Item says "blocking question exists" without stating the question
- No link to where the question can be answered

---

## Trace 09E: Cross-section consistency

- **Path:** All dashboard sections

### Check

Every item in Action Required should be traceable to its detail section:
- Verification debt tasks → appear in Tasks with correct status
- Pending decision → appears in Decisions with "proposed" status and link
- Human tasks → appear in Tasks with correct owner
- Blocking question → appears in Action Required → Reviews

### Pass criteria

- [ ] No item in Action Required references a task/decision that's missing from detail sections
- [ ] Blocking question appears in Action Required → Reviews with link to questions.md
- [ ] Tasks shows task 7 as "Awaiting Verification" (not hidden or mislabeled)

### Fail indicators

- Dashboard says "2 tasks have verification debt" but Tasks shows them as "Finished" without any indicator
- Decision appears as pending in Action Required but as "approved" in Decisions
- Blocking question blocks work but isn't surfaced in Action Required
