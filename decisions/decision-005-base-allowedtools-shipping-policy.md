---
id: DEC-005
title: Base allowedTools shipping policy and merge strategy
status: approved
category: process
created: 2026-04-14
decided: 2026-04-14
related:
  tasks: []
  decisions: []
  feedback: [FB-012]
implementation_anchors: []
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# Base `allowedTools` shipping policy and merge strategy

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Ship base set, add-only merge (safe, simple)
- [ ] Option B: Ship base set, key-granular merge with version-tracked removal
- [ ] Option C: Ship base set, full-file sync (clobbers user additions — rejected by default)
- [ ] Option D: Don't ship — keep current policy
- [x] Option E: Ship base set as fully template-owned `settings.json`; require user additions in `settings.local.json` (layered)

*Check one box above, then fill in the Decision section below.*

---

## Context

The template currently does not ship `.claude/settings.json`. Policy is documented in `health-check.md` Part 5c: *"confirm template doesn't ship settings files"*. Only `.claude/settings.local.json` exists (user-specific, gitignored in practice).

The problem: `acceptEdits` mode (Max plan can't use auto mode) triggers a permission prompt for every Bash call, Edit, etc. that isn't pre-approved. Each downstream project ends up rebuilding the same base set of safe permissions — `Bash(git status:*)`, `Bash(ls:*)`, `Bash(grep:*)`, and so on. Shipping a conservative base set from the template would eliminate that duplication.

Claude Code settings layer additively: user-level (`~/.claude/settings.json`) → project-level (`.claude/settings.json`) → project-local (`.claude/settings.local.json`). **Critical research finding:** array fields like `permissions.allow[]` are concatenated and deduplicated across these layers at runtime — they do NOT replace each other. This changes the design space significantly.

Scope caveat: FB-012 scoped the reversal to `allowedTools` only. Hooks, env vars, theme stay user-owned. Any in-file merge strategy must be key-granular to respect that. The layered alternative (Option E) sidesteps this by keeping the template's `settings.json` to `permissions.allow` only and letting users put hooks/env/theme in `settings.local.json`.

## Questions to Research

(Answers in `## Research Findings` below.)

1. Which commands belong in a safe, universally-applicable base set?
2. What does Claude Code itself do (defaults, merge semantics)?
3. How do other tools (VS Code, ESLint) handle shipping a base config?
4. What happens on template update if the base set drops a permission?
5. Does `sync-manifest.json` have a `merge` category, or is one needed?

## Options Comparison

| Criteria | A: Add-Only | B: Key-Granular Merge | C: Full Sync | D: Don't Ship | E: Layered (two-file) |
|----------|-------------|-----------------------|--------------|---------------|------------------------|
| Reduces permission prompts | Yes | Yes | Yes | No | Yes |
| Preserves user additions | Always | Always | No | N/A | Always (separate file) |
| Handles base-set removals | No (drift) | Yes (origin tracking) | Yes (clobbers) | N/A | Yes (template owns file) |
| Implementation complexity | Low | Medium-High | Low (rejected) | Zero | Low |
| Sync logic changes | Small (new merge cat.) | Medium (new merge cat. + sidecar) | Small (sync cat.) | None | Small (sync cat. only) |
| Schema changes to manifest | New `merge` category | New `merge` category | None | None | None |
| Allows tightening base set | No | Yes | Yes | N/A | Yes |
| Risk to user-customized hooks/env | None (scoped to `allow`) | None (key-granular) | High (clobbers) | None | None (separate file) |
| Conceptual model clarity | Medium (drift accumulates) | Low (origin tracking is non-obvious) | High but unsafe | High | High (layered = familiar) |
| Effort to ship v1 | ~1 task | ~2-3 tasks | ~1 task | 0 | ~1 task |

**Recommendation:** Option E is the strongest choice — see `## Recommendation` below.

## Option Details

### Option A: Ship base, add-only merge

**Description:** Template ships `.claude/settings.json` with a base `allowedTools` array. On template sync, `/health-check` adds any new entries from the template to the project's list without removing anything. If the template removes a permission, the project keeps the old one (drift).

**Strengths:**
- Simplest merge logic
- Never loses user additions
- Never breaks project workflows by removing a permission

**Weaknesses:**
- Drift over time: projects accumulate stale permissions from old template versions
- No way to tighten the base set
- Requires a new `merge` category in `sync-manifest.json`
- Conflates template-owned and user-owned entries in one file

**Research Notes:** Functional but introduces silent drift. If the template ever wants to narrow `Bash(chmod:*)` to `Bash(chmod +x scripts/*)` for safety, projects will keep both rules forever (broad rule shadows narrow). Add-only merge is a one-way ratchet on the permission surface — usually worse, not better, over time. Acceptable as a v1 if Option B is too complex.

### Option B: Ship base, key-granular merge with version tracking

**Description:** Template ships `.claude/settings.json` with a base `allowedTools` array. `.claude/sync-manifest.json` gets a new `merge` category for `settings.json`. On template sync, `/health-check` tracks which `allowedTools` entries come from the template (via a sidecar file `.claude/.template-managed-settings.json`) vs. which are user additions. Template updates can add or remove template-owned entries; user additions always stay.

**Strengths:**
- Handles base-set tightening (security improvements possible)
- Never loses user additions
- Supports key-granular: hooks/env/theme stay untouched

**Weaknesses:**
- Requires sidecar file for origin tracking, plus merge logic in `/health-check`
- More complex mental model — users must understand that some entries are "managed"
- Sidecar can drift from reality if user manually edits `settings.json`
- Strong candidate for script extraction (FB-011) but until then, LLM-executed merge is error-prone

**Research Notes:** Most flexible option but heaviest implementation. The origin-tracking sidecar (`.claude/.template-managed-settings.json`) is unfamiliar to users and adds a file they shouldn't touch. Worth doing if there's a clear future need to tighten the base set; speculative if not. Could be implemented by a deterministic script per FB-011 to address the LLM-reliability concern.

### Option C: Ship base, full-file sync (rejected default)

**Description:** Treat `.claude/settings.json` as a regular `sync` file — template replaces project's version on sync. User additions are lost.

**Strengths:** Simple
**Weaknesses:** Clobbers user-specific permissions in the same file. Violates the "hooks/env/theme stay user-owned" scope constraint if the user also put those in `settings.json`.
**Research Notes:** Not viable per FB-012 scope as written. However, see Option E for a variant that uses full-file sync but moves user-owned content out of the file.

### Option D: Don't ship — keep current policy

**Description:** Keep Part 5c's current stance. Document a reference base set in a workspace file that users can copy manually.

**Strengths:** Zero implementation cost. Preserves current design intent. No new sync semantics.
**Weaknesses:** Doesn't solve the friction FB-012 raised. Every new project re-derives the same base set by clicking through permission prompts.
**Research Notes:** Fails the primary user goal. Listed for completeness as the status-quo baseline.

### Option E: Layered (two-file)

**Description:** Template ships `.claude/settings.json` containing **only** `permissions.allow` with the base set. The file is added to the existing `sync` category (fully template-owned, replaced wholesale on update). All user-specific additions — extra `permissions.allow` entries, hooks, env vars, theme, anything else — go in `.claude/settings.local.json` (already gitignored, already in `ignore` category).

This works because **Claude Code's runtime merge concatenates and deduplicates `permissions.allow` arrays across all settings layers**. The user never edits `.claude/settings.json`; the template owns it entirely. The user's additions in `.claude/settings.local.json` merge in automatically at runtime, and template sync never touches them.

**Strengths:**
- No new `sync-manifest.json` category needed — `.claude/settings.json` slots into existing `sync`
- No origin-tracking sidecar — file ownership is unambiguous
- Tightening works trivially (template just removes the entry; sync replaces the file)
- User additions are physically separated and impossible to clobber
- Uses Claude Code's documented runtime merge as the integration point — leverages the platform instead of fighting it
- Conceptual model matches existing template philosophy: "template owns the template-owned files; user owns the user-owned files"
- Sidesteps the entire merge-strategy debate
- Lowest implementation cost of all viable options

**Weaknesses:**
- Requires user to know that custom permissions go in `settings.local.json`, not `settings.json` (documentation problem; mitigated by README + `/health-check` Part 5c message)
- If a user does add entries to `.claude/settings.json`, template sync silently overwrites them — this needs a clear health-check warning ("Found local edits to template-owned `settings.json`. Move to `settings.local.json`?")
- `.claude/settings.local.json` is gitignored, so user-extended permissions are not shared across team members — but this is already the case today and is consistent with how Claude Code itself splits the files
- Doesn't allow team-shared project-specific permissions in `.claude/settings.json` — those would need a project-level decision to either (a) ship a `.claude/settings.project.json` extension (not a Claude Code primitive; would need custom merge), or (b) accept that team-shared additions go into `.claude/settings.json` and overwrite the template's base — falling back to Option A or B for that subset

**Research Notes:** The runtime-merge property is documented in the official Claude Code permissions docs and corroborated by community deep-dives (Vincent Qiao, claudefa.st). This is not a workaround — it's the platform's intended design. The layered approach mirrors how managed/user/project/local already coexist. The biggest risk is the team-sharing edge case: if a project legitimately needs shared permissions beyond the template base, the user has to decide between gitignoring them (current approach) or developing a project-level extension pattern (out of scope for FB-012).

**Why this wasn't in the original four options:** FB-012's framing assumed the merge problem was inevitable. The runtime-merge research finding is what unlocks this option.

## Research Findings

### Q1: Safe base set composition

Audit of `.claude/settings.local.json` shows three classes:

**Universally safe (proposed base set, all read-only or strictly local-inspecting):**
```
Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*),
Bash(git check-ignore:*), Bash(git ls-tree:*), Bash(ls:*), Bash(tree:*),
Bash(wc:*), Bash(head:*), Bash(grep:*), Bash(find:*), Bash(test:*),
Bash(sort:*), Bash(shasum:*)
```

**Project-context-dependent (NOT in base; user opts in per project):**
- `Bash(git add/commit/rm/push:*)` — write/network operations
- `Bash(python3:*)`, `Bash(npm:*)`, language-specific runners
- `Bash(chmod:*)` — too broad; safer narrowed forms project-specific
- `Bash(unzip:*)` — can clobber files
- `WebSearch`, `WebFetch(domain:*)` — network access

**Garbage entries to filter out** (artifacts of misclick on multi-line command approvals):
`Bash(for f in .claude/tasks/task-*.json)`, `Bash(do python3 -c ...)`, `Bash(done)` — these are shell fragments, not real permissions.

### Q2: Claude Code's own behavior

- **Settings precedence (highest first):** Managed → CLI flags → Local project (`settings.local.json`) → Shared project (`settings.json`) → User (`~/.claude/settings.json`).
- **Array merge:** `permissions.allow[]`, `hooks[]`, and similar arrays are **concatenated and deduplicated across all layers at runtime** — they do not replace each other. This is the foundational finding.
- **Default permissions:** Claude Code itself ships **no default `allowedTools`**. Read-only tools (Read, Grep, Glob) are pre-approved by category, not by entries.
- **Deny precedence:** Deny rules at any level cannot be overridden by allow at any other level. Shipping a base allow cannot accidentally subvert a project deny.

### Q3: Merge patterns in the wild

- **VS Code:** Extensions ship defaults via `contributes.configuration`; user settings override defaults at the field level. For arrays, user settings replace defaults entirely — the "user-extends-base" property is lost on update.
- **ESLint:** `extends:` inherits rule sets; per-rule override; removal via `"rule-name": "off"`. Works because rules are keyed objects, not arrays.
- **`systemd`-style drop-in (used by Claude Code's own `managed-settings.d/`):** Multiple files merged alphabetically; arrays concatenate. Same model as the user/project/local layering.
- **Community tool `merge-claude-code-settings`:** Confirms others have hit this exact problem.

Pattern summary: three options for "ship base + user extends":
1. **Last-writer-wins at field** (VS Code default for arrays) — loses user additions on update
2. **Concat+dedupe at runtime** (Claude Code's actual cross-layer behavior) — perfect, but requires layers to be separate files
3. **Origin-tracked merge at write time** (Option B) — needed when source and dest are the same file

Pattern 2 is what makes Option E possible.

### Q4: Removing entries from base set

- **Option A:** Drift forever. Tightening impossible without manual user action. Add-only merge is a one-way ratchet on the permission surface.
- **Option B:** Works via sidecar origin tracking. Template-managed entries replaced; user additions kept. Most flexible, most complex.
- **Option C:** Trivially works but clobbers user additions. Out of scope.
- **Option D:** N/A.
- **Option E:** Trivially works. Template removes the entry, sync replaces the whole file, user's `settings.local.json` is untouched. If the user had also added the now-removed entry in `settings.local.json`, it stays — which is correct (user explicitly opted in).

### Q5: `sync-manifest.json` categories

Three exist: `sync`, `customize`, `ignore`. **No `merge` category.**

- Options A and B require a new `merge` category with documented merge semantics.
- Option E needs no schema change — `.claude/settings.json` slots into existing `sync`, and `.claude/settings.local.json` stays in `ignore` (where it already is implicitly via the gitignore convention).

## Your Notes & Constraints

*Add any constraints, preferences, or context that should inform this decision.*

**Constraints:**
- Template-maintenance decision record — ephemeral, removed after resolution
- Scope is `allowedTools` only (hooks, env, theme stay user-owned)
- Must work with existing `.claude/sync-manifest.json` categories or add a new one

**Research Questions for the user:**
1. **Team-shared permissions** — Some projects may want permissions shared across team members (e.g., everyone on the team should auto-allow `Bash(npm test:*)`). In Option E this would either (a) be added to the template-owned `.claude/settings.json` and lost on next sync, or (b) be gitignored in `.claude/settings.local.json` and re-added per developer. Is this a real need for downstream projects, or is per-developer customization acceptable? If team-shared is needed, Options A or B (in-file merge) become more attractive.
2. **Tightening cadence** — Do you anticipate ever needing to narrow or remove an entry from the base set (e.g., for a security improvement)? If yes, Option A is poor (drift). If no, Option A's simplicity becomes more attractive.
3. **Tolerance for the "edit-the-wrong-file" failure mode in Option E** — If a user mistakenly adds permissions to `.claude/settings.json`, template sync silently overwrites them. `/health-check` can detect and warn, but it's a recoverable mistake the user has to learn. Acceptable?

## Recommendation

**Strong preference for Option E (layered, two-file).**

**Key tradeoff:** Option E gets the friction-reduction win of Option A, the tightening capability of Option B, and the simplicity of Option D's policy story — at the cost of constraining team-shared additions to live in `settings.local.json` (which is gitignored). This works because Claude Code's runtime merge concatenates `permissions.allow` arrays across files automatically; we don't need any merge logic in `/health-check` at all.

**Why Option E over the alternatives:**
- vs. **A:** No drift accumulation; tightening works; no new manifest category needed.
- vs. **B:** No origin-tracking sidecar to maintain; no complex merge logic to write or test; lower cognitive load for users.
- vs. **C:** Doesn't clobber anything because user content lives in a different file.
- vs. **D:** Solves the actual user friction.

**The one real concern with Option E** is the team-sharing edge case (Question 1 above). If downstream projects regularly want team-shared additions to the base set, Option B becomes preferable — but this is speculative and has no evidence yet. Recommend deferring that complexity until a concrete project demands it.

**If Option E is rejected on the team-sharing concern, recommend Option B over Option A.** Option A's drift property is a long-term liability that compounds. Option B's complexity is bounded and a strong candidate for script extraction under FB-011.

**Confidence:** High on the research findings (runtime merge behavior is well-documented). Moderate on the recommendation — Option E is novel and depends on the team-sharing question.
