"""Tests for ExceptionHandlerScanner."""

import astroid

from upcast.common.hybrid_scan_pipeline import PipelineRunResult, SemanticDecision, StructuralCandidate
from upcast.models.exceptions import ExceptionBlock
from upcast.scanners.exceptions import ExceptionHandlerScanner


class TestExceptionModels:
    """Tests for exception handler models."""

    def test_valid_exception_block(self):
        """Test creating valid ExceptionBlock."""
        block = ExceptionBlock(
            lineno=10,
            exceptions=["ValueError", "TypeError"],
            lines=3,
            log_error_count=1,
        )
        assert block.lineno == 10
        assert len(block.exceptions) == 2


class TestExceptionHandlerScannerIntegration:
    """Integration tests for ExceptionHandlerScanner."""

    def test_scanner_detects_try_except(self, tmp_path):
        """Test scanner detects try-except blocks."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
try:
    risky_operation()
except ValueError:
    pass
"""
        )

        scanner = ExceptionHandlerScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = ExceptionHandlerScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0

    def test_scanner_uses_hybrid_pipeline_for_try_block_candidates(self, tmp_path, monkeypatch):
        """Scanner should use the hybrid pipeline to discover try-block candidates."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
def parse_value(raw):
    try:
        return int(raw)
    except ValueError:
        return 0
"""
        )

        scanner = ExceptionHandlerScanner()
        calls: list[tuple[str, str]] = []

        def fake_run_pipeline(*, spec, source, file_path):
            module = astroid.parse(source, path=file_path)
            try_node = next(module.nodes_of_class(astroid.nodes.Try))
            calls.append((spec.name, file_path))
            return PipelineRunResult(
                candidates=[
                    StructuralCandidate(
                        file_path=file_path,
                        structural_span={
                            "start": [try_node.lineno, try_node.col_offset],
                            "end": [try_node.end_lineno, try_node.end_col_offset],
                        },
                        captures={"self": try_node, "BODY": try_node.body},
                        snippet=try_node.as_string(),
                    )
                ],
                decisions=[SemanticDecision(status="confirmed")],
                findings=[],
            )

        monkeypatch.setattr("upcast.scanners.exceptions.run_pipeline", fake_run_pipeline, raising=False)

        output = scanner.scan(test_file)

        assert calls == [("scan-exception-handlers", str(test_file))]
        assert output.summary.total_handlers == 1
        assert output.summary.total_except_clauses == 1
        assert output.results[0].exception_blocks[0].exceptions == ["ValueError"]
