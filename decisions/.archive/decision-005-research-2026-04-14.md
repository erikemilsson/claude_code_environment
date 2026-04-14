# Research Archive: DEC-005 — Base allowedTools Shipping Policy

**Date:** 2026-04-14
**Researcher:** research-agent (Opus 4.6)
**Decision record:** `decisions/decision-005-base-allowedtools-shipping-policy.md`
**Feedback source:** FB-012 (`.claude/support/feedback/feedback.md`)

---

## Investigation Methodology

1. Read decision record draft (Options A-D pre-populated, 5 research questions)
2. Read FB-012 full text (capture, refinement, assessment notes)
3. Audited current template state:
   - `.claude/settings.local.json` (current personal permissions — proxy for "what's actually used")
   - `.claude/sync-manifest.json` (file categories — confirmed no `merge` category exists)
   - `.claude/commands/health-check.md` Part 5 (Template Sync) and Part 5c (Settings — currently asserts template doesn't ship settings)
   - `system-overview.md` (Template Sync section — confirms ownership boundaries)
4. Web research on Claude Code permission semantics (official docs + community sources)
5. Web research on VS Code extension contribution model as a "ship base config" precedent
6. Reviewed `merge-claude-code-settings` community tool for prior art on allow-array merging

---

## Q1 Research: Safe base set composition

### Audit of current `.claude/settings.local.json`

Categorized by safety:

**Universally safe (read-only / inspection):**
- `Bash(git status:*)` — read-only
- `Bash(git diff:*)` — read-only
- `Bash(git log:*)` — read-only
- `Bash(git check-ignore:*)` — read-only
- `Bash(git ls-tree:*)` — read-only
- `Bash(git branch:*)` — branch listing is read-only; creation is mutating but local-only
- `Bash(ls:*)` — read-only
- `Bash(tree:*)` — read-only
- `Bash(wc:*)` — read-only
- `Bash(grep:*)` — read-only
- `Bash(find:*)` — read-only (without `-delete`/`-exec`)
- `Bash(head:*)` — read-only
- `Bash(test:*)` and `Bash(test -f:*)` — read-only
- `Bash(sort:*)` — read-only stream processing
- `Bash(shasum:*)` — read-only checksum

**Local-mutating but bounded (debatable for base set):**
- `Bash(git add:*)` — stages files; bounded to repo
- `Bash(git commit:*)` — local commit; reversible
- `Bash(git checkout:*)` — can lose uncommitted work; risky
- `Bash(git rm:*)` — destructive
- `Bash(git init:*)` — only creates `.git/`; safe
- `Bash(chmod:*)` — broad pattern is too permissive (`chmod -R 000` is disastrous); narrow form `Bash(chmod +x scripts/*)` is safer
- `Bash(unzip:*)` — can clobber files; project-context-dependent
- `Bash(python3:*)` — arbitrary code execution; project-context-dependent

**Should NOT be in base (network / push):**
- `Bash(git push:*)` and `Bash(git push)` — pushes to remote; user-owned
- `WebSearch` — network; user can opt in per-project

**Garbage entries (artifacts of misclick on the permission prompt):**
- `Bash(for f in .claude/tasks/task-*.json)` — fragment of a multi-line script
- `Bash(do python3 -c ...)` — fragment
- `Bash(done)` — shell keyword
- These should NOT be in any base set; they're noise from approving compound commands

### Proposed base set (universally safe, template-shipped)

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git branch:*)",
      "Bash(git check-ignore:*)",
      "Bash(git ls-tree:*)",
      "Bash(ls:*)",
      "Bash(tree:*)",
      "Bash(wc:*)",
      "Bash(head:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(test:*)",
      "Bash(sort:*)",
      "Bash(shasum:*)"
    ]
  }
}
```

Rationale for inclusion: every entry is read-only or strictly local-state-inspecting. None mutate the working tree, none reach the network, none can damage the repo. All are commonly invoked by `/work`, `/health-check`, and the implement/verify agents during normal operation.

Deliberately excluded from base set (project-owned additions):
- `Bash(git add/commit/rm/push:*)` — write operations should be opt-in per project
- `Bash(python3:*)`, `Bash(npm:*)`, `Bash(cargo:*)`, etc. — language-specific
- `Bash(chmod:*)` — too broad; user can add `Bash(chmod +x scripts/*)` per project
- `WebSearch`, `WebFetch(domain:*)` — user-controlled per project

---

## Q2 Research: Claude Code's own behavior

### Settings layering (from official docs at code.claude.com/docs/en/permissions)

Precedence (highest first):
1. Managed settings (org policy, MDM-deployed)
2. CLI flags (`--allowedTools`, `--disallowedTools`)
3. Local project (`.claude/settings.local.json`)
4. Shared project (`.claude/settings.json`)
5. User (`~/.claude/settings.json`)

### Array merge semantics — KEY FINDING

From the docs and corroborated by community write-ups (Vincent Qiao's deep-dive blog, claudefa.st reference):

> **Array fields (such as `permissions.allow[]`, hooks, enabledMcpjsonServers, etc.) are concatenated and deduplicated — not overridden, so that rules from both sources are kept.**

This is foundational. It means:
- Shipping a base `allowedTools` in `.claude/settings.json` does **not** clobber `.claude/settings.local.json` user additions — Claude Code merges them at runtime
- The user's project-level additions to `.claude/settings.json` likewise merge with the template's base set if both arrays exist in the same file (but they don't — there's only one file)
- The risk is solely at the **file-write** stage during template sync, not at the runtime evaluation stage

### Default shipped permissions

Claude Code itself ships **no default `allowedTools`**. Read-only operations (Read, Grep, Glob) are pre-approved by tool category, not by `allowedTools` entries. Bash, Edit, and similar mutating tools require explicit approval per project.

### Deny precedence

Deny rules at any level cannot be overridden by allow rules at any other level. Deny > ask > allow. Relevant for the base set: shipping `Bash(git status:*)` as allow cannot accidentally override a project's deny rule.

---

## Q3 Research: Merge patterns in the wild

### VS Code extensions (closest analog)

VS Code extensions contribute settings via `package.json` `contributes.configuration`. Defaults from extensions form the lowest layer; user/workspace settings override them. **Arrays of strings in user settings replace defaults entirely** (last-writer-wins at field level), but extensions can mark defaults as "inherited and merged" via specific schema decorations.

Key insight: VS Code's model treats extension-shipped values as **defaults** that user settings override. There's no "tracking which entries came from where" — the user's array fully replaces the default. This is simpler than what FB-012 requires but loses the user-extends-base property.

### ESLint plugins

ESLint configs use `extends:` to inherit rule sets. Override is per-rule (the config map's keys). Removal happens by setting `"rule-name": "off"`. There's no array-merge problem because rules are keyed objects, not arrays.

### `systemd`-style drop-in directories

`managed-settings.d/` in Claude Code itself uses systemd's drop-in convention: multiple files merged alphabetically, later files override earlier ones for object fields, arrays concatenate. This is the same merge model we already get for free across the user/project/local layers.

### `merge-claude-code-settings` (community tool)

Found at `github.com/massongit/merge-claude-code-settings`. A TypeScript utility that merges multiple project-specific Claude Code settings files into the global one. Confirms the community is hitting this exact problem. (Couldn't fetch full source due to permissions, but the existence and stated purpose validate the use case.)

### Pattern summary

Three observed patterns for "ship base + user extends":
1. **Last-writer-wins at field level** (VS Code default for arrays): simple, but loses user additions on update
2. **Concatenate-and-dedupe at runtime** (Claude Code's actual behavior across layers): perfect, but only works because the layers are separate files
3. **Origin-tracked merge at write time** (what Option B proposes): needed when source and destination are the same file

For DEC-005, pattern 2 is the loophole that makes Option A workable: if the template ships `.claude/settings.json` and projects keep their own additions in `.claude/settings.local.json`, **merging is automatic at runtime and no template-sync logic is needed at all**. The merge problem only exists if we want template additions and project additions to coexist in the same file.

---

## Q4 Research: Removing entries from base set

If the base set drops an entry (e.g., narrowing `Bash(chmod:*)` to `Bash(chmod +x scripts/*)`):

- **Option A (add-only):** Project keeps the old broad `Bash(chmod:*)` indefinitely. Adding the new narrow rule is harmless (deduplication keeps both, but the broad one shadows the narrow one). Net effect: tightening is impossible without manual user action.
- **Option B (key-granular with origin tracking):** Requires a sidecar file (e.g., `.claude/settings.template-base.json` or a `_template_origin` array inside `settings.json`) recording which entries came from the template. On sync, template-origin entries are replaced; user-origin entries are kept. Tightening works.
- **Option C (full sync):** Tightening trivially works but clobbers user additions. Out of scope.
- **Option D (don't ship):** N/A.

Recommended encoding for Option B: a sidecar file `.claude/.template-managed-settings.json` listing the template-managed keys/entries. Not user-edited; regenerated on sync. Avoids polluting `settings.json` with non-Claude-Code-recognized fields.

**Layered alternative (not in original options):** Ship the base set as-is in `.claude/settings.json`, treat that file as **fully template-owned** (sync category), and require all user additions to live in `.claude/settings.local.json` (which is gitignored anyway). Claude Code's runtime merge handles the union. This sidesteps the merge-strategy debate entirely. **See "Option E" in Recommendation below.**

---

## Q5 Research: Existing `sync-manifest.json` categories

Three categories exist today:
- `sync` — fully template-owned, replaced wholesale on update
- `customize` — user may modify; template-version is a starter only
- `ignore` — never touched by sync

There is **no `merge` category**. Currently `.claude/settings.local.json` is in `ignore`, and `.claude/settings.json` is not listed at all (because the template doesn't ship it).

For Options A or B, a new `merge` category would need to be added with documented merge semantics. For the layered alternative (Option E), `.claude/settings.json` would simply be added to the existing `sync` category and `.claude/settings.local.json` stays in `ignore` — no schema change.

---

## Discarded Approaches

### "Track origin inside settings.json via a custom field"

E.g., a `_templateManaged: ["Bash(git status:*)", ...]` field inside `.claude/settings.json`. Rejected because Claude Code may emit warnings on unrecognized top-level fields and we'd be polluting a file the harness owns. Sidecar file is cleaner.

### "Use Claude Code's `--allowedTools` CLI flag injection via a wrapper script"

Rejected because (a) the template can't control how the user invokes Claude Code, and (b) the goal is durable cross-session permission, not per-invocation injection.

### "Ship the base set in `~/.claude/settings.json` (user-level)"

Rejected because the template can't write to the user's home directory without explicit user action, and user-level settings affect every project the user runs Claude Code in — including non-template projects. Keeping the base set project-scoped respects isolation.

---

## Cross-cutting Considerations

### Interaction with FB-010 (subagent sandbox)

FB-010 reports that subagents are sandboxed and can't write outside the project's primary cwd. Settings reads are unaffected (read-only operations always work). No interaction with the choice between A/B/C/D/E.

### Interaction with FB-011 (scripts as alternative to commands)

If Option B is selected, the merge logic is a strong candidate for extraction into a deterministic script (`.claude/scripts/sync-settings.py` or similar). The merge is well-defined and benefits from determinism over LLM execution. Option E avoids this entirely since no merge logic is needed.

### Sync ordering risk

If `.claude/settings.json` lands in the `sync` or new `merge` category, it must be applied before any subsequent file operations that depend on the new permissions. In practice this is fine because all template sync happens in a single `/health-check` pass.

---

## Sources

- Claude Code permissions docs: https://code.claude.com/docs/en/permissions
- Vincent Qiao's settings deep-dive (Part 2): https://blog.vincentqiao.com/en/posts/claude-code-settings-permissions/
- Vincent Qiao's settings deep-dive (Part 1): https://blog.vincentqiao.com/en/posts/claude-code-settings-intro/
- claudefa.st settings reference: https://claudefa.st/blog/guide/settings-reference
- FlorianBruniaux deepwiki: https://deepwiki.com/FlorianBruniaux/claude-code-ultimate-guide/4.2-settings-and-permissions-files
- Community merge tool: https://github.com/massongit/merge-claude-code-settings
- VS Code settings hierarchy: https://code.visualstudio.com/docs/configure/settings
- VS Code contribution points: https://code.visualstudio.com/api/references/contribution-points

---

## Recommendation Summary

See the Recommendation section in the decision record itself. Short version: **Option E (layered, two-file)** is a strong addition to consider — it gets the friction-reduction win of Option A with the tightening-capable property of Option B and the simplicity of Option D's policy story, by exploiting Claude Code's runtime array merge semantics. Among the originally-drafted options, **Option B** is preferred over Option A because it preserves the ability to tighten the base set; **Option A** is acceptable as a v1 if Option B's merge logic is deemed too complex to ship initially.
