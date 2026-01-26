# Core Coding Guidelines

*Shared principles for all languages - see language-specific files for details.*

## 1. Error Handling Patterns

### Custom Exceptions
Create specific exception classes with context:
- Include relevant data (field, value, operation)
- Provide meaningful messages explaining what failed
- Enable recovery by including actionable information

### Error Recovery
- Use try/catch (or equivalent) with specific exception types
- Log errors with context for debugging
- Return structured error responses (success/failure with details)
- Never silently swallow errors

### Graceful Degradation
- Provide fallback values for non-critical failures
- Use circuit breaker patterns for external dependencies
- Validate inputs at system boundaries

## 2. File Operation Patterns

### Read Before Write
- Always read existing content before modification
- Merge changes rather than overwrite
- Validate paths exist before operations

### Resource Management
- Use context managers/RAII for automatic cleanup
- Close handles in finally blocks or equivalents
- Set appropriate timeouts on connections

### Path Handling
- Use language-native path objects (Path, os.path, etc.)
- Validate paths before operations
- Handle both absolute and relative paths

## 3. Testing Approaches

### Test Structure (AAA Pattern)
1. **Arrange**: Set up test fixtures and data
2. **Act**: Execute the code under test
3. **Assert**: Verify expected outcomes

### Test Levels
- **Unit tests**: Individual functions, isolated
- **Integration tests**: Component interactions
- **End-to-end tests**: Full workflows

### Test Quality
- Use descriptive test names explaining the scenario
- One assertion per test when practical
- Use fixtures for shared setup
- Mock external dependencies

## 4. Documentation Standards

### Code Comments
- Explain WHY, not WHAT
- Document non-obvious decisions
- Keep comments current with code

### Function Documentation
- Describe purpose and behavior
- Document parameters and return types
- Note exceptions/errors that may be raised
- Include usage examples for complex APIs

### Self-Documenting Code
- Use descriptive variable names
- Keep functions small and focused
- Follow naming conventions consistently

## 5. Security Practices

### Input Validation
- Validate all external input at boundaries
- Use parameterized queries for databases
- Sanitize content before display (XSS prevention)

### Sensitive Data
- Never hardcode credentials
- Use environment variables or secure vaults
- Exclude sensitive files from version control

### Principle of Least Privilege
- Request only necessary permissions
- Validate authorization for each operation
- Audit security-sensitive operations

## 6. Performance Patterns

### Parallel Execution
- Use async/parallel for independent I/O operations
- Batch similar operations together
- Avoid blocking calls in async contexts

### Efficient Data Structures
- Use sets for membership testing (O(1) vs O(n))
- Choose appropriate collections for access patterns
- Profile before optimizing

### Resource Efficiency
- Avoid unnecessary allocations in loops
- Use lazy evaluation for large datasets
- Cache expensive computations

## 7. Code Quality Metrics

| Metric | Target |
|--------|--------|
| Function length | Max 20 lines (prefer 10) |
| Cyclomatic complexity | Max 5 |
| Nesting depth | Max 3 levels |
| Parameters | Max 5 per function |

## Quick Reference

### Universal Anti-Patterns
| Avoid | Do Instead |
|-------|------------|
| Silent error handling | Log and handle specifically |
| Magic numbers | Named constants |
| Deep nesting | Early returns, guard clauses |
| Mutable global state | Dependency injection |
| Implicit type conversions | Explicit typing |

### Universal Best Practices
- Read before write
- Validate at boundaries
- Fail fast with clear messages
- Keep functions focused
- Document non-obvious decisions
