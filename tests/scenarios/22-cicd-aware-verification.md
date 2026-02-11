# Scenario 22: CI/CD-Aware Verification

Verify that verify-agent accounts for existing CI/CD pipelines when validating work.

## Context

Projects with CI/CD pipelines already have automated checks that run on push. The verify-agent should be aware of these: mirror the same commands locally for fast feedback, avoid duplicating CI-only checks (like multi-version matrix builds), and note that CI will provide additional validation on push.

## State

- Project has `.github/workflows/test.yml`:
  - Runs `pytest --cov` on push to main and PRs
  - Tests against Python 3.10, 3.11, 3.12 matrix
  - Runs `ruff check` for linting
- Project has `netlify.toml` with build command `pnpm build`
- verify-agent is validating a completed task that modified Python source files

## Trace 22A: CI config discovery

- **Path:** verify-agent → pre-verification environment scan
- verify-agent reads project root for CI/CD configuration files

### Expected

- verify-agent discovers `.github/workflows/test.yml` and `netlify.toml`
- Reads CI config to understand what checks exist
- Notes CI commands in verification context (knows what will run on push)

### Pass criteria

- [ ] CI/CD configuration files are discovered and read
- [ ] verify-agent understands what checks CI performs
- [ ] CI awareness is noted in verification output

### Fail indicators

- CI config files are ignored entirely
- verify-agent doesn't know what checks CI will perform
- No mention of CI in verification output

---

## Trace 22B: Local verification mirrors CI checks

- **Path:** verify-agent → test/lint execution
- CI runs `pytest --cov` and `ruff check`
- verify-agent chooses local verification commands

### Expected

- verify-agent runs `pytest` locally (matching CI's test command)
- verify-agent runs `ruff check` locally (matching CI's lint command)
- Local commands use the same configuration as CI
- Results are reported immediately (faster feedback than waiting for CI)

### Pass criteria

- [ ] Local verification commands match CI commands
- [ ] Same test configuration used locally and in CI
- [ ] Linting matches CI's linter and rules

### Fail indicators

- verify-agent runs different tests than CI would
- verify-agent uses a different linter than what CI configures
- Local verification produces different results than CI would

---

## Trace 22C: No redundant multi-environment testing

- **Path:** verify-agent → deciding what to run locally vs. defer to CI
- CI tests against Python 3.10, 3.11, 3.12 matrix
- Local environment has Python 3.11

### Expected

- verify-agent runs tests against the local Python version only
- Does NOT attempt to replicate the multi-version matrix locally
- Notes that CI will validate against other Python versions on push
- Reports which checks are local-only vs. CI-validated

### Pass criteria

- [ ] No redundant multi-environment testing locally
- [ ] Local verification runs against the available environment only
- [ ] CI's broader coverage is acknowledged, not duplicated
- [ ] Verification report distinguishes local checks from CI checks

### Fail indicators

- verify-agent tries to install multiple Python versions locally
- verify-agent skips testing because it can't replicate the full matrix
- No distinction between what was verified locally and what CI will verify
