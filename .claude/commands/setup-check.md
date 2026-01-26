# Setup Check

Validate template configuration for new users.

## Usage
```
/setup-check
```

## Process

Run all checks and output a summary report. This helps new users ensure they've properly configured the template for their project.

### Checks to Perform

1. **CLAUDE.md customization**
   - Check for `[bracketed text]` placeholders
   - Look for template markers like "DELETE EVERYTHING ABOVE"
   - ✓ Pass: No placeholders found
   - ⚠ Warn: Placeholders remain

2. **version.json configuration**
   - Check if `source_repo` still points to template
   - ✓ Pass: Updated to user's fork/repo
   - ⚠ Warn: Still points to template repo

3. **Specification file**
   - Check if `.claude/spec_v1.md` exists
   - Check for placeholder content like "[Brief description"
   - ✓ Pass: Spec file has real content
   - ⚠ Warn: Spec missing or contains placeholder text

4. **README.md customization**
   - Check for template boilerplate
   - ✓ Pass: README appears customized
   - ⚠ Warn: README still contains template text

5. **settings.local.json paths**
   - Verify paths in permissions match current directory
   - ✓ Pass: Paths are correct
   - ⚠ Warn: Paths need updating

6. **.gitignore configuration**
   - Check standard entries exist
   - ✓ Pass: Properly configured
   - ⚠ Warn: Missing recommended entries

## Output Format

```markdown
## Setup Validation

### Results

✓ CLAUDE.md customized
✓ .gitignore configured
⚠ version.json source_repo still points to template
  → Update to your fork URL
⚠ spec_v1.md contains placeholder text
  → Run specification_creator to create your spec
✓ README.md customized
✓ settings.local.json paths correct

### Summary

5/6 checks passed
2 warnings to address

### Next Steps

1. Update version.json with your repository URL
2. Create your project specification using specification_creator/
```

## Check Details

### CLAUDE.md Placeholders

Look for these patterns:
- `[bracketed text]` - unfilled placeholders
- `<!-- DELETE EVERYTHING` - template markers
- `## Maintaining This Template` - template-specific section

### version.json

Check the `source_repo` field:
```json
{
  "source_repo": "https://github.com/USER/REPO"
}
```

Should NOT still contain the original template URL (check if it matches the URL in the template's own version.json, or contains placeholder text like "YOUR-USERNAME" or "TEMPLATE").

### Spec File

The spec should exist at `.claude/spec_v1.md` (or higher version).
Should not contain placeholder patterns like:
- `[Brief description`
- `[Your project`
- `TBD`

### settings.local.json

Verify the working directory in permission paths matches the actual project path. Look for hardcoded paths that might be from the template user's machine.

## When to Run

- After cloning the template for a new project
- Before starting actual development work
- When onboarding new team members
- After updating from template (to check for new required config)
