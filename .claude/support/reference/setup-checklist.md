# Setup Checklist

> **Read once during first decomposition.** `/work` runs these checks when decomposing a spec into tasks for the first time. Advisory only — warnings are reported but do not block decomposition.

## Checks

### 1. `.claude/CLAUDE.md` Customization

Look for unfilled template placeholders:
- `[bracketed text]` — unfilled placeholders
- `<!-- DELETE EVERYTHING` — template markers
- `## Maintaining This Template` — template-specific section

✓ Pass: No placeholders found
⚠ Warn: Placeholders remain — list which ones

### 2. `version.json` Configuration

Check that `.claude/version.json` exists and has a `template_repo` field pointing to the upstream template repository:
```json
{
  "template_repo": "https://github.com/TEMPLATE-OWNER/TEMPLATE-REPO"
}
```

This is the source repo for template sync (`/health-check` Part 5). It should point to the template origin, not the user's project repo.

✓ Pass: File exists with a `template_repo` value
⚠ Warn: File missing or `template_repo` is empty

### 3. `settings.local.json` Paths

Verify paths in permission settings match the current project directory. Look for hardcoded paths from a different machine.

✓ Pass: Paths are correct
⚠ Warn: Paths reference a different directory

### 4. `.gitignore` Configuration

Check standard entries exist for the project type.

✓ Pass: Properly configured
⚠ Warn: Missing recommended entries

## Output

Report results inline during decomposition as a brief summary block:

```
Setup check (first decomposition):
  ✓ CLAUDE.md customized
  ✓ version.json configured
  ⚠ settings.local.json — paths reference /Users/old-user/...
  ✓ .gitignore configured
```

Continue with decomposition regardless of warnings.
