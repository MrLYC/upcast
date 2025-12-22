"""Signal scanner implementation with Pydantic models.

This module provides signal detection for Django and Celery frameworks,
including signal handlers, custom signal definitions, and signal sends.
"""

from pathlib import Path
from typing import Any

from upcast.common.scanner_base import BaseScanner
from upcast.models.signals import SignalInfo, SignalOutput, SignalSummary, SignalUsage

# ============================================================================
# Scanner Implementation
# ============================================================================


class SignalScanner(BaseScanner[SignalOutput]):
    """Scanner for Django and Celery signal patterns.

    This scanner detects:
    - Django signal receivers (@receiver decorator, .connect())
    - Celery signal handlers (@task_success.connect, etc.)
    - Custom signal definitions (Signal())
    - Signal sends (.send(), .send_robust())

    Example:
        scanner = SignalScanner()
        output = scanner.scan(Path("/project"))
        print(f"Found {output.summary.total_count} signals")
    """

    def __init__(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ):
        """Initialize signal scanner.

        Args:
            include_patterns: File patterns to include (default: ["**/*.py"])
            exclude_patterns: File patterns to exclude
            verbose: Enable verbose output
        """
        super().__init__(include_patterns, exclude_patterns, verbose)

    def scan(self, path: Path) -> SignalOutput:
        """Scan for signal patterns in Python files.

        Args:
            path: Directory or file to scan

        Returns:
            SignalOutput with detected signals and summary
        """
        import time

        from upcast.common.signals.signal_checker import SignalChecker

        start_time = time.time()

        # Get files to scan
        files = self.get_files_to_scan(path)

        # Initialize checker from old implementation
        checker = SignalChecker(root_path=str(path.resolve()), verbose=self.verbose)

        # Scan each file
        for file_path in files:
            checker.check_file(str(file_path))

        # Get results from old checker
        old_results = checker.get_results()
        old_summary = checker.get_summary()

        # Transform to new model
        signals = self._transform_results(old_results)

        # Calculate summary
        summary = self._calculate_summary(
            signals=signals,
            files_scanned=len(files),
            scan_duration_ms=int((time.time() - start_time) * 1000),
            old_summary=old_summary,
        )

        return SignalOutput(
            summary=summary,
            results=signals,
            metadata={
                "scanner_name": "signal",
                "root_path": str(path.resolve()),
            },
        )

    def scan_file(self, file_path: Path) -> Any:
        """Scan a single file for signals.

        This method is provided for compatibility with BaseScanner interface.
        For signal scanning, use the scan() method instead.

        Args:
            file_path: Path to file to scan

        Returns:
            Intermediate results (not used in signal scanner)
        """
        # Signal scanner doesn't use per-file scanning
        # All scanning is done through the main scan() method
        return None

    def _transform_results(self, old_results: dict[str, Any]) -> list[SignalInfo]:
        """Transform old checker results to new SignalInfo models.

        Args:
            old_results: Results from SignalChecker.get_results()

        Returns:
            List of SignalInfo objects
        """
        signals: list[SignalInfo] = []

        # Process Django signals
        if "django" in old_results:
            signals.extend(self._process_framework_signals(old_results["django"], framework="django"))

        # Process Celery signals
        if "celery" in old_results:
            signals.extend(self._process_framework_signals(old_results["celery"], framework="celery"))

        return signals

    def _process_framework_signals(self, framework_data: dict[str, Any], framework: str) -> list[SignalInfo]:
        """Process signals for a specific framework.

        Args:
            framework_data: Signal data for the framework
            framework: Framework name ('django' or 'celery')

        Returns:
            List of SignalInfo objects
        """
        signals: list[SignalInfo] = []

        for category, category_data in framework_data.items():
            # Handle unused_custom_signals (list format)
            if category == "unused_custom_signals" and isinstance(category_data, list):
                for signal_def in category_data:
                    signals.append(
                        SignalInfo(
                            signal=signal_def.get("name", "unknown"),
                            type=framework,
                            category=category,
                            status="unused",
                            receivers=[],
                            senders=[],
                        )
                    )
                continue

            # Handle regular signals (dict format)
            if not isinstance(category_data, dict):
                continue

            for signal_name, signal_data in category_data.items():
                if not isinstance(signal_data, dict):
                    continue

                # Extract receivers
                receivers = [SignalUsage(**self._normalize_usage(r)) for r in signal_data.get("receivers", [])]

                # Extract senders
                senders = [SignalUsage(**self._normalize_usage(s)) for s in signal_data.get("senders", [])]

                signals.append(
                    SignalInfo(
                        signal=signal_name,
                        type=framework,
                        category=category,
                        receivers=receivers,
                        senders=senders,
                        status="",
                    )
                )

        return signals

    def _normalize_usage(self, usage_dict: dict[str, Any]) -> dict[str, Any]:
        """Normalize usage dict to match SignalUsage model.

        Args:
            usage_dict: Raw usage dictionary from old checker

        Returns:
            Normalized dictionary ready for SignalUsage(**dict)
        """
        return {
            "file": usage_dict.get("file", ""),
            "line": usage_dict.get("line", 1),
            "column": usage_dict.get("column", 0),
            "handler": usage_dict.get("handler"),
            "pattern": usage_dict.get("pattern"),
            "code": usage_dict.get("code"),
            "sender": usage_dict.get("sender"),
            "context": usage_dict.get("context"),
        }

    def _calculate_summary(
        self,
        signals: list[SignalInfo],
        files_scanned: int,
        scan_duration_ms: int,
        old_summary: dict[str, Any],
    ) -> SignalSummary:
        """Calculate summary statistics.

        Args:
            signals: List of detected signals
            files_scanned: Number of files scanned
            scan_duration_ms: Scan duration in milliseconds
            old_summary: Summary from old checker (for validation)

        Returns:
            SignalSummary with statistics
        """
        # Count signals by type
        django_receivers = 0
        django_senders = 0
        celery_receivers = 0
        celery_senders = 0
        custom_signals_defined = 0
        unused_custom_signals = 0

        for signal in signals:
            if signal.type == "django":
                django_receivers += len(signal.receivers)
                django_senders += len(signal.senders)
                if signal.category == "custom_signals":
                    custom_signals_defined += 1
                if signal.status == "unused":
                    unused_custom_signals += 1
            elif signal.type == "celery":
                celery_receivers += len(signal.receivers)
                celery_senders += len(signal.senders)

        # Total count is number of unique signals
        total_count = len(signals)

        return SignalSummary(
            total_count=total_count,
            files_scanned=files_scanned,
            scan_duration_ms=scan_duration_ms,
            django_receivers=django_receivers,
            django_senders=django_senders,
            celery_receivers=celery_receivers,
            celery_senders=celery_senders,
            custom_signals_defined=custom_signals_defined,
            unused_custom_signals=unused_custom_signals,
        )


# ============================================================================
# CLI Interface
# ============================================================================


def main() -> None:
    """CLI entry point for signal scanner.

    This is the main command-line interface for scanning signal patterns.
    It uses the common CLI utilities for consistent behavior across all scanners.
    """
    import sys

    import click

    from upcast.common.cli import add_scanner_arguments, run_scanner_cli

    @click.command("scan-signals")
    @click.argument("path", type=click.Path(exists=True), required=False, default=".")
    @add_scanner_arguments
    def scan_signals_command(
        path: str,
        output: str | None,
        format: str,  # noqa: A002
        include: tuple[str, ...],
        exclude: tuple[str, ...],
        no_default_excludes: bool,
        verbose: bool,
    ) -> None:
        """Scan for Django and Celery signal usage.

        Detects signal handlers, custom signal definitions, and signal sends
        in Python codebases using Django and Celery.

        PATH: Directory or file to scan (defaults to current directory)

        \b
        Examples:
            upcast scan-signals .
            upcast scan-signals /app --include "**/signals/**"
            upcast scan-signals . -o signals.yaml --verbose
            upcast scan-signals /project --exclude "**/tests/**"
        """
        # Create scanner
        scanner = SignalScanner(
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )

        # Run scanner with common CLI logic
        try:
            run_scanner_cli(
                scanner=scanner,
                path=path,
                output=output,
                format=format,
                include=include,
                exclude=exclude,
                no_default_excludes=no_default_excludes,
                verbose=verbose,
            )
        except Exception as e:
            click.echo(f"Error during scan: {e}", err=True)
            if verbose:
                import traceback

                click.echo("\nFull traceback:", err=True)
                click.echo(traceback.format_exc(), err=True)
            sys.exit(1)

    scan_signals_command()


if __name__ == "__main__":
    main()
