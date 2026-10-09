# Phase and Decision Gates

Procedure for checking phase boundaries, decision dependencies, and late decision cross-references. Run as `/work` Step 2b.

---

## Phase Check

Determine the current active phase by walking phases in ascending order:

```
1. Group tasks by `phase` field
2. Sort phases numerically (ascending)

   Gate state lives in the sidecar `dashboard-state.json` `phase_gates` object,
   keyed by transition (e.g. "1→2"); the dashboard is read-only HTML, so the
   user approves via CLI (not an in-file checkbox) — DEC-024.

   FOR each phase P (ascending):
     IF all tasks in phase P are "Finished":
       IF tasks exist in a higher phase (next_phase exists):
         gate = phase_gates["{P}→{next_phase}"]   (absent → treat as new)
         1. IF gate.status == "approved":
              → Already approved. Continue to next phase.
         2. Evaluate auto-conditions (all Phase P tasks Finished; all their
            per-task verifications passed; plus any spec-defined gate criteria).
            Unratified agent decisions (status `recorded`) are never a
            condition: they don't block a gate.
         3. IF auto-conditions NOT all met:
              → Set gate.status = "active"; surface the gate in the dashboard's
                "Needs you" card (the script renders the gate row once the phase is Complete,
                and any verification debt; record unmet spec-defined criteria as an
                `augment_rows` entry, and prune that entry on approval).
              → Log: "Phase gate {P}→{next_phase}: {N} of {M} conditions met."
              → STOP — do not dispatch any tasks
         4. IF auto-conditions met but the user has not yet approved:
              → Set gate.status = "active"; surface in "Needs you": the
                conditions (all met) + the approval prompt.
              → Prompt via CLI: "Phase {P} complete — approve transition to
                Phase {next_phase}? [Y] Approve  [N] Hold". STOP until approved.
                When any decision record has status `recorded`, the prompt adds
                one line: "{N} agent decision(s) not yet ratified: {DEC ids} —
                /work ratify all (does not block this gate)".
         5. ON user approval (CLI reply Y):
              → Set gate.status = "approved" in the sidecar (orchestrator write).
              → Log: "Phase {P} → {next_phase} approved"
              → Learning capture (lightweight, skippable):
                  "Phase {P} complete. Any patterns or learnings to capture? [L] Share  [S] Skip"
                  If [L]: append to .claude/support/learnings/phase-learnings.md
              → Execute Version Transition Procedure (see iterate.md § "Version Transition Procedure")
              → Suggest running /iterate to flesh out Phase {next_phase} sections
              → Continue to next phase
       ELSE (final phase, all tasks Finished):
         → Fall through to Step 3 routing (phase-level verification → completion)
     ELSE (phase P has non-Finished tasks):
       → This is the active phase

   For target task(s):
   IF task.phase > active_phase AND task.cross_phase != true:
     "Task {id} is in Phase {task.phase}, but Phase {active_phase} is still in progress.
      {N} tasks remaining in Phase {active_phase}."
     → Skip this task, work on active-phase tasks instead

   IF task.phase > active_phase AND task.cross_phase == true:
     → Cross-phase task — bypass gate. Proceed to task-level dependency/decision checks.
     → Log: "Task {id} is cross-phase (Phase {task.phase}) — eligible despite active Phase {active_phase}."
```

### Cross-Phase Tasks

Tasks with `cross_phase: true` (see `task-schema.md`) are exempt from the phase gate on eligibility checks only. They still belong to their declared phase for verification and dashboard rendering. Typical use: long-lead human work (recruitment, procurement, approvals) that must start before the prior phase is fully done.

---

## Decision Dependency Check

For target task(s), check `decision_dependencies`:

```
1. Read each referenced decision record
2. Check if decision has a checked box in "## Select an Option"

   IF frontmatter status is "recorded" (agent-recorded; it has no
   "## Select an Option" section), or "approved"/"implemented" with no checked box:
     → Resolved. It does not block; ratification (/work ratify) is separate.

   IF frontmatter status is "superseded" or "partially_superseded" (checked box or not):
     → Resolved. It does not block. When the record has a `superseded_by` key and
       status "superseded", print one line per decision per run and continue:
       "ℹ {DEC-NNN} was superseded by {superseded_by}; Task(s) {ids} still list {DEC-NNN} in decision_dependencies (remove it, or depend on {superseded_by})."

   IF any decision is unresolved (record missing, or status "draft"/"proposed"
   with no checked box):
     📋 Decision {DEC-NNN}: "{title}" is unresolved and blocks {N} task(s).
       [R] Research options (spawns research-agent; its findings populate the decision record — see `.claude/commands/research.md`)
       [S] Skip (you'll research manually — open the decision doc and check your selection, then run /work)

     IF user selects [R]:
       → No record file yet: first create it via research.md Step 1 (topic branch), then Steps 2-4 as below
       → Gather context (decision record, spec, related tasks/decisions)
       → Spawn research-agent (see research.md Steps 2-4)
       → After research completes, re-present the decision for user selection
       → If user selects via checkbox, fall through to the auto-update logic below

     IF user selects [S]:
       → Skip this decision for now
       → Continue checking remaining decisions
       → Non-blocked tasks still dispatch normally

   IF decision has a checked box AND frontmatter status is "draft"/"proposed":
     → AUTO-UPDATE FRONTMATTER:
       1. Extract selected option name from the checked line (text after `[x] `)
       2. Update frontmatter fields:
          - status: approved
          - decided: [today's date, YYYY-MM-DD]
          - ratified: [today's date] — only when the record has
            `decided_by: implement-agent` or `orchestrator` (a reconsidered agent
            decision: the tick is the user's confirmation; `decided_by` stays)
       3. Log: "Decision {id} resolved → status updated to 'approved' (selected: {option_name})"
     → Run post-decision check (see below)

   IF decision has a checked box AND frontmatter status is "recorded"/"approved"/"implemented":
     → Already processed (a box on a "recorded" record is not a ratification; only /work ratify sets "approved"). Run post-decision check if dependent tasks are still blocked.
```

---

## Late Decision Check (Reverse Cross-Reference)

Catches decisions that reference tasks which don't know about the decision yet:

```
For each decision-*.md file, read `related.tasks` array:
  (Skip records with `decided_by: implement-agent` or `orchestrator`, whatever
   their status: their `related.tasks` names the task or tasks that produced
   them and, when a reconsider led to one, a follow-up task appended last
   (§ "Post-Decision Check").)
  For each referenced task ID:
    Read task JSON
    Check if decision ID is in task's `decision_dependencies`

    IF NOT (task doesn't know about this decision):
      Check task status:
      ├─ "Finished" or "In Progress":
      │    ⚠️ Decision {id} ({title}) was created after task {task_id} began.
      │
      │    Status:
      │    - Task {id}: "{status}" — {impact description}
      │
      │    Options:
      │    [1] Add {DEC-ID} as dependency + pause/flag affected tasks
      │    [2] Proceed as-is (risk: rework if decision contradicts implementation)
      │    [3] Review affected task(s) before deciding
      │
      │    IF user picks [1]:
      │      - Add decision ID to task's decision_dependencies
      │      - "In Progress" tasks → set to "Pending" (now blocked)
      │      - "Finished" tasks → add note: "Review after {DEC-ID} resolved — may need rework"
      │      - Regenerate dashboard
      │
      └─ "Pending":
           Report and ask before adding decision_dependencies (`related.tasks` can also
           list the task that produced the decision, which must not block on its own output)

    IF YES: task already tracks this decision → no issue
```

---

## Post-Decision Check

**Reconsidered agent decision (both callers — `/work` Step 2b and `/iterate` Step 1a — with or without dependent tasks).** When the record just approved by a tick carries `decided_by: implement-agent` or `orchestrator` and the selection differs from what its related task built (the `**Selected:**` choice the agent wrote; note it before repopulating `## Decision`), offer to create a new task for the change. When that task is created, append its id to the record's frontmatter `related.tasks` (after the ids already there): on a reconsidered record `/review` reads the last id as the follow-up. The Finished task is not reset. The new task follows the creation contract (`task-schema.md § "Drift Prevention Fields"`): run `fingerprint.py --provenance` on the related task's `spec_section` for current hashes (don't copy that task's fingerprints, which may predate a spec edit); if the related task is `spec_unmapped`, so is the new one.

A `superseded` or `partially_superseded` record gets no post-decision check; a task that was set to Blocked only for it is unblocked.

When `/work` detects a resolved decision (status `recorded`, `approved` or `implemented`) that has dependent tasks:

```
1. Read the decision record
2. Check `inflection_point` field in frontmatter

IF inflection_point: false (or absent):
  → Pick-and-go: unblock dependent tasks, continue to Step 2c
  → Log: "Decision {id} resolved → {N} tasks unblocked"

IF inflection_point: true:
  → Run chosen-option no-op scan (Step 2a.1 below) BEFORE checking `spec_revised`
  │
  │  Step 2a.1: Read the chosen option's `### Option X: <name>` block under
  │             `## Option Details`. Scan the first paragraph (lines until the
  │             first blank line) for these case-insensitive markers:
  │               - "no spec amendment"
  │               - "no spec impact"
  │               - "no spec change"
  │               - "no-op" (with word boundary, to exclude e.g., "no-operation")
  │
  │  IF any marker is found in the same paragraph AND no contradicting phrase
  │  ("will need spec", "requires spec", "spec change in v2", etc.) appears in
  │  the same paragraph:
  │    → No-op option chosen — no spec impact. Skip the /iterate suggestion.
  │    → Unblock dependent tasks.
  │    → Log: "Decision {id} resolved (inflection point, no-op option chosen) → {N} tasks unblocked"
  │    → Continue to Step 2c
  │
  │  IF no marker found OR a contradicting phrase exists in same paragraph:
  │    → Proceed to spec_revised check below
  │
  → Check `spec_revised` field in frontmatter
  │
  │  IF spec_revised: true
  │    → Spec already updated for this decision. Unblock dependent tasks.
  │    → Log: "Decision {id} (inflection point) resolved and spec revised → {N} tasks unblocked"
  │    → Continue to Step 2c
  │
  │  IF spec_revised is false OR absent:
  │    → Pause execution
  │    │
  │    │  ⚠️ Decision {id} ({title}) was an inflection point.
  │    │  The outcome may change what needs to be built.
  │    │
  │    │  Run `/iterate` to review affected spec sections,
  │    │  then `/work` to continue.
  │    │
  │    └─ Do NOT proceed. Wait for user to run `/iterate`.
```

**No-op scan rationale (FB-078):** `inflection_point` declares "the option space was spec-shaping at creation"; the chosen option may still turn out to be a close/defer/no-op selection with no spec consequences. The 4-marker scan catches the common authoring pattern ("Drop this question — no spec impact") without requiring a schema change. The contradicting-phrase guard prevents false-positives on "no spec impact NOW but v2 will need it" prose. If this heuristic accumulates ≥3 false-negatives across projects within 6 months, escalate to Option 2 (per-option `spec_impact: true | false | unclear` schema field) — see `template-maintenance/feedback.md § FB-078`.

**Session resilience:** The `spec_revised` field is the durable checkpoint. Across session boundaries, `/work` re-reads the decision record and checks this field — no conversation state needed.

---

## Early-Exit Conditions

To avoid unnecessary work, check these before running the full procedure:

```
IF no tasks have a `phase` field → skip Phase Check entirely
IF no decision-*.md files exist → skip Decision Check and Late Decision Check
IF both skipped → proceed directly to Step 2c
```
