# Scenario 45 — Template sync removes retired template files (FB-126)

Conceptual trace test for v5.10.0 (row shapes and statuses as of v5.12.0, FB-136; classification itself is scenario 50). `/health-check` Part 5 runs `sync-check.py` after the fetch. A sync pattern the template no longer syncs is not compared and is offered for dropping. A file the template shipped (as a sync file, or with exactly this content) and later deleted is offered for removal (`⚠ deletes`, explicit inclusion only). A file the template never shipped is never flagged. Step 5 offers to commit what the sync changed, including an earlier sync that was never committed, even after the template has moved on.

## Setup / State

- A downstream git project on template v5.7.4. The `template` remote exists, `git fetch template` succeeds, and `template/main` is at v5.10.0. `python3` is available.
- The local `.claude/sync-manifest.json` `sync` list holds the v5.7.4 patterns plus `.claude/skills/*/SKILL.md`, which the template dropped in v4.12.0.
- Tracked and committed:
  - `.claude/skills/dashboard-style/SKILL.md`, `.claude/skills/decomposition-heuristics/SKILL.md` and `.claude/skills/spec-checklist/SKILL.md`, byte-identical to the copies the template deleted in v4.12.0 (commit `<del-412>`), when `.claude/skills/*/SKILL.md` was in its `sync` list.
  - `.claude/commands/complete-task.md`. The template deleted it in v1.5.0 (commit `<del-150>`), when `.claude/commands/*.md` was in `sync`. The project has since rewritten it as a redirect stub, so it matches no template version.
  - `.claude/skills/outfit-rules/SKILL.md`, the project's own skill. It has never existed in template history.
  - `.claude/commands/work.md`, which differs from `template/main`; it is byte-identical to the template's v5.7.4 copy of that path.
- `.claude/.sync-state.json` (gitignored) has `files` entries for `.claude/commands/work.md`, `.claude/skills/dashboard-style/SKILL.md` (from a sync before v4.12.0) and `.claude/support/reference/legacy-notes.md` (deleted by hand long ago).
- Nothing else differs from `template/main`, file modes match, the local `customize` and `ignore` lists equal the upstream ones, and no other part queues a row. `src/app.py` (unrelated work) is staged but not committed when `/health-check` starts.

## Trace A — the report: retired files, the retired pattern, and the project's own skill

Command path: `commands/health-check.md § "Part 5: Template Sync Check"` → `§ "2. Compare Sync Files"` → `§ "3. Present Changes (report) and Queue Apply Rows"` → `§ "Step 4: Batch Fix Triage"`.

1. Step 1 fetches. Step 2 runs `python3 .claude/scripts/sync-check.py --ref template/main` from the project root. Output (excerpt; `ref_commit` and most of `compare` omitted):
   ```json
   {
     "ref": "template/main",
     "upstream_version": "5.10.0",
     "local_version": "5.7.4",
     "git": true,
     "patterns": {
       "compare": [".claude/CLAUDE.md", "…"],
       "project_added": [],
       "retired": [{"pattern": ".claude/skills/*/SKILL.md", "removed_in": "4.12.0"}]
     },
     "retired_files": [
       {"path": ".claude/commands/complete-task.md", "state": "modified", "owned": true,
        "removed_in": "1.5.0", "removed_commit": "<del-150>"},
       {"path": ".claude/skills/dashboard-style/SKILL.md", "state": "unmodified", "owned": true,
        "removed_in": "4.12.0", "removed_commit": "<del-412>"},
       {"path": ".claude/skills/decomposition-heuristics/SKILL.md", "state": "unmodified", "owned": true,
        "removed_in": "4.12.0", "removed_commit": "<del-412>"},
       {"path": ".claude/skills/spec-checklist/SKILL.md", "state": "unmodified", "owned": true,
        "removed_in": "4.12.0", "removed_commit": "<del-412>"}
     ],
     "uncommitted_sync": [],
     "warnings": []
   }
   ```
   The keys v5.12.0 added are left out of the excerpt: `history_complete` is true, `manifest` has empty `add` and `drop` lists, `sidecar` is `{"exists": true, "gitignored": true, "tracked": false}`, and every `files[]` entry is `up_to_date` except `{"path": ".claude/commands/work.md", "status": "template_copy", "mode": "100644", "mode_matches": true, "version": "5.7.4", "basis": "history", "shared_lines": null}`.
2. `patterns.compare` is the compare set, and `.claude/skills/*/SKILL.md` is not in it. `.claude/commands/work.md` is an Unchanged template copy. `.claude/commands/complete-task.md` matches `.claude/commands/*.md` and is absent upstream, but it is in `retired_files`, so its status is Retired upstream, not Local only.
3. `.claude/skills/outfit-rules/SKILL.md` appears nowhere. No compare pattern matches it, and the template never deleted it (it never had it), so it isn't a `retired_files` candidate. The same walk lists the three template skills in the same directory (positive control).
4. Report:
   ```
   Template updates available (v5.7.4 → v5.10.0):

     Unchanged template copies (no local edits):
       .claude/commands/work.md (copy of v5.7.4)

     Retired upstream (the template removed these files):
       .claude/commands/complete-task.md (removed in v1.5.0; locally modified)
       .claude/skills/dashboard-style/SKILL.md (removed in v4.12.0; unchanged template copy)
       .claude/skills/decomposition-heuristics/SKILL.md (removed in v4.12.0; unchanged template copy)
       .claude/skills/spec-checklist/SKILL.md (removed in v4.12.0; unchanged template copy)

     Retired sync patterns (the template no longer syncs these):
       .claude/skills/*/SKILL.md (as of v4.12.0)
   ```
   No `ℹ️` line: `uncommitted_sync` is empty.
5. The triage table:
   ```
   | # | Part | File | Proposed fix | Risk |
   |---|------|------|--------------|------|
   | 1 | 5 | .claude/commands/work.md | Update template file (unchanged copy of v5.7.4) | — |
   | 2 | 5 | .claude/commands/complete-task.md | Remove retired template file (removed upstream in v1.5.0; locally modified, [D] shows the diff) | ⚠ deletes |
   | 3 | 5 | .claude/skills/dashboard-style/SKILL.md | Remove retired template file (removed upstream in v4.12.0; unchanged template copy) | ⚠ deletes |
   | 4 | 5 | .claude/skills/decomposition-heuristics/SKILL.md | Remove retired template file (removed upstream in v4.12.0; unchanged template copy) | ⚠ deletes |
   | 5 | 5 | .claude/skills/spec-checklist/SKILL.md | Remove retired template file (removed upstream in v4.12.0; unchanged template copy) | ⚠ deletes |
   | 6 | 5 | .claude/sync-manifest.json | Drop retired sync pattern ".claude/skills/*/SKILL.md" (the template no longer syncs it as of v4.12.0) | — |
   ```
6. `[D] 2` prints `git show <del-150>^:.claude/commands/complete-task.md | diff -u - .claude/commands/complete-task.md`, truncated like other `[D]` output, and re-prompts without consuming the response.

Variant A2, no `python3`: the Step 2 fallback finds the same pattern (`git log template/main -S'".claude/skills/*/SKILL.md"' --format=%h -1 -- .claude/sync-manifest.json` prints a commit) and the same four files. When it doesn't determine a version, the rows leave it out: `(removed upstream; unchanged template copy)`, `(removed upstream; locally modified, [D] shows the diff)` and `(the template no longer syncs it)`.

**Expected:** the three template skills and the rewritten command are each offered for removal as a `⚠ deletes` row, and the stale pattern is offered for dropping as a `—` row. The project's own skill never appears, although it sits in the same directory under the same retired pattern. Nothing is prompted mid-run.

**Pass criteria:** the retired pattern is not compared; `complete-task.md` is Retired upstream, not Local only; `outfit-rules` is absent from the script output, the report and the table; each removal row says whether the file is an unchanged template copy or locally modified; `[D]` on a removal row diffs against the template's last version.

## Trace B — the user includes some rows: removals, pruning, write-back, sidecar

Command path: `§ "Step 4: Batch Fix Triage"` → Part 5 `§ "4. Apply Updates"`.

1. The user answers `A include 3, 4, 5`. Bare `A` applies rows 1 and 6 (unflagged), and rows 3, 4 and 5 apply by explicit inclusion. Row 2 (`⚠ deletes`, not named) is listed back as still open.
2. Step 4a runs first. Rows 3–5: each file is tracked, so each is removed with `git rm -q -- {path}`, which also deletes its now-empty skill directory. The parent-directory pass finds nothing more to prune: `.claude/skills/` still holds `outfit-rules/`. Had the files been untracked, `rm -- {path}` would leave the three skill directories empty, and the pass would remove them and stop at `.claude/skills/`.
3. Step 4b: one call, `python3 .claude/scripts/sync-apply.py --ref template/main --paths-from <file>`, the file holding the one line `.claude/commands/work.md`. No `--keep-pattern` (row 6 was included) and no `--manifest-lists` (no such row). The script writes `work.md` with the content at `template/main`.
4. Row 1 is a sync-file update, so the script sets `template_version` to `5.10.0` and `template_release_date` to the upstream date in `.claude/version.json`. Removal and drop rows alone would leave both as they were.
5. Write-back: the local `sync` list becomes `patterns.compare`. Row 6 was applied, so `.claude/skills/*/SKILL.md` is gone. Had row 6 been excluded, the call would carry `--keep-pattern ".claude/skills/*/SKILL.md"`, the list would be `patterns.compare` plus that pattern, and the next run would offer the drop again.
6. Sidecar: every compare-set file now equals upstream, so each has a `synced_hash` entry, `work.md` with its new hash. The `.claude/skills/dashboard-style/SKILL.md` entry is dropped (the file was removed in step 2), and so is `.claude/support/reference/legacy-notes.md` (not a compare-set path). `last_full_sync_version` becomes `5.10.0`, `last_full_sync_date` today.
7. `.claude/commands/complete-task.md` is untouched and stays in `retired_files` for the next run.
8. Post-apply summary: applied 1, 3, 4, 5 and 6; still open: 2.

**Expected:** only the included removal rows delete files; empty directories are pruned up to, never including, `.claude/`, and a directory that still has files is kept.

**Pass criteria:** bare `A` deletes nothing; the excluded locally modified file survives; removals run before the script call, so the sidecar keeps no entry for a missing path; the write-back drops exactly the included retired pattern.

## Trace C — Step 5 commits only the sync's paths

Command path: Part 5 `§ "5. Commit Offer"`, after Trace B's post-apply summary.

1. A Part 5 row was applied, so Step 5 fires. Paths: the script's `changed_paths` (`.claude/.sync-state.json`, `.claude/commands/work.md`, `.claude/sync-manifest.json`, `.claude/version.json`) plus the three removed skill files; `uncommitted_sync` was empty. `.claude/.sync-state.json` is gitignored and drops out. `src/app.py` is not a Part 5 path.
2. Prompt:
   ```
   Template sync changed 6 files and they are not committed:
     M .claude/commands/work.md
     D .claude/skills/dashboard-style/SKILL.md
     D .claude/skills/decomposition-heuristics/SKILL.md
     D .claude/skills/spec-checklist/SKILL.md
     M .claude/sync-manifest.json
     M .claude/version.json
   Commit them now? [C] Commit as "Sync template v5.7.4 → v5.10.0" | [L] Leave uncommitted
   ```
   `{old}` is `5.7.4`, from `HEAD:.claude/version.json`; `{new}` is the local `5.10.0`.
3. `[C]`: `git add -- .claude/commands/work.md .claude/sync-manifest.json .claude/version.json`, leaving out the three deleted paths (`git rm` staged them, and `git add` would reject them), then `git commit -m "Sync template v5.7.4 → v5.10.0" -- <the six paths>`.
4. Result: one commit with exactly the six paths. `src/app.py` is still staged and not in the commit. Nothing is pushed.

Variant: had `HEAD:.claude/version.json` already said `5.10.0`, the message would be `Sync template files (v5.10.0)`.

Variant C2: had the user answered `A except 1` in Trace B, only row 6 (the pattern drop) would apply. No sync-file row applied, so `template_version` stays `5.7.4`, and Step 5 lists one path, `M .claude/sync-manifest.json`, with the message `Sync template files (v5.7.4)`. Had the drop bumped the version, the commit would read `Sync template v5.7.4 → v5.10.0` while holding no v5.10.0 file.

**Expected:** one commit holding exactly what the sync changed; the user's other staged work is untouched.

**Pass criteria:** the offer comes after the post-apply summary; the list holds only Part 5 paths, with gitignored ones dropped; the commit contains the six paths and nothing else; `src/app.py` stays staged.

**Fail indicators:** `git commit -a`; `git add -A` with no paths (stages the whole tree); `git add` given a path `git rm` already removed (it aborts, staging nothing, and the commit then fails); `src/app.py` in the sync commit; a push.

## Trace D — `[L]`, then the next run offers the commit again

Command path: Part 5 `§ "5. Commit Offer"` (`[L]`) → next run: `§ "2. Compare Sync Files"` (`uncommitted_sync`) → `§ "3. Present Changes (report) and Queue Apply Rows"` → `§ "5. Commit Offer"`.

1. At Trace C's prompt the user picks `[L]` instead: `Left uncommitted. The next /health-check will offer this commit again.` Step 5 stages and commits nothing.
2. The next `/health-check` (`template/main` unchanged). The script reports `local_version` `5.10.0`, an empty `patterns.retired`, and only `.claude/commands/complete-task.md` in `retired_files` (the removed skills are no longer on disk). `uncommitted_sync`:
   ```json
   [
     {"path": ".claude/commands/work.md", "change": "modified"},
     {"path": ".claude/skills/dashboard-style/SKILL.md", "change": "deleted"},
     {"path": ".claude/skills/decomposition-heuristics/SKILL.md", "change": "deleted"},
     {"path": ".claude/skills/spec-checklist/SKILL.md", "change": "deleted"},
     {"path": ".claude/sync-manifest.json", "change": "modified"},
     {"path": ".claude/version.json", "change": "modified"}
   ]
   ```
   `work.md` is listed because it matches a compare pattern and equals a template version of that path (here the current one); the skills because they are template deletions of files the template owned; `version.json` and `sync-manifest.json` because other paths are listed and their status shows a change.
3. Report: every `files[]` entry is `up_to_date`. The Retired upstream group lists `complete-task.md` again (excluded in Trace B), followed by `ℹ️ 6 synced files are not committed (an earlier sync was never committed)`. The table has one row: the `complete-task.md` removal (`⚠ deletes`).
4. The user answers `N`. No Part 5 row applies, but `uncommitted_sync` is non-empty, so Step 5 fires after the post-apply summary with the same six paths and the same `Sync template v5.7.4 → v5.10.0` message (`HEAD` still says `5.7.4`).

Variant D2: after `[L]`, the user edits `.claude/commands/work.md` by hand. It now equals no template version of that path, so `uncommitted_sync` leaves it out, `files[]` gives it as `modified` (Locally modified, a `⚠ overwrites local` row), and the commit offer lists five paths.

**Expected:** `[L]` changes nothing; the next run surfaces the uncommitted sync, and offers the commit again, even when every sync file is up to date; a hand edit made after the sync is never swept into the sync commit.

**Pass criteria:** the `ℹ️` line appears whenever `uncommitted_sync` is non-empty; the offer fires with no Part 5 row applied; the message uses `HEAD`'s version as `{old}`; an excluded removal row is offered again.

## Trace E — `--report`

Command path: `§ "Fix Queue Protocol"` (`--report`) → Part 5 Steps 2–3 → `§ "5. Commit Offer"` (`--report`).

State: Trace D's second run, invoked as `/health-check --report`.

1. The script runs as usual; it is read-only.
2. The report shows the Retired upstream group (`complete-task.md`) and `ℹ️ 6 synced files are not committed (an earlier sync was never committed)`.
3. No queue, no table and no commit offer. Nothing is removed, staged or committed, and neither the manifest nor the sidecar is written.

**Pass criteria:** `--report` shows the same findings as a normal run and changes nothing.

## Trace F — the template moved past an earlier uncommitted sync

Command path: next run: `§ "2. Compare Sync Files"` (`uncommitted_sync`) → `§ "3. Present Changes (report) and Queue Apply Rows"` → `§ "5. Commit Offer"`.

State: Trace D after `[L]`: the v5.10.0 sync's six paths are uncommitted. Before the next `/health-check`, the template releases v5.11.0, which changes `.claude/commands/work.md` again (`+4 -1`), and the fetch moves `template/main` there.

1. The script reports `local_version` `5.10.0` and `upstream_version` `5.11.0`. The local `work.md` is v5.10.0's copy: no longer the template's current copy, but one of the versions of that path in `template/main`'s history. `uncommitted_sync` holds the same six paths as in Trace D.
2. Report: `Template updates available (v5.10.0 → v5.11.0)`; `work.md` under Unchanged template copies (`copy of v5.10.0`: v5.10.0 was the release that set this content); `complete-task.md` under Retired upstream; `ℹ️ 6 synced files are not committed (an earlier sync was never committed)`. Table: row 1 `Update template file (unchanged copy of v5.10.0)` for `work.md` (`—`), row 2 removes `complete-task.md` (`⚠ deletes`).
3. The user answers `N`. No row applies, so `template_version` stays `5.10.0`. Step 5 offers the six paths with `Sync template v5.7.4 → v5.10.0`, and `[C]` commits the v5.10.0 sync whole: `version.json` at 5.10.0 together with 5.10.0's `work.md`.
4. Variant F2: the user answers `A`. Row 1 applies (row 2 stays open): `work.md` is written at v5.11.0 and, a sync-file row having applied, `template_version` becomes `5.11.0`. Step 5 lists the same six paths with `Sync template v5.7.4 → v5.11.0`.

Had `uncommitted_sync` listed a changed file only when it equals the template's *current* copy, `work.md` would drop out at step 1, leaving the three deletions, `version.json` and `sync-manifest.json`. `[C]` would then commit `version.json` at 5.10.0 without 5.10.0's `work.md`, and later runs wouldn't list `work.md` either: it would stay uncommitted until a sync row overwrote it. difficult-conversation-simplifier shows the stakes: measured against the template at v5.9.0, its uncommitted v5.7.4 sync has 62 listed paths, and a current-copy-only rule lists 26 of them.

**Expected:** an uncommitted sync is recognized by content, however far the template has moved since, and `[C]` commits all of it at once.

**Pass criteria:** `work.md`, equal to an older template version of its path but not the current one, is in `uncommitted_sync`; the offer lists all six paths, and `[C]` commits them together; a hand edit equal to no template version (Variant D2) is still left out.

**Fail indicators:** `uncommitted_sync` without `work.md`; a commit holding `version.json` at 5.10.0 without 5.10.0's `work.md`.

## Invariant checks

- Nothing is deleted without explicit inclusion of its `⚠ deletes` row; bare `A` never deletes.
- A file the template never shipped is never listed, whatever pattern matches it and whatever directory it sits in.
- Retired patterns are never compared. One stays in the local `sync` list only while its drop row is declined, and is offered again on every run.
- A local `sync` pattern never brings in a file that an upstream `customize` or `ignore` pattern matches (e.g. `.claude/support/reference/project-api.md`). Only a path the upstream `sync` list names exactly is compared despite an `ignore` match (`.claude/vision/README.md`).
- Step 5 stages and commits only the paths it listed (`git commit -- <paths>`). It never runs `git commit -a` or a pathless `git add`, never pushes, and leaves other staged work staged.
- `sync-check.py` writes nothing and never fetches; `sync-apply.py` is the only writer, and writes only inside `.claude/`.
- `uncommitted_sync` lists a changed sync file when its content equals any template version of its path, current or older; a file equal to none is never listed.
- After Step 4, `.sync-state.json` has no entry for a path that doesn't exist.
