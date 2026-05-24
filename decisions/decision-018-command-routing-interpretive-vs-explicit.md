---
id: DEC-018
title: Command routing — interpretive router vs explicit-arg dispatch
status: approved
category: architecture
created: 2026-05-24
decided: 2026-05-24
related:
  tasks: []
  decisions: [DEC-005, DEC-016]
implementation_anchors: []
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# Command routing — interpretive router vs explicit-arg dispatch

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Interpretive router on `/iterate` (prototype-gated)
- [x] Option B: Status quo — explicit-arg dispatch everywhere
- [ ] Option C: Thin discoverability layer (no interpretive dispatch)

*Check one box above, then fill in the Decision section below. (The research-agent may add or rename options during investigation — selection happens only after the record reaches `proposed` and you review it.)*

## Background

CCE dispatches command sub-modes via **explicit string args**: `/iterate distill`, `/iterate hygiene`, `/work complete`, `/work pause`, `/feedback review`. Each multi-mode command grows its own file (`iterate.md` ~31 KB / 4 modes; `work.md` ~63 KB / many phases). Wave 1 added three more spec-adjacent commands (`/grill`, `/diagnose`, `/zoom-out`), increasing the surface users must remember.

FB-072 (captured 2026-05-20, during the FB-068 `/grill` ship review) asks whether some commands should become **interpretive routers** — dispatching sub-purposes from natural language rather than explicit args. The user's framing:

> *"From a UX perspective it is one more command to remember. I think we should look into making `/iterate` a router that routes to other commands depending on what is being asked. … I guess the larger question is how effective routing is at all, and perhaps that is something to do research on."*

A boundary survey (deliverable 1) was completed at `.claude/support/workspace/router-survey.md` (2026-05-20). It assessed five candidate umbrellas and reached a net recommendation: **prototype interpretive routing on `/iterate` only; keep `/work` and `/research` explicit; keep `/audit-*` menu-dispatched; defer the help-me-think umbrella.** Per FB-072's 2026-05-24 triage, this decision routes through `/research` so the research-agent **validates or extends** the survey's recommendation and produces this DEC-shaped output, rather than walking the survey's three decision points inline.

**The core question this DEC resolves:** which command-dispatch pattern should CCE adopt — and if interpretive routing, scoped to which command(s) and under what trial gate before full commitment?

**Constraints carried in from the survey:**
- The "announce-interpretation" safety surface is non-optional for any interpretive option (misclassification must cost ≤1 redirect, never a silent wrong action).
- FB-072 is explicitly **research-first AND prototype-first** — any interpretive option must carry a trial gate (≈10–15 real `/iterate` invocations across this repo + ≥1 downstream project, 4–6 weeks; thresholds ≥85% first-interpretation accuracy, ≤1 redirect/session) before the pattern is declared the default.
- Interaction with FB-071 (Command Invocation Gates) and DEC-016 (spec/decision/vision Edit/Write ask) must be preserved — see survey § "Cross-umbrella concerns".

## Options Comparison

Scores are qualitative (Strong / Moderate / Weak, or a short phrase). Confidence noted where it's not high. Full reasoning per criterion is in the research archive (`decisions/.archive/decision-018-research-2026-05-24.md`).

| Criteria | Option A (router on `/iterate`) | Option B (status quo) | Option C (thin pointer) |
|----------|----------|----------|----------|
| Classification accuracy / risk | **Moderate-Strong** — sub-modes have distinct lexical signals (distill / hygiene / "stress-test" / "the spec is fuzzy"); router mis-routes mainly on out-of-sample phrasing, which is the lowest-risk failure class | **N/A** — no classification; explicit arg is deterministic | **N/A** — no classification; user still invokes explicitly |
| Misclassification recovery cost | **Low** — router sits *upstream* of DEC-016's write gate, so a wrong sub-mode pick costs one redirect but cannot land a wrong spec edit (the write still needs approval) | **None** (no misclassification possible) | **None** |
| Discoverability gain | **Moderate, narrower than it looks** — native `/`-autocomplete already surfaces command *existence*; the genuine win is "say it however you want" (no need to learn the sub-mode token). Hidden-vocabulary-boundary is a partial offsetting cost | **Weak** — relies on `## Usage` + README + `/`-menu only | **Moderate** — closes the *sub-mode* discovery gap the `/`-menu leaves open + helps Desktop app (no autocomplete there); cheap |
| File-size / maintenance cost | **Moderate** — router preamble inline is small now (~41 KB after grill migration; ~46 KB with propose formalization), but the ~50 KB extract trigger is ~one sub-mode addition away → expect extraction near-term | **None** (no change) | **Low** — one short pointer file + doc edits; no command-logic change |
| Latency / token cost | **Low** — router pass ≈500 tokens; lives in the existing prompt, not a separate dispatch. Announce step is a natural turn boundary, avoiding 32K-budget contention with heavy sub-mode output | **None** | **None** (or one extra read of the pointer) |
| FB-071 gating interaction | **Neutral-positive** — one gate on `iterate.md` covers all sub-modes (same as today); *if* sub-modes later extract to per-file, each could carry its own gate (splits the currently-coupled gate — could be feature or friction) | **Neutral** — current per-command gates unchanged | **Neutral** — pointer is read-only discovery; gate it or not, no state impact |
| Reversibility | **High** — purely additive (explicit args keep working); revert = delete router preamble. Per-sub-mode kill-switch lets one bad classifier revert without condemning the router | **High** (it *is* the baseline) | **High** — delete the pointer file + doc lines |
| Overall | **Recommended, prototype-gated** — preserves all safety surfaces, adds a convenience layer, fully reversible; value (vs the hidden-boundary cost) is what the trial must prove | **Safe null** — zero risk, zero gain; the honest fallback if the trial fails | **Cheap complement** — addresses the real residual gap (sub-mode + Desktop discovery); not mutually exclusive with A |

## Option Details

### Option A: Interpretive router on `/iterate` (prototype-gated)

**Description:** `/iterate {natural language}` classifies intent → sub-mode (review / distill / propose / hygiene / grill), announces its interpretation before any substantive action ("I read this as a distill request — say 'no' to redirect"), and falls back to no-arg review when input doesn't lexically signal a sub-mode. Scope limited to `/iterate`; `/work`, `/research`, `/audit-*` unchanged. Ships behind a trial gate before being declared the default pattern.

Refined during research into four load-bearing properties (all fold into this one option; none changes the option set):

1. **Additive, not replacing.** Explicit args (`/iterate distill`) keep dispatching deterministically — a zero-ambiguity fast lane for users who know the token. The NL router is a *parallel* convenience path, not a replacement. This makes the change strictly safe (existing muscle memory unaffected) and the revert trivial.
2. **Scope-statement in the announce step.** When announcing an interpretation, occasionally list the alternative sub-purposes ("…other things I can do here: propose a change, run a hygiene cross-check, grill you on it"). Borrowed from the agentic-UX "Confidence Signal / Scope statement" pattern; turns the router into a teacher of its own boundary, closing the hidden-vocabulary-boundary discoverability cost.
3. **Announce-as-turn-boundary.** The announce step is a genuine response boundary (cheap turn); heavy sub-mode work happens in the next turn. Aligns with both the 32K output budget and the redirect-before-act safety design.
4. **Per-sub-mode kill-switch in the trial gate.** Track redirect rate *per sub-mode*; a single bad classifier (e.g., distill-vs-propose confusion) reverts to requiring its explicit arg without condemning the whole router.

**Inline vs extract (implementation sub-decision, not a separate option):** sub-modes stay inline in `iterate.md` first. Exact byte math: `iterate.md` is 31.6 KB today; migrating `/grill` (9.8 KB) inline → ~41 KB; formalizing `propose` as an explicit mode + router preamble → ~46 KB — i.e. the ~50 KB extract trigger is roughly *one sub-mode addition away*. Treat extraction as a near-term likelihood, not a remote contingency. Extraction is an orthogonal *file-organization* axis (you can have explicit-or-interpretive × inline-or-extracted independently); it interacts with FB-071 because a per-file `iterate-distill.md` could carry its own `disable-model-invocation` gate, splitting the gate that's currently coupled by living in one file.

**Invariant to preserve:** any sub-mode reachable by the router must retain an independent confirmation gate for irreversible actions (DEC-016 + propose-approve-apply). The router must never be the *only* thing between an interpretation and a write. Today all sub-modes satisfy this (distill/propose/hygiene end in propose-approve-apply; grill is interactive).

**Strengths:**
- **Preserves every existing safety surface while adding only convenience.** The router is upstream of DEC-016's `permissions.ask` and propose-approve-apply, so misclassification wastes a turn but cannot land a wrong spec edit. Validated by the agentic-UX Autonomy-Dial framework (classification = `Plan & Propose` level = cheap to get wrong; the write stays at `Act with Confirmation`).
- **Strong lexical separation between `/iterate`'s sub-modes** (distill / hygiene / "stress-test" / "the spec is fuzzy on X") → the LLM-router failure mode (out-of-sample phrasing) is the low-risk class here, not concept confusion.
- **Announce-interpretation is the documented industry pattern** ("Intent Preview" / "restate before acting" / "did you mean"), not a speculative mitigation — strongly corroborated externally.
- **Fully reversible and additive** — explicit args keep working; revert = delete the router preamble; per-sub-mode kill-switch contains blast radius during the trial.
- **FB-071-compatible** — one gate on `iterate.md` covers all sub-modes today; no regression.

**Weaknesses:**
- **Hidden-vocabulary-boundary discoverability cost.** An interpretive surface trades a *visible, learnable* boundary (the explicit arg, listed in `## Usage`) for an *invisible, inferred* one (which phrasings classify as which sub-mode). Announce-interpretation catches wrong *actions* but not wrong *expectations*; refinement #2 (scope-statement) partially mitigates but doesn't eliminate this.
- **The headline UX driver is partly already solved by the platform.** Native `/`-autocomplete surfaces command *existence* in the terminal, so "one fewer command to remember" is weaker than FB-072's framing; the genuine, narrower win is "say it however you want." The trial must show that convenience outweighs the hidden-boundary cost.
- **Adds an LLM classification pass** (~500 tokens) and a near-term file-extraction obligation (~one sub-mode away from the 50 KB trigger).
- **Value is unproven for this exact pattern** — external evidence is directional (Slack bots, generic LLM routers, agentic-UX principles), not a controlled study of interpretive routing on a spec-amendment command. Hence prototype-gated.

**Research Notes:** Primary inputs — `.claude/support/workspace/router-survey.md` § 1 + § "Cross-umbrella concerns"; full analysis + external evidence in `decisions/.archive/decision-018-research-2026-05-24.md` (§ 2 byte math, § 3.3–3.4 announce/recovery validation, § 4.4 agentic-UX framework, § 5.1–5.4 refinements). Confidence: **moderate** — high on the safety analysis (codebase-grounded + externally corroborated), moderate on the value analysis (discoverability benefit smaller than the original framing).

### Option B: Status quo — explicit-arg dispatch everywhere

**Description:** Keep the current explicit-arg pattern (`/iterate distill`, `/work complete`, etc.). Address the "one more command to remember" concern, if at all, through documentation only. No router, no interpretive dispatch.

**Strengths:**
- **Zero risk, zero new surface.** No classifier to mis-route, no hidden-vocabulary-boundary, no file growth, no new failure mode.
- **Deterministic dispatch** — `/iterate distill` always means distill; the user has full control and predictability.
- **Native `/`-autocomplete already provides command-existence discoverability** in the terminal (type `/i` → `/iterate` surfaces with its description), so the baseline is less impoverished than FB-072's framing implies.
- **It is the honest fallback** if Option A's trial fails — choosing B later costs nothing because B *is* the current state.

**Weaknesses:**
- **Does nothing for the original UX driver** — the user must still know the sub-mode token (`distill`, `hygiene`) and remember which spec-adjacent command to reach for. Sub-mode discovery in particular is unaddressed (the `/`-menu shows `/iterate` but not its args).
- **Surface keeps growing** — each Wave-2 command (`/tdd`, `/prototype`, etc.) adds another top-level entry, the exact accretion FB-072 flagged.
- **Forgoes a low-cost, reversible convenience** that the safety analysis shows can be added without relaxing any existing gate.

**Research Notes:** Survey § "Net recommendation" point 2 (the no-change baseline). The research did not surface any evidence that the status quo is *harmful* — only that it leaves a modest, addressable convenience/discoverability gap. B remains a fully legitimate choice if the user weights predictability and zero-new-surface over the convenience Option A offers. See archive § 4.5 (native autocomplete reframes the baseline) + § 7.

### Option C: Thin discoverability layer (no interpretive dispatch)

**Description:** Address the UX driver without interpretive classification — a `/help` or `/think` pointer (and/or a README grouping) that lists related commands *and their sub-modes* with one-line triggers. Users still invoke the specific command; the layer only aids discovery. Research narrowed C's real value: native `/`-autocomplete already covers command *existence* in the terminal, so C's residual contribution is (a) **sub-mode discovery** — enumerating that `/iterate` has distill/hygiene, and grouping the help-me-think family (`/zoom-out`, `/grill`, `/diagnose`) — and (b) **Desktop-app discoverability**, where there is no autocomplete at all.

**Strengths:**
- **Very cheap and fully reversible** — one short pointer file + doc edits; no command-logic change, no classifier, no file-size pressure.
- **Closes the genuine residual gap** the `/`-menu leaves open: sub-mode discovery and Desktop-app command discovery.
- **No hidden-vocabulary-boundary** — the boundary stays visible (it *lists* the explicit triggers).
- **Not mutually exclusive with Option A** — a scope/pointer doc complements a router (and Option A's refinement #2 is a lightweight, per-invocation version of the same idea).

**Weaknesses:**
- **Doesn't deliver the "say it however you want" convenience** — the user still types the explicit command/arg; C only helps them *find* it.
- **Partly redundant with the native `/`-menu** for command existence; its value is narrower than the survey originally implied.
- **Another artifact to maintain** (a `/help` pointer drifts as commands are added/removed) — modest, but real. Mitigated if it's a thin generated/short list rather than hand-curated prose.

**Research Notes:** Survey § 5 "Three options" (A standalone + B thin pointer). Research reframed C's value via archive § 4.5 (native autocomplete) + § 6 (C is distinct from B but narrower than implied). Because C and A address *different* parts of the problem (C = find it; A = say it loosely), they can ship together — the user may legitimately pick "C now, A after trial" or "A with C's scope-statement folded into the announce step."

## Recommendation

*(Research-agent recommendation — NOT a selection. The user selects via the checkboxes above.)*

> **Outcome (2026-05-24): the user selected Option B**, diverging from this recommendation after a value deep-dive (see § Decision below). This recommendation is preserved as the research-agent's advisory input; it did not carry the decision. The divergence is intentional: the research was high-confidence on Option A's *safety* but only moderate on its *value*, and the value probe (CCE's own usage logs) resolved that open question against adopting the router now.

**Recommend Option A (interpretive router on `/iterate`), prototype-gated** — confirming the boundary survey's net recommendation, with the four refinements folded into Option A's description (additive-not-replacing, scope-statement-in-announce, announce-as-turn-boundary, per-sub-mode kill-switch).

**Single most important reason:** the router sits *upstream* of CCE's existing irreversible-action gates (DEC-016 `permissions.ask` + propose-approve-apply), so a misclassification costs one redirect but **cannot** land a wrong spec edit. This is the precise mechanism behind the survey's "low recovery cost" claim, and it is corroborated by the agentic-UX Autonomy-Dial framework: classifying the sub-mode is a `Plan & Propose`-level decision (cheap to get wrong), while the spec write stays at `Act with Confirmation`. Option A adds convenience without relaxing any safety surface.

**Confidence: moderate.** High on the safety analysis (codebase-grounded + externally corroborated). Moderate on the *value* analysis — research found the discoverability benefit is smaller than FB-072's framing suggests (native `/`-autocomplete already solves command-*existence* in the terminal; the genuine win is "say it however you want," partly offset by a hidden-vocabulary-boundary cost). That value gap is exactly what a trial measures — which is why the recommendation preserves FB-072's prototype-first gate rather than recommending an immediate full commit.

**Relationship to the other options:**
- **Option C is a cheap complement, not a competitor** — it addresses *finding* the right command/sub-mode (including the Desktop-app gap, where there's no autocomplete); Option A addresses *not having to know the sub-mode token*. A legitimate path is "C now (cheap, safe), A after the trial proves the convenience is worth it" — or fold C's scope-statement into Option A's announce step (refinement #2) and ship one thing.
- **Option B is the honest fallback** if the trial fails — and costs nothing to choose later because it is the current state.

**On the survey's other four umbrellas: fully validated, no divergence.** Keep `/work` + `/research` explicit, keep `/audit-*` menu-dispatched, defer the help-me-think umbrella. The `/work` analysis is even stronger than the survey stated: `/work` already exposes a natural-language surface (`/work {request}`) that routes from *project state* (task status, decomposition state, dependencies) rather than user phrasing — which is correctly *more* reliable than word-based dispatch for an orchestrator. The general principle: interpretive routing fits commands whose sub-modes are **user-intent-distinct** (`/iterate`) and misfits commands whose sub-modes are **state-determined** (`/work`).

**Prototype-gate (carry forward from FB-072, with the research refinement):**
- Trial scope: ~10–15 real `/iterate` invocations across this repo + ≥1 downstream project, 4–6 weeks.
- Thresholds: ≥85% first-interpretation accuracy (treat as *directional* on a small sample), ≤1 redirect/session.
- **Added by research:** a **per-sub-mode redirect-rate kill-switch** (agentic-UX 5%-style per-task reversion metric) — more sample-size-robust and lets one bad classifier revert without condemning the router.
- If thresholds met → this DEC is selected/approved as Option A; if unmet → fall back to Option B (and optionally ship Option C).

## Your Notes & Constraints

*Add any constraints, preferences, or context that should inform this decision. This section is yours — Claude reads it but never overwrites it.*

**Constraints:**
-

**Research Questions** *(added by research-agent — answers here would sharpen a follow-up pass or inform your selection):*

1. **Trial denominator.** Is ~10–15 `/iterate` invocations enough to trust an 85% accuracy read, or should the gate widen toward ~25–30? (Research recommends treating 85% as directional + relying on the per-sub-mode redirect-rate kill-switch as the harder gate.)
2. **Grill migration coupling.** Option A's natural companion move is migrating `/grill` → `/iterate grill`. Do you want the prototype to (a) include grill-as-sub-mode from the start — accepting ~41–46 KB file size + likely near-term extraction — or (b) prototype the router on the existing four modes (review/distill/propose/hygiene) and defer grill until the router proves out? (Research recommends (b): smaller blast radius, cleaner accuracy signal; `/grill`'s standalone command keeps working as the dispatch target either way.)
3. **Discoverability honesty.** Given that native `/`-autocomplete already surfaces command existence in the terminal, does the "one fewer command to remember" motivation still feel compelling, or does the value re-center on "say it however you want"? (This reframing may change how you weight Option A vs Option C, and whether you want both.)

**Questions:**
-

## Decision

**Selected:** Option B — Status quo (explicit-arg dispatch everywhere)

**Rationale:**
Selected 2026-05-24 after a value deep-dive that went past the research archive's *structural* analysis into CCE's own *usage* evidence. The research established Option A is **safe** (high confidence) but only **moderate on value**. A follow-up empirical probe of the repo's 26 cross-project session exports (echothread, styler, SIREN, flirty-gym; ~May 14–22) settled the value question against A:

- **Zero** recorded instances of the friction Option A removes (no "which command/sub-mode," no "forgot," no "how do I run") across all 26 sessions.
- `/iterate` is used heavily but almost always **bare** (the propose/amend flow); the named sub-mode tokens (`distill`, `hygiene`) — the exact thing a router would let you reach via natural language — barely appear in real usage.
- Decomposed by segment, the value is **front-loaded-and-transient** (new-adopter onboarding, already partly covered by native `/`-autocomplete) plus **diffuse-and-unmeasurable** (think-out-loud fluency), while the costs (an LLM classification pass per NL invocation, the hidden-vocabulary-boundary, near-term `iterate.md` file extraction, ongoing maintenance) are **permanent-and-concrete**. Both sides are small; the asymmetry favors not adding the surface.

The primary user already knows the explicit tokens and uses bare `/iterate` fluently, so the headline "one fewer command to remember" benefit is near-zero for the actual audience. Option A remains a *correct, safe* design — it simply solves a problem the evidence shows CCE does not currently have.

*Caveats acknowledged (do not overturn the call, but bound it):* session exports are curated summaries, not raw transcripts, so sub-second micro-friction may be under-captured; the window is ~2 weeks; `distill` is a once-per-project (kickoff) event structurally under-sampled by mid-project logs. The decision is "not worth it **now**, for `/iterate` alone," not "never" (see Re-open condition).

## Trade-offs

**Gaining:**
- Zero new surface, zero new failure mode (no classifier to mis-route, no hidden-vocabulary-boundary), no file-size pressure on `iterate.md`, no per-invocation LLM-pass cost, no router/announce-step maintenance.
- Deterministic, predictable dispatch — `/iterate distill` always means distill.

**Giving Up:**
- The "say it however you want" fluency ergonomic (unmeasurable on paper; judged not worth a permanent cost given near-absent recall-friction in practice).
- The cheap-learning value a prototype would have produced about interpretive routing **as a pattern** for CCE's growing command surface — deferred, not foreclosed (see Re-open condition).

## Impact

**Implementation Notes:**
None. Option B is the current state — no code change, no `template_version` bump, no ship. Mirrors DEC-003 (selected option was the status quo; record stays `approved` with no implementation commit).

**Affected Areas:**
- None changed. `.claude/commands/iterate.md` keeps explicit-arg dispatch (`distill` / `hygiene` / no-arg review + embedded propose); `/grill` stays standalone; FB-071 gating, DEC-016, and propose-approve-apply are untouched.

**FB-072 disposition:** closed (decided against the interpretive-router proposal). The boundary survey (`.claude/support/workspace/router-survey.md`) and research archive (`decisions/.archive/decision-018-research-2026-05-24.md`) are preserved as the durable record. The `/walkthrough` / `/preflight` sibling idea folded into FB-072 during triage was not part of this decision and can be re-captured as its own FB if it resurfaces with signal.

**Re-open condition:** if Wave 2 (`/tdd`, `/prototype`, …) materially grows the command surface and "interpretive routing as a pattern" resurfaces as a live question, open a fresh DEC — DEC-018's option framing + the survey + the research archive are the starting point.

**Risks:**
- Minimal. The status quo carries the pre-existing, accepted condition that the command surface grows by one top-level entry per new command (the accretion FB-072 originally flagged). The Re-open condition above is the pressure valve if that accretion becomes painful.
