## Why

Upcast already provides reusable astroid inference helpers and a CST/AST mapper, but it does not provide a common AST-native matcher that can combine structural patterns with semantic inference constraints. As a result, scanners repeatedly re-implement partial matching logic for inferred builtin types, qualified names, and nested semantic checks.

## What Changes

- Add a new `common-utilities` capability requirement for an astroid-powered pattern matcher.
- Define a v1 public model based on `pattern + rule`, where pattern handles structure and rule handles inference-aware predicates.
- Scope v1 to builtin type checks, inferability checks, qualified-name matching, negative predicates, and nested child subpatterns.
- Explicitly defer full ast-grep compatibility, CST-backed matching, and YAML-only rule entrypoints.

## Impact

- Affected specs: `common-utilities`
- Affected code: `upcast/common/` matcher utilities, `tests/test_common/`, and `docs/type-inference.md`
