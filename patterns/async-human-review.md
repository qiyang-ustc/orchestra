# Async Human Review Pattern

## The Problem

LLMs encounter uncertainty:
- Unclear code intent
- Multiple valid interpretations
- Domain expertise needed

Naive approach: block and wait for human.

Problems:
- Wastes compute time
- Human may not be available
- Single uncertainty blocks ALL progress

## The Pattern

**Submit → Skip → Continue**

```
Agent encounters uncertainty
    ↓
Submit to review queue
    ↓
Mark module as PENDING_HUMAN
    ↓
IMMEDIATELY continue with OTHER modules
    ↓
Human reviews async (whenever)
    ↓
Next session picks up resolved items
```

## Implementation

### The Queue

Shared document (e.g., `notes/human_review_queue.md`):

```markdown
## PENDING

### [ID-001] file.ext - Issue description
- **Options**: 1) Do X, 2) Do Y, 3) Ask expert
- **Blocking**: [dependent_module]
- **Status**: ⏸️ PENDING

## RESOLVED

### [ID-000] other.ext - Previous issue
- **Decision**: Option 2
- **Resolved by**: @human
```

### Agent Behavior

```python
def translate(module):
    if uncertain:
        queue.submit(
            file=module,
            issue="description",
            options=["A", "B", "C"],
            blocking=[module]
        )
        return Status.PENDING_HUMAN  # Don't block!
    
    # Continue with translation...
```

### Orchestrator Behavior

```python
for module in modules:
    result = translate(module)
    if result == Status.PENDING_HUMAN:
        pending.append(module)
        continue  # Move to next module
    # Process successful result...
```

### Session Start

```python
resolved = queue.get_resolved()
for item in resolved:
    unblock(item.module)
```

## Benefits

1. **No wasted time** — work continues on unblocked items
2. **Batch review** — human reviews multiple items efficiently
3. **Audit trail** — full history of decisions
4. **Async friendly** — human doesn't need to be present

## Properties

- **Persistent**: Queue survives sessions
- **Transparent**: Both sides see same state
- **Prioritized**: Critical items surface first
- **Non-blocking**: Never wait synchronously

## Anti-patterns

❌ `while not resolved: wait()`  
❌ `input("What should I do?")`  
❌ Blocking on user confirmation  

✅ Submit to queue → return → continue elsewhere
