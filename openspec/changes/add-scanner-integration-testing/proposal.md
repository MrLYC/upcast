# Proposal: Add Scanner Integration Testing

## Why

**Current Gap**: The project lacks automated integration testing for all scanners working together on a real-world codebase. While unit tests validate individual scanner functionality, there's no mechanism to:

1. Verify all scanners work correctly on a large, realistic Django project
2. Detect regressions in scanner output quality or accuracy
3. Ensure scanning results remain deterministic across code changes
4. Provide a comprehensive example of scanner capabilities

**Use Case**: The `example/blueking-paas` directory contains a real-world Django application (蓝鲸 PaaS) that's ideal for integration testing. By scanning this project with all 12 scanners and tracking results, we can:

- **Catch regressions**: Any change in YAML output indicates behavioral changes
- **Validate consistency**: Ensure scanners produce identical output across runs
- **Document capabilities**: Generated scan results serve as real-world examples
- **CI/CD validation**: GitHub Actions can verify no unexpected changes

**Real-World Impact**: This prevents bugs like:

- Scanner silently stopping detection of patterns after refactoring
- Output format changes that break downstream consumers
- Performance regressions on large codebases

## What Changes

### 1. Makefile Integration Test Command

Add `make test-integration` command that:

- Scans `example/blueking-paas` with all 12 scanners
- Outputs results to `example/scan-results/` directory
- Uses YAML format for human readability
- Captures scan duration and statistics

**Scanners to run** (12 total):

- `scan-blocking-operations`
- `scan-complexity-patterns`
- `scan-concurrency-patterns`
- `scan-django-models`
- `scan-django-settings`
- `scan-django-urls`
- `scan-env-vars`
- `scan-exception-handlers`
- `scan-http-requests`
- `scan-metrics`
- `scan-signals`
- `scan-unit-tests`

### 2. Output Structure

```
example/scan-results/
├── blocking-operations.yaml
├── complexity-patterns.yaml
├── concurrency-patterns.yaml
├── django-models.yaml
├── django-settings.yaml
├── django-urls.yaml
├── env-vars.yaml
├── exception-handlers.yaml
├── http-requests.yaml
├── metrics.yaml
├── signals.yaml
└── unit-tests.yaml
```

### 3. GitHub Action: Scan Consistency Check

Add `.github/workflows/scanner-integration.yml` that:

- Runs on PRs and main branch pushes
- Executes `make test-integration`
- Compares new scan results against committed baseline
- **Fails if YAML `results` sections differ** (indicates regression)
- Allows updating baseline when intentional changes occur

**Key validation**: Extract `results:` section from each YAML and compare using deterministic diff:

```bash
# Extract results section (skip metadata like scan_duration_ms)
yq '.results' baseline.yaml > baseline-results.yaml
yq '.results' new.yaml > new-results.yaml
diff -u baseline-results.yaml new-results.yaml
```

### 4. Baseline Scan Results (Optional)

Optionally commit initial scan results as baseline:

- Provides regression detection from day one
- Serves as documentation of expected output
- Can be regenerated with `make test-integration-update`

## How

See `tasks.md` for detailed implementation steps.

## Impact

### Benefits

1. **Quality Assurance**: Automated detection of scanner regressions
2. **Documentation**: Real-world examples for all scanner outputs
3. **Confidence**: Can refactor scanners knowing tests catch breakage
4. **CI/CD Integration**: Automated validation in GitHub Actions

### Performance

- Integration test adds ~30-60s to CI pipeline (scanning large Django project)
- Only runs on PRs/main, not on every commit
- Can be parallelized if needed

### Maintenance

- Baseline results need updates when:
  - Scanner logic intentionally changes
  - New patterns added to detection
  - Bug fixes change output
- Simple workflow: `make test-integration-update` + commit

## Alternatives Considered

### Alternative 1: Unit Tests Only

**Pros**: Faster, more focused
**Cons**: Miss integration issues, no real-world validation
**Decision**: Rejected - need both unit and integration tests

### Alternative 2: Mock Project Instead of Real Code

**Pros**: Smaller, faster to scan
**Cons**: Artificial, may miss real-world edge cases
**Decision**: Rejected - real project is more valuable

### Alternative 3: Snapshot All Fields (Including Metadata)

**Pros**: Catches all changes
**Cons**: Fails on expected variations (scan_duration_ms, timestamps)
**Decision**: Rejected - only compare `results` section

## Success Criteria

1. **Makefile Command**:

   - [ ] `make test-integration` runs all 12 scanners
   - [ ] Outputs to `example/scan-results/*.yaml`
   - [ ] Completes successfully on blueking-paas project
   - [ ] Takes < 2 minutes to complete

2. **GitHub Action**:

   - [ ] Runs on PR and main branch
   - [ ] Compares `results` sections of YAML files
   - [ ] Fails on unexpected differences
   - [ ] Provides clear diff output
   - [ ] Can be updated with new baseline

3. **Documentation**:

   - [ ] README documents integration testing
   - [ ] Instructions for updating baseline
   - [ ] Example scan results committed (optional)

4. **Validation**:
   - [ ] Action detects intentional changes (add test case)
   - [ ] Action passes on identical scans
   - [ ] No false positives from non-deterministic fields
