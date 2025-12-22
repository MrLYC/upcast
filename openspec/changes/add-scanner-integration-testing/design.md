# Design: Scanner Integration Testing

## Overview

This design introduces automated integration testing for all 12 Upcast scanners using a real-world Django project (blueking-paas) as the test target. The system consists of:

1. **Makefile commands** to run integration tests locally
2. **GitHub Action** to validate scan result consistency in CI
3. **Baseline results** to detect regressions

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Integration Test Flow                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  make test-integration │
                  └───────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ Scanner 1│      │ Scanner 2│ ...  │ Scanner 12│
    └──────────┘      └──────────┘      └──────────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              ▼
                   example/scan-results/
                   ├── blocking-operations.yaml
                   ├── complexity-patterns.yaml
                   └── ... (12 files)
                              │
                              ▼
            ┌─────────────────────────────────┐
            │   GitHub Action: Compare Results │
            └─────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
    Extract          Extract           Compare
    baseline         new results       results
    results          results           sections
           │                  │                  │
           └──────────────────┼──────────────────┘
                              ▼
                      ┌───────────────┐
                      │  Pass / Fail   │
                      └───────────────┘
```

## Component Design

### 1. Makefile Integration

**Target**: `test-integration`

**Purpose**: Run all scanners on blueking-paas and generate YAML reports.

**Implementation**:

```makefile
.PHONY: test-integration
test-integration: ## Run integration tests on example project
	@echo "🚀 Running scanner integration tests on blueking-paas"
	@mkdir -p example/scan-results
	@uv run upcast scan-blocking-operations example/blueking-paas \
		-o example/scan-results/blocking-operations.yaml
	@uv run upcast scan-complexity-patterns example/blueking-paas \
		-o example/scan-results/complexity-patterns.yaml --threshold 10
	@uv run upcast scan-concurrency-patterns example/blueking-paas \
		-o example/scan-results/concurrency-patterns.yaml
	@uv run upcast scan-django-models example/blueking-paas \
		-o example/scan-results/django-models.yaml
	@uv run upcast scan-django-settings example/blueking-paas \
		-o example/scan-results/django-settings.yaml --mode usage
	@uv run upcast scan-django-urls example/blueking-paas \
		-o example/scan-results/django-urls.yaml
	@uv run upcast scan-env-vars example/blueking-paas \
		-o example/scan-results/env-vars.yaml
	@uv run upcast scan-exception-handlers example/blueking-paas \
		-o example/scan-results/exception-handlers.yaml
	@uv run upcast scan-http-requests example/blueking-paas \
		-o example/scan-results/http-requests.yaml
	@uv run upcast scan-metrics example/blueking-paas \
		-o example/scan-results/metrics.yaml
	@uv run upcast scan-signals example/blueking-paas \
		-o example/scan-results/signals.yaml
	@uv run upcast scan-unit-tests example/blueking-paas \
		-o example/scan-results/unit-tests.yaml
	@echo "✓ Integration tests complete. Results in example/scan-results/"
```

**Design Decisions**:

- **Sequential execution**: Simplifies Makefile, acceptable for ~1-2 min runtime
- **Explicit scanner list**: Clear what's being tested, easy to add/remove
- **YAML format**: Human-readable for manual inspection
- **Fixed output paths**: Predictable for GitHub Action consumption

### 2. GitHub Action Workflow

**File**: `.github/workflows/scanner-integration.yml`

**Purpose**: Validate scan results haven't changed unexpectedly.

**Workflow Structure**:

```yaml
name: Scanner Integration Tests

on:
  pull_request:
    types: [opened, synchronize, reopened]
  push:
    branches: [main]

jobs:
  integration-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          submodules: recursive # For blueking-paas submodule

      - name: Set up environment
        uses: ./.github/actions/setup-uv-env

      - name: Run integration tests
        run: make test-integration

      - name: Install yq for YAML processing
        run: |
          wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
          chmod +x /usr/local/bin/yq

      - name: Compare results against baseline
        run: |
          # ... comparison script ...

      - name: Upload scan results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: scan-results
          path: example/scan-results/
```

**Design Decisions**:

- **Baseline comparison**: Only compare `results` section, ignore metadata
- **Artifact upload**: Always save results for debugging
- **Fail fast**: Stop on first difference for quick feedback
- **Clear diffs**: Show exact changes in action output

### 3. Baseline Management

**Storage**: `example/scan-results-baseline/`

**Format**: Same as scan output (YAML files)

**Update Process**:

1. Developer makes intentional scanner change
2. Run `make test-integration` locally
3. Copy new results to baseline: `cp -r example/scan-results/* example/scan-results-baseline/`
4. Commit baseline updates
5. GitHub Action passes on next run

**Design Decisions**:

- **Git-tracked baseline**: Version controlled, visible in PRs
- **Manual updates**: Prevents accidental baseline changes
- **Full file storage**: Simple, no compression needed
- **Optional initially**: Can start without baseline, generate on first run

### 4. Result Comparison Logic

**Challenge**: Scan output includes non-deterministic fields (timestamps, scan_duration_ms).

**Solution**: Extract and compare only `results` section.

**Implementation**:

```bash
#!/bin/bash
set -e

BASELINE_DIR="example/scan-results-baseline"
RESULTS_DIR="example/scan-results"
FAILED=0

for file in "$RESULTS_DIR"/*.yaml; do
  filename=$(basename "$file")
  baseline="$BASELINE_DIR/$filename"

  if [ ! -f "$baseline" ]; then
    echo "⚠️  No baseline for $filename (first run?)"
    continue
  fi

  # Extract results sections
  yq '.results' "$baseline" > /tmp/baseline-results.yaml
  yq '.results' "$file" > /tmp/new-results.yaml

  # Compare
  if ! diff -u /tmp/baseline-results.yaml /tmp/new-results.yaml > /tmp/diff.txt; then
    echo "❌ Results changed in $filename:"
    cat /tmp/diff.txt
    FAILED=1
  else
    echo "✓ $filename matches baseline"
  fi
done

exit $FAILED
```

**Design Decisions**:

- **yq tool**: Industry-standard YAML processor
- **Unified diff**: Readable output with context
- **Exit code**: Non-zero on any difference
- **Tolerance**: First run without baseline is OK

## Data Flow

### 1. Scan Execution

```
User runs `make test-integration`
  ↓
For each scanner:
  ↓ Read Python files
  example/blueking-paas/**/*.py
  ↓ Parse with Astroid
  AST nodes
  ↓ Pattern detection
  Scanner-specific logic
  ↓ Model creation
  Pydantic models
  ↓ YAML serialization
  example/scan-results/scanner-name.yaml
```

### 2. CI Validation

```
GitHub Action triggered
  ↓ Checkout code + submodules
  Repository + blueking-paas
  ↓ Run integration tests
  make test-integration
  ↓ Generate new results
  example/scan-results/*.yaml
  ↓ Load baseline
  example/scan-results-baseline/*.yaml
  ↓ Extract results sections
  yq '.results' for each file
  ↓ Compare
  diff baseline vs new
  ↓ Report
  Pass (identical) or Fail (differences)
```

## Edge Cases

### 1. Scan Failure

**Scenario**: Scanner crashes or returns non-zero exit code.

**Handling**:

- Makefile continues to next scanner (use `-` prefix or `|| true`)
- Partial results saved
- GitHub Action reports which scanners failed
- Developer investigates logs

### 2. Missing Baseline

**Scenario**: New scanner added, no baseline exists yet.

**Handling**:

- Comparison script skips if baseline missing
- Prints warning message
- Does not fail workflow
- Developer runs `make test-integration` and commits baseline

### 3. Non-Deterministic Output

**Scenario**: Scanner produces different output on each run.

**Handling**:

- Investigate root cause (random ordering, timestamps, etc.)
- Fix scanner to be deterministic
- Update tests to validate determinism

### 4. Large Diffs

**Scenario**: Scanner improvement touches many files.

**Handling**:

- GitHub Action shows full diff
- Developer reviews changes
- Updates baseline if expected
- Documents changes in PR description

## Performance Considerations

### Expected Timings

- **12 scanners** × **blueking-paas (~200k LOC)**
- Estimated per-scanner: 5-10 seconds
- Total: **1-2 minutes**

### Optimization Opportunities

1. **Parallel execution**: Run scanners concurrently

   - Requires: Change Makefile to use `&` and `wait`
   - Benefit: 3-5x speedup
   - Tradeoff: More complex error handling

2. **Caching**: Cache Astroid parse trees

   - Benefit: Faster subsequent runs
   - Tradeoff: Complexity, cache invalidation

3. **Selective scanning**: Only scan changed files
   - Benefit: Much faster on PRs
   - Tradeoff: Not truly "integration" test

**Decision**: Start with sequential execution, optimize if > 2 minutes.

## Security Considerations

1. **Git submodule**: blueking-paas is external code

   - **Risk**: Malicious code in submodule
   - **Mitigation**: Pin to specific commit, review updates

2. **Artifact upload**: Scan results may contain code snippets

   - **Risk**: Sensitive information exposure
   - **Mitigation**: Review baseline before committing, artifacts are private

3. **Workflow permissions**: Read-only by default
   - **Risk**: None, workflow doesn't need write access
   - **Mitigation**: Explicit `permissions: read-all`

## Testing Strategy

### Unit Tests

- Test comparison script with mock YAML files
- Test baseline update process
- Test failure scenarios

### Integration Tests

- Run `make test-integration` on main branch
- Verify all 12 outputs created
- Check YAML validity

### CI Tests

- Create test PR with no changes (should pass)
- Create test PR with scanner change (should fail)
- Verify diff output readable

## Alternatives Considered

### Alternative 1: JSON instead of YAML

**Pros**: Faster parsing, smaller files
**Cons**: Less human-readable
**Decision**: YAML for readability

### Alternative 2: SQLite for baseline storage

**Pros**: Queryable, efficient diffs
**Cons**: Binary format, harder to review in PRs
**Decision**: YAML files for transparency

### Alternative 3: Compare full output including metadata

**Pros**: Catches all changes
**Cons**: False positives from timestamps, durations
**Decision**: Only compare `results` section

### Alternative 4: Hash-based comparison

**Pros**: Fast, compact
**Cons**: No diff output, harder to debug
**Decision**: Diff for better debugging

## Future Enhancements

1. **Performance regression detection**: Track scan duration over time
2. **Coverage metrics**: Track how many patterns detected
3. **Parallel execution**: Speed up integration tests
4. **Incremental scanning**: Only scan changed files in PRs
5. **Visual diffs**: HTML report of changes
6. **Automatic baseline updates**: Bot updates baseline on approval
