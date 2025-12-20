"""Export utilities for test scan results."""

import json
from pathlib import Path
from typing import Any

from upcast.common.export import export_to_yaml as common_export_to_yaml
from upcast.unit_test_scanner.test_parser import UnitTestInfo


def format_test_output(tests: list[UnitTestInfo], base_path: Path | None = None) -> dict[str, list[dict[str, Any]]]:  # noqa: C901
    """Format tests for export, grouped by file.

    Args:
        tests: List of test functions
        base_path: Base path for relative file paths (None = use absolute paths)

    Returns:
        Dictionary mapping file paths to test data
    """
    # Group tests by file
    tests_by_file: dict[str, list[UnitTestInfo]] = {}
    for test in tests:
        file_key = test.file
        # Convert to relative path if base_path provided
        if base_path:
            try:
                file_path = Path(test.file)
                if file_path.is_absolute():
                    file_key = str(file_path.relative_to(base_path))
            except (ValueError, OSError):
                # Keep absolute path if relative conversion fails
                pass

        if file_key not in tests_by_file:
            tests_by_file[file_key] = []
        tests_by_file[file_key].append(test)

    # Sort tests by line number within each file
    for file_tests in tests_by_file.values():
        file_tests.sort(key=lambda t: t.line)

    # Convert to output format
    output: dict[str, list[dict[str, Any]]] = {}
    for file_path in sorted(tests_by_file.keys()):
        test_list = []
        for test in tests_by_file[file_path]:
            test_dict: dict[str, Any] = {
                "name": test.name,
                "line_range": list(test.line_range),
                "body_md5": test.body_md5,
                "assert_count": test.assert_count,
            }

            # Add targets if present
            if test.targets:
                targets_list = []
                for target in sorted(test.targets, key=lambda t: t.module):
                    targets_list.append({
                        "module": target.module,
                        "symbols": sorted(target.symbols),
                    })
                test_dict["targets"] = targets_list
            else:
                test_dict["targets"] = []

            test_list.append(test_dict)

        output[file_path] = test_list

    return output


def export_to_yaml(tests: list[UnitTestInfo], output_path: Path | None = None, base_path: Path | None = None) -> str:
    """Export tests to YAML format.

    Args:
        tests: List of test functions
        output_path: Optional path to write YAML file
        base_path: Base path for relative file paths

    Returns:
        YAML string
    """
    data = format_test_output(tests, base_path=base_path)

    if output_path:
        common_export_to_yaml(data, output_path)
        return ""
    else:
        # Return YAML string
        import yaml

        return yaml.dump(data, sort_keys=False, allow_unicode=True, indent=2)


def export_to_json(tests: list[UnitTestInfo], output_path: Path | None = None, base_path: Path | None = None) -> str:
    """Export tests to JSON format.

    Args:
        tests: List of test functions
        output_path: Optional path to write JSON file
        base_path: Base path for relative file paths

    Returns:
        JSON string
    """
    data = format_test_output(tests, base_path=base_path)

    json_str = json.dumps(data, indent=2, ensure_ascii=False)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json_str, encoding="utf-8")

    return json_str
