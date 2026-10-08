# Plan: v5.14.2 — renderer guards, Notes headings, `/review` agent-decision skip; template hygiene

**Status:** IN PROGRESS 2026-10-07 (commit 1 done: 232a72c)
**Closes:** FB-127 (n), (g), (r), (e), (k); FB-112 (a), (c), (d)
**Not included:** the sentinel and recovery cluster (FB-127 aa–af, FB-104 case 1, FB-127 (c)); FB-127 (a)/(j) wording sweep; (s), (m), (b), (d), (i)

## Measured first (2026-10-07, read-only)

- Sessions on v5.14.x in the 9 downstream projects: 0. Open sentinels 0; tasks In Progress 0, Awaiting Verification 0.
- (n) `### X` and `# X` in sidecar `user_notes` render as `<p>### X</p>`; lists and bold render. 6 heading lines in 4 of 9 sidecars (conversation_opener 2, OEMMatInsightBI 2, flirty-gym 1, PortfolioWebsite 1).
- (g) `dashboard-render.py --html` exits 1 with `AttributeError` on: `verification-result.json` holding a JSON string; sidecar `section_toggles` a list or string; sidecar `audit_digest` a list or string. Does not crash on: list `version.json`, list `verification-result.json`, non-object `phase_gates`, `augment_rows`, `user_notes`, a list task file, wrong-typed task fields.
- (r) `review.md:85` flags `approved` records with no anchors. Agent-decided (`decided_by: implement-agent`/`orchestrator`) and `approved` with no anchors: 17, all in styler (9 with one id in `related.tasks`, 8 with several); none carries `ratified`. *(Corrected 2026-10-07 after the docs review: the first count, "styler 18, conversation_opener 4", came from a pattern that missed inline `[...]` anchor lists and counted one record wrongly; re-measured by the orchestrator, and it matches the reviewer's 17.)*
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

- **A1 (B, 2026-10-07).** `extension-patterns.md` gets `ratified` only for the reconsidered-record case: the section covers the ticked-box path, which `/work ratify` does not use.

### Decisions after agent B's return (user, 2026-10-07)

6. Commit 1 as built (DEC-003's placeholder `## Decision` body and root `CLAUDE.md`'s "21 records" line left as they are).
7. (r) exception: `/review` does not skip an agent-decided record that was reconsidered and whose newly ticked option is not yet built (follow-up task unfinished). Sent back to agent B.
8. From B's six out-of-scope gaps, `research.md:45` (no `partially_superseded` branch) and `dashboard-regeneration.md:459` (status display mapping omits `superseded` and `partially_superseded`) go to the fixer pass; the other four are logged under FB-127: `audit-coherence.md:196` (the superseded lens treats a partially superseded record as wholly replaced), `audit-coherence.md:91` (`superseded_by` / `superseded_date` defined nowhere), `health-check.md:461` (legacy check matches `implement-agent` only), `health-check.md:441` (anchors required on `implemented` records, no agent-record exemption).

Settled by agent B, not decided by the user (for the reviewer): the skip is a second sentence on the same bullet; the lifecycle diagram is untouched; `partially_superseded` is given a one-clause meaning inferred from its name (no consumer defines it); "resolved for `decision_dependencies`" rests on the renderer (`UNRESOLVED_DECISION`); `extension-patterns.md:165-167` (pre-DEC-024 table) left alone.

### Agent B, second return (2026-10-07): decision 7 narrowed, back to the user

Nothing on disk links a decision record to its follow-up task (`phase-decision-gates.md:165` only offers to create one; `related.tasks` keeps the original task; the old selection is overwritten, `work.md:392`). So "follow-up unfinished" and "selection differs from the build" cannot be read from files. B implemented a proxy instead: don't skip an agent-decided record that has a ticked box under `## Select an Option` and `ratified` equal to `decided` (a reconsider tick sets both to the same day, `work.md:391`; plain `/work ratify` leaves `decided` alone, `work.md:725`). Known false positives, all advisory: the user re-ticked the option that was built; the follow-up is Finished but the record was never moved to `implemented`; a legacy agent-ticked record ratified on its `decided` date. B also added the `decided` reset to `decisions.md:235`. B's line citations are not yet reproduced by the orchestrator or the reviewer.

### Agent A return (2026-10-07), copied back by file list

Files: `scripts/dashboard-render.py`, `scripts/tests/test_dashboard_render_html.py`, `support/reference/dashboard-regeneration.md`. 428 tests green on 3.13.15 and 3.10.20 after the copy-back (407 + 21: `TestNonObjectInputs` 11, `TestNotesHeadings` 10), run by the orchestrator.

Reproduced by the orchestrator (old script exits 1, new exits 0 with a `warning:`): `version.json` `[1]`; `verification-result.json` string; `section_toggles` list; `audit_digest` string. `### Quick Links` renders `<h5>`, `# Top <b>` renders an escaped `<h3>`, `#hashtag` stays a paragraph. A task with `status` as a list still exits 1 on both.

Correction to "Measured first": the orchestrator's "does not crash" list was wrong for a truthy non-object `version.json` (`[1]`; only `[]` is safe), a truthy non-object `phase_gates` once a phase boundary is reached, a non-empty list `verification-result.json`, and wrong-typed task fields.

Agent-reported, not reproduced: fuzz of 17 values at 131 paths (3,774 runs per script) leaves only task-field crashes; six fixture projects byte-identical old vs new; each of the 11 crash tests fails on the original.

- **A2 (A).** Guards beyond the three measured inputs: truthy non-object `version.json`; `phase_gates` and its entries; `audit_digest.items` / `dismissed_ids`; `custom_views_instructions`; `criteria` entries and non-integer counts; the spec index; `archive-index.json`; null/falsy `dependencies` and `decision_dependencies`.
- **A3 (A).** Heading mapping: `#` → `<h3>`, `##` → `<h4>`, `###` → `<h5>`, `####`–`######` → `<h6>`, styled inline (15/14/13/12px).

Settled by agent A, not decided by the user (for the reviewer): styles inline rather than in `CSS_HTML` (a stylesheet rule would change every page's bytes); `.mini h3`'s uppercase overridden inline; a closing hash run is dropped; fence lines suppress headings only; one `warning:` per wrong-shaped file or sidecar object field, entries inside skipped silently; `[]`, `""`, `0` for `version.json`, `verification-result.json`, `phase_gates`, `audit_digest` now warn (HTML unchanged); sidecar `null` fields silent; helpers `load_json_object()` and `_sidecar_object()`; a Lifecycle paragraph in `dashboard-regeneration.md` on wrong-shape handling; a code comment citing FB-127 n.

Left by agent A (task-file fields, still crash): `status`, `owner`, `phase_name` as list/object; `dependencies` / `decision_dependencies` as a truthy non-list; `task_verification` as a truthy non-object; `due_date` / `external_dependency.expected_date` as a non-string. `validate-tasks.py` type-checks none of `dependencies`, `task_verification`, `phase_name`, `due_date`.

### Decisions after both returns (user, 2026-10-07)

9. (r), replaces 7's wording: when the follow-up task is created after a reconsider, its id is appended to the record's `related.tasks`; `/review` flags a reconsidered agent-decided record only while that task is not Finished. With no follow-up task, the date-equality proxy applies.
10. Wrong-typed task-file fields stay as they are in the renderer; logged under FB-127 (g).
11. The new warnings on empty wrong-shaped files (`[]`, `""`, `0`) are kept.

### In progress

- Fixer (agent B resumed, fresh mirror-c): decision 9 across `review.md`, `phase-decision-gates.md`, `work.md`, `decisions.md`, scenario 49; `research.md:45`; the status display mapping line in `dashboard-regeneration.md`.
- Independent reviewer, pass 1: the three renderer files only (the docs change follows when the fixer returns).

### Fixer return (2026-10-07), copied back by file list

Files: `commands/review.md`, `commands/research.md`, `support/reference/phase-decision-gates.md`, `support/reference/decisions.md`, `support/reference/dashboard-regeneration.md` (the status display mapping line only), `tests/scenarios/49-agent-decisions-recorded-and-ratified.md`. `work.md` and `iterate.md` needed no change (they cite the Post-Decision Check).

- **A4 (decision 9).** The write lives in `phase-decision-gates.md § "Post-Decision Check"`: the follow-up task's id is appended to `related.tasks`, the original id stays first. `/review`: with more than one id the last is the follow-up, flag until it is Finished; with one id, flag when a box is ticked under `## Select an Option` and `ratified` equals `decided`.
- **A5 (orchestrator).** `work-procedures.md:21` "an agent record for this task already exists" now matches on the first id of `related.tasks`, so a follow-up task's own held choices are not taken for a repeat of the reconsidered record. Found by the fixer; edited inline by the orchestrator.

Settled by the fixer, not decided by the user (for the reviewer): with two ids the reconsidered signature is dropped (the second id is the evidence); the Late Decision Check note was updated; the mapping line in `dashboard-regeneration.md` got `superseded` and `partially_superseded` although its second sentence ("Selected column…") is pre-DEC-024 text, left as is; `research.md` treats `partially_superseded` like `superseded` (report and stop); nothing says whether the follow-up task carries the decision in `decision_dependencies` (`/health-check` Part 3 check 6 will report it, report-only).

Known misclassifications of the `/review` rule (advisory check): same option re-ticked (flagged); follow-up declined or reconsidered before this release (flagged); follow-up Absorbed or Broken Down (stays flagged); a hand-added second id is read as the follow-up; a Finished but wrong follow-up is not flagged.

DEC-016: the fixer reads `rules/spec-workflow.md:37` ("frontmatter updates (e.g. …)") as covering the `related.tasks` append; the file is unchanged.

## Review, docs (2026-10-07)

Independent read-only reviewer over the docs diff (a second reviewer has the renderer files). No blocker. D1–D5 hold for every record the v5.11+ flow produces; all twelve traced cases match intent except multi-id and zero-id legacy records. The three claims the fallback rests on hold (`work.md:391`, `:725`; `research.md:47`). The write is stated once in the owner and both callers reach it; no other writer of `related.tasks`; no missed reader; the renderer does not read the field (control: `decided_by` hits). Not run: a live `/review`.

- **D-R1 should-fix** `review.md:85`: with more than one id the last is read as a follow-up with no "reconsidered" test; 8 of the 17 styler legacy records have several ids (0 false flags today, all last-listed tasks Finished). Fix: require the reconsidered signature (ticked box and `ratified` equal to `decided`) in both branches; split the bullet. Same premise in `phase-decision-gates.md:130-131` and `work-procedures.md:21`.
- **D-R2 should-fix** `decisions.md:202`: "resolved for `decision_dependencies`" is true of the renderer only; the `/work` gate (`phase-decision-gates.md:83-88`) names neither superseded status. Fix: attribute it to the dashboard.
- **D-R3 should-fix** a record with no ids matches neither branch. Fixed by D-R1's "otherwise".
- **D-R4 should-fix** `work-procedures.md:21` "names the task first" can be misread. Reword to "the first id in its `related.tasks` is this task". Side effect: a legacy record listing the reworked task second no longer matches, so a rework writes an unlinked new record.
- **D-R5 nit** one-id flags never clear; say that adding `implementation_anchors` clears them. **D-R6 nit** an archived follow-up counts as Finished; an Absorbed one stays flagged. **D-R7 nit** `health-check.md:408` `decided` description stale after a reconsider. **D-R8 nit** scenario 49 Trace F does not exercise the `/review` rule or the follow-up's own record. **D-R9 nit** check 6 reports the follow-up task as a mismatch on every run (report-only). **D-R10** DEC-016 paragraph covers the append as written.

Orchestrator: D-R1–D-R8 to the fixer on a fresh mirror (mirror-d), then the same reviewer re-verifies. D-R1 keeps decision 9's outcomes and adds the signature to the multi-id branch (told to the user). D-R6's Absorbed case and D-R9 are left as known and logged under FB-127.

## Fix pass, docs (2026-10-07)

Same fixer, fresh mirror (mirror-d): D-R1–D-R8 applied, copied back by file list (`review.md`, `phase-decision-gates.md`, `work-procedures.md`, `decisions.md`, `health-check.md`, scenario 49). The same docs reviewer re-verifies.

Settled by the fixer, departing from the reviewer's draft (X1–X4; under re-verification):

- **X1** The draft's "(a task file under `.claude/tasks/archive/` is Finished)" is false: a rejected out-of-spec task is archived without being Finished (`work-user-flows.md:91-95`). Written instead: "(if its file is not among the active tasks, read it in `.claude/tasks/archive/`)".
- **X2** The clearing hint says "marking the record `implemented` with `implementation_anchors`", not anchors alone (`decisions.md:330` adds anchors at `implemented`).
- **X3** Scenario 49: DEC-006 is "never flagged, whether still `recorded` or ratified" (it is `recorded` in Trace F).
- **X4** The write in `phase-decision-gates.md` now says the follow-up id goes "after the ids already there" and that `/review` reads the last id "on a reconsidered record".

Left open by the fixer: a legacy record produced by several tasks does not match a rework of its second or later task at `work-procedures.md:21` (an extra record is written); a rejected out-of-spec follow-up keeps the record flagged; a legacy agent-ticked record ratified on its `decided` date reads as reconsidered; a legacy multi-id record genuinely reconsidered with the follow-up declined reads its last original task as the follow-up (accepted by the orchestrator in the brief).

## Re-verification, docs (2026-10-07)

Same docs reviewer: D-R1, D-R2, D-R3, D-R5, D-R7, D-R8 fixed; D-R4 and D-R6 partly (wording → D-S1; an Absorbed follow-up stays flagged, accepted). X1–X4 sound. Seventeen cases traced against the two-bullet text, all match intent except the known holes. The three legacy holes are acceptable for an advisory check. Nothing holds the release. Not re-done by the reviewer: the downstream count; scenario 49 Trace F's opening state (it relied on the orchestrator for DEC-006 being `recorded` there).

- **D-S1 nit** `work-procedures.md:21`: the parenthesis read as three conditions. **D-S2 nit** `phase-decision-gates.md:130-132`: "after a reconsider, a follow-up task" implied one always exists. **D-S3 nit** `review.md:86`: a follow-up id whose file is in neither place had no outcome.

All three applied by the orchestrator with the reviewer's exact replacement text (D-S1: "both hold: … does not count as a match …"; D-S2: "when a reconsider led to one"; D-S3: "if it is in neither, flag the record and say the task is missing"). The reviewer wrote these sentences but has not re-read them in place.

## Review, renderer (2026-10-07)

Independent read-only reviewer over the three renderer files. No blocker. Byte-identity reproduced: 8 fixtures of its own plus the implementer's 6 on 3.13.15 and 3.10.20 (28 comparisons, stdout and stderr identical); 7 real heading-free projects identical, 4 with headings differ only inside the Notes card. Against the old script 11 of 11 `TestNonObjectInputs` and 8 of 10 `TestNotesHeadings` fail and nothing else. Its own fuzz (21 values at 286 paths, 10,689 `--html` renders per script): nothing crashes on new that rendered on old; the only crash outside task-file fields is R1. 75 mutants listed one by one, 64 caught, 11 survived (1 equivalent). Settled items a–j sound (e, g, i with the caveats in R5, R6). Not run by the reviewer: the implementer's own fuzz script; the full suite on 3.10; `--task-hash` fuzz.

Side effects reported by the reviewer and checked by the orchestrator: a Playwright MCP console log written to the repo root and removed (no `.playwright-mcp` left, `git status` unchanged); a local `http.server` on 127.0.0.1:8731, stopped (nothing listening). Its `real.py` read every `~/Developer/*/.claude`, read-only, which includes tinder-streamliner-cc and PQ-CC-pipeline-builder.

- **R1 should-fix** a wrong-typed `phase_name` in an `archive-index.json` entry still exits 1 (`build_phases`); the doc says wrong shapes never stop the render.
- **R2 should-fix (tests)** three null-dependency guards in `phase_status` are reached by no test (mutants survive).
- **R3 nit** Notes headings are no larger than body text (measured: paragraphs 14.5px, list items 13px; headings 15/14/13/12).
- **R4 nit, pre-existing** non-UTF-8 bytes in any file read, a 100,000-deep JSON or a 5,000-digit integer still exit 1.
- **R5 nit, pre-existing** `user_notes: null` renders `<p>None</p>`.
- **R6 nit** three overstated clauses in the wrong-shape paragraph of `dashboard-regeneration.md`.
- **R7 nit** one fence flag shared by both markers; an inline triple-backtick span opens a fence. **R8 nit** a heading that is only a closing hash run renders the hashes. **R9 nit** integral-float criteria counts now hide the Acceptance section. **R10 nit** test gaps (gate object with a non-approved status, a valid `custom_views_instructions`, style properties, silent-skip stderr, exit code through the CLI).
- Outside the diff, old and new: a `-->` in `version.json` `template_version` or spec frontmatter `status:` breaks out of the META comment; `_mdi` accepts any link scheme.

Orchestrator: R1, R2, R5–R10 to the fixer (the implementing agent resumed, fresh mirror-e). R1's fix also removes the task-file `phase_name` crash, a narrow overlap with decision 10 (told to the user). R3 and R4 to the user. The two out-of-diff observations are logged under FB-127.

## Fix pass, renderer (2026-10-07)

The implementing agent resumed on a fresh mirror (mirror-e): R1, R2, R5–R10 applied, 3 files copied back by file list. 438 tests green on 3.13.15 and 3.10.20, run by the orchestrator after the copy-back (428 + 10). Agent-reported, for the reviewer to reproduce: six fixtures still byte-identical to the original script; 26 mutants listed one by one, 25 killed, 1 equivalent (controls: identity survives, a deliberate break is killed); archive-index entry re-fuzz 357 runs per script, 20 crashes before (all `phase_name`), 0 after; the rewritten wrong-shape paragraph verified clause by clause in 56 CLI runs.

Settled by the fixer, not decided by the user (Y1–Y6; for the reviewer):

- **Y1 (R9)** integral-float counts print as ints (`2/3`); the original printed `2.0/3.0`. The one valid input that renders differently from v5.14.1. `inf` and `nan` are rejected.
- **Y2** one `or []` from the first pass removed as unreachable (`phase_status` eligible `dependencies`; the line above requires a truthy value).
- **Y3 (R7)** any line of three or more of the opening character closes a fence; a line with an info string opens but never closes.
- **Y4 (R5)** a non-null non-string `user_notes` warns; `null` is silent; read only while `notes` is on.
- **Y5 (R8)** a heading with no text after stripping the closing run stays a paragraph of the original line.
- **Y6** the notes sentence in `dashboard-regeneration.md` § 5 and the `_html_notes` docstring gained the fence and empty-heading clauses.

Pending with the user: R3 (heading sizes), R4 (unreadable content).

### Decisions after the renderer review (user, 2026-10-08)

12. (R3) Notes heading sizes 17/16/15/14px.
13. (R4) Non-UTF-8 content is fixed now (the file reads as unreadable, with a warning); deep JSON and huge integers are logged under FB-127 (g).
14. (Y1) Integral-float criteria counts print as ints (`2/3`).

Addendum sent to the same fixer on mirror-e (12, 13); then the renderer reviewer re-verifies the fix pass and the addendum together.

## Addendum, renderer (2026-10-08)

Same fixer, mirror-e: decisions 12 and 13 applied, 3 files copied back by file list. 445 tests green on 3.13.15 and 3.10.20, run by the orchestrator (438 + 7). Reproduced by the orchestrator: a non-UTF-8 `version.json` exits 0 with `warning: unreadable version.json: …`; `### Quick Links` renders at 15px.

Agent-reported, for the reviewer: body sizes confirmed in `CSS_HTML` (paragraphs inherit 14.5px, `.notescard li` 13px); six `except` clauses gained `UnicodeDecodeError` by name and nothing wider (deep JSON and a 5,000-digit integer still exit 1); these six are the script's only file reads; 14 mutants, 14 killed; six fixtures byte-identical to the original.

Settled by the fixer (Z1–Z4; for the reviewer): **Z1** a non-UTF-8 spec follows the existing unreadable-spec result (version kept, status and fingerprint `—`), not "absent". **Z2** that case prints two warnings (its own and "drift unchecked"). **Z3** `load_spec` now warns for every unreadable spec, the previously silent `OSError` case included (stderr only). **Z4** a test pins the stylesheet's 14.5px and 13px beside the heading sizes. Known: `<h6>` at 14px is 0.5px under paragraph text.

## Re-verification, renderer (2026-10-08)

Same renderer reviewer (no Playwright, no server, this repo and its scratch only): R1, R2, R5–R10 and the addendum all fixed; byte-identity to HEAD reproduced on 14 fixtures on both Pythons (28 comparisons); differential fuzz (3,050 cases) shows no regression, and whole-float counts are the only valid input that renders differently; every clause of the rewritten paragraph matches the script in 76 CLI runs; the six `read_text` sites are the only reads, and only `UnicodeDecodeError` was added. 51 mutants one by one (controls first): 48 caught, 2 equivalent, 1 real survivor (S2). Y2–Y5 and Z1–Z4 sound. Nothing holds the release. Not run by the reviewer: the full suite on 3.10; the fixer's own fuzz; `--task-hash` fuzz.

- **S1 nit** the doc said the drift warning is "a second warning" although it prints first. **S2 nit** no test pinned that a run shorter than three does not close a fence. **S3 nit** the notes sentence omitted that a backtick line with a later backtick is not a fence.

All three applied by the orchestrator (S1, S3 with the reviewer's wording; S2 as one added case in `test_fence_closes_only_on_its_own_marker`, shown to fail with the `len(line) >= 3` guard removed). 445 tests green on 3.13.15 and 3.10.20 afterwards. The reviewers have not re-read these last edits in place (D-S1–D-S3, S1–S3).

**Status:** built, reviewed, re-verified; release bookkeeping done (`version.json` 5.14.2, ship-log, FB-127 stubs and (ag)–(ai), root `CLAUDE.md`, architecture map); awaiting the user's OK to commit, tag and push.
