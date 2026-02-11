# Project Structure Patterns Test Checklist

Verify that phases and decisions work correctly. Run on a fresh project.

---

## Part 1: Phases

### Setup

1. [ ] Create a spec with two phases:

   ```markdown
   ## Phase 1: Data Pipeline

   - Ingest CSV data
   - Validate and store in database

   ## Phase 2: Visualization

   - Build chart components
   - Create dashboard layout
   ```

2. [ ] Run `/work` to decompose into tasks

### Verify Phase Behavior

3. [ ] Check tasks have `phase` field in JSON files (e.g., `"phase": "1"` and `"phase": "2"`)

4. [ ] Dashboard groups tasks under `### Phase 1: Data Pipeline` and `### Phase 2: Data Pipeline` headers

5. [ ] Dashboard shows phase breakdown in Quick Status:
   ```
   | Phase | Done | Total | Status |
   ```

6. [ ] Run `/work` — should only dispatch Phase 1 tasks. Phase 2 tasks should show as blocked.

7. [ ] Complete all Phase 1 tasks — `/work` should detect phase transition and make Phase 2 tasks eligible

---

## Part 2: Decisions

### Create a Decision

8. [ ] Create a decision record at `.claude/support/decisions/decision-001-database-choice.md` using the template from `decision-template.md`

9. [ ] Verify frontmatter includes `inflection_point: false` and `blocks: []`

10. [ ] Add options to the decision doc (e.g., PostgreSQL, SQLite, MongoDB)

### Block Tasks on Decision

11. [ ] Create a task with `"decision_dependencies": ["DEC-001"]`

12. [ ] Run `/work` — should show:
    ```
    📋 Decision DEC-001 (Database Choice) blocks N task(s).
    Open the decision doc to make your selection, then run /work again.
    ```

### Resolve Decision (Pick-and-Go)

13. [ ] Open decision doc, check one box in `## Select an Option`

14. [ ] Run `/work` — should detect resolution, unblock tasks, and continue

### Dashboard Decision Format

15. [ ] Dashboard `## 📋 All Decisions` table uses format:
    ```
    | ID | Decision | Status | Selected |
    ```

16. [ ] Decided entry shows selected option name (e.g., "PostgreSQL")

17. [ ] Pending entry links to the decision doc

---

## Part 3: Inflection Points

### Setup

18. [ ] Create a decision with `inflection_point: true` in frontmatter

19. [ ] Create tasks with `decision_dependencies` pointing to this decision

### Test Inflection Point Behavior

20. [ ] Resolve the decision (check a box in Select an Option)

21. [ ] Run `/work` — should **pause** and suggest running `/iterate`:
    ```
    ⚠️ Decision DEC-002 was an inflection point.
    Run /iterate to review affected spec sections, then /work to continue.
    ```

22. [ ] Run `/iterate` — should auto-detect the resolved inflection point and suggest spec adjustments

23. [ ] After spec review, run `/work` — should now proceed normally

---

## Part 4: Checkbox Selection Mechanism

24. [ ] Verify `/work` reads checked boxes from `## Select an Option` to detect resolution

25. [ ] Verify only one box can be checked (if multiple are checked, first checked is used)

26. [ ] Verify unchecking all boxes returns decision to unresolved state

---

## Cleanup

After testing, remove:
- Test spec
- Test decision records
- Test task files
- Regenerate dashboard
