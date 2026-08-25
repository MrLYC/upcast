## Context

PR #2 added a large Markdown report generator on an old `develop` snapshot. The current `main` branch has newer scanner output models and additional scanners, so the generator must consume the stable `summary`/`results` envelope without assuming every historical field exists.

## Goals / Non-Goals

- Goals: deterministic Markdown, useful executive summary, scanner sections for common findings, graceful partial input, and a CLI contract consistent with the project.
- Non-Goals: executing scanned projects, regenerating committed sample reports, or interpreting arbitrary scanner-specific data as facts.

## Decisions

- Load only top-level `*.yaml` files and use each filename stem as the scanner key.
- Treat missing sections and missing fields as empty data rather than failing the whole report.
- Keep the report generator independent from scanner classes so it can consume saved results.
- Escape table cells and code spans sufficiently to keep generated Markdown valid for paths and expressions.

## Risks / Trade-offs

- Scanner schemas may evolve; the report intentionally favors conservative summaries over exhaustive assumptions.
- A generic report cannot replace scanner-specific analysis; each section links its counts to the source YAML name.

## Migration Plan

1. Add failing model/loader/report tests with synthetic YAML.
2. Implement the generator and `generate-report` CLI on current `main`.
3. Verify the generator against current checked-in scan results without committing the generated artifact.
