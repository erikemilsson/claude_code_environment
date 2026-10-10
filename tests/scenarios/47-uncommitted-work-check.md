# Scenario 47 — Uncommitted-work check counts tasks by their files (FB-134)

Conceptual trace test for v5.10.0. `/work` Step 0e counts a Finished task only when at least one of its `files_affected` entries matches an uncommitted file (FB-134 c). `completion_date` is a date, so the old date-only count also caught tasks finished and committed earlier on the day of the last commit. Bundled FB-134 (d): session exports write `verification_pass_rate: null` when no task has a verification result, instead of `0.0`.

## Setup / State

- A git project whose root is the repository root. `.claude/tasks/` is gitignored (as in styler), so task-file edits never appear in MODIFIED or UNTRACKED. Tracked `.claude/` files, such as `.claude/skills/`, do.
- "Last-commit date" is `git log -1 --format=%ct HEAD` as YYYY-MM-DD. MODIFIED = `git diff --name-only --relative HEAD`, UNTRACKED = `git ls-files --others --exclude-standard`, both run from the project root. `{M}` and `{K}` are their sizes.
- Each trace lists the Finished tasks it relies on. No other task is Finished.

## Trace A — the styler case: same-day commit, unrelated dirty files → silent

Command path: `commands/work.md § "Step 0e: Uncommitted-Work Check"`.

State: the last commit is from 2026-10-01 16:00. Tasks 1–4 finished on 2026-10-01, and their files (`src/look/a.ts` to `src/look/d.ts`, one each) were committed in it. The working tree holds three changes no task lists: `.claude/skills/one/SKILL.md`, `.claude/skills/two/SKILL.md` and `.claude/skills/three/SKILL.md` deleted by an uncommitted template sync. They are tracked, so they appear in MODIFIED.

1. Steps 1–3: `git rev-parse --is-inside-work-tree` prints `true`; last-commit date 2026-10-01.
2. Step 4: MODIFIED = the three `SKILL.md` paths; UNTRACKED is empty.
3. Step 5: Tasks 1–4 pass the date test (2026-10-01 ≥ 2026-10-01), but none of their entries matches a changed path, so `finished_uncommitted` = 0.
4. Step 6: 0 < 3 → silent; proceed to Step 0f.

**Expected:** no message. Before v5.10.0 the count was date-only: 4 tasks ≥ 3 with 3 changed files printed `Step 0e: 4 tasks Finished since last commit (3 files modified, 0 untracked)…`, although all four tasks' work was committed. This is styler's live tree at survey time (FB-134 c).

**Pass criteria:** a task whose files are all committed isn't counted, whatever its completion date; dirty files that no Finished task lists never make a task count; no output.

## Trace B — tasks finished after the last commit, files dirty → fires

Command path: as Trace A, through Step 7.

State: the last commit is from 2026-10-01. Task 5 (`src/export/csv.ts`) and Task 6 (`src/export/pdf.ts`) finished on 2026-10-02, Task 7 (`docs/export.md`, a new file) on 2026-10-03. `csv.ts` and `pdf.ts` are modified, `docs/export.md` is untracked, and `README.md` is modified, though no task lists it.

1. Step 4: MODIFIED = `README.md`, `src/export/csv.ts`, `src/export/pdf.ts`; UNTRACKED = `docs/export.md`.
2. Step 5: Tasks 5 and 6 match a modified path exactly, Task 7 an untracked one → `finished_uncommitted` = 3.
3. Step 6: 3 ≥ 3 and there are changes, so Step 7 prints the default form:
   ```
   Step 0e: 3 finished tasks have uncommitted changes in their files (3 files modified, 1 untracked). Consider committing before continuing. Use `git status` to inspect.
   ```
4. Variant: Step 0a consumed and deleted a handoff in this run, so Step 7 prints the post-handoff form instead:
   ```
   Step 0e: 3 finished tasks have uncommitted changes in their files (prior session paused without committing). Consider committing before resuming work.
   ```
5. Step 8: nothing blocks; Step 0f runs next.

**Expected:** the nudge fires on the same threshold as before (3 tasks), now with the reworded message. `{M}` counts all of MODIFIED, `README.md` included, matching what `git status` shows.

**Pass criteria:** modified and untracked files both count as a task's uncommitted changes; the message is the pinned default form (or the post-handoff form after a consumed handoff); `{N}` = 3, `{M}` = 3, `{K}` = 1; `/work` continues.

## Trace C — directory and glob entries

Command path: as Trace A, Step 5's matching rule.

State: the last commit is from 2026-10-01. Tasks 8–11 finished on 2026-10-02:

| Task | `files_affected` | Uncommitted file | Counts? |
|---|---|---|---|
| 8 | `src/reports/` | `src/reports/summary.ts` (modified) | yes: the directory entry contains it |
| 9 | `src/**/*.test.ts` | `src/reports/__tests__/summary.test.ts` (untracked, in a new directory) | yes: `**` crosses `/` |
| 10 | `src/app/api/items/[id]/*.ts` | `src/app/api/items/[id]/route.ts` (modified) | yes: `[id]` is literal and `*` matches `route.ts` |
| 11 | `docs/*.md` | `docs/api/ref.md` (modified) | no: `*` doesn't cross `/` |

1. Step 4: MODIFIED = `docs/api/ref.md`, `src/app/api/items/[id]/route.ts`, `src/reports/summary.ts`; UNTRACKED = `src/reports/__tests__/summary.test.ts`. `git ls-files --others` lists each file inside a new directory, so Task 9's glob sees the file path.
2. Step 5: Tasks 8, 9 and 10 count; Task 11 doesn't → `finished_uncommitted` = 3.
3. Step 7: the default form with `(3 files modified, 1 untracked)`.
4. Variant: Task 11 lists `docs/**/*.md` instead. It counts too, so `{N}` = 4.

**Expected:** directory entries and globs count the same as exact paths. Square brackets are literal: Next.js and Astro route paths such as `src/app/api/wardrobe/[id]/route.ts` (styler) and `src/pages/insights/[slug].astro` (PortfolioWebsite) are exact paths. Read as a character class, `[id]` would match only `i` or `d`, and Task 10 would miss its own file.

**Pass criteria:** a `dir/` entry matches any path under it, at any depth; `**` crosses `/`, `*` and `?` don't; `[`, `]` and every other character are literal; one matching entry is enough for a task to count.

## Trace D — an older Finished task whose file is dirty from newer work → not counted

Command path: as Trace A, Step 5's date test.

State: the last commit is from 2026-10-03. Task 12 finished on 2026-09-20 and lists `src/auth/session.ts`; Task 15 (In Progress) is editing that file now. Tasks 13 (`src/auth/login.ts`) and 14 (`src/auth/logout.ts`) finished on 2026-10-04, and their files are modified.

1. Step 4: MODIFIED = `src/auth/login.ts`, `src/auth/logout.ts`, `src/auth/session.ts`.
2. Step 5: Task 12 fails the date test (2026-09-20 < 2026-10-03) and isn't counted, although its file is dirty. Task 15 isn't Finished. Tasks 13 and 14 count → 2.
3. Step 6: 2 < 3 → silent.
4. Variant (day granularity): had Task 12 finished on 2026-10-03, the last-commit date, it would pass the date test and match `session.ts` → 3 → the message fires, although Task 12's own work was committed. Accepted: the date test is coarse, and the file match only removes tasks whose files are clean.

**Expected:** the date test still applies on top of the file match. A files-only count would have counted Task 12 and fired on 3.

**Pass criteria:** a Finished task with `completion_date` before the last-commit date never counts, even when its file is dirty; an In Progress task editing the same file doesn't count.

## Trace E — no git → no-op

Command path: as Trace A, Steps 1–2.

State: the project is in no git work tree (as with LTP and escalation_map_training). A Finished task from today lists `a.txt`, which exists.

1. Step 1: `git rev-parse --is-inside-work-tree` fails (`fatal: not a git repository`) and prints no `true`, so Step 0e is a no-op: no other git command runs and nothing is printed.
2. Variant: a work tree whose repository has no commits. Step 2's `git log -1` fails, so Step 0e is skipped before Step 4.
3. `/work` proceeds to Step 0f in both cases.

**Variant E2 — a project nested in a larger repository.** The project root is `app/` inside a monorepo; `app/` has no `.git` of its own. Step 1 prints `true`, so Step 0e runs. Step 4, run from `app/`, lists only paths under it, relative to it: with `app/src/a.ts` and `lib/l.ts` modified and `app/src/new.ts` and `lib/x.ts` untracked, MODIFIED = `src/a.ts` and UNTRACKED = `src/new.ts`, which match the tasks' project-relative `files_affected`. The v5.9.0 test for `.git` in the project root made Step 0e a silent no-op here.

**Pass criteria:** no message and no error; `/work` continues. E2: Step 0e runs in a nested project and counts only paths inside it.

## Trace F — markers-only export when no task was verified → `verification_pass_rate: null`

Command path: `.claude/hooks/pre-compact-handoff.sh` (the embedded Python's export block) → schema in `context-transitions.md § "Session Export"`; recovered exports in `work-recovery.md § "Stale Track 2 Recovery"` step 5.

State: `/work pause` wasn't run, and compaction fires the PreCompact hook. `.claude/tasks/` holds Task 1 (Pending) and Task 2 (Finished today, `owner: human`), neither with a `task_verification` result. `.session-log.jsonl` holds one friction marker. There is no `.handoff.json`, and `version.json` has no `template_inbox_path`.

1. The hook writes the structural handoff and, because markers exist, a markers-only export.
2. No task has a verification result, so the export has `"verification_pass_rate": null` (JSON `null`), with `"tasks_completed": 1`, `"claude_assessment": null` and `"export_quality": "markers_only"`. The session log is deleted.
3. Variants:
   - Task 1 has `"task_verification": null` (a cleared result): still `null`, and the export is written. The v5.9.0 hook crashed here (`AttributeError` on `None.get`), wrote no export and kept the session log.
   - Task 1 has a `fail` result: `0.0`, a real zero, since the one result failed.
   - Two `pass` results and one `fail`: `0.67`.
4. The same rule applies to `/work pause` exports (the `context-transitions.md` example shows `null` and states the rule) and to Step 0f recovered exports (`[computed; null when no task has a verification result]`).

**Expected:** before v5.10.0 the hook wrote `0.0` when nothing had been verified, which reads as "every verification failed" in the export corpus.

**Pass criteria:** `null` when no task has a verification result; a number rounded to 2 decimals when at least one does; `0.0` only when results exist and none passed; the hook exits 0 and writes the export in every variant.

## Invariant checks

- Step 0e only reads: it never blocks, commits or edits files.
- Gitignored paths never count: MODIFIED lists tracked files only, and UNTRACKED uses `--exclude-standard`. Tracked `.claude/` files do count (FB-099).
- A task counts only when it is Finished, finished on or after the last-commit date, and at least one `files_affected` entry matches an uncommitted path. A task with no `files_affected` never counts, and an entry outside the project root (`../other-repo/…`, seen in styler) never matches, because git lists only paths inside it.
- The threshold is still 3, and `{M}`/`{K}` describe the whole working tree, as `git status` does, not only the matched files.
- `verification_pass_rate` is a number only when at least one task has a verification result.
