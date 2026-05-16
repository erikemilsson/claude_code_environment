---
id: DEC-011
title: Track 1 / Track 2 pipeline execution — fix tier for marker-append + session-export reliability
status: implemented
category: architecture
created: 2026-05-13
decided: 2026-05-13
implemented: 2026-05-13
related:
  tasks: []
  decisions: [DEC-001]
  feedback: [FB-057]
implementation_anchors:
  - .claude/commands/work.md                           # behavioral nudge ("do NOT defer") + startup catchup + dual-write to .pending-markers.jsonl
  - .claude/support/reference/parallel-execution.md    # parallel-batch mirror of dual-write
  - .claude/hooks/pre-compact-handoff.sh               # catchup at PreCompact reads .pending-markers.jsonl
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# Track 1 / Track 2 pipeline execution — fix tier for marker-append + session-export reliability

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Tier A only — behavioral nudge (tighter wording in `work.md:543` + `parallel-execution.md`)
- [ ] Option B: Tier B only — idempotent catchup (no wording change)
- [ ] Option C: Tier C only — structural PostToolUse / SubagentStop hook (per-project install)
- [ ] Option D: Tier D only — deterministic `.claude/scripts/append-markers.py`
- [ ] Option AB: Hybrid A+B — behavioral nudge + idempotent catchup (recommended)
- [x] Option ABp: Hybrid A+B + `.pending-markers.jsonl` transient buffer (recommended + abrupt-kill protection)
- [ ] Option E: Defer — wait for first downstream session export before deciding

*Check one box above, then fill in the Decision section below.*

---

## Context

DEC-001 Option C (Track 1 friction markers + Track 2 retrospective + Phase 3 ingest) is documented end-to-end across `implement-agent.md`, `verify-agent.md`, `work.md`, `pre-compact-handoff.sh`, and `health-check.md`. But empirical evidence (styler Phase 20 observation 2026-04-27 + DEC-001 Option C audit 2026-05-13) suggests the pipeline isn't reliably executed:

- **Cause 1 (resolved 2026-05-13 by FB-040 Part 5d):** downstream `template_inbox_path` discoverability gap. Closed.
- **Cause 2 (open):** orchestrator-side marker append (`work.md:543`) documented but not reliably executed during `/work` runs. Styler Phase 20: 8 markers batch-appended at pause; abrupt termination would have lost all.
- **Cause 3 (open):** `/work pause` Track 2 + Session Export step not reliably run.

FB-057's tiered fix path:

- **A. Behavioral nudge:** tighter protocol — "append marker via single bash call immediately after agent return; do not batch."
- **B. Idempotent catchup:** orchestrator (or PreCompact hook) auto-appends missing markers detected from task notes.
- **C. Structural hook:** PostAgentReturn / PostToolUse hook gated on Task subagent (un-skippable by the orchestrator).
- **D. Deterministic script:** extract marker-append into a `.claude/scripts/` script (FB-011 Family D/E candidate).

These tiers are not mutually exclusive — a final ship could combine, e.g., B (idempotent catchup) + lightweight A (behavioral nudge). The decision is the right combination.

**Telemetry gate:** currently no downstream project has `template_inbox_path` set, so there's no Track-1 telemetry to inspect yet. (FB-040 Part 5d will surface this in the next downstream `/health-check`.) Research can prepare the option analysis but the final selection waits for empirical evidence from real downstream sessions.

## Questions to Research

*(Answers in `## Research Findings` below.)*

1. What's the current orchestrator-side marker append mechanic in `commands/work.md:543` (and parallel-execution.md mirror)? Is it specified as inline or batched, and does the prose match a reliable execution pattern?
2. Hook-based approaches in Claude Code: does PostToolUse fire after Task subagent completion? Can a hook gate be set on `subagent_type` or model? How would such a hook compose with the existing PreCompact handoff hook in `.claude/hooks/pre-compact-handoff.sh`?
3. Deterministic script approach (FB-011 Family D/E): what would the script's invocation contract be? Pure stdlib? Read-only or write? Idempotent given multiple invocations? Where would it live in the orchestrator's workflow?
4. What's the cost of each tier — how much template-side change, how much downstream-side change, what new failure modes does each introduce?
5. Is there a way to detect that markers are *missing* (the canonical state — what *should* be in `.session-log.jsonl` — derived from agent reports) so an idempotent catchup is even possible?
6. Could the lightweight tier (behavioral nudge) succeed under Opus 4.7's stronger instruction following alone? Is there a way to A/B-test this against current behavior without burning real downstream sessions?
7. What does the styler Phase 20 evidence specifically reveal about WHY the orchestrator skipped the append step? Was it Claude prioritizing user-facing communication, was it a misread of the procedure, or a context-pressure forgetting?
8. Are there other Track 1 / Track 2 pipeline parts that have the same execution-skip risk (e.g., `/work pause` Session Export step), or is the marker-append step a uniquely-skippable case?

## Options Comparison

Criteria scored qualitatively (✓✓ strong / ✓ moderate / – neutral / ✗ weak / ✗✗ blocking concern). The four tiers (A–D) are evaluated standalone; two hybrid combinations (A+B, B+C) are also assessed because FB-057 explicitly invites combination.

| Criterion | A — Behavioral nudge | B — Idempotent catchup | C — Structural hook | D — Deterministic script | A+B (lightweight + safety net) | B+C (catchup + hook) |
|---|---|---|---|---|---|---|
| **Template-side change cost** | ✓✓ tiny (one paragraph in `work.md`) | ✓ moderate (catchup procedure in orchestrator + hook update) | ✗ large (new hook + settings.local.json change for every project) | ✓ moderate (one Python file + invocation) | ✓ moderate | ✗ large |
| **Downstream-side change cost** | ✓✓ zero | ✓✓ zero | ✗✗ requires per-project `settings.local.json` install (template-owned settings.json forbids hooks) | ✓ zero if invoked by orchestrator; ✗ if user must install | ✓✓ zero | ✗✗ per-project install required |
| **Reliability under context pressure** | ✗ same failure mode as today — LLM may still skip under load | ✓ catches the skip at the next /work or pre-compact gate | ✓✓ un-skippable (runs outside the model's loop) | ✓ deterministic when invoked; ✗ invocation still LLM-gated | ✓ skip is caught within the same session | ✓✓ hook fires + catchup as backstop |
| **Reliability under abrupt termination** | ✗ markers lost between agent return and pause | ✗ catchup runs on next /work or pre-compact only — sudden process kill before either still loses markers | ✓✓ runs synchronously on each Task tool return — captures markers within the same poll cycle | ✗ same as A — only as reliable as the orchestrator's invocation discipline | ✓ catchup runs at pre-compact (hook fires automatically) | ✓✓ best of both |
| **Failure-mode introduced** | – none new | ✓ duplicate-marker risk if dedup key wrong (mitigable with timestamp+task_id+details hash) | ✗ hook script bug = silent failure; settings layering complexity (`settings.local.json` only per DEC-005/8) | ✓ script bug = silent miss but easier to debug; dependency on Python (already present per FB-011 Family A/B) | ✓ same as B alone | ✗ compounds hook + script complexity |
| **Composability with PreCompact hook** | – orthogonal | ✓✓ catchup logic lives next to the existing PreCompact handoff — natural shared module | ✓ separate hook event (PostToolUse) but coexists fine | – orthogonal | ✓✓ same as B | ✓ two hooks acceptable |
| **Telemetry gate sensitivity** | ✗ cannot validate effect without real markers reaching the inbox | ✓ effect is observable (catchup count in PreCompact export logs) | ✓ effect observable but requires per-project hook install before telemetry flows | ✓ deterministic — easy to test offline | ✓ observable | ✓ observable |
| **Opus 4.7 instruction-following sufficiency** | ⚠ **unresolvable without empirical evidence** — see Q6 finding | – not affected | – not affected | – not affected | – partial answer ('B' covers any A residual) | – not affected |
| **Reversibility** | ✓✓ trivial — revert one paragraph | ✓ revert catchup function | ✗ users must remove from settings.local.json | ✓ delete script, revert orchestrator invocation | ✓ revert both | ✗ revert both, plus user setting cleanup |
| **Implementation effort (P-50 estimate)** | < 1 hour | 1–3 hours | 4–8 hours (hook + tests + per-project install docs) | 2–4 hours | 1–3 hours | 6–10 hours |

**Recommended for serious consideration:** A+B (lightweight + safety net). C is structurally strongest but blocked by the template-owned `settings.json` invariant and the harness bug (gh #34692) that PostToolUse may not fire for subagent-internal calls. D is redundant with A+B for this specific concern.

## Option Details

### Tier A — Behavioral nudge

**Description.** Tighten the marker-append protocol in `commands/work.md:543` and the parallel-execution mirror (`parallel-execution.md:285,306`). Explicitly forbid batching: "Append marker via single Edit/Bash call immediately after each agent return; do not defer to `/work pause`. If the session ends abruptly before append, those markers are permanently lost." Possibly add a friction-marker-of-its-own (type `template_gap`, details: "orchestrator deferred marker append") so a deferred append is itself a signal.

**Strengths.**
- Smallest possible diff; reversible in one edit.
- No downstream change required.
- Composes with every other tier (can be A-alone, A+B, or A+anything).
- Aligns with Opus 4.7's stronger instruction following (vs Sonnet baseline).

**Weaknesses.**
- Same failure mode as today — under context pressure or when prioritizing user-facing communication, the orchestrator may still skip the step. The styler Phase 20 observation (`feedback-archive.md:551`) shows this is exactly what happened: 8 markers batched at `/work pause` instead of appended inline.
- No safety net if the session terminates between agent return and pause.
- Effectiveness is empirically unverifiable without real downstream sessions — see Q6.

**Research notes.** This is the cheapest fix and a precondition for A+B. The honest assessment is that the FB-057 evidence (styler Phase 20) shows the *current* protocol failed in execution — the prose was already there. Whether tightening the wording fixes it depends entirely on whether the prior skip was "underspecified procedure" (a wording problem) or "context-pressure deprioritization" (a structural problem). Opus 4.7's interleaved thinking marginally improves the wording-problem case but does not address the structural one.

### Tier B — Idempotent catchup

**Description.** Add a catchup procedure that compares the canonical state (markers in agent return reports, recorded in task notes or `verification_history`) against the actual `.session-log.jsonl` content. Any markers present in task notes but absent from the session log get appended. Idempotency key: `(task_id, timestamp, type, details_hash)`.

Two natural invocation points:
1. **Inside `/work`** — at the top of each `/work` invocation, before any agent dispatch, reconcile any missing markers from prior agent reports (e.g., a styler-Phase-20-style batch sits in task notes; next `/work` autocompletes them).
2. **Inside the PreCompact hook** — extend `hooks/pre-compact-handoff.sh` to do the same reconciliation before compiling the markers-only export. This catches sessions where `/work pause` was never run.

**Strengths.**
- Zero downstream change — orchestrator + existing hook host the logic.
- Composes naturally with PreCompact (same file, same Python entry point).
- Idempotent — safe to re-run; deduplicate by composite key.
- Observable — log "Appended N catchup markers" to stderr or `.handoff.json`.
- Does NOT require a separate `.claude/scripts/` script — can live inline in `pre-compact-handoff.sh` and as inline procedure in `work.md`.

**Weaknesses.**
- Detection requires task-note markers to survive. Implementation-agent reports include `friction_markers[]`, and the orchestrator currently writes the notes field of the task JSON. The current flow doesn't explicitly persist markers in a recoverable form *outside* `.session-log.jsonl` — so catchup needs either (a) marker copies in task notes, or (b) a transient `.pending-markers.jsonl` file the orchestrator writes alongside notes.
- Catchup runs on the *next* `/work` or PreCompact — if the process is killed without either firing (rare but possible), markers are still lost.
- Duplicate-marker risk if dedup key is wrong (mitigable).

**Research notes.** Currently `work.md:543` says markers go to `.session-log.jsonl` and notes via `notes: report.notes`. The agent's `friction_markers[]` are appended to the session log directly — they are NOT visible in task notes by default. For catchup to work, we need to add a small change: either (a) the orchestrator dual-writes markers to task notes (or a pending-markers file) before final session-log append, or (b) the catchup looks at `verification_history` entries that already serialize the agent reports. The second is cheaper but requires structural change to how verification history is composed. Recommend (a): write to a transient `.pending-markers.jsonl` first, then merge into `.session-log.jsonl`.

### Tier C — Structural hook (PostToolUse / SubagentStop)

**Description.** Move marker-append into a Claude Code hook that fires when a Task subagent completes, capturing the return text and appending markers automatically. Candidate events:
- `PostToolUse` with `matcher: "Task"` — fires when the Task tool returns to the main session, with `tool_response` containing the subagent's output text.
- `SubagentStop` with `matcher: "general-purpose"` — fires when the subagent finishes.

**Strengths.**
- Un-skippable by the orchestrator (runs outside Claude's loop).
- Captures markers synchronously on each agent return, so abrupt termination after the *next* tool call still has those markers logged.
- Cleanly separates "produce report" (LLM) from "persist marker" (deterministic).

**Weaknesses.**
- **Settings layering invariant (DEC-005 / DEC-008).** Template-owned `.claude/settings.json` ships only `permissions.allow`. Hooks must go in `.claude/settings.local.json`, which is user-owned. The template can SHIP a hook script (`.claude/hooks/post-task-marker-append.sh`) but CANNOT auto-wire it into settings — each project must opt in via `setup-checklist.md`.
- **`SubagentStop` doesn't include the agent's output text** in stdin (only `agent_id`, `agent_type`, `effort.level`). To capture markers, the hook would need to read the transcript file (`transcript_path` in stdin), parse the agent return, and extract markers. This is fragile.
- **`PostToolUse` on `Task` — output schema undocumented for `tool_response`**. Whether `tool_response` includes the subagent's return text is not documented (Anthropic docs only show `tool_response` examples for `ExitPlanMode`). Implementation requires empirical probing.
- **GitHub #34692 (open bug, Mar 2026):** "PreToolUse/PostToolUse hooks do not fire for tool calls made by subagents." For our purpose (orchestrator-side hook on the main-thread Task tool), this is fine — the orchestrator's Task call IS a main-session tool use, so `PostToolUse` should fire. But this bug indicates the hook semantics around subagents are still unstable and may shift.
- Settings-install friction: every downstream project must install the hook into its local settings to benefit. This compounds the FB-040 discoverability gap (which we just resolved).
- Slowest reversal path — users must remove from `settings.local.json`.

**Research notes.** Hook system supports `SubagentStop` with matcher on `agent_type` (literal exact match or `|`-separated list, or regex if special chars). PostToolUse supports matcher on `tool_name`. Both can return exit code 2 to block (not useful here) or write to additional logs. Hook scripts run as shell subprocesses with stdin JSON — `python3` is already used by `pre-compact-handoff.sh` so adding another hook in the same idiom is straightforward. The blocker is settings layering + the unclear `tool_response` schema, not hook capability itself.

### Tier D — Deterministic script

**Description.** Extract marker-append into `.claude/scripts/append-markers.py`. Orchestrator invokes via Bash after each agent return: `python3 .claude/scripts/append-markers.py --task-id N --markers '[...]'`. Script handles dedup and atomic append.

**Strengths.**
- Deterministic when invoked — no formatting drift, no race conditions.
- Composable with FB-011 Family A/B/D scripts that already live in `.claude/scripts/`.
- Easier to unit-test than inline prose procedure.

**Weaknesses.**
- **Invocation is still LLM-gated.** The orchestrator must remember to call the script — same failure mode as Tier A.
- For this specific concern (the orchestrator skipping the step), the script doesn't solve the problem; it just makes the skipped step a one-line bash call instead of a Read+Write pair. Per `scripts-candidates.md` Tier 3 guidance, scripts should be extracted on observed need — here the need is reliability of invocation, which a script doesn't fix.
- Adds maintenance surface for a step that's currently 2 lines of prose.

**Research notes.** Per `scripts-candidates.md:170`, Family D and E are explicitly "extract on observed need." Marker-append is technically not in Family D (parallel-plan) or E (decision auto-finalization) — it would be a new family (call it F: marker pipeline). The recommendation in `scripts-candidates.md` is that scripts solve *determinism* and *cognitive load*; they do not solve *invocation discipline*. For this concern, A+B addresses invocation discipline (via catchup) without adding a script.

### Hybrid A+B — Behavioral nudge + Idempotent catchup [RECOMMENDED for ship-now]

**Description.** Combine (a) the tightened wording in `work.md` and `parallel-execution.md`, and (b) the catchup procedure inline in `/work` opening + extended in `pre-compact-handoff.sh`.

**Strengths.**
- Cheapest viable safety net. A handles the happy path; B handles the skip-under-load path.
- Both pieces are zero-downstream-change.
- Reversibility preserved (each piece independently revertible).
- Catchup observability lets us empirically diagnose whether A alone would have sufficed (if catchup count is consistently 0, A is working).

**Weaknesses.**
- Still does not protect against abrupt process kill before either `/work` or PreCompact runs. The catchup happens at the *next* gate, not in-line. For sessions that hit a hard process kill mid-batch (rare), the markers between last task notes write and the kill are still lost. (Mitigation: have the orchestrator dual-write markers to a `.pending-markers.jsonl` immediately after agent return; PreCompact / next /work merge into `.session-log.jsonl`. This narrows the loss window to the time between agent return and dual-write — sub-second.)
- Marginally more code than A alone.

**Research notes.** Recommended ship target given the constraints: zero downstream change, settings-invariant-respecting, observable, reversible. The "abrupt kill" residual risk is small — the styler Phase 20 case wasn't an abrupt kill; it was orchestrator deferral. A+B addresses the actual observed failure mode.

### Hybrid B+C

**Description.** Idempotent catchup AND PostToolUse/SubagentStop hook. Hook handles happy path; catchup handles cases where hook didn't fire (e.g., user hasn't installed the hook in `settings.local.json` yet, or the hook errored out).

**Strengths.**
- Maximum reliability — un-skippable hook + idempotent reconciliation.
- Defense in depth.

**Weaknesses.**
- Compound complexity: two implementations of the same logic.
- Per-project hook install required (template invariant — see Tier C).
- The marginal reliability over A+B is small relative to the marginal cost. For a lightweight pipeline like this, A+B is the right rigor level.

**Research notes.** Worth considering ONLY if A+B telemetry shows persistent gaps after a trial period.

## Recommendation

**Recommended ship target: Hybrid A+B (behavioral nudge + idempotent catchup), with an optional `.pending-markers.jsonl` transient buffer for sub-second loss-window protection.**

**Telemetry gate.** Final selection is gated on real downstream telemetry — currently blocked because no downstream project has `template_inbox_path` set (FB-040 Part 5d will surface this in the next downstream `/health-check`). Until at least one downstream project produces session exports, we cannot empirically evaluate:
- Whether the styler Phase 20 case is representative or a one-off
- Whether Opus 4.7's instruction following alone (Tier A solo) would close the gap
- How frequently the catchup branch in Tier B actually fires (if zero across multiple sessions, Tier A alone is sufficient and B is overhead)

**Why A+B over the alternatives:**
1. **A alone** — would be the right answer IF Opus 4.7's stronger instruction following is sufficient; we have zero evidence either way (Q6 is genuinely unresolvable a priori). Ship A unconditionally; it's reversible and a precondition for B.
2. **C alone** — structurally strongest but violates the template-owned `settings.json` invariant (hooks must go in `settings.local.json`, which is user-owned). Forces per-project install friction, regressing the FB-040 discoverability work. Also has unresolved schema unknowns (`tool_response` for Task tool) and intersects with the gh#34692 hook-subagent bug, both indicating hook semantics here are not yet stable.
3. **D alone** — does not solve the actual problem (the orchestrator skipping the step). Script extraction is appropriate for *determinism*, not *invocation discipline*.
4. **B alone** — covers the failure mode but the prose stays the same; users get the same skip behavior, just papered over by catchup. Better paired with A (tightened prose).

**Ship-now vs wait-for-telemetry:**
- The lightweight Tier A wording change is a strict improvement; ship it now (it costs almost nothing and is reversible).
- Tier B (catchup) is the meaningful safety net; ship it now too IF the user is comfortable with no empirical pre-validation. Otherwise wait one downstream session.
- The `.pending-markers.jsonl` transient buffer is optional polish — defer until B's catchup logs show a non-zero kill-window loss case.

**Decision-record-level recommendation: ship A+B as the canonical pipeline; revisit C or D only if A+B telemetry shows catchup firing consistently (would suggest A is failing more often than tolerable, motivating a structural escalation).**

## Research Findings

### Q1: Current orchestrator-side marker append in `commands/work.md:543` and `parallel-execution.md` mirror

`commands/work.md:543` (in the "After implement-agent returns" protocol):

> "Append friction markers: for each marker in `report.friction_markers`, add `task_id: report.task_id` and append as a JSON line to `.claude/support/workspace/.session-log.jsonl` (Read existing content, then Write with appended line; if file doesn't exist, create it)"

The mirror in `parallel-execution.md:285,306` is similar inside the parallel collection loop ("Append friction_markers to .claude/support/workspace/.session-log.jsonl").

**Inline vs batched: prose specifies inline, but the protocol describes a Read+Write pair which is ambiguous about timing.** Nothing in the wording explicitly forbids batching, and the implicit "Append immediately after agent return" intent is not stated. The styler Phase 20 observation (`feedback-archive.md:551`) is exactly this gap — the orchestrator deferred to `/work pause`, where it batch-appended 8 markers in one shot.

**Reliable execution pattern would require:**
- Explicit "do not defer" wording
- Possibly an inline call-out: "Append BEFORE dispatching verify-agent — markers must be persisted before the next blocking call"
- The current procedure does not state these. A Tier A fix addresses exactly this gap.

### Q2: Claude Code hook semantics — PostToolUse, SubagentStop, PreCompact composition

**PostToolUse** fires after any tool call on the main session and supports a `matcher` filter on `tool_name`. Matcher value `"Task"` (only letters) is interpreted as an exact string match. Stdin includes `tool_name`, `tool_input`, `tool_response`, `tool_use_id`, plus common fields (`session_id`, `cwd`, `hook_event_name`). However the `tool_response` schema for the `Task` tool is undocumented — Anthropic docs only show examples for `ExitPlanMode` ("approved plan, plus internal status flags"). Whether `tool_response` contains the subagent's structured return is unverified; empirical probing required.

**SubagentStop** is a dedicated event for subagent completion. Matcher filters on `agent_type` (e.g., `"general-purpose"`). Stdin includes `agent_id`, `agent_type`, `effort.level`, but **does NOT include the subagent's return output** — to capture marker content, the hook would need to read the transcript file (`transcript_path`) and parse it.

**Critical caveat (GitHub anthropics/claude-code#34692, open as of March 2026):** "PreToolUse/PostToolUse hooks do not fire for tool calls made by subagents." For our use case (orchestrator-side hook on the main-thread Task call), this is OK — the Task call is a main-session tool use, so PostToolUse should fire. But it signals hook semantics here are in flux.

**Composition with PreCompact hook (`.claude/hooks/pre-compact-handoff.sh`):** Adding a PostToolUse hook in the same Python idiom is straightforward — both write to the workspace, both read JSON from stdin. They are orthogonal events and coexist fine. The hooks are configured in `.claude/settings.local.json` (per DEC-005/DEC-008), not the template-owned `.claude/settings.json`.

**Hook gating possibility:** Yes — both matchers support exact-string or regex match on subagent_type / tool_name. So a hook gated on `subagent_type: "general-purpose"` (which is what `/work` spawns per `work.md:606`) is supported.

Sources: [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks); [GitHub anthropics/claude-code#34692](https://github.com/anthropics/claude-code/issues/34692).

### Q3: Deterministic script approach (FB-011 Family D/E + a new "Family F")

`scripts-candidates.md:175-211` defines the script invocation contract:
- **Home:** `.claude/scripts/`
- **Dependencies:** Python stdlib only — no `pip install` required
- **I/O:** read-only by default; writes must be orchestrator-invoked, documented, opt-in
- **Stdout:** machine-parseable (JSON or newline-delimited)
- **Stderr:** human-readable diagnostics
- **Exit code:** 0 success, 1 validation failure, 2 runtime error

Marker append is not in Family D (parallel-plan) or E (decision auto-finalization). It would be a new **Family F: marker pipeline**. Shape would be `.claude/scripts/append-markers.py` — reads `--task-id` and `--markers '[...]'` args, deduplicates against existing entries (composite key: `task_id + timestamp + type + details_hash`), atomically appends to `.session-log.jsonl`. Read-write (writes to workspace, not `.claude/`-rooted state — workspace files are mutable).

**Workflow placement:** Called by the orchestrator immediately after each agent return, replacing the inline Read+Write pair in `work.md:543`. Idempotent across invocations.

**Critical assessment:** This solves *determinism* and *atomicity*, but not *invocation reliability*. The orchestrator still has to remember to call the script. Per `scripts-candidates.md:170`, the Family D/E gate is "observed need" — here the observed need is reliability of execution, which a script doesn't address. Recommend against extracting unless A+B telemetry shows persistent issues.

### Q4: Cost of each tier

| Tier | Template change | Downstream change | New failure modes |
|---|---|---|---|
| A | 1 paragraph in `work.md` + 1 paragraph in `parallel-execution.md` | none | none (no new code) |
| B | 1 procedure in `/work` opening + ~30 lines in `pre-compact-handoff.sh` | none | duplicate-marker (mitigated by composite-key dedup) |
| C | new hook script + entry in `setup-checklist.md` | per-project install in `.claude/settings.local.json` | settings-layering complexity; hook errors silent; per-project drift; hook semantics may shift (gh#34692) |
| D | new `.claude/scripts/append-markers.py` + invocation change in `work.md` | none | dependency on Python (already required for Family A/B); same invocation-discipline failure mode as today |
| A+B | A + B above | none | B's dedup risk only |
| B+C | B + C above | per-project hook install | compound of B and C |

**Settings invariant constraint (Tier C):** `.claude/CLAUDE.md § Critical Invariants` enforces: "Settings layering: `.claude/settings.json` is template-owned (base `permissions.allow` only); put hooks, env vars, theme, and any additional permissions in `.claude/settings.local.json`." Tier C cannot be template-default — every downstream project must opt-in.

### Q5: Can we detect missing markers (canonical state derivation)?

**Yes, conditionally.** The canonical state is each agent return report's `friction_markers[]` array. The orchestrator currently:
1. Receives the report
2. Should append markers to `.session-log.jsonl` (the failure point)
3. Writes `notes` field to task JSON
4. Writes `task_verification` field including `verification_history[]` entries

The `friction_markers[]` from the return report are NOT currently persisted *anywhere* outside `.session-log.jsonl`. So if step 2 is skipped, the markers are only in the orchestrator's transient conversation context — lost on compaction.

**For catchup to work**, we need one of:
- **(a)** Dual-write markers to a transient buffer (`.pending-markers.jsonl`) immediately at agent-return time, before the next blocking action. Then catchup compares pending vs session-log.
- **(b)** Include `friction_markers` in the structured `verification_history` entries (which already get written to task JSON). Then catchup walks all `verification_history` entries and reconciles.
- **(c)** Embed marker JSON in task `notes` (semi-structured). Catchup parses notes. Fragile.

**Recommendation:** Option (a) — `.pending-markers.jsonl`. Simplest, most idempotent, least invasive to existing schemas. The orchestrator writes the marker to both files (or just `.pending-markers.jsonl` if the main write fails). Catchup is a one-pass merge.

### Q6: Could Tier A alone succeed under Opus 4.7's stronger instruction-following?

**This is genuinely unresolvable without empirical evidence.**

What we know:
- Opus 4.7 has documented stronger instruction following than Sonnet baselines (per Anthropic model card guidance; also reflected in this template's `.claude/CLAUDE.md` mandating Opus 4.7 for all agents).
- The styler Phase 20 case (`feedback-archive.md:551`) WAS Opus 4.7 (this template requires it). So at least one Opus 4.7 run did skip. That's n=1.
- We do not know whether the styler skip was (a) prompt-underspecification (Tier A wording would have helped) or (b) contextual deprioritization (Tier A wording would NOT have helped — the orchestrator was prioritizing user-facing communication per the FB-045 observation).

**There is no a-priori way to answer this without burning a real downstream session.** Acceptable mitigations:
- **Ship A+B together** — A handles the happy path; if A solves the problem, B's catchup count stays at 0 (cheap observability).
- **Ship A alone, defer B** — only if comfortable with the risk that the same case recurs and the markers are silently lost again.
- **A/B test against current behavior** — not feasible without controlled environments. Real-world `/work` sessions are too variable.

**Recommendation:** Ship A+B together. The catchup count (in `pre-compact-handoff.sh` stderr or `.handoff.json` annotation) IS the A/B test — across a few sessions, catchup count = 0 means A is working; non-zero means A alone wouldn't have been enough.

### Q7: Styler Phase 20 evidence — WHY did the orchestrator skip the append step?

From `feedback-archive.md:551`:
> "the orchestrator (Claude Code, executing /work in auto mode) skipped this step throughout the session — friction markers from agent reports were captured in task notes (task-XXX.json) but NOT appended to .session-log.jsonl in real-time. At /work pause time, the orchestrator caught up and batch-appended 8 markers from the session."

And `feedback-archive.md:561`:
> "This is partly a behavioral nudge for the orchestrator — the 'skip' was a judgment call to focus on user-facing communication, with the cost being post-hoc reconstruction at pause time."

**Diagnosis: contextual deprioritization, not misread of procedure.** The orchestrator understood the step existed (proven by the eventual batch append at pause time) but judged that inline user-facing communication was higher value than persisting markers immediately. This is the "judgment call" case — Tier A's tighter wording ("do not defer; markers must be persisted within the same step") would address it IF the orchestrator weighs the imperative wording above the user-communication imperative. Whether it does is empirically unknowable a-priori.

**Note:** This is NOT a context-pressure forgetting case — context was healthy enough to remember the procedure at pause time. It's a deprioritization case, which is exactly what Tier A is designed for. So the FB-057 evidence is genuinely a positive signal for A.

### Q8: Other Track 1 / Track 2 pipeline parts with execution-skip risk

Audit of `/work pause` flow (`work.md:932-998`):

1. **Track 2 Interaction Assessment write (`work.md:944-961`)** — same skip risk. Writes `.interaction-assessment.json` based on conversation context. If `/work pause` itself is skipped or context-pressured, this write doesn't happen. Catchup is impossible (it depends on conversation context that's lost).
2. **Session Export compile (`work.md:970-994`)** — same skip risk. Reads markers + assessment, writes export, copies to inbox. The PreCompact hook (`pre-compact-handoff.sh:138-208`) already provides a markers-only fallback for this exact case (`export_quality: "markers_only"`).
3. **`template_inbox_path` copy (`work.md:996-997`)** — gated on configuration; not a skip-risk in itself, but discoverability resolved by FB-040 Part 5d.

**Marker-append is NOT uniquely skippable** — `/work pause` Track 2 write has the same risk profile. However, marker-append is the most-frequently-invoked step (fires per agent return, ~once per task), so its loss is amplified.

**Implication:** If Tier B catchup ships, it should also handle Track 2 partial-state cases gracefully — at minimum, document that PreCompact fallback to `markers_only` is the canonical degraded-mode for missed `/work pause`. Currently `pre-compact-handoff.sh:182-194` already does this. Track 2 itself can never be fully reconstructed by catchup (requires conversation context), so the PreCompact fallback is the right design.

**Conclusion:** Marker-append is the highest-frequency skip-risk surface; Tier A+B addresses it cleanly. The `/work pause` Session Export step has the same risk but is partially mitigated by the existing PreCompact fallback. No new tier needed for Track 2 — its design already accepts the lossy fallback.

---

**Sources:**
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [GitHub anthropics/claude-code#34692 — PreToolUse/PostToolUse hooks do not fire for subagent tool calls](https://github.com/anthropics/claude-code/issues/34692)
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/commands/work.md:543,932-998`
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/agents/implement-agent.md:142-149,235-260`
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/agents/verify-agent.md:335,679-694`
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/hooks/pre-compact-handoff.sh:138-208`
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/support/reference/parallel-execution.md:285,306`
- `/Users/erikemilsson/Developer/claude_code_environment/template-maintenance/feedback-archive.md:504-563` (FB-041 + FB-045 source observations)
- `/Users/erikemilsson/Developer/claude_code_environment/template-maintenance/feedback.md:78-110` (FB-057)
- `/Users/erikemilsson/Developer/claude_code_environment/template-maintenance/scripts-candidates.md:114-211` (Family D/E + invocation contract)
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/CLAUDE.md § Critical Invariants` (settings-layering invariant)
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/commands/health-check.md:695-735` (Part 7 downstream telemetry consumer)

## Your Notes & Constraints

*(user notes go here)*
