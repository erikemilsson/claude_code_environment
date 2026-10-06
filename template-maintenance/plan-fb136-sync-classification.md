# Plan: v5.12.0 — sync classification by template blob history (FB-136)

**Status:** IMPLEMENTED in v5.12.0 (2026-10-06); see ship-log. Contract amended A1–A10; review fixes R1–R8 and re-verify nits below. Originally APPROVED 2026-10-06 (decisions 1–8: template copies apply under bare `[A]`; the script reads the sidecar; manifest row rewrites `customize`/`ignore`; tracked sidecar gets an untrack offer; `shared_lines` < 0.25; non-git path ships; `sync-apply.py` ships; v5.12.0 minor).
**Target:** v5.12.0 (minor: new `sync-check.py` output keys, new writer script, template copies apply by default, two new row types, non-git sync path).
**Scope:** FB-136 (a)–(e); classification half of FB-127 (p); FB-127 (q).

## Survey (2026-10-06, read-only)

- **Live, `--ref v5.11.0`:** all 9 projects 85/85 `up_to_date`; no retired patterns or files; no mode mismatch; sidecars complete. `uncommitted_sync` = 3 in styler, flirty-gym, difficult-conversation-simplifier (the retired-skill deletions). Sidecar not gitignored: conversation_opener (untracked), flirty-gym (tracked). `ignore` lists `.claude/dashboard.md` and lacks `.claude/dashboard.html`: difficult-conversation-simplifier, flirty-gym, OEMMatInsightBI, PortfolioWebsite, styler.
- **History** (committed `.claude/` tree at the parent of each project's sync commit, against `v5.10.0`; PortfolioWebsite against `v5.11.0`), as up_to_date / new / template_copy / modified: conversation_opener 33/7/45/0; difficult-conversation-simplifier 15/21/49/0; flirty-gym 27/15/43/0; nordgrid-data-engineering 32/9/44/0; OEMMatInsightBI 19/36/29/1 (`dashboard-render.py`; its "new" is inflated by gitignored files); styler 35/4/46/0; PortfolioWebsite 30/4/51/0. 307 differing files are template copies, 1 is modified.
- **Sidecar rule replay:** only flirty-gym tracks the sidecar: of 43 differing files the v5.11.0 rule calls 5 "Modified upstream"; all 5 are template copies.
- Template files with mode `100755` at `v5.11.0`: `hooks/pre-compact-handoff.sh`, `scripts/fingerprint.py`, `scripts/persist-friction.py`, `scripts/validate-tasks.py`.
- Scratch exports of those pre-sync committed trees: `<scratchpad>/head/<project>/.claude/` (not git work trees).

## Build split

Each agent edits a scratch mirror (`.claude/` copied as `dot-claude/`, plus `tests/`). No shared files.

| Agent | Owns |
|---|---|
| **A** scripts | `.claude/scripts/sync-check.py`, `.claude/scripts/sync-apply.py` (new), `.claude/scripts/tests/test_sync_check.py`, `.claude/scripts/tests/test_sync_apply.py` (new), `.claude/scripts/README.md` |
| **B** Part 5 | `.claude/commands/health-check.md`, `.claude/support/reference/workflow.md`, `.claude/README.md` (only if it restates a changed rule), `tests/scenarios/39-health-check-batch-triage.md`, `tests/scenarios/45-template-sync-retired-files.md`, `tests/scenarios/50-template-sync-classification.md` (new), `tests/README.md` |

Main session: `.claude/version.json`, ship-log, FB stubs + archive, root `CLAUDE.md`, one `architecture-map.md` row for the new script.

## Build contract (pinned)

Everything in `plan-v5.10.0-sync-retirement.md` § Build contract (with A1–A9, F1–F8) still holds; existing output keys are unchanged. Terms from there: U = upstream manifest at `REF`, L = local manifest, `compare`, template blob ids of a path (`blob_ids`).

### 1. `sync-check.py` — new output keys (every key always present)

```json
{
  "history_complete": true,
  "files": [
    {"path": ".claude/commands/work.md", "status": "template_copy", "mode": "100644",
     "mode_matches": true, "version": "5.4.0", "basis": "history", "shared_lines": null}
  ],
  "manifest": {
    "customize": {"add": [], "drop": [], "list": [".claude/README.md", "…"]},
    "ignore": {"add": [".claude/dashboard.html"], "drop": [".claude/dashboard.md"], "list": ["…"]}
  },
  "sidecar": {"exists": true, "gitignored": true, "tracked": false}
}
```

**`files`.** One entry per path that is a blob in the tree at `REF`, matches a `compare` pattern, and (is named exactly in U.sync or matches no U.customize/U.ignore pattern). Sorted by `path`. Every entry carries all seven keys.
- `mode`: the path's mode at `REF`, `"100644"` or `"100755"`.
- Local state: `PROJECT/<path>` via `lstat`. Absent → `status: "new"`. Present but not a regular file (symlink, directory) → `status: "modified"`, `mode_matches: null`, `shared_lines: null`.
- Local blob id = `git -C TEMPLATE_REPO hash-object --no-filters <absolute path>` (batched, as `hash_files`).
- `status`, first match wins:
  1. `up_to_date`: local id equals the path's blob id at `REF`.
  2. `template_copy`, `basis: "history"`: local id is among the path's template blob ids. `version` = `template_version` in `.claude/version.json` at the newest commit reachable from `REF` that set the path to that blob (the new id of a `--raw` line); `null` when that file is unreadable there or the id only ever appears as an old id.
  3. `template_copy`, `basis: "sidecar"`, `version: null`: the sidecar's `files[path].synced_hash` equals `"sha256:" + sha256(local bytes).hexdigest()`.
  4. `modified`.
- `basis` is `null` except for `template_copy`; `version` is `null` except for history copies.
- `mode_matches`: `null` for `new` and non-regular; otherwise `(st_mode & 0o100 != 0) == (mode == "100755")`.
- `shared_lines` (only for `modified` regular files, else `null`): local lines = the file's bytes split on `\n`, each stripped of surrounding whitespace, empty ones dropped; template lines = the same over every template blob of the path (its template blob ids plus the blob at `REF`). Value = `round(count of local lines present in the template set / count of local lines, 2)`; `null` when the local file has no non-blank line.

**`history_complete`** = `git -C TEMPLATE_REPO rev-parse --is-shallow-repository` prints `false`. When it is not: warning `template history is shallow; files it cannot place are classified from the sync-state sidecar`.

**Sidecar read** (`PROJECT/.claude/.sync-state.json`, read-only): a JSON object with a `files` object. Missing → no entries, no warning. Present but unparseable or not that shape → no entries + warning `sync-state sidecar unreadable; ignored`.

**`sidecar`.** `exists` = the path is a regular file. `gitignored` = `git -C PROJECT check-ignore -q --no-index -- .claude/.sync-state.json` exits 0 (`--no-index` so a tracked file still reports its ignore rule); `tracked` = `git -C PROJECT ls-files --error-unmatch -- .claude/.sync-state.json` exits 0. Both `null` when `git` is false.

**`manifest`** (for each of `customize`, `ignore`; `H_cat` = union of that category's lists over every parseable manifest version in `git log REF -- .claude/sync-manifest.json`):
- `add` = U[cat] entries missing from L[cat] (upstream order, deduplicated).
- `drop` = L[cat] entries (local order, deduplicated) not in U[cat] that are in `H_cat`, or in U.sync, or in the other U category.
- `list` = U[cat] (deduplicated) followed by the L[cat] entries that are in neither U[cat] nor `drop` (local order): the upstream list plus project-added entries.
- Local manifest missing or unparseable: `add` = U[cat], `drop` = `[]`, `list` = U[cat].

**Expected real data** (template history = this repo): `<scratchpad>/head/<project>` with `--ref v5.10.0` (PortfolioWebsite: `v5.11.0`) → the Survey's counts (`files` length 85; statuses as listed; the one `modified` is OEMMatInsightBI `dashboard-render.py`). Live projects with `--ref v5.11.0` → 85 `up_to_date`, all `mode_matches` true; `manifest.ignore` = add `.claude/dashboard.html`, drop `.claude/dashboard.md` in the five projects named in the Survey and empty elsewhere; `sidecar.gitignored` false for conversation_opener and flirty-gym, `tracked` true only for flirty-gym; LTP and escalation_map_training `null`/`null`.

### 2. `sync-apply.py` (new; the one writer for Part 5 Step 4)

**CLI.** `python3 .claude/scripts/sync-apply.py [--project DIR] [--template-repo DIR] [--ref REF] [--status LIST] [--paths-from FILE] [--keep-pattern PATTERN]… [--manifest-lists] [--dry-run]`
- `--project`, `--template-repo`, `--ref`: as `sync-check.py`. The script loads `sync-check.py` from its own directory (`importlib`) and calls `check()`; it never re-implements classification.
- Selection = union of:
  - `--status`: comma-separated subset of `new`, `template_copy`; any other value is a usage error (exit 2). Selects every `files[]` entry with that status.
  - `--paths-from FILE` (`-` = stdin): one project-root-relative path per line; blank lines ignored. Every path must be in `files[]`, else exit 2 before anything is written (the script never writes outside the compare set). This is the only way to select a `modified` file.
- A selected `up_to_date` file is written only if `mode_matches` is false (mode fix).
- `--keep-pattern`: a retired sync pattern whose drop row the user did not include; it stays in the local `sync` list. Values not in `patterns.retired` are ignored with a warning.
- `--manifest-lists`: also set the local `customize` and `ignore` lists to `manifest.<cat>.list`.
- `--dry-run`: compute and print the result, write nothing.
- No selection flags is valid: only the bookkeeping below runs.

**Writes**, in this order, all inside `PROJECT/.claude/`:
1. **Files.** For each selected path: content = the blob at `REF`; written to a temp file in the target directory and `os.replace`d; mode `0o755` when `mode` is `100755`, else `0o644`; parent directories created. Refused (entry in `failed`, nothing written for that path) when the local path exists and is not a regular file, or when the real path of its parent directory is not inside the real path of `PROJECT/.claude`. A mode-only fix is a `chmod`.
2. **`version.json`**, only when at least one file's content was written (status `new`, `template_copy` or `modified`): `template_version` and `template_release_date` set to the values at `REF`, by replacing the two JSON string values in the file's text (every other byte kept); a key that is absent is added by a parsed rewrite (`indent=2`, trailing newline). Missing or unparseable local file → skipped + warning. Never touches other keys.
3. **`sync-manifest.json`:** `sync` = `patterns.compare` followed by the kept retired patterns; with `--manifest-lists`, `customize` and `ignore` = `manifest.<cat>.list`. Lists live in the `categories` object when the file has one, else at top level; other keys kept. Written (`indent=2`, `ensure_ascii=False`, trailing newline) only when a list changed. Missing or unparseable → skipped + warning (never created).
4. **Sidecar** (`.claude/.sync-state.json`): `files[path].synced_hash` = `"sha256:" + hex` for **every** `files[]` path whose local content now equals the blob at `REF`; entries whose path no longer exists locally are dropped; other entries and unknown top-level keys are kept. `last_full_sync_version` (upstream version) and `last_full_sync_date` (today, ISO date) refreshed when step 2 bumped the version. Created with `schema_version: "1.0"` when missing; an unparseable one is replaced. Written only when its content changed.

Not done by the script (Part 5 prose keeps them): removing retired files, `.gitignore` edits, `git rm --cached`, staging, committing, dashboard regeneration.

**Output** (stdout JSON, `indent=2`, every key present):
```json
{
  "ref": "template/main", "ref_commit": "<40-hex>", "dry_run": false,
  "written": [{"path": "…", "status": "template_copy", "mode": "100644"}],
  "mode_fixed": ["…"],
  "failed": [{"path": "…", "error": "…"}],
  "version": {"from": "5.11.0", "to": "5.12.0", "bumped": true},
  "manifest": {"changed": true, "sync_added": [], "sync_dropped": [], "lists_updated": true},
  "sidecar": {"recorded": 85, "dropped": 0, "created": false, "changed": true},
  "changed_paths": [".claude/commands/work.md", ".claude/version.json"],
  "remaining": [{"path": "…", "status": "modified"}],
  "warnings": []
}
```
`changed_paths` = every path the run changed (written files, mode fixes, `version.json`, the manifest, the sidecar), sorted. `remaining` = `files[]` entries that are still not `up_to_date` after the run. `version.to` is the local value after the run. With `--dry-run` the same object describes what would happen.
Exit `0` success; `1` when `failed` is non-empty (everything else was still applied); `2` usage or runtime error (including every `sync-check.py` exit-2 condition and an unknown path in `--paths-from`).

`scripts/README.md`: update the `sync-check.py` row; add a `sync-apply.py` row and name it wherever the README lists scripts that write (the README's read-only-by-default wording must stay true).

### 3. Part 5 text (B)

- **Requirements:** `python3` for both scripts (optional; prose fallback below).
- **Sync State Sidecar section:** rewritten. The test for "did the project edit this file" is the template's own history: a file whose content equals any template version of its path is an unchanged template copy. The sidecar is the fallback for when history can't place a file (shallow clone, rewritten or forked template history). Schema unchanged. Lifecycle: read by `sync-check.py`; written by `sync-apply.py` for every compare-set file that equals upstream after a run (not only files it wrote). Must be gitignored (see the gitignore row).
- **Step 1, non-git projects:** when the project is not a git work tree (`git rev-parse --is-inside-work-tree` fails), don't add a remote: `git clone --quiet {template_repo} "$TMP/template"` into a temporary directory outside the project, pass `--template-repo "$TMP/template" --ref origin/HEAD` (or `HEAD`) to both scripts, skip Step 5, and delete the clone at the end. Clone failure → the offline report line. Git projects keep the `template` remote.
- **Step 2:** run `sync-check.py`; classification comes from `files[]`. The per-file `git diff` loop, `local_hash`/`shasum` paragraph and the sidecar-based status definitions go. Per-file statuses:
  - **Up to date** — `up_to_date`.
  - **Unchanged template copy** — `template_copy`: the local content equals template v{version} of this path (or, with `basis: "sidecar"`, the content recorded at the last sync). Nothing local is lost by updating.
  - **Locally modified** — `modified`: matches no template version. User adjudicates.
  - **New in template** — `new`.
  - Retired upstream / Local only: unchanged.
  - When `history_complete` is false, say so in the report: `ℹ️ Template history is shallow: files it can't place are classified from the sync-state sidecar; "Locally modified" may include unchanged copies. git fetch --unshallow template gives the full answer.`
  - **Fallback** (script missing or failing): a differing file is an unchanged template copy when its `git hash-object --no-filters` id is among the path's template blob ids; otherwise locally modified. Keep the existing three fallback bullets.
- **Step 3 report groups** rename to `Unchanged template copies (no local edits):` with `(copy of v5.4.0)` per file, and `Locally modified (review before including):`.
- **Step 3 queue rows:**
  - `template_copy` → `Update template file (unchanged copy of v5.4.0)` (`basis: "sidecar"`: `(unchanged since the last sync)`), risk `—`, included in bare `[A]`.
  - `modified` → `Update template file (locally modified, [D] shows the diff)`, risk `⚠ overwrites local`, explicit inclusion. When `shared_lines` is not null and below 0.25: `Update template file (local content is not a variant of the template file: {N}% of its lines appear in any template version; move it to a project-*.md file before including)`.
  - `new` → risk `—` (unchanged).
  - `mode_matches` false on an otherwise up-to-date file → `Fix file mode ({mode})`, risk `—`.
  - `manifest.customize`/`ignore` with a non-empty `add` or `drop` → one row: `Update local manifest lists (add .claude/dashboard.html; drop .claude/dashboard.md)`, file `.claude/sync-manifest.json`, risk `—`. Project-added entries are kept.
  - `sidecar.gitignored` false → `Add .claude/.sync-state.json to .gitignore`, file `.gitignore`, risk `—`; when `sidecar.tracked` is also true the row reads `Stop tracking .claude/.sync-state.json and add it to .gitignore` (apply: `git rm --cached -q -- .claude/.sync-state.json`, then append the line). Not queued for non-git projects.
- **Fix Queue Protocol:** `⚠ overwrites local` now names only locally modified sync files.
- **Step 4:** one call: `python3 .claude/scripts/sync-apply.py --ref … --paths-from <file of included sync-file and mode rows> [--keep-pattern …] [--manifest-lists]` (the paths file goes in the scratchpad or `.claude/support/workspace/`), then the prose steps the script doesn't do (retired-file removal, `.gitignore` row, dashboard re-check). Report from its JSON; `failed` entries are failed rows. The bullets on checking out files, bumping `version.json` (now including `template_release_date`), writing the manifest and updating the sidecar collapse into "the script does these"; keep a short prose fallback (`git show {ref}:{path} > {path}` plus `chmod`, the two `version.json` fields, the `sync` list, sidecar entries for every file equal to upstream).
- **Step 5:** paths = `changed_paths` minus gitignored, plus removed files, `.gitignore` when the row applied, the sidecar deletion when untracked, plus `uncommitted_sync`. Everything else unchanged.
- **Key Rules:** the two sidecar bullets are replaced by: `**Blob history decides, the sidecar is the fallback** — a file equal to any template version of its path is an unchanged copy and updates under bare [A]; only a file matching no template version needs adjudication.` "No silent changes" stays.
- **Scenarios:** 45 and 39 updated where a row shape or status name changed; new scenario 50 traces: (A) pre-sync tree with 45 copies, 7 new, 0 modified and no sidecar → bare `[A]` applies all; (B) one modified file with `shared_lines` 0.03 → the not-a-variant row, excluded from `[A]`; (C) shallow history + sidecar; (D) stale manifest lists and an untracked, un-ignored sidecar; (E) non-git project via temporary clone, Step 5 skipped.

## Contract amendments

After agent B's report (2026-10-06):

**A1. Step 4 order.** Retired-file removal runs before `sync-apply.py` (the script drops sidecar entries only for paths that no longer exist). Order: removals, script, `.gitignore` row, dashboard re-check. The script runs whenever a Part 5 row other than the `.gitignore` row was included; `--paths-from` is left out when no file or mode row was.

**A2. Committing the sidecar untracking.** After `git rm --cached`, `git commit -- <paths>` re-adds a file that still exists on disk (tested, git 2.48.1). Step 5 `[C]`: leave the sidecar's `D` out of `git add`, move `.claude/.sync-state.json` out of the project for the commit and back afterwards. Step 5 lists the sidecar only as `D`, and only when the stop-tracking row applied.

**A3. Unpinned row texts.** History copy with `version: null`: `Update template file (unchanged copy of an earlier template version)`. `new`: `Add new template file`, risk `—`. `{N}%` = `shared_lines` × 100, rounded.

**A4. `sync-apply.py` exit 2.** Every exit-2 condition is detected before the first write; a re-run after any interruption is idempotent.

**A5. `[D]` for update rows** is `git show {ref}:{path} | diff -u - {path}` (one form for git and non-git projects). Diff stats leave the report lines and rows (the script emits none).

**A6. Non-git details.** `--ref origin/HEAD`, full-history clone, clone deleted when the run ends (Part 5c reads `settings.json` from it). The `.gitignore` row targets the project root's `.gitignore` (created when missing) and is queued whenever `sidecar.gitignored` is false.

After agent A's report (2026-10-06; 268 tests on 3.10 and 3.13, real-data counts all match the Survey):

**A8. `check-ignore` and literal pathspecs.** `git check-ignore` exits 128 under `GIT_LITERAL_PATHSPECS=1` ("pathspec magic not supported"), so every project read as not ignored. The script runs that one call without the variable.

**A9. `files[]` holds regular-file blobs only** (tree mode `100…`); any mode other than `100755` reports as `100644`. New keys sit after `uncommitted_sync`; `warnings` stays last.

**A10. `sync-apply.py` details.** `--paths-from` matches exactly (`./.claude/x` is rejected). `version.json` is replaced textually only when each key already holds a string, occurs once and the result parses to the intended object; otherwise a parsed rewrite. `template_release_date` is set only if upstream has one. A bare run (no selection flags) still drops retired sync patterns and records the sidecar, so Part 5 passes `--keep-pattern` for every drop row not included, on every call. The local `sync` list is rewritten in `compare` order (a pure reorder counts as a change). Sidecar: stale entries are dropped for every entry, not only compare-set paths; a sidecar path that is not a regular file is never written (warning). An I/O error writing `version.json`, the manifest or the sidecar exits 2 after file writes may have landed (the one exception to A4); a re-run is idempotent. The script sets `sys.dont_write_bytecode` before loading `sync-check.py`. `remaining[]` carries pre-run statuses.

**A7. Part 2a** queues its revert/keep/merge row for `.claude/CLAUDE.md` only when Part 5 classifies the file as `modified` (an unchanged copy is already a `—` update row). To apply in the review-fix pass.

### Review fixes (2026-10-06, independent review: 1 blocker, 5 should-fix, 4 nits; these supersede the text above where they differ)

- **R1 (blocker):** the sidecar is consulted only when `history_complete` is false. With full history, a `synced_hash` match never makes a file a `template_copy` (live sidecars hold entries for project-own commands the old prose recorded, e.g. difficult-conversation-simplifier `commands/talk.md`; if the template later ships that path, bare `[A]` would have overwritten the project's file). `sync-apply.py` drops sidecar entries whose path is not in `files[]` and entries for `files[]` paths that do not equal `REF` after the run. The sidecar section no longer names rewritten or forked template history.
- **R2 (should-fix, decision 9: yes):** `settings.json` allowed every `.claude/scripts/*.py` without a prompt, and `sync-apply.py` writes (pointed at a repo holding the template's history plus one hostile commit, it rewrote `settings.json` unprompted). `permissions.ask` gains `Bash(python3 .claude/scripts/sync-apply.py:*)`; `.claude/CLAUDE.md`, `.claude/README.md`, `rules/agents.md` and Part 5 Step 4 say so.
- **R3 (should-fix):** `version.json` is bumped when a file's content was written, **or** when every `files[]` entry equals `REF` after the run and the local version differs (an interrupted run could otherwise never bump). After an exit 2, Part 5 re-runs and takes Step 5's paths from `sync-check.py`'s `uncommitted_sync` as well. Docstring states the bookkeeping-I/O exception.
- **R4 (should-fix):** scenario 50 Trace A starts from a project already on v5.12.0+ (the first sync into v5.12.0 runs the project's older Part 5) and uses a non-script `new` example.
- **R5 (should-fix):** `history_complete` is about `REF`'s history, not the repository: true when no commit listed in the repository's `shallow` file is reachable from `REF`.
- **R6 (should-fix):** `sync-apply.py` exits 2 when `PROJECT/template-maintenance/` exists (the template repo), except with `--dry-run`.
- **R7 (nit):** prose says a local `customize`/`ignore` entry naming something the template syncs is not project-added: it is dropped and never excluded the file.
- **R8 (tests):** pin the parent-directory guard's separator (`.claude/commands` symlinked to a sibling `.claude-x/`), atomic replace, and symlink blobs staying out of `files[]`.
- **A7 applied.** Accepted as-is: the `version` label can lag one release for a few files (display only); a manifest rewrite un-escapes non-ASCII in `notes` once.
- **Re-verify (2026-10-06):** all findings fixed or accepted; ask beats allow per the Claude Code permissions docs. One addition after the fixer: a sidecar entry is kept when the run classified its file as a sidecar-basis copy and did not update it (shallow history only). Re-verify nits applied: Step 4's bump sentence, the prose fallback's shallow exception, a test for the empty-compare-set guard. 277 tests on 3.10 and 3.13; 51 of 55 mutations caught. Open, for the maintainer: the ask rule matches only the literal invocation (`python3 .claude/scripts/../scripts/sync-apply.py` slips past it to the allow glob).
