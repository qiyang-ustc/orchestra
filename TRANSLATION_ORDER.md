# Translation Planning

## The Fundamental Question

**How does a human understand this codebase?**

Not by dependency graph. Not by file size. By **conceptual hierarchy**.

## The Onion Model

```
┌───────────────────────────────────────────────┐
│  Layer 4: Edge                                │
│  IO, CLI, visualization, logging              │
│  → Understand last, L2 acceptable             │
├───────────────────────────────────────────────┤
│  Layer 3: API                                 │
│  Public interfaces, orchestration             │
│  → High-level tests here reveal core bugs     │
├───────────────────────────────────────────────┤
│  Layer 2: Algorithm                           │
│  Domain-specific logic (VUMPS, DMRG, etc.)    │
│  → Where domain expertise matters             │
├───────────────────────────────────────────────┤
│  Layer 1: Building Blocks                     │
│  Composable structures (MPS, Environment)     │
│  → Must be solid before algorithms            │
├───────────────────────────────────────────────┤
│  Layer 0: Core Math                           │
│  SVD, eigendecomposition, tensor contraction  │
│  → Understand FIRST, MUST be L3+              │
└───────────────────────────────────────────────┘
```

## Core Principle: Inside-Out Understanding

**You cannot understand Layer N without understanding Layer N-1.**

Translation order follows understanding order:
1. Core Math (L0) → must reach L3 before anything else
2. Building Blocks (L1) → L3 before algorithms
3. Algorithm (L2) → L2 acceptable initially
4. API (L3) → L2 acceptable
5. Edge (L4) → L2 acceptable

## Why Core Math Must Be L3+

| Property | Implication |
|----------|-------------|
| Everything depends on it | One bug corrupts entire codebase |
| Small and well-defined | Adversarial testing is cheap |
| Mathematical specification | Clear right/wrong, no ambiguity |
| Foundation of understanding | Human must trust this first |

**There is no excuse for L2-only core math.**

## Verification Level by Layer

| Layer | Minimum Level | Rationale |
|-------|---------------|-----------|
| Core Math | **L3** | Non-negotiable. Adversarial is cheap, stakes are high |
| Building Blocks | **L3** | Composition errors are subtle |
| Algorithm | L2 initially, L3 before release | Domain complexity, iterate |
| API | L2 | High-level integration tests catch issues |
| Edge | L2 | Low stakes, easy to fix later |

## The Translation Planner Role

A **Translation Planner** agent maintains:

### 1. Conceptual Map

```yaml
conceptual_layers:
  core_math:
    description: "Fundamental mathematical operations"
    modules:
      - name: svd.py
        concepts: [singular value decomposition, truncation]
        min_level: L3
      - name: contract.py
        concepts: [tensor contraction, index manipulation]
        min_level: L3

  building_blocks:
    description: "Composable domain structures"
    modules:
      - name: mps.py
        concepts: [matrix product state, canonical form]
        depends_on_concepts: [svd, contract]
        min_level: L3

  algorithm:
    description: "Domain algorithms"
    modules:
      - name: vumps.py
        concepts: [variational optimization, fixed point]
        depends_on_concepts: [mps, environment]
        min_level: L2
```

### 2. Verification State

```yaml
verification_state:
  core_math:
    svd.py: L3 ✓
    contract.py: L3 ✓
    eigensolve.py: L2 ⚠️  # BLOCKING: must reach L3

  building_blocks:
    mps.py: BLOCKED  # waiting for eigensolve.py L3

  algorithm:
    vumps.py: NOT_STARTED
```

### 3. Failure Propagation

When a high-level test fails:

```yaml
failure_event:
  module: vumps.py
  test: test_convergence
  symptom: "Energy not decreasing"

propagation_analysis:
  likely_causes:
    - module: environment.py
      reason: "Environment update uses eigensolve"
      action: UPGRADE_TO_L3
    - module: eigensolve.py
      reason: "Core dependency"
      action: UPGRADE_TO_L3

  decision:
    - eigensolve.py: L2 → L3 (run adversarial)
    - environment.py: L2 → L3 (run adversarial)
    - vumps.py: PAUSE until dependencies L3
```

## Planning Algorithm

### Phase 1: Conceptual Classification

```python
def classify_modules(codebase):
    """Human-guided classification into conceptual layers."""

    for module in codebase:
        # These questions determine layer:
        # 1. Is this pure math with no domain knowledge? → Core Math
        # 2. Is this a reusable structure? → Building Block
        # 3. Is this domain-specific logic? → Algorithm
        # 4. Is this a public interface? → API
        # 5. Is this peripheral? → Edge

        layer = ask_human_or_infer(module)
        min_level = L3 if layer in [CORE_MATH, BUILDING_BLOCK] else L2

        yield ModuleClassification(module, layer, min_level)
```

### Phase 2: Concept Dependency Analysis

```python
def build_concept_graph(modules):
    """Build graph of conceptual dependencies (not just imports)."""

    # Example: vumps.py imports mps.py
    # But conceptually: VUMPS depends on concept of "canonical form"
    # which is defined in mps.py

    # This is deeper than import analysis
    # Requires understanding what concepts each module implements/uses
```

### Phase 3: Inside-Out Translation

```python
def translate_inside_out(concept_graph):
    current_layer = CORE_MATH

    while current_layer <= EDGE:
        modules = get_modules_at_layer(current_layer)

        for module in modules:
            translate(module)
            verify_to_min_level(module)  # L3 for core, L2 for outer

            if not meets_min_level(module):
                # BLOCK: cannot proceed until this is fixed
                fix_until_passes(module)

        current_layer += 1
```

### Phase 4: Failure Propagation

```python
def handle_test_failure(failing_module, failure_info):
    """When high-level test fails, propagate verification requirements."""

    # Identify which core concepts are involved
    concepts_used = get_concepts_used_by(failing_module)

    # Find modules implementing those concepts
    suspect_modules = find_modules_implementing(concepts_used)

    # Upgrade their verification requirements
    for module in suspect_modules:
        if module.level < L3:
            module.required_level = L3
            add_to_verification_queue(module)

    # Pause high-level work until core is solid
    pause_dependent_work(failing_module)
```

## Coupling Analysis

### High Cohesion Modules (Good)

```yaml
module: svd.py
  concepts_implemented: [svd, truncated_svd]
  concepts_used: []  # self-contained
  coupling: LOW
  → Easy to verify in isolation
  → Good candidate for early L3
```

### High Coupling Modules (Careful)

```yaml
module: environment.py
  concepts_implemented: [environment_tensor]
  concepts_used: [mps, contract, svd, eigensolve]
  coupling: HIGH
  → Depends on many core concepts
  → Failures here often mean core bugs
  → Verify dependencies to L3 first
```

## Deliverable Structure

Final translation should be **high cohesion, low coupling**:

```
Package Structure:

tenet_py/
├── core/           # Layer 0: Core Math (all L3+)
│   ├── linalg.py   # SVD, QR, eigen
│   └── contract.py # Tensor operations
│
├── structures/     # Layer 1: Building Blocks (all L3)
│   ├── mps.py
│   └── mpo.py
│
├── algorithms/     # Layer 2: Algorithms (L2+)
│   ├── vumps.py
│   └── dmrg.py
│
├── api/            # Layer 3: Public API (L2)
│   └── optimize.py
│
└── utils/          # Layer 4: Edge (L2)
    ├── io.py
    └── viz.py
```

Each layer only imports from inner layers. Never outward.

## The Planner's Questions

Before translating, the Planner asks:

1. **Conceptual**: What concept does this module implement?
2. **Dependency**: What concepts does it depend on?
3. **Coupling**: How many other modules does it touch?
4. **Criticality**: If this is wrong, what breaks?
5. **Testability**: Can we adversarially test this cheaply?

From these answers, determine:
- Which layer
- Minimum verification level
- Translation order

## Summary

| Old Thinking | New Thinking |
|--------------|--------------|
| Dependency graph order | Conceptual layer order |
| Mechanical priority score | Human understanding flow |
| L2 gate for all | L3 gate for core, L2 for edge |
| Linear progress | Inside-out with failure propagation |
| Weight-based ranking | Cohesion/coupling analysis |

**The goal is not to translate code. The goal is to transfer understanding.**
