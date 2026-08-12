# Router Boundary Survey (FB-072)

**Status:** survey draft, awaiting user review
**Captured:** 2026-05-20
**Source:** FB-072 deliverable 1 — *"Boundary survey: for each candidate umbrella, list sub-purposes that would route through it; flag any that don't fit cleanly."*

---

## Background

FB-072 captures the question of whether some CCE commands should become **interpretive routers** (dispatch sub-purposes from natural language) rather than the current **explicit-arg dispatch** (`/iterate distill`, `/work complete`). The user's framing:

> *"From a UX perspective it is one more command to remember. I think we should look into making `/iterate` a router that routes to other commands depending on what is being asked. ... I guess the larger question is how effective routing is at all, and perhaps that is something to do research on."*

This document is **deliverable 1** of the FB-072 research-light track. Its job is to identify which candidate umbrellas have clean routing semantics before any prototype lands.

---

## Method

For each candidate umbrella:
1. Current shape (sub-modes, dispatch pattern, file size)
2. Routing trigger candidates (sample natural-language inputs → expected sub-mode)
3. Fit assessment (Strong / Medium / Weak) with rationale
4. Concerns + recommendation

Cross-umbrella concerns (accuracy, file size, latency, FB-071 interaction) at the end.

---

## Candidate umbrellas

### 1. `/iterate` — spec-source-of-truth umbrella

**Current shape (~31KB):**

| Sub-mode | Trigger | Purpose |
|----------|---------|---------|
| `/iterate` (no args) | default | Review spec, focus weakest area |
| `/iterate {topic}` | topic arg | Focus on a specific area |
| `/iterate distill` | `distill` literal | Extract buildable spec from vision document |
| `/iterate hygiene` | `hygiene` literal | Cross-check spec claims against project's structured artifact |

Propose-flow is *embedded* in the main review path (Step 4: Propose Changes); not a standalone sub-mode today, but conceptually it's one.

**Proposed additions surfaced by FB-072 / adjacent work:**

- `/iterate grill` — currently standalone `/grill`; could route here as a sub-mode
- `/iterate propose` — make the propose-flow an explicit sub-mode rather than embedded in review

**Routing trigger candidates:**

| User input (sample) | Expected sub-mode |
|---------------------|-------------------|
| "review the spec" / "what's weak in the spec?" | review (no-arg default) |
| "let's distill a buildable spec from this vision" | distill |
| "the spec is fuzzy on cancellation semantics" | propose (focused on cancellation) |
| "check the spec against the registry" | hygiene |
| "stress-test this plan" / "interrogate me on §40" | grill |
| "I want to nail down what we're building" | review or propose (clarification helpful) |

**Fit assessment: STRONG.**

All current and proposed sub-modes share a clear unifying purpose: **the spec as source of truth**. User naturally expresses intent in domain language ("the spec is fuzzy", "let's distill", "stress-test this"); the router's job is to map those to existing sub-flows. The sub-modes are mutually exclusive (one flow runs per invocation). Misclassification cost is low — wrong sub-flow can be redirected with one sentence.

**Concerns:**

- **File size growth.** `iterate.md` is ~31KB / ~700 lines covering 4 modes. Adding `grill` (now standalone ~8KB) + tightening `propose` would push past ~40KB. Two routes: (a) keep inline and lean on Claude's selective-read behavior, or (b) extract per-sub-mode files (`iterate-distill.md`, `iterate-propose.md`, …) with `iterate.md` as thin dispatcher. Recommendation: inline first; extract when file exceeds ~50KB.
- **Decision auto-finalization (Step 1a).** Already shared between `/iterate` and `/work` Step 2b. The router doesn't change this surface; it adds a routing layer at the top of the existing flow. No regression risk.
- **`{topic}` arg vs natural language.** The current `/iterate {topic}` shape is positional. If routing goes interpretive, the topic-focusing intent has to be inferred from the same input that picks the sub-mode. Mitigation: router announces interpretation + sub-mode + topic together. *"I read this as a propose request focused on cancellation semantics — proceeding."*

**Recommendation:** **Strong prototype candidate.** Ship interpretive routing here first.

---

### 2. `/work` — orchestration umbrella

**Current shape (~63KB):**

| Sub-mode | Trigger | Purpose |
|----------|---------|---------|
| `/work` (no args) | default | Auto-detect what needs doing |
| `/work {task-id}` | numeric arg | Work on specific task |
| `/work {request}` | natural language arg | Handle ad-hoc request |
| `/work complete [id]` | `complete` literal | Complete current or specific task |
| `/work pause` | `pause` literal | Graceful wind-down |

Sub-purposes embedded in single file (Steps 0-5 + Pause + Complete flows):

- Step 0a-0d: context restoration + recovery + friction-marker catchup
- Step 1a-1d: dashboard freshness + drift detection + spec state summary + non-actionable fast path
- Step 2-2c: spec check + decision gate + parallelism eligibility
- Step 3-4: action determination + execution (decompose / execute / verify / complete)
- Pause flow (~end of file)
- Complete flow (~end of file)

**Routing trigger candidates:**

| User input (sample) | Expected sub-mode |
|---------------------|-------------------|
| "what's next?" / no args | auto-detect (current default) |
| "complete this" / "mark T123 done" | complete |
| "I'm done for the day" / "wind down" | pause |
| "decompose §40.17 into tasks" | decompose phase (within Execute) |
| "implement T123" | execute phase |
| "verify T123" | verify phase |

**Fit assessment: WEAK.**

`/work` is structurally an orchestrator, not a router-friendly umbrella. The internal phases (Steps 0-5) aren't user-selected modes; they're orchestrator-internal sequencing that fires based on detected state. The user's explicit args (`complete`, `pause`) are minimal and already work well as explicit.

Interpretive routing here would:

- **Risk firing the wrong internal phase.** Interpreting "implement T123" as decompose when T123 is already decomposed would be a real foot-gun; current auto-detect handles this from task state, not user phrasing.
- **Duplicate auto-detect.** The no-args path already does interpretive routing from project state, not user words. Adding word-based routing on top would create two competing systems.
- **Obscure where the action surface is.** Today `/work complete` is a discoverable command; `/work "let's wrap up T123"` would be the same intent expressed three different ways. The complexity grows; the user's mental model doesn't simplify.

**Concerns:**

- The `/work {request}` shape *already* allows natural-language ad-hoc requests. That's the right router-shaped surface inside `/work` — but it routes to the existing orchestrator phases via state-based logic, not interpretive sub-mode dispatch. Working as designed.

**Recommendation:** `/work` stays explicit-arg. Auto-detect handles the no-args case. Out of scope for this router prototype.

(Separate question worth surveying: should `/work complete` and `/work pause` *split* into separate command files (`/work-complete`, `/work-pause`) for discoverability + reduced gating coupling? Independent of router architecture; tracked as a future refactor option in FB-071's sub-mode coupling note.)

---

### 3. `/research` and `/iterate` overlap

**Current shape:**

- `/iterate` (~31KB) — spec amendments. Output: spec changes.
- `/research` (~6.5KB) — investigates options for decisions. Output: decision records.

**Overlap:** both touch spec adjacency. A spec-amendment proposal often surfaces decisions that should be researched. A research investigation often produces decisions that should be reflected in the spec (post-decision /iterate suggestion via `/work` Step 2b).

**Routing trigger candidates (if unified):**

| User input (sample) | Expected sub-mode |
|---------------------|-------------------|
| "amend the spec to clarify cancellation" | iterate propose |
| "what are our options for retry strategy?" | research investigation |
| "the spec is fuzzy and I want to research how to nail it down" | both (sequence: research → iterate) |

**Fit assessment: WEAK as unified umbrella.**

The outputs are structurally distinct — `/iterate` modifies the spec file; `/research` writes a decision record. Unifying them would force the router to dispatch based on **output-type** rather than **input-language**, which is fragile (the user often doesn't know whether their question is "research" or "iterate" until the answer is found).

The handoff pattern (research → iterate) is already structurally present via `/work` Step 2b (post-decision check) and FB-078's refinement (chosen-option spec_impact detection, pending).

**Recommendation:** preserve the distinction; tighten the breadcrumb (research → iterate auto-suggestion when a closed decision has spec impact). Out of scope for this router prototype.

---

### 4. `/audit-coherence` and `/audit-ui`

**Current shape:**

- `/audit-coherence` (~47KB) — 6 lenses (superseded-decisions / vocab-drift / path-drift / feedback-decay / retired-features / friction-register)
- `/audit-ui` (~46KB) — N lenses (gaps / duplications / rambling / affordance / …)

Both already have sub-modes:

| Sub-mode | Available where |
|----------|-----------------|
| Default (run all lenses) | Both |
| `triage` (interactive walker) | Both |
| `promote` (turn findings → FB) | Both |
| `fix` (bundle-eligible only, DEC-013 Option C) | `/audit-ui` only |

Both already discoverable via `/health-check` Part 8 menu.

**Routing trigger candidates:**

| User input (sample) | Expected sub-mode |
|---------------------|-------------------|
| "audit my codebase for drift" | audit-coherence default run |
| "audit the UI" | audit-ui default run |
| "walk through the findings" | triage mode of whichever audit ran most recently |
| "fix the bundle issues" | fix mode (`/audit-ui`) |

**Fit assessment: SUFFICIENT AS-IS** (cross-command umbrella); **MEDIUM** (within-command routing).

**Cross-command umbrella `/audit "find drift"`:** worth considering only if `/health-check` Part 8 grows beyond comfortable scrolling. Today the menu surface is small (~2 entries); umbrella overhead doesn't pay back.

**Within-command interpretive routing (`/audit-coherence "walk through the findings"` → triage):** lighter refactor, doesn't cross command files. Possible later refinement; not the FB-072 prototype.

**Recommendation:** out of scope for this prototype. Surface only if Part 8 menu grows materially or if `/audit-*` modes acquire natural-language demand.

---

### 5. Help-me-think family — `/zoom-out`, `/grill`, `/diagnose`

**Current shape:**

| Command | Size | Shape | Gated? |
|---------|------|-------|--------|
| `/zoom-out` | ~3KB | Micro-command: broaden lens; consume `./CONTEXT.md` if present | Yes (per FB-070) |
| `/grill` | ~8KB | Interactive: branch-by-branch interrogation; auto-detects with-docs vs grill-me modes | No (interactivity is the safeguard) |
| `/diagnose` | ~10KB | Procedural: 6-phase methodology (feedback loop → reproduce → hypotheses → instrument → fix + regression test → cleanup) | No (autonomous fire is the feature) |

**Routing trigger candidates (if unified under `/help` or `/think`):**

| User input (sample) | Expected sub-mode |
|---------------------|-------------------|
| "I need broader context on this" | zoom-out |
| "interrogate this plan" / "stress-test this" | grill |
| "something is wrong, I don't know why" / "this test fails intermittently" | diagnose |

**Fit assessment: WEAK to MEDIUM.**

The three commands are **tonally cohesive** (user asks for cognitive support) but **operationally distinct**:

- `/zoom-out` is read-mostly, ~50 lines effective, fires once
- `/grill` is multi-turn, one-question-at-a-time, ~200 lines
- `/diagnose` is procedural with 6 sequential phases

The mental states don't blend cleanly: `/diagnose` is *"I'm stuck"*; `/grill` is *"I want to be challenged"*; `/zoom-out` is *"I'm too narrow"*. An umbrella might obscure rather than clarify.

**Stronger argument FOR umbrella:** discoverability. Three short commands are easier to forget than one umbrella with three sub-modes. New users see `/help` in the help text and stumble into the family naturally.

**Stronger argument AGAINST:** each command already has a sticky-enough name (zoom-out, grill, diagnose are mnemonic). Pocock's `/zoom-out` and `/diagnose` shipped as standalone in his repo and the names don't seem to cause discoverability issues there.

**Three options:**

A. **Standalone, status quo.** Keep three commands. Add a short "Cognitive support" mention to `.claude/README.md` Environment Commands table for discoverability.

B. **Thin pointer.** Add `/help` (or `/think`) as a non-routing pointer that lists the three with one-line descriptions and triggers. No interpretive dispatch; user reads + invokes the right one.

C. **Full umbrella.** `/help "interrogate me"` → grill; `/help "I'm stuck"` → diagnose. Interpretive dispatch.

**Recommendation:** **Defer.** Ship `/iterate` umbrella first. After 4-6 weeks of trial data, revisit help-me-think with the question *"did `/iterate` discoverability improve enough to justify the help-me-think umbrella too?"*. If yes, choose between B (thin pointer) and C (full umbrella); if not, stay with A.

---

## Cross-umbrella concerns

### Accuracy of intent classification

Expected classifier accuracy varies by umbrella:

| Umbrella | Expected accuracy | Misclassification cost |
|----------|-------------------|------------------------|
| `/iterate` | HIGH — sub-modes share lexical signal (distill / propose / hygiene / grill / review are all spec-related) | LOW — one-sentence redirect |
| `/work` | LOW — sub-modes are orchestrator-internal phases; classifier has to predict orchestrator state, not user words | HIGH — wrong phase could fire before user can intervene |
| Help-me-think | MEDIUM — three sub-modes have distinct triggers but tonal overlap ("walk me through" could be zoom-out or grill) | LOW — restart command |

Only `/iterate` has the right shape (high accuracy + low recovery cost) for interpretive routing.

### Failure-mode mitigation: announce interpretation

Critical safety surface from FB-072's capture: **the router announces its interpretation before any substantive action.**

> *"I read this as a distill request — proceeding with the distill sub-flow. Say 'no' to redirect."*

Without it, misclassifications are silent (bad). With it, misclassifications cost one redirect (acceptable). This pattern is non-optional; the prototype must include it.

### File size and dispatch shape

If `/iterate` becomes router + 5 sub-modes (review, distill, propose, hygiene, grill):

- **Inline all sub-modes in `iterate.md`:** preserves single-file readability. Risk: file grows ~40-50KB; Claude's selective reading mitigates context cost. Recommendation: **start here.**
- **Extract sub-modes to per-file:** improves modularity (`iterate-distill.md`, `iterate-propose.md`, `iterate-hygiene.md`, `iterate-grill.md`, with `iterate.md` as thin dispatcher). Adds N+1 files to maintain + sync. Recommendation: **switch when file exceeds ~50KB.**
- **Hybrid:** keep small sub-flows inline; extract large ones (e.g., distill is the longest current sub-mode; could extract first). Pragmatic option if size pressure builds.

### Latency / cost

Interpretive routing adds an LLM pass before substantive work fires. Estimated cost: ~500 output tokens + the classified sub-mode's context load. Comparable to sub-mode dispatch's own context load. Not a blocker; not free either.

If router lives in `iterate.md` itself, the router pass is part of the existing prompt (not a separate dispatch). Cost shifts but doesn't grow.

### Interaction with FB-071 (Command Invocation Gates)

If `/iterate` umbrella ships with `disable-model-invocation: true`, all sub-modes are covered by one gate. This **simplifies** FB-071's sub-mode coupling concern:

- Today: `/iterate` is gated → all 4 sub-modes are non-ambient-invokable, including read-only review path.
- With router: same gate, same scope. No regression.
- Plus: future help-me-think umbrella (if shipped) would similarly inherit one gate covering three sub-modes — potentially replacing the per-command gating decisions needed today.

The router pattern is **compatible** with the gating story; it doesn't fight it.

### Interaction with DEC-016 (spec/decision/vision Edit/Write ask)

Unchanged. The permission-layer ask fires at the Edit/Write boundary regardless of how the write was reached. Router doesn't bypass; sub-flows that propose spec edits still go through propose-approve-apply.

---

## Net recommendation

1. **Prototype interpretive routing on `/iterate` only.** Strong fit, clear sub-modes, natural lexical signals, low misclassification recovery cost. The prototype should include:
   - Router classifies input, picks sub-mode
   - Router announces interpretation + sub-mode (+ topic if `propose`-shaped)
   - User can redirect with one word ("no", "I meant distill"); router re-classifies
   - Fallback to no-arg review mode if input doesn't lexically signal a sub-mode

2. **Keep `/work` and `/research` distinct.** Wrong shape for router. Auto-detect handles `/work` no-args; research → iterate breadcrumb handles the handoff.

3. **Audit commands stay menu-dispatched.** `/health-check` Part 8 menu is fine.

4. **Defer help-me-think umbrella.** Revisit after `/iterate` trial data accumulates.

---

## Effectiveness data to collect during `/iterate` router trial

| Metric | Threshold candidate (FB-072 capture) |
|--------|--------------------------------------|
| Sub-mode classification accuracy | ≥ 85% on first interpretation |
| Recovery cost (redirects per session) | ≤ 1 |
| User feedback on natural-language vs explicit-arg | Positive trend |
| Latency observed (router pass duration) | No observable hang at session boundaries |

Trial scope: ~10-15 real `/iterate` invocations across this template repo + at least one downstream project (echothread or styler) within 4-6 weeks. If thresholds met: open DEC via `/research`. If unmet: FB-072 closes; explicit-arg pattern stays.

---

## Decision points awaiting user response

1. **Proceed to `/iterate` router prototype?** (Recommended: yes) — or pick a different umbrella, or pause FB-072 entirely.
2. **Within `/iterate` router, inline-all-sub-modes or extract per-file?** (Recommended: inline now, extract when file exceeds ~50KB)
3. **Confirm help-me-think umbrella deferred until `/iterate` trial completes?** (Recommended: yes)

---

## Out of scope for this survey

- The actual router prototype (deliverable 2)
- Effectiveness data collection (deliverable 3)
- DEC candidate (deliverable 4)
- Cross-command umbrella for `/audit-*` (independent question)
- Within-command interpretive routing for `/audit-*` modes (independent question)
- `/work-complete` / `/work-pause` file splits (independent FB-071 follow-up)
