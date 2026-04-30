"""Tests for the astroid pattern matcher."""

import importlib

import astroid
import pytest


def _load_matcher_api() -> tuple[object, object]:
    try:
        module = importlib.import_module("upcast.common.astroid_matcher")
    except ModuleNotFoundError:
        pytest.fail("upcast.common.astroid_matcher should exist")

    match = getattr(module, "match", None)
    find_matches = getattr(module, "find_matches", None)

    assert callable(match), "match() should be defined"
    assert callable(find_matches), "find_matches() should be defined"

    return match, find_matches


def _matched_node(result: object) -> object:
    node = getattr(result, "node", None)
    if node is not None:
        return node
    return getattr(result, "matched_node", None)


class TestAstroidMatcher:
    """Tests for astroid matcher API and inference-aware predicates."""

    def test_match_matches_capture_with_builtin_type_constraint(self) -> None:
        """Should match when capture infers to the requested builtin type."""
        match, _ = _load_matcher_api()
        node = astroid.parse('value = "hello"').body[0].value

        result = match(node, "$VALUE", rule={"captures": {"VALUE": {"builtin_type": "str"}}})

        assert result is not None
        assert _matched_node(result) is node
        assert result.captures["VALUE"] is node

    def test_match_rejects_capture_with_mismatched_builtin_type(self) -> None:
        """Should reject matches when builtin type constraint does not hold."""
        match, _ = _load_matcher_api()
        node = astroid.parse("value = 42").body[0].value

        result = match(node, "$VALUE", rule={"captures": {"VALUE": {"builtin_type": "str"}}})

        assert result is None

    def test_match_checks_inferable_constraint(self) -> None:
        """Should allow inference-aware constraints on captures."""
        match, _ = _load_matcher_api()
        inferable_node = astroid.parse("value = 1 + 2").body[0].value
        uninferable_node = astroid.parse("value = unknown_func()").body[0].value

        inferable_result = match(
            inferable_node,
            "$VALUE",
            rule={"captures": {"VALUE": {"inferable": True}}},
        )
        uninferable_result = match(
            uninferable_node,
            "$VALUE",
            rule={"captures": {"VALUE": {"inferable": True}}},
        )

        assert inferable_result is not None
        assert inferable_result.captures["VALUE"] is inferable_node
        assert uninferable_result is None

    def test_find_matches_collects_nodes_matching_builtin_type(self) -> None:
        """Should find all nodes whose capture satisfies builtin type constraints."""
        _, find_matches = _load_matcher_api()
        module = astroid.parse('["alpha"]\n2\n["beta"]\n')

        results = find_matches(
            module,
            "$VALUE",
            rule={"captures": {"VALUE": {"builtin_type": "str"}}},
        )

        assert [result.captures["VALUE"].value for result in results] == ["alpha", "beta"]

    def test_match_supports_qname_suffix_on_specific_node(self) -> None:
        """Should match a specific node when its inferred qname satisfies the rule."""
        match, _ = _load_matcher_api()
        module = astroid.parse('from pathlib import Path\nPath("demo")\nprint("demo")\n')
        path_call = module.body[1].value
        print_call = module.body[2].value

        path_result = match(
            path_call,
            "$VALUE",
            rule={"captures": {"VALUE": {"qname": {"suffix": "Path"}}}},
        )
        print_result = match(
            print_call,
            "$VALUE",
            rule={"captures": {"VALUE": {"qname": {"suffix": "Path"}}}},
        )

        assert path_result is not None
        assert path_result.captures["VALUE"] is path_call
        assert print_result is None

    def test_match_supports_not_rule(self) -> None:
        """Should reject a match when the nested not-rule matches."""
        match, _ = _load_matcher_api()
        node = astroid.parse("value = 42").body[0].value

        result = match(
            node,
            "$VALUE",
            rule={"not": {"captures": {"VALUE": {"builtin_type": "int"}}}},
        )

        assert result is None

    def test_match_filters_by_has_subpattern(self) -> None:
        """Should keep only nodes that contain a matching child subpattern."""
        match, _ = _load_matcher_api()
        module = astroid.parse('print("demo")\nprint(42)\n')
        string_call = module.body[0].value
        int_call = module.body[1].value

        string_result = match(
            string_call,
            "$VALUE",
            rule={
                "has": {
                    "pattern": "$ARG",
                    "rule": {"captures": {"ARG": {"builtin_type": "str"}}},
                }
            },
        )
        int_result = match(
            int_call,
            "$VALUE",
            rule={
                "has": {
                    "pattern": "$ARG",
                    "rule": {"captures": {"ARG": {"builtin_type": "str"}}},
                }
            },
        )

        assert string_result is not None
        assert string_result.captures["VALUE"] is string_call
        assert int_result is None

    def test_match_supports_inferable_false_constraint(self) -> None:
        """Should match only nodes that fail inference when inferable is false."""
        match, _ = _load_matcher_api()
        inferable_node = astroid.parse("value = 1 + 2").body[0].value
        uninferable_node = astroid.parse("value = unknown_func()").body[0].value

        inferable_result = match(
            inferable_node,
            "$VALUE",
            rule={"captures": {"VALUE": {"inferable": False}}},
        )
        uninferable_result = match(
            uninferable_node,
            "$VALUE",
            rule={"captures": {"VALUE": {"inferable": False}}},
        )

        assert inferable_result is None
        assert uninferable_result is not None
        assert uninferable_result.captures["VALUE"] is uninferable_node

    def test_match_raises_for_unsupported_pattern_shape(self) -> None:
        """Should reject patterns outside the capture-only v1 contract."""
        match, _ = _load_matcher_api()
        node = astroid.parse('print("demo")').body[0].value

        with pytest.raises(ValueError, match="capture-only"):
            match(node, "print($VALUE)")

    def test_match_raises_for_unknown_rule_key(self) -> None:
        """Should reject unknown rule keys instead of silently ignoring them."""
        match, _ = _load_matcher_api()
        node = astroid.parse("value = 42").body[0].value

        with pytest.raises(ValueError, match="Unknown rule key"):
            match(node, "$VALUE", rule={"capturez": {"VALUE": {"builtin_type": "int"}}})

    def test_match_raises_for_unknown_predicate_key(self) -> None:
        """Should reject unknown predicate keys instead of silently matching."""
        match, _ = _load_matcher_api()
        node = astroid.parse('value = "hello"').body[0].value

        with pytest.raises(ValueError, match="Unknown predicate key"):
            match(node, "$VALUE", rule={"captures": {"VALUE": {"builtin_typo": "str"}}})

    def test_common_package_exports_matcher_api(self) -> None:
        """Should export matcher API from upcast.common."""
        common = importlib.import_module("upcast.common")

        assert getattr(common, "match", None) is not None
        assert getattr(common, "find_matches", None) is not None
        assert getattr(common, "MatchResult", None) is not None
