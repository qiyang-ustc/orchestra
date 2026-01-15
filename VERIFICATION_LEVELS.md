# Verification Levels

Every translated unit (function, class, module) carries a verification level indicating its trust status.

## Level Definitions

| Level | Name | Meaning | Requirements |
|-------|------|---------|--------------|
| **L0** | `draft` | Just written, no verification | Initial output from any agent |
| **L1** | `cross-checked` | Another agent reviewed, no contradictions found | At least one other agent confirmed consistency |
| **L2** | `tested` | Basic tests pass | Oracle comparison succeeds |
| **L3** | `adversarial` | Survived adversarial attacks | Attacker agent failed to break it |
| **L4** | `proven` | Triangular consistency + adversarial + human review | Full verification chain complete |

## State Transitions

```
L0 (draft)
   │
   ├──[another agent reviews]──→ L1 (cross-checked)
   │                                │
   │                                ├──[basic tests pass]──→ L2 (tested)
   │                                │                           │
   │                                │                           ├──[adversarial pass]──→ L3 (adversarial)
   │                                │                           │                           │
   │                                │                           │                           ├──[human review]──→ L4 (proven)
   │                                │                           │                           │
   │                                │                           │     ┌─────────────────────┘
   │                                │                           │     │
   └──[challenge raised]───────────┴───────────────────────────┴─────┴──→ L0 (draft) [DOWNGRADE]
```

**Key rule: Any challenge immediately downgrades to L0.**

## Marking Syntax

### In Python Code

```python
# orchestra: L2 | challenger: equivalence-prover | date: 2024-01-15
# source: TeneT.jl/src/contract.jl:45-78
def contract_tensors(a: Tensor, b: Tensor, dims: list[int]) -> Tensor:
    ...
```

### In Tests

```python
@pytest.mark.orchestra(level="L3", source="TeneT.jl:contract.jl:45")
@pytest.mark.adversarial(attacker="equivalence-prover", attempts=50, failures=0)
def test_contract_tensors_equivalence():
    ...
```

### In Documentation (Frontmatter)

```yaml
---
function: contract_tensors
source_file: TeneT.jl/src/contract.jl
target_file: tenet_py/contract.py
verification:
  level: L3
  history:
    - level: L0
      date: 2024-01-10
      agent: doc-writer
      action: initial draft
    - level: L1
      date: 2024-01-11
      agent: source-to-target
      action: cross-checked, no challenges
    - level: L2
      date: 2024-01-12
      agent: equivalence-prover
      action: basic tests pass (15/15)
    - level: L3
      date: 2024-01-13
      agent: equivalence-prover
      action: adversarial tests pass (50 attempts, 0 failures)
  challenges: []
  pending: human review for L4
---
```

## Challenge Records

When an agent finds inconsistency:

```yaml
challenges:
  - id: CHG-001
    date: 2024-01-14
    raised_by: equivalence-prover
    severity: critical  # critical | major | minor
    description: "Doc says dims is 1-indexed, but source uses 0-indexed"
    evidence:
      - file: contract.jl
        line: 52
        content: "dims[1]  # Julia is 1-indexed"
      - file: contract_tensors.md
        section: Parameters
        content: "dims: 0-indexed dimension list"
    resolution:
      status: pending  # pending | resolved | wontfix
      decision: null
      resolved_by: null
      date: null
```

## Adversarial Testing Protocol

The attacker agent (usually `equivalence-prover`) attempts to:

1. **Find breaking inputs**: Inputs where `source(x) != target(x)`
2. **Find undocumented behavior**: Code behavior not described in docs
3. **Find doc-code mismatch**: Doc claims not satisfied by code
4. **Find edge cases**: Boundary conditions, NaN, Inf, empty inputs

### Adversarial Report Format

```yaml
adversarial_report:
  target: contract_tensors
  attacker: equivalence-prover
  date: 2024-01-13
  config:
    max_attempts: 50
    strategies:
      - random_inputs
      - boundary_values
      - type_coercion
      - dimension_mismatch
  results:
    total_attempts: 50
    failures: 0
    near_misses: 2  # passed but close to tolerance
    coverage:
      input_space: 0.73
      edge_cases: 0.85
  conclusion: PASS
  notes: "Near-miss on complex input with very small imaginary part"
```

## Verification in Git Commits

Every atomic commit must include the verification level:

```
feat(contract): translate contract_tensors [L3]

- Translate contract.jl:45-78 to Python
- Add oracle-based equivalence tests
- Pass adversarial testing (50 attempts)

Verification: L3 (adversarial)
Challenger: equivalence-prover
Pending: human review for L4

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Level Requirements Summary

| Level | Code | Test | Doc | Cross-check | Adversarial | Human |
|-------|------|------|-----|-------------|-------------|-------|
| L0 | ✓ | - | - | - | - | - |
| L1 | ✓ | - | ✓ | ✓ | - | - |
| L2 | ✓ | ✓ | ✓ | ✓ | - | - |
| L3 | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| L4 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## Trust Degradation

**Critical principle: Later agents do NOT trust earlier agents.**

- Translator reads doc → must verify against source code
- Verifier reads code → must verify against doc AND source
- Any inconsistency → immediate downgrade to L0

This creates a **triangular confrontation** where no single agent's output is trusted without independent verification.
