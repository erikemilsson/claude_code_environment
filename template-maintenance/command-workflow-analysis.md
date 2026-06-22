# Command Workflow Analysis — streamlining the command surface

**Started:** 2026-06-22 · **Status:** analysis / pre-design · **Owner:** template maintenance

**Purpose.** Erik's ask: the commands are individually useful but "fully dependent on the user remembering them and firing them in the right order," and "some don't work together as smoothly as I'd like." This doc maps the current command surface + the canonical journeys, locates the seams, and lays out a menu of streamlining interventions at escalating cost — each checked against prior decisions (esp. DEC-018).

**Two distinct frictions** (keep them separate — they have different fixes):
1. **Recall + ordering** — remembering *which* command and the *right sequence*.
2. **Handoff smoothness** — state doesn't carry between commands; the next step isn't surfaced; seams are manual.

---

## 1. Command catalog

| Command | Purpose | Gated? | Inputs | Outputs | Sub-modes |
|---|---|---|---|---|---|
| `/work` | Start/continue work; decompose, route to agents, complete | No | spec, tasks, dashboard, decisions, feedback | task transitions, agent dispatch, drift reconciliation, dashboard regen | `pause`, `complete {id}` |
| `/iterate` | Spec review & refinement; propose→approve→apply | Yes | spec, feedback, decisions, vision | spec change declarations, version transitions, decision finalization | `distill`, `hygiene {topic}` |
| `/grill` | Interview-style interrogation; sharpen vocab | No | spec, code, `./CONTEXT.md` | CONTEXT.md entries, sharpened terms, decision suggestions | (plain vs with-docs) |
| `/shakedown` | Acceptance-by-example; probe built system vs real-use examples | No | spec, running system, shakedown corpus | capability-boundary corpus, verdicts, routing suggestions | (corpus persists) |
| `/diagnose` | Hard-bug/regression discipline (6 phases) | No | code, tests, state | reproduction, hypothesis, fix, post-mortem friction | (linear 6-phase) |
| `/zoom-out` | Map an abstraction layer | Yes | spec, code, CONTEXT.md | component map | — |
| `/review` | Implementation quality review (advisory, read-only) | No | task JSONs, files_affected, spec | advisory suggestions (no task creation) | — |
| `/status` | Quick read-only state view | No | dashboard, tasks, spec, drift/verify state | phase, counts, health, actionables | `--brief`, `--tasks` |
| `/research` | Investigate options for decisions | Yes | decision records, spec, learnings | populated decision record + research archive + recommendation | (auto vs explicit) |
| `/feedback` | Capture & manage improvement ideas | Yes | feedback.md, archive, tasks | FB-NNN entries, archive transitions | `list`, `review`, `review {id}`, `template:` |
| `/health-check` | Validate system health + template sync + audit dispatch | No | all `.claude/` state, template remote, interaction logs | fix queue, audit menu, sync diffs | `--report` |
| `/audit-coherence` | Spec-vs-reality coherence audit | No | spec, decisions, friction, retired manifests | findings + digest | `triage`, `promote`, `fix` |
| `/audit-ui` | UI/UX audit via Playwright (7 lenses) | No | running app | findings + per-page artifacts | `triage`, `promote`, `fix`, `--mobile`, `--vector`, `--depth` |
| `/breakdown {id}` | Split complex task into subtasks | Yes | task JSON, spec | subtask files, parent → "Broken Down" | — |

---

## 2. Handoff graph (the inter-command wiring)

**Automatic handoffs** (orchestrator does it — no recall needed):
- `/work` → `/diagnose` (autonomous fire-when-stuck on hard bug, FB-071)
- `/health-check` → `/audit-coherence` / `/audit-ui` (Part 8 dispatch)
- `/work` Step 1b → drift reconciliation (detects spec drift)
- implement-agent → verify-agent (auto on completion)
- `/feedback review` → `/iterate` (ready items appear as context in `/iterate` Step 1b)

**Manual / prose-only handoffs** (a command *says* "you might run /X" but carries no state; user re-fires + re-supplies context):
- `/grill` → `/research` ("offer to route precedent-setting decisions")
- `/grill` → `/iterate` (spec changes route through DEC-016 guardrail)
- `/iterate` → `/research` ("[C] Create decision record and research options")
- `/iterate` → `/work` ("Spec changes applied. Run /work to start building.")
- `/iterate distill` → `/work` ("When the spec passes readiness checks, run /work")
- `/shakedown` → `/iterate` / `/research` (⚠ verdicts propose routes)
- `/audit-* promote` → `/iterate` (findings queued as FB → user routes)

**Dead-ends** (no outbound next-step pointer): `/status`, `/review`, `/zoom-out`, `/diagnose` (ends at post-mortem), `/breakdown` (user must re-fire `/work`).

**Cold-starts** (no inbound pointer — reachable only by remembering them cold): `/grill`, `/shakedown`, `/feedback`, `/zoom-out`, `/diagnose`, `/work pause`.

> **Centerpiece observation:** the "help-me-think / vet" commands — `/grill`, `/research`, `/shakedown`, `/zoom-out`, `/review`, `/diagnose` — are **orphaned from the workflow graph**. Almost nothing points *to* them, so they live or die by user recall. Meanwhile the automatic handoffs all cluster *inside the build loop* (`/work`, `/health-check`, verification). This is the structural shape of Erik's complaint.

---

## 3. Journey traces + seams

### Journey 1 — Initial spec creation (nothing → buildable spec)
`(.claude/vision/ doc)` → **`/grill {vision}`** *(optional)* → **`/iterate distill`** → spec v1 → **`/work`**

- **SEAM 1a (recall):** grill not auto-routed before distill — docs-only recommendation, no marker/handoff. *1 action + 1 recall.*
- **SEAM 1d (gap):** distill flags `[NEEDS APPROVAL]` decisions but doesn't create records or route to `/research`. *0–2 manual actions.*
- **SEAM 1e (recall):** spec creation doesn't trigger decomposition; user must remember `/work`. *1 action + 1 recall.*

### Journey 2 — Adding a fully-vetted feature (idea → built + verified)
**`/grill {topic}`** *(opt)* → **`/research`** *(opt)* → **`/work "{feature}"`** (spec check) → *(maybe `/iterate`)* → implement → verify → Finished

- **SEAM 2a (recall):** `/work` never suggests vetting a new feature with `/grill` first. *1 action.*
- **SEAM 2b (prose-only handoff):** grill→research is "offer to…" — no auto-creation, user re-fires + re-supplies. *1 action + context switch.*
- **SEAM 2c (drift risk):** "Proceed anyway" allows out-of-spec tasks without a spec update. *Silent drift.*

### Journey 3 — Structured edits to an existing project (mid-flight scope change)
*(recognize need)* → **`/iterate {section}`** → *(maybe `/research {DEC}`)* → spec amended → `/work` drift reconciliation → re-scope/new tasks → resume

- **SEAM 3a (disambiguation):** nothing surfaces "is this a spec / task / decision change?" — user must know. *1 mental model.*
- **SEAM 3c (prose-only handoff):** `/iterate`→`/research` is manual `[C]` select; no auto-creation. *1 action.*
- **SEAM 3e (transparency):** In-Progress tasks whose spec drifted get a fingerprint update but no suggest-restart/continue. *1 awareness gap.*

### Seam categories
- **Recall** (1a, 1e, 2a): the next/right command isn't surfaced — pure memory burden.
- **Prose-only handoff** (2b, 3c): a command points at another but carries no state; user is the integration glue.
- **Disambiguation** (3a): no surface answers "which command do I want?"
- **By-design gates** (1c, 2d, decision batches, per-task verify): *not* seams to remove — keep.

---

## 4. Prior art (build on these; don't re-tread)

### DEC-018 — declined the interpretive router (2026-05-24, Option B / status quo)
- **Why declined:** safety was high but value was only moderate. A probe of 26 sessions found **"zero recorded instances of the friction Option A removes (no 'which command/sub-mode,' no 'forgot,' no 'how do I run')"** — recall-the-token friction was near-absent *in the build-loop sessions measured*. Benefit front-loaded/transient (onboarding, covered by `/`-autocomplete); cost permanent (an LLM pass per invocation, hidden vocab boundary).
- **Re-open condition (verbatim):** *"if Wave 2 … materially grows the command surface and 'interpretive routing as a pattern' resurfaces as a live question, open a fresh DEC — DEC-018's option framing + the survey + the research archive are the starting point."*
- **Boundary for THIS effort:** the router mapped *fuzzy intent → one command*. Erik's friction is at the **vetting/spec-shaping front-end** and in **state-losing handoffs** — which DEC-018 never measured or addressed. We enter through the re-open door, but the target is workflow *legibility + handoff*, not intent-routing.

### Surveyed-but-deferred
- **`/walkthrough` / `/preflight`** — "help-me-think" companion to the router; parked at FB-072, "available for separate re-capture," no dedicated FB. A *lifecycle map* idea, distinct from the router.
- **Help-me-think umbrella** (`/zoom-out`+`/grill`+`/diagnose` under one pointer) — survey § 5, deferred pending the (never-shipped) `/iterate` router trial.

### Existing next-step machinery (mostly concentrated in the build loop)
- **Dashboard "Action Required"** — human-gated coverage invariant; every user-blocked item gets a row with the concrete action. Regens at Tier 1 moments.
- **`/work` Step 0** — handoff detection (0a), plan-file discovery (0a2), session recovery (0b), uncommitted-work nudge (0e, FB-088), human-gated queue (0g).
- **`/work` Step 3 "Contextual Command Suggestions"** — already appends 1–3 next-action suggestions at stopping points. ← *the seed pattern for Level 1 below.*
- **Phase & decision gates** (`/work` Step 2b) — on phase complete, suggests `/iterate` for the next phase; unresolved decisions offer `[R]esearch`.
- **`/status`** — read-only "Attention Needed" (decisions pending, human tasks ready).
- **`/iterate` Step 1a** — auto-finalizes checked decisions on every invocation.

> The machinery is real but **build-loop-centric**. The spec-shaping front-end (grill → research → iterate → work) has almost none of it.

---

## 5. Diagnosis

**The build loop is well-orchestrated; the pre-build / vetting / spec-shaping front-end is a chain of individually-excellent but loosely-coupled commands where the user is the integration glue.**

- Every **automatic** handoff is inside/adjacent to `/work` + `/health-check` + verification.
- Every **prose-only** handoff is in the front-end (grill→research→iterate→work).
- The **think/vet commands are orphaned** (no inbound pointer) → pure recall.
- DEC-018 measured build-loop sessions and correctly found low recall friction *there*. The friction Erik feels lives where DEC-018 didn't look.

So the fix is almost certainly **not** "chain commands into meta-commands" (declined router in a costume). It's **workflow legibility + state-carrying handoffs at the front-end.**

---

## 6. Intervention menu (lightest → heaviest)

### Level 0 — Don't build
Some seams are by-design gates (keep). Some "friction" is docs-discoverability (e.g. grill-before-distill is recommended but unknown). A docs pass is near-free.

### Level 1 — Next-step breadcrumbs ★ recommended first
Generalize `/work`'s existing "Contextual Command Suggestions" to **every** command: each ends by surfacing the likely next step with the exact command. e.g. `/grill` → "Next: `/iterate distill`"; `/iterate distill` → "Next: `/work`"; `/work` spec-check on a new feature → "Vet first? `/grill {topic}`". Pure additive guidance — **no new command, no router, no state machine.** Directly attacks recall+ordering. Consistent with minimalism + DEC-018 (it's surfacing, not routing). This is FB-088's pattern, generalized.

### Level 2 — State-carrying handoffs (medium)
Kill the worst **prose-only** handoffs: when `/grill` or `/research` surfaces a decision/spec-change, **write a queued artifact** the next command auto-consumes (extend the precedent where `/feedback review` ready-items already appear in `/iterate` Step 1b). Attacks "re-supply context." Touches a few command defs + one small shared handoff file. Target the 2–3 worst seams (2b, 3c, 1d), not all.

### Level 3 — Lifecycle "you are here" surface (heavier; genuine DEC-018 re-open)
A read-only journey map + current position, **folded into `/status`** (not a new command, not a router): *"Lifecycle: vision✓ → spec✓ → [decompose ← you are here] → build → verify. Next: `/work`."* This is the parked `/walkthrough`/`/preflight` idea done as a map. Gate it on whether L1+L2 already close the gap (trial-the-cheap-thing-first, per DEC-018's own instinct).

### Level 4 — Wrapper / chaining commands (heaviest; likely decline)
`/add-feature` = grill→research→iterate→work as one command. Closest to the declined router + the "combine commands" idea. Named here so it can be **explicitly rejected** rather than drifted into. Probably wrong per DEC-018's reasoning.

**Provisional recommendation:** **L1 now** (high leverage, prior-consistent), **L2 on the 2–3 worst state-losing seams**, **L3 gated** on whether L1+L2 suffice, **L4 declined.**

---

## 7. Open questions for Erik (steer the design)
1. **Journey priority** — which of the three (or others: debugging via `/diagnose`, auditing, shakedown) hurts most in practice? Where do you actually stall?
2. **Intervention appetite** — comfortable starting at L1 (breadcrumbs), or do you want the L3 lifecycle surface designed up front?
3. **Front-end vs build-loop** — does this match your felt experience (build loop fine, front-end loose), or is there build-loop friction the trace missed?
4. **The orphaned think/vet commands** — is "nothing points to them" the real pain, or is it more "even when I remember them, the handoff back is clumsy"?

### Erik's answers (2026-06-22)
1. Keep commands separate ✓. But `/grill` and `/shakedown` are **deliberate ad-hoc excursions** (often a separate conversation) to improve the spec / probe something specific — the friction is **re-entry**: folding their output *back into the flow naturally, when wanted*.
2. The pain is **handoff-back clumsiness**, not recall → **L2 (state-carrying handoffs) is the priority, not L1 breadcrumbs.**
3. All three journeys stall. Plus: **`/shakedown` under-extracts per example** and **under-uses the user**.
4. **Initial spec creation should use `/shakedown` too** (against the spec/vision, pre-build). → **Start here.**

---

## 8. Design — initial-spec journey (active)

### 8.1 Validating fact (confirmed 2026-06-22)
`/iterate` reads **none** of the excursion artifacts: 0 references to `shakedown`, `CONTEXT.md`, or `corpus`. `/iterate distill` reads the vision doc only. The excursion artifacts persist (CONTEXT.md, `.claude/support/shakedowns/*.md`) but nothing in the main flow **consumes** them → 100% manual re-entry. This is the L2 gap, exactly.

### 8.2 Redesigned journey
```
(vision doc)
   │
   ▼  /grill {vision}          excursion — sharpen meaning (often separate convo)
   │                            → writes CONTEXT.md + surfaced decisions
   ▼  ══ merge-back ══         /iterate distill consumes CONTEXT.md + grill findings
   │
   ▼  /iterate distill          → draft spec v1
   │
   ▼  /shakedown (spec mode)    excursion — throw REAL examples at the DRAFT SPEC, find gaps
   │                            → writes corpus with ⚠ gaps + drafted spec-deltas
   ▼  ══ merge-back ══         /iterate surfaces unmerged ⚠ / parked / deltas
   │                            ↕ loop shakedown ↔ iterate until saturation
   ▼  spec v1 hardened
   │
   ▼  /work                     decompose + build
```
Two changes: **(i)** `/shakedown` becomes a spec-creation step (pre-build), **(ii)** **merge-back gates** make `/iterate`/distill proactively consume the excursion artifacts.

### 8.3 Merge-back mechanism — the priority fix
**Behavior (what Erik experiences):** returning to `/iterate` after an excursion, it *greets you with the delta* instead of making you re-state from memory:
> *Excursion findings since last spec update:*
> *— 3 ⚠ gaps from shakedown `personal-style-2026-06-22` (2 unaddressed, 1 parked)*
> *— 2 new CONTEXT terms not reflected in spec*
> *Fold in? [Y] all · [R] review each · [S] skip*

**Mechanism fork:**
- **(a) Spec merge-queue** — `/grill` + `/shakedown` append a structured signal (`{source, ref, kind: gap|term|decision, summary, status: open}`) to a small `.claude/support/.spec-merge-queue.jsonl`; `/iterate` drains it + marks merged. *Proven pattern* (friction register FR-NNN; `/feedback review` ready-items already surface in `/iterate` Step 1b). Unambiguous "what's open." Cost: one tiny state file. ★ lean
- **(b) Artifacts-as-queue** — `/iterate` reads CONTEXT.md + corpus directly, using a "last-merged" marker to compute the delta. No new file; but parsing free-form docs for "what's unmerged" is fuzzy. More minimal, less reliable.

### 8.4 Shakedown — spec-target mode (point 4)
`/shakedown` today is built-system-oriented (grounds against "actual code/real structure"). Add a **spec-target mode** (auto-detected when no build exists, or explicit): grounding shifts to *"does the spec specify how the system handles this example?"* Verdict legend adapts: ✓ spec covers it · ⚠ spec gap (→ spec addition) · ✗ out of scope · ❓ spec ambiguous. Phase-0 lens derives from the spec's described structure, not code. This makes shakedown a **spec-hardening** tool and couples it *even more* naturally to `/iterate` (a ⚠ against a spec *is* a spec delta).

### 8.5 Shakedown — extract more per example (point 3a)
Current loop: restate → breakdown → ground → verdict → write. Add:
- **Generalize:** each concrete example implies a *family* — extract "what class does this represent?" so one example hardens a whole dimension, not just itself.
- **Draft the delta:** for ⚠, don't just label "gap" — draft the *specific spec addition* the example implies (a proposal for `/iterate`, not writing the spec — DEC-016-safe). Full extraction = example → concrete spec delta.
- **Seed acceptance:** for ✓, draft the acceptance/regression probe (currently "optional" → first-class).

### 8.6 Shakedown — use the user more (point 3b)
Today: user dumps examples → Claude verdicts → write (user is *source* then *spectator*). Inject user judgment at the points where Claude currently decides alone — **principle: Claude grounds & proposes; the user adjudicates the judgment calls.** Concretely:
- **Adjudicate flattening** (highest-value): the "expressible-but-flattening" verdict is a *value* call — *"the spec can approximate this as X but loses Y — acceptable, or is Y essential?"* Don't let Claude decide alone.
- **Confirm/challenge the verdict:** propose it, let the user override — keeps the user's model authoritative.
- **Prioritize:** periodically ask which surfaced gaps matter most → corpus carries priority, feeds `/iterate` fold-order.
- **Pull the user's anxieties:** beyond Claude's hypothesis-steering, ask *"what case are you most worried it won't handle?"* — high-signal examples.
- **Throughput resolution** (shakedown is breadth — don't Q&A every example): **auto-verdict the clear ✓/✗; stop and involve the user only on ⚠ (gaps: co-draft delta + priority), flattening calls, and ❓ (ambiguity).** User involvement concentrates where it's load-bearing.

### 8.7 Open forks (need Erik's steer)
- **F1 — merge-back mechanism:** (a) merge-queue file ★ vs (b) artifacts-as-queue.
- **F2 — shakedown interactivity:** is "Claude grounds+proposes, user adjudicates gaps/flattening/ambiguity, auto-verdict clear cases" the right shape — or do you want heavier involvement (co-verdict everything)?
- **F3 — process:** ship as FB items (incremental) or, if the merge-queue is a real architectural commitment, a DEC? (DEC-018 re-open names a fresh DEC for routing-class changes — but this is handoff plumbing + a command upgrade, arguably FB-ship.)

### Erik's F1–F3 answers + the overlap problem (2026-06-22, turn 2)
- **F1:** create the merge-queue file ✓ — *but* resolve how `/feedback` ties in (feedback overlaps with grill especially).
- **F2:** auto-verdict clear cases ✓ — *but* **shakedown's purpose must shine through** (see § 9 reframe): it's for capturing **knowledge only the user has** (edge cases, real incidents, hidden relationships/constraints Claude can't see — out-of-distribution, domain-unique), explained with the user's reasoning. Not "run examples on limited info."
- **F3:** drafting the delta ✓ — *but* `/feedback` has an **impact-assessment** step shakedown wouldn't; resolve where impact-assessment lives.
- **Cross-cutting:** both `/grill` and `/shakedown` **go too deep into repo specifics too fast** → want **general-first, then deepen**.
- **History:** Erik used to lean on `/feedback`, giving extra info at triage + answering a clarifying question or two. With grill/shakedown now present, the boundary is fuzzy — esp. for "an idea not developed yet."

---

## 9. The capture / develop / route family — conceptual model

The three commands overlap because they're all "extract something from the user." The clean cut is **what** each extracts and **at what idea-maturity**:

| Command | Core verb | Pulls from the user | Question | Distinctive step |
|---|---|---|---|---|
| `/feedback` | **capture + route** | the idea + sense of its worth | "what do we do with this?" | **impact assessment** |
| `/grill` | sharpen **meaning** | what you *mean* (fuzzy → precise) | "what do you actually mean?" | branch-walking interrogation |
| `/shakedown` | capture **world-knowledge** | what you *know* that Claude can't see — edge cases, real incidents, hidden constraints | "what does reality throw at this that I can't see?" | example-grounding + boundary map |

### Shakedown purpose reframe (lead with this in the command)
Not "Claude tests the system." Shakedown is the **channel for knowledge only the user has** — edge cases, real-world incidents, relationships/constraints Claude structurally can't see (out of training distribution, domain-unique). The user asserts concrete examples *with reasoning*; the system grounds each and captures it as a durable spec-delta + boundary map. **Auto-verdicting clear cases exists to clear the deck so the dialogue concentrates on what only the user knows.** "Use the user more" isn't UX polish — the user is the *source of the information that gives shakedown its value*.

(Contrast: grill extracts what you *mean* — you have the meaning, it's just fuzzy. Shakedown extracts what you *know about reality* — facts Claude lacks. Different privileged information.)

### Composition
- **`/feedback` = inbox + dispatcher, NOT a mandatory gate.** Captures any idea (incl. undeveloped). Triage does a **light clarify** (a question or two — to *route*, not to develop). When an item needs more, triage **escalates**: → `/grill` (gap is *meaning*) or `/shakedown` (gap is *world-knowledge/edge-cases*). Grill/shakedown also stay **directly enterable** as ad-hoc excursions.
- **feedback↔grill boundary** (the overlap Erik named): feedback-triage = *quick clarify to route*; grill = *deep interrogation to develop*. Triage hands off to grill rather than becoming grill.
- **Shared plumbing = the merge-queue** (F1). Grill/shakedown (and feedback) emit developed findings → `/iterate` drains into the spec.
- **Impact assessment stays in `/feedback`** (don't duplicate into shakedown). Shakedown drafts the *delta* (the *what*); feedback assesses *impact* (worth + blast radius). Routing is **maturity-dependent**:
  - *Initial-spec creation* → nothing to impact-assess → shakedown → `/iterate` directly.
  - *Mature-project feature-add* → developed delta routes **back through `/feedback`** for impact assessment → then `/iterate`.

### Cross-cutting conduct fix (grill + shakedown)
**General-first, then deepen.** Open at the conceptual/general level, confirm the frame with the user, *then* progressively delve into repo specifics. Refines shakedown Phase 0 + grill's interrogation discipline. (Today both dive into internals too fast.)

### Open forks (need Erik's steer)
- **G1 — feedback as dispatcher-not-gate:** confirm grill/shakedown stay directly enterable AND feedback can escalate to them. (vs. making feedback the single front door.)
- **G2 — impact-assessment routing:** confirm it lives only in feedback, and a mature-project shakedown-delta routes back through feedback before `/iterate`. (Open detail: does the merge-queue carry a "needs impact-assessment" flag, or does `/iterate`'s drain decide? — settle after the model is confirmed.)
- **G3 — escalation explicitness:** should feedback-triage *actively offer* "this needs a grill/shakedown — want to run one?" (an escalation prompt), or just document the boundary and leave it to the user?
- **G4 — merge-queue scope:** one queue for all three producers (feedback/grill/shakedown), or per-source? (Lean: one queue, `source` field — mirrors friction register.)

### Erik's confirmations (2026-06-22, turn 3)
**G1 ✓** dispatcher-not-gate · **G2 ✓** impact-in-feedback · **G3 ✓** active-offer escalation · **G4 ✓** one queue. → Build plan below.

---

## 10. Build plan

### Process
- **DEC for the spine.** The capture/develop/route model (§9) + the merge-queue is a real multi-command commitment with cost-of-reversal; DEC-018's re-open explicitly invites a DEC for workflow-class changes. The reasoning is already done (turns 1–3) → a **record DEC** (model + chosen options G1–G4 + F1/F3), not a heavy `/research` spike. Home: root `decisions/` (template decision). *Alternative:* skip DEC, ship as an FB bundle (faster, thinner rationale).
- **FB items for the limbs** — per-command implementations sequenced under the DEC.

### Phasing

**Phase A — Foundation (all journeys)**
- **A1.** Merge-queue schema + new `.claude/support/reference/merge-queue.md` (mirror `friction-register.md`). One queue `.claude/support/.spec-merge-queue.jsonl`; schema: `{id, source: grill|shakedown|feedback, origin_ref, kind: gap|term|decision|delta, summary, drafted_delta?, status: open|merged|dismissed, needs_impact_assessment: bool, created}`.
- **A2.** *(optional, later)* `persist-merge-item.py` mirroring FB-098's `persist-friction.py` (collision-safe IDs, append-only). Prose protocol first; script if it earns it.

**Phase B — Initial-spec journey (START HERE — Erik's pick)**
- **B1.** `/iterate` + `/iterate distill` **drain** the queue (+ read `CONTEXT.md`): on entry, surface open items as the merge-back prompt (§8.3); mark merged/dismissed on resolution. ← *priority payoff (the re-entry fix).*
- **B2.** `/shakedown` rewrite: **purpose reframe leads** (§9 — "knowledge only you have"); **spec-target mode** (§8.4); **general-first conduct** (§9); **extract-more** (generalize → family, draft-delta, seed-acceptance, §8.5); **use-user-more** (§8.6); **emit** ⚠/deltas to queue (`source=shakedown`); maturity-aware routing (G2).
- **B3.** `/grill`: **general-first conduct**; **emit** decisions/spec-changes to queue (`source=grill`). (CONTEXT.md vocab already handled.)
- **B4.** `spec-workflow.md` initial-spec journey update (+ shakedown-in-spec-creation); CLAUDE.md `/shakedown` one-liner reframe.

**Phase C — Feature-add / mature project (journeys 2 & 3)**
- **C1.** `/feedback`: dispatcher/escalation — triage **actively offers** grill/shakedown when an item exceeds light-clarify (G1/G3); document the *light-clarify-to-route* vs *deep-develop* boundary; impact-assessment as the home (G2), incl. picking up returning shakedown-deltas (`needs_impact_assessment: true`) for mature projects.
- **C2.** Family-model section (§9) into `spec-workflow.md` (or a short reference doc).

### Sequencing logic
A → **B1** (drain delivers re-entry value with *any* producer) → **B2** (shakedown, the focus) → B3/B4 → C. **B1 + B2 = a working initial-spec loop** (shakedown → queue → iterate).

### Dependency / risk checks
- **DEC-016:** shakedown drafting a delta is safe (proposes, never writes spec); `/iterate` applying merged items runs its normal propose-approve-apply + the DEC-016 ask gate. ✓
- **Subagent boundary (DEC-004):** grill/shakedown/feedback/iterate are main-thread user-driven commands → they *can* write `.claude/` (not subagents). ✓
- **Merge-queue is project state** (like `friction.jsonl`/tasks) → project-side likely gitignored; template ships the reference doc + producing/draining logic, not a populated queue.
- **Scope creep guard:** Phase C (feedback) is journey-2/3 work — don't pull it into the initial-spec build unless B1/B2 surface a real need.

---

## 11. Vision as the development hub — styler evidence + model revision

**Erik's flag (turn 4):** he uses the **vision doc** as the workspace to develop *larger* features broadly — repeated `/grill` + `/shakedown` passes until tight, *before* the spec. Fear: pointing grill/shakedown at the *spec* would cannibalize this. Pointed me at styler's last 3–4 visions. **The evidence overturns the centerpiece of the plan.**

### 11.1 Finding — the vision is a sophisticated, already-templated recurring per-feature workspace
Not the template's "one-time pre-spec brainstorm." Styler has ~11 feature visions (Mar–Jun 2026) + 26 dated shakedown corpora, evolving through many grill/shakedown/decide/iterate passes. **Erik has already converged on an implicit "feature-vision" template** — the template should *formalize his pattern*, not impose a new merge-queue.

### 11.2 The de-facto feature-vision structure (extracted from styler)
1. **Immutable header** — `Status` (vision/distilled-to-spec/historical) · `Captured` · `Author` · `Supersedes` · `Predecessors` · scope IN/OUT.
2. **Thesis + framing** — north-star, the gap, non-negotiables.
3. **Structural sections** (§1, §2…) named for the *actual subsystem*, each opening with a **maturity banner** — 🟢 SHIPPED / 🔵 RESEARCHED / 🟡 DRAFTED — **citing verifiable evidence** (corpus refs, commits, test counts), not a feeling.
4. **Open-forks tracker** — each fork → its **named probe tool** (`→ /grill`, `→ /shakedown`, `→ /research`, code) + resolution (struck through w/ `DEC-###` + date) or pending.
5. **Status map** (table: Thread | Maturity | Next step | Tool).
6. **Evidence index** — canonical map: where each thread lives (spec § / code / config / corpus / decision). Corpora are **cited, never copied**.
7. **Dated amendment blocks** — refinement layers (date + who + what + verification + source link).
8. **Immutability note** — once distilled → spec, the vision is **read-only**; further changes route via `/iterate`.

### 11.3 The awkwardness Erik sensed ("no structure, kind of weird")
- **Open questions scattered across 3 surfaces** (e.g. personal-style-engine §3.6 + §5 + §8 all track forks) → want **one canonical fork-tracker**.
- **Amendment blocks are prose-heavy**, not structured (contrast the crisp header block).
- **Shakedown findings land inconsistently** — sometimes inline, sometimes in a separate §8/§9 annotation layer.
- **Calibration-vs-fork** not always distinguished in the fork list.

### 11.4 Two tensions with the *current* template
- **DEC-016 vision protection vs. co-refinement.** The template treats vision as paste-from-Claude-Desktop + protected (Claude shouldn't edit). Erik's practice has Claude **co-refining the vision in-place** across passes (amendment blocks say "Erik's request, this session"). **Reconciliation that matches his practice:** vision is **editable during development, immutable after graduation to spec** (his immutability note already encodes the second half). DEC-016's vision stance needs this carve-out.
- **One-time vs. recurring.** Template frames vision as initial-spec ideation; Erik uses it as a **recurring per-feature** workspace. The structure must support the lifecycle, not fight it.

### 11.5 Model revision
- **Vision = the hub/destination for larger features.** grill/shakedown findings fold *into the structured vision* (fork-tracker verdicts + linked corpora + amendment blocks), which matures (🟡→🔵→🟢) until tight, then graduates to spec via `/iterate`.
- **grill/shakedown become target-aware:** **vision** (primary, larger features) · **spec** (secondary, hardening committed scope / smaller direct changes) · **build** (original shakedown target). Spec-target mode (§8.4) is the *secondary* mode, not the centerpiece.
- **Merge-queue retargeted, possibly demoted.** Erik's structured vision IS the accumulation surface — so for larger features the "merge-back destination" is the vision, not a queue. Residual queue role: the *transport* that flags "shakedown corpus Y has findings not yet folded into vision fork X / spec §Z — fold them?" carrying a `target: vision|spec`. **Open: is the queue still worth it, or do grill/shakedown just fold into the vision directly?** (See D3.)

### 11.6 Revised build-plan shape (supersedes §10 phasing where it conflicts)
- **Phase 0 (NEW, front) — Formalize the feature-vision structure.** A vision scaffold (`.claude/vision/_TEMPLATE.md` or analog) + documented conventions (the §11.2 skeleton) + fix the §11.3 awkwardness (one fork-tracker; structured amendment blocks) + the DEC-016 editable-during-dev / immutable-after-graduation carve-out. *This is the flagged gap + the hub everything else hangs off.*
- **grill/shakedown target-awareness** (vision primary) — folds into the structured vision; spec-target is secondary.
- **vision→spec graduation** via `/iterate` — formalize the maturity-flip + immutability.
- Merge-queue: decide D3 before building it.

### 11.7 Decisions for Erik
- **D1 — centerpiece:** make *formalizing your feature-vision structure* the front of the plan (vs. the merge-queue)? (Lean: yes — it's your real workflow + the gap you flagged.)
- **D2 — vision editability:** adopt **editable-during-development, immutable-after-graduation** (update DEC-016's vision stance to match)? (Lean: yes — matches your practice.)
- **D3 — merge-queue fate:** (a) drop it; grill/shakedown fold directly into the structured vision/spec · (b) keep it retargeted as a `target: vision|spec` transport that surfaces un-folded corpus findings on re-entry. (Lean: (b)-lite — the re-entry surfacing is the original pain, even with a structured vision as destination.)
