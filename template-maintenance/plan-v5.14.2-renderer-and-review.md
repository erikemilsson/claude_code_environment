# Plan: v5.14.2 — renderer guards, Notes headings, `/review` agent-decision skip; template hygiene

**Status:** IN PROGRESS 2026-10-07
**Closes:** FB-127 (n), (g), (r), (e), (k); FB-112 (a), (c), (d)
**Not included:** the sentinel and recovery cluster (FB-127 aa–af, FB-104 case 1, FB-127 (c)); FB-127 (a)/(j) wording sweep; (s), (m), (b), (d), (i)

## Measured first (2026-10-07, read-only)

- Sessions on v5.14.x in the 9 downstream projects: 0. Open sentinels 0; tasks In Progress 0, Awaiting Verification 0.
- (n) `### X` and `# X` in sidecar `user_notes` render as `<p>### X</p>`; lists and bold render. 6 heading lines in 4 of 9 sidecars (conversation_opener 2, OEMMatInsightBI 2, flirty-gym 1, PortfolioWebsite 1).
- (g) `dashboard-render.py --html` exits 1 with `AttributeError` on: `verification-result.json` holding a JSON string; sidecar `section_toggles` a list or string; sidecar `audit_digest` a list or string. Does not crash on: list `version.json`, list `verification-result.json`, non-object `phase_gates`, `augment_rows`, `user_notes`, a list task file, wrong-typed task fields.
- (r) `review.md:85` flags `approved` records with no anchors. Agent-decided (`decided_by: implement-agent`/`orchestrator`) and `approved` with no anchors: styler 18, conversation_opener 4; none carries `ratified`.
- (e) `partially_superseded`: 0 mentions in `support/reference/decisions.md`; used in `dashboard-render.py`, `dashboard-regeneration.md`, `health-check.md`, `audit-coherence.md`.
- Map: `Current as of: v5.1.1`, 26 tagged releases behind; `persist-session-export.py` absent; "~29 reference docs" against 33.
- Root `decisions/`: 22 records; anchors in the mapping shape 4 (021, 022, 023, 025), hash-comment 9, quoted 3, prose 2, bare 2, empty 2; 8 lack `## Decision` (004, 005, 006, 007, 008, 010, 011, 020); DEC-003 lacks `## Options Comparison`.

## Decisions (user, 2026-10-07)

1. Two commits: template-only hygiene (no version bump), then v5.14.2.
2. The sentinel cluster is held until a harvest shows v5.14.x has run.
3. (r): `/review` skips agent-decided records, keyed on `decided_by`.
4. The (a)/(j) wording sweep is left out.
5. All 16 non-conforming `implementation_anchors` blocks are converted to the mapping shape.

## Build

### Commit 1 (orchestrator; `template-maintenance/`, `decisions/`)

Map reconcile; anchors; missing section headings.

### Commit 2 (two agents, scratch mirrors, no shared files)

| Agent | Files |
|---|---|
| A | `scripts/dashboard-render.py`, `scripts/tests/test_dashboard_render_html.py`, `scripts/tests/test_dashboard_render.py`, `support/reference/dashboard-regeneration.md` |
| B | `commands/review.md`, `support/reference/decisions.md`, `support/reference/extension-patterns.md` |
| Orchestrator | `version.json`, ship-log, feedback stubs, root `CLAUDE.md` |

### Amendments

(none yet)
