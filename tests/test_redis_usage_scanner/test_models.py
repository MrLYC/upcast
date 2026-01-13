"""Tests for Redis usage scanner models."""

import pytest
from pydantic import ValidationError

from upcast.models.redis_usage import (
    RedisUsageType,
    RedisConfig,
    RedisUsage,
    RedisUsageSummary,
    RedisUsageOutput,
)


class TestRedisUsageTypeEnum:
    """Test RedisUsageType enum."""

    def test_enum_values(self):
        """Enum should have all expected values."""
        assert RedisUsageType.CACHE_BACKEND == "cache_backend"
        assert RedisUsageType.SESSION_STORAGE == "session_storage"
        assert RedisUsageType.CELERY_BROKER == "celery_broker"
        assert RedisUsageType.DIRECT_CLIENT == "direct_client"


class TestRedisConfigModel:
    """Test RedisConfig model."""

    def test_redis_config_valid(self):
        """Valid RedisConfig should be created."""
        config = RedisConfig(
            backend="django_redis.cache.RedisCache",
            location="redis://localhost:6379/1",
            db=1,
            host="localhost",
            port=6379,
        )

        assert config.backend == "django_redis.cache.RedisCache"
        assert config.location == "redis://localhost:6379/1"
        assert config.db == 1
        assert config.host == "localhost"
        assert config.port == 6379

    def test_redis_config_defaults(self):
        """RedisConfig should have default values."""
        config = RedisConfig()

        assert config.backend is None
        assert config.location is None
        assert config.options == {}


class TestRedisUsageModel:
    """Test RedisUsage model."""

    def test_redis_usage_valid(self):
        """Valid RedisUsage should be created."""
        usage = RedisUsage(
            type=RedisUsageType.CACHE_BACKEND,
            file="settings.py",
            line=42,
            library="django_redis",
            operation="get",
            key="user:...",
            statement="cache.get(key)",
        )

        assert usage.type == RedisUsageType.CACHE_BACKEND
        assert usage.file == "settings.py"
        assert usage.line == 42
        assert usage.library == "django_redis"
        assert usage.operation == "get"
        assert usage.key == "user:..."

    def test_redis_usage_invalid_line(self):
        """RedisUsage with invalid line should fail."""
        with pytest.raises(ValidationError):
            RedisUsage(
                type=RedisUsageType.DIRECT_CLIENT,
                file="test.py",
                line=0,  # Must be > 0
            )

    def test_redis_usage_with_config(self):
        """RedisUsage with config should be created."""
        config = RedisConfig(host="localhost", port=6379)
        usage = RedisUsage(
            type=RedisUsageType.CACHE_BACKEND,
            file="settings.py",
            line=10,
            config=config,
        )

        assert usage.config == config
        assert usage.config.host == "localhost"


class TestRedisUsageSummaryModel:
    """Test RedisUsageSummary model."""

    def test_summary_valid(self):
        """Valid RedisUsageSummary should be created."""
        summary = RedisUsageSummary(
            total_count=5,
            total_usages=5,
            files_scanned=2,
            scan_duration_ms=100,
            categories={"cache_backend": 3, "direct_client": 2},
            warnings=["Warning 1"],
        )

        assert summary.total_usages == 5
        assert summary.categories == {"cache_backend": 3, "direct_client": 2}
        assert summary.warnings == ["Warning 1"]

    def test_summary_defaults(self):
        """RedisUsageSummary should have default values."""
        summary = RedisUsageSummary(
            total_count=0,
            total_usages=0,
            files_scanned=0,
            scan_duration_ms=0,
        )

        assert summary.categories == {}
        assert summary.warnings == []


class TestRedisUsageOutputModel:
    """Test RedisUsageOutput model."""

    def test_output_valid(self):
        """Valid RedisUsageOutput should be created."""
        summary = RedisUsageSummary(
            total_count=1,
            total_usages=1,
            files_scanned=1,
            scan_duration_ms=50,
        )

        usage = RedisUsage(
            type=RedisUsageType.CACHE_BACKEND,
            file="test.py",
            line=1,
        )

        output = RedisUsageOutput(
            summary=summary,
            results={"cache_backend": [usage]},
        )

        assert output.summary == summary
        assert len(output.results) == 1
        assert "cache_backend" in output.results

    def test_output_empty(self):
        """Empty RedisUsageOutput should be created."""
        summary = RedisUsageSummary(
            total_count=0,
            total_usages=0,
            files_scanned=0,
            scan_duration_ms=0,
        )

        output = RedisUsageOutput(summary=summary, results={})

        assert len(output.results) == 0
