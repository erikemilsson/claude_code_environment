# Scenario 15: Tech Stack Discovery During Spec Creation

Verify that `/iterate` correctly identifies the project tech stack from existing files and adapts spec template sections accordingly.

## Context

A user applies the template to an existing codebase and runs `/iterate` for the first time. The project already has framework-specific config files but the spec and CLAUDE.md are still placeholder. `/iterate` should detect the stack and suggest filling in the relevant sections — not auto-fill them (suggest-only boundary).

## State

- Empty spec (`spec_v1.md` with placeholders)
- Project root contains: `package.json` (Next.js 15), `tsconfig.json`, `tailwind.config.ts`, `src/app/page.tsx`
- No CLAUDE.md "Technology Stack" section filled in
- No test framework configured (no vitest.config, no jest.config)

## Trace 15A: Stack detection from project files

- **Path:** `/iterate` Step 1 (project structure discovery)
- `/iterate` reads project root files to understand what exists
- Detects Next.js from `package.json` dependencies + `src/app/` directory (App Router)
- Detects TypeScript from `tsconfig.json`
- Detects Tailwind from `tailwind.config.ts`

### Expected

- `/iterate` reports detected stack: Next.js 15, TypeScript, Tailwind CSS
- Suggests pre-filling the Technology Stack section in CLAUDE.md
- Presents suggestion to user rather than editing CLAUDE.md directly

### Pass criteria

- [ ] Tech stack detection produces accurate results from file inspection
- [ ] Suggestions are presented to user, not auto-applied (suggest-only boundary respected)
- [ ] Detection covers framework (Next.js), language (TypeScript), and styling (Tailwind)

### Fail indicators

- `/iterate` ignores existing project files and treats it as greenfield
- CLAUDE.md Technology Stack section is edited directly without user approval
- Only partial detection (finds Next.js but misses Tailwind, or vice versa)

---

## Trace 15B: Missing test infrastructure flagged

- **Path:** `/iterate` Step 1 → test framework detection
- No `vitest.config.*`, `jest.config.*`, or `playwright.config.*` found
- No `test` script in `package.json`

### Expected

- `/iterate` notes that no testing framework is configured
- Asks about testing framework preference (Vitest vs Jest vs Playwright)
- Does NOT assume a testing framework if none is configured
- Flags this as a gap for the user to decide

### Pass criteria

- [ ] Missing test infrastructure is flagged, not silently ignored
- [ ] User is asked to choose a testing approach rather than having one assumed
- [ ] The gap is surfaced as a question, not treated as an error

### Fail indicators

- `/iterate` assumes Vitest/Jest without user input
- Missing test framework is not mentioned at all
- A test config file is created without user approval

---

## Trace 15C: Non-standard project (no package.json)

- **Alternate state:** Project root contains `pyproject.toml`, `src/main.py`, `requirements.txt`
- No JavaScript/TypeScript files

### Expected

- `/iterate` detects Python project from `pyproject.toml` and file extensions
- Checks `pyproject.toml` for `[tool.pytest.ini_options]` to detect test framework
- Checks `requirements.txt` for framework dependencies (Flask, Django, FastAPI, etc.)

### Pass criteria

- [ ] Detection works for non-JavaScript projects
- [ ] `pyproject.toml` sections are inspected for tool configuration
- [ ] Framework detection is language-agnostic, not hardcoded to Node.js

### Fail indicators

- Detection only works for JavaScript/TypeScript projects
- Python project files are ignored or misidentified
