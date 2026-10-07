# Plan: v5.14.0 — `/work` loop protocol bundle

**Status:** BUILT AND REVIEWED 2026-10-07; awaiting the user's OK to commit, tag and push
**Closes:** FB-130, FB-131, FB-132, FB-133; FB-119 gaps 1–4; FB-127 (l), (o), (t) ((c) withdrawn, D11)
**Not included:** FB-127 (s) (needs a `settings.json` permissions change); FB-112.

## Measured first (2026-10-07, read-only, 9 downstream projects)

- Handoffs on disk: 7; 4 over 2.5KB (flirty-gym 4207B, escalation_map_training 3087B, conversation_opener 3079B, OEMMatInsightBI 2609B); 2 overflow files exist.
- Root-level images: styler 70 PNGs (all hidden by a project-added `/*.png` ignore line), escalation_map_training 1, others 0.
- Task files mentioning playwright/browser/rendered/screenshot (loose keyword count): PortfolioWebsite 57/79, styler 102/313, conversation_opener 11/19.
- Project-own scripts under `.claude/scripts/`: styler only (4), the known `test_python_floor.py` failures.

## Decisions (user, 2026-10-07)

1. Ship everything below as one release, v5.14.0.
2. Delta bound: files already in the task's `files_affected`; no line cap.
3. Browser conflicts: implement in parallel, verify one at a time.
4. After a limit cutoff the inline size bound still applies; a larger task goes on the Needs-you card.
5. Residue: the orchestrator stops servers the agent started, moves stray root files to scratch, then reports.
6. FB-127 (s) left out.

## Build contract

Two implementing agents, scratch mirrors (`dot-claude/` = `.claude/`, plus `tests/`), no shared files.

### File ownership

| Agent | Files |
|---|---|
| A (verification + dispatch) | `commands/work.md`, `support/reference/work-procedures.md`, `rules/agents.md`, `agents/verify-agent.md`, `agents/implement-agent.md`, `support/reference/task-schema.md` |
| B (reference docs + tests) | `support/reference/context-transitions.md`, `parallel-execution.md`, `mcp-patterns.md`, `work-recovery.md`, `work-user-flows.md`, `scripts/tests/test_python_floor.py`, `tests/scenarios/40-handoff-schema-cap.md`, new `tests/scenarios/52-post-verify-delta-and-residue.md`, `tests/README.md` if it indexes scenarios |
| Orchestrator | `version.json`, ship-log, feedback stubs + archive, root `CLAUDE.md` |

### Pinned names (both sides cite these exactly)

- **C1 Post-verify delta.** Canonical body: `work-procedures.md`, a block titled `**Post-verify delta (after a per-task pass):**` (A). Allowed only when all hold: the task passed per-task verification in this session; the change is the verifier's own non-blocking finding or a micro-edit the user approved; it touches only files already in the task's `files_affected`; the same verifier can be resumed. Sequence: set the task Awaiting Verification → make the edit → prepend a `[DELTA {YYYY-MM-DD}]` note (what changed, why) → resume the same verifier with SendMessage, giving the diff and asking for the standard per-task report → apply "After verify-agent returns (per-task mode)" with the new `verification_history[]` entry carrying `"delta": true` (attempt number and `verification_attempts` increment as for any attempt; `cost` recorded). Fail → the normal fail path. Anything outside the conditions → a fresh verify dispatch. The orchestrator never marks a delta as passed itself. `task-schema.md` documents the optional `delta` key (A) and notes that DEC-025 cost counts exclude delta attempts.
- **C2 Single-instance resources.** Canonical body: `parallel-execution.md § "Single-Instance Resources"` (B). Rule: tasks may be implemented in parallel, but verifications that need the same single-session MCP (browser/Playwright) run one at a time; tasks that rebuild the same build output directory don't share a batch. Judged from the tasks' criteria and the project's build command; no new task field. `work.md` Step 2c summary cites the section by that name (A). `mcp-patterns.md` drops "lower priority" and points there (B).
- **C3 Residue check.** Canonical body: `work-procedures.md`, a block titled `**Residue check (after any agent returns):**` (A), also run after an infrastructure termination. Compare `git status --short` with the pre-dispatch state; check the ports the agent reported using (and the project's usual dev port) for listeners; stop servers the agent started; move stray files in the project root to the evidence directory; untracked probe files elsewhere are reported, not deleted; tell the user what was found. It never stops a process the agent did not start, and "Respect prior kills" still governs restarts. `parallel-execution.md` and `work-recovery.md` cite `work-procedures.md § "Residue check"` (B).
- **C4 Evidence directory.** Every implement and verify dispatch brief names a per-dispatch directory for screenshots and scratch files: `{scratch}/agent-{task_id}-{role}/`, where `{scratch}` is the session scratchpad when the harness lists one, else a fresh `mktemp -d` directory; never the project root, never a generic shared name. `verify-agent.md` (Web UI row) and `implement-agent.md` say to pass that path as the screenshot filename (A).
- **C5 Handoff total.** `context-transitions.md` (B): after writing the handoff, measure it (`wc -c`); over 2560 bytes runs the overflow procedure on the total, largest field first, and re-measures. Overflow file: `handoff-overflow-{YYYY-MM-DD-HHMM}.md`.
- **C6 Inline contract** (`rules/agents.md`, A; always-loaded, so keep it tight): (1) inline work runs implement-agent's "search for what your change invalidates" step; (2) a task whose deliverable is a `.claude/` path is inline at any difficulty; (3) the inline size bound still applies after a limit cutoff or zero-token return: a larger task is not implemented inline, it goes on the Needs-you card (also at the FB-103 bullet in `work-procedures.md`); (4) claims the orchestrator puts in a dispatch brief are measured or labelled unverified, and the brief tells the agent to challenge them; fixtures for a producer-consumer pair come from the producer's own emit path or tests.
- **C7 Small ones.** (c) the sequential implement dispatch in `work.md` states a turn budget, the same figure parallel mode uses (A reads `parallel-execution.md`, does not edit it). (l) `work-procedures.md`: backfill `cost` when the completion notification arrives after the report (A). (o) `user_feedback` is appended newest-first with a date prefix, never overwritten: `work-user-flows.md` (B) and the `work-procedures.md` sites (A), same convention as task `notes`. (t) `test_python_floor.py` tests a fixed tuple of the 7 shipped scripts; when `template-maintenance/` exists at the repo root it also asserts the tuple equals the glob (B).

### Amendments

From side A's return (2026-10-07):

- **A1 (C3 baseline).** The pre-dispatch baseline is `git status --short` plus `ls -A` of the project root (styler's root PNGs are gitignored, so git alone misses them) plus an `lsof` check of the project's usual dev port. Recorded in `work.md § "Before Any Dispatch"` (new subsection: Residue baseline, Evidence directory, Claims in the brief).
- **A2 (C3 attribution; narrows decision 5).** The orchestrator stops a listener only on a port the agent reported in `servers_started`. Any other new listener, and every listener after a cutoff (no report exists), is ask-first. *Confirmed by the user 2026-10-07 (decision 5 as narrowed).*
- **A3 (C4).** Phase-level verification uses `{scratch}/agent-phase-{phase}-verify/`.
- **A4 (C4).** New report field `servers_started: [{command, port, stopped}]` in implement-agent Step 6 and both verify-agent report schemas. Side B cites it by that name.
- **A5 (C7 o).** Convention lives in `work-procedures.md § "State Persistence Protocol"` ("`user_feedback` is history too, newest first, dated"): `"[YYYY-MM-DD] " + new_text + "\n" + user_feedback`. Side B's `work-user-flows.md` cites it.
- **A6 (C1).** `verify-agent.md` Step T7 gains a "Delta re-check" paragraph so the resumed verifier knows what to return.
- **A7 (C4/C6).** `parallel-execution.md` § 3 and § 4 dispatch briefs cite `work.md § "Before Any Dispatch"` for the evidence-directory and brief-claims lines (side B).

Open after side A (for the reviewer or a follow-up):
- `parallel-execution.md:272` (`partial` by tool call 35) and `implement-agent.md § "Approaching Usage Limits"` (`partial_resume_pending` at 75%) disagree; predates this release.
- `browser_take_screenshot`'s `filename` may reject an absolute path on some Playwright MCP versions; a move-before-return fallback is written but untested.
- The residue baseline is held in context, so it does not survive compaction or an orchestrator crash.
- Not touched: `commands/diagnose.md:153-155` (screenshots with no path); "fresh context" wording in `.claude/CLAUDE.md:44` and `workflow.md:187`; `<!-- FEEDBACK:{id} -->` markers still read in `work-procedures.md` step 4b (FB-127 (j) residue).

### Decisions after review (user, 2026-10-07)

- **D7 (R1; narrows decision 5).** The residue check moves only regular evidence-shaped files (images, logs, traces, temp scripts), and only when the agent returned a report and no other agent is running. Every other new root entry is reported with its path. After a cutoff or termination nothing is moved. The destination is always printed.
- **D8 (R2).** Baseline all listening ports before dispatch (`lsof -nP -iTCP -sTCP:LISTEN`). After the return: new and reported in `servers_started` → stop; new and unreported → ask first; present at baseline → never touched. No baseline → report only.
- **D9 (R4; restores decision 3; replaces C2's build clause).** The build is treated like the browser: implement briefs in a batch say not to run the production build (type-check and tests only); verifications that build or use the browser, and the orchestrator's own client-bundle check, take turns in one exclusive-verify queue. A task is held out of a batch only when its implementation can't proceed without running the build.
- **D10 (R5, R11; replaces C1's "increment as for any attempt").** A delta fail or refusal does not count toward the 3-attempt escalation; a refusal leads to a fresh verify dispatch. A delta is allowed only while no dependent task has started and the phase hasn't been verified.
- **D11 (R10).** FB-127 (c) is dropped from this release: the sequential implement dispatch states no turn budget. The parallel/sequential wind-down mismatch stays open under FB-127 (c).
- **D12.** All remaining findings (R3, R6–R9, R12–R18) are fixed by one fixer agent on a fresh mirror, unowned files included, then re-verified by the same reviewer.

## Review

Both sides copied back 2026-10-07; 388 tests green on 3.13 and 3.10. Independent read-only review of the uncommitted diff, findings R1–R18 (fixes pending):

- **R1 blocker** Residue check moves any new root entry not in `files_modified`/`files_affected`: would move `node_modules/`, `dist/`, a user's or second session's file, a killed agent's legitimate new file, a running sibling's file. `parallel-execution.md` "everything left … is attributable" is false. Fix: move only regular evidence-shaped files (images, logs, traces, tmp scripts), only with a report and no other agent running; everything else reported with its path; after a termination report-only; always print the destination.
- **R2 blocker** Baseline records only "the project's usual dev port" (defined nowhere), so "was listening at baseline" can't be evaluated for other ports; a user's server on a mis-reported port could be stopped; the FB-133 second listener (port+1) is never probed. Fix: baseline all listeners (`lsof -nP -iTCP -sTCP:LISTEN`), diff after return: new + reported → stop; new + unreported → ask; present at baseline → never touch.
- **R3 should-fix** Delta step sends `git diff -- <files>`, which is the whole uncommitted implementation, not the delta (no per-task commits), and the verifier is told to fail a diff that "is not small". Fix: copy the files to the evidence directory before the edit and send `diff -u` old vs new.
- **R4 should-fix (design)** The build-output rule ("or the project's checks include the build") serialises implementation in UI-heavy projects, undoing decision 3. Fix: treat the build like the browser: implement briefs say no production build (type-check and tests only); building verifications and the orchestrator's client-bundle check take turns in one exclusive-verify queue; hold a task out of a batch only when its implementation can't proceed without the build.
- **R5 should-fix** Delta outcomes: a delta fail can hit the 3-attempt escalation over a cosmetic edit; the verifier's out-of-scope refusal is a counted `fail`; the two-invalid-reports rule contradicts the step it cites.
- **R6 should-fix** `session-recovery.md` (untouched) re-verifies every Awaiting Verification task at once (recreates the browser collision) and has no residue look; `work-recovery.md`'s residue line is unreachable after a platform cutoff.
- **R7 should-fix** Two `user_feedback` formats (side B's `notes`-style vs A5).
- **R8 should-fix** `parallel-execution.md` lacks `servers_started` and the `work.md § "Before Any Dispatch"` citation (A4, A7 not done); evidence line stated twice in different words; its baseline is `git status` only; brief-claims line missing.
- **R9 should-fix** "Don't use the browser MCP" line is conditional on batch composition at build time; incremental re-dispatch and the orchestrator's own gate miss it. Fix: every browser task's implement brief in parallel mode.
- **R10 should-fix** Turn budget: sequential now says 40 with `partial_resume_pending` past 30 calls (stalls auto-continuation); parallel says plain `partial` by call 35. The release makes the known conflict worse.
- **R11 should-fix (low)** Delta states undefined: Finished parent / started dependents / verified phase; no baseline for a resume; Evidence Gate skipped and `evidence[]` overwritten; `user_review_pending` re-set on an already-reviewed `owner: both` task; "Awaiting Verification" vs inline contract's "In Progress first".
- **R12 nit** Scenario 52 traces B3, D (port 8888, killed variant, baseline), A step 7 don't match side A's text.
- **R13 nit** "parallel/heavy re-dispatch" undefined at the zero-token bullet.
- **R14 nit** `work.md` parallel key rule doesn't mention the queue.
- **R15 nit** `scripts/README.md:24` still "compiles every script".
- **R16 nit** Stale text: "fresh context" (`.claude/CLAUDE.md:44`, `workflow.md:187`, `implement-agent.md:116`); `files_affected`-only parallel condition (`rules/task-management.md:32`, `health-check.md:105`); `diagnose.md:153-155` screenshots; `rules/archiving.md:15` workspace for temp documents vs subagents.
- **R17 nit** `rules/agents.md` +150 words; brief-claims paragraph duplicates `work.md`; cutoff bound and `.claude/`-inline each stated in three places.
- **R18 nit** Evidence directory reused across attempts; cost backfill matched by attempt number only (repeats after a drift reset); no baseline → say "report only"; orphaned MCP Chrome profile lock not addressed.

Found sound: floor test (8 mutation and layout checks), handoff total check and `-HHMM` name, all cross-side citations resolve, delta ordering is crash-safe, schema `delta` key, FB-119 gaps 1, 2, 4, browser queue within one session.
Could not check: absolute `filename` on the installed Playwright MCP; SendMessage resume after long gaps or compaction; behaviour in a real downstream project.

## Fix pass (2026-10-07)

One fixer agent on a fresh mirror applied R1–R18 (R18(d), the orphaned MCP Chrome profile lock, left open). 22 files changed in the pass; copied back; the same reviewer is re-verifying.

Settled by the fixer, not decided by the user (S1–S13; under re-verification):

- **S1** Parent already Finished → no delta and no reopen; the change becomes a new task (the last subtask of a broken-down task never gets a delta).
- **S2** A task others have built on (dependent dispatched, or phase verified) → the change is a new task.
- **S3** "Phase verified" = `verification-result.json` newer than the task's `task_verification.timestamp`.
- **S4** Evidence-shaped is a fixed list: `.png .jpg .jpeg .gif .webp .log .har .trace`, `trace*.zip`, scripts named `tmp*`, `temp*`, `scratch*`, `debug*`, `probe*`.
- **S5** Listeners are compared by port, not port+PID.
- **S6** Batch-end moves go to `{scratch}/batch-residue-{HHMM}/`; mid-batch, an unreported listener is asked about only when no agent is running.
- **S7** Post-limit dispatch rule (defined in the `parallel-execution.md` pre-flight bullet): the user's go-ahead is needed for two or more agents at once, or adding one while another runs, and for re-dispatching the cut-off job at its original size; one agent at a time on anything else doesn't wait.
- **S8** A delta entry's `attempt` repeats the current value; a delta fail writes a `[DELTA FAIL]` note; a refusal or unusable reply writes no history entry.
- **S9** Refusal shape: `{"task_id", "delta_refused": true, "reason"}` in place of a report.
- **S10** A SendMessage resume takes no residue baseline; its residue look is report-only.
- **S11** Evidence directory `{scratch}/agent-{task_id}-{role}-{n}/`, n = `verification_attempts` + 1, letter suffix on collision; phase-level n counts that phase's runs in the session.
- **S12** An implementation that needs the build runs alone.
- **S13** The delta step runs the project's existing checks on the edit before resuming the verifier.

Left open by the fix pass: a returned agent's reported port is stopped even if a still-running sibling has since started a server on it; the residue baseline lives in conversation only (lost on compaction → report-only); `lsof` portability (`ss -ltnp` named as fallback, untested); FB-127 (c) wind-down mismatch (D11); the `<!-- FEEDBACK:{id} -->` marker read in `/work complete` step 4b.

## Re-verification (2026-10-07)

388 tests green on 3.13 and 3.10 after the fix pass. Same reviewer, against the fixed text: R1–R9, R11–R17 fixed (failure scenarios re-run); R10 closed per D11; R18 fixed except (d). S1–S13 all judged safe and executable (S1/S2 costly, see R24). All cross-file names resolve; scenario 52 matches the text except where noted. New findings (fixes pending):

- **R19 should-fix (unsafe)** `work-procedures.md` Residue check: mid-batch, a returned agent's reported port is stopped even when a still-running sibling has since started a server on it. Fix: while another agent of the batch is running, stop nothing; note the reported ports and stop any still listening at the first moment no agent is running, using the union of `servers_started[]`. Update `parallel-execution.md` and scenario 52 Trace E step 4.
- **R20 should-fix** "New and not reported → ask" covers every process on the machine (the baseline is system-wide; this machine has 10 listeners), so an app opened during a dispatch stops the loop. Fix: ask only when the listener's working directory is inside the project (`lsof -a -p {pid} -d cwd -Fn`); mention any other new listener in the report and continue. Same filter for the no-baseline listing.
- **R21 should-fix** `session-recovery.md § "Residue From a Previous Session"` fires on almost every session start (a clean pause leaves tasks In Progress) and would list styler's 70 PNGs each time. Fix: full-scan path only, with R20's filter.
- **R22 should-fix** `settings.json` (unchanged) has no allow rule for `lsof`, `mkdir`, `cp`, `diff`, `mv`, `kill`, `mktemp`; outside auto mode the new mandatory commands prompt. Needs the user's decision (no settings change was decided for this release).
- **R23 should-fix (low)** A fresh verification after a reopened pass can escalate on its first failure (passed on attempt 2 → fresh verify is attempt 3). Fix: reset `verification_attempts` to 0 when a Finished task is reopened, as drift reconciliation does.
- **R24 nit** S1/S2 close the delta window often (last subtask; auto-continuation dispatches the dependent straight after the pass). Fix: in `work.md`'s pass bullet, decide on the verifier's minor findings before looping back.
- **R25 nits** `parallel-execution.md:212` "at its original size" and the queue-hold wording; loop pseudo-code lists the residue check after the protocol steps (text says first); the queue's non-dispatch job kinds (orchestrator gate, resumed delta) read as verify-agent dispatches; `user_review_pending` "absent" → "absent or false"; "a script whose name starts with…" needs extensions; printed move destination should say it is under the temp directory.

Could not check (unchanged): absolute `filename` on the installed Playwright MCP; SendMessage resume after long gaps; `lsof … -d cwd` on Linux; behaviour in a real downstream project.

### Decisions after re-verification (user, 2026-10-07)

- **D13 (R20; narrows D8).** A new, unreported listener is asked about only when its working directory is inside the project; any other new listener is mentioned in the report and the run continues.
- **D14 (R22).** `settings.json` is not changed in this release; the ship-log notes that the new commands (`lsof`, `mkdir`, `cp`, `diff`, `mv`, `kill`, `mktemp`) prompt once outside auto mode.
- **D15 (R23).** `verification_attempts` is reset to 0 when a Finished task is reopened for a fresh verification.
- **D16 (R24).** The orchestrator decides on the verifier's minor findings before looping to the next task.
- **D17.** R19, R21 and R25 are applied in the same fixer pass, then re-verified by the same reviewer.

## Second fix pass (2026-10-07)

Same fixer, fresh mirror, R19–R25 applied (R22: no file change, D14). 7 files changed; copied back; final re-verification by the same reviewer in progress.

Settled by the fixer in this pass (T1–T7):

- **T1** A listener whose working directory can't be determined counts as outside the project (mentioned, not asked).
- **T2** "Inside the project": cwd equals the project root as `pwd -P` prints it, or starts with it plus `/`; read with `lsof -a -p {pid} -d cwd -Fn`; Linux fallback `readlink /proc/{pid}/cwd` (untested).
- **T3** The verifier's minor findings get four outcomes: delta, new task, ask the user, or drop with a `notes` line.
- **T4** The counter also resets after an interrupted delta re-check.
- **T5** A no-baseline listing of more than ten root files is a count plus one example.
- **T6** Two collection-loop branches in `parallel-execution.md` lost one step each (verify 5→4, failure 6→5).
- **T7** Queue entries are `{task_id, kind}` with `verify`, `delta`, `gate`.

Costs flagged: a server leaked by an exclusive verifier stays up until no agent is running (R19's deferral); after a cutoff with a clean-exit sentinel under 24 hours old, the previous-session residue look is skipped (R21's narrowing).

## Final re-verification (2026-10-07)

388 tests green on 3.13 and 3.10 after the second pass. Same reviewer: R19–R21, R23–R25 fixed (scenarios re-run); R22 closed by D14; T1–T7 sound; no seam broken; scenario 52 matches the text trace by trace. Nothing holds the release. New, not fixed (the shipped text is exactly what the reviewer last saw), carried to FB-127:

- **R26 should-fix (low)** → FB-127 (v): `last-clean-exit` is never deleted, so the previous-session residue look rarely runs.
- **R27 nit** → FB-127 (w): the counter reset is "before that dispatch", which a next-session recovery scan doesn't know to do.
- **R28 nit** → FB-127 (x): no loop step appends a `gate` entry; the failure branch omits a `delta` re-check.
- **R29 nit, pre-existing** → FB-127 (w): a guided-testing fail reopens a Finished task without a counter reset.

Reviewer on R19's cost (a leaked verifier server stays up until no agent is running): not a real problem, the next verifier finds a busy port; left as is, noted under FB-127 (y).
