# Plan: v5.13.0 — section provenance on every task (FB-135)

**Status:** IMPLEMENTED in v5.13.0 (2026-10-07); see ship-log. Contract amended A1–A9; review fixes R1–R9 and re-verify fixes below. Originally APPROVED 2026-10-06 (decisions 1–6: baseline from the spec's git history; new `spec_unmapped` marker; `fingerprint.py --baseline --write` stamps; `validate-tasks.py` warns; free-form `spec_section` values left out; v5.13.0 minor).
**Target:** v5.13.0 (minor: new task field, new script modes including a write mode, new validation warning).

## Survey (2026-10-06, read-only, `fingerprint.py --drift` + a session script)

- `no_provenance`: PortfolioWebsite 77, styler 20, OEMMatInsightBI 8, conversation_opener 1; the other five projects 0. Total 106.
- Shape: `spec_section` resolves to a current heading but there is no `section_fingerprint`: 83 (PortfolioWebsite 75, OEMMatInsightBI 7, conversation_opener 1). `spec_section` set but unresolvable: 5 (styler 4, OEMMatInsightBI 1). No `spec_section`: 18 (styler 16, PortfolioWebsite 2).
- Origin, where it can be told: 5 OEMMatInsightBI tasks carry `source: verify-agent (phase-level …)`; PortfolioWebsite's 77 were created July–October with `spec_version` + `spec_section` and never a fingerprint; styler's 20 were created in June for one phase; `/breakdown` children: 0.
- Baseline risk: comparing each resolvable task's date (completion date when Finished, else updated/created) with the date its `## ` section last changed in the spec's git history, the section changed **after** the task for 43 of 83 (PortfolioWebsite 40: 37 Finished, 2 On Hold, 1 Pending; OEMMatInsightBI 3 Finished). styler's spec is not tracked by git.
- Scratch clones with full history and live task files, for write trials: `<scratchpad>/clones/{PortfolioWebsite,OEMMatInsightBI,conversation_opener}`.

## Build split

Each agent edits a scratch mirror (`.claude/` copied as `dot-claude/`, plus `tests/`). No shared files.

| Agent | Owns |
|---|---|
| **A** scripts | `.claude/scripts/fingerprint.py`, `.claude/scripts/validate-tasks.py`, `.claude/scripts/tests/test_fingerprint.py`, `.claude/scripts/tests/test_validate_tasks.py`, `.claude/scripts/README.md` |
| **B** prose | `.claude/support/reference/task-schema.md`, `drift-reconciliation.md`, `work-procedures.md`, `decomposition.md`, `phase-decision-gates.md`, `friction-register.md`, `shared-definitions.md` (only if it lists task fields), `.claude/commands/work.md`, `breakdown.md`, `health-check.md`, `.claude/agents/verify-agent.md`, `implement-agent.md`, `tests/scenarios/44-drift-detection-reaches-user.md`, `tests/scenarios/51-task-provenance-baseline.md` (new), `tests/README.md` |

Main session: `version.json`, ship-log, FB stubs + archive, root `CLAUDE.md`, architecture map.

## Build contract (pinned)

Terms: *current spec* = `find_current_spec()`; *resolve* = `_match_section()` on the stripped value (a `## ` heading as is or with `## ` prefixed, else a `### ` value naming exactly one current `### ` heading); *no-provenance task* = a task `compute_drift()` reaches rule 3 with (not Absorbed/Broken Down, not `out_of_spec`, current spec version, `spec_section` or `section_fingerprint` missing or blank).

### 1. Task field `spec_unmapped`

Optional boolean. `true` = the task is in-spec work that belongs to no single spec section (cross-cutting infrastructure, a repo-wide sweep), so there is no section to drift from. Distinct from `out_of_spec` (work beyond the spec, which needs approval). A task has section provenance (`spec_section` + `section_fingerprint`), or `spec_unmapped: true`, or `out_of_spec: true`.

### 2. `fingerprint.py`

**`compute_drift()` rule 3.** A no-provenance task with `spec_unmapped is True` is counted in the new result key `unmapped` (int, placed after `no_provenance`) instead of `no_provenance`. Nothing else changes: a task that has both provenance and `spec_unmapped: true` is checked like any task with provenance.

**`--provenance DIR --section HEADING`** (read-only). Prints the fields a new task for that section carries:
```json
{"spec_version": "spec_v3", "spec_fingerprint": "sha256:…", "spec_section": "## Authentication", "section_fingerprint": "sha256:…"}
```
`spec_section` is the real current heading the value resolved to; `spec_fingerprint` is the full-file hash (`--spec`); for a `### ` match `section_fingerprint` is that subsection's hash. Exit 1 with `error: no current spec heading matches '<value>'` on stderr when it doesn't resolve; exit 2 when DIR is not a directory, has no current spec, or `--section` is missing.

**`--baseline DIR`** (read-only). One proposal per no-provenance task (not the `unmapped` ones):
```json
{
  "spec": "spec_v1", "history": "git",
  "tasks": [
    {"id": "166", "file": "task-166.json", "status": "Finished", "title": "…",
     "recorded_section": "Overview", "action": "stamp_history",
     "spec_section": "## Overview", "section_fingerprint": "sha256:…",
     "reference_date": "2026-08-26", "reference_field": "completion_date",
     "commit": "<40-hex>", "commit_date": "2026-08-20",
     "changed_since": true, "same_day_edit": false, "reason": ""}
  ],
  "counts": {"stamp_history": 0, "confirm_current": 0, "needs_section": 0, "report_only": 0}
}
```
- `history`: `"git"` when DIR is inside a git work tree and the current spec file has at least one commit; else `"none"`.
- **Reference date** of a task (the `updated_date` fallback here is superseded by R3): `completion_date` when status is Finished, falling back to `updated_date` then `created_date`; for any other status `created_date`. The value's first 10 characters must parse as `YYYY-MM-DD`; otherwise the task has no reference date.
- **Spec history:** commits touching the current spec file (`git log` on its repo-relative path, newest first), each with its committer date as a calendar date (`%cs`). Section hashes at a commit use the same recipe as `--sections` / `--sections --depth 3` on that commit's content.
- **Action**, first match wins:
  1. The recorded `spec_section` does not resolve against the current spec (or is blank): `report_only` when Finished, else `needs_section`. `spec_section`/`section_fingerprint`/`commit` fields `null`.
  2. `history` is `"none"`, or the task has no reference date, or no spec commit is dated on or before it, or the resolved heading does not exist (for a `### ` match: is not unique) in the spec at the chosen commit: `confirm_current`. `section_fingerprint` = the **current** hash; `commit` `null`; `reason` says which of these applied.
  3. Otherwise `stamp_history`. Chosen commit = the newest commit dated on or before the reference date. When the section's hash at that commit differs from its hash at the newest commit dated strictly before the reference date (the section was edited on the reference date itself, which a date can't order against the task): take the earlier commit and set `same_day_edit: true`. `section_fingerprint` = the section's hash at the chosen commit; `changed_since` = it differs from the current hash (the next drift check will report the task).
- `tasks` sorted by natural id; `counts` always has the four keys.

**`--baseline DIR --write --ids ID[,ID…] [--confirm-current]`.** Writes the proposals for the listed ids. An id that is not a proposal, or whose action is `needs_section`/`report_only`, or is `confirm_current` without `--confirm-current` → exit 2 before anything is written (the message names the ids). `--write` without `--ids` is a usage error. For each task file: set `spec_section` (the real heading) and `section_fingerprint`; set `spec_version` to the current spec's stem only when it is missing or blank; prepend to `notes` (newest first, as every notes write): `[BASELINE] section_fingerprint stamped from the spec at <commit 7-hex> (<commit date>); the task records no hash of its own.` or, for `confirm_current`, `[BASELINE] section_fingerprint set to the current section text on <today>, confirmed by the user as what the task was built against.` No other key changes: `updated_date`, `spec_fingerprint`, status and verification fields stay as they are (a changed `updated_date` would invalidate a phase-level verification result). The file keeps its key order, indent width and trailing-newline state; written via a temp file and `os.replace`. Output: `{"written": [{"id", "file", "action", "spec_section", "section_fingerprint", "changed_since"}], "unchanged": [ids already carrying exactly these values]}`. Exit 0.

**Expected real data** (read-only on live projects; write trials only on the scratch clones): PortfolioWebsite 75 with a hash to stamp + 2 unresolvable (1 Finished → `report_only`, 1 On Hold → `needs_section`); OEMMatInsightBI 7 + 1 `report_only`; conversation_opener 1; styler 20 `report_only`. Of the stampable ones about 43 should come out `changed_since: true` (the Survey compared dates with a strict "after", so `same_day_edit` cases will add to it: report how many). After a write trial, `--drift` on the clone shows `no_provenance` 2 / 1 / 0 and the `changed_since` tasks as drifted.

### 3. `validate-tasks.py`

- `spec_unmapped` joins the boolean fields (a non-boolean value is a schema error).
- New summary key `provenance_warnings`: `[{"file", "task_id", "reason"}]` for tasks that are not Absorbed/Broken Down, not `out_of_spec: true`, not `spec_unmapped: true`, and lack a non-blank `spec_section` or `section_fingerprint` (`reason`: `no spec_section`, `no section_fingerprint`, or both); and for tasks with `spec_unmapped: true` that also carry a `section_fingerprint` (`reason`: `spec_unmapped set on a task with section provenance`).
- Warnings never change the exit code. Text output adds one line: `Provenance: N task(s) without section provenance (/health-check offers a one-time baseline)` or `Provenance: OK`.

### 4. Prose (B)

- **`task-schema.md`:** `spec_unmapped` in the field table and the Full Task example; § "Drift Prevention Fields" gains the creation contract: *every* new task file gets section provenance at creation, whoever creates it and by whatever path; get the four fields from `python3 .claude/scripts/fingerprint.py --provenance .claude --section "<heading>"` (exit 1 means the heading is not a real one: pick a real one, don't write the free-form value); a task that belongs to no single section gets `spec_unmapped: true`; an out-of-spec task gets `out_of_spec: true`. The existing "No provenance" bullet is rewritten (missing vs unmapped; the baseline).
- **Creation paths** each get one line pointing at that contract, with what is specific to the path:
  - `work-procedures.md` phase-level step 2 (fix tasks): verify-agent's `task_json` names `spec_section` (a real `## ` heading) or sets `spec_unmapped: true`; the orchestrator runs `--provenance` and merges the fields before writing; when the heading doesn't resolve, the orchestrator picks the section from the spec index, or sets `spec_unmapped: true` and says so in the task's `notes`.
  - follow-up tasks the orchestrator creates from implement-agent `issues_discovered` entries (wherever that step lives).
  - `work.md` "Create a task for the request" (a user request mid-`/work`) and the out-of-spec path (already marked).
  - `phase-decision-gates.md`: the task offered after a reconsidered decision.
  - `friction-register.md`: a task created to fix register entries.
  - `decomposition.md` step 8: name `--provenance` as the script route; a task mapping to no section gets `spec_unmapped: true`.
  - `breakdown.md`: children also copy `spec_unmapped`.
- **`verify-agent.md`** Step 7 `task_json`: includes `spec_section` (a real `## ` heading from the spec it just verified against) or `spec_unmapped: true`. **`implement-agent.md`** `issues_discovered`: an entry with `suggested_action: create new task` names the spec section when it knows it.
- **`drift-reconciliation.md`:** rule 3 and the JSON example gain `unmapped`; the "never flagged" paragraph points at the baseline.
- **`health-check.md` Part 1 check 11 (Provenance Integrity)** gains **Section provenance baseline**: run `python3 .claude/scripts/fingerprint.py --baseline .claude`; report the counts; queue:
  - `stamp_history` tasks → **one** row for all of them: `Stamp section provenance on {N} tasks from the spec's history ({M} will then show as drift: their section changed after the task)` (drop the parenthesis when M is 0), risk `—`, included in bare `[A]`. Apply: `--baseline .claude --write --ids <ids>`. Say what follows: the next `/work` reports the M tasks' sections under Drift Reconciliation, where `[K]` keeps verified work.
  - `confirm_current` tasks → one `needs-input` row: `{N} tasks name a section but the spec has no history to date them ({reason summary}). Stamp the current section text as what they were built against? (yes / no / list of ids)`. `yes` applies with `--confirm-current`. This is the user's assertion, the same one as Drift Reconciliation's `[K]`; never a default.
  - `needs_section` tasks → one `needs-input` row per task: `Task {id} "{title}" names no resolvable spec section: which section, or unmapped?` (answer: a heading → set fields via `--provenance`; `unmapped` → `spec_unmapped: true`).
  - `report_only` → `ℹ️ {N} finished tasks name no resolvable spec section; drift can't be checked for them` (no row).
  - Also the `validate-tasks.py` `provenance_warnings` contradiction case as a WARNING line.
  - Never stamp by hand what the script declined: a current hash on a task whose section changed after it records a false "built against this text".
  - Task Auto-Fixes list and the Process / Batch Fix Triage mentions updated to match.
- **Scenarios:** 44 updated where the drift JSON is shown (`unmapped`); new 51 with traces: (A) baseline with history: unchanged-since and changed-since tasks, bare `[A]`, drift appears on the next `/work` and `[K]` absorbs it; (B) spec not in git → `needs-input` row, `yes` → `--confirm-current`; (C) `needs_section` answered with a heading and with `unmapped`; (D) a phase-level fix task and a mid-session user-request task created with provenance via `--provenance`, including the exit-1 free-form heading; (E) `same_day_edit`.

## Contract amendments

After both agents reported (2026-10-06; 357 tests on 3.10 and 3.13; action counts on live data match the Survey):

**A1. Real data.** `stamp_history` 75 / 7 / 1 (PortfolioWebsite / OEMMatInsightBI / conversation_opener), `needs_section` 1, `report_only` 1 / 1 / 0 / 20 (styler). `changed_since` 49 (43 + 6); `same_day_edit` 15 of 83 (PortfolioWebsite 9 of 75, OEMMatInsightBI 6 of 7). The same-day rule itself turns 6 tasks into drift reports; at least OEMMatInsightBI task-062 is the task's own spec edit (commit `fix(task-062)` on its completion date).

**A2. `reason` strings are constants.** Rule 1: `no spec_section`; `spec_section names no current spec heading`. `confirm_current`: `the spec has no git history`; `the task has no usable date`; `no spec commit on or before the task's date`; `the spec can't be read at the commit for the task's date`; `the section is not in the spec at the commit for the task's date`. Check 11's `{reason summary}` groups them with counts.

**A3. Reference date.** The fallback (`completion_date` → `updated_date` → `created_date` for Finished) applies only to a missing, null or blank field; a set but unparseable value means no reference date. A timestamp parses by its first 10 characters.

**A4. Same-day edges.** No commit strictly before the reference date: compare with the spec's oldest commit (one commit that day → stamped, `same_day_edit: false`; several that differ in the section → the oldest, `true`). Section absent at the earlier commit (added on the reference date): keep the same-day commit, `false`. Commit order is `git log`'s; no `--follow`.

**A5. `--write` idempotence.** A listed id that already has provenance is `unchanged` when its `spec_section` and `section_fingerprint` equal its recomputed proposal exactly (no `--confirm-current` needed); otherwise exit 2. Extra refusals before any write: an id used by two task files, `notes` of an unusable type, an unreadable file. Not atomic across files; a rerun finishes.

**A6. Write details.** Notes: string → note + space + notes; list → note inserted first; missing/blank → the note. New keys: `section_fingerprint` right after `spec_section`, `spec_version` right before it. Indent, line endings, escaping and file mode kept.

**A7. CLI edges.** `--baseline` on a directory with no spec exits 0 with `spec: null`, empty `tasks` (as `--drift`). `--provenance --section ""` exits 1.

**A8. Prose additions (B).** An unmapped task gets `spec_version` by hand (else it never goes `unmigrated` after a version bump). `section_snapshot_ref` stays decomposition-only. Follow-up tasks from `issues_discovered` get a creation paragraph in `work-procedures.md` (none existed). The reconsidered-decision task runs `--provenance` for current hashes rather than copying the related task's. Phase-level fix-task filename corrected to `task-{id}.json`. Two more creation paths: the test-harness subtask (copies its parent's provenance) and Phase UI smoke fix tasks (`work-web-evidence.md`).

**A9. To settle in the review-fix pass.** Prose says a re-listed stamped id exits 2 (A5 says `unchanged`) and that `--baseline` exits 2 without a spec (A7 says 0). `validate-tasks.py`'s text line promises a baseline even when every task is `report_only`, and counts old-spec-version tasks `--drift` treats as historical (styler 26 vs 20): reword, and have check 11 take counts from `--baseline`. A baseline write is a dashboard regen trigger (`rules/dashboard.md`, `dashboard-regeneration.md`). `%cs` needs git 2.21. A symlinked task file would be replaced by a regular file.

### Review fixes (2026-10-07, independent review: no corruption or out-of-scope write on real data; 8 should-fix, 4 nits; these supersede the text above where they differ)

- **R1 (write safety):** `--write` encodes every file in the planning phase, so an unencodable file (a lone surrogate) is refused before the first write. An I/O error while writing exits 2 and names the ids already written; README and check 11 say "exit 2 before the first write, except an I/O error during writing; a rerun finishes". A task file with duplicate JSON keys is refused (re-serialising would drop one). A task file that is not a regular file (symlink) or has more than one hard link is refused.
- **R2 (false in-sync, merges):** spec history is read with `--first-parent`, so a side-branch spec commit is dated by its merge. A fast-forwarded branch can't be told apart; `drift-reconciliation.md` and check 11 say history-dated hashes assume the spec was edited on the line the task was built on. Dates use `--date=short` with `%cd` (no git 2.21 requirement). Documented, not fixed: a commit's date is in the committer's own timezone.
- **R3 (false in-sync, reference date):** Finished → `completion_date` → `task_verification.timestamp` → `created_date`; `updated_date` is no longer used (291 of 474 Finished tasks downstream have `updated_date` after completion). Supersedes A3's order.
- **R4 (task older than the spec file):** a task with no `spec_version` whose reference date is on or before the current spec file's oldest commit date is `confirm_current` with reason `the task may predate this spec version`, never `stamp_history`. Check 11 splits the `confirm_current` row by reason: for `the spec has no git history` and `the task has no usable date` the question stays; for `no spec commit on or before the task's date`, `the section is not in the spec at the commit for the task's date` and `the task may predate this spec version` the row reads `{N} tasks are older than the spec's history for their section ({reason summary}). The current text is not what they were built against; accept it as their baseline anyway? (yes / no / list of ids)`. `--confirm-current` writes the note `[BASELINE] section_fingerprint set to the current section text on <today>, accepted by the user as the task's baseline.` for those three reasons, and the pinned "confirmed by the user as what the task was built against" note for the first two.
- **R5 (same-day rule; confirmed by the maintainer 2026-10-07):** measured on the 15 real same-day cases, the earlier-commit rule stamps the right hash in 5, no rule in 9 (with 2 false in-syncs). The default stays; two exceptions from git evidence are tried first, in order: **(a) own edit** — the task's `files_affected` names the current spec file and a spec commit dated on the reference date also touches the task's own file: stamp the newest such commit, `reason: "own spec edit"`; **(b) filed after the edit** — the task file first enters git in or after a spec commit dated on the reference date: stamp the newest same-day spec commit at or before the task file's first commit, `reason: "task filed after the edit"`; **(c)** otherwise the earlier commit. `same_day_edit` stays `true` in all three. Expected: right hash in 14 of 15, no false drift, no false in-sync; drift reports 49 → 45.
- **R6 (reconciliation diff):** a task with no snapshot whose notes carry `[BASELINE] … stamped from the spec at <sha>` is diffed against that commit (`git diff <sha> -- .claude/spec_v{N}.md`, cut to the section). `[BASELINE]` joins the note-tag list in `task-schema.md`. Scenario 51 Trace A step 8 follows.
- **R7 (creation paths):** `rules/task-management.md` gains `## Creating Tasks` (the always-loaded pointer; PortfolioWebsite's 77 tasks were filed mid-session with no command path); `work-web-evidence.md` Phase UI smoke gets its pointer; `/work` Step 1b names a grown `no_provenance` as tasks created without provenance.
- **R8 (one-time):** `validate-tasks.py`'s line reads `Provenance: N task(s) without section provenance (see /health-check Part 1 check 11)`; check 11 takes its counts from `--baseline`, shows ✓ with the `ℹ️` line when only `report_only` tasks remain, and reads `spec: null` (not exit 2) as "skip". A section that already has a deferral covers freshly stamped tasks too (said in check 11). A baseline write is a dashboard regen trigger (`rules/dashboard.md`, `dashboard-regeneration.md`).
- **R9 (tests):** `tasks/archive/` is neither proposed nor writable; a file whose name differs from its id (`task-007.json`, id `7`) is the file written; author date ≠ committer date.
- **Prose corrections from A9:** a re-listed stamped id is `unchanged`, not exit 2.
- **Decided 2026-10-07:** no `permissions.ask` rule for `fingerprint.py --baseline --write`; it changes four keys of task files the user already included in the triage table.
- **Re-verify (2026-10-07):** all twelve findings fixed or decided. Two new should-fix items in R5's exceptions, both able to stamp a false in-sync, fixed in the main session with tests that fail without them: **(a)** takes the **oldest** same-day spec commit that touches the task file (a later one may carry another edit; supersedes "newest" above); **(b)** applies only when the task was not yet Finished at its file's first commit (a file first committed as Finished, by a bulk commit or a rename, proves nothing). For an open task (b) still assumes the file was committed soon after it was written; check 11 says so. Real data unchanged by both. 387 tests on 3.10 and 3.13.
