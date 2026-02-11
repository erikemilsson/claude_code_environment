# Dashboard

<!-- DASHBOARD META
generated: 2026-01-28T14:30:00Z
task_hash: sha256:a3f8c91d2e7b4056890cd1ef23456789abcdef0123456789abcdef0123456789
task_count: 12
verification_debt: 1
drift_deferrals: 0
-->

<!-- FORMAT GUIDE — kept in every regenerated dashboard (invisible to users, guides Claude)

  **Action Item Contract:**
  Every item in "Action Required" must be:
  1. Actionable — the user can see what to do without guessing
  2. Linked — if the action involves a file, include a relative path link
  3. Completable — include a checkbox, command, or clear completion signal
  4. Contextual — if feedback is needed, provide a feedback area or link

  **Review Item Derivation:**
  Review items are derived, not stored. During regeneration:
  1. Scan for unresolved items — out_of_spec without approval, draft/proposed decisions, blocking questions
  2. Populate Reviews sub-section from current data
  3. Never carry forward stale entries — resolved items disappear on next regeneration
  4. No dangling references — every item must link to a concrete file

  **Section Display Rules:**
  - Action Required sub-sections: only render when they have content (omit empty categories entirely)
  - Timeline sub-section in Progress: only render when tasks have due_date or external_dependency.expected_date
  - Phase table in Progress: always show ALL phases (including blocked/future)
  - Critical path owners: ❗ (human), 🤖 (Claude), 👥 (both)
  - Critical path >5 steps: show first 3 + "... N more → Done"
  - "This week" line: omit when all counts are zero
  - Tasks grouped by phase with per-phase progress lines
  - Decisions: decided → show selected option name; pending → link to doc in Selected column
  - Out-of-spec tasks: prefix title with ⚠️
  - Footer: healthy = spec aligned tooltip; issues = ⚠️ with counts

  **Domain Agnosticism:**
  This format works for any project type — software, research, procurement, renovation, event planning.
  Use language appropriate to the project domain. No code-specific assumptions are built in.
-->

> **This is a format example** using a fictional renovation project. It will be replaced with your actual project data when you run `/work`.

**Community Center Renovation** · Execute · Started 2026-01-15

**42% complete** — 12 tasks · 2 decisions

---

## 🚨 Action Required

<!-- ACTION REQUIRED: Only show sub-sections that have content. Omit empty categories entirely.
     Sub-sections in order: Verification Debt, Decisions, Your Tasks, Reviews -->

<!-- VERIFICATION DEBT: Show when any task is "Awaiting Verification", "Finished" without task_verification,
     or task_verification.result == "fail". Exclude out-of-spec tasks. -->
### Verification Debt

⛔ **Verification debt: 1 task** — must resolve before completion

| Task | Title | Issue |
|------|-------|-------|
| 6 | Order materials | Awaiting verification |

*Run `/work` to trigger verification.*

<!-- DECISIONS: Show when any decision-*.md has no checked box in "Select an Option". -->
### Decisions

| Decision | Question | Doc |
|----------|----------|-----|
| DEC-002 | Hardwood vs luxury vinyl for main hall? | [decision-002.md](support/decisions/decision-002-flooring.md) |

*Open the doc, review options, check your selection, then run `/work`.*

<!-- YOUR TASKS: Show when human-owned tasks have status "Pending" and all deps satisfied.
     Every row must say what to DO and link to where. -->
### Your Tasks

| Task | What To Do | Where |
|------|------------|-------|
| 8 | Obtain building permit from city hall | [permit-application.pdf](../permits/permit-application.pdf) |
| 10 | Schedule electrical inspection with city inspector | [inspector-contacts.md](support/workspace/inspector-contacts.md) |

---

## 📊 Progress

<!-- PROGRESS: Phase table always shows ALL phases. Status values: Complete, Active, Blocked (reason). -->

| Phase | Done | Total | Status |
|-------|------|-------|--------|
| 1 — Planning | 4 | 4 | Complete |
| 2 — Construction | 2 | 5 | Active |
| 3 — Finishing | 0 | 3 | Blocked (DEC-002) |

<!-- TIMELINE: Only show when tasks have due_date or external_dependency.expected_date.
     Sorted chronologically. Overdue: strikethrough date + ⚠️ OVERDUE prefix.
     External dependencies shown with contact info. Human tasks marked with ❗. -->
### Timeline

| Date | Item | Status | Notes |
|------|------|--------|-------|
| ~~2026-01-28~~ | ⚠️ OVERDUE: Task 6 — Order materials | Awaiting Verification | Vendor: Acme Surfaces |
| 2026-02-05 | Task 9 — Rough plumbing | In Progress | |
| 2026-02-10 | Task 10 — Electrical inspection | Pending | ❗ Human task |
| 2026-02-15 | External: Flooring delivery | Waiting | Contact: Bob at FloorCo |

**Critical path:** ❗ Resolve DEC-002 → 🤖 Install flooring → 🤖 Final walkthrough → Done *(3 steps)*

**This week:** 1 completed · 1 started · 0 created

---

## 📋 Tasks

<!-- TASKS: Group by phase. Per-phase progress line with blocking reason if applicable.
     Columns: ID | Title | Status | Diff | Owner | Deps
     Out-of-spec tasks: prefix title with ⚠️. Summary after all phases. -->

### Phase 1: Planning

| ID | Title | Status | Diff | Owner | Deps |
|----|-------|--------|------|-------|------|
| 1 | Site assessment and measurements | Finished | 3 | claude | — |
| 2 | Architectural drawings | Finished | 4 | claude | 1 |
| 3 | Budget estimation | Finished | 3 | claude | 1 |
| 4 | Contractor selection research | Finished | 2 | claude | — |

*Phase 1: 4/4 complete (100%)*

### Phase 2: Construction

| ID | Title | Status | Diff | Owner | Deps |
|----|-------|--------|------|-------|------|
| 5 | Demolition plan | Finished | 3 | claude | 2 |
| 6 | Order materials | Awaiting Verification | 4 | claude | 3 |
| 7 | Structural reinforcement | Finished | 5 | claude | 5 |
| 8 | Obtain building permit | Pending | 2 | human | 2 |
| 9 | Rough plumbing | In Progress | 4 | claude | 5 |

*Phase 2: 2/5 complete (40%) — 1 awaiting verification, 1 human task pending*

### Phase 3: Finishing

| ID | Title | Status | Diff | Owner | Deps |
|----|-------|--------|------|-------|------|
| 10 | Electrical inspection | Pending | 2 | human | 9, DEC-002 |
| 11 | Install flooring | Pending | 4 | claude | DEC-002 |
| 12 | Final walkthrough and punch list | Pending | 3 | both | 10, 11 |

*Phase 3: 0/3 complete (0%) — blocked by DEC-002*

*5/12 tasks complete (42%)*

---

## 📋 Decisions

<!-- DECISIONS TABLE: Decided → show selected option name. Pending → link to decision doc. -->

| ID | Decision | Status | Selected |
|----|----------|--------|----------|
| DEC-001 | Contractor selection | Decided | BuildRight Construction |
| DEC-002 | Main hall flooring | Pending | [Review options](support/decisions/decision-002-flooring.md) |

---

## 💡 Notes

<!-- USER SECTION -->

[Your notes here — ideas, questions, reminders]

<!-- END USER SECTION -->

---
*2026-01-28 14:30 UTC · 12 tasks · [Spec aligned](# "0 drift deferrals, 1 verification debt")*
