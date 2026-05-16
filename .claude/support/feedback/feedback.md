# Feedback Log

Items are captured via `/feedback` and triaged via `/feedback review`.

---

## FB-006: Audit-findings dashboard/CLI workflow — courier pattern, dead UI, name burden, opacity

**Status:** ready
**Captured:** 2026-05-16
**Split:** 2026-05-16 — Original FB-006 split during `/feedback review` Phase 1. This item retains sub-issues 1-4 (dashboard/CLI workflow UX). Sub-issue 5 (Claude direct-edit guardrail) extracted to FB-007 because it is a behavioral/rule concern orthogonal to the UX rough edges and worth a separate assessment + promotion track.
**Refined:** 2026-05-16 — The audit-findings → feedback → spec-amendment workflow has four convergent UX rough edges that compound during triage: **(a) courier pattern** — dashboard tick is the only interactive element, but acting on ticks requires re-specifying state in the CLI (`/audit-coherence promote <name>`); user couriers the audit name from dashboard to terminal. **(b) name memory burden** — audit names (e.g. `coherence-2026-05-15-2337`) must be remembered or copy-pasted; especially painful when multiple audits have populated the dashboard. **(c) dead UI** — inline `[Promote to FB] / [Dismiss]` text per finding looks selectable but isn't; only the checkbox is interactive and it can only express promote-tick (unticked is ambiguous: not-yet-triaged vs dismissed). **(d) opacity at decision moment** — dashboard digest shows only short titles; full description lives in `findings.md` which the user must open separately; auto-routing via `/audit-coherence promote` doesn't surface plain-English at the moment of decision. User-stated requirement: "a simple description in plain English about what was found and what the issue is" *on the dashboard*, enough to triage without opening `findings.md`. Three candidate directions (not mutually exclusive): **(1) render-time consolidation** — drop dead inline text, expand each finding's dashboard entry to a one-line plain-English description, render audit name in one copy-paste-friendly header; **(2) single triage command** — `/audit-coherence triage` reads dashboard state and walks promote/dismiss interactively, eliminating name-memory; **(3) dual-checkbox column** — promote-tick vs dismiss-tick, removes implicit-state ambiguity. Implementation surface is template-owned (`commands/audit-coherence.md`, dashboard render rules in `rules/dashboard.md` + `support/reference/dashboard-regeneration.md`, audit digest format under `.claude/support/audits/<name>/`).
**Assessed:** 2026-05-16 — Scope: corrective + additive (dead-UI removal reductive; plain-English description per finding + triage command additive). Template files affected: `commands/audit-coherence.md` (digest synthesizer + possible `triage` subcommand), `rules/dashboard.md` + `support/reference/dashboard-regeneration.md` (audit-findings render rules), `skills/dashboard-style/SKILL.md` (section format), possibly `support/audits/<name>/digest.json` schema (`plain_english_description` field per finding). No decision conflicts — DEC-013 specified routing rules for findings, not the visual element shape; Direction 1's change to the `[Promote to FB] / [Dismiss]` inline text is compatible. Active follow-ups: precursor to deferred Audit family Stage 7 (bundled-apply batch UX); no interaction with Fix-eligible inline-apply expansion telemetry gate; no interaction with FB-011/FB-033/FB-060/FB-062/FB-063. Decision character: pick-and-go (no inflection). Version bump on promotion: likely sequenced as PATCH (drop dead-UI inline text alone) → MINOR (plain-English digest extension) → MINOR (`/audit-coherence triage` interactive walker) → MINOR-or-deferred (dual-checkbox column; depends on whether single triage command obsoletes the need). Promotion route: direct template change(s); no /research needed.

Surfaced live while working `coherence-2026-05-15-2337` finding C-01 in the styler project. User concerns, captured directly:

1. **Dashboard ticking is disconnected from the CLI follow-up.** On the dashboard the user can only tick boxes. To act on those ticks the user has to go to the CLI and re-specify what they want (`/audit-coherence promote <audit-name>`). The dashboard knows the audit name; the CLI also wants it; the user is the courier between them.

2. **Audit-name memory burden.** The user has to remember the audit name (e.g. `coherence-2026-05-15-2337`) when running the CLI command. Especially painful if more than one audit has populated the dashboard.

3. **"[Promote to FB] / [Dismiss]" inline text is dead UI.** Each finding renders "[Promote to FB] / [Dismiss]" next to its title. These look like options but aren't selectable — the only interactive element on the dashboard is the checkbox, and there's no way to express "dismiss" via the checkbox (ticking it = promote; not-ticking = ambiguous between "not yet triaged" and "dismissed"). The "[Dismiss]" text takes up real estate without offering function. (Promote text is also moot since the actual promote action is the CLI command at the bottom of the section, not the inline text.)

4. **Promotion is opaque.** The dashboard digest gives only a short title per finding. The full description lives in `.claude/support/audits/<name>/findings.md`, which the user has to open and read separately. And if a ticked finding auto-routes onward (e.g. into `/iterate` after `/audit-coherence promote`), the user doesn't see the plain-English description at the moment of decision. The user wants "a simple description in plain English about what was found and what the issue is" *on the dashboard* — enough to triage without opening the findings.md.

Possible directions for the broader dashboard ↔ CLI split (user has not chosen — starting points only):

- **Render-time consolidation:** drop the dead `[Promote to FB] / [Dismiss]` inline text; expand each finding's dashboard entry to include a one-line plain-English description (currently it's just a short title); render the audit name in one copy-paste-friendly header so the user reads it from one place
- **Single triage command:** `/audit-coherence triage` (or similar) reads the dashboard state, walks the user through promote/dismiss per finding interactively, and removes the need to remember the audit name
- **Add a second checkbox column** so the dashboard supports both promote-tick and dismiss-tick, removing the implicit-state ambiguity of unticked-vs-dismissed

### Context

Triggered while working audit `coherence-2026-05-15-2337` finding C-01 (Phase 28 `template/` prefix drift) in styler. The audit's path-drift evidence was largely stale (~40 claimed callsites → 0 bare-path matches in current spec, since Phase 28 implementation work had already swept them). The behavioral concern that surfaced in the same session — Claude running direct `Edit` calls on the spec instead of routing through `/iterate` — is extracted to FB-007.

### Related

Sibling capture FB-007 covers the Claude direct-edit guardrail concern that surfaced in the same C-01 session.

### Tags

audit-findings, dashboard-cli-split, workflow-friction, render-consolidation, triage-command

---

## FB-007: Claude direct-edit guardrail on `.claude/spec_v*.md` — rule tension between "direct edits safe" and audit `iterate_routing: /iterate`

**Status:** ready
**Captured:** 2026-05-16
**Split:** 2026-05-16 — Extracted from original FB-006 during `/feedback review` Phase 1. Sub-issue 5 of the original capture. FB-006 retains sub-issues 1-4 (dashboard/CLI workflow UX). This item carries the behavioral/rule concern about direct spec edits because (a) it's structurally independent — the rule tension exists regardless of whether the source is an audit finding, and (b) the implementation surface is `rules/spec-workflow.md` not `commands/audit-coherence.md`.
**Refined:** 2026-05-16 — Two rule sources are in direct tension. `.claude/rules/spec-workflow.md` says: "Direct edits to the spec are always safe — the decomposed snapshot preserves the before-state, and drift detection handles reconciliation." Audit findings declare `iterate_routing.target: "/iterate"` and the dashboard prose says "spec amendment via /iterate". When Claude judges audit evidence stale and decides to sweep residual drift inline, no rule explicitly intercepts. Observed in styler `coherence-2026-05-15-2337` C-01 session: Claude ran 5 direct `Edit` calls on `spec_v13.md` to sweep residual noun-drift (`Personalized principles` → `Archetype Principles`) before being challenged, then reverted via 5 more direct edits. Net spec state unchanged, workflow bypassed twice. Three structural alternatives (user has not chosen): **(1) explicit rule override** — spec/decision-file edits sourced from an audit finding's `iterate_routing` MUST route through `/iterate`, regardless of how small the change appears (rule-only, lightest, narrowest); **(2) size-based carveout** — distinguish "drift sweep <N lines" from "spec amendment requiring formal flow" (rule-only, lighter still but introduces a numeric threshold needing calibration); **(3) permission/hooks-layer gate** — intercept `Edit` calls on `.claude/spec_v*.md` for confirmation regardless of provenance (structural, heavier-handed, catches non-audit-sourced edits too — broader than the originating concern). Implementation surface is template-owned: `.claude/rules/spec-workflow.md` as primary; possibly `.claude/rules/agents.md` for behavioral framing adjacent to "Root Cause Over Symptom"; option (3) would touch `.claude/settings.json` PreToolUse hooks. Tension also exists with `.claude/rules/spec-workflow.md`'s "Propose-Approve-Apply" rule which already says infrastructure operations are autonomous-OK but spec text changes are user-facing — option (1) could be framed as a clarifying refinement of that existing rule rather than a new constraint.
**Assessed:** 2026-05-16 — Scope: corrective (sharpening implicit constraint to explicit). Template files affected: `rules/spec-workflow.md` (primary site for rule clarification); possibly `rules/agents.md` adjacent to "Root Cause Over Symptom" for behavioral framing; Option 3 (PreToolUse hook) would touch `.claude/settings.json` PreToolUse hooks on Edit/Write for `.claude/spec_v*.md` paths. Pre-existing structural enforcement (already in place): DEC-013 HARD RULE at `audit-coherence.md:394` routes spec-file findings to `kind: decision` → `[Fix it]` never modifies spec inline — this is the **audit-system** layer. FB-007's concern is at a **different layer**: Claude's general Edit-tool usage on spec files outside the audit fix-it flow. Pre-existing rule: propose-approve-apply already says spec changes need user approval; "infrastructure operations autonomous" carveout enumerates archiving/version transitions/frontmatter updates — substantive text edits not in the enumeration. FB-007 sharpens the implicit constraint. Decision conflicts: DEC-013 (supportive — extends same principle from audit-system layer to Claude's general behavior); propose-approve-apply pattern (Option 1 is a clarifying refinement of the existing rule, not a new constraint). Active follow-ups: closes a gap revealed by Audit family Stage 6 / DEC-013 — DEC-013 secured the audit-system surface; FB-007 secures Claude's general behavior on the same files. Decision character: borderline — Option 1 and Option 2 are pick-and-go; Option 3 (PreToolUse hook) is an inflection point with structural permission-layer impact. Three alternatives with materially different blast radii. Version bump on promotion: MINOR for Option 1 or 2 (rule clarification); MAJOR for Option 3 (PreToolUse hook is a permission-layer change). Promotion route: **/research → DEC-NNN** (per user disposition 2026-05-16) — three architectural alternatives warrant evaluation together rather than direct promotion of one. Active Follow-up entry added to root `CLAUDE.md` to trigger `/research` at next template-side session.

The captured concern, verbatim from FB-006 sub-issue 5:

**No Claude guardrail against direct spec edits.** Audit findings declare `iterate_routing.target: "/iterate"` and the dashboard prose says "spec amendment via /iterate". But `spec-workflow.md` says "Direct edits to the spec are always safe — the decomposed snapshot preserves the before-state, and drift detection handles reconciliation." These are in tension. In a live C-01 session, Claude judged most of the audit's evidence to be stale (path-drift swept in earlier work) and ran 5 direct `Edit` calls to sweep the residual noun-drift before being challenged. The reverts also went through direct edits. Net spec state was unchanged, but the workflow was bypassed twice. Possible directions:

- An explicit override clause: spec/decision-file edits sourced from an audit finding's `iterate_routing` MUST route through `/iterate`, regardless of how small the change appears
- A carveout that distinguishes "drift sweep <N lines" from "spec amendment requiring formal flow"
- A permission/hooks-layer gate that intercepts `Edit` calls on `.claude/spec_v*.md` for confirmation (heavier-handed, but structural rather than rule-based)

### Context

Triggered while working audit `coherence-2026-05-15-2337` finding C-01 (Phase 28 `template/` prefix drift) in styler. Claude found the audit's path-drift evidence largely stale (~40 claimed callsites → 0 bare-path matches in current spec, since Phase 28 implementation work had already swept them) and made 5 direct `Edit` calls to sweep the residual Layer-2 noun-drift (`Personalized principles` → `Archetype Principles`). User challenged the bypass; Claude reverted via 5 more direct Edits. Net change to `styler/.claude/spec_v13.md`: zero — but the workflow was bypassed twice.

### Related

Sibling capture FB-006 covers the dashboard/CLI workflow UX rough edges (sub-issues 1-4) that surfaced in the same session.

### Tags

spec-edit-guardrails, claude-behavior, rule-tension, audit-iterate-routing, hooks-layer-gate, propose-approve-apply
