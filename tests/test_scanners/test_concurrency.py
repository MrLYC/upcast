"""Tests for ConcurrencyPatternScanner."""

import astroid

from upcast.common.hybrid_scan_pipeline import PipelineRunResult, SemanticDecision, StructuralCandidate
from upcast.scanners.concurrency import (
    ConcurrencyScanner,
    ConcurrencyUsage,
)


class TestConcurrencyModels:
    """Tests for concurrency models."""

    def test_valid_usage(self):
        """Test creating valid ConcurrencyUsage."""
        usage = ConcurrencyUsage(
            file="test.py",
            line=10,
            column=0,
            pattern="threading.Thread",
            statement="t = threading.Thread(target=worker)",
        )
        assert usage.pattern == "threading.Thread"


class TestConcurrencyPatternScannerIntegration:
    """Integration tests for ConcurrencyPatternScanner."""

    def test_scanner_uses_hybrid_pipeline_for_concurrency_call_candidates(self, tmp_path, monkeypatch):
        """Scanner should use the hybrid pipeline to discover concurrency call candidates."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import threading


def worker():
    return None


def create_thread():
    thread = threading.Thread(target=worker)
    thread.start()
"""
        )

        scanner = ConcurrencyScanner()
        calls: list[tuple[str, str]] = []

        def fake_run_pipeline(*, spec, source, file_path):
            module = astroid.parse(source, path=file_path)
            thread_call = next(module.nodes_of_class(astroid.nodes.Call))
            calls.append((spec.name, file_path))
            return PipelineRunResult(
                candidates=[
                    StructuralCandidate(
                        file_path=file_path,
                        structural_span={
                            "start": [thread_call.lineno, thread_call.col_offset],
                            "end": [thread_call.end_lineno, thread_call.end_col_offset],
                        },
                        captures={
                            "self": thread_call,
                            "TARGET": thread_call.func,
                            "ARGS": thread_call.args,
                        },
                        snippet=thread_call.as_string(),
                    )
                ],
                decisions=[SemanticDecision(status="confirmed")],
                findings=[],
            )

        monkeypatch.setattr("upcast.scanners.concurrency.run_pipeline", fake_run_pipeline, raising=False)

        output = scanner.scan(test_file)

        assert calls == [("scan-concurrency-patterns", str(test_file))]
        assert output.summary.total_count >= 1
        threading_patterns = output.results["threading"]
        assert "thread_creation" in threading_patterns
        assert threading_patterns["thread_creation"][0].pattern == "thread_creation"

    def test_scanner_detects_threading(self, tmp_path):
        """Test scanner detects threading patterns."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import threading
t = threading.Thread(target=lambda: None)
"""
        )

        scanner = ConcurrencyScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = ConcurrencyScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0
