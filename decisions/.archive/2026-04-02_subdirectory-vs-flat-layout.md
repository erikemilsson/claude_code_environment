# Research Archive: Subdirectory vs. Flat Repo Layout (DEC-003)

**Date:** 2026-04-02
**Researcher:** research-agent
**Decision:** DEC-003 — Subdirectory vs. flat repo layout for projects using the template

---

## Research Questions and Findings

### Q1: How do other AI-assisted development environments handle project structure?

**Method:** Web search for configuration directory patterns across 7 AI coding tools.

**Findings:**

#### Cursor
- Uses `.cursor/rules/` directory at the project root (migrated from deprecated `.cursorrules` file in 2025)
- Also supports `.cursor/memory/` for persistent AI context
- Rules are `.mdc` files with activation modes (Always, Auto, Manual)
- The `.cursor/` directory is a peer of the project's source code, not a wrapper
- Sources: [Cursor AI Complete Guide 2025](https://medium.com/@hilalkara.dev/cursor-ai-complete-guide-2025-real-experiences-pro-tips-mcps-rules-context-engineering-6de1a776a8af), [Cursor Rules Configuration](https://cursor.document.top/en/tips/usage/set-rules/), [Complete Guide to .cursorignore](https://eastondev.com/blog/en/posts/dev/20260115-cursor-codebase-index-optimization/)

#### Windsurf
- Uses `.windsurf/rules/` directory at the project root
- Also supports `.windsurfrules` file at root
- Rule files are `.md` format, limited to 6000 characters each, 12000 total
- Supports hierarchical rule lookup: searches `.windsurf/rules/` in project root and parent directories up to git root
- Four activation modes: Manual, Always On, Model Decision, and one more
- Sources: [Windsurf Rules Directory](https://windsurf.com/editor/directory), [Cascade Memories](https://docs.windsurf.com/windsurf/cascade/memories), [Windsurf AI Rules Guide](https://uibakery.io/blog/windsurf-ai-rules)

#### GitHub Copilot
- Uses `.github/copilot-instructions.md` for project-level instructions
- Prompt files in `.github/prompts/`, chat modes in `.github/chatmodes/`
- Reuses the existing `.github/` convention rather than creating a new dotfile directory
- Workspace context includes all indexable files except `.gitignore`d ones
- Sources: [GitHub Docs: Custom Instructions](https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot), [Copilot Workspace Context](https://code.visualstudio.com/docs/copilot/reference/workspace-context), [Custom Prompts Structure](https://raffertyuy.com/raztype/ghcp-custom-prompts-structure/)

#### Devin
- Uses `.devin/wiki.json` at repo root for wiki generation customization
- Primary configuration is through web UI at app.devin.ai, not repo-level files
- Minimal in-repo footprint compared to other tools
- Sources: [Devin Docs: Repo Setup](https://docs.devin.ai/onboard-devin/repo-setup), [DeepWiki Docs](https://docs.devin.ai/work-with-devin/deepwiki)

#### OpenHands
- Uses `.openhands/microagents/` directory at project root
- Microagents are YAML files with specialized prompts for domain-specific knowledge
- Global config at `~/.openhands/`
- Sources: [OpenHands Local Setup](https://docs.openhands.dev/openhands/usage/run-openhands/local-setup), [OpenHands Configuration Issue](https://github.com/OpenHands/OpenHands/issues/3947)

#### Aider
- Uses `.aider.conf.yml` at repo root (and home directory)
- Additional dotfiles: `.aider.model.settings.yml`, `.aider.model.metadata.json`
- Three-level precedence: home directory < git repo root < current directory
- Sources: [Aider YAML Config](https://aider.chat/docs/config/aider_conf.html), [Aider Configuration](https://aider.chat/docs/config.html)

#### Claude Code (native)
- Uses `.claude/` directory at project root with `CLAUDE.md` at root
- Supports hierarchical `CLAUDE.md` (root, subdirectory, global)
- Directory contains commands/, agents/, settings.json
- Sources: [Claude Code .claude Directory](https://code.claude.com/docs/en/claude-directory), [Anatomy of .claude/ Folder](https://blog.dailydoseofds.com/p/anatomy-of-the-claude-folder)

**Conclusion:** Universal pattern is dotfiles/dotdirs at project root. Zero tools wrap the user's project in a subdirectory.

---

### Q2: Monorepo conventions (Turborepo, Nx, Lerna)

**Method:** Web search for monorepo directory structure conventions and comparison with the template's subdirectory layout.

**Findings:**

Standard Turborepo/Nx monorepo structure:
```
repo-root/
  apps/
    web/           # Framework app with own package.json
    admin/         # Another app
  packages/
    ui/            # Shared library
    config/        # Shared config
  turbo.json       # Workspace orchestrator
  package.json     # Root workspace config
  .cursor/         # AI tooling (dotfile at root)
  CLAUDE.md        # AI instructions (at root)
```

Key differences between monorepos and the template's subdirectory layout:
1. **Root purpose:** Monorepo root is a workspace orchestrator (turbo.json, nx.json). Template root is the Claude environment.
2. **App independence:** Monorepo apps have their own package.json and build independently. Template's `app/` is the only buildable unit.
3. **Tooling at root:** Monorepo root has workspace management tools. Template root has AI environment tools.
4. **AI tooling placement:** In monorepos, `.cursor/`, `CLAUDE.md`, etc. go at the *workspace root* alongside turbo.json — they're peers of the orchestrator, not above it.

**Conclusion:** The template's subdirectory layout superficially resembles monorepo patterns but lacks the workspace orchestrator that makes the pattern work. It gets the costs (path resolution issues, framework confusion) without the benefits (workspace management, shared dependencies, independent builds).

Sources: [Turborepo + Nx + Lerna 2026](https://dev.to/dataformathub/turborepo-nx-and-lerna-the-truth-about-monorepo-tooling-in-2026-71), [JavaScript Monorepos Guide 2025](https://jeffbruchado.com.br/en/blog/javascript-monorepos-turborepo-nx-2025), [Monorepo Architecture Guide 2025](https://feature-sliced.design/blog/frontend-monorepo-explained), [Turborepo Next.js Guide](https://turborepo.dev/docs/guides/frameworks/nextjs)

---

### Q3: Real benefits of subdirectory layout

**Method:** Web search for concrete cases where dotfile directories conflict with app tooling, and analysis of the separation-of-concerns argument.

**Findings:**

**Benefits confirmed:**
- Visual separation in file tree (`.claude/`, `docs/`, `foundation/` clearly separated from `app/src/`)
- Conceptually clean mental model: the project is more than just the app

**Benefits NOT confirmed:**
- No evidence found that `.claude/` at project root causes conflicts with any framework's build tooling
- Dotfiles/dotdirs are excluded by default from framework builds, IDE file trees (usually), and deployment artifacts
- Analogous tools (`.git/`, `.github/`, `.vscode/`, `.husky/`, `.cursor/`, `.windsurf/`) coexist at project root without issues in thousands of projects

**Costs documented:**
- See Q5 for framework-specific issues
- Path resolution complexity for CI/CD (need `rootDirectory` config on Vercel, Netlify, etc.)
- Developer onboarding friction: non-standard layout requires explanation

**Conclusion:** The separation-of-concerns benefit is real but aesthetic. The dotfile convention provides adequate separation through a different mechanism (visibility rather than hierarchy). No concrete tooling conflicts with `.claude/` at project root were found.

---

### Q4: Graduation scenario

**Method:** Analysis of file operations required to remove Claude Code environment under each layout.

**Findings:**

**Flat layout graduation:**
```bash
rm -rf .claude/ CLAUDE.md
# Done. Project is now a standard framework project.
```

**Subdirectory layout graduation:**
```bash
# Move all app files to root
mv app/* app/.* .
rmdir app/
# Remove Claude environment
rm -rf .claude/ CLAUDE.md docs/ foundation/
# Fix all imports, CI/CD paths, deploy configs
# Update any hardcoded paths in the codebase
```

**Adding to existing project:**

Flat layout: Copy `.claude/` directory and `CLAUDE.md` into the project root. Done.

Subdirectory layout: Restructure the entire existing project into an `app/` subdirectory, then add the Claude environment at root. This is a disruptive change to an existing project.

**Industry direction:** The `.uignore` convention (universal AI-tool ignore file) is emerging, suggesting the industry direction is toward AI tooling as removable dotfiles rather than structural reorganization.

Sources: [uignore for AI tools](https://dev.to/geekfarmer/uignore-a-gitignore-for-ai-coding-tools-3h7)

---

### Q5: Framework-specific constraints

**Method:** Web search for documented issues with subdirectory layouts across major web frameworks.

**Findings:**

#### Next.js (Turbopack)
- **Issue:** Turbopack expects the app at repo root. `turbopack.root` config exists but doesn't resolve all edge cases.
- **Documented bugs:** CSS resolution failures, path doubling with `outputFileTracingRoot`, "Next.js package not found" errors in monorepo setups.
- **Workaround:** `--webpack` flag, but Webpack is the deprecated path.
- **Severity:** High — active bugs, no complete workaround.
- Sources: [Turbopack monorepo issue #74731](https://github.com/vercel/next.js/issues/74731), [Path resolution issue #79335](https://github.com/vercel/next.js/issues/79335), [Path doubling issue #88579](https://github.com/vercel/next.js/issues/88579), [Turbopack config docs](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack)

#### Vite
- **Issue:** Defaults `root` to `process.cwd()`. Apps in subdirectories require explicit `root` and `publicDir` configuration.
- **Impact:** Affects all Vite-based frameworks.
- **Workaround:** Set `root: path.resolve(__dirname, 'your-subdirectory')` in vite.config.js.
- **Severity:** Medium — configurable but adds friction.
- Sources: [Vite Shared Options](https://vite.dev/config/shared-options), [Vite Subdirectory Guide](https://www.codegenes.net/blog/how-to-run-vite-server-if-index-html-file-is-not-in-the-root-directory/)

#### Remix
- **Issue:** "Cannot resolve asset path outside of root directory" when using Vite backend in monorepo.
- **Note:** Works fine without Vite (classic compiler).
- **Severity:** Medium-High.
- Sources: [Remix monorepo issue #7960](https://github.com/remix-run/remix/issues/7960), [Remix Vite monorepo issue #7927](https://github.com/remix-run/remix/issues/7927)

#### SvelteKit
- **Issue:** Module resolution uses cwd rather than project root. Configuration files (svelte.config.js, tsconfig.json) expected at repo root.
- **Multiple open issues** about monorepo compatibility.
- **Severity:** Medium.
- Sources: [SvelteKit monorepo issue #2973](https://github.com/sveltejs/kit/issues/2973), [SvelteKit Nx issue #12499](https://github.com/sveltejs/kit/issues/12499), [SvelteKit subdirectory issue #8858](https://github.com/sveltejs/kit/issues/8858)

#### Astro
- **Issue:** Build process bundles source under outDir, breaking source location expectations in nested structures. Monorepo hydration root issues.
- **Severity:** Medium.
- Sources: [Astro monorepo build issue #11392](https://github.com/withastro/astro/issues/11392), [Astro dev server issue #14319](https://github.com/sveltejs/kit/issues/14319), [Astro Vite dep issue #15221](https://github.com/withastro/astro/issues/15221)

#### Angular
- **Issue:** Generally works in monorepos via Nx. `angular.json` handles project roots explicitly.
- **Severity:** Low.

**Conclusion:** This is NOT a Next.js-specific problem. Every Vite-based framework has documented subdirectory issues. The trend is toward deeper integration with bundlers that assume repo root = project root, meaning subdirectory layouts will face more issues over time, not fewer.

---

## Next.js 16 AGENTS.md Convention (Notable Finding)

Next.js 16 introduced a significant convention: `create-next-app` now generates `AGENTS.md` at the project root. This file directs AI coding agents to bundled documentation at `node_modules/next/dist/docs/`.

Key details:
- AGENTS.md is read by Claude Code, Cursor, GitHub Copilot, and other agents automatically
- Marker comments (`<!-- BEGIN:nextjs-agent-rules -->` / `<!-- END:nextjs-agent-rules -->`) protect the Next.js-managed section
- Users can add custom instructions outside the markers
- Vercel evaluation: AGENTS.md achieved 100% pass rate on Next.js 16 API tasks (+47pp vs baseline)

**Implication for DEC-003:** Next.js (the most popular React framework, maintained by Vercel who also maintains Turborepo) has explicitly endorsed the flat layout where AI config lives at the project root alongside framework files. This is a strong signal about industry direction.

Sources: [Next.js AI Agents Guide](https://nextjs.org/docs/app/guides/ai-agents), [Next.js 16.2 AI Improvements](https://nextjs.org/blog/next-16-2-ai), [Building Next.js for an Agentic Future](https://nextjs.org/blog/agentic-future)

---

## Summary Table

| Research Question | Finding | Implication for DEC-003 |
|-------------------|---------|------------------------|
| AI tool conventions | All 7 tools use dotfiles at project root | Strongly favors Option B |
| Monorepo patterns | Template doesn't match monorepo architecture | Undermines Option A's conceptual basis |
| Subdirectory benefits | Aesthetic only; no tooling conflicts with dotfiles at root | Weakens Option A's main advantage |
| Graduation | Flat is trivially removable; subdirectory requires restructuring | Strongly favors Option B |
| Framework constraints | 6+ frameworks have subdirectory issues; none have dotfile-at-root issues | Strongly favors Option B |

**Overall assessment:** The evidence consistently and strongly favors Option B (flat layout). The subdirectory layout's one advantage (visual separation) is addressed by the dotfile convention that the entire industry has converged on.
