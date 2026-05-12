---
id: DEC-010
title: partial_completion envelope — schema and threshold for usage-limit graceful resume
status: draft
category: architecture
created: 2026-05-13
decided:
related:
  tasks: []
  decisions: [DEC-004]
  feedback: [FB-049]
implementation_anchors: []
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# partial_completion envelope — schema and threshold for usage-limit graceful resume

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Minimal envelope — three fields, implement-only, in-handoff
- [ ] Option B: Full envelope — five fields + integrity hash, implement-only, dedicated sidecar
- [ ] Option C: Middle path — four fields, implement-only, in-handoff (recommended)
- [ ] Option D: Symmetric envelope — Option C + matching verify-agent contract
- [ ] Option E: Defer — rely on SDK `error_max_turns` + existing `[PARTIAL]` notes; do nothing template-side

*Check one box above, then fill in the Decision section below.*

---

## Context

Anthropic usage-limit cuts mid-implement-agent or mid-verify-agent are recurring. Two cases in a single styler Phase 20 session (2026-04-27): T433's first dispatch was cut at 41 tool uses with no structured report; T454's verify-agent dispatch never even started before the limit hit. Current handoff is via free-form task notes + dashboard prose + `.last-clean-exit.json` — entirely manual. Subsequent invocations have to audit partial work by reading git diff + task notes, costing ~10-15 minutes of audit overhead per case.

FB-049 proposes a `partial_completion` envelope that implement-agent fills when sensing usage-limit approach with unfinished sub-targets. Orchestrator persists to task JSON; next dispatch brokers a "resume from where you stopped" prompt instead of re-deriving context from git diff.

Multiple design questions remain unresolved:

1. **Envelope minimality:** What fields are strictly necessary vs nice-to-have? Token budget for the envelope matters — every field the agent fills costs context.
2. **Detection threshold:** FB-049 proposes "tool_uses > 75% of typical session budget AND remaining sub-targets > 0." But 75% is arbitrary and depends on `max_turns` (40 default for implement, 25-30 for verify). Per-agent threshold or unified?
3. **verify-agent symmetry:** Should verify-agent get a matching envelope (`partial_verification_pending`), or is its work atomic enough that a graceful-cut behavior would be more confusing than useful?
4. **.handoff.json schema impact:** Should the existing handoff schema absorb task-level partial state, or should a separate per-task `task-{id}.partial.json` file hold it?
5. **Re-dispatch context contract:** When the orchestrator re-dispatches a task with a `partial_completion` envelope, what's the exact prompt shape? "Resume from {completed_subtargets}" — but how does the implement-agent verify the previous attempt's edits didn't corrupt state?

## Questions to Research

*(Answers in `## Research Findings` below.)*

1. What does the Anthropic API signal when approaching usage limits? Is there an in-band hint the agent can use, or does the agent have to estimate from `tool_uses` count alone?
2. What does the current implement-agent return schema (`.claude/agents/implement-agent.md` § Step 6) cost in tokens? Adding a `partial_completion` envelope with N fields adds how much?
3. Are there existing precedents in the template (or other agent frameworks the user has integrated) for partial-completion / structured-resume contracts? What fields proved necessary vs decorative?
4. How does a `partial_completion` flow interact with verify-agent? If implement-agent returns `partial_resume_pending`, does verify-agent never run, or does it run on the partial state?
5. What's the right unit for "remaining work" — sub-targets (named work items within the task), file-level (which files still need edits), or step-level (Step 4 done, Step 5 partial)?
6. How does the orchestrator detect that a re-dispatched task's prior edits are still intact (not rolled back, no merge conflicts)? Does the envelope need a `prior_attempt_files_hash` field?
7. What's the failure mode if the partial envelope is wrong (e.g., agent says `completed_subtargets: [A, B]` but B was actually only half-done)? How is this guarded?
8. Should the envelope have a `confidence` field (high/moderate/low) like research-agent's recommendation, to surface uncertainty to the next dispatch?

## Options Comparison

| Criteria | A: Minimal (3 fields) | B: Full (5+hash, sidecar) | C: Middle (4 fields, handoff) | D: Symmetric (C + verify) | E: Defer |
|----------|:---:|:---:|:---:|:---:|:---:|
| Solves observed pain (10-15 min audit/incident) | Partial | Yes | Yes | Yes | No |
| Envelope output-token cost (per partial return) | ~80 tok | ~300 tok | ~150 tok | ~150 tok (impl) + ~80 (verify) | 0 |
| Detection signal available to agent | tool_uses count only | tool_uses count only | tool_uses count + SDK wrap-up | tool_uses + wrap-up | n/a |
| New file types in `.claude/` | None | One (`.partial-{id}.json`) | None | None | None |
| Re-dispatch context fidelity | Notes-grade | Schema-grade + integrity verifiable | Schema-grade | Schema-grade (both legs) | Notes + git diff |
| verify-agent symmetry | No | No | No | Yes | n/a |
| Risk of envelope being wrong (false-complete) | High | Low (hash gates resume) | Medium (orchestrator audits diff vs claims) | Medium | Low (no claim made) |
| Schema churn elsewhere | implement-agent only | implement-agent + work.md + new schema doc | implement-agent + work.md + context-transitions.md | + verify-agent | None |
| Confidence-of-recovery surfaced to user | No | Yes (`confidence` field) | Yes (`confidence` field) | Yes | No |
| Failure mode if envelope absent (back-compat) | `partial` notes path | `partial` notes path | `partial` notes path | `partial` notes path | (default) |
| Implementation cost | 1 file edit | 4 file edits + script | 3 file edits | 4 file edits | 0 |
| Reversibility if it doesn't help | Easy | Medium (sidecar lifecycle) | Easy | Easy | Trivial |

**Recommendation:** Option C — see `## Recommendation` below.

## Option Details

### Option A: Minimal envelope — three fields

**Description:** Extend the implement-agent return schema with the smallest envelope that improves on free-form `[PARTIAL]` notes. Three fields:

```json
{
  "implementation_status": "partial_resume_pending",
  "completed_subtargets": ["..."],
  "remaining_subtargets": ["..."],
  "partial_state_notes": "..."
}
```

No `resume_instructions` (folds into `partial_state_notes`), no `confidence`, no integrity hash. Orchestrator persists the envelope to the task's `notes` field as structured JSON in a fenced block, or alongside notes in a `partial_completion` field on the task JSON. No `.handoff.json` schema change — partial state lives on the task only.

**Strengths:**
- Lowest output-token cost (~80 tokens per partial return). Matters because output budget caps at 32K and partial returns happen exactly when budget is already tight.
- Lowest schema-churn footprint: only implement-agent.md and a small bullet in work.md State Persistence Protocol.
- Easy to expand later if usage data shows the minimal version isn't enough.

**Weaknesses:**
- Doesn't capture "how" to resume (only "what's left"). Re-dispatch prompt has to reconstruct resume instructions from the `partial_state_notes` blob, which is the same prose-parsing problem we have today (just with structured boundaries).
- No integrity check — orchestrator must trust the agent's claim that completed subtargets are really done. If T433's situation recurs (agent edits crash mid-write), `completed_subtargets` might lie.
- No confidence signal — user can't tell if the partial is "I cleanly stopped at a boundary" vs "I think I'm done with X but didn't verify."

**Research notes:** Mirrors the spirit of the verify-agent wind-down protocol (return what you have, no decoration). Cheap to revert if it doesn't help.

### Option B: Full envelope — five fields + integrity hash, dedicated sidecar

**Description:** The full FB-049 proposal plus integrity guards. Five envelope fields:

```json
{
  "implementation_status": "partial_resume_pending",
  "completed_subtargets": [{"name": "field_X", "files_touched": ["src/x.py"], "files_hash": "sha256:..."}],
  "remaining_subtargets": ["field_Y", "field_Z"],
  "partial_state_notes": "...",
  "resume_instructions": "...",
  "confidence": "high | moderate | low",
  "prior_attempt_files_hash": "sha256:..."
}
```

Orchestrator persists to a new sidecar file: `.claude/tasks/task-{id}.partial.json`. The sidecar has its own lifecycle (created on partial return, consumed on next dispatch, deleted on successful re-dispatch completion). On re-dispatch, the orchestrator re-computes the hash of `files_touched` and compares against `files_hash`; mismatch triggers a "previous edits may have been rolled back — resume with caution" prompt.

**Strengths:**
- Highest fidelity: completed subtargets carry file lists, the envelope carries integrity hashes, confidence is explicit.
- Sidecar lifecycle keeps the task JSON clean and visually identical to non-partial tasks (no `partial_completion` field cluttering normal tasks).
- Integrity hash addresses Question 6 directly — orchestrator can detect rollbacks or merge conflicts before re-dispatch.

**Weaknesses:**
- Highest output-token cost (~300 tokens, of which hashes are ~80). When the agent is already at 75% budget, spending another 300 output tokens on the envelope is a real concern.
- Sidecar adds a new file class to maintain. Lifecycle is "delete after consume" but if something breaks mid-flow (crash, abort), orphan sidecars accumulate — needs cleanup logic in `/health-check` or session recovery.
- The hash computation has to happen in the agent's context (Bash + `shasum`), which consumes tool-uses precisely when they're scarce.
- Symmetry with `.handoff.json` becomes inconsistent — handoff already absorbs `active_work[].partial_notes` and `files_modified_this_session`. A separate sidecar duplicates that surface.

**Research notes:** The most "engineering-correct" option but also the most expensive in tokens and template-maintenance surface. Probably an over-fit for a problem that only fires on rate-limit cuts.

### Option C: Middle path — four fields, implement-only, in-handoff

**Description:** Recommended option. Extend the implement-agent return schema with four envelope fields plus a `confidence` signal:

```json
{
  "implementation_status": "partial_resume_pending",
  "partial_completion": {
    "completed_subtargets": ["field_X (4 buckets, validated)", "field_Y (3 buckets)"],
    "remaining_subtargets": ["field_Z", "field_W"],
    "resume_instructions": "Resume from field_Z. Follow same bucket-taxonomy precedent as field_X.",
    "confidence": "high | moderate | low"
  }
}
```

`partial_state_notes` folds into `resume_instructions` (one prose field, not two). No `prior_attempt_files_hash` — orchestrator instead audits at re-dispatch time using `git diff` against the task's `files_affected` and surfaces "N files modified since partial — review before resuming?" if the diff is non-empty in unexpected areas (cheaper, no agent-side hash cost).

Persistence: orchestrator writes the envelope to the task JSON as a top-level `partial_completion` object (sibling to `notes`, `task_verification`, etc.). On re-dispatch, work.md reads the envelope, injects it into the agent's dispatch prompt, and **deletes the envelope field** after the new dispatch returns `completed` or a fresh `partial_resume_pending`.

`.handoff.json` schema impact: extend `active_work[].partial_notes` from a single string to a discriminated union — either a string (current behavior, fallback) or the envelope object. This is a tiny additive schema change; old handoffs still parse.

Detection threshold: agent returns `partial_resume_pending` when (a) tool_uses > 75% of `max_turns` AND remaining subtargets > 0, OR (b) the SDK has surfaced an `error_max_turns` wrap-up signal (graceful turn-limit feature — see Research Findings Q1). The "OR" form means even if 75% is wrong for this session, the SDK's own wrap-up steers the agent.

**Strengths:**
- Solves the observed 10-15 min audit overhead per incident at moderate cost (~150 tokens per partial return, 3 template files touched).
- No new file class — fits within the existing task JSON + handoff schema surfaces.
- `confidence` field surfaces uncertainty to user/next-dispatch without forcing the agent to compute hashes.
- Audit-via-git-diff at re-dispatch is cheaper than hashing and works even if the agent never wrote a hash (back-compat with old `[PARTIAL]` notes).
- Detection threshold is dual-trigger: relies on the SDK wrap-up signal when present (authoritative), falls back to heuristic when not.
- Reversible: if envelopes don't help, deleting the schema is a one-file revert.

**Weaknesses:**
- 75% heuristic is still arbitrary — but the OR with SDK wrap-up makes it a soft trigger, not a hard one.
- Re-dispatch audit relies on git availability — fails open (no audit) in non-git contexts, but those are rare for this template's intended use.
- Doesn't catch the case where the agent crashes mid-edit and never returns an envelope at all. That case still falls back to `[PARTIAL]` notes + manual audit, which is no worse than today.

**Research notes:** The threshold/symmetry/sidecar tradeoffs all bias toward "smaller surface, bigger payoff per change" for a feature whose firing rate is "occasional but recurring." Output-token cost (Q2) matters most when the agent is exactly at its budget edge, which makes Option B's 300-token envelope feel like a tax on the moment it matters most.

### Option D: Symmetric envelope — Option C + matching verify-agent contract

**Description:** Everything in Option C, plus a parallel `partial_verification_pending` envelope for verify-agent. The verify-agent schema gains:

```json
{
  "result": "partial",
  "partial_verification": {
    "checks_completed": ["files_exist", "consistency_check", "spec_alignment"],
    "checks_remaining": ["runtime_validation", "integration_ready", "scope_validation"],
    "tentative_findings": [...],
    "resume_instructions": "..."
  }
}
```

On `result: "partial"`, orchestrator leaves the task at "Awaiting Verification" (does not transition to Finished, does not increment `verification_attempts`), writes the envelope to the task JSON, and re-dispatches verify-agent at the next `/work`. The new dispatch reads the envelope and skips the already-passed checks.

**Strengths:**
- Symmetric: both agent types get a graceful-cut path.
- Per-check skip on re-dispatch saves tool-uses on the second pass (verify-agent doesn't redo `files_exist` if Pass 1 already confirmed it).

**Weaknesses:**
- Verification is canonically binary (pass/fail) per `context-transitions.md` § "Verify-Agent Wind-Down" — partial verification is explicitly disallowed there because a partial result "could be mistaken for a real result." Adding a third state contradicts that invariant.
- Verify-agent already has a structurally cleaner wind-down: return `result: null` with notes, leave status untouched, let session recovery Case 1 re-spawn fresh. The orchestrator-side cost is "re-run verify from scratch" — measurable but small (per-task verify is ≤30 turns).
- Skipping previously-passed checks introduces a subtle bug surface: if the spec changed between Pass 1 and Pass 2, the cached `files_exist: pass` is stale. The integrity check (spec fingerprint) would need to be added to keep this safe.
- Doubles the schema-churn footprint for an asymmetric payoff: implement-agent's partial state is hard-to-reconstruct prose, verify-agent's partial state is just "redo the checks."

**Research notes:** The asymmetry is real — implement-agent's wind-down is about preserving created state (file edits), verify-agent's is about preserving evaluation state (pass/fail decisions). The first is hard to reconstruct from observation; the second is cheap. Different problems, different solutions. Option D's parity treats them as the same problem when they're not.

### Option E: Defer

**Description:** Do nothing template-side. Rely on:
- The Claude Agent SDK's `error_max_turns` `ResultMessage` subtype and graceful "wrap up immediately" steering message (which already exist — see Research Findings Q1, Q3).
- The existing `implementation_status: "partial"` path with `[PARTIAL]`-prefixed notes.
- Manual audit at re-dispatch (current behavior).

**Strengths:**
- Zero implementation cost.
- Zero schema churn.
- Avoids potentially over-fitting to two observed incidents in one project's session.

**Weaknesses:**
- Doesn't address FB-049's measurable 10-15 min audit overhead per incident.
- The SDK's wrap-up message is steering, not structured output — the agent can write whatever prose it wants, and the orchestrator still has to parse.
- Doesn't surface a `confidence` signal — user can't differentiate "clean partial" from "rushed partial."
- Doesn't establish a contract for the next time this fires; we re-litigate the audit each time.

**Research notes:** Defer is rational if you believe rate-limit cuts will become rarer (Anthropic doubled Claude Code's 5-hour rate limits in May 2026 — see Q1). If usage limits keep tightening with model size, the envelope pays for itself. The observed evidence (twice in one styler session) suggests the second hypothesis holds.

## Recommendation

**Option C (Middle path)** — four-field implement-only envelope, persisted to the task JSON, with the `.handoff.json` schema extended for in-band carriage. Recommended for the following reasons:

1. **Solves the observed pain at moderate cost.** The 10-15 min audit overhead per FB-049 incident is real and recurring. Option C's ~150-output-token envelope is small enough to fit comfortably even when the agent is at 75% budget. Options A (3-field) and B (full + sidecar) sit at the extremes of "too thin to fully replace prose audit" and "too expensive at the moment it matters most."
2. **No new file class.** Persistence reuses the task JSON and a minimal extension to `.handoff.json`'s `active_work[].partial_notes` (string-or-object union). This avoids the orphan-sidecar lifecycle problem from Option B.
3. **Dual-trigger detection.** The 75% heuristic is arbitrary (Question 2 flagged this), but pairing it with the SDK's `error_max_turns` wrap-up steering signal (Q1, Q3 finding) means the agent has an authoritative in-band signal too. The heuristic becomes a backstop, not the primary trigger.
4. **Re-dispatch integrity via git diff, not agent-side hashing.** Question 6 surfaces the "did prior edits survive?" risk. Option C handles it orchestrator-side at re-dispatch time (cheap, runs in fresh context) rather than agent-side (expensive, runs at budget edge). The agent's `confidence: low` plus an orchestrator-detected diff mismatch produces a stronger signal than either alone.
5. **Asymmetric scope for an asymmetric problem.** Question 3 and Option D analysis: implement-agent's partial state is observation-hard (files created, decisions made), verify-agent's is observation-cheap (just rerun). Option C matches the scope of the symmetry actually needed. If observed verify-agent cuts become a measurable pain (none on file today; only the T454 case where verify never started), revisit then.
6. **Confidence field addresses Question 8.** Adding `confidence: high | moderate | low` to the envelope is essentially free in tokens (~5 tokens) and gives the user/next-dispatch a clear signal of how trustworthy the partial claim is. Mirrors `research-agent.md` Step R5's confidence reporting.
7. **Reversible.** If post-trial observation shows envelopes don't help (or always fire too late / too early), removing the schema is a single-commit revert across implement-agent.md, work.md, and context-transitions.md.

Confidence in this recommendation: **moderate** — the design is sound but rests on one open question (the actual fire-rate of partial returns post-implementation). Recommend a 30-day trial window (mirroring FB-011 Family E pattern) where partial envelopes are tracked, with a check-in decision at end-of-window: keep as-is, tighten thresholds, or escalate to Option B if integrity issues surface.

## Research Findings

### Q1: Anthropic API signals when approaching usage limits

**Out-of-band (HTTP response headers, harness-only):** The Anthropic Messages API returns `anthropic-ratelimit-{requests,tokens,input-tokens,output-tokens}-{limit,remaining,reset}` headers on every response, plus `retry-after` on 429s. These are visible to the SDK and Claude Code harness but **not in-band to the agent's prompt context**. The agent cannot read its own remaining-budget headers.

Source: [Claude API Rate Limits](https://platform.claude.com/docs/en/api/rate-limits) § Response headers.

**In-band (SDK steering messages):** The Claude Agent SDK implements a "graceful turn limit" — when `max_turns` is being approached, a steering message is injected: *"Wrap up immediately — provide your final answer now."* The agent sees this in its conversation context and can use it as a trigger to return a structured partial report instead of pushing through. The SDK then yields a `ResultMessage` with `subtype: "error_max_turns"` if the limit is hit.

Source: [Claude Code Agent Loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) § "Handle the result" (lists `error_max_turns` and `error_max_budget_usd` as terminal subtypes).

**Recent context (May 2026):** Anthropic doubled Claude Code's 5-hour rate limits across paid plans and lifted API rate limits for Opus. Frequency of usage-limit cuts should decrease but they're not gone.

Source: [Anthropic doubles Claude Code rate limits (May 2026)](https://appwrite.io/blog/post/anthropic-doubles-claude-code-rate-limits).

**Conclusion for envelope design:** The agent has TWO viable detection signals: (a) self-estimated `tool_uses` count vs `max_turns` (always available), and (b) SDK wrap-up steering message (when SDK enforces graceful turn limits). The envelope's detection logic should treat these as an OR — either signal triggers the structured partial return. The 75% heuristic from FB-049 becomes the fallback when the SDK signal is unavailable or arrives too late.

### Q2: Token cost of the current implement-agent return schema

The current schema has 7 top-level fields (`task_id`, `implementation_status`, `completion_date`, `notes`, `files_modified`, `friction_markers`, `issues_discovered`, `decisions_to_record`). A typical completed-task return weighs in around 150-400 output tokens depending on `notes` verbosity and friction-marker count. Reference: `.claude/agents/implement-agent.md:127-160`.

**Estimated marginal cost per envelope option:**

| Option | New fields | Estimated tokens | % of 32K output cap |
|--------|-----------|:---:|:---:|
| A (minimal, 3 fields) | `completed_subtargets[]`, `remaining_subtargets[]`, `partial_state_notes` | ~80 | 0.25% |
| B (full + hash) | + `resume_instructions`, `confidence`, `prior_attempt_files_hash`, per-subtarget `files_hash` | ~300 | 0.94% |
| C (middle, 4 fields) | `completed_subtargets[]`, `remaining_subtargets[]`, `resume_instructions`, `confidence` | ~150 | 0.47% |

The "% of 32K" framing matters because partial returns happen when the agent is already at budget edge. Output-token cost shares the 32K cap with thinking, text, and tool-call arguments. Spending 300 tokens (Option B) at 75% budget cuts deeper into available headroom than spending 80 (Option A) or 150 (Option C).

### Q3: Precedents for partial-completion / structured-resume contracts

**Claude Agent SDK (most direct precedent):** Implements the graceful turn-limit pattern documented in Q1. Key fields:
- `ResultMessage.subtype: "error_max_turns"` — terminal signal
- `ResultMessage.session_id` — resume identifier
- The conversation transcript is preserved verbatim across resume (subagents that resume "retain their full conversation history, including all previous tool calls, results, and reasoning" — [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)).

Source: [SDK Agent Loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) § "Sessions and continuity".

**Template's own precedent — `.handoff.json` `active_work[]`:** Already implements a partial-state contract for `/work pause`-triggered wind-downs (`.claude/support/reference/context-transitions.md` § "Field Definitions"):
- `partial: boolean` — discriminator
- `partial_notes: string` — what was done and what remains
- `files_modified_this_session: array` — for re-dispatch fidelity
- `ready_for_verify: boolean` — gate signal

**Fields that proved necessary in `.handoff.json`:** discriminator (`partial`), narrative state (`partial_notes`), file list (`files_modified_this_session`). **Fields not present** (deliberately not added): integrity hashes, per-step decomposition, confidence. Those decisions reflect "user-paused wind-downs are clean by construction; rate-limit cuts are not." This is a meaningful asymmetry — the rate-limit case justifies more fields than the user-pause case.

**Template's own verify-agent wind-down:** Explicitly rejects partial verification (`context-transitions.md:286-290`): *"Do NOT write partial `task_verification` — verification is binary (pass/fail). A partial result could be mistaken for a real result."* This is a strong precedent that the implement-side and verify-side asymmetry is intentional, not accidental.

### Q4: Interaction with verify-agent

**If implement-agent returns `partial_resume_pending`:** verify-agent should NOT run on the partial state. The atomic implement→verify contract requires `implementation_status: "completed"` to trigger verification (per `implement-agent.md:537-541`). Treating `partial_resume_pending` as a third implementation status keeps verify-agent out of the loop by construction — the orchestrator's State Persistence Protocol routes only `completed` to verify dispatch.

**Re-dispatch flow with envelope:**
1. Orchestrator detects task with `partial_completion` field at `/work` startup or routing.
2. Orchestrator dispatches implement-agent with envelope content injected into the prompt: "Resume task {id}. Previously completed: {completed_subtargets}. Remaining: {remaining_subtargets}. Resume instructions: {resume_instructions}. Confidence in prior state: {confidence}."
3. Orchestrator may also inject a git-diff audit if changes exist outside `files_affected` ("N files modified since partial; review before resuming").
4. Re-dispatched agent finishes work, returns `completed`.
5. Orchestrator clears the `partial_completion` field and dispatches verify-agent normally.

**verify-agent never sees the envelope** — by the time verify-agent runs, the task is complete and the envelope is cleared. This keeps verify-agent's "fresh eyes" property intact (DEC-004 invariant).

### Q5: Right unit for "remaining work" — sub-targets vs file-level vs step-level

**Sub-targets is the right unit** for the following reasons:

- **File-level under-counts work.** A single file may have 18 declared sub-targets (T433 reference). "Edits to src/x.py" is one file; "edits to fields A, B, C, ... R in src/x.py" is 18 sub-targets. The agent's value-add over a re-derived `git diff --name-only` view is the named decomposition.
- **Step-level over-counts.** Implement-agent has 6 named steps (Select Task → Return Report). At a granularity where rate-limit cuts happen, the agent is always mid-Step 4 (Implement). Step-level partial state collapses to "Step 4 not done."
- **Sub-targets match the agent's own mental model.** The agent decomposes large tasks into named work items during implementation (typically reflected in task `notes` field as "[Phase 1/3]" or similar progress markers). Sub-targets formalize that decomposition into the structured return.

**Granularity guideline:** Sub-targets should be named work items the agent can describe in a short phrase (e.g., "field_X bucket sweep", "auth-flow integration test setup") — not individual file edits and not abstract phases.

### Q6: Re-dispatch integrity — verifying prior edits survived

**Two layers of integrity check, in order of cost:**

**Layer 1 (cheap, orchestrator-side, recommended for Option C):** At re-dispatch, orchestrator runs `git diff --name-only` against the task's `files_affected` AND against the union of the previous attempt's `files_modified_this_session` (from the handoff `active_work[]` entry, if present). If the diff shows:
- Files in `files_affected` that have NOT been modified → "previous edits may have been rolled back" warning surfaces to user
- Files outside both lists have been modified → "concurrent work detected" warning surfaces

This is essentially free — it's the same git query verify-agent already runs in T2b (scope validation). Reusing that machinery for re-dispatch costs zero new code.

**Layer 2 (expensive, agent-side, only in Option B):** Per-subtarget `files_hash: sha256:...` computed via `Bash(shasum -a 256 file1 file2)`. Pro: deterministic detection of any byte-level rollback. Con: each hash is a tool-use, and rate-limit-cut returns happen exactly when tool-uses are scarce. The agent would burn 3-5 tool calls hashing files at the worst possible moment.

**Recommendation:** Layer 1 only. If observed sessions show Layer 1 missing real rollback cases, escalate to Layer 2.

### Q7: Failure mode if the envelope is wrong

**Concrete failure modes:**

1. **Over-claim:** Agent says `completed_subtargets: [A, B]` but B was actually half-done. Re-dispatch starts on `remaining_subtargets` and never circles back to finish B.
2. **Under-claim:** Agent says `remaining_subtargets: [Z]` but Z was actually done. Re-dispatch re-does Z, possibly inconsistent with prior pass.
3. **Phantom files:** Agent lists a sub-target as complete but the file was never actually written (Bash call failed silently mid-implementation).

**Mitigations in Option C:**

- **Orchestrator audit at re-dispatch (Layer 1 above).** Detects rollback / missing edits in the declared file set before the re-dispatched agent starts work.
- **Re-dispatched agent instruction.** The prompt that injects the envelope into re-dispatch should include: "Before continuing, spot-check that the `completed_subtargets` are actually present in the deliverable. If any are missing, treat them as `remaining_subtargets` instead." This is a one-line addition to the dispatch prompt template in work.md.
- **`confidence` field as user signal.** When `confidence: low`, the orchestrator surfaces a "Resume cautiously — agent low-confidence in partial state" warning rather than silently re-dispatching.
- **Falls back to current behavior.** If the envelope is wholly wrong, the worst case is the user audits manually — same as today, with no regression.

**Mitigations in Option B (additional):** Hash-based detection catches phantom-file failures directly. Higher integrity but higher cost. The marginal benefit over Option C's Layer 1 + spot-check is small for the observed failure modes.

### Q8: Confidence field

**Recommendation:** Include `confidence: "high" | "moderate" | "low"` in the envelope. Cost: ~5 output tokens. Benefit:

- Surfaces uncertainty to the next dispatch (and to the user). Mirrors `research-agent.md` Step R5's confidence-in-recommendation reporting (a precedent already accepted in the template).
- Lets the orchestrator differentiate auto-resume (high confidence) from confirm-before-resume (low confidence) without requiring per-incident user judgment.
- Provides a third signal beyond "did the envelope exist?" and "did the git-diff audit pass?" — when all three agree, auto-resume is safe; when they disagree, surface the conflict.

**Calibration guidance for the agent** (to be documented in implement-agent.md when the envelope ships):
- `high`: Clean boundary — finished a logical unit, declared remaining work has not been started.
- `moderate`: Mid-unit boundary — declared completed subtargets verified by self-review, but remaining sub-targets are in flux.
- `low`: Rushed boundary — SDK wrap-up fired before self-review; declared completed subtargets not independently re-checked.

### Sources cited

- [Claude API Rate Limits](https://platform.claude.com/docs/en/api/rate-limits)
- [Claude Code Agent Loop](https://code.claude.com/docs/en/agent-sdk/agent-loop)
- [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)
- [Anthropic doubles Claude Code rate limits (May 2026)](https://appwrite.io/blog/post/anthropic-doubles-claude-code-rate-limits)
- Template files:
  - `.claude/agents/implement-agent.md` (return schema, Step 6)
  - `.claude/agents/verify-agent.md` (verify modes; wind-down)
  - `.claude/support/reference/context-transitions.md` (handoff schema, verify wind-down)
  - `.claude/commands/work.md` (State Persistence Protocol)
  - `template-maintenance/feedback.md` § FB-049 (originating proposal)

## Your Notes & Constraints

*(user notes go here)*

---

## Decision

*(populated after user selects an option)*
