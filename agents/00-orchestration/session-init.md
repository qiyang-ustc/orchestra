---
name: session-init
description: Initialize session, verify environment. Run FIRST at every session.
tools: Bash, Read
model: claude-opus-4-20250514
---

# Session Init Agent

## Purpose

Verify environment is ready for translation work.
**Run at the START of every session.**

## Checklist

### 1. Source Repository
```bash
if [ -d "{{SOURCE_PATH}}" ]; then
    echo "✓ Source repository exists"
    find {{SOURCE_PATH}} -name "*.{{SOURCE_EXT}}" -type f | wc -l | xargs echo "  Total files:"
else
    echo "✗ Source repository NOT FOUND"
    exit 1
fi
```

### 2. Target Directory
```bash
if [ -d "{{TARGET_PATH}}" ]; then
    echo "✓ Target directory exists"
else
    echo "Creating target directory..."
    mkdir -p {{TARGET_PATH}}
fi
```

### 3. Source Language Runtime
```bash
# Check if source language is available
# Example for MATLAB:
# matlab -batch "disp('OK')" 2>/dev/null && echo "✓ MATLAB available"
# Example for Julia:
# julia -e "println(\"OK\")" && echo "✓ Julia available"
```

### 4. Python Environment
```bash
cd {{TARGET_PATH}}
if [ -f "pyproject.toml" ] && [ -d ".venv" ]; then
    echo "✓ Python environment ready"
else
    echo "⚠ Need to initialize: uv sync"
fi
```

### 5. Notes Directory
```bash
for file in human_review_queue.md decisions_log.md module_status.yaml; do
    [ -f "notes/$file" ] && echo "✓ notes/$file" || touch "notes/$file"
done
```

## Output Format

```yaml
session_init:
  timestamp: "{{TIMESTAMP}}"
  source:
    path: {{SOURCE_PATH}}
    status: OK | MISSING
    file_count: N
  target:
    path: {{TARGET_PATH}}
    status: OK | NEEDS_SETUP
  source_runtime:
    available: true | false
  python:
    venv: OK | MISSING
  ready: true | false
```

## Rules

1. **Run FIRST** — before any other agents
2. **Fail fast** — report issues immediately
3. **Create missing pieces** — auto-setup where possible
