# Plan: v5.14.1 — `/work` loop residuals

**Status:** BUILT AND REVIEWED 2026-10-07; awaiting the user's OK to commit, tag and push
**Closes:** FB-127 (v), (w), (x), (z); (y) baseline-on-disk slice; (u), (h) closed without a settings change
**Not included:** FB-127 (c) (needs an automatic re-dispatch design), (s), the rest of (y)

## Measured first (2026-10-07, read-only, 9 downstream projects)

- Sessions on v5.14.0: 0 (newest sentinel PortfolioWebsite 2026-10-06 17:02, before the sync).
- `.last-clean-exit.json`: present in 9 of 9, never deleted; ages 0, 5, 17, 38, 57, 92, 107, 138, 187 days; 1 inside the 24h fast path.
- In-progress list key: `in_progress_tasks` 7, `in_progress` 1 (PortfolioWebsite), `in_progress_task_ids` 1 (flirty-gym).
- Tasks In Progress or Awaiting Verification now: 0 in all 9.
- Handoffs: 7 on disk, 4 over 2560 bytes. Overflow files: 5 in 3 projects, 30 KB, oldest 71 days.
- Permission mode: user-level `defaultMode: auto`; no project sets one. 8 of 9 projects allow `find` locally; styler also `kill`, `mv`, `lsof`; none allows `rg`.
- The PreCompact hook has no test.

## Decisions (user, 2026-10-07)

1. Ship the six items below as v5.14.1.
2. (v): the sentinel is marked open at the first dispatch (not FB-127's fast-path comparison).
3. (u), (h): closed as absorbed by auto mode, one line in `.claude/README.md § Known Constraints`; no `settings.json` change.
4. (z): the overflow file a handoff names is deleted when that handoff is consumed.
5. (c) left out.
6. Test an absolute screenshot `filename` on the installed Playwright MCP (orchestrator, scratchpad only).

## Build contract

Two implementing agents, scratch mirrors (`dot-claude/` = `.claude/`, plus `tests/`), no shared files.

### File ownership

| Agent | Files |
|---|---|
| A | `commands/work.md`, `support/reference/work-procedures.md`, `support/reference/session-recovery.md`, `support/reference/work-user-flows.md` |
| B | `support/reference/parallel-execution.md`, `support/reference/context-transitions.md`, `hooks/pre-compact-handoff.sh`, new `scripts/tests/test_pre_compact_hook.py`, `tests/scenarios/19-*.md`, `40-*.md`, `52-*.md`, `support/reference/paths.md` if a path row changes |
| Orchestrator | `.claude/README.md`, `version.json`, ship-log, feedback stub, root `CLAUDE.md` |

### Pinned names (both sides cite these exactly)

- **C1 Open sentinel (A).** `work.md § "Before Any Dispatch"` gains a step: at the first dispatch of a session, and the first after a `/work pause` in the same session, write `.claude/tasks/.last-clean-exit.json` with `"open": true` added (Write tool; other keys kept). Clean exit and pause write it without `open` (or `"open": false`). `session-recovery.md`: a sentinel with `"open": true` is not a clean exit → full scan, whatever its timestamp; schema block documents `open`. `context-transitions.md` (B) pause step 6 and `work.md` Step 5 write the sentinel closed; B cites "the sentinel is written closed (`open` absent or false)".
- **C2 Reset at reopen (A).** `verification_attempts` is set to 0 in the same task write that moves a Finished task back to Awaiting Verification (or any non-Finished status) for a fresh verification: `work-procedures.md` "Reopening resets the counter" reworded from "before that dispatch" to "in the write that reopens"; `work-user-flows.md` guided-testing fail does the same. A delta re-check that passes must not lose anything: check and say what happens to the counter on a delta pass.
- **C3 Queue pseudo-code (B).** `parallel-execution.md` loop: a step appends `{task_id, kind: "gate"}` where the orchestrator's evidence gate needs the exclusive resource; the failure branch of the collection loop includes the `delta` re-check case.
- **C4 Hook total (B).** `pre-compact-handoff.sh`: after building the handoff, measure the serialized bytes; over 2560, shorten the per-task notes heads (largest first) until under, and set `"truncated": true`. New `test_pre_compact_hook.py` (stdlib unittest, runs the hook against a temp project; skips cleanly if `bash` is missing). The test count changes from 388; report the new number.
- **C5 Overflow cleanup (A + B).** `context-transitions.md` (B): the handoff records the overflow file's path in a field named `overflow_file` (use the existing field if one already exists, and report its name). `work.md` Step 0a (A): when a handoff is consumed and deleted, the file named in `overflow_file` is deleted with it, only if it is under `.claude/support/workspace/` and matches `handoff-overflow-*.md`; a preserved (concurrent-session) handoff keeps its overflow file.
- **C6 FEEDBACK marker (A).** `work-procedures.md` step 4b (`<!-- FEEDBACK:{id} -->` dashboard read) removed; renumber nothing else.
- **C7 Baseline on disk (A).** `work.md § "Before Any Dispatch"`: the residue baseline is also written to `{scratch}/residue-baseline.txt`; `work-procedures.md` Residue check reads it when the baseline is no longer in context; only when neither exists is the check report-only. B's `parallel-execution.md` cites it if it restates the baseline.

### Unverified claims in the briefs (agents check and report)

- The fast path may also miss recovery (not only the residue look) of a task stranded by a session that was cut off after an earlier clean exit.
- Resetting the counter at delta reopen loses nothing `verification_history` doesn't hold.
- `overflow_file` may already exist under another name.

### Amendments

From the two sides' returns (2026-10-07):

- **A1 (C5).** The handoff field already exists as `overflow_ref`; `overflow_file` is dropped. Both sides use `overflow_ref`.
- **A2 (C1).** Trigger simplified: every "Before Any Dispatch" run (dispatch or SendMessage resume) marks the sentinel open unless it is known to be open; a batch marks once; when unsure it reads the file. "First after a pause" is not reliably recognisable (Step 5 and `/work complete` also close it; compaction forgets).
- **A3 (C1).** The reader accepts `in_progress` and `in_progress_task_ids` from older sentinels; `in_progress_tasks` is the one key written.
- **A4 (C2).** Delta step 1 writes the counter to 0 with Awaiting Verification; a delta pass restores it to the attempt number of the pass it follows (newest history entry without `delta`), so the end state matches v5.14.0.
- **A5 (C4).** When cutting notes heads is not enough (12 In Progress tasks with empty notes = 3881 bytes), the hook drops `active_work` entries from the end and writes `active_work_omitted: N`. `truncated` and `active_work_omitted` are hook-only keys.

## Build

Both sides copied back by file list 2026-10-07 (11 files changed, 1 new test file); 396 tests green on 3.13.15 and 3.10.20 (388 + 8 hook tests; 3 of the 8 fail against the old hook).

Decision 6 result: an absolute screenshot `filename` works on the installed Playwright MCP when the directory exists; with a missing parent directory it fails with `ENOENT` (the MCP does not create it). `/work` creates the evidence directory before dispatch, so the shipped path holds; the move-before-return fallback is not needed for this case.

Settled by the implementing agents, not decided by the user (under review):

- **S1** = A1. **S2** Step 0a's stale-handoff delete (item 3) also deletes the overflow file. **S3** `residue-baseline.txt` carries a first line naming its dispatch; the check uses the file only if that line names the returning dispatch. **S4** The previous-session residue look also runs when the sentinel is open and a task is In Progress. **S5** Step 5 does not close the sentinel while an agent is still running. **S6** = A4. **S7** `work-user-flows.md`: CLI-direct `[F] Needs fixes` follows the failed-step path, reset included. **S8** The open mark applies to SendMessage resumes too.
- **T1** = A5; entries are dropped in glob order; if `active_work` is empty and the file is still over, it is written as is. **T2** "Largest first" is one common ceiling found by binary search. **T3** A fresh verify-agent called for by a delta's step 5 joins the queue tail as a `verify` entry when exclusive (v5.14.0 text could start two exclusive jobs). **T4** A queued gate dual-writes friction markers at the return. **T5** = hook-only keys.

Seams not yet closed (for the reviewer, then the fixer):

- `work-procedures.md` "Post-verify delta" step 5 says "dispatch a fresh verify-agent now"; T3 needs it to defer to the queue in parallel mode.
- Scenario 52 Trace A step 8 and Trace C step 2 counter values against A4; Trace 19F's names against side A's edited text.
- `task-schema.md` (`verification_attempts` and `attempt` rows), `commands/feedback.md:423` (FEEDBACK markers), scenarios 27–30 (sentinel without `open`): unowned, not edited.

Open questions for the user (not settled by agents):

- **Q1** A task stranded In Progress under 24h ago matches no recovery case even on the full scan (case 6 needs `updated_date` over 24h); Step 3 routing has no In Progress branch. Option: case 6 applies at any age when the sentinel is open (adds a prompt after a cutoff).
- **Q2** Inline implementation makes no dispatch, so it never marks the sentinel open.
- **Q3** Overflow files still orphaned when a later pause in the same session overwrites a handoff that names one (delete-on-overwrite was drafted and removed: after compaction the old file may be the only copy).
- **Q4** A guided-testing fail reopens a Finished task without the delta path's "others have built on it" guard.

## Review (2026-10-07)

Independent read-only review of the uncommitted diff. No blocker; six should-fix (F1–F6), nits F7–F14. D7–D17 of v5.14.0 intact; every cross-file citation resolves; hook output byte-identical at ≤ 2560 bytes (152 randomized handoffs, both Pythons); 26 hook mutants, 21 caught (survivors: `>=` at the trigger, drop-from-front, three harmless or equivalent). Fixes pending.

- **F1 should-fix (C1)** A sub-mode (`/work complete`, `/work pause`) skips Step 0b and its sentinel write closes a sentinel another session left open, so the cutoff is hidden again. Fix: Step 5 item 3 keeps `open: true` when the sentinel on disk is open and this session neither marked it nor ran Step 0b.
- **F2 should-fix (C1/Q1)** Scenario 19F (`:198`, `:210`), `context-transitions.md:243` and `pre-compact-handoff.sh:173` claim a stranded In Progress task is recovered; case 6 needs `updated_date` over 24h and Step 3 has no In Progress branch. Reword, or adopt Q1's option.
- **F3 should-fix (T3 seam)** `work-procedures.md:135-137` "dispatch a fresh verify-agent now / at once" vs the queue-tail rule in `parallel-execution.md`.
- **F4 should-fix (C2/A4)** `task-schema.md:366` (delta `attempt` "repeats the current value", now 0), `:359`, `:135` stale.
- **F5 should-fix, low (C4/T1)** The hook's drop loop can empty `active_work` and still miss the bound (600 tasks Finished today + 1 In Progress = 8081 bytes); a 5000-character title drops its entry instead of being cut.
- **F6 should-fix, low (C3)** "or a delta re-check" unqualified at `parallel-execution.md:392`, `:416`: a non-exclusive delta returning while an exclusive verifier runs triggers "run the head"; a delta pass's gate skips the busy-queue check.
- **F7 nit+** README Known Constraints line omits `rm` and the baseline redirect; "once per session" likely wrong for Bash (saved per project); "auto mode handles them without asking" is absolute against FB-077.
- **F8 nit (C7/S3)** The baseline file's first line names a dispatch, so after compaction a queued verifier or incremental dispatch of the same batch doesn't match → report-only. Fix: name the batch.
- **F9 nit** Stale and unedited: scenario 37:46, scenario 07 Trace B (`:39-68`), `commands/feedback.md:423`, `workflow.md:449`, `tests/README.md:72,114,125`.
- **F10 nit (C5)** The overflow file is deleted at Step 0a item 6, before the session knows whether the summary is enough; `context-transitions.md:277-281` (stale) doesn't mention the overflow delete (S2); no stale variant in 40E.
- **F11 nit (C3/T4)** A queued gate's kept report lives in conversation only; after compaction, recovery re-verifies and friction markers are written twice.
- **F12 nit (tests)** Nothing pins exactly 2560 or which entries are dropped; list/null/non-UTF-8 task files exit the hook 1 (pre-existing); `truncated` and `active_work_omitted` have no reader.
- **F13 nit** Scenario 52 Trace A step 8 / step 3, Trace C step 2 counter wording; 19F fail indicator `:217`; 19F "no dispatch" variant.
- **F14 style** "closed (`open` absent or false)" defined five times; overflow deletion stated five times; hook cut three times; T3 three times; `work.md:530` bullet about 190 words.

Reviewer on the settled items: S1, S4–S8, T2–T5 sound; S2 can stand but extends decision 4 (tell the user); S3 → F8; **T1 goes back to the user** (dropping task ids contradicts the Path A rule at `context-transitions.md:203`, and can be futile, F5).
Reviewer on Q1–Q4: Q1 likely, medium cost (every implement cutoff followed by `/work` within 24h; a daily user's sentinel never goes stale); Q2 unlikely, cheap; Q3 moderately likely, low cost (`/health-check` already offers workspace files over 30 days); Q4 low to moderate, low cost.
Could not check: live permission-prompt behaviour, SendMessage resume after compaction, Linux fallbacks, a real downstream run.

### Decisions after review (user, 2026-10-07)

- **D7 (Q1, F2).** Recovery case 6 (In Progress) applies at any age when the sentinel is open; one prompt after a cutoff is accepted. Scenario 19F then stands.
- **D8 (T1, F5; replaces A5/T1).** The hook never drops an `active_work` entry. Over the bound it cuts notes heads, then titles and `recently_completed`, then reduces entries to the task id and its ready-for-verify flag; still over, it writes the handoff over the bound with a flag, as `/work pause` does. `active_work_omitted` is removed.
- **D9 (F10).** Decision 4 stands: the overflow file is deleted when the handoff is consumed; the session reads it first when the handoff names one.
- **D10 (S2).** A stale handoff's overflow file is deleted with it.
- **D11 (Q2, Q3, Q4).** Left open under FB-127.
- **D12.** F1, F3, F4, F6, F8, F9, F11–F14 go to one fixer on a fresh mirror, unowned files included, then the same reviewer re-verifies. F7 (README) fixed by the orchestrator: `rm` added, "once per session" and the absolute auto-mode claim removed.

## Fix pass (2026-10-07)

One fixer on a fresh mirror applied D7–D10 and F1–F6, F8–F14 (F7 by the orchestrator). 17 files changed in the pass, copied back by file list; 401 tests green on 3.13.15 and 3.10.20 (388 + 13 hook tests; 6 of the 13 fail against the first-build hook; fixer reports 25 hook mutants, 0 surviving). The same reviewer is re-verifying.

Hook cut order under D8: notes heads → titles over 60 characters down to 60 → `recently_completed` (prefix that fits) → remaining titles → every entry reduced to `task_id` + `ready_for_verify` → still over: written as is. `truncated` is the only flag. Measured: a reduced entry is 68 bytes; fits up to about 32 tasks in flight (30 = 2390 B, 34 = 2662 B, 50 = 3750 B, 300 = 20951 B).

Settled by the fixer, not decided by the user (U1–U12; under re-verification):

- **U1** The title/`recently_completed` stage split above (`TITLE_KEEP = 60`). **U2** `truncated` alone carries the still-over case. **U3** Reduction applies to all entries at once. **U4** `context-transitions.md`: a reader accepts a reduced entry when `truncated` is set (Step 0a item 2's "missing required fields" delete is unchanged).
- **U5** New `work.md` Step 3 paragraph "Continued from recovery": a task continued with `[C]` from recovery case 6 is routed as if requested by id, after verification items, to implement-agent. Also makes `[C]` true for the over-24h case, which promised routing the algorithm did not do.
- **U6** Case 6 presents all matching tasks in one prompt; its wording takes `{since}` (open sentinel: "since a session that did not end cleanly (last updated {date})").
- **U7** A stale handoff's overflow file is deleted unread; read-first applies to consumption only. **U8** F1: when the session can't tell after compaction, the sentinel is kept open. **U9** Incremental re-dispatch adds the new task's id to the baseline file's first line. **U10** `active_verifiers` entries are marked `exclusive` (and `delta`); "busy" is defined on that mark. **U11** `shared-definitions.md:170` FEEDBACK-marker text fixed too. **U12** Scenario 19F gained two variants, 40D four.

Left by the fixer: D8's order costs the notes head before `recently_completed` in the many-finished-today case; an open sentinel can belong to a live concurrent session or to this session after a mid-run compaction (case 6's "no agent currently running" guard is the only protection; no "leave it" option); a cleanly paused In Progress task under 24h still has no Step 3 branch (outside D7); `dashboard-regeneration.md:338` and scenario 07's Context and Trace E still describe an editable dashboard (FB-127 (a)/(j)).

## Re-verification (2026-10-07)

Same reviewer, against the fixed text: F1–F14 fixed (F1 with one residual, G3); D7 traced end to end and executable; U1–U12 stand (U4 → G1; U5 stands and also changes the over-24h `[C]`, which previously routed nothing; U8 → G4). Nothing holds the release. 401 tests on 3.13.15; hook tests 13/13 on both Pythons; byte-identical to the v5.14.0 hook on 103 fitting handoffs and at 2558–2560 bytes; 400 randomized projects: 0 over the bound, 0 wrong id sets; capacity 32 tasks in flight (2526 B), 33 over; 40 hook mutants, 37 caught (fixer's "0 surviving" not replicated; survivors: last title stage skipped, `TITLE_KEEP = 20`, `recently_completed` suffix instead of prefix). New findings (fixes pending):

- **G1 nit+ (U4)** `work.md` Step 0a item 2 and `context-transitions.md` Restoration step 2 still delete a handoff with "missing required fields"; a reduced (`truncated`) handoff lacks four required entry fields. Fix: one clause in both.
- **G2 low (D7/U5)** Case 6 has no owner filter: with the sentinel open, an `owner: human` In Progress task is asked about after every cutoff and `[C]` routes it to implement-agent.
- **G3 low (F1 residual)** The Step 5 exception requires "this session neither marked it open"; a fresh session's `/work complete` that needs a verify dispatch re-marks the already-open file, then closes it. Fix: key on "already open when this session first read it, and Step 0b did not run".
- **G4 low (U8)** "Can't tell after compaction: keep it open" hits the most common pause (long session, compaction, pause); the next `/work` then prompts for every paused In Progress task. Fix: a session that ran `/work` or dispatched in this conversation counts as having marked it.
- **G5 nit (U3)** Reduction cliff: 8 tasks = 2530 B whole, 9 tasks = 962 B reduced, about 1600 B unused up to roughly 25 tasks. D8-literal.
- **G6 nit (U5)** The `[C]` choice lives in conversation only; compaction before later continued tasks are reached strands them again.
- **Open-sentinel owner (unsettled).** An open sentinel may belong to a live concurrent session (the "no agent currently running" guard is not evaluable there; `[C]` double-dispatches, `[P]` dispatches without asking again, `[H]` is overwritten; the second session's Step 5 then closes the first's sentinel) or to this session after a mid-run compaction (partly evaluable). Reviewer: low likelihood, high cost. Options: a fourth choice `[L] Leave`, or a warning line when a `pre_compact` handoff is recent or the task's `updated_date` is today.

### Decisions after re-verification (user, 2026-10-07)

- **D13 (open-sentinel owner).** Case 6's prompt gains a fourth choice, `[L] Leave` (another session or a running agent has it: the task is not touched and not routed this run), and one warning line when the task's `updated_date` is today.
- **D14 (G5).** After reducing entries, the hook restores titles while they fit.
- **D15.** G1–G4, G6 and the three missing hook tests (last title stage, `TITLE_KEEP`, `recently_completed` prefix) go to the same fixer on a fresh mirror, then the same reviewer re-verifies.

## Second fix pass (2026-10-07)

Same fixer, fresh mirror: D13, D14, G1–G6 applied. 7 files changed in the pass, copied back by file list; 407 tests green on 3.13.15 and 3.10.20 (388 + 19 hook tests). The same reviewer is doing the final re-verification.

Correction from the fixer: its first-pass "25 mutants, 0 surviving" was not a measurement (the harness failed on import and counted every run as caught). This pass: 42 mutants listed one by one, 40 caught, 2 surviving and equivalent (binary-search variants).

Hook sizes now (short ids, 13-character titles): 8 tasks 2559 B whole; 9 tasks 1295 B with 9 of 9 titles back; 20 tasks 2461 B, 20 of 20; 25 tasks 2538 B, 13 of 25; 32 tasks 2526 B, none; 33 over.

Settled by the fixer in this pass (V1–V9; under re-verification):

- **V1** Restored titles are cut to 60 and go back in `active_work` (glob) order as a prefix, stopping at the first that doesn't fit. **V2** A non-string title is never cut or restored. **V3** The sentinel is kept open after `[L]` only when it was open at the answer (narrows the brief's "written open whenever `[L]` was chosen": with a closed or missing sentinel no owner has it open). **V4** If compaction loses the `[L]` answer but shows `/work` ran, the sentinel is written closed; nothing is persisted for `[L]`. **V5** "Continued from recovery" keys on notes beginning with `[CONTINUE`, not on the newest-state-tag list. **V6** Note text `[CONTINUE {YYYY-MM-DD}] continued from recovery`. **V7** Case 6 asks about `owner` `claude` and `both`, never `human` (also removes human tasks from the old over-24h prompt). **V8** "Kept open" rule (b) is per conversation. **V9** Capacity wording "more than about 32 tasks in flight".

Left by the fixer: a continued task that is dispatched and still running keeps `[CONTINUE]` first in its notes, so after a compaction only "no agent running" stops a second dispatch; a `misaligned` return writes no notes and keeps the status, so such a task is routed again by its `[CONTINUE]` note; with `[L]` the run goes on dispatching other tasks.

## Final re-verification (2026-10-07)

Same reviewer: G2–G6 fixed, G1 fixed in `work.md` only (→ H4); D13 traced for a live concurrent session and for the same session after compaction: `[L]` writes nothing, the task is not routed, the sentinel stays open. Sentinel scenarios (i)–(iv) confirmed; (v) and (vi) below. Hook: 19/19 on both Pythons; 53 mutants, 53 caught (the reviewer's own set, including its three earlier survivors and the title-restore mutants); byte-identical to the v5.14.0 hook on 103 fitting handoffs and at 2558–2560 bytes; every in-flight id present in 297 randomized over-bound cases and for 9–300 tasks; sizes confirmed (32 fit, 33 over; with four-digit ids 32 is already over at 2599 B). Every citation resolves. The full 407-test suite was not re-run by the reviewer (run by the orchestrator on both Pythons after the copy-back). Nothing holds the release. New, not yet fixed:

- **H1 low (pre-existing)** `session-recovery.md` case 1 has no "agent running" guard and no prompt: with an open sentinel owned by a live session, an Awaiting Verification task whose verifier is still out gets a second verify-agent. `[L]` does not cover it. Fix: when the sentinel is open and the task's `updated_date` is today, case 1 asks (verify now / leave).
- **H2 low** `[L]` answered on a task that already carries a leading `[CONTINUE]` is still routed by `work.md` "Continued from recovery". Fix: "and not left with `[L]` in this run".
- **H3 low** A continued task keeps `[CONTINUE]` first in its notes after dispatch, after a `misaligned` return and after a zero-token return, so it can be routed again. Fix: the "Continued from recovery" dispatch prepends a note (e.g. `[RE-DISPATCHED {date}]`).
- **H4 nit** `context-transitions.md:274` Restoration step 2 lacks the `truncated` exemption `work.md:74-75` has.
- **V3 → user.** `[L]` in the over-24h case with a closed sentinel leaves it closed, so a daily user is not asked about that task again until the sentinel is over 24h old. The alternative (keep it open whenever `[L]` was chosen) costs one full scan per run.
- **V4 stands** (narrow); option if wanted: a `left: [ids]` key in the sentinel. **V7 stands**: human-owned tasks leave the old over-24h prompt too (it offered routing a human task to implement-agent).

### Decisions after the final re-verification (user, 2026-10-07)

- **D16 (V3; replaces V3).** `[L]` always leaves the sentinel written open at Step 5, whatever its state at the answer. One full scan and one repeat prompt per run until the task moves is accepted.
- **D17 (H1).** Not fixed here; carried to FB-104 (concurrency).
- **D18.** H2, H3, H4 and D16 go to the same fixer on a fresh mirror; the same reviewer checks those lines; then release bookkeeping.

## Third fix pass and last check (2026-10-07)

Same fixer, fresh mirror: D16, H2, H3 applied (3 files: `work.md`, `session-recovery.md`, scenario 19); H4 needed no edit (the exemption was already at `context-transitions.md:275`; the reviewer's check had matched line 274 only, and it withdrew the finding). The dispatch made by "Continued from recovery" prepends `[RE-DISPATCHED {YYYY-MM-DD}]` in the existing "If Executing" pre-dispatch write. Settled by the fixer: W1 the tag is not a state tag; W2 rule (a) says "may still be working on it"; W3 the rule's intro dropped "kept". 407 tests green on 3.13.15 and 3.10.20 after the copy-back.

Same reviewer, changed sentences only: D16, H2, H3, H4 confirmed; `[RE-DISPATCHED` collides with nothing; a continued task always dispatches through "If Executing" (a parallel batch is built from Pending tasks only); scenarios (i)–(iii) unchanged. Nothing holds the release. The shipped text is exactly what the reviewer last saw. New, not fixed, carried to FB-127:

- **J1 nit (D16 consequence)** → FB-127 (af): after `[L]` with a closed sentinel, the next `/work` finds it open, words the prompt "since a session that did not end cleanly", and asks about every In Progress `claude`/`both` task of any age, on each run while the user keeps answering `[L]`.

Carried: Q2–Q4 → FB-127 (aa)–(ac); the paused-In-Progress routing gap → (ad); V4 → (ae); H1 → FB-104. Not run: a real `/work` session, a real PreCompact event, Linux.
