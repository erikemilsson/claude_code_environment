# Extended Thinking Triggers

*Version: 1.0 | Based on: Anthropic Claude Code Best Practices*

## Overview

Claude Code supports extended thinking modes that allocate more reasoning depth for complex problems. Use these trigger phrases to activate deeper analysis when needed.

## Trigger Phrases (Increasing Depth)

| Trigger | Thinking Depth | Best For |
|---------|---------------|----------|
| **"think"** | Basic extended | Simple multi-step problems |
| **"think hard"** | Thorough | Moderate complexity, debugging |
| **"think harder"** | Deep | Complex logic, multi-file changes |
| **"ultrathink"** | Maximum | Architecture decisions, difficult problems |

## When to Use Each Level

### "think" - Basic Extended Reasoning
```markdown
USE WHEN:
- Simple debugging
- Straightforward refactoring
- Basic code review
- Single-file changes

EXAMPLE PROMPTS:
- "think about why this test might be failing"
- "think through this function's logic"
- "think about potential edge cases"
```

### "think hard" - Thorough Analysis
```markdown
USE WHEN:
- Debugging complex issues
- Multi-step problem solving
- Code optimization
- API design decisions

EXAMPLE PROMPTS:
- "think hard about the best data structure here"
- "think hard about why performance is degrading"
- "think hard about error handling approaches"
```

### "think harder" - Deep Analysis
```markdown
USE WHEN:
- Complex algorithm design
- Multi-file refactoring
- Security analysis
- Integration challenges
- Difficulty 7-8 task planning

EXAMPLE PROMPTS:
- "think harder about how to restructure this module"
- "think harder about the authentication flow"
- "think harder about database schema design"
```

### "ultrathink" - Maximum Reasoning Depth
```markdown
USE WHEN:
- Major architecture decisions
- System-wide refactoring
- Complex debugging with no clear cause
- Difficulty 9-10 task analysis
- Trade-off analysis with many factors
- Breaking down complex requirements

EXAMPLE PROMPTS:
- "ultrathink about the overall system architecture"
- "ultrathink about how to migrate this legacy system"
- "ultrathink about the implications of this design choice"
- "ultrathink about breaking down this complex feature"
```

## Integration with Workflows

### Explore-Plan-Code-Commit
```markdown
PHASE: PLAN
RECOMMENDED: "think harder" or "ultrathink"

Example:
User: "Now that I've explored the codebase, ultrathink about the best
       approach to implement the caching layer"
```

### Task Breakdown
```markdown
BEFORE: Breaking down difficulty >= 8 tasks
RECOMMENDED: "ultrathink"

Example:
User: "ultrathink about how to break down this authentication system task"
```

### Architecture Review
```markdown
CONTEXT: Major design decisions
RECOMMENDED: "ultrathink"

Example:
User: "ultrathink about whether we should use microservices or monolith"
```

### Debugging
```markdown
PROGRESSIVE APPROACH:
1. Start with "think" for basic issues
2. Escalate to "think hard" if not resolved
3. Use "think harder" for persistent bugs
4. Use "ultrathink" for systemic issues

Example:
User: "think about why this fails"
[Still unclear]
User: "think harder about the root cause"
[Complex interaction discovered]
User: "ultrathink about the full system interaction"
```

## Practical Examples

### Example 1: Feature Planning
```markdown
User: "I need to add real-time notifications to the app"

Claude: "I'll explore the codebase first..."
[Reads relevant files]

User: "Now ultrathink about the implementation approach"

Claude: [Extended reasoning about WebSocket vs SSE, scaling
        considerations, message queue options, client architecture,
        failure handling, etc.]
```

### Example 2: Bug Investigation
```markdown
User: "Users are seeing intermittent 500 errors"

Claude: "Let me think about potential causes..."
[Basic analysis - identifies logging gap]

User: "think harder about what could cause intermittent failures"
[Deeper analysis - identifies race condition possibility]

User: "think harder about the database connection handling"
[Thorough analysis - finds connection pool exhaustion pattern]
```

### Example 3: Architecture Decision
```markdown
User: "We need to decide between Redux and Zustand for state management"

Claude: "Let me ultrathink about this..."

[Extended reasoning covering:
- Application complexity and growth trajectory
- Team experience and learning curve
- Bundle size implications
- DevTools and debugging capabilities
- Middleware and async handling needs
- TypeScript integration
- Community and ecosystem
- Specific use cases in this application]
```

## Best Practices

### DO:
```markdown
✅ Match thinking depth to problem complexity
✅ Start lower and escalate if needed
✅ Use ultrathink for irreversible decisions
✅ Allow time for extended responses
✅ Follow up with clarifying questions
```

### DON'T:
```markdown
❌ Use ultrathink for trivial questions
❌ Interrupt extended thinking prematurely
❌ Expect instant responses with deep thinking
❌ Skip exploration before requesting deep analysis
❌ Use on well-understood, simple tasks
```

## Integration with Task Difficulty

```markdown
TASK DIFFICULTY → RECOMMENDED TRIGGER:

1-3 (Trivial)    → No trigger needed
4-5 (Low)        → "think" if uncertain
6   (Moderate)   → "think" or "think hard"
7-8 (High)       → "think harder" before breakdown
9-10 (Extreme)   → "ultrathink" before breakdown
```

## Tips for Effective Use

1. **Provide context first** - Extended thinking works better with full context
2. **Be specific** - "ultrathink about X" is better than just "ultrathink"
3. **Allow completion** - Don't interrupt the reasoning process
4. **Follow up** - Ask clarifying questions about the analysis
5. **Trust the process** - Deeper thinking may surface non-obvious insights

## Related Commands

- `/explore-plan-code-commit` - Workflow that leverages extended thinking
- `/breakdown` - Use extended thinking before complex task decomposition
- `/complete-task` - May benefit from extended thinking at start
