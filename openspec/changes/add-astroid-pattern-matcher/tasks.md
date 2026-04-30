## 1. Specification

- [ ] 1.1 Review `openspec/specs/common-utilities/spec.md` and confirm the matcher belongs under common utilities.
- [ ] 1.2 Review `openspec/changes/add-astroid-pattern-matcher/proposal.md` and `design.md` before starting implementation.
- [ ] 1.3 Validate `add-astroid-pattern-matcher` with `openspec validate add-astroid-pattern-matcher --strict`.
- [ ] 1.4 Wait for proposal approval before changing production code.

## 2. Test-First Implementation

- [ ] 2.1 Add failing tests in `tests/test_common/test_astroid_matcher.py` for builtin type matching.
- [ ] 2.2 Run the targeted tests and confirm they fail for the expected missing behavior.
- [ ] 2.3 Add failing tests for inferability checks and qualified-name matching.
- [ ] 2.4 Run the targeted tests and confirm they fail for the expected missing behavior.
- [ ] 2.5 Add failing tests for negative predicates and nested child subpatterns.
- [ ] 2.6 Run the targeted tests and confirm they fail for the expected missing behavior.

## 3. Minimal Matcher Implementation

- [ ] 3.1 Create `upcast/common/astroid_matcher.py` with `match()` and `find_matches()`.
- [ ] 3.2 Implement structural pattern capture for the supported v1 metavariable subset.
- [ ] 3.3 Implement rule evaluation for `inferable`, `builtin_type`, and `qname`.
- [ ] 3.4 Implement `not` and `has` semantics without moving matcher orchestration into helper modules.
- [ ] 3.5 Export the matcher API from `upcast/common/__init__.py`.

## 4. Verification and Documentation

- [ ] 4.1 Re-run `tests/test_common/test_astroid_matcher.py` and the related common utility tests until all pass.
- [ ] 4.2 Run repository validation commands required for the changed files.
- [ ] 4.3 Update `docs/type-inference.md` with matcher scope, supported predicates, and deferred features.
- [ ] 4.4 Re-run the relevant validation commands after documentation and exports are updated.
