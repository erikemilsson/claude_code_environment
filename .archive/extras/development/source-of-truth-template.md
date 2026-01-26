# Source of Truth Document Template

Use this template to document the authoritative sources for your project.

---

# Source of Truth: [Project Name]

**Last Updated:** [Date]

## Document Hierarchy

```
1. CLAUDE.md                    # Project rules and conventions
   ├── .claude/context/overview.md  # Project context
   └── .claude/tasks/           # Current work
2. [Primary Source]             # e.g., API docs, regulatory docs
3. [Secondary Sources]          # Supporting documentation
```

## Primary Sources

### [Source Name]
- **What**: [What this document covers]
- **Location**: [URL or file path]
- **Version**: [Version number or date]
- **Authority Level**: Primary / Secondary / Reference
- **When to Reference**: [When Claude should consult this]

### [Another Source]
- **What**: [Description]
- **Location**: [URL or path]
- **Version**: [Version]
- **Authority Level**: [Level]
- **When to Reference**: [When to use]

## Data Sources

| Source | Type | Location | Refresh | Owner |
|--------|------|----------|---------|-------|
| [Name] | Database / API / File | [Location] | Daily / Weekly / Manual | [Who] |
| [Name] | [Type] | [Location] | [Frequency] | [Who] |

## Code References

### Primary Codebase
- **Repository**: [URL]
- **Branch**: [main / develop]
- **Key Paths**:
  - `/src/` - Source code
  - `/tests/` - Test files
  - `/docs/` - Documentation

### Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| [name] | [version] | [what it's used for] |

## Conflict Resolution

When sources conflict:

1. **CLAUDE.md** overrides all other documents
2. **Primary sources** override secondary sources
3. **More recent** versions override older versions
4. **When in doubt**: Ask user for clarification

## Update Process

1. Update the relevant source document
2. Update version/date in this file
3. Notify affected team members
4. Update any dependent documentation

## Notes

[Any additional context about source management]
