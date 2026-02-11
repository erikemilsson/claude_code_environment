# Scenario 19: Nested/Monorepo Project Structure

Verify that `/work` and agents correctly handle projects where code lives in a subdirectory, not the repository root.

## Context

Real-world repositories often have a nested structure: the repo root contains documentation, config, and `.claude/`, while the actual application lives in a subdirectory (`app/`, `packages/client/`, etc.). Agents must discover where code lives and run commands from the correct working directory.

## State

- Repository root contains: `CLAUDE.md`, `.claude/`, `README.md`
- All source code lives in `budget-app/`:
  - `budget-app/package.json` (Next.js 15, TypeScript)
  - `budget-app/src/app/page.tsx`
  - `budget-app/src/components/`
  - `budget-app/node_modules/`
  - `budget-app/tsconfig.json`
- Spec references components like "the home screen" → `budget-app/src/app/page.tsx`
- Task-1: "Add expense tracking form to the home screen"
- No `package.json` at repo root

## Trace 19A: Implement-agent finds source files in subdirectory

- **Path:** `/work` → implement-agent dispatched for Task-1
- Task references "the home screen" which lives at `budget-app/src/app/page.tsx`

### Expected

- implement-agent locates source files inside `budget-app/src/`, not at repo root
- New files are created within `budget-app/src/components/`, not at root `src/`
- Import paths in new/modified files use correct relative paths within `budget-app/`

### Pass criteria

- [ ] Agent does not create files at repo root when they belong in the subdirectory
- [ ] Source file discovery correctly identifies `budget-app/` as the application root
- [ ] Import paths are correct relative to the subdirectory structure

### Fail indicators

- Agent creates `src/components/ExpenseForm.tsx` at repo root
- Agent can't find `page.tsx` because it only searches the repo root
- Import paths are broken because they're relative to the wrong root

---

## Trace 19B: Build and test commands run from correct directory

- **Path:** verify-agent → build/test execution after Task-1 implementation
- `package.json` with `build` and `test` scripts lives in `budget-app/`
- No `package.json` at repo root

### Expected

- verify-agent runs `npm run build` from `budget-app/` (where `package.json` lives)
- Test commands execute from the correct subdirectory
- Build output references correct paths

### Pass criteria

- [ ] Build commands execute in the correct working directory (`budget-app/`)
- [ ] `npm run build` does not fail with "no package.json found"
- [ ] Test execution uses the subdirectory's test configuration

### Fail indicators

- verify-agent runs `npm run build` from repo root and fails
- Agent attempts to create a `package.json` at repo root
- Build succeeds but tests run against wrong directory

---

## Trace 19C: Dashboard file references use full paths

- **Path:** dashboard.md regeneration with task details
- Task-1 modified `budget-app/src/app/page.tsx`

### Expected

- Dashboard file references use paths relative to repo root: `budget-app/src/app/page.tsx`
- Not truncated to just `src/app/page.tsx` (ambiguous if multiple apps exist)
- Links and references are navigable from the repo root

### Pass criteria

- [ ] Dashboard file references use paths relative to repo root
- [ ] File paths are unambiguous and navigable
- [ ] No confusion between repo-level config and app-level config

### Fail indicators

- File paths shown without the `budget-app/` prefix
- Dashboard references files that don't exist at the listed path
- Mixed path conventions (some from root, some from subdirectory)
