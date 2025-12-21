# Command: Resolve Ambiguities (Phase 0 - Step 2)

## Purpose
Present the next batch of unresolved ambiguities (maximum 5) for user resolution and document decisions.

## Prerequisites
- `initialize-project.md` has been run
- `.claude/reference/ambiguity-report.md` exists

## Phase 0 Progress

**BEFORE STARTING**: Display current progress from `.claude/tasks/_phase-0-status.md`

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 0 PROGRESS - Step 2 of 4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Initialize Project        ✅  (Completed)
Step 2: Resolve Ambiguities       🔄  (Est. 30-60 min)
Step 3: Generate Artifacts        ⬜  (Est. 15-20 min)
Step 4: Extract Queries           ⬜  (Est. 10-15 min)

Current: Step 2 - Resolving batch [X] of [Y]
Ambiguities resolved: [N] of [Total]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Process

### 1. Load Ambiguity Report
Read `.claude/reference/ambiguity-report.md` and identify all ambiguities with status "⏳ Pending Resolution".

### 2. Determine Next Batch
Select up to 5 ambiguities with "⏳ Pending Resolution" status.
Order by:
1. Risk level (High → Medium → Low)
2. Impact scope (affects multiple queries first)
3. Sequential order in document

### 3. Present Batch to User
Format presentation clearly:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AMBIGUITY RESOLUTION - Batch [X] of [Total Batches]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ambiguities Remaining: [Count]
Progress: [Resolved]/[Total] resolved

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Ambiguity [ID]: [Category]

**Source:** [Document], [Section]

**Context:**
> [Exact quote from document]

**Issue:**
[Clear description of what's ambiguous]

**Options:**
A) [Interpretation 1 - with rationale]
B) [Interpretation 2 - with rationale]
C) [Interpretation 3 - if applicable]

**Impact:** Affects [which queries/calculations]
**Risk Level:** [High/Medium/Low]

**Your Decision:** [Leave blank for user to fill]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Repeat for up to 5 ambiguities]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Instructions:**
Please respond with your decisions in this format:

1. [A/B/C] - [Optional: Brief rationale or additional notes]
2. [A/B/C] - [Optional: Brief rationale]
...

If you need more context or have questions about any ambiguity, ask before deciding.
```

### 4. Wait for User Response
User provides decisions for the batch.

### 5. Document Decisions
For each resolved ambiguity:

**Update ambiguity-report.md:**
- Change status from "⏳ Pending Resolution" to "✅ Resolved"
- Add resolution details:
  ```markdown
  **Resolution:** Option [A/B/C] selected
  **Rationale:** [User's rationale if provided]
  **Resolved By:** User
  **Resolved Date:** [Date]
  ```

**Update/Create assumptions.md:**
Append to `.claude/context/assumptions.md`:

```markdown
## Assumption [ID]: [Brief Title]

**Source:** [Document], [Section]

**Original Text:**
> [Exact quote]

**Ambiguity:**
[What was unclear]

**Decision:**
[Selected interpretation - Option A/B/C details]

**Rationale:**
[User's rationale or standard reference]

**Impact:**
- Affects: [List of queries/calculations]
- Implementation: [How this will be coded]

**Date:** [Date]
**Status:** Approved

---
```

### 6. Update Phase 0 Status
Update `.claude/tasks/_phase-0-status.md`:
- Update Step 2 progress: "[Resolved] of [Total] ambiguities resolved"
- Update time elapsed
- If all complete: Change Step 2 status from 🔄 to ✅, Step 3 to 🔄

### 7. Check Completion
**If more ambiguities remain:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Batch [X] Resolved
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROGRESS:
Step 1: Initialize Project        ✅  (Completed)
Step 2: Resolve Ambiguities       🔄  (In progress)
Step 3: Generate Artifacts        ⬜
Step 4: Extract Queries           ⬜

Ambiguities: [Resolved]/[Total] resolved ([Percentage]%)
Remaining batches: [Count]
Estimated time: [Count*10] minutes

NEXT STEP:
Run /resolve-ambiguities again for next batch
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If all ambiguities resolved:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Phase 0 - Step 2 Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROGRESS:
Step 1: Initialize Project        ✅  (Completed)
Step 2: Resolve Ambiguities       ✅  (Completed in ~[X] min)
Step 3: Generate Artifacts        🔄  NEXT
Step 4: Extract Queries           ⬜

RESULTS:
Total ambiguities resolved: [Count]
Batches completed: [Count]

All decisions documented in:
- .claude/context/assumptions.md
- .claude/reference/ambiguity-report.md (all marked ✅)

NEXT STEP:
Run /generate-artifacts
This will create glossary, data contracts, query manifest, and tasks.
Estimated time: 15-20 minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Output Files
- `.claude/context/assumptions.md` - Updated with new decisions
- `.claude/reference/ambiguity-report.md` - Updated statuses
- `.claude/tasks/_phase-0-status.md` - Updated progress

## Handling Edge Cases

### User Asks Questions
If user asks for clarification before deciding:
- Provide additional context from source documents
- Explain implications of each option
- Suggest which option aligns with common practices
- DO NOT make the decision for them

### User Proposes New Interpretation
If user suggests Option D (not in original list):
- Acknowledge the new interpretation
- Evaluate feasibility and implications
- Add to ambiguity report as Option D
- Document this in assumptions.md

### User Wants to Skip/Revisit
If user wants to skip an ambiguity:
- Mark as "⏸️ Deferred"
- Continue with others in batch
- Will be presented in a future batch

### Conflicting Decisions
If a decision conflicts with a previous one:
- Flag the conflict immediately
- Present both decisions for review
- Ask user to resolve the conflict before continuing

## Quality Checks

Before documenting each decision:
- Verify decision is clear and unambiguous
- Check for consistency with prior decisions
- Ensure rationale is documented (even if minimal)
- Confirm impact is understood

## Notes
- **Maximum 5 ambiguities per batch** - prevents overwhelm
- **Run multiple times** - until all resolved
- **Interactive process** - user makes all decisions
- **Full documentation** - every decision is traceable
- **No assumptions by Claude** - all interpretations by user
