#!/usr/bin/env python3
"""Compare YAML scan results with semantic normalization.

This script compares YAML files or entire directories of scanner results,
with intelligent normalization to ignore formatting differences while detecting real changes.

Features:
- Extracts 'results' section (ignores metadata like timestamps, counts)
- Recursively sorts dictionary keys for stable comparison
- Generates unified diff with context
- Checks git history for baseline comparison
- Supports both single file and directory comparison modes

Exit codes:
  0 - All files are semantically identical
  1 - Files differ (intentional changes or regressions)
  2 - Error occurred

Usage:
    # Compare two files
    python compare-scan-yaml.py old.yaml new.yaml

    # Compare directory against git baseline
    python compare-scan-yaml.py --check-dir example/scan-results/

    # Custom diff truncation
    python compare-scan-yaml.py old.yaml new.yaml --max-lines 50
"""

import argparse
import difflib
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


def sort_dict_recursive(obj: Any) -> Any:
    """Sort dictionary keys recursively for stable comparison.

    Args:
        obj: The object to sort (dict, list, or primitive)

    Returns:
        Sorted object with same structure
    """
    if isinstance(obj, dict):
        return {k: sort_dict_recursive(v) for k, v in sorted(obj.items())}
    elif isinstance(obj, list):
        # Preserve list order but sort nested structures
        return [sort_dict_recursive(item) for item in obj]
    return obj


def load_and_normalize(file_path: str) -> str:
    """Load YAML file and normalize for comparison.

    Args:
        file_path: Path to YAML file

    Returns:
        Normalized YAML as string

    Raises:
        FileNotFoundError: If file doesn't exist
        yaml.YAMLError: If YAML is invalid
    """
    with open(file_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Extract results section (ignore metadata)
    if isinstance(data, dict) and "results" in data:
        data = data["results"]

    # Sort keys recursively for stable comparison
    normalized = sort_dict_recursive(data)

    # Serialize with consistent style
    return yaml.dump(
        normalized,
        default_flow_style=False,
        sort_keys=True,
        allow_unicode=True,
        width=120,
    )


def compare_yaml_files(old_file: str, new_file: str, max_lines: int = 100) -> tuple[bool, list[str]]:
    """Compare two YAML files with normalization.

    Args:
        old_file: Path to old/committed YAML file
        new_file: Path to new/generated YAML file
        max_lines: Maximum diff lines to include in output

    Returns:
        Tuple of (files_identical, diff_lines)
    """
    try:
        old_content = load_and_normalize(old_file)
        new_content = load_and_normalize(new_file)
    except FileNotFoundError as e:
        return False, [f"Error: File not found - {e}"]
    except yaml.YAMLError as e:
        return False, [f"Error: Invalid YAML - {e}"]
    except Exception as e:
        return False, [f"Error: {e}"]

    # Quick equality check
    if old_content == new_content:
        return True, []

    # Generate unified diff
    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff_lines = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"committed/{Path(old_file).name}",
            tofile=f"generated/{Path(new_file).name}",
            lineterm="",
        )
    )

    # Truncate if too long
    if len(diff_lines) > max_lines:
        truncated = diff_lines[:max_lines]
        truncated.append(f"\n... (diff truncated, {len(diff_lines) - max_lines} more lines)")
        return False, truncated

    return False, diff_lines


def get_git_baseline(file_path: str) -> str | None:
    """Get committed version of file from git.

    Args:
        file_path: Path to file in working tree

    Returns:
        Content of committed file, or None if file not in git
    """
    try:
        # Check if file is tracked by git
        subprocess.run(  # noqa: S603
            ["git", "ls-files", "--error-unmatch", file_path],  # noqa: S607
            check=True,
            capture_output=True,
            text=True,
        )

        # Get committed version
        result = subprocess.run(  # noqa: S603
            ["git", "show", f"HEAD:{file_path}"],  # noqa: S607
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return None
    else:
        return result.stdout


def check_directory(results_dir: str, max_lines: int = 100) -> tuple[int, int, int]:
    """Check all YAML files in directory against git baseline.

    Args:
        results_dir: Directory containing YAML scan results
        max_lines: Maximum diff lines to display per file

    Returns:
        Tuple of (files_with_diffs, new_files, total_files)
    """
    results_path = Path(results_dir)
    if not results_path.is_dir():
        print(f"Error: {results_dir} is not a directory", file=sys.stderr)
        sys.exit(2)

    print("📊 Checking for scan result changes...")
    print("Using semantic YAML comparison to ignore formatting differences")
    print()

    yaml_files = sorted(results_path.glob("*.yaml"))
    if not yaml_files:
        print(f"⚠️  No YAML files found in {results_dir}")
        return 0, 0, 0

    files_with_diffs = 0
    new_files = 0
    total_files = len(yaml_files)

    for yaml_file in yaml_files:
        filename = yaml_file.name

        # Check git history
        baseline_content = get_git_baseline(str(yaml_file))

        if baseline_content is None:
            print(f"⚠️  {filename} is new (not in git history yet)")
            print("    This is expected for new scanners.")
            print("    Commit the file to establish baseline.")
            new_files += 1
            print()
            continue

        # Write baseline to temp file for comparison
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write(baseline_content)
            tmp_path = tmp.name

        try:
            identical, diff_lines = compare_yaml_files(tmp_path, str(yaml_file), max_lines)

            if not identical:
                if diff_lines and diff_lines[0].startswith("Error:"):
                    print(f"⚠️  {filename}: {diff_lines[0]}", file=sys.stderr)
                else:
                    print(f"⚠️  Results changed in {filename}:")
                    print("----------------------------------------")
                    print("".join(diff_lines))
                    print("----------------------------------------")
                files_with_diffs += 1
            else:
                print(f"✅ {filename}: no changes")

            print()
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    return files_with_diffs, new_files, total_files


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Compare YAML scan results with semantic normalization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare two specific files
  %(prog)s old.yaml new.yaml

  # Check entire directory against git baseline
  %(prog)s --check-dir example/scan-results/

  # Limit diff output
  %(prog)s old.yaml new.yaml --max-lines 50

Exit codes:
  0 - All files are semantically identical
  1 - Files differ (changes detected)
  2 - Error occurred
        """,
    )

    # Support two modes: file comparison or directory checking
    parser.add_argument(
        "old_file",
        nargs="?",
        help="Path to old/committed YAML file (for file mode)",
    )
    parser.add_argument(
        "new_file",
        nargs="?",
        help="Path to new/generated YAML file (for file mode)",
    )
    parser.add_argument(
        "--check-dir",
        metavar="DIR",
        help="Check all YAML files in directory against git baseline (for directory mode)",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=100,
        help="Maximum diff lines to display per file (default: 100)",
    )

    args = parser.parse_args()

    # Directory checking mode
    if args.check_dir:
        files_with_diffs, new_files, total_files = check_directory(args.check_dir, args.max_lines)

        print()
        if files_with_diffs > 0:
            print("::warning::Scanner results changed. Review diffs above.")
            print()
            print("If changes are intentional (scanner improvements):")
            print("  1. Review the diffs to ensure they are correct")
            print("  2. Run: make test-integration")
            print("  3. Commit: git add example/scan-results/ && git commit -m 'Update scan results'")
            print()
            print("If changes are unexpected (possible bugs):")
            print("  1. Investigate which code change caused the diff")
            print("  2. Fix the scanner or revert the problematic change")
            sys.exit(1)
        elif new_files > 0:
            print("⚠️  Some scanner result files are new.")
            print("To establish baseline:")
            print("  1. Run: make test-integration")
            print("  2. Commit: git add example/scan-results/ && git commit -m 'Add new scanner results'")
            sys.exit(0)
        else:
            print("✅ All scan results match committed baseline")
            sys.exit(0)

    # File comparison mode
    if not args.old_file or not args.new_file:
        parser.error("Either provide old_file and new_file, or use --check-dir")

    identical, diff_lines = compare_yaml_files(args.old_file, args.new_file, args.max_lines)

    if identical:
        print(f"✅ {Path(args.new_file).name}: no changes")
        sys.exit(0)
    else:
        if diff_lines and diff_lines[0].startswith("Error:"):
            print(diff_lines[0], file=sys.stderr)
            sys.exit(2)
        else:
            print(f"⚠️  {Path(args.new_file).name}: changes detected")
            print("".join(diff_lines))
            sys.exit(1)


if __name__ == "__main__":
    main()
