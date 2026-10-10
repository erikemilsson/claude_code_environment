# Parallel Execution

Procedures for assessing parallelism eligibility, detecting file and single-instance-resource conflicts, building conflict-free batches, and dispatching/collecting parallel agents. These run inline during `/work` Steps 2c and 4.

**Scope:** this doc covers *intra-session* parallelism — multiple `Agent` subagents coordinated by one `/work` orchestrator within a single conversation. For *inter-session* parallelism (many independent `claude` processes for batch workloads), see `.claude/support/reference/automation.md`.

---

## Parallelism Eligibility Assessment

After phase and decision checks pass, assess whether multiple tasks can be dispatched in parallel (runs as `/work` Step 2c).

### 1. Read Configuration

```
Read parallel_execution from spec frontmatter:
├─ enabled: true (default)
├─ max_parallel_tasks: 3 (default)
└─ If not present, use defaults
```

If `enabled: false`, skip to Step 3 (sequential mode).

### 2. Gather Eligible Tasks

```
eligible = tasks where ALL of:
  - status == "Pending" (excludes On Hold, Absorbed, Blocked, Broken Down)
  - owner != "human"
  - all dependencies have status "Finished"
  - task.phase <= active_phase OR task.cross_phase == true (no phase dependency blocks the task)
  - all decision_dependencies are resolved
  - difficulty < 7
```

### 3. Build Conflict-Free Batch

#### File Conflict Detection Algorithm

Two paths conflict if either could affect the other's output. The comparison uses **normalized paths** and **directory containment**:

```
FUNCTION paths_conflict(path_a, path_b) -> bool:
  # 1. Normalize both paths: resolve "." and "..", lowercase on case-insensitive
  #    filesystems (macOS), strip trailing slashes
  a = normalize(path_a)
  b = normalize(path_b)

  # 2. Exact match
  IF a == b: return true

  # 3. Directory containment: if either path is a prefix of the other
  #    (a directory contains a file, or vice versa)
  #    e.g., "src/" conflicts with "src/auth.py"
  #    e.g., "src/models/" conflicts with "src/models/user.py"
  IF a.startswith(b + "/") OR b.startswith(a + "/"): return true

  # 4. No conflict
  return false
```

**Rules:**
- Paths are relative to project root (no leading `./ `)
- `src/auth.py` vs `src/auth.py` → conflict (exact match)
- `src/` vs `src/auth.py` → conflict (directory containment)
- `src/auth.py` vs `src/models.py` → no conflict (different files)
- `.env` vs `.env.example` → no conflict (different files)
- Glob patterns in `files_affected` (e.g., `src/*.py`) are expanded before comparison

#### Batch Building

```
batch = []
held_back = []  # tracks tasks skipped due to file conflicts

For each eligible task (sorted by priority, then ID):
  conflicts = false
  conflict_with = null
  conflict_files = []
  For each task already in batch:
    For each pair (file_a from task.files_affected, file_b from batch_task.files_affected):
      IF paths_conflict(file_a, file_b):
        conflicts = true
        conflict_with = batch_task.id
        conflict_files.append(file_a + " vs " + file_b)
        break
    IF conflicts: break
  IF NOT conflicts AND batch is non-empty
     AND (task, or a task already in batch, can't be implemented without running the build):
    # § "Single-Instance Resources": such a task runs alone. Needing the build or the
    # browser only for verification is not a conflict.
    conflicts = true
    conflict_with = that batch_task.id (the first batch task when the candidate is the one)
    conflict_files = ["build output " + the directory the build writes]
  IF task has empty files_affected AND parallel_safe != true:
    skip (unknown file impact — not safe for parallel)
  ELSE IF conflicts:
    held_back.append({
      task_id: task.id,
      blocked_by: conflict_with,
      conflict_files: conflict_files
    })
  ELSE IF len(batch) < max_parallel_tasks:
    add task to batch
```

### 4. Determine Dispatch Mode

```
IF len(batch) >= 2:
  → parallel_mode = true
  → Log: "Parallel dispatch: {batch_size} tasks eligible"
  → IF held_back is non-empty:
      Log for each: "Task {id} held back — file conflict with Task {conflict_with} on: {conflict_files}"
ELSE:
  → parallel_mode = false
  → Fall back to sequential execution in Step 3
```

### 5. Scan for Shared Scaffolding Contracts

After determining `parallel_mode = true`, run shared-scaffolding detection on the batch. See § "Shared Scaffolding Contracts" below.

### Single-Instance Resources

Two tasks with no file in common can still collide on something the checkout has only one of: the browser session and the build output directory. Neither keeps tasks from being implemented together. Implement-agents are told to leave both alone, and the verifications that need one take turns. No task field records the need. The orchestrator judges each task from its `title` and `description` (acceptance criteria included), its `test_protocol` if it has one, its `files_affected`, and the project's build command (root `./CLAUDE.md § Verification Hooks`).

| Resource | A task's verification needs it when |
|----------|-------------------------------------|
| **A single-session MCP**: the browser (Playwright), or any other MCP `mcp-patterns.md § "MCP and Parallel Execution"` lists | verifying it means loading a page: a criterion about what a route renders, layout, a screenshot or an interaction, or `files_affected` that are web-UI routes or components |
| **The build output directory**: whatever the build command writes (`dist/`, `.next/`, `build/`, `target/`) | its verify-agent will run the build command: a criterion or `test_protocol` step needs a successful or production build, or the project's Verification Hooks run the build for the files it touches |

A verification that needs either one is an **exclusive** verification.

**Implement in parallel, without the browser or the build.** In parallel mode every implement brief carries both lines, whether the agent is dispatched with the batch or later by incremental re-dispatch, and whatever the other tasks are:

- "Don't use the browser MCP: its one session is shared with other agents. Check your work with tests, the type checker or HTTP requests; rendered checks happen in verification."
- "Don't run the production build (`{build command}`): its output directory is shared with other agents. Type-check and run the tests; the build runs in verification." (Omit when the project declares no build command.)

**Verify one at a time: the exclusive-verify queue.**

- At most one exclusive job runs at a time. When the implement-agent of a task returns `completed` and its verification is exclusive while the queue is busy, the task stays "Awaiting Verification" and joins `exclusive_verify_queue`. The queue is first in, first out, in the order the implement reports were processed.
- Three kinds of job take a turn, and a queue entry records which (`{task_id, kind}`). Running the head of the queue means, by kind:
  - `verify`, an exclusive verify-agent: dispatch it and add it to `active_verifiers` marked `exclusive`.
  - `delta`, a post-verify delta re-check that will use the browser or the build (`work-procedures.md`, "Post-verify delta"): send that verifier its SendMessage resume (step 4 there) and add it to `active_verifiers` marked `delta` and `exclusive`, so the loop waits for its reply; the reply is handled by step 5 there, not by the verify protocol. A delta re-check that needs neither resource takes no turn: it is resumed at once and tracked in `active_verifiers` marked `delta` only, so the loop waits for it too, but it never makes the queue busy and its return does not run the head. **Fresh verifier after a delta:** a fresh verify-agent that step 5 calls for is an ordinary verification. When it is exclusive it joins the tail as a `verify` entry, never ahead of the queue, and the head is run if the queue is not busy.
  - `gate`, the orchestrator's own Empirical Evidence Gate (`work-web-evidence.md`: its browser assertions and its client-bundle production build) for a task whose verification or delta re-check was not exclusive. **Queued gate:** it gets an entry when that pass arrives while the queue is busy: dual-write the report's `friction_markers` then (not again when the entry is run), keep the report, and leave the task "Awaiting Verification" until its turn. With the queue free the gate runs at once, with no entry. At the head: run the gate now, finish that task's after-return steps with the kept report (a failing gate makes it a fail), then run the next head. The kept report exists only in the conversation. If it is lost (compaction, a cutoff), the task is still "Awaiting Verification" and is verified again, by `session-recovery.md` case 1 or Step 3; the new verifier's markers are written as any return's, so the log can hold the lost report's markers twice, which is accepted.
- The queue is busy while `active_verifiers` holds an exclusive job: an exclusive verify-agent, or a delta re-check marked `exclusive`. The orchestrator's gate is its own work inside one turn; nothing is dispatched during it, so it never leaves the queue busy between notifications.
- The gate after an exclusive verification or an exclusive delta re-check needs no entry: it runs inside that task's turn, after the verifier returns and before the head of the queue is run.
- When an exclusive job ends, with a report or without one, finish its after-return steps, then run the head of the queue. The residue check among those steps stops a server the agent reported and left listening only once no other agent of the batch is running (`work-procedures.md § "Residue check"`, "In a parallel batch"); the queue doesn't wait for that moment.
- Verifications that are not exclusive are dispatched at once, as before, and run alongside.
- Unsure whether a verification needs the browser or the build → treat it as exclusive. A queued verification costs minutes; two agents driving one tab produce snapshots of each other's pages with no error, and two builds into one directory produce a bundle neither wrote.

**Held out of a batch: only a task that can't be implemented without running the build** (build configuration, a bundler plugin, the build script itself). It is the one case where the no-build line can't apply, so it runs alone: in § 3 it is held back like a file conflict, with `conflict_files: ["build output {dir}"]`, whenever the batch already has a task, and other tasks are held back the same way when it is already in the batch. At incremental re-dispatch it starts only when no other agent is running and the queue is empty, and nothing else is dispatched until its implement-agent returns. Its verification joins the queue like any other. A task whose checks merely include the build is not this case: its implement-agent skips the build and its verifier runs it.

A sequential run needs none of this: one agent at a time holds both resources.

---

## Shared Scaffolding Contracts

When a parallel batch contains two or more tasks that share test scaffolding (allowlists, fixtures, expected-violation arrays) where one task writes the scaffolding and another drains it, the orchestrator must compose a single shared briefing block both agents receive verbatim. Without this, the dispatched briefs can contradict each other on file boundaries.

**Example:** Task A's brief says "do not touch `registry-consistency.test.ts`" (B's territory). Task B's implementation writes a failing-test assertion in that file that A must drain, so A has to violate its own brief to keep the test suite green.

### Detection

After the conflict-free batch is built (Eligibility § 3), scan for shared-scaffolding pairs. A pair triggers a shared contract when ALL of:

- The two tasks have an **overlap relationship** on at least one file — either explicit `files_affected` overlap that survived conflict-detection (rare; usually a glob vs explicit path), OR an implicit overlap inferred from task descriptions (e.g., both mention the same fixture/allowlist filename)
- One task's description (`title` + `description`) mentions any of: `expected`, `allowlist`, `fixture`, `scaffolding`, `expected_violations`
- The other task's description mentions any of: `drain`, `drop`, `close`, `resolve`, `remove`, `clean up`

When the heuristic fires for a pair, compose a `shared_contract` payload and attach it to BOTH agents' dispatch context.

### Shared Contract Schema

```json
{
  "shared_contract": {
    "type": "allowlist_drain | fixture_sync | scaffolding_handoff",
    "file": "path/to/shared/scaffolding/file",
    "constants": ["EXPECTED_T463_VIOLATIONS", "..."],
    "owner": "task-id that writes the scaffolding",
    "drainer": "task-id that drops entries when work resolves",
    "test_signal": "failing-test message or assertion that mediates the contract",
    "agreement": "one-sentence statement both agents must accept verbatim — overrides any contradictory per-agent brief"
  }
}
```

### Briefing Behavior

Both implement-agents receive the same `shared_contract` block as part of their dispatch context. The `agreement` field is presented as authoritative: if any per-agent brief contradicts it (e.g., "do not touch file X" vs the contract's "X is shared between tasks"), the contract wins.

The orchestrator does NOT autonomously invent `shared_contract` payloads — it composes them only when the detection heuristic fires. The heuristic is not exhaustive (may miss less-obvious scaffolding patterns) nor perfectly precise (may fire on false positives). When a contract is composed, log the pair + match reason for post-batch review. If no contract is composed but agents still collide on scaffolding, both agents should emit friction markers (type: `template_gap`, details: "shared scaffolding contract not detected") so the heuristic can be refined.

### Interaction with Pre-Dispatch Confirmation

When the batch is presented to the user (Pre-Dispatch Confirmation § Format), include any composed contracts inline so the user can sanity-check the owner/drainer assignment before dispatch:

```
Shared contracts:
  - allowlist_drain on registry-consistency.test.ts (owner: T463, drainer: T462)
    Agreement: T463 writes EXPECTED_T463_VIOLATIONS scaffolding; T462 drains it as violations resolve.
```

---

## Pre-Dispatch Confirmation

When Step 2c produces a parallel batch of **3 or more tasks**, confirm with the user before spawning. Batches of 2 skip this step — the parallel-dispatch default of 3 means a 2-batch is a partial use of the budget and the cheapest case to interrupt if wrong.

### Pre-flight checks (before presenting the prompt; apply to 2-batches too)

- **Working-tree re-check:** run `git status` immediately before dispatch — not only at Step 0e session start. A concurrent session (or the user) may have changed the tree since; if unexpected modifications appear, surface them and re-run the conflict assessment before spawning. This is also the moment to take the batch's residue baseline (`work.md § "Before Any Dispatch"`: git status, root listing, listening ports). (Observed downstream: a concurrent retirement broke the tree — dangling imports — while a batch's agents were mid-flight.)
- **Session-budget awareness:** parallel long-running agents multiply exposure to a platform usage/session limit — a cutoff kills ALL in-flight agents with zero-token returns and partial on-disk state (recovery: `work-procedures.md § "After implement-agent returns"`, zero-token branch). If the session has already consumed heavy budget (long conversation, prior limit warnings), prefer sequential or a smaller batch. **Post-limit dispatch rule:** after one limit hit in a session, three things wait for the user's explicit go-ahead: (a) dispatching two or more agents at once, or adding an agent while another is running; (b) anything more from the current batch or its queue, even when nothing is running; (c) dispatching the cut-off job again, whole or its remainder (that implementation, or that verification). One agent at a time on anything else doesn't wait: the zero-token recovery's confirm-only implement-agent, a verify-agent for work that is complete on disk, the next sequential task. The follow-up batch is likely to be cut too (observed: an immediate second parallel batch was also lost).

### Format

```
Parallel dispatch ready: {N} tasks

  Task {id}: "{title}" → files: [{files_affected}]
  Task {id}: "{title}" → files: [{files_affected}]
  ...

Verify strategy: per-task verify-agent dispatched as each implement-agent completes.
{If two or more batch tasks have an exclusive verification (§ "Single-Instance Resources"):}
Exclusive verification: Tasks {ids} are verified one at a time (browser session / build output).

{If held_back is non-empty:}
Held back (file conflicts):
  Task {id}: "{title}" — conflict with Task {conflict_with} on [{conflict_files}]
  (a task that must run the build to be implemented shows as: runs alone, on [build output {dir}])

[D] Dispatch  [S] Skip — review batch first  [1] Dispatch only first task
```

### Behavior

- `[D]` Dispatch → proceed to § "Parallel Dispatch" Step 1 (Log the Parallel Dispatch)
- `[S]` Skip → return to `/work` Step 2c. User can review tasks, adjust priorities, edit `files_affected`, then re-run `/work`.
- `[1]` Dispatch only first task → drop the batch, treat as sequential single-task dispatch on the highest-priority eligible task.

### Rationale

Parallel batches scale Claude's throughput but also remove the natural pause-points that sequential dispatch provides (per-call permission prompts, post-task user-visible state changes). A pre-dispatch confirmation restores a cheap human checkpoint without changing parallel-batch behavior.

Independent of permission settings or auto-mode classifier behavior — auto mode (which removes per-call permission prompts) actually makes this checkpoint *more* valuable, not less.

---

## Parallel Dispatch

When Step 2c produces a parallel batch of >= 2 tasks, execute them concurrently (runs as `/work` Step 4 "If Executing (Parallel)").

### 1. Log the Parallel Dispatch

```
Dispatching N tasks in parallel:
  - Task {id}: "{title}" → files: [{files_affected}]
  - Task {id}: "{title}" → files: [{files_affected}]
  ...
  File conflicts: none between batch members (verified in Step 2c)

Held back (file conflicts):
  - Task {id}: "{title}" — conflict with Task {conflict_with} on [{conflict_files}]
  (Or: "None" if held_back is empty)
```

### 2. Set Batch Tasks to "In Progress" and Annotate Held-Back Tasks

Before spawning agents, update every task in the batch:
```json
{
  "status": "In Progress",
  "updated_date": "YYYY-MM-DD"
}
```

For each held-back task, add a temporary `conflict_note` to the task JSON:
```json
{
  "conflict_note": "Held: file conflict with Task {id} on {files}. Auto-clears when conflict resolves."
}
```

The dashboard does not render this note (`dashboard-render.py` doesn't read `conflict_note`); it is removed when the task is dispatched.

### Write Ownership Rules

During parallel execution, strict write ownership prevents file corruption. The rules apply **while agents are running** (between spawning in Step 3 and result collection in Step 4):

| Writer | May write to | Must NOT write to |
|--------|-------------|-------------------|
| Each parallel agent | Nothing — agents return structured reports only (harness prohibits subagent writes to `.claude/`) | Any `.claude/` path |
| `/work` orchestrator | All task JSONs, parent task JSONs, decision records, dashboard.html, verification-result.json, dashboard-state.json, session-log.jsonl, fix-task JSON files | Nothing — orchestrator is the sole writer in this architecture |

The orchestrator performs all writes: it sets `conflict_note` fields before dispatch, consumes each agent's return report to persist task-JSON state, performs parent auto-completion, and regenerates the dashboard at batch end.

**Key invariants:**
- **Single writer:** The orchestrator is the only writer for all `.claude/` state (task JSON, dashboard, verification-result.json, session-log.jsonl). Agents return structured reports; all persistence is mediated.
- **`.claude/`-path tasks never batch:** a task whose `files_affected` includes `.claude/` paths is orchestrator-authored inline and cannot join an agent-dispatch batch; split mixed tasks at decomposition (`decomposition.md § Procedure` step 8, `.claude/`-boundary split).
- **Sequential result processing:** When several completion notifications arrive together, the orchestrator processes them one at a time (the `For each completed agent` loop is sequential). This naturally serializes task-JSON writes, parent auto-completion, and friction-marker appends — no race conditions possible since there's only one writer.
- **Verify-agent dispatch per implement-agent:** After each implement-agent report is processed, the orchestrator dispatches that task's verify-agent. Verify-agents can run concurrent with subsequent implement-agents, preserving pipeline throughput. The one exception is exclusive verifications (browser or build), which take turns (§ "Single-Instance Resources").

### 3. Spawn Parallel Agents

Use Claude Code's `Agent` tool to spawn one agent per task. **Always set `model: "opus"` and state a turn budget of about 40 tool calls in the prompt** so agents run on the Opus tier (1M context) and know when to wind down — the budget is advisory, not enforced (canonical dispatch value + pin relationship: `.claude/CLAUDE.md § Model Requirement`). Each agent receives:
- The task JSON to execute
- Instructions to read `.claude/agents/implement-agent.md`
- Instructions to follow Steps 1-6 (understand, implement, run existing checks, return structured report)
- **Sibling files:** the `files_affected` of every other task in the batch, with the instruction: "Don't edit these files; they belong to parallel tasks. If your change requires one, report it in `issues_discovered` with `suggested_action: 'stop and report'`." Files outside the whole batch's declared scope may be edited and reported, per implement-agent Step 2
- **The "Before Any Dispatch" lines** (`work.md § "Before Any Dispatch"`, the one place they are worded): the evidence-directory line, naming this agent's own `{scratch}/agent-{task_id}-implement-{n}/`, which also asks for `servers_started`; and the brief-claims line. Every agent in the batch gets its own directory, and so does each verify dispatch (step 4), so one agent's cleanup can't delete another's evidence
- **The no-browser and no-production-build lines** (§ "Single-Instance Resources"), on every implement brief
- **Held decisions:** if the task has `decisions_pending` (a fix round or resume), its entries: the agent restates the set, amended as needed, in its report
- **Wind-down instruction:** "Turn budget: about 40 tool calls. If you get close, stop and return your report with what you have, marked partial — by tool call 35 if not complete, with `implementation_status: 'partial'` and detailed notes. Do NOT attempt writes to `.claude/` — subagents cannot write there; orchestrator handles all persistence from your report."
- **Explicit instruction:** "Return a structured implementation report per `.claude/agents/implement-agent.md` § Step 6. Do NOT write to task JSON, do NOT spawn verify-agent, do NOT regenerate dashboard — orchestrator owns all state persistence."

All agents run concurrently via parallel `Agent` tool calls with `model: "opus"`.

### 4. Collect Results with Incremental Re-Dispatch

`Agent` calls run in the background, and the harness notifies you as each agent finishes (completed or failed), with its report. Don't poll, and never read an agent's output file — it's the full transcript and floods your context. With `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`, `Agent` calls block and return their reports directly; process them the same way. If an agent seems stalled, tell the user; stopping it counts as an interruption. Handle each notification as it arrives:

```
active_agents = {task_id: {agent_id, spawned_at} for each spawned implement-agent}
active_verifiers = {task_id: {agent_id, spawned_at, exclusive?, delta?} for each spawned or resumed verifier}
exclusive_verify_queue = []  # {task_id, kind} entries waiting for the browser or the build; kinds, "busy" and
                             # "run the head" are defined in § "Single-Instance Resources"

WHILE active_agents, active_verifiers or exclusive_verify_queue is non-empty:
  Wait for the next completion notification (end your turn if nothing else is pending; it resumes you)

  For each completed implement-agent:
    1. Read implement-agent's return report (structured schema per implement-agent.md § Step 6)
       and run the Residue check for this agent first (work-procedures.md § "Residue check";
       see "Residue in a batch" below the loop)
    2. Apply "After implement-agent returns" protocol from work.md § State Persistence Protocol:
       - Status transition on task JSON per implementation_status
       - Dual-write friction_markers to .pending-markers.jsonl AND .session-log.jsonl
         immediately upon agent return (do NOT defer or batch)
       - Hold decisions_to_record in the task's decisions_pending (no decision file yet)
    3. If implementation_status == "completed":
       IF the task's verification is exclusive AND the queue is busy:
         Append {task_id, kind: "verify"} to exclusive_verify_queue; the task stays
         "Awaiting Verification"
       ELSE:
         Dispatch verify-agent for this task (Agent tool, model: "opus", turn budget of about
         30 tool calls in the prompt, the "Before Any Dispatch" lines with evidence directory
         {scratch}/agent-{task_id}-verify-{n}/)
         Add to active_verifiers (marked `exclusive` when its verification is). Verify-agent
         dispatch is individual — one per completed implement-agent, runs concurrent with
         remaining implement-agents.
    4. Remove implement-agent from active_agents
    5. INCREMENTAL RE-DISPATCH:
       - Re-run Step 2c eligibility assessment with current state
         (completed tasks are now "Awaiting Verification" or "Finished", their files are released)
       - Any previously held-back tasks whose conflicts are now resolved
         become eligible
       - If new eligible tasks found AND len(active_agents) < max_parallel_tasks:
         Spawn new implement-agents for newly-eligible tasks, with the same brief as § 3
         (the no-browser and no-production-build lines included)
         Add to active_agents
       - Clear conflict_note from newly-dispatched tasks

  For each completed verify-agent:
    (A reply from a verifier resumed for a delta re-check, marked `delta` in active_verifiers:
     apply work-procedures.md "Post-verify delta" step 5 in place of steps 1-2, then steps 3-4.
     Its gate on a pass is queued or run as step 2 says; a fresh verify-agent it calls for
     follows § "Single-Instance Resources", "Fresh verifier after a delta".)
    1. Read verify-agent's return report (structured schema per verify-agent.md § Step T6)
       and run the Residue check for this agent first (work-procedures.md § "Residue check")
    2. On a pass, run the Empirical Evidence Gate first when it applies (work.md § "If
       Verifying (Per-Task)"). After an exclusive job it uses this task's turn. Otherwise it
       runs now if the queue is not busy; if the queue is busy, append {task_id, kind: "gate"}
       to exclusive_verify_queue as § "Single-Instance Resources", "Queued gate" says, and
       apply the rest of this step when the entry is run. Then apply "After verify-agent
       returns (per-task mode)" protocol from work.md § State Persistence Protocol:
       - Write task_verification, append verification_history, increment verification_attempts
       - Transition status (Finished / In Progress retry / Blocked escalate)
       - On pass: persist decisions_pending as one `recorded` decision record ("Persist
         decisions"); the id is assigned here, so tasks in a batch can't pick the same one
       - Dual-write friction_markers (see work.md § State Persistence Protocol step 2)
       - Check parent auto-completion
       - No valid report → ask once for it (no increment; it stays in active_verifiers); a
         second invalid return → protocol step 5. Infrastructure termination (usage limit /
         HTTP 429 / zero-token return / API or harness error) or a stop the user asked for is
         an interruption: no increment, task stays "Awaiting Verification"
    3. Remove verify-agent from active_verifiers (unless it was re-asked above)
    4. If it was marked `exclusive` (a verification or a delta re-check) and it left
       active_verifiers: run the head of exclusive_verify_queue (a `verify` entry is
       dispatched as in implement step 3, ELSE branch; a `gate` entry runs that task's gate
       and finishes its step 2, then the next head is run)

  For each agent whose notification reports a failure (no report returned):
    Run the Residue check for this agent first (work-procedures.md § "Residue check"), in both
    cases 1 and 2: an agent that was killed stopped nothing and removed nothing. Its evidence
    directory is kept.
    (A verifier resumed for a delta re-check, marked `delta` in active_verifiers, that ends
     without a report: apply work-procedures.md "Post-verify delta" step 5 in place of cases
     1-2 — its "infrastructure termination" outcome for case 1, its "anything else" outcome
     otherwise: no second ask, no "[VERIFICATION TIMEOUT]", no Blocked — then steps 3-5. The
     fresh verify-agent follows § "Single-Instance Resources", "Fresh verifier after a delta".)
    1. Infrastructure termination (usage limit / HTTP 429 / zero-token return / API or harness error) or a stop the user asked for is an interruption, not a timeout:
       - Implement-agent: follow work-procedures.md "Zero-token return — platform limit cutoff"
       - Verify-agent: no increment, task stays "Awaiting Verification"; apply that
         bullet's post-limit dispatch rule before re-dispatching
    2. Any other failure:
       - Implement-agent: if task still "In Progress", set to "Blocked" with
         "[AGENT TIMEOUT] Parallel agent ended without a report"
       - Verify-agent: no valid report → protocol step 5 (ask once, then "[VERIFICATION TIMEOUT]")
    3. Remove from active_agents / active_verifiers
    4. Report to user: "Task {id}: agent ended without a report — may need investigation or retry"
    5. If it was marked `exclusive` (a verification or a delta re-check): run the head of
       exclusive_verify_queue, unless case 1's post-limit dispatch rule holds the queue for
       the user's go-ahead (the queued tasks then stay "Awaiting Verification")
```

This enables **incremental re-dispatch**: when Task A completes and releases its files, Task C (which was held back due to conflict with A) can start immediately — even while Tasks B and D are still running. A task held because its implementation must run the build is the exception: it starts only when nothing else is running (§ "Single-Instance Resources").

**Residue in a batch.** `work-procedures.md § "Residue check"` ("In a parallel batch") says what the check may do while other agents are running and what waits for step 5.

### 5. Post-Parallel Cleanup

After all agents complete (active_agents, active_verifiers AND exclusive_verify_queue are empty):

```
0. Residue check for the batch as a whole (work-procedures.md § "Residue check", "In a
   parallel batch"): the files and listeners left for the end are handled now

1. Final parent auto-completion check

2. Single dashboard regeneration:
   Regenerate dashboard.html per the Dashboard Regeneration Procedure
   - Remove all conflict_note fields from task JSONs (cleanup)

3. Operational checks (Step 5)

4. Loop back to Step 2c:
   Reassess remaining tasks for next parallel batch or phase transition
```

### 6. Handling Mixed Results

When some tasks pass and others fail verification:
- Passed tasks remain "Finished" — they are done
- Failed tasks are set back to "In Progress" by the orchestrator when it processes their verify-agent report
- On the next loop iteration, failed tasks are re-eligible for dispatch (potentially in a new parallel batch)
