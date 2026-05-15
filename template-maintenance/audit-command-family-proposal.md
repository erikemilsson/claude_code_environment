# Audit Command Family + Coherence Audit + Friction Register Proposal

**Purpose:** Add a structured loose-end-detection capability to the template. `/health-check` extends to dispatch project-aware audits; first audit shipped is `coherence` (spec/decision/path drift). Existing Styler-only `/audit-ui` generalizes into the same shape. Output is a small bundled plain-English digest that lands on the dashboard for async user attention, with a tightly-scoped bundled-apply tier for spec-confirmable cleanups.

**Status:** Draft proposal, no code written. Frames a future decision record (DEC-012?) and a multi-stage implementation. Last updated: 2026-05-15.

**Origin:** Conversation with template maintainer 2026-05-15 — observation that the dashboard isn't load-bearing for navigation but the "Notable (non-approved) decisions" surface hinted at higher-value use: surfacing async cleanup work that Claude can't do alone. Inventory of Styler confirmed real signal exists across superseded decisions, vocab drift, path drift, friction markers buried in dashboard prose, and decayed feedback items. Audit-ui command pattern (capture → parallel lenses → synthesize → digest + promote) identified as the right precedent.

---

## Constraints (load-bearing)

- **No new top-level commands.** `/health-check` is the only user surface. Maintainer is at the edge of how many commands they want.
- **Audits are commands** (`.claude/commands/audit-*.md`) — single markdown file per audit, mirroring Styler's existing `/audit-ui` shape. Template-shipped audits ship with the template; project-local audits live in the project's `.claude/commands/` and are auto-discovered by `/health-check` Part 8 (Component 1). See Component 9 for the project→template graduation pattern.
- **Specification is read-only outside `/iterate`.** The spec (`.claude/spec_v*.md`), decision records (`.claude/support/decisions/decision-*.md`), and vision documents (`.claude/vision/**/*.md`) are **never** modified by [Fix it] or bundled-apply. The only path that mutates these files is `/iterate`. Audits read these files to detect drift; only `/iterate` writes them. Enforced structurally at the file-path level (Component 6 hard exclusion + Component 8 action table). The user's load-bearing instinct ("only reading it, no writing at all, unless we go through the iterate command") is the rule.
- **Implementation-file edits via [Fix it] / bundled-apply are gated on at-apply-time source re-read**, not Claude's first-pass confidence. Audit synthesizer's classification is not trusted; orchestrator re-verifies before any write.
- **Dashboard digest persists across regens** until each item is promoted, dismissed, or resolved by a subsequent audit run.
- **Subagent constraint preserved.** Sub-agents (e.g., lens agents dispatched from audit commands) cannot write to `.claude/`; orchestrator (`/health-check`) writes all artifacts and applies bundled fixes after user approval.

---

## What it looks like to use

```
$ /health-check

Part 1-5: [existing structural checks run as today]
  ✓ Task system: clean
  ⚠ Decisions: 2 stale drafts (>30d old)
  ✓ Archive: clean
  ✓ Template sync: in sync

Part 8: Audit dispatch

  Audits available for this project:
    [1] coherence  — spec/decision/path drift detection (~2 min)
    [2] ui         — web app surface walk + 7 quality lenses (~5 min, requires dev server)
    [A] all applicable
    [S] skip

  > 1

  Running coherence audit...
  ├─ capture: 79 decisions · spec_v13 (4859 lines) · 524 tasks · 0 friction-register entries
  ├─ lenses (parallel): superseded-decisions · vocab-drift · path-drift · feedback-decay · retired-features · friction-register
  └─ synthesize: 23 raw findings → 8 clustered → 3 bundle-eligible / 5 promote-eligible

  🔍 Coherence audit complete

  Bundle-eligible cleanups (implementation-only, source-confirmed, reversible):
    C-04  Remove orphan dep react-native-pager-view from styler-phone/package.json (per T647)
    C-10  Sync test count anchor in style-nav-inventory.test.ts (current 14, actual 15 after T654)
    C-11  Delete OutfitAlternativeCard.tsx (audit 2026-05-14 — no callers post-DEC-066)

  Apply now? [Y]es / [N]o / [I]ndividual review / [P]romote all to feedback instead

  > Y
  Re-reading source for verification... ✓
  Applied 3 cleanups in 1 commit.
  Diff: .claude/support/audits/coherence-2026-05-15-1430/applied.diff
  Rollback: git revert HEAD

  Promote-eligible findings (judgment required; spec changes route through /iterate) — surfaced on dashboard:
    C-01  Spec § 5.2 still describes per-user generation; DEC-050 selected maintainer-curated (spec amendment)
    C-02  "sub-tab" vs "section nav" vocab inconsistency across spec § 9.1, 11.1, 42.5 (spec amendment)
    C-03  Oracle-thesis contradiction pattern recurring (3 friction register entries cluster)
    C-05  5 FB items >30 days open without status change
    C-06  Spec § 22.2 path foundation/coloring/ → foundation/user/coloring/ per § 28.1 (spec amendment)
    C-07  Phase 27 § 27.1 feature retirement workflow referenced but not implemented
    C-08  Retired feature pull-to-refresh missing spec retirement marker (Phase 41 — spec amendment)

  Skipped — already covered by in-flight work:
    C-04 → T725 (Pending)    "spec § 28 path migration" overlaps task files_affected
    C-09 → T712 (In Progress) "FB-071 Phase 27 retirement scaffolding" overlaps annotations

  Dashboard updated. Findings persist until you fix, promote, dismiss, or re-audit.
  Address any finding from any session: "address C-02 from the latest coherence audit".
```

The dashboard's `🔍 Audit Findings` section then shows those 5 items with `[Promote to FB] / [Dismiss]` controls per item, persistent across regens.

---

## Architecture

```
/health-check
├── Parts 1-5: existing structural checks (unchanged)
└── Part 8: Audit Dispatch (NEW)
    ├── detect applicable audits via command frontmatter (`applies_when`)
    ├── present menu
    ├── dispatch selected audits (sequentially — each is internally parallel via lens sub-agents)
    ├── receive digest.json from each
    ├── present bundled-apply prompt for any bundle-eligible findings
    ├── apply approved bundles (after spec re-read)
    └── update dashboard digest section

.claude/commands/                    ← audits are commands (single .md per audit)
├── health-check.md                  # existing, now with Part 8 dispatch
├── audit-coherence.md               # NEW — frontmatter + capture procedure + 6 lens prompts + synthesizer prompt + digest schema, all in one file
├── audit-ui.md                      # migrated from Styler (was Styler-local; now template-shipped)
└── (future audit-* commands; project-local audits in project's .claude/commands/audit-*.md also auto-detected by Part 8)

.claude/support/
├── friction.jsonl                   # NEW: persistent register, append-only
├── audits/                          # NEW: per-run reports
│   └── coherence-{YYYY-MM-DD-HHmm}/
│       ├── findings.md              # full Claude-readable report
│       ├── digest.json              # 4-5 user-facing items
│       ├── applied.diff             # if bundled-apply happened
│       └── lenses/                  # per-lens raw output
└── decisions/, feedback/, ...       # existing

.claude/dashboard.md
└── Action Required → 🔍 Audit Findings (NEW persistent section, marker-bracketed)
```

---

## Components

### 1. `/health-check` Part 8: Audit Dispatch

After existing Parts 1-5 complete, the new Part 8:

1. **Detect applicable audits.** Scan `.claude/commands/audit-*.md` for `applies_when` frontmatter declarations. Each audit command self-declares its trigger conditions (e.g., `audit-coherence` applies when any `.claude/spec_v*.md` exists; `audit-ui` applies when project `package.json` declares Next.js / React / Vue / Svelte / Vite as a dep). Both template-shipped audits and project-local audits live at the same path (`.claude/commands/audit-*.md`) and are surfaced together — covers the "I built a project-specific audit and want it surfaced through `/health-check`" case (see Component 9, graduation path).
2. **Present menu** with rough time estimates, prerequisites, and source (template-shipped vs project-local).
3. **Dispatch selected audits.** Orchestrator invokes each in sequence (audits are internally parallel via lens agents; sequencing across audits avoids MCP collisions and keeps output legible).
4. **Aggregate digests** into the dashboard's `🔍 Audit Findings` section.
5. **Bundled-apply prompt** if any digest contains bundle-eligible findings. Re-read `source_anchors` before each apply.

**Subagent constraint:** lens agents cannot write to `.claude/`. They return text; the synthesizer step (also a subagent) returns `findings.md` + `digest.json` text; `/health-check` (orchestrator) writes both to disk.

**Form factor:** Audits are commands (`.claude/commands/audit-*.md`), single markdown file each. Each command file contains its frontmatter (`applies_when`, `estimated_runtime`, `prerequisites`), capture procedure, lens prompts (sections, dispatched as parallel sub-agents), synthesizer prompt, and digest schema in one place. Mirrors Styler's existing `/audit-ui` shape exactly. (Skill-based form was considered and rejected — see Open Question 2 resolution. Single-file commands also have the practical advantage that project-local audits can be created in the same shape and graduate to template-shipped without restructuring.)

### 2. Audit command interface

Every audit command exposes:

```yaml
# .claude/commands/audit-{name}.md frontmatter
applies_when:
  any_file_exists: [".claude/spec_v*.md"]            # coherence example
  # OR
  package_json_has_dep: ["next", "react", "vue", "svelte", "vite"]  # ui example
estimated_runtime: "2 min"
prerequisites: []                                     # ui: ["dev server reachable at {url}"]
```

**Single-file structure.** The command file body contains all the audit machinery in one place: capture procedure (orchestrator-side, walks the project), lens prompts (one per section, each dispatched as a parallel sub-agent during Phase 2), synthesizer prompt (one section, dispatched as a single sub-agent during Phase 3), digest schema (one section, defines the output contract). This mirrors `audit-ui.md`'s existing 720-line structure. New audits clone the skeleton (Component 9) and fill in the lens prompts.

Every audit produces:
- `findings.md` — full clustered report (Claude-readable, all evidence, all original lens findings)
- `digest.json` — 4-5 bundled items in user-facing language with eligibility flags
- Optional `applied.diff` — if bundled-apply ran

**`digest.json` schema:**

```json
{
  "audit": "coherence",
  "ran_at": "2026-05-15T14:30:00Z",
  "findings_count": {
    "raw": 23,
    "clustered": 8,
    "bundle_eligible": 3,
    "promote_eligible": 5,
    "deduped_to_pending_work": 2
  },
  "items": [
    {
      "id": "C-04",
      "title": "Orphan dep react-native-pager-view in styler-phone/package.json (per T647)",
      "kind": "bundle-eligible",
      "fix_one_liner": "Remove react-native-pager-view from package.json dependencies",
      "source_anchors": ["task-647.json#verification_history", "package.json"],
      "files_to_touch": ["styler-phone/package.json"],
      "evidence_path": ".claude/support/audits/coherence-2026-05-15-1430/findings.md#C-04",
      "bundle_eligibility": {
        "source_confirmed": true,
        "reversible": true,
        "files_count": 1,
        "touches_spec_or_decisions": false,
        "kind_classification": "orphan_dep_removal"
      },
      "status": "pending"
    },
    {
      "id": "C-01",
      "title": "Spec § 5.2 still describes per-user generation; DEC-050 selected maintainer-curated",
      "kind": "decision",
      "fix_one_liner": "Spec amendment via /iterate (3 occurrences in § 5.2)",
      "source_anchors": ["spec_v13.md § 5.2.1", "decision-050-*.md"],
      "files_to_touch": [".claude/spec_v13.md"],
      "evidence_path": ".claude/support/audits/coherence-2026-05-15-1430/findings.md#C-01",
      "iterate_routing": { "reason": "spec file modification — read-only outside /iterate" },
      "status": "pending"
    }
  ],
  "annotations": [
    {
      "type": "covered_by_pending_task",
      "what": "Spec § 28 path migration cleanup",
      "covered_by": "T725",
      "covered_by_status": "Pending",
      "source_anchors": ["spec_v13.md § 28.1"],
      "suppressed_finding_id": "C-09"
    }
  ]
}
```

**Naming note:** `source_anchors` (was `spec_anchors` in earlier drafts) — generalized because not all anchors are spec sections. Could be a decision ID, a task JSON field, an on-disk file. Spec-anchor findings are a strict subset that always route to `/iterate`.

`status` per item: `pending` | `resolved` | `dismissed` | `escalated_to_iterate` | `escalated_to_work`. Updated atomically by [Fix it] / bundled-apply / dismiss actions (Component 8).

### 3. `audit-coherence` command (concrete first audit)

**Capture (orchestrator-side, no parallelism):**
- All decision frontmatter (status, superseded_by, related)
- Spec content + section fingerprints
- Friction register entries (status: open)
- Sample of recent task JSONs (verification_history.issues, notes — sample, don't enumerate 500+)
- Feedback.md status fields
- `drift-deferrals.json` if exists
- `.claude/support/retired/*/manifest.json`

**Lenses (parallel sub-agents, fresh context each):**

| Lens | Catches | Detection mode |
|------|---------|---------------|
| `superseded-decisions` | Decisions marked superseded whose old language still appears in spec | Auto: grep spec for superseded decision IDs and decision-text remnants |
| `vocab-drift` | Terms used inconsistently between spec sections, or between spec and friction register | Auto: cross-section term frequency + register read |
| `path-drift` | File paths in spec that don't exist on disk | Auto: glob filesystem + spec scan |
| `feedback-decay` | FB-* entries open >30d with no status change | Auto: parse feedback.md status fields |
| `retired-features` | Manifests in `.claude/support/retired/` without spec retirement marker | Auto: filesystem + spec scan |
| `friction-register` | Cluster open register entries by theme, surface high-frequency patterns | Read register + thematic grouping (Claude judgment) |

**Synthesizer:** Reuses audit-ui's algorithm — pre-cluster within lens, cross-lens cluster, severity/effort/impact scoring, surface bucket grouping. Adds a `kind` classification per finding: `bundle-eligible` / `fix-eligible` / `decision` / `design`. Targets ≤8 user-facing items in digest (cluster aggressively).

**Pending-work dedupe (synthesizer post-cluster step):** Before emitting the digest, scan tasks in `{Pending, In Progress, Awaiting Verification}` for `files_affected` overlap with each candidate finding's `files_to_touch`, OR title/description match against the finding's `source_anchors`. On match: suppress the finding from `items` and emit it under `annotations` instead — *"C-04 covered by T725 (Pending). See task."* Friction register entries with `captured_in.task` set auto-dedupe (they already have an owner; emit as annotation citing both the FR-id and the task). This avoids surfacing duplicate work and respects in-flight ownership. Same pattern as audit-ui's promote-mode dedupe against existing FB-* entries, applied at synthesis time against task state. The user still sees the issue exists (under annotations), but routed to the existing work stream rather than spawning a parallel one.

### 4. `audit-ui` command (migrated from Styler)

The existing `/audit-ui` command at `styler/.claude/commands/audit-ui.md` migrates to `.claude/commands/audit-ui.md` in the **template** with the same shape (walk → lenses → synthesize → promote). Generalization needed:

- **Lens prompts** use generic UI vocabulary, not Styler-specific surface names ("Get Dressed" / "Wardrobe" become example surfaces, not hardcoded buckets).
- **Surface bucket grouping** in synthesizer becomes URL-prefix-based (configurable via project config).
- **Project config:** the command reads `.claude/audit-ui.config.json` if present (maps URL prefixes to named buckets); otherwise defaults to URL-prefix grouping.
- **Promote target:** existing `/feedback` flow, unchanged.
- **Bundled-apply:** UI audit findings rarely qualify for bundled-apply (most are design judgments). The command emits `kind: bundle-eligible` only for clear orphan cases (e.g., dead-end CTA pointing at a 404 route the spec also no longer references) — and only if the fix touches no spec/decision/vision files (Component 6 hard exclusion).

Migration of audit-ui is independent of audit-coherence — they can ship in any order.

### 5. Friction register

`.claude/support/friction.jsonl` — append-only JSONL, one entry per line:

```jsonl
{"id":"FR-001","captured":"2026-05-15T11:35Z","captured_in":{"agent":"verify-agent","task":"task-654"},"kind":"vocab_drift","what":"spec § 42.5 says 'sub-tab' but /style uses synthetic section nav","spec_anchor":"spec_v13.md § 42.5","status":"open"}
{"id":"FR-002","captured":"2026-05-15T11:35Z","captured_in":{"agent":"verify-agent","task":"task-654"},"kind":"path_drift","what":"spec § 42.2/42.5 reference foundation/coloring/celebrity-references.json; on-disk is foundation/user/coloring/...","spec_anchor":"spec_v13.md § 42.2","status":"open"}
```

**Field reference:**
- `id` — monotonic `FR-NNN`
- `captured` — ISO timestamp
- `captured_in` — who flagged it (agent type + context object)
- `kind` — `vocab_drift` | `path_drift` | `design_contradiction` | `spec_implementation_gap` | `terminology_mismatch` | `other`
- `what` — one-sentence description
- `spec_anchor` — file + section reference
- `status` — `open` | `resolved` | `dismissed`

**Written by:**
- `implement-agent` when it notices friction during implementation (new return-report field)
- `verify-agent` when it spots discrepancies (new return-report field)
- `/iterate` when it surfaces drift during spec review
- `/work` orchestrator when receiving a friction-flag from any subagent return report

The actual `friction.jsonl` write is done by the orchestrator (subagents return the entry; orchestrator appends). This keeps the harness write-constraint clean.

**Read by:** `audit-coherence` lens-friction-register

**Resolved by:**
- bundled-apply (status → `resolved` + audit run reference)
- promotion to FB (status → `resolved` + FB-NNN reference)
- explicit dismissal during audit review (status → `dismissed` + reason)

**Not a replacement for `feedback.md`.** Feedback is feature-level signal ("this UX could be better, here's an idea"). Friction register is spec-level signal ("the spec and reality diverged here at the moment of implementation"). Distinct concerns; both feed the audit synthesizer.

### 6. Bundled apply

**Bundled apply is the batch-mode UX over the [Fix it] mechanism (Component 8)** — same at-apply source re-read invariant, same per-finding `digest.json` status update, same audit-trail commit shape. The only difference is one bulk approval instead of N per-finding interactions, and findings are combined into a single commit. The eligibility criteria below define which findings can ride the batch path; everything else uses per-finding [Fix it] (which can still apply many of the same changes — just one at a time, with explicit approval each).

#### Hard exclusion — specification is read-only outside `/iterate`

The spec, decision records, and vision documents are **never** modified by [Fix it] or bundled-apply. The only path that mutates these files is `/iterate`. Any finding whose `files_to_touch` includes any of:

- `.claude/spec_v*.md`
- `.claude/support/decisions/decision-*.md`
- `.claude/vision/**/*.md`

is automatically classified `kind: decision` regardless of how clear the proposed fix looks. [Fix it] on these findings auto-routes to `/iterate` (Component 8 mechanism); bundled-apply skips them entirely. There is no command-line flag, no force option, no "trust me" override.

This is a structural enforcement of the user's load-bearing instinct that the specification must remain clean and never be silently rewritten — enforced at the file-path level, not just by criteria. The audit *reads* the spec to detect drift; only `/iterate` *writes* the spec to resolve it.

#### Eligibility criteria (for everything not hard-excluded)

A finding qualifies for bundled-apply only if **all** of:

1. **Implementation-file-only.** `files_to_touch` contains zero spec / decision / vision file paths (per the hard exclusion above). Typical eligible files: `package.json`, source code (`.ts`, `.tsx`, `.py`, etc.), test files, config files, dashboard sidecar, friction register, retired-feature manifests.
2. **Source-confirmed at apply time.** Before applying, the orchestrator re-reads the cited `source_anchors` (decision metadata, task JSON, or on-disk file) and confirms the proposed fix is a sync from one authoritative source to a derived/dependent one. Synthesizer's first-pass classification is not trusted — orchestrator re-verifies.
3. **Reversible.** Text replacements, dep removals from package.json, deletion of clearly-orphaned files (manifest exists or no callers verifiable via grep). NOT structural refactors.
4. **No new judgment.** The fix's content is already present somewhere authoritative. The audit isn't picking among options; it's syncing one source to match another.
5. **Bounded scope.** ≤3 files touched per finding, ≤10 total files in the bundle.

**Also always promote to FB (in addition to the hard exclusion):**
- Anything labeled `design` kind (research/discussion required)
- Anything affecting acceptance criteria or task definitions (operational state Claude shouldn't silently rewrite)
- Cross-file refactors >3 files
- Anything where the surfacing friction register entry has `kind: design_contradiction`

**Approval flow:**

```
🔍 Coherence audit found 3 bundle-eligible cleanups (spec-confirmed, reversible):

  C-01  Spec § 5.2 — replace 3x "personalized generation" → "maintainer-curated" (per DEC-050)
  C-04  styler-phone/package.json — remove orphan dep react-native-pager-view (per T647)
  C-06  Spec § 22.2 — update path foundation/coloring/ → foundation/user/coloring/ (per § 28.1, 2 occurrences)

Full diff: .claude/support/audits/coherence-2026-05-15-1430/auto-apply.diff

[Y] Apply all 3
[I] Individual review (Y/N each)
[N] Skip — promote all to feedback instead
[D] Dismiss this run (don't promote, don't apply)
```

**Post-apply behavior:**
- Single git commit with standardized message: `audit: bundled apply {audit-ts} ({N} cleanups)\n\n{list of C-IDs}`
- Successful applications update `findings.md` and `digest.json` to mark applied items
- Friction register entries that the applied items resolved get status → `resolved` with audit reference
- Bumps related fingerprints in affected task JSONs (orchestrator handles)
- Rollback contract: `git revert HEAD` reverses the bundle. No template-side rollback machinery beyond that.

### 7. Dashboard slim

**Cuts (independent of audit work, can ship Stage 1):**

- **META block**: drop ALL `session_*` keys. Currently the Styler dashboard has dozens of multi-thousand-character `session_*` entries that are run-on session journals — handoff content, not navigation. META keeps only structural fields: `generated`, `task_count`, `task_hash`, `spec_version`, `spec_status`, `spec_fingerprint`, `template_version`, `verification_debt`, `drift_deferrals`, `decision_count`, `decisions_approved`, `decisions_superseded`, `decisions_partially_superseded`. (12-15 fields, not 50+.)
- **"Recent Activity (last 7 days)"**: cap at 7 entries, each ≤1 line. Format: `**YYYY-MM-DD** — {Task ID} {title} — {one-line outcome}`. No prose paragraphs, no embedded friction markers (those go to the register), no session-summary blocks.
- **Session-handoff content**: relocates to handoff file or git log; not duplicated in the navigation hub.

**Adds (depends on audit work):**

- Action Required → `🔍 Audit Findings` sub-section, marker-bracketed for sidecar persistence:

  ```markdown
  ### 🔍 Audit Findings

  *Last audit: coherence 2026-05-15 14:30Z (3 bundle-applied · 5 promote-eligible · 2 deduped to pending tasks)*

  <!-- AUDIT DIGEST -->
  - [ ] **C-02** "sub-tab" vs "section nav" vocab inconsistency (spec § 9.1, 11.1, 42.5) — [Fix it] / [Promote to FB] / [Dismiss]
  - [ ] **C-03** Oracle-thesis contradiction pattern recurring (3 friction register entries cluster) — [Promote] / [Dismiss]  *(design — no inline fix path)*
  - [ ] **C-05** 5 FB items >30 days open without status change — [Review FB] / [Dismiss]
  - [ ] **C-07** Phase 27 § 27.1 feature retirement workflow referenced but not implemented — [Fix it] / [Promote] / [Dismiss]
  - [ ] **C-08** Retired feature pull-to-refresh missing spec retirement marker (Phase 41) — [Fix it] / [Promote] / [Dismiss]
  <!-- END AUDIT DIGEST -->

  *Already covered by in-flight work (annotations):*
  - C-04 → T725 (Pending) — "spec § 28 path migration cleanup"
  - C-09 → T712 (In Progress) — "FB-071 Phase 27 retirement scaffolding"

  *To address any finding from any session: "address C-02 from the latest coherence audit". See Component 8.*
  ```

- Persistent across regens. Items removed only when promoted, dismissed, or resolved by next audit.
- Empty state: `*No audit findings. Last audit: {date}. Run `/health-check` to refresh.*`

**Changes to existing dashboard regen rules** (`.claude/support/reference/dashboard-regeneration.md`):

- META schema: drop `session_*` entries entirely; specify whitelist of allowed keys
- Recent Activity: enforce one-line-per-entry format, max 7 entries, max-7-days lookback
- Action Required sub-section ordering gets new entry: `Audit Findings` between `Spec Drift` and `Feedback`
- Sidecar (`dashboard-state.json`) gets new field: `audit_digest: { items: [...], dismissed_ids: [...] }`
- Section toggle for `🔍 Audit Findings` defaults to `[x]` if any audit command is applicable; `[ ]` otherwise

### 8. Async fix workflow ([Fix it] mechanism)

Audit findings need a different state model than `/work`'s sequential single-thread continuity. The user wants to chew through findings *in parallel* to `/work` running — possibly in a separate conversation, possibly in spare moments between active tasks. The audit naturally supports this because the audit dir is durable, `digest.json` is atomic-update, and each finding is independently addressable from any session.

**State isolation property:** The `audits/` directory + `digest.json` are independent of `.handoff.json` + `tasks/`. Two parallel sessions (one running `/work`, another addressing audit findings) don't fight over the same state. The dashboard digest section is the discoverable surface; the audit dir is the durable per-finding state; per-finding atomic updates avoid concurrency hazards. This directly addresses the "/work has only one handoff file" concern — audit work doesn't *need* a handoff because each finding is self-describing and re-loadable from disk.

**The mechanism:**

1. User opens any conversation (new or existing), references a finding by id: *"address C-02 from the latest coherence audit"* (or clicks the `[Fix it]` link in the dashboard, which expands to the same prompt).
2. Claude resolves the latest audit dir (`.claude/support/audits/coherence-{latest-ts}/`) and reads `findings.md#{C-02}` for full evidence + cited `source_anchors`. Rejects if finding `status` is already `resolved` / `dismissed` (avoids accidental re-application).
3. Claude **re-reads** the `source_anchors` to verify the finding's claim still holds (same at-apply invariant as bundled-apply — the synthesizer's first-pass classification is not trusted). If `files_to_touch` includes any spec / decision / vision file path, Claude **immediately** routes to `/iterate` regardless of how clear the fix looks (per Component 6 hard exclusion — those files are read-only outside `/iterate`).
4. Claude assesses scope and routes:
   - **Implementation-only, source-confirmed, single-source-of-truth fix** → applies inline, asks for approval before commit, single commit message `audit-fix: C-02 — {one-line summary}`, marks finding `status: resolved` in `digest.json`, marks any cited friction register entries `resolved` with audit + commit refs.
   - **Touches spec / decision record / vision document** → stops, says *"this requires spec amendment via /iterate"*, marks finding `status: escalated_to_iterate` with timestamp + reason, leaves it visible on dashboard. (No exception, even if the fix looks unambiguous — the read-only-outside-/iterate rule is structural.)
   - **Implementation file but ambiguous** (multiple plausible fixes, conflicting source statements) → stops, asks for clarification or routes to `/iterate` if disambiguation requires spec edits.
   - **Multi-file refactor or new design judgment required** → stops, says *"this is task-sized work"*, suggests creating a task via `/work`, marks `status: escalated_to_work` with reason.
5. On completion (any path), the dashboard's next regen reflects the new status. Resolved/dismissed items disappear from the digest; escalated items stay visible with an annotation pointing at the downstream work.

**Available actions per finding kind** (rendered as dashboard digest action links):

| Finding kind | `[Fix it]` | `[Promote to FB]` | `[Dismiss]` |
|--------------|:---:|:---:|:---:|
| `bundle-eligible` (impl-only, source-confirmed) | ✓ inline apply (single-finding mode) | ✓ | ✓ |
| `fix-eligible` (impl-only, clear fix, single source) | ✓ inline apply (may escalate) | ✓ | ✓ |
| `decision` (touches spec / decision record / vision) | ✓ auto-routes to `/iterate` (no inline apply — ever) | ✓ | ✓ |
| `design` (needs research / discussion) | — | ✓ | ✓ |

**The `decision` kind is structural, not advisory.** Any finding whose `files_to_touch` includes a spec / decision / vision path is auto-classified `decision` regardless of perceived clarity. [Fix it] on these only routes to `/iterate` — it never edits the file. This enforces the Component 6 hard exclusion at the action layer too.

For `design` kind, [Fix it] doesn't appear because there's nothing for Claude to do without judgment input — promote to FB → `/research` → DEC is the right path.

**Mid-fix escalation contract:** When [Fix it] routes to `/iterate` or `/work`, it leaves the finding in `escalated_to_*` status (not `resolved`) and adds an annotation: *"C-02 escalated to /iterate 2026-05-15 — see [link]"*. This keeps the finding visible on the dashboard until the downstream work closes the loop. The downstream work (a spec change in `/iterate` or a task in `/work`) is responsible for setting `status: resolved` once it lands. Convention: include the finding id in the spec change commit message or task `notes` field; a future audit run picks up the resolution.

**Bundled-apply (Component 6) is the batch-mode UX over this same mechanism** — same re-read invariant, same digest update protocol, same audit-trail commit shape; the only difference is one bulk approval instead of N per-finding interactions, and findings are combined into a single commit. That's why Stage 7 (bundled-apply UX) depends on Stage 6 ([Fix it] mechanism) and not the other way around.

### 9. Project-to-template graduation path

New audit types emerge from real project needs. The pattern is: discover the need in a project → build it as a project-local audit → run several times to validate → propose template integration → migrate. Styler's `/audit-ui` is exactly this story — Styler-only command for months, now being generalized into a template-shipped audit. Other anticipated examples:

- A data-engineering project might want `audit-data-quality` (schema drift, null-rate spikes, dimension consistency)
- A research project might want `audit-evidence` (claims without citations, stale references)
- A renovation project might want `audit-vendor-coverage` (line items without vendor quotes)

The template should formalize this graduation pattern so users don't have to reinvent the lens/synthesizer/digest interface each time.

**The pattern (3 stages):**

**Stage A — Project-local discovery (in the project, not the template):**
- User identifies a recurring quality concern in their project
- Creates `.claude/commands/audit-{name}.md` in the project, modeled on the template-shipped audit-command skeleton (see below)
- Implements lens prompts + synthesizer + digest output
- `applies_when` frontmatter declares conditions (so `/health-check` Part 8 picks it up)
- Runs the audit several times, refines lens prompts based on real findings
- Promotes findings via existing [Fix it] / [Promote to FB] mechanisms — same as template-shipped audits

**Stage B — Template-integration proposal (in the template repo):**
- When the project-local audit has stabilized AND is generalizable across projects of similar shape
- User opens the template repo, references the project-local audit definition
- Proposes integration via `template-maintenance/{audit-name}-template-integration.md` (same format as this proposal)
- Records open questions (what configurability is needed? what's project-specific that needs externalizing?)

**Stage C — Migration (in the template repo):**
- Audit moves to `.claude/commands/audit-{name}.md` in the template (same path shape as project-local — graduation is mainly about generalization + sync-flag inclusion, not restructuring)
- Project-specific bits become config files (e.g., `audit-ui.config.json` for surface bucket names)
- `applies_when` declarations updated for cross-project relevance
- Project's local copy stays until template version is verified equivalent, then deleted

**Template-side scaffolding to support this:**

1. **`.claude/support/reference/audit-template-pattern.md`** — canonical reference doc. Documents the lens/synthesizer/digest interface, `digest.json` schema, `applies_when` frontmatter, `[Fix it]` integration. Anyone building a new audit (project-local or template-shipped) reads this first.
2. **`.claude/support/templates/audit-skeleton.md`** — copy-paste skeleton for new audits. Contains placeholder `audit-{NAME}.md` with frontmatter, lens prompt structure, synthesizer prompt, digest schema. User clones into their project's `.claude/commands/` (renaming to their audit name) and fills in lens prompts + synthesizer logic.
3. **`/health-check` Part 8 detection** (already in Component 1) — picks up project-local `.claude/commands/audit-*.md` audits as first-class citizens, so they're discoverable through the same surface as template-shipped ones.

This pattern keeps experimentation fast (no template ceremony to try a new audit) while providing a clear upgrade path when an audit proves valuable beyond a single project.

---

## Staging (independent shippable chunks)

Designed so each stage is small, reviewable, and independently valuable.

### Stage 1 — Dashboard slim (no audit dependency)

Cut META session_* keys; cap Recent Activity to 1-line entries. Pure dashboard regen rule edit.

**Ships:** revised `dashboard-regeneration.md`, template version bump.
**Validates:** Styler dashboard regen drops from 67KB to ~15KB; no information loss (handoff content is in handoff files / git log).
**Risk:** low. Rollback via revert.

### Stage 2 — Friction register (no audit dependency)

Define schema, document write protocol, add return-report fields to implement-agent and verify-agent agent definitions. Register starts populating organically as agents run.

**Ships:** new `.claude/support/reference/friction-register.md`, updated `agents.md`, updated `implement-agent.md` and `verify-agent.md`.
**Validates:** entries appear in `friction.jsonl` after running `/work` for a few cycles in any project.
**Risk:** low. Agents that don't yet emit the field still work fine.

### Stage 3 — `audit-coherence` command

The command itself, including all 6 lenses and the synthesizer prompt. Initially exercised by direct invocation (`/audit-coherence` callable directly during development; `/health-check` Part 8 dispatch is Stage 5).

**Ships:** `.claude/commands/audit-coherence.md` (single file with frontmatter, capture procedure, 6 lens prompts as sections, synthesizer prompt as section, digest schema as section).
**Validates:** dry run on Styler produces a digest with at least 1 bundle-eligible finding (e.g., the react-native-pager-view orphan dep) and several promote-eligible spec-drift findings (DEC-010, foundation path divergences). Confirm hard-exclusion fires for any finding whose `files_to_touch` includes a spec/decision/vision path (those land in `decision` kind, not `bundle-eligible`).
**Risk:** medium. Lens prompts may over- or under-cluster — tune via Styler dry runs.

### Stage 4 — `audit-ui` command migration

Generalize Styler's `/audit-ui` command into the template's `.claude/commands/audit-ui.md`. Lens prompts stay nearly identical; surface bucket config externalized via optional `.claude/audit-ui.config.json`.

**Ships:** `.claude/commands/audit-ui.md` (template-shipped, sync-flagged), optional `audit-ui.config.json` schema in reference docs.
**Validates:** running on Styler produces equivalent output to the current Styler-local `/audit-ui` command.
**Risk:** low — mostly relocation + generalization. Styler's command file can stay until template version is verified equivalent, then deleted from Styler.

### Stage 5 — `/health-check` Part 8 (audit dispatch)

The router. Detects applicable audits (`.claude/commands/audit-*.md`), presents menu, dispatches selected audits.

**Ships:** edits to `.claude/commands/health-check.md`.
**Depends on:** Stage 3 (something to dispatch).
**Validates:** `/health-check` on Styler shows audit menu with `coherence` + `ui`; selecting `1` runs coherence audit and lands digest in dashboard.
**Risk:** low.

### Stage 6 — Dashboard digest section + [Fix it] mechanism

The persistent `🔍 Audit Findings` sub-section in Action Required, plus the per-finding [Fix it] async-fix mechanism (Component 8). These ship together because [Fix it] is the action surfaced on dashboard digest items.

**Ships:** `dashboard-regeneration.md` edits (digest section spec, marker pair `<!-- AUDIT DIGEST -->`), sidecar schema bump (`audit_digest: { items: [...], dismissed_ids: [...] }`), [Fix it] mechanism documentation in a new reference doc (`.claude/support/reference/audit-fix-workflow.md`), the at-apply spec re-read invariant, single-commit-per-finding contract, mid-fix escalation contract.
**Depends on:** Stage 5.
**Validates:** dry-run on Styler — pick a known finding (e.g., DEC-010 spec drift), invoke *"address C-01 from latest audit"* in a fresh session, confirm spec re-read happens, change applies as single commit, `digest.json` marks `resolved`. Test mid-fix escalation: inject a finding whose spec is genuinely ambiguous, confirm Claude routes to `/iterate` and marks `escalated_to_iterate` instead of applying. Test parallel-session safety: run [Fix it] on C-02 in one session while `/work` is active in another; confirm no state collision.
**Risk:** medium. This is the autonomy boundary — Claude can modify spec/code text after one approval per finding. Mitigation is in the at-apply re-read invariant. Could be staged to "promote-only" first (digest + promote + dismiss + escalation routing, no inline apply), then add inline-apply once the re-read protocol is battle-tested.

### Stage 7 — Bundled-apply batch-mode UX

The batch UX over Stage 6's [Fix it] mechanism. **No new autonomy expansion** — same at-apply re-read invariant — just a different prompting flow that handles N findings in one approval and one combined commit. Lower-risk because the autonomy boundary was established in Stage 6.

**Ships:** edits to `health-check.md` Part 8 to detect bundle-eligible findings post-audit and present the bulk approval prompt; combined-commit logic with per-finding `digest.json` updates; rejection-falls-through-to-individual-review path.
**Depends on:** Stage 6.
**Validates:** dry-run on Styler — confirm 3 bundle-eligible findings present together, single approval applies all 3 in one commit; rejection of any one falls through to per-finding [Fix it] for the rest; spec re-read happens once per finding (not collapsed across the batch).
**Risk:** low (autonomy already established in Stage 6; this is UX layer only).

**Suggested ship order:** Stage 1 → Stage 2 → Stage 3 → Stage 4 (parallel with 3) → Stage 5 → Stage 6 → Stage 7.

---

## Migration

### Template repo

1. Create `.claude/commands/audit-coherence.md` (Stage 3).
2. Migrate audit-ui from Styler to `.claude/commands/audit-ui.md` in the template (Stage 4).
3. Add Part 8 to `.claude/commands/health-check.md` (Stage 5).
4. Update `.claude/support/reference/dashboard-regeneration.md` per Stages 1 + 7.
5. Update `.claude/rules/agents.md` with friction-flag return-report convention.
6. New reference doc: `.claude/support/reference/friction-register.md` (schema + write protocol).
7. Bump template version per stage; sync flag set on all touched files.

### Styler-specific

- Existing `/audit-ui` command at `styler/.claude/commands/audit-ui.md` stays until the template-shipped version is verified equivalent. Then delete Styler's local copy — the template's `audit-ui.md` is auto-discovered by `/health-check` Part 8 (same `applies_when` trigger).
- Existing audit artifact dirs at `.claude/support/workspace/audit-*/` — leave alone (history). New audits land at `.claude/support/audits/`.
- Friction register starts empty — no backfill from existing dashboard prose (too messy; let next implementation cycles populate it organically).
- Existing dashboard prose stays until next regen, which slims it per new rules.

### Other projects using the template

- `audit-coherence` ships and triggers automatically (any project with a spec).
- `audit-ui` ships but only triggers on web-app projects (per `applies_when`).
- `/health-check` Part 8 runs on next invocation; first run shows audit menu.
- No data migration; new behavior on next run.
- **Project-local audits in `.claude/commands/audit-*.md` are auto-discovered** by Part 8 — no further action required to surface them through `/health-check`. See Component 9 for the graduation pattern from project-local to template-shipped.

---

## Open questions

1. **Lens granularity for coherence.** ✓ **Resolved (2026-05-15):** test first, decide after Stage 3 dry run on Styler. 6 lenses ship initially; fold if they over-cluster.

2. **Skill vs command for template-shipped audits.** ✓ **Resolved (2026-05-15):** ship as commands (`.claude/commands/audit-*.md`). Research (claude-code-guide agent) confirmed skills CAN dispatch sub-agents per docs but with murkiness around parallel-agent dispatch reliability; `/health-check` always explicitly dispatches audits (no auto-trigger needed), which is the use case where commands are "clearer" per Anthropic docs; existing precedent (`/audit-ui` in Styler) is already a command; project-local audits live in `.claude/commands/` regardless, so command-based template audits keep the file shape uniform across project-local and template-shipped (no restructuring needed at graduation). Reconsider migration to skills only if auto-trigger-by-project-shape becomes a needed feature later.

3. **Re-running the audit.** ✓ **Resolved (2026-05-15):** dedupe against prior digest. Persistent findings show "(unchanged)" badge; fresh ones show "(new)". Lets user track convergence.

4. **Friction-flag adoption staging.** ✓ **Resolved (2026-05-15):** Stage 2 ships schema + agent return-report fields. Audit-coherence's friction-register lens handles empty register gracefully. Acceptable to ship with cold register and let it warm up.

5. **Bundled-apply rollback.** ✓ **Resolved (2026-05-15):** single git commit per bundled-apply; revert is `git revert HEAD`. No template-side rollback machinery beyond standard git.

6. **Autonomy boundary.** ✓ **Resolved (2026-05-15):** structural rule, not a sliding criterion — **the specification (`.claude/spec_v*.md`), decision records (`.claude/support/decisions/decision-*.md`), and vision documents (`.claude/vision/**/*.md`) are read-only outside `/iterate`**. Audits read these files to detect drift; only `/iterate` writes them to resolve it. Enforced at the file-path level in Component 6 (hard exclusion) and Component 8 (action table — `decision` kind always routes to `/iterate`, no inline apply path exists). The user's load-bearing instinct ("only reading it, no writing at all, unless we go through the iterate command") is the rule. No DEC-013 needed — there is no autonomy expansion to review because the autonomy never extends to spec writes.

7. **Mid-fix escalation criteria.** ✓ **Resolved (2026-05-15):** ship with conservative defaults — implementation-file-only findings of **≤3 files** apply inline via [Fix it]; **>3 files** route to `/work` (creates a task). Tune after Stage 6 dry-runs if observed friction warrants. (Spec/decision/vision touches always route to `/iterate` regardless of file count, per Q6 hard rule.)
7. **Dashboard-state.json schema migration.** Adding `audit_digest` field is additive but downstream projects with existing `dashboard-state.json` files need a one-time read-and-merge. Existing schema migrations in the template don't have a clean precedent — worth checking how `template_version` field addition was handled.

---

## Out of scope (future audit types this enables, not building now)

- `audit-perf` — bundle size, slow imports, heavy dependencies (web app)
- `audit-a11y` — accessibility lens family (web app, separate from `audit-ui`'s cohesion lenses)
- `audit-test-coverage` — gaps between what's tested and what spec acceptance criteria require
- `audit-decision-coverage` — areas of the spec that lack a decision record despite implied design choices
- `audit-deps` — outdated/vulnerable dependencies, license issues

Each future audit follows the same command interface — `applies_when` frontmatter declaration, capture procedure, lens prompts as sections, synthesizer prompt as section, `digest.json` schema. The pattern this proposal establishes is the reusable bit; the specific audits beyond `coherence` and `ui` are future opportunistic adds, often emerging from real project needs and graduating per Component 9.
