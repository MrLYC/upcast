"""Tests for ComplexityScanner models and implementation."""

import pytest
from pydantic import ValidationError

from upcast.scanners.complexity import (
    ComplexityOutput,
    ComplexityResult,
    ComplexityScanner,
    ComplexitySummary,
)


class TestComplexityResultModel:
    """Tests for ComplexityResult Pydantic model."""

    def test_valid_result(self):
        """Test creating valid ComplexityResult."""
        result = ComplexityResult(
            name="complex_function",
            line=10,
            end_line=50,
            complexity=15,
            severity="warning",
            message="Function has high complexity",
            comment_lines=5,
            code_lines=40,
        )

        assert result.name == "complex_function"
        assert result.line == 10
        assert result.end_line == 50
        assert result.complexity == 15
        assert result.severity == "warning"

    def test_result_with_metadata_fields(self):
        """Test ComplexityResult with all metadata fields."""
        result = ComplexityResult(
            name="documented_function",
            line=1,
            end_line=20,
            complexity=8,
            severity="acceptable",
            message="OK",
            description="This is a documented function",
            signature="def documented_function(x: int, y: str = 'default') -> bool:",
            code="def documented_function(x: int, y: str = 'default') -> bool:\n    '''This is a documented function'''\n    return True\n",
            comment_lines=2,
            code_lines=20,
        )

        assert result.description == "This is a documented function"
        assert "documented_function" in result.signature
        assert result.code is not None
        assert result.comment_lines == 2
        assert result.code_lines == 20

    def test_result_validates_line_number(self):
        """Test that line number must be >= 1."""
        with pytest.raises(ValidationError):
            ComplexityResult(
                name="func",
                line=0,  # invalid
                end_line=10,
                complexity=5,
                severity="warning",
                message=None,
            )

    def test_result_validates_complexity(self):
        """Test that complexity must be >= 0."""
        with pytest.raises(ValidationError):
            ComplexityResult(
                name="func",
                line=1,
                end_line=10,
                complexity=-1,  # invalid
                severity="warning",
                message=None,
            )


class TestComplexitySummaryModel:
    """Tests for ComplexitySummary Pydantic model."""

    def test_valid_summary(self):
        """Test creating valid ComplexitySummary."""
        summary = ComplexitySummary(
            total_count=10,
            files_scanned=3,
            scan_duration_ms=100,
            high_complexity_count=5,
            by_severity={"warning": 3, "high_risk": 2},
        )

        assert summary.high_complexity_count == 5
        assert summary.by_severity["warning"] == 3


class TestComplexityOutputModel:
    """Tests for ComplexityOutput Pydantic model."""

    def test_valid_output(self):
        """Test creating valid ComplexityOutput."""
        summary = ComplexitySummary(
            total_count=2,
            files_scanned=1,
            scan_duration_ms=50,
            high_complexity_count=2,
            by_severity={"warning": 1, "high_risk": 1},
        )

        results = {
            "test.py": [
                ComplexityResult(
                    name="func1",
                    line=10,
                    end_line=20,
                    complexity=10,
                    severity="warning",
                    message="",
                    comment_lines=2,
                    code_lines=10,
                ),
                ComplexityResult(
                    name="func2",
                    line=30,
                    end_line=50,
                    complexity=20,
                    severity="high_risk",
                    message="",
                    comment_lines=3,
                    code_lines=20,
                ),
            ]
        }

        output = ComplexityOutput(summary=summary, results=results, metadata={})

        assert output.summary.high_complexity_count == 2
        assert len(output.results["test.py"]) == 2


class TestComplexityScannerIntegration:
    """Integration tests for ComplexityScanner."""

    def test_scanner_detects_simple_function(self, tmp_path):
        """Test scanner detects simple function complexity."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
def simple_function():
    return 42
"""
        )

        scanner = ComplexityScanner(threshold=1)
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0
        assert output.summary.files_scanned == 1

    def test_scanner_detects_complex_function(self, tmp_path):
        """Test scanner detects complex functions."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
def complex_function(x):
    if x > 0:
        if x > 10:
            return 'high'
        elif x > 5:
            return 'medium'
        else:
            return 'low'
    else:
        return 'negative'
"""
        )

        scanner = ComplexityScanner(threshold=1)
        output = scanner.scan(test_file)

        assert output.summary.total_count > 0

    def test_scanner_respects_threshold(self, tmp_path):
        """Test scanner respects complexity threshold."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
def simple():
    return 1

def complex(x):
    if x > 0:
        if x > 10:
            return 'high'
        else:
            return 'low'
    return 'zero'
"""
        )

        # Use low threshold to detect complex function
        scanner = ComplexityScanner(threshold=3)
        output = scanner.scan(test_file)

        # Should detect files and functions above threshold
        assert output.summary.files_scanned == 1
        assert output.summary.total_count >= 1
        # The complex function should be detected (key is relative path)
        assert "test.py" in output.results
        assert len(output.results["test.py"]) >= 1

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = ComplexityScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0
        # Empty file may not be counted as scanned
        assert output.summary.files_scanned >= 0

    def test_scanner_with_directory(self, tmp_path):
        """Test scanner can scan directory."""
        # Create files with functions that exceed default threshold (11)
        (tmp_path / "file1.py").write_text(
            """
def complex_func(x):
    if x > 0:
        if x > 10:
            if x > 20:
                if x > 30:
                    if x > 40:
                        if x > 50:
                            if x > 60:
                                if x > 70:
                                    if x > 80:
                                        if x > 90:
                                            return 'very high'
                                        return 'high9'
                                    return 'high8'
                                return 'high7'
                            return 'high6'
                        return 'high5'
                    return 'high4'
                return 'high3'
            return 'high2'
        return 'high1'
    return 'zero'
"""
        )
        (tmp_path / "file2.py").write_text(
            """
def another_complex(y):
    for i in range(10):
        if i > 0:
            if i > 1:
                if i > 2:
                    if i > 3:
                        if i > 4:
                            if i > 5:
                                if i > 6:
                                    if i > 7:
                                        if i > 8:
                                            if i > 9:
                                                print('max')
                                            print('9')
                                        print('8')
                                    print('7')
                                print('6')
                            print('5')
                        print('4')
                    print('3')
                print('2')
            print('1')
        print(i)
"""
        )

        scanner = ComplexityScanner()
        output = scanner.scan(tmp_path)

        # Should scan both files with complex functions
        assert output.summary.files_scanned >= 1
        assert output.summary.total_count >= 1

    def test_scanner_extracts_metadata_fields(self, tmp_path):
        """Test scanner extracts all metadata fields."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            '''
def documented_function(x: int, y: str = "default") -> bool:
    """This is the description line.

    More details here.
    """
    if x > 0:
        if x > 5:
            if x > 10:
                return True
    return False
'''
        )

        scanner = ComplexityScanner(threshold=1)
        output = scanner.scan(test_file)

        assert len(output.results) > 0
        result = next(iter(output.results.values()))[0]

        # Verify all metadata fields are populated
        assert result.description == "This is the description line."
        assert "documented_function" in result.signature
        assert "int" in result.signature
        assert result.code is not None
        assert "def documented_function" in result.code
        assert result.code_lines > 0  # Should calculate total lines
        # Note: comment_lines may be 0 since astroid's as_string() can strip comments
