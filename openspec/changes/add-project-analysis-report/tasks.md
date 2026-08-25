## 1. Report loading and formatting

- [x] 1.1 Add failing tests for YAML loading, missing directories, deterministic ordering, and Markdown escaping.
- [x] 1.2 Implement the report result loader and shared Markdown formatting helpers.
- [x] 1.3 Add failing tests for executive summary and scanner sections.
- [x] 1.4 Implement the supported report sections with graceful missing-field handling.

## 2. CLI and documentation

- [x] 2.1 Add failing CLI tests for stdout and `--output` behavior.
- [x] 2.2 Register `generate-report` in `upcast.main`.
- [x] 2.3 Document the command in README and CLI docs.

## 3. Verification

- [x] 3.1 Validate this OpenSpec change with `openspec validate add-project-analysis-report --strict`.
- [x] 3.2 Run focused report tests and the full test suite.
- [x] 3.3 Verify generation against current checked-in YAML without committing a generated report.
