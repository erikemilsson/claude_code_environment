#!/bin/bash
# Pre-commit hook: warn if sync-category files changed but version.json not bumped
#
# This hook checks whether any files in the sync-manifest.json "sync" category
# are being committed. If so, it warns that version.json should be bumped.
# The hook does NOT block the commit — it warns and lets the developer decide.
#
# NOTE: Patterns here approximate sync-manifest.json. If the manifest changes,
# update these patterns too. project-*.md files are excluded (they're in the
# manifest's "ignore" category).

# Only run in the template repo (check for system-overview.md at root)
if [ ! -f "system-overview.md" ]; then
    exit 0
fi

# Get list of staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACMR)

# Sync-category patterns from sync-manifest.json
# Directory patterns use prefix matching; explicit files use exact matching.
# project-*.md files are excluded (they're user-created, in the ignore category).
SYNC_PATTERNS=(
    ".claude/CLAUDE.md"
    ".claude/commands/"
    ".claude/agents/"
    ".claude/rules/"
    ".claude/support/reference/"
    ".claude/support/learnings/README.md"
    ".claude/support/workspace/README.md"
    ".claude/support/previous_specifications/README.md"
    ".claude/vision/README.md"
    ".claude/support/feedback/README.md"
    ".claude/hooks/"
)

# Patterns to exclude from sync detection (user-created files)
EXCLUDE_PATTERNS=(
    "project-"
)

# Check if a file should be excluded
is_excluded() {
    local file="$1"
    local basename
    basename=$(basename "$file")
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        if [[ "$basename" == $pattern* ]]; then
            return 0
        fi
    done
    return 1
}

# Check if any staged file matches a sync pattern (excluding user files)
SYNC_FILES_CHANGED=()
for file in $STAGED_FILES; do
    # Skip excluded files
    if is_excluded "$file"; then
        continue
    fi
    for pattern in "${SYNC_PATTERNS[@]}"; do
        if [[ "$file" == $pattern* ]]; then
            SYNC_FILES_CHANGED+=("$file")
            break
        fi
    done
done

# If sync files changed, check if version.json is also staged
if [ ${#SYNC_FILES_CHANGED[@]} -gt 0 ]; then
    VERSION_STAGED=false
    for file in $STAGED_FILES; do
        if [ "$file" = ".claude/version.json" ]; then
            VERSION_STAGED=true
            break
        fi
    done

    if [ "$VERSION_STAGED" = false ]; then
        echo ""
        echo "⚠️  Template sync files changed but version.json not updated:"
        for f in "${SYNC_FILES_CHANGED[@]}"; do
            echo "    $f"
        done
        echo ""
        echo "  Downstream projects using /health-check will see a stale version."
        echo "  Consider bumping template_version in .claude/version.json"
        echo ""
        echo "  Committing anyway. Run 'git commit --amend' to add the version bump."
        echo ""
    fi
fi

exit 0
