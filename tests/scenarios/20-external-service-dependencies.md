# Scenario 20: External API/Service Dependencies in Task Decomposition

Verify that `/work` task decomposition correctly handles tasks that depend on external services (APIs, databases, cloud platforms).

## Context

Many real projects depend on external services — APIs requiring keys, databases requiring setup, cloud platforms requiring credentials. Task decomposition must identify these dependencies as prerequisites and surface missing configuration before implementation begins, rather than letting implement-agent fail at runtime.

## State

- Spec includes a feature requiring: PostgreSQL database, Gemini API, and Obsidian vault integration
- `.env.example` exists with `GEMINI_API_KEY`, `DATABASE_URL`, `OBSIDIAN_VAULT_PATH`
- No `.env` file present (not yet configured by user)
- Spec tasks involve: database schema migration, API integration, and file sync

## Trace 20A: Dependency identification during decomposition

- **Path:** `/work` Step 3 (task decomposition)
- Spec feature references external services in its description
- `.env.example` enumerates required environment variables

### Expected

- Task decomposition identifies external dependencies as prerequisites
- Environment setup task(s) created before feature implementation tasks
- Setup tasks are human-owned (user must provide credentials)
- Blocking relationships established: implementation tasks blocked by setup tasks

### Pass criteria

- [ ] External dependencies are identified during decomposition
- [ ] Setup/configuration tasks are created with appropriate blocking relationships
- [ ] Setup tasks are assigned to human owner (Claude can't create API keys)
- [ ] Implementation tasks depend on setup completion

### Fail indicators

- External dependencies are not mentioned in any task
- Implementation tasks are created without setup prerequisites
- Setup tasks are assigned to Claude (who can't obtain credentials)
- No blocking relationships between setup and implementation

---

## Trace 20B: Missing environment variables surfaced

- **Path:** `/work` → implement-agent attempts task that requires `.env`
- `.env` file does not exist
- `.env.example` lists required variables

### Expected

- implement-agent checks for `.env` or equivalent before attempting API calls
- Missing configuration is surfaced immediately, not discovered via runtime error
- Dashboard shows "needs configuration" in the attention section with specific variables listed

### Pass criteria

- [ ] Missing environment variables are surfaced, not silently ignored
- [ ] Dashboard attention section lists what needs to be configured
- [ ] Implement-agent does not attempt API calls without credentials

### Fail indicators

- implement-agent writes code that calls the API, then fails at runtime
- Missing `.env` is not detected until a test fails
- Dashboard shows no indication that configuration is incomplete

---

## Trace 20C: Partial configuration handling

- **Path:** `/work` → some but not all environment variables configured
- `.env` exists with `DATABASE_URL` set but `GEMINI_API_KEY` and `OBSIDIAN_VAULT_PATH` empty/missing

### Expected

- Tasks depending only on database are unblocked
- Tasks requiring Gemini API remain blocked with specific reason
- Dashboard shows granular status: which services are configured, which are not

### Pass criteria

- [ ] Partial configuration unblocks only the relevant tasks
- [ ] Still-missing variables are specifically named
- [ ] Dashboard reflects granular dependency status

### Fail indicators

- All tasks remain blocked because one variable is missing
- All tasks unblocked because `.env` file exists (regardless of contents)
- No distinction between configured and unconfigured services
