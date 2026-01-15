#!/bin/bash
# ============================================================================
# Orchestra Reset Script
# ============================================================================
#
# Resets the project to orchestra's initial state, removing all translation
# progress. Use this to:
#   1. Start fresh after a failed attempt
#   2. Pull updates from orchestra upstream
#   3. Test the framework with clean state
#
# What gets REMOVED:
#   - dst package contents (translated code)
#   - tests/ (except ground_truth/)
#   - docs/ (generated documentation)
#   - reports/ (verification reports)
#
# What gets KEPT:
#   - orchestra.yaml (project config)
#   - CLAUDE.md and framework docs
#   - notes/knowledge_base.md (human knowledge)
#   - tests/ground_truth/ (oracle data)
#   - .git history
#
# Usage:
#   ./scripts/reset.sh              # Interactive mode (asks for confirmation)
#   ./scripts/reset.sh --force      # Skip confirmation
#   ./scripts/reset.sh --pull       # Reset and pull from orchestra upstream
#
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Parse args
FORCE=false
PULL_UPSTREAM=false
for arg in "$@"; do
    case $arg in
        --force|-f) FORCE=true ;;
        --pull|-p) PULL_UPSTREAM=true ;;
    esac
done

echo "=== Orchestra Reset ==="
echo ""
echo "Project: $PROJECT_DIR"
echo ""

# Read dst from orchestra.yaml
if [ -f orchestra.yaml ]; then
    DST=$(grep "^dst:" orchestra.yaml | sed 's/dst: *//' | tr -d '"' | tr -d "'")
    DST_DIR="$PROJECT_DIR/$DST"
else
    echo "WARNING: orchestra.yaml not found"
    DST_DIR=""
fi

echo "Will remove:"
[ -n "$DST_DIR" ] && [ -d "$DST_DIR" ] && echo "  - $DST (translated code)"
[ -d "tests" ] && echo "  - tests/ (except ground_truth/)"
[ -d "docs" ] && echo "  - docs/"
[ -d "reports" ] && echo "  - reports/"
echo ""
echo "Will keep:"
echo "  - orchestra.yaml"
echo "  - CLAUDE.md, framework docs"
echo "  - notes/knowledge_base.md"
echo "  - tests/ground_truth/"
echo "  - .git history"
echo ""

if [ "$FORCE" != true ]; then
    read -p "Continue? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

echo "Resetting..."

# Remove dst package contents (keep directory with __init__.py)
if [ -n "$DST_DIR" ] && [ -d "$DST_DIR" ]; then
    find "$DST_DIR" -type f ! -name '__init__.py' -delete
    find "$DST_DIR" -type d -empty -delete 2>/dev/null || true
    # Recreate __init__.py if it was the only thing
    mkdir -p "$DST_DIR"
    touch "$DST_DIR/__init__.py"
    echo "  ✓ Cleared $DST"
fi

# Remove tests (except ground_truth/)
if [ -d "tests" ]; then
    find tests -type f ! -path "tests/ground_truth/*" -delete
    find tests -type d -empty ! -name "ground_truth" -delete 2>/dev/null || true
    echo "  ✓ Cleared tests/ (kept ground_truth/)"
fi

# Remove docs/
if [ -d "docs" ]; then
    rm -rf docs/*
    echo "  ✓ Cleared docs/"
fi

# Remove reports/
if [ -d "reports" ]; then
    rm -rf reports/*
    echo "  ✓ Cleared reports/"
fi

# Pull from upstream if requested
if [ "$PULL_UPSTREAM" = true ]; then
    echo ""
    echo "Pulling from orchestra upstream..."

    # Check if upstream remote exists
    if ! git remote | grep -q "^upstream$"; then
        echo "Adding orchestra upstream remote..."
        git remote add upstream git@github.com:qiyang-ustc/orchestra.git
    fi

    # Fetch and merge
    git fetch upstream
    git merge upstream/main --no-edit -m "chore: Merge orchestra upstream updates"
    echo "  ✓ Merged upstream/main"
fi

echo ""
echo "=== Reset Complete ==="
echo ""
echo "Project is ready for fresh translation."
echo "Run 'claude' to start."
echo ""
