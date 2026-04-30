## Why

Upcast already has the building blocks for structural and semantic analysis, but scanners still compose them ad hoc. `CSTASTMapper` bridges ast-grep results into astroid nodes, `astroid_matcher` provides inference-aware predicates, and individual scanners shape their own staged pipelines. This leads to duplicated orchestration logic, inconsistent evidence handling, and no shared internal model for combining structural search with semantic verification.

## What Changes

- Add a new `common-utilities` capability requirement for a hybrid scan pipeline that composes ast-grep structural location, CST/AST mapping, astroid semantic filtering, and result projection.
- Scope v1 to an internal typed pipeline API for scanner/core usage, not a public YAML/JSON rule engine.
- Define v1 as a single-round pipeline: `locate -> map -> semantic filter -> project`.
- Standardize v1 intermediate artifacts and outcome semantics around structural candidates, semantic decisions, and shaped findings.
- Require rigorous testing through core unit tests, focused integration tests, and one end-to-end acceptance example using Pydantic model discovery.
- Extend the approved rollout beyond the proving case so every scanner command in `upcast.main:main` can adopt the hybrid pipeline incrementally without replacing the existing CLI framework.
- Require a documented migration plan that sequences scanner adoption in waves, closes the current `map-failure -> unknown` semantic gap first, and preserves public CLI/output compatibility during migration.
- Require old-vs-new comparison for every migrated scanner command at the public CLI boundary, including command-specific option behavior and normalized output comparison.

## Impact

- Affected specs: `common-utilities`, `cli-interface`, `testing-infrastructure`
- Affected code: `upcast/common/` pipeline utilities, shared models/configs, `tests/test_common/`, `tests/test_cli/`, scanner integration points under `upcast/scanners/`, parity/integration baselines under `example/scan-results/`, and documentation/plans for migration rollout
