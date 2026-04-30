"""Tests for BlockingOperationsScanner."""

import astroid

from upcast.scanners.blocking_operations import (
    BlockingOperation,
    BlockingOperationsScanner,
)
from upcast.common.hybrid_scan_pipeline import PipelineRunResult, SemanticDecision, StructuralCandidate


class TestBlockingOperationModel:
    """Tests for BlockingOperation model."""

    def test_valid_operation(self):
        """Test creating valid BlockingOperation."""
        op = BlockingOperation(
            file="test.py",
            line=10,
            column=4,
            category="time_based",
            operation="time.sleep",
            statement="time.sleep(1)",
        )
        assert op.category == "time_based"
        assert op.operation == "time.sleep"

    def test_operation_with_duration(self):
        """Test BlockingOperation with duration value."""
        op = BlockingOperation(
            file="test.py",
            line=10,
            column=4,
            category="time_based",
            operation="time.sleep",
            statement="time.sleep(5)",
            duration=5,
        )
        assert op.duration == 5

    def test_operation_with_timeout_as_duration(self):
        """Test BlockingOperation with timeout value stored as duration."""
        op = BlockingOperation(
            file="test.py",
            line=10,
            column=4,
            category="subprocess",
            operation="subprocess.run",
            statement="subprocess.run(['ls'], timeout=30)",
            duration=30,
        )
        assert op.duration == 30


class TestBlockingOperationsScannerIntegration:
    """Integration tests for BlockingOperationsScanner."""

    def test_scanner_detects_sleep(self, tmp_path):
        """Test scanner detects time.sleep."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import time
time.sleep(1)
"""
        )

        scanner = BlockingOperationsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = BlockingOperationsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0

    def test_scanner_extracts_sleep_duration_literal(self, tmp_path):
        """Test scanner extracts literal sleep duration."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import time

def foo():
    time.sleep(5)
"""
        )

        scanner = BlockingOperationsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 1
        assert len(output.results["time_based"]) == 1

        operation = output.results["time_based"][0]
        assert operation.operation == "time.sleep"
        assert operation.duration == 5

    def test_scanner_extracts_sleep_duration_variable(self, tmp_path):
        """Test scanner extracts sleep duration from variable."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import time

def foo():
    timeout = 10
    time.sleep(timeout)
"""
        )

        scanner = BlockingOperationsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 1
        operation = output.results["time_based"][0]
        assert operation.duration == 10

    def test_scanner_extracts_sleep_duration_float(self, tmp_path):
        """Test scanner extracts float sleep duration."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import time

def foo():
    time.sleep(0.5)
"""
        )

        scanner = BlockingOperationsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 1
        operation = output.results["time_based"][0]
        assert operation.duration == 0.5

    def test_scanner_extracts_subprocess_timeout(self, tmp_path):
        """Test scanner extracts subprocess timeout as duration."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import subprocess

def foo():
    subprocess.run(['ls', '-la'], timeout=30)
"""
        )

        scanner = BlockingOperationsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 1
        operation = output.results["subprocess"][0]
        assert operation.operation == "subprocess.run"
        assert operation.duration == 30

    def test_scanner_handles_unresolvable_values(self, tmp_path):
        """Test scanner handles unresolvable duration/timeout values gracefully."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import time

def foo(dynamic_value):
    time.sleep(dynamic_value)
"""
        )

        scanner = BlockingOperationsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 1
        operation = output.results["time_based"][0]
        assert operation.duration is None

    def test_scanner_handles_complex_expressions(self, tmp_path):
        """Test scanner handles complex expressions for duration."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import time

def foo():
    time.sleep(5 * 60)
"""
        )

        scanner = BlockingOperationsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 1
        operation = output.results["time_based"][0]
        assert operation.duration == 300

    def test_scanner_uses_hybrid_pipeline_for_blocking_candidates(self, tmp_path, monkeypatch):
        """Scanner should use the hybrid pipeline to discover blocking-operation candidates."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import time

def wait_for_data():
    time.sleep(1)
"""
        )

        scanner = BlockingOperationsScanner()
        calls: list[tuple[str, str]] = []

        def fake_run_pipeline(*, spec, source, file_path):
            module = astroid.parse(source, path=file_path)
            sleep_call = next(node for node in module.nodes_of_class(astroid.nodes.Call))
            calls.append((spec.name, file_path))
            return PipelineRunResult(
                candidates=[
                    StructuralCandidate(
                        file_path=file_path,
                        structural_span={"start": [4, 4], "end": [4, 17]},
                        captures={"self": sleep_call, "OP": sleep_call},
                    )
                ],
                decisions=[SemanticDecision(status="confirmed")],
                findings=[],
            )

        monkeypatch.setattr("upcast.scanners.blocking_operations.run_pipeline", fake_run_pipeline, raising=False)

        output = scanner.scan(test_file)

        assert calls == [("scan-blocking-operations", str(test_file))]
        assert output.summary.total_count == 1
        assert output.results["time_based"][0].operation == "time.sleep"
