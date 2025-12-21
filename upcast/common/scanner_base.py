"""Abstract base class for all scanners.

This module provides the BaseScanner class that all scanner implementations
should extend to ensure consistent behavior for file discovery and filtering.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar

from upcast.common.patterns import match_patterns
from upcast.models.base import ScannerOutput

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
