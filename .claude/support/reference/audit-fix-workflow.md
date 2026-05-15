# Audit Findings — Dashboard Surface and Action Protocol

Documents the user-facing surface for audit findings (the dashboard's `🔍 Audit Findings` section) and the action protocol for resolving them. Audits themselves are documented per-command in `.claude/commands/audit-*.md`; this doc covers what happens *after* an audit runs.

**Scope:** Stage 6a of the audit family proposal (`template-maintenance/audit-command-family-proposal.md`). Surfaces digest items on the dashboard with `[Promote to FB]` / `[Dismiss]` actions. The `[Fix it]` inline-apply mechanism (and bundled-apply UX) is **deferred to Stage 6 full** — sections below marked `(Stage 6 full)` are placeholders documenting what's coming, not what currently works.

---

## Where findings live

Each audit run writes to `.claude/support/audits/{audit}-{YYYY-MM-DD-HHmm}/`:

- `findings.md` — full clustered report (Claude-readable, all evidence)
- `digest.json` — machine-readable digest (audit family Component 2 schema)
- `lenses/` — per-lens raw output
- `inputs/` — captured project state (audit-coherence) or page snapshots (audit-ui)

`digest.json` is the surface-facing artifact. The dashboard's `🔍 Audit Findings` section is a projection of the most recent `digest.json` filtered for `status: pending` and not in the user's dismissal list.

---

## Dashboard surface

The `🔍 Audit Findings` sub-section in Action Required renders when the dashboard sidecar (`dashboard-state.json`) has any pending, non-dismissed audit items. The sub-section is **persistent across regens** until each item is promoted, dismissed, or resolved by a subsequent audit run.

**Rendered shape:**

```markdown
### 🔍 Audit Findings

*Last audit: coherence 2026-05-15 14:30Z (5 pending · 0 promoted · 0 dismissed since last audit)*

<!-- AUDIT DIGEST -->
- [ ] **C-02** "sub-tab" vs "section nav" vocab inconsistency (spec § 9.1, 11.1, 42.5) — [Promote to FB] / [Dismiss]
- [ ] **C-03** Oracle-thesis contradiction pattern recurring (3 friction register entries cluster) — [Promote] / [Dismiss]
- [ ] **C-05** 5 FB items >30 days open without status change — [Review FB] / [Dismiss]
- [ ] **C-07** Phase 27 § 27.1 feature retirement workflow referenced but not implemented — [Promote] / [Dismiss]
- [ ] **C-08** Retired feature pull-to-refresh missing spec retirement marker (Phase 41) — [Promote] / [Dismiss]
<!-- END AUDIT DIGEST -->

*Already covered by in-flight work:*
- C-04 → T725 (Pending) — "spec § 28 path migration cleanup"
- C-09 → T712 (In Progress) — "FB-071 Phase 27 retirement scaffolding"
```

**Section ordering:** between Spec Drift and Feedback in Action Required.

**Empty state:** when an audit has run but all items are resolved/dismissed:
```
*No pending audit findings. Last audit: 2026-05-15. Run /health-check to refresh.*
```

When no audit has ever run (sidecar `audit_digest.latest_audit` is empty), the section is skipped entirely.

---

## Action protocol — Stage 6a (currently shipped)

Two actions per item: `[Promote to FB]` and `[Dismiss]`. Both are user-driven — Claude doesn't take either action without explicit user instruction.

### `[Promote to FB]`

Lifts a single audit finding into a feedback entry. Same shape as `/audit-{name} promote {audit-ts}` but scoped to one finding.

**User invocation:** the user clicks/copies the action and runs (or asks Claude to run) `/audit-coherence promote {audit-ts} {C-ID}` or `/audit-ui promote {audit-ts} {F-ID}`.

**Mechanism (handled by the audit command's promote mode):**

1. Read finding body from `audits/{ts}/findings.md#{ID}`.
2. Compute next `FB-NNN` from `feedback.md` + `feedback/archive.md`.
3. Dedupe pass against existing FB entries (per the audit's promote-mode dedupe — `[S]kip / [U]persede / [M]erge / [N]ew anyway`).
4. Append FB entry to `feedback.md` with `**Source:** audit-{name}-{audit-ts} {C-ID}`.
5. Update `digest.json` in place: `items[i].status = "promoted"`, `resolved_by = {kind: "promote_fb", ref: "FB-NNN", at: now}`.
6. Update `friction.jsonl` in place for any friction register entries cited by the promoted finding: `status: resolved`, `resolved_by` set per the same shape (see `friction-register.md` § "Status update protocol").
7. Update `findings.md` in place: replace `- [x] C-NN — title` with `- [x] C-NN → FB-NNN promoted {date}`.

**Effect on dashboard:** next regen detects `digest.json` updated, re-runs Step 5f, the promoted item drops out (status != pending). Header line counters update (promoted count +1).

### `[Dismiss]`

Marks a finding as not-a-problem-to-fix. Doesn't promote, doesn't change source, just removes from view. Reason capture is optional but encouraged.

**User invocation:** the user asks Claude to dismiss a specific finding (e.g., *"dismiss C-05 — those FB items are stale because they're tracking long-term ideas"*).

**Mechanism (orchestrator-handled, no audit-command sub-mode needed):**

1. Add `id` to `dashboard-state.json` `audit_digest.dismissed_ids[]`.
2. Update `digest.json` in place: `items[i].status = "dismissed"`, `dismiss_reason = "{user reason or 'user dismissed via dashboard'}"`, `dismissed_at = ISO timestamp`.
3. If the finding cites friction register entries: optionally mark those `status: dismissed` (with same reason) — ask user, since dismissing a finding doesn't always mean dismissing the underlying friction. Default: leave friction entries `open` so a future audit can re-cluster them.
4. Regenerate dashboard. The dismissed item filters out (id in `dismissed_ids` + `status: dismissed`).

**Permanence:** `dismissed_ids` persists across regens via the sidecar. To un-dismiss, the user manually removes the id from `dashboard-state.json` `audit_digest.dismissed_ids` and runs a regen.

### Other actions (no special handling for Stage 6a)

- **`[Review FB]`** (appears on `feedback-decay` lens findings): a label-only — the user reads the cited FB entries via `/feedback review`. Resolution comes through normal feedback triage; the audit finding remains pending until next audit run re-evaluates (decayed FB entries that got triaged drop off naturally).

---

## Action protocol — Stage 6 (full) — *deferred*

The following sections document what Stage 6 (full) will add. **Not currently shipped.**

### `[Fix it]` *(Stage 6 full — not yet implemented)*

Per-finding inline-apply mechanism. Available actions per kind will be:

| Finding kind | `[Fix it]` (Stage 6 full) | `[Promote to FB]` | `[Dismiss]` |
|--------------|:---:|:---:|:---:|
| `bundle-eligible` (impl-only, source-confirmed) | ✓ inline apply (single-finding mode) | ✓ | ✓ |
| `fix-eligible` (impl-only, clear fix, single source) | ✓ inline apply (may escalate) | ✓ | ✓ |
| `decision` (touches spec / decision record / vision) | ✓ auto-routes to `/iterate` (no inline apply — ever) | ✓ | ✓ |
| `design` (needs research / discussion) | — | ✓ | ✓ |

**Hard rule (Component 6 of audit family proposal):** the spec, decision records, and vision documents are read-only outside `/iterate`. Any finding whose `files_to_touch` includes a spec/decision/vision file path is auto-classified `kind: decision` by the synthesizer, and `[Fix it]` on those will route to `/iterate` rather than apply inline. Two enforcement points: synthesizer step 5 (HARD RULE FIRST) and post-synth sanity check.

**Mechanism (Stage 6 full):**

1. User invokes inline (any session): *"address C-02 from latest coherence audit"*.
2. Claude resolves latest audit dir, reads `findings.md#{C-02}`.
3. **Re-reads `source_anchors`** at apply time — synthesizer's classification is not trusted.
4. Routes by kind:
   - `bundle-eligible` / `fix-eligible`: applies inline, asks for approval, single commit `audit-fix: C-02 — {summary}`, marks `status: resolved` in digest.json + friction.jsonl.
   - `decision`: stops, says *"requires spec amendment via /iterate"*, marks `status: escalated_to_iterate`.
   - `fix-eligible` mid-fix scope-growth: stops, suggests `/work` task creation, marks `status: escalated_to_work`.

**State isolation property:** the audit dir + `digest.json` are independent of `.handoff.json` + `tasks/`. Two parallel sessions (one running `/work`, another addressing audit findings) don't fight over the same state.

### Bundled apply *(Stage 7 — not yet implemented)*

Batch-mode UX over the `[Fix it]` mechanism. Same at-apply re-read invariant; one bulk approval prompt instead of N per-finding interactions; combined into a single commit. Eligibility criteria (Component 6 of proposal): implementation-file-only, source-confirmed at apply time, reversible, no new judgment, ≤3 files per finding + ≤10 total in the bundle.

---

## Sidecar persistence

The `audit_digest` field in `dashboard-state.json` is the durable store for dashboard-side audit state:

```json
"audit_digest": {
  "latest_audit": "coherence-2026-05-15-1430",
  "items": [ /* projection of latest digest.json items[] */ ],
  "dismissed_ids": ["C-04", "C-09"]
}
```

**Update lifecycle:**

- **On dashboard regen (Step 5f):** scan `.claude/support/audits/*/digest.json` for newest by `ran_at`. If newer than `latest_audit`, replace `items` with new digest's items (preserve `dismissed_ids`).
- **On user dismissal:** append id to `dismissed_ids`, also update `digest.json` `status: dismissed`.
- **On promote:** the audit's promote mode updates `digest.json` `status: promoted`. Sidecar items[] picks up the change at next regen.
- **On `[Fix it]` apply** *(Stage 6 full)*: the apply mechanism updates `digest.json` `status: resolved`. Sidecar items[] picks up at next regen.

**Cross-audit coexistence:** if both `/audit-coherence` and `/audit-ui` ran in a session, sidecar's `latest_audit` reflects whichever ran most recently. The dashboard digest section shows that audit's findings only — to switch view, run the other audit again. (Future: support multiple latest audits per audit-name; defer until observed need.)

---

## Open considerations

- **Re-running an audit while previous findings are pending.** Current behavior: new run replaces old `items` in sidecar; pending-but-not-yet-dismissed items from prior run are lost. If the new audit re-detects them, they reappear with new C-IDs. Acceptable for Stage 6a; Stage 3 open question 3 ("dedupe against prior digest, badge as unchanged/new") would refine this.
- **Audit findings cited by multiple lenses across multiple audit families.** Currently each audit-name has its own `audits/{name}-{ts}/`. If `/audit-coherence` and `/audit-ui` both flag the same UI surface vs spec issue, the dashboard shows them as two separate items. Cross-audit dedupe is future scope.
- **Dismissal scope.** Dismissing a finding doesn't auto-dismiss related friction register entries. Reasonable default (a dismissed dashboard finding doesn't mean the underlying friction is wrong; just that the user judged it not worth surfacing right now). The auto-cluster will re-surface it in a future audit if it persists; user can dismiss again or escalate.
