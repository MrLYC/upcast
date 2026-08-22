## Context

The requested report is source inventory, not runtime queue monitoring. The scanner must work when queue dependencies are not installed and must not execute application configuration or connect to brokers.

## Goals / Non-Goals

- Goals: identify common Python queue APIs, preserve source expressions, infer literal/static values where safe, and expose per-parameter hardcoding status.
- Goals: use the existing `BaseScanner`, Pydantic output models, and `run_scanner_cli` conventions.
- Non-goals: measure queue depth, lag, throughput, latency, consumer health, or broker state; perform general call-graph analysis; resolve arbitrary framework configuration across files.

## Decisions

- Use import-aware qualified names rather than matching bare names alone. This keeps `Queue()` from an unrelated library out of confirmed findings.
- Group findings under `in_process`, `task_queue`, `redis`, `kafka`, and `rabbitmq`. Store the concrete framework separately so Celery/RQ/Dramatiq/Huey and Kafka client variants remain distinguishable.
- Represent constructor/configuration and enqueue/publish/consume calls as individual findings. `parameters` contains the relevant positional/keyword arguments with their source expression and static-analysis status.
- Treat literals and resolvable literal constants as `hardcoded: true`; environment/config/function inputs as `false`; unresolved or mixed expressions as `unknown`. The status is parameter-level, not a single finding-wide boolean.
- Do not expose literal values for obvious credential-bearing parameters or URLs containing userinfo. Keep a redacted expression marker instead.

## Risks / Trade-offs

- Static import resolution is conservative and may miss dynamically imported or aliased framework objects. The output preserves `unknown` rather than guessing.
- Framework APIs evolve. The initial detector tables are intentionally explicit and can be extended without changing the output contract.
- A source statement can still contain sensitive text outside a detected parameter. Documentation will describe this as a source-reporting risk and users can choose an output destination accordingly.
