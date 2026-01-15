#!/bin/bash
# ============================================================================
# Orchestra Example Project Initializer
# ============================================================================
#
# This is an EXAMPLE script for setting up a TeneT.jl → PyTorch translation.
# Copy and modify for your own project.
#
# Expected directory layout after running:
#   ~/works/
#   ├── TeneT.jl/        # src (already cloned)
#   ├── orchestra/       # this repo
#   └── pytenet/         # created by this script
#
# Usage:
#   cd ~/works
#   git clone git@github.com:someone/TeneT.jl.git
#   git clone git@github.com:qiyang-ustc/orchestra.git
#   ./orchestra/scripts/example-init.sh git@github.com:you/pytenet.git
#
# ============================================================================

set -e

DST_REMOTE=${1:?Usage: $0 <dst-remote-url>}

# Get the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ORCHESTRA_DIR="$(dirname "$SCRIPT_DIR")"
WORKS_DIR="$(dirname "$ORCHESTRA_DIR")"

PROJECT_NAME="pytenet"
PROJECT_DIR="$WORKS_DIR/$PROJECT_NAME"
SRC_DIR="$WORKS_DIR/TeneT.jl"

echo "=== Orchestra Example Project Initializer ==="
echo ""
echo "Works dir:  $WORKS_DIR"
echo "Source:     $SRC_DIR"
echo "Project:    $PROJECT_DIR"
echo "Remote:     $DST_REMOTE"
echo ""

# Check src exists
if [ ! -d "$SRC_DIR" ]; then
    echo "ERROR: Source not found at $SRC_DIR"
    echo "Please clone TeneT.jl first:"
    echo "  cd $WORKS_DIR"
    echo "  git clone git@github.com:someone/TeneT.jl.git"
    exit 1
fi

# Check project doesn't exist
if [ -d "$PROJECT_DIR" ]; then
    echo "ERROR: Project directory already exists: $PROJECT_DIR"
    echo "Remove it first if you want to start fresh:"
    echo "  rm -rf $PROJECT_DIR"
    exit 1
fi

echo "Creating project..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Initialize git
git init

# Copy orchestra framework files
cp "$ORCHESTRA_DIR/CLAUDE.md" .
cp "$ORCHESTRA_DIR/VERIFICATION_LEVELS.md" .
cp "$ORCHESTRA_DIR/EQUIVALENCE_TYPES.md" .
cp "$ORCHESTRA_DIR/TRANSLATION_ORDER.md" .
cp "$ORCHESTRA_DIR/ATOMIC_COMMIT.md" .

# Create directory structure
mkdir -p notes
mkdir -p tests/ground_truth
mkdir -p docs
mkdir -p pytenet  # dst package

# Create orchestra.yaml (hardcoded for this example)
cat > orchestra.yaml << 'EOF'
# ============================================================================
# ORCHESTRA DECLARATION (v0.1 - MVP)
# ============================================================================

# Source code (read-only) - Original Julia library
src: ../TeneT.jl

# Target location (local, read-write)
dst: ./pytenet

# Framework/language
framework: julia -> pytorch

# ----------------------------------------------------------------------------
# Human Notes
# ----------------------------------------------------------------------------
notes: |
  This is a tensor network library for variational quantum simulations.

  Key things to know:
  - Julia uses 1-indexed arrays, Python uses 0-indexed
  - The core algorithm is VUMPS (variational uniform MPS)
  - Ground state energy for Heisenberg model should be negative (~-0.44/site)
  - Complex gradients: Julia uses conjugate convention, PyTorch uses Wirtinger

  Priority:
  - Start with core linear algebra (svd, qr, eigensolve)
  - Then MPS data structures
  - Then VUMPS algorithm

  Watch out for:
  - Phase ambiguity in eigenvectors
  - Sign convention in QR decomposition
  - Memory layout (column-major vs row-major)
EOF

# Create empty knowledge base
cat > notes/knowledge_base.md << 'EOF'
# Project Knowledge Base

This document contains ALL human decisions and domain knowledge.
**Agents: consult this before asking humans again.**

---

## Conventions

(Add decisions here as they are made)

---

## Domain Constraints

(Add physical/mathematical constraints here)

---

## Translation Decisions

(Add implementation choices here)

---

## Gotchas

(Add pitfalls and warnings here)
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.egg-info/
dist/
build/
.pytest_cache/
.venv/
*.npz
.DS_Store
EOF

# Create empty __init__.py
touch pytenet/__init__.py

# Initial commit
git add -A
git commit -m "init: Orchestra translation project for pytenet (TeneT.jl -> PyTorch)"

# Set remote
git remote add origin "$DST_REMOTE"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Project created at: $PROJECT_DIR"
echo ""
echo "Directory structure:"
echo "  $WORKS_DIR/"
echo "  ├── TeneT.jl/        # src (read-only)"
echo "  ├── orchestra/       # framework"
echo "  └── pytenet/         # your project"
echo "      ├── orchestra.yaml"
echo "      ├── CLAUDE.md"
echo "      ├── pytenet/     # dst package"
echo "      ├── tests/"
echo "      ├── docs/"
echo "      └── notes/"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_DIR"
echo "  git push -u origin main"
echo "  claude"
echo "  > 'Read orchestra.yaml and start translation'"
echo ""
