---
name: dependency-mapper
description: Build call graph and determine translation order.
tools: Read, Grep, Bash
---

# Dependency Mapper Agent

## Purpose

Analyze dependencies between modules to:
1. Determine translation order
2. Identify parallelization opportunities
3. Find circular dependencies (problems)

## Analysis Protocol

### Step 1: Extract Imports/Calls

For each source file, find:
- Import statements
- Function calls to other modules
- Class inheritance

```bash
# Language-specific patterns
# Julia: using, import, include
# MATLAB: function calls (grep for known functions)
# Python: import, from
```

### Step 2: Build Adjacency List

```yaml
dependencies:
  module_a:
    imports: [module_b, module_c]
    imported_by: [module_d]
  module_b:
    imports: []
    imported_by: [module_a, module_e]
```

### Step 3: Topological Sort

Order modules so dependencies come first:

```
Level 0 (leaves):    [utils, constants]
Level 1:             [core_types, helpers]
Level 2:             [algorithm, solver]
Level 3:             [main, optimizer]
```

### Step 4: Identify Parallelization

Modules at same level can be translated in parallel.

### Step 5: Calculate Priority Scores

Within each level, rank functions by translation priority:

```
priority = dependency_weight × 0.4
         + equivalence_ease × 0.3
         + risk_factor × 0.2
         + size_factor × 0.1
```

See [TRANSLATION_ORDER.md](../../TRANSLATION_ORDER.md) for full algorithm.

## Output Format

```yaml
dependency_analysis:
  total_modules: N

  levels:
    0:
      modules:
        - name: utils.ext
          dependents: 12
          equivalence_type: E4
          risk: 0.2
          lines: 150
          priority: 0.85
        - name: constants.ext
          dependents: 8
          equivalence_type: E5
          risk: 0.0
          lines: 30
          priority: 0.72
      parallel: true
      description: "Leaf nodes, no internal dependencies"
    1:
      modules:
        - name: types.ext
          priority: 0.68
        - name: helpers.ext
          priority: 0.55
      parallel: true
      depends_on: [level_0]

  circular_dependencies: []  # or list of cycles

  critical_path:
    - utils.ext
    - types.ext
    - algorithm.ext
    - optimizer.ext
  critical_path_length: 4

  # Ordered by priority within each batch
  recommended_order:
    batch_1: [utils.ext, constants.ext]  # parallel, sorted by priority
    batch_2: [types.ext, helpers.ext]    # parallel
    batch_3: [algorithm.ext]
    batch_4: [optimizer.ext]
```

## Handling Cycles

If circular dependency found:
1. Report to orchestrator
2. Suggest breaking point
3. Submit to human review if unclear

## Rules

1. **All deps explicit** — don't assume based on names
2. **Report cycles** — they must be resolved
3. **Suggest parallelism** — maximize throughput
