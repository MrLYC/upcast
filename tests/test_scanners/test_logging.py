"""Hybrid candidate-selection tests for LoggingScanner."""

import astroid

from upcast.common.hybrid_scan_pipeline import PipelineRunResult, SemanticDecision, StructuralCandidate
from upcast.scanners.logging_scanner import LoggingScanner


def test_scanner_uses_hybrid_pipeline_for_logging_call_candidates(tmp_path, monkeypatch):
    """Scanner should use the hybrid pipeline to discover logging call candidates."""
    test_file = tmp_path / "test.py"
    test_file.write_text(
        """
import logging

logger = logging.getLogger(__name__)


def log_values():
    logger.info("hello world")
""".strip()
        + "\n",
        encoding="utf-8",
    )

    scanner = LoggingScanner()
    calls: list[tuple[str, str]] = []

    def fake_run_pipeline(*, spec, source, file_path):
        module = astroid.parse(source, path=file_path)
        log_call = next(
            node
            for node in module.nodes_of_class(astroid.nodes.Call)
            if isinstance(node.func, astroid.nodes.Attribute) and node.func.attrname == "info"
        )
        calls.append((spec.name, file_path))
        return PipelineRunResult(
            candidates=[
                StructuralCandidate(
                    file_path=file_path,
                    structural_span={
                        "start": [log_call.lineno, log_call.col_offset],
                        "end": [log_call.end_lineno, log_call.end_col_offset],
                    },
                    captures={
                        "self": log_call,
                        "TARGET": log_call.func,
                        "ARGS": log_call.args,
                    },
                    snippet=log_call.as_string(),
                )
            ],
            decisions=[SemanticDecision(status="confirmed")],
            findings=[],
        )

    monkeypatch.setattr("upcast.scanners.logging_scanner.run_pipeline", fake_run_pipeline, raising=False)

    output = scanner.scan(test_file)

    assert calls == [("scan-logging", str(test_file))]
    assert output.summary.total_count == 1
    assert output.summary.by_level == {"info": 1}
    file_info = output.results["test.py"]
    assert file_info.logging[0].message == "hello world"
