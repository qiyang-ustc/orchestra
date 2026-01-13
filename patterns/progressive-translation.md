# Progressive Translation Pattern

## The Problem

Large codebases can't be translated all at once:
- Context window limits
- Dependencies between modules
- Need to verify as you go

## The Pattern

Translate in dependency order: leaves first, work up the tree.

## Steps

### Step 1: Build Dependency Graph

```
      main.py
         │
    ┌────┴────┐
    │         │
 algo.py   model.py
    │         │
    └────┬────┘
         │
     utils.py  ← LEAF
```

### Step 2: Topological Sort

```
Level 0: [utils.py]           # No internal deps
Level 1: [algo.py, model.py]  # Depend on L0
Level 2: [main.py]            # Depends on L0, L1
```

### Step 3: Translate by Level

```
1. Translate Level 0
2. Verify Level 0
3. Translate Level 1 (can use verified L0)
4. Verify Level 1
5. Continue...
```

### Step 4: Parallelize Within Levels

Same-level modules can translate concurrently:

```
Level 0: 1 agent
Level 1: 2 agents in parallel
Level 2: 1 agent
```

## Benefits

1. **Early error detection** — catch bugs in foundations
2. **Verified dependencies** — each level builds on verified code
3. **Clear progress** — know exactly where you are
4. **Parallelization** — maximize throughput

## Implementation

### Dependency Analysis

```python
def build_dependency_graph(source_files):
    graph = {}
    for file in source_files:
        imports = extract_imports(file)
        graph[file] = [f for f in imports if f in source_files]
    return graph
```

### Topological Sort

```python
def get_levels(graph):
    levels = []
    remaining = set(graph.keys())
    
    while remaining:
        # Find nodes with no remaining dependencies
        level = [n for n in remaining 
                 if all(d not in remaining for d in graph[n])]
        levels.append(level)
        remaining -= set(level)
    
    return levels
```

### Translation Loop

```python
for level_num, modules in enumerate(levels):
    # Parallel translation within level
    results = parallel_translate(modules)
    
    # Verify all before proceeding
    for module in modules:
        verify_equivalence(module)
    
    # Only continue if all pass
    if any_failed(results):
        break
```

## Handling Cycles

Circular dependencies break topological sort.

Solutions:
1. **Break the cycle** — refactor to remove circularity
2. **Translate together** — treat cycle as single unit
3. **Interface extraction** — create interface module

## Critical Path

The longest dependency chain determines minimum time:

```
utils → types → algo → optimizer
  1   →   2   →   3  →    4      = 4 levels minimum
```

Prioritize critical path modules.
