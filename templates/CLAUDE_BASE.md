# {{PROJECT_NAME}}: {{SOURCE_LANG}} → {{TARGET_LANG}} Translation

## Mission

Translate {{SOURCE_REPO}} to {{TARGET_LANG}} with {{N}}-way equivalence proof.

---

## Source & Target

```
SOURCE (READ-ONLY):
  {{SOURCE_PATH}}

TARGET:
  {{TARGET_PATH}}
```

---

## Equivalence Standard

For each module, prove equivalence across {{N}} dimensions:

| Check | Description | Verification Method |
|-------|-------------|---------------------|
| `C_S ≡ C_T` | Source code ≡ Target code | Output comparison |
| `T_S ≡ T_T` | Source test ≡ Target test | Same assertions |
| `D_S ≡ D_T` | Source doc ≡ Target doc | Semantic match |
| `C ↔ D` | Code-doc consistency | Doc describes code |
| `T ↔ D` | Test-doc consistency | Tests verify claims |

**A module is PROVEN only when all checks pass.**

---

## Orchestrator Protocol

**You are the ORCHESTRATOR. You dispatch tasks to sub-agents.**

### Session Start

```
1. @session-init          → Verify environment
2. @progress-tracker      → Report current state
3. @human-review-gate     → Check resolved items
4. @dependency-mapper     → Plan parallel work
```

### Dispatch Rules

1. **Never block on human review** — skip and continue
2. **Parallelize aggressively** — same-level modules concurrent
3. **Document first** — understand before translate
4. **Test immediately** — verify before moving on

### Human Review Protocol

When any agent encounters uncertainty:
```
1. Submit to queue (notes/human_review_queue.md)
2. Mark module as PENDING_HUMAN
3. IMMEDIATELY continue with next module
4. Report pending items at session end
```

---

## Sub-Agent Roster

| Category | Agent | Purpose |
|----------|-------|---------|
| orchestration | `session-init` | Environment check |
| orchestration | `progress-tracker` | Status tracking |
| orchestration | `human-review-gate` | Async human decisions |
| analysis | `codebase-scanner` | Build file index |
| analysis | `dependency-mapper` | Call graph analysis |
| analysis | `legacy-archaeologist` | Analyze old code |
| preprocessing | `file-splitter` | Break large files |
| preprocessing | `refactor-advisor` | Identify cleanups |
| translation | `source-to-target` | Main translation |
| documentation | `doc-writer` | Generate docs |
| verification | `equivalence-prover` | Prove correctness |
| debug | `code-verifier` | File state checks |

---

## Directory Structure

```
{{TARGET_PATH}}/
├── CLAUDE.md
├── {{PACKAGE_NAME}}/        # Translated code
├── tests/
│   ├── ground_truth/        # Source-generated reference data
│   └── test_*/              # Test modules
├── docs/
│   ├── {{SOURCE_LANG_LOWER}}/   # Source language docs
│   └── {{TARGET_LANG_LOWER}}/   # Target language docs
├── notes/
│   ├── human_review_queue.md
│   ├── decisions_log.md
│   └── module_status.yaml
└── scripts/
    └── generate_ground_truth.{{SOURCE_EXT}}
```

---

## Notes Protocol

### human_review_queue.md

```markdown
## PENDING
### [ID-XXX] file.ext - Brief description
- **Issue**: What's unclear
- **Options**: Possible decisions
- **Blocking**: What can't proceed
- **Status**: ⏸️ PENDING

## RESOLVED
### [ID-XXX] file.ext - Brief description
- **Decision**: What was decided
- **Date**: When
```

---

## Session Protocol

### START
```
@session-init
@progress-tracker
@human-review-gate
```

### DURING
- Dispatch parallel where possible
- Submit uncertainties immediately
- Update progress after each module

### END
```
@progress-tracker
Report: "X completed, Y pending, Z blocked"
```

---

## Do NOT

- Modify source files
- Block on human decisions
- Translate without understanding
- Skip equivalence checks

---

## Current Phase

`[ ] Phase 0: Setup & Analysis`

---

## Customization Notes

Replace these placeholders:
- `{{PROJECT_NAME}}`: Your project name
- `{{SOURCE_LANG}}`: Source language (Julia, MATLAB, etc.)
- `{{TARGET_LANG}}`: Target language (Python, Rust, etc.)
- `{{SOURCE_PATH}}`: Path to source repo
- `{{TARGET_PATH}}`: Path to target repo
- `{{N}}`: Number of equivalence dimensions (4, 6, etc.)
- `{{PACKAGE_NAME}}`: Python/target package name
- `{{SOURCE_EXT}}`: Source file extension (.jl, .m, etc.)
