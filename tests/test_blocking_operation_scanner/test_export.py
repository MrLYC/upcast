"""Tests for export module."""

import json

import yaml

from upcast.blocking_operation_scanner.export import (
    export_to_json,
    export_to_yaml,
    format_operations_output,
)
from upcast.blocking_operation_scanner.operation_parser import (
    BlockingOperation,
    OperationType,
)


def test_format_operations_output():
    """Test formatting operations for output."""
    operations = [
        BlockingOperation(
            type=OperationType.TIME_SLEEP,
            file="test.py",
            line=10,
            column=4,
            statement="time.sleep(5)",
            duration=5,
        ),
        BlockingOperation(
            type=OperationType.LOCK_ACQUIRE,
            file="test.py",
            line=15,
            column=4,
            statement="lock.acquire()",
        ),
    ]

    result = format_operations_output(operations)

    assert "summary" in result
    assert result["summary"]["total_operations"] == 2
    assert "time_based" in result["operations"]
    assert "synchronization" in result["operations"]


def test_format_operations_output_with_base_path(tmp_path):
    """Test formatting with relative paths."""
    test_file = tmp_path / "subdir" / "test.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("")

    operations = [
        BlockingOperation(
            type=OperationType.TIME_SLEEP,
            file=str(test_file),
            line=10,
            column=4,
            statement="time.sleep(5)",
        ),
    ]

    result = format_operations_output(operations, base_path=tmp_path)

    # Check that path is relative
    assert "subdir/test.py" in str(result)


def test_format_operations_output_grouping():
    """Test operations are grouped by category."""
    operations = [
        BlockingOperation(
            type=OperationType.TIME_SLEEP,
            file="a.py",
            line=1,
            column=0,
            statement="time.sleep(1)",
        ),
        BlockingOperation(
            type=OperationType.DB_SELECT_FOR_UPDATE,
            file="b.py",
            line=1,
            column=0,
            statement="select_for_update()",
        ),
        BlockingOperation(
            type=OperationType.LOCK_ACQUIRE,
            file="c.py",
            line=1,
            column=0,
            statement="lock.acquire()",
        ),
        BlockingOperation(
            type=OperationType.SUBPROCESS_RUN,
            file="d.py",
            line=1,
            column=0,
            statement="subprocess.run()",
        ),
    ]

    result = format_operations_output(operations)

    assert len(result["operations"]["time_based"]) == 1
    assert len(result["operations"]["database"]) == 1
    assert len(result["operations"]["synchronization"]) == 1
    assert len(result["operations"]["subprocess"]) == 1


def test_format_operations_output_sorting():
    """Test operations are sorted by file and line."""
    operations = [
        BlockingOperation(
            type=OperationType.TIME_SLEEP,
            file="b.py",
            line=20,
            column=0,
            statement="sleep(2)",
        ),
        BlockingOperation(
            type=OperationType.TIME_SLEEP,
            file="a.py",
            line=10,
            column=0,
            statement="sleep(1)",
        ),
        BlockingOperation(
            type=OperationType.TIME_SLEEP,
            file="b.py",
            line=5,
            column=0,
            statement="sleep(3)",
        ),
    ]

    result = format_operations_output(operations)
    time_ops = result["operations"]["time_based"]

    # Should have all operations
    assert len(time_ops) == 3
    # Check that all locations are present
    locations = {op["location"] for op in time_ops}
    assert locations == {"a.py:10:0", "b.py:5:0", "b.py:20:0"}


def test_export_to_yaml():
    """Test exporting to YAML format."""
    operations = [
        BlockingOperation(
            type=OperationType.TIME_SLEEP,
            file="test.py",
            line=10,
            column=4,
            statement="time.sleep(5)",
            duration=5,
        ),
    ]

    result = export_to_yaml(operations)

    assert isinstance(result, str)
    data = yaml.safe_load(result)
    assert "summary" in data
    assert "operations" in data


def test_export_to_json():
    """Test exporting to JSON format."""
    operations = [
        BlockingOperation(
            type=OperationType.TIME_SLEEP,
            file="test.py",
            line=10,
            column=4,
            statement="time.sleep(5)",
            duration=5,
        ),
    ]

    result = export_to_json(operations)

    assert isinstance(result, str)
    data = json.loads(result)
    assert "summary" in data
    assert "operations" in data


def test_export_preserves_metadata():
    """Test that export preserves all operation metadata."""
    operations = [
        BlockingOperation(
            type=OperationType.TIME_SLEEP,
            file="test.py",
            line=10,
            column=4,
            statement="time.sleep(5)",
            function="my_func",
            class_name="MyClass",
            is_async_context=True,
            duration=5,
        ),
    ]

    result = export_to_yaml(operations)
    data = yaml.safe_load(result)

    op = data["operations"]["time_based"][0]
    assert op["function"] == "my_func"
    assert op["class"] == "MyClass"
    assert op["async_context"] is True
    assert op["duration"] == 5


def test_export_summary_stats():
    """Test summary statistics in export."""
    operations = [
        BlockingOperation(
            type=OperationType.TIME_SLEEP,
            file="test1.py",
            line=10,
            column=4,
            statement="sleep(1)",
        ),
        BlockingOperation(
            type=OperationType.TIME_SLEEP,
            file="test2.py",
            line=5,
            column=0,
            statement="sleep(2)",
        ),
        BlockingOperation(
            type=OperationType.LOCK_ACQUIRE,
            file="test1.py",
            line=20,
            column=4,
            statement="lock.acquire()",
        ),
    ]

    result = format_operations_output(operations)
    summary = result["summary"]

    assert summary["total_operations"] == 3
    assert summary["by_category"]["time_based"] == 2
    assert summary["by_category"]["synchronization"] == 1
    assert summary["files_analyzed"] == 2
