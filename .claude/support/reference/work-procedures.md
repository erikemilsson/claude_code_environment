# /work Procedures

Deferred procedures extracted verbatim from `commands/work.md` in v4.18.0 (Plan 2 P3 — the orchestrator file had grown past reliable single-pass size; ~20 ship-log patches trace to prose procedures skipped under load). `work.md` keeps STOP-gated stubs under the same section names; this file is the canonical body. Read the section the stub names AT the moment the stub fires — once read, it stays in context for the session.

## State Persistence Protocol

After any agent (implement-agent or verify-agent) returns a structured report, the orchestrator is responsible for all state transitions, JSON persistence, and dashboard updates. Agents cannot write to `.claude/` paths — this is enforced by the Claude Code harness (see DEC-004). Follow this protocol precisely to preserve the atomic implement→verify contract.

**Schemas:** The two agent return schemas are defined in `.claude/agents/implement-agent.md` § "Step 6: Return Structured Report" and `.claude/agents/verify-agent.md` § "Step T6: Construct Verification Report" (per-task) + § "Step 7: Include Verification Result in Report" (phase-level).

**Task `notes` are history, newest first.** Every `notes` write, here and everywhere else, prepends: `notes` becomes `new_text + " " + notes` (just `new_text` when `notes` is empty). Never replace them: a re-implementation must keep the `[VERIFICATION FAIL #N]` trail the verifier reads.

**`user_feedback` is history too, newest first, dated.** Every `user_feedback` write prepends: `user_feedback` becomes `"[YYYY-MM-DD] " + new_text + "\n" + user_feedback` (just the dated entry when the field is empty or absent). Never overwrite it: a second round of guided testing or a later `/work complete` must not erase what the user said before.

**Friction entries a task fixes.** When a task with `resolves_friction` becomes Finished with no user review pending — a per-task pass without `user_review_pending` ("After verify-agent returns (per-task mode)" step 4), `/work complete` (which also completes a pending review), or parent auto-completion (step 7 there; `/work complete` step 6) once no subtask has `user_review_pending` (`/work complete` on that subtask re-runs the parent check) — set each listed entry that is `open` in `.claude/support/friction.jsonl` to `status: "resolved"`, `resolved_by: {"kind": "task", "ref": "<task id>", "at": "<ISO timestamp>"}`, via `friction-register.md § "Status update protocol"`. Skip ids not in the register and entries already `resolved` or `dismissed`.

**Persist decisions (when a task becomes Finished).** Every path that sets a task Finished — a per-task pass ("After verify-agent returns (per-task mode)" step 4), `/work complete` step 5, parent auto-completion — checks the task's `decisions_pending`. If it is non-empty, write **one** record for the task, `.claude/support/decisions/decision-NNN-{slug}.md`, with the next free project id (`.claude/support/reference/decisions.md` § "Numbering namespace"; ids are assigned here, one report at a time, so parallel tasks can't collide):
- Frontmatter per the template in `decisions.md`, with `status: recorded`, `decided: <date of the verify pass>`, `decided_by: implement-agent` (`orchestrator` when the entries carry it) and `related.tasks: [<task id>]`. Title: the entry's title, or one title covering the set.
- Body: `## Background`, `## Options Comparison` (the options each entry considered), `## Decision` (per choice, a `**Selected:**` line and its rationale), `## Trade-offs`, `## Impact`. Use the template's `## Decision` heading, not `## Selected`. **No `## Select an Option` section**: the user ratifies with `/work ratify`, not a checkbox.

**If an agent record for this task already exists** (its `related.tasks` names the task and its `decided_by` is `implement-agent` or `orchestrator` — the task was reworked after Finished, or a crash followed the write): when the held set repeats that record's choices, write nothing. Otherwise write the new record with `related.decisions: [<old id>]` and, if the old one is still `recorded`, set the old one's `status: superseded` (frontmatter only). An old record in any other status (e.g. ratified, `approved`) is left as it is and only linked: the new `recorded` record reaching the user is the signal.

Then remove `decisions_pending` from the task. Don't regenerate the dashboard here: the regen that follows in the calling sequence shows the record ("After verify-agent returns (per-task mode)" step 9, or the batch-end regen in parallel mode; `/work complete` step 7). Regenerate (Tier 1) only when called from a path with no regen after it: the `/work` Step 0g recovery of an interrupted write. The Needs-you card's ratification row is script-derived from the `recorded` status. Never add the new id to any task's `decision_dependencies`. Never write `status: approved` for a choice the user didn't make.

**Residue check (after any agent returns):** run it first on every implement-agent or verify-agent return, and after an infrastructure termination (zero-token return, usage-limit kill, API or harness error, user stop), before any further dispatch. It compares the current state with the baseline taken before the dispatch (work.md § "Before Any Dispatch") and uses the report's `files_modified` and `servers_started[]` when there is a report.

1. **Compare.** Re-run the three baseline commands (`git status --short`, `ls -A` on the project root, `lsof -nP -iTCP -sTCP:LISTEN`). "New" below means absent from the baseline: a root entry, a `git status` line, or a listening port (compare ports; a PID is what you report and stop).
2. **Files.** Move a new root entry into that dispatch's evidence directory only when all of these hold, and print each move as `{old path} → {new path} (scratch directory; the OS may clear it, so copy out anything you want to keep)`:
   - it is a regular file (never a directory or a symlink);
   - it is evidence-shaped: an image (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`), a log (`.log`), a trace (`.har`, `.trace`, `trace*.zip`), or a script (`.sh`, `.py`, `.js`, `.mjs`, `.cjs`, `.ts`, `.rb`) whose name starts with `tmp`, `temp`, `scratch`, `debug` or `probe`;
   - it is not in the report's `files_modified` or the task's `files_affected`;
   - the agent returned a report, and no other agent is running.

   Every other new root entry is reported with its path and left where it is: a directory (`node_modules/`, `dist/`, `.next/`, `coverage/`), a lockfile, a document, anything you can't classify. It may be a build product, a file the agent legitimately created, or something the user or another session saved meanwhile. A new untracked file outside the root that is not in `files_modified` (a probe route, a test page) is likewise reported, not deleted or moved. After a verify-agent dispatch, any new change to a tracked file is reported too: a verifier edits nothing.
3. **Servers.** For each listening port now:
   - **listening at baseline** → never touched, whatever PID holds it now and whatever the agent reported. If the agent reported starting a server on it, tell the user.
   - **new, and in the report's `servers_started[]`** → stop it, whatever its `stopped` value says (an agent has reported a server stopped while two were still listening): `kill` the PID `lsof` shows on that port, then confirm the port is free.
   - **new, and not reported** → it is the project's only if its working directory is inside the project. `lsof -a -p {pid} -d cwd -Fn` prints three lines, the last one `n` followed by that directory (with `ss`, `readlink /proc/{pid}/cwd`); "inside" means the path equals the project root as `pwd -P` prints it, or starts with that root plus `/`. Inside (the second listener on port+1, a watcher's server) → name its port, PID and command to the user and ask before stopping it. Outside, or no directory printed (another user's process, or no tool to ask) → not the project's: name it in step 4's line and carry on without asking. The baseline covers the whole machine, so an app the user opened during the dispatch shows up here.
4. **Tell the user** in one line what was found and what you did (moved where, stopped, left for them); say nothing when the check is clean.

**When the check only reports.** After a termination there is no report: nothing is moved, and every new listener goes through step 3's last case (inside the project → ask first; outside → mentioned). With no baseline (work.md § "Before Any Dispatch" lists the cases) nothing is moved or stopped: tell the user which evidence-shaped files are in the root (a count and one example when there are more than ten) and which listeners have their working directory inside the project, and leave both to them. Listeners outside the project are not listed.

**In a parallel batch** one baseline serves the batch. While another agent of the batch is running, the check at a return stops nothing, moves nothing and asks nothing: a port the returned agent reported may by now be held by a running sibling's server, and a new file or listener may be a sibling's. Keep the returned agent's `servers_started[]`. At the first moment no agent of the batch is running (between two queued verifications, or batch end at the latest), run step 3 against the union of the `servers_started[]` kept so far: stop what is still listening on those ports, and put unreported new listeners through its last case. At batch end (`parallel-execution.md § "Parallel Dispatch"` step 5), run the whole check once for the batch: step 2 uses the union of the batch's `files_modified` and `files_affected`, with moves going to `{scratch}/batch-residue-{HHMM}/`. If any agent of the batch ended without a report, nothing is moved at the end either.

Stopping an agent's leftover server is cleanup, not a restart; `rules/agents.md § "Behavioral Rules"` ("Respect prior kills") still governs starting anything again.

**After implement-agent returns:**

Run the Residue check above first, whatever the return (a zero-token return included).

1. **Status transition** based on `implementation_status`:
   - `completed`: write `{ "status": "Awaiting Verification", "completion_date": report.completion_date, "updated_date": today }` to task JSON and prepend `report.notes` to `notes`
   - `partial`: leave status "In Progress"; prepend `"[PARTIAL] " + report.notes` to `notes`
   - `partial_resume_pending` (per DEC-010): leave status "In Progress"; write `{ "partial_completion": report.partial_completion, "updated_date": today }` to task JSON and prepend `"[PARTIAL_RESUME_PENDING] " + report.notes` to `notes`. Surface inline: `Task {id} returned partial — resume scheduled. Confidence: {confidence}. Run /work again to re-dispatch.` Do NOT dispatch verify-agent — verification is gated on `completed`.
   - `blocked`: write `{ "status": "Blocked", "updated_date": today }` to task JSON and prepend `"[BLOCKED] " + report.notes` to `notes`; surface `issues_discovered[]` to user
   - `misaligned`: do not advance status; route to spec-alignment flow with `issues_discovered[]` context
   - **Zero-token return — platform limit cutoff (FB-103):** if the agent returns `subagent_tokens: 0` with no structured report at all, a platform usage/session limit killed it mid-tool-call. This is NOT a normal failure and NO envelope exists — DEC-010's `partial_completion` covers only *self-detected* turn-budget limits; a platform cutoff gives zero warning. Recovery (proven twice downstream): (1) assess on-disk state directly — run the project's typecheck + test suite from the orchestrator (cheap, no agent risk); (2) if genuinely green, dispatch a FRESH implement-agent whose only job is to confirm spec alignment of the on-disk work and return the structured report (verify-agent dispatch needs one) — instruct explicitly "do not rebuild; the mechanical work is on disk"; (3) if not green, treat the partial files as an interrupted implementation. A remainder inside the inline size bound is finished inline (`rules/agents.md § "Dispatch Invariants vs Efficiency Defaults"` states the bound and what a cutoff does to it). A larger remainder needs the cut-off job dispatched again with the on-disk state described, and the post-limit dispatch rule holds that for the user's go-ahead: leave the task In Progress with a note of what is on disk, and put it on the Needs-you card (an `augment_rows[]` entry naming the task and the choice: re-dispatch now, or wait). Surface the limit-hit to the user. The post-limit dispatch rule is defined in `parallel-execution.md § "Pre-Dispatch Confirmation"` (pre-flight checks): it says which dispatches wait for the user after a limit hit and which don't (step (2)'s confirm-only agent doesn't).

2. **Append friction markers (DEC-011 Option ABp + audit register).** For each marker in `report.friction_markers`, add `task_id: report.task_id` and **dual-write the marker as a JSON line to BOTH** `.claude/support/workspace/.pending-markers.jsonl` (transient buffer; survives abrupt termination) **AND** `.claude/support/workspace/.session-log.jsonl` (canonical log; consumed by PreCompact + Track 1 export). Append immediately within this step — **do NOT defer to `/work pause` or batch across multiple agent returns**. Markers between an agent return and the next sync point are at risk of permanent loss if the session terminates abruptly; the dual-write narrows that loss window to sub-second.

   - Pending-buffer write is append-only: open in append mode, write `{...}\n`, close. No read-modify-write cycle.
   - Session-log write also appends. If file doesn't exist, create it.
   - The next `/work` invocation (or PreCompact hook) will reconcile the two files via the catchup procedure in `work-recovery.md § "Friction-Marker Catchup"` (triggered by work.md Step 0d).
   - If `report.friction_markers` is empty, this step is a no-op — skip all writes.

   **Friction register projection (audit-eligible kinds):** For each marker whose `type` is one of `vocab_drift`, `path_drift`, `design_contradiction`, `terminology_mismatch`, or `spec_implementation_gap`, ALSO append to `.claude/support/friction.jsonl` (the audit register — see `.claude/support/reference/friction-register.md`). The register entry has additional structure beyond the session-log raw marker:
   - `id`: assigned at append time. Read existing `friction.jsonl` (create if missing), find max existing `FR-NNN`, increment by 1 (zero-padded to 3 digits, starting at FR-001).
   - `captured`: ISO timestamp from the marker.
   - `captured_in`: `{"agent": "{agent_type}", "task": "{task_id}", "command": "/work"}`.
   - `kind`: copy from marker `type`.
   - `what`: copy from marker `details`.
   - `source_anchor`: copy from marker `source_anchor` (REQUIRED — if missing on an audit-eligible kind, log a warning and skip the register write; session-log write still happens).
   - `status`: `"open"`.

   Register write is append-only at insert time. Status updates (later, by `audit-coherence` or user dismissal) use a read-modify-write of the entire file keyed by `id` — see friction-register.md § "Status update protocol".

   **Script helper (advisory, FB-098).** The orchestrator MAY compute this entire step's payload with `python3 .claude/scripts/persist-friction.py` (markers as a JSON array on stdin). It reads the existing `friction.jsonl` — and any `--scan` paths (e.g. `.claude/tasks/`, the handoff, the dashboard) — and returns the dual-write `markers`, the `register` projection with **collision-safe `FR-NNN` ids** (one past the max of register ids AND textual `FR-<n>` references, which a naive max+1 misses — the flirty-gym FR-001 / styler FR-031 collisions), the `assigned_ids` to echo into task notes, and any `warnings` (e.g. an audit-eligible marker missing `source_anchor`). It is read-only — the orchestrator still performs the appends described above. The prose here remains the source of truth; if the script is absent or fails, follow it by hand, and keep the two in lockstep (`.claude/scripts/README.md § "Dual-location risk"`).

3. **Hold decisions** (any return that carries a report; write **no** decision file here — the work isn't verified yet):
   - For each entry in `report.decisions_to_record[]` that meets `.claude/support/reference/decisions.md` § "Skip Records For", prepend `[CHOICE] {title}: {selected_option} — {rationale}` to the task's `notes` (skip a line already there) and drop the entry.
   - Set the task's `decisions_pending` to the remaining entries, **replacing** any earlier value (the agent restates its full set on every return); if none remain, remove the field.

   Subagents cannot write under `.claude/`, so holding and later persisting are the orchestrator's responsibility — implement-agent only generates content (DEC-004; `rules/agents.md § State Ownership`). Inline implementation by the orchestrator (`rules/agents.md § "Dispatch Invariants vs Efficiency Defaults"`) holds its own significant choices the same way, in the same entry shape plus `"decided_by": "orchestrator"` on each entry.

4. **Dashboard regeneration:** in sequential mode, regenerate `dashboard.html` per `.claude/support/reference/dashboard-regeneration.md`. In parallel mode, defer — handled at batch-end. Held decisions aren't on the dashboard yet; they appear when "Persist decisions" writes the record.

5. **For `completed` status:** dispatch verify-agent (see work.md § "If Verifying (Per-Task)") and then apply the "After verify-agent returns" protocol below.

**Follow-up tasks from `issues_discovered`.** A task you create from an entry with `suggested_action: "create new task"` follows the creation contract (`task-schema.md § "Drift Prevention Fields"`). Run `fingerprint.py --provenance` on the entry's `spec_section` when it names one, otherwise on the originating task's `spec_section` if the follow-up belongs to the same section; set `spec_unmapped: true` when it belongs to no single section. A follow-up that goes beyond the spec is created with `out_of_spec: true` instead.

**After verify-agent returns (per-task mode):**

Run the Residue check above first (after an infrastructure termination too, step 5).

1. **Read task's current `verification_attempts`** (default 0), compute `new_attempts = current + 1`
2. **Build `verification_history` entry** from report's `checks`, `issues`, `notes`, with `{"attempt": new_attempts, "result": report.result, "timestamp": report.timestamp}`. Add `"cost": {"total_tokens": N, "tool_uses": N, "duration_ms": N}` copied from the usage the harness reports for this verify-agent dispatch (the token count may arrive as `subagent_tokens` or `total_tokens` — store it as `total_tokens`); omit `cost` (or any sub-key) the harness didn't report — never estimate it. Append to task's `verification_history[]` array (create array if absent). **Backfill:** the usage can arrive after the report, in the agent's task-completion notification. Write the entry without `cost` rather than waiting, then add `cost` to that same entry when the notification arrives, matching it by `attempt` and `timestamp` together (attempt numbers repeat on delta entries and after every counter reset); this is the one edit an existing entry takes. An attempt made through "Post-verify delta" below also carries `"delta": true`; no other entry has the key.
3. **Write `task_verification`** field to task JSON using report's `result`, `timestamp`, `checks`, `notes`, `issues` — plus `evidence[]` when the Empirical Evidence Gate ran (see `work-web-evidence.md § "Empirical Evidence Gate"`). Remove `drift_reverify` if the task carries it, on pass or fail: the re-verification after a spec edit is done, and a fix after a fail is verified against its real diff.
4. **Status transition** based on `result`:
   - `pass`: set `status: "Finished"`, `updated_date: today`. If `report.user_review_pending == true`, also write `user_review_pending: true`, `test_protocol: report.test_protocol`, `interaction_hint: report.interaction_hint` (its friction entries then wait for `/work complete`); otherwise close the task's friction entries ("Friction entries a task fixes" above). Either way, run "Persist decisions" above — a pending user review doesn't delay it.
   - `fail` AND `new_attempts < 3`: set `status: "In Progress"`, `updated_date: today`. Clear `completion_date`. Prepend `[VERIFICATION FAIL #{new_attempts}]` to notes with the fail summary. `decisions_pending` stays on any fail; the next implement report replaces it
   - `fail` AND `new_attempts >= 3`: set `status: "Blocked"`, `updated_date: today`. Prepend `[VERIFICATION ESCALATED]` note — "3 attempts exhausted — requires human review"
5. **Timeout detection** (for a dispatched verifier; a delta re-check has its own rule, "Post-verify delta" step 5): if verify-agent returned without a valid report (prose instead of the report schema, malformed JSON, or nothing usable), ask it once for the report — resume it with SendMessage, or re-dispatch — without incrementing `verification_attempts`. Any re-dispatch in this step, like every per-task verify dispatch, adds the `drift_reverify` line when the task carries that field (work.md § "If Verifying (Per-Task)"). Only a second invalid return is a timeout — treat as fail: increment `verification_attempts`, set status to "Blocked", add `[VERIFICATION TIMEOUT]` note (no result is written, so `drift_reverify` stays for the retry in `session-recovery.md`). **Infrastructure terminations are interruptions, not timeouts (FB-120):** after a zero-token return, a usage-limit/HTTP 429 kill, an API or harness error, or a stop the user asked for, do NOT increment `verification_attempts` or write `task_verification` (same rule as an interrupted verifier at `/work pause`); leave status "Awaiting Verification". Per "After implement-agent returns" step 1, "Zero-token return — platform limit cutoff (FB-103)", report the interruption to the user and apply its post-limit dispatch rule before re-dispatching a fresh verify-agent.
6. **Append friction markers** from `report.friction_markers` (same as implement-agent)
7. **Parent auto-completion:** if task has `parent_task` and all siblings are now "Finished", set parent to "Finished", close the parent's friction entries ("Friction entries a task fixes" above) and persist the parent's `decisions_pending` if it has any ("Persist decisions" above)
8. **`files_affected` drift update (FB-086):** if `report.issues[]` contains a minor severity entry with the form "files_affected declared {N} files but implementation touched {M}" AND `report.friction_markers[]` includes a `verification_gap` marker with `template_area: "task-schema files_affected"`, update the task JSON's `files_affected` to match the union of declared and actually-touched files (excluding infrastructure paths filtered in verify-agent T2b step 3). This keeps Step 2c's parallel-batch heuristic accurate for future dispatches.
9. **Dashboard regeneration:** sequential mode — regenerate now; parallel mode — defer

**Post-verify delta (after a per-task pass):** a small change to a task that has just passed goes back to the verifier that passed it, instead of a fresh verify dispatch (125–230K tokens each downstream) or an edit nobody re-checks. Independence holds because that verifier implemented nothing: it still judges work it did not write, which is why this is allowed and the orchestrator checking its own edit is not.

**A task others have built on is not reopened.** If any of these is true, leave the task Finished and make the change a new task (creation contract: `task-schema.md § "Drift Prevention Fields"`; same `spec_section`, depending on this task), implemented and verified by the normal path:

- a task whose `dependencies` include this one has been dispatched (its status is anything but Pending or On Hold);
- a phase-level verification has run since this task's pass (`.claude/verification-result.json` has a `timestamp` later than the task's `task_verification.timestamp`);
- the task is a subtask and its parent is already Finished (parent auto-completion, step 7 above, runs when the last sibling passes, and nothing sets a parent back).

Otherwise the delta is allowed when **all** of these hold:

- the task passed per-task verification in this session;
- the change is that verifier's own non-blocking finding (a `minor` entry in its `issues[]`, or a suggestion in its `notes`) or a micro-edit the user approved;
- it touches only files already in the task's `files_affected`;
- the same verifier can be resumed (you have its agent id and SendMessage is available).

A change that fails any of these four reopens the task for a fresh verification: set it In Progress with `completion_date` cleared (as a fail does), make the change by the normal implement path (the inline contract, or implement-agent), and continue through Awaiting Verification to work.md § "If Verifying (Per-Task)". That verification is an ordinary attempt.

**Reopening resets the counter.** Every time this block sends a task that had passed to a fresh verify-agent (the reopen just described, and the fail, refusal, unusable-reply and interruption outcomes of step 5), set `verification_attempts` to 0 before that dispatch, as drift reconciliation does when it sends a Finished task back (`drift-reconciliation.md`, "Attempt counter"). The attempts that led to the earlier pass are spent; without the reset a task that passed on its second attempt would escalate on the fresh verifier's first fail. `verification_history` keeps every entry.

Within the four conditions:

1. Note whether the user has already completed this task's review: it is `owner: "both"` or has a `test_protocol`, and `user_review_pending` is absent or `false`. Then set `status: "Awaiting Verification"`, `updated_date: today`. Awaiting Verification, not the inline contract's In Progress, is deliberate: if the session ends anywhere after this step, the recovery scan sends the task to a fresh verify-agent, which checks whatever is on disk.
2. Copy each file the edit will touch into `delta-before/` inside that verifier's evidence directory (keeping relative paths; replace an earlier delta's copies). Make the edit, and run the project's existing checks that cover it.
3. Prepend `[DELTA {YYYY-MM-DD}] {what changed, and why}` to `notes`.
4. Resume the same verifier with SendMessage. In parallel mode, a re-check that will use the browser or the build first waits its turn in the exclusive-verify queue as a `delta` entry (`parallel-execution.md § "Single-Instance Resources"`). Give it the delta alone: `diff -u {delta-before copy} {edited file}` for each file, or the literal old and new strings for a one-line edit. Not `git diff`: without per-task commits that is the whole implementation, and it omits untracked files. Ask it to re-check what the diff affects and return the standard per-task report (`verify-agent.md` § "Step T6"), raw JSON only, or its `delta_refused` reply.
5. When it returns, run the Residue check; a resume took no baseline, so it only reports. Then, by what came back:
   - **A report with `pass`.** Run the Empirical Evidence Gate if it applies (work.md § "If Verifying (Per-Task)"; a gate failure makes this a delta fail). If the gate doesn't run, copy the existing `task_verification.evidence[]` into the rewritten `task_verification`. Then apply "After verify-agent returns (per-task mode)" above with three differences: `verification_attempts` is not incremented (`new_attempts` is its current value); the `verification_history[]` entry carries `"delta": true`, repeats that attempt number, and its `cost` is the resumed turn's usage; and if step 1 found the review already completed, `user_review_pending`, `test_protocol` and `interaction_hint` are not written again.
   - **A report with `fail`.** Append the history entry the same way (`"delta": true`, nothing incremented) and write `task_verification` from the report. A delta fail never escalates, whatever the attempt count. Set `status: "In Progress"`, clear `completion_date`, prepend `[DELTA FAIL] {summary}` to `notes`. Then either restore the `delta-before/` copies or fix the edit, by the normal implement path, set Awaiting Verification, and dispatch a fresh verify-agent: attempt 1 after the reset above. Status path: Finished → Awaiting Verification → In Progress → Awaiting Verification → Finished on the fresh verifier's pass.
   - **`delta_refused`** (the verifier judges the change too large for a re-check, or finds it reaches outside `files_affected`). Write nothing to `verification_history[]`. The task is already Awaiting Verification with the edit on disk: reset the counter as above and dispatch a fresh verify-agent now.
   - **Anything else** (prose, malformed JSON, nothing usable, or the verifier can't be resumed after all). Same as a refusal: no history entry, the counter reset, a fresh verify-agent at once. This replaces step 5 above for a delta re-check: no second ask, no `[VERIFICATION TIMEOUT]`, no Blocked.
   - **An infrastructure termination** is an interruption as in step 5 above: the task stays Awaiting Verification, and a fresh verify-agent follows once the post-limit dispatch rule allows.

Never mark a delta as passed yourself, and never leave the edit in place with the task set back to Finished unverified.

**After verify-agent returns (phase-level mode):**

Run the Residue check above first.

1. **Write `.claude/verification-result.json`** using the report's payload: `result`, `timestamp`, `spec_version`, `spec_fingerprint`, `summary`, `criteria_passed`, `criteria_failed`, `criteria`, `issues`, plus a `tasks_created[]` array populated with the IDs of task files you create in the next step
2. **Create fix task files:** for each entry in `report.fix_tasks_to_create[]`, write `task-{id}.json` with the entry's `task_json` payload plus `out_of_spec` flag. An in-spec fix task gets provenance first (creation contract: `task-schema.md § "Drift Prevention Fields"`): run `python3 .claude/scripts/fingerprint.py --provenance .claude --section "<task_json.spec_section>"` and merge the four fields into the payload; a payload with `spec_unmapped: true` is written as it is. If the heading doesn't resolve (exit 1), or the payload has neither, pick the section from the spec index (`.claude/spec_v{N}.index.json`) and run `--provenance` on that, or set `spec_unmapped: true`; say which in the task's `notes`. Entries with `out_of_spec: true` need neither
3. **Append friction markers**
4. **Regenerate dashboard** — include Verification Debt sub-section if debt exists; show out-of-spec tasks with ⚠️ prefix
5. **If result is `fail`:** loop back to Execute phase for fix tasks. If `pass`: proceed to "If Completing"

## Task Completion (`/work complete`)

Use `/work complete` for manual task completion outside of implement-agent's workflow. This is useful when:
- Completing human-owned tasks
- Marking tasks done that were worked on outside the normal flow
- Quick tasks that don't need the full implement-agent process

**Note:** When implement-agent executes tasks, it handles completion internally (Steps 3-6 of its workflow). You don't need to run `/work complete` after implement-agent finishes.

### Process

1. **Identify task** - If no ID provided, use current "In Progress" task
2. **Validate task is completable:**
   - Status must be "In Progress", OR "Finished" with `user_review_pending: true`
   - Reject: "Pending", "Broken Down", "On Hold", "Absorbed", or "Finished" without `user_review_pending`
   - For quick tasks, first set status to "In Progress", then complete
   - Dependencies must all be "Finished"
3. **Verification enforcement:**
   - If the task has `task_verification.result == "pass"` → proceed (already verified)
   - If the task is Finished with `user_review_pending: true` → proceed (verification already passed, user is completing their review). The flag is only set together with Finished; on any other status it's stale — ignore it
   - If the task has `owner: "human"` AND no `task_verification` → auto-generate self-attestation:
     ```json
     {
       "task_verification": {
         "result": "pass",
         "timestamp": "ISO 8601",
         "checks": { "self_attested": "pass" },
         "notes": "Human task — completed by user",
         "issues": []
       }
     }
     ```
     Write to task JSON and proceed. Human tasks are verified by the user's attestation of completion, not by verify-agent.
   - If the task has `owner: "both"` → close each half on its own track (FB-100):
     - **Claude's half** is verified the normal way. If `user_review_pending: true` (verify-agent already passed Claude's contribution and set the flag, per the State Persistence Protocol § "After verify-agent returns"), proceed — the user's completion attests their half.
     - If there is no `task_verification` yet and Claude's contribution was a **mechanical deliverable**, spawn verify-agent first (as in the next bullet), then let the user attest their half on the pass.
     - If Claude's contribution was a **lived/conversational gate** with nothing mechanical to verify, auto-generate the same `self_attested` block as `owner: "human"` above, with `"notes": "Both-owned task — Claude's contribution delivered in-session; user attested completion"`. This is the clean close for "lived gates where Claude's half is done" — no verify-agent round-trip needed. (Distinguish the two sub-cases from the task's deliverable expectations; when ambiguous, ask the user which applies rather than defaulting to verify-agent.)
     - **Real personal / gitignored data (FB-108):** when the deliverable is the user's real personal data or lives on gitignored paths, do NOT dispatch verify-agent — it would pull personal data into a subagent context, and gitignored paths have no git baseline to diff against. Verification = user sign-off (acceptance — e.g. section-by-section review) + an orchestrator structural self-check (invariants, losslessness), recorded as `task_verification` with `"verified_by": "user + orchestrator"`. For losslessness checks on gitignored data, pass the pre-change "before" content explicitly to whoever verifies — no git baseline exists. (Proven downstream on real-canonical-data migrations.)
   - If the task has NO `task_verification` or `task_verification.result != "pass"` → **spawn verify-agent (per-task)** before allowing completion. Do not mark Finished without passing verification.
   - This ensures the structural invariant: no task reaches "Finished" without `task_verification.result == "pass"`.
3b. **Human deliverable validation** (for `human` and `both`-owned tasks):
   When the user completes a task that required them to provide deliverables (files, documents, configuration, credentials setup, etc.), validate before continuing:
   - **Check quantity:** Does what was provided match what the task expected? (e.g., task said "provide 2-3 CSV files" but user provided 1, or 5)
   - **Check usability:** Are the deliverables in a usable state? (e.g., files parse correctly, headers contain expected fields, format matches what downstream tasks need)
   - **Check plan validity:** Given what was actually provided, do dependent tasks still make sense as written, or do they need adjustment?
   - If any mismatch: surface the discrepancy and assess impact on dependent tasks. Options:
     ```
     Deliverable check for Task {id}:
     [issue description — e.g., "Expected 2-3 CSV files, received 1"]

     [A] Adjust — update dependent tasks to work with what was provided
     [P] Proceed — continue as-is (deliverables are sufficient despite the difference)
     [W] Wait — task stays in progress until deliverables are corrected
     ```
   - If deliverables pass validation: proceed silently to step 3c
3c. **Collect completion notes (interactive):**

   Ask for two clearly-separated kinds of notes so the user does not have to context-switch between project-focused and template-focused thinking. The two prompts run in sequence; each is independently skippable with Enter.

   **First prompt — Project notes (always shown):**

   ```
   Task {id}: "{title}" — any notes about the work itself? (Enter to skip)
   (decisions made, follow-ups, gotchas, anything worth remembering for this task)
   >
   ```

   - If non-empty: prepend it to the task's `user_feedback` as a dated entry (§ "State Persistence Protocol", "`user_feedback` is history too")
   - If empty: proceed without setting `user_feedback`

   **Second prompt — Template notes (shown only if `template_inbox_path` is configured in `.claude/version.json`):**

   ```
   Any notes about how Claude or the workflow handled this? (Enter to skip — bridges to template repo)
   (e.g. a step that felt off, an instruction that was unclear, something the template could do better)
   >
   ```

   - If non-empty: invoke the `/feedback template:` Mode 1 procedure with these notes as the capture body. Prepend a source line to the body so the template-side FB entry carries task context:
     ```
     Captured during /work complete on Task {id}: "{title}".

     [user's template notes]
     ```
     Mode 1 writes the local `FB-NNN` entry and, since `template_inbox_path` is set, writes the bridge export to the template inbox.
   - If empty: proceed without creating a template feedback item.

   **Why the conditional second prompt:** When `template_inbox_path` is unset, capturing template notes would create local-only FB entries in the downstream project that the user then has to carry over manually — the same friction the bridge was built to eliminate. Skipping the prompt when the bridge is disabled keeps the UX honest: we only ask the user to write template feedback when there is a destination for it.

   **Language principles for both prompts:**
   - Plain English only. Do not use template-internal terminology in user-facing prompt text (no "spec drift", "friction signal", "scope creep", "user_feedback signal", etc.).
   - Each label states what the prompt is for AND where the input lands. The user should not have to guess.
   - The two prompts are visually adjacent but clearly labeled — the user can tell at a glance which slot they are filling in.

   This is the PRIMARY feedback path for `/work complete`. Dashboard FEEDBACK markers remain as an ASYNC alternative for project notes — if the user wrote feedback in the dashboard before running `/work complete`, Step 4b captures it as fallback. (A template-side dashboard marker is not yet implemented; the second prompt is currently the only path for template notes during `/work complete`.)
4. **Check work** - Review all changes made for this task
   - Look for bugs, edge cases, inefficiencies
   - If issues found, fix them before proceeding
4b. **Capture dashboard feedback (fallback)** - Read dashboard for `<!-- FEEDBACK:{id} -->` markers matching the completing task
   - If non-empty content found AND no inline feedback was captured in Step 3c, prepend it to the task's `user_feedback` as a dated entry
   - If both inline (Step 3c) and marker feedback exist, they share one dated entry: inline first, then marker content (newline-separated)
5. **Update task file:**
   ```json
   {
     "status": "Finished",
     "completion_date": "YYYY-MM-DD",
     "updated_date": "YYYY-MM-DD",
     "notes": "{what was done, any follow-ups needed} {existing notes}",
     "user_feedback": "[YYYY-MM-DD] Use OAuth2 instead of JWT. The client requires SSO support.\n{existing user_feedback}"
   }
   ```
   - `notes`: prepend what was done to the existing `notes` (just the new text when `notes` is empty); never replace them (§ "State Persistence Protocol").
   - If `user_review_pending` is `true`, clear it.
   - `user_feedback`: the dated entry from Steps 3c/4b prepended to the existing value; never replace it. If `test_protocol` exists and guided testing was completed, the results go in that same entry.
   - Close the task's friction entries (State Persistence Protocol, "Friction entries a task fixes").
   - If the task has a non-empty `decisions_pending`, write its decision record (State Persistence Protocol, "Persist decisions").
6. **Check parent auto-completion:**
   - If parent_task exists and all non-Absorbed sibling subtasks are "Finished"
   - Set parent status to "Finished", close the parent's friction entries and persist its `decisions_pending` (same two rules)
7. **Regenerate dashboard** - Follow `.claude/support/reference/dashboard-regeneration.md` (this is user-initiated, so the dashboard should be current when they're done)
8. **Surface unblocked tasks** - After regen, check if this completion unblocked any human-owned or both-owned tasks. If so, announce inline: `Note: Task {id} ("{title}") is now available for you — {brief description}`.
9. **Auto-archive check** - If active task count > 100, archive old tasks (§ "Auto-Archive" below)
10. **Post-dispatch validation** - Run main `/work` Step 5 checks (task file integrity, dashboard exists, session sentinel)

### Rules

- Never work on "Broken Down", "On Hold", or "Absorbed" tasks directly
- Parent tasks auto-complete when all non-Absorbed subtasks finish
- Always add notes about what was actually done

## Auto-Archive

After regenerating the dashboard, check if archiving is needed:

1. **Count active tasks** - All non-archived task-*.json files
2. **If count > 100:**
   - Identify finished tasks older than 7 days, except any with `user_review_pending: true` (once archived, its open review would drop off the "Needs you" card and Verification Pending could fire)
   - Move to `.claude/tasks/archive/`
   - Update archive-index.json with lightweight summaries
   - Regenerate dashboard again

### Archive Structure

```
.claude/tasks/archive/
├── task-1.json           # Full task data (preserved)
├── task-2.json
└── archive-index.json    # Lightweight summary
```

### Referencing Archived Tasks

When a task ID is referenced but not found in active tasks:
- Check `.claude/tasks/archive/` for context
- Read archived task for reference (provides historical context)
- Archived tasks are read-only reference material
