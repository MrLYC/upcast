"""Abstract base class for all scanners.

This module provides the BaseScanner class that all scanner implementations
should extend to ensure consistent behavior for file discovery and filtering.
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar

from astroid import nodes

from upcast.common.patterns import match_patterns
from upcast.models.base import ScannerOutput

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=ScannerOutput)


class BaseScanner(ABC, Generic[T]):
    """Abstract base class for all scanners.

    All scanner implementations should extend this class and implement
    the abstract methods: scan() and scan_file().

    Type Parameters:
        T: The ScannerOutput type this scanner produces

    Attributes:
        include_patterns: File patterns to include (glob patterns)
        exclude_patterns: File patterns to exclude (glob patterns)
        verbose: Whether to output verbose logging
    """

    def __init__(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ):
        """Initialize the base scanner.

        Args:
            include_patterns: Glob patterns for files to include (default: ["**/*.py"])
            exclude_patterns: Glob patterns for files to exclude (default: [])
            verbose: Enable verbose output
        """
        self.include_patterns = include_patterns or ["**/*.py"]
        self.exclude_patterns = exclude_patterns or []
        self.verbose = verbose

    @abstractmethod
    def scan(self, path: Path) -> T:
        """Scan the given path and return typed results.

        This is the main entry point for the scanner. It should discover
        files, scan them, and return a complete ScannerOutput.

        Args:
            path: Directory or file path to scan

        Returns:
            Complete scanner output with summary, results, and metadata
        """
        ...

    @abstractmethod
    def scan_file(self, file_path: Path) -> Any:
        """Scan a single file.

        Returns scanner-specific intermediate results. The exact return type
        varies by scanner implementation.

        Args:
            file_path: Path to the file to scan

        Returns:
            Scanner-specific intermediate results
        """
        ...

    def get_files_to_scan(self, path: Path) -> list[Path]:
        """Get list of files to scan based on include/exclude patterns.

        Args:
            path: Directory or file path to scan

        Returns:
            List of file paths that match include patterns and don't match exclude patterns
        """
        if path.is_file():
            return [path] if self.should_scan_file(path) else []

        # Collect files matching include patterns
        files: set[Path] = set()
        for pattern in self.include_patterns:
            matched = path.glob(pattern)
            files.update(f for f in matched if f.is_file())

        # Filter with should_scan_file (applies exclude logic)
        return sorted(f for f in files if self.should_scan_file(f))

    def should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned.

        Args:
            file_path: Path to check (can be absolute or relative)

        Returns:
            True if file should be scanned, False otherwise
        """
        # Check exclude patterns first
        if self.exclude_patterns and match_patterns(file_path, self.exclude_patterns):
            return False

        # Check include patterns
        if self.include_patterns:
            return match_patterns(file_path, self.include_patterns)

        return True

    def parse_file(self, file_path: Path) -> nodes.Module | None:
        """Parse Python file to AST module with unified error handling.

        This method provides consistent file parsing behavior across all scanners:
        - Reads file with UTF-8 encoding
        - Parses to astroid Module
        - Logs warnings on failure
        - Returns None on any error

        Args:
            file_path: Path to Python file to parse

        Returns:
            Parsed astroid Module, or None if parsing fails

        Examples:
            >>> module = self.parse_file(Path("app.py"))
            >>> if module:
            ...     # Process module
            ...     pass
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Import astroid here to avoid deprecation warning in type hint
            import astroid

            return astroid.parse(content, path=str(file_path))

        except FileNotFoundError:
            if self.verbose:
                logger.warning("File not found: %s", file_path)
            return None
        except UnicodeDecodeError:
            if self.verbose:
                logger.warning("Failed to decode file (encoding issue): %s", file_path)
            return None
        except Exception as e:
            # Catch AstroidSyntaxError and other exceptions
            if self.verbose:
                logger.warning("Failed to parse %s: %s", file_path, e)
            return None
