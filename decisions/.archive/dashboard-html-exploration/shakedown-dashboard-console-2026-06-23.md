# Shakedown — HTML dashboard console (render-target design)

**Date:** 2026-06-23 · **Target:** the `dashboard.html` prototype as a *build* (grounded against what it renders today). **Adaptation:** template-maintenance design-validation — corpus kept here in the workspace, no project merge-queue emission.

## Lens (confirmed)

- **Purpose:** does the HTML console hold up across the full range of real dashboard states the user's projects produce — not just styler's 99%-done happy path — well enough to justify building Option B (a derived, read-only, gitignored HTML render target alongside `dashboard.md`)?
- **Primary cleave (confirmed):** **display vs. interaction.** The Markdown dashboard is a read-*write* control surface (the user edits checkboxes / text / toggles in-place; Claude reads them back via the marker+sidecar system). A derived HTML *view* is read-only. Hypothesis: display states → HTML wins; interaction states → must stay in Markdown/CLI.
- **Verdict legend:** ✓ handled · ⚠ gap (HTML-expressible, feeds build scope) · ⛔ **boundary** (interaction the read-only view structurally can't host) · flatten (renders but loses something) · ✗ out of scope · ❓ split.
- **Dimensions per example:** section · render-affordance needed · **read vs write-back** · consumption axis (human / Claude-reread / git / offline) · scale-trigger.
- **Corpus:** 11 real downstream dashboards swept (`sweep.py`); positive control `SECTION TOGGLES` hit 11/11.

## Model so far — the boundary this shakedown draws

The cleave holds, with a sharpened sub-finding: **the interaction features are not rare edge cases — they're the spine of small/mid dashboards.** A read-only HTML view can render *about* them but cannot *be* the surface the user acts on. Net boundary:

> The HTML console is a strong **read** surface for **display-at-scale** (many decisions / many phases). It is **not** a substitute for the Markdown dashboard as a **control surface**. Every project keeps acting in Markdown/CLI; the HTML is a parallel lens, valuable in proportion to how much there is to *read* (≈ project size).

## Boundary criteria (in / out for the HTML view)

- **IN (display, HTML wins, scale-gated):** decisions list (search/filter/collapse), phase roll-up (active vs 50-collapsed), status summary, acceptance criteria, blocked/partial/on-hold badges, timeline, mermaid, custom-views render, retired-features list.
- **OUT (interaction, stays in Markdown/CLI):** phase-gate ticks, inline-feedback entry, out-of-spec approve/reject, both-await-review sign-off, audit promote/dismiss/fix, section-toggle edits.

---

## ⛔ INTERACTION family — the boundary (read-only view cannot host; majority of dashboards)

| # | Family | Real examples (cited) | Grounding vs prototype | Verdict |
|---|--------|----------------------|------------------------|---------|
| I1 | **Phase-gate checkboxes** | `nordgrid:32-34` (3× `PHASE GATE:N→N+1 APPROVED`); also PQ-CC(5), SIREN(1), flirty-gym(2) — **4/11** | Pre-approval these render `- [ ] Approve transition` boxes the user *ticks*; the tick is read back to gate `/work`. HTML view can show the gate but can't host the tick. | ⛔ boundary |
| I2 | **Inline feedback write-back** | `nordgrid:58-71` (`<!-- FEEDBACK:1 -->` "[Leave feedback here, then run /work complete 1]"); SIREN, target-BOM, PQ-CC, renovation — **5/11** | User *types prose* into the marker block; Claude reads it via sidecar on `/work complete`. A read-only view has nowhere to type that writes back. | ⛔ boundary |
| I3 | **Section-toggle edits** | `nordgrid:25,27` (`- [ ] Decisions`, `- [ ] Custom Views`); **8/11** have ≥1 section off | The user edits the checklist to control what renders. (a) The view has no equivalent control; (b) the prototype *ignores* toggles and renders everything — a correctness gap even as a view. | ⛔ boundary + ⚠ (prototype must respect toggles) |
| I4 | **Out-of-spec / task Reviews approval** | `OEMMatInsightBI:52-56` (Reviews: task 021 "review the diff… confirm the call"); styler — **2/11** | `[A]ccept / [R]eject / [D]efer` is a write to task state. View can list, can't approve. | ⛔ boundary |
| I5 | **Both-owner await-review sign-off** | `nordgrid:55` ("✅ Verified — awaiting your review… run /work complete 24"); styler — **2/11** | The sign-off (`/work complete {id}`) is the action; view can surface it but the act is CLI. | ⛔ boundary (degrades to a prompt) |
| I6 | **Audit findings promote/dismiss/fix** | `OEMMatInsightBI:42-48` (🔎 table: C-02→FR-004, FR-002, FR-003); `nordgrid:46-48` empty-state — **≥2/11** *(sweep false-negative: `🔎`≠`🔍`)* | `[Fix it]` / promote (tick+command) / dismiss are writes. View can render the list, not the actions. | ⛔ boundary |

**I-family conclusion:** six independent interaction families, present across the **majority** of real dashboards (and *dominant* in small ones). They converge on one structural fact — **the dashboard is a control surface, not just a display.** This is the load-bearing finding for the value call (see "For the user").

---

## ⚠ DISPLAY-GAP family — prototype doesn't render, but HTML easily can (build scope, not boundary)

| # | Family | Real examples | Verdict |
|---|--------|--------------|---------|
| D1 | **Timeline + overdue** | `renovation:84-91` (`~~2026-01-28~~ ⚠️ OVERDUE`), styler:166 — 2/11 | ⚠ omitted; HTML renders it *better* (sortable, red overdue). A latent HTML win. |
| D2 | **External dependencies** | `renovation:91` ("External: Flooring delivery… Contact: Bob"), styler, tinder — 3/11 | ⚠ omitted; trivial to add. |
| D3 | **Mermaid project-overview** | 5/11 (OEM, SIREN, renovation, difficult-conv, styler) | ⚠ prototype omits. Note: `OEMMatInsightBI:71` FB-007 — the *current* `dashboard-render.py` reintroduces a broken mermaid each regen (hyphen→phantom nodes). HTML+mermaid.js could sidestep that bug. |
| D4 | **Custom Views** | `PortfolioWebsite:80`, SIREN, renovation — 3/11 | ⚠ prototype omits the section. LLM-rendered content; HTML can host. |

## flatten family — renders but loses something

| # | Family | Real examples | Verdict |
|---|--------|--------------|---------|
| F1 | **Absorbed tasks** | PQ-CC, SIREN(2), styler — 3/11 | flatten — prototype shows only the count stat-card; loses the `Absorbed → Task X` audit trail. |
| F2 | **Retired features** | `styler:612` (13 entries) | flatten — dumped into Notes prose; HTML *could* structure it better (opportunity, not just loss). |
| F3 | **Cross-phase tasks** | `OEMMatInsightBI:164` (6×), styler (6×) — 2/11 | flatten — shown as raw title text; no `(cross-phase)` affordance. |

## ✓ HANDLED-WELL family (auto-verdicted, deck cleared)

- Status summary 7/11 → ✓ stat-cards. · Acceptance criteria 4/11 → ✓ collapsed disclosure. · Blocked/partially-actionable phases 4/11 + styler → ✓ badges + active/complete split. · On-hold (styler 8×, tinder 6×) → ✓ Action Required + badges. · Decisions-at-scale (styler 141) → ✓✓ the showcase.

## Parked — spec features NOT observed in any real dashboard (untested; do NOT fabricate)

`repair_retries` 0/11 · `verification_pending` 0/11 · `spec_drift` 0/11. Real data says these states don't occur in the user's projects → low build priority. (Distinct from "the prototype fails them" — they were never exercised; the method forbids inventing them.)

## Scale finding (emergent dimension)

Small projects (nordgrid 27 tasks, PQ-CC, PortfolioWebsite 120 lines) are **dominated by the ⛔ interaction families** and already fit one Markdown viewport — so the HTML view (a) has almost nothing to collapse/search and (b) can't host their interactions. **HTML's value rises with read-volume (≈ project size); it approaches zero for small projects.** Sharpens Option B's size-threshold: gate on decisions/tasks count, and don't bother below it.

## Saturation

Near saturation on families — the last several real examples (audit table, cross-phase, custom views) added no *new* structural dimension beyond display-vs-interaction + scale. One or two user-supplied examples (a worry I can't derive) could still move it.
