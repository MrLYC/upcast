## 1. Specification and scope

- [x] 1.1 Define supported offset-producing patterns, exclusions, and parameter evidence semantics.
- [x] 1.2 Validate this change with `openspec validate add-offset-usage-scanner --strict`.

## 2. Typed output and scanner behavior

- [x] 2.1 Add failing model tests for parameter evidence, usage records, summary counts, and output grouping.
- [x] 2.2 Add failing scanner tests for QuerySet slices, Django Paginator, DRF pagination, raw SQL, aliases, dynamic expressions, and exclusions.
- [x] 2.3 Implement the Pydantic models and static AST scanner with deterministic ordering.
- [x] 2.4 Add edge-case tests for zero offsets, open-ended slices, configuration defaults, ordinary list slices, and cursor pagination.

## 3. CLI integration

- [x] 3.1 Add failing CLI tests for YAML stdout, JSON output, filters, and help text.
- [x] 3.2 Register `scan-offset-usage` and make the CLI tests pass.

## 4. Documentation and verification

- [x] 4.1 Add scanner documentation with supported patterns, output fields, examples, and static-analysis limits.
- [x] 4.2 Export the new models and scanner according to project conventions.
- [x] 4.3 Run focused tests, full pytest, lint/type checks for changed files, and strict OpenSpec validation.
