# Atomic Commit Specification

Every translation unit produces exactly one atomic commit containing all artifacts for that unit.

## What is a Translation Unit?

A translation unit is the smallest independently verifiable piece of translation:
- A single function
- A single class
- A small module (if tightly coupled)

**Rule: If you can't verify it independently, it's too big. Split it.**

## Atomic Commit Structure

```
commit: "feat(<module>): translate <function_name> [L<n>]"

files changed:
  ├── <package>/<module>.py           # Target code
  ├── tests/test_<module>.py          # Tests
  ├── docs/<function_name>.md         # Documentation
  └── reports/<function_name>.yaml    # Verification report
```

## Commit Message Format

```
<type>(<scope>): <description> [L<level>]

<body>

Verification: L<level> (<level_name>)
Source: <source_file>:<line_range>
Challenger: <agent_name>
Challenges: <n> raised, <m> resolved
Pending: <what's needed for next level>

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Type

| Type | When |
|------|------|
| `feat` | New translation |
| `fix` | Bug fix in translation |
| `challenge` | Raise a challenge against existing translation |
| `resolve` | Resolve a challenge |
| `upgrade` | Upgrade verification level (e.g., L2 → L3) |

### Level Tag

Always include `[L<n>]` in the commit title:
- `[L0]` - Draft, not verified
- `[L1]` - Cross-checked
- `[L2]` - Basic tests pass
- `[L3]` - Adversarial tests pass
- `[L4]` - Fully proven

## Example Commits

### New Translation (L2)

```
feat(tensor): translate contract_tensors [L2]

Translate TeneT.jl/src/contract.jl:45-78 to Python.

- Implements tensor contraction with arbitrary dimension specification
- Handles complex tensors with proper conjugation
- Matches Julia's memory layout conventions

Verification: L2 (tested)
Source: TeneT.jl/src/contract.jl:45-78
Challenger: equivalence-prover
Challenges: 0 raised
Pending: adversarial testing for L3

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Challenge Raised

```
challenge(tensor): dims indexing inconsistency [L0]

Challenge CHG-042: Documentation claims 0-indexed dims, but source
code adds 1 before internal call, suggesting external API is 0-indexed
but doc description is misleading.

Evidence:
- contract.jl:52 shows `dims .+ 1` conversion
- docs/contract_tensors.md says "0-indexed list"

This downgrades contract_tensors from L2 to L0.

Verification: L0 (draft) [DOWNGRADED from L2]
Challenger: source-to-target
Challenge-ID: CHG-042

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Challenge Resolved

```
resolve(tensor): clarify dims indexing (CHG-042) [L2]

Resolved CHG-042 by clarifying documentation.

The source accepts 0-indexed dims (Python convention) and internally
converts to 1-indexed for Julia. Updated doc to explain this clearly.

Resolution: clarify_doc
- Updated docs/contract_tensors.md with conversion note
- Re-verified doc-source consistency
- Re-ran equivalence tests

Verification: L2 (tested) [RESTORED]
Challenge-ID: CHG-042
Resolved-By: doc-writer

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Level Upgrade

```
upgrade(tensor): contract_tensors L2 → L3 [L3]

Passed adversarial testing for contract_tensors.

Adversarial Results:
- Attempts: 50
- Failures: 0
- Near-misses: 2 (complex inputs with small imaginary parts)
- Strategies: random, boundary, sparse, ill-conditioned

All near-misses investigated and confirmed within tolerance.

Verification: L3 (adversarial)
Challenger: equivalence-prover
Pending: human review for L4

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Verification Report Format

Every commit includes `reports/<function_name>.yaml`:

```yaml
function: contract_tensors
source:
  file: TeneT.jl/src/contract.jl
  lines: 45-78
  commit: abc123  # source repo commit

target:
  file: tenet_py/tensor/contract.py
  lines: 12-45

documentation:
  file: docs/contract_tensors.md

verification:
  level: L3
  date: 2024-01-15

  triangular_check:
    doc_source: pass
    doc_target: pass
    source_target: pass

  oracle_tests:
    total: 15
    passed: 15
    failed: 0

  adversarial:
    attacker: equivalence-prover
    attempts: 50
    failures: 0
    near_misses: 2
    strategies:
      - random: 20 attempts
      - boundary: 10 attempts
      - sparse: 10 attempts
      - ill_conditioned: 10 attempts

  challenges:
    total_raised: 1
    resolved: 1
    pending: 0
    history:
      - id: CHG-042
        status: resolved
        resolution: clarify_doc

  pending_for_next_level:
    - human review of algorithm correctness
    - human review of edge case handling
```

## Git Hooks

Recommended pre-commit hook to enforce atomic commit structure:

```bash
#!/bin/bash
# .git/hooks/commit-msg

MSG_FILE=$1
MSG=$(cat "$MSG_FILE")

# Check for level tag
if ! echo "$MSG" | grep -qE '^\w+\([^)]+\):.*\[L[0-4]\]'; then
    echo "ERROR: Commit message must include verification level [L0-L4]"
    echo "Example: feat(tensor): translate foo [L2]"
    exit 1
fi

# Check for verification footer
if ! echo "$MSG" | grep -qE '^Verification: L[0-4]'; then
    echo "ERROR: Commit must include 'Verification: L<n>' footer"
    exit 1
fi
```

## Why Atomic Commits?

1. **Traceability**: Every function has a complete history
2. **Bisectability**: `git bisect` works at function granularity
3. **Reviewability**: Each commit is a complete, reviewable unit
4. **Rollbackability**: Revert a single function without affecting others
5. **Progress Tracking**: Count commits = count verified functions

## Anti-Patterns

### ❌ Bulk Commit

```
feat: translate 15 functions

- contract.py
- decompose.py
- ... 13 more files
```

**Problem**: Can't track individual function verification levels.

### ❌ Missing Report

```
feat(tensor): translate contract [L2]

# No reports/contract.yaml included
```

**Problem**: No evidence of verification.

### ❌ Split Artifacts

```
# Commit 1
feat(tensor): add contract.py

# Commit 2 (later)
test(tensor): add test_contract.py

# Commit 3 (even later)
docs(tensor): add contract.md
```

**Problem**: Function exists without tests/docs between commits.
