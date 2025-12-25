# Add Logging Scanner

## Summary

Create a new scanner to detect and analyze logging patterns across Python projects, supporting multiple logging libraries (logging, loguru, structlog, django) with intelligent logger name resolution, message extraction, and sensitive information detection.

## Motivation

### Problem

Python projects use various logging libraries with different patterns and conventions. Understanding logging behavior is crucial for:

- **Observability Analysis**: Identifying what gets logged and at what levels
- **Security Audits**: Detecting sensitive data in logs (passwords, tokens, PII)
- **Migration Planning**: Understanding logging dependencies when modernizing applications
- **Debugging Support**: Locating log statements related to specific functionality

Currently, there is no automated way to:

- Inventory all logging calls across different libraries
- Map logger names to their actual module paths
- Detect patterns of sensitive information logging
- Analyze logging message formats (string vs f-string)

### Use Cases

1. **Security Review**: Scan codebase for potential credential/PII leakage in logs
2. **Logging Migration**: Map existing logging patterns before migrating to structured logging
3. **Observability Assessment**: Understand what information is available for debugging
4. **Compliance Check**: Ensure logging practices meet security standards

## Goals

- ✅ Detect logging calls from multiple libraries (logging, loguru, structlog, django)
- ✅ Resolve logger names to actual module paths (handle `__name__`, `__main__`)
- ✅ Extract complete message strings and arguments
- ✅ Identify message format type (string interpolation, f-string, etc.)
- ✅ Flag potential sensitive information in log messages
- ✅ Organize results by file and logging library
- ✅ Support both direct and indirect logging patterns

## Non-Goals

- ❌ Analyzing log output formats or handlers
- ❌ Tracing dynamic logger creation at runtime
- ❌ Validating logging configuration files
- ❌ Rewriting or refactoring logging code

## Prior Art

Similar scanners in upcast:

- **env-var-scanner**: Detects environment variable access patterns
- **exception-handler-scanner**: Counts logging calls within exception handlers
- **http-request-scanner**: Detects HTTP request patterns across libraries

Industry tools:

- **Semgrep**: Can detect specific logging patterns with custom rules
- **Bandit**: Security-focused, checks for logging of sensitive data
- **pylint**: Has basic logging checks but limited analysis

## Success Metrics

- Accurately detect 95%+ of logging calls in test codebases
- Correctly resolve logger names including `__name__` patterns
- Zero false positives in sensitive information detection on known-safe test cases
- Process 1000+ Python files in under 10 seconds
