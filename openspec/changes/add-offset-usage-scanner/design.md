## Context

The report is a source-level inventory of code paths that can produce SQL offset pagination. It must work when Django and DRF are not installed, must preserve source expressions for review, and must not claim that a static match proves a runtime query plan.

## Goals / Non-Goals

- Goals: find common Django ORM/DRF offset patterns, expose offset/limit/page evidence, and identify dynamic values that need runtime review.
- Goals: reuse `BaseScanner`, the shared Pydantic output models, file filtering, and `run_scanner_cli`.
- Non-goals: execute Django setup, compile SQL, inspect database indexes or query plans, estimate table sizes, or recommend a specific keyset/cursor schema.
- Non-goals: report cursor pagination or ordinary Python list/tuple slicing as offset findings.

## Decisions

- Use import-aware matching for Django and DRF symbols, with explicit method-chain evidence for QuerySet expressions. A bare `Paginator` or arbitrary `.page()` call is not enough for a confirmed framework finding.
- Treat a QuerySet subscript with a non-empty lower bound as `queryset_slice`. Preserve the lower and upper slice expressions; classify a literal zero lower bound separately because it is a LIMIT-only boundary rather than a costly non-zero offset.
- Represent Django `Paginator` and DRF page-number pagination as `indirect_pagination`: the page/page-size values imply an offset at runtime even if source code does not spell out `OFFSET`.
- Detect SQL text through safe static string inference. Literal SQL is hardcoded; concatenated/f-string SQL with dynamic portions is reported with a dynamic source kind. Do not parse arbitrary SQL beyond identifying `LIMIT` and `OFFSET` tokens.
- Use deterministic ordering by relative file path, source line, column, and pattern. The output carries a warning that static findings require runtime query-plan validation.

## Risks / Trade-offs

- QuerySet type inference is necessarily conservative. The detector may miss custom managers or dynamic aliases, but it should avoid treating ordinary collection slicing as ORM pagination.
- A configured default DRF paginator can affect many views without a local pagination declaration. Configuration findings will identify the setting and remain separate from per-view usage findings.
- SQL text may contain sensitive literals unrelated to pagination. Statements and SQL expressions should be redacted using the same conservative policy used by other source-reporting scanners where applicable.
