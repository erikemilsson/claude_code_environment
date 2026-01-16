# Pattern: Bulk Rename Files

## Metadata
- **ID**: pattern-file-bulk-rename
- **Version**: 1.0.0
- **Category**: file-operations
- **Difficulty Range**: 3-5 (systematic file renaming)

## Triggers
Keywords that suggest this pattern applies:
- rename files
- bulk rename
- rename multiple
- reorganize files
- standardize naming
- fix naming convention

File types: All files (focus on text/code files for safety)

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| target_pattern | string | yes | Glob pattern for files to rename (e.g., "src/**/*.py") |
| naming_strategy | enum | yes | How to rename: prefix/suffix/replace/sequential/convention |
| pattern_match | string | conditional | Required for 'replace' strategy |
| pattern_replacement | string | conditional | Required for 'replace' strategy |
| prefix | string | conditional | Required for 'prefix' strategy |
| suffix | string | conditional | Required for 'suffix' strategy |
| dry_run | boolean | no | Preview changes without executing (default: true) |

## Pre-Conditions
- [ ] All target files exist and are accessible
- [ ] New names won't conflict with existing files
- [ ] Naming convention is well-defined
- [ ] All affected files are under version control (if applicable)
- [ ] No files are currently open/locked by other processes

## Template

### Process Flow

```
1. GATHER FILES
   Use Glob tool with target_pattern
   List all matching files
   Count total files affected

2. PREVIEW CHANGES (if dry_run=true)
   For each file:
     old_path: {current path}
     new_path: {computed new path}

   Show summary:
     Total files: {count}
     Naming conflicts: {conflict_count}

   Confirm before proceeding

3. EXECUTE RENAMES
   For each file in order:
     mv "{old_path}" "{new_path}"
     Log change

   Handle errors:
     If rename fails, note but continue
     Collect all errors for final report

4. UPDATE REFERENCES
   Search for file path references in code
   Update import statements
   Update configuration files

5. VERIFY
   Confirm all files renamed successfully
   Check no broken references
   Update version control if needed
```

## Naming Strategies

### 1. Prefix Strategy
```
old: utils.py
prefix: "common_"
new: common_utils.py
```

### 2. Suffix Strategy
```
old: test_api.py
suffix: "_integration"
new: test_api_integration.py
```

### 3. Replace Strategy
```
old: user_mgmt.py
pattern_match: "_mgmt"
pattern_replacement: "_management"
new: user_management.py
```

### 4. Sequential Strategy
```
old: file1.txt, file2.txt, file3.txt
format: "document_{seq:03d}.txt"
new: document_001.txt, document_002.txt, document_003.txt
```

### 5. Convention Strategy
```
old: UserAPI.py, ProductAPI.py
convention: "snake_case"
new: user_api.py, product_api.py
```

## Post-Conditions
- [ ] All files renamed according to strategy
- [ ] No naming conflicts created
- [ ] All file references updated (imports, configs, etc.)
- [ ] Version control updated (git mv used if in repo)
- [ ] Rename log created in task notes
- [ ] No broken links or missing files

## Anti-Patterns
**DON'T do this:**
- Rename without dry run preview first
- Ignore naming conflicts
- Forget to update import statements
- Use regular `mv` instead of `git mv` for tracked files
- Rename files that are currently open
- Make changes without version control
- Skip verification after renaming

**WHY**:
- Dry runs prevent catastrophic mistakes
- Naming conflicts cause overwrites (data loss)
- Broken imports break the codebase
- Regular mv loses git history
- Open files may cause conflicts
- Difficult to recover without version control
- Verification catches issues before they propagate

## Examples

### Example 1: Standardize Test File Names
**Input:**
```
target_pattern: tests/**/*.py
naming_strategy: prefix
prefix: test_
dry_run: true
```

**Process:**
```
1. Glob: tests/**/*.py
   Found 15 files

2. Preview:
   tests/api.py → tests/test_api.py
   tests/database.py → tests/test_database.py
   tests/models.py → tests/test_models.py
   ... (12 more)

   Conflicts: None

   Proceed with renaming? [Y/N]
```

**Result (if Y):**
```
Renamed 15 files:
  ✓ tests/api.py → tests/test_api.py
  ✓ tests/database.py → tests/test_database.py
  ... (13 more)

Updated 8 import statements in:
  - src/main.py (3 imports)
  - tests/conftest.py (5 imports)

All operations successful.
```

### Example 2: Replace Abbreviation
**Input:**
```
target_pattern: src/**/*_mgmt.py
naming_strategy: replace
pattern_match: _mgmt
pattern_replacement: _management
dry_run: false
```

**Result:**
```
Found 4 files matching pattern

Renaming:
  ✓ src/user_mgmt.py → src/user_management.py
  ✓ src/product_mgmt.py → src/product_management.py
  ✓ src/order_mgmt.py → src/order_management.py
  ✓ src/inventory_mgmt.py → src/inventory_management.py

Updating references...
  ✓ Updated 12 import statements across 6 files
  ✓ Updated config/modules.json

Complete: 4 files renamed, 12 references updated
```

### Example 3: Snake Case Convention
**Input:**
```
target_pattern: src/models/*.py
naming_strategy: convention
convention: snake_case
dry_run: true
```

**Preview:**
```
Found 6 files

Proposed changes:
  src/models/UserProfile.py → src/models/user_profile.py
  src/models/ProductCatalog.py → src/models/product_catalog.py
  src/models/OrderHistory.py → src/models/order_history.py
  src/models/InventoryItem.py → src/models/inventory_item.py
  src/models/ShippingAddress.py → src/models/shipping_address.py
  src/models/PaymentMethod.py → src/models/payment_method.py

⚠️  Warning: This will affect 23 import statements

Impact analysis:
  - 23 files import from these modules
  - All will need imports updated
  - Consider updating in separate commit

Proceed? [Y/N]
```

### Example 4: Sequential Numbering
**Input:**
```
target_pattern: migrations/*.sql
naming_strategy: sequential
format: {seq:04d}_{original_name}
dry_run: false
```

**Result:**
```
Found 8 migration files

Renaming with sequential numbering:
  ✓ create_users.sql → 0001_create_users.sql
  ✓ add_products.sql → 0002_add_products.sql
  ✓ update_schema.sql → 0003_update_schema.sql
  ... (5 more)

Migrations now properly ordered.
```

## Usage Notes

### Critical Safety Steps
1. **Always dry run first** - Preview changes before executing
2. **Check for conflicts** - Ensure new names don't exist
3. **Version control** - Use git mv for tracked files
4. **Update references** - Search and update all imports/configs
5. **Verify after** - Confirm all references still work

### Best Practices
- Rename in small batches (easier to review)
- Use descriptive naming conventions
- Document naming standard in project docs
- Run tests after bulk renaming
- Commit renames separately from other changes

### When to Use This Pattern
- Standardizing file naming across project
- Migrating to new naming convention
- Organizing files systematically
- Preparing for automated tools that expect specific names

### When NOT to Use
- Single file rename (just use mv or git mv)
- Files actively being modified
- Production files without backup
- When unsure of impact

## Error Handling

**Naming conflict:**
```
Error: Cannot rename to existing file
  source/user.py → target/user.py
  But target/user.py already exists

Resolution:
  - Choose different naming strategy
  - Manually resolve conflict first
  - Add suffix to distinguish
```

**Broken references:**
```
Warning: Found 5 import statements that may be broken
  src/main.py:12: from models.UserProfile import User

Post-rename verification:
  → Search for old names in codebase
  → Update all references manually
  → Run tests to verify
```

**Permission denied:**
```
Error: Cannot rename file (permission denied)
  logs/production.log

Resolution:
  - Check file permissions
  - Ensure file not locked by other process
  - Close file in editors/IDEs
```

## Reference Update Patterns

**Python imports:**
```
Old: from models.UserProfile import User
New: from models.user_profile import User
```

**JavaScript/TypeScript imports:**
```
Old: import { User } from './models/UserProfile'
New: import { User } from './models/user_profile'
```

**Configuration files:**
```
Old: "module": "src/user_mgmt.py"
New: "module": "src/user_management.py"
```

## Related Patterns
- `create-file.pattern.md` - For new files
- `modify-file.pattern.md` - For updating file references
- Project-specific refactoring patterns
