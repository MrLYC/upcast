"""Pattern matching for file filtering."""

from pathlib import Path
from typing import Optional

# Default patterns to exclude
DEFAULT_EXCLUDES = [
    "venv/**",
    "env/**",
    ".venv/**",
    "virtualenv/**",
    "site-packages/**",
    "__pycache__/**",
    "*.pyc",
    "build/**",
    "dist/**",
    "*.egg-info/**",
    ".tox/**",
    ".pytest_cache/**",
    ".mypy_cache/**",
    "node_modules/**",
    ".git/**",
]


def match_patterns(path: Path, patterns: list[str]) -> bool:
    """Check if path matches any of the given glob patterns.

    Args:
        path: Path to check (should be relative for pattern matching)
        patterns: List of glob patterns

    Returns:
        True if path matches at least one pattern
    """
    path_str = str(path).replace("\\", "/")  # Normalize for cross-platform

    for pattern in patterns:
        # Use pathlib's match which supports glob patterns
        if path.match(pattern):
            return True

        # Handle patterns like "venv/**" by checking if path starts with "venv/"
        if "/**" in pattern:
            prefix = pattern.replace("/**", "")
            if path_str.startswith(f"{prefix}/") or path_str == prefix:
                return True

        # Also try simple string matching for exact matches
        if path_str == pattern or path_str.endswith(f"/{pattern}"):
            return True

    return False


def should_exclude(
    path: Path,
    include_patterns: Optional[list[str]] = None,
    exclude_patterns: Optional[list[str]] = None,
    use_default_excludes: bool = True,
) -> bool:
    """Determine if a file should be excluded based on patterns.

    Processing order:
    1. Check default excludes (if enabled)
    2. Check custom exclude patterns
    3. Check include patterns (if specified)

    Args:
        path: Relative path to check
        include_patterns: Patterns for files to include (if None, include all)
        exclude_patterns: Patterns for files to exclude
        use_default_excludes: Whether to apply DEFAULT_EXCLUDES

    Returns:
        True if file should be excluded
    """
    # Check default excludes first
    if use_default_excludes and match_patterns(path, DEFAULT_EXCLUDES):
        return True

    # Check custom excludes
    if exclude_patterns and match_patterns(path, exclude_patterns):
        return True

    # Check includes (if specified, must match at least one)
    return bool(include_patterns and not match_patterns(path, include_patterns))
