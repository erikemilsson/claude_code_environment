# DEC-004 Implementation Plan — Formalize Orchestrator Ownership

**Purpose:** Execute DEC-004 Option B across 6 files. This plan contains the design contracts, per-file change specs, execution order, and verification checklist. A fresh session can read this plan and execute without re-deriving context.

**Status:** Ready to execute
**Created:** 2026-04-17
**Upstream:** Template upgrade tracker `template-upgrade-2026-04.md`, Phase 1
**Cleanup tag:** DELETE-AFTER (tracked in upgrade tracker's Cleanup Manifest)

---

## Context to Load Before Executing

Read these in order at session start:

1. `template-upgrade-2026-04.md` — upgrade phase state
2. `decisions/decision-004-subagent-capability-contract.md` — decision + full research
3. Current state of the 6 target files (listed in Per-File Change Specs below)

Then execute this plan.

---

## Approved Context

### The decision (locked)

DEC-004 Option B: **Formalize orchestrator ownership**. All task-JSON writes and Task-tool dispatches move from subagents to the `/work` orchestrator. Agents return structured reports; orchestrator persists state.

### Verified constraints (Apr 2026 research still current)

- Subagents still cannot write to `.claude/` paths (Anthropic issue #38806, unresolved)
- Subagents still cannot use the `Task` tool (issue #4182, deliberate design limitation)
- Subagents still do not inherit parent `permissions.allow` (issues #18950, #22665, #37730)
- Orchestrator (main `/work` session, not a subagent) has full `.claude/` write access — this is why Option B works

### Approved judgment calls

1. **Verify-agent dispatch timing in parallel mode:** after each implement-agent returns, orchestrator dispatches its verify-agent individually (not batched). Preserves pipeline throughput — verify-agents can run concurrent with subsequent implement-agents.
2. **State Persistence Protocol placement:** inlined as a new sub-section in `work.md` Step 4 (not extracted to `support/reference/`). Orchestrator is the only consumer — splitting adds indirection.
3. **Timeout logic ownership:** verification_attempts increment, Blocked at 3 attempts, `[VERIFICATION TIMEOUT]` note — behavior unchanged, but the logic moves from verify-agent to orchestrator.
4. **Friction markers:** (user Q2 answer = a) agents emit friction markers in their structured report; orchestrator appends to `.claude/support/workspace/.session-log.jsonl`.
5. **Write scope:** (user Q1 answer = confirm) all subagent writes move to orchestrator — not just status transitions. Includes `task_verification`, `verification_history`, `test_protocol`, `interaction_hint`, `user_review_pending`, fix task creation, `verification-result.json`, `dashboard.md` regeneration.

---

## Design Contracts — Agent Return Schemas

These are the CONTRACTS. Do not deviate; these schemas must appear verbatim in the rewritten agent files as the "Output" specification.

### Implement-agent structured report

```json
{
  "task_id": "string (e.g., '7' or '7.2')",
  "implementation_status": "completed | partial | blocked | misaligned",
  "completion_date": "YYYY-MM-DD (null if not completed)",
  "notes": "one-paragraph summary including [Multi-file: N] flag when N>=2 files modified",
  "files_modified": ["relative/path/to/file"],
  "friction_markers": [
    {
      "type": "workflow_deviation | spec_drift | informal_decision | scope_creep | user_feedback_signal | template_gap",
      "timestamp": "ISO 8601",
      "details": "one-sentence summary",
      "template_area": "which template file/section the marker applies to"
    }
  ],
  "issues_discovered": [
    {
      "type": "blocker | non_blocking | scope_creep | spec_drift | decision_made | spec_misalignment",
      "description": "one-sentence description",
      "suggested_action": "create new task | flag for human | proceed | stop and report"
    }
  ]
}
```

**Implementation_status semantics:**
- `completed`: all work done per spec, ready for verification
- `partial`: wind-down triggered — work incomplete, status stays "In Progress" with `[PARTIAL]` notes
- `blocked`: cannot proceed (dependency, ambiguity, permission) — status → "Blocked"
- `misaligned`: implementation revealed spec-conflict — orchestrator handles spec-check conversation

### Verify-agent structured report (per-task mode)

```json
{
  "task_id": "string",
  "mode": "per_task",
  "result": "pass | fail",
  "attempt_number": "N (caller computes from verification_attempts + 1; agent records it in response for audit)",
  "timestamp": "ISO 8601",
  "checks": {
    "files_exist": "pass | fail",
    "consistency_check": "pass | fail",
    "spec_alignment": "pass | fail",
    "output_quality": "pass | fail",
    "runtime_validation": "pass | fail | partial | not_applicable",
    "integration_ready": "pass | fail",
    "scope_validation": "pass | fail"
  },
  "notes": "human-readable summary",
  "issues": [
    { "severity": "minor | major | critical", "description": "one-sentence issue" }
  ],
  "test_protocol": { "...T4b shape..." } | null,
  "interaction_hint": "cli_direct | dashboard | null",
  "user_review_pending": true | false,
  "friction_markers": [ "...same shape as implement-agent..." ]
}
```

### Verify-agent structured report (phase-level mode)

```json
{
  "mode": "phase_level",
  "result": "pass | fail",
  "timestamp": "ISO 8601",
  "spec_version": "spec_vN",
  "spec_fingerprint": "sha256:...",
  "summary": "one-paragraph",
  "criteria_passed": "N",
  "criteria_failed": "N",
  "criteria": [ {"name": "...", "status": "pass|fail", "notes": "..."} ],
  "issues": { "critical": "N", "major": "N", "minor": "N" },
  "fix_tasks_to_create": [
    {
      "task_json": { "...full task JSON shape per task-schema.md..." },
      "out_of_spec": true | false,
      "reason": "why this fix task is needed"
    }
  ],
  "friction_markers": [ "..." ]
}
```

---

## Per-File Change Specs

### File 1: `.claude/agents/implement-agent.md`

**Editing strategy:** Full rewrite via `Write` tool — touches more than a third of the file and restructures multiple sections.

**Sections to keep unchanged:**
- `# Implementation Agent` header
- `**Model: Claude Opus 4.7** (...)` line
- `## Reasoning Effort` section
- `## Purpose` section
- `## Tool Preferences` section
- `## When to Follow This Workflow` section
- `## Inputs` section
- `## How This Workflow Is Invoked` section
- `### Step 1: Select Task`
- `### Step 1b: Validate Task`
- `### Step 2: Understand Task`
- `### Step 4: Implement`
- `### Step 5: Self-Review`
- `## Implementation Guidelines` section (Scope Discipline, Progress Tracking)
- `## Handling Issues` section (Blocking Issues, Non-Blocking Issues, Scope Creep, Decisions Made During Implementation, Spec Misalignment Discovered) — but update language so "document in notes" → "include in report notes/issues_discovered"
- `## Wind-Down Protocol` (update to: return report with `implementation_status: "partial"`)

**Sections to rewrite:**

**`## Outputs` section:** Replace with:
> The agent returns a structured implementation report (see "Structured Report" section below). The orchestrator consumes this report and performs all task-JSON state transitions, friction-marker persistence, and dashboard regeneration. Agents never write to `.claude/` paths — that write class is owned by `/work`.

**`### Step 3: Set In Progress` section:** Replace with:
> The orchestrator sets task status to "In Progress" before dispatching this agent. You do not write this transition yourself. Start implementation assuming the task is already "In Progress" per the orchestrator.

**`### Step 6: Document and Trigger Verification` section + 6a/6b/6c subsections:** Replace entire section with a new `### Step 6: Return Structured Report`:

> After self-review (Step 5), construct and return the structured implementation report per the schema below. Do not attempt to write to `.claude/tasks/`, do not attempt to spawn verify-agent — subagents cannot do either, and the orchestrator handles both.
>
> [Insert Implement-agent report schema from Design Contracts above]
>
> **Completion status values:**
> - `completed` — all work done per spec, ready for verification
> - `partial` — wind-down triggered mid-implementation; orchestrator leaves status as "In Progress" with `[PARTIAL]` notes
> - `blocked` — cannot proceed; orchestrator sets status to "Blocked"
> - `misaligned` — implementation revealed spec conflict; orchestrator handles spec-check conversation
>
> **What the orchestrator does with your report:**
> - For `completed`: sets status to "Awaiting Verification", writes your notes/completion_date, dispatches verify-agent
> - For `partial`: leaves status "In Progress", prepends `[PARTIAL]` to notes, returns control to `/work`
> - For `blocked`: sets status to "Blocked", returns control with your issues_discovered list
> - For `misaligned`: does not advance status, routes to spec-alignment flow
>
> In all cases, the orchestrator appends your `friction_markers` to `.claude/support/workspace/.session-log.jsonl` and regenerates the dashboard (per phase-end policy). You do not perform any of these persistence steps yourself.

**`## Friction Markers` section:** Replace with:

> During implementation, observe workflow deviations, spec drift, informal decisions, scope creep, user feedback signals, or template guidance gaps. Include observations in the `friction_markers` array of your return report. The orchestrator appends each marker to `.claude/support/workspace/.session-log.jsonl`.
>
> **When to emit markers:** [Keep the existing table intact — Event / Marker type / What to capture]
>
> **Marker object shape (within your return report):**
> ```json
> {"type": "workflow_deviation", "timestamp": "2026-04-17T14:30:00Z", "details": "Skipped Step 5 self-review due to trivial change", "template_area": "implement-agent Step 5"}
> ```
> Note: `task_id` is added by the orchestrator from the task dispatched to you — do not include it yourself.
>
> **Rules:** [Keep existing rules, update "Write one JSON line" → "Include in report"]

**`## Handoff Criteria` section:** Update:
> Task is ready for verification when your report declares `implementation_status: "completed"`, includes `notes`, and lists all `files_modified`. The orchestrator performs the actual status transition to "Awaiting Verification" and dispatches verify-agent. Verification pass/fail is the orchestrator's subsequent responsibility.

---

### File 2: `.claude/agents/verify-agent.md`

**Editing strategy:** Full rewrite via `Write` tool — major restructuring of Steps T6, T7, Phase Steps 6, 7.

**Sections to keep unchanged:**
- `# Verification Agent` header
- `**Model:** ...` line
- `## Reasoning Effort` section
- `## Purpose`, `## Verification Modes`, `## Tool Preferences`, `## When to Follow This Workflow`, `## Inputs`, `## How This Workflow Is Invoked`, `## Using the Think Tool`
- `### Step T1: Read Task and Spec Context`
- `### Step T2: Verify File Artifacts` (T2a, T2b, T2c)
- `### Step T3: Verify Spec Alignment`
- `### Step T4: Verify Output Quality and Patterns`
- `### Step T4b: Runtime Validation` (keep check logic, including test_protocol construction — but change the "write to task JSON" language to "include in report")
- `### Step T5: Verify Integration Boundaries`
- Phase-level Steps 1-5 (Gather Context, Run Tests, Validate Against Spec, Manual Verification, Identify Issues)
- `## Separation of Concerns`, `## Handling Ad-Hoc Tasks`, `## Handling Failures`

**Sections to rewrite:**

**`## Outputs` section (both modes):** Replace with:
> **Per-task mode:** returns structured verification report (see schema below). The orchestrator writes `task_verification`, `verification_history`, `test_protocol`, `interaction_hint`, and `user_review_pending` fields to the task JSON and handles status transitions.
>
> **Phase-level mode:** returns structured phase-level verification report including `fix_tasks_to_create[]`. The orchestrator writes `.claude/verification-result.json` and creates fix task JSON files.

**`## Turn Budget Protocol` section:** Replace "Write task_verification" / "Write verification-result.json" language with:
> **Per-task mode (default: 30 turns):** If you reach turn 25 without completing all checks, return your partial report with `result: "fail"` and `notes: "Verification incomplete — N of 7 checks completed before turn limit"`. Checks not yet completed get value `"skipped"`. The orchestrator handles the retry flow.
>
> **Phase-level mode (default: 50 turns):** If you reach turn 43 without completing all criteria, return your partial report with `result: "fail"` and `notes: "Verification incomplete — evaluated N of M criteria"` and a single fix task in `fix_tasks_to_create[]`: "Complete phase-level verification". The orchestrator writes verification-result.json and creates the fix task.

**`## Wind-Down Protocol` section:** Replace with:
> When `/work pause` is triggered during verification, return an empty report with `result: null` and `notes: "Intentional pause — verification not completed"`. The orchestrator leaves task status as "Awaiting Verification" — session recovery Case 1 handles re-spawn. Do not treat intentional pause as a failed attempt (orchestrator does not increment `verification_attempts` for pause-triggered halts).

**`### Step T6: Produce Verification Result`:** Replace entirely with `### Step T6: Construct Verification Report`:
> Construct and return the structured per-task verification report per the schema below. Do NOT write to the task JSON. The orchestrator persists `task_verification`, appends to `verification_history`, increments `verification_attempts`, and performs the status transition.
>
> [Insert per-task schema from Design Contracts]
>
> **Include examples:** pass, pass-with-partial-runtime, fail, minor-scope-violation-passes, major-scope-violation-fails — preserve the existing 5 example shapes but present them as the `task_verification` sub-object within the report envelope.

**`### Step T7: Route Result`:** Replace entirely with `### Step T7: Return Report`:
> Return your verification report to the caller. Do NOT set task status, do NOT write to task JSON, do NOT regenerate dashboard. The orchestrator performs all status transitions, JSON persistence, and dashboard updates based on your report.
>
> **What the orchestrator does with your report:**
> - `result: "pass"`: writes `task_verification`, appends `verification_history`, sets status to "Finished", writes `user_review_pending`/`test_protocol`/`interaction_hint` if present
> - `result: "fail"` (attempts < 3): writes `task_verification`, appends `verification_history`, sets status to "In Progress", prepends `[VERIFICATION FAIL #N]` to notes
> - `result: "fail"` (attempts >= 3): writes `task_verification`, appends `verification_history`, sets status to "Blocked", adds `[VERIFICATION ESCALATED]` note
>
> You do not distinguish retry vs. escalate — that's the orchestrator's responsibility using the report's `attempt_number` and the current task JSON's `verification_attempts`.

**Phase-level `### Step 6: Create Fix Tasks and Update Dashboard`:** Replace with `### Step 6: Identify Fix Tasks`:
> For each major/critical issue found, construct a fix-task entry in the `fix_tasks_to_create[]` array of your report. Do NOT write task JSON files. Do NOT regenerate the dashboard. The orchestrator creates the task files and regenerates the dashboard.
>
> **Fix-task entry shape:**
> ```json
> {
>   "task_json": { "id": "string", "title": "...", "description": "...", "difficulty": N, "owner": "claude", "source": "verify-agent", "status": "Pending", ... },
>   "out_of_spec": true | false,
>   "reason": "why this fix task is needed"
> }
> ```
> **Distinguish:** in-spec bug fixes (`out_of_spec: false`) — the orchestrator routes them automatically to implement-agent via `/work`. Recommendations beyond spec acceptance criteria (`out_of_spec: true`) — the orchestrator queues them for user approval before execution.

**Phase-level `### Step 7: Persist Verification Result`:** Replace with `### Step 7: Include Verification Result in Report`:
> Do NOT write `.claude/verification-result.json`. Include the full verification result payload in your return report (see phase-level schema in Design Contracts). The orchestrator writes the JSON file. Fields `result`, `timestamp`, `spec_version`, `spec_fingerprint`, `summary`, `criteria_passed`, `criteria_failed`, `criteria[]`, `issues`, `tasks_created[]` all flow through your report.

**`## Friction Markers` section:** Same pattern as implement-agent — change "Write one JSON line" → "Include in `friction_markers[]` of your return report. The orchestrator appends each marker to `.claude/support/workspace/.session-log.jsonl`."

**`## Handoff Criteria` section:** Update to reflect report-returning contract.

---

### File 3: `.claude/commands/work.md` — Step 4 additions

**Editing strategy:** Targeted `Edit` calls. Step 4 gains a new "State Persistence Protocol" sub-section; existing sub-sections reference it.

**New sub-section to add (immediately after "#### If Executing" and before "#### If Executing (Parallel)"):**

```markdown
#### State Persistence Protocol

After any agent (implement-agent or verify-agent) returns a structured report, the orchestrator is responsible for all state transitions, JSON persistence, and dashboard updates. Agents cannot write to `.claude/` paths — this is enforced by the Claude Code harness (see DEC-004). Follow this protocol precisely to preserve the atomic implement→verify contract.

**Schemas:** The two agent return schemas are defined in `.claude/agents/implement-agent.md` § "Step 6: Return Structured Report" and `.claude/agents/verify-agent.md` § "Step T6: Construct Verification Report" (per-task) + § "Step 7: Include Verification Result in Report" (phase-level).

**After implement-agent returns:**

1. **Status transition** based on `implementation_status`:
   - `completed`: write `{ "status": "Awaiting Verification", "completion_date": report.completion_date, "updated_date": today, "notes": report.notes }` to task JSON
   - `partial`: leave status "In Progress"; prepend `[PARTIAL]` to notes
   - `blocked`: write `{ "status": "Blocked", "notes": "...", "updated_date": today }`; surface `issues_discovered[]` to user
   - `misaligned`: do not advance status; route to spec-alignment flow with `issues_discovered[]` context

2. **Append friction markers:** for each marker in `report.friction_markers`, add `task_id: report.task_id` and append as a JSON line to `.claude/support/workspace/.session-log.jsonl` (Read existing content, then Write with appended line; if file doesn't exist, create it)

3. **Dashboard regeneration:** in sequential mode, regenerate `dashboard.md` per `.claude/support/reference/dashboard-regeneration.md`. In parallel mode, defer — handled at batch-end.

4. **For `completed` status:** dispatch verify-agent (see "If Verifying (Per-Task)" section) and then apply the "After verify-agent returns" protocol below.

**After verify-agent returns (per-task mode):**

1. **Read task's current `verification_attempts`** (default 0), compute `new_attempts = current + 1`
2. **Build `verification_history` entry** from report's `checks`, `issues`, `notes`, with `{"attempt": new_attempts, "result": report.result, "timestamp": report.timestamp}`. Append to task's `verification_history[]` array (create array if absent).
3. **Write `task_verification`** field to task JSON using report's `result`, `timestamp`, `checks`, `notes`, `issues`
4. **Status transition** based on `result`:
   - `pass`: set `status: "Finished"`, `updated_date: today`. If `report.user_review_pending == true`, also write `user_review_pending: true`, `test_protocol: report.test_protocol`, `interaction_hint: report.interaction_hint`
   - `fail` AND `new_attempts < 3`: set `status: "In Progress"`, `updated_date: today`. Clear `completion_date`. Prepend `[VERIFICATION FAIL #{new_attempts}]` to notes with the fail summary
   - `fail` AND `new_attempts >= 3`: set `status: "Blocked"`, `updated_date: today`. Prepend `[VERIFICATION ESCALATED]` note — "3 attempts exhausted — requires human review"
5. **Timeout detection:** if verify-agent exhausted max_turns without returning a valid report, treat as fail: increment `verification_attempts`, set status to "Blocked", add `[VERIFICATION TIMEOUT]` note
6. **Append friction markers** from `report.friction_markers` (same as implement-agent)
7. **Parent auto-completion:** if task has `parent_task` and all siblings are now "Finished", set parent to "Finished"
8. **Dashboard regeneration:** sequential mode — regenerate now; parallel mode — defer

**After verify-agent returns (phase-level mode):**

1. **Write `.claude/verification-result.json`** using the report's payload: `result`, `timestamp`, `spec_version`, `spec_fingerprint`, `summary`, `criteria_passed`, `criteria_failed`, `criteria`, `issues`, `tasks_created`
2. **Create fix task files:** for each entry in `report.fix_tasks_to_create[]`, write `task_{id}.json` with the entry's `task_json` payload plus `out_of_spec` flag
3. **Append friction markers**
4. **Regenerate dashboard** — include Verification Debt sub-section if debt exists; show out-of-spec tasks with ⚠️ prefix
5. **If result is `fail`:** loop back to Execute phase for fix tasks. If `pass`: proceed to "If Completing"
```

**Update existing sub-section `#### If Executing`:** Replace:
> Read `.claude/agents/implement-agent.md` and follow Steps 1-6. Required artifacts:
>    - Step 1: Task selected (logged)
>    - Step 1b: Validation checks passed
>    - Step 3: Task JSON updated to `"In Progress"` **before any implementation begins**
>    - Step 4: Implementation done
>    - Step 5: Self-review completed
>    - Step 6a: Task JSON updated to `"Awaiting Verification"`
>    - Step 6b: verify-agent **spawned as a separate Task agent** (fresh context)
>    - Step 6c: Inline status update (tier 2) — ...

With:
> **Before dispatch:** orchestrator sets task JSON to `{"status": "In Progress", "updated_date": today}`.
>
> Dispatch implement-agent (Task tool with `model: "opus[1m]"`) instructing it to read `.claude/agents/implement-agent.md` and follow Steps 1-6. Agent returns structured report.
>
> **After agent returns:** apply "After implement-agent returns" from State Persistence Protocol. Then dispatch verify-agent per "If Verifying (Per-Task)" and apply "After verify-agent returns" protocol.

**Update existing sub-section `#### If Executing (Parallel)`:** Replace the "Key rules" block:
> - Each parallel agent reads `implement-agent.md` and runs Steps 2/4/5/6a/6b independently
> - Agents must NOT regenerate dashboard, select next task, or check parent auto-completion
> - After all agents complete: final parent auto-completion, single dashboard regeneration, Step 5

With:
> - Orchestrator sets all batch tasks to "In Progress" before dispatch (see parallel-execution.md § 2)
> - Each parallel implement-agent reads `implement-agent.md` and follows Steps 1-6; returns structured report
> - As each implement-agent report arrives, orchestrator applies "After implement-agent returns" protocol AND dispatches the per-task verify-agent (see parallel-execution.md § 4)
> - As each verify-agent report arrives, orchestrator applies "After verify-agent returns" protocol
> - After all reports processed: final parent auto-completion, single dashboard regeneration, post-dispatch validation (Step 5)

**Update existing sub-section `#### If Verifying (Per-Task)`:** After the Task tool call block, replace "After per-task verification completes:" section with:
> verify-agent returns a structured per-task report. Apply "After verify-agent returns (per-task mode)" from State Persistence Protocol.
>
> **Auto-continuation:** after orchestrator persists verification state:
> - **Pass**: announce inline `Task {id} verified`. If `user_review_pending: true`, check `interaction_hint` for routing. Surface newly-unblocked human/both tasks inline. Loop back to Step 3.
> - **Fail (retry)**: announce inline `Task {id} verification failed: {summary} — routing back to implement-agent`. Route to implement-agent to fix.
> - **Fail (escalated)**: announce inline `Task {id} verification escalated after 3 attempts`. Stop auto-continuation; report to user.

**Update existing sub-section `#### If Verifying (Phase-Level)`:** After the Task tool call block, replace "After phase-level verification completes:" with:
> verify-agent returns a structured phase-level report. Apply "After verify-agent returns (phase-level mode)" from State Persistence Protocol.
>
> | Result | Action |
> |--------|--------|
> | `pass` | Proceed to "If Completing". Present any out-of-spec recommendations for user approval. |
> | `fail` | Fix tasks created by orchestrator. Loop back to Execute, then re-verify when all spec tasks finished. |

---

### File 4: `.claude/support/reference/parallel-execution.md`

**Editing strategy:** Targeted `Edit` calls on sections 3, 4, 5, plus "Write Ownership Rules" table.

**Update `### Write Ownership Rules` table:**

Replace:
| Writer | May write to | Must NOT write to |
|--------|-------------|-------------------|
| Each parallel agent | Its own `task-{id}.json` only | Any other task JSON, parent task JSON, dashboard.md, verification-result.json, dashboard-state.json |
| `/work` orchestrator | Nothing (waits for agents) | Any task JSON file owned by a running agent |

With:
| Writer | May write to | Must NOT write to |
|--------|-------------|-------------------|
| Each parallel agent | Nothing — agents return structured reports only (harness prohibits subagent writes to `.claude/`, per DEC-004) | Any `.claude/` path |
| `/work` orchestrator | All task JSONs, parent task JSONs, dashboard.md, verification-result.json, dashboard-state.json, session-log.jsonl, fix-task JSON files | Nothing — orchestrator is the sole writer in this architecture |

**Update "Key invariants" bullets:**

Replace:
> - **One writer per file:** Each agent writes only to its own task JSON file. No two agents share a task file because each is dispatched for a distinct task.
> - **Parent auto-completion is orchestrator-only:** Agents are instructed "DO NOT check parent auto-completion." The orchestrator performs parent checks sequentially in the collect loop (Step 4), so concurrent writes to a parent task file cannot occur.
> - **Sequential result processing:** When multiple agents complete in the same poll cycle, the orchestrator processes them one at a time (the `For each completed agent` loop is sequential), preventing race conditions on shared state like parent task files.

With:
> - **Single writer:** The orchestrator is the only writer for all `.claude/` state (task JSON, dashboard, verification-result.json, session-log.jsonl). Agents return structured reports; all persistence is mediated.
> - **Sequential result processing:** When multiple agents complete in the same poll cycle, the orchestrator processes them one at a time (the `For each completed agent` loop is sequential). This naturally serializes task-JSON writes, parent auto-completion, and friction-marker appends — no race conditions possible since there's only one writer.
> - **Verify-agent dispatch per implement-agent:** After each implement-agent report is processed, the orchestrator dispatches that task's verify-agent. Verify-agents can run concurrent with subsequent implement-agents, preserving pipeline throughput.

**Update `### 3. Spawn Parallel Agents`:**

Replace the bulleted list describing what each agent receives:
> - The task JSON to execute
> - Instructions to read `.claude/agents/implement-agent.md`
> - Instructions to follow Steps 2, 4, 5, 6a, and 6b (understand, implement, self-review, mark awaiting verification, spawn verify-agent as a sub-agent for per-task verification)
> - **Wind-down instruction:** "TURN BUDGET: You have 40 turns. If you reach turn 35 without completing, stop implementation, update task notes with progress so far, and return your status. Do NOT leave the task in an inconsistent state — either mark Awaiting Verification (if implementation is complete) or leave as In Progress with detailed notes (if not)."
> - **Explicit instruction: "DO NOT regenerate dashboard. DO NOT select next task. DO NOT check parent auto-completion. Return results when verification completes."**
> - **Note:** Each parallel implement-agent will spawn its own verify-agent sub-agent (nested Task call). This is expected — verification separation applies in parallel mode too.

With:
> - The task JSON to execute
> - Instructions to read `.claude/agents/implement-agent.md`
> - Instructions to follow Steps 1-6 (understand, implement, self-review, return structured report)
> - **Wind-down instruction:** "TURN BUDGET: You have 40 turns. If you reach turn 35 without completing, stop implementation and return your report with `implementation_status: 'partial'` and detailed notes. Do NOT attempt writes to `.claude/` — subagents cannot write there; orchestrator handles all persistence from your report."
> - **Explicit instruction:** "Return a structured implementation report per `.claude/agents/implement-agent.md` § Step 6. Do NOT write to task JSON, do NOT spawn verify-agent, do NOT regenerate dashboard — orchestrator owns all state persistence."

**Update `### 4. Collect Results with Incremental Re-Dispatch`:**

Inside the "For each completed agent" block, replace the bullet list:
> 1. Record result (task ID, status, verification result, files modified, issues)
> 2. Remove from active_agents
> 3. Check parent auto-completion for finished tasks
> 4. INCREMENTAL RE-DISPATCH: ...

With:
> 1. **Read implement-agent's return report** (structured schema per implement-agent.md § Step 6)
> 2. **Apply "After implement-agent returns" protocol** from `work.md` § State Persistence Protocol:
>    - Status transition on task JSON per `implementation_status`
>    - Append `friction_markers` to `.claude/support/workspace/.session-log.jsonl`
> 3. **Dispatch verify-agent for this task** (Task tool, `model: "opus[1m]"`, `max_turns: 30`) if `implementation_status == "completed"`. Verify-agent dispatch is individual — one per completed implement-agent, runs concurrent with remaining implement-agents.
> 4. **When verify-agent returns**, apply "After verify-agent returns (per-task mode)" protocol from `work.md` § State Persistence Protocol: write `task_verification`, append `verification_history`, increment `verification_attempts`, transition status, append friction markers, check parent auto-completion
> 5. Remove implement-agent from `active_agents`; track verify-agent in a separate `active_verifiers` map with the same timeout logic
> 6. **INCREMENTAL RE-DISPATCH:** (unchanged — re-run eligibility for held-back tasks)

**Update `### 5. Post-Parallel Cleanup`:**

Add a step between existing steps 1 and 2:
> 1. Wait for all `active_verifiers` to complete or timeout (same timeout logic as implement-agents)
> 2. Final parent auto-completion check
> 3. [existing step about single dashboard regeneration]
> ...

---

### File 5: `system-overview.md`

**Editing strategy:** Grep for the phrases "atomic implement→verify contract", "atomic agent", "agent owns", "agent-owned state", "fresh eyes", "Step 6a", "Step 6b", "verify-agent writes" — then apply surgical `Edit` calls to reframe.

**Key reframes:**

1. The atomic contract is preserved — implement→verify is still atomic in the sense that a task cannot be "Finished" without passing verification. But state ownership moves to the orchestrator.

2. "Fresh eyes" property is preserved — verify-agent still runs in a separate Task context with no implementation memory. The property is about *judgment* separation (fresh context evaluates the work), not about *write* separation.

3. Any descriptions of "implement-agent writes `Awaiting Verification`" should read "orchestrator writes `Awaiting Verification` after implement-agent returns a completed report".

4. Any descriptions of "verify-agent writes `task_verification`" should read "orchestrator writes `task_verification` from verify-agent's structured report".

5. Add a reference to DEC-004 with a 1-line rationale: "State persistence is centralized in the orchestrator because the Claude Code harness prohibits subagent writes to `.claude/` paths (see DEC-004)."

**At minimum, include these edits:**

- Update any architecture diagrams or flowcharts that show agents writing to task JSON — label the write arrow as originating from the orchestrator.
- Update the "Verification Is Structurally Enforced" invariant description (if present) to clarify: "A task cannot reach Finished without `task_verification.result == 'pass'` — the orchestrator writes this field based on verify-agent's returned judgment."

---

### File 6: `.claude/rules/agents.md`

**Editing strategy:** Targeted `Edit` calls on the "Context Separation" and "Tool Preferences" sections.

**Update `## Context Separation`:**

Replace:
> verify-agent always runs as a separate Task agent, never inline in the implementation conversation. This applies to both sequential and parallel execution modes.

With:
> verify-agent always runs as a separate Task agent, dispatched by the `/work` orchestrator — never inline in the implementation conversation. This applies to both sequential and parallel execution modes. "Fresh eyes" is preserved because the verifier evaluates in its own context with no implementation memory; the fact that the orchestrator (not the verify-agent itself) writes the verification result to the task JSON does not affect verification independence. See DEC-004.

**Add a new section `## State Ownership`** after Context Separation:

> All `.claude/` state transitions (task JSON writes, dashboard regeneration, verification-result.json, session-log.jsonl) are owned by the `/work` orchestrator. Subagents (implement-agent, verify-agent, research-agent) return structured reports; they do not write to `.claude/` paths. This is a hard constraint of the Claude Code harness (subagents are sandboxed from `.claude/` writes per Anthropic issue #38806) and is not expected to change. See DEC-004 for the full rationale.

**Tool Preferences section:** add a note:
> Subagents cannot write to `.claude/` paths, cannot spawn nested `Task` tool calls, and do not inherit parent `permissions.allow` rules. When an agent's documented workflow describes a state transition, it means "include in return report"; the orchestrator performs the actual write.

---

## Execution Order

Recommended order (dependencies between files are limited — all 6 can be edited in one session):

1. **Read** DEC-004, tracker, all 6 files' current state
2. **File 1** (implement-agent.md) — full rewrite via `Write`
3. **File 2** (verify-agent.md) — full rewrite via `Write`
4. **File 3** (work.md) — targeted `Edit` calls
5. **File 4** (parallel-execution.md) — targeted `Edit` calls
6. **File 5** (system-overview.md) — grep-driven `Edit` calls
7. **File 6** (rules/agents.md) — targeted `Edit` calls
8. **Verify:** grep for stale "agent writes task", "agent spawns verify-agent", "Step 6a", "Step 6b", "Step 6c" references — all should be gone from subagent-side instructions
9. **Update tracker:** Session Log entry, Current State → next decision or paused
10. **Commit:** see commit message below

---

## Verification Checklist (Post-Execution)

Before commit, confirm:

- [ ] `implement-agent.md` — Steps 3, 6, 6a, 6b, 6c restructured; no `Write`/`Edit`/`Task` tool calls in the agent's own workflow; Return Schema section present with full JSON contract
- [ ] `verify-agent.md` — T6, T7, Phase Steps 6, 7 restructured; no `Write` calls to `task_verification`, `verification_history`, `test_protocol`, `verification-result.json`, fix task JSONs; Return Schema section present (both per-task and phase-level)
- [ ] `work.md` — new State Persistence Protocol sub-section present in Step 4; the 4 existing sub-sections (If Executing, If Executing Parallel, If Verifying Per-Task, If Verifying Phase-Level) reference it
- [ ] `parallel-execution.md` — Write Ownership Rules table updated; Section 3 spawn prompt updated; Section 4 collect loop updated to include verify-agent dispatch per implement-agent
- [ ] `system-overview.md` — atomic contract reframed; state-write arrows point to orchestrator; DEC-004 reference present
- [ ] `rules/agents.md` — Context Separation clarification; new State Ownership section; Tool Preferences note
- [ ] Grep for lingering references: `agent writes task`, `Step 6a`, `Step 6b`, `verify-agent writes`, `spawn verify-agent` (in subagent contexts) — all stale references cleared

---

## Commit Message

```
DEC-004: formalize orchestrator ownership of task state transitions

Per Option B, all task JSON writes, dashboard regeneration, verify-agent dispatch, and verification-result.json writes move from subagents to the /work orchestrator. Subagents (implement-agent, verify-agent) now return structured reports; orchestrator persists state.

Rationale: Claude Code harness prohibits subagent writes to .claude/ paths (#38806) and prevents nested Task tool calls (#4182). The previous docs described an atomic agent-owned contract that never matched runtime. This commit aligns docs with runtime, preserves the atomic implement→verify invariant (no "Finished" without passing verification), and keeps the fresh-eyes property (verify-agent runs in separate context; only the writer changes).

Closes FB-010.

Changes:
- .claude/agents/implement-agent.md: Steps 3/6 restructured as return schema
- .claude/agents/verify-agent.md: T6/T7 + Phase Steps 6/7 restructured as return schema
- .claude/commands/work.md: Step 4 gains State Persistence Protocol sub-section
- .claude/support/reference/parallel-execution.md: write ownership + dispatch flow updated
- system-overview.md: atomic contract reframing, DEC-004 reference added
- .claude/rules/agents.md: Context Separation clarification, new State Ownership section

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Post-Execution Tracker Updates

After successful commit:

1. Update `template-upgrade-2026-04.md`:
   - Add Session Log entry for DEC-004 execution
   - Update Current State → "Phase 1 — DEC-005 next"
   - Mark DEC-004 checkbox in Phase 1 as `[x]` with commit SHA
   - Update File Collision Map: strike through DEC-004 column entries (done)
2. Add this plan file to its own DELETE-AFTER entry in Cleanup Manifest if not already present
