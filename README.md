# Orchestra

**A framework for provably correct code translation using multi-agent LLM orchestration.**

## What is Orchestra?

Orchestra translates large codebases between programming languages using LLMs, with correctness guarantees.

The key insight: **The source implementation IS the oracle. Match its behavior exactly.**

```
∀ valid input x:  target(x) ≈ source(x)
```

## Core Principles

1. **Oracle is Truth**: Source behavior is the ONLY standard. Doc helps understand, but source decides.
2. **One Function at a Time**: Translate, verify, commit. No bulk translation.
3. **Inside-Out**: Core math first (L3), then building blocks (L3), then algorithms (L2).
4. **Conductor Pattern**: Main agent orchestrates sub-agents, doesn't write code.

## Quick Start

### Option A: Use example script (for TeneT.jl → PyTorch)

```bash
cd ~/works

# 1. Clone source
git clone git@github.com:someone/TeneT.jl.git

# 2. Clone orchestra as your project
git clone git@github.com:qiyang-ustc/orchestra.git pytenet
cd pytenet

# 3. Run example init script
./scripts/example-init.sh git@github.com:you/pytenet.git

# 4. Start
git push -u origin main
claude
```

This creates:
```
~/works/
├── TeneT.jl/        # src (read-only)
└── pytenet/         # your project (cloned from orchestra)
    ├── orchestra.yaml
    ├── CLAUDE.md
    └── pytenet/     # dst package
```

### Option B: Manual setup

```bash
cd ~/works
git clone git@github.com:someone/TeneT.jl.git
git clone git@github.com:qiyang-ustc/orchestra.git pytenet
cd pytenet
vim orchestra.yaml
git remote set-url origin git@github.com:you/pytenet.git
git push
claude
```

### orchestra.yaml

```yaml
src: ../TeneT.jl            # Source (read-only)
dst: ./pytenet              # Target output
framework: julia -> pytorch

notes: |
  Key things:
  - Julia 1-indexed → Python 0-indexed
  - Ground state energy should be negative
```

### Reset & Update

```bash
./scripts/reset.sh          # Reset to clean state
./scripts/reset.sh --pull   # Reset and pull orchestra updates
```

## Verification

### Oracle Testing

The ONLY way to verify correctness:

```python
def test_oracle():
    expected = load_source_output("func_case_1")
    actual = target_func(input)
    assert_close(actual, expected, rtol=1e-10)
```

### Verification Levels

| Level | Meaning |
|-------|---------|
| **L2** | Oracle tests pass |
| **L3** | L2 + adversarial attacks fail |

### Adversarial Testing

Try to find inputs where `target(x) ≠ source(x)`:
- Boundary values, ill-conditioned, edge dimensions, random stress

## Translation Order

```
Layer 0: Core math (svd, qr)     ← L3 required
Layer 1: Building blocks (MPS)   ← L3 required
Layer 2: Algorithms (VUMPS)      ← L2 sufficient
Layer 3: API                     ← L2 sufficient
```

**Core must be L3 before anything else.**

## Documentation

Doc helps **understand** source, not define truth.

- Doc-Writer generates hypothesis about source behavior
- Translator uses doc to understand, but follows source when conflict
- If doc test fails but oracle passes → our understanding is wrong, update doc

## Directory Structure

```
orchestra/
├── CLAUDE.md                    # Conductor instructions
├── PHILOSOPHY.md                # Core principles
├── VERIFICATION_LEVELS.md       # L0-L4 spec
├── EQUIVALENCE_TYPES.md         # E0-E5 comparison types
├── agents/                      # Sub-agent definitions
│   ├── 00-orchestration/
│   ├── 03-translation/
│   ├── 04-documentation/
│   └── 05-verification/
└── patterns/
    └── oracle-verification.md
```

## Key Documents

| Document | Purpose |
|----------|---------|
| [PHILOSOPHY.md](PHILOSOPHY.md) | Core principles |
| [VERIFICATION_LEVELS.md](VERIFICATION_LEVELS.md) | L0-L4 spec |
| [EQUIVALENCE_TYPES.md](EQUIVALENCE_TYPES.md) | Comparison types |

## When to Use Orchestra

✅ **Good fit:**
- Large legacy codebases
- Scientific computing (numerical precision)
- Code where correctness > speed

❌ **Not ideal for:**
- Small scripts
- Prototypes
- Languages with existing transpilers

## License

MIT
