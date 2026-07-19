---
id: DEC-017
title: Capability authoring doc + freshness mechanism (FB-082+083)
status: implemented
category: methodology
created: 2026-05-24
decided: 2026-05-24
decided_by: user
related:
  tasks: []
  decisions: [DEC-016]
  feedback: [FB-082, FB-083]
implementation_anchors:
  - .claude/support/reference/claude-code-authoring.md (NEW)
  - .claude/sync-manifest.json (register new doc in sync array)
  - .claude/CLAUDE.md (Navigation row)
  - .claude/agents/implement-agent.md (Editing strategy cross-ref)
  - .claude/rules/agents.md (cross-refs in State Ownership + Command Invocation Gates)
  - .claude/commands/iterate.md (distill/propose capability-claim cross-check)
  - .claude/commands/work.md (decomposition Pre-Pass cross-ref)
  - .claude/commands/health-check.md (new Part for capability-doc freshness)
  - .claude/skills/dashboard-style/SKILL.md (em-dash convention) — shipped v4.9.0; file later deleted by DEC-020 (skills trial concluded, mirrors retired). Convention lives on in support/reference/dashboard-regeneration.md
  - .claude/version.json (MINOR bump)
implemented_note: "Shipped v4.9.0 (2026-05-24). status: flipped approved → implemented 2026-07-19 during a maintenance housekeeping pass — the flag had been left at approved by oversight; 8 of 9 anchors verified present, the 9th intentionally removed by DEC-020."
inflection_point: true
spec_revised:
spec_revised_date:
blocks: []
---

# Capability authoring doc + freshness mechanism (FB-082+083)

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Footer-only (signal-only, no active validation)
- [x] Option B: Footer + `/health-check` capability-doc-freshness lens (manual at cadence)
- [ ] Option C: Footer + periodic WebFetch sync (auto sync at cadence)
- [ ] Option D: Footer + version-pinned + manual update at template-version bumps

*Check one box above, then fill in the Decision section below.*

## Background

Two FBs surfaced 2026-05-20–22 share a "design pattern only obvious after hitting a wall" shape and were bundled during 2026-05-24 triage:

- **FB-082** (template_maintenance/feedback-archive.md): YAML frontmatter `description:` field rejects unquoted `: ` (colon-space) under strict YAML 1.2 / PyYAML. Claude Code's deployment parser is permissive (silent runtime), but `verify-agent`'s strict YAML check fails. flirty-gym standardized on em-dashes (` — `) empirically across 5 SKILL.md files; no template-side documentation.

- **FB-083** (template_maintenance/feedback-archive.md): flirty-gym's spec claimed runtime model-switching as a feature of a multi-turn chat skill, on the assumption that SKILL.md `model:` frontmatter governs model selection across the full skill invocation. Per `code.claude.com/docs/en/skills` (verified during research): *"The override applies for the rest of the current turn and is not saved to settings; the session model resumes on your next prompt."* `model:` is turn-scoped, not session-scoped or skill-lifetime-scoped. A multi-turn chat skill cannot use that field for cross-turn model continuity. The mismatch survived spec authoring AND task decomposition.

Both are structurally the same class — claims about Claude Code platform behavior that don't hold under inspection, surfacing only after hitting a wall during implementation. Neither `/iterate` (spec hygiene), `/work` decomposition, `/audit-coherence` (spec-vs-code), nor DEC-016 (spec/decision/vision Edit/Write gate) catches them — they're all spec-vs-runtime-platform claims, structurally distinct from spec-vs-code or spec-vs-design.

This decision opens the freshness-mechanism scoping. The reference doc content (Need 1) is mechanical once the mechanism (Need 2) is chosen.

**Research artifact:** `.claude/support/workspace/fb-082-083-research.md` (matrix populated; recommendation = Option B with footer + `/health-check` lens combination).

## Options Comparison

| Criteria | Option A (footer only) | Option B (footer + lens) | Option C (footer + WebFetch sync) | Option D (footer + version-pin) |
|----------|------------------------|--------------------------|-----------------------------------|--------------------------------|
| Catches drift? | None alone (signal only) | Manual at cadence | Auto | Only when maintainer notices |
| False-positive risk | None | Low | High (silent contradiction with spec) | Very low |
| Implementation cost | Trivial (one line) | Low (new `/health-check` Part) | Medium (cron-like, or pre-`/iterate` hook) | Low (frontmatter field) |
| Maintainer burden | None | Medium (user spends a turn reviewing) | Low ongoing | High (track Claude Code releases) |
| Composability with reference doc body | Poor (no actor) | Excellent | OK (auto fires updates) | OK (paired with footer) |
| Failure mode | Silent staleness | Late discovery (≤90d cycle) | Spec/doc contradiction lands silently | Drift between maintainer-update gaps |
| User control over doc body changes | n/a | Full (adjudicates each diff) | None (auto-applies) | Full (manual update) |
| Overall | Cheap but blind | Active signal, manual gate | Auto-cadence, silent failure mode | Conservative, predictable, maintainer-dependent |

## Option Details

### Option A: Footer-only

**Description:** Add `<!-- Last verified against Claude Code docs: <URL> @ <YYYY-MM-DD>; against template_version: <X.Y.Z> -->` footer at the bottom of `claude-code-authoring.md`. No active mechanism — the footer is signal-only.

**Strengths:**
- Trivial implementation (one line)
- Structurally honest ("here's when we last checked; if docs have moved, this might be stale")
- Composes with everything (can be added to a future Option B/C/D)

**Weaknesses:**
- No active drift detection — the doc just goes stale silently
- Relies on user noticing the footer date and acting on it
- Worst-of-both: ships the visible accountability without the active mechanism

**Research Notes:** Recommended as the floor of any combination; rejected as standalone in research recommendation.

### Option B: Footer + `/health-check` capability-doc-freshness lens

**Description:** Footer (per Option A) + a new `/health-check` Part (likely 2d or 5e) that reads the footer date, warns if older than threshold (recommend 90 days), and offers `[V] Verify against current docs` action. The `[V]` action runs WebFetch on the docs URL + diffs body sections + presents changes for user adjudication. Manual confirmation preserves authority — the user decides whether each change should land.

**Strengths:**
- Active signal at predictable cadence (whenever user runs `/health-check`)
- User retains adjudication authority — no silent body updates
- Footer doubles as both staleness marker AND the input to the lens
- Composes with existing `/health-check` Parts pattern (8 parts shipped; this is part 9 or sub-part)
- WebFetch is invoked only when the user opts in via `[V]` — no surprise network calls

**Weaknesses:**
- Requires user to run `/health-check` periodically (already the existing convention)
- Threshold (90 days) is a tunable constant — calibration may need adjustment
- New Part adds surface area to `/health-check.md`

**Research Notes:** Recommended in research with this rationale: "footer is cheap and pairs with everything; lens is the active signal; WebFetch is invoked only when user opts in via `[V]` action — no silent network calls, no surprise updates."

### Option C: Footer + periodic WebFetch sync

**Description:** Footer (per Option A) + automatic WebFetch sync from `code.claude.com/docs` on a cadence (e.g., per-session at `/work` entry, or on every `template_version` bump). Auto-applies updates to the reference doc body.

**Strengths:**
- Always-fresh by construction
- No user effort required (automatic)
- Catches Claude Code platform changes the moment they ship

**Weaknesses:**
- **High false-positive risk** — synced doc may silently contradict the project's current spec. The drift surface moves from "spec vs Claude Code" to "spec vs synced doc vs Claude Code" — more layers, harder to audit.
- Auto-applied body changes can break spec assumptions that referenced the doc
- Requires WebFetch-on-every-cadence — visible network surface
- Failure mode is the worst (silent contradiction)

**Research Notes:** Rejected in research — *"The failure mode FB-083 named (synced doc silently contradicting current spec) is real and gets worse as the doc grows. Auto-sync's primary value (immediacy) is also its primary failure mode (no human in the loop to catch contradictions)."*

### Option D: Footer + version-pinned + manual update at template-version bumps

**Description:** Footer (per Option A) + bind the capability doc to a specific Claude Code version range; force an explicit update step on template-version bumps (PATCH/MINOR/MAJOR). Maintainer reviews + updates the doc body when bumping template version.

**Strengths:**
- Conservative and predictable cadence (driven by template release cycle)
- Avoids silent network calls
- Strong audit trail (every doc-body change tied to a template version)

**Weaknesses:**
- **Cadence unpredictable from doc's perspective** — Claude Code releases on its own schedule, template_version on a different one. The doc could be 3 months stale relative to Claude Code while the template hasn't bumped.
- Template has no current mechanism to pin against a Claude Code release version (only `template_version`)
- Requires maintainer to manually track Claude Code releases — high burden
- Doesn't scale to multiple downstream projects (each has its own template_version cadence)

**Research Notes:** Rejected as standalone in research — *"Requires maintainer to track Claude Code releases; the cadence is unpredictable; the template has no current mechanism to pin against a Claude Code release version."*

## Your Notes & Constraints

*Add any constraints, preferences, or context that should inform this decision. This section is yours — Claude reads it but never overwrites it.*

**Constraints:**
- (none — fill in if any)

**Questions:**
- Should the freshness threshold (Option B) be 90 days or different?
- Should the `[V] Verify` action diff the entire doc body or only specific sections?
- Should the lens be a new `/health-check` Part or fold into existing Part 2 (instruction-files audit)?

## Decision

**Selected:** Option B — Footer + `/health-check` capability-doc-freshness lens (manual at cadence)

**Rationale:**

Option B is the active-signal-with-user-adjudication route, which is correct for this concern:

1. **Drift detection at predictable cadence.** The `/health-check` lens fires whenever the user runs `/health-check` — already an established convention in the template. Footer date + threshold (90 days recommended) gives a structurally honest "this might be stale" signal.

2. **User retains adjudication authority.** Option B's `[V] Verify` action runs WebFetch on the docs URL + diffs against the current doc body + presents changes for user approval. The user decides which changes land. Option C's silent auto-sync would create the worst failure mode FB-083 surfaced — synced doc silently contradicting current spec ("spec vs synced doc vs Claude Code" — three-way drift instead of two-way).

3. **Composability with existing patterns.** Option B fits the existing `/health-check` Parts pattern (8 Parts shipped; this becomes Part 9 or a new sub-part of Part 2). No new file system surfaces; no new permission-layer mechanisms; reuses the user-confirmation flow.

4. **Failure mode is benign.** If the user ignores warnings, the doc just goes stale — which is the current state pre-DEC-017, so this is no worse than today. If the user dismisses `[V]` after diffing and not approving, the doc stays at its prior verified state — which is correct (no silent forward drift).

5. **Footer as the floor.** Option B includes the Option A footer as its visible accountability surface. Anyone reading the doc directly sees the verification date even if `/health-check` hasn't run recently.

Rejected paths:
- **Option A (footer only):** ships visible accountability without active mechanism. Worst-of-both — user sees the date but has no prompt to act.
- **Option C (WebFetch sync):** silent contradiction risk is structural, not tunable. The auto-sync's primary value (immediacy) is its primary failure mode. Rejected by research with explicit reasoning.
- **Option D (version-pinned):** cadence mismatch between Claude Code releases and `template_version` bumps. Maintainer burden high. No existing pinning mechanism to lean on.

## Trade-offs

**Gaining:**
- Active drift detection at predictable cadence (user-driven `/health-check`)
- User adjudication authority (no silent body updates)
- Visible footer accountability (current-state signal even without `/health-check` run)
- Composability with existing template patterns (`/health-check` Parts; user-confirmation flow)
- Lower false-positive risk than Option C (no silent contradictions)
- Lower maintainer burden than Option D (no Claude Code release tracking)
- A canonical home for capability/hazard facts that authors currently learn only by hitting walls

**Giving Up:**
- Auto-immediacy of Option C (Claude Code platform changes don't propagate to the reference doc until user runs `/health-check` + opts into `[V]` action)
- Predictability of Option D (cadence depends on user's `/health-check` rhythm; the threshold is a tunable, not a binding contract)
- Trivial-implementation cost of Option A (Option B requires new `/health-check` Part, ~30-40 lines)
- One new reference doc to maintain (cross-referenced by 9 files; cross-reference fragility on future refactors)

## Impact

**Implementation Notes:**

If Option B (recommended) selected, ship lands as ~10 files (one PR):

1. **`.claude/support/reference/claude-code-authoring.md`** — NEW. ~150-200 lines, 5 sections + footer:
   1. YAML Frontmatter Hazards (FB-082 fold-in)
   2. Skill Frontmatter Scope (turn-scoped `model:` / `effort:`; `disable-model-invocation`; `context: fork` + `agent:` pattern)
   3. Subagent Boundaries (no `.claude/` writes per DEC-004; no nested Task; no `permissions.allow` inheritance)
   4. Tool & Dispatch Surface (`Agent` tool `model` granularity; `subagent_type: "general-purpose"` portability; skill content lifecycle)
   5. MCP Constraints (pointer to `rules/agents.md § "MCP and Parallel Execution"` + `§ "MCP and Result-Size Constraints"`)
   6. Footer: `<!-- Last verified against Claude Code docs: https://code.claude.com/docs @ YYYY-MM-DD; against template_version: X.Y.Z -->`

2. **`.claude/sync-manifest.json`** — register `claude-code-authoring.md` in `sync` array.

3. **`.claude/CLAUDE.md § Navigation`** — add row pointing to new doc.

4. **`.claude/agents/implement-agent.md § "Editing strategy for structured documents"`** — one-line pointer to YAML Frontmatter Hazards section.

5. **`.claude/rules/agents.md`** — cross-references in `§ State Ownership` and `§ Command Invocation Gates` pointing into the new doc.

6. **`.claude/commands/iterate.md § distill/propose`** — one-bullet capability-claim cross-check before proposing spec text.

7. **`.claude/commands/work.md § Step 4 (decomposition)` or `decomposition.md`** — Pre-Pass row pointing to capability doc.

8. **`.claude/commands/health-check.md`** — new Part for capability-doc freshness (Part 2d or 5e); reads footer; warns if >threshold days; offers `[V] Verify` action.

9. **`.claude/skills/dashboard-style/SKILL.md`** — frontmatter authoring convention note (em-dash convention).

10. **`.claude/version.json`** — bump `template_version` (MINOR — new behavior surface, no breaking change).

**Estimated effort:** 4-6 hours (one focused session). Bulk of time is content writing for the new reference doc.

**Affected Areas:**
- New file: `.claude/support/reference/claude-code-authoring.md`
- Modified: `agents/implement-agent.md`, `rules/agents.md`, `commands/iterate.md`, `commands/work.md` or `decomposition.md`, `commands/health-check.md`, `skills/dashboard-style/SKILL.md`, `sync-manifest.json`, `CLAUDE.md`, `version.json`
- Related FBs: FB-082 (folds into Section 1), FB-083 (drives Sections 2-4 + freshness mechanism)
- Related decisions: DEC-016 (spec/decision/vision Edit/Write gate — orthogonal but complementary), DEC-005 (auto-mode classifier — capability claims are content not tool calls; classifier doesn't catch)

**Risks:**

- **Doc-body staleness despite lens.** If user dismisses warnings or `[V]` checks return false-negatives (e.g., Claude Code doc URL changes), staleness can persist. Mitigation: footer date is visible at the top of the doc; users encountering the doc see the staleness directly.
- **WebFetch failures.** `[V]` action requires network access; offline sessions can't verify. Acceptable failure mode (warning persists; next online run can act).
- **Threshold calibration.** 90 days may be too long (Claude Code ships features more frequently) or too short (false noise). Cheap to retune.
- **Cross-reference fragility.** 9 cross-references mean the doc is load-bearing; refactoring it requires touching 9 sites. Mitigated by the `sync-manifest.json` registration and the existing reference-doc maintenance pattern (`agents.md`, `task-schema.md`, `friction-register.md` all follow this pattern).
- **Interaction with future `/audit-coherence` capability-claim lens.** Research mentions deferring a new audit-coherence lens for capability-claim drift. If shipped later, it would consume the same reference doc as a source of truth — no conflict, but adds another cross-reference site.

## See Also

- `.claude/support/workspace/fb-082-083-research.md` — full research artifact with matrix, recommendation, and 6 open scoping questions
- `template-maintenance/feedback-archive.md § FB-082` + `§ FB-083` — original captures (archived 2026-05-24 via v4.8.0 promotion stubs; full content in archive)
- `.claude/rules/agents.md § "MCP and Parallel Execution"` + `§ "MCP and Result-Size Constraints"` — existing scattered capability constraints (NOT consolidating into new doc — cross-link only)
- `decision-016-spec-file-edit-guardrail.md` — sibling decision protecting spec/decision/vision files (DEC-016 is about Edit/Write gating; DEC-017 is about reference doc authoring grounding — orthogonal layers)
- `code.claude.com/docs/en/skills` — authoritative source for capability claims (verified during research; `model:` turn-scope quote at "The override applies for the rest of the current turn and is not saved to settings; the session model resumes on your next prompt")
