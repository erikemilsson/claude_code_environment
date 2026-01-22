# JavaScript/TypeScript Guidelines

*Language-specific patterns - see core.md for shared principles.*

## Modern Syntax
- Use `const`/`let` (never `var`)
- Arrow functions for callbacks
- Destructuring for cleaner access
- Template literals for string building
- Spread operator for object/array manipulation

## TypeScript Types
```typescript
// Comprehensive types
interface User {
    id: string;
    name: string;
    preferences?: UserPreferences;
}

type ApiResponse<T> =
    | { success: true; data: T }
    | { success: false; error: string };

// Avoid: any, implicit types
```

## Async Patterns
```javascript
// Use async/await over callbacks
const result = await fetchWithRetry(url, { timeout: 5000, maxRetries: 3 });

// Parallel independent operations
const [profile, posts] = await Promise.all([
    fetchProfile(id),
    fetchPosts(id)
]);

// AbortController for timeouts
const controller = new AbortController();
setTimeout(() => controller.abort(), 5000);
```

## React Patterns
- `useMemo` for expensive computations
- `useCallback` for stable references
- Early returns for loading/error states
- Custom hooks for reusable logic
- React.memo for expensive components

## Quick Reference

| Feature | Use | Avoid |
|---------|-----|-------|
| Variables | const, let | var |
| Strings | Template literals | Concatenation |
| Async | async/await | Nested callbacks |
| Arrays | map, filter, reduce | for loops when functional works |
| State | Immutable updates | Direct mutation |
| Effects | Cleanup functions | Forgetting cleanup |
