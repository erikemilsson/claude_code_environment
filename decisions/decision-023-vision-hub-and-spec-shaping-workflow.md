---
id: DEC-023
title: Spec-shaping workflow — vision-as-development-hub, target-driven grill/shakedown, and the capture/develop/route family
status: implemented
category: process
created: 2026-06-22
decided: 2026-06-22
implemented: 2026-06-23
related:
  tasks: []
  decisions: [DEC-016, DEC-018, DEC-019, DEC-021, DEC-022, DEC-004]
  feedback: [FB-101, FB-102]
implementation_anchors:
  - file: ".claude/vision/_feature-vision-template.md"
    description: "Phase 0 — feature-vision scaffold (maturity banners, one fork-tracker, structured amendments)"
  - file: ".claude/rules/spec-workflow.md"
    description: "Vision-as-hub lifecycle + target-awareness + DEC-016 vision carve-out + working-backward pointer"
  - file: ".claude/support/reference/merge-queue.md"
    description: "Phase A — the re-entry transport contract (schema + protocols + composition with the vision fork-tracker)"
  - file: ".claude/commands/iterate.md"
    description: "Phase B — Step 1c drains the merge queue on entry"
  - file: ".claude/commands/grill.md"
    description: "Phase B — emit to merge queue + general-first conduct"
  - file: ".claude/commands/shakedown.md"
    description: "Phase B — purpose reframe + target-awareness + general-first + extract-more + use-the-user-more + emit"
  - file: ".claude/commands/feedback.md"
    description: "Phase C — dispatcher (escalation offers + impact-assessment home for returning deltas)"
  - file: ".claude/CLAUDE.md"
    description: "Navigation (merge-queue) + Critical Invariant (vision editability) + /shakedown one-liner"
  - file: "decisions/decision-016-spec-file-edit-guardrail.md"
    description: "Amended — vision portion (editable-during-dev / frozen-after-graduation)"
  - file: ".claude/version.json"
    description: "template_version 4.28.0 → 4.31.0 (Phases 0 / A+B / B-reframe / C)"
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# Spec-shaping workflow — vision-as-development-hub, target-driven grill/shakedown, and the capture/develop/route family

## Select an Option

Mark your selection by checking one box:

- [ ] Option A — **Status quo.** Keep the commands as-is; the user remembers which to fire and in what order; excursion findings are folded back by hand. (This is the friction that prompted the review.)
- [ ] Option B — **Interpretive router / wrapper commands.** A meta-layer that maps intent → command, or `/add-feature`-style chains. (DEC-018 already declined the router on value grounds; re-examined here and declined again — it doesn't address the *handoff/re-entry* friction, which is the real pain.)
- [x] Option C — **Spec-shaping workflow model (this design).** Vision as a first-class recurring **development hub** for larger features; **target-driven** grill/shakedown (vision · spec · build); a lightweight **re-entry transport**; impact-assessment kept in `/feedback`; **general-first conduct**; `/shakedown` reframed around user-held knowledge. **Recommended.**

*Check Option C to approve the design below and authorize the phased build.*

---

## Background

**Trigger.** A `/feedback review` (FB-101/FB-102) opened into a broader user ask: the command surface is individually strong but *"fully dependent on the user remembering them and firing them in the right order,"* and *"some don't work together as smoothly as I'd like."* Full analysis + the command catalog, handoff graph, journey traces, and styler evidence live in `template-maintenance/command-workflow-analysis.md` (§ 1–12); this record captures the decision.

**Diagnosis (analysis § 5).** Two distinct frictions: **(1) recall + ordering** and **(2) handoff smoothness** (state doesn't carry; the next step isn't surfaced). The build loop (`/work` + dashboard + verification) is well-orchestrated — every *automatic* handoff lives there. The **spec-shaping front-end** (grill → research → iterate → work) is a chain of individually-excellent but loosely-coupled commands where *the user is the integration glue*: every handoff there is **prose-only** (a command says "you might run /X" but carries no state), and the think/vet commands (`/grill`, `/shakedown`, `/research`, `/zoom-out`, `/review`) are **orphaned** from the graph (nothing points to them → pure recall). Confirmed structurally: `/iterate` reads **none** of the excursion artifacts (0 references to the shakedown corpus / CONTEXT.md), so excursion output is stranded and re-stated from memory.

**The user's reframe (analysis § 8.7, § 11).** The real pain is **re-entry**, not forward-recall: `/grill` and `/shakedown` are deliberate, often-separate-conversation **excursions** to develop or probe something; the friction is folding their output *back into the flow naturally*. And critically — the **vision document** is already used as a **recurring per-feature development hub**: larger features get developed broadly in a vision via repeated grill/shakedown passes *until tight*, then graduate to spec. The template treats vision as one-time pre-spec ideation; the user's practice is far richer (styler: ~11 feature visions + 26 dated shakedown corpora, Mar–Jun 2026, with a remarkably consistent implicit structure — analysis § 11.2).

**Why a decision record.** This is a multi-command architectural change with cost-of-reversal (a new shared transport + a formalized vision structure + altitude-aware commands touching `/grill`, `/shakedown`, `/iterate`, `/feedback`), and it **amends DEC-016's vision stance** (a governance boundary). DEC-018's re-open condition explicitly names "a fresh DEC" for workflow-class changes that resurface as the command surface grows (Wave 1/2 + DEC-019 grew it). Reasoning was done collaboratively (not a `/research` spike); this record documents it for sign-off.

## The model (Option C)

### 1. Three altitudes; the target sets the altitude
Grill/shakedown become **target-aware**, and *what you point them at* selects the path — no separate routing decision:

| Change size | Aim grill/shakedown at | Develop | Apply | Vision hub? |
|---|---|---|---|---|
| Small refinement (one section) | `spec §X` directly (DEC-021 section index scopes the read) | probe just that section | `/iterate` (section-scoped) | no |
| Larger feature | a vision doc | repeated passes fold into the structured vision; mature 🟡→🔵→🟢 | `/iterate` distill / graduate | **yes** |
| Built-system behavior | the running build | shakedown corpus | route ⚠ to vision or spec | depends |

**Escalation:** a path can grow — a section probe that turns out to be a feature spins up a vision hub (as feedback-triage escalates to grill/shakedown). The user is never trapped at the wrong altitude.

### 2. Vision = the development hub (centerpiece — D1)
Formalize the user's de-facto "feature-vision" structure (analysis § 11.2) so larger features have a structured home that accumulates grill/shakedown findings: immutable header (Status · Captured · Author · Supersedes · scope) · thesis · **sections with maturity banners** (🟢 SHIPPED / 🔵 RESEARCHED / 🟡 DRAFTED, each citing verifiable evidence) · **one canonical open-forks tracker** (each fork → its probe tool + resolution/pending) · status map · **evidence index** (where each thread lives — corpora *cited, never copied*) · structured dated amendment blocks · immutability note. This *also* fixes the awkwardness the user flagged (analysis § 11.3: forks scattered across 3 surfaces; prose-heavy amendments; inconsistent finding placement).

### 3. Capture / develop / route family (analysis § 9)
Three distinct verbs, no new commands:

| Command | Core verb | Pulls from the user | Distinctive step |
|---|---|---|---|
| `/feedback` | capture + route | the idea + sense of its worth | **impact assessment** |
| `/grill` | sharpen **meaning** | what you *mean* (fuzzy → precise) | branch-walking interrogation |
| `/shakedown` | capture **world-knowledge** | what you *know* that Claude can't see (edge cases, real incidents, hidden constraints) | example-grounding + boundary map |

`/feedback` is the **inbox + dispatcher, not a gate**: triage does a light clarify, and **actively offers** to escalate to `/grill` (meaning gaps) or `/shakedown` (world-knowledge gaps) — grill/shakedown also stay directly enterable. **Impact assessment stays in `/feedback`**: shakedown drafts the *delta*; for a mature-project feature the delta routes back through `/feedback` for impact assessment before `/iterate`; for initial-spec it goes straight to `/iterate`.

### 4. Re-entry transport (D3 — lightweight)
One **merge-queue** (`source` + `target: vision|spec` fields; mirrors the friction register) carries excursion findings so that on return, `/iterate` (or the vision) surfaces *un-folded* findings — *"shakedown corpus Y has findings not yet folded into vision fork X / spec §Z — fold them?"* — instead of re-stating from memory. The **structured vision is the destination** for the larger-feature altitude; the queue is the transport that prevents stranding, especially across conversations.

### 5. `/shakedown` reframe + conduct (analysis § 9, § 8.5–8.6)
- **Purpose leads:** shakedown is the channel for **knowledge only the user has**; auto-verdicting clear ✓/✗ exists to **clear the deck** so the dialogue concentrates on what only the user knows (gaps, flattening calls, ambiguity). "Use the user more" is the mechanism, not polish.
- **Extract more per example:** generalize each example to its *family*; draft the spec-delta (a proposal — never writes the spec, DEC-016-safe); seed an acceptance probe for ✓.
- **General-first conduct (both grill and shakedown):** open at the conceptual level, confirm the frame, *then* deepen into repo specifics (today both dive into internals too fast).

### Design parameters (resolved in conversation)
| Ref | Decision |
|---|---|
| D1 | Formalize the feature-vision structure as the centerpiece (over a queue-centric design). |
| D2 | Vision is **editable during development, immutable after graduation** to spec — **amends DEC-016's vision stance**. |
| D3 | Keep a lightweight re-entry transport (the merge-queue), retargeted `vision|spec`. |
| G1 | `/feedback` = dispatcher, not gate; grill/shakedown stay directly enterable + feedback can escalate to them. |
| G2 | Impact-assessment lives only in `/feedback`; mature-project shakedown-deltas route back through it before `/iterate`. |
| G3 | feedback-triage **actively offers** the grill/shakedown escalation. |
| G4 | One merge-queue with a `source` field (not per-source). |
| F1 | The merge-queue file is created (the transport). |
| F3 | Shakedown *drafts* the spec-delta as a proposal (never writes spec — DEC-016-safe). |

## Tensions reconciled (analysis § 11.4)
- **DEC-016 vision protection vs. co-refinement.** DEC-016 currently treats `.claude/vision/**/*.md` as paste-from-outside + structurally gated (`permissions.ask`). The user's practice has Claude co-refining the vision in-place across passes. **D2 reconciliation:** vision is editable during development, frozen after graduation. *Implementation question deferred to build:* how the `permissions.ask` gate + DEC-016's carveout encode "dev-phase editable / post-graduation frozen" (the gate can't trivially distinguish the two states — likely a status-frontmatter-driven convention + a documented carveout). The DEC sets the principle; the build resolves the mechanism.
- **One-time vs. recurring.** Vision reframed from one-time ideation to a recurring per-feature workspace; the structure supports the lifecycle.

## Options Comparison

| Criterion | A — Status quo | B — Router / wrappers | C — This design |
|---|---|---|---|
| Addresses recall+ordering | ✗ | ✓ (router) | ✓ (target-sets-altitude + dispatcher offers) |
| Addresses handoff/re-entry (the real pain) | ✗ | ✗ (router maps intent, not state) | ✓✓ (transport + structured vision destination) |
| Honors DEC-018's value finding | ✓ (no change) | ✗ (the declined router) | ✓ (surfacing/plumbing, not intent-routing) |
| Matches the user's actual workflow | – | ✗ | ✓✓ (formalizes the styler vision practice) |
| New command surface | none | high (router/wrappers) | none (upgrades existing commands) |
| Cost of reversal | n/a | high | moderate (transport + vision template + per-command edits; each reversible) |
| Fixes the "vision has no structure" gap | ✗ | ✗ | ✓✓ |

## Recommendation

**Option C.** It targets the friction that actually bites (handoff/re-entry), formalizes a workflow the user has already validated in practice (the styler vision hub), adds **no new command surface**, and stays clear of DEC-018's declined router while honoring its re-open call for a DEC. Confidence **high** on the model; the one genuinely open mechanism (the DEC-016 dev/frozen gate encoding) is bounded to the build phase and flagged.

## Build plan (phased; implementation_anchors populated on completion)

Supersedes the earlier §10 phasing where it conflicts (the vision-structure work moved to the front).

- **Phase 0 — Formalize the feature-vision structure.** Vision scaffold (`.claude/vision/_TEMPLATE.md` or analog) + documented conventions (§ 11.2 skeleton) + fix the § 11.3 awkwardness (one fork-tracker; structured amendment blocks) + the DEC-016 editable-during-dev / immutable-after-graduation carve-out. *The hub everything hangs off + the gap the user flagged.*
- **Phase A — Re-entry transport.** Merge-queue schema + `.claude/support/reference/merge-queue.md` (mirror `friction-register.md`); one queue, `source` + `target` fields. Optional later: a `persist-merge-item.py` (mirror FB-098's `persist-friction.py`).
- **Phase B — Target-aware grill/shakedown + drain.** `/shakedown` reframe (purpose-leads) + target-awareness (vision primary) + general-first + extract-more + use-user-more + emit-to-queue; `/grill` general-first + emit; `/iterate` (+ distill) **drain** the queue + read CONTEXT.md (the merge-back payoff); vision→spec graduation (maturity-flip + immutability).
- **Phase C — feedback dispatcher.** Active grill/shakedown escalation (G1/G3) + impact-assessment home (G2) incl. picking up returning shakedown-deltas (`needs_impact_assessment`).
- **Docs.** `spec-workflow.md` (the model + altitudes + vision lifecycle), `agents.md`/reference (the family model), `.claude/CLAUDE.md` navigation + `/shakedown` one-liner reframe, DEC-016 amendment.

**Sequencing:** Phase 0 → A → B (the working loop) → C. Risk checks: shakedown drafting deltas is DEC-016-safe (proposes, never writes spec); grill/shakedown/iterate/feedback are main-thread user commands → can write `.claude/` (no DEC-004 conflict); merge-queue is project state (likely gitignored downstream; template ships the reference + logic).

**Version bump on promotion:** likely MINOR per phase (new conventions + command upgrades; no task-schema change). The DEC-016 vision-gate change is the one piece to watch for MAJOR-ness (permission-layer touch) — assess at Phase 0.

## Your Notes & Constraints

*This section is yours — Claude reads it but never overwrites it.*

**Constraints:**
- Template repo: this changes template workflow/governance, not a project build. Source of truth is `system-overview.md` + the rules files + the analysis doc.
- D2 amends DEC-016 — keep the `/iterate`-routing + `permissions.ask` behavior intact for genuine post-graduation spec/vision edits; only the *development-phase vision* gets the editability carve-out.

**Open question carried to the build (not blocking sign-off):**
- How to encode "vision editable during development, frozen after graduation" against the `permissions.ask` gate (status-frontmatter convention + documented carveout is the leading idea).

## Decision

**Selected: Option C — the spec-shaping workflow model.** User sign-off 2026-06-22 (checked Option C). Approved to proceed with the phased build, Phase 0 first.

**Rationale:** Option C targets the friction that actually bites — handoff/re-entry, not forward-recall — which neither the status quo (A) nor the interpretive router (B, declined again per DEC-018) addresses. It formalizes a workflow the user has already validated in practice (the styler vision-as-hub: ~11 visions + 26 shakedown corpora), adds **no new command surface**, and stays clear of DEC-018's declined router while honoring its re-open call for a fresh DEC. The one open mechanism (encoding DEC-016's dev-editable / graduated-frozen vision gate) is bounded to Phase 0 and resolved with the user there.

Design parameters as tabled (D1/D2/D3, G1–G4, F1/F3). DEC-023 **amends DEC-016's vision stance** (D2): vision is editable during development, immutable after graduation — DEC-016 gets a reciprocal cross-reference when the carve-out lands in Phase 0.

## Implementation

Shipped across four MINOR releases (2026-06-22 → 2026-06-23), status `implemented`:

- **v4.28.0 — Phase 0:** feature-vision scaffold + hub-model lifecycle + DEC-016 vision carve-out (editable-during-dev / frozen-after-graduation; gate kept).
- **v4.29.0 — Phase A+B:** merge-queue transport contract (`merge-queue.md`) + `/iterate` Step 1c drain + `/grill`/`/shakedown` emit hooks — re-entry live.
- **v4.30.0 — Phase B reframe:** `/shakedown` purpose-leads + target-aware (vision/spec/build) + general-first + extract-more + use-the-user-more; `/grill` general-first.
- **v4.31.0 — Phase C:** `/feedback` dispatcher — `[G] Develop` escalation + the light-clarify-vs-deep-develop boundary + impact-assessment home for returning merge-queue deltas (G2).

Per-ship detail in `template-maintenance/ship-log.md`; substrate/analysis in `template-maintenance/command-workflow-analysis.md`.
