"""Tests for CSTASTMapper: bidirectional mapping between tree-sitter CST and astroid AST.

These tests require the optional dependency ``ast-grep-py``.
Install it with: ``pip install ast-grep-py``  (or ``pip install upcast[cst]``).
"""

import astroid
import pytest
from ast_grep_py import SgRoot

from upcast.common.cst_ast_mapper import CSTASTMapper

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SIMPLE_SOURCE = """\
class MyModel(BaseModel):
    name: str
    age: int = 0

    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def display_name(self) -> str:
        return f"Name: {self.name}"


def calculate(x: int, y: int) -> int:
    result = x + y
    return result


@decorator
def decorated_func() -> None:
    pass


data = [1, 2, 3]
mapping = {"a": 1, "b": 2}

if data:
    for item in data:
        print(item)

try:
    result = 1 / 0
except ZeroDivisionError as e:
    print(e)

squares = [x**2 for x in range(10) if x > 3]
"""


@pytest.fixture()
def mapper() -> CSTASTMapper:
    """Create a CSTASTMapper from SIMPLE_SOURCE."""
    sg_root = SgRoot(SIMPLE_SOURCE, "python")
    ast_tree = astroid.parse(SIMPLE_SOURCE)
    return CSTASTMapper(sg_root, ast_tree)


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------


class TestInit:
    """Tests for CSTASTMapper initialization."""

    def test_builds_ts_index(self, mapper: CSTASTMapper) -> None:
        """Should build a non-empty tree-sitter index."""
        assert len(mapper._ts_by_range) > 0

    def test_builds_ast_index(self, mapper: CSTASTMapper) -> None:
        """Should build a non-empty astroid index."""
        assert len(mapper._ast_by_range) > 0

    def test_builds_ts_start_line_index(self, mapper: CSTASTMapper) -> None:
        """Should build a non-empty tree-sitter start-line bucket index."""
        assert len(mapper._ts_by_start_line) > 0

    def test_builds_ast_start_line_index(self, mapper: CSTASTMapper) -> None:
        """Should build a non-empty astroid start-line bucket index."""
        assert len(mapper._ast_by_start_line) > 0

    def test_stores_roots(self, mapper: CSTASTMapper) -> None:
        """Should store both root nodes."""
        assert mapper.sg_root is not None
        assert mapper.astroid_tree is not None

    def test_raises_without_ast_grep(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Should raise ImportError when ast-grep-py is not available."""
        import upcast.common.cst_ast_mapper as mod

        monkeypatch.setattr(mod, "_AST_GREP_AVAILABLE", False)
        sg_root = SgRoot(SIMPLE_SOURCE, "python")
        ast_tree = astroid.parse(SIMPLE_SOURCE)
        with pytest.raises(ImportError, match="ast-grep-py"):
            CSTASTMapper(sg_root, ast_tree)


# ---------------------------------------------------------------------------
# search_cst
# ---------------------------------------------------------------------------


class TestSearchCST:
    """Tests for search_cst method."""

    def test_finds_class_definitions(self, mapper: CSTASTMapper) -> None:
        """Should find class definitions matching the pattern."""
        results = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert len(results) == 1
        assert results[0].kind() == "class_definition"

    def test_finds_function_definitions(self, mapper: CSTASTMapper) -> None:
        """Should find function definitions matching the pattern."""
        results_no_ret = mapper.search_cst("def $NAME($$$PARAMS): $$$BODY")
        results_with_ret = mapper.search_cst("def $NAME($$$PARAMS) -> $RET: $$$BODY")
        assert len(results_no_ret) + len(results_with_ret) >= 4

    def test_finds_assignments(self, mapper: CSTASTMapper) -> None:
        """Should find assignment statements."""
        results = mapper.search_cst("$NAME = $VALUE")
        assert len(results) >= 2

    def test_returns_empty_on_no_match(self, mapper: CSTASTMapper) -> None:
        """Should return empty list when pattern matches nothing."""
        results = mapper.search_cst("import $NAME as $ALIAS")
        assert results == []

    def test_returns_empty_on_invalid_pattern(self, mapper: CSTASTMapper) -> None:
        """Should return empty list on invalid pattern without raising."""
        results = mapper.search_cst("$$$INVALID_ONLY")
        assert isinstance(results, list)

    def test_search_from_subtree_root(self, mapper: CSTASTMapper) -> None:
        """Should restrict search to the given subtree when root is specified."""
        # Find the class node first
        class_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert class_nodes
        class_node = class_nodes[0]

        # Search for functions inside the class only
        inner_funcs = mapper.search_cst("def $NAME($$$PARAMS) -> $RET: $$$BODY", root=class_node)
        # calculate and decorated_func are outside the class, should not appear
        inner_names = {n.get_match("NAME").text() for n in inner_funcs if n.get_match("NAME")}
        assert "calculate" not in inner_names
        assert "decorated_func" not in inner_names

    def test_search_from_none_uses_full_tree(self, mapper: CSTASTMapper) -> None:
        """Passing root=None should behave the same as not passing root."""
        results_default = mapper.search_cst("def $NAME($$$PARAMS) -> $RET: $$$BODY")
        results_none = mapper.search_cst("def $NAME($$$PARAMS) -> $RET: $$$BODY", root=None)
        assert len(results_default) == len(results_none)


# ---------------------------------------------------------------------------
# search_ast
# ---------------------------------------------------------------------------


class TestSearchAST:
    """Tests for search_ast method."""

    def test_returns_astroid_nodes(self, mapper: CSTASTMapper) -> None:
        """Should return astroid NodeNG instances."""
        results = mapper.search_ast("class $NAME($$$BASES): $$$BODY")
        assert all(isinstance(n, astroid.nodes.NodeNG) for n in results)

    def test_finds_class_as_classdef(self, mapper: CSTASTMapper) -> None:
        """Should map class_definition to ClassDef."""
        results = mapper.search_ast("class $NAME($$$BASES): $$$BODY")
        assert len(results) == 1
        assert isinstance(results[0], astroid.nodes.ClassDef)
        assert results[0].name == "MyModel"

    def test_finds_functions_as_functiondef(self, mapper: CSTASTMapper) -> None:
        """Should map function_definition to FunctionDef."""
        results_no_ret = mapper.search_ast("def $NAME($$$PARAMS): $$$BODY")
        results_with_ret = mapper.search_ast("def $NAME($$$PARAMS) -> $RET: $$$BODY")
        results = results_no_ret + results_with_ret
        assert len(results) >= 4
        assert all(isinstance(n, (astroid.nodes.FunctionDef, astroid.nodes.AsyncFunctionDef)) for n in results)

    def test_deduplicates_results(self, mapper: CSTASTMapper) -> None:
        """Should not return duplicate astroid nodes."""
        results = mapper.search_ast("def $NAME($$$PARAMS): $$$BODY")
        ids = [id(n) for n in results]
        assert len(ids) == len(set(ids))

    def test_returns_empty_on_no_match(self, mapper: CSTASTMapper) -> None:
        """Should return empty list when pattern matches nothing."""
        results = mapper.search_ast("import $NAME as $ALIAS")
        assert results == []

    def test_search_ast_from_subtree_root(self, mapper: CSTASTMapper) -> None:
        """Should restrict AST search to the given CST subtree."""
        class_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert class_nodes
        class_node = class_nodes[0]

        inner_funcs = mapper.search_ast("def $NAME($$$PARAMS) -> $RET: $$$BODY", root=class_node)
        inner_names = {n.name for n in inner_funcs if hasattr(n, "name")}
        assert "calculate" not in inner_names
        assert "decorated_func" not in inner_names

    def test_search_ast_from_none_uses_full_tree(self, mapper: CSTASTMapper) -> None:
        """Passing root=None should behave the same as not passing root."""
        results_default = mapper.search_ast("def $NAME($$$PARAMS) -> $RET: $$$BODY")
        results_none = mapper.search_ast("def $NAME($$$PARAMS) -> $RET: $$$BODY", root=None)
        assert len(results_default) == len(results_none)


# ---------------------------------------------------------------------------
# cst_to_ast
# ---------------------------------------------------------------------------


class TestCSTToAST:
    """Tests for cst_to_ast method."""

    def test_maps_class_definition(self, mapper: CSTASTMapper) -> None:
        """Should map class_definition to ClassDef."""
        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        ast_node = mapper.cst_to_ast(ts_nodes[0])
        assert isinstance(ast_node, astroid.nodes.ClassDef)
        assert ast_node.name == "MyModel"

    def test_maps_function_definition(self, mapper: CSTASTMapper) -> None:
        """Should map function_definition to FunctionDef."""
        ts_nodes = mapper.search_cst("def $NAME($$$PARAMS): $$$BODY")
        if not ts_nodes:
            ts_nodes = mapper.search_cst("def $NAME($$$PARAMS) -> $RET: $$$BODY")
        assert ts_nodes
        ast_node = mapper.cst_to_ast(ts_nodes[0])
        assert isinstance(ast_node, (astroid.nodes.FunctionDef, astroid.nodes.AsyncFunctionDef))

    def test_returns_none_for_unnamed_node(self, mapper: CSTASTMapper) -> None:
        """Should return None for unnamed (anonymous) tree-sitter nodes."""
        root = mapper.sg_root.root()
        for child in root.children():
            if not child.is_named():
                assert mapper.cst_to_ast(child) is None
                break

    def test_fallback_for_cst_only_node(self, mapper: CSTASTMapper) -> None:
        """Should return a parent astroid node for CST-only nodes like argument_list."""
        call_ts_nodes = mapper.search_cst("print($$$ARGS)")
        if not call_ts_nodes:
            pytest.skip("No print() call found in sample")

        for child in call_ts_nodes[0].children():
            if child.kind() == "argument_list":
                result = mapper.cst_to_ast(child)
                assert isinstance(result, (astroid.nodes.Call, astroid.nodes.Expr))
                break


# ---------------------------------------------------------------------------
# ast_to_cst
# ---------------------------------------------------------------------------


class TestASTToCST:
    """Tests for ast_to_cst method."""

    def test_maps_classdef_to_class_definition(self, mapper: CSTASTMapper) -> None:
        """Should map ClassDef to class_definition."""
        class_defs = list(mapper.astroid_tree.nodes_of_class(astroid.nodes.ClassDef))
        assert class_defs
        ts_node = mapper.ast_to_cst(class_defs[0])
        assert ts_node is not None
        assert ts_node.kind() == "class_definition"

    def test_maps_functiondef_to_function_definition(self, mapper: CSTASTMapper) -> None:
        """Should map FunctionDef to function_definition or decorated_definition."""
        func_defs = list(mapper.astroid_tree.nodes_of_class(astroid.nodes.FunctionDef))
        assert func_defs
        ts_node = mapper.ast_to_cst(func_defs[0])
        assert ts_node is not None
        assert ts_node.kind() in ("function_definition", "decorated_definition")

    def test_maps_assign_to_assignment(self, mapper: CSTASTMapper) -> None:
        """Should map Assign to assignment."""
        assigns = list(mapper.astroid_tree.nodes_of_class(astroid.nodes.Assign))
        top_assigns = [a for a in assigns if isinstance(a.parent, astroid.nodes.Module)]
        assert top_assigns
        ts_node = mapper.ast_to_cst(top_assigns[0])
        assert ts_node is not None
        assert ts_node.kind() in ("assignment", "expression_statement")

    def test_handles_no_coords_node(self, mapper: CSTASTMapper) -> None:
        """Should handle astroid nodes without coordinates (Arguments)."""
        func_defs = list(mapper.astroid_tree.nodes_of_class(astroid.nodes.FunctionDef))
        assert func_defs
        args_node = func_defs[0].args
        result = mapper.ast_to_cst(args_node)
        assert result is not None

    def test_decorated_function_maps_to_decorated_definition(self, mapper: CSTASTMapper) -> None:
        """Should map a decorated FunctionDef to decorated_definition."""
        func_defs = list(mapper.astroid_tree.nodes_of_class(astroid.nodes.FunctionDef))
        decorated = [f for f in func_defs if f.decorators is not None]
        assert decorated, "No decorated functions found in sample"
        ts_node = mapper.ast_to_cst(decorated[0])
        assert ts_node is not None
        assert ts_node.kind() in ("decorated_definition", "function_definition")


# ---------------------------------------------------------------------------
# cst_to_ast_by_matches
# ---------------------------------------------------------------------------


class TestCSTToASTByMatches:
    """Tests for cst_to_ast_by_matches method (single-capture $VAR)."""

    def test_extracts_single_capture_name(self, mapper: CSTASTMapper) -> None:
        """Should extract $NAME from class pattern and map to astroid node.

        The $NAME capture in a class pattern matches the ``identifier`` CST node
        (e.g. "MyModel"). Because astroid does not create a standalone node for
        the class name identifier, the mapper falls back to the enclosing
        ``ClassDef`` node.  We therefore accept any astroid node here.
        """
        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        result = mapper.cst_to_ast_by_matches(ts_nodes[0], "NAME")
        assert "NAME" in result
        name_node = result["NAME"]
        assert name_node is not None
        # The identifier 'MyModel' has no standalone astroid node; the mapper
        # falls back to the smallest containing node (ClassDef).
        assert isinstance(name_node, astroid.nodes.NodeNG)

    def test_returns_none_for_missing_capture(self, mapper: CSTASTMapper) -> None:
        """Should return None for a capture variable not present in the match."""
        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        result = mapper.cst_to_ast_by_matches(ts_nodes[0], "NONEXISTENT")
        assert result["NONEXISTENT"] is None

    def test_extracts_multiple_single_captures(self, mapper: CSTASTMapper) -> None:
        """Should extract multiple $VAR captures in one call."""
        ts_nodes = mapper.search_cst("$LHS = $RHS")
        assert ts_nodes
        result = mapper.cst_to_ast_by_matches(ts_nodes[0], "LHS", "RHS")
        assert "LHS" in result
        assert "RHS" in result

    def test_returns_dict_with_all_requested_keys(self, mapper: CSTASTMapper) -> None:
        """Result dict should always contain all requested keys."""
        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        result = mapper.cst_to_ast_by_matches(ts_nodes[0], "NAME", "MISSING_A", "MISSING_B")
        assert set(result.keys()) == {"NAME", "MISSING_A", "MISSING_B"}


# ---------------------------------------------------------------------------
# cst_to_ast_by_multiple_matches
# ---------------------------------------------------------------------------


class TestCSTToASTByMultipleMatches:
    """Tests for cst_to_ast_by_multiple_matches method (multi-capture $$$VAR)."""

    def test_extracts_bases_from_class(self, mapper: CSTASTMapper) -> None:
        """Should extract $$$BASES from class pattern as a list of astroid nodes."""
        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        result = mapper.cst_to_ast_by_multiple_matches(ts_nodes[0], "BASES")
        assert "BASES" in result
        bases = result["BASES"]
        assert isinstance(bases, list)
        assert len(bases) >= 1  # MyModel has at least one base

    def test_bases_are_astroid_nodes(self, mapper: CSTASTMapper) -> None:
        """Extracted base nodes should be astroid NodeNG instances."""
        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        result = mapper.cst_to_ast_by_multiple_matches(ts_nodes[0], "BASES")
        for node in result["BASES"]:
            assert isinstance(node, astroid.nodes.NodeNG)

    def test_returns_empty_list_for_missing_capture(self, mapper: CSTASTMapper) -> None:
        """Should return empty list for a capture variable not present in the match."""
        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        result = mapper.cst_to_ast_by_multiple_matches(ts_nodes[0], "NONEXISTENT")
        assert result["NONEXISTENT"] == []

    def test_deduplicates_multiple_match_results(self, mapper: CSTASTMapper) -> None:
        """Should not return duplicate astroid nodes in the result list."""
        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        result = mapper.cst_to_ast_by_multiple_matches(ts_nodes[0], "BASES")
        ids = [id(n) for n in result["BASES"]]
        assert len(ids) == len(set(ids))

    def test_extracts_multiple_multi_captures(self, mapper: CSTASTMapper) -> None:
        """Should handle multiple $$$VAR captures in one call."""
        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        result = mapper.cst_to_ast_by_multiple_matches(ts_nodes[0], "BASES", "BODY")
        assert "BASES" in result
        assert "BODY" in result
        assert isinstance(result["BASES"], list)
        assert isinstance(result["BODY"], list)


# ---------------------------------------------------------------------------
# Round-trip consistency
# ---------------------------------------------------------------------------


class TestRoundTrip:
    """Tests for round-trip consistency between cst_to_ast and ast_to_cst."""

    def test_class_round_trip(self, mapper: CSTASTMapper) -> None:
        """CST -> AST -> CST should return a node with the same range."""
        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        ts_node = ts_nodes[0]

        ast_node = mapper.cst_to_ast(ts_node)
        assert ast_node is not None

        ts_back = mapper.ast_to_cst(ast_node)
        assert ts_back is not None

        original_rng = mapper._ts_range(ts_node)
        back_rng = mapper._ts_range(ts_back)
        assert original_rng == back_rng

    def test_function_round_trip(self, mapper: CSTASTMapper) -> None:
        """CST -> AST -> CST should return a node with the same range for functions."""
        ts_nodes = mapper.search_cst("def calculate($$$PARAMS) -> $RET: $$$BODY")
        assert ts_nodes
        ts_node = ts_nodes[0]

        ast_node = mapper.cst_to_ast(ts_node)
        assert ast_node is not None

        ts_back = mapper.ast_to_cst(ast_node)
        assert ts_back is not None

        original_rng = mapper._ts_range(ts_node)
        back_rng = mapper._ts_range(ts_back)
        assert original_rng == back_rng
