---
id: DEC-019
title: New command /shakedown — standalone acceptance-by-example surface vs folding into /grill
status: implemented
category: architecture
created: 2026-05-27
decided: 2026-05-27
related:
  tasks: []
  decisions: [DEC-016, DEC-017, DEC-018]
implementation_anchors:
  - ".claude/commands/shakedown.md (new command)"
  - ".claude/support/shakedowns/README.md (artifact-home convention)"
  - ".claude/CLAUDE.md (Navigation + Environment Commands rows)"
  - ".claude/rules/spec-workflow.md § Workflow Cycle (working-backward pointer)"
  - ".claude/commands/grill.md § Where it fits (inverse-sibling cross-ref)"
  - ".claude/sync-manifest.json (README registered; commands/*.md glob auto-covers the command)"
  - ".claude/version.json (4.11.0); .claude/dashboard.md (META bump)"
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# New command `/shakedown` — standalone acceptance-by-example surface vs folding into `/grill`

## Select an Option

Mark your selection by checking one box:

- [x] Option A: New standalone `/shakedown` command (directed-grill Phase 0 → probe loop)
- [ ] Option B: `/grill probe` sub-mode (fold into `/grill`)
- [ ] Option C: Two-command pipeline (`/grill {topic}` → `/probe`)
- [ ] Option D: Pattern doc only (reference doc + `spec-workflow.md` pointer; no command)

*Check one box above, then fill in the Decision section below. This DEC formalizes a decision already walked branch-by-branch in a `/grill` session (2026-05-27) — the Recommendation is Option A; the selection is yours.*

## Background

CCE has `/grill` (interrogate the user to sharpen *meaning*) and `/iterate` (refine the *spec*), but no capability for **working backward from the built system** — sitting at the running/envisioned product, throwing real and edge-case usage at it one example at a time, and judging each against what the system *actually* does. Styler surfaced the gap: from the spec alone, the user couldn't tell which of his real personal-style rules the engine could express. The only way to find out was to *try them*, against the actual rule model, and watch where it broke. Two 2026-05-27 styler transcripts demonstrated the workflow end-to-end; it produced the clearest gap analysis + forward-direction artifact the project had. Captured as **FB-093**.

The activity is **acceptance-by-example**: hold the envisioned product up to the full range of real use (typical paths + edge cases), ground each against the system, and map where it delivers vs. falls short. The output is a dated, snapshot-anchored doc that is simultaneously a gap analysis (⚠/✗), a set of acceptance probes (✓), and a forward-direction map (parked items + boundary criteria). It is the **mirror of `/grill`**: grill drills *down* to sharpen what you mean; this sweeps *across* to test behaviour against the vision.

**Why this is a decision record (not just a ship).** A standalone new command + a new artifact convention + a new home directory is the *hard-to-reverse, surprising-without-rationale, real-trade-off* case — by `/grill`'s own three ADR criteria, and by the inverse of the reasoning that kept `/visual-verify` out of the command surface (FB-085: a trivially-reversible recipe-fold got **no** DEC; a standalone surface is the opposite). The governing precedent is **DEC-018**, which *declined* an interpretive router on command-surface-discipline grounds after a value deep-dive. This DEC must clear the same bar — and be honest that, unlike DEC-018 (which had 26 sessions of usage logs), the evidence here is **one deep styler run**. The DEC's durable job is to preserve the `/grill`-vs-`/shakedown` boundary so it isn't re-litigated or accidentally folded later.

**How this DEC was produced.** Not via a fresh research-agent investigation — the option matrix was walked interactively in a `/grill` of the design itself (the CCE-native move for surface decisions, exactly how `/visual-verify` was resolved). Re-investigating the surface choice with a fresh agent that lacked the grill's inverse-flow reasoning would only add noise. The research-agent-equivalent work lives in `.claude/support/workspace/fb-093-research.md` (pre-grill option analysis) and `template-maintenance/shakedown-workflow-vision.md § "Resolution (post-grill)"` (the grilled conclusions). The one genuinely-open residue — implementation/authoring feasibility — *was* freshly investigated against `.claude/support/reference/claude-code-authoring.md` (DEC-017); findings in Option A's Research Notes.

**Constraints carried in:**
- **Domain-agnostic.** The template serves software / research / procurement / renovation. Ship the *meta-protocol*; **derive the lens per-project** at the calibrate phase. The styler lens (mechanism/bite/direction/when/unless + ✓/⚠/✗/🎨/❓) is a worked illustration, never baked-in vocabulary.
- **DEC-016 preserved.** `/shakedown` *proposes and routes* (⚠ → `/iterate` or `/research`); it never writes spec/decision/vision text itself.
- **DEC-018 discipline.** New surface must justify itself; the recommendation is honest that value evidence is n=1.

## Options Comparison

Scores qualitative. Full reasoning in the grill resolution + research doc cited above.

| Criteria | A: standalone `/shakedown` | B: `/grill probe` sub-mode | C: pipeline `/grill`→`/probe` | D: pattern doc, no command |
|----------|----------|----------|----------|----------|
| Conceptual fit (inverse-flow coherence) | **Strong** — names the inverse activity; one home for the [grill→probe] arc | **Weak** — inverts grill's "interrogate *me*" identity into "*I* assert, you verdict"; one command hosts both flow directions | **Moderate** — clean, but the arc is split across two invocations | **Weak** — no named home; activity stays implicit |
| New command surface | +1 command (+ artifact dir + README) | **0** (mode of grill) | +1 command (`/probe`) + a handoff artifact | **0** (one reference doc) |
| `/grill` identity impact | **None** — grill unchanged | **Stretched** — grill now hosts an inverted mode + must own a corpus artifact it otherwise never produces | None | None |
| Directed-grill Phase-0 fit (the OQ2 requirement) | **Native** — Phase 0 built in, by cross-ref to grill's discipline | **Awkward / circular** — a "sub-mode" that still *requires* grill's directed interrogation as a precondition isn't a lightweight mode (you can't fold X into Y when X needs Y) | **Native** — the first command *is* the directed grill | **Unenforced** — a doc can describe the sequence but nothing runs it |
| Durable triple-duty artifact | **Owns it** — writes its dated doc in `support/shakedowns/` | grill must own an artifact outside its remit (scope creep) | `/probe` owns it — clean | **No owner** — artifact home unsolved |
| UX (invocation flow) | **Single invocation, continuous** | Single invocation (mode-switch within grill) | **Two invocations** + handoff | No invocation — "ask in plain language"; undiscoverable |
| Reversibility | **Moderate** — command + dir + convention; reversible but more than a recipe | **High** — delete the mode | Moderate — two commands | **High** — delete the doc |
| Overall | **Recommended** — coherent, single-invocation, self-contained, grill untouched; cost is +1 command on n=1 evidence | Cheapest surface, but overloads grill and the Phase-0 requirement makes "sub-mode" a misnomer | Clean separation, but worse UX (2 steps) for no gain over A | Cheapest, but undiscoverable and leaves the artifact home unsolved |

## Option Details

### Option A: New standalone `/shakedown` command — RECOMMENDED

**Description:** A new ungated command. **Phase 0** opens with a *directed grill* (cross-referencing `/grill`'s interrogation discipline) that establishes (1) what this session tests for, (2) the relevant parts of the system, (3) a non-thin lens — then states the lens back before any example. **Phases 1–5** run the probe loop: per user example → restate (+ flag if it forks) → break down against the lens → **ground against the actual system with a precise *why*** → verdict (base legend ✓/⚠/✗/❓, project-extensible) → write to the dated doc immediately; refine the shared model between examples; proactively steer toward the highest-signal next input; stop at saturation; route verdicts onward (suggested, not automatic). Domain-agnostic: the lens is derived per-project; the styler dimensions are illustration only.

**Strengths:**
- **Conceptually coherent** — names the inverse-of-grill activity with its own clean identity ("get interrogated" vs "stress the system with your examples"), so neither command's mental model is muddied.
- **The required directed-grill Phase 0 makes standalone the natural shape.** Because calibrate is mandatory (rejected silent self-calibration: it optimises against what's *salient*, not what *matters*, and a thin lens only shows itself after sunk examples), the workflow has grill as a *precondition/phase* — which is precisely what disqualifies the "lightweight sub-mode of grill" framing (Option B's circularity).
- **Owns its durable artifact** — a dated triple-duty corpus in `.claude/support/shakedowns/`, mirroring how `/audit-*` owns its output dir. Grill produces no such artifact, so housing it in grill would be scope creep.
- **Single continuous invocation** — Phase 0 → loop in one session; no two-step handoff (Option C's cost).
- **Leaves `/grill` untouched** for its existing uses (pre-distill enrichment, vocab repair).
- **Fully reversible if it underperforms** — it can be folded into `/grill` later exactly as `/visual-verify` was nearly folded; nothing here forecloses that.

**Weaknesses:**
- **Adds command surface** — the exact cost DEC-018 was vigilant about. Mitigated by: it's a genuinely distinct activity (not a convenience layer over an existing one), it's ungated so it doesn't add a foot-gun, and the artifact + home are net-new capability, not duplication.
- **Value evidence is n=1** (one deep styler run). Unlike DEC-018's 26-session probe, there's no usage corpus showing recurring demand across projects. This is the honest soft spot (see Recommendation confidence + Re-open condition).
- **Multi-session command** → must be authored compaction-safe and as standing patterns (see Research Notes); a real but well-precedented authoring constraint.

**Research Notes (implementation feasibility — the freshly-investigated residue):** Checked against `.claude/support/reference/claude-code-authoring.md`. **Buildable, no blocking hazards.** Key findings: (1) `/shakedown` runs at **orchestrator / main-conversation level** (like `/grill`, `/diagnose`), not as a dispatched subagent — so the subagent `.claude/`-write sandbox (DEC-004) does **not** apply and it can write its own `support/shakedowns/` doc + run the interactive loop. (2) Author the body as **standing patterns, not fire-once steps** (skill content persists for the session — same discipline `grill.md`/`diagnose.md` follow). (3) Keep the body **compaction-safe** (~10–15KB, under the 25K re-attachment budget; multi-session ⇒ compaction likely). (4) Embed Phase 0 **by prose cross-reference** to `grill.md § Process`, not duplication; do **not** rely on frontmatter `model:`/`effort:` for cross-turn behaviour (turn-scoped). (5) Ungated (`disable-model-invocation` OFF) is consistent with `/grill`/`/diagnose` — interactivity is the safeguard. Confidence: **high** on feasibility (platform-grounded); **moderate** on value (n=1, see below).

### Option B: `/grill probe` sub-mode (fold into `/grill`)

**Description:** No new command; `/grill` gains a third mode where, after its directed interrogation builds the lens, it flips to running the user's examples against it.

**Why not (summary):** Cheapest on surface (0 new commands) and the surface-discipline prior favours it — but it **inverts grill's core identity** (interrogation = Claude asks; probe = user asserts), forces grill to own a durable corpus artifact outside its remit, and — decisively — the mandatory directed-grill Phase 0 makes "sub-mode" a misnomer: a mode that requires grill's own interrogation as a precondition isn't lightweight, it's circular. Overloads one command with two flow directions and three modes. *Research note:* this was the original pre-grill lean; the OQ2 resolution (calibrate-is-required) is what moved it off the table.

### Option C: Two-command pipeline (`/grill {topic}` → `/probe`)

**Description:** Two distinct commands: run `/grill` to build/validate the lens (producing a scaffold artifact), then `/probe` to consume it and run examples.

**Why not (summary):** Clean separation and reuses grill's directed interrogation untouched — but it costs **two invocations + a defined handoff artifact** for no gain over Option A, which gets the same directed-grill calibration *inside* one continuous invocation. `/grill` already runs separately for anyone who wants to pre-build understanding, so the pipeline's separability is not a unique benefit. Strictly more steps than A.

### Option D: Pattern doc only (no command)

**Description:** Document the workflow as a reference doc + a `spec-workflow.md` pointer; invoke it "in plain language" with no dedicated command.

**Why not (summary):** Cheapest (0 commands) and the styler run did happen without a command — but undiscovered patterns don't get used, and the user's framing explicitly wants an *invocable* entry point. It also leaves the durable-artifact home unsolved (a doc-pattern neither creates nor maintains the corpus). Fails on discoverability + artifact ownership.

## Recommendation

*(Research-advisory — NOT a selection. You select via the checkboxes above.)*

**Recommend Option A (new standalone `/shakedown` command).** It was reached branch-by-branch in the design grill, walking OQ2 (calibrate-required) → OQ1 (surface) → name → mechanicals.

**Single most important reason:** the *required* directed-grill Phase 0 is what makes standalone the honest shape. Once calibrate-is-mandatory was settled (rejecting silent self-calibration), the workflow has grill as a precondition/phase — which structurally disqualifies the "lightweight sub-mode of grill" framing (you cannot fold X into Y when X requires Y as a precondition). Given that, Option A is the cleanest of the remaining shapes: one coherent invocation, owns its distinct durable artifact, leaves `/grill` untouched, and is fully reversible (fold-later stays available, à la `/visual-verify`).

**Confidence: moderate.** *High* on conceptual fit (the inverse-flow distinction is real and was pressure-tested in the grill) and on implementation feasibility (platform-grounded against `claude-code-authoring.md`). *Moderate* on **value** — the soft spot is the same shape as DEC-018's, inverted: DEC-018 had 26 sessions showing near-zero demand and declined; this has **one** deep styler run showing strong value but no cross-project corpus confirming recurrence. The recommendation is to build it anyway, because (a) unlike DEC-018's router, this is a *net-new capability*, not a convenience layer over an existing one — there's nothing it duplicates; (b) it's ungated and reversible, so the downside of being wrong is bounded; (c) the primary user lived the workflow and judged it valuable. But the n=1 caveat is real and bounds the claim to "worth building now," not "proven across projects."

**Relationship to the alternatives:** B is the surface-thrift option the prior would favour, defeated by the Phase-0-requirement circularity + grill-identity cost; C is strictly-worse UX than A; D fails discoverability + artifact ownership. None is a live competitor after the grill.

## Your Notes & Constraints

*This section is yours — Claude reads it but never overwrites it.*

**Constraints:**
-

**Research Questions** *(answers would sharpen the build or a follow-up):*

1. **Evidence bar.** Are you comfortable shipping on n=1 (one deep styler run), or would you rather gate the build on a 2nd real run (this template repo or another downstream project) — mirroring CCE's signal-gating discipline (FB-076/085)? (Recommendation: build now — it's net-new + reversible + you lived the value — but the gate is a legitimate alternative.)
2. **Artifact home name.** `.claude/support/shakedowns/` (dir + README ships; contents project-generated/gitignored, mirroring `support/audits/`) — confirm, or prefer a different name?
3. **Verdict legend base set.** Ship ✓/⚠/✗/❓ as the base, project-extensible (styler added 🎨)? Or a different base?

**Questions:**
-

## Decision

**Selected:** Option A — new standalone `/shakedown` command

**Rationale:**
Selected 2026-05-27, confirming the Recommendation and the `/grill` design resolution. The deciding logic: once *calibrate-is-required* was settled (Phase 0 is a mandatory directed grill), the workflow has grill as a precondition — which structurally rules out the "lightweight sub-mode of grill" framing (Option B's circularity). Of the remaining shapes, standalone is the cleanest: one continuous invocation, owns its durable triple-duty artifact, leaves `/grill` untouched, fully reversible.

On the evidence bar (Research Question 1): chose to **build now on n=1** rather than gate on a 2nd run. Unlike DEC-018's declined router, `/shakedown` is *net-new capability* (it duplicates nothing), ungated, and reversible — so the cost of being wrong is bounded (it can fold into `/grill` later, the inverse of this DEC). The primary user lived the workflow on styler and judged it valuable; deferring a net-new, low-footprint, reversible capability buys little when the downside is already bounded. The n=1 caveat is acknowledged and carried in the Re-open/down-grade condition.

## Trade-offs

*(Advisory, reflecting the recommended Option A — confirm on selection.)*

**Gaining:**
- A net-new capability: working backward from the built product to map its capability boundary, in a single coherent invocation that owns a durable, snapshot-anchored, triple-duty artifact (gap analysis + acceptance probes + forward direction).
- A clean `/grill`-vs-`/shakedown` boundary (interrogate-me vs stress-the-system), documented so it isn't re-litigated.

**Giving Up:**
- One new top-level command (the DEC-018 surface cost) — accepted here because it's net-new, ungated, and reversible, not a convenience layer over an existing command.
- Certainty that the demand recurs across projects (n=1 evidence) — bounded by the Re-open/down-grade condition below.

## Impact

**Implementation Notes (if Option A is selected):**
- New `.claude/commands/shakedown.md` — ungated; body as standing patterns; ~10–15KB (compaction-safe); Phase 0 cross-references `grill.md § Process` rather than duplicating it.
- New `.claude/support/shakedowns/` dir + `README.md` (artifact convention; dir + README ship, contents project-generated — mirror `support/audits/`, which carries **no** template `.gitignore` entry either; per-project gitignore is the project's choice). *(Shipped deviation from the original note's "add to `.gitignore`": followed the audits precedent — the template does not pre-ignore project-generated `support/` dirs.)*
- Integration: `.claude/CLAUDE.md` Navigation + Environment Commands rows; `spec-workflow.md` pointer (backward-from-built-product workflow); `agents.md` note if agents should read shakedown docs; the `/grill`↔`/shakedown` cross-references.
- `sync-manifest.json`: register `.claude/commands/*.md` (auto-covered) + the new `support/shakedowns/README.md`.
- `version.json` MINOR bump (new command surface); `dashboard.md` META `template_version`.

**Affected Areas:** new command file + new support dir; navigation/command-table edits; `/grill` cross-ref (one-line, non-breaking); sync-manifest + version.

**Re-open / down-grade condition:** if `/shakedown` sees little use across the next few projects, or its `/grill` overlap produces friction, fold it into `/grill` as a `probe` mode (Option B) or down-grade to a pattern doc (Option D) — the inverse of this DEC, and the same move `/visual-verify` took. Reversibility is by design.

**Risks:**
- **Low–moderate.** The main risk is the n=1 value bet; bounded by reversibility (fold-later) and ungated/low-footprint shipping. Secondary: authoring drift if the body isn't kept compaction-safe + standing-pattern-shaped — mitigated by the `grill.md`/`diagnose.md` precedent and the Research Notes constraints.
