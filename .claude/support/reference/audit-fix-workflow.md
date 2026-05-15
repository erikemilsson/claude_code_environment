# Audit Findings — Dashboard Surface and Action Protocol

Documents the user-facing surface for audit findings (the dashboard's `🔍 Audit Findings` section) and the action protocol for resolving them. Audits themselves are documented per-command in `.claude/commands/audit-*.md`; this doc covers what happens *after* an audit runs.

**Scope:** Stage 6a + Stage 6 Option C (per DEC-013) of the audit family proposal (`template-maintenance/audit-command-family-proposal.md`). Stage 6a surfaces digest items on the dashboard with `[Promote to FB]` / `[Dismiss]` actions for all kinds. Stage 6 Option C adds a `[Fix it]` inline-apply action for `bundle-eligible` kind only — per DEC-013's autonomy-boundary review (2026-05-15). `fix-eligible` kind defers to a future DEC pending telemetry validation. Stage 7 (bundled-apply batch UX) remains deferred — the `(Stage 7)` section below is a placeholder.

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

## Action protocol — Stage 6 (Option C per DEC-013) — *currently shipped*

Adds `[Fix it]` to the dashboard digest, scoped to `bundle-eligible` kind only. Per DEC-013 (approved 2026-05-15), `fix-eligible` defers to a future DEC pending telemetry validation; `decision` and `design` kinds are unchanged from Stage 6a.

### `[Fix it]` — inline apply (bundle-eligible only)

Lifts a single bundle-eligible audit finding into an inline applied change with one user approval.

**User invocation patterns (any session):**

- **Slash command:** `/audit-coherence fix {audit-ts} {C-ID}` or `/audit-ui fix {audit-ts} {F-ID}` — analogous to existing `promote` sub-mode
- **Natural language:** *"fix C-02 from the latest coherence audit"* or *"address F-04 from the ui audit"* — Claude infers the slash command
- **Dashboard click:** the `[Fix it]` link in the `🔍 Audit Findings` section expands to the slash command form

**Mechanism (orchestrator-side):**

1. **Resolve audit dir.** From the audit name + timestamp (or "latest" → newest by `ran_at`): `.claude/support/audits/{audit-name}-{ts}/`.
2. **Read finding.** Read `digest.json`, find item by id. Read `findings.md#{C-ID}` for the full evidence + cited `source_anchors`.
3. **Kind gate.** If `kind != "bundle-eligible"`, refuse with a kind-specific message:
   - `fix-eligible` → *"C-XX is fix-eligible, not bundle-eligible. Inline apply for fix-eligible kind is deferred per DEC-013 — review the finding manually or run `/audit-{name} promote {ts} {C-ID}` to route to feedback."*
   - `decision` → *"C-XX touches spec/decision/vision (read-only outside `/iterate`). Use `/audit-{name} promote {ts} {C-ID}` to route to feedback for `/iterate` triage."*
   - `design` → *"C-XX requires design judgment. Promote to feedback (`/audit-{name} promote {ts} {C-ID}`) for `/research` consideration."*
4. **Status gate.** If finding `status != "pending"`, refuse — the item has already been resolved / dismissed / promoted. Surface what status it has.
5. **At-apply re-read (load-bearing safety property).** For each path in `source_anchors[]`, re-read the cited file/section and confirm the finding's claim still holds. If the cited source has changed in a way that invalidates the finding (e.g., a referenced decision was edited, a cited file was moved or removed, a magic value the finding depends on was changed), refuse with: *"Finding C-XX is stale — its source_anchor `{anchor}` no longer asserts `{claim}`. Re-run the audit to refresh."*
6. **Hard-exclusion re-verify (defense-in-depth).** Confirm `files_to_touch[]` contains NO paths matching `.claude/spec_v*.md`, `.claude/support/decisions/decision-*.md`, or `.claude/vision/**/*.md`. If any path matches: this is a synthesizer mis-classification (kind should have been `decision`); refuse and ask the user to file a friction marker. (Should never happen if synthesizer step 5 + post-synth sanity check worked; this is defense-in-depth.)
7. **Compute the concrete change.** Based on the finding's `fix_one_liner` + evidence + `files_to_touch[]`, formulate the actual edit. For bundle-eligible findings this is typically a single-line change (remove a dep from package.json, delete an orphan file, sync a numerical anchor).
8. **Show + approve.** Display the concrete change to the user (file paths + 1-3 lines of context per file showing what changes) and ask single approval: `Apply this change? [Y/N]`.
9. **On approval (Y):**
   - Apply the change using Edit / Write tools.
   - Single git commit: `audit-fix: {C-ID} — {one-line summary from fix_one_liner}` with body listing the changed files + the C-ID + audit run reference.
   - Update `digest.json` in place: `items[i].status: "resolved"`, `resolved_by: {kind: "fix_it", ref: "<commit-sha>", at: "<ISO timestamp>"}`.
   - For each friction register entry cited in the finding: update `friction.jsonl` in place per `friction-register.md` § "Status update protocol" — `status: resolved`, `resolved_by: {kind: "fix_it", ref: "<commit-sha>", at: "<ISO>"}`.
   - Update `findings.md` in place: replace `- [ ] {C-ID} — title` with `- [x] {C-ID} → fixed in <short-sha> ({date})`.
   - Print summary: `Applied {C-ID} in commit {sha}. Run your test suite if this touched package.json or source code.`
10. **On refusal (N or any non-Y):** don't apply. Don't change `status` (stays `pending`). Print: `{C-ID} not applied. Run /audit-{name} promote {ts} {C-ID} to route to feedback instead, or invoke [Fix it] again later.`

### Per-kind action availability

| Finding kind | `[Fix it]` | `[Promote to FB]` | `[Dismiss]` |
|--------------|:---:|:---:|:---:|
| `bundle-eligible` (impl-only, source-confirmed, ≤3 files, reversible) | ✓ inline apply | ✓ | ✓ |
| `fix-eligible` (impl-only but >3 files or ambiguous) | — *(deferred per DEC-013; manual review)* | ✓ | ✓ |
| `decision` (touches spec/decision/vision) | — *(routes via /iterate; never inline)* | ✓ | ✓ |
| `design` (needs research/discussion) | — *(promote to FB → /research)* | ✓ | ✓ |

For non-bundle-eligible kinds, the dashboard digest renders a one-line italicized annotation explaining why `[Fix it]` doesn't appear (see `dashboard-regeneration.md` § "Audit Findings sub-section in Action Required").

### Known limitations (per DEC-013 research)

- **Transitive-consumer risk for orphan-dep removal (DEC-013 Q3).** Bundle-eligibility criteria can't catch dynamic-require / `importlib.import_module` / string-keyed import patterns that static analysis misses. **After any [Fix it] touching `package.json`, run your test suite** to catch transitive consumers the audit didn't model. If a test fails after a [Fix it] apply, `git revert HEAD` undoes the change cleanly. Same applies to source-code deletions of seemingly-orphan files.
- **Parallel-session collision (DEC-013 Q5).** [Fix it] does not coordinate with concurrent `/work` sessions. The at-apply re-read window doesn't lock against an implement-agent's edits to the same file. If you suspect overlap (e.g., `/work` running in another session targeting the same area), run [Fix it] serially after `/work` completes.
- **Synthesizer classification trust (DEC-013 Q1).** If the audit synthesizer mis-classifies a finding as bundle-eligible when the fix actually requires judgment (e.g., a test count anchor pinned for an intentional design reason; a "dead" link whose target was about to be created), the at-apply re-read invariant won't catch this — it only checks that the cited source still says what it claimed, not whether the inferred fix is correct. **Quick visual review at the show+approve step is the user's protection** — read the proposed diff before pressing Y. If it looks unexpected, refuse and use `[Promote to FB]` for human triage.
- **Single-commit-per-finding rollback (DEC-013 Q4).** `git revert {sha}` works cleanly for an isolated finding. If the user notices days later, subsequent commits may have built on the audit-fix commit and the revert may merge-conflict — standard git problem, no template-side mitigation.

### State isolation property

The `audits/` directory + `digest.json` + `friction.jsonl` are independent of `.handoff.json` + `tasks/`. Two parallel sessions (one running `/work`, another addressing audit findings) don't fight over the same *audit metadata*. File-content collisions are a separate concern — see "Parallel-session collision" under Known Limitations above.

---

## Bundled apply *(Stage 7 — deferred)*

Batch-mode UX over the `[Fix it]` mechanism — apply N bundle-eligible findings in one bulk approval and one combined commit.

**Status:** deferred. DEC-013 Q4's rollback analysis showed Stage 7's all-or-nothing revert (`git revert HEAD` reverts ALL N findings, including the (N-1) that were correct) is materially worse than Stage 6 Option C's single-commit-per-finding rollback. Reconsider once Stage 6 Option C has accumulated usage signal.

When/if shipped: same at-apply re-read invariant per finding (called N times); same hard-exclusion enforcement; same eligibility filter (only bundle-eligible findings ride the batch path). Eligibility criteria documented in `audit-command-family-proposal.md` Component 6.

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
