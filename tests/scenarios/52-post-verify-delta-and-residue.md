# Scenario 52 — Post-verify delta, the residue check, one exclusive verification at a time, and the inline bound after a cutoff (FB-130, FB-132, FB-133, FB-119)

Conceptual trace test for v5.14.0, with the v5.14.1 residuals (FB-127 w, x, and the baseline on disk). Four rules of the `/work` loop:

- A small fix after a per-task pass can be re-checked by resuming the **same** verifier (a post-verify delta) when it is the verifier's own finding or a micro-edit the user approved, it stays inside the task's `files_affected`, and nothing has been built on the task yet. A delta re-check is recorded but never counted as a verification attempt, and a passed task that is reopened for a fresh verification starts its attempt count again. The orchestrator never passes a delta itself.
- After any agent returns or is killed, the orchestrator runs a residue check against a baseline taken before the dispatch: new files in the project root, new listening ports, untracked probe files. It moves and stops only what it can attribute, asks only about listeners that run from inside the project, and reports the rest.
- Tasks are implemented in parallel without the browser or the production build; verifications that need either take turns in one exclusive-verify queue.
- After a limit cutoff the inline size bound still applies: a larger task is not finished inline by the orchestrator.

## Setup / State

- A project at v5.14.0 or later with a small web report (Phase 3). Root `./CLAUDE.md § Verification Hooks` names the build command `npm run build`, which writes `dist/`. `npm run preview` serves on port 4173.
- The session scratchpad is `{scratch}`. Every dispatch brief names an evidence directory `{scratch}/agent-{task_id}-{role}-{n}/`, `{n}` being the verification attempt the dispatch belongs to (`commands/work.md § "Before Any Dispatch"`).
- The residue baseline is the output of three commands run before each dispatch: `git status --short`, `ls -A` on the project root, and `lsof -nP -iTCP -sTCP:LISTEN`. From v5.14.1 it is also written to `{scratch}/residue-baseline.txt`, under a first line naming the batch, or the one dispatch in sequential mode.
- "Post-verify delta" and "Residue check" are the blocks titled `**Post-verify delta (after a per-task pass):**` and `**Residue check (after any agent returns):**` in `work-procedures.md`. "After verify-agent returns (per-task mode)" is the protocol of that name in `work-procedures.md § "State Persistence Protocol"`. The inline contract is `rules/agents.md § "Dispatch Invariants vs Efficiency Defaults"`. The traces name blocks, not step numbers.
- `git status --short` is clean before each dispatch unless a trace says otherwise.
- Each trace starts from this state, not from the previous trace, except C, which continues A.

## Trace A — post-verify delta allowed: the same verifier is resumed

Command path: `work-procedures.md`: "After verify-agent returns (per-task mode)" → "Post-verify delta".

State: Task 21 "Add CSV export of the summary table" (`owner: claude`, no parent, `files_affected: ["src/export/csv.py", "tests/test_csv.py"]`). Earlier in this session verify-agent V1 (evidence directory `{scratch}/agent-21-verify-1/`) returned `pass` for it: status Finished, `verification_attempts: 1`, one `verification_history[]` entry (attempt 1, `pass`). V1's report carried one non-blocking issue: the header reads `Std Dev` where the spec's column list says `SD`. V1 is still resumable. Task 30 depends on Task 21 and is still Pending. No phase-level verification has run since the pass.

1. The orchestrator settles V1's minor finding before looping to the next task (`commands/work.md § "If Verifying (Per-Task)"`, Pass): the spec's column list says `SD`, so it is applied now, while Task 30 has not been dispatched. Nothing has been built on Task 21: its one dependent is Pending, `.claude/verification-result.json` has no timestamp later than the pass, and it has no parent. It may be reopened.
2. The orchestrator checks the four delta conditions: the task passed per-task verification in this session; the change is the verifier's own non-blocking finding; the fix touches only `src/export/csv.py` and `tests/test_csv.py`, both in `files_affected`; V1 can be resumed. All hold.
3. Task 21 → Awaiting Verification, with `verification_attempts` set from 1 to 0 in the same write (not In Progress: a crash from here on leaves a state the recovery scan re-verifies, and that fresh verifier starts at attempt 1).
4. The orchestrator copies `src/export/csv.py` and `tests/test_csv.py` into `{scratch}/agent-21-verify-1/delta-before/`, makes the edit (the header string, and the test's expected header) and runs the project's tests for it.
5. It prepends `[DELTA 2026-10-07] Header "Std Dev" → "SD" in csv.py and its test; verifier's finding from attempt 1.` to `notes`. The attempt-1 notes stay below it.
6. It resumes V1 with SendMessage, giving `diff -u` of each copy against the edited file (not `git diff`, which would be the whole uncommitted implementation) and asking for the standard per-task report.
7. V1 returns. The residue check runs first; a resume took no baseline, so it only reports, and it finds nothing.
8. V1's report is `pass`. Task 21 is not a web-UI task, so the Empirical Evidence Gate does not apply. "After verify-agent returns (per-task mode)" is applied with the delta differences: `task_verification` rewritten; `verification_attempts` goes from 0 back to 1, the attempt number of the pass the delta follows; a second `verification_history[]` entry with `"attempt": 1`, `"result": "pass"`, `"delta": true` and `cost` (the resumed turn's usage); Task 21 → Finished.

Variant, a micro-edit the user approved: after the pass the user says "rename the output file to `summary.csv`, that's all". The default filename is set in `src/export/csv.py`. Same path, and the `[DELTA]` note says the user asked for it.

Variant, the review was already done: Task 21 is `owner: both`, and the user ran `/work complete 21` before asking for the rename, so `user_review_pending` is absent. V1's delta report says `user_review_pending: true`, as it does for every `owner: both` task. The orchestrator does not write the flag again: the user has reviewed this task.

**Expected:** before v5.14.0 the choice was a full fresh verify dispatch for a one-word fix, or an edit nobody re-checked. Now the fix is re-checked by the agent that already holds the task's context and never implemented anything, and the record shows it as a delta entry that costs no attempt.

**Pass criteria:** status path is Finished → Awaiting Verification → Finished; the task is never Finished between the edit and V1's second report; the same verifier is resumed, not a new one dispatched; V1 is sent the before/after diff of the edit only; the new history entry has `"delta": true`, attempt 1 and a `cost`; `verification_attempts` is 0 while the delta is out and 1 again after its pass; `notes` begins with the `[DELTA 2026-10-07]` note and keeps the earlier text; in the review variant `user_review_pending` stays absent.

**Fail indicators:** the edit made with Task 21 left Finished; the orchestrator writing `result: "pass"` for the delta without V1's report; `verification_attempts` incremented to 2, or left at 0 after the delta pass; `git diff` of the whole implementation sent as "the delta"; a history entry without `delta`, or attempt 1's entry overwritten; `notes` replaced by the delta note; no `cost` on the entry; files moved or a server stopped by the residue check on a resume's return.

## Trace B — no delta: outside the conditions, refused, or already built on

Command path: `work-procedures.md`: "Post-verify delta" (conditions) → `commands/work.md § "If Verifying (Per-Task)"`.

State: Task 21 as at the start of Trace A.

1. **Outside `files_affected`.** V1's finding is instead that the summary table itself labels the column `Std Dev`, in `src/report/table.py`. That file is not in Task 21's `files_affected`, so the third condition fails. No delta: Task 21 → In Progress with `completion_date` cleared and `verification_attempts` set to 0 in the same write (reopening a passed task resets the counter in the write that reopens it), the change is implemented the normal way (inline if it is within the inline bound, with an `[INLINE]` note; otherwise by implement-agent), Task 21 → Awaiting Verification, and a **fresh** verify-agent is dispatched. This is attempt 1 again; `{scratch}/agent-21-verify-1/` already exists, so its evidence directory is `{scratch}/agent-21-verify-1b/`. Its history entry has `"attempt": 1`, a later `timestamp` than the first attempt-1 entry, and no `delta` key.
2. **Verifier can't be resumed.** The fix is the one from Trace A, but the session was restarted since the pass (or SendMessage reports that V1 no longer exists). The first and fourth conditions fail. Same path as case 1: reopened, counter reset, edited by the normal implement path, fresh verify-agent, attempt 1, no `delta` key.
3. **Not a finding and not approved.** The orchestrator itself notices a clumsy variable name in `src/export/csv.py` after the pass. It is neither the verifier's finding nor a micro-edit the user approved, so the second condition fails. If the orchestrator makes the change, it is by case 1's path with a fresh verify-agent; V1 is not resumed for it. If the user then approves it as a micro-edit before it is made, Trace A's variant applies instead.
4. **The verifier refuses.** All four conditions held, the orchestrator followed Trace A through step 6, but the edit grew: it also restructured the export function. V1 returns `{"task_id": "21", "delta_refused": true, "reason": "..."}` instead of a report. Nothing is written to `verification_history[]` for the refusal, Task 21 stays Awaiting Verification with the edit on disk, `verification_attempts` is 0 when the fresh verify-agent is dispatched, and it is dispatched at once. Its entry is attempt 1 with no `delta` key.
5. **The resumed verifier answers with prose.** As case 4, but V1 replies with a paragraph and no JSON. The orchestrator does not ask again and does not write `[VERIFICATION TIMEOUT]`: it dispatches a fresh verify-agent at once, with the counter at 0; no entry is written for the prose reply.
6. **A dependent has started.** As Trace A, but Task 30 (which depends on Task 21) is In Progress. Task 21 is not reopened: it stays Finished and the header fix becomes a new task with section provenance, depending on Task 21, implemented and verified by the normal path. The same happens when a phase-level verification has run since Task 21's pass, or when Task 21 is the last subtask of a parent that auto-completed on its pass.

**Expected:** the delta path is narrow. A change that widens the task, a verifier that is gone or unwilling, or a task others have built on gets the full independent check, and none of these outcomes is charged to the task's attempt count as a failure.

**Pass criteria:** in cases 1–3 a new verify-agent is dispatched and the task is not Finished until it reports `pass`; in cases 4 and 5 no history entry is written for the resumed turn, the task is never Blocked, and a fresh verify-agent runs; no entry in any case carries `delta`; in case 6 Task 21's status never changes and a new task file exists.

**Fail indicators:** V1 resumed for an edit to `src/report/table.py`; `src/report/table.py` edited under a `[DELTA]` note; a new verify-agent's attempt recorded with `"delta": true`; the orchestrator re-checking the diff itself because V1 was gone; a refusal recorded as `result: "fail"` or followed by an implement-agent sent to "fix" it; a second ask, or `[VERIFICATION TIMEOUT]` and Blocked, after V1's prose reply; Task 21 set to Awaiting Verification while Task 30 is running.

## Trace C — the delta fails: recorded, not counted, never escalated

Command path: `work-procedures.md`: "Post-verify delta", the `fail` outcome.

State: Trace A through step 6, with two changes: Task 21 had passed on its second attempt (`verification_attempts: 2` before the delta, set to 0 at Trace A's step 3; V1's directory is `{scratch}/agent-21-verify-2/`), and the orchestrator changed the header in `src/export/csv.py` but not the expected header in `tests/test_csv.py` (and skipped the test run).

1. V1 runs the task's tests on resume and returns `fail`: `test_csv.py::test_header` expects `Std Dev`.
2. The entry is appended to `verification_history[]` with `"attempt": 2`, `"result": "fail"`, `"delta": true` and `cost` (attempt 2 is the number of the pass it follows, not the counter); `task_verification` is written from the report; the delta increments nothing, so `verification_attempts` stays 0. No escalation: the task is not Blocked.
3. Task 21 → In Progress, `completion_date` cleared, `[DELTA FAIL] test_header still expects "Std Dev"` prepended to `notes`.
4. The orchestrator either restores the two files from `delta-before/` or fixes the test, by the normal implement path (here inline, with an `[INLINE]` note), then Task 21 → Awaiting Verification, and a fresh verify-agent is dispatched with `{scratch}/agent-21-verify-1b/`; `verification_attempts` is still the 0 written when the delta reopened the task. That verification is attempt 1, with no `delta` key: if it fails, the task goes back to In Progress for a normal retry, where a third counted attempt would have escalated it.

**Expected:** a failed delta is a real result: it is on the record and the task is not Finished until an independent pass. But a cosmetic follow-up edit cannot push a task that already passed into "requires human review".

**Pass criteria:** Task 21 is In Progress after step 3, not Finished and not Blocked; the failed entry is in the history with `"delta": true`; `verification_attempts` goes 2 → 0 when the delta reopens the task, is 0 when the fresh verifier is dispatched and 1 when it returns; the history then holds two attempt-1 entries and two attempt-2 entries, told apart by `timestamp`; the `[DELTA]` and `[DELTA FAIL]` notes are both in `notes`, newest first; status path is Finished → Awaiting Verification → In Progress → Awaiting Verification → Finished on the fresh pass.

**Fail indicators:** Task 21 set back to Finished "because attempt 2 passed"; `[VERIFICATION ESCALATED]` and Blocked because the delta, or the fresh verification after it, was "the third attempt"; a late `cost` written to the first attempt-1 entry instead of the new one; the delta entry left out of the history because it failed; V1 resumed a second time for the fixed edit; the orchestrator fixing the test and marking the task passed without a verifier's report.

## Trace D — residue check after a return

Command path: `work-procedures.md`: "After verify-agent returns (per-task mode)" → "Residue check".

State: Task 22 "Summary page shows the totals row" (web-UI task), sequential mode, no other agent running. The baseline before the verify dispatch: `git status --short` clean; the root listing; and, among the machine's listeners, the user's own notebook server on port 8888 (started before the session). The verify brief named the evidence directory `{scratch}/agent-22-verify-1/`. The verifier returns `pass` with `servers_started: [{"command": "npm run preview", "port": 4173, "stopped": true}]`. While it ran, the user saved `meeting-notes.md` in the project root.

1. The three baseline commands are re-run. New root entries: `summary-page.png`, `dist/`, `meeting-notes.md`. New untracked path outside the root: `web/pages/_probe.html`. Listening ports now that the baseline lacks: 4173, 4174 and 57621. Port 8888 is still listening.
2. `summary-page.png` is a regular file, an image, not in `files_modified` or `files_affected`; the agent returned a report and no other agent is running. It is moved, and the move is printed with the warning that the destination is a scratch directory the OS may clear: `summary-page.png → {scratch}/agent-22-verify-1/summary-page.png (scratch directory; the OS may clear it, so copy out anything you want to keep)`.
3. `dist/` is a directory: reported with its path and left. `meeting-notes.md` is not evidence-shaped: reported with its path and left.
4. `web/pages/_probe.html` is an untracked probe file outside the root: reported, not deleted or moved.
5. Port 4173 is new and in `servers_started`: the orchestrator kills the PID `lsof` shows on it and confirms the port is free. The report said it was already stopped; the check trusted the port, not the report.
6. Port 4174 is new and not reported (the preview server had started a second time and moved up a port). `lsof -a -p {pid} -d cwd -Fn` ends with `n` and the project root, so it runs from inside the project: the orchestrator names its port, PID and command and asks the user before stopping it.
7. Port 57621 is new and not reported, and its process's working directory is `/` (a music app the user opened during the dispatch): outside the project. It is named in the report line and nobody is asked.
8. Port 8888 was listening at baseline: not touched.
9. The user is told in one line: one server stopped (4173), one listener waiting for their answer (4174), one new listener outside the project noted (57621), one screenshot moved (with both paths), `dist/`, `meeting-notes.md` and `_probe.html` left in place.

Variant, the agent was killed: the verifier ends with a zero-token return instead of a report. The check runs, and only reports and asks: `summary-page.png` stays in the root and is listed, the listeners on 4173 and 4174, both running from inside the project, are named to the user, who is asked before either is stopped, and 57621 is only mentioned. The interruption rules for the verification itself are unchanged (no attempt counted, task stays Awaiting Verification).

Variant, the baseline is out of context: the conversation was compacted while the verifier ran and the baseline output is gone from it. The check reads `{scratch}/residue-baseline.txt`, finds that its first line names this dispatch (Task 22, verify), and proceeds as in steps 1–9. Had the line named another dispatch, the check would only report.

Variant, no baseline: the copy on disk is gone too (the scratch directory was cleared). The check tells the user which evidence-shaped files are in the root and which listeners run from inside the project (4173 and 4174, not 8888 or 57621), and moves and stops nothing.

Variant, an earlier kill: the user stopped the dev server by hand earlier in the session. The check stops and moves things; it starts nothing. Starting that server again is still governed by "Respect prior kills" (`rules/agents.md § "Behavioral Rules"`).

**Expected:** before v5.14.0 nothing looked. Screenshots collected in the project root and a server reported as stopped kept its port.

**Pass criteria:** the check runs after the return without the user asking; the comparison is against all three baseline outputs; the 4173 listener is stopped, the 4174 listener is asked about, the 57621 listener is mentioned without a question, the 8888 listener is untouched; the screenshot ends up in `{scratch}/agent-22-verify-1/` and its new path is printed; `dist/`, `meeting-notes.md` and `_probe.html` still exist where they were and are named to the user; in the killed and no-baseline variants nothing is moved and nothing is stopped without the user's answer; after a compaction the check works from `{scratch}/residue-baseline.txt` when its first line names this dispatch or its batch, and is not report-only.

**Fail indicators:** `dist/` or `meeting-notes.md` moved into the evidence directory; `_probe.html` deleted; the screenshot deleted instead of moved, or moved without saying where; the 8888 server stopped; the 4174 listener stopped without asking, or never noticed because only reported ports were probed; the run halted to ask about 57621; the agent's "server stopped" taken as fact with no port check; files moved after a zero-token return; the check falling back to report-only after a compaction while `{scratch}/residue-baseline.txt` exists; nothing said to the user because the verification passed.

## Trace E — a batch of UI tasks: implemented in parallel, verified one at a time

Command path: `commands/work.md § "Step 2c"` → `parallel-execution.md § "Single-Instance Resources"` → `§ "Parallel Dispatch"` steps 3 and 4.

State: Task 23 "Totals row on the summary page" (`files_affected: ["web/pages/summary.html", "web/js/summary.js"]`), Task 24 "Legend on the trend chart" (`files_affected: ["web/pages/trend.html", "web/js/trend.js"]`) and Task 25 "Print stylesheet is included in the production bundle" (`files_affected: ["web/css/print.css"]`), all Pending, `owner: claude`, difficulty 3, no dependencies. Tasks 23 and 24 each have a criterion about what their page renders; Task 25 has a criterion "the production build succeeds and `dist/` contains `print.css`". None of them changes the build configuration.

1. Step 2c: no path conflicts. All three verifications are exclusive (23 and 24 need the browser, 25 runs the build), which keeps no task out of the batch: none needs the build to be *implemented*. `parallel_mode = true`.
2. A 3-batch gets the confirmation prompt, which names Tasks 23, 24 and 25 as verified one at a time. The pre-flight takes the batch's one residue baseline.
3. Three implement-agents are dispatched together. Each brief names its own evidence directory (`{scratch}/agent-23-implement-1/` and so on), lists the other tasks' files as sibling files, and carries both lines: don't use the browser MCP, and don't run `npm run build` (type-check and tests only).
4. Task 23's implement-agent returns `completed` first, reporting a test server on port 3000 that it stopped. Port 3000 is listening: Task 24's implement-agent, still running, has since started its own server there. The residue check stops nothing, moves nothing and asks nothing while another agent of the batch is running; it keeps Task 23's `servers_started`. After-return protocol; Task 23 → Awaiting Verification. No exclusive job is running: its verify-agent is dispatched with `{scratch}/agent-23-verify-1/`.
5. Task 25's implement-agent returns `completed` while Task 23's verifier is running. Task 25 → Awaiting Verification and joins `exclusive_verify_queue`. Task 24's implement-agent returns next; Task 24 joins the queue behind it.
6. Task 23's verifier returns `pass` with `runtime_validation: "partial"`. The residue check runs first. No agent of the batch is running at this moment (Tasks 25 and 24 are queued, not dispatched), so it goes through the ports kept so far: 3000 is free now, and 4173, which the verifier reported, is confirmed stopped. The Empirical Evidence Gate applies and runs in the same turn, before anything else is dispatched; then the pass is persisted. Then the head of the queue: Task 25's verify-agent, which will run `npm run build`.
7. Task 25's verifier returns; Task 24's verify-agent is dispatched. When it returns, the queue is empty and no agent is running: post-parallel cleanup, with the batch-level residue check, which may now move evidence-shaped files (to `{scratch}/batch-residue-{HHMM}/`) and ask about unreported listeners.

Variant, compaction during the batch: the conversation is compacted while Task 25's verifier runs. When it returns, the check reads `{scratch}/residue-baseline.txt`; its first line names the batch (Tasks 23, 24, 25), which this verifier belongs to, so the file is used. The same holds for Task 24's verifier, dispatched from the queue later, and for Task 28 in the re-dispatch variant below, whose id was added to that line when it was dispatched.

Variant, a task whose verification is not exclusive: Task 27 "Document the export format" is in the batch. Its verify-agent is dispatched the moment its implement-agent returns, whatever the queue holds.

Variant, a gate for a task whose verification was not exclusive: Task 31 "Correct the unit labels" (`files_affected: ["web/js/labels.js"]`) is in the batch. Its criteria are checked by unit tests, so its verification was not judged exclusive and its verify-agent is dispatched at once. It returns `pass` with `runtime_validation: "partial"`; `labels.js` is part of a web-UI component, so the Empirical Evidence Gate applies. Task 25's verifier is running the build at that moment: the queue is busy. The orchestrator appends `{task_id: "31", kind: "gate"}` to `exclusive_verify_queue`, writes the report's friction markers now (and not again later), keeps the report, and leaves Task 31 Awaiting Verification. When Task 25's verifier returns and its after-return steps are done, the entry is at the head: the gate runs, Task 31's pass is persisted with the gate's `evidence[]`, and the next head (Task 24's verify-agent) is run. Had no exclusive job been running when Task 31's verifier returned, the gate would have run at once, with no entry.

Variant, incremental re-dispatch: Task 28, another UI task, was held back on a file conflict with Task 23 and starts when Task 23's implement-agent returns. Its brief carries the same no-browser and no-build lines, although it was not part of the batch when the batch was built.

Variant, the first verification is cut off: Task 23's verifier ends with a zero-token return. Task 23 stays Awaiting Verification with no attempt counted; the residue check reports and asks; the post-limit dispatch rule holds the rest of the batch and its queue for the user's go-ahead, so Tasks 25 and 24 stay queued and Awaiting Verification until they answer.

Variant, a task that must run the build to be implemented: Task 29 "Switch the bundler to content-hashed filenames" edits the build configuration; its implement-agent can't check its work without `npm run build`. Step 2c holds it back with `conflict_files: ["build output dist/"]`. It is dispatched alone once no other agent is running and the queue is empty, with no no-build line in its brief, and nothing else is dispatched until its implement-agent returns.

**Expected:** before v5.14.0 both browser verifiers were dispatched as their implement-agents returned and drove the same tab; a snapshot could show the other task's page with no error. A rule that kept building tasks out of a batch would have serialised most UI work; instead only verification takes turns.

**Pass criteria:** all three implement-agents run at the same time; Task 24's server on port 3000 is still running after step 4; at no moment are two exclusive jobs active (two browser verifiers, a browser verifier and a building verifier, or a verifier and the orchestrator's gate); queued tasks are Awaiting Verification, not Blocked or Pending, while they wait; each queued verifier is dispatched only after the previous one's residue check and after-return steps; in the gate variant Task 31 is not Finished until its gate has run, and the gate does not run while Task 25's verifier is building; the evidence directories are all distinct; the non-exclusive task's verification is not queued; Task 28's brief has both lines; no task has a new field recording that it needs the browser or the build.

**Fail indicators:** the listener on port 3000 killed at step 4 because Task 23 reported that port; Task 24 or 25 held out of the batch because its verification needs the browser or the build; two exclusive verifiers dispatched at once; Task 25's verifier building while the orchestrator's gate builds; Task 31's pass persisted with the gate skipped, or its gate never run because no step put it in the queue; an implement-agent taking screenshots through the MCP or running `npm run build` during the batch; Task 25's verifier dispatched before Task 23's after-return steps are done; a `needs_browser` field written to the task files; two verifiers sharing one evidence directory; Task 29 implemented alongside other tasks.

## Trace F — a larger task after a zero-token return is not implemented inline

Command path: `work-procedures.md`: "After implement-agent returns", "Zero-token return — platform limit cutoff" → `rules/agents.md § "Dispatch Invariants vs Efficiency Defaults"` → "Residue check".

State: Task 26 "Rebuild the trend chart on the aggregated series" (difficulty 5, six files in `files_affected`), In Progress. Its implement-agent returns `subagent_tokens: 0` and no report: a usage limit cut it off.

1. The residue check runs for the killed agent: it reports, moves nothing, and asks before stopping any new listener.
2. The orchestrator assesses the on-disk state itself: three of the six files are changed, and the test suite fails in `tests/test_trend.py`. The work is not complete.
3. The remaining work is three files of a difficulty-5 task: above the inline size bound. The cutoff does not lift the bound, so the orchestrator does not write the rest itself.
4. Finishing it means dispatching the cut-off job again, which the post-limit dispatch rule holds for the user's go-ahead. Task 26 keeps its status (not Awaiting Verification, not Finished) with a note of what is on disk, and an `augment_rows[]` entry puts it on the Needs-you card with the question inline: Task 26 was cut off by a usage limit with three of six files changed and `tests/test_trend.py` failing; re-dispatch now, or later? The dashboard is regenerated.
5. The user is told about the limit hit and the row.

Variant, a small task: Task 27 (difficulty 2, one file) is cut off the same way with the edit half made. That is within the inline bound: the orchestrator finishes it inline under the inline contract (`[INLINE]` note, existing checks run, the search for what the change invalidates), sets Awaiting Verification, and dispatches a verify-agent: one agent, for work that is complete on disk, which the post-limit rule does not hold. It does not verify it itself.

**Expected:** a cutoff used to read as licence to finish whatever was left inline, which put a difficulty-5 implementation in the orchestrator's context with no implement-agent contract behind it.

**Pass criteria:** no implementation edits by the orchestrator to Task 26's files after the cutoff; a Needs-you row exists for Task 26 with the concrete question; nothing is dispatched for it before the user answers; the residue check ran; the small task in the variant still reaches Finished only through a verify-agent.

**Fail indicators:** the orchestrator writing the three remaining files "because the agent can't be re-dispatched"; Task 26 set to Awaiting Verification on half-done work; the limit hit mentioned only in conversation or the handoff, with no Needs-you row; the cut-off implementation re-dispatched, or a parallel batch started, without the user's go-ahead.

## Invariant checks

- A task reaches Finished only through a verify-agent's `pass`, delta or not. The orchestrator never marks a delta as passed.
- A delta re-check is recorded with `"delta": true` and its cost, never increments `verification_attempts`, and never escalates a task. A refusal or an unusable reply writes no entry and leads to a fresh verify-agent.
- A passed task sent to a fresh verify-agent starts again at `verification_attempts: 0`, set in the write that reopens it, whichever path reopens it (a change after the pass, a failed or lost delta re-check, a guided-testing fail, drift). A delta re-check that passes puts the counter back to the attempt number of the pass it follows.
- A delta never touches a file outside the task's `files_affected`, is never run by a verifier other than the one that passed the task in this session, and never reopens a task that a dependent, a phase-level verification or a Finished parent has built on.
- The residue check never deletes a file, never moves a directory or a file that is not evidence-shaped, never moves anything after a termination or without a baseline for that dispatch or its batch (in context or in `{scratch}/residue-baseline.txt`), and always says where a moved file went.
- The residue check never touches a port that was listening at baseline, stops a new listener without asking only when an agent reported that port and no other agent of the batch is running, asks only about listeners whose working directory is inside the project, and with no baseline stops nothing.
- At most one exclusive job (a verification or delta re-check using the browser or the build, the orchestrator's own gate) runs at a time; a gate that finds the queue busy waits in it as a `gate` entry. Needing the browser or the build for verification never keeps a task out of a batch; only needing the build for implementation does.
- Whether a task needs the browser or the build is judged from its criteria and the project's build command. No task field records it.
- Every dispatch has its own evidence directory, never the project root and never one shared with another dispatch or another attempt.
- The inline size bound is the same after a cutoff as before it.
