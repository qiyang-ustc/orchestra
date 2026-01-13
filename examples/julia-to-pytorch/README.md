# Julia → PyTorch Translation Example

This example shows Orchestra configuration for translating TeneT.jl (VUMPS tensor network library) to PyTorch.

## Source

- **Repository**: TeneT.jl
- **Language**: Julia
- **Domain**: Tensor networks, iPEPS, VUMPS algorithm
- **Size**: ~5000 lines
- **Branch**: `origin/Array-of-Array` (critical!)

## Target

- **Package**: pytenet
- **Language**: Python + PyTorch
- **Focus**: AD-compatible VUMPS for iPEPS optimization

## Equivalence Dimensions

4-way equivalence:
1. Code_Julia ≡ Code_Python
2. Test_Julia ≡ Test_Python
3. Gradient_Julia ≡ Gradient_Python
4. Physics results match published values

## Special Considerations

### Julia-Specific

- Column-major arrays (vs Python row-major)
- 1-based indexing
- `ein"..."` syntax → `torch.einsum`
- Zygote AD → PyTorch autograd

### Gradient Convention

- Julia Zygote: standard gradient
- PyTorch: Wirtinger derivative (conjugated for complex)
- Need to conjugate when comparing

### Eigenvector Phase

Eigenvectors unique only up to phase e^{iθ}.
Compare projectors |v⟩⟨v| instead of v directly.

## Key Modules

```
Level 0: tensor_utils, struct_array
Level 1: canonical (qrpos, lqpos)
Level 2: fixed_point, environment
Level 3: runtime, algorithm
Level 4: contraction
Level 5: models (ising, kitaev)
Level 6: optimizer
```

## Files

See this directory for:
- `CLAUDE.md` — Full orchestration config
- `agents/` — Julia-specific agent customizations

## Success Criteria

1. Unit tests match Julia output (rtol=1e-10)
2. Ising model energy matches exact solution
3. Kitaev model reproduces paper results
4. `torch.autograd.gradcheck` passes
