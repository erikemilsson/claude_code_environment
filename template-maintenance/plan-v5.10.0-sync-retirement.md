# Plan: v5.10.0 — retired template files leave downstream (FB-126) + FB-134 patch bundle

**Status:** IMPLEMENTED in v5.10.0 (2026-10-05); see ship-log. Contract amended A1–A9; review fixes below. Originally APPROVED 2026-10-05: all six design decisions as recommended (v5.10.0 minor; locally modified retired files get a removal offer with a diff; Step 0e counts by task files; `resolves_friction` ships now, no one-time backfill of open entries; the commit offer stages only the paths Part 5 touched; five parallel agents + independent reviewer).
**Target:** v5.10.0 (minor: Part 5 proposes deletions and gains a commit step, new script, new optional task field, new `resolved_by.kind`).
**Scope:** FB-126 template-side fix (retired sync patterns, retired template files, commit offer) + FB-134 (a)–(e).
**Line numbers** are at v5.9.0 (`3ae187d`).

## Survey (2026-10-04/05, read-only)

- **Retired files.** A prototype check run against the committed (pre-cleanup) `.claude/` trees of styler, flirty-gym and difficult-conversation-simplifier found exactly the 9 retired Skill files (3 per project; all byte-identical to the copies the template deleted in v4.12.0, all in the template's `sync` category when deleted) and the stale `.claude/skills/*/SKILL.md` pattern in flirty-gym and difficult-conversation-simplifier. It did not flag flirty-gym's 7 own skills; positive control: the same walk flagged the 3 template skills in the same directory. Live trees: only OEMMatInsightBI's `.claude/commands/complete-task.md` and `sync-tasks.md` (the template deleted both in v1.5.0, in `sync` at the time; the project rewrote them as redirect stubs, so they are "locally modified").
- **Why ownership matters.** The template has deleted 420 paths under `.claude/` that it never re-added, including example `tasks/task-*.json` and `dashboard.md` (both `ignore`-category project data). "The template once had this path" alone would flag project data, so a file is flagged only when it was in the template's `sync` category when deleted, or is byte-identical to a template version.
- **Retired patterns in manifest history:** 22 `sync` patterns the template once listed and no longer does (old `.claude/reference/*`, `specification_creator/*`, `skills/*/SKILL.md`, etc.).
- **Step 0e (FB-134 c).** styler's live tree fires today on 4 tasks finished and committed on 2026-10-01 (its 3 dirty files are the uncommitted skill deletions). The files-based count is silent there. Other git projects: silent under both rules. `files_affected` shapes across Finished tasks: mostly real paths; also `dir/` entries (nordgrid 40) and globs (styler 11, PortfolioWebsite 2).
- **Friction register (FB-134 e).** 37 open entries across 5 projects are cited by a Finished task (citation includes tasks that *raised* the entry, so citation alone can't auto-close). Projects improvise `resolved_by.kind: "task"` (PortfolioWebsite 1, styler 3) and string forms (`"task-068"` ×6 in OEMMatInsightBI, `"T734"` in styler).
- **Retirement manifests (FB-134 a).** 21 manifests in 4 projects, all on the README schema. 14 retirement commits (the commit that added the manifest) are the direct child of `commit_sha`; 4 retirement commits retired two features at once; styler `wardrobe-gaps-tab` pins the retirement commit itself; 2 styler pins (`68add9a`) don't exist. **Adjacent bug:** `/audit-coherence` Lens 5 reads `slug`, `retirement_reason`, `replaced_by`; every real manifest has `feature_slug`, `rationale`, `successor_feature`.

## Design

### FB-126 — `/health-check` Part 5

1. **New read-only script `.claude/scripts/sync-check.py`** (contract below): retired sync patterns, retired template files, and synced-but-uncommitted changes. It reads template history either from the project repo's `template` remote (Part 5) or from a separate clone (`--template-repo`, used to test against downstream repos without fetching into them).
2. **Step 2 compare set** = upstream `sync` patterns + project-added patterns (local patterns the template never listed). Retired patterns are no longer compared. A path matching an upstream `customize`/`ignore` pattern is never compared, even when a sync pattern also matches it.
3. **Step 3 queue rows:** "Drop retired sync pattern" (risk `—`); "Remove retired template file" (new risk flag `⚠ deletes`, explicit inclusion; `[D]` shows the diff against the template's last version).
4. **Step 4 write-back:** local `sync` list = `patterns.compare` + any retired pattern whose drop row wasn't included. Removal = `git rm` (tracked) or `rm`, prune now-empty directories up to `.claude/`, drop the `.sync-state.json` entry. Also drop `.sync-state.json` entries for paths that no longer exist.
5. **New Step 5 commit offer**, after the batch applies: when Part 5 changed anything in this run or the script found `uncommitted_sync`. Stages and commits only those paths.
6. **Key rule reworded:** files the template never shipped are never flagged; a file the template shipped as a sync file and later deleted is offered for removal.

### FB-134

- **(a) Restore path.** Revert the retirement commit (the commit that added the manifest); when it retired several features, apply the inverse diff of this feature's paths only; files-only route checks paths out from the retirement commit's parent; a partly retired file is merged by hand, never copied over. No cherry-pick anywhere (it replays the pinned commit's own diff). Step 2 adds a pin check. `spec_excerpt_path` may be `null`. Lens 5 field names fixed.
- **(b)** Every `notes` write from a report or a `/work complete` prepends; never replaces.
- **(c)** Step 0e counts Finished tasks (`completion_date` ≥ last-commit date) with at least one `files_affected` entry among the uncommitted files. No schema change.
- **(d)** `verification_pass_rate` is `null` when no task has a verification result.
- **(e)** Optional task field `resolves_friction`; the fixing task's Finished transition closes those register entries with `resolved_by.kind: "task"`.

## Files (blast radius) and build split

Disjoint ownership; each agent edits a scratch mirror (`.claude/` copied as `dot-claude/`, plus `tests/`).

| Agent | Owns | Change |
|---|---|---|
| **A** script | `.claude/scripts/sync-check.py` (new), `.claude/scripts/tests/test_sync_check.py` (new), `.claude/scripts/README.md` | script per contract; tests (temp git repos); README table row |
| **B** Part 5 | `.claude/commands/health-check.md`, `.claude/support/reference/workflow.md`, `.claude/README.md`, `tests/scenarios/39-health-check-batch-triage.md`, `tests/scenarios/45-template-sync-retired-files.md` (new) | Part 5 Steps 2–5, Fix Queue Protocol flag + exception, Key Rules, report formats, Process Step 1/Step 4 mentions; workflow.md sync table (its `customize` example `.claude/CLAUDE.md` is stale: it is `sync`) + one line on retired files; `.claude/README.md` only if it states sync never removes files |
| **C** retirement | `.claude/rules/feature-retirement.md`, `.claude/support/retired/README.md`, `.claude/commands/audit-coherence.md`, `tests/scenarios/48-feature-restore.md` (new) | FB-134(a) + Lens 5 field names |
| **D** notes + FR | `.claude/support/reference/work-procedures.md`, `.claude/support/reference/task-schema.md`, `.claude/support/reference/friction-register.md`, `.claude/agents/implement-agent.md`, `.claude/rules/agents.md`, `.claude/support/reference/session-recovery.md`, `.claude/support/reference/parallel-execution.md`, `tests/scenarios/16-verification-failure-rework.md`, `tests/scenarios/46-notes-history-and-friction-close.md` (new) | FB-134(b) + (e) (touch `rules/agents.md`, `session-recovery.md`, `parallel-execution.md` only if they restate a notes overwrite) |
| **E** Step 0e + export | `.claude/commands/work.md`, `.claude/hooks/pre-compact-handoff.sh`, `.claude/support/reference/context-transitions.md`, `.claude/support/reference/work-recovery.md`, `tests/scenarios/47-uncommitted-work-check.md` (new) | FB-134(c) + (d) (`work.md`: Step 0e only) |

Main session after copy-back: `.claude/version.json`, `template-maintenance/ship-log.md`, FB stubs + archive, root `CLAUDE.md`, `template-maintenance/architecture-map.md` (one row for the new script only; the map otherwise stays FB-112(a)).

## Not in this release

FB-127 residuals, FB-119's inline-contract gaps, FB-112 (a)/(c)/(d), FB-129 (next), FB-130–FB-133, FB-135. No backfill of the 37 open register entries cited by Finished tasks. Part 5 still requires git (LTP and escalation_map_training have none; not addressed). Downstream repos stay read-only; the retired-skill deletions in styler, flirty-gym and difficult-conversation-simplifier stay uncommitted for the user.

## Build contract (pinned; every agent codes and documents against this text)

### 1. `sync-check.py` (A implements; B documents)

**CLI.** `python3 .claude/scripts/sync-check.py [--project DIR] [--template-repo DIR] [--ref REF]`
- `--project` (default `.`): the project root, which contains `.claude/`.
- `--template-repo` (default: the `--project` value): the git repository whose history holds the template. In Part 5 that is the project repo itself, with the `template` remote fetched.
- `--ref` (default `template/main`): the template commit-ish. Part 5 passes `--ref template/{branch}`. With `--template-repo`, pass a ref of that repo (e.g. `HEAD`).
- Exit `0` on success, findings or none. Exit `2` (message on stderr): `--project` has no `.claude/` directory; `--template-repo` is not a git repository; `--ref` doesn't resolve to a commit; no parseable `.claude/sync-manifest.json` at `REF`; usage error; Python below 3.10 (floor check as in the other scripts).
- Read-only: never writes files, never fetches. Runs `git status` with `GIT_OPTIONAL_LOCKS=0` so it doesn't refresh the index. Stdlib only.

**Output** (stdout, JSON, `indent=2`; every key always present; lists sorted as stated):
```json
{
  "ref": "template/main",
  "ref_commit": "<40-hex>",
  "upstream_version": "5.10.0",
  "local_version": "5.7.4",
  "git": true,
  "patterns": {
    "compare": [".claude/CLAUDE.md", "…"],
    "project_added": [],
    "retired": [{"pattern": ".claude/skills/*/SKILL.md", "removed_in": "4.12.0"}]
  },
  "retired_files": [
    {"path": ".claude/skills/dashboard-style/SKILL.md", "state": "unmodified", "owned": true,
     "removed_in": "4.12.0", "removed_commit": "<40-hex>"}
  ],
  "uncommitted_sync": [{"path": ".claude/commands/work.md", "change": "modified"}],
  "warnings": []
}
```

**Definitions.**
- **Manifest categories:** a manifest's `categories` object if present, else the top-level object; keys `sync`, `customize`, `ignore`; a missing or non-list key is an empty list. U = upstream manifest at `REF`; L = local `.claude/sync-manifest.json` (missing or unparseable → all lists empty + warning `local sync-manifest.json missing or unreadable; local patterns treated as empty`).
- **Glob semantics** (patterns against project-root-relative POSIX paths): `**` matches any characters including `/`; `*` matches any characters except `/`; `?` matches one character except `/`; every other character is literal.
- `upstream_version` = `template_version` in `REF:.claude/version.json`; `local_version` = the project's `.claude/version.json` `template_version`. `null` when missing or unreadable.
- `git` = `--project` is inside a git work tree. When false: `uncommitted_sync` is `[]` and warning `project is not a git work tree; uncommitted_sync skipped`.
- **H** = union of the `sync` lists of every parseable version of `.claude/sync-manifest.json` in `git log REF -- .claude/sync-manifest.json` (unparseable versions skipped silently).

**`patterns`.** For each pattern `p` in L.sync (local order, deduplicated) that is not in U.sync: **retired** when `p ∈ H` or `p ∈ U.customize ∪ U.ignore`; otherwise **project_added**. `compare` = U.sync (upstream order, deduplicated) followed by `project_added` (local order). `retired[].removed_in` = `template_version` in `.claude/version.json` at the manifest commit that dropped `p` from `sync`: walk the manifest-changing commits newest → oldest, find the newest one whose `sync` lists `p`; the next newer manifest-changing commit dropped it. `null` when unavailable or when `p` was never in H. `retired` is sorted by `pattern`; `project_added` keeps local order.

**`retired_files`.** Candidates: regular files (not symlinks) under `PROJECT/.claude/`, as project-root-relative POSIX paths; prune directories named `.git`, `node_modules`, `__pycache__`, and `.claude/worktrees`. A candidate `F` is listed when all hold:
1. `F` is not a path in the tree at `REF`.
2. `F` matches no pattern in U.customize, U.ignore, L.customize, L.ignore.
3. `F` was deleted in template history: it appears in `git log REF --no-renames --diff-filter=D --name-only -- .claude/`. `removed_commit` = the newest such commit (full SHA).
4. `owned` = the manifest at `removed_commit^` is parseable and `F` matches one of its `sync` patterns.
5. `state` = `"unmodified"` when `F`'s blob id (`git -C TEMPLATE_REPO hash-object --no-filters <absolute path>`) equals any blob id `F` had in template history (`git log REF --no-renames --raw --no-abbrev --format= -- F`, old and new ids, all-zero ids excluded); otherwise `"modified"`.
6. Listed when `owned` is true **or** `state` is `"unmodified"`.

`removed_in` = `template_version` in `removed_commit:.claude/version.json` (`null` when unavailable). Sorted by `path`.

**`uncommitted_sync`** (only when `git` is true). Parse `git -C PROJECT status --porcelain=v1 -z --untracked-files=all -- .claude`; convert repo-root-relative paths to project-root-relative by stripping `git rev-parse --show-prefix`. Skip renames and copies (`R`/`C`). `change` = `"deleted"` when X or Y is `D`; `"added"` when XY is `??` or X is `A`; otherwise `"modified"`.
- `modified`/`added`: listed when the path matches a `compare` pattern, matches no U.customize/U.ignore pattern, exists at `REF`, and its local blob id equals its blob id at `REF`.
- `deleted`: listed when the path is in the template's deleted set (rule 3 above) and either it was `owned` at deletion (rule 4) or the project's committed blob (`git -C PROJECT rev-parse HEAD:<repo-relative path>`) is among its template-history blob ids (rule 5).
- When at least one path is listed, also list `.claude/version.json` and `.claude/sync-manifest.json` if their status shows a change (`"change": "modified"`).
- Sorted by `path`.

**Expected real-data results** (A verifies early; template history = this repo at `HEAD`): committed-state exports at `<scratchpad>/head/{flirty-gym,difficult-conversation-simplifier}` → retired pattern `.claude/skills/*/SKILL.md` (`removed_in` `4.12.0`) + 3 retired files each (`unmodified`, `owned`, `4.12.0`); `<scratchpad>/head/styler` → the same 3 files, no retired pattern; live `~/Developer/OEMMatInsightBI` → `complete-task.md` and `sync-tasks.md` (`modified`, `owned`, `1.5.0`); other live repos → no retired files. Example tasks (`tasks/task-*.json`) and `dashboard.md` never listed.

### 2. Part 5 text (B implements; strings pinned)

- **Requirements:** add `python3` for `.claude/scripts/sync-check.py` (optional; the prose fallback works without it).
- **Step 2:** run `python3 .claude/scripts/sync-check.py --ref template/{branch}` from the project root after the fetch. Use `patterns.compare` as the sync pattern set; carry `patterns.retired`, `retired_files` and `uncommitted_sync` into Steps 3 and 5. A path matching an upstream `customize` or `ignore` pattern is never compared, even when a sync pattern also matches it. State the glob semantics above. If the script is missing or fails, fall back to (keep it short): retired patterns via `git log template/{branch} -S'"<pattern>"' --format=%h -1 -- .claude/sync-manifest.json` (non-empty → the template once listed it); retired files via `git log template/{branch} --no-renames --diff-filter=D --name-only --format=%H -- .claude/`, keeping paths that exist locally, are absent upstream and match no `customize`/`ignore` pattern, and that were in the `sync` patterns of `git show <commit>^:.claude/sync-manifest.json` or whose `git hash-object --no-filters` id appears in `git log template/{branch} --no-renames --raw --no-abbrev --format= -- <path>`; uncommitted sync via `git status --porcelain -- .claude` (sync files equal to `template/{branch}`: `git diff --quiet template/{branch} -- <path>`; deletions of retired files).
- **Per-file statuses:** "Local only — exists locally but not in template (kept, never flagged)" becomes "Local only — the template never shipped this path (kept, never flagged)"; add "Retired upstream — the template shipped this path as a sync file and later deleted it (offered for removal)".
- **Step 3 report groups** (inside the existing "Template updates available" block):
```
  Retired upstream (the template removed these files):
    .claude/skills/dashboard-style/SKILL.md (removed in v4.12.0; unchanged template copy)
    .claude/commands/complete-task.md (removed in v1.5.0; locally modified)

  Retired sync patterns (the template no longer lists these):
    .claude/skills/*/SKILL.md (dropped in v4.12.0)
```
  Plus, when `uncommitted_sync` is non-empty: `ℹ️ {N} synced files are not committed (an earlier sync was never committed)`.
- **Step 3 queue rows:**
  - `Drop retired sync pattern ".claude/skills/*/SKILL.md" (the template dropped it in v4.12.0)` · file `.claude/sync-manifest.json` · risk `—`
  - `Remove retired template file (removed upstream in v4.12.0; unchanged template copy)` · risk `⚠ deletes`
  - `Remove retired template file (removed upstream in v1.5.0; locally modified, [D] shows the diff)` · risk `⚠ deletes`
  - When `removed_in` is `null`, drop the version: `(removed upstream; …)` / `(the template dropped it)`.
  - `[D]` on a removal row prints `git show {removed_commit}^:{path} | diff -u - {path}` (truncated like other `[D]` output).
- **Fix Queue Protocol risk flag** (new bullet after `⚠ overwrites local`): `` `⚠ deletes` — removes a file: Part 5 retired-template-file rows. Excluded from bare `[A]`; explicit inclusion required. The row says whether the file is an unchanged template copy (nothing local is lost) or locally modified (`[D]` shows the diff against the template's last version). ``
- **Fix Queue Protocol exceptions:** add `**Part 5 Step 5** (commit offer) runs after the batch applies — it commits files, so it asks once.`
- **Step 4 additions:** apply an included removal row with `git rm -q -- {path}` when tracked, else `rm -- {path}`; then remove parent directories left empty, up to but not including `.claude/`; drop `files["{path}"]` from `.sync-state.json`. Write-back: set the local `sync` list to `patterns.compare` plus any retired pattern whose drop row the user did not include (this replaces the v5.7.4 union sentence). Drop `.sync-state.json` entries whose path no longer exists locally.
- **Step 5: Commit offer** (new). Fires when the project is a git work tree and either a Part 5 row was applied in this run or `uncommitted_sync` is non-empty; runs after the batch triage's post-apply summary (or after the report when the queue was empty). Paths = files Part 5 changed or removed in this run, plus `.claude/version.json` and `.claude/sync-manifest.json` when changed, plus `uncommitted_sync` paths; minus gitignored paths (`git check-ignore -q`) and paths with no change in `git status`. Prompt:
```
Template sync changed {N} files and they are not committed:
  M .claude/commands/work.md
  D .claude/skills/dashboard-style/SKILL.md
  M .claude/version.json
Commit them now? [C] Commit as "Sync template v{old} → v{new}" | [L] Leave uncommitted
```
  `{old}` = `template_version` in `HEAD:.claude/version.json` (fallback: the local value before this run); `{new}` = the local value after this run; when equal the message is `Sync template files (v{new})`. `[C]`: `git add -A -- <paths>`, then `git commit -m "<message>" -- <paths>` (commits only those paths, even if other changes are staged). Never pushes. `[L]`: `Left uncommitted. The next /health-check will offer this commit again.` With `--report`: no offer; the `ℹ️` line only.
- **Key Rules:** replace "Local-only files are kept — never suggest removing files that aren't in the template" with: `**Files the template never shipped are never flagged** (e.g. a project's own skills or commands). A file the template shipped as a sync file and later deleted is offered for removal (`⚠ deletes`, explicit inclusion only); nothing is removed without that.` Add to "Sync category only": upstream `customize`/`ignore` lists win over a local `sync` pattern.
- **Batch Fix Triage → Apply mechanics:** add `After the post-apply summary, run Part 5 Step 5 (commit offer) when it applies.` Update the example table only if a row shape changed.

### 3. FB-134 strings (C, D, E)

**(a) C — restore.** Retirement commit: `RETIRE=$(git log --diff-filter=A --format=%H -1 -- .claude/support/retired/$SLUG/manifest.json)` (the commit that added the manifest). Pin check: `git rev-parse "$RETIRE^"` should equal `commit_sha`; when it differs, trust `$RETIRE^` as the last-live state and say so. Routes: (1) default, when `$RETIRE` added only this feature's manifest: `git checkout -b restore/$SLUG && git revert --no-commit "$RETIRE"` — undoes exactly what retirement changed (deleted files, fragments in shared files, dependency lines, the snapshot, and the spec marker when it landed in that commit); (2) when `$RETIRE` retired several features: `git diff "$RETIRE" "$RETIRE^" -- <this feature's affected_paths> | git apply --3way`, then remove this feature's snapshot directory by hand; (3) files only, or no git history: for each `affected_paths` entry absent from the tree, `git checkout "$RETIRE^" -- <path>` (no history: copy the snapshot file); a path that still exists was partly retired — never copy over it; re-apply the removed fragment by hand from `git diff "$RETIRE^" "$RETIRE" -- <path>` (or the snapshot copy). One sentence on why not cherry-pick: `git cherry-pick "$SHA"` replays that commit's own diff (whatever the last pre-retirement commit changed), not the feature. Step 2 adds: retire in one commit that adds the manifest (one feature per commit where practical); after committing, check `git rev-parse HEAD^` equals `commit_sha` and fix the manifest in a follow-up commit if not. README: `commit_sha` = last commit where the feature was live (restore checks out from the retirement commit's parent, which should equal it); no cherry-pick wording (`:55`, `:72`, `:74`, `:86`). `spec_excerpt_path`: `string | null`, key required, `null` when no spec section described the feature (then no `spec-excerpt.md`); Step 1's spec-excerpt bullet says "when the spec described the feature". Lens 5 method step 1: `feature_slug`, `feature_title`, `retirement_date`, `rationale`, `successor_feature` (if any).

**(b) D — notes.** Prepend = `new_text + " " + existing_notes` (just `new_text` when `notes` is empty); never replace. Applies to: `completed` (`report.notes`), `partial` (`"[PARTIAL] " + report.notes`), `partial_resume_pending` (`"[PARTIAL_RESUME_PENDING] " + report.notes`), `blocked` (`"[BLOCKED] " + report.notes`), and `/work complete`'s notes. Completion Notes Contract gains: each write prepends, so a re-implementation keeps the `[VERIFICATION FAIL #N]` trail the verifier reads.

**(e) D — friction.** Task field `resolves_friction`: optional array of `FR-NNN` strings, the friction-register entries this task was created to fix; set when the task is created (or before it is verified) by whoever creates it — e.g. a task filed from an audit finding, a review, or a user request citing FR ids. When the task reaches Finished (per-task verify pass, or `/work complete`), for each listed id whose entry is `open`: `status: "resolved"`, `resolved_by: {"kind": "task", "ref": "<task id>", "at": "<ISO timestamp>"}` via friction-register.md § Status update protocol; ids not in the register, or already `resolved`/`dismissed`, are skipped. `friction-register.md`: `resolved_by.kind` gains `task`; trigger bullet `**Fixing task finished**`; creation rule sentence.

**(c) E — Step 0e.** Step 4 computes MODIFIED with `git diff --name-only --relative HEAD` and UNTRACKED with `git ls-files --others --exclude-standard`, both run from the project root. Step 5: `finished_uncommitted` = tasks with `status == "Finished"`, `completion_date >= last-commit-date`, and at least one `files_affected` entry matching a path in MODIFIED ∪ UNTRACKED (exact path; a directory entry ending `/` that contains one; or a glob matching one). Step 6: `finished_uncommitted < 3` OR no changed files → silent. Messages: default `Step 0e: {N} finished tasks have uncommitted changes in their files ({M} files modified, {K} untracked). Consider committing before continuing. Use \`git status\` to inspect.`; post-handoff `Step 0e: {N} finished tasks have uncommitted changes in their files (prior session paused without committing). Consider committing before resuming work.` One sentence on why: tasks finished and committed earlier the same day have clean files, so they no longer count.

**(d) E — pass rate.** `verification_pass_rate` is `null` when no task has a verification result: hook `round(pass_rate, 2) if verified else None`; `context-transitions.md` example shows `null` with the rule stated beside it; `work-recovery.md` `[computed; null when no task has a verification result]`.

### Contract amendments (2026-10-05, after agents B, D and E reported)

**A1. Exact sync entries beat customize/ignore globs.** Upstream `customize`/`ignore` patterns win over `sync` *patterns*, except for a path the `sync` list names exactly. The current manifest names `.claude/vision/README.md`, `.claude/vision/_feature-vision-template.md`, `.claude/support/previous_specifications/README.md` and `.claude/support/learnings/README.md`, which `ignore` globs also match; under the original rule they would never sync. Applies to Part 5's per-file comparison (B); `sync-check.py` `uncommitted_sync` (the customize/ignore exclusion doesn't apply when U.sync names the exact path); and `retired_files` rule 2 (the exclusion doesn't apply when the manifest at `removed_commit^` names `F` exactly in `sync`).

**A2. Step 5 `[C]` staging.** `git add -- <listed paths that still exist>` (skipped when none exist), then `git commit -m "<message>" -- <paths>`. Never `git add -A`: it exits 128 on a path `git rm` already removed (staging nothing), and with an empty path list it stages the whole tree. Verified on git 2.48.1: the commit holds exactly the listed paths, including `git rm` deletions and working-tree-only deletions; unrelated staged files stay out.

**A3. Notes are newest-first everywhere.** Every write prepends, drift-reconciliation notes included (`drift-reconciliation.md`'s three "Append to the … notes" sentences; `task-schema.md` § Drift Reconciliation Notes). `session-recovery.md` Cases 2–5 match on the task's **newest state tag**: the first of `[BLOCKED]`, `[AGENT TIMEOUT]`, `[VERIFICATION TIMEOUT]`, `[VERIFICATION ESCALATED]`, `[VERIFICATION FAIL #N]`, `[PARTIAL]`, `[PARTIAL_RESUME_PENDING]` found in `notes` (old tags now stay in the history, so "notes containing" would match stale ones). Case 2 no longer clears a note (the status change is enough); Case 3 prepends its `[VERIFICATION ESCALATED] …` note.

**A4. When `resolves_friction` entries close.** When the task is Finished with no pending user review: the per-task pass without `user_review_pending`, `/work complete` (which also completes a pending review), and parent auto-completion (protocol step 7 and `/work complete`'s parent step). A `both`-owned task whose guided test is still pending doesn't close them yet.

**A5. `[PARTIAL]` is added once, by the orchestrator.** implement-agent returns plain notes on `partial` (its Wind-Down Protocol no longer asks for a `[PARTIAL]` prefix). `context-transitions.md` § Implement-Agent Wind-Down steps 3–4 say the agent returns the notes and the orchestrator prepends them with the tag (DEC-004: agents don't write task JSON).

**A6. Handoff size.** The PreCompact hook's `partial_notes` = the first 600 characters of `notes` (newest entries first), with `…` appended when cut.

**A7. Other notes overwrites.** `/breakdown` step 3 prepends `Broken down into N subtasks` to the parent's notes instead of replacing them. `parallel-execution.md`'s line saying verify-agent sets failed tasks back to In Progress names the orchestrator instead.

**A8. Deleted paths in `uncommitted_sync`** (agent A's reading, pinned by its tests): a `deleted` entry must also pass `retired_files` rules 1 and 2 (absent at `REF`; not customize/ignore, with A1's exact-entry exception). Rule 3 alone would offer to commit the deletion of a path the template deleted and later re-added (`.claude/README.md`) or of an ignore-category example file.

**A9. Parent auto-completion and open reviews.** A parent's `resolves_friction` entries close at parent auto-completion only when no subtask has `user_review_pending`; `/work complete` on that subtask re-runs the parent check and closes them then.

Owner changes: D also owns `.claude/support/reference/drift-reconciliation.md` and `.claude/commands/breakdown.md` (A3, A7).

### Review fixes (2026-10-05, independent review: 0 blockers, 5 should-fix, 8 nits; these supersede the text above where they differ)

- **F1 (should-fix):** `uncommitted_sync` lists a modified/added path (present at `REF`) when its local blob id equals **any** blob id the path had in template history reachable from `REF`, not only its blob at `REF`. Equal-to-REF alone missed most of an earlier uncommitted sync once the template moved on (difficult-conversation-simplifier: 26 listed, 36 missed), so `[C]` committed a fragment and hid the rest. Prose fallback and scenario 45 follow (new trace: REF moved past an earlier uncommitted sync).
- **F2 (should-fix):** the prose fallback for uncommitted sync uses `git status --porcelain -uall -- .claude` (without `-uall` a new directory collapses to `?? .claude/support/`) and compares `git hash-object --no-filters <path>` with the template blob ids (`git diff --quiet` reports an untracked file as a deletion).
- **F3 (should-fix):** restore route 2 is `git diff --binary --no-ext-diff --no-color --src-prefix=a/ --dst-prefix=b/ "$RETIRE" "$RETIRE^" -- <paths> | git apply --3way` (the plain form fails on binary files, `diff.noprefix` and `diff.external`). Scenario 48 Trace B gains a binary asset.
- **F5 (should-fix):** `extension-hooks.md`'s "the template ships no skills — any skill dir here is project-owned … untouched by sync" now names the three retired Skills as retired template files Part 5 offers to remove.
- **F7 (should-fix, pre-existing):** `rules/feature-retirement.md` was never lazy: Claude Code loads every `.claude/rules/**/*.md` without `paths:` frontmatter at launch, like `.claude/CLAUDE.md` (code.claude.com/docs/en/memory, checked 2026-10-05), so ~17.7 KB loaded into every session despite `.claude/CLAUDE.md`'s "lazy, NOT auto-loaded" claim (v4.16.0). Fix: `paths:` frontmatter (`".claude/support/retired/**"`), which loads it when Read/Write/Edit touches a matching file (not on Bash reads); the explicit "READ it first" pointer stays. `claude-code-authoring.md` records the loading facts; `.claude/CLAUDE.md` and scenario 35 say how it loads.
- **F6 (nits):** (a) the fallback's retired-files rule names upstream + local customize/ignore and A1's exception; (b) retired-pattern wording says the template "no longer syncs" a pattern (a pattern retired because upstream now lists it as customize/ignore was never "dropped"); (c) "Retired upstream" = the template shipped this path (as a sync file, or this exact content) and later deleted it; "Local only" = present locally, absent upstream, not a retired template file; (d) Step 4 bumps `template_version` only when a sync-file row (update or new file) applied, so a pattern-drop-only run doesn't commit a misleading "Sync template vA → vB"; (e) restore put-back covers decision records (`.claude/support/decisions/decision-*.md`) as well as spec files (both DEC-016-gated); (f) Step 0e step 1 checks `git rev-parse --is-inside-work-tree` instead of `.git` in the project root, so `--relative` works for nested projects; (g) symlink test for the modified/added regular-file guard; (h) Lens 5 declares its direct read of each manifest's excerpt file.
- **F8 (re-verify nits, 2026-10-05):** the architecture map's 2026-07-19 "at least one harness auto-loads `rules/*.md`" caveat (the cause of F7, observed but never fixed) is replaced by the documented rule; Step 5's commit message appends ` (partial: {k} sync files not updated)` when a sync-file row was left unapplied, since a bare `[A]` that applies only new files still bumps `template_version`. Re-verification: all 13 findings fixed, 197 tests on 3.10 and 3.13, 18/18 meaningful mutations caught, downstream `.git/index` files unchanged.
