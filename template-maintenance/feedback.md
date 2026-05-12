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

## FB-038: Action Required regression — completion summaries still clutter section despite FB-015 fix

**Status:** ready
**Captured:** 2026-04-22
**Refined:** 2026-05-13 — Audit whether FB-015's Action Item Contract negative rule (now at `dashboard-regeneration.md:333`) actually fires during regeneration. Styler 2026-04-22 evidence shows completion summaries still clutter Action Required despite FB-015 promoted 2026-04-17. Two follow-ups: (a) audit dashboard-emission call sites for compliance; (b) if violations persist, escalate to FB-011 Family C (extract regen into a script — enforced by construction). Scope: `dashboard-regeneration.md`, `commands/work.md` post-completion emission paths, `health-check.md` Part 6 check #4.
**Assessed:** 2026-05-13 — Affects `.claude/support/reference/dashboard-regeneration.md` (verify rule landed and is well-formed; already at line 333), `.claude/commands/work.md` post-completion emission paths, `.claude/commands/health-check.md` Part 6 check #4 (extend to detect summary-shaped content if feasible). Scope: corrective. Two-step: (a) audit downstream emitters for compliance with FB-015's negative rule; (b) if LLM compliance keeps failing, escalate to FB-011 Family C (extract dashboard regen to a script — tracked in `template-maintenance/scripts-candidates.md`). Direct dependency on FB-015 (just promoted; freshness risk that the rule was added but emitters bypass it). Route: Phase 4 direct for the audit; FB-011 Family C escalation is a separate gate.

The dashboard's Action Required section is again dominated by non-actionable content even after FB-015 (currently `ready`) was supposed to address exactly this. Observed in the styler project dashboard export (`dashboard_export_styler.pdf`, 2026-04-22).

**What the section contains (none of which is user-action):**
- Paragraph-long closure summary for § 17.15 Phone Layout Remediation ("2 BLOCKERs + 12 HIGHs → [OK]")
- Bulleted shipped-tasks list (321–330) with one-line descriptions
- Multi-paragraph Task 331 completion report (fix details, verification method, "suggest bundling into a commit")
- Repo state narrative (committed vs uncommitted, untracked PNGs to discard)
- "Phase 5 still On Hold" reminder and "Residual follow-ups from earlier phases" with accepted spec drift

The only arguably-actionable fragment — "Change is uncommitted" — is buried inside a paragraph, not surfaced as an action item.

**User-reported phrasing:** *"even more cluttered with stuff that isn't actionable now after we implemented a fix. Something is going on"* — pattern appears to be regressing, not just failing to improve.

**Possible root causes** (to refine):
1. FB-015 is `ready` but not yet promoted via `/iterate` — the rule edit may never have landed in `dashboard-regeneration.md` § Action Item Contract. Verify before anything else.
2. Rule landed but generators (`/work complete`, phase-closure regen, implement-agent post-completion emission) bypass the Action Item Contract in practice.
3. LLM interprets completion summaries as "actionable" because they imply follow-ups (commit change, discard PNGs, resume On Hold phase).
4. Action Required is being used as a catch-all narrative slot because the dashboard has no dedicated "recent activity" or "session recap" section — matter removed from Action Required has nowhere else to go.

**Possible direction:** reopen/extend FB-015 rather than treat this as a new independent item. Also consider whether FB-011's deterministic generator is the only reliable backstop for a contract the LLM persistently violates.

Source: `dashboard_export_styler.pdf` (styler project, 2026-04-22).

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

## FB-050: /iterate spec-vs-registry hygiene pass — grep-validate spec claims

**Status:** ready
**Captured:** 2026-04-27
**Migrated:** 2026-05-13 — originally captured as FB-010 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler
**Refined:** 2026-05-13 — Add an `/iterate hygiene` pass that grep-validates spec noun-phrase claims about registry/schema state. Patterns: 'previously-empty X', 'field Y under section Z', 'update the X description'. Cross-reference against project's structured artifact (path configurable in `.claude/version.json`). Flag drift as `[NEEDS APPROVAL]` in the 'Decisions in This Proposal' section. Lighter alternative: fold into `/health-check` as per-spec consistency audit. Scope: `commands/iterate.md` OR `commands/health-check.md`.
**Assessed:** 2026-05-13 — Affects `.claude/commands/iterate.md` (new hygiene sub-command). Scope: additive. Complements FB-032 (Decisions in This Proposal — drift findings surface there). New config field needed: `structured_artifact_path` in `.claude/version.json` (project-configurable). Route: Phase 4 direct. The 'lighter alternative' (fold into `/health-check`) is a sub-decision worth flagging at implementation time — pick one before writing.

Spec text drifts from registry/schema state over time. Each drift triggers a `spec_drift` friction marker but is otherwise resolvable inline by the implement-agent — meaning the drift accumulates silently until a future spec edit is needed.

**Two concrete examples from one session:**

1. **Spec § 20.2** said the `extremities` subsection was "previously-empty" — registry actually had `feet` / `hands` / `head` / `glasses_sunglasses` / `everyday_jewelry` already populated. Implementer (T430) had to interpret intent and add new fields under the existing `head` composite rather than treating the subsection as truly empty. Friction marker logged.

2. **Spec § 20.2** instruction "update the extremities subsection description" — `SubsectionDefSchema` has only `id` / `label` / `order` / `storage_file` (no `description` field). Instruction was unimplementable as written; implementer worked around by updating `head.description` (the composite field's description) instead. Friction marker logged.

Each case caused avoidable confusion and post-hoc workaround. Both would have been caught at spec-revision time by a static cross-check.

**Proposed fix:** Add a `/iterate hygiene` sub-command (or fold into existing `/iterate`) that runs at spec-revision time:

1. **Parse the spec** for noun-phrase claims about registry/schema state — patterns like:
   - "the X subsection / field / type"
   - "previously-empty / previously-X / now-X"
   - "field Y under section Z"
2. **Cross-reference against the actual structured artifact** (project-specific: `field-definitions.json`, `schema.ts`, etc. — could be parameterized via a config field in `.claude/version.json`).
3. **Flag drift:** "Spec § 20.2 says 'previously-empty extremities' but registry has 5 top-level fields under `extremities`." Surface as a `[NEEDS APPROVAL]` item in `/iterate`'s "Decisions in This Proposal" section.
4. **Cross-reference spec instructions** like "update the X description" against the schema (`SubsectionDefSchema`, `FieldDefSchema`) to verify the target attribute exists. Flag unimplementable instructions before they reach decomposition.

This is generally useful even outside styler: any spec-driven project with a structured artifact (registry, schema, config) accumulates this drift over many revisions.

Alternative (lighter): add this to `/health-check` as a per-spec consistency audit, run on demand rather than as a separate `/iterate` mode.

## FB-055: subagent_type "general-purpose" used to dispatch specialist agents in work.md / research.md

**Status:** ready
**Captured:** 2026-04-28
**Migrated:** 2026-05-13 — originally captured as FB-015 in `.claude/support/feedback/feedback.md` (shipped path; misroute predates the v3.1.0 `/feedback template:` bridge).
**Source project:** styler — multi-agent template audit, 2026-04-28. `commands/work.md` and `commands/research.md` byte-identical to template.
**Refined:** 2026-05-13 — Three call sites (`work.md:603,686`; `research.md:74`) dispatch named specialist agents with `subagent_type: 'general-purpose'`. Switch to named subagent_types (`implement-agent`, `verify-agent`, `research-agent`) — aligns dispatch with definition, leverages `.claude/agents/` auto-discovery the template implicitly assumes by shipping definition files. Alternative (b) — document 'general-purpose' as intentional in `rules/agents.md` for portability — is the fallback if auto-discovery proves harness-version-fragile. Scope: `commands/work.md`, `commands/research.md`.
**Assessed:** 2026-05-13 — Affects `.claude/commands/work.md` (lines 603, 686 — implement-agent + verify-agent dispatch), `.claude/commands/research.md` (line 74 — research-agent dispatch). Scope: corrective. Dependency on DEC-004 (subagent capability contract — must verify named subagent_type doesn't change sandbox behavior relative to general-purpose; low risk but check first with a smoke test). Route: Phase 4 direct. Small change (3 sites + smoke test).

Three call sites dispatch named specialist agents (implement-agent, verify-agent, research-agent) but with `subagent_type: "general-purpose"`:

- `work.md:603` (implement-agent dispatch)
- `work.md:686` (verify-agent dispatch)
- `research.md:74` (research-agent dispatch)

The agent definitions live at `.claude/agents/{implement,verify,research}-agent.md` but the dispatch shape doesn't reference them as named subagent types. This works because the dispatched agent's prompt directs it to read its own definition file — but it bypasses any per-agent configuration that Claude Code's `.claude/agents/` discovery would otherwise apply (e.g., per-agent model default, per-agent tool allowlist if/when the harness supports them via frontmatter).

Two paths:

- **(a) Switch to named subagent_types** — `subagent_type: "implement-agent"`, `"verify-agent"`, `"research-agent"`. Relies on Claude Code's auto-discovery of `.claude/agents/*.md`. Aligns dispatch with definition.
- **(b) Document that "general-purpose" is intentional** — perhaps for portability across harness versions where named subagents might not auto-discover, or to keep the persona-via-prompt-content pattern. Add a one-line note in `rules/agents.md` explaining the choice.

Either is defensible; the current state is "neither documented nor uniformly applied." Worth picking one and being explicit. (a) seems cleaner if Claude Code's `.claude/agents/` discovery is stable, which the template implicitly assumes by shipping definition files there.

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
