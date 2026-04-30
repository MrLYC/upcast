"""Tests for the hybrid structural + semantic scan pipeline core."""

import importlib

import pytest


def _load_pipeline_module() -> object:
    try:
        return importlib.import_module("upcast.common.hybrid_scan_pipeline")
    except ModuleNotFoundError:
        pytest.fail("upcast.common.hybrid_scan_pipeline should exist")


class TestHybridScanPipelineContracts:
    """Tests for v1 pipeline artifacts and typed configuration contracts."""

    def test_exposes_core_pipeline_types(self) -> None:
        """Should expose the core artifact and spec types."""
        module = _load_pipeline_module()

        assert getattr(module, "PipelineSpec", None) is not None
        assert getattr(module, "LocateStage", None) is not None
        assert getattr(module, "MapStage", None) is not None
        assert getattr(module, "SemanticFilterStage", None) is not None
        assert getattr(module, "ProjectStage", None) is not None
        assert getattr(module, "StructuralCandidate", None) is not None
        assert getattr(module, "SemanticDecision", None) is not None
        assert getattr(module, "Finding", None) is not None

    def test_pipeline_spec_requires_single_round_stage_contract(self) -> None:
        """Should require locate/map/semantic_filters/project for v1 single-round execution."""
        module = _load_pipeline_module()

        LocateStage = getattr(module, "LocateStage")
        MapStage = getattr(module, "MapStage")
        ProjectStage = getattr(module, "ProjectStage")
        PipelineSpec = getattr(module, "PipelineSpec")

        locate = LocateStage(pattern="class $NAME($$$BASES): $$$BODY")
        map_stage = MapStage()
        project = ProjectStage(kind="pydantic_model")

        spec = PipelineSpec(
            name="discover-pydantic-models",
            locate=locate,
            map=map_stage,
            semantic_filters=[],
            project=project,
        )

        assert spec.name == "discover-pydantic-models"
        assert spec.locate.pattern == "class $NAME($$$BASES): $$$BODY"
        assert spec.semantic_filters == []

    def test_semantic_decision_preserves_three_state_outcomes(self) -> None:
        """Should represent confirmed, rejected, and unknown as distinct outcomes."""
        module = _load_pipeline_module()
        SemanticDecision = getattr(module, "SemanticDecision")

        confirmed = SemanticDecision(status="confirmed", reason_codes=["inherits-from-target"])
        rejected = SemanticDecision(status="rejected", reason_codes=["does-not-inherit"])
        unknown = SemanticDecision(status="unknown", reason_codes=["inference-failed"])

        assert confirmed.status == "confirmed"
        assert rejected.status == "rejected"
        assert unknown.status == "unknown"

    def test_semantic_decision_rejects_invalid_status(self) -> None:
        """Should reject statuses outside the confirmed/rejected/unknown contract."""
        module = _load_pipeline_module()
        SemanticDecision = getattr(module, "SemanticDecision")

        with pytest.raises((ValueError, TypeError), match="confirmed|rejected|unknown"):
            SemanticDecision(status="maybe", reason_codes=[])

    def test_finding_preserves_evidence_chain(self) -> None:
        """Should carry evidence needed to explain why a result was selected."""
        module = _load_pipeline_module()
        Finding = getattr(module, "Finding")

        finding = Finding(
            kind="pydantic_model",
            primary_span={"start": [1, 0], "end": [3, 0]},
            evidence_chain=["located-class", "mapped-classdef", "confirmed-inheritance"],
            fields={"class_name": "UserModel"},
        )

        assert finding.kind == "pydantic_model"
        assert finding.evidence_chain == ["located-class", "mapped-classdef", "confirmed-inheritance"]


class TestHybridScanPipelineIntegration:
    """Focused integration tests for the single-round locate/map/filter/project flow."""

    def test_run_pipeline_preserves_primary_map_failure_as_unknown(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Should preserve structural hits as unknown when the primary CST->AST map fails."""
        module = _load_pipeline_module()
        PipelineSpec = getattr(module, "PipelineSpec")
        LocateStage = getattr(module, "LocateStage")
        MapStage = getattr(module, "MapStage")
        SemanticFilterStage = getattr(module, "SemanticFilterStage")
        ProjectStage = getattr(module, "ProjectStage")
        run_pipeline = getattr(module, "run_pipeline")

        class _FakePoint:
            def __init__(self, line: int, column: int) -> None:
                self.line = line
                self.column = column

        class _FakeRange:
            def __init__(self) -> None:
                self.start = _FakePoint(0, 0)
                self.end = _FakePoint(1, 0)

        class _FakeSgNode:
            def range(self) -> _FakeRange:
                return _FakeRange()

            def text(self) -> str:
                return "class GhostModel(BaseModel):\n    pass\n"

        class _FakeMapper:
            def search_cst(self, pattern: str) -> list[_FakeSgNode]:
                assert pattern == "class $NAME($$$BASES): $$$BODY"
                return [_FakeSgNode()]

            def cst_to_ast(self, sg_node: _FakeSgNode) -> None:
                return None

            def cst_to_ast_by_matches(self, sg_node: _FakeSgNode, *var_names: str) -> dict[str, object]:
                return {}

            def cst_to_ast_by_multiple_matches(self, sg_node: _FakeSgNode, *var_names: str) -> dict[str, object]:
                return {}

        monkeypatch.setattr(module, "_build_mapper", lambda source, file_path: _FakeMapper())

        spec = PipelineSpec(
            name="preserve-map-failure",
            locate=LocateStage(pattern="class $NAME($$$BASES): $$$BODY"),
            map=MapStage(),
            semantic_filters=[
                SemanticFilterStage(
                    predicate="inherits_from",
                    target="BASES",
                    rule={"qname": {"suffix": "BaseModel"}},
                )
            ],
            project=ProjectStage(kind="pydantic_model"),
        )

        result = run_pipeline(spec=spec, source="class GhostModel(BaseModel):\n    pass\n", file_path="models.py")

        assert len(result.candidates) == 1
        assert result.candidates[0].stage_name == "map"
        assert result.decisions[0].status == "unknown"
        assert "map-failure" in result.decisions[0].reason_codes
        assert result.findings == []

    def test_run_pipeline_preserves_capture_map_failure_as_unknown(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Should preserve missing mapped captures as unknown rather than raising target errors."""
        module = _load_pipeline_module()
        PipelineSpec = getattr(module, "PipelineSpec")
        LocateStage = getattr(module, "LocateStage")
        MapStage = getattr(module, "MapStage")
        SemanticFilterStage = getattr(module, "SemanticFilterStage")
        ProjectStage = getattr(module, "ProjectStage")
        run_pipeline = getattr(module, "run_pipeline")

        real_module = importlib.import_module("astroid").parse(
            "from pydantic import BaseModel\nclass UserModel(BaseModel):\n    pass\n"
        )
        class_node = real_module.body[1]

        class _FakePoint:
            def __init__(self, line: int, column: int) -> None:
                self.line = line
                self.column = column

        class _FakeRange:
            def __init__(self) -> None:
                self.start = _FakePoint(1, 0)
                self.end = _FakePoint(2, 8)

        class _FakeSgNode:
            def range(self) -> _FakeRange:
                return _FakeRange()

            def text(self) -> str:
                return "class UserModel(BaseModel):\n    pass\n"

        class _FakeMapper:
            def search_cst(self, pattern: str) -> list[_FakeSgNode]:
                return [_FakeSgNode()]

            def cst_to_ast(self, sg_node: _FakeSgNode):
                return class_node

            def cst_to_ast_by_matches(self, sg_node: _FakeSgNode, *var_names: str) -> dict[str, object]:
                return {"NAME": class_node}

            def cst_to_ast_by_multiple_matches(self, sg_node: _FakeSgNode, *var_names: str) -> dict[str, object]:
                return {}

        monkeypatch.setattr(module, "_build_mapper", lambda source, file_path: _FakeMapper())

        spec = PipelineSpec(
            name="preserve-capture-map-failure",
            locate=LocateStage(pattern="class $NAME($$$BASES): $$$BODY"),
            map=MapStage(),
            semantic_filters=[
                SemanticFilterStage(
                    predicate="inherits_from",
                    target="BASES",
                    rule={"qname": {"suffix": "BaseModel"}},
                )
            ],
            project=ProjectStage(kind="pydantic_model"),
        )

        result = run_pipeline(spec=spec, source="class UserModel(BaseModel):\n    pass\n", file_path="models.py")

        assert result.decisions[0].status == "unknown"
        assert "capture-map-failure" in result.decisions[0].reason_codes
        assert result.findings == []

    def test_run_pipeline_confirms_rejects_and_preserves_unknown(self) -> None:
        """Should execute locate -> map -> semantic filter -> project with three-state outcomes."""
        module = _load_pipeline_module()
        PipelineSpec = getattr(module, "PipelineSpec")
        LocateStage = getattr(module, "LocateStage")
        MapStage = getattr(module, "MapStage")
        SemanticFilterStage = getattr(module, "SemanticFilterStage")
        ProjectStage = getattr(module, "ProjectStage")
        run_pipeline = getattr(module, "run_pipeline")

        source = (
            "from pydantic import BaseModel\n"
            "\n"
            "class UserModel(BaseModel):\n"
            "    id: int\n"
            "\n"
            "class PlainObject(object):\n"
            "    pass\n"
            "\n"
            "class UnknownBase(ExternalBase):\n"
            "    pass\n"
        )

        spec = PipelineSpec(
            name="discover-pydantic-models",
            locate=LocateStage(pattern="class $NAME($$$BASES): $$$BODY"),
            map=MapStage(),
            semantic_filters=[
                SemanticFilterStage(
                    predicate="inherits_from",
                    target="BASES",
                    rule={"qname": {"suffix": "BaseModel"}},
                )
            ],
            project=ProjectStage(kind="pydantic_model"),
        )

        result = run_pipeline(spec=spec, source=source, file_path="models.py")

        findings = result.findings
        decisions = {decision.facts.get("class_name"): decision for decision in result.decisions}

        assert [finding.fields["class_name"] for finding in findings] == ["UserModel"]
        assert findings[0].kind == "pydantic_model"
        assert findings[0].fields["decision_status"] == "confirmed"
        assert findings[0].evidence_chain == ["located-class", "mapped-classdef", "confirmed-inheritance"]

        assert decisions["UserModel"].status == "confirmed"
        assert decisions["PlainObject"].status == "rejected"
        assert decisions["UnknownBase"].status == "unknown"

    def test_run_pipeline_requires_matching_capture_target(self) -> None:
        """Should reject semantic filters that target captures not produced by mapping."""
        module = _load_pipeline_module()
        PipelineSpec = getattr(module, "PipelineSpec")
        LocateStage = getattr(module, "LocateStage")
        MapStage = getattr(module, "MapStage")
        SemanticFilterStage = getattr(module, "SemanticFilterStage")
        ProjectStage = getattr(module, "ProjectStage")
        run_pipeline = getattr(module, "run_pipeline")

        spec = PipelineSpec(
            name="invalid-target",
            locate=LocateStage(pattern="class $NAME($$$BASES): $$$BODY"),
            map=MapStage(),
            semantic_filters=[
                SemanticFilterStage(
                    predicate="inherits_from",
                    target="MISSING",
                    rule={"qname": {"suffix": "BaseModel"}},
                )
            ],
            project=ProjectStage(kind="pydantic_model"),
        )

        with pytest.raises(ValueError, match="Unknown semantic filter target"):
            run_pipeline(spec=spec, source="class Example(object):\n    pass\n", file_path="models.py")

    def test_run_pipeline_returns_stable_candidates_and_findings(self) -> None:
        """Should preserve source order for candidates, decisions, and findings."""
        module = _load_pipeline_module()
        PipelineSpec = getattr(module, "PipelineSpec")
        LocateStage = getattr(module, "LocateStage")
        MapStage = getattr(module, "MapStage")
        SemanticFilterStage = getattr(module, "SemanticFilterStage")
        ProjectStage = getattr(module, "ProjectStage")
        run_pipeline = getattr(module, "run_pipeline")

        source = (
            "from pydantic import BaseModel\n"
            "class FirstModel(BaseModel):\n    pass\n"
            "class SecondModel(BaseModel):\n    pass\n"
        )

        spec = PipelineSpec(
            name="ordered-models",
            locate=LocateStage(pattern="class $NAME($$$BASES): $$$BODY"),
            map=MapStage(),
            semantic_filters=[
                SemanticFilterStage(
                    predicate="inherits_from",
                    target="BASES",
                    rule={"qname": {"suffix": "BaseModel"}},
                )
            ],
            project=ProjectStage(kind="pydantic_model"),
        )

        result = run_pipeline(spec=spec, source=source, file_path="models.py")

        assert [candidate.captures["NAME"].name for candidate in result.candidates] == ["FirstModel", "SecondModel"]
        assert [decision.facts["class_name"] for decision in result.decisions] == ["FirstModel", "SecondModel"]
        assert [finding.fields["class_name"] for finding in result.findings] == ["FirstModel", "SecondModel"]


class TestHybridScanPipelineAcceptance:
    """Acceptance tests for the initial Pydantic model discovery use case."""

    def test_common_package_exposes_pydantic_discovery_pipeline_api(self) -> None:
        """Should expose the single-round pipeline API from upcast.common."""
        common = importlib.import_module("upcast.common")

        LocateStage = getattr(common, "LocateStage")
        MapStage = getattr(common, "MapStage")
        SemanticFilterStage = getattr(common, "SemanticFilterStage")
        ProjectStage = getattr(common, "ProjectStage")
        PipelineSpec = getattr(common, "PipelineSpec")
        run_pipeline = getattr(common, "run_pipeline")
        PipelineRunResult = getattr(common, "PipelineRunResult")

        source = (
            "from pydantic import BaseModel\n"
            "class UserModel(BaseModel):\n    id: int\n"
            "class PlainObject(object):\n    pass\n"
        )

        spec = PipelineSpec(
            name="discover-pydantic-models",
            locate=LocateStage(pattern="class $NAME($$$BASES): $$$BODY"),
            map=MapStage(),
            semantic_filters=[
                SemanticFilterStage(
                    predicate="inherits_from",
                    target="BASES",
                    rule={"qname": {"suffix": "BaseModel"}},
                )
            ],
            project=ProjectStage(kind="pydantic_model"),
        )

        result = run_pipeline(spec=spec, source=source, file_path="models.py")

        assert isinstance(result, PipelineRunResult)
        assert [finding.fields["class_name"] for finding in result.findings] == ["UserModel"]
        assert result.findings[0].fields["decision_status"] == "confirmed"
