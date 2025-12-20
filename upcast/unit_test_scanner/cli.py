"""CLI interface for unit test scanner."""

import logging
import sys
from pathlib import Path

from upcast.common.file_utils import collect_python_files
from upcast.unit_test_scanner.checker import check_file
from upcast.unit_test_scanner.export import export_to_json, export_to_yaml
from upcast.unit_test_scanner.test_parser import UnitTestInfo

logger = logging.getLogger(__name__)


def scan_unit_tests(
    path: str,
    root_modules: list[str] | None = None,
    output: str | None = None,
    output_format: str = "yaml",
    include: list[str] | None = None,
    exclude: list[str] | None = None,
    no_default_excludes: bool = False,
    verbose: bool = False,
) -> list[UnitTestInfo]:
    """Scan for unit tests in Python files.

    Args:
        path: File or directory path to scan
        root_modules: List of root module prefixes to match (None = match all)
        output: Optional output file path
        output_format: Output format ('yaml' or 'json')
        include: Include patterns (glob)
        exclude: Exclude patterns (glob)
        no_default_excludes: Disable default exclude patterns
        verbose: Enable verbose logging

    Returns:
        List of detected test functions

    Raises:
        SystemExit: If path doesn't exist
    """
    # Configure logging
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Validate path
    path_obj = Path(path)
    if not path_obj.exists():
        logger.error(f"Path does not exist: {path}")
        sys.exit(1)

    # Collect files
    try:
        files = collect_python_files(
            path_obj,
            include_patterns=include or [],
            exclude_patterns=exclude or [],
            use_default_excludes=not no_default_excludes,
        )
    except Exception:
        logger.exception("Failed to collect files")
        sys.exit(1)

    logger.debug(f"Collected {len(files)} Python files")

    # Scan files
    all_tests: list[UnitTestInfo] = []
    for file_path in files:
        # Only scan test files
        file_name = file_path.name
        if file_name.startswith("test_") or file_name.endswith("_test.py"):
            logger.debug(f"Scanning {file_path}")
            tests = check_file(file_path, root_modules)
            all_tests.extend(tests)
            logger.debug(f"Found {len(tests)} tests in {file_path}")

    logger.debug(f"Total tests found: {len(all_tests)}")

    # Export results with relative paths (use path as base if it's a directory)
    output_path = Path(output) if output else None
    base_path = path_obj if path_obj.is_dir() else path_obj.parent

    if output_format == "json":
        result = export_to_json(all_tests, output_path, base_path=base_path)
    else:
        result = export_to_yaml(all_tests, output_path, base_path=base_path)

    # Output to stdout if no file specified
    if not output:
        print(result)

    return all_tests
