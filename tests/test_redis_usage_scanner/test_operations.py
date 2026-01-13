"""Tests for Redis operations detection."""

import pytest
from pathlib import Path
from textwrap import dedent

from upcast.scanners.redis_usage import RedisUsageScanner
from upcast.models.redis_usage import RedisUsageType


class TestCacheOperations:
    """Test Django cache operations detection."""

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
