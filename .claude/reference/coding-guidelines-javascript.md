# JavaScript Coding Guidelines for Claude 4

## JavaScript/TypeScript Best Practices

### 1. Modern Syntax and Structure

```javascript
// GOOD: Modern ES6+ syntax
// Use const/let, arrow functions, destructuring
const processUserData = async (userData) => {
    const { id, name, email, preferences = {} } = userData;

    try {
        const result = await validateUser(id);
        const formattedData = {
            ...result,
            displayName: name.trim(),
            email: email.toLowerCase(),
            settings: {
                ...DEFAULT_SETTINGS,
                ...preferences
            }
        };

        return { success: true, data: formattedData };
    } catch (error) {
        console.error(`Failed to process user ${id}:`, error);
        return { success: false, error: error.message };
    }
};

// BAD: Outdated patterns
var processUserData = function(userData) {
    var id = userData.id;
    var name = userData.name;
    var email = userData.email;

    return validateUser(id).then(function(result) {
        var formattedData = Object.assign({}, result);
        formattedData.displayName = name.trim();
        return {success: true, data: formattedData};
    });
};
```

### 2. TypeScript Type Safety

```typescript
// GOOD: Comprehensive type definitions
interface UserPreferences {
    theme: 'light' | 'dark';
    notifications: boolean;
    language: string;
}

interface User {
    id: string;
    name: string;
    email: string;
    createdAt: Date;
    preferences?: UserPreferences;
}

type ApiResponse<T> =
    | { success: true; data: T }
    | { success: false; error: string };

const fetchUser = async (userId: string): Promise<ApiResponse<User>> => {
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return { success: true, data };
    } catch (error) {
        return {
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error'
        };
    }
};

// BAD: Weak typing
const fetchUser = async (userId: any): Promise<any> => {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
};
```

### 3. Error Handling Patterns

```javascript
// GOOD: Comprehensive error handling
class ValidationError extends Error {
    constructor(field, value, message) {
        super(message);
        this.name = 'ValidationError';
        this.field = field;
        this.value = value;
    }
}

const validateFormData = (formData) => {
    const errors = [];

    // Validate email
    if (!formData.email) {
        errors.push(new ValidationError('email', formData.email, 'Email is required'));
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
        errors.push(new ValidationError('email', formData.email, 'Invalid email format'));
    }

    // Validate password
    if (!formData.password) {
        errors.push(new ValidationError('password', null, 'Password is required'));
    } else if (formData.password.length < 8) {
        errors.push(new ValidationError('password', null, 'Password must be at least 8 characters'));
    }

    if (errors.length > 0) {
        const error = new Error('Validation failed');
        error.validationErrors = errors;
        throw error;
    }

    return formData;
};

// Error boundary for React
class ErrorBoundary extends React.Component {
    state = { hasError: false, error: null };

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error('Error caught by boundary:', error, errorInfo);
        // Log to error reporting service
        logErrorToService(error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return <ErrorFallback error={this.state.error} />;
        }

        return this.props.children;
    }
}
```

### 4. Async Operations and Promises

```javascript
// GOOD: Proper async handling
const fetchDataWithRetry = async (url, options = {}, maxRetries = 3) => {
    const { timeout = 5000, ...fetchOptions } = options;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), timeout);

            const response = await fetch(url, {
                ...fetchOptions,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.warn(`Attempt ${attempt} failed:`, error.message);

            if (attempt === maxRetries) {
                throw new Error(`Failed after ${maxRetries} attempts: ${error.message}`);
            }

            // Exponential backoff
            await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
        }
    }
};

// GOOD: Parallel operations
const fetchUserData = async (userId) => {
    const [profile, posts, followers] = await Promise.all([
        fetchUserProfile(userId),
        fetchUserPosts(userId),
        fetchUserFollowers(userId)
    ]);

    return { profile, posts, followers };
};

// GOOD: Sequential when needed
const processOrderWorkflow = async (orderId) => {
    const order = await fetchOrder(orderId);
    const validation = await validateOrder(order);

    if (validation.isValid) {
        const payment = await processPayment(order);
        const shipment = await scheduleShipment(order, payment);
        return { success: true, shipment };
    }

    return { success: false, errors: validation.errors };
};
```

### 5. React Best Practices

```jsx
// GOOD: Modern React patterns
import { useState, useEffect, useCallback, useMemo } from 'react';

const UserList = ({ filters }) => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Memoize expensive computations
    const filteredUsers = useMemo(() => {
        if (!filters) return users;

        return users.filter(user => {
            const matchesSearch = !filters.search ||
                user.name.toLowerCase().includes(filters.search.toLowerCase());
            const matchesStatus = !filters.status ||
                user.status === filters.status;

            return matchesSearch && matchesStatus;
        });
    }, [users, filters]);

    // Stable callback reference
    const fetchUsers = useCallback(async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await api.getUsers();
            setUsers(response.data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchUsers();
    }, [fetchUsers]);

    // Early returns for loading/error states
    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorMessage message={error} />;
    if (filteredUsers.length === 0) return <EmptyState />;

    return (
        <div className="user-list">
            {filteredUsers.map(user => (
                <UserCard key={user.id} user={user} />
            ))}
        </div>
    );
};

// Custom hooks for reusable logic
const useDebounce = (value, delay) => {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => clearTimeout(timer);
    }, [value, delay]);

    return debouncedValue;
};
```

### 6. DOM Manipulation and Events

```javascript
// GOOD: Efficient DOM handling
const VirtualList = ({ items, itemHeight, containerHeight }) => {
    const [scrollTop, setScrollTop] = useState(0);

    // Calculate visible range
    const startIndex = Math.floor(scrollTop / itemHeight);
    const endIndex = Math.min(
        items.length - 1,
        Math.ceil((scrollTop + containerHeight) / itemHeight)
    );

    // Only render visible items
    const visibleItems = items.slice(startIndex, endIndex + 1);

    const handleScroll = useCallback((e) => {
        setScrollTop(e.target.scrollTop);
    }, []);

    return (
        <div
            className="virtual-list-container"
            style={{ height: containerHeight, overflow: 'auto' }}
            onScroll={handleScroll}
        >
            <div style={{ height: items.length * itemHeight }}>
                {visibleItems.map((item, index) => (
                    <div
                        key={startIndex + index}
                        style={{
                            position: 'absolute',
                            top: (startIndex + index) * itemHeight,
                            height: itemHeight
                        }}
                    >
                        {item}
                    </div>
                ))}
            </div>
        </div>
    );
};

// GOOD: Event delegation
const handleTableClick = (event) => {
    const target = event.target;

    // Find the clicked row
    const row = target.closest('tr[data-row-id]');
    if (!row) return;

    const rowId = row.dataset.rowId;

    // Handle different actions
    if (target.matches('.delete-btn')) {
        deleteRow(rowId);
    } else if (target.matches('.edit-btn')) {
        editRow(rowId);
    } else {
        selectRow(rowId);
    }
};

document.querySelector('#data-table').addEventListener('click', handleTableClick);
```

### 7. State Management Patterns

```javascript
// GOOD: Redux Toolkit pattern
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk for API calls
export const fetchTodos = createAsyncThunk(
    'todos/fetchTodos',
    async (userId, { rejectWithValue }) => {
        try {
            const response = await api.getTodos(userId);
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response.data);
        }
    }
);

const todosSlice = createSlice({
    name: 'todos',
    initialState: {
        items: [],
        status: 'idle',
        error: null
    },
    reducers: {
        todoAdded: (state, action) => {
            state.items.push(action.payload);
        },
        todoToggled: (state, action) => {
            const todo = state.items.find(t => t.id === action.payload);
            if (todo) {
                todo.completed = !todo.completed;
            }
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchTodos.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(fetchTodos.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.items = action.payload;
            })
            .addCase(fetchTodos.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.payload;
            });
    }
});

// Context API for simpler cases
const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
    const [theme, setTheme] = useState(() => {
        // Initialize from localStorage
        return localStorage.getItem('theme') || 'light';
    });

    const toggleTheme = useCallback(() => {
        setTheme(prev => {
            const newTheme = prev === 'light' ? 'dark' : 'light';
            localStorage.setItem('theme', newTheme);
            return newTheme;
        });
    }, []);

    const value = useMemo(() => ({ theme, toggleTheme }), [theme, toggleTheme]);

    return (
        <ThemeContext.Provider value={value}>
            {children}
        </ThemeContext.Provider>
    );
};
```

### 8. Performance Optimization

```javascript
// GOOD: Optimize re-renders
const ExpensiveComponent = React.memo(({ data, onUpdate }) => {
    // Only re-render if props actually change
    const processedData = useMemo(() => {
        return heavyProcessing(data);
    }, [data]);

    return <DisplayComponent data={processedData} onUpdate={onUpdate} />;
}, (prevProps, nextProps) => {
    // Custom comparison
    return prevProps.data.id === nextProps.data.id &&
           prevProps.data.version === nextProps.data.version;
});

// GOOD: Lazy loading
const HeavyComponent = lazy(() => import('./HeavyComponent'));

const App = () => {
    return (
        <Suspense fallback={<LoadingSpinner />}>
            <HeavyComponent />
        </Suspense>
    );
};

// GOOD: Debouncing expensive operations
const SearchInput = ({ onSearch }) => {
    const [value, setValue] = useState('');
    const debouncedSearch = useMemo(
        () => debounce(onSearch, 300),
        [onSearch]
    );

    const handleChange = (e) => {
        setValue(e.target.value);
        debouncedSearch(e.target.value);
    };

    return <input value={value} onChange={handleChange} />;
};
```

### 9. Testing Patterns

```javascript
// GOOD: Comprehensive testing
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('UserForm', () => {
    // Setup and teardown
    let mockSubmit;

    beforeEach(() => {
        mockSubmit = jest.fn();
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    test('validates required fields', async () => {
        render(<UserForm onSubmit={mockSubmit} />);

        // Try to submit empty form
        const submitButton = screen.getByRole('button', { name: /submit/i });
        fireEvent.click(submitButton);

        // Check for error messages
        expect(screen.getByText(/email is required/i)).toBeInTheDocument();
        expect(screen.getByText(/password is required/i)).toBeInTheDocument();
        expect(mockSubmit).not.toHaveBeenCalled();
    });

    test('submits valid data', async () => {
        render(<UserForm onSubmit={mockSubmit} />);

        // Fill in form
        await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
        await userEvent.type(screen.getByLabelText(/password/i), 'SecurePass123!');

        // Submit
        fireEvent.click(screen.getByRole('button', { name: /submit/i }));

        await waitFor(() => {
            expect(mockSubmit).toHaveBeenCalledWith({
                email: 'test@example.com',
                password: 'SecurePass123!'
            });
        });
    });

    // Testing async operations
    test('loads user data', async () => {
        const mockUser = { id: 1, name: 'Test User' };
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(mockUser)
            })
        );

        render(<UserProfile userId={1} />);

        expect(screen.getByText(/loading/i)).toBeInTheDocument();

        await waitFor(() => {
            expect(screen.getByText(mockUser.name)).toBeInTheDocument();
        });
    });
});
```

### 10. Security Best Practices

```javascript
// GOOD: Security-conscious coding
// Sanitize HTML content
import DOMPurify from 'dompurify';

const SafeHTML = ({ content }) => {
    const sanitized = DOMPurify.sanitize(content);
    return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
};

// Validate and escape user input
const validateInput = (input) => {
    // Remove any script tags or javascript: protocols
    const cleaned = input
        .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
        .replace(/javascript:/gi, '');

    return cleaned;
};

// Use CSP headers
const cspMiddleware = (req, res, next) => {
    res.setHeader(
        'Content-Security-Policy',
        "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    );
    next();
};

// Secure cookie handling
const setSecureCookie = (res, name, value) => {
    res.cookie(name, value, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 3600000 // 1 hour
    });
};

// Rate limiting
const rateLimiter = new Map();

const checkRateLimit = (userId, maxRequests = 10, windowMs = 60000) => {
    const now = Date.now();
    const userRequests = rateLimiter.get(userId) || [];

    // Remove old requests outside window
    const recentRequests = userRequests.filter(time => now - time < windowMs);

    if (recentRequests.length >= maxRequests) {
        throw new Error('Rate limit exceeded');
    }

    recentRequests.push(now);
    rateLimiter.set(userId, recentRequests);
};
```

## Anti-Patterns to Avoid

### 1. Callback Hell
```javascript
// BAD: Nested callbacks
getData(function(a) {
    getMoreData(a, function(b) {
        getMoreData(b, function(c) {
            getMoreData(c, function(d) {
                // Deep nesting
            });
        });
    });
});

// GOOD: Use async/await
const data = await getData();
const moreData = await getMoreData(data);
const evenMore = await getMoreData(moreData);
```

### 2. Mutating State Directly
```javascript
// BAD: Direct mutation
state.items.push(newItem);
setState(state);

// GOOD: Create new state
setState(prevState => ({
    ...prevState,
    items: [...prevState.items, newItem]
}));
```

### 3. Memory Leaks
```javascript
// BAD: Forgetting to clean up
useEffect(() => {
    const timer = setInterval(() => {
        // Do something
    }, 1000);
    // Missing cleanup!
});

// GOOD: Proper cleanup
useEffect(() => {
    const timer = setInterval(() => {
        // Do something
    }, 1000);

    return () => clearInterval(timer);
}, []);
```

## Quick Reference

| Feature | Use | Avoid |
|---------|-----|-------|
| Variables | const, let | var |
| Functions | Arrow functions | function keyword (except classes) |
| Async | async/await | Nested callbacks |
| Arrays | map, filter, reduce | for loops when functional works |
| Objects | Spread operator | Object.assign |
| Strings | Template literals | String concatenation |
| DOM | React/Vue/Framework | Direct manipulation |
| Events | Event delegation | Many individual listeners |
| State | Immutable updates | Direct mutation |
| Errors | Try/catch, Error boundaries | Silent failures |