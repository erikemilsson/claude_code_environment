# Permission Configuration Guide

*Version: 1.0 | Based on: Anthropic Claude Code Best Practices*

## Overview

Claude Code uses a permission system to balance safety with workflow efficiency. Understanding and configuring permissions properly enables smoother automation while maintaining appropriate safeguards.

## Permission System Basics

### Default Behavior
```markdown
BY DEFAULT, Claude Code will:
✅ Read files without prompting
✅ Search code without prompting
✅ Prompt for file writes/edits
✅ Prompt for bash commands
✅ Prompt for potentially destructive operations
```

### Permission Levels
```markdown
ALLOW: Execute without prompting
PROMPT: Ask user before executing (default for writes)
DENY: Block operation entirely
```

## Bootstrapped Environments (Vibe Coding Ready)

Projects created from this template system automatically include `.claude/settings.json` pre-configured for uninterrupted development workflows.

### Auto-Allowed Operations

**File writes** - Everything in `.claude/`:
- Tasks, context, reference, decisions, checkpoints, scratchpad

**Commands** - Common development operations:
- Git read-only (status, diff, log, branch, show)
- Tests (npm test, pytest, cargo test, go test, bun test, make test)
- Linting (eslint, prettier, mypy, ruff, clippy)
- Building (npm run build, cargo check, tsc --noEmit)
- Project scripts

### Still Requires Permission

- Source file writes (src/, tests/)
- Git commits and pushes
- Package installation
- Deployment commands

### Explicitly Denied

- `rm -rf`, `git push --force`, `git reset --hard`, `sudo`, publish commands

### Customizing

Extend `.claude/settings.json` for your project. Example for full trust:

```jsonc
{
  "permissions": {
    "file": {
      "allow_write": [
        ".claude/**/*",
        "src/**/*",
        "tests/**/*"
      ]
    }
  }
}
```

## Configuration Methods

### 1. Interactive Commands

```bash
# View current permissions
/permissions

# Add permission during session
/permissions add bash "npm test"
/permissions add bash "npm run build"

# Remove permission
/permissions remove bash "npm test"
```

### 2. Configuration File

```jsonc
// .claude/settings.json (project-level)
// or ~/.claude/settings.json (user-level)
{
  "permissions": {
    "bash": {
      "allow": [
        "npm test",
        "npm run build",
        "npm run lint",
        "git status",
        "git diff",
        "python -m pytest"
      ],
      "deny": [
        "rm -rf",
        "sudo *"
      ]
    },
    "file": {
      "allow_write": [
        "src/**/*.ts",
        "tests/**/*.ts",
        ".claude/**/*"
      ],
      "deny_write": [
        "*.env*",
        "*credentials*",
        "package-lock.json"
      ]
    }
  }
}
```

### 3. CLI Flags

```bash
# Skip all permission prompts (dangerous!)
claude --dangerously-skip-permissions

# Start with specific allowed commands
claude --allow-bash "npm test" --allow-bash "npm run build"
```

## Permission Profiles

### Development Profile (Balanced)

```jsonc
// Good for everyday development
{
  "permissions": {
    "bash": {
      "allow": [
        // Testing
        "npm test*",
        "pytest*",
        "go test*",

        // Building
        "npm run build",
        "npm run dev",
        "make build",

        // Linting
        "npm run lint*",
        "eslint*",
        "prettier*",

        // Git (read-only)
        "git status",
        "git diff*",
        "git log*",
        "git branch*",
        "git show*"
      ],
      "prompt": [
        // Git (write operations)
        "git commit*",
        "git push*",
        "git checkout*",
        "git merge*"
      ],
      "deny": [
        "git push --force*",
        "git reset --hard*",
        "rm -rf*"
      ]
    }
  }
}
```

### Automation Profile (CI/CD)

```jsonc
// For automated pipelines - use in isolated environments
{
  "permissions": {
    "bash": {
      "allow": [
        // Build and test
        "*test*",
        "*build*",
        "*lint*",

        // Analysis
        "*analyze*",
        "*report*",

        // No destructive operations
      ],
      "deny": [
        "rm *",
        "git push*",
        "*deploy*",
        "*delete*",
        "sudo *"
      ]
    },
    "file": {
      "allow_write": [
        "reports/**/*",
        "coverage/**/*",
        ".claude/scratchpad/**/*"
      ],
      "deny_write": [
        "src/**/*",
        "*.json",
        "*.lock"
      ]
    }
  }
}
```

### Restricted Profile (Review Only)

```jsonc
// For code review and analysis only
{
  "permissions": {
    "bash": {
      "allow": [
        "git status",
        "git diff*",
        "git log*",
        "cat *",
        "ls *"
      ],
      "deny": [
        "*"  // Deny everything else
      ]
    },
    "file": {
      "allow_write": [],  // No writes
      "deny_write": ["**/*"]
    }
  }
}
```

## Pattern Matching

### Wildcards
```markdown
PATTERNS:
- "npm test" - Exact match only
- "npm test*" - Starts with "npm test"
- "*test*" - Contains "test"
- "git *" - Any git command
- "src/**/*.ts" - TypeScript files in src/ tree
```

### Examples
```jsonc
{
  "bash": {
    "allow": [
      "npm *",           // All npm commands
      "git status",      // Exact command
      "python -m *",     // Python module execution
      "docker compose *" // Docker compose commands
    ]
  }
}
```

## Safe YOLO Mode

### What It Does
```markdown
--dangerously-skip-permissions:
- Skips ALL permission prompts
- Executes any bash command
- Writes any file
- Useful for automation in isolated environments
```

### Safety Requirements
```markdown
BEFORE USING YOLO MODE:

✅ Isolated environment (container/VM)
✅ No network access (or very limited)
✅ No access to production systems
✅ Disposable environment
✅ Source code is version controlled
✅ No sensitive credentials present
```

### Example Safe Setup
```bash
# Create isolated Docker container
docker run -it --rm \
  --network none \           # No network
  --read-only \              # Read-only root (mostly)
  --tmpfs /tmp \             # Writable tmp
  -v $(pwd):/workspace:rw \  # Only workspace is writable
  -w /workspace \
  claude-automation \
  claude --dangerously-skip-permissions -p "Fix all linting errors"
```

### Appropriate Use Cases
```markdown
SAFE FOR YOLO:
✅ Linting/formatting fixes
✅ Boilerplate generation
✅ Test scaffolding
✅ Documentation generation
✅ Code analysis/reporting

NOT SAFE FOR YOLO:
❌ Production deployments
❌ Database operations
❌ Credential handling
❌ Network operations
❌ Bulk file deletions
```

## Best Practices

### DO:
```markdown
✅ Start with restrictive permissions, expand as needed
✅ Use project-level settings for team consistency
✅ Allow test commands to speed up TDD workflow
✅ Use YOLO mode only in isolated environments
✅ Review permission patterns regularly
✅ Document why specific permissions are granted
```

### DON'T:
```markdown
❌ Use YOLO mode on production systems
❌ Allow "rm -rf" or similar destructive commands
❌ Grant broad permissions without review
❌ Allow credential file writes
❌ Skip permission prompts for git push/deploy
```

## Troubleshooting

### Permission Not Working
```markdown
CHECK:
1. Pattern syntax (wildcards, escaping)
2. File location (project vs user settings)
3. Reload after config changes
4. Conflicting deny rules (deny takes precedence)
```

### Too Many Prompts
```markdown
SOLUTIONS:
1. Add frequently-used commands to allow list
2. Use /permissions add during session
3. Create project-specific settings file
4. Consider if prompts are actually warranted
```

### Commands Still Blocked
```markdown
CHECK:
1. Deny patterns override allow patterns
2. Command might match a deny pattern
3. Try more specific allow pattern
4. Check both project and user settings
```

## Related Documentation

- `.claude/reference/headless-automation.md` - CI/CD automation patterns
- `.claude/reference/multi-claude-patterns.md` - Multi-instance coordination
- Claude Code documentation for full permission reference
