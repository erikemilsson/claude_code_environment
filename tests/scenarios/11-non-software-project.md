# Scenario 11: Non-Software Specification Project

Verify that the template works for a project where the deliverable is a specification document, not runnable code.

## Context

Not all projects produce code. Some produce specifications, research documents, data analyses, or Markdown knowledge bases. The template's implement → verify cycle must adapt: implement-agent writes documentation, verify-agent validates document completeness and internal consistency rather than running builds or tests.

## State

- Spec describes a "knowledge base system specification" with sections for architecture, security model, and API design
- Tasks decomposed from spec are all documentation tasks:
  - Task-1: "Write security threat model" (Markdown deliverable)
  - Task-2: "Define API schema" (OpenAPI YAML + prose description)
  - Task-3: "Create test scenarios" (Markdown test plan, not code)
- No `src/`, no `package.json`, no `pyproject.toml`, no build tools
- No test framework configured

## Trace 11A: Implement-agent adapts to documentation deliverables

- **Path:** `/work` dispatches implement-agent for a documentation task
- Task-1 deliverable is a Markdown document (`docs/security-threat-model.md`)
- No code to write, compile, or lint

### Expected

- implement-agent writes Markdown documentation, not code
- File is placed in a reasonable location (per spec or project convention)
- Agent does not attempt to create source code files or test stubs
- Document follows any structure guidelines from the spec

### Pass criteria

- [ ] implement-agent produces documentation-appropriate output
- [ ] No phantom source code files are created
- [ ] Deliverable location matches spec expectations

### Fail indicators

- implement-agent creates `src/` directory or code stubs for a docs-only task
- Agent errors out because it can't find a build system
- Documentation is placed in an unexpected location

---

## Trace 11B: Verify-agent validates documents, not builds

- **Path:** verify-agent invoked after implement-agent completes a documentation task
- No test suite exists. No build system exists. Deliverable is a Markdown file.

### Expected

- verify-agent validates document completeness (all required sections present)
- Checks internal consistency (e.g., referenced components exist in other docs)
- Does NOT attempt to run `npm test`, `pytest`, `make`, or any build/test commands
- Verification output describes document quality, not test results

### Pass criteria

- [ ] verify-agent does not attempt to run non-existent tests or builds
- [ ] Verification covers document completeness and consistency
- [ ] Verification output uses documentation-appropriate language

### Fail indicators

- verify-agent errors out looking for a test framework
- Verification is skipped entirely because no tests exist
- verify-agent creates test stubs for a documentation project

---

## Trace 11C: Dashboard language adapts to project type

- **Path:** dashboard regeneration after task progress
- 1 of 3 tasks complete, 2 pending

### Expected

- Dashboard shows documentation-appropriate progress language
- No references to "build passing", "test coverage", or "lint status"
- Progress metrics reference deliverables completed, not code metrics
- Attention section references documents to review, not PRs to merge

### Pass criteria

- [ ] Dashboard language is appropriate for non-code projects
- [ ] Progress tracking works without code-specific metrics
- [ ] Task completion criteria make sense for documentation tasks

### Fail indicators

- Dashboard shows "Build: N/A" or "Tests: N/A" instead of omitting those sections
- Progress is reported in code-centric terms (lines of code, test coverage %)
- Empty code-specific sections clutter the dashboard
