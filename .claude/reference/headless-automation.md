# Headless Mode & CI/CD Automation

*Version: 1.0 | Based on: Anthropic Claude Code Best Practices*

## Overview

Claude Code can run in headless mode for automation, CI/CD pipelines, and programmatic orchestration. This enables powerful patterns like task fan-out, data pipelining, and automated code operations.

## Basic Headless Usage

### Command Syntax
```bash
# Basic headless execution
claude -p "your prompt here"

# With JSON output for parsing
claude -p "your prompt here" --output-format stream-json

# Non-interactive with timeout
claude -p "your prompt here" --no-input --timeout 300
```

### Output Formats
```markdown
FORMATS:
- text (default): Human-readable output
- stream-json: Newline-delimited JSON for parsing
- json: Single JSON object (when complete)
```

## Fan-Out Pattern

**Purpose:** Distribute work across multiple Claude invocations.

### Basic Fan-Out
```bash
#!/bin/bash
# fan-out-analysis.sh

# Step 1: Generate task list
tasks=$(claude -p "List all Python files that need security review. Output as JSON array of file paths." --output-format stream-json | jq -r '.files[]')

# Step 2: Process each task in parallel
echo "$tasks" | parallel -j4 '
  claude -p "Review {} for security vulnerabilities. Output findings as JSON." \
    --output-format stream-json >> results/{/.}-security.json
'

# Step 3: Aggregate results
claude -p "Summarize security findings from results/*.json" > security-report.md
```

### Fan-Out with Progress Tracking
```bash
#!/bin/bash
# fan-out-with-progress.sh

TASK_FILE=".claude/scratchpad/fan-out-tasks.json"
RESULTS_DIR=".claude/scratchpad/results"
mkdir -p "$RESULTS_DIR"

# Generate tasks
claude -p "Analyze codebase and create task list for refactoring. Output as JSON with id, file, and description for each task." \
  --output-format stream-json > "$TASK_FILE"

# Process with progress
total=$(jq '. | length' "$TASK_FILE")
current=0

jq -c '.[]' "$TASK_FILE" | while read task; do
  current=$((current + 1))
  id=$(echo "$task" | jq -r '.id')
  file=$(echo "$task" | jq -r '.file')

  echo "Processing $current/$total: $file"

  claude -p "Refactor $file according to: $(echo "$task" | jq -r '.description')" \
    --output-format stream-json > "$RESULTS_DIR/$id.json"

  echo "Completed: $id" >> "$RESULTS_DIR/progress.log"
done

echo "Fan-out complete. Results in $RESULTS_DIR"
```

## Pipeline Pattern

**Purpose:** Chain Claude operations in data processing pipelines.

### Basic Pipeline
```bash
#!/bin/bash
# analysis-pipeline.sh

# Stage 1: Extract
cat requirements.txt | \
  claude -p "Parse these dependencies and output as JSON with name, version, and category" \
    --output-format stream-json | \

# Stage 2: Transform
  claude -p "For each dependency, check if newer version exists. Add 'latest_version' and 'update_available' fields" \
    --output-format stream-json | \

# Stage 3: Filter
  jq 'select(.update_available == true)' | \

# Stage 4: Report
  claude -p "Create a dependency update report from this JSON. Include risk assessment for each update." \
    > dependency-report.md
```

### Multi-Stage Pipeline
```bash
#!/bin/bash
# code-quality-pipeline.sh

FILE=$1

# Pipeline stages
claude -p "Analyze $FILE for code smells" --output-format stream-json | \
claude -p "Prioritize these issues by severity" --output-format stream-json | \
claude -p "Generate fix suggestions for top 3 issues" --output-format stream-json | \
claude -p "Create a refactoring plan" > "refactor-plan-$(basename $FILE .js).md"
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Get changed files
        id: changed
        run: |
          echo "files=$(git diff --name-only origin/main...HEAD | tr '\n' ' ')" >> $GITHUB_OUTPUT

      - name: Run Claude Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Review these changed files for issues: ${{ steps.changed.outputs.files }}" \
            --output-format stream-json > review.json

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = JSON.parse(fs.readFileSync('review.json', 'utf8'));
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: review.summary
            });
```

### GitLab CI

```yaml
# .gitlab-ci.yml
claude-analysis:
  stage: test
  image: node:20
  before_script:
    - npm install -g @anthropic-ai/claude-code
  script:
    - |
      claude -p "Analyze code quality for files changed in this MR" \
        --output-format stream-json > analysis.json
    - cat analysis.json | jq '.issues[] | select(.severity == "high")' > high-severity.json
    - |
      if [ -s high-severity.json ]; then
        echo "High severity issues found!"
        cat high-severity.json
        exit 1
      fi
  artifacts:
    paths:
      - analysis.json
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Get staged files
staged_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|ts|py)$')

if [ -n "$staged_files" ]; then
  echo "Running Claude pre-commit check..."

  result=$(claude -p "Quick review of these staged files for obvious issues: $staged_files" \
    --output-format stream-json --timeout 30)

  issues=$(echo "$result" | jq '.blocking_issues | length')

  if [ "$issues" -gt 0 ]; then
    echo "Blocking issues found:"
    echo "$result" | jq '.blocking_issues[]'
    exit 1
  fi
fi

exit 0
```

## Safe YOLO Mode

**Purpose:** Uninterrupted automation in isolated environments.

```markdown
REQUIREMENTS FOR SAFE YOLO MODE:
✅ Isolated container/VM
✅ No network access (or limited)
✅ No access to production systems
✅ Disposable environment
✅ Version-controlled source
```

### Docker Setup
```dockerfile
# Dockerfile.claude-automation
FROM node:20-slim

# Install Claude Code
RUN npm install -g @anthropic-ai/claude-code

# Create non-root user
RUN useradd -m claude
USER claude
WORKDIR /workspace

# No network by default
# Run with: docker run --network none
```

### Usage
```bash
# Build isolated environment
docker build -f Dockerfile.claude-automation -t claude-auto .

# Run with YOLO mode in isolation
docker run --network none -v $(pwd):/workspace claude-auto \
  claude --dangerously-skip-permissions -p "Run full lint fix on all files"
```

### Safe YOLO Use Cases
```markdown
APPROPRIATE:
✅ Linting and formatting fixes
✅ Boilerplate generation
✅ Test scaffolding
✅ Documentation generation
✅ Code migration scripts

INAPPROPRIATE:
❌ Production deployments
❌ Database operations
❌ File deletion at scale
❌ Network operations
❌ Credential handling
```

## Batch Processing Scripts

### Batch Refactoring
```bash
#!/bin/bash
# batch-refactor.sh

PATTERN=$1  # e.g., "*.js"
INSTRUCTION=$2  # e.g., "Convert to TypeScript"

find . -name "$PATTERN" -type f | while read file; do
  echo "Processing: $file"

  claude -p "Refactor $file: $INSTRUCTION" \
    --output-format stream-json \
    > ".claude/scratchpad/refactor-$(basename $file).json"
done
```

### Batch Documentation
```bash
#!/bin/bash
# batch-document.sh

# Find all undocumented functions
claude -p "Find all exported functions without JSDoc in src/" \
  --output-format stream-json | \
  jq -r '.functions[] | "\(.file):\(.line)"' | \
  while read location; do
    claude -p "Add JSDoc documentation to the function at $location"
  done
```

## Output Parsing

### JSON Stream Processing
```bash
# Process streaming JSON output
claude -p "Analyze codebase" --output-format stream-json | \
  while IFS= read -r line; do
    type=$(echo "$line" | jq -r '.type // empty')
    case "$type" in
      "progress")
        echo "Progress: $(echo "$line" | jq -r '.message')"
        ;;
      "finding")
        echo "$line" >> findings.jsonl
        ;;
      "complete")
        echo "Analysis complete"
        ;;
    esac
  done
```

### Extracting Specific Data
```bash
# Extract just the summary
claude -p "Summarize this file" --output-format stream-json | \
  jq -s 'map(select(.type == "summary")) | .[0].content'

# Extract all issues
claude -p "Find bugs in code" --output-format stream-json | \
  jq -s '[.[] | select(.type == "issue")]'
```

## Error Handling

### Robust Script Pattern
```bash
#!/bin/bash
set -euo pipefail

run_claude() {
  local prompt=$1
  local output_file=$2
  local max_retries=3
  local retry=0

  while [ $retry -lt $max_retries ]; do
    if claude -p "$prompt" --output-format stream-json > "$output_file" 2>&1; then
      return 0
    fi

    retry=$((retry + 1))
    echo "Attempt $retry failed, retrying..."
    sleep $((retry * 2))
  done

  echo "Failed after $max_retries attempts"
  return 1
}

# Usage
run_claude "Analyze code" "analysis.json" || exit 1
```

### Timeout Handling
```bash
# With timeout
timeout 60 claude -p "Quick analysis" --output-format stream-json || {
  echo "Claude timed out"
  exit 1
}
```

## Best Practices

### DO:
```markdown
✅ Use --output-format stream-json for parsing
✅ Implement retry logic for reliability
✅ Set appropriate timeouts
✅ Use isolated environments for YOLO mode
✅ Log all operations for debugging
✅ Validate JSON output before processing
```

### DON'T:
```markdown
❌ Use YOLO mode with network access
❌ Process unbounded input without limits
❌ Ignore error handling
❌ Run destructive operations without backup
❌ Parse output without validation
```

## Related Documentation

- `.claude/reference/multi-claude-patterns.md` - Coordinating multiple instances
- `.claude/reference/permission-configuration.md` - Permission handling
- `.claude/commands/explore-plan-code-commit.md` - Interactive workflow
