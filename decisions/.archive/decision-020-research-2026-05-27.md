# DEC-020 Research Archive — 2026-05-27

**Decision:** Conclude the DEC-007 Skills/reference duplication trial — retire which location, or re-charter.
**Researcher:** research-agent (Opus 4.7). **Authority:** evidence + options only; no selection.
**Method:** read DEC-020 + DEC-007 + the 3 SKILL/ref pairs + `claude-code-authoring.md` + README + health-check; grep citation surface; WebFetch live Claude Code docs (skills, debug-your-config, monitoring-usage) + 2 GitHub issues; WebSearch corroboration.

## Sources consulted (URLs)

- https://code.claude.com/docs/en/skills — Skills reference (auto-invoke, content lifecycle, frontmatter, description budget, troubleshooting, context:fork)
- https://code.claude.com/docs/en/debug-your-config — `/context`, `/skills`, `/doctor`, `/debug`; the "skill never invokes" symptom table
- https://code.claude.com/docs/en/monitoring-usage — OpenTelemetry: `claude_code.skill_activated` event, `skill.name` attribute, `invocation_trigger`, `OTEL_LOG_TOOL_DETAILS`
- https://github.com/anthropics/claude-code/issues/35319 — [FEATURE] Skill invocation tracking (OPEN, 2026-03-17; re-files stale #20970)
- https://github.com/anthropics/claude-code/issues/43287 — Model ignores auto-invoke skill instructions (closed as duplicate, 2026-04-03)

## Q1 — Auto-invoke reliability + observability

**Reliability — imperfect, treated as expected:**
- skills § Troubleshooting: "If a skill seems to stop influencing behavior after the first response, the content is usually still present and the model is choosing other tools or approaches." Prescribes hooks for must-happen behavior.
- debug-your-config symptom table: "Skill appears in `/skills` but Claude never invokes it → … its description doesn't match how you phrase the request."
- #43287 (OPEN as dup): "the model still ignores it and manually performs the steps itself instead of invoking the skill … the model's instinct is to create a 'feedback memory' file … which defeats the purpose of the skill system entirely."

**Observability — two-tier:**
- *In-session, no external tooling:* presence YES, auto-fire NO.
  - `/context` lists a **skills** category; `/skills` lists available skills + badge (debug-your-config). Invoked SKILL.md "enters the conversation as a single message and stays there for the rest of the session" (skills § Skill content lifecycle) → a post-trigger `/context` can show the body is now resident.
  - BUT per-session metadata is aggregate-only — #35319: "session metadata tracks `"Skill": 3` (aggregate tool count) but not which skill was invoked … there is no way to know which skills are actually being used." `/doctor` validates config + shows description-budget overflow ("Run `/doctor` to see whether the budget is overflowing and which skills are affected", skills) — NOT firing.
  - Constructible probe: a skill body can log `${CLAUDE_SESSION_ID}` (skills § substitutions) — proves body executed, not that auto-fire happened when it should have; requires editing the SKILL bodies.
- *Opt-in OpenTelemetry + external backend: per-skill auto-fire IS precisely observable.*
  - monitoring-usage § Skill activated event: `claude_code.skill_activated` "Logged when a skill is invoked, whether Claude calls it through the Skill tool or you run it as a `/` command." Attributes: `skill.name`, `skill.source` (e.g. `"projectSettings"`), and **`invocation_trigger`: "user-slash" | "claude-proactive" | "nested-skill"**.
  - Caveats: requires `CLAUDE_CODE_ENABLE_TELEMETRY=1` + OTLP endpoint; user-defined skill names redacted to `"custom_skill"` unless `OTEL_LOG_TOOL_DETAILS=1`.
- **Conclusion:** value-of-auto-invoke is empirically answerable ONLY via OTel `invocation_trigger` capture across real sessions; NOT from in-session UI; nothing in this repo captures it today → otherwise decide on principle.

## Q2 — Live docs vs repo `claude-code-authoring.md` (footer @ 2026-05-24 / v4.9.0)

Contradictions/staleness to fix on next Part 2d `[V]` pass:
1. Skill-listing cap: repo doc says flat "1,536-char cap on description + when_to_use." Live: total listing budget "scales at 1% of the model's context window" (`skillListingBudgetFraction` / `SLASH_COMMAND_TOOL_CHAR_BUDGET`), least-used dropped first; 1,536 is now the PER-ENTRY cap (`maxSkillDescriptionChars`). Repo doc conflates per-entry cap with total budget.
2. `/doctor` budget-overflow visibility — absent from repo doc.
3. `/context` + `/skills` presence-inspection — absent from repo doc; directly relevant to "did the skill load?"
Consistent (no contradiction): turn-scoped model/effort (verbatim); 25K re-attach + first-5,000-tokens-each (live adds most-recent-first fill order); one-message-and-stays lifecycle (verbatim); context:fork inheritance (verbatim); disable-model-invocation (live adds: "removes the skill from Claude's context entirely" + blocks subagent preload).

## Q3 — Evidentiary basis (value vs safety)

Decisive codebase fact: orchestrator NEVER explicitly invokes the 3 skills — it path-cites the reference docs. `work.md` "Read `.claude/support/reference/decomposition.md`"; `iterate.md` "See `.claude/support/reference/spec-checklist.md`"; dashboard pipeline cites `dashboard-regeneration.md` ×9 by path. No Skill-tool / auto-invoke trigger in work.md/iterate.md. ⇒ Skills earn value ONLY via auto-fire (unreliable + unobservable, Q1); refs earn value via resolving explicit citations (observed).
- Value confidence: LOW/unproven for Skills; the "decomposition SKILL leads ref by 52 lines" is a maintenance-attention signal, not runtime-value. Proven value sits with the location B deletes.
- Safety confidence: A high (0 re-points; DEC-007 "reversal easy"); C high-as-an-act; B moderate (most churn).
- DEC-018 / auto-memory "pressure-test value before adopting" ⇒ don't retire proven (refs) for unproven (Skills) absent evidence ⇒ favors A or C over B.

## Q4 — Ripple / reversibility

- Skill referenceable by path === reference doc (skills: commands & SKILL.md "work the same way"; supporting files by relative path). Only mechanism diff: SKILL.md also participates in auto-invoke/description-budget. Under B, citations become "Read …/SKILL.md" AND still pay description budget; under A, auto-invoke role vanishes, citations unmoved.
- Real (non-archive, non-illustrative) citation re-points if B: dashboard ~9 (work ×4, audit-coherence ×3, audit-ui ×2, breakdown, rules/dashboard, phase-decision-gates, workflow, extension-patterns, audit-fix-workflow ×2); decomposition 1 (work.md:635); spec-checklist 2 (spec-workflow:52, iterate:415). `rules/dashboard.md:21` already names the SKILL path; `health-check.md:551` is an illustrative sync-output snippet (not a dep). A re-points NONE.
- Drift merge unavoidable for ALL THREE before any delete (and C must reconcile now to stop the active 2-sources bug): decomposition 52/11 = real semantic merge; dashboard 1/9 light; spec-checklist 1/1 trivial.
- Sync/health-check touch-points (whichever retired): `sync-manifest.json` sync[] has `.claude/skills/*/SKILL.md` (L9) + the 3 ref companions (L24/27/32). `health-check.md` has NO dedicated skills-sync check (skills ride generic Part 5 glob); skill-specific strings = illustrative L551 + Part 5 post-sync dashboard re-check keyed on `dashboard-regeneration.md` (L610, B must re-key). README § Skills (L92–103) + rows L46/L232 describe duplication (edit under A or B).

## Recommendation (evidence only; no selection)

Leans **A**, with **C** as the principled alternative ONLY IF the re-charter mandates OTel `skill_activated`/`invocation_trigger` capture + deadline + owner. **B** is weakest: it bets the kept location on the unproven, unobservable, documented-unreliable auto-invoke mechanism AND pays the highest ripple. Separation: safety favors A (high) ≈ C-as-act (high) > B (moderate); value evidence sits with the refs (proven via citations) not the Skills (unmeasured, unmeasurable in-session) ⇒ retiring refs for Skills (B) is the move the maintainer's evidence-first posture argues against. The value question is answerable but only via opt-in OTel telemetry across real sessions; absent that, decide on principle (which favors A).
