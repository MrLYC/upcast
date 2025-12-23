"""Generate project analysis reports from scan results."""

from pathlib import Path
from typing import Any

import yaml


class ReportGenerator:
    """Generate markdown reports from scan results."""

    def __init__(self, scan_results_dir: str):
        """Initialize the report generator.

        Args:
            scan_results_dir: Directory containing YAML scan results
        """
        self.scan_results_dir = Path(scan_results_dir)
        self.results: dict[str, Any] = {}

    def load_results(self) -> None:
        """Load all YAML files from the scan results directory."""
        if not self.scan_results_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.scan_results_dir}")

        for yaml_file in self.scan_results_dir.glob("*.yaml"):
            if yaml_file.name == "README.md":
                continue
            with open(yaml_file, encoding="utf-8") as f:
                self.results[yaml_file.stem] = yaml.safe_load(f)

    def generate_report(self) -> str:
        """Generate a comprehensive markdown report.

        Returns:
            Markdown-formatted report string
        """
        sections = [
            self._generate_header(),
            self._generate_executive_summary(),
            self._generate_code_quality_section(),
            self._generate_architecture_section(),
            self._generate_infrastructure_section(),
            self._generate_testing_section(),
            self._generate_dependencies_section(),
        ]

        return "\n\n".join(filter(None, sections))

    def _generate_header(self) -> str:
        """Generate report header."""
        return "# Project Analysis Report\n\nGenerated from static code analysis scan results."

    def _generate_executive_summary(self) -> str:
        """Generate executive summary section."""
        lines = ["## Executive Summary"]

        # Collect overall statistics
        total_files = 0
        total_findings = 0

        for _scan_type, data in self.results.items():
            if isinstance(data, dict) and "summary" in data:
                summary = data["summary"]
                if "files_scanned" in summary:
                    total_files += summary["files_scanned"]
                if "total_count" in summary:
                    total_findings += summary["total_count"]

        lines.append(f"\n- **Total Files Scanned**: {total_files}")
        lines.append(f"- **Total Findings**: {total_findings}")
        lines.append(f"- **Scan Types**: {len(self.results)}")

        return "\n".join(lines)

    def _generate_code_quality_section(self) -> str:
        """Generate code quality analysis section."""
        lines = ["## Code Quality Analysis"]

        # Complexity patterns
        if "complexity-patterns" in self.results:
            complexity = self.results["complexity-patterns"]
            if "summary" in complexity:
                summary = complexity["summary"]
                lines.append("\n### Cyclomatic Complexity")
                lines.append(f"\n- **High Complexity Functions**: {summary.get('high_complexity_count', 0)}")
                lines.append(f"- **Files Analyzed**: {summary.get('files_scanned', 0)}")

                if "by_severity" in summary:
                    lines.append("- **By Severity**:")
                    for severity, count in summary["by_severity"].items():
                        lines.append(f"  - {severity.replace('_', ' ').title()}: {count}")

                # Show top 5 most complex functions
                if complexity.get("results"):
                    lines.append("\n#### Top 5 Most Complex Functions")
                    results_list = []
                    for file_path, functions in complexity["results"].items():
                        if isinstance(functions, list):
                            for func in functions:
                                results_list.append((func.get("complexity", 0), file_path, func))

                    results_list.sort(reverse=True, key=lambda x: x[0])
                    for complexity_val, file_path, func in results_list[:5]:
                        severity = func.get("severity", "unknown")
                        lines.append(
                            f"\n- **{func.get('name', 'unknown')}** "
                            f"(Complexity: {complexity_val}, Severity: {severity})"
                        )
                        lines.append(f"  - File: `{file_path}:{func.get('line', '?')}`")
                        if func.get("description"):
                            lines.append(f"  - Description: {func['description']}")

        # Blocking operations
        if "blocking-operations" in self.results:
            blocking = self.results["blocking-operations"]
            if "summary" in blocking:
                summary = blocking["summary"]
                lines.append("\n### Blocking Operations")
                lines.append(f"\n- **Total Operations**: {summary.get('total_count', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                if "by_category" in summary:
                    lines.append("- **By Category**:")
                    for category, count in summary["by_category"].items():
                        lines.append(f"  - {category.replace('_', ' ').title()}: {count}")

                # Add recommendations
                lines.append("\n**Recommendations:**")
                lines.append("- Consider using async alternatives for blocking I/O operations")
                lines.append("- Review time.sleep() calls in async contexts")
                lines.append("- Optimize database queries with select_for_update()")

        return "\n".join(lines)

    def _generate_architecture_section(self) -> str:
        """Generate architecture analysis section."""
        lines = ["## Architecture & Patterns"]

        # Django models
        if "django-models" in self.results:
            models = self.results["django-models"]
            if "summary" in models:
                summary = models["summary"]
                lines.append("\n### Django Models")
                lines.append(f"\n- **Total Models**: {summary.get('total_models', 0)}")
                lines.append(f"- **Total Fields**: {summary.get('total_fields', 0)}")
                lines.append(f"- **Total Relationships**: {summary.get('total_relationships', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                # Calculate average fields per model
                if summary.get("total_models", 0) > 0:
                    avg_fields = summary.get("total_fields", 0) / summary.get("total_models", 1)
                    lines.append(f"- **Average Fields per Model**: {avg_fields:.1f}")

        # Django URLs
        if "django-urls" in self.results:
            urls = self.results["django-urls"]
            if "summary" in urls:
                summary = urls["summary"]
                lines.append("\n### Django URL Patterns")
                lines.append(f"\n- **Total URL Patterns**: {summary.get('total_patterns', 0)}")
                lines.append(f"- **URL Configuration Files**: {summary.get('files_scanned', 0)}")

                # Count different pattern types
                if "results" in urls:
                    path_count = 0
                    include_count = 0
                    for file_patterns in urls["results"].values():
                        if isinstance(file_patterns, dict) and "urlpatterns" in file_patterns:
                            for pattern in file_patterns["urlpatterns"]:
                                if pattern.get("type") == "path":
                                    path_count += 1
                                elif pattern.get("type") == "include":
                                    include_count += 1
                    lines.append(f"- **Path Patterns**: {path_count}")
                    lines.append(f"- **Include Patterns**: {include_count}")

        # Concurrency patterns
        if "concurrency-patterns" in self.results:
            concurrency = self.results["concurrency-patterns"]
            if "summary" in concurrency:
                summary = concurrency["summary"]
                lines.append("\n### Concurrency Patterns")
                lines.append(f"\n- **Total Patterns**: {summary.get('total_count', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                if "by_category" in summary:
                    lines.append("- **By Category**:")
                    for category, count in summary["by_category"].items():
                        lines.append(f"  - {category.title()}: {count}")

                lines.append("\n**Note:** Consider using asyncio for I/O-bound operations to improve performance.")

        # Signals
        if "signals" in self.results:
            signals = self.results["signals"]
            if "summary" in signals:
                summary = signals["summary"]
                lines.append("\n### Signal Usage")
                lines.append(f"\n- **Total Signals**: {summary.get('total_count', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")
                if "django_receivers" in summary:
                    lines.append(f"- **Django Receivers**: {summary.get('django_receivers', 0)}")
                if "celery_receivers" in summary:
                    lines.append(f"- **Celery Receivers**: {summary.get('celery_receivers', 0)}")
                if "custom_signals_defined" in summary:
                    lines.append(f"- **Custom Signals Defined**: {summary.get('custom_signals_defined', 0)}")
                if "unused_custom_signals" in summary:
                    unused = summary.get("unused_custom_signals", 0)
                    if unused > 0:
                        lines.append(f"- ⚠️ **Unused Custom Signals**: {unused}")

        return "\n".join(lines)

    def _generate_infrastructure_section(self) -> str:
        """Generate infrastructure analysis section."""
        lines = ["## Infrastructure"]

        # Environment variables
        if "env-vars" in self.results:
            env_vars = self.results["env-vars"]
            if "summary" in env_vars:
                summary = env_vars["summary"]
                lines.append("\n### Environment Variables")
                lines.append(f"\n- **Total Variables**: {summary.get('total_env_vars', 0)}")
                lines.append(f"- **Required Variables**: {summary.get('required_count', 0)}")
                lines.append(f"- **Optional Variables**: {summary.get('optional_count', 0)}")

                # List required variables
                if "results" in env_vars:
                    required_vars = [
                        name for name, info in env_vars["results"].items() if isinstance(info, dict) and info.get("required", False)
                    ]
                    if required_vars:
                        lines.append("\n**Critical Required Variables:**")
                        for var in sorted(required_vars)[:10]:  # Show top 10
                            lines.append(f"- `{var}`")
                        if len(required_vars) > 10:
                            lines.append(f"- ... and {len(required_vars) - 10} more")

        # Redis usage
        if "redis-usage" in self.results:
            redis = self.results["redis-usage"]
            if "summary" in redis:
                summary = redis["summary"]
                lines.append("\n### Redis Usage")
                lines.append(f"\n- **Total Usages**: {summary.get('total_usages', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                if "categories" in summary:
                    lines.append("- **By Category**:")
                    for category, count in summary["categories"].items():
                        lines.append(f"  - {category.replace('_', ' ').title()}: {count}")

                # Check for warnings
                if summary.get("warnings"):
                    lines.append(f"\n⚠️ **Warnings**: {len(summary['warnings'])} issues detected")

        # Metrics
        if "metrics" in self.results:
            metrics = self.results["metrics"]
            if "summary" in metrics:
                summary = metrics["summary"]
                lines.append("\n### Prometheus Metrics")
                lines.append(f"\n- **Total Metrics**: {summary.get('total_metrics', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                if "by_type" in summary:
                    lines.append("- **By Type**:")
                    for metric_type, count in summary["by_type"].items():
                        lines.append(f"  - {metric_type.title()}: {count}")

        # Django settings
        if "django-settings" in self.results:
            settings = self.results["django-settings"]
            if "summary" in settings:
                summary = settings["summary"]
                lines.append("\n### Django Settings")
                lines.append(f"\n- **Total Settings References**: {summary.get('total_count', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

        return "\n".join(lines)

    def _generate_testing_section(self) -> str:
        """Generate testing analysis section."""
        lines = ["## Testing & Reliability"]

        # Unit tests
        if "unit-tests" in self.results:
            tests = self.results["unit-tests"]
            if "summary" in tests:
                summary = tests["summary"]
                lines.append("\n### Unit Tests")
                lines.append(f"\n- **Total Test Files**: {summary.get('total_test_files', 0)}")
                lines.append(f"- **Total Tests**: {summary.get('total_tests', 0)}")

                if "by_framework" in summary:
                    lines.append("- **By Framework**:")
                    for framework, count in summary["by_framework"].items():
                        lines.append(f"  - {framework.title()}: {count}")

        # Exception handlers
        if "exception-handlers" in self.results:
            exceptions = self.results["exception-handlers"]
            if "summary" in exceptions:
                summary = exceptions["summary"]
                lines.append("\n### Exception Handlers")
                lines.append(f"\n- **Total Handlers**: {summary.get('total_count', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

        return "\n".join(lines)

    def _generate_dependencies_section(self) -> str:
        """Generate external dependencies section."""
        lines = ["## External Dependencies"]

        # HTTP requests
        if "http-requests" in self.results:
            http = self.results["http-requests"]
            if "summary" in http:
                summary = http["summary"]
                lines.append("\n### HTTP Requests")
                lines.append(f"\n- **Total Requests**: {summary.get('total_count', 0)}")
                lines.append(f"- **Unique URLs**: {summary.get('unique_urls', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                if "by_library" in summary:
                    lines.append("- **By Library**:")
                    for library, count in summary["by_library"].items():
                        lines.append(f"  - {library}: {count}")

                # Show top external APIs if available
                if "results" in http:
                    external_urls = []
                    for url, info in http["results"].items():
                        if isinstance(info, dict) and url.startswith(("http://", "https://")):
                            count = len(info.get("usages", []))
                            external_urls.append((count, url))

                    if external_urls:
                        external_urls.sort(reverse=True)
                        lines.append("\n**Top External APIs:**")
                        for count, url in external_urls[:5]:
                            # Truncate long URLs
                            display_url = url if len(url) <= 60 else url[:57] + "..."
                            lines.append(f"- `{display_url}` ({count} calls)")

        return "\n".join(lines)
