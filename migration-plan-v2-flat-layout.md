# Migration Plan: Template v2 (Flat Layout)

Moving from subdirectory layout to flat layout across the template and existing projects.

---

## Part 1: What Actually Needs to Change

The research agent found that the template's operational code (`.claude/` commands, agents, rules, reference docs) is **already layout-agnostic**. No command assumes `app/`. No agent runs `cd app/`. No rule references subdirectory paths. The `.claude/` environment works the same whether the app is at root or in a subdirectory.

What needs to change is **guidance and metadata**, not behavior:

| Change | Scope | Effort |
|--------|-------|--------|
| Update `system-overview.md` references to subdirectory pattern | Template repo | Small — a few paragraphs |
| Update or simplify KI-001 in `known-issues.md` | Template repo | Trivial — add note that flat layout avoids this |
| Add `session-management.md` to `sync-manifest.json` | Template repo | One line |
| Bump `template_version` to 2.0.0 in `version.json` | Template repo | One line |
| Update `setup-checklist.md` to note flat layout assumption | Template repo | Small |
| Update `root-claude-md-template.md` Key Commands section | Template repo | Small |
| Clean up decision/analysis docs (optional) | Template repo | Delete temp files |

**Total template changes: ~1 hour of focused work.**

The `.claude/` directory that ships to projects doesn't change structurally. Commands, agents, rules — all identical. A project on v2 runs the same `/work`, `/iterate`, `/review` as v1.

---

## Part 2: What Changes for Existing Projects

This is the real question. Each existing project has:

- App source code in a subdirectory (e.g., `app/`)
- `package.json`, `next.config.js`, etc. inside that subdirectory
- Task JSON files with `files_affected` referencing `app/src/...` paths
- Spec referencing subdirectory paths
- CI/CD configured with `rootDirectory: app/`
- Dev scripts that `cd` into the subdirectory
- `.claude/` at repo root (already correct for flat layout)

### Per-Project Migration Procedure

If you choose to migrate a project, here's the procedure:

**Step 1: Pre-flight (5 min)**
```
- Ensure all tasks are Finished or On Hold (no In Progress work)
- Commit everything — clean working tree
- Create a branch: git checkout -b migrate-to-flat-layout
```

**Step 2: Move app files to root (10-30 min depending on project size)**
```
- Move app contents to repo root:
    mv app/package.json ./
    mv app/next.config.js ./  (or vite.config.js, etc.)
    mv app/src/ ./
    mv app/public/ ./
    mv app/tsconfig.json ./
    ... (all app files)
- Remove empty app/ directory
- Keep .claude/, foundation/, docs/ where they are (already at root)
- Update .gitignore if it had app/-prefixed entries
```

**Step 3: Fix paths (15-60 min depending on complexity)**
```
- package.json scripts: remove any cd app/ or ../foundation references
- Framework config: remove root/base directory overrides
- CI/CD: remove rootDirectory settings
- Docker: update WORKDIR and COPY paths
- Import statements: grep for '../../../foundation' or similar deep paths
  (these get shorter — foundation/ is now a sibling of src/)
```

**Step 4: Fix template artifacts (10 min)**
```
- Task JSON files: find-and-replace 'app/src/' → 'src/' in files_affected
- Spec: update any path references
- Dashboard: will regenerate on next /work run
- Dev scripts (start-dev.sh etc.): remove --webpack flag, remove cd app/
```

**Step 5: Verify (15 min)**
```
- npm install (from repo root now)
- npm run dev (should work without --webpack)
- npm run build
- Run /health-check
```

**Step 6: Commit and merge**

**Estimated total per project: 1-2 hours for a straightforward Next.js project.**

### When to Migrate vs. When to Leave Alone

| Project State | Recommendation |
|---------------|----------------|
| Not yet started | Start flat. No migration needed. |
| Early stage (< 20% complete) | Migrate now — low cost, high benefit |
| Mid-execution (active tasks) | Finish current phase, then migrate at the phase boundary |
| Near completion (> 80%) | Don't migrate. Finish with `--webpack`. |
| Completed / maintenance only | Migrate only if you'll do significant new work |

---

## Part 3: Do You Need to Migrate At All?

**For new projects: no migration, just start flat.** Copy `.claude/` into your project root (where `package.json` already lives). Done.

**For existing projects: the `--webpack` workaround works.** Your existing projects aren't broken — they have a workaround. Migration is about removing friction, not fixing something that's down. You can migrate projects opportunistically:

- When you start a new phase and want a clean break
- When CI/CD friction justifies the time investment
- When you're doing a major refactor anyway
- Never, if the project is winding down

**The template sync (health-check) continues to work.** `.claude/` contents are the same in both layouts. Health-check syncs `.claude/` files — it doesn't care where `package.json` lives. A v1-layout project can run v2 template commands without migrating.

---

## Part 4: Fork vs. Evolve

**You don't need a fork.** Here's why:

The template ships `.claude/`. The `.claude/` directory is layout-agnostic. There's nothing in v1's `.claude/` that breaks in a flat layout, and nothing in v2's `.claude/` that breaks in a subdirectory layout.

What changes between v1 and v2:
- **Guidance** — setup docs say "app at root" instead of "app in subdirectory"
- **Known issues** — KI-001 gets a note that flat layout avoids it
- **Version number** — 1.5.0 → 2.0.0 (signals the conceptual change)

What stays identical:
- Every command definition
- Every agent definition
- Every rule file
- Every reference doc (except setup-checklist, known-issues)
- The sync manifest
- The task system, dashboard, verification pipeline

A fork would mean maintaining two sets of commands, agents, and rules that are functionally identical. That's pure overhead with zero benefit. Evolving the template is the right call — v2 is a guidance update, not a rewrite.

---

## Part 5: The Conceptual Migration

This is what you said matters most. The template's value is making the mental model smaller.

### The Old Model

```
You have a WORKSPACE that contains:
  ├── A Claude Code environment (.claude/)
  ├── A foundation layer (foundation/)
  ├── Documentation (docs/)
  └── An application (app/)
```

You think: "I'm managing a system. The app is one part of it."

### The New Model

```
You have a PROJECT that contains:
  ├── Your application (src/, package.json, configs — the repo root)
  ├── A Claude Code environment (.claude/)
  ├── A foundation layer (foundation/)
  └── Documentation (docs/)
```

You think: "I'm building an app. Claude helps me build it."

### Why the New Model Is Actually Simpler

The old model had an extra concept: the "workspace" that wraps everything. You had to think about:
- Where is the app relative to the workspace root?
- How do I tell the framework that it's in a subdirectory?
- How do I tell CI/CD where to find the app?
- How do I tell dev tools about the non-standard layout?

The new model removes that concept entirely. The app is the project. Everything else is infrastructure inside it. You never think about "where is the app" because the answer is always "here, at the root."

This is the same simplification that happened when version control moved from "a VCS that manages your project" (SVN with separate repository) to "version control embedded in your project" (.git/ directory). The tool became invisible infrastructure rather than a visible system.

### What You Need to Internalize

One thing: **the repo root is your app, not your workspace.**

That's it. Everything else follows:
- `npm run dev` works from the repo root (no `cd app/`)
- Framework configs use default paths (no `root` overrides)
- CI/CD uses default settings (no `rootDirectory`)
- `.claude/` is just another dotfile directory, like `.git/`
- `foundation/` and `docs/` are just directories in your project

### What Stays the Same (the Important Part)

- You still run `/work` and it decomposes, routes, and verifies
- You still run `/iterate` and it refines your spec
- The spec is still the source of truth
- Tasks still go through implement → verify cycles
- The dashboard still shows you what needs attention
- Session management still works (handoff, plan files, memory)
- Health-check still syncs template updates
- Everything in `.claude/` is identical

The workflow is the value. The layout was just scaffolding.

---

## Part 6: Concrete Next Steps

### Step A: Update the template (this repo) — ~1 hour

1. Update `system-overview.md` — note flat layout as default, update any subdirectory references
2. Update `known-issues.md` KI-001 — note that flat layout avoids this entirely
3. Add `session-management.md` to `sync-manifest.json`
4. Bump `version.json` to 2.0.0
5. Update `setup-checklist.md` — check that app is at repo root
6. Update `root-claude-md-template.md` Key Commands — standard framework commands
7. Clean up: delete `flat-layout-impact-analysis.md` and optionally archive DEC-003
8. Commit as a single "Template v2: flat layout default" commit

### Step B: For your next new project — 0 extra effort

1. Scaffold the framework first: `npx create-next-app my-project`
2. Copy `.claude/` into `my-project/`
3. Add `CLAUDE.md` at root
4. Start working. Everything just works.

### Step C: For existing projects — whenever you're ready

1. Check project state against the "When to Migrate" table above
2. If migrating: follow the per-project procedure in Part 2
3. If not migrating: keep using `--webpack`. Health-check will still sync template updates.

### Step D: Clean up this repo's temporary files — after you've decided

These root-level files are temporary analysis artifacts:
- `flat-layout-impact-analysis.md` — can delete after decision
- `decisions/decision-003-subdirectory-vs-flat-layout.md` — archive or keep as record
- `decisions/.archive/2026-04-02_subdirectory-vs-flat-layout.md` — keep as research reference
- `migration-plan-v2-flat-layout.md` — this file; keep until migration is done
