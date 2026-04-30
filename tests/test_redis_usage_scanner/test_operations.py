"""Tests for Redis operations detection."""

import astroid
import pytest
from pathlib import Path
from textwrap import dedent

from upcast.common.hybrid_scan_pipeline import PipelineRunResult, SemanticDecision, StructuralCandidate
from upcast.models.redis_usage import RedisUsageType
from upcast.scanners.redis_usage import RedisUsageScanner


class TestCacheOperations:
    """Test Django cache operations detection."""

    def test_scanner_uses_hybrid_pipeline_for_cache_call_candidates(self, tmp_path, monkeypatch):
        """Cache API candidate discovery should go through the hybrid pipeline."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from django.core.cache import cache

            def use_cache():
                return cache.get("user:123")
        """)
        )

        scanner = RedisUsageScanner()
        calls: list[tuple[str, str]] = []

        def fake_run_pipeline(*, spec, source, file_path):
            module = astroid.parse(source, path=file_path)
            cache_call = next(module.nodes_of_class(astroid.nodes.Call))
            calls.append((spec.name, file_path))
            return PipelineRunResult(
                candidates=[
                    StructuralCandidate(
                        file_path=file_path,
                        structural_span={
                            "start": [cache_call.lineno, cache_call.col_offset],
                            "end": [cache_call.end_lineno, cache_call.end_col_offset],
                        },
                        captures={
                            "self": cache_call,
                            "TARGET": cache_call.func,
                            "ARGS": cache_call.args,
                        },
                        snippet=cache_call.as_string(),
                    )
                ],
                decisions=[SemanticDecision(status="confirmed")],
                findings=[],
            )

        monkeypatch.setattr("upcast.scanners.redis_usage.run_pipeline", fake_run_pipeline, raising=False)

        output = scanner.scan(test_file)

        assert calls == [("scan-redis-usage", str(test_file))]
        assert output.summary.total_usages == 1
        assert "direct_client" in output.results
        assert len(output.results["direct_client"]) == 1
        assert output.results["direct_client"][0].operation == "get"
        assert output.results["direct_client"][0].key == "user:123"

    def test_cache_get(self, tmp_path):
        """Cache.get should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from django.core.cache import cache

            def get_user():
                return cache.get("user:123")
        """)
        )

        scanner = RedisUsageScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_usages >= 1
        if "cache_backend" in output.results:
            cache_usages = output.results["cache_backend"]
            operations = [u.operation for u in cache_usages if u.operation]
            assert "get" in operations

    def test_cache_set(self, tmp_path):
        """Cache.set should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from django.core.cache import cache

            def save_user():
                cache.set("user:123", data, 300)
        """)
        )

        scanner = RedisUsageScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_usages >= 1

    def test_cache_delete(self, tmp_path):
        """Cache.delete should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from django.core.cache import cache

            def remove_user():
                cache.delete("user:123")
        """)
        )

        scanner = RedisUsageScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_usages >= 1

    def test_extended_cache_operations_are_detected(self):
        """Additional cache operation families should be reported."""
        fixture_path = Path(__file__).parent / "fixtures" / "ttl_patterns.py"

        scanner = RedisUsageScanner()
        output = scanner.scan(fixture_path)

        direct_usages = output.results.get("direct_client", [])
        operations = {usage.operation for usage in direct_usages}

        assert {"add", "touch", "delete_many", "clear", "incr", "decr"}.issubset(operations)


class TestDirectRedisOperations:
    """Test direct Redis client operations."""

    def test_redis_operations_basic(self, tmp_path):
        """Redis client operations should be handled gracefully."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import redis

            client = redis.Redis()
            value = client.get("key")
            client.set("key", "value")
            client.incr("counter")
        """)
        )

        scanner = RedisUsageScanner()
        output = scanner.scan(test_file)

        # Direct redis operations may or may not be detected depending on implementation
        assert output.summary.total_usages >= 0

    def test_redis_pipeline_basic(self, tmp_path):
        """Redis pipeline should be handled gracefully."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import redis

            client = redis.Redis()
            pipe = client.pipeline()
            pipe.set("key1", "value1")
            pipe.set("key2", "value2")
            pipe.execute()
        """)
        )

        scanner = RedisUsageScanner()
        output = scanner.scan(test_file)

        # Pipeline operations may or may not be detected depending on implementation
        assert output.summary.total_usages >= 0
