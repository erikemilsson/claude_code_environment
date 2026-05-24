# `/visual-verify` — Vision Doc

**Stage:** RESOLVED via `/grill` (2026-05-24) — see Resolution below. The open questions at the bottom were the grill targets; all are now answered. The pre-grill exploration is preserved below as the record of how the conclusion was reached.

**Scope:** template-maintenance artifact (a candidate template command). Does NOT go through the `.claude/` project spec/`/iterate` workflow — that's for projects *using* the template.

---

## Resolution (post-grill, 2026-05-24)

**Outcome: do NOT build `/visual-verify` as a command. Fold into `/diagnose`.** The grill walked all 8 open questions; the design tree collapsed onto `/diagnose`'s existing six phases (Phase 1 option 4 is a browser-MCP feedback loop; Phase 3 is the falsifiable-hypothesis discipline; Phase 5 is conditional persistence). The genuinely visual-specific residue is ~20 lines.

- **Shipped now (v4.10.2):** the outcome-not-mechanism hypothesis discipline → `/diagnose` Phase 3 (general-merit; applies to all bug classes, not just UI).
- **Captured, ready-to-ship on a 2nd-project signal:** the `## Visual / browser-rendering bugs` recipe → tracked in `template-maintenance/feedback.md` FB-085 with the full locked design.
- **No DEC** (the fold fails the hard-to-reverse criterion — a ~20-line recipe edit is trivially reversible). **No new command surface** (FB-072/DEC-018 discipline upheld).

Full locked decisions: see FB-085 § "Resolved design".

---

## Problem

UI tasks recur as the template's worst multi-pass offender. The insights report (2026-04-27 → 2026-05-24) names the pattern directly: the T697 scroll-anchor bug took **three passes**, gradient discontinuities at boundaries needed repeated tweaks, cursor-proximity gradients fought the same fight.

The root cause is captured as **FB-085** (deferred, signal-gated): on `runtime_validation: partial` + `owner: both` tasks, implement-agent claims a load-bearing browser behavior, verify-agent confirms it *by reading the diff* — and **both share the same documentation-derived model, so both can be wrong together.** T697's false premise ("native browser anchor scroll re-evaluates the target during smooth-scroll animation") survived both agents and was only caught by an orchestrator-driven Playwright re-test at user hand-off. The writer/reviewer separation — normally the template's quality backbone — collapses when the premise is empirical and neither agent measured it.

**The gap in one line:** empirical verification currently happens *after* the writer/reviewer cycle, so wrong premises propagate through both. There is no loop that makes measurement the arbiter *during* the fix.

## Core idea

A tight, single-agent loop where **the running browser, not a code read, decides whether the fix worked**:

1. **Contract** — the task carries (or the user states) a falsifiable visual/behavioral acceptance contract.
2. **Apply** — make the CSS/renderer/layout edit.
3. **Measure** — drive Playwright to capture the relevant evidence at the edge cases the contract names.
4. **Diagnose** — compare evidence against the contract; if it fails, form a *falsifiable* hypothesis about why (not "tweak and see").
5. **Re-apply** — fix per the hypothesis.
6. **Converge or surface** — repeat until the contract passes or an iteration cap is hit; on cap, surface before/after evidence + the unmet contract to the user. Never silently declare success.

The reframe that makes this worth a command: it replaces "both agents agree from docs" with "the browser is the source of truth," which is exactly the FB-085 failure mode.

## Why this is distinct from what already exists

The UX cost of a new top-level command is real (cf. FB-072 / DEC-018 — we declined a router; the cost-awareness stands). So the boundary has to be clean, or this should fold into an existing command instead.

| | `/audit-ui` (exists) | `/diagnose` (exists) | `/visual-verify` (proposed) |
|---|---|---|---|
| Shape | One-pass audit | 6-phase bug methodology | Tight fix-loop |
| Direction | Read-only / advisory | General, domain-neutral | Visual/render-specific |
| Breadth vs depth | Breadth (7 lenses, parallel) | Depth (any bug) | Depth (one visual contract) |
| Catches | Content/IA/affordance quality | "Something's wrong, why?" | Pixel/layout/render correctness |
| Loops? | No | Loosely (feedback loop phase) | Yes — convergence is the feature |
| Arbiter | Sub-agent judgment | Falsifiable hypothesis | Empirical measurement |

`/audit-ui` finds "this status pill has no action"; it would never catch "this gradient steps by 0.2 alpha at the MAX_DIST boundary." `/diagnose` *could* drive this, but its generality means the visual contract, the measurement recipe, and the MCP-session discipline aren't encoded — you'd re-derive them each time. **The open question (below) is whether `/visual-verify` is a standalone command or a `--visual` mode / documented recipe of `/diagnose`.**

## Hard constraints (grounded in existing rules — not up for grabs)

These come straight from shipped template rules and FB-085's own triage; grill the design *within* them.

- **Single browser session → single-agent sequential.** `agents.md § "MCP and Parallel Execution"`: one Playwright session can't fan out across parallel subagents. The loop is inherently sequential; it cannot be a parallel batch.
- **Runs at the orchestrator level, not in a dispatched subagent.** FB-085's triage flagged that "verify-agent's subagent sandbox limits direct Playwright access, so the empirical-verification step might need to route through the orchestrator instead." MCP access is not reliably inherited by `Task`-dispatched subagents. This likely forces the loop into the main session (orchestrator or a user-invoked command), *not* implement-agent or verify-agent.
- **Dev-server dependency + respect-prior-kills.** Like `/audit-ui`, needs a running dev server. Starting one for verification is an explicitly-sanctioned feature, but `agents.md § "Behavioral Rules"` forbids silently restarting a server the user killed.
- **Domain-agnostic template, UI-only feature.** The template serves software/research/procurement/renovation. This ships as an opt-in capability gated by `applies_when` (web-framework deps in `package.json`), mirroring how `/audit-ui` already gates.

## Open questions — the grill targets

Each has a provisional lean, but all are unresolved. These are what `/grill` should walk.

1. **Where does the acceptance contract come from?** Inline at invocation / derived from the task's `test_protocol` / a stored baseline screenshot / none (loop until "looks right")? — *Lean: explicit falsifiable contract, inline or from `test_protocol`. "Looks right" is the swap-and-see anti-pattern `agents.md` forbids. This is the single most important fork — a loop with no falsifiable contract is worse than no loop.*

2. **How does it measure — computed-style assertions, pixel diffs, or both?** — *Lean: `browser_evaluate` computed-style/geometry assertions (scroll position, bounding rects, `getComputedStyle` at named edge cases) over pixel diffs. Pixel diffs carry noise and need a golden baseline; assertions are falsifiable and self-documenting. But pixel diff may be the only option for "does this gradient look continuous" — grill where assertions run out.*

3. **Standalone command vs `/diagnose --visual` vs a recipe inside `diagnose.md`?** — *Lean: undecided, and this is a UX-cost decision. Folding into `/diagnose` honors the "don't add surface" instinct; a standalone command is more discoverable for the (frequent) UI case. Grill whether the visual specifics (contract, measurement, MCP discipline) earn their own surface.*

4. **Ephemeral loop or durable regression artifact?** Does it leave behind a reusable Playwright assertion / stored baseline so the defect can't regress (cf. `/diagnose` Phase 5 regression test, FB-064 test-harness awareness), or is it throwaway once the task passes? — *Lean: offer to persist an assertion when a project harness exists; ephemeral otherwise. Connects to FB-085 Option 2 (`partial_empirical` vs `partial_documented` verification field).*

5. **Iteration cap and the non-convergence exit.** What's N, and what happens at N? Surface evidence + unmet contract / hand to `/diagnose` / hard stop? — *Lean: N≈3 (matches the observed T697 reality), then surface before/after + the failing contract to the user. Never auto-declare success past the cap.*

6. **Where does it sit in `/work`?** A capability invoked *within* a single task's implementation, an orchestrator step after implement-agent returns on visual tasks, or purely a user-invoked command? — *Lean: user-invoked first (lowest risk, proves the loop), with a later option to auto-trigger on `runtime_validation: partial` + visual-surface tasks. Note the orchestrator-level constraint above bounds this.*

7. **Scope of "visual."** Static layout/CSS only, or also interaction states (hover, cursor-proximity), transitions/animation, responsive breakpoints? — *Lean: start with static layout + computed geometry; defer animation/timing (hardest to make falsifiable). Grill the boundary.*

8. **Does the "measure" step absorb the queued "math-check before commit-to-pixels" signal?** (Pre-compute the arithmetic trade-off of a layout change *before* spending a screenshot iteration — currently queued, single-project, niche.) — *Lean: yes, fold it in as a pre-apply check; it's cheap and the loop is its natural home.*

## What success looks like (acceptance for the feature itself)

- A UI fix that previously took 3 passes converges in the loop without a human catching the false premise mid-way.
- The loop never reports "done" on an unmet contract; non-convergence always surfaces evidence.
- Zero MCP-session contention (single-agent discipline holds).
- The command is either clearly distinct from `/audit-ui` + `/diagnose`, or consciously folded into one — no third overlapping surface added carelessly.

## Out of scope (initial)

- Parallel multi-route visual verification (MCP single-session constraint; out of scope until multi-instance browser setup is worth it).
- Cross-browser / device-farm matrices.
- Non-UI domains (the loop is browser-specific by construction).
- Auto-generating the acceptance contract from scratch — a human (or the task) states what "correct" means; the loop verifies it, it doesn't invent it.

## Related signals

- **FB-085** (deferred) — the motivating gap; this command is the mechanism that would close it. Building this likely retires or absorbs FB-085.
- **FB-076** (deferred) — verify-agent runtime_validation gaps; adjacent (empirical verification of runtime claims), different surface.
- **"Math-check before commit-to-pixels"** (queued signal-item) — candidate to fold into the measure step (Q8).
- **FB-072 / DEC-018** — the command-surface cost discipline that Q3 must satisfy.
