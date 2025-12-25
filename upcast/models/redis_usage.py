"""Redis usage data models."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class RedisUsageType(str, Enum):
    """Types of Redis usage patterns."""

    CACHE_BACKEND = "cache_backend"
    SESSION_STORAGE = "session_storage"
    CELERY_BROKER = "celery_broker"
    CELERY_RESULT = "celery_result"
    CHANNELS = "channels"
    DISTRIBUTED_LOCK = "distributed_lock"
    DIRECT_CLIENT = "direct_client"
    RATE_LIMITING = "rate_limiting"
    FEATURE_FLAGS = "feature_flags"


class RedisConfig(BaseModel):
    """Redis configuration details."""

    backend: str | None = Field(None, description="Backend class name")
    location: str | None = Field(None, description="Redis connection URL")
    client_class: str | None = Field(None, description="Client class name")
    db: int | None = Field(None, description="Redis database number")
    host: str | None = Field(None, description="Redis host")
    port: int | None = Field(None, description="Redis port")
    options: dict[str, Any] = Field(default_factory=dict, description="Additional configuration options")


class RedisUsage(BaseModel):
    """Individual Redis usage record."""

    type: RedisUsageType = Field(description="Type of Redis usage")
    file: str = Field(description="File path where usage is found")
    line: int = Field(gt=0, description="Line number")
    library: str | None = Field(None, description="Library used (redis, django_redis, etc.)")
    operation: str | None = Field(None, description="Redis operation (get, set, incr, etc.)")
    key: str | None = Field(None, description="Redis key (with ... for dynamic parts)")
    statement: str | None = Field(None, description="Code statement")
    config: RedisConfig | None = Field(None, description="Configuration details")
    has_ttl: bool | None = Field(None, description="Whether TTL is specified")
    timeout: int | None = Field(None, description="Timeout value in seconds")
    pattern: str | None = Field(None, description="Usage pattern identifier")
    warning: str | None = Field(None, description="Warning message for anti-patterns")
    is_pipeline: bool = Field(False, description="Whether this is a pipeline operation")


class RedisUsageSummary(ScannerSummary):
    """Summary of Redis usage scan."""

    total_count: int = Field(ge=0, description="Total number of Redis usages found (same as total_usages)")
    total_usages: int = Field(ge=0, description="Total number of Redis usages found")
    categories: dict[str, int] = Field(
        default_factory=dict, description="Count of usages by category (cache_backend, celery_broker, etc.)"
    )
    warnings: list[str] = Field(default_factory=list, description="List of warnings about anti-patterns")


class RedisUsageOutput(ScannerOutput[dict[str, list[RedisUsage]]]):
    """Complete Redis usage scanner output."""

    summary: RedisUsageSummary = Field(description="Summary statistics")
    results: dict[str, list[RedisUsage]] = Field(default_factory=dict, description="Redis usages grouped by category")
