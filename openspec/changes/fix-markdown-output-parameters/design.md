# Design: Fix Markdown Output Parameters

## Context

A PR was merged that added markdown output support with language selection to some scanner commands. However, the changes were incomplete - not all commands received the necessary parameters, causing runtime errors.

## Current State

### Working Commands (Have Parameters)

- `scan-complexity-patterns`
- `scan-env-vars`
- `scan-logging`

### Broken Commands (Missing Parameters)

- 12 other scanner commands are missing the markdown parameters

### Parameter Pattern

Working commands follow this pattern:

```python
@main.command(name="scan-xyz")
@click.option("-o", "--output", ...)
@click.option("-v", "--verbose", ...)
@click.option(
    "--format",
    type=click.Choice(["yaml", "json", "markdown"], case_sensitive=False),
    default="yaml",
    help="Output format (yaml, json, or markdown)",
)
@click.option(
    "--markdown-language",
    type=click.Choice(["en", "zh"], case_sensitive=False),
    default="en",
    help="Language for markdown output (default: en)",
)
@click.option(
    "--markdown-title",
    type=str,
    help="Title for markdown output",
)
# ... other options ...
@click.argument("path", ...)
def scan_xyz_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,
    markdown_language: str,
    markdown_title: Optional[str],
    # ... other params ...
    path: str,
) -> None:
    scanner = XyzScanner(...)
    run_scanner_cli(
        scanner=scanner,
        path=path,
        output=output,
        format=format,
        markdown_title=markdown_title,
        markdown_language=markdown_language,
        # ... other args ...
    )
```

## Implementation Approach

### 1. Consistent Parameter Ordering

All commands should follow this order for markdown-related parameters:

1. `-o, --output`
2. `-v, --verbose`
3. `--format` (with markdown choice)
4. `--markdown-language`
5. `--markdown-title`
6. Scanner-specific options
7. `--include/--exclude` patterns
8. `--no-default-excludes`
9. `path` argument

### 2. Parameter Specifications

**`--format`**:

- Type: `click.Choice(["yaml", "json", "markdown"], case_sensitive=False)`
- Default: `"yaml"`
- Help: `"Output format (yaml, json, or markdown)"`

**`--markdown-language`**:

- Type: `click.Choice(["en", "zh"], case_sensitive=False)`
- Default: `"en"`
- Help: `"Language for markdown output (default: en)"`

**`--markdown-title`**:

- Type: `str`
- Default: `None` (Optional)
- Help: `"Title for markdown output"`

### 3. Function Signature Pattern

```python
def scan_xyz_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    markdown_language: str,
    markdown_title: Optional[str],
    # ... scanner-specific params ...
    path: str,
) -> None:
```

Note: `# noqa: A002` is needed because `format` is a Python builtin.

### 4. Call to run_scanner_cli

Always pass these parameters:

```python
run_scanner_cli(
    scanner=scanner,
    path=path,
    output=output,
    format=format,
    markdown_title=markdown_title,
    markdown_language=markdown_language,
    # ... other parameters ...
)
```

## Concurrent Fix: Django Model Scanner

While fixing the CLI parameters, also addressing the Django model field parameter duplication issue discovered in the output:

### Problem

The scanner was passing the entire `field_info` dict (including `type`, `name`, `line`) to `parameters`, causing duplication in the output.

### Solution

Filter out fields that are already DjangoField attributes:

```python
parameters = {k: v for k, v in field_info.items() if k not in ("type", "name", "line")}
```

This ensures `parameters` only contains actual field arguments like `max_length`, `default`, `null`, etc.

## Testing Strategy

1. **Integration Tests**: Run `make test-integration` to verify all commands execute
2. **Markdown Output**: Test at least one command with markdown format
3. **Language Support**: Verify both English and Chinese output
4. **Parameter Validation**: Ensure all scanners accept the new parameters
5. **Regression**: Check that YAML/JSON output still works correctly

## Rollout

Since this is a bug fix for broken functionality:

1. Fix all affected commands
2. Update integration test baselines if needed
3. No feature flag or gradual rollout needed
4. Changes are backward compatible (new optional parameters)
