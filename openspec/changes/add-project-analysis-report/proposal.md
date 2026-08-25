## Why

Users can generate individual scanner outputs, but there is no current-main command that turns a directory of YAML results into one navigable Markdown project report. PR #2 contains a useful report-generation idea, but its implementation is tied to an obsolete branch and has no focused tests.

## What Changes

- Add a `generate-report` command that reads scanner YAML results and writes a Markdown project analysis report.
- Preserve scanner-specific sections when their input files are present, while tolerating missing or newer scanner fields.
- Add focused unit and CLI coverage using synthetic scan-result fixtures.
- Do not commit a large project-specific generated report from the old PR.

## Impact

- Affected specs: `project-analysis-report` (new), `cli-interface` (command documentation).
- Affected code: `upcast/report_generator.py` and `upcast/main.py`.
- Affected tests/docs: report-generator unit tests, CLI tests, and README usage documentation.
