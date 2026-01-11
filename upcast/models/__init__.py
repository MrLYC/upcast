"""Pydantic data models for all scanners.

This module provides standardized, type-safe data models for scanner outputs,
enabling both scanners and future analyzers to work with structured data.

Usage:
    from upcast.models import (
        ScannerSummary,
        ScannerOutput,
        BlockingOperation,
        ComplexityResult,
        DjangoModel,
    )

The models are organized by scanner type:
- Base: ScannerSummary, ScannerOutput
- Blocking Operations: BlockingOperation, BlockingOperationsSummary, BlockingOperationsOutput
- Concurrency: ConcurrencyUsage, ConcurrencyPatternSummary, ConcurrencyPatternOutput
- Complexity: ComplexityResult, ComplexitySummary, ComplexityOutput
- Django Models: DjangoField, DjangoModel, DjangoModelSummary, DjangoModelOutput
- Django Settings: SettingsUsage, SettingDefinition, DjangoSettingsSummary, DjangoSettings*Output
- Django URLs: UrlPattern, DjangoUrlSummary, DjangoUrlOutput
- Environment Variables: EnvVarInfo, EnvVarSummary, EnvVarOutput
- Exception Handlers: ExceptionHandler, ExceptionHandlerSummary, ExceptionHandlerOutput
- HTTP Requests: HttpRequestInfo, HttpRequestSummary, HttpRequestOutput
- Metrics: MetricInfo, PrometheusMetricSummary, PrometheusMetricOutput
- Signals: SignalInfo, SignalSummary, SignalOutput
- Unit Tests: UnitTestInfo, UnitTestSummary, UnitTestOutput
"""

# Base models
from upcast.models.base import ScannerOutput, ScannerSummary

# Blocking operations
from upcast.models.blocking_operations import (
    BlockingOperation,
    BlockingOperationsOutput,
    BlockingOperationsSummary,
)

# Complexity
from upcast.models.complexity import ComplexityOutput, ComplexityResult, ComplexitySummary

# Concurrency patterns
from upcast.models.concurrency import (
    ConcurrencyPatternOutput,
    ConcurrencyPatternSummary,
    ConcurrencyUsage,
)

# Django models
from upcast.models.django_models import (
    DjangoField,
    DjangoModel,
    DjangoModelOutput,
    DjangoModelSummary,
    DjangoRelationship,
)

# Django settings
from upcast.models.django_settings import (
    DjangoSettingsOutput,
    DjangoSettingsSummary,
    SettingDefinitionItem,
    SettingInfo,
    SettingUsageItem,
)

__all__ = [
    # Django Models
    "DjangoField",
    "DjangoModel",
    "DjangoModelOutput",
    "DjangoModelSummary",
    "DjangoRelationship",
    # Django Settings
    "DjangoSettingsOutput",
    "DjangoSettingsSummary",
    "SettingDefinitionItem",
    "SettingInfo",
    "SettingUsageItem",
    # Other scanners (add as needed)
]

# Django URLs
from upcast.models.django_urls import DjangoUrlOutput, DjangoUrlSummary, UrlModule, UrlPattern

# Environment variables
from upcast.models.env_vars import EnvVarInfo, EnvVarLocation, EnvVarOutput, EnvVarSummary

# Exception handlers
from upcast.models.exceptions import (
    ExceptionBlock,
    ExceptionHandler,
    ExceptionHandlerOutput,
    ExceptionHandlerSummary,
)

# HTTP requests
from upcast.models.http_requests import (
    HttpRequestInfo,
    HttpRequestOutput,
    HttpRequestSummary,
    HttpRequestUsage,
)

# Prometheus metrics
from upcast.models.metrics import MetricInfo, MetricUsage, PrometheusMetricOutput, PrometheusMetricSummary

# Redis usage
from upcast.models.redis_usage import (
    RedisConfig,
    RedisUsage,
    RedisUsageOutput,
    RedisUsageSummary,
    RedisUsageType,
)

# Signals
from upcast.models.signals import SignalInfo, SignalOutput, SignalSummary, SignalUsage

# Unit tests
from upcast.models.unit_tests import TargetModule, UnitTestInfo, UnitTestOutput, UnitTestSummary

__all__ = [
    # Blocking operations
    "BlockingOperation",
    "BlockingOperationsOutput",
    "BlockingOperationsSummary",
    "ComplexityOutput",
    # Complexity
    "ComplexityResult",
    "ComplexitySummary",
    "ConcurrencyPatternOutput",
    "ConcurrencyPatternSummary",
    # Concurrency
    "ConcurrencyUsage",
    # Django models
    "DjangoField",
    "DjangoModel",
    "DjangoModelOutput",
    "DjangoModelSummary",
    "DjangoRelationship",
    "DjangoSettingsOutput",
    "DjangoSettingsSummary",
    "DjangoUrlOutput",
    "DjangoUrlSummary",
    "EnvVarInfo",
    # Environment variables
    "EnvVarLocation",
    "EnvVarOutput",
    "EnvVarSummary",
    # Exception handlers
    "ExceptionBlock",
    "ExceptionHandler",
    "ExceptionHandlerOutput",
    "ExceptionHandlerSummary",
    "FinallyClause",
    "HttpRequestInfo",
    "HttpRequestOutput",
    "HttpRequestSummary",
    # HTTP requests
    "HttpRequestUsage",
    "MetricInfo",
    # Metrics
    "MetricUsage",
    "PrometheusMetricOutput",
    "PrometheusMetricSummary",
    "RedisConfig",
    "RedisUsage",
    "RedisUsageOutput",
    "RedisUsageSummary",
    "RedisUsageType",
    "ScannerOutput",
    # Base models
    "ScannerSummary",
    "SettingDefinition",
    # Django settings
    "SettingsLocation",
    "SettingsModule",
    "SettingsUsage",
    "SignalInfo",
    "SignalOutput",
    "SignalSummary",
    # Signals
    "SignalUsage",
    # Unit tests
    "TargetModule",
    "UnitTestInfo",
    "UnitTestOutput",
    "UnitTestSummary",
    "UrlModule",
    # Django URLs
    "UrlPattern",
]
