# Scenario 50 — Template sync classifies files by template history (FB-136)

Conceptual trace test for v5.12.0. `/health-check` Part 5 takes each sync file's status from `sync-check.py`'s `files[]`. A file whose content equals any template version of its path is an Unchanged template copy: a `—` row, applied by bare `[A]`, whatever the sync-state sidecar says. Only a file that matches no template version is Locally modified (`⚠ overwrites local`). The sidecar is the fallback when template history is shallow. `sync-apply.py` does the writing. Stale local manifest lists and a sidecar that isn't gitignored each get a row. A project that isn't a git repository syncs through a temporary clone.

## Setup / State

- A downstream project whose commands and scripts are at v5.12.0 or later (the first sync into v5.12.0 runs the project's older Part 5); the template's default branch is at v5.14.0. `python3` is available. The compare set holds 85 upstream files.
- Unless a trace says otherwise: the project is a git work tree with a clean working tree, the `template` remote exists and `git fetch template` succeeds with full history, `.claude/.sync-state.json` is listed in `.gitignore`, the local `customize` and `ignore` lists equal the upstream ones, file modes match, nothing is retired, and no other part queues a row.
- Each trace starts from this state, not from the previous trace.

## Trace A — 45 unchanged copies, 7 new files, no sidecar: bare `[A]` applies all

Command path: `commands/health-check.md § "Part 5: Template Sync Check"` → `§ "2. Compare Sync Files"` → `§ "3. Present Changes (report) and Queue Apply Rows"` → `§ "Step 4: Batch Fix Triage"` → `§ "4. Apply Updates"` → `§ "5. Commit Offer"`.

State: 33 of the 85 files equal the template's current copy. 45 differ from it, and each of those is byte-identical to an earlier template version of its path (the project never edited them). 7 don't exist locally. There is no `.claude/.sync-state.json`.

1. Step 2 runs `python3 .claude/scripts/sync-check.py --ref template/main`. `history_complete` is true. `files[]` has 85 entries: 33 `up_to_date`, 45 `template_copy`, 7 `new`, 0 `modified`. Two of them:
   ```json
   {"path": ".claude/commands/work.md", "status": "template_copy", "mode": "100644",
    "mode_matches": true, "version": "5.12.0", "basis": "history", "shared_lines": null},
   {"path": ".claude/support/reference/new-feature.md", "status": "new", "mode": "100644",
    "mode_matches": null, "version": null, "basis": null, "shared_lines": null}
   ```
   `sidecar` is `{"exists": false, "gitignored": true, "tracked": false}`. The missing sidecar produces no warning.
2. Report (shortened):
   ```
   Template updates available (v5.12.0 → v5.14.0):

     Unchanged template copies (no local edits):
       .claude/commands/work.md (copy of v5.12.0)
       .claude/rules/agents.md (copy of v5.6.0)
       … 43 more

     New:
       .claude/support/reference/new-feature.md
       … 6 more
   ```
   There is no Locally modified group.
3. The table has 52 rows, all risk `—`: 45 `Update template file (unchanged copy of v{version})` and 7 `Add new template file`.
4. The user answers `A`. All 52 rows apply.
5. Step 4b: the 52 paths go into a file, one per line, and `python3 .claude/scripts/sync-apply.py --ref template/main --paths-from <file>` runs once. Its output (excerpt):
   ```json
   {
     "dry_run": false,
     "mode_fixed": [],
     "failed": [],
     "version": {"from": "5.12.0", "to": "5.14.0", "bumped": true},
     "sidecar": {"recorded": 85, "dropped": 0, "created": true, "changed": true},
     "remaining": [],
     "warnings": []
   }
   ```
   `written` has 52 entries. `.claude/version.json` now carries v5.14.0's `template_version` and `template_release_date`. The sidecar is created with 85 `files` entries: the 52 written files and the 33 that already matched.
6. Step 5: `changed_paths` holds the 52 files, `.claude/version.json`, `.claude/sync-manifest.json` (the upstream `sync` list gained entries) and `.claude/.sync-state.json`. The sidecar is gitignored and drops out. The offer lists 54 paths (45 `M` and 7 `A` sync files, `M .claude/sync-manifest.json`, `M .claude/version.json`) with `[C] Commit as "Sync template v5.12.0 → v5.14.0"`.

**Expected:** before v5.12.0 a differing file with no sidecar entry was treated as a local edit: all 45 rows would have been `⚠ overwrites local`, bare `A` would have applied only the 7 new files, and the user would have been asked to adjudicate 45 diffs containing no local change. Now one `A` brings the project to v5.14.0.

**Pass criteria:** no row is `⚠`; the 45 copies are classified without a sidecar; one `sync-apply.py` call writes all 52 files; the sidecar has 85 entries, including the 33 files the run did not write; `template_release_date` is updated together with `template_version`; the commit offer excludes the sidecar.

**Fail indicators:** a per-file `git diff` loop or a `shasum` call used for classification; a `⚠ overwrites local` row for a file that equals a template version; sidecar entries only for the files written.

## Trace B — a file that is not a variant of the template file

Command path: `§ "2. Compare Sync Files"` → `§ "3. Present Changes (report) and Queue Apply Rows"` → `§ "Step 4: Batch Fix Triage"` → `§ "4. Apply Updates"`.

State: 82 files are up to date. `.claude/rules/agents.md` is an unchanged copy of v5.6.0. `.claude/commands/work.md` carries a project edit of a few lines. `.claude/support/reference/merge-queue.md` holds the project's own merge queue (pending items and an applied log), written at the template's path; the file is gitignored in this project, so there is no other copy.

1. `files[]` (the three entries that aren't `up_to_date`; `mode` `100644`, `mode_matches` true in each):

   | `path` | `status` | `version` | `basis` | `shared_lines` |
   |---|---|---|---|---|
   | `.claude/rules/agents.md` | `template_copy` | `5.6.0` | `history` | `null` |
   | `.claude/commands/work.md` | `modified` | `null` | `null` | `0.97` |
   | `.claude/support/reference/merge-queue.md` | `modified` | `null` | `null` | `0.03` |
2. Report: `agents.md` under Unchanged template copies; `work.md` and `merge-queue.md` under Locally modified (review before including).
3. Table:
   ```
   | # | Part | File | Proposed fix | Risk |
   |---|------|------|--------------|------|
   | 1 | 5 | .claude/rules/agents.md | Update template file (unchanged copy of v5.6.0) | — |
   | 2 | 5 | .claude/commands/work.md | Update template file (locally modified, [D] shows the diff) | ⚠ overwrites local |
   | 3 | 5 | .claude/support/reference/merge-queue.md | Update template file (local content is not a variant of the template file: 3% of its lines appear in any template version; move it to a project-*.md file before including) | ⚠ overwrites local |
   ```
   Row 3 gets the not-a-variant text because `shared_lines` is not null and below 0.25. Row 2, at 0.97, gets the plain text.
4. The user answers `A`. Row 1 applies. Rows 2 and 3 are listed back as still open, and `merge-queue.md` is untouched.
5. `sync-apply.py` gets a paths file with the one line `.claude/rules/agents.md`. Its `remaining` lists the two `modified` files. The version is bumped (a file's content was written), and Step 5's message is `Sync template v5.12.0 → v5.14.0 (partial: 2 sync files not updated)`.
6. Later the user copies the queue content to `.claude/support/reference/project-merge-queue.md` (an `ignore` path, never compared), leaving `merge-queue.md` in place, and answers `A include 3` on the next run (the row is unchanged: the file is still `modified`). The script writes the template's `merge-queue.md` over it.

Variant, boundary: a `modified` file with `shared_lines` `0.25` gets the plain "locally modified" row; the test is below 0.25. A `modified` path that is a symlink or directory has `shared_lines: null` and also gets the plain row; if its row is included, `sync-apply.py` refuses it and it is reported as a failed row.

**Expected:** the only copy of the project's data is not overwritten by a default answer, and the row says what to do with it before the user ever opens a diff.

**Pass criteria:** rows 2 and 3 are `⚠ overwrites local` and excluded from bare `A`; row 3 carries `3%` and the move instruction; row 1 applies under bare `A` in the same run; a `modified` file can reach `sync-apply.py` only through `--paths-from`.

**Fail indicators:** `merge-queue.md` written by a bare `A`; `--status modified` passed to the script (a usage error).

## Trace C — shallow template history: the sidecar classifies

Command path: `§ "Sync State Sidecar"` → `§ "2. Compare Sync Files"` → `§ "3. Present Changes (report) and Queue Apply Rows"`.

State: the `template` remote was fetched with `--depth 1`, so the only template version of each path the history holds is the current one. `.claude/commands/work.md` and `.claude/rules/agents.md` both differ from it; neither was edited by the project. The sidecar, written by an earlier sync, has a `synced_hash` for `work.md` that equals the file's current hash, and no entry for `agents.md`.

1. `sync-check.py` reports `history_complete: false` and the warning `template history is shallow; files it cannot place are classified from the sync-state sidecar`.
2. `work.md`: its blob id is not among the path's template blob ids (history holds one), but its hash equals the sidecar's `synced_hash` → `status: "template_copy"`, `basis: "sidecar"`, `version: null`.
3. `agents.md`: no template version matches and there is no sidecar entry → `status: "modified"`.
4. Report: `work.md` under Unchanged template copies with `(unchanged since the last sync)`; `agents.md` under Locally modified; and the line
   `ℹ️ Template history is shallow: files it can't place are classified from the sync-state sidecar; "Locally modified" may include unchanged copies. git fetch --unshallow template gives the full answer.`
5. Table: row 1 `Update template file (unchanged since the last sync)` for `work.md`, risk `—`; row 2 `Update template file (locally modified, [D] shows the diff)` for `agents.md`, risk `⚠ overwrites local`.
6. The user runs `git fetch --unshallow template` and then `/health-check` again. `history_complete` is true, no warning, and both files are `template_copy` with `basis: "history"` and a version; both rows are `—`.

Variant, unreadable sidecar: the sidecar is not valid JSON. The script warns `sync-state sidecar unreadable; ignored` and both files are `modified` while history is shallow. The next `sync-apply.py` run replaces the sidecar.

**Expected:** with history missing, the sidecar still spares the user a diff for every file it recorded, and the report says why the Locally modified group may be too large and how to fix that.

**Pass criteria:** the sidecar is consulted only while history is shallow, and only for a file that matches no template version; a sidecar match gives a `—` row with the "unchanged since the last sync" text; the `ℹ️` line appears exactly when `history_complete` is false; a file with neither a history match nor a sidecar match is `⚠`, never applied by default.

## Trace D — stale manifest lists and a sidecar that isn't gitignored

Command path: `§ "2. Compare Sync Files"` → `§ "3. Present Changes (report) and Queue Apply Rows"` → `§ "4. Apply Updates"` → `§ "5. Commit Offer"`.

State: the project is already on v5.14.0 and all 85 files are `up_to_date`. The local `ignore` list still has `.claude/dashboard.md`, lacks `.claude/dashboard.html`, and has one entry the project added, `.claude/support/data/*.csv`. `.claude/.sync-state.json` exists, is untracked and is not in `.gitignore`.

1. `sync-check.py`:
   ```json
   "manifest": {
     "customize": {"add": [], "drop": [], "list": ["…"]},
     "ignore": {"add": [".claude/dashboard.html"], "drop": [".claude/dashboard.md"],
                "list": ["…", ".claude/support/data/*.csv"]}
   },
   "sidecar": {"exists": true, "gitignored": false, "tracked": false}
   ```
   `ignore.list` is the upstream list followed by the project's own entry. `.claude/dashboard.md` is in `drop` because the template once listed it under `ignore`; the `.csv` entry was never a template entry, so it is neither dropped nor reported.
2. Report: `✓ Template up to date (v5.14.0)`. Table:
   ```
   | # | Part | File | Proposed fix | Risk |
   |---|------|------|--------------|------|
   | 1 | 5 | .claude/sync-manifest.json | Update local manifest lists (add .claude/dashboard.html; drop .claude/dashboard.md) | — |
   | 2 | 5 | .gitignore | Add .claude/.sync-state.json to .gitignore | — |
   ```
3. The user answers `A`. Step 4b runs `python3 .claude/scripts/sync-apply.py --ref template/main --manifest-lists` with no `--paths-from` (no file row was included). It writes the manifest's `ignore` list from `manifest.ignore.list`; `written` is empty and `version.bumped` is false.
4. Step 4c appends `.claude/.sync-state.json` to `.gitignore`. No `git rm --cached`: the file isn't tracked.
5. Step 5: `M .claude/sync-manifest.json` and `M .gitignore`, with the message `Sync template files (v5.14.0)`. The sidecar is not listed.

Variant D2, tracked sidecar: `sidecar` is `{"exists": true, "gitignored": false, "tracked": true}`. Row 2 reads `Stop tracking .claude/.sync-state.json and add it to .gitignore`. Step 4c runs `git rm --cached -q -- .claude/.sync-state.json` (the file stays on disk), then appends the line. Step 5 lists `D .claude/.sync-state.json` as well. On `[C]` the sidecar is moved out of the project for the duration of the commit and moved back afterwards; committed in place, `git commit -- <paths>` would re-add the file and it would stay tracked. After the commit, `git ls-files --error-unmatch -- .claude/.sync-state.json` fails and the file is on disk, ignored.

Variant D3, row 2 excluded (`A except 2`): the manifest row applies, and the sidecar stays untracked and un-ignored. Step 5 does not list it (it never adds the sidecar to git), and the next run queues row 2 again.

**Expected:** the local manifest describes the project again without losing the project's own entries, and the sidecar stops showing up in `git status`.

**Pass criteria:** one manifest row covers both lists; the project-added entry survives; a run with no file row doesn't bump the version; the sidecar row's wording follows `sidecar.tracked`; the sidecar is never committed as an addition or modification, and in D2 it is no longer tracked after `[C]`.

**Fail indicators:** `.claude/support/data/*.csv` removed from `ignore`; `Sync template v… → v…` as the message for a run that wrote no sync file; the sidecar still tracked after D2's commit; the sidecar file deleted from disk.

## Trace E — a project that isn't a git repository

Command path: `§ "1. Setup Remote"` (non-git project) → `§ "2. Compare Sync Files"` → `§ "3. Present Changes (report) and Queue Apply Rows"` → `§ "4. Apply Updates"` → `§ "5. Commit Offer"` (skipped).

State: the project directory has no git repository. `.claude/rules/agents.md` is an unchanged copy of v5.6.0, `.claude/commands/work.md` carries a project edit, `.claude/skills/dashboard-style/SKILL.md` is an unchanged copy of a file the template removed in v4.12.0, and the other 83 compare-set files are up to date. The sidecar exists.

1. Step 1: `git rev-parse --is-inside-work-tree` fails. No remote is added and no `git init` runs. `git clone --quiet {template_repo} "$TMP/template"` clones the template, with full history, into a temporary directory outside the project.
2. Step 2: `python3 .claude/scripts/sync-check.py --template-repo "$TMP/template" --ref origin/HEAD`. Output: `git: false`, `uncommitted_sync: []`, the warning `project is not a git work tree; uncommitted_sync skipped`, `history_complete: true`, and `sidecar` `{"exists": true, "gitignored": null, "tracked": null}`. Classification is the same as in a git project: `agents.md` `template_copy`, `work.md` `modified`.
3. Table: row 1 `Update template file (unchanged copy of v5.6.0)` (`—`), row 2 `Update template file (locally modified, [D] shows the diff)` (`⚠ overwrites local`), row 3 `Remove retired template file (removed upstream in v4.12.0; unchanged template copy)` (`⚠ deletes`). No `.gitignore` row: it is not queued for a non-git project.
4. `[D] 2` prints `git -C "$TMP/template" show origin/HEAD:.claude/commands/work.md | diff -u - .claude/commands/work.md`.
5. The user answers `A include 3`. Step 4a removes the skill file with `rm --` (nothing is tracked) and prunes its empty directory. Step 4b runs `python3 .claude/scripts/sync-apply.py --template-repo "$TMP/template" --ref origin/HEAD --paths-from <file>` with the one path `.claude/rules/agents.md`. Row 2 stays open.
6. Step 5 is skipped: there is nothing to commit to.
7. The clone at `$TMP/template` is deleted when the run ends. The project directory holds no `.git` and no clone.

Variant, clone fails (offline, invalid URL): the report shows `⚠️ Cannot reach template repository — skipping template sync` and the remaining sync steps are skipped.

**Expected:** before v5.12.0 Part 5 needed the project to be a git repository (it added a remote to it). A non-git project now gets the same classification and the same rows.

**Pass criteria:** no remote is added and no repository is created in the project; both scripts get `--template-repo` and `--ref origin/HEAD`; no `.gitignore` row and no commit offer; the temporary clone is outside the project and is deleted.

**Fail indicators:** `git init` or `git remote add` in the project; a `--depth` clone (the history is what classifies); the clone left behind, or created inside the project.

## Invariant checks

- A file whose content equals any template version of its path is never `⚠ overwrites local`, with or without a sidecar entry.
- A file that matches no template version (and, when history is shallow, no sidecar entry) is never written without explicit inclusion of its row.
- The sidecar never overrides history: it is read only when the template history is shallow, and then only for a file history can't place. With the whole history, a sidecar entry never makes a file an unchanged copy.
- `sync-check.py` writes nothing. `sync-apply.py` writes only inside `.claude/`, and only compare-set files, `version.json`, `sync-manifest.json` and the sidecar; retired-file removal, `.gitignore`, `git rm --cached`, staging and committing stay with Part 5's prose steps.
- `template_version` and `template_release_date` change together, and only when a sync file's content was written, or when every compare-set file equals upstream and the local version differs (the re-run after an interrupted run).
- After Step 4 the sidecar has an entry for every compare-set file that equals upstream, and no other entry, except one a shallow-history classification still rests on (the file was not updated in the run).
- Project-added entries in the local `sync`, `customize` and `ignore` lists that the template lists in no category survive every run.
- `--report` runs `sync-check.py` and nothing else: no rows, no `sync-apply.py`, no commit offer.
