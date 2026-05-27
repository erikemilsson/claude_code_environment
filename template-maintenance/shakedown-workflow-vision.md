# Shakedown Workflow — Vision Doc

**Stage:** RESOLVED via `/grill` (2026-05-27) — see Resolution below. The open questions at the bottom were the grill targets; all are now answered. The pre-grill exploration is preserved below as the record of how the conclusion was reached (it used the working name **"probe"**, retired in favor of **`/shakedown`**).

**Scope:** template-maintenance artifact (a candidate template command). Does NOT go through the `.claude/` project spec / `/iterate` workflow — that's for projects *using* the template.

**Provenance:** FB-093; research at `.claude/support/workspace/fb-093-research.md`; two styler CLI transcripts (2026-05-27). Mirrors the `/visual-verify` grill precedent (`template-maintenance/visual-verify-vision.md`).

---

## Resolution (post-grill, 2026-05-27)

**Outcome: build `/shakedown` as a new standalone command.** *Acceptance-by-example* — hold the envisioned product up to the full range of real use (typical paths + edge cases) and map where it delivers vs. falls short. The mirror of `/grill`: grill drills *down* to sharpen meaning; `/shakedown` sweeps *across* to test behaviour against the envisioned product.

The grill walked OQ2 → OQ1 → name → mechanicals. Locked decisions:

- **Calibrate is a required Phase 0 (resolves OQ2).** `/shakedown` opens with a *directed grill* — establish (1) what this session tests for, (2) the relevant parts of the system, (3) a non-thin lens — before any example. Silent self-calibration was **rejected**: it optimises against what's *salient*, not what *matters*, and a thin/misdirected lens only shows itself after sunk examples. A prior standalone `/grill` is optional enrichment, not the mechanism. *(This requirement is what killed the "probe is a lightweight self-calibrating sub-mode of grill" framing — you can't fold X into Y when X requires Y as a precondition.)*
- **Surface: standalone command (resolves OQ1).** Directed-grill Phase 0 → probe loop, in one invocation. Chosen over **(1)** a `/grill probe` sub-mode [overloads grill; stretches its "interrogate *me*" identity into "*I* assert, you verdict"] and **(3)** a two-command `/grill`→`/probe` pipeline [more steps, little gain since `/grill` already runs separately]. Earns its own surface on three grounds: the **inverse flow** (you assert → it verdicts), the **required directed-grill Phase 0**, and a **distinct durable artifact** grill never produces.
- **Name: `/shakedown`.** A *shakedown run* = take the new thing out, run it through real conditions, find what's not ready. "Probe" rejected (carries grill's *depth* connotation; this is *breadth*). "Scenarios" rejected (collides with `tests/scenarios/` + `test_protocol` — vocab drift).
- **Home: new `.claude/support/shakedowns/`** — one dated doc per run; the dir + a README ship with the template, the *contents* are project-generated (gitignored), mirroring `.claude/support/audits/`. Not `vision/` (wrong provenance), not `learnings/` (how-to-build, not what-to-build).
- **"Gold turn" contract:** per example → restate (+ flag if it forks) → break down against the lens → **ground against the actual system with a precise *why*** → verdict (base legend ✓/⚠/✗/❓, project-extensible like styler's 🎨) → write immediately. The grounding step is the non-negotiable that separates signal (*"it's a predicate over one item"*) from noise (*"seems hard"*).
- **Routing onward: suggested, not automatic.** Names the exit per verdict (⚠ → `/iterate` or `/research`; ✗ → out-of-scope/setting note; ✓ → optional `test_protocol` seed; Parked → backlog). Proposes; never writes spec itself (DEC-016).
- **Stop + steer, both encoded:** stop when new examples stop revealing dimensions (announce when close); proactively request the highest-signal next input (*"throw me a pairing rule — I bet that breaks the model"*).
- **Gating: ungated** (like `/grill`, `/diagnose`) — one-example-at-a-time interactivity is the safeguard; it writes only to its own doc.

**Next step → `/research` for a decision record.** A standalone new command + new artifact convention + new home dir is the hard-to-reverse, needs-documented-rationale, real-trade-off case (grill's own three ADR criteria). The DEC's job: preserve the `/grill`-vs-`/shakedown` boundary so it isn't re-litigated or accidentally folded, and be honest that the evidence base is **one deep styler run** (DEC-018's bar is usage evidence). Inputs for `/research`: this doc + `fb-093-research.md` + FB-093. Likely **DEC-019** (next in root `decisions/`).

---

## Problem

Large, long-running projects drift into "just building" — forward from the spec, without a live check on whether the thing being built actually does what the user wants. The spec says what was *intended*; the running product reveals what's *missing*. There is no structured way to **work backward from the built system** — to sit at the output, throw real and edge-case usage at it, and discover the boundary of what it can and can't express.

Styler hit this at the personal-style-rule engine: Erik couldn't tell, from the spec, which of his real style rules the engine could represent. The only way to find out was to *try them* — one at a time, against the actual rule model — and watch where the model broke. That probing produced, as a side effect, the clearest gap analysis and forward-direction artifact the project had.

**The gap in one line:** the template has `/grill` (sharpen what you *mean*) and `/iterate` (refine the *spec*), but nothing that **maps a built system's capability boundary by adjudicating the user's examples against it** — and nowhere durable to keep the resulting map.

## Core idea

A structured, multi-turn loop where **the user brain-dumps examples and the running/real system — not abstract reasoning — decides whether each is expressible**, accumulating a dated, snapshot-anchored capability map. Six phases:

0. **Calibrate the lens** — read the current system (spec + code + glossary); state back, *before any input*: the dimensions each example is decomposed against, the verdict legend, the cleave/heuristic, what trips a "new dimension" finding, the per-example output contract.
1. **Probe loop** (per example) — plain restatement (+ flag if it forks) → structured breakdown → **ground against the actual system** (expressible? *why not*, precisely? approximation, and does it flatten intent?) → verdict (✓ / ⚠ / ✗ / ❓ + project extras) → write the entry immediately (the doc is the persistence layer; survives `/clear`).
2. **Maintain the model** between examples — refine a shared "Model so far / Parked / Boundary criteria" as findings accumulate.
3. **Steer** — hypothesis-driven; request the highest-signal next input.
4. **Stop signal** — saturation: stop when new examples stop revealing new dimensions.
5. **Defer & route** — batch hard sub-questions to `/research`; surface forks with a recommendation + record the user's call; exit → distill → `/research` → `/iterate` → `/work`.

**The reframe that makes it worth a surface:** it replaces "reason about whether the system handles this" with "**adjudicate it against the system, and write down precisely why.**" The output is triple-duty — ✓ = acceptance probes, ⚠/✗ = gap analysis, Parked + boundary map = forward direction — and snapshot-anchored: *"where the system is and where I want it, as of date X."*

## Why this is distinct from what already exists

The UX cost of a new top-level command is real (FB-072 / DEC-018 declined a router; FB-085 folded `/visual-verify` into `/diagnose` rather than add surface). So the boundary has to be clean, or this folds into an existing command. The honest tension: **the probe overlaps `/grill` more than `/visual-verify` overlapped `/diagnose`** — it shares grill's host competency (interrogate-and-ground). What separates it is **flow direction**.

| | `/grill` (exists) | `/iterate` (exists) | vision docs (exist) | probe (proposed) |
|---|---|---|---|---|
| Flow | Claude asks → user answers | propose → approve → apply | pasted in from outside | **user asserts → Claude verdicts** |
| Purpose | sharpen *meaning* | refine the *spec* | pre-build *ideation* | map the *system's capability boundary* |
| Tense | pre-spec / mid-project | spec lifecycle | pre-build | **post-build, empirical** |
| Arbiter | shared understanding | user approval | — | **the actual system** |
| Output | sharper terms, `CONTEXT.md` | spec edits | a buildable input | a snapshot-anchored gap/acceptance/direction map |

`/grill` interrogates *you* to sharpen what you mean; the probe has *you* assert examples and grounds each against the system. Same discipline, opposite direction. **The open question (OQ1) is whether that inversion earns its own surface, or is best expressed as a second mode/recipe of `/grill` — which already scaffolds the probe's lens.**

## Hard constraints (grounded in existing rules — not up for grabs)

Grill the design *within* these.

- **Domain-agnostic.** The template serves software/research/procurement/renovation. Ship the *meta-protocol*; **derive the lens per-project at Phase 0**. The styler lens (mechanism/bite/direction/when/unless + ✓/⚠/✗/🎨/❓) is a *worked illustration*, never baked-in vocabulary. (Pattern: `/diagnose` ships a methodology; `decomposition-heuristics` ships a procedure + examples.)
- **Surface-discipline prior.** DEC-018 + the `/visual-verify`→`/diagnose` fold set the bar: *fold unless standalone is earned, and the bar is usage evidence, not novelty.* Current evidence is n=1 (styler).
- **The persistent doc needs a real home regardless of OQ1.** It is durable (multi-session, snapshot-anchored, triple-duty) — `workspace/` (where styler put it) is scratch and wrong for the end-state. OQ3 stands whatever OQ1 decides.
- **No direct writes to spec/decision/vision (DEC-016).** The probe *proposes and routes* (⚠ → `/iterate` or `/research`); it never edits the spec itself.
- **Gating follows the interactive-safeguard logic.** `/grill` is ungated because one-question-at-a-time interactivity is its safeguard; the probe's one-example-at-a-time loop is the same shape (OQ7).

## Open questions — the grill targets

Each has a provisional lean; all are unresolved.

1. **Surface: standalone `/probe` vs `/grill` sub-mode vs recipe-fold-into-`/grill` vs pattern-doc-only (no command).** *The governing fork.* — *Lean: grill-adjacent (sub-mode/recipe/pattern) over standalone, because the surface prior is strong and grill is the natural host — BUT the inverse-flow distinction is the real counterweight and could flip it. Walk it branch-by-branch; this is the whole point of the grill.*

2. **Is the calibrate-half (Phase 0) just `/grill` run first, or part of this capability?** In styler, a grill *scaffolded* the lens, then the brain-dump *ran* it. — *Lean: undecided, and it gates OQ1. If "calibrate = grill," the probe is literally grill's second half → fold strengthens. If the probe self-calibrates (the styler fresh session re-derived the lens from the doc, so it can), it's more self-contained → standalone strengthens. Resolve this before OQ1.*

3. **Where does the artifact live, and what is its type?** `.claude/vision/` sibling / new `.claude/support/probes/` / `.claude/support/learnings/` / workspace-graduate. — *Lean: purpose-built `.claude/support/probes/` — the artifact is distinct enough (empirical + snapshot-anchored + triple-duty) that piggybacking on `vision/` (wrong provenance) or `learnings/` (how-to-build, not what-to-build) muddies both. Downstream of OQ1.*

4. **What is the per-example output contract — i.e., what makes a turn "gold" vs noise?** — *Lean: enforce (a) grounding against the actual system with a precise* why *(not "seems hard"), (b) a fixed base verdict legend (✓/⚠/✗/❓) the project extends, (c) immediate write to the doc. The grounding step is the non-negotiable; abstract verdicts are the failure mode.*

5. **How much of routing-onward (Phase 5) is automatic vs manual?** ⚠ → `/iterate` or `/research`; ✗ → out-of-scope/toggle note; ✓ → seed `test_protocol`; Parked → backlog. — *Lean: manual/suggested, not auto-generated — the probe names the exit per verdict; the user fires `/iterate` / `/research`. Auto-emitting FB items is a maybe, deferred.*

6. **Stop signal + steering — encoded or emergent?** Is "stop when new examples stop revealing dimensions" + hypothesis-driven steering ("feed me a pairing rule next, I bet it breaks") a written instruction or left to model judgment? — *Lean: write both as explicit instructions; they're what kept the styler run productive and convergent rather than open-ended.*

7. **Gating (`disable-model-invocation`)?** — *Lean: leave ungated (like `/grill`) — interactivity is the safeguard, and autonomous fire isn't a foot-gun for a read-mostly probe. Moot if it folds into grill (inherits grill's status).*

8. **Family membership — does this wait for the deferred help-me-think umbrella?** `router-survey.md § 5` deferred a `/zoom-out`+`/grill`+`/diagnose` umbrella; FB-067 Wave 2 has `/prototype` + `/improve-codebase-architecture`. — *Lean: the probe is plausibly a member of that design/cognitive-support family; if so, deciding its surface in isolation may be premature. Grill whether OQ1 should be settled now or rolled into the umbrella question.*

## What success looks like (acceptance for the feature itself)

- A probe pass on a real system yields one doc that is simultaneously a usable gap analysis (⚠s become `/iterate` / `/research` items), a set of acceptance probes (✓s), and a forward-direction map (Parked + boundary) — without re-deriving the lens each time.
- The surface decision is **conscious**: either clearly distinct from `/grill`, or consciously folded — no third overlapping interrogation surface added carelessly.
- Phase 0 produces a lens that is legible and reviewable *before* probing starts.
- The probe converges (the stop signal fires) rather than running forever.

## Out of scope (initial)

- Continuing the styler brain-dump (different repo; not a template concern).
- Auto-*generating* examples — the user brain-dumps real ones; the probe adjudicates, it doesn't invent the corpus (mirrors `/visual-verify`'s "the loop verifies the contract, it doesn't invent it").
- The actual command/recipe/pattern artifact (depends on OQ1).
- Effectiveness-data collection (depends on whether a 2nd real run is wanted before deciding).

## Related signals

- **FB-093** — the capture; this doc is its grill target.
- **`.claude/support/workspace/fb-093-research.md`** — the option analysis behind every lean here.
- **`/grill` (FB-068)** — the inverse-flow sibling and the likely host; OQ1/OQ2 turn on the relationship to it.
- **Vision docs + `/iterate distill`** — adjacent artifact type + downstream consumer of the probe's ⚠s.
- **FB-072 / DEC-018 + FB-085 `/visual-verify` fold** — the command-surface discipline OQ1 must satisfy; the precedent for resolving a surface question *by grilling the design*.
- **FB-067 Wave 2 + `router-survey.md § 5`** — the deferred help-me-think umbrella; OQ8's family-membership question.
