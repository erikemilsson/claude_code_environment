# Claude 4 Coding Guidelines

## Core Principles

### 1. Read Before Edit
**ALWAYS** read files before modifying them. Never assume content.

```
GOOD: Read → Understand → Edit
BAD: Guess → Write → Overwrite existing code
```

### 2. Minimize File Creation
- **Prefer editing existing files** over creating new ones
- Only create files when explicitly required by user or task
- Never proactively create documentation unless requested

### 3. Tool Usage Hierarchy

#### File Operations
1. **Read** - Use for reading files (NEVER use `cat` via Bash)
2. **Edit** - Use for modifying existing files (NEVER use `sed/awk` via Bash)
3. **Write** - Use only for new files (NEVER use `echo >` via Bash)

#### Search Operations
1. **Glob** - Use for file pattern matching
2. **Grep** - Use for content search
3. **Task with Explore agent** - Use for complex, multi-step searches

### 4. Error Handling Patterns

#### Graceful Failures
```python
# GOOD: Explicit error handling with recovery
try:
    result = risky_operation()
except SpecificError as e:
    # Log error details
    # Attempt recovery or fallback
    # Return meaningful error to user

# BAD: Silent failures or generic catches
try:
    everything()
except:
    pass
```

#### Validation Gates
- Pre-execution validation
- Mid-task checkpoints
- Post-execution verification

### 5. Avoiding Over-Engineering

#### YAGNI (You Aren't Gonna Need It)
```python
# GOOD: Simple, direct solution
def calculate_total(items):
    return sum(item.price for item in items)

# BAD: Over-abstracted for future that may never come
class TotalCalculationStrategyFactory:
    def create_strategy(self, calculation_type):
        # 50 lines of abstraction for a sum operation
```

#### Start Simple, Iterate
1. Implement minimal working solution
2. Test and validate
3. Add complexity only when proven necessary
4. Document why complexity was added

### 6. Avoiding Hallucinations

#### File Content
- **NEVER** guess file contents
- **ALWAYS** read before referencing
- **VERIFY** paths exist before operations

#### API/Library Usage
- Don't assume methods exist
- Verify syntax with documentation
- Test with minimal examples first

#### Data Structures
- Don't invent fields or properties
- Check actual schema/structure
- Validate assumptions with reads

### 7. Performance Patterns

#### Parallel Execution
```python
# GOOD: Parallel independent operations
results = await asyncio.gather(
    read_file("a.txt"),
    read_file("b.txt"),
    read_file("c.txt")
)

# BAD: Sequential when parallel possible
a = await read_file("a.txt")
b = await read_file("b.txt")
c = await read_file("c.txt")
```

#### Batch Operations
- Group related file operations
- Use bulk updates where possible
- Minimize repeated tool calls

### 8. Testing Patterns

#### Test-First Approach
1. Write test cases from requirements
2. Implement to pass tests
3. Refactor with confidence

#### Validation Levels
- **Unit**: Individual functions
- **Integration**: Component interactions
- **End-to-end**: Full workflows

### 9. Code Quality Metrics

#### Complexity Thresholds
- Functions: Max 20 lines (prefer 10)
- Cyclomatic complexity: Max 5
- Nesting depth: Max 3 levels

#### Documentation Requirements
- Public functions: Always document
- Complex logic: Inline comments
- Non-obvious decisions: Explain why

### 10. Security Considerations

#### Never Create
- Credentials in code
- Unvalidated user input execution
- Unrestricted file operations

#### Always Validate
- Input boundaries
- File paths
- Command arguments

## Common Anti-Patterns to Avoid

### 1. Echo-Driven Development
```bash
# BAD: Using echo for everything
echo "Starting process" >> log.txt
echo "$content" > file.py

# GOOD: Use proper tools
# Use Write tool for new files
# Use Edit tool for modifications
```

### 2. Blind Overwrites
```python
# BAD: Writing without checking
write_file("config.json", new_config)

# GOOD: Read, merge, write
existing = read_file("config.json")
merged = merge_configs(existing, new_config)
write_file("config.json", merged)
```

### 3. Assumption-Based Coding
```python
# BAD: Assuming structure
data["user"]["preferences"]["theme"]

# GOOD: Defensive access
data.get("user", {}).get("preferences", {}).get("theme", "default")
```

### 4. Context Explosion
```python
# BAD: Loading everything
all_files = read_entire_project()

# GOOD: Targeted reads
relevant_files = read_files(["src/main.py", "src/config.py"])
```

## Language-Specific Guides

- [Python Guidelines](./coding-guidelines-python.md)
- [SQL Guidelines](./coding-guidelines-sql.md)
- [Power Query/M Guidelines](./coding-guidelines-powerquery.md)
- [JavaScript Guidelines](./coding-guidelines-javascript.md)

## Quick Reference Card

| Operation | Use This Tool | Never Use |
|-----------|--------------|-----------|
| Read file | Read | cat, head, tail via Bash |
| Edit file | Edit | sed, awk via Bash |
| Create file | Write | echo >, cat > via Bash |
| Find files | Glob | find via Bash |
| Search content | Grep | grep via Bash |
| Complex search | Task (Explore) | Multiple manual searches |

## Confidence Thresholds

| Confidence | Action |
|------------|--------|
| >90% | Proceed automatically |
| 70-90% | Minimal clarification |
| 50-70% | Detailed clarification |
| <50% | Full requirements gathering |