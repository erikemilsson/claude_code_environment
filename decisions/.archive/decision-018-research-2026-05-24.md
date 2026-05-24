# DEC-018 Research Archive — Command routing: interpretive vs explicit-arg dispatch

**Decision:** DEC-018
**Researched:** 2026-05-24
**Researcher:** research-agent (Opus 4.7)
**Source feedback:** FB-072 (captured 2026-05-20, triaged 2026-05-24)
**Primary input:** `.claude/support/workspace/router-survey.md` (FB-072 deliverable 1, 2026-05-20)

---

## 1. Investigation methodology

This research was scoped by its caller as **validate-or-extend**, not redo-from-scratch. The boundary survey already did the option-gathering work (Step R2 equivalent) across five candidate umbrellas. My job was Step R3-heavy: stress-test the survey's assumptions, bring external evidence, surface missed failure modes, and sanity-check the option framing.

**Sources consulted:**

- **Codebase (ground truth):** `iterate.md`, `work.md`, `research.md`, `grill.md`, `zoom-out.md`, `diagnose.md` (file sizes + dispatch shapes); `rules/agents.md § Command Invocation Gates` (FB-071); DEC-005 + DEC-016 records (interaction surface); `template-maintenance/feedback.md § FB-072` (full capture + triage note).
- **External (general evidence on NL-vs-explicit dispatch):** see § 4 below. Five web searches + two page fetches covering Slack-bot intent routing, LLM intent-router design, CLI-vs-NLI discoverability tradeoffs, agentic-AI confirmation UX patterns, and Claude Code's native slash-command autocomplete.

**Confidence calibration:** the codebase findings are high-confidence (direct file reads). The external findings are moderate-confidence directional evidence — they establish that the survey's mitigations match documented industry patterns, but none is a controlled study of *this specific* pattern (interpretive routing on a spec-amendment command in an AI coding agent). The recommendation is therefore explicitly prototype-gated, which is also FB-072's stated intent.

---

## 2. Ground-truth file sizes (corrects/sharpens the survey)

The survey quoted approximate sizes. Exact (as of 2026-05-24):

| File | Bytes | Lines | Survey said |
|------|------:|------:|-------------|
| `iterate.md` | 31,615 | 581 | ~31 KB / ~700 lines |
| `grill.md` | 9,792 | 156 | ~8 KB |
| `work.md` | 71,744 | 1,150 | ~63 KB |
| `research.md` | 6,494 | 180 | ~6.5 KB |
| `diagnose.md` | 10,401 | 157 | ~10 KB |
| `zoom-out.md` | 2,700 | 46 | ~3 KB |
| `audit-coherence.md` | 46,866 | 640 | ~47 KB |
| `audit-ui.md` | 45,815 | 904 | ~46 KB |

**Implication for the inline-vs-extract call:** if `/grill` (9.8 KB) migrated inline into `iterate.md` (31.6 KB), the result is **~41 KB** — below the survey's ~50 KB extract trigger, but only by ~9 KB. Adding a `propose` sub-mode formalization (currently embedded in Step 4, ~3 KB if pulled into its own explicit mode header) plus the router-dispatch preamble (~2 KB) lands the file at **~46 KB**, brushing the trigger. **The survey's ~50 KB threshold is defensible but the margin is thin** — the prototype should treat extraction as a *near-term likelihood*, not a remote contingency. See § 6 (Option D as orthogonal axis).

A second, more important correction: the survey frames inline-vs-extract as a binary. The byte math shows it's really a **sequence** — inline works for the first router increment, but the second increment (grill migration) is what tips it. Recommending "inline now, extract at 50 KB" is correct but should be stated as "expect to extract within one or two sub-mode additions," not "extract is a distant maybe."

---

## 3. Validation of the survey's key assumptions

### 3.1 The "`/work` is WEAK for routing" claim — VALIDATED, and for a sharper reason

The survey says `/work` is weak because its internal phases (Steps 0-5) are orchestrator-internal sequencing, not user-selected modes, so interpretive routing would "risk firing the wrong internal phase" and "duplicate auto-detect."

**Codebase confirms this and adds a decisive detail the survey understates:** `/work` *already exposes a natural-language surface* — `/work {request}` (work.md line 15, Step 2 line 404, Step 3 line 485). But it routes the NL request through **spec-check → task-creation → state-based orchestration** (Step 2c parallelism assessment, Step 3 action determination), NOT through user-word-based sub-mode dispatch. So `/work` is not "missing" a router; it has the *correct* router shape for an orchestrator — interpret the request, then let **project state** (task status, dependencies, decomposition state) decide which phase fires, rather than letting **user phrasing** decide.

This is the strongest single argument that interpretive *sub-mode* routing is the wrong tool for `/work`: the orchestrator's whole value is that it routes from ground-truth state, not from how the user phrased the ask. "Implement T123" vs "decompose T123" should be resolved by *whether T123 is already decomposed*, not by which verb the user typed. The survey's "WEAK" verdict is correct; the underlying reason is "`/work` already routes from state, which is more reliable than routing from words for orchestration." This is worth stating explicitly in the DEC because it generalizes: **interpretive routing fits commands whose sub-modes are user-intent-distinct (iterate), and misfits commands whose sub-modes are state-determined (work).**

### 3.2 The ≥85% first-interpretation accuracy + ≤1 redirect/session thresholds — DEFENSIBLE but UNDER-INSTRUMENTED

The thresholds originate in FB-072's capture, not in measured data. They are reasonable targets. Two stress-test observations:

- **≥85% accuracy is measurable only with a denominator.** Across "~10-15 real `/iterate` invocations" (the survey's trial scope), 85% means ≤2 misclassifications tolerated. That's a small sample — a single bad week could fail or pass the gate by noise. The trial should either widen N (toward ~25-30 invocations) or treat the threshold as directional ("no systematic misclassification pattern") rather than a hard numeric pass/fail on a tiny sample.
- **External evidence offers a better operational metric.** The agentic-UX literature (Smashing Magazine, § 4.4 below) uses a **reversion rate > 5% → disable automation for that task** kill-switch. This is more actionable than "≤1 redirect/session" because (a) it's per-task (per-sub-mode here), so a single bad sub-mode classifier can be caught without condemning the whole router, and (b) it's a rate, so it's sample-size-robust. **Recommend folding a per-sub-mode redirect-rate kill-switch into the trial gate** alongside the existing thresholds. Concretely: if any one sub-mode (e.g., distill-vs-propose confusion) shows a redirect rate materially above the others, that sub-mode reverts to requiring its explicit arg while the rest of the router stays.

### 3.3 The "announce-interpretation" mitigation — STRONGLY VALIDATED by external evidence

This is the survey's load-bearing safety claim, and it is exactly the documented industry pattern. The agentic-AI UX literature calls it **"Intent Preview"** and treats it as foundational:

> *"Before an agent takes any significant action, the user must have a clear, unambiguous understanding of what is about to happen."* — Smashing Magazine, Designing for Agentic AI (2026)

> *"By surfacing the agent's interpretation before acting, it gives the user a chance to correct a pattern match that was technically confident but contextually wrong."* — ibid.

The conversational-AI design literature independently describes the same **"restate interpretation before acting"** + **"did you mean"** progressive-repair pattern (Bland.ai, designative.info). And the Slack-bot / LLM-router literature universally uses a **confidence threshold with fallback-to-default-intent** when classification is uncertain (Question Base, Vellum, Zep). The survey's "fallback to no-arg review mode if input doesn't lexically signal a sub-mode" is precisely this fallback-to-default pattern.

**Conclusion:** the mitigation is not speculative; it's the established practice. The survey is right to make it non-optional.

### 3.4 The "low misclassification recovery cost" claim — VALIDATED with a precise mechanism

The survey asserts `/iterate` has low recovery cost ("one-sentence redirect"). External evidence supplies *why* this holds and *where it could fail*:

The agentic-UX **"Autonomy Dial"** distinguishes four authorization levels: Observe & Suggest → Plan & Propose → Act with Confirmation → Act Autonomously. The confirmation-gate rule is explicit:

> *"This pattern is non-negotiable for any action that is irreversible, involves a financial transaction of any amount, shares information with other people or systems, or makes a significant change that a user cannot easily undo."* — Smashing Magazine

**Mapping onto CCE:** the router's *classification step* (pick review/distill/propose/hygiene/grill) is a `Plan & Propose` decision — it selects a flow but takes no irreversible action. The actual irreversible action (a spec/decision/vision write) is **already gated** by DEC-016's `permissions.ask` and by propose-approve-apply. So misclassification is cheap **precisely because the router sits upstream of the existing confirmation gate** — a wrong sub-mode pick wastes one turn but cannot land a wrong spec edit, because the edit itself still requires explicit approval. This is the mechanism that makes the survey's claim true, and it should be stated in the DEC: **interpretive routing is safe here because every downstream irreversible action retains its own independent gate (DEC-016).** The router does not relax any existing safety surface; it only chooses which already-gated flow to enter.

**Where it could fail:** if a future sub-mode under `/iterate` took an irreversible action *without* its own confirmation gate, the "low recovery cost" property would break. Today none do (distill/propose/hygiene all end in propose-approve-apply; grill is interactive). The DEC should note this as an invariant to preserve: **any sub-mode reachable by the router must retain an independent confirmation gate for irreversible actions** — the router must never be the *only* thing standing between an interpretation and a write.

### 3.5 The inline-vs-extract ~50 KB trigger — see § 2. Defensible, thin margin, treat extraction as near-term.

---

## 4. External evidence summary (NL vs explicit dispatch in comparable tools)

### 4.1 Slack bots / chat-ops (the closest "command-vs-conversation" analog)

Modern Slack bots have largely moved from slash commands to NL because LLMs got good at intent extraction. The standard architecture: **entity extraction → action classification → skill matching**, with an **ML confidence threshold** below which the bot falls back to a **default intent** rather than guessing. (Question Base, Guru, Workato.) **Relevance:** validates the router architecture *and* the fallback-to-default design. Note the trajectory — the industry moved *toward* NL — but Slack bots serve a broad, non-expert audience; CCE serves a single expert user who already knows the explicit args. The discoverability payoff that justifies NL for Slack is weaker here (see § 4.5).

### 4.2 LLM intent routers (the mechanism)

Intent routers mis-route when "a user's phrasing is far from all samples." Mitigation is testing across query variability before production + semantic-similarity thresholds. (Vellum, Zep, Khaneja/Medium.) **Relevance:** the failure mode is phrasing-drift, not concept confusion — `/iterate`'s sub-modes have strong distinct lexical signals (distill / hygiene / "stress-test" / "the spec is fuzzy"), so phrasing-drift risk is low, which is exactly why the survey rates `/iterate` HIGH-accuracy. Confirms the survey's per-umbrella accuracy ranking is well-founded.

### 4.3 CLI subcommands vs natural-language interfaces (discoverability)

The HN/UX-literature consensus: **both** explicit-subcommand CLIs and NL interfaces have poor discoverability, in *different* ways. Explicit: you must know the command exists. NL: "natural language is often ambiguous… implementing a working NL system usually requires restricting it to a limited subset of vocabulary and syntax" — **and that restriction is invisible to the user**, who "must phrase requests effectively" without being told the boundary. (Toronto NLI paper, jmmv.dev, HN threads, Medium/Omidvar.) **Relevance — this is a failure mode the survey underweights:** an interpretive `/iterate` creates a *hidden vocabulary boundary*. The user learns that "distill" works, but does "extract a spec" work? Does "turn this vision into requirements"? The announce-interpretation step mitigates *silent wrong action* but does NOT mitigate *the user not knowing what phrasings route where*. This is a discoverability cost that partially offsets the "one fewer command to remember" benefit. See § 5.1.

### 4.4 Agentic-AI confirmation UX (the safety frame) — most directly applicable

Smashing Magazine's "Designing for Agentic AI" (2026) supplies the cleanest decision framework, summarized above (§ 3.3, § 3.4). Key reusable rules:

- **Intent Preview** before any significant action (= announce-interpretation). Plain-language, not API-speak.
- **Confirmation gates non-negotiable** for irreversible / shared / hard-to-undo actions.
- **Autonomy Dial** — four levels; match the gate to the action's reversibility.
- **Reversion Rate > 5% → disable automation for that task** (operational kill-switch; better metric than the survey's redirect count — see § 3.2).
- **Confidence Signal / Scope statement** — "a clear statement of the agent's area of expertise (e.g., Scope: Travel bookings only) helps manage user expectations and prevents them from asking the agent to perform tasks it's not designed for." **This is a discoverability mechanism the survey didn't name** — see § 5.1 and Option A's announce-interpretation refinement.

### 4.5 Claude Code native slash-command discoverability (reframes the UX driver)

Typing `/` in the Claude Code terminal shows a **filterable autocomplete dropdown of all commands**, with the first `#`-heading line used as the description. Type `/g` → `/grill` surfaces. (Medium/Kondur "Complete Guide to Slash Commands May 2026"; multiple anthropics/claude-code autocomplete issues confirm the menu exists and is the expected surface.)

**Two decisive implications:**

1. **The "one more command to remember" driver behind FB-072 is partly already solved by the platform.** The user does not have to *remember* `/grill` exists — `/`-autocomplete lists it. What the menu does *not* surface is **sub-mode args** (`/iterate distill`, `/iterate hygiene` don't appear as separate menu rows; only `/iterate` does). So the real discoverability gap is **sub-mode discovery**, not **command discovery** — and a router does not fix sub-mode discovery either (the user still has to know to *say* "distill"). The mechanism that fixes sub-mode discovery is documentation or a scope-statement that *lists* the sub-purposes (Option C territory, or Option A's announce step listing alternatives).
2. **Desktop app has no autocomplete** (confirmed in the same sources). On Desktop, discoverability degrades to "know the full command name." This is a real but minority-surface gap.

**Net:** the platform already addresses command-existence discoverability in the terminal. This *lowers* the value of Option A's discoverability benefit and *raises* the relative value of a documentation-only Option C — but Option C also doesn't fully solve sub-mode discovery unless it explicitly enumerates sub-modes. The cleanest sub-mode-discovery fix is orthogonal to all three options: **ensure each multi-mode command's `## Usage` block and the README enumerate the sub-modes** (already true for `/iterate` — Usage lists distill/hygiene). The genuinely novel capability a router adds is **not having to learn the sub-mode token at all** — you can say it however you want. That is the actual, narrow value proposition, and it should be stated honestly in the DEC.

---

## 5. Failure modes / options the survey missed

### 5.1 Hidden-vocabulary-boundary discoverability cost (NEW)

Covered in § 4.3 + § 4.5. An interpretive router trades a *visible, learnable* boundary (the explicit arg `distill`, surfaced in `## Usage`) for an *invisible, inferred* boundary (which phrasings classify as distill). Announce-interpretation catches wrong *actions* but not wrong *expectations*. **Mitigation to add to Option A:** the announce step should occasionally surface the scope/alternatives ("I read this as distill — other things I can do here: propose a spec change, run a hygiene cross-check, or grill you on it"), borrowing the agentic-UX **Confidence Signal / Scope statement** pattern. This converts the router's first few uses into a discoverability *teacher* rather than a silent classifier. Low cost; meaningfully addresses the § 4.3 concern.

### 5.2 The explicit-arg-still-works hybrid is implicit in Option A — make it EXPLICIT (NEW framing)

The survey and skeleton describe Option A as "classify intent → sub-mode." But nothing in the design *removes* the existing explicit args. The right and almost-certainly-intended shape is **additive, not replacing**: `/iterate distill` continues to dispatch deterministically (no classification, no ambiguity); `/iterate {natural language}` *also* routes interpretively. This is strictly safer than a replace-the-args design and costs nothing — the explicit-arg path is a zero-ambiguity fast lane for users who know the token, and the NL path is the convenience layer for those who don't. **This should be stated as a first-class property of Option A, not left implicit.** It also means the migration is genuinely low-risk: existing muscle memory (`/iterate distill`) keeps working unchanged; the router is purely additive surface. (I considered whether this deserves to be a separate 4th option — "additive NL layer over preserved explicit args" — but concluded it *is* Option A done correctly, not a distinct option. Calling it out within Option A is the right move; splitting it would imply Option A means replacing the args, which would be a strictly worse design no one is actually proposing.)

### 5.3 Per-file sub-mode extraction is an ORTHOGONAL axis, not a 4th routing option (sanity-check result)

The caller asked whether per-file extraction belongs as a 4th option. **Conclusion: it's orthogonal, not a peer option** — it's a *file-organization* decision independent of the *dispatch-pattern* decision. You can have: explicit-arg + inline (status quo), explicit-arg + extracted (refactor work.md-style without changing dispatch), interpretive + inline (Option A as drafted), or interpretive + extracted (Option A after the 50 KB trigger). Extraction interacts with FB-071 gating (per-file `disable-model-invocation` — extracting `iterate-distill.md` as its own file would let it carry its own gate, which could *split* the currently-coupled gate the survey notes as a benefit of keeping things together). **Recommendation:** represent extraction as an **implementation sub-decision within Option A** (the survey's inline-vs-extract decision point #2), NOT as a 4th top-level option. Adding it as a 4th option would muddle the central question (which dispatch pattern?) with a downstream how (how to organize the files once the pattern is chosen). I am keeping three options and documenting extraction as an Option-A implementation note + a flagged interaction with FB-071. This preserves the skeleton's intent.

### 5.4 Router-pass-eats-the-output-budget interaction with the 32K cap (NEW, minor)

`.claude/CLAUDE.md` notes Claude Code caps output at 32K tokens/response (thinking + text + tool args shared). The survey's latency analysis ("~500 output tokens for the router pass") is right that cost is modest, but misses that **if the router pass and the sub-mode's first substantive output share one response**, they compete for the same 32K budget. For `distill` (which produces a large spec-change declaration) this could matter. **Mitigation:** the announce-interpretation step is a natural response boundary — announce in one turn (cheap), do the heavy sub-mode work in the next. This actually *aligns* with the safety design (announce → user can redirect → then act), so it's not an added cost; it's a reason the announce step should be a genuine turn boundary, not a same-response preamble. Worth a one-line note in Option A.

---

## 6. Option framing sanity-check (final)

The three seeded options (A interpretive router on `/iterate` / B status quo / C thin discoverability layer) are the **right framing**. Verdict on each framing question the caller raised:

- **Is a 4th option warranted?** No. The two candidates considered — "additive NL over preserved explicit args" (§ 5.2) and "per-file extraction" (§ 5.3) — are respectively *Option A done correctly* and *an orthogonal implementation axis*. Folding both into Option A keeps the decision crisp. Adding either as a peer would conflate the dispatch-pattern question with implementation detail.
- **Should options be renamed?** Minor: Option A's name is fine, but its *description* should be tightened to (a) make the additive-not-replacing property explicit, (b) name the scope-statement discoverability refinement, (c) note the extraction sub-decision + FB-071 interaction. Options B and C unchanged.
- **Is C distinct enough from B?** Yes, but C's value is now *narrower* than the survey implied, given § 4.5 (native autocomplete already covers command-existence). C's real residual value is **sub-mode discovery** (enumerating `/iterate`'s sub-purposes + the help-me-think family in one place) and **Desktop-app discoverability** (no autocomplete there). C should be framed as "documentation/pointer that closes the sub-mode-discovery gap the `/`-menu leaves open," not "general discoverability help."

---

## 7. Recommendation (research-agent)

**Recommend Option A (interpretive router on `/iterate`), prototype-gated — confirming the survey's net recommendation, with four refinements.**

**Single most important reason:** the router sits *upstream* of CCE's existing irreversible-action gates (DEC-016 `permissions.ask` + propose-approve-apply), so a misclassification costs one redirect but **cannot** land a wrong spec edit. This is the precise mechanism behind the survey's "low recovery cost" claim, and it's validated by the agentic-UX Autonomy-Dial framework: classification is a `Plan & Propose`-level decision (cheap to get wrong), while the write stays at `Act with Confirmation`. The safety surface is preserved; only the convenience of not-needing-the-sub-mode-token is added.

**Confidence:** moderate. High on the *safety* analysis (codebase-grounded + externally corroborated). Moderate on the *value* analysis — the discoverability benefit is smaller than FB-072's framing suggests (native `/`-autocomplete already solves command-existence; the genuine win is "say it however you want"), so the prototype must demonstrate that the convenience is worth the hidden-vocabulary-boundary cost (§ 5.1). This is exactly what a trial measures.

**Four refinements to carry into the prototype (all fold into Option A; none changes the option set):**

1. **Additive, not replacing (§ 5.2).** Keep explicit args (`/iterate distill`) as a zero-ambiguity fast lane; add NL routing alongside. State this as a first-class property.
2. **Scope-statement in the announce step (§ 5.1, § 4.4).** When announcing an interpretation, occasionally list the alternative sub-purposes so the router teaches its own boundary. Closes the hidden-vocabulary-boundary discoverability gap.
3. **Per-sub-mode redirect-rate kill-switch (§ 3.2, § 4.4).** Add the agentic-UX 5%-style per-task reversion metric to the trial gate alongside the existing thresholds; a single bad sub-mode classifier reverts to its explicit arg without condemning the whole router.
4. **Announce-as-turn-boundary (§ 5.4).** The announce step is a genuine response boundary (cheap turn), with heavy sub-mode work in the next turn — aligns with both the 32K budget and the redirect-before-act safety design.

**Invariant to preserve (§ 3.4):** any sub-mode reachable by the router must retain an independent confirmation gate for irreversible actions. The router must never be the *only* thing between an interpretation and a write.

**On the survey's other four umbrellas:** I fully validate "keep `/work` + `/research` explicit, keep `/audit-*` menu-dispatched, defer help-me-think." The `/work` analysis is even stronger than the survey stated (§ 3.1 — `/work` already routes from state, which is correctly more reliable than routing from words). No divergence.

---

## 8. Open questions for the user (added to DEC § Your Notes & Constraints)

1. **Trial denominator.** Is ~10-15 `/iterate` invocations enough to trust an 85% accuracy read, or should the gate widen toward ~25-30 (§ 3.2)? Recommend treating 85% as directional + adding the per-sub-mode redirect-rate kill-switch as the harder gate.
2. **Grill migration coupling.** Option A's natural companion move is migrating `/grill` to `/iterate grill` (FB-068/FB-072 interaction). Do you want the prototype to (a) include grill-as-sub-mode from the start, accepting the ~41-46 KB file size (§ 2) + likely near-term extraction, or (b) prototype the router on the *existing* four modes only (review/distill/propose/hygiene) and defer grill until the router proves out? Recommend (b) — smaller blast radius, cleaner accuracy signal, and `/grill`'s standalone command keeps working as the dispatch target either way.
3. **Discoverability honesty.** Given that native `/`-autocomplete already surfaces command existence (§ 4.5), does the "one fewer command to remember" motivation still feel compelling, or does the value re-center on "say it however you want"? This reframing might change how you weight Option A vs Option C.

---

## 9. Discarded / not-pursued

- **A standalone 4th option for "additive NL layer."** Discarded — it's Option A done correctly (§ 5.2), not a distinct choice.
- **A standalone 4th option for per-file extraction.** Discarded — orthogonal implementation axis, folded into Option A's notes (§ 5.3).
- **Researching the help-me-think umbrella in depth.** Out of scope per the survey's defer recommendation and FB-072's "prototype `/iterate` first" sequencing. Re-surfaces only if the `/iterate` trial succeeds.
- **Cross-command `/audit` umbrella.** Out of scope; survey rates it "sufficient as-is" and `/health-check` Part 8 menu is small. No external evidence suggested revisiting.

---

## Sources (external)

- [Designing For Agentic AI: Practical UX Patterns For Control, Consent, And Accountability — Smashing Magazine](https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/) — Intent Preview, Autonomy Dial, confirmation-gate rule, 5% reversion-rate kill-switch, Confidence Signal / Scope statement.
- [Designing Human-Agent Interaction: Principles for Trustworthy Collaboration — designative.info](https://www.designative.info/2026/01/15/designing-human-agent-interaction-principles-for-trustworthy-collaboration/) — restate-interpretation-before-acting, progressive repair.
- [What Is Conversational AI Design? — Bland.ai](https://www.bland.ai/blogs/conversational-ai-design) — "did you mean" / parse-confidence surfacing.
- [A Beginner's Guide to LLM Intent Classification for Chatbots — Vellum](https://www.vellum.ai/blog/how-to-build-intent-detection-for-your-chatbot) — intent-classifier accuracy, phrasing-variability failure mode.
- [Semantic Similarity as an Intent Router for LLM Apps — Zep](https://blog.getzep.com/building-an-intent-router-with-langchain-and-zep/) — semantic-similarity routing + threshold/fallback.
- [LLM as a Router — Khaneja, Medium](https://medium.com/@vanshkhaneja/llm-as-a-router-how-to-fine-tune-models-for-intent-based-workflows-6d272eab55d1) — router mis-routing on out-of-sample phrasing.
- [Slack knowledge base bot — Question Base](https://www.questionbase.com/resources/blog/slack-knowledge-base-bot) — entity-extraction → action-classification → skill-matching; confidence threshold → default intent.
- [What is a Slack Bot? — Guru](https://www.getguru.com/reference/what-is-a-slack-bot) — NL-over-slash trajectory in modern bots.
- [CLI discoverability — Hacker News](https://news.ycombinator.com/item?id=23329723) + [jmmv.dev: Subcommand-based interfaces](https://jmmv.dev/2013/09/cli-design-subcommand-based-interfaces.html) — subcommand structure vs discoverability.
- [Natural Language as an Interface Style — University of Toronto](https://www.dgp.toronto.edu/public_user/byron/papers/nli.html) — NL ambiguity + invisible-vocabulary-boundary problem.
- [The Complete Guide to Claude Code Slash Commands (May 2026) — Kondur, Medium](https://medium.com/@ekondur/the-complete-guide-to-claude-code-slash-commands-may-2026-48a127aef832) — `/`-autocomplete filterable menu, first-`#`-line description; Desktop app lacks autocomplete.
