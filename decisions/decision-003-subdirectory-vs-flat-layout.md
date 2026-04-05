---
id: DEC-003
title: Subdirectory vs. flat repo layout for projects using the template
status: approved
category: architecture
created: 2026-04-02
decided: 2026-04-05
related:
  tasks: []
  decisions: []
  feedback: [FB-003]
implementation_anchors: []
inflection_point: true
spec_revised:
spec_revised_date:
blocks: []
---

# Subdirectory vs. flat repo layout for projects using the template

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Subdirectory layout (current)
- [x] Option B: Flat layout
- [ ] Option C: Guided choice during project setup

*Check one box above, then fill in the Decision section below.*

---

## Context

The template currently establishes a project structure where the app lives in a subdirectory (e.g., `app/`) with `.claude/`, `foundation/`, and `docs/` as siblings at the repo root. This is architecturally clean — the app is one component of a larger system that includes the Claude Code environment.

However, this layout triggers tooling issues (Turbopack CSS resolution failure in Next.js 16, documented in KI-001) and is non-standard for most web frameworks that expect to own the repo root. The workaround (`--webpack`) works but is a band-aid.

The broader question: when Claude Code coexists with the deployed app in the same repo, what's the right directory structure?

## Questions to Research

1. **How do other AI-assisted development environments handle this?** (Cursor, Windsurf, Copilot Workspace, Devin) — do they assume they own the repo root, or do they nest in a subdirectory?
2. **What's the standard monorepo practice** for projects where tooling config lives alongside the app? (e.g., Turborepo, Nx, Lerna patterns)
3. **Does the subdirectory layout provide real benefits** beyond aesthetic separation? Are there concrete cases where `.claude/` at the repo root conflicts with the app's tooling?
4. **What happens when projects "graduate"** — when the user wants to deploy the app without the Claude Code environment? Is a flat layout easier to extract from?
5. **Framework-specific constraints** — which frameworks (Next.js, Vite, Remix, etc.) have issues with subdirectory layouts? Is this a Next.js-specific problem or a broader pattern?

## Research Findings

### Q1: How do other AI-assisted development environments handle this?

**Every major AI coding tool uses a dotfile directory at the project root.** None of them assume they own the repo root or push the user's app into a subdirectory.

| Tool | Configuration Location | Pattern |
|------|----------------------|---------|
| **Claude Code** | `.claude/` dir + `CLAUDE.md` at project root | Dotfile dir at root |
| **Cursor** | `.cursor/rules/` dir at project root (deprecated: `.cursorrules` file) | Dotfile dir at root |
| **Windsurf** | `.windsurf/rules/` dir at project root (also `.windsurfrules` file) | Dotfile dir at root |
| **GitHub Copilot** | `.github/copilot-instructions.md` + `.github/prompts/` | Dotfile dir at root (reuses `.github/`) |
| **Devin** | `.devin/wiki.json` at repo root; config via web UI | Dotfile at root (minimal) |
| **OpenHands** | `.openhands/microagents/` dir at repo root | Dotfile dir at root |
| **Aider** | `.aider.conf.yml` + `.aider.model.settings.yml` at repo/home root | Dotfiles at root |

**Key insight:** The universal convention is that AI tooling lives *inside* the user's project as dotfiles, not the other way around. No tool creates a wrapper structure where the app is nested inside the AI environment. The AI environment is always a guest in the project, not the host.

This is directly analogous to how `.git/`, `.github/`, `.vscode/`, `.idea/`, and `.husky/` all work — they are invisible infrastructure that coexists with the project rather than reorganizing it.

**Next.js 16 has embraced this pattern explicitly.** `create-next-app` now generates `AGENTS.md` and `CLAUDE.md` at the project root automatically, alongside the framework's own files. Vercel's AI agent guide assumes the flat layout where AI config files are siblings of `next.config.js`, `package.json`, etc.

### Q2: What's the standard monorepo practice?

Monorepo tools (Turborepo, Nx, Lerna) use a well-established pattern:

```
repo-root/
  apps/
    web/          ← Next.js app with its own package.json
    admin/        ← Another app
  packages/
    ui/           ← Shared library
    config/       ← Shared config
  turbo.json      ← Orchestrator config at root
  package.json    ← Root workspace config
```

**Critical distinction:** In a Turborepo/Nx monorepo, the root is a *workspace orchestrator*, not an app wrapper. Each app in `apps/` has its own `package.json`, its own framework config, and its own build pipeline. The root-level config is for the *workspace manager* (turbo.json, nx.json), not for any individual app.

**This is fundamentally different from the template's current subdirectory layout.** The template puts the app in a subdirectory but the root is not a workspace orchestrator — it's the Claude Code environment. There's no `turbo.json` or workspace manager at the root, so the pattern doesn't map onto established monorepo conventions. The root has `.claude/`, `docs/`, `foundation/` — environment files, not workspace infrastructure.

**When monorepos do include AI tooling**, the AI dotfiles go at the workspace root alongside the orchestrator config — `.cursor/rules/`, `CLAUDE.md`, `.github/copilot-instructions.md` all live at the same level as `turbo.json`. They don't get their own wrapper directory.

### Q3: Does the subdirectory layout provide real benefits?

**Aesthetic separation is real but comes at a concrete cost.** Research found the following:

**Benefits of subdirectory layout (confirmed):**
- Visually clear that the app is one component of a larger system
- Multiple apps can coexist naturally (though this is the monorepo pattern, which has its own tooling)
- `.claude/` files don't appear in the app's directory listing

**Costs of subdirectory layout (documented):**
- **Turbopack resolution failures** — Next.js Turbopack expects the app at the repo root. The `turbopack.root` config option exists but adds configuration complexity and doesn't resolve all edge cases (CSS resolution, PostCSS config discovery).
- **Vite root mismatch** — Vite defaults `root` to `process.cwd()`. Apps in subdirectories require explicit `root` configuration in `vite.config.js` plus `publicDir` adjustments.
- **Remix asset path resolution** — Remix with Vite in monorepos encounters "Cannot resolve asset path outside of root directory" errors.
- **SvelteKit module resolution** — File resolutions are made from cwd rather than the project root, breaking in subdirectory layouts.
- **Astro build path issues** — Monorepo source code relocation can break Astro's build process expectations.
- **CI/CD path complexity** — Deploy tools (Vercel, Netlify, etc.) need `rootDirectory` or similar config to point to the subdirectory, adding setup friction.

**No concrete cases were found where `.claude/` at the repo root conflicts with any app's tooling.** Dotfile directories are conventionally ignored by frameworks, bundlers, and linters. `.claude/` is invisible to `next build`, `vite build`, `astro build`, etc. because:
1. Dotfiles/directories are excluded by default in most tool configurations
2. Framework entry points (`src/`, `app/`, `pages/`) are explicitly configured
3. `.gitignore`-style patterns already handle dotfile exclusion

### Q4: What happens when projects "graduate"?

**Flat layout is strictly easier for graduation.** When the user wants to deploy the app without the Claude Code environment:

| Action | Flat Layout | Subdirectory Layout |
|--------|------------|-------------------|
| Remove Claude env | `rm -rf .claude/ CLAUDE.md` | Move app contents to root, update all imports, fix CI/CD paths |
| Deploy without Claude | Already standard structure | Must either deploy from subdirectory or restructure |
| Add to existing project | Copy `.claude/` in, add `CLAUDE.md` | Restructure entire project into subdirectory |
| Version control cleanup | `.claude/` in `.gitignore` or delete | Requires repo reorganization |

**The "graduation" scenario heavily favors flat layout.** The `.uignore` convention (a universal AI-tool ignore file, analogous to `.gitignore`) is emerging to let projects exclude AI tooling from context without removing it. This suggests the industry direction is toward AI tooling as removable dotfiles, not structural reorganization.

### Q5: Framework-specific constraints

| Framework | Subdirectory Issues | Severity |
|-----------|-------------------|----------|
| **Next.js (Turbopack)** | `turbopack.root` required; CSS/PostCSS resolution failures; path doubling with `outputFileTracingRoot` | High — active bugs |
| **Next.js (Webpack)** | Works with `--webpack` flag but Webpack is deprecated path | Medium — workaround exists |
| **Vite** | Requires explicit `root` config; `publicDir` adjustment; dev server allow-list issues with symlinks | Medium |
| **Remix** | "Cannot resolve asset path outside of root directory" with Vite backend | Medium-High |
| **SvelteKit** | Module resolution from cwd not project root; monorepo compatibility issues | Medium |
| **Astro** | Build path expectations broken in nested structures; monorepo hydration root issues | Medium |
| **Angular** | Generally works in monorepos via Nx; angular.json handles project roots | Low |

**This is not a Next.js-specific problem.** Every Vite-based framework (Remix, SvelteKit, Astro) has documented issues with subdirectory layouts because Vite itself defaults to `process.cwd()` as the project root. While configuration options exist, they add complexity and don't always fully resolve edge cases.

**The trend is toward more issues, not fewer.** As frameworks adopt newer bundlers (Turbopack, Vite), the assumption that the app owns the repo root becomes more deeply embedded in the toolchain.

## Options

### Option A: Subdirectory layout (current)

App lives in `app/` (or similar), Claude Code environment at repo root.

**Pros:**
- Clean separation of concerns — app is one component, not the whole repo
- `.claude/` doesn't pollute the app's directory
- Multiple apps could coexist (e.g., `app/`, `admin/`, `api/`)

**Cons:**
- Triggers Turbopack bug in Next.js 16 (KI-001)
- Non-standard for most web frameworks — no other AI tool uses this pattern
- Every Vite-based framework (Remix, SvelteKit, Astro) has documented issues with subdirectory layouts
- Framework tooling (dev servers, bundlers, linters) assume repo root = project root
- More complex path resolution for CI/CD
- Does not match the monorepo pattern (no workspace orchestrator at root)
- Graduation requires project restructuring

**Evidence:** Zero of 7 surveyed AI coding tools use this pattern. Turborepo/Nx monorepos do use subdirectories, but with a workspace orchestrator at root — a fundamentally different architecture.

### Option B: Flat layout

App owns the repo root. `.claude/` is a dotfile directory within the app.

**Pros:**
- Standard framework layout — matches every surveyed AI tool's convention
- No Turbopack, Vite, or bundler issues
- Simpler CI/CD configuration (no `rootDirectory` overrides)
- Easiest graduation — `rm -rf .claude/ CLAUDE.md` leaves a standard project
- Matches Next.js 16's own convention (`create-next-app` generates `CLAUDE.md` at project root)
- `.claude/` as a dotfile is conventionally hidden in file explorers and ignored by build tools

**Cons:**
- `.claude/` mixed into the app's directory tree (though dotfiles are conventionally hidden)
- No clear visual separation between "Claude's environment" and "the project"
- Harder to support multiple apps in one repo (but that's the monorepo pattern's job)

**Evidence:** All 7 surveyed AI tools use this pattern. Next.js 16 `create-next-app` generates AI config files at project root. Dotfiles are the universal convention for development tooling (`.git/`, `.github/`, `.vscode/`, `.husky/`, `.cursor/`, `.windsurf/`).

### Option C: Guided choice during project setup

Template asks during `/iterate distill` which layout to use, based on the project's needs.

**Pros:**
- Adapts to the specific project and framework
- Can recommend based on known issues (e.g., Next.js -> flat)
- User makes an informed choice upfront

**Cons:**
- More complexity in the template — two layout paths to maintain and test
- Decision fatigue during project setup
- Research shows one layout is strictly better for framework compatibility; offering the choice implies parity where there is none
- The subdirectory option would still carry all of Option A's documented issues

**Evidence:** No surveyed AI tool offers this choice. The convention is strongly settled: dotfiles at project root.

## Comparison Matrix

| Factor | A: Subdirectory | B: Flat | C: Guided |
|--------|:-:|:-:|:-:|
| Framework compatibility | ✗ Documented issues with 6+ frameworks | ✓ Standard | ✓ Adapts (but one path still broken) |
| Industry convention | ✗ No AI tool uses this | ✓ Universal pattern | ⚠️ Implies false parity |
| Separation of concerns | ✓ Clean visual separation | ⚠️ Mixed (but dotfiles are hidden) | Depends on choice |
| CI/CD simplicity | ⚠️ Requires rootDirectory config | ✓ Standard | Depends on choice |
| Multi-app support | ✓ Natural | ✗ Requires monorepo tooling | Depends on choice |
| Template maintenance | ✓ One path | ✓ One path | ✗ Two paths |
| User experience | ✗ Non-obvious tooling issues | ✓ Familiar to all developers | ⚠️ Extra decision upfront |
| Graduation ease | ✗ Requires restructuring | ✓ Delete dotfiles | Depends on choice |
| Next.js 16 alignment | ✗ Contradicts create-next-app conventions | ✓ Matches create-next-app | Depends on choice |

## Recommendation

**The research strongly favors Option B (flat layout).** The evidence is consistent across all five research questions:

1. **Industry consensus:** Every surveyed AI coding tool (Cursor, Windsurf, GitHub Copilot, Devin, OpenHands, Aider, Claude Code itself) places its configuration as dotfiles at the project root. None wrap the user's app in a subdirectory.

2. **Framework compatibility:** The subdirectory layout has documented issues with Next.js (Turbopack), Vite, Remix, SvelteKit, and Astro. The flat layout has zero known framework conflicts.

3. **Trend direction:** Next.js 16's `create-next-app` now generates `AGENTS.md` and `CLAUDE.md` at the project root, cementing the dotfile-at-root convention. Frameworks are building *toward* this pattern, not away from it.

4. **Graduation:** Flat layout makes it trivial to remove the Claude Code environment. Subdirectory layout requires project restructuring.

5. **Monorepo misalignment:** The current subdirectory layout superficially resembles a monorepo but lacks the workspace orchestrator that makes monorepos work. It gets the costs (path resolution issues) without the benefits (workspace management, shared dependencies).

The one advantage of subdirectory layout — visual separation — is adequately addressed by the dotfile convention. `.claude/` is invisible in most file explorers by default, just as `.git/`, `.vscode/`, and `.cursor/` are.

**Option C adds complexity without clear benefit.** Since the research shows one layout is strictly superior for framework compatibility, offering the choice implies a parity that doesn't exist and creates maintenance burden.

## Decision

*To be filled by the decision-maker after reviewing the research above.*

## Notes

- This is marked as an inflection point because the layout choice affects how every template feature (agents, verification, dev server management) interacts with the project's build tooling.
- KI-001 (Turbopack workaround) provides a band-aid for Option A, but doesn't resolve the underlying architectural question.
- Research conducted 2026-04-02. Full research archive: `decisions/.archive/2026-04-02_subdirectory-vs-flat-layout.md`
- If Option B is selected, the template migration would involve: moving app files to repo root, updating all path references in commands/agents/rules, updating the archiving rules, and updating documentation. The `.claude/` directory itself requires no changes — it already lives at the project root.
