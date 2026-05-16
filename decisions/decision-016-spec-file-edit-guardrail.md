---
id: DEC-016
title: Claude direct-edit guardrail on `.claude/spec_v*.md` — beyond audit-system [Fix it]
status: implemented
category: process
created: 2026-05-16
decided: 2026-05-16
implemented: 2026-05-16
related:
  tasks: []
  decisions: [DEC-013, DEC-005, DEC-008]
  feedback: [FB-007]
implementation_anchors:
  - .claude/settings.json
  - .claude/rules/spec-workflow.md
  - .claude/CLAUDE.md
  - .claude/sync-manifest.json
  - .claude/README.md
  - .claude/support/reference/extension-hooks.md
  - .claude/commands/health-check.md
inflection_point: true
spec_revised:
spec_revised_date:
blocks: []
---

# Claude direct-edit guardrail on `.claude/spec_v*.md` — beyond audit-system [Fix it]

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Explicit rule override in `.claude/rules/spec-workflow.md` — audit-sourced edits (edits whose origin is an audit finding's `iterate_routing`) MUST route through `/iterate`, regardless of how small the change appears. Rule-only; behavioral; narrowest scope.
- [ ] Option B: Size-based carveout in `.claude/rules/spec-workflow.md` — distinguish "drift sweep < N lines" (Claude may apply directly under propose-approve-apply) from "spec amendment requiring formal flow." Rule-only with a numeric threshold; lighter touch, calibration cost.
- [ ] Option C: PreToolUse permission-layer gate in `.claude/settings.json` — intercept `Edit` / `Write` calls on `.claude/spec_v*.md` paths (and possibly decision/vision paths) for confirmation regardless of provenance. Structural; permission-layer; broadest catch.
- [x] Option D: Composite (A + C) — A as the behavioral rule, C as the structural safety net (rule says "route through /iterate"; hook catches the violation if the rule is ignored). Belt-and-suspenders.

*Check one box above, then fill in the Decision section below.*

---

## Background

**Trigger:** FB-007 captured a tension between two rule sources, observed live in a styler `coherence-2026-05-15-2337` C-01 session.

The audit finding declared `iterate_routing.target: "/iterate"` and the dashboard prose said "spec amendment via /iterate". Concurrently, `.claude/rules/spec-workflow.md` says: *"Direct edits to the spec are always safe — the decomposed snapshot preserves the before-state, and drift detection handles reconciliation."* When Claude judged the audit's evidence largely stale (path-drift already swept in earlier work) and decided to sweep the residual noun-drift (`Personalized principles` → `Archetype Principles`) inline, no rule explicitly intercepted. Net result: 5 direct `Edit` calls on `spec_v13.md` before being challenged, then 5 more to revert. Net spec state unchanged; workflow bypassed twice.

**Existing structural enforcement (already in place — the gap FB-007 fills lies outside these):**

- **DEC-013 HARD RULE** (`audit-coherence.md:394`) — audit findings whose `files_to_touch` includes a spec/decision/vision path are auto-classified `kind: decision`; `[Fix it]` on `decision` kind routes to `/iterate` and never modifies the file inline. Two-point enforcement (synthesizer step 5 + post-synth sanity check), plus a third action-table gate. **This secured the audit-system layer for the inline-apply mechanism specifically.**
- **Propose-Approve-Apply pattern** (`rules/spec-workflow.md`) — "Present spec changes as explicit declarations (what changes, where, proposed text); apply only after user approval." Infrastructure operations are autonomous (archiving, version transitions, frontmatter updates); substantive text edits are NOT in the autonomous-OK enumeration.

**What FB-007 secures (the unprotected surface):** Claude's general `Edit`/`Write` tool usage on spec files **outside** the audit `[Fix it]` flow. DEC-013 closed the inline-apply surface from the audit family. FB-007 closes the broader behavioral surface. Sessions can still:

1. Decide audit evidence is partially stale and rationalize "I'll just sweep the residual inline" (the observed pattern).
2. Receive a user request that touches spec language without being formally framed as an `/iterate` proposal.
3. Run drift-detection-style cleanups inferred from `/work` or `/audit-coherence` output without going through any audit-system gate.

In all three, the rule that gets read says "direct edits are safe" — the audit-routing context provides no override unless Claude bridges the inference itself, which (per the live observation) it does not reliably do.

**The rule sources in tension** (verbatim from the template):

> `rules/spec-workflow.md`: *"Direct edits to the spec are always safe — the decomposed snapshot preserves the before-state, and drift detection handles reconciliation."*

> `commands/audit-coherence.md` (finding-routing prose) + dashboard digest annotations: *"spec amendment via /iterate"*

A reader of just one rule wouldn't notice the other. The behavior FB-007 observed is the predictable consequence of that gap.

**Three architectural shapes from FB-007's refined entry:**

1. **Explicit rule override** — clarifying refinement of propose-approve-apply: audit-sourced edits MUST route through `/iterate`, regardless of how small the change appears. Closes the specific scenario observed. Rule-only, behavioral, narrowest. May be insufficient if "audit-sourced" provenance is hard to track in practice or if the same rationalization recurs from non-audit contexts (case 2 + 3 above).

2. **Size-based carveout** — keeps "direct edits are safe" but adds a numeric threshold: drift sweep < N lines is treated as infrastructure-class and remains autonomously editable; larger changes require `/iterate`. Lighter than (1) because it preserves Claude's ability to do trivial sync-style sweeps without round-tripping. Calibration cost: N is hard to pick without empirical data. May invite "boil the frog" abuse — repeated sub-threshold edits accumulate.

3. **PreToolUse permission-layer gate** — `.claude/settings.json` `PreToolUse` hook that intercepts `Edit` / `Write` calls whose target matches `.claude/spec_v*.md` (and possibly `.claude/support/decisions/decision-*.md`, `.claude/vision/**/*.md`). The hook prompts the user before the edit lands, regardless of provenance. Heaviest of the three: structural rather than behavioral; catches every edit including non-audit-sourced ones (broader than the originating concern). **This option is an inflection point**: it's a permission-layer change with template-wide blast radius, not a rule-only clarification.

## Questions to Research

*(Answers in `## Research Findings` below — to be populated by research-agent.)*

1. **Is provenance trackable?** Option A's "audit-sourced" qualifier requires that Claude (or a hook, or the rule reader) can determine when an edit's origin is an audit finding. In current Claude Code (Opus 4.7, harness as of 2026-05), what mechanism (if any) tracks "this Edit was prompted by /audit-coherence" vs "this Edit was prompted by free-form user request"? If no provenance is trackable, Option A degenerates to "all spec edits route through /iterate" — broader than intended (effectively becomes Option C's behavioral equivalent without the structural enforcement).

2. **What's the right N for Option B?** Size-based carveouts work in some patterns (linter line-limit thresholds, diff-stat thresholds in CI). What's a defensible numeric threshold for "drift sweep small enough to apply directly"? Evidence sources: typical drift-sweep edit sizes in the styler / template-maintenance history; pre-existing thresholds in other parts of the template (if any); analogous patterns in other agent frameworks.

3. **PreToolUse hook precedent + feasibility.** Option C requires a working PreToolUse hook in `.claude/settings.json`. Does Claude Code currently support PreToolUse hooks that match on tool name + arg patterns (e.g., `Edit` on file paths matching `.claude/spec_v*.md`)? Cite Anthropic docs / GitHub issues / release notes. If hook support exists but with limitations (e.g., no path-pattern matching, hook can't access tool args), Option C's feasibility is materially affected. **This is the load-bearing technical question.**

4. **Blast radius of Option C.** A PreToolUse gate fires on every Edit/Write to the gated path. How many legitimate spec edits per project per month would the gate intercept (forcing user re-approval that's otherwise covered by propose-approve-apply)? Are there any current command flows (e.g., `/iterate apply`) where the gate would fire spuriously? How does the hook distinguish "legitimate /iterate-driven write" from "any other Edit on the spec"?

5. **Composite (Option D) — necessary or redundant?** If the rule clarification (A) is structurally sound AND the hook (C) is technically feasible, is the composite redundant or load-bearing? Belt-and-suspenders has a real cost (more friction, double-approve UX). Reference: DEC-013 used three-layer enforcement for HARD RULE (synthesizer step 5 + post-synth sanity check + action-table). What did each layer catch that the others didn't? Does that pattern generalize?

6. **Symmetric extension to decision records and vision documents.** DEC-013's HARD RULE covers spec + decision + vision uniformly. FB-007 phrased the concern only on `.claude/spec_v*.md`. Should the guardrail extend to `decision-*.md` and `vision/**/*.md` for symmetry? If yes, the rule/hook target widens (cheap on the hook side; needs explicit rule wording on the A side). If no, why is spec the asymmetric case?

7. **Interaction with `/iterate`'s own edits.** `/iterate` itself eventually writes the spec (at the apply stage of propose-approve-apply). A PreToolUse hook on spec files would also intercept `/iterate`'s legitimate writes. How is this exempted? Common pattern: hook-side allowlist for tool-call traces originating in `/iterate`, or session-stamped exemption. Implementation cost of the exemption + risk of the exemption being overly broad.

8. **Failure mode if the guardrail fails.** If Option A's rule is ignored (Claude rationalizes "this is just drift sweep") or Option C's hook misfires (allowing a spec edit through that shouldn't be), what's the worst case? The drift-detection reconciliation flow already exists per `rules/spec-workflow.md`. Is the guardrail preventing a class of *corruption* (semantic state divergence that drift detection can't catch), or just a *workflow infraction* (state ends up identical, but the audit trail is missing)? Severity calibration matters for the "is this worth the complexity" decision.

## Research Findings

*Full methodology and sources in `decisions/.archive/decision-016-research-2026-05-16.md`. Findings summarized per question below.*

### Q1: Is provenance trackable (audit-sourced vs free-form)?

**Finding: No — not at the permission-layer/hook-layer level.** Per [Claude Code permissions docs](https://code.claude.com/docs/en/permissions), permission rule syntax is `Tool` + path/argument specifier; there is no "invoking slash command" or "command source" specifier. Per the [hooks reference](https://code.claude.com/docs/en/hooks), the PreToolUse JSON input includes `tool_name`, `tool_input`, `cwd`, `permission_mode`, `session_id`, `transcript_path`, `tool_use_id` — but no field equivalent to "active slash command." (`UserPromptExpansion` hooks do receive `command_name` / `command_source` but they fire at prompt-expansion time, not at tool-call time — they can't directly gate Edit calls.)

**Implication for Option A:** "audit-sourced" can only be identified *behaviorally* by Claude itself reading the audit-routing context. Option A is therefore a behavioral rule clarification, not a structural enforcement — it depends on Claude reliably reading and applying the rule. The C-01 incident is direct evidence that the rule-only approach has a known failure mode: Claude read the audit's `iterate_routing: "/iterate"` annotation, rationalized "the evidence is partially stale, sweep the residual inline," and bypassed. The rule clarification fixes the *rule-source tension* (two contradictory rules, the wrong one wins) but doesn't add enforcement beyond Claude's own reading.

### Q2: What's the right N for Option B's size threshold?

**Finding: There is no defensible N.** The template has no existing size-based thresholds for edit-class autonomy — Propose-Approve-Apply uses *kind* (infrastructure operations vs substantive text edits), drift detection uses *section_fingerprint*, audit bundle-eligibility uses *file count* (≤3). The C-01 incident showed 5 small Edits (~10 lines total) bypassing the workflow — individually trivial, cumulatively material. Any threshold (N=1, 5, 10, %file) creates a boil-the-frog window. Industry analogues (Cursor, ESLint autofix) use *rule-class* / *fix-class* axes, not absolute line counts.

**Stronger framing:** the autonomy axis users want isn't size — it's *kind*. DEC-013 already established this axis for the audit family (ALL spec-touching findings → `kind: decision` → `/iterate`, regardless of size). Option B as proposed duplicates a less-precise version of work DEC-013 did better. **Recommend Option B be discarded.** If a kind-based carveout is desired, extend the existing Propose-Approve-Apply enumeration ("infrastructure operations — archiving, version transitions, frontmatter updates") explicitly — but that's a rule clarification, not a new threshold.

### Q3: PreToolUse hook precedent + feasibility (LOAD-BEARING)

**Finding: Option C is technically straightforward and materially simpler than initially framed.** The decision record's framing of Option C as "PreToolUse hook" overstates the implementation complexity. Three load-bearing platform mechanisms (per [Claude Code permissions docs](https://code.claude.com/docs/en/permissions)):

1. **Permission rule syntax supports `Edit(path-pattern)` / `Write(path-pattern)` directly** — gitignore-style globs work. A rule of the form `"Edit(.claude/spec_v*.md)"` correctly matches `spec_v1.md`, `spec_v13.md`, etc. relative to project root. **No custom hook required.**
2. **`ask` rules pre-empt the auto-mode classifier short-circuit.** Per the rule evaluation order (deny → ask → allow → classifier), an `ask` rule fires before any auto-mode approval — downstream users on auto mode (FB-026/DEC-008) still get prompted. The rule applies in addition to, not instead of, the classifier check.
3. **PreToolUse hooks remain available for richer logic** (custom messages, telemetry, conditional approval based on `tool_input` contents) — but for FB-007's stated goal (intercept and prompt on spec edits), the bare `permissions.ask` rule is sufficient.

**Simplest viable Option C: 2-6 lines of JSON in template-owned `.claude/settings.json`.** This is the same primitive DEC-005 / DEC-008 already use for `permissions.allow` — just using `ask` instead of `allow` for a path-glob. The implementation-complexity criterion in the comparison table drops from "medium-high" to "low."

```json
{
  "permissions": {
    "ask": [
      "Edit(.claude/spec_v*.md)",
      "Write(.claude/spec_v*.md)"
    ]
  }
}
```

Hook+rule interaction safety property (per the docs): "Hook decisions do not bypass permission rules. Deny and ask rules are evaluated regardless of what a PreToolUse hook returns." This means the permission rule layer is durable against hook misconfiguration.

Bypass conditions to be aware of: (a) `bypassPermissions` mode skips all prompts but is documented for isolated environments only; (b) managed-settings `allowManagedPermissionRulesOnly: true` would discard user/project `ask` rules — negligible concern for template's target audience.

### Q4: Blast radius of Option C

**Finding: Blast radius is narrow and easily mitigable. The "large" framing in the comparison table is overstated.** Audit of every command that could legitimately write to `.claude/spec_v*.md`:

- `/iterate apply` — the *only* legitimate spec-write path. Estimated cadence: 1-3 amendments per month per active project, 5-15 Edits per amendment → 5-45 raw prompts/month.
- `/work decomposition` — reads spec, writes tasks. **No spec writes.**
- `/health-check` Part 5 sync — `spec_v{N}.md` is in `sync-manifest.json` `ignore` category. **No spec writes.**
- `/feedback review` promotion — routes spec-touching items through `/iterate`. **No direct spec writes.**
- Audit `[Fix it]` — DEC-013 HARD RULE auto-classifies spec-touching findings as `kind: decision` → never inline-applies. **No spec writes.**

So the *only* legitimate spec-write path is `/iterate apply`, and the per-amendment cost is mitigated by Claude Code's platform-native **session-bounded "Yes don't ask again"** UX. Per the [permissions docs](https://code.claude.com/docs/en/permissions): for File modification tools, "Yes, don't ask again" persists "Until session end." User clicks once at the start of an `/iterate apply` session; subsequent Edits proceed without prompts; resets on next session.

**Net legitimate-flow cost: ~1 extra click per `/iterate apply` invocation, ~1-3 clicks/month per project.**

The comparison table's "blast radius beyond originating concern: large (every spec edit)" criterion should be revised to "small (one extra click per `/iterate apply` session)."

### Q5: Composite (Option D) — necessary or redundant?

**Finding: Option D is recommended — not redundant.** Each layer catches a failure mode the other doesn't:

- **Option A catches "Claude's intent should reflect the workflow contract"** (preventive). When the rule is unambiguous, Claude reads it and doesn't try the Edit in the first place — instead drafts an `/iterate` proposal. User experience: "Claude did the right thing on its own," no prompt at all.
- **Option C catches "Claude's intent was overridden by rationalization"** (corrective). When Claude reads "the audit's evidence is partially stale, sweep the residual inline" (the C-01 reasoning), the rationalization may win against the rule. The `ask` rule doesn't care about the rationalization — the Edit just prompts.

**Cost of belt-and-suspenders is small.** Unlike DEC-013's three-layer HARD RULE enforcement (which had real per-layer implementation cost), Option D's two layers are cheap individually (~5 lines of prose + ~6 lines of JSON) and don't compound their costs. The rule doesn't add prompts; the permission doesn't add prose.

**DEC-013 precedent supports the pattern.** The audit-system layer already uses three-layer enforcement (synthesizer step 5 + post-synth sanity check + action-table gate) for spec/decision/vision protection. FB-007 asks for the same pattern to extend to Claude's general behavior outside the audit family — Option D is the natural shape.

### Q6: Symmetric extension to decision records and vision documents?

**Finding: Recommend symmetric extension.** The asymmetry in FB-007 (spec-only framing) is likely accidental — captured what was *observed* (spec edit), not what was *at risk* (any of the three categories DEC-013 already protects on the audit-system side: `.claude/spec_v*.md`, `.claude/support/decisions/decision-*.md`, `.claude/vision/**/*.md`).

Costs of symmetric extension:
- For Option A: trivial prose extension — "spec, decision, and vision file edits MUST route through `/iterate` (or analogous flow per category)." Zero additional lines beyond the rule wording itself.
- For Option C: 4 additional path globs in the `ask` array. Total ~6-10 lines of JSON.

**Spurious-fire site to handle:** research-agent (this very agent class) writes to `.claude/support/decisions/decision-*.md` as part of its workflow. Under symmetric extension, every research-agent invocation prompts at first decision-write. Mitigation: same session-bounded "Yes don't ask again" UX as `/iterate apply` — one click per `/research` invocation. Acceptable cost.

**Vision docs** are user-pasted from outside Claude Code (per `rules/spec-workflow.md` — "Brainstorm in Claude Desktop, save to `.claude/vision/`"). The vision-path entries would intercept nothing in the normal flow; they only fire if Claude tries to edit an existing vision doc, which is exactly the bypass surface to protect.

### Q7: Interaction with `/iterate`'s own edits (exemption mechanism)

**Finding: Use platform-native session-bounded "Yes don't ask again" UX. No custom hook needed.** Per Q3 finding A2, `ask` rules pre-empt `acceptEdits` mode (so toggling `acceptEdits` inside `/iterate apply` would NOT exempt the prompts). The viable mechanisms are:

1. **Session-bounded "Yes don't ask again"** (recommended) — platform-native, 1 click per `/iterate apply`, resets per session.
2. Custom PreToolUse hook with `transcript_path` parsing to detect `/iterate apply` invocation — fragile, not recommended for v1.
3. Env-var-gated hook (e.g., `CLAUDE_ITERATE_APPLY_IN_PROGRESS=1` set by `/iterate apply`) — moderate complexity, available as upgrade path if user finds session-bounded UX too friction-y.

**Documentation surface:** `/iterate apply` setup notes should mention "the first Edit in this session will prompt; click 'Yes, don't ask again' to proceed."

### Q8: Failure-mode severity if the guardrail fails

**Finding: Low-to-medium per incident; compounds via audit-trail erosion.** Three severity classes:

- **Class A — Corruption (state diverges semantically without detection).** Drift detection's fingerprint-based approach catches gross changes but can miss subtle semantic shifts (e.g., "should" → "must" if word count preserved). Audit trail also lost. The guardrail prevents this class.
- **Class B — Workflow infraction (state ends up correct, audit trail missing).** The C-01 scenario: hit-and-revert leaves fingerprint identical, drift detection sees nothing, no `/iterate` proposal record explains the cleanup intent. Severity: low per incident; cumulative cost as audit-trail reliability degrades over time.
- **Class C — Pure cosmetic.** Negligible.

**Worst-case under each option:**
- Option A fails (Claude rationalizes past rule): Class B incident — exactly what C-01 was.
- Option C fails (user clicks through carelessly): Class B or A depending on review depth.
- Option D fails (both bypassed): requires simultaneous failure of two independent layers — residual.

**Worth-it calculation:** Option C is cheap (2-6 lines JSON, 1 click per `/iterate apply`); Option A is free (rule wording). Even at low per-incident severity, the cumulative audit-trail erosion + marginal implementation cost favor shipping the guardrail. Option D combines both at near-zero combined cost — favorable complexity-to-value ratio.

## Options Comparison

*Scores updated post-research. Q3 finding materially revised the implementation-complexity scores for Options C and D — the simplest viable Option C is a `permissions.ask` rule in template-owned `settings.json` (2-6 lines of JSON), not a custom PreToolUse hook script. Q4 finding materially revised the blast-radius scores — only `/iterate apply` legitimately writes spec, and platform-native session-bounded "Yes don't ask again" reduces per-amendment friction to one click.*

| Criterion | A — Explicit rule override | B — Size-based carveout | C — Permission-layer `ask` rule | D — Composite (A + C) |
|---|---|---|---|---|
| **Provenance tracking required** | ✗ Yes (audit-sourced flag) — but Q1 finding: provenance NOT trackable at platform layer, so degenerates to "all spec edits" | ✓ No | ✓ No | – Yes (rule side only — same Q1 caveat as A) |
| **Catches non-audit-sourced edits** | ✗ No (rule-only, narrowed by "audit-sourced" qualifier per FB-007 framing) | – Partial (size threshold) — Q2: no defensible N | ✓✓ Yes (path-based, structural) | ✓✓ Yes |
| **Catches Claude rationalization bypass (C-01 scenario)** | ✗ No — rule-only depends on Claude reading & applying rule; C-01 demonstrated this fails | ✗ No — same dependence | ✓✓ Yes — `ask` prompt fires regardless of Claude's reasoning | ✓✓ Yes |
| **Calibration cost** | ✓ None | ✗ Yes (pick N — Q2: no defensible value) | ✓ None | ✓ None |
| **Permission-layer change (inflection)** | ✓ No | ✓ No | – Yes (inflection) — but Q3: same primitive as DEC-005/DEC-008 `permissions.allow`, just `ask` flavor | – Yes (inflection) |
| **Blast radius beyond originating concern** | ✓ Minimal (rule applies only when Claude reads it) | ✓ Small (size-gated) | ✓ Small — Q4: only `/iterate apply` legitimately writes spec; ~1-3 amendments/month per project | ✓ Small |
| **Friction added per legitimate edit (`/iterate apply`)** | ✓ None (rule clarification) | ✓ None (size-gated) | ✓ Session-bounded: 1 click per `/iterate apply` invocation (Q4 + Q7) | ✓ Same as C |
| **Composability with propose-approve-apply** | ✓✓ Clarifies existing rule (extends "infrastructure operations" enumeration's implicit scope) | – Extends with numeric threshold — different axis | ✓ Orthogonal (permission-layer; rule unchanged) | ✓✓ Clarifies rule + adds structural safety net |
| **Implementation complexity** | ✓✓ Low (~5 lines of new prose in `rules/spec-workflow.md`) | ✓ Low-medium (threshold + rule wording) | ✓ Low (~2-6 lines JSON in `.claude/settings.json`; Q3 reframing) | ✓ Low (sum of A + C) |
| **Reversibility** | ✓✓ Trivial (revert prose) | ✓✓ Trivial (remove threshold) | ✓ Easy (remove `ask` entry; downstream projects pick up on next sync) | ✓ Easy (remove either or both) |
| **`/iterate` exemption needed** | ✓ No (rule doesn't trigger prompts) | ✓ No | – Yes — but Q7: platform-native "Yes don't ask again" handles it (session-bounded for File modifications) | – Yes (same as C) |
| **Works under auto mode** (DEC-008 context) | ✓ Yes (behavioral) | ✓ Yes (behavioral) | ✓✓ Yes — Q3 A2: `ask` rules pre-empt auto-mode classifier short-circuit | ✓✓ Yes |
| **Symmetric to DEC-013 audit-system protection** | ✓ Easy to extend wording to decisions + vision (Q6) | – Same axis applies to decisions/vision but threshold not meaningful for them | ✓✓ Easy to extend with 4 more path globs (Q6) | ✓✓ Easy (sum of A + C extensions) |
| **Failure-mode severity if bypassed** | ✗ Class B (workflow infraction; audit-trail erodes over time) — Q8 | ✗ Class B or A depending on cumulative size | – Class B/A only if user clicks through `ask` carelessly (Q8) | ✓ Residual — requires simultaneous failure of both independent layers |
| **Preventive vs corrective coverage** | – Preventive only (rule-reading time) | – Preventive only (rule-reading time) | – Corrective only (tool-call time) | ✓✓ Both (Q5 — A preventive + C corrective) |

**Legend:** ✓✓ strong, ✓ acceptable, – neutral/conditional, ✗ weak, ✗✗ disqualifying. See research archive for evidence per cell.

## Per-option Summaries

### Option A — Explicit rule override

**What ships:** rule clarification in `.claude/rules/spec-workflow.md`. The "Direct edits to the spec are always safe" sentence is replaced (or qualified) with: spec edits sourced from audit findings' `iterate_routing` (or, in the recommended Q6 extension, ALL substantive spec/decision/vision text edits) MUST route through `/iterate` regardless of how small the change appears. The Propose-Approve-Apply rule's "infrastructure operations are autonomous" enumeration stays unchanged — archiving, version transitions, frontmatter updates still proceed without `/iterate`. Cross-reference added in `.claude/CLAUDE.md` § Critical Invariants pointing to the clarified rule.

**Costs:** template-side ~3-5 lines of new prose; sync-manifest unchanged; downstream pick-up via standard `/health-check` Part 5 sync. Zero new friction in Claude's behavior — the rule is read once per session via memory.

**Failure modes introduced:** none structurally — the rule is text. The known failure mode is the *existing* one: Claude may rationalize past the rule under audit-context pressure (C-01 pattern). The clarification reduces the surface area for this pattern (no more rule-source tension to weigh against), but doesn't eliminate it because there's no enforcement layer.

**What it doesn't solve:** the rationalization-bypass failure mode (when Claude reads the rule but reasons "this case is different"). The Q1 finding establishes that provenance is not platform-trackable, so the rule is purely behavioral — depends on Claude reliably reading and applying it. Acceptable as a minimum-change ship if the user treats FB-007 as a rule-source-tension issue rather than a structural enforcement gap.

### Option B — Size-based carveout

**What ships:** rule wording in `.claude/rules/spec-workflow.md` distinguishing "drift sweep < N lines" (Claude may apply directly under propose-approve-apply) from "spec amendment requiring formal flow" (must route through `/iterate`).

**Costs:** template-side ~5-10 lines of new prose including the threshold + worked examples; potentially a `/iterate` triage step that classifies a proposed sweep by size.

**Failure modes introduced:** boil-the-frog — repeated sub-threshold edits accumulate to material spec drift while each individual Edit stays "under the threshold." The C-01 incident itself was 5 single-token Edits totaling ~10 lines; whether any single value of N would have stopped it depends on the chosen N, but every value (N=1, 5, 10, % file) creates a window. Q2 finding: no defensible N — the autonomy axis users want is *kind*, not *size*, and DEC-013 already established the kind-based axis for the audit family.

**What it doesn't solve:** the same rationalization-bypass failure mode as Option A (rule-only, behavioral). Adds the boil-the-frog window on top. **Recommend Option B be discarded** in favor of either Option A (no threshold; rule wording only) or a kind-based extension of the existing Propose-Approve-Apply "infrastructure operations" enumeration.

### Option C — Permission-layer `ask` rule

**What ships:** `permissions.ask` entries in template-owned `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [ "Bash(git status:*)", ... existing entries ... ],
    "ask": [
      "Edit(.claude/spec_v*.md)",
      "Write(.claude/spec_v*.md)"
    ]
  }
}
```

With Q6's symmetric extension recommended:

```json
"ask": [
  "Edit(.claude/spec_v*.md)",
  "Edit(.claude/support/decisions/decision-*.md)",
  "Edit(.claude/vision/**/*.md)",
  "Write(.claude/spec_v*.md)",
  "Write(.claude/support/decisions/decision-*.md)",
  "Write(.claude/vision/**/*.md)"
]
```

Plus a one-line update to `.claude/CLAUDE.md` § Critical Invariants language ("`.claude/settings.json` is template-owned (base `permissions.allow` AND `permissions.ask` only)") clarifying that both kinds of template-set rules live in the same file. `/health-check` Part 5c boundary validation gets a corresponding update.

**Costs:** template-side ~6-10 lines of JSON in `.claude/settings.json` + ~1 line in `.claude/CLAUDE.md` + ~1 line in `health-check.md` Part 5c. Sync-manifest unchanged (`.claude/settings.json` already in `sync` category per DEC-005). Downstream pick-up via standard sync.

Per-amendment friction: 1 click per `/iterate apply` session at the first Edit; subsequent Edits in same session proceed without prompts via platform-native "Yes don't ask again" (resets per session). Total: ~1-3 extra clicks/month per active project for `/iterate apply` flow. Research-agent decision-writing flow (one click per `/research` invocation) handled by the same mechanism.

**Failure modes introduced:** if user habituates to clicking through `ask` prompts without review (a known UX risk for any frequent prompt), the structural protection degrades to "audit trail of the click." Mitigated by the fact that the prompt is infrequent (only fires on spec/decision/vision files, not general Edit calls).

`bypassPermissions` mode and managed-settings `allowManagedPermissionRulesOnly: true` would discard the rule — both are explicit user/admin opt-outs documented as such. Not vulnerabilities; user choices.

**What it doesn't solve:** purely corrective (catches the Edit at tool-call time, after Claude has already decided to try it). Doesn't change Claude's behavior at rule-reading time — if Claude tries to edit, it hits the prompt, but Claude's *intent* still needs the rule clarification (Option A) to recognize that `/iterate` is the right path. Without Option A, the corrective layer is the only signal; Claude may repeatedly try Edits and get repeatedly prompted, accumulating friction.

### Option D — Composite (A + C)

**What ships:** sum of Option A and Option C — rule clarification in `.claude/rules/spec-workflow.md` + `permissions.ask` entries in `.claude/settings.json` + CLAUDE.md Critical Invariants update + health-check Part 5c update.

**Costs:** sum of A and C costs — template-side ~3-5 lines of prose + ~6-10 lines of JSON + ~2 lines of cross-reference updates. Total ~15-20 lines of new content across 3-4 template files. Downstream friction: same as C alone (1 click per `/iterate apply` session) — A doesn't add prompts; C doesn't add prose.

**Failure modes introduced:** strictly minimal. Each layer catches the other's failure mode:
- A's rule-only weakness (Claude rationalizes past the rule) is corrected by C's `ask` prompt at tool-call time.
- C's purely-corrective weakness (Claude keeps trying Edits and accumulates click-through fatigue) is corrected by A's intent shaping at rule-reading time (Claude doesn't try Edits in the first place under normal flow).
- C's "user habituates to clicking through" risk is bounded by A reducing the rate at which prompts fire (since Claude routes through `/iterate` instead of trying Edits).

Residual: requires simultaneous failure of two independent layers — Claude both ignores the rule AND user clicks through the prompt without review. Highly unlikely.

**What it doesn't solve:** parallel-session edit collisions (DEC-013 Q5; same scope as DEC-013 — not in FB-007's surface). Transitive-consumer breakage on package.json-style edits (DEC-013 Q3; same scope as DEC-013 — not in FB-007's surface). Drift detection's known semantic-shift gaps (Q8 Class A residual) — the guardrail makes Class A harder to trigger but doesn't eliminate the underlying drift-detection limitation.

**DEC-013 precedent comparison:** DEC-013 used a three-layer enforcement pattern (synthesizer step 5 + post-synth sanity check + action-table gate) for the audit-system surface. Option D uses a two-layer pattern (rule clarification + permission `ask`) for the broader behavioral surface — appropriate because the audit-system has a structured pipeline with three distinct lifecycle stages to gate at, whereas Claude's general Edit-tool usage has only two natural gates (intent-shaping at rule-read time + tool-call interception). Same defense-in-depth philosophy; appropriate granularity for each surface.

## Recommendation

**Recommended: Option D — Composite (A + C).** Symmetric extension to decisions and vision (per Q6) included.

### Evidence base

1. **Q3 reframing changed the calculus.** The decision record's framing of Option C as "PreToolUse hook" overstated its complexity. The simplest viable implementation is a `permissions.ask` rule in template-owned `.claude/settings.json` — 2-6 lines of JSON, same primitive DEC-005/DEC-008 already use for `permissions.allow`. No custom hook script required. This drops Option C's implementation-complexity criterion from "medium-high" to "low" and makes the composite (Option D) cheap enough that there's no cost-driven reason to prefer A alone.

2. **Q4 narrowed the blast radius.** Audit of all spec-writing paths confirmed only `/iterate apply` legitimately writes the spec; `/work decomposition`, `/health-check` Part 5 sync, `/feedback review`, and audit `[Fix it]` (DEC-013 HARD RULE) all already route correctly. Platform-native session-bounded "Yes don't ask again" reduces per-amendment friction to one click. Total monthly cost: ~1-3 extra clicks per active project. The decision record's "blast radius: large" criterion is overstated — should be "small."

3. **Q5 confirmed A and C are not redundant.** Each catches a failure mode the other doesn't. A is preventive (Claude reads rule → routes through `/iterate` → no Edit attempted → no prompt). C is corrective (Claude rationalizes past rule → Edit attempted → prompt fires → user catches). DEC-013's three-layer precedent supports the layered-enforcement pattern for spec/decision/vision protection.

4. **Q1 disqualified Option A alone for the "audit-sourced" qualifier.** Provenance is not platform-trackable; "audit-sourced" can only be identified behaviorally by Claude. The C-01 incident is direct evidence that this behavioral path can fail. Option A alone is acceptable only if FB-007 is treated as a rule-source-tension issue, not a structural enforcement gap — but the C-01 evidence suggests it's the latter.

5. **Q2 disqualified Option B.** No defensible N; the autonomy axis users want is *kind*, not *size*; DEC-013 already established the kind-based axis better than any line threshold could. Discard.

### Confidence: High

The platform mechanisms underlying Option C (gitignore-glob in `Edit(path)` rules, `ask` rule pre-emption of auto-mode classifier, session-bounded "Yes don't ask again" for File modifications) are well-documented in current Claude Code docs and corroborated by DEC-005/DEC-008 internal precedent. Cost calculation favors Option D unambiguously over Option A or C alone, and overwhelmingly over Option B (discarded).

### Minimum-change alternative

If the user prefers the lightest-touch ship, **Option A alone** is acceptable — rule clarification only, no permission-layer change. Acknowledged limitation: Q1 finding establishes this depends on Claude reliably reading the rule (the precondition that failed in C-01). The path forward would be "ship A; if behavioral recurrence happens, ship C as a follow-up DEC."

This is the conservative ship. It avoids the inflection-point of touching the permission layer for now, at the cost of leaving the structural gap open. Acceptable if FB-007 is judged a one-time observation rather than a recurring pattern.

### Implementation surface (Option D)

Files to edit on promotion (would be a MAJOR bump per FB-007's "Version bump on promotion: MAJOR for Option 3" rationale, since Option C is the permission-layer inflection):

1. **`.claude/rules/spec-workflow.md`** — rule clarification. Either replace or qualify the "Direct edits to the spec are always safe" sentence; explicitly state that substantive text edits to `.claude/spec_v*.md`, `.claude/support/decisions/decision-*.md`, and `.claude/vision/**/*.md` MUST route through `/iterate` (or analogous flow per category). Keep the "infrastructure operations autonomously" carveout enumeration unchanged.
2. **`.claude/settings.json`** — add `permissions.ask` array with 6 path globs (Edit + Write × spec/decisions/vision).
3. **`.claude/CLAUDE.md`** — update Critical Invariants line to "`.claude/settings.json` is template-owned (base `permissions.allow` AND `permissions.ask` only)" and add a one-line cross-reference to the spec-workflow rule clarification.
4. **`.claude/commands/health-check.md`** Part 5c — update boundary validation to recognize `permissions.ask` as a template-owned key alongside `permissions.allow`.
5. **`.claude/commands/iterate.md`** (if it exists as a separate file) or `setup-checklist.md` — document the one-click exemption: "first Edit in `/iterate apply` session will prompt; click 'Yes, don't ask again' to proceed."
6. **`.claude/version.json`** — bump (MAJOR per FB-007 framing; user may choose MINOR if treated as a clarifying refinement rather than a breaking change).

Optional Q6 extension: include decision and vision globs in (2). Recommend including — symmetric with DEC-013's audit-system surface coverage, marginal extra cost.

*Add any constraints, preferences, or context that should inform this decision. This section is yours — Claude reads it but never overwrites it.*

**Constraints:**

- Option C is an inflection point per FB-007's framing — a permission-layer change is structurally heavier than rule-only clarification.
- The guardrail must not impede `/iterate`'s own spec writes (that's the point of `/iterate` — it IS the formal flow).
- DEC-013 already secured the audit-system surface for `[Fix it]`. DEC-016 secures the broader behavioral surface across all Claude `Edit`/`Write` usage on spec files.
- Spec-language rule clarification (Option A) is a clarifying *refinement* of the existing propose-approve-apply pattern, not a new constraint. That framing affects how the change reads to downstream-project Claude sessions.

**Preferences (none locked in yet):**

- The user's stated disposition at FB-007 capture: "open via `/research` → DEC-NNN to evaluate the three together" — i.e., this decision record is the intended evaluation surface; no implicit preference.

**FB-007 captured concern (verbatim, for the research-agent's reference):**

> No Claude guardrail against direct spec edits. Audit findings declare `iterate_routing.target: "/iterate"` and the dashboard prose says "spec amendment via /iterate". But `spec-workflow.md` says "Direct edits to the spec are always safe — the decomposed snapshot preserves the before-state, and drift detection handles reconciliation." These are in tension. In a live C-01 session, Claude judged most of the audit's evidence to be stale (path-drift swept in earlier work) and ran 5 direct `Edit` calls to sweep the residual noun-drift before being challenged. The reverts also went through direct edits. Net spec state was unchanged, but the workflow was bypassed twice. Possible directions:
>
> - An explicit override clause: spec/decision-file edits sourced from an audit finding's `iterate_routing` MUST route through `/iterate`, regardless of how small the change appears
> - A carveout that distinguishes "drift sweep <N lines" from "spec amendment requiring formal flow"
> - A permission/hooks-layer gate that intercepts `Edit` calls on `.claude/spec_v*.md` for confirmation (heavier-handed, but structural rather than rule-based)

## Decision

**Selected: Option D — Composite (A + C).** Confirms research-agent recommendation 2026-05-16. Symmetric extension to `.claude/support/decisions/decision-*.md` and `.claude/vision/**/*.md` per Q6 (user answer: yes). Version bump on promotion: MAJOR (user answer: major) — reflects FB-007's framing that permission-layer changes are a template-wide structural inflection.

**Rationale:**

- **Q3 reframing changed the cost calculus.** What FB-007 originally called "PreToolUse hook" is actually `permissions.ask` with gitignore-glob path matching — the same primitive DEC-005 / DEC-008 already use for `permissions.allow`, just `ask` flavor. Implementation drops from "medium-high" to "low" complexity. With Option C this cheap, Option D's composite shape is reachable at near-zero combined cost.
- **Q5 confirmed A and C catch different failure modes.** A is preventive (rule shapes Claude's intent so the Edit isn't attempted). C is corrective (the `ask` prompt fires when Claude rationalizes past the rule — exactly the C-01 pattern). DEC-013's three-layer precedent supports the layered-enforcement philosophy for spec/decision/vision protection.
- **Q1 disqualified Option A alone.** Provenance is not platform-trackable (`PreToolUse` JSON input has no slash-command-source field). "Audit-sourced edits MUST route via /iterate" degenerates in practice to "all spec edits" — which is Option C's behavioral semantics without the structural enforcement.
- **Q2 disqualified Option B.** No defensible numeric threshold; the autonomy axis users want is *kind*, not *size*; DEC-013 already established the kind-based axis better than any line threshold could.
- **Q4 narrowed Option C's blast radius.** Only `/iterate apply` legitimately writes spec files; platform-native session-bounded "Yes don't ask again" makes per-amendment cost one click. Total monthly friction: ~1-3 extra clicks per active project. The "large blast radius" framing in the original proposal was overstated.
- **Symmetric extension per Q6.** DEC-013 already protects spec + decision + vision uniformly on the audit-system side. The asymmetry in FB-007 (spec-only framing) was incidental — captured what was observed, not what's at risk. Extending Option C to all three categories costs 4 extra path globs and aligns the broader behavioral surface with the audit-system surface.

## Trade-offs

**Gaining:**

- Structural enforcement against substantive spec/decision/vision edits outside formal flows (`/iterate`, `/research`, vision-paste). Closes the rule-source tension between `spec-workflow.md` ("direct edits are always safe") and audit `iterate_routing: /iterate`.
- Two-layer defense-in-depth: rule clarifies Claude's intent (preventive); `permissions.ask` catches rationalization bypasses (corrective).
- Audit-trail preservation: every spec/decision/vision text change is either an `/iterate` proposal record OR an explicit `ask` prompt the user said yes to.
- Symmetry with DEC-013's audit-system protection across the three categories.
- Works under auto mode (`ask` rules pre-empt the classifier short-circuit).

**Giving Up:**

- One click per `/iterate apply` session at the first spec Edit (mitigated by platform-native "Yes don't ask again"; resets per session).
- One click per `/research` session at the first decision-record Edit (same mitigation).
- Template-owned `settings.json` now contains both `permissions.allow` AND `permissions.ask` — slight expansion of the "template-owned base" convention. Documented in `.claude/CLAUDE.md` Critical Invariants and Part 5c validation.
- MAJOR version bump reflects the inflection-point nature of touching the permission layer for the first template-wide guardrail. Downstream projects must explicitly accept the new `ask` rules on next sync (visible as a `permissions.ask` addition to `settings.json`).

## Impact

**Implementation Notes:**

Shipped in template_version 4.0.0 (2026-05-16), commit pending.

Files modified:

1. **`.claude/settings.json`** — added 6 `permissions.ask` entries (Edit + Write × spec/decisions/vision path globs).
2. **`.claude/rules/spec-workflow.md`** — added new section "Direct edits to spec, decision, and vision files (DEC-016)" after Propose-Approve-Apply. Removed the "Direct edits to the spec are always safe" line (the source of the FB-007 rule tension); the new section subsumes that claim with the routing requirement plus infrastructure-operations carveout.
3. **`.claude/CLAUDE.md`** — updated Critical Invariants: settings layering invariant now references both `permissions.allow` AND `permissions.ask`; added a new invariant pointing to the new spec-workflow section.
4. **`.claude/sync-manifest.json`** — updated `notes` field to reflect the expanded template-owned base set.
5. **`.claude/README.md`** — updated `.claude/settings.json` description to mention both base sets.
6. **`.claude/support/reference/extension-hooks.md`** — updated settings-layering reference line.
7. **`.claude/commands/health-check.md`** Part 5c — updated validation to accept `permissions.ask` as a template-owned key (removed it from the warn-list; updated drift-comparison to compare both arrays; updated rationale prose).
8. **`.claude/version.json`** — bumped 3.19.0 → 4.0.0 (MAJOR per user decision).
9. **`.claude/support/feedback/feedback.md` + `archive.md`** — FB-007 archived as `promoted` with reference to this DEC.
10. **`CLAUDE.md`** (root) — removed FB-007 from Shipped-queue follow-ups; added v4.0.0 to Recent ships.

**Affected Areas:**

- All downstream projects using the template will receive the new `ask` rules on next `/health-check` Part 5 sync.
- First Edit to a spec/decision/vision file in a session will now prompt (one click; "Yes, don't ask again" persists through session end for File modifications).
- Research-agent decision-writing flow (which writes `decisions/decision-*.md` in template / `.claude/support/decisions/decision-*.md` in projects) will prompt once per `/research` invocation; same one-click mitigation.

**Risks:**

- **User habituation to clicking-through.** Frequent prompts could degrade structural protection to "audit trail of the click." Mitigated by the fact that the prompts are infrequent (only fire on three specific path patterns, not general Edits) and that the rule clarification (Option A) reduces the rate at which Claude attempts these Edits in the first place.
- **`bypassPermissions` mode skips all prompts.** Documented for isolated environments only; user choice, not a vulnerability.
- **Managed-settings `allowManagedPermissionRulesOnly: true`** would discard the template's `ask` rules. Negligible concern for template's target audience (individual developers and small teams).
- **Downstream MAJOR-bump cost.** Projects pinned to template 3.x must explicitly opt into 4.x. Sync flow surfaces the new `permissions.ask` entries; user reviews and accepts.

**Future considerations:**

- **Telemetry passive observation.** Per Q4: count `permission_decision: deny` events in transcript logs (Anthropic provides hook-level telemetry) over 30-90 days post-ship to validate (a) the prompts fire on the right paths, (b) the user-friction per amendment matches the Q4 estimate (1-3 clicks/month per project). No new infrastructure needed.
- **Anthropic platform evolution.** If Claude Code adds a slash-command-source field to `PreToolUse` JSON input (currently a feature request), the rule clarification (Option A) could tighten from "all substantive edits" to "audit-sourced edits" — narrower scope. Re-open this DEC as a refinement if/when that platform change ships. No expected timeline.
- **Decision and vision write flows.** Currently both go through Claude's `/research` (decisions) and user-paste (vision). If a future flow needs autonomous decision/vision text edits, that's a separate DEC to revisit the carveout enumeration.
