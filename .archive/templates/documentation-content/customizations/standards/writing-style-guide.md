# Writing Style Guide

## Purpose

This guide establishes consistent writing standards for all content in this project. It covers voice, tone, formatting, terminology, and grammar conventions to ensure clarity, professionalism, and accessibility.

## Voice and Tone

### Voice

**Definition**: The consistent personality and perspective of your content across all pieces.

**Default Recommendation**: Professional yet approachable
- Clear and direct without being cold
- Knowledgeable without being condescending
- Helpful without being overly casual

**Customization Questions**:
- What personality should your content convey? (Formal, conversational, friendly, authoritative)
- What impression do you want readers to have of your organization?
- What differentiates your voice from competitors?

### Tone

**Definition**: The emotional quality that varies based on context and content type.

**Tone Variations by Content Type**:

| Content Type | Tone | Example |
|-------------|------|---------|
| Getting Started Guide | Encouraging, supportive | "Let's get you up and running in just a few minutes" |
| API Reference | Neutral, precise | "Returns a 200 status code on successful authentication" |
| Troubleshooting | Empathetic, solution-focused | "If you're seeing this error, here's how to fix it" |
| Release Notes | Informative, factual | "Version 2.0 includes the following changes" |
| Blog Posts | Engaging, conversational | "We're excited to share our approach to..." |

## Person and Perspective

### Second Person (You/Your) - Recommended Default

**Use for**: Tutorials, guides, instructions, how-to content

**Benefits**:
- Direct and engaging
- Creates sense of conversation
- Clearly addresses the reader

**Examples**:
- "You can configure the settings by..."
- "Your application will now connect to..."
- "Follow these steps to deploy your project"

### First Person Plural (We/Our)

**Use for**: Explanations of design decisions, organizational perspective, collaborative language

**Examples**:
- "We designed this feature to..."
- "Our recommendation is to..."
- "We'll guide you through the process"

### Third Person (The user, developers, administrators)

**Use for**: General reference, formal documentation, describing user roles

**Examples**:
- "Administrators can grant permissions..."
- "The system logs all user actions"
- "Developers should follow these conventions"

**Avoid**: Unless specifically required for formal tone

### First Person Singular (I/My)

**Avoid in general documentation**

**Exception**: Personal blog posts, individual perspectives in multi-author content

## Active vs. Passive Voice

### Prefer Active Voice

**Active**: Subject performs the action
- "The function returns a string"
- "Click the Submit button to save changes"
- "The API validates the request parameters"

**Passive**: Subject receives the action
- "A string is returned by the function" (avoid)
- "Changes are saved when the Submit button is clicked" (avoid)
- "The request parameters are validated by the API" (avoid)

### When Passive Voice Is Acceptable

1. **When the actor is unknown or unimportant**:
   - "The database was updated overnight"
   - "Your password must be changed every 90 days"

2. **When emphasizing the action over the actor**:
   - "All requests are logged for security purposes"
   - "Data is encrypted at rest and in transit"

## Formatting Conventions

### Headings

**Capitalization**: Sentence case (capitalize only the first word and proper nouns)
- Correct: "Getting started with authentication"
- Incorrect: "Getting Started With Authentication"

**Hierarchy**:
- Use H1 (#) for page title only
- Use H2 (##) for main sections
- Use H3 (###) for subsections
- Avoid going deeper than H4 (####)

**Length**: Keep headings concise (under 60 characters when possible)

**Style**: Use descriptive, action-oriented headings
- Good: "Installing dependencies"
- Better: "Install project dependencies"
- Good: "Configuration options"
- Better: "Configure application settings"

### Lists

**When to Use**:
- Bulleted lists: Unordered items, features, options
- Numbered lists: Sequential steps, ranked items, prioritized information

**Formatting**:
- Start each item with a capital letter
- Use periods if items are complete sentences
- Omit periods if items are fragments or single words
- Maintain parallel structure (all items use same grammatical form)

**Example - Parallel Structure**:
Good:
- Configure the database
- Install dependencies
- Run the application

Bad:
- Configure the database
- Dependencies should be installed
- Running the application

### Code and Technical Elements

**Inline Code**: Use backticks for:
- Function names: `calculateTotal()`
- Variable names: `user_id`
- File names: `config.json`
- Command-line commands: `npm install`
- Short code snippets: `if (x > 0)`

**Code Blocks**: Use fenced code blocks with language specification:

```python
def hello_world():
    print("Hello, World!")
```

**UI Elements**: Use bold for clickable elements:
- Click **Save** to confirm changes
- Navigate to **Settings** > **Security**
- Select **File** > **New Project**

**Parameters and Values**: Use inline code:
- Set `timeout` to `5000`
- The `status` field returns `"active"` or `"inactive"`

### Links

**Link Text**: Use descriptive text, not "click here" or URLs
- Good: "See the [installation guide](link) for details"
- Bad: "Click [here](link) for installation"
- Bad: "Visit https://example.com/install for installation"

**External Links**: Consider adding context
- "Learn more in the [official Python documentation](link)"
- "Read the [OAuth 2.0 specification](link) for protocol details"

## Terminology and Word Choice

### Consistency

**Maintain a Glossary**: Document preferred terms for your domain
- Decide: "login" vs "log in" vs "sign in"
- Decide: "email" vs "e-mail"
- Decide: "setup" (noun) vs "set up" (verb)

**Example Decisions**:
| Preferred | Avoid | Notes |
|-----------|-------|-------|
| log in (verb) | login, sign in | "Click to log in" |
| login (noun/adj) | log in, sign in | "Enter your login credentials" |
| email | e-mail, Email | Lowercase unless starting sentence |
| set up (verb) | setup | "Set up your account" |
| setup (noun/adj) | set up | "Complete the initial setup" |

### Abbreviations and Acronyms

**First Use**: Spell out with acronym in parentheses
- "Application Programming Interface (API)"
- "Structured Query Language (SQL)"

**Subsequent Uses**: Use acronym only
- "The API returns JSON responses"

**Common Acronyms**: Don't spell out universally known terms
- OK to use directly: API, URL, HTML, CSS, JSON, XML, PDF, HTTP, HTTPS

**Latin Abbreviations**: Use English equivalents
- Use "for example" instead of "e.g."
- Use "that is" instead of "i.e."
- Use "and so on" instead of "etc."

**Exceptions**: Technical documentation where Latin is standard practice

### Jargon and Technical Language

**Know Your Audience**:
- **Developer docs**: Technical terms expected, still define complex concepts
- **End-user docs**: Avoid jargon, explain technical concepts in simple terms
- **Mixed audience**: Define terms on first use, consider glossary

**Guidelines**:
1. Use technical terms when they're the most precise way to communicate
2. Define specialized terms on first use
3. Link to definitions or glossary for complex concepts
4. Consider your audience's background knowledge

### Inclusive Language

**Use**:
- "they/their" for singular gender-neutral pronoun
- "people" instead of "guys" or "mankind"
- "allowlist/denylist" instead of "whitelist/blacklist"
- "primary/replica" instead of "master/slave"

**Examples**:
- "Each user should verify their email address"
- "The primary database replicates to three replicas"

## Grammar and Mechanics

### Contractions

**Informal Content**: Use contractions for conversational tone
- "You'll need to install..." (blog posts, tutorials)
- "We're excited to announce..." (announcements)

**Formal Content**: Avoid contractions
- "You will need to configure..." (API reference)
- "The system does not support..." (technical specifications)

**Consistency**: Choose approach per content type and stick to it

### Numbers

**Spell Out**: Numbers one through nine
- "Install three dependencies"
- "Complete the first step"

**Use Numerals**: Numbers 10 and above
- "Configure 15 environment variables"
- "Process 1000 requests per second"

**Exceptions**:
- Always use numerals for: Technical values, measurements, percentages, versions
  - "Set timeout to 5 seconds" (technical value)
  - "Version 2.0 includes..." (version number)
  - "3 GB of RAM" (measurement)

### Punctuation

**Serial Comma (Oxford Comma)**: Use it
- "Install Python, Node.js, and Docker" (clear)
- "Install Python, Node.js and Docker" (ambiguous - avoid)

**Colons**: Use to introduce lists, examples, or explanations
- "You'll need the following tools: Python, Git, and VS Code"

**Semicolons**: Use sparingly; prefer separate sentences or bulleted lists

**Em Dashes**: Use for emphasis or parenthetical information
- "The new feature—now available in beta—improves performance"

**Hyphens**: Use for compound modifiers before nouns
- "real-time updates"
- "command-line interface"
- But: "updates in real time" (no hyphen after noun)

## Accessibility

### Alt Text for Images

**Provide**: Descriptive alt text for all images
- Describe what the image shows
- Include relevant text visible in the image
- Keep it concise (under 150 characters)

**Example**:
```markdown
![Screenshot of the dashboard showing three metrics: 150 active users, 1,247 API calls, and 99.9% uptime](dashboard.png)
```

### Heading Structure

**Maintain Hierarchy**: Don't skip heading levels
- Good: H1 → H2 → H3
- Bad: H1 → H3 (skipped H2)

**Descriptive Headings**: Make headings clear and meaningful
- Screen readers use headings for navigation
- Users should understand content structure from headings alone

### Link Context

**Descriptive Links**: Ensure link text makes sense out of context
- Good: "Read the [API authentication guide](link)"
- Bad: "Click [here](link)" (no context for screen readers)

### Lists for Structure

**Use Lists**: For better scannability and screen reader support
- Break up long paragraphs with bulleted lists
- Use numbered lists for sequential information
- Maintain parallel structure

## Content-Specific Guidelines

### Code Examples

**Complete and Runnable**: Provide working code when possible
- Include necessary imports
- Show realistic variable names
- Add comments for clarity

**Syntax Highlighting**: Always specify language in code blocks

**Context**: Explain what the code does before or after the example

### Error Messages

**Format**: Use code formatting for exact error text
- "If you see `Error: Connection timeout`, check your network settings"

**Solutions**: Always provide resolution steps
- Don't just show the error
- Explain what causes it
- Provide clear steps to fix it

### Warnings and Notes

**Use Callouts**: For important information

**Types**:
- **Note**: Additional information, tips, optional details
- **Important**: Critical information users should know
- **Warning**: Potential problems or risks
- **Caution**: Actions that can't be undone or have serious consequences

**Format** (if your platform supports it):
```markdown
> **Note**: This feature requires API version 2.0 or later.

> **Warning**: Deleting a project cannot be undone.
```

## Review Checklist

Before publishing, verify:

- [ ] Voice and tone appropriate for content type
- [ ] Active voice used (passive only where appropriate)
- [ ] Headings use sentence case
- [ ] Lists have parallel structure
- [ ] Code elements properly formatted
- [ ] Links use descriptive text
- [ ] Terminology consistent with glossary
- [ ] Acronyms spelled out on first use
- [ ] Contractions match content formality level
- [ ] Serial commas used
- [ ] Images have alt text
- [ ] Heading hierarchy maintained
- [ ] Gender-neutral language used
- [ ] No jargon without definitions
- [ ] Code examples are complete and tested

## Customization Instructions

To adapt this guide for your project:

1. **Define Your Voice**: Update the voice section with your specific personality
2. **Choose Person**: Decide on second person, first person plural, or third person
3. **Set Formality Level**: Determine use of contractions, technical depth
4. **Create Glossary**: Document your specific terminology decisions
5. **Add Industry Terms**: Include domain-specific jargon and definitions
6. **Set Tone Variations**: Define tone for each of your content types
7. **Update Examples**: Replace generic examples with ones from your domain

## Resources

**Grammar and Style**:
- The Chicago Manual of Style
- AP Stylebook (for news/blog content)
- Microsoft Writing Style Guide (for technical content)
- Google Developer Documentation Style Guide

**Readability**:
- Hemingway Editor (readability scoring)
- Grammarly (grammar and style checking)
- LanguageTool (open-source grammar checking)

**Accessibility**:
- WCAG Guidelines
- WebAIM resources
- A11Y Project
