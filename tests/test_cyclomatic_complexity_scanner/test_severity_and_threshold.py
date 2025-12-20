"""Tests for severity assignment and threshold filtering."""

from pathlib import Path

import pytest

from upcast.cyclomatic_complexity_scanner.checker import ComplexityChecker
from upcast.cyclomatic_complexity_scanner.complexity_parser import (
    ComplexityResult,
    assign_severity,
    filter_by_threshold,
)


class TestSeverityAssignment:
    """Tests for assign_severity function."""

    def test_healthy_severity(self):
        """Test healthy severity for complexity <= 5."""
        assert assign_severity(1) == "healthy"
        assert assign_severity(3) == "healthy"
        assert assign_severity(5) == "healthy"

    def test_acceptable_severity(self):
        """Test acceptable severity for complexity 6-10."""
        assert assign_severity(6) == "acceptable"
        assert assign_severity(8) == "acceptable"
        assert assign_severity(10) == "acceptable"

    def test_warning_severity(self):
        """Test warning severity for complexity 11-15."""
        assert assign_severity(11) == "warning"
        assert assign_severity(13) == "warning"
        assert assign_severity(15) == "warning"

    def test_high_risk_severity(self):
        """Test high_risk severity for complexity 16-20."""
        assert assign_severity(16) == "high_risk"
        assert assign_severity(18) == "high_risk"
        assert assign_severity(20) == "high_risk"

    def test_critical_severity(self):
        """Test critical severity for complexity > 20."""
        assert assign_severity(21) == "critical"
        assert assign_severity(50) == "critical"
        assert assign_severity(100) == "critical"

    def test_boundary_values(self):
        """Test boundary values between severity levels."""
        # Boundaries
        assert assign_severity(5) == "healthy"
        assert assign_severity(6) == "acceptable"
        assert assign_severity(10) == "acceptable"
        assert assign_severity(11) == "warning"
        assert assign_severity(15) == "warning"
        assert assign_severity(16) == "high_risk"
        assert assign_severity(20) == "high_risk"
        assert assign_severity(21) == "critical"


class TestThresholdFiltering:
    """Tests for filter_by_threshold function."""

    @pytest.fixture
    def sample_results(self):
        """Create sample complexity results."""
        return [
            ComplexityResult(
                name="func1",
                line=1,
                end_line=3,
                complexity=5,
                severity="healthy",
                description="Function 1",
                signature="def func1():",
                is_async=False,
                is_method=False,
                class_name=None,
                code="def func1():\n    pass",
                comment_lines=0,
                code_lines=2,
            ),
            ComplexityResult(
                name="func2",
                line=5,
                end_line=10,
                complexity=11,
                severity="warning",
                description="Function 2",
                signature="def func2():",
                is_async=False,
                is_method=False,
                class_name=None,
                code="def func2():\n    pass",
                comment_lines=0,
                code_lines=6,
            ),
            ComplexityResult(
                name="func3",
                line=12,
                end_line=20,
                complexity=15,
                severity="warning",
                description="Function 3",
                signature="def func3():",
                is_async=False,
                is_method=False,
                class_name=None,
                code="def func3():\n    pass",
                comment_lines=0,
                code_lines=9,
            ),
            ComplexityResult(
                name="func4",
                line=22,
                end_line=30,
                complexity=25,
                severity="critical",
                description="Function 4",
                signature="def func4():",
                is_async=False,
                is_method=False,
                class_name=None,
                code="def func4():\n    pass",
                comment_lines=0,
                code_lines=9,
            ),
        ]

    def test_default_threshold(self, sample_results):
        """Test filtering with default threshold of 11."""
        filtered = filter_by_threshold(sample_results)

        # Should include func2 (11), func3 (15), func4 (25)
        assert len(filtered) == 3
        names = {r.name for r in filtered}
        assert names == {"func2", "func3", "func4"}

    def test_custom_threshold(self, sample_results):
        """Test filtering with custom threshold."""
        filtered = filter_by_threshold(sample_results, threshold=15)

        # Should include func3 (15) and func4 (25)
        assert len(filtered) == 2
        names = {r.name for r in filtered}
        assert names == {"func3", "func4"}

    def test_high_threshold(self, sample_results):
        """Test filtering with high threshold."""
        filtered = filter_by_threshold(sample_results, threshold=20)

        # Should only include func4 (25)
        assert len(filtered) == 1
        assert filtered[0].name == "func4"

    def test_threshold_zero(self, sample_results):
        """Test that threshold 0 returns all results."""
        filtered = filter_by_threshold(sample_results, threshold=0)

        # Should include all 4 functions
        assert len(filtered) == 4

    def test_threshold_higher_than_all(self, sample_results):
        """Test threshold higher than all complexities."""
        filtered = filter_by_threshold(sample_results, threshold=100)

        # Should return empty list
        assert len(filtered) == 0

    def test_empty_input(self):
        """Test filtering empty list."""
        filtered = filter_by_threshold([])
        assert len(filtered) == 0


class TestCheckerThreshold:
    """Tests for ComplexityChecker threshold parameter."""

    @pytest.fixture
    def simple_fixture_path(self):
        """Path to simple.py fixture."""
        return Path(__file__).parent / "fixtures" / "simple.py"

    @pytest.fixture
    def complex_fixture_path(self):
        """Path to complex.py fixture."""
        return Path(__file__).parent / "fixtures" / "complex.py"

    def test_default_threshold_11(self, complex_fixture_path):
        """Test that default threshold is 11."""
        checker = ComplexityChecker()  # Default threshold
        results = checker.check_file(complex_fixture_path)

        # Should only return functions with complexity >= 11
        for result in results:
            assert result.complexity >= 11

    def test_custom_threshold_5(self, simple_fixture_path):
        """Test custom threshold of 5."""
        checker = ComplexityChecker(threshold=5)
        results = checker.check_file(simple_fixture_path)

        # Should return functions with complexity >= 5
        for result in results:
            assert result.complexity >= 5

    def test_threshold_1_returns_all(self, simple_fixture_path):
        """Test that threshold 1 returns all functions."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(simple_fixture_path)

        # Should return all functions (all have complexity >= 1)
        assert len(results) > 0
        for result in results:
            assert result.complexity >= 1

    def test_high_threshold_returns_none(self, simple_fixture_path):
        """Test that very high threshold returns no results."""
        checker = ComplexityChecker(threshold=100)
        results = checker.check_file(simple_fixture_path)

        # Simple functions should not have complexity >= 100
        assert len(results) == 0

    def test_threshold_affects_multiple_files(self, simple_fixture_path, complex_fixture_path):
        """Test threshold applies to multiple files."""
        checker = ComplexityChecker(threshold=10)
        results = checker.check_files(
            [simple_fixture_path, complex_fixture_path],
            base_path=simple_fixture_path.parent,
        )

        # All results should meet threshold
        for module_results in results.values():
            for result in module_results:
                assert result.complexity >= 10


class TestSeverityInResults:
    """Tests that severity is correctly assigned in results."""

    @pytest.fixture
    def complex_fixture_path(self):
        """Path to complex.py fixture."""
        return Path(__file__).parent / "fixtures" / "complex.py"

    def test_severity_matches_complexity(self, complex_fixture_path):
        """Test that severity field matches complexity value."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(complex_fixture_path)

        for result in results:
            expected_severity = assign_severity(result.complexity)
            assert result.severity == expected_severity

    def test_all_severity_levels_present(self, complex_fixture_path):
        """Test that we can find different severity levels."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(complex_fixture_path)

        severities = {r.severity for r in results}
        # Complex.py should have at least some different severity levels
        assert len(severities) > 1
