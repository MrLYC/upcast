"""Test Pydantic models for blocking operations scanner."""

import pytest
from pydantic import ValidationError

from upcast.models.blocking_operations import (
    BlockingOperation,
    BlockingOperationsOutput,
    BlockingOperationsSummary,
)


class TestBlockingOperationModel:
    """Test BlockingOperation model validation."""

    def test_blocking_operation_model_valid(self):
        """Test creating a valid BlockingOperation instance."""
        operation = BlockingOperation(
            file="test.py",
            line=10,
            column=5,
            category="time_based",
            operation="time.sleep",
            statement="time.sleep(1)",
            function="my_function",
            class_name="MyClass",
        )

        assert operation.file == "test.py"
        assert operation.line == 10
        assert operation.column == 5
        assert operation.category == "time_based"
        assert operation.operation == "time.sleep"
        assert operation.statement == "time.sleep(1)"
        assert operation.function == "my_function"
        assert operation.class_name == "MyClass"

    def test_blocking_operation_minimal_fields(self):
        """Test BlockingOperation with only required fields."""
        operation = BlockingOperation(
            file="test.py",
            line=10,
            column=0,
            category="database",
            operation="select_for_update",
        )

        assert operation.file == "test.py"
        assert operation.line == 10
        assert operation.column == 0
        assert operation.category == "database"
        assert operation.operation == "select_for_update"
        assert operation.statement is None
        assert operation.function is None
        assert operation.class_name is None

    def test_blocking_operation_invalid_line(self):
        """Test that line number must be >= 1."""
        with pytest.raises(ValidationError) as exc_info:
            BlockingOperation(
                file="test.py",
                line=0,  # Invalid: must be >= 1
                column=0,
                category="time_based",
                operation="time.sleep",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("line",) for error in errors)

    def test_blocking_operation_invalid_column(self):
        """Test that column must be >= 0."""
        with pytest.raises(ValidationError) as exc_info:
            BlockingOperation(
                file="test.py",
                line=1,
                column=-1,  # Invalid: must be >= 0
                category="time_based",
                operation="time.sleep",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("column",) for error in errors)

    def test_blocking_operation_with_context(self):
        """Test BlockingOperation with all context fields."""
        operation = BlockingOperation(
            file="app/services.py",
            line=42,
            column=8,
            category="synchronization",
            operation="threading.Lock",
            statement="lock = threading.Lock()",
            function="process_data",
            class_name="DataProcessor",
        )

        assert operation.file == "app/services.py"
        assert operation.function == "process_data"
        assert operation.class_name == "DataProcessor"

    def test_blocking_operation_serialization(self):
        """Test that BlockingOperation can be serialized to dict."""
        operation = BlockingOperation(
            file="test.py",
            line=10,
            column=5,
            category="subprocess",
            operation="subprocess.run",
            statement="subprocess.run(['ls'])",
        )

        data = operation.model_dump()
        assert isinstance(data, dict)
        assert data["file"] == "test.py"
        assert data["line"] == 10
        assert data["category"] == "subprocess"
        assert data["operation"] == "subprocess.run"


class TestBlockingOperationsSummaryModel:
    """Test BlockingOperationsSummary model validation."""

    def test_summary_model_valid(self):
        """Test creating a valid BlockingOperationsSummary instance."""
        summary = BlockingOperationsSummary(
            total_count=10,
            files_scanned=5,
            by_category={"time_based": 4, "database": 3, "synchronization": 2, "subprocess": 1},
            scan_duration_ms=150,
        )

        assert summary.total_count == 10
        assert summary.files_scanned == 5
        assert summary.by_category == {
            "time_based": 4,
            "database": 3,
            "synchronization": 2,
            "subprocess": 1,
        }
        assert summary.scan_duration_ms == 150

    def test_summary_model_empty_categories(self):
        """Test summary with empty by_category."""
        summary = BlockingOperationsSummary(total_count=0, files_scanned=10, by_category={}, scan_duration_ms=100)

        assert summary.total_count == 0
        assert summary.files_scanned == 10
        assert summary.by_category == {}

    def test_summary_model_partial_categories(self):
        """Test summary with only some categories."""
        summary = BlockingOperationsSummary(
            total_count=5, files_scanned=3, by_category={"time_based": 5}, scan_duration_ms=75
        )

        assert summary.total_count == 5
        assert len(summary.by_category) == 1
        assert summary.by_category["time_based"] == 5

    def test_summary_model_serialization(self):
        """Test that summary can be serialized to dict."""
        summary = BlockingOperationsSummary(
            total_count=3,
            files_scanned=2,
            by_category={"database": 3},
            scan_duration_ms=200,
        )

        data = summary.model_dump()
        assert isinstance(data, dict)
        assert data["total_count"] == 3
        assert data["files_scanned"] == 2
        assert data["by_category"] == {"database": 3}
        assert data["scan_duration_ms"] == 200


class TestBlockingOperationsOutputModel:
    """Test BlockingOperationsOutput model validation."""

    def test_output_model_valid(self):
        """Test creating a valid BlockingOperationsOutput instance."""
        summary = BlockingOperationsSummary(
            total_count=2, files_scanned=1, by_category={"time_based": 2}, scan_duration_ms=100
        )

        operation1 = BlockingOperation(file="test.py", line=10, column=4, category="time_based", operation="time.sleep")
        operation2 = BlockingOperation(
            file="test.py", line=15, column=4, category="time_based", operation="asyncio.sleep"
        )

        output = BlockingOperationsOutput(
            summary=summary,
            results={
                "time_based": [operation1, operation2],
                "database": [],
                "synchronization": [],
                "subprocess": [],
            },
        )

        assert output.summary.total_count == 2
        assert len(output.results["time_based"]) == 2
        assert len(output.results["database"]) == 0

    def test_output_model_empty_results(self):
        """Test output with no operations found."""
        summary = BlockingOperationsSummary(
            total_count=0,
            files_scanned=5,
            by_category={},
            scan_duration_ms=50,
        )

        output = BlockingOperationsOutput(
            summary=summary,
            results={"time_based": [], "database": [], "synchronization": [], "subprocess": []},
        )

        assert output.summary.total_count == 0
        assert all(len(ops) == 0 for ops in output.results.values())

    def test_output_model_multiple_categories(self):
        """Test output with operations in multiple categories."""
        summary = BlockingOperationsSummary(
            total_count=4,
            files_scanned=2,
            by_category={"time_based": 2, "database": 1, "subprocess": 1},
            scan_duration_ms=200,
        )

        output = BlockingOperationsOutput(
            summary=summary,
            results={
                "time_based": [
                    BlockingOperation(file="a.py", line=1, column=0, category="time_based", operation="time.sleep"),
                    BlockingOperation(
                        file="a.py",
                        line=2,
                        column=0,
                        category="time_based",
                        operation="asyncio.sleep",
                    ),
                ],
                "database": [
                    BlockingOperation(
                        file="b.py",
                        line=10,
                        column=0,
                        category="database",
                        operation="select_for_update",
                    )
                ],
                "synchronization": [],
                "subprocess": [
                    BlockingOperation(
                        file="c.py",
                        line=20,
                        column=0,
                        category="subprocess",
                        operation="subprocess.run",
                    )
                ],
            },
        )

        assert output.summary.total_count == 4
        assert len(output.results["time_based"]) == 2
        assert len(output.results["database"]) == 1
        assert len(output.results["subprocess"]) == 1
        assert len(output.results["synchronization"]) == 0

    def test_output_model_serialization(self):
        """Test that output can be serialized to dict."""
        summary = BlockingOperationsSummary(
            total_count=1, files_scanned=1, by_category={"time_based": 1}, scan_duration_ms=100
        )

        operation = BlockingOperation(
            file="test.py",
            line=10,
            column=4,
            category="time_based",
            operation="time.sleep",
            statement="time.sleep(1)",
        )

        output = BlockingOperationsOutput(
            summary=summary,
            results={
                "time_based": [operation],
                "database": [],
                "synchronization": [],
                "subprocess": [],
            },
        )

        data = output.model_dump()
        assert isinstance(data, dict)
        assert "summary" in data
        assert "results" in data
        assert isinstance(data["results"], dict)
        assert len(data["results"]["time_based"]) == 1
        assert data["results"]["time_based"][0]["file"] == "test.py"
