# Pattern: Create File

## Metadata
- **ID**: pattern-file-create
- **Version**: 1.0.0
- **Category**: file-operations
- **Difficulty Range**: 1-3 (simple file creation tasks)

## Triggers
Keywords that suggest this pattern applies:
- create file
- new file
- generate file
- write file
- initialize

File types: All text-based files (.py, .md, .json, .txt, .m, .dax, .sql, etc.)

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_path | string | yes | Full path where file should be created |
| file_type | string | yes | Type/extension of file (.py, .md, etc.) |
| file_purpose | string | yes | What this file is for (used in header comment) |
| author | string | no | Author name for header (default: "Claude Code") |
| include_header | boolean | no | Whether to include header comment (default: true) |
| initial_content | string | no | Any initial content besides header |

## Pre-Conditions
- [ ] Parent directory exists or will be created
- [ ] File does not already exist (or overwrite is intentional)
- [ ] File path follows project naming conventions
- [ ] Permissions allow file creation

## Template

```
{{#if include_header}}
{{header_comment_start}}
{{file_purpose}}

Created: {{timestamp}}
{{#if author}}
Author: {{author}}
{{/if}}
{{header_comment_end}}

{{/if}}
{{initial_content}}
```

## Template Logic

**Header comment style by file type:**
- `.py`: `# ` prefix
- `.js, .ts, .java, .c, .cpp`: `// ` prefix or `/* */` block
- `.sql, .m, .dax`: `-- ` prefix
- `.html, .xml`: `<!-- -->` block
- `.md`: No header comment (use frontmatter if needed)

## Post-Conditions
- [ ] File created at specified path
- [ ] File has appropriate header comment (if enabled)
- [ ] File is valid for its type (e.g., valid JSON if .json)
- [ ] File permissions are correct
- [ ] File added to version control (if project uses git)

## Anti-Patterns
**DON'T do this:**
- Create files without checking if they already exist
- Use hardcoded absolute paths (use relative to project root)
- Forget header comments for code files
- Create files with incorrect encoding (always use UTF-8)
- Skip adding new files to .gitignore if they should be ignored

**WHY**: Creating files without checks can overwrite existing work. Hardcoded paths break portability. Missing headers reduce code maintainability.

## Examples

### Example 1: Python Module
**Input:**
```
file_path: src/utils/calculator.py
file_type: .py
file_purpose: Utility functions for mathematical calculations
author: Claude Code
include_header: true
initial_content:
```

**Output:**
```python
# Utility functions for mathematical calculations
#
# Created: 2025-12-05 10:30:00
# Author: Claude Code


```

### Example 2: Markdown Documentation
**Input:**
```
file_path: docs/api-reference.md
file_type: .md
file_purpose: API endpoint documentation
include_header: false
initial_content: # API Reference\n\n## Endpoints
```

**Output:**
```markdown
# API Reference

## Endpoints
```

### Example 3: JSON Configuration
**Input:**
```
file_path: config/settings.json
file_type: .json
file_purpose: Application configuration
include_header: false
initial_content: {\n  "version": "1.0.0"\n}
```

**Output:**
```json
{
  "version": "1.0.0"
}
```

### Example 4: Power Query M File
**Input:**
```
file_path: queries/Bronze_SalesData.m
file_type: .m
file_purpose: Bronze layer: Sales data from Excel source
author: Data Team
include_header: true
```

**Output:**
```powerquery-m
// Bronze layer: Sales data from Excel source
//
// Created: 2025-12-05 10:30:00
// Author: Data Team


```

## Usage Notes

- **Always check before creating**: Use Read tool first to verify file doesn't exist
- **Use Write tool**: This pattern guides content, actual creation uses Write tool
- **Relative paths preferred**: Makes project portable
- **Encoding**: Always specify UTF-8 encoding
- **Git tracking**: Remember to git add new files if under version control

## Related Patterns
- `modify-file.pattern.md` - For editing existing files
- `bulk-rename.pattern.md` - For renaming multiple files
