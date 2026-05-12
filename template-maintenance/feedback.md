# Feedback Log

Items are captured via `/feedback` and triaged via `/feedback review`.

---

## FB-011: Explore scripts as alternative to commands or within skills folders

**Status:** ready
**Captured:** 2026-04-08
**Refined:** 2026-04-14 — Identify command procedures where a deterministic script would outperform LLM-executed natural-language instructions — starting with the dashboard, where output variation across regenerations makes the artifact harder to comprehend. Scripts could live alongside commands or inside skills folders if that's a valid pattern. Gains: (1) consistency of standardized artifacts, (2) reduced error rate from procedure drift, (3) lower token cost. Scope is exploratory — inventory candidates and propose which procedures to extract before committing.
**Assessed:** 2026-04-14 — Primary target is dashboard regeneration (touching `.claude/support/reference/dashboard-regeneration.md`, `.claude/rules/dashboard.md`, and call sites in implement-agent Steps 3, 6a, 6c). Shipping scripts needs a new home (likely `.claude/scripts/` — root `scripts/` is template-maintenance and does not ship). Conflict: `rules/agents.md` restricts Bash, and scripts depend on it — connects to FB-010 (subagent Bash sandbox limits). Dependencies: FB-017 (checkbox detection is a concrete second candidate). Scope: start with a workspace inventory doc (`.claude/support/workspace/scripts-candidates.md`) listing candidates with tradeoffs; first extraction targets dashboard regen.

Look into where scripts could be used instead of commands, or even perhaps as part of skills folders if that is a valid use-case. Needs to be more robust or save tokens or minimize errors, improve quality etc.

## FB-033: Spec-auditor subagent + PreToolUse gate (research-first; trial FB-032 first; candidate DEC-009)

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects new `.claude/agents/spec-auditor.md` (subagent, not Skill — resolved by DEC-007), hook wiring, verify-agent integration. Scope: exploratory. Research-first AND trial-gated on FB-032 (only pursue if the structural output contract proves insufficient after real `/iterate` sessions under Opus 4.7). FB-020 dependency resolved by DEC-007 (subagent is the correct home). FB-026 dependency resolved by DEC-008 (layered settings stay; hook wiring goes in `settings.local.json` if pursued). Route: Phase 3 research — **deferred** until FB-032 trial data exists (candidate DEC-009).

Source: Claude Code usage insights report (fetched 2026-04-17) — "On the Horizon" section proposes an adversarial-reviewer subagent that intercepts every `Write`/`Edit` to `spec*.md` or `decisions/*.md`. User edit on capture: *"wait until A1 is trialed properly before deciding"* — this item is explicitly gated on FB-032's trial outcome.

A bigger-hammer version of FB-032. The spec-auditor would diff each proposed change against the prior version, extract new assertions/decisions, cross-reference them against the current session's explicit user instructions, emit a "user-requested vs agent-inferred" table, and block the write until agent-inferred items are approved.

**Trial-gate:** Do not pursue until FB-032's structural output contract is trialed across several real `/iterate` sessions under Opus 4.7. If FB-032 materially reduces silent-decision friction, FB-033 is unnecessary. If FB-032 proves insufficient — silent decisions still slip through, or the output contract is bypassed — FB-033 becomes the structural backstop.

**Questions to resolve if FB-032 proves insufficient (likely via a decision record):**
- Should the spec-auditor be a subagent (`.claude/agents/`) or a Skill (`.claude/skills/`)? Depends on FB-020's findings on subagent-vs-skill context-window separation.
- Where does the PreToolUse hook live — template-owned `.claude/settings.json` (DEC-005 currently restricts that file to `permissions.allow` only), user-owned `settings.local.json`, or a documented example in `setup-checklist.md`?
- If auto mode (DEC-008 / FB-026 outcome) already covers most of the "block unapproved write" goal at the permission layer, does the hook reduce to a narrower belt-and-braces?
- Performance cost of running an adversarial diff-and-review before every spec/decision write.

**Impact scope if pursued:** potentially large — new `.claude/agents/spec-auditor.md` (or `.claude/skills/spec-auditor/`), hook wiring, integration with verify-agent contract.

**Likely outcome:** candidate DEC-009 after FB-032 trial, FB-020 research, and FB-026 resolution all close.

## FB-049: Anthropic usage-limit partial-completion structured resume contract

**Status:** ready
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-009 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler
**Refined:** 2026-05-13 — Extend implement-agent return schema with a `partial_completion` envelope the agent fills when sensing usage-limit approach with unfinished sub-targets: `implementation_status: partial_resume_pending`, `completed_subtargets[]`, `remaining_subtargets[]`, `partial_state_notes`, `resume_instructions`. Orchestrator persists to task JSON; next dispatch brokers a 'resume from where you stopped' prompt instead of re-deriving from git diff. Detection heuristic: tool_uses > 75% of budget AND remaining sub-targets > 0. Extend `.handoff.json` schema for task-level partial state. Scope: `implement-agent.md` schema + `work.md` dispatch.
**Assessed:** 2026-05-13 — Affects `.claude/agents/implement-agent.md` (return schema fields), `.claude/commands/work.md` (dispatch + persistence), `.claude/tasks/.handoff.json` schema. Possibly `.claude/agents/verify-agent.md` (matching envelope?). Scope: additive. No conflict with DEC-004 state ownership (orchestrator persists; agent reports). Multiple non-trivial design choices remain: minimal envelope vs full, detection threshold (75% of budget — arbitrary), whether verify-agent gets a matching envelope, `.handoff.json` schema impact. **Route: Phase 3 research → candidate DEC-010.** Trial-gated on real usage-limit incidents (already observed twice in styler session per body — sufficient empirical basis to research now).

Anthropic usage-limit cuts mid-implement-agent or mid-verify-agent are recurring (twice in one styler session: T433's first dispatch was cut at 41 tool uses with no structured report; T454's verify-agent dispatch in the same session never started before the limit hit). Current handoff is via free-form task notes + dashboard prose + `.last-clean-exit.json` — entirely manual. Subsequent invocations have to audit partial work and reason about resumption.

**Concrete repro (styler T433, 2026-04-27 13:25 UTC):**

First implement-agent dispatch hit usage limit at 41 tool uses / 297s, returned no structured report. Working tree had partial edits across 3 of the task's ~18 declared sub-targets. Second invocation had to:

1. Read git diff to infer what landed
2. Read task notes for partial-progress hints (none present — orchestrator had only logged "dispatch cut by limit")
3. Audit which sub-targets within the cluster sweep were already done vs remaining
4. Compose a unified report covering both invocations once it finished the rest

Workflow handled it gracefully but the cross-invocation reasoning is fragile and adds ~10–15 minutes of audit overhead.

**Proposed fix:** Extend the implement-agent return schema with a `partial_completion` envelope that the agent can fill if it senses approaching limit AND has not finished:

```json
{
  "implementation_status": "partial_resume_pending",
  "completed_subtargets": ["field_X (4 buckets)", "field_Y (3 buckets)"],
  "remaining_subtargets": ["field_Z", "field_W", "field_V"],
  "partial_state_notes": "Stopped mid-sweep at field_Z; no edits to field_Z yet. Bucket taxonomy precedent: field_X = activity-family (indoor/outdoor/...).",
  "resume_instructions": "Resume from field_Z. Follow same bucket-taxonomy precedent as field_X. After all remaining, sweep audit to confirm 0 violations."
}
```

The orchestrator persists this to task JSON. Next dispatch reads it and brokers a "resume from where you stopped" prompt — the agent doesn't have to re-derive context from git diff + task notes.

`/work pause` already has graceful wind-down for user-initiated halts; this would mirror the pattern for the rate-limit case (which the agent itself can detect by approaching `max_turns` or by Anthropic's rate-limit response surface). The `.handoff.json` schema could be extended to include task-level partial state alongside session-level state.

Detection heuristic for the agent: if `tool_uses` count exceeds 75% of typical session budget AND remaining subtargets > 0, return `partial_resume_pending` instead of pushing through.

## FB-057: DEC-001 Option C execution gaps — friction-marker append + end-to-end pipeline

**Status:** ready
**Captured:** 2026-05-13
**Combined from:** FB-041 + FB-045
**Refined:** 2026-05-13 — Audit DEC-001 Option C pipeline execution. Cause 1 (template_inbox_path discoverability) resolved by FB-040 Part 5d. Causes 2 (orchestrator marker-append skipped under load — styler Phase 20 batch-appended at pause; abrupt termination would have lost all markers) and 3 (`/work pause` Track 2 + Session Export not reliably run) remain. Tiered fix: behavioral nudge → idempotent catchup → structural PostAgentReturn hook → deterministic script (FB-011 Family D/E candidate). Investigation steps documented (real downstream session probes). Scope: `commands/work.md`, `pre-compact-handoff.sh`, possibly new scripts.
**Assessed:** 2026-05-13 — Affects (investigation phase first): `.claude/commands/work.md` (marker-append protocol or hook), `.claude/hooks/pre-compact-handoff.sh` (idempotent catchup), possibly new `.claude/scripts/` script (FB-011 Family D/E). Scope: corrective. Gates on (a) empirical data from real downstream sessions — currently blocked because no downstream project has `template_inbox_path` set (next downstream `/health-check` will surface this via FB-040 Part 5d), and (b) FB-011 Family D/E decision per `scripts-candidates.md`. **Route: Phase 3 research → candidate DEC-011** for fix-tier selection after investigation. Cannot proceed to Phase 4 direct without telemetry.

DEC-001 Option C (Track 1 friction markers + Track 2 retrospective + Phase 3 ingest) is documented end-to-end across `implement-agent.md`, `verify-agent.md`, `work.md`, `pre-compact-handoff.sh`, and `health-check.md`, but empirical evidence suggests the pipeline isn't reliably executed.

**Observed gaps:**

1. **(from FB-041)** `interaction-logs/inbox/` empty as of 2026-05-13. Three causes:
   - Cause 1 (**resolved 2026-05-13**): no downstream project had `template_inbox_path` set — discoverability gap closed by `/health-check` Part 5d (FB-040 ship).
   - Cause 2: orchestrator-side marker append (`work.md:543,559`) documented but not reliably executed during `/work` runs.
   - Cause 3: `/work pause` Track 2 + Session Export step not reliably run (users close without pause; Claude may skip under context pressure).

2. **(from FB-045 — concrete repro for cause 2)** Styler Phase 20: orchestrator skipped the marker-append step throughout the session — markers from agent reports landed in task notes but NOT in `.session-log.jsonl` in real-time. At `/work pause` the orchestrator batch-appended 8 markers. Abrupt termination (compaction, crash, usage limit) would have silently lost those markers from Track 1 telemetry — task notes aren't structured for cross-project consumption.

**Investigation steps:**

- Run `/work` in a downstream project with markers expected to fire; inspect `.session-log.jsonl`.
- Run `/work pause`; confirm `.session-export-YYYY-MM-DD.json` appears in workspace and reaches `template_inbox_path`.
- Audit whether marker-append happens real-time vs catchup at pause.

**Proposed fixes (tiered):**

- Behavioral nudge: tighter protocol — append via single bash call immediately after agent return; do not batch.
- Idempotent catchup: if task notes contain markers without corresponding `.session-log` entries, orchestrator (or PreCompact hook) auto-appends.
- Structural: move append into a PostAgentReturn / PostToolUse hook gated on Task subagent — un-skippable.
- Or extract into a deterministic script (FB-011 Family D/E candidate) — removes the LLM reliability layer entirely.

Sources: FB-041 (2026-05-13, Option C audit) + FB-045 (2026-04-27, styler Phase 20).
