"""Test Pydantic models for concurrency pattern scanner."""

import pytest
from pydantic import ValidationError

from upcast.models.concurrency import (
    ConcurrencyUsage,
    ConcurrencyPatternOutput,
    ConcurrencyPatternSummary,
)


class TestConcurrencyUsageModel:
    """Test ConcurrencyUsage model validation."""

    def test_concurrency_usage_model_valid(self):
        """Test creating a valid ConcurrencyUsage instance."""
        usage = ConcurrencyUsage(
            file="test.py",
            line=10,
            column=5,
            pattern="thread_creation",
            statement="t = threading.Thread(target=worker)",
            function="create_thread",
            class_name="ThreadManager",
            details={"target": "worker", "name": "thread-1"},
            api_call="Thread",
        )

        assert usage.file == "test.py"
        assert usage.line == 10
        assert usage.column == 5
        assert usage.pattern == "thread_creation"
        assert usage.statement == "t = threading.Thread(target=worker)"
        assert usage.function == "create_thread"
        assert usage.class_name == "ThreadManager"
        assert usage.details == {"target": "worker", "name": "thread-1"}
        assert usage.api_call == "Thread"

    def test_concurrency_usage_minimal_fields(self):
        """Test ConcurrencyUsage with only required fields."""
        usage = ConcurrencyUsage(
            file="test.py",
            line=10,
            column=0,
            pattern="async_function",
        )

        assert usage.file == "test.py"
        assert usage.line == 10
        assert usage.column == 0
        assert usage.pattern == "async_function"
        assert usage.statement is None
        assert usage.function is None
        assert usage.class_name is None
        assert usage.details is None
        assert usage.api_call is None

    def test_concurrency_usage_invalid_line(self):
        """Test that line number must be >= 1."""
        with pytest.raises(ValidationError) as exc_info:
            ConcurrencyUsage(
                file="test.py",
                line=0,  # Invalid: must be >= 1
                column=0,
                pattern="thread_creation",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("line",) for error in errors)

    def test_concurrency_usage_invalid_column(self):
        """Test that column must be >= 0."""
        with pytest.raises(ValidationError) as exc_info:
            ConcurrencyUsage(
                file="test.py",
                line=1,
                column=-1,  # Invalid: must be >= 0
                pattern="thread_creation",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("column",) for error in errors)

    def test_concurrency_usage_with_details(self):
        """Test ConcurrencyUsage with various details."""
        usage = ConcurrencyUsage(
            file="async_app.py",
            line=42,
            column=8,
            pattern="create_task",
            statement="task = asyncio.create_task(worker())",
            function="main",
            details={"coroutine": "worker"},
            api_call="create_task",
        )

        assert usage.file == "async_app.py"
        assert usage.pattern == "create_task"
        assert usage.details["coroutine"] == "worker"
        assert usage.api_call == "create_task"

    def test_concurrency_usage_serialization(self):
        """Test that ConcurrencyUsage can be serialized to dict."""
        usage = ConcurrencyUsage(
            file="test.py",
            line=10,
            column=5,
            pattern="thread_pool_executor",
            statement="executor = ThreadPoolExecutor(max_workers=4)",
            details={"max_workers": 4},
        )

        data = usage.model_dump()
        assert isinstance(data, dict)
        assert data["file"] == "test.py"
        assert data["line"] == 10
        assert data["pattern"] == "thread_pool_executor"
        assert data["details"]["max_workers"] == 4


class TestConcurrencyPatternSummaryModel:
    """Test ConcurrencyPatternSummary model validation."""

    def test_summary_model_valid(self):
        """Test creating a valid ConcurrencyPatternSummary instance."""
        summary = ConcurrencyPatternSummary(
            total_count=20,
            files_scanned=5,
            by_category={"threading": 8, "multiprocessing": 4, "asyncio": 6, "celery": 2},
            scan_duration_ms=250,
        )

        assert summary.total_count == 20
        assert summary.files_scanned == 5
        assert summary.by_category == {
            "threading": 8,
            "multiprocessing": 4,
            "asyncio": 6,
            "celery": 2,
        }
        assert summary.scan_duration_ms == 250

    def test_summary_model_empty_categories(self):
        """Test summary with empty by_category."""
        summary = ConcurrencyPatternSummary(total_count=0, files_scanned=10, by_category={}, scan_duration_ms=100)

        assert summary.total_count == 0
        assert summary.files_scanned == 10
        assert summary.by_category == {}

    def test_summary_model_partial_categories(self):
        """Test summary with only some categories."""
        summary = ConcurrencyPatternSummary(
            total_count=10, files_scanned=3, by_category={"asyncio": 10}, scan_duration_ms=75
        )

        assert summary.total_count == 10
        assert len(summary.by_category) == 1
        assert summary.by_category["asyncio"] == 10

    def test_summary_model_serialization(self):
        """Test that summary can be serialized to dict."""
        summary = ConcurrencyPatternSummary(
            total_count=5,
            files_scanned=2,
            by_category={"threading": 3, "asyncio": 2},
            scan_duration_ms=200,
        )

        data = summary.model_dump()
        assert isinstance(data, dict)
        assert data["total_count"] == 5
        assert data["files_scanned"] == 2
        assert data["by_category"] == {"threading": 3, "asyncio": 2}
        assert data["scan_duration_ms"] == 200


class TestConcurrencyPatternOutputModel:
    """Test ConcurrencyPatternOutput model validation."""

    def test_output_model_valid(self):
        """Test creating a valid ConcurrencyPatternOutput instance."""
        summary = ConcurrencyPatternSummary(
            total_count=2, files_scanned=1, by_category={"threading": 2}, scan_duration_ms=100
        )

        usage1 = ConcurrencyUsage(file="test.py", line=10, column=4, pattern="thread_creation")
        usage2 = ConcurrencyUsage(file="test.py", line=15, column=4, pattern="thread_pool_executor")

        output = ConcurrencyPatternOutput(
            summary=summary,
            results={
                "threading": {"thread_creation": [usage1], "thread_pool_executor": [usage2]},
                "multiprocessing": {},
                "asyncio": {},
                "celery": {},
            },
        )

        assert output.summary.total_count == 2
        assert len(output.results["threading"]["thread_creation"]) == 1
        assert len(output.results["threading"]["thread_pool_executor"]) == 1
        assert len(output.results["asyncio"]) == 0

    def test_output_model_empty_results(self):
        """Test output with no patterns found."""
        summary = ConcurrencyPatternSummary(
            total_count=0,
            files_scanned=5,
            by_category={},
            scan_duration_ms=50,
        )

        output = ConcurrencyPatternOutput(
            summary=summary,
            results={"threading": {}, "multiprocessing": {}, "asyncio": {}, "celery": {}},
        )

        assert output.summary.total_count == 0
        assert all(len(patterns) == 0 for patterns in output.results.values())

    def test_output_model_multiple_categories(self):
        """Test output with patterns in multiple categories."""
        summary = ConcurrencyPatternSummary(
            total_count=4,
            files_scanned=2,
            by_category={"threading": 2, "asyncio": 2},
            scan_duration_ms=200,
        )

        output = ConcurrencyPatternOutput(
            summary=summary,
            results={
                "threading": {
                    "thread_creation": [ConcurrencyUsage(file="a.py", line=1, column=0, pattern="thread_creation")],
                    "thread_pool_executor": [
                        ConcurrencyUsage(file="a.py", line=2, column=0, pattern="thread_pool_executor")
                    ],
                },
                "multiprocessing": {},
                "asyncio": {
                    "async_function": [ConcurrencyUsage(file="b.py", line=10, column=0, pattern="async_function")],
                    "await": [ConcurrencyUsage(file="b.py", line=11, column=4, pattern="await")],
                },
                "celery": {},
            },
        )

        assert output.summary.total_count == 4
        assert len(output.results["threading"]) == 2
        assert len(output.results["asyncio"]) == 2
        assert len(output.results["multiprocessing"]) == 0

    def test_output_model_serialization(self):
        """Test that output can be serialized to dict."""
        summary = ConcurrencyPatternSummary(
            total_count=1, files_scanned=1, by_category={"asyncio": 1}, scan_duration_ms=100
        )

        usage = ConcurrencyUsage(
            file="test.py",
            line=10,
            column=4,
            pattern="create_task",
            statement="task = asyncio.create_task(worker())",
            details={"coroutine": "worker"},
        )

        output = ConcurrencyPatternOutput(
            summary=summary,
            results={
                "threading": {},
                "multiprocessing": {},
                "asyncio": {"create_task": [usage]},
                "celery": {},
            },
        )

        data = output.model_dump()
        assert isinstance(data, dict)
        assert "summary" in data
        assert "results" in data
        assert isinstance(data["results"], dict)
        assert "create_task" in data["results"]["asyncio"]
        assert len(data["results"]["asyncio"]["create_task"]) == 1
        assert data["results"]["asyncio"]["create_task"][0]["file"] == "test.py"
