## 1. Specification

- [ ] 1.1 Review `openspec/specs/common-utilities/spec.md` and confirm the hybrid pipeline belongs under common utilities.
- [ ] 1.2 Review `openspec/changes/add-hybrid-scan-pipeline/proposal.md` and `design.md` before implementation.
- [ ] 1.3 Validate `add-hybrid-scan-pipeline` with `openspec validate add-hybrid-scan-pipeline --strict`.
- [ ] 1.4 Wait for proposal approval before changing production code.

## 2. Risk Closure Before Broad Adoption

- [ ] 2.1 Add a failing test that proves primary CST-to-astroid map failure is preserved as internal `unknown` rather than silently dropped.
- [ ] 2.2 Add a failing test that proves capture-specific map failure preserves enough context for downstream debugging.
- [ ] 2.3 Implement the smallest pipeline change needed to preserve map/inference ambiguity without breaking current public output.
- [ ] 2.4 Re-run focused hybrid/common tests and lint after the risk closure.

## 3. Shared Migration Harness

- [ ] 3.1 Add a migration plan document under `docs/plans/` that inventories all scanner commands, migration waves, and stop/go gates.
- [ ] 3.2 Add or extend CLI-facing comparison helpers so old vs new command behavior can be compared through `upcast.main:main`.
- [ ] 3.3 Normalize parity comparisons around public output structure (`ScannerOutput`, YAML/JSON/file output) rather than internal pipeline artifacts.
- [ ] 3.4 Add one proving comparison for a migrated command before starting broad rollout.

## 4. Incremental Scanner Migration

- [ ] 4.1 Migrate low-risk scanners first, keeping CLI and output contracts stable.
- [ ] 4.2 Migrate medium-risk scanners using shared adapters/projection helpers instead of rewriting CLI wiring.
- [ ] 4.3 Migrate high-risk scanners last, only after parity harness and shared abstractions are proven.
- [ ] 4.4 Commit migrations atomically, ideally one scanner per commit plus separate shared-abstraction commits.

## 5. Verification and Documentation

- [ ] 5.1 For every migrated scanner command, compare old and new behavior at the public CLI boundary, including command-specific options.
- [ ] 5.2 Re-run affected common tests, CLI functional tests, and integration/baseline checks after each migration wave.
- [ ] 5.3 Document final scope limits: internal single-round pipeline core, incremental scanner adoption, and parity-first rollout.
- [ ] 5.4 Re-run `openspec validate add-hybrid-scan-pipeline --strict` after documentation/spec updates.
