# Scenario 51 — Every task carries section provenance; a baseline for those that don't (FB-135)

Conceptual trace test for v5.13.0. Every task-creation path stamps section provenance when it writes the task (`fingerprint.py --provenance`), or marks the task `spec_unmapped: true` or `out_of_spec: true`. Tasks created earlier without a `section_fingerprint` get a one-time baseline from `/health-check` Part 1 check 11: `fingerprint.py --baseline` proposes, per task, the hash its section had in the spec's git history at the task's date, and `--baseline --write` stamps it. Where history can't date a task, the user confirms or names the section; the script never guesses.

## Setup / State

- A downstream project at v5.13.0 or later. `python3` is available. The current spec is `.claude/spec_v2.md` with `## ` sections `## Import`, `## Reports`, `## Search` and `## Export`.
- Unless a trace says otherwise, the spec is tracked by git and three commits touch it:

  | Commit | Committer date | Change |
  |---|---|---|
  | `a1b2c3d` | 2026-07-01 | spec_v2 created |
  | `d4e5f6a` | 2026-08-20 | `## Reports` edited |
  | `b7c8d9e` | 2026-09-10 | `## Export` edited |

- Tasks from decomposition carry full provenance and are in sync. The tasks each trace lists were created outside decomposition before v5.13.0: they have `spec_version: "spec_v2"` unless stated, no `section_fingerprint` and no `section_snapshot_ref`.
- No `drift-deferrals.json`. No other part of `/health-check` queues a row.
- Each trace starts from this state, not from the previous trace.

## Trace A — baseline from history: bare `[A]` stamps, and the hidden drift shows up

Command path: `commands/health-check.md § "11. Provenance Integrity"` (Section provenance baseline) → `§ "Step 4: Batch Fix Triage"` → next `/work`: `commands/work.md § "Step 1b"` → `drift-reconciliation.md § "Granular Reconciliation UI"`.

State:

| Task | Status | Date used | `spec_section` |
|---|---|---|---|
| 31 | Finished | `completion_date: 2026-08-05` | `Import` (no `## `), and no `spec_version` |
| 32 | Finished | no `completion_date`; `task_verification.timestamp: 2026-08-05T14:10:00Z`, `updated_date: 2026-09-02` | `## Reports` |
| 33 | Pending | `created_date: 2026-09-01` | `## Reports` |

1. `python3 .claude/scripts/fingerprint.py --drift .claude` (before): `no_provenance: 3`, `unmapped: 0`, nothing drifted. `validate-tasks.py` prints `Provenance: 3 task(s) without section provenance (see /health-check Part 1 check 11)`.
2. Check 11 runs `python3 .claude/scripts/fingerprint.py --baseline .claude`. Output (excerpt; `file`, `title` and `reason` omitted):
   ```json
   {
     "spec": "spec_v2", "history": "git",
     "tasks": [
       {"id": "31", "status": "Finished", "recorded_section": "Import", "action": "stamp_history",
        "spec_section": "## Import", "section_fingerprint": "sha256:<Import at a1b2c3d>",
        "reference_date": "2026-08-05", "reference_field": "completion_date",
        "commit": "a1b2c3d…", "commit_date": "2026-07-01",
        "changed_since": false, "same_day_edit": false},
       {"id": "32", "status": "Finished", "recorded_section": "## Reports", "action": "stamp_history",
        "spec_section": "## Reports", "section_fingerprint": "sha256:<Reports at a1b2c3d>",
        "reference_date": "2026-08-05", "reference_field": "task_verification.timestamp",
        "commit": "a1b2c3d…", "commit_date": "2026-07-01",
        "changed_since": true, "same_day_edit": false},
       {"id": "33", "status": "Pending", "recorded_section": "## Reports", "action": "stamp_history",
        "spec_section": "## Reports", "section_fingerprint": "sha256:<Reports at d4e5f6a>",
        "reference_date": "2026-09-01", "reference_field": "created_date",
        "commit": "d4e5f6a…", "commit_date": "2026-08-20",
        "changed_since": false, "same_day_edit": false}
     ],
     "counts": {"stamp_history": 3, "confirm_current": 0, "needs_section": 0, "report_only": 0}
   }
   ```
   Task 32 was verified before the 2026-08-20 edit to `## Reports`, so its hash is the older one; its later `updated_date` is not used (it would date the task after the edit and hide it). Task 31 has no `spec_version` but is younger than the spec file's first commit, so history dates it. Task 33 was created after that edit, so its hash is the current one.
3. The report gives the four counts. The table has one row for the three tasks, file `.claude/tasks/ (3 files)`, risk `—`:
   `Stamp section provenance on 3 tasks from the spec's history (1 will then show as drift: their section changed after the task)`
4. The user answers `A`. The row applies: `python3 .claude/scripts/fingerprint.py --baseline .claude --write --ids 31,32,33`. Output: three `written` entries, `unchanged: []`.
5. Each task file now has `spec_section` (Task 31: `## Import`, the real heading), `section_fingerprint`, and a note prepended to `notes`, e.g. `[BASELINE] section_fingerprint stamped from the spec at a1b2c3d (2026-07-01); the task records no hash of its own.` Task 31 also gets `spec_version: "spec_v2"`. `updated_date`, `spec_fingerprint`, status and verification fields are as they were, and key order and indentation are unchanged.
6. The post-apply summary says that one task now differs from its section and that the next `/work` lists `## Reports` under Drift Reconciliation, where `[K]` keeps verified work. The batch regenerates the dashboard once: Needs-you → Spec Drift shows `## Reports changed since its tasks were built (1 Finished) → run /work to reconcile`.
7. Next `/work`, Step 1b: `no_provenance: 0`; `## Reports` is under `drifted` with Task 32 only (Task 33 is in sync); `unreconciled_sections: 1`.
8. Drift Reconciliation shows the section prompt for `## Reports`. Task 32 has no `section_snapshot_ref`, but its `[BASELINE]` note names the commit it was stamped from, so the prompt shows the diff of `## Reports` since then (`git diff a1b2c3d -- .claude/spec_v2.md`, cut to the section). The user reads it, sees the edit didn't change what Task 32 built, and picks `[K]`: fingerprints refreshed, a `[DRIFT KEPT …]` note prepended, status and `task_verification` untouched.
9. Running the baseline again proposes nothing (all counts 0).

**Expected:** bare `[A]` gives all three tasks provenance without a question, because the spec's history says which text each was built against. The one task whose section changed afterwards surfaces as drift on the next `/work`, and the user settles it there.

**Pass criteria:** one `—` row covers every `stamp_history` task and names how many will show as drift; the write goes through `--baseline --write --ids`, never a hand edit; Task 32 gets the 2026-07-01 hash, not the current one, dated by its verification timestamp and not by `updated_date`; the reconciliation prompt for it shows a diff against `a1b2c3d`; Task 31's bare `Import` becomes `## Import`; `updated_date` is unchanged; the dashboard is regenerated after the write; the next `/work` reports `## Reports` with Task 32 and not Task 33; `[K]` leaves Task 32 Finished and verified.

**Fail indicators:** the current section hash stamped on Task 32 (the edit after it would then be invisible for good); the current section text shown without a diff for a task whose `[BASELINE]` note names a commit; one row per task; a `needs-input` row for tasks the history can date; `updated_date` bumped (a phase-level verification result would be invalidated); the drift on Task 32 applied or kept without the user's pick.

## Trace B — the spec isn't in git: the user confirms, or nothing is stamped

Command path: `commands/health-check.md § "11. Provenance Integrity"` → `§ "Step 4: Batch Fix Triage"`.

State: `.claude/spec_v2.md` is not tracked by git. Tasks 41 and 42 (Finished) and 43 (Pending) name `## Search`.

1. `--baseline .claude`: `history: "none"`. All three tasks are `confirm_current`: `spec_section: "## Search"`, `section_fingerprint` is the **current** hash, `commit` is `null`, and `reason` says the spec has no git history. `counts.confirm_current: 3`.
2. The table has one `needs-input` row (say id 5): `3 tasks name a section but the spec has no history to date them ({reason summary}). Stamp the current section text as what they were built against? (yes / no / list of ids)`
3. The user answers `A`. Bare `[A]` skips `needs-input` rows: nothing is written, and the summary lists row 5 as still open.
4. On a later run the user answers `5: yes`: `python3 .claude/scripts/fingerprint.py --baseline .claude --write --ids 41,42,43 --confirm-current`. Each task gets the current hash and the note `[BASELINE] section_fingerprint set to the current section text on <today>, confirmed by the user as what the task was built against.`

Variant, a list: `5: 41,43` writes only those two with `--confirm-current`. Task 42 stays in `no_provenance` and the row returns on the next run with 1 task.

Variant, `5: no`: nothing is written; the three tasks stay in `no_provenance`.

Variant, the flag is left out: `--baseline .claude --write --ids 41` exits 2 naming id 41, and no file changes.

Variant, the row is applied twice: after `5: yes`, the same `--write --ids 41,42,43` call reports all three under `unchanged` and exits 0.

Variant, a task older than the spec file: the spec is tracked (the Setup commits). Task 44 (Finished, `completion_date: 2026-06-20`, no `spec_version`) names `## Search`. It is dated before `a1b2c3d`, the first commit of `spec_v2.md`, and nothing says it was built against spec_v2: `confirm_current` with `reason: "the task may predate this spec version"`. It gets its own `needs-input` row: `1 tasks are older than the spec's history for their section (the task may predate this spec version: 1). The current text is not what they were built against; accept it as their baseline anyway? (yes / no / list of ids)`. A yes applies with `--confirm-current` and the note ends `accepted by the user as the task's baseline.` The same holds for a task dated 2026-07-01 itself. With `spec_version: "spec_v2"`, a task dated 2026-06-20 lands on the same row with `reason: "no spec commit on or before the task's date"`, and one dated 2026-07-01 is `stamp_history` at `a1b2c3d`.

**Expected:** with no history the only available hash is the current one, and stamping it asserts "this text is what the tasks were built against". Only the user can assert that, as with `[K]`.

**Pass criteria:** one `needs-input` row for the undated `confirm_current` tasks and a separate one, worded as accepting a baseline, for tasks older than the spec's history; bare `[A]` writes nothing for either; `yes` applies with `--confirm-current`; a list of ids applies only those; the note records what the user asserted (confirmed, or accepted as baseline).

**Fail indicators:** `confirm_current` tasks folded into the `—` row; `--confirm-current` passed without a yes; the orchestrator writing the current hash into the task files itself after the script exits 2.

## Trace C — no resolvable section: the user names one, or says unmapped

Command path: `commands/health-check.md § "11. Provenance Integrity"` → `§ "Step 4: Batch Fix Triage"` → `task-schema.md § "Drift Prevention Fields"` (creation contract).

State: Task 51 (On Hold) has `spec_section: "§ 3.1 (filters) + § 3.6 (sorting)"`. Task 52 (Pending) has no `spec_section`. Task 53 (Finished) has `spec_section: "§ 4 export, misc"`.

1. `--baseline .claude`: Tasks 51 and 52 are `needs_section`, Task 53 is `report_only`; for all three `spec_section`, `section_fingerprint` and `commit` are `null`. `counts`: `needs_section: 2`, `report_only: 1`.
2. Report line: `ℹ️ 1 finished tasks name no resolvable spec section; drift can't be checked for them`. No row for Task 53.
3. Two `needs-input` rows (say ids 3 and 4): `Task 51 "{title}" names no resolvable spec section: which section, or unmapped?` and the same for Task 52.
4. The user answers `3: Search, 4: unmapped`.
   - Row 3: `python3 .claude/scripts/fingerprint.py --provenance .claude --section "Search"` prints `{"spec_version": "spec_v2", "spec_fingerprint": "sha256:…", "spec_section": "## Search", "section_fingerprint": "sha256:…"}`. The four fields are written to Task 51; its free-form value is replaced by `## Search`.
   - Row 4: Task 52 gets `spec_unmapped: true`.
   - `updated_date` is unchanged on both.
5. `--drift .claude` afterwards: `no_provenance: 1` (Task 53), `unmapped: 1` (Task 52); Task 51 is checked and in sync.
6. The next `/health-check` proposes nothing for Tasks 51 and 52. Task 53 still gives the `ℹ️` line.

Variant, the answer isn't a heading: `3: Filters` → `--provenance` exits 1 with `error: no current spec heading matches 'Filters'`. Nothing is written; row 3 stays open and the summary lists the real headings.

**Expected:** a task whose section can't be resolved gets one from the user or is declared unmapped. A Finished task with a free-form section is reported and left alone.

**Pass criteria:** one `needs-input` row per `needs_section` task; no row for `report_only`; a heading answer goes through `--provenance` and the task stores the real heading; `unmapped` sets `spec_unmapped: true` and the task moves from `no_provenance` to `unmapped`; an unresolvable answer writes nothing.

**Fail indicators:** the orchestrator guessing `## Search` for Task 51 from its free-form text without asking; the free-form value kept beside a fingerprint; Task 53 stamped with any hash; `Filters` written as `spec_section`.

## Trace D — new tasks are created with provenance

Command path: `work-procedures.md § "State Persistence Protocol"`: "After verify-agent returns (phase-level mode)" step 2 → `commands/work.md § "Step 2: Spec Check"` → `§ "Step 3: Determine Action"` → `task-schema.md § "Drift Prevention Fields"` (creation contract).

State: every existing task has provenance. Phase-level verification returns `result: "fail"` with three `fix_tasks_to_create[]` entries:

| Entry | `task_json` | `out_of_spec` |
|---|---|---|
| 1 | `spec_section: "## Export"` | false |
| 2 | `spec_section: "Export — CSV edge cases"` | false |
| 3 | neither `spec_section` nor `spec_unmapped` | true |

1. Entry 1: `--provenance .claude --section "## Export"` exits 0. Its four fields are merged into the payload and the task file is written.
2. Entry 2: `--provenance .claude --section "Export — CSV edge cases"` exits 1 with `error: no current spec heading matches 'Export — CSV edge cases'`. The orchestrator reads the spec index, sees the fix belongs to `## Export`, runs `--provenance` on that heading and writes the task with `spec_section: "## Export"`. Its `notes` say the verifier's value didn't resolve and which section was chosen.
3. Entry 3 is a recommendation: written with `out_of_spec: true` and no section fields.
4. Later in the session the user asks `/work add a retry to the importer`. Step 2 finds it aligned with `## Import`. Step 3 creates the task with the fields from `--provenance .claude --section "## Import"`.
5. The user then asks `/work run the formatter across the repo`: a minor request that belongs to no single section. The task is created with `spec_unmapped: true`, `spec_version: "spec_v2"` and no `spec_section`.
6. `--drift .claude`: `no_provenance: 0`, `unmapped: 1`. `validate-tasks.py` prints `Provenance: OK`.

Variant: entry 2 with `spec_unmapped: true` in place of the free-form heading is written as it is, with no `--provenance` call.

**Expected:** no task written under v5.13.0 lands in `no_provenance`, whichever path created it.

**Pass criteria:** fix tasks 1 and 2 carry `spec_version`, `spec_fingerprint`, `spec_section` and `section_fingerprint` for a real heading; the free-form value is never written; the substitution is noted on the task; the recommendation carries only `out_of_spec: true`; the user-request task has the `## Import` fields; the formatter task is `spec_unmapped`; a later edit to `## Export` reports both fix tasks as drift.

**Fail indicators:** the verifier's `task_json` written as returned (the pre-v5.13.0 behaviour); `spec_section: "Export — CSV edge cases"` on disk; a hash computed by verify-agent; `spec_unmapped: true` used to avoid looking up a section that plainly applies; `out_of_spec: true` on the formatter task (it is in-spec work, needing no approval).

## Trace E — a spec edit on the task's own date (`same_day_edit`)

Command path: `scripts/fingerprint.py --baseline .claude` → `commands/health-check.md § "11. Provenance Integrity"`.

State: commit `d4e5f6a` (2026-08-20) edited `## Reports`. Four tasks have that date as their reference date:

| Task | Status, date | `spec_section` | Its file in git |
|---|---|---|---|
| 61 | Finished, `completion_date: 2026-08-20` | `## Reports` | committed on 2026-08-10; `d4e5f6a` doesn't touch it |
| 62 | Finished, `completion_date: 2026-08-20` | `## Import` | the same |
| 63 | Finished, `completion_date: 2026-08-20`, `files_affected` includes `.claude/spec_v2.md` | `## Reports` | committed on 2026-08-10, and changed again in `d4e5f6a` |
| 64 | Pending, `created_date: 2026-08-20` | `## Reports` | first committed on 2026-08-21, after `d4e5f6a` |

1. `--baseline .claude`, Task 62: `## Import` has the same hash at `d4e5f6a` and at `a1b2c3d`, so nothing about it changed that day: `commit: "d4e5f6a…"`, `same_day_edit: false`, `changed_since: false`. No further git call is made for it.
2. Tasks 61, 63 and 64: the hash of `## Reports` at `d4e5f6a` differs from its hash at the newest commit dated strictly before 2026-08-20 (`a1b2c3d`), so the section was edited on the task's own date and a date can't say which came first. All three get `same_day_edit: true`; git evidence about the task's own file picks the commit, first match wins:
   - **(a) own edit, Task 63:** its `files_affected` names the spec, and `d4e5f6a` also touches `task-63.json`. The edit was this task's work: `commit: "d4e5f6a…"`, `reason: "own spec edit"`, `changed_since: false`.
   - **(b) filed after the edit, Task 64:** `task-64.json` first enters git after `d4e5f6a`, still Pending, so it is taken as written with the edit in place (this assumes the file was committed soon after it was written): `commit: "d4e5f6a…"`, `reason: "task filed after the edit"`, `changed_since: false`.
   - **(c) neither, Task 61:** its file was in git before the edit and the edit's commit leaves it alone. The script takes the earlier commit: `commit: "a1b2c3d…"`, `commit_date: "2026-07-01"`, `reason: ""`, `changed_since: true`.
3. All four are `stamp_history`. The row reads `Stamp section provenance on 4 tasks from the spec's history (1 will then show as drift: their section changed after the task)`.
4. After `A`, the next `/work` reports `## Reports` with Task 61 only. If the task was in fact built against the edited text, the user picks `[K]`; if not, `[V]` or `[A]`.

Variant, several spec commits that day: a second commit `e9f0a1b`, later on 2026-08-20, edits `## Reports` again and touches no task file. Task 63 is still stamped at `d4e5f6a`, the oldest commit of the day that touches its own file, and now has `changed_since: true`: the later edit is shown to the user. Task 64 (filed after both) is stamped at `e9f0a1b`.

Variant, task files not in git (`.claude/tasks/` ignored or never committed): there is no evidence, so Tasks 63 and 64 fall to (c) like Task 61, and the row reads `(3 will then show as drift …)`.

**Expected:** a same-day spec edit is ordered against the task from git evidence where there is some. Where there is none, the baseline takes the older text, so the edit is shown to the user once instead of being assumed away.

**Pass criteria:** Task 61 gets the pre-edit hash and counts in the row's drift number; Tasks 63 and 64 get the post-edit hash with their `reason`; `same_day_edit` is true on all three; Task 62 is unaffected by a same-day commit that didn't touch its section; with no tracked task files every same-day case is (c).

**Fail indicators:** Task 61 stamped with the post-edit hash; Task 63's own edit reported back to the user as drift; (a) applied to a task whose `files_affected` doesn't name the spec; `same_day_edit` true on Task 62; any of them moved to a `needs-input` row.

## Invariant checks

- A task has section provenance (`spec_section` + `section_fingerprint`), or `spec_unmapped: true`, or `out_of_spec: true`. Every creation path writes one of the three with the task.
- `spec_section` on a new or baselined task is always a real current heading, as `--provenance` or `--baseline` returned it. A free-form value is never written.
- `--provenance` and `--baseline` without `--write` write nothing.
- `--baseline --write` changes only `spec_section`, `section_fingerprint`, a missing `spec_version` and `notes`. It never touches `updated_date`, `spec_fingerprint`, status or verification fields.
- The current section hash is stamped on an existing task only after the user's yes (`--confirm-current`), and the note says whether the user confirmed it as what the task was built against or accepted it as a baseline. `needs_section` and `report_only` tasks are never stamped by the script, and nobody stamps by hand what the script declined.
- The baseline never applies or keeps drift. It makes drift visible; `/work`'s Drift Reconciliation, with the user's pick, settles it.
- `spec_unmapped: true` on a task that has both section fields changes nothing in the drift check; `validate-tasks.py` and check 11 warn about it.
