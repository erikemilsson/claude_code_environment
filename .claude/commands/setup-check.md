# Setup Check

Validate template configuration for new users.

## Usage
```
/setup-check
```

## Process

Run all checks and output a summary report. This helps new users ensure they've properly configured the template for their project.

### Checks to Perform

1. **`.claude/CLAUDE.md` customization**
   - Check for `[bracketed text]` placeholders
   - Look for template markers like "DELETE EVERYTHING ABOVE"
   - ✓ Pass: No placeholders found
   - ⚠ Warn: Placeholders remain

2. **version.json configuration**
   - Check if `template_repo` still points to original template
   - ✓ Pass: Updated to user's fork/repo
   - ⚠ Warn: Still points to template repo

3. **Specification file exists**
   - Check if `.claude/spec_v1.md` (or higher version) exists
   - Check for placeholder content like "[Brief description", "YYYY-MM-DD"
   - ✓ Pass: Spec file has real content
   - ⚠ Warn: Spec missing or contains placeholder text

4. **Specification readiness** (gate for `/work`)
   - Assess against readiness criteria from `.claude/support/reference/spec-checklist.md`
   - Check for red flags: `[TBD]`, vague statements, missing sections
   - ✓ Pass: Spec is ready for `/work`
   - ⚠ Warn: Spec needs more detail
   - ✗ Fail: Major gaps - run `/iterate`

5. **README.md customization**
   - Check for template boilerplate
   - ✓ Pass: README appears customized
   - ⚠ Warn: README still contains template text

6. **settings.local.json paths**
   - Verify paths in permissions match current directory
   - ✓ Pass: Paths are correct
   - ⚠ Warn: Paths need updating

7. **.gitignore configuration**
   - Check standard entries exist
   - ✓ Pass: Properly configured
   - ⚠ Warn: Missing recommended entries

## Output Format

```markdown
## Setup Validation

### Results

✓ .claude/CLAUDE.md customized
✓ version.json configured
✓ Spec file exists
⚠ Spec readiness: needs more detail
  → Missing acceptance criteria
  → Run /iterate
✓ README.md customized
✓ settings.local.json paths correct
✓ .gitignore configured

### Summary

6/7 checks passed
1 warning to address

**Ready for /work:** No ← Spec not ready

### Next Steps

1. Run /iterate to improve spec readiness
```

## Check Details

### `.claude/CLAUDE.md` Placeholders

Look for these patterns:
- `[bracketed text]` - unfilled placeholders
- `<!-- DELETE EVERYTHING` - template markers
- `## Maintaining This Template` - template-specific section

### version.json

Check the `template_repo` field:
```json
{
  "template_repo": "https://github.com/USER/REPO"
}
```

Should point to the environment builder template repo (or your fork of it). Used by `/update-template` to compare against template updates. The project's own repo is determined from `git remote`.

### Spec File

The spec should exist at `.claude/spec_v1.md` (or higher version).
Should not contain placeholder patterns like:
- `[Brief description`
- `[Your project`
- `YYYY-MM-DD`

### Spec Readiness

Assess the spec against readiness criteria (see `.claude/support/reference/spec-checklist.md`):

**Must have for "Ready":**
- Problem and users are clear
- Core components/architecture decided
- Has testable acceptance criteria
- Remaining questions are implementation details (not blockers)

**Red flags (cause warning/fail):**
- Placeholder text: `[TBD]`, `[describe here]`, `YYYY-MM-DD`
- Vague statements: "make it better", "should be fast"
- Requirements that are really tasks: "add login button"
- Missing sections: no acceptance criteria, no scope definition
- Unresolved blocking questions

**Output guidance:**
- ✓ Pass: All core criteria met, no red flags
- ⚠ Warn: Some criteria met but gaps remain (list specific gaps)
- ✗ Fail: Major gaps - can't explain what it does or no acceptance criteria

### settings.local.json

Verify the working directory in permission paths matches the actual project path. Look for hardcoded paths that might be from the template user's machine.

## When to Run

- After cloning the template for a new project
- **Before running `/work`** - this is the readiness gate
- When onboarding new team members
- After updating from template (to check for new required config)

## Relationship to /work

`/setup-check` is the gate before `/work`. The workflow is:

1. Create spec: Run `/iterate`
2. Configure project: Fix `.claude/CLAUDE.md`, version.json, README.md
3. Validate: `/setup-check` → all green
4. Build: `/work`

If `/setup-check` shows spec readiness warnings, run `/iterate` until the spec is ready.
