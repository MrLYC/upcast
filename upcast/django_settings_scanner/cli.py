"""Command-line interface for Django settings scanner."""

from pathlib import Path

import click

from upcast.common.file_utils import collect_python_files, validate_path
from upcast.django_settings_scanner.checker import DjangoSettingsChecker
from upcast.django_settings_scanner.export import (
    export_combined,
    export_definitions_only,
    export_to_yaml_string,
    export_usages_only,
)


def format_definition_display(name: str, definition) -> str:
    """Format a single setting definition for console display.

    Args:
        name: Setting name
        definition: SettingsDefinition object

    Returns:
        Formatted string for display
    """
    lines = [f"  {name}:"]

    # Check if value is dynamic (wrapped in backticks)
    if isinstance(definition.value, str) and definition.value.startswith("`") and definition.value.endswith("`"):
        # Dynamic value - use statement field
        statement = definition.value[1:-1]  # Remove backticks
        lines.append(f"    statement: {statement}")
    else:
        # Static value - use value field
        lines.append(f"    value: {definition.value}")

    lines.append(f"    lineno: {definition.line}")
    return "\n".join(lines)


def _process_files(checker: DjangoSettingsChecker, files: list[Path], verbose: bool) -> None:
    """Process Python files with the checker.

    Args:
        checker: DjangoSettingsChecker instance
        files: List of files to process
        verbose: Enable verbose output
    """
    for file_path in files:
        if verbose:
            click.echo(f"Scanning: {file_path}")
        try:
            checker.check_file(str(file_path))
        except Exception as e:
            click.echo(f"Error scanning {file_path}: {e!s}", err=True)


def scan_django_settings(  # noqa: C901
    path: str,
    output: str | None = None,
    verbose: bool = False,
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    use_default_excludes: bool = True,
    scan_definitions: bool = False,
    scan_usages: bool = True,
    output_mode: str = "auto",
) -> dict:
    """Scan Django project for settings usage and/or definitions.

    Args:
        path: Path to scan (file or directory)
        output: Optional output file path for YAML
        verbose: Enable verbose output
        include_patterns: File patterns to include
        exclude_patterns: File patterns to exclude
        use_default_excludes: Use default exclude patterns
        scan_definitions: Whether to scan for settings definitions
        scan_usages: Whether to scan for settings usages
        output_mode: Output mode - 'auto', 'definitions', 'usages', or 'combined'

    Returns:
        Dictionary of results (settings usages and/or definitions)
    """
    try:
        # Validate path using common utilities
        root_path = validate_path(path)
    except (FileNotFoundError, ValueError) as e:
        raise click.ClickException(str(e)) from e

    # Determine base path for relative path calculation
    base_path = root_path if root_path.is_dir() else root_path.parent

    # Initialize checker
    checker = DjangoSettingsChecker(str(base_path))

    # Scan definitions if requested
    if scan_definitions:
        if verbose:
            click.echo(f"Scanning for settings definitions in {root_path}...")
        checker.scan_definitions(str(root_path))

        if verbose and checker.definitions:
            total_defs = sum(len(mod.definitions) for mod in checker.definitions.values())
            click.echo(f"Found {len(checker.definitions)} settings modules with {total_defs} definitions.")

    # Scan usages if requested
    if scan_usages:
        # Collect Python files using common utilities
        if verbose:
            click.echo(f"Collecting Python files from {root_path}...")
        python_files = collect_python_files(
            root_path,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            use_default_excludes=use_default_excludes,
        )

        if not python_files:
            if not scan_definitions:
                click.echo("No Python files found.")
                return {}
        else:
            if verbose:
                click.echo(f"Found {len(python_files)} Python files.")

            # Process files
            _process_files(checker, python_files, verbose)

            if verbose and checker.settings:
                total_usages = sum(var.count for var in checker.settings.values())
                click.echo(f"Found {len(checker.settings)} unique settings with {total_usages} total usages.")

    # Determine output mode
    actual_mode = output_mode
    if actual_mode == "auto":
        if scan_definitions and scan_usages:
            actual_mode = "combined"
        elif scan_definitions:
            actual_mode = "definitions"
        else:
            actual_mode = "usages"

    # Output results
    if output:
        if actual_mode == "definitions":
            export_definitions_only(checker.definitions, output)
        elif actual_mode == "usages":
            export_usages_only(checker.settings, output)
        else:  # combined
            export_combined(checker.definitions, checker.settings, output)
        click.echo(f"Results written to {output}")
    else:
        # Print to stdout
        if actual_mode == "definitions":
            # Format definitions for display
            click.echo("\n=== Settings Definitions ===")
            for module_path, module in sorted(checker.definitions.items()):
                # Skip empty modules (no definitions, no imports)
                if not module.definitions and not module.star_imports and not module.dynamic_imports:
                    continue
                click.echo(f"\n{module_path}:")
                for name, definition in sorted(module.definitions.items()):
                    click.echo(format_definition_display(name, definition))
        elif actual_mode == "usages":
            if checker.settings:
                yaml_output = export_to_yaml_string(checker.settings)
                click.echo("\n" + yaml_output)
            else:
                click.echo("No Django settings usage found.")
        else:  # combined
            if checker.definitions:
                click.echo("\n=== Settings Definitions ===")
                for module_path, module in sorted(checker.definitions.items()):
                    # Skip empty modules (no definitions, no imports)
                    if not module.definitions and not module.star_imports and not module.dynamic_imports:
                        continue
                    click.echo(f"\n{module_path}:")
                    for name, definition in sorted(module.definitions.items()):
                        click.echo(format_definition_display(name, definition))

            if checker.settings:
                click.echo("\n=== Settings Usages ===")
                yaml_output = export_to_yaml_string(checker.settings)
                click.echo(yaml_output)

    return {"definitions": checker.definitions, "usages": checker.settings}
