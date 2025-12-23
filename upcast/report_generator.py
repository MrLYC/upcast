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
            self._generate_summary_and_recommendations(),
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
                    lines.append("\n**Distribution by Severity:**")
                    lines.append("\n| Severity | Count | Description |")
                    lines.append("|----------|-------|-------------|")
                    severity_desc = {
                        "acceptable": "6-10: Reasonable complexity",
                        "warning": "11-15: Refactoring recommended",
                        "high_risk": "16-20: Significant maintenance cost",
                        "critical": ">20: Design issues likely",
                    }
                    for severity, count in sorted(summary["by_severity"].items(), key=lambda x: x[1], reverse=True):
                        desc = severity_desc.get(severity, "Unknown")
                        lines.append(f"| {severity.replace('_', ' ').title()} | {count} | {desc} |")

                # Show top 10 most complex functions with more details
                if complexity.get("results"):
                    lines.append("\n#### Top 10 Most Complex Functions")
                    results_list = []
                    for file_path, functions in complexity["results"].items():
                        if isinstance(functions, list):
                            for func in functions:
                                results_list.append((func.get("complexity", 0), file_path, func))

                    results_list.sort(reverse=True, key=lambda x: x[0])
                    
                    lines.append("\n| # | Function | Complexity | Severity | File | Lines |")
                    lines.append("|---|----------|------------|----------|------|-------|")
                    
                    for idx, (complexity_val, file_path, func) in enumerate(results_list[:10], 1):
                        severity = func.get("severity", "unknown")
                        name = func.get("name", "unknown")
                        line_start = func.get("line", "?")
                        line_end = func.get("end_line", "?")
                        code_lines = func.get("code_lines", "?")
                        
                        # Truncate long file paths
                        short_path = file_path if len(file_path) <= 50 else "..." + file_path[-47:]
                        
                        lines.append(
                            f"| {idx} | `{name}` | {complexity_val} | {severity} | "
                            f"`{short_path}:{line_start}` | {code_lines} |"
                        )

        # Blocking operations
        if "blocking-operations" in self.results:
            blocking = self.results["blocking-operations"]
            if "summary" in blocking:
                summary = blocking["summary"]
                lines.append("\n### Blocking Operations")
                lines.append(f"\n- **Total Operations**: {summary.get('total_count', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                if "by_category" in summary:
                    lines.append("\n**By Category:**")
                    lines.append("\n| Category | Count | Impact |")
                    lines.append("|----------|-------|--------|")
                    category_impact = {
                        "time_based": "May cause delays in async contexts",
                        "database": "Can cause deadlocks with improper locking",
                        "synchronization": "May block threads unnecessarily",
                        "subprocess": "Blocks until process completes",
                    }
                    for category, count in sorted(summary["by_category"].items(), key=lambda x: x[1], reverse=True):
                        impact = category_impact.get(category, "May impact performance")
                        lines.append(f"| {category.replace('_', ' ').title()} | {count} | {impact} |")

                # Show examples of blocking operations
                if "results" in blocking:
                    lines.append("\n#### Examples of Blocking Operations")
                    
                    # Group by category and show examples
                    for category in ["time_based", "database", "synchronization", "subprocess"]:
                        if category in blocking["results"] and blocking["results"][category]:
                            operations = blocking["results"][category]
                            if operations:
                                lines.append(f"\n**{category.replace('_', ' ').title()} Operations:**")
                                
                                for op in operations[:3]:  # Show top 3 per category
                                    file_path = op.get("file", "unknown")
                                    line_no = op.get("line", "?")
                                    func = op.get("function", "unknown")
                                    class_name = op.get("class_name")
                                    operation = op.get("operation", "unknown")
                                    statement = op.get("statement", "")
                                    
                                    location = f"`{file_path}:{line_no}`"
                                    if class_name:
                                        context = f"`{class_name}.{func}()`"
                                    else:
                                        context = f"`{func}()`"
                                    
                                    lines.append(f"\n- {location} in {context}")
                                    lines.append(f"  - Operation: `{operation}`")
                                    if statement and len(statement) < 100:
                                        lines.append(f"  - Statement: `{statement}`")

                # Add recommendations
                lines.append("\n**Recommendations:**")
                lines.append("- Consider using async alternatives for blocking I/O operations")
                lines.append("- Review time.sleep() calls in async contexts")
                lines.append("- Optimize database queries with select_for_update()")
                lines.append("- Use asyncio.sleep() instead of time.sleep() in async functions")

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

                # Analyze model details
                if "results" in models:
                    # Find models with most fields
                    model_field_counts = []
                    model_relationship_counts = []
                    
                    for model_name, model_data in models["results"].items():
                        if isinstance(model_data, dict):
                            field_count = len(model_data.get("fields", {}))
                            rel_count = len(model_data.get("relationships", []))
                            model_field_counts.append((field_count, model_name, model_data))
                            if rel_count > 0:
                                model_relationship_counts.append((rel_count, model_name, model_data))

                    if model_field_counts:
                        model_field_counts.sort(reverse=True)
                        lines.append("\n**Models with Most Fields:**")
                        lines.append("\n| Model | Fields | Module |")
                        lines.append("|-------|--------|--------|")
                        for count, model_name, model_data in model_field_counts[:10]:
                            module = model_data.get("module", "unknown")
                            # Truncate long names
                            short_name = model_name.split(".")[-1] if "." in model_name else model_name
                            short_module = module if len(module) <= 40 else "..." + module[-37:]
                            lines.append(f"| `{short_name}` | {count} | `{short_module}` |")

                    if model_relationship_counts:
                        model_relationship_counts.sort(reverse=True)
                        lines.append("\n**Models with Most Relationships:**")
                        lines.append("\n| Model | Relationships | Types |")
                        lines.append("|-------|---------------|-------|")
                        for count, model_name, model_data in model_relationship_counts[:10]:
                            short_name = model_name.split(".")[-1] if "." in model_name else model_name
                            rel_types = set()
                            for rel in model_data.get("relationships", []):
                                if isinstance(rel, dict):
                                    rel_types.add(rel.get("type", "").replace("models.", ""))
                            types_str = ", ".join(sorted(rel_types))
                            lines.append(f"| `{short_name}` | {count} | {types_str} |")

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
                    patterns_by_file = {}
                    
                    for file_path, file_patterns in urls["results"].items():
                        if isinstance(file_patterns, dict) and "urlpatterns" in file_patterns:
                            pattern_count = len(file_patterns["urlpatterns"])
                            patterns_by_file[file_path] = pattern_count
                            
                            for pattern in file_patterns["urlpatterns"]:
                                if pattern.get("type") == "path":
                                    path_count += 1
                                elif pattern.get("type") == "include":
                                    include_count += 1
                    
                    lines.append(f"\n- **Path Patterns**: {path_count}")
                    lines.append(f"- **Include Patterns**: {include_count}")

                    # Show files with most URL patterns
                    if patterns_by_file:
                        sorted_files = sorted(patterns_by_file.items(), key=lambda x: x[1], reverse=True)
                        lines.append("\n**Files with Most URL Patterns:**")
                        lines.append("\n| File | Pattern Count |")
                        lines.append("|------|---------------|")
                        for file_path, count in sorted_files[:10]:
                            short_path = file_path if len(file_path) <= 60 else "..." + file_path[-57:]
                            lines.append(f"| `{short_path}` | {count} |")

        # Concurrency patterns
        if "concurrency-patterns" in self.results:
            concurrency = self.results["concurrency-patterns"]
            if "summary" in concurrency:
                summary = concurrency["summary"]
                lines.append("\n### Concurrency Patterns")
                lines.append(f"\n- **Total Patterns**: {summary.get('total_count', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                if "by_category" in summary:
                    lines.append("\n**By Category:**")
                    lines.append("\n| Category | Count | Use Case |")
                    lines.append("|----------|-------|----------|")
                    use_cases = {
                        "threading": "I/O-bound operations, concurrent tasks",
                        "multiprocessing": "CPU-bound operations, parallel processing",
                        "asyncio": "Async I/O operations, high concurrency",
                    }
                    for category, count in summary["by_category"].items():
                        use_case = use_cases.get(category, "Various use cases")
                        lines.append(f"| {category.title()} | {count} | {use_case} |")

                lines.append("\n**Performance Tips:**")
                lines.append("- Use asyncio for I/O-bound operations (network, file I/O)")
                lines.append("- Use multiprocessing for CPU-bound operations")
                lines.append("- Threading is suitable for I/O-bound with GIL limitations")

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

                # Show signal details
                if "results" in signals:
                    signal_receiver_counts = {}
                    for signal_info in signals["results"]:
                        if isinstance(signal_info, dict):
                            signal_name = signal_info.get("signal", "unknown")
                            receiver_count = len(signal_info.get("receivers", []))
                            signal_receiver_counts[signal_name] = signal_receiver_counts.get(signal_name, 0) + receiver_count

                    if signal_receiver_counts:
                        sorted_signals = sorted(signal_receiver_counts.items(), key=lambda x: x[1], reverse=True)
                        lines.append("\n**Most Used Signals:**")
                        lines.append("\n| Signal | Receiver Count |")
                        lines.append("|--------|----------------|")
                        for signal_name, count in sorted_signals[:10]:
                            lines.append(f"| `{signal_name}` | {count} |")

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

                # List required and optional variables in a table
                if "results" in env_vars:
                    required_vars = []
                    optional_vars = []
                    
                    for name, info in env_vars["results"].items():
                        if isinstance(info, dict):
                            var_data = {
                                "name": name,
                                "required": info.get("required", False),
                                "default": info.get("default_value"),
                                "locations": len(info.get("locations", []))
                            }
                            if var_data["required"]:
                                required_vars.append(var_data)
                            else:
                                optional_vars.append(var_data)

                    if required_vars:
                        lines.append("\n**Required Environment Variables:**")
                        lines.append("\n| Variable | Usage Count | Notes |")
                        lines.append("|----------|-------------|-------|")
                        for var in sorted(required_vars, key=lambda x: x["name"]):
                            lines.append(f"| `{var['name']}` | {var['locations']} | Must be set |")

                    if optional_vars:
                        lines.append("\n**Optional Environment Variables (with defaults):**")
                        lines.append("\n| Variable | Default | Usage Count |")
                        lines.append("|----------|---------|-------------|")
                        for var in sorted(optional_vars, key=lambda x: x["locations"], reverse=True)[:10]:
                            default = var.get("default")
                            default_str = str(default) if default and len(str(default)) <= 30 else "(dynamic)"
                            lines.append(f"| `{var['name']}` | `{default_str}` | {var['locations']} |")

        # Redis usage
        if "redis-usage" in self.results:
            redis = self.results["redis-usage"]
            if "summary" in redis:
                summary = redis["summary"]
                lines.append("\n### Redis Usage")
                lines.append(f"\n- **Total Usages**: {summary.get('total_usages', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                if "categories" in summary:
                    lines.append("\n**By Category:**")
                    lines.append("\n| Category | Count | Purpose |")
                    lines.append("|----------|-------|---------|")
                    category_purposes = {
                        "cache_backend": "Django cache framework",
                        "celery_broker": "Task queue message broker",
                        "celery_result": "Task result storage",
                        "direct_client": "Direct Redis operations",
                        "session_storage": "User session storage",
                        "distributed_lock": "Distributed locking",
                        "rate_limiting": "API rate limiting",
                        "channels": "Django Channels layer",
                    }
                    for category, count in sorted(summary["categories"].items(), key=lambda x: x[1], reverse=True):
                        purpose = category_purposes.get(category, "Various uses")
                        cat_display = category.replace("_", " ").title()
                        lines.append(f"| {cat_display} | {count} | {purpose} |")

                # Show Redis usage examples
                if "results" in redis:
                    lines.append("\n**Redis Operations:**")
                    for category in ["direct_client", "distributed_lock"]:
                        if category in redis["results"] and redis["results"][category]:
                            operations = redis["results"][category][:3]  # Show top 3
                            for op in operations:
                                op_type = op.get("operation", "unknown")
                                file_path = op.get("file", "unknown")
                                line_no = op.get("line", "?")
                                key = op.get("key", "?")
                                has_ttl = op.get("has_ttl")
                                
                                lines.append(f"\n- `{file_path}:{line_no}`")
                                lines.append(f"  - Operation: `{op_type}`")
                                lines.append(f"  - Key pattern: `{key}`")
                                if has_ttl is not None:
                                    ttl_status = "✓ Has TTL" if has_ttl else "⚠️ No TTL"
                                    lines.append(f"  - {ttl_status}")

                # Check for warnings
                if summary.get("warnings"):
                    lines.append(f"\n⚠️ **Warnings**: {len(summary['warnings'])} issues detected")
                    lines.append("- Review Redis operations without TTL")
                    lines.append("- Consider connection pooling for performance")

        # Metrics
        if "metrics" in self.results:
            metrics = self.results["metrics"]
            if "summary" in metrics:
                summary = metrics["summary"]
                lines.append("\n### Prometheus Metrics")
                lines.append(f"\n- **Total Metrics**: {summary.get('total_metrics', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                if "by_type" in summary:
                    lines.append("\n**Metrics by Type:**")
                    lines.append("\n| Type | Count | Use Case |")
                    lines.append("|------|-------|----------|")
                    metric_uses = {
                        "Counter": "Monotonically increasing values (requests, errors)",
                        "Gauge": "Values that can go up and down (memory, connections)",
                        "Histogram": "Observations and distributions (latency, sizes)",
                        "Summary": "Similar to Histogram with percentiles",
                    }
                    for metric_type, count in sorted(summary["by_type"].items(), key=lambda x: x[1], reverse=True):
                        use_case = metric_uses.get(metric_type.title(), "Various metrics")
                        lines.append(f"| {metric_type.title()} | {count} | {use_case} |")

                # Show metric examples
                if "results" in metrics:
                    lines.append("\n**Sample Metrics:**")
                    metric_count = 0
                    for metric_name, metric_info in list(metrics["results"].items())[:5]:
                        if isinstance(metric_info, dict):
                            metric_type = metric_info.get("type", "unknown")
                            help_text = metric_info.get("help", "No description")
                            labels = metric_info.get("labels", [])
                            
                            lines.append(f"\n- **`{metric_name}`** ({metric_type})")
                            lines.append(f"  - {help_text}")
                            if labels:
                                lines.append(f"  - Labels: {', '.join([f'`{l}`' for l in labels])}")
                            metric_count += 1
                            if metric_count >= 5:
                                break

        # Django settings
        if "django-settings" in self.results:
            settings = self.results["django-settings"]
            if "summary" in settings:
                summary = settings["summary"]
                lines.append("\n### Django Settings")
                lines.append(f"\n- **Total Settings References**: {summary.get('total_count', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                # Show most referenced settings
                if "results" in settings:
                    setting_counts = []
                    for setting_name, setting_info in settings["results"].items():
                        if isinstance(setting_info, dict):
                            count = setting_info.get("count", 0)
                            setting_counts.append((count, setting_name))

                    if setting_counts:
                        setting_counts.sort(reverse=True)
                        lines.append("\n**Most Referenced Settings:**")
                        lines.append("\n| Setting | Reference Count |")
                        lines.append("|---------|-----------------|")
                        for count, setting_name in setting_counts[:15]:
                            lines.append(f"| `{setting_name}` | {count} |")

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
                    lines.append("\n**By Framework:**")
                    lines.append("\n| Framework | Test Count | Percentage |")
                    lines.append("|-----------|------------|------------|")
                    total_tests = summary.get("total_tests", 0)
                    for framework, count in sorted(summary["by_framework"].items(), key=lambda x: x[1], reverse=True):
                        percentage = (count / total_tests * 100) if total_tests > 0 else 0
                        lines.append(f"| {framework.title()} | {count} | {percentage:.1f}% |")

        # Exception handlers
        if "exception-handlers" in self.results:
            exceptions = self.results["exception-handlers"]
            if "summary" in exceptions:
                summary = exceptions["summary"]
                lines.append("\n### Exception Handlers")
                lines.append(f"\n- **Total Handlers**: {summary.get('total_count', 0)}")
                lines.append(f"- **Files Scanned**: {summary.get('files_scanned', 0)}")

                # Analyze exception handler patterns
                if "results" in exceptions:
                    bare_except_count = 0
                    handlers_with_logging = 0
                    handlers_with_reraise = 0
                    exception_type_counts = {}

                    for handler in exceptions["results"]:
                        if isinstance(handler, dict):
                            # Check for bare except
                            if "except_clauses" in handler:
                                for clause in handler["except_clauses"]:
                                    if isinstance(clause, dict):
                                        exception_types = clause.get("exception_types", [])
                                        if not exception_types or exception_types == ["bare"]:
                                            bare_except_count += 1
                                        else:
                                            for exc_type in exception_types:
                                                exception_type_counts[exc_type] = exception_type_counts.get(exc_type, 0) + 1

                                        # Check for logging
                                        has_logging = (
                                            clause.get("log_error_count", 0) > 0
                                            or clause.get("log_exception_count", 0) > 0
                                            or clause.get("log_warning_count", 0) > 0
                                        )
                                        if has_logging:
                                            handlers_with_logging += 1

                                        # Check for reraise
                                        if clause.get("raise_count", 0) > 0:
                                            handlers_with_reraise += 1

                    lines.append(f"\n**Handler Analysis:**")
                    lines.append(f"- Handlers with logging: {handlers_with_logging}")
                    lines.append(f"- Handlers that reraise: {handlers_with_reraise}")
                    if bare_except_count > 0:
                        lines.append(f"- ⚠️ Bare except clauses: {bare_except_count} (anti-pattern)")

                    # Show top exception types
                    if exception_type_counts:
                        lines.append("\n**Top Exception Types Caught:**")
                        lines.append("\n| Exception Type | Count |")
                        lines.append("|----------------|-------|")
                        for exc_type, count in sorted(exception_type_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                            lines.append(f"| `{exc_type}` | {count} |")

                    lines.append("\n**Best Practices:**")
                    lines.append("- ✓ Log exceptions before handling")
                    lines.append("- ✓ Catch specific exception types")
                    lines.append("- ✗ Avoid bare except clauses")
                    lines.append("- ✓ Re-raise exceptions when appropriate")

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
                    lines.append("\n**By Library:**")
                    lines.append("\n| Library | Count | Notes |")
                    lines.append("|---------|-------|-------|")
                    for library, count in sorted(summary["by_library"].items(), key=lambda x: x[1], reverse=True):
                        notes = "Synchronous" if library == "requests" else "May support async"
                        lines.append(f"| `{library}` | {count} | {notes} |")

                # Show top external APIs if available
                if "results" in http:
                    external_urls = []
                    internal_patterns = []
                    
                    for url, info in http["results"].items():
                        if isinstance(info, dict):
                            count = len(info.get("usages", []))
                            if url.startswith(("http://", "https://")):
                                external_urls.append((count, url, info))
                            elif url != "...":
                                internal_patterns.append((count, url))

                    if external_urls:
                        external_urls.sort(reverse=True)
                        lines.append("\n**Top External APIs:**")
                        lines.append("\n| URL | Calls | Method | Library |")
                        lines.append("|-----|-------|--------|---------|")
                        for count, url, info in external_urls[:10]:
                            # Truncate long URLs
                            display_url = url if len(url) <= 50 else url[:47] + "..."
                            method = info.get("method", "?")
                            library = info.get("library", "?")
                            lines.append(f"| `{display_url}` | {count} | {method} | {library} |")

                    if internal_patterns:
                        internal_patterns.sort(reverse=True)
                        lines.append("\n**Internal/Dynamic URL Patterns:**")
                        for count, pattern in internal_patterns[:5]:
                            lines.append(f"- Pattern `{pattern}`: {count} usages")

                lines.append("\n**Recommendations:**")
                lines.append("- Consider using connection pooling for frequently called APIs")
                lines.append("- Implement retry logic with exponential backoff")
                lines.append("- Add timeout configuration for all HTTP requests")
                lines.append("- Monitor external API response times and failures")

        return "\n".join(lines)

    def _generate_summary_and_recommendations(self) -> str:
        """Generate overall summary and recommendations."""
        lines = ["## Summary & Key Recommendations"]

        # Collect key metrics
        total_complexity_issues = 0
        total_blocking_ops = 0
        total_exception_handlers = 0
        bare_except_count = 0

        if "complexity-patterns" in self.results:
            summary = self.results["complexity-patterns"].get("summary", {})
            total_complexity_issues = summary.get("high_complexity_count", 0)

        if "blocking-operations" in self.results:
            summary = self.results["blocking-operations"].get("summary", {})
            total_blocking_ops = summary.get("total_count", 0)

        if "exception-handlers" in self.results:
            summary = self.results["exception-handlers"].get("summary", {})
            total_exception_handlers = summary.get("total_count", 0)

        lines.append("\n### Key Findings")
        lines.append(f"\n- **High Priority**: {total_complexity_issues} high-complexity functions need review")
        lines.append(f"- **Performance**: {total_blocking_ops} blocking operations detected")
        lines.append(f"- **Reliability**: {total_exception_handlers} exception handlers analyzed")

        lines.append("\n### Priority Recommendations")
        lines.append("\n#### 🔴 High Priority")
        if total_complexity_issues > 0:
            lines.append("- **Refactor complex functions**: Focus on functions with complexity > 15")
            lines.append("  - Break down large functions into smaller, testable units")
            lines.append("  - Consider using design patterns (Strategy, Command, etc.)")

        lines.append("\n#### 🟡 Medium Priority")
        if total_blocking_ops > 0:
            lines.append("- **Optimize blocking operations**:")
            lines.append("  - Replace `time.sleep()` with `asyncio.sleep()` in async code")
            lines.append("  - Review database operations with `select_for_update()`")
            lines.append("  - Consider async alternatives for I/O operations")

        lines.append("\n#### 🟢 Low Priority / Best Practices")
        lines.append("- **Code quality improvements**:")
        lines.append("  - Add logging to exception handlers")
        lines.append("  - Avoid bare except clauses")
        lines.append("  - Document complex business logic")
        lines.append("- **Monitoring & Observability**:")
        lines.append("  - Add metrics for critical operations")
        lines.append("  - Implement distributed tracing for external API calls")
        lines.append("  - Monitor Redis usage and set appropriate TTLs")

        lines.append("\n### Next Steps")
        lines.append("\n1. **Review Critical Issues**: Address high-complexity functions and blocking operations")
        lines.append("2. **Improve Test Coverage**: Focus on untested complex functions")
        lines.append("3. **Performance Optimization**: Profile and optimize hot paths")
        lines.append("4. **Documentation**: Document architecture decisions and complex logic")
        lines.append("5. **Continuous Monitoring**: Set up alerts for performance regressions")

        return "\n".join(lines)
