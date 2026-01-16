# Visual Iteration Workflow

*Version: 1.0 | Based on: Anthropic Claude Code Best Practices*

## Overview

Visual iteration is a powerful workflow for UI/UX development where you provide design mocks, Claude implements them, and you iterate through visual comparison until the implementation matches the design.

## Core Workflow

### Phase 1: Provide Visual Reference

**Methods to Share Visuals:**

```markdown
1. SCREENSHOT (Recommended for macOS):
   - Capture: Cmd + Ctrl + Shift + 4
   - Paste directly: Ctrl + V in Claude Code

2. DRAG AND DROP:
   - Drag image file into Claude Code terminal/chat

3. FILE PATH:
   - "Here's the design mock: /path/to/design.png"

4. URL (if accessible):
   - "Implement this design: https://figma.com/..."
```

**What to Include:**
```markdown
ESSENTIAL:
□ Full design mock or screenshot
□ Specific component to implement
□ Expected behavior/interactions

HELPFUL:
□ Color values if specific
□ Font specifications
□ Spacing requirements
□ Responsive breakpoints
```

### Phase 2: Initial Implementation

**Prompt Pattern:**
```markdown
User: "Implement this component based on the attached design.
[Attached: design-mock.png]

Requirements:
- Match the visual design closely
- Use [React/Vue/etc.]
- Follow existing component patterns in src/components/"
```

**Claude's Approach:**
1. Analyze the visual design
2. Identify components, colors, spacing
3. Check existing codebase patterns
4. Implement matching component
5. Report what was created

### Phase 3: Visual Verification

**Screenshot the Result:**

Using Playwright MCP (if available):
```markdown
User: "Take a screenshot of the implemented component"

Claude: [Uses mcp__playwright__browser_take_screenshot]
```

Manual verification:
```markdown
User: "I've attached a screenshot of the result. Compare to original."
[Attached: implementation-screenshot.png]
```

### Phase 4: Iterate (2-3 Rounds Typical)

**Feedback Pattern:**
```markdown
Round 1:
User: "The button spacing is off - should have more padding.
       The header text should be bold.
       Colors look good."

Round 2:
User: "Much better! Just fix the border radius on cards -
       should be more rounded like the design."

Round 3:
User: "Perfect! Matches the design. Let's commit."
```

### Phase 5: Commit

```markdown
User: "Looks good, commit this with message about matching design spec"

Claude: [Creates commit with visual implementation details]
```

## Integration with Playwright MCP

When Playwright MCP is available, automate visual verification:

### Automated Screenshot Workflow
```markdown
1. NAVIGATE to component:
   mcp__playwright__browser_navigate to localhost:3000/component-preview

2. CAPTURE initial state:
   mcp__playwright__browser_take_screenshot

3. IMPLEMENT changes:
   [Edit component files]

4. REFRESH and capture:
   mcp__playwright__browser_navigate (refresh)
   mcp__playwright__browser_take_screenshot

5. COMPARE visually:
   Analyze differences between screenshots
```

### Example Session
```markdown
User: "Implement the attached card design and show me the result"
[Attached: card-design.png]

Claude: "I'll implement this and capture a screenshot for comparison.

First, let me navigate to the dev server..."
[mcp__playwright__browser_navigate: http://localhost:3000]

"Now implementing the card component..."
[Creates/edits component files]

"Taking screenshot of the result..."
[mcp__playwright__browser_take_screenshot]

"Here's the comparison:
- Card layout: Matches design
- Colors: Need adjustment (current: #333, design appears: #2d2d2d)
- Spacing: Padding looks correct
- Border: Missing subtle shadow from design

Shall I fix the color and add the shadow?"
```

## Visual Comparison Techniques

### Side-by-Side Analysis
```markdown
COMPARISON CHECKLIST:
□ Layout structure matches
□ Spacing/margins correct
□ Colors accurate
□ Typography matches (font, size, weight)
□ Border/shadow effects present
□ Icons/images positioned correctly
□ Responsive behavior (if applicable)
```

### Pixel-Perfect vs. Spirit Match
```markdown
PIXEL-PERFECT (when required):
- Exact color values
- Precise spacing (px values)
- Exact font sizes
- Shadow specifications

SPIRIT MATCH (usually sufficient):
- Overall layout correct
- Visual hierarchy preserved
- Colors "close enough"
- Responsive and functional
```

## Common Visual Issues

### Layout Problems
```markdown
SYMPTOM: Elements misaligned
FIX: Check flexbox/grid properties, margin/padding values

SYMPTOM: Wrong sizing
FIX: Verify width/height, check responsive units

SYMPTOM: Overflow issues
FIX: Check overflow properties, container sizing
```

### Styling Problems
```markdown
SYMPTOM: Colors don't match
FIX: Use color picker on design, verify hex values

SYMPTOM: Fonts look different
FIX: Check font-family, font-weight, letter-spacing

SYMPTOM: Missing visual effects
FIX: Add shadows, borders, gradients as specified
```

### Interaction Problems
```markdown
SYMPTOM: Hover states missing
FIX: Add :hover pseudo-class styles

SYMPTOM: Animation not smooth
FIX: Use transitions, check easing functions

SYMPTOM: Click targets too small
FIX: Increase padding, add larger hit area
```

## Best Practices

### DO:
```markdown
✅ Provide clear, high-quality design mocks
✅ Specify which component/section to implement
✅ Give specific feedback on differences
✅ Iterate in focused rounds (2-3 typically sufficient)
✅ Commit after visual approval
✅ Note any intentional deviations
```

### DON'T:
```markdown
❌ Expect pixel-perfect match always
❌ Change requirements mid-iteration
❌ Skip visual verification step
❌ Iterate endlessly (diminishing returns)
❌ Ignore responsive considerations
```

## Prompt Templates

### Initial Implementation
```markdown
"Implement [component name] based on the attached design.

Design: [attached image]
Framework: [React/Vue/etc.]
Location: [where to create/modify]

Key requirements:
- [specific requirement 1]
- [specific requirement 2]

Reference existing: [similar component to follow]"
```

### Iteration Feedback
```markdown
"Comparing to the design:

CORRECT:
- [what matches]

NEEDS ADJUSTMENT:
- [specific issue 1] - [how to fix]
- [specific issue 2] - [how to fix]

Please fix these issues."
```

### Approval
```markdown
"Looks good! This matches the design.

Please commit with:
- Summary of component implemented
- Reference to design spec if applicable
- Note any intentional deviations"
```

## Integration with Task System

```markdown
VISUAL IMPLEMENTATION TASK WORKFLOW:

1. CREATE task for visual implementation
2. ATTACH design reference in task description
3. START task with /complete-task
4. IMPLEMENT following visual workflow
5. ITERATE until approved
6. COMMIT implementation
7. MARK task complete
```

## Related Documentation

- `.claude/commands/explore-plan-code-commit.md` - General implementation workflow
- `.claude/reference/multi-claude-patterns.md` - Writer + Reviewer for visual QA
- MCP Playwright documentation for automated screenshots
