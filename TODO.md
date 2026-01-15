# TODO

Future improvements for Orchestra.

---

## Source Evolution (v2.0)

**Problem**: Currently assumes source code is static. Real projects evolve.

### Challenges

1. **Source updates**: How to detect and propagate changes?
2. **Sync strategy**: Full re-translate vs incremental?
3. **Conflict resolution**: What if target was modified independently?
4. **Version tracking**: Which source commit does target correspond to?

### Possible Approach

```yaml
source_tracking:
  source_repo: git@github.com:user/source.git
  source_commit: abc123
  target_commit: def456

  per_function:
    contract.py:
      source_file: contract.jl
      source_hash: sha256:...
      last_synced: 2024-01-15

change_detection:
  # On each session, check source for updates
  - git fetch source
  - diff source_commit..source/main
  - identify changed functions
  - mark corresponding target functions as NEEDS_REVIEW
```

### Questions to Resolve

- Should target track source commit explicitly?
- How to handle semantic changes vs refactoring?
- Can we auto-detect "safe" updates (comments, formatting)?
- Integration with git submodules or subtrees?

---

## Other Ideas

### CI/CD Integration
- GitHub Actions workflow for automated verification
- Pre-commit hooks for level checking
- Automated adversarial testing on PR

### Cross-Project Knowledge
- Share knowledge_base across similar projects
- "Julia → Python" conventions library
- Community-contributed domain constraints

### Performance Verification
- Add performance equivalence as verification dimension
- Complexity analysis (O(n) vs O(n²))
- Memory profiling comparison

### Interactive Debugging
- Step-through comparison of source vs target
- Visual diff of tensor values
- Gradient flow visualization
