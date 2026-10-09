# v5.14.4: decision-status gaps (FB-127 ah, part of ag)

**Status:** built and reviewed; release bookkeeping done; awaiting the user's OK to commit, tag and push.

## Measured (2026-10-09, 9 downstream projects, 232 decision records, read-only)

- `/health-check` check 6 (decision → task): 77 of 78 task links on agent-decided records are mismatches (styler 45, PortfolioWebsite 13, OEMMatInsightBI 11, conversation_opener 8, plus 4 links to missing tasks in OEMMatInsightBI). By design those tasks never carry the decision in `decision_dependencies`.
- `superseded_by` / `superseded_date`: 13 styler records use them; `/audit-coherence` reads them; no shipped file defined them.
- Superseded records: 16 (all styler), 10 with dependent tasks, 0 with an open dependent task; 7 without a ticked box.
- `partially_superseded`: 0 records. `decided_by: orchestrator`: 0. Agent-decided `implemented` without anchors: 0.
- Reconsidered-signature records (agent-decided, ticked, `ratified` == `decided`): 3 in PortfolioWebsite, all with anchors, so `/review`'s no-anchors rule doesn't reach them. No record has been reconsidered anywhere.
- Legacy agent records with several ids in `related.tasks`: 23; none reworked.
- The renderer already treats only `draft` / `proposed` as unresolved (`UNRESOLVED_DECISION`), so both superseded statuses are resolved there.

## Build contract (docs and command text only)

1. `health-check.md` check 6: skip agent-decided records in the decision → task direction.
2. `decisions.md` and `health-check.md` field list: define optional `superseded_by`, `superseded_date`; the superseding procedure adds them.
3. `health-check.md` check 7: also match `decided_by: orchestrator`.
4. `audit-coherence.md` superseded lens: a `partially_superseded` record is checked only for its replaced part; no spec finding when the record doesn't say which part.
5. `phase-decision-gates.md` Decision Dependency Check: `superseded` and `partially_superseded` are resolved and never block; for `superseded` with `superseded_by`, `/work` prints one line naming the replacing record.
6. `dashboard-regeneration.md` "Selected column" sentence and `extension-patterns.md` "Dashboard Integration" rewritten to match the HTML dashboard.

## Decisions (user, 2026-10-09)

1. Ship items 1–6; hold the reconsidered-record holes of (ag) and the legacy multi-task rework match with the sentinel cluster until a harvest shows a real reconsider; drop the anchors-warning exemption (`/review` already says to add anchors when marking a record `implemented`).
2. A task depending on a superseded decision is not blocked; one line names the replacing record when `superseded_by` is set; `partially_superseded` is treated like `approved`.
3. Built by the main session, one independent read-only reviewer, ships as v5.14.4 with a 9-project sync.

## Amendments

1. Review (one independent read-only pass; renderer read, not run): no blocker, the gate branches are disjoint by status and `work.md`, `status.md` and `UNRESOLVED_DECISION` agree. Fixed after it, not seen by the reviewer: the Blocked-tasks bullet and the selected-option clause now match the renderer's conditions; the two decision rows in `dashboard-regeneration.md`'s format table; the audit lens exempts surviving anchors of a `partially_superseded` record; the Post-Decision Check says a superseded record gets no check and a task Blocked only for it is unblocked; the gate line prints once per decision per run and names the two ways to clear it; `partially_superseded` names the same optional fields; check 6 wording.
2. Left: `dashboard-render.py`'s comment near the ratify row still names only `implement-agent` (behaviour is keyed on status; no script change this release); scenario 49 Trace G has no orchestrator variant; the other pre-HTML dashboard text the reviewer listed (`work.md` "resolve it in the dashboard", scenario 08, "Tasks section" lines) stays under FB-127's open post-DEC-024 doc item.
