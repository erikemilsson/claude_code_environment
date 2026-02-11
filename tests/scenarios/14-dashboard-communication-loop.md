# Scenario 14: Dashboard Communication Loop

Verify that the dashboard functions as a complete communication loop: Claude surfaces what it needs → User acts → Claude picks up the result. Tests that the loop doesn't break (lost feedback, missed signals, stale state).

## Context

The user runs Claude Code CLI in one pane and has `dashboard.md` open in the other. Their workflow is: check dashboard → do what it says → run `/work` → check dashboard again. If any step in this loop fails silently, the user loses trust in the system.

---

## Trace 14A: The complete attention-to-resolution loop

### Loop steps

```
1. Claude works → updates task JSON → regenerates dashboard
2. Dashboard shows item in "Action Required"
3. User reads dashboard, sees item
4. User follows link, performs action (edits file, writes feedback, checks checkbox)
5. User runs /work (or /work complete)
6. /work reads updated files → detects resolution → removes item from dashboard
7. Dashboard regenerates → item gone → new items (if any) appear
```

### State for testing

- Task 7: "Awaiting Verification" → verify-agent will flag it
- Claude runs → verify-agent finds issues → creates fix tasks → regenerates dashboard

### Expected sequence

1. **Before:** Dashboard shows Task 7 under "Claude → In Progress"
2. **After verification:** Dashboard updates:
   - Task 7 → "In Progress" (failed verification, needs fixes)
   - New fix task 7a appears under "Claude → Ready to Start"
   - Verification Debt section shows Task 7
3. **After fix:** Claude implements fix → re-verifies → passes
4. **After pass:** Dashboard updates:
   - Task 7 → "Finished" (verification passed)
   - Fix task 7a → "Finished"
   - Verification Debt cleared
   - Task 7 appears in Progress "this week" activity

### Pass criteria

- [ ] Each state transition produces a dashboard regeneration
- [ ] Dashboard accurately reflects the current state at every step
- [ ] No "phantom" items remain from previous states
- [ ] The user can follow the entire lifecycle from dashboard alone

### Fail indicators

- Dashboard shows Task 7 as "Finished" while verification is still running
- Fix task appears in dashboard before its JSON file exists
- Verification debt persists after task passes verification
- Dashboard requires manual refresh (user must re-run /work just to see current state)

---

## Trace 14B: Feedback written in dashboard survives until read

### Scenario

User writes feedback for Task 11 in the dashboard inline area:
```markdown
**Task 11 — Feedback:**
Use OAuth2 instead of JWT. The client requires SSO support.
<!-- Write your feedback here, then run /work complete 11 -->
```

Then BEFORE the user runs `/work complete`, something triggers a dashboard regeneration (e.g., a parallel agent finishes, or the user runs `/work` to check on another task).

### Risk

The "Your Tasks" section is rebuilt from source data. The inline feedback area is part of that section. On regeneration, the feedback is overwritten with a fresh empty template.

### Expected behavior (current spec)

dashboard.md states:
- Action Required sub-sections are rebuilt from source data
- Only the Notes section (between `<!-- USER SECTION -->` markers) is preserved
- Inline feedback areas in "Your Tasks" are NOT in the user section

**This means feedback IS lost on regeneration.** This is a design gap.

### Mitigation options

1. **Read inline feedback during `/work complete`** — `/work complete` reads the dashboard for inline feedback and captures it in task JSON before regenerating
2. **Store feedback in a durable location** — Link to a file where feedback persists (e.g., task-specific feedback file or a section in questions.md)
3. **Treat feedback areas as user-preserved** — Add feedback area markers similar to `<!-- USER SECTION -->`

### Pass criteria

- [ ] If feedback areas exist in the dashboard, there's a defined mechanism to prevent data loss
- [ ] `/work complete` captures inline feedback before dashboard regeneration
- [ ] OR: feedback is directed to a durable location (file linked from dashboard)
- [ ] User is warned if feedback might be lost (or it simply can't be lost)

### Fail indicators

- User writes feedback, dashboard regenerates from another trigger, feedback silently disappears
- No mechanism exists to capture inline feedback before regeneration
- User discovers their feedback is gone and has to rewrite it
- The system relies on the user always running `/work complete` before any other dashboard regeneration

---

## Trace 14C: Decision resolution detection

### Scenario

User opens decision doc DEC-002, reviews options, checks a box:
```markdown
## Select an Option

- [ ] Option A: Redis
- [x] Option B: Memcached
- [ ] Option C: In-memory
```

Then runs `/work`.

### Expected detection sequence

1. `/work` Step 2b reads decision-002.md
2. Detects checked box (`- [x]`) in "Select an Option" section
3. Updates decision status to "approved" (or keeps "proposed" and marks as selected?)
4. Checks if inflection_point → routes accordingly
5. Unblocks dependent tasks
6. Regenerates dashboard → DEC-002 moves from Action Required → Decisions sub-section to the Decisions section with selected option shown

### Gap analysis

**Who updates the decision status field?**
- The user checks a box in the markdown
- Does `/work` update the frontmatter `status: proposed` → `status: approved`?
- Or does it just use the checked box as the resolution signal?

**Current behavior (from work.md Step 2b):**
- Checks "if decision has a checked box in '## Select an Option'"
- If checked → runs post-decision check (Step 2b-post)
- But doesn't explicitly state that frontmatter status is updated

### Pass criteria

- [ ] Checking a box in the decision doc is sufficient to unblock dependent tasks
- [ ] Next `/work` run detects the change and acts on it
- [ ] Dashboard reflects the resolution (selected option shown in Decisions)
- [ ] If decision is inflection point, `/work` pauses and directs to `/iterate`
- [ ] Decision frontmatter status is updated to reflect the resolution

### Fail indicators

- User checks box but `/work` doesn't detect it (checkbox parsing failure)
- Decision shown as resolved but dependent tasks still blocked
- Dashboard still shows decision as "pending" after user selected an option
- Frontmatter status stays "proposed" permanently (ambiguous — is it resolved or not?)

---

## Trace 14D: Stale dashboard detection after external changes

### Scenario

User manually edits a task JSON file (changes status from "Pending" to "In Progress") without running `/work`. Then opens the dashboard.

### Expected detection

1. Dashboard META block has `task_hash` from last regeneration
2. The manual edit changed a task status → hash is now different
3. Next `/work` run detects hash mismatch → regenerates dashboard
4. Dashboard now reflects the manual edit

### But what if the user ONLY looks at the dashboard (doesn't run /work)?

- The dashboard is stale — it shows old data
- The header line says: *"May be stale if tasks were modified outside `/work`."*
- But the user might not notice or might trust the displayed data

### Pass criteria

- [ ] Dashboard META block hash enables staleness detection
- [ ] `/work` Step 1a catches the mismatch and regenerates
- [ ] Stale warning in header line is visible and clear
- [ ] After regeneration, dashboard matches actual file state

### Fail indicators

- Dashboard shows stale data and user doesn't notice
- Stale warning is too subtle (part of the boilerplate the user learned to ignore)
- `/work` doesn't regenerate even though hash mismatches
- Manual edits to task JSON are lost on next dashboard regeneration (dashboard is NOT source of truth, tasks are)

---

## Trace 14E: Multi-session feedback continuity

### Scenario

Session 1: User writes feedback for Task 11 in a durable location (e.g., dashboard notes section, questions.md, or a linked feedback file).
Session ends.
Session 2: User runs `/work`. Claude should pick up the feedback and incorporate it.

### Expected behavior

- Feedback persists across sessions (it's in a file, not conversation memory)
- `/work` or `/work complete` reads the feedback from its durable location
- Claude incorporates feedback when working on or completing the task
- Feedback is captured in task JSON notes for historical record

### Pass criteria

- [ ] Feedback mechanism is file-based (survives session boundaries)
- [ ] `/work` reads feedback locations as part of its context gathering
- [ ] Feedback written in Session 1 is available in Session 2
- [ ] No conversation-state dependency for feedback (everything in files)

### Fail indicators

- Feedback relies on conversation context (lost between sessions)
- `/work` in Session 2 doesn't read the feedback file
- User has to re-state their feedback in the new session
- Feedback exists in a file but Claude doesn't know to look there
