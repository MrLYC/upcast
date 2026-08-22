## Why

Upcast can already report general concurrency and Redis usage, but it does not provide one inventory of queue construction, publishing, and consuming patterns. Reviewers need to see queue-routing parameters and distinguish values fixed in source from values supplied by configuration or runtime inputs.

## What Changes

- Add a `scan-queue-usage` command with the standard scanner CLI options.
- Add a typed queue-usage output model grouped by queue category and operation.
- Detect supported in-process queues, task queues, Redis List/Stream usage, Kafka usage, and RabbitMQ/Kombu usage using static AST/import evidence.
- Report each relevant parameter as an expression, best-effort static value, source kind, and parameter-level `hardcoded` status (`true`, `false`, or `unknown`).
- Include summary counts by category/framework and hardcoding status while preserving deterministic ordering.
- Avoid importing or connecting to queue libraries during scanning; redact obvious credential-bearing parameter values and document static-analysis limits.

## Impact

- Affected specs: new `queue-usage-scanner`, plus `cli-interface`, `data-models`, and `scanner-architecture`.
- Affected code: new queue usage model/scanner, registration in `upcast/main.py`, `upcast/scanners/__init__.py`, and `upcast/models/__init__.py`.
- Affected tests/docs: dedicated scanner/model/CLI tests and `docs/scanners/queue-usage.md`.
- Compatibility: existing scanner commands and serialized output remain unchanged.
