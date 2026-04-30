## Context

Upcast now has three relevant shared pieces:

- `CSTASTMapper` for ast-grep/tree-sitter structural matching plus CST ↔ astroid bridging
- `astroid_matcher` for constrained astroid-side semantic predicates
- Existing scanners that already implement staged analysis manually

The requested refactor is not another matcher. It is a higher-level orchestration layer that lets scanners describe a reusable analysis chain without rewriting the same bridging, filtering, and evidence-shaping logic.

The user explicitly approved these v1 scope constraints:

- first users are internal scanner/core code, not external rule authors
- testing must be rigorous
- v1 should stay single-round rather than supporting arbitrary relaunch chains
- after the proving case, all scanner commands should be migrated incrementally with explicit old-vs-new output comparison before final submission

## Goals / Non-Goals

### Goals

- Introduce an internal hybrid pipeline core that composes structural locate, CST/AST mapping, semantic filtering, and result projection.
- Keep the pipeline typed and code-first so scanner authors get explicit contracts and testable components.
- Produce stable, inspectable intermediate artifacts that preserve captures, spans, evidence, and semantic status.
- Support one concrete acceptance case: discovering Pydantic models.
- Extend the proving-case core into a migration path for all scanner commands in `upcast.main:main` while preserving the public CLI and `ScannerOutput` contracts.
- Require per-command old-vs-new parity checks at the CLI boundary before a migrated command is accepted.

### Non-Goals

- No public/general-purpose rule engine in v1.
- No YAML-only or JSON-only DSL commitment in v1.
- No arbitrary multi-round or looping pipelines in v1.
- No replacement of the existing CLI/scanner architecture.
- No requirement that every scanner be rewritten into a pure `PipelineSpec`; scanner-specific aggregation/projection may remain outside the core when needed for parity.

## Decisions

### Decision: Add a higher-level hybrid pipeline orchestrator

The new core should sit above `CSTASTMapper` and `astroid_matcher`, not replace either of them. Its job is orchestration, lifecycle management, typed artifacts, and stable result shaping.

### Decision: Keep v1 pipeline single-round

The v1 execution shape is:

1. structural locate via ast-grep pattern
2. map matched CST nodes/captures to astroid nodes
3. semantic filter using astroid-aware predicates / inference helpers
4. project confirmed/unknown results into command-specific findings

This keeps the execution graph simple enough to test rigorously and leaves room for multi-round chaining in a later change.

### Decision: Use typed internal config, not public rule files

The internal API should use typed config/models (dataclass or Pydantic-style internal schema) for pipeline stages. If a declarative file format is ever needed, it should be layered on top later as serialization, not baked into the execution core.

### Decision: Standardize on three artifact types

Recommended v1 artifacts:

- `StructuralCandidate`: file path, structural span, capture spans/nodes, source snippet, rule/stage metadata
- `SemanticDecision`: `confirmed | rejected | unknown`, reason codes, resolved semantic facts, inference errors if any
- `Finding`: final result object with primary span, related spans, evidence chain, and projected fields for scanner output

### Decision: Preserve three-state semantics

Semantic verification must not collapse uncertainty into falsehood. Inference and mapping can fail for legitimate reasons, so v1 must preserve `unknown` distinctly from `rejected`.

### Decision: Mapping failures must not disappear silently

The current proving-case implementation can drop structural hits when CST-to-astroid mapping fails. For broader scanner adoption this is too weak: mapping failure must be represented explicitly as internal `unknown` evidence, even if a migrated public command chooses not to expose that unknown directly in user-facing output for parity reasons.

### Decision: Keep CLI stable and adopt scanners incrementally

The migration target is not a new command surface. Existing commands in `upcast.main:main` remain the public boundary, continue to execute through `upcast/common/cli.py::run_scanner_cli(...)`, and adopt the hybrid pipeline behind the scanner boundary.

### Decision: Compare old and new behavior per command

Each migrated scanner command must be validated against the legacy behavior at the public CLI boundary. The parity contract includes exit codes, default YAML output, JSON/file output, and command-specific option behavior. Internal pipeline artifacts are not sufficient for acceptance.

## Proposed Internal Shape

Illustrative v1 internal config model:

- `PipelineSpec`
  - `name`
  - `locate: LocateStage`
  - `map: MapStage`
  - `semantic_filters: list[SemanticFilterStage]`
  - `project: ProjectStage`

The stage contracts should be closed and typed. Examples of v1 semantic predicates include inheritance/qualified-name checks, inferability checks, builtin-type checks, and node-based semantic facts that can be backed by existing helpers.

## Testing Strategy

The agreed v1 verification depth is:

1. **Core unit tests**

   - stage config validation
   - structural candidate creation
   - CST/AST mapping behavior for captures
   - semantic predicate evaluation
   - three-state decision behavior
   - stable ordering and deduplication

2. **Focused integration tests**

   - real chain from ast-grep locate → CSTASTMapper → semantic verification
   - evidence/capture preservation across the chain

3. **One end-to-end acceptance example**

   - Pydantic model discovery from source file to final finding/output

4. **Per-command migration parity checks**
   - old vs new command comparison via `CliRunner.invoke(upcast.main:main, ...)`
   - normalized output comparison against current command contracts
   - command-specific option checks before accepting each migration wave

## Risks / Trade-offs

- Single-round v1 is intentionally narrower than the original long-term vision. It does not support iterative relaunch chains yet.
- A typed internal API is safer for v1 but less immediately flexible for external rule authors.
- Mapping and inference failures need explicit handling and logging to keep `unknown` useful rather than noisy.
- If `ast-grep-py` is unavailable, the pipeline must fail in a controlled and well-documented way rather than pretending semantic-only fallback is equivalent.
- Full scanner migration is significantly broader than the proving case; without wave sequencing and parity gates it risks changing user-visible command behavior unintentionally.
- Some scanners fit only partial adoption in v1. It is acceptable for the hybrid pipeline to handle candidate selection / semantic verification while existing scanner-specific aggregation and output shaping remain in place.

## Migration Plan

1. Expand OpenSpec scope to cover all scanner command migration, parity verification, and explicit map-failure semantics.
2. Close the `map-failure -> unknown` semantic gap in the shared pipeline before migrating more scanners.
3. Add shared adapters/projection helpers so scanners can adopt the core incrementally without replacing CLI wiring.
4. Build a comparison harness at the public CLI boundary.
5. Migrate scanner commands in waves, ordered by risk and structural fit.
6. For each migrated command, run old-vs-new parity comparison before proceeding.
7. Finish with a full integration sweep and updated docs/baselines.

## Open Questions

- Which scanners should remain partial adopters in v1 if full projection parity proves too expensive?
- Should parity baselines be stored entirely in `tests/test_cli/`, or partly refreshed through `example/scan-results/` integration snapshots?
