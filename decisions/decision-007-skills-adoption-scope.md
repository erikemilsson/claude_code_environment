---
id: DEC-007
title: Skills adoption scope — where Skills fit in the template
status: proposed
category: architecture
created: 2026-04-17
decided:
related:
  tasks: []
  decisions: [DEC-004]
  feedback: [FB-020]
implementation_anchors: []
inflection_point: false
spec_revised:
spec_revised_date:
blocks: [FB-033]
---

# Skills adoption scope — where Skills fit in the template

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Don't adopt Skills — keep status quo (commands + rules + subagents)
- [ ] Option B: Adopt Skills for on-demand reference only (subset of `support/reference/`)
- [ ] Option C: Broader adoption — move eligible `rules/` content and domain packs to Skills; keep orchestration in commands; keep verify and agent flows in subagents
- [ ] Option D: Defer — wait for a concrete use case or Skills API stabilization

*Check one box above, then fill in the Decision section below.*

---

## Context

Claude Code Skills (official feature, documented at `code.claude.com/docs/en/skills`) load domain-specific guidance on demand, as opposed to CLAUDE.md + rules which load every session. The best-practices doc recommends Skills for "domain knowledge or workflows that are only relevant sometimes."

This template currently uses three mechanisms for prompting Claude:
- **Commands** (`.claude/commands/`) — orchestration entry points, slash-invoked
- **Rules** (`.claude/rules/`) — always-loaded workflow constraints
- **Subagents** (`.claude/agents/`) — isolated-context workers (implement-agent, verify-agent, research-agent)

Plus reference docs (`support/reference/`) that are cited from commands/rules but not always pre-loaded.

FB-020 asks whether Skills can carry template-owned domain guidance (software vs. research vs. procurement vs. renovation patterns) and whether they can host subagent-like workflows. User's primary concern: would Skills-hosted subagents still get fresh context (critical for DEC-004's verify-flow isolation)?

FB-033 (spec-auditor, deferred until FB-032 trialed) depends on this decision: if pursued, should the auditor be a subagent or a Skill?

## Questions to Research

(Answers in `## Research Findings` below.)

1. **Primary concern:** Does a Skill's execution share the caller's context, or get its own? What about subagents spawned from within a Skill?
2. How are Skills invoked, and what does `disable-model-invocation` actually control?
3. Can Skills ship from a template (`.claude/skills/`) the same way commands do?
4. Do Skills inherit parent CLAUDE.md permissions or carry their own?
5. What are the known limitations or blockers for migrating command/rule/subagent content to Skills?

## Options Comparison

| Criteria | A: No adoption | B: Reference only | C: Rules + domain packs | D: Defer |
|----------|---|---|---|---|
| Context-discipline benefit (on-demand loading) | None | Moderate | High | None |
| Risk to verify-flow isolation (DEC-004) | None | None | None (verify stays in subagents) | None |
| Implementation effort | Zero | Small (1–2 Skills) | Medium (new `.claude/skills/` + content migration) | Zero |
| Impact on users' mental model | None | Low | Medium (new dir, new pattern) | None |
| Unblocks FB-033 decision (auditor home) | Yes, implicitly (subagent) | Yes (subagent) | Yes (subagent) | No — defers FB-033 further |
| Reversibility | N/A | High | Moderate (migration to undo) | N/A |
| Future-proofing | Low (ignores a platform feature) | Moderate | High | Low (keeps kicking the can) |

**Recommendation:** Option B is the safest first move — see `## Recommendation` below.

## Option Details

### Option A: Don't adopt Skills

**Description:** Leave the template structure unchanged. All guidance stays in commands, rules, and subagents. Skills are not used.

**Strengths:**
- Zero work, zero risk
- Preserves the current mental model for existing users
- No new directory or pattern for template maintainers to manage

**Weaknesses:**
- Template fails to leverage a documented platform feature
- Context budget remains loaded with rules content that is not always relevant (e.g., `task-management.md` loads even for spec-only discussions)
- Leaves FB-033 in a weaker position: the spec-auditor decision has one less tool to consider

**Research notes:** Defensible if Skills are considered experimental or the user has low tolerance for maintaining a third content location. Not the strongest choice given the research findings are clear and favorable.

### Option B: Adopt Skills for on-demand reference only

**Description:** Create `.claude/skills/` with a small initial set of Skills for reference material that is not always needed: e.g., a "spec-checklist" Skill that loads the full checklist when `/iterate` invokes it, a "decomposition-heuristics" Skill that loads when `/work` decomposes, a "dashboard-style" Skill for dashboard regeneration. Each Skill is a thin wrapper over content that currently lives in `support/reference/`, with the same semantics but on-demand loading.

**Rules, commands, and subagents remain unchanged.** Orchestration and verify flows stay in commands/subagents where context-isolation semantics are preserved.

**Strengths:**
- Context-budget benefit without architectural risk
- Easy to reverse (delete `.claude/skills/`, content still lives in `support/reference/`)
- Validates Skills in a low-stakes corner before broader adoption
- Cleanly answers FB-033: spec-auditor is a subagent (Skills don't host orchestration)

**Weaknesses:**
- Small benefit — the reference docs it moves aren't that large
- Two copies of the content (`.claude/skills/X/SKILL.md` and `support/reference/X.md`) unless one is removed — requires a sync decision
- Introduces a new content location that template users must understand

**Research notes:** The on-demand loading property is genuinely useful for content that's >500 lines and not every-session relevant. `support/reference/decomposition.md`, `support/reference/spec-checklist.md`, and `support/reference/dashboard-regeneration.md` are strong candidates. Trial with one or two Skills; expand only if they demonstrate value.

### Option C: Broader adoption — rules + domain packs

**Description:** Migrate eligible content from `.claude/rules/` into Skills. Add domain-specific Skill packs (software-patterns, research-patterns, procurement-patterns) that load based on the spec's domain tag. Keep verify flows and orchestration logic in subagents and commands respectively — those remain unchanged for DEC-004 compatibility.

**Strengths:**
- Biggest context-discipline win — always-loaded rules become on-demand
- Domain-agnostic philosophy (CLAUDE.md § Design Philosophy) gets a structural home
- Future-aligned: Skills are the recommended direction per best-practices doc

**Weaknesses:**
- Largest migration effort
- Rules are intentionally always-loaded — some of them (e.g., `agents.md`, `session-management.md`) need to be in context for `/work` decisions. Moving them to Skills would mean re-loading every invocation, which may produce the opposite of the intended benefit
- Risk of Skills not being invoked when they should be (description-matching reliability)
- Mental model shift for template maintainers (third primary content location)

**Research notes:** A subset of rules may be Skill-eligible: `archiving.md` is rarely needed mid-session; `dashboard.md` is only needed during dashboard regen; `decisions.md` is only needed when decisions are being made. Core rules (`task-management.md`, `agents.md`, `spec-workflow.md`, `session-management.md`) should stay always-loaded.

### Option D: Defer

**Description:** Don't commit to an adoption path yet. Wait for a concrete use case (e.g., domain-specific pack request from a downstream project, or Skills API changes) before deciding.

**Strengths:**
- Zero risk of premature commitment
- Allows Skills feature to mature (it's documented but recently added; behavior may change)
- Keeps FB-033 in its current deferred state; consistent with "don't decide until you need to"

**Weaknesses:**
- Leaves a research finding stranded — the blocking question is answered; deferring doesn't generate new information
- FB-033 gets further blocked (FB-033 wanted to consider Skill vs. subagent for spec-auditor; deferring means the auditor decision has to re-open this question later)
- Kicks the same decision into the future without clarifying what would trigger a revisit

**Research notes:** Defensible if Erik prefers to see Skills used in another project first. Worth noting: deferring under a "gather evidence" framing means setting a concrete trigger (e.g., "revisit after the first downstream project using this template requests domain-specific behavior").

## Research Findings

### Q1: Context/memory semantics (primary concern)

**Skills inherit the caller's context.** The Skill's SKILL.md content is injected into the caller's message stream: *"When you or Claude invoke a skill, the rendered SKILL.md content enters the conversation as a single message and stays there for the rest of the session."* ([code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills.md))

**Subagents spawned from within a Skill DO get fresh context.** Subagents are isolated regardless of where they're spawned: *"Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions."* ([code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents))

**Implication for DEC-004:** A Skill that wraps a verify-flow orchestration would see the implementation context at the Skill layer, even if the verify-agent it spawns is fresh. This violates the "no implementation memory" guarantee that DEC-004 depends on. **Skills are not suitable for hosting verify flows or any orchestration requiring context isolation.**

### Q2: Invocation semantics

- **User invocation:** `/skill-name` (same as commands).
- **Auto-invocation:** Claude loads a Skill based on description matching current conversation context, unless `disable-model-invocation: true`.
- **`disable-model-invocation`:** Only controls auto-invoke. Does NOT prevent a Skill from being called explicitly, and does NOT prevent a Skill from spawning subagents. ([code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills.md))
- **Parameters:** Skills support `$ARGUMENTS`, `$0`, `$1` like commands.

### Q3: Distribution / template-ownership

- Skills ship the same way commands do: `.claude/skills/` directory in the template.
- Required file: `SKILL.md` at the skill's root. Optional supporting files alongside.
- Discovery is identical to commands (watched for live edits; auto-discovered at session start).

### Q4: Permissions / settings

- Skills inherit the session's permission context.
- Skills may declare `allowed-tools` in frontmatter to pre-approve tools during Skill execution. This is additive — it does not create a sandboxed scope or override parent permissions.
- No documented way to restrict a Skill's caller or limit invocation to a specific subagent.

### Q5: Known limitations and blockers

**Blockers for replacing orchestration logic with Skills:**
- Context inheritance (Q1) — any flow requiring fresh context cannot live in a Skill.
- Invocation control is coarse — no "this Skill is only callable by the orchestrator."

**Not blockers for reference content:**
- No size limits that would affect typical reference docs.
- No documented reliability issues with description-based auto-invocation for well-scoped descriptions.

**Open docs gaps:**
- Token overhead of Skill auto-invocation (description-matching cost) not quantified.
- Compaction interaction when a Skill spawns a subagent that is later resumed.

### Cross-cutting note on FB-033

Research answers FB-033's embedded question: **spec-auditor must be a subagent, not a Skill.** The spec-auditor's value is adversarial review with no implementation memory. A Skill cannot provide that isolation. This applies regardless of which option is selected here.

## Your Notes & Constraints

*Add any constraints, preferences, or context that should inform this decision.*

**Constraints:**
- Template-maintenance decision record — ephemeral, removed after resolution
- DEC-004 subagent capability contract is load-bearing; any Skill adoption must not compromise verify-agent isolation
- FB-033 currently depends on this decision (for the Skill-vs-subagent question); that part is answered regardless of option

**Research questions for the user:**
1. **Reference migration scope (Option B):** If Option B is chosen, which reference docs are the first candidates? Starter set suggested: `spec-checklist.md`, `decomposition.md`, `dashboard-regeneration.md`. These are large (>500 lines) and not every-session relevant.
2. **Rules subset (Option C):** If Option C is pursued, which current rules are candidates for Skill migration? Suggested: `archiving.md`, `dashboard.md`, `decisions.md` (situational). NOT suggested: `task-management.md`, `agents.md`, `spec-workflow.md`, `session-management.md` (always-relevant).
3. **Downstream impact:** Would downstream projects using this template be affected by a Skills adoption? Skills are backward-compatible — projects that don't use them see no change — but if domain-specific packs were added, users would need to opt in.

## Recommendation

**Option B (reference-only adoption) is the safest first move.**

**Why B over the alternatives:**
- vs. **A:** Captures a real context-budget win with minimal work and easy reversibility. Validates the pattern.
- vs. **C:** Larger migration without validation data. If Option B proves the on-demand loading is as beneficial as expected, Option C becomes a follow-on decision with evidence behind it.
- vs. **D:** Deferring without a concrete trigger tends to leave decisions in limbo. The research is decisive on Q1 (the blocking concern); further waiting doesn't generate new info.

**Proposed first Skills:**
1. `decomposition-heuristics/SKILL.md` — on-demand loading during `/work` decomposition (currently `support/reference/decomposition.md` is cited but not pre-loaded, so this is a lateral move that validates the pattern)
2. `spec-checklist/SKILL.md` — on-demand loading during `/iterate`
3. `dashboard-style/SKILL.md` — on-demand loading during dashboard regeneration

Each is a thin wrapper over existing reference content, with description frontmatter tuned so Claude auto-invokes at the right moment.

**Explicitly out of scope under Option B (so FB-033 is clearly answered):**
- Orchestration logic stays in commands
- Verify flows stay in subagents
- Domain-specific packs (software/research/procurement/renovation) deferred to a future Option C revisit

**Confidence:** High on research (blocking concern definitively answered). Moderate on recommendation — Option B is conservative; a user who wants bigger gains faster might reasonably prefer Option C, but the migration load is larger and the research hasn't validated the rules subset empirically.
