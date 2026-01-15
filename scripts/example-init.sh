#!/bin/bash
# ============================================================================
# Orchestra Example Project Initializer
# ============================================================================
#
# This is an EXAMPLE script for setting up a TeneT.jl → PyTorch translation.
# Run this script FROM WITHIN the orchestra directory after cloning it.
#
# The orchestra repo itself becomes your project.
#
# Expected directory layout after running:
#   ~/works/
#   ├── TeneT.jl/        # src (already cloned, read-only)
#   └── pytenet/         # orchestra cloned as pytenet (your project)
#       ├── orchestra.yaml
#       ├── CLAUDE.md
#       └── pytenet/     # dst package (inside project)
#
# Usage:
#   cd ~/works
#   git clone git@github.com:someone/TeneT.jl.git
#   git clone git@github.com:qiyang-ustc/orchestra.git pytenet
#   cd pytenet
#   ./scripts/example-init.sh git@github.com:you/pytenet.git
#
# ============================================================================

set -e

DST_REMOTE=${1:?Usage: $0 <dst-remote-url>}

# Get the script and project directories
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PARENT_DIR="$(dirname "$PROJECT_DIR")"

# Source is expected to be a sibling directory
SRC_DIR="$PARENT_DIR/TeneT.jl"

echo "=== Orchestra Example Project Initializer ==="
echo ""
echo "Project dir: $PROJECT_DIR"
echo "Source:      $SRC_DIR"
echo "Remote:      $DST_REMOTE"
echo ""

# Check src exists
if [ ! -d "$SRC_DIR" ]; then
    echo "ERROR: Source not found at $SRC_DIR"
    echo "Please clone TeneT.jl first:"
    echo "  cd $PARENT_DIR"
    echo "  git clone git@github.com:someone/TeneT.jl.git"
    exit 1
fi

# Work in project directory
cd "$PROJECT_DIR"

echo "Configuring project..."

# Create directory structure (if not exists)
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

# Update .gitignore (append if needed)
if [ ! -f .gitignore ]; then
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
fi

# Create empty __init__.py
touch pytenet/__init__.py

# Change remote to user's repo
git remote set-url origin "$DST_REMOTE"

# Stage and commit changes
git add -A
git commit -m "init: Configure for TeneT.jl -> PyTorch translation"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Directory structure:"
echo "  $PARENT_DIR/"
echo "  ├── TeneT.jl/        # src (read-only)"
echo "  └── $(basename $PROJECT_DIR)/         # your project"
echo "      ├── orchestra.yaml"
echo "      ├── CLAUDE.md"
echo "      ├── pytenet/     # dst package"
echo "      ├── tests/"
echo "      ├── docs/"
echo "      └── notes/"
echo ""
echo "Next steps:"
echo "  git push -u origin main"
echo "  claude"
echo "  > 'Read orchestra.yaml and start translation'"
echo ""
