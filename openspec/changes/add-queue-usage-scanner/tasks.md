## 1. Specification and scope

- [x] 1.1 Define supported queue categories, parameter fields, and three-state hardcoding semantics.
- [x] 1.2 Validate this change with `openspec validate add-queue-usage-scanner --strict`.

## 2. Typed output and scanner behavior

- [x] 2.1 Add failing model tests for queue parameters, usage records, summary counts, and output grouping.
- [x] 2.2 Add failing scanner tests for in-process queues, task queues, Redis, Kafka, and RabbitMQ/Kombu.
- [x] 2.3 Implement the Pydantic models and AST scanner with deterministic ordering and redaction.
- [x] 2.4 Add edge-case tests for aliases, dynamic/config values, unresolved expressions, and unsupported same-name APIs.

## 3. CLI integration

- [x] 3.1 Add failing CLI tests for YAML stdout, JSON file output, filters, and help text.
- [x] 3.2 Register `scan-queue-usage` and make the CLI tests pass.

## 4. Documentation and verification

- [x] 4.1 Add `docs/scanners/queue-usage.md` with supported APIs, output fields, examples, and static/runtime limits.
- [x] 4.2 Export the new models/scanner according to project conventions.
- [x] 4.3 Run focused tests, full pytest, lint/type checks for changed files, and strict OpenSpec validation.
