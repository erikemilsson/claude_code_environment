# Claude 4 Model Knowledge Reference

*Version: 1.0 | Created: 2025-12-16*

## Model Identification

### Opus 4.1
- **Model ID:** `claude-opus-4-1-20250805`
- **API Name:** `claude-3-opus-20240229` (legacy), `claude-opus-4.1` (current)
- **Knowledge Cutoff:** January 2025
- **Context Window:** 200K tokens
- **Primary Use:** Complex reasoning, code generation, long-context analysis

### Sonnet 4.5
- **Model ID:** `claude-sonnet-4-5-20250929`
- **API Name:** `claude-3-5-sonnet-20241022` (legacy), `claude-sonnet-4.5` (current)
- **Knowledge Cutoff:** April 2024
- **Context Window:** 200K tokens
- **Primary Use:** Balanced performance, general tasks, rapid iteration

## Knowledge Boundaries

### What Claude 4 Knows Natively

#### ✅ INCLUDED in Training Data

**Programming & Technology (up to cutoff):**
- Programming languages syntax and best practices
- Frameworks and libraries (versions before cutoff)
- Software architecture patterns
- Database systems and SQL
- Cloud platforms (AWS, Azure, GCP basics)
- Git and version control
- Testing frameworks and methodologies

**General Knowledge:**
- Mathematics and algorithms
- Scientific concepts
- Historical events (up to cutoff)
- Language and writing conventions
- Business and economics fundamentals

**Specific Versions Known:**
- Python: Up to 3.11/3.12
- Node.js: Up to v20
- React: Up to v18
- TypeScript: Up to v5.0
- Major frameworks as of early 2024

### What Requires External Sources

#### ❌ NOT in Training Data

**Current Information:**
- Events after knowledge cutoff
- Latest software releases
- Current stock prices/crypto values
- Today's news and weather
- Recent research papers
- Updated documentation
- Live API changes

**Real-time Data:**
- Current time/date
- Live system status
- Running process information
- Network connectivity
- Database contents
- User-specific data

**Post-Cutoff Technology:**
- Framework versions released after cutoff
- New programming languages
- Recent security vulnerabilities
- Latest best practices updates
- New cloud services
- Recent API changes

## Tool Usage Guidelines

### When to Use Claude Native Knowledge

```markdown
USE CLAUDE DIRECTLY FOR:
✅ Coding standard patterns
✅ Algorithm implementation
✅ Syntax and language features
✅ Established best practices
✅ Mathematical calculations
✅ Logical reasoning
✅ Code review and refactoring
```

### When to Use Web Search/Gemini MCP

```markdown
USE EXTERNAL SOURCES FOR:
❌ Current events or news
❌ Latest framework versions
❌ Recent security advisories
❌ Updated API documentation
❌ Real-time data
❌ Post-2024 technologies
❌ Specific version compatibility
```

## Decision Framework

### Determining Information Currency

```markdown
IF user asks about:
  "latest" → USE Web Search
  "current" → USE Web Search
  "today's" → USE Web Search
  "recent" → USE Web Search
  "2025" or later → USE Web Search
  Specific version > known → USE Web Search
ELSE:
  USE Claude native knowledge
```

### Gemini MCP Integration

```markdown
# When to Route to Gemini

1. GROUNDING REQUIRED:
   - Current regulations
   - Market trends
   - Industry news
   - Recent research

2. DOMAIN EXPERTISE:
   - Specialized industry knowledge
   - Compliance requirements
   - Regional regulations
   - Business intelligence

3. VERIFICATION:
   - Fact-checking current claims
   - Validating recent changes
   - Confirming latest versions
```

## Model Capabilities

### Claude 4 Strengths

**Opus 4.1:**
- Complex multi-step reasoning
- Large codebase analysis
- Architecture design
- Long document processing
- Creative problem-solving

**Sonnet 4.5:**
- Rapid code generation
- Quick iterations
- Standard implementations
- Documentation writing
- Code review

### Processing Characteristics

**Both Models:**
- Parallel tool execution
- Explicit instruction following
- Proactive action taking
- Structured output generation
- Error recovery patterns

## Self-Identification

### Model Announcement Strings

```markdown
# Opus 4.1
"You are powered by the model named Opus 4.1. The exact model ID is claude-opus-4-1-20250805."

# Sonnet 4.5
"You are powered by the model named Sonnet 4.5. The exact model ID is claude-sonnet-4-5-20250929."
```

### Capability Disclosure

```markdown
When asked about capabilities:
1. State model name and version
2. Mention knowledge cutoff date
3. Explain tool availability
4. Clarify external source access
```

## Version-Specific Knowledge

### Framework Versions Known

| Framework | Latest Known Version | Cutoff Date |
|-----------|---------------------|-------------|
| React | 18.2.0 | April 2024 |
| Vue | 3.4 | April 2024 |
| Angular | 17 | April 2024 |
| Next.js | 14 | April 2024 |
| Django | 5.0 | April 2024 |
| Flask | 3.0 | April 2024 |
| Express | 4.18 | April 2024 |
| Spring Boot | 3.2 | April 2024 |

### Language Versions Known

| Language | Latest Known Version | Features Known |
|----------|---------------------|----------------|
| Python | 3.12 | Pattern matching, walrus operator |
| JavaScript | ES2023 | Array methods, private fields |
| TypeScript | 5.3 | Decorators, satisfies operator |
| Java | 21 LTS | Records, pattern matching |
| C# | 12 | Primary constructors |
| Go | 1.21 | Built-in functions |
| Rust | 1.75 | Async traits |

## Information Verification

### Confidence Levels

```markdown
HIGH CONFIDENCE (90-100%):
- Core programming concepts
- Established patterns
- Mathematical operations
- Logical reasoning

MEDIUM CONFIDENCE (60-89%):
- Specific version features
- Framework details
- Best practices

LOW CONFIDENCE (<60%):
- Latest updates
- Specific dates
- Version compatibility
- Current statistics

When confidence < 70%:
→ Recommend Web Search
→ Suggest Gemini MCP
→ Acknowledge uncertainty
```

## Quick Reference

### Always Use External Sources For:

1. **Dates/Time:** Current date, time zones, calendars
2. **Live Data:** Stock prices, weather, sports scores
3. **Recent Events:** News, releases, announcements
4. **Versions:** Latest releases, compatibility
5. **Documentation:** Current API docs, changelogs
6. **Statistics:** Current numbers, trends, metrics

### Never Need External Sources For:

1. **Logic:** Algorithms, data structures, patterns
2. **Syntax:** Language grammar, basic usage
3. **Math:** Calculations, formulas, proofs
4. **Concepts:** Programming paradigms, principles
5. **Standards:** HTTP, SQL, REST, GraphQL basics
6. **History:** Events before 2024

## Implementation Guidelines

### Handling Knowledge Gaps

```markdown
When encountering knowledge boundary:

1. ACKNOWLEDGE limitation:
   "My knowledge extends to [date]"

2. SUGGEST alternative:
   "For current information, I'll use Web Search"

3. EXECUTE search:
   Use WebSearch or mcp__gemini tools

4. INTEGRATE results:
   Combine native knowledge with current data
```

### Model Selection for Tasks

```markdown
Choose Opus 4.1 when:
- Complex reasoning required
- Large context processing
- Multi-step planning
- Architecture design

Choose Sonnet 4.5 when:
- Speed is priority
- Standard implementations
- Iterative development
- Quick responses needed
```

## Conclusion

This reference serves as the authoritative guide for understanding Claude 4's knowledge boundaries and capabilities. Always verify currency of information when dealing with:
- Specific versions
- Recent developments
- Time-sensitive data
- External systems

Default to native knowledge for conceptual and logical tasks, use external sources for current information.