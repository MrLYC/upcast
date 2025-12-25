# Technical Design: GitHub Actions Improvements

## Context

The project uses GitHub Actions for CI/CD with the following workflows:

- `main.yml` - Code quality checks and tests on main branch and PRs
- `scanner-integration.yml` - Validates scanner outputs against committed baselines
- `on-release-main.yml` - Publishes to PyPI on GitHub releases

Current problems:

1. Scanner integration tests produce unstable YAML output due to:

   - Non-deterministic key ordering in dictionaries
   - Inconsistent quote styles (single vs double)
   - Array ordering differences in metadata fields
   - This causes false positive failures: https://github.com/MrLYC/upcast/actions/runs/20498769620/job/58902894286

2. Release process requires manual steps:
   - Creating GitHub release
   - Manual version updates
   - No automated testing before publish

## Goals / Non-Goals

**Goals:**

- Stable, deterministic scanner integration tests
- Automated PyPI publishing on version tags
- Zero false positives from formatting differences
- Catch real scanner behavior changes

**Non-Goals:**

- Changing scanner output format itself
- Migrating from YAML to another format
- Comprehensive integration test refactoring
- Multi-environment testing (current Ubuntu-only is fine)

## Decisions

### Decision 1: YAML Normalization Approach

**Choice:** Use Python script with PyYAML for normalization

**Rationale:**

- PyYAML already installed (dependency of the project)
- Provides programmatic control over sorting and formatting
- Can handle edge cases better than shell scripts
- Reproducible across different environments

**Alternatives Considered:**

- `yq` with sorting flags: Limited control over nested structures and specific fields
- `jq`: Would require YAML→JSON→YAML conversion, losing comments
- `diff --ignore-space-change`: Too coarse, doesn't handle quote styles

### Decision 2: Tag-Based Publishing Instead of Release-Based

**Choice:** Trigger on git tags (`v*.*.*`) instead of GitHub releases

**Rationale:**

- Git tags are simpler and more developer-friendly
- No need to create GitHub release in UI
- Tag = version = single source of truth
- `git tag v1.2.3 && git push --tags` is the standard workflow

**Alternatives Considered:**

- Keep GitHub release trigger: Extra step, less automated
- Manual workflow dispatch: Not truly automated
- Schedule-based: No clear trigger for when to publish

### Decision 3: Version Validation

**Choice:** Verify tag matches `pyproject.toml` version before publishing

**Rationale:**

- Prevents accidental publishes with wrong version
- Ensures package metadata is correct
- Fails fast with clear error message

**Implementation:**

```bash
TAG_VERSION="${GITHUB_REF#refs/tags/v}"  # Remove 'refs/tags/v' prefix
TOML_VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)
if [ "$TAG_VERSION" != "$TOML_VERSION" ]; then
  echo "Version mismatch: tag=$TAG_VERSION, pyproject.toml=$TOML_VERSION"
  exit 1
fi
```

## Technical Details

### YAML Normalization Script

Location: `.github/scripts/compare-scan-yaml.py`

```python
#!/usr/bin/env python3
"""Normalize YAML output for stable comparisons."""
import sys
import yaml

def sort_dict_recursive(obj):
    """Sort dictionary keys recursively."""
    if isinstance(obj, dict):
        return {k: sort_dict_recursive(v) for k, v in sorted(obj.items())}
    elif isinstance(obj, list):
        # Sort specific metadata arrays but preserve order for semantic lists
        return [sort_dict_recursive(item) for item in obj]
    return obj

def normalize_yaml(file_path):
    """Load, normalize, and re-serialize YAML."""
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    # Extract results section (ignore metadata)
    if 'results' in data:
        data = data['results']

    # Sort keys recursively
    normalized = sort_dict_recursive(data)

    # Serialize with consistent style
    return yaml.dump(normalized,
                     default_flow_style=False,
                     sort_keys=True,
                     allow_unicode=True)

if __name__ == '__main__':
    print(normalize_yaml(sys.argv[1]), end='')
```

### Updated Comparison Logic

Replace the comparison section in `scanner-integration.yml`:

```yaml
- name: Compare results
  run: |
    for file in example/scan-results/*.yaml; do
      filename=$(basename "$file")

      # Normalize committed version
      git show "HEAD:$file" | python .github/scripts/compare-scan-yaml.py > /tmp/old.yaml

      # Normalize current version
      python .github/scripts/compare-scan-yaml.py "$file" > /tmp/new.yaml

      # Compare
      if ! diff -u /tmp/old.yaml /tmp/new.yaml > /tmp/diff-$filename.txt; then
        echo "⚠️ Results changed in $filename"
        cat /tmp/diff-$filename.txt
        DIFF_FOUND=1
      fi
    done
```

### PyPI Publishing Workflow

Location: `.github/workflows/publish-on-tag.yml`

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*.*.*"

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-uv-env

      - name: Run tests
        run: |
          make check
          make test
          make test-integration

  publish:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-uv-env

      - name: Validate version
        run: |
          TAG_VERSION="${GITHUB_REF#refs/tags/v}"
          TOML_VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)
          if [ "$TAG_VERSION" != "$TOML_VERSION" ]; then
            echo "::error::Version mismatch: tag=$TAG_VERSION, pyproject.toml=$TOML_VERSION"
            exit 1
          fi
          echo "✓ Version validated: $TAG_VERSION"

      - name: Build and publish
        run: make publish
        env:
          UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

## Risks / Trade-offs

### Risk: False negatives (missing real changes)

**Mitigation:**

- Keep metadata section comparison as-is (timestamps, counts)
- Only normalize the `results` section
- Test with known scanner improvements to ensure changes are detected

### Risk: Python script dependency

**Mitigation:**

- PyYAML is already a project dependency
- Script is simple and well-tested
- Fallback: manual comparison if script fails

### Risk: Tag-based publishing might publish broken code

**Mitigation:**

- All tests run before publishing (test job must succeed)
- Version validation fails fast on mismatch
- Can always delete/retag if needed

## Migration Plan

1. **Phase 1: Fix integration tests**

   - Add normalization script
   - Update scanner-integration.yml
   - Test on develop branch
   - Verify no false positives

2. **Phase 2: Add PyPI publishing**

   - Create publish-on-tag.yml workflow
   - Add PYPI_TOKEN secret if not exists
   - Test with pre-release tag (v0.0.0-test)
   - Document new release process

3. **Rollback:**
   - If normalization causes issues: revert to old comparison
   - If publishing fails: delete tag, fix, re-tag
   - Workflows are independent: can rollback individually

## Open Questions

- Should we normalize all arrays or just specific metadata fields?
  → Start conservative: only sort dict keys, keep array order

- Should we support both GitHub releases and tags?
  → No, simplify to tags only

- Should we publish to TestPyPI first?
  → Not in initial implementation, can add later if needed
