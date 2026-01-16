# Pattern: Modify File

## Metadata
- **ID**: pattern-file-modify
- **Version**: 1.0.0
- **Category**: file-operations
- **Difficulty Range**: 2-4 (file editing tasks)

## Triggers
Keywords that suggest this pattern applies:
- modify file
- edit file
- update file
- change file
- fix file
- refactor

File types: All text-based files

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_path | string | yes | Path to file to modify |
| modification_type | enum | yes | Type of change: add/replace/delete/refactor |
| target_section | string | yes | What part to modify (line number, function name, section) |
| old_content | string | conditional | Required for replace type |
| new_content | string | conditional | Required for add/replace types |
| preserve_formatting | boolean | no | Keep original indentation/style (default: true) |

## Pre-Conditions
- [ ] File exists and is readable
- [ ] File has been read with Read tool first (CRITICAL)
- [ ] Target section/content exists in file (for replace/delete)
- [ ] Modification follows project coding standards
- [ ] Backup/checkpoint created (if using checkpoint system)

## Template

### Strategy Selection

**For add (new content):**
```
Identify insertion point in file
Preserve existing indentation
Insert new content
Maintain spacing consistency
```

**For replace (modify existing):**
```
Locate exact old_content string
Verify it appears only once (or use replace_all if intentional)
Replace with new_content
Preserve surrounding context
```

**For delete (remove content):**
```
Locate target section
Remove cleanly (no orphaned comments/imports)
Update references if needed
```

**For refactor (restructure):**
```
Extract reusable logic
Rename for clarity
Update all call sites
Maintain backwards compatibility if possible
```

## Process

### 1. Read First (MANDATORY)
```
Use Read tool to get current file contents
Review target section
Confirm modification location
```

### 2. Use Edit Tool
```
For single replacements:
  Use Edit tool with exact old_string match

For multiple changes:
  Consider breaking into separate Edit calls
  OR use replace_all if replacing all occurrences
```

### 3. Verify Changes
```
Read file again to confirm change
Check formatting preserved
Verify no unintended changes
```

## Post-Conditions
- [ ] File modification successful
- [ ] Original formatting/indentation preserved
- [ ] No syntax errors introduced
- [ ] All references still valid
- [ ] File still follows project conventions
- [ ] Changes logged in task notes

## Anti-Patterns
**DON'T do this:**
- Modify file without reading it first (CRITICAL ERROR)
- Use ambiguous old_string that matches multiple locations
- Change indentation accidentally (breaks Python, etc.)
- Forget to update related files (imports, tests, etc.)
- Make multiple unrelated changes in one edit
- Skip verification after modification

**WHY**:
- **Reading first is MANDATORY** - Edit tool will ERROR if you haven't read the file
- Ambiguous matches cause Edit tool to fail
- Indentation errors break code
- Related files become out of sync
- Multiple changes harder to review and rollback

## Examples

### Example 1: Replace Function Implementation
**Input:**
```
file_path: src/utils/calculator.py
modification_type: replace
target_section: calculate_total function
old_content: |
  def calculate_total(numbers):
      return sum(numbers)
new_content: |
  def calculate_total(numbers: list[float]) -> float:
      """Calculate total from list of numbers."""
      if not numbers:
          raise ValueError("Cannot calculate total of empty list")
      return sum(numbers)
preserve_formatting: true
```

**Process:**
1. Read src/utils/calculator.py
2. Locate function in file content
3. Use Edit tool with exact match
4. Verify indentation preserved

### Example 2: Add Import Statement
**Input:**
```
file_path: src/main.py
modification_type: add
target_section: import section (after existing imports)
new_content: from utils.calculator import calculate_total
```

**Process:**
1. Read src/main.py
2. Find last import statement
3. Use Edit to add after last import
4. Maintain alphabetical ordering if present

### Example 3: Delete Deprecated Function
**Input:**
```
file_path: src/legacy.py
modification_type: delete
target_section: old_calculate function
old_content: |
  def old_calculate(a, b):
      # Deprecated: Use calculate_total instead
      return a + b
```

**Process:**
1. Read src/legacy.py
2. Search for function usage (should be none)
3. Use Edit to replace with empty string
4. Verify no broken references

### Example 4: Refactor Variable Names
**Input:**
```
file_path: src/processor.py
modification_type: refactor
target_section: All occurrences of 'df'
old_content: df
new_content: sales_dataframe
preserve_formatting: true
```

**Process:**
1. Read src/processor.py
2. Count occurrences of 'df'
3. Use Edit with replace_all=true
4. Verify all replacements sensible (no false matches)

## Usage Notes

### Critical Rules
1. **ALWAYS Read first** - Edit tool requires this
2. **Exact matches** - old_string must match exactly (including whitespace)
3. **One change at a time** - Multiple edits = multiple Edit calls
4. **Verify after** - Read again to confirm changes

### When to Use Edit Tool
- Single, precise string replacement
- Known exact content to replace
- Line-by-line preservation important

### When NOT to Use This Pattern
- Creating new file (use create-file pattern)
- Bulk renaming files (use bulk-rename pattern)
- Complex code generation (use code-generation patterns)

## Error Handling

**File not found:**
```
Error: Cannot modify non-existent file
→ Verify file_path is correct
→ Use create-file pattern if file should be created
```

**Haven't read file:**
```
Error: Must use Read tool before Edit
→ Read file first to see current contents
→ Then use Edit with exact old_string
```

**Ambiguous match:**
```
Error: old_string matches multiple locations
→ Provide more context in old_string
→ OR use replace_all if replacing all is intended
```

## Related Patterns
- `create-file.pattern.md` - For new files
- `python-function.pattern.md` - For Python-specific refactoring
- `bulk-rename.pattern.md` - For renaming operations
