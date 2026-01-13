"""Tests for complexity scanner models."""

import pytest

from upcast.models.complexity import ComplexityOutput, ComplexityResult, ComplexitySummary


class TestComplexityResult:
    """Test ComplexityResult model."""

    def test_basic_result(self):
        """Test basic complexity result creation."""
        result = ComplexityResult(
            name="my_function",
            line=10,
            end_line=20,
            complexity=15,
            severity="warning",
            message="Complexity 15 exceeds threshold 11",
            description="A complex function",
            signature="def my_function(x, y):",
            code="def my_function(x, y):\n    pass",
            comment_lines=2,
            code_lines=10,
        )

        assert result.name == "my_function"
        assert result.line == 10
        assert result.end_line == 20
        assert result.complexity == 15
        assert result.severity == "warning"

    def test_minimal_result(self):
        """Test result with minimal fields."""
        result = ComplexityResult(
            name="func",
            line=1,
            end_line=5,
            complexity=12,
            severity="warning",
            comment_lines=0,
            code_lines=5,
        )

        assert result.name == "func"
        assert result.message == ""
        assert result.description == ""
        assert result.signature == ""
        assert result.code == ""
        assert result.comment_lines == 0
        assert result.code_lines == 5

    def test_result_validation_line_positive(self):
        """Test that line number must be positive."""
        with pytest.raises(ValueError):
            ComplexityResult(
                name="func",
                line=0,  # Invalid: must be >= 1
                end_line=5,
                complexity=10,
                severity="acceptable",
            )

    def test_result_validation_complexity_non_negative(self):
        """Test that complexity must be non-negative."""
        with pytest.raises(ValueError):
            ComplexityResult(
                name="func",
                line=1,
                end_line=5,
                complexity=-1,  # Invalid: must be >= 0
                severity="healthy",
            )


class TestComplexitySummary:
    """Test ComplexitySummary model."""

    def test_summary_creation(self):
        """Test summary creation."""
        summary = ComplexitySummary(
            total_count=10,
            files_scanned=3,
            scan_duration_ms=150,
            high_complexity_count=10,
            by_severity={"warning": 5, "high_risk": 3, "critical": 2},
        )

        assert summary.total_count == 10
        assert summary.files_scanned == 3
        assert summary.high_complexity_count == 10
        assert summary.by_severity == {"warning": 5, "high_risk": 3, "critical": 2}

    def test_summary_validation(self):
        """Test summary validation."""
        with pytest.raises(ValueError):
            ComplexitySummary(
                total_count=-1,  # Invalid: negative count
                files_scanned=1,
                scan_duration_ms=100,
                high_complexity_count=0,
                by_severity={},
            )


class TestComplexityOutput:
    """Test ComplexityOutput model."""

    def test_output_structure(self):
        """Test output structure."""
        result = ComplexityResult(
            name="complex_func",
            line=10,
            end_line=30,
            complexity=15,
            severity="warning",
            message="Too complex",
            comment_lines=5,
            code_lines=20,
        )

        summary = ComplexitySummary(
            total_count=1,
            files_scanned=1,
            scan_duration_ms=50,
            high_complexity_count=1,
            by_severity={"warning": 1},
        )

        output = ComplexityOutput(
            summary=summary,
            results={"module.py": [result]},
        )

        assert output.summary.total_count == 1
        assert "module.py" in output.results
        assert len(output.results["module.py"]) == 1
        assert output.results["module.py"][0].name == "complex_func"

    def test_output_multiple_modules(self):
        """Test output with multiple modules."""
        result1 = ComplexityResult(
            name="func1",
            line=1,
            end_line=10,
            complexity=12,
            severity="warning",
            comment_lines=2,
            code_lines=10,
        )

        result2 = ComplexityResult(
            name="func2",
            line=20,
            end_line=40,
            complexity=18,
            severity="high_risk",
            comment_lines=3,
            code_lines=20,
        )

        summary = ComplexitySummary(
            total_count=2,
            files_scanned=2,
            scan_duration_ms=100,
            high_complexity_count=2,
            by_severity={"warning": 1, "high_risk": 1},
        )

        output = ComplexityOutput(
            summary=summary,
            results={
                "module1.py": [result1],
                "module2.py": [result2],
            },
        )

        assert len(output.results) == 2
        assert output.summary.total_count == 2

    def test_output_serialization(self):
        """Test output can be serialized to dict."""
        result = ComplexityResult(
            name="func",
            line=1,
            end_line=5,
            complexity=11,
            severity="warning",
            comment_lines=1,
            code_lines=5,
        )

        summary = ComplexitySummary(
            total_count=1,
            files_scanned=1,
            scan_duration_ms=10,
            high_complexity_count=1,
            by_severity={"warning": 1},
        )

        output = ComplexityOutput(
            summary=summary,
            results={"test.py": [result]},
        )

        data = output.model_dump()
        assert isinstance(data, dict)
        assert "summary" in data
        assert "results" in data
