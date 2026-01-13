# MATLAB → Python Translation Example

This example shows Orchestra configuration for translating Philippe Corboz's iPEPS SU/FU codebase to Python.

## Source

- **Repository**: Corboz TN library
- **Language**: MATLAB
- **Domain**: iPEPS, Simple Update, Full Update, CTM
- **Size**: ~50,000+ lines
- **Age**: 15+ years of development

## Target

- **Package**: pytn
- **Language**: Python + PyTorch
- **Goal**: Modern, documented, AD-compatible

## Equivalence Dimensions

6-way equivalence:
1. Code_MATLAB ≡ Code_Python
2. Test_MATLAB ≡ Test_Python
3. Docs_MATLAB ≡ Docs_Python
4. Code ↔ Docs consistency (both)
5. Test ↔ Docs consistency
6. Physics results match

## Special Considerations

### MATLAB-Specific

- File = Function (each .m is one function)
- @Class directories for OOP
- 1-based indexing
- Column-major storage
- `scon` tensor contraction DSL

### Legacy Code

- 15 years of accumulated code
- Some functions deprecated but kept
- Multiple implementations of same algorithm
- Need archaeology before translation

### Knowledge Preservation

This codebase is legendary but underdocumented.
Translation produces two valuable outputs:
1. Python implementation
2. Comprehensive bilingual documentation

## Key Components

```
minclude/           # Core utilities
├── @SymTensorNew/  # Symmetric tensors
├── scon.m          # Tensor contraction
├── tensorsvd.m     # SVD decomposition
└── ...

ipeps/              # Main algorithms
├── @CTM/           # Corner transfer matrix
├── @Epepo/         # PEPO expectations
├── goAD.m          # AD optimization
├── gofullupdate.m  # Full update
└── gosimpleupdate.m # Simple update
```

## Special Agents

This translation requires additional agents:

- `symtensor-specialist.md` — Handle symmetric tensor code
- `scon-translator.md` — Parse scon contraction syntax
- `matlab-class-translator.md` — @Class → Python class

## Human Review Emphasis

Many decisions need human input:
- Which duplicate to keep?
- Is this code still used?
- What does this magic number mean?

The async review queue will be heavily used.

## Success Criteria

1. All tutorials reproduce exactly
2. Documentation complete for both languages
3. Physics benchmarks match (Heisenberg, Kitaev)
4. Legacy code decisions documented
