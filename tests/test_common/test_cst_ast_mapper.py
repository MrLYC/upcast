"""Tests for CSTASTMapper: bidirectional mapping between tree-sitter CST and astroid AST."""

import pytest

try:
    import astroid
    from ast_grep_py import SgRoot

    from upcast.common.cst_ast_mapper import CSTASTMapper

    _DEPS_AVAILABLE = True
except ImportError:
    _DEPS_AVAILABLE = False

pytestmark = pytest.mark.skipif(not _DEPS_AVAILABLE, reason="ast-grep-py not installed")


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
def mapper() -> "CSTASTMapper":
    """Create a CSTASTMapper from SIMPLE_SOURCE."""
    sg_root = SgRoot(SIMPLE_SOURCE, "python")
    ast_tree = astroid.parse(SIMPLE_SOURCE)
    return CSTASTMapper(sg_root, ast_tree)


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------


class TestInit:
    """Tests for CSTASTMapper initialization."""

    def test_builds_ts_index(self, mapper: "CSTASTMapper") -> None:
        """Should build a non-empty tree-sitter index."""
        assert len(mapper._ts_by_range) > 0

    def test_builds_ast_index(self, mapper: "CSTASTMapper") -> None:
        """Should build a non-empty astroid index."""
        assert len(mapper._ast_by_range) > 0

    def test_stores_roots(self, mapper: "CSTASTMapper") -> None:
        """Should store both root nodes."""
        assert mapper.sg_root is not None
        assert mapper.astroid_tree is not None


# ---------------------------------------------------------------------------
# search_cst
# ---------------------------------------------------------------------------


class TestSearchCST:
    """Tests for search_cst method."""

    def test_finds_class_definitions(self, mapper: "CSTASTMapper") -> None:
        """Should find class definitions matching the pattern."""
        results = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert len(results) == 1
        assert results[0].kind() == "class_definition"

    def test_finds_function_definitions(self, mapper: "CSTASTMapper") -> None:
        """Should find function definitions matching the pattern."""
        # Functions without return type annotation
        results_no_ret = mapper.search_cst("def $NAME($$$PARAMS): $$$BODY")
        # Functions with return type annotation
        results_with_ret = mapper.search_cst("def $NAME($$$PARAMS) -> $RET: $$$BODY")
        # __init__, display_name, calculate, decorated_func
        assert len(results_no_ret) + len(results_with_ret) >= 4

    def test_finds_assignments(self, mapper: "CSTASTMapper") -> None:
        """Should find assignment statements."""
        results = mapper.search_cst("$NAME = $VALUE")
        assert len(results) >= 2

    def test_returns_empty_on_no_match(self, mapper: "CSTASTMapper") -> None:
        """Should return empty list when pattern matches nothing."""
        results = mapper.search_cst("import $NAME as $ALIAS")
        assert results == []

    def test_returns_empty_on_invalid_pattern(self, mapper: "CSTASTMapper") -> None:
        """Should return empty list on invalid pattern without raising."""
        results = mapper.search_cst("$$$INVALID_ONLY")
        assert isinstance(results, list)


# ---------------------------------------------------------------------------
# search_ast
# ---------------------------------------------------------------------------


class TestSearchAST:
    """Tests for search_ast method."""

    def test_returns_astroid_nodes(self, mapper: "CSTASTMapper") -> None:
        """Should return astroid NodeNG instances."""
        from astroid import nodes as anodes

        results = mapper.search_ast("class $NAME($$$BASES): $$$BODY")
        assert all(isinstance(n, anodes.NodeNG) for n in results)

    def test_finds_class_as_classdef(self, mapper: "CSTASTMapper") -> None:
        """Should map class_definition to ClassDef."""
        from astroid import nodes as anodes

        results = mapper.search_ast("class $NAME($$$BASES): $$$BODY")
        assert len(results) == 1
        assert isinstance(results[0], anodes.ClassDef)
        assert results[0].name == "MyModel"

    def test_finds_functions_as_functiondef(self, mapper: "CSTASTMapper") -> None:
        """Should map function_definition to FunctionDef."""
        from astroid import nodes as anodes

        results_no_ret = mapper.search_ast("def $NAME($$$PARAMS): $$$BODY")
        results_with_ret = mapper.search_ast("def $NAME($$$PARAMS) -> $RET: $$$BODY")
        results = results_no_ret + results_with_ret
        assert len(results) >= 4
        assert all(isinstance(n, (anodes.FunctionDef, anodes.AsyncFunctionDef)) for n in results)

    def test_deduplicates_results(self, mapper: "CSTASTMapper") -> None:
        """Should not return duplicate astroid nodes."""
        results = mapper.search_ast("def $NAME($$$PARAMS): $$$BODY")
        ids = [id(n) for n in results]
        assert len(ids) == len(set(ids))

    def test_returns_empty_on_no_match(self, mapper: "CSTASTMapper") -> None:
        """Should return empty list when pattern matches nothing."""
        results = mapper.search_ast("import $NAME as $ALIAS")
        assert results == []


# ---------------------------------------------------------------------------
# cst_to_ast
# ---------------------------------------------------------------------------


class TestCSTToAST:
    """Tests for cst_to_ast method."""

    def test_maps_class_definition(self, mapper: "CSTASTMapper") -> None:
        """Should map class_definition to ClassDef."""
        from astroid import nodes as anodes

        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        ast_node = mapper.cst_to_ast(ts_nodes[0])
        assert isinstance(ast_node, anodes.ClassDef)
        assert ast_node.name == "MyModel"

    def test_maps_function_definition(self, mapper: "CSTASTMapper") -> None:
        """Should map function_definition to FunctionDef."""
        from astroid import nodes as anodes

        # Use a function without return type annotation
        ts_nodes = mapper.search_cst("def $NAME($$$PARAMS): $$$BODY")
        if not ts_nodes:
            # Fallback: try with return type
            ts_nodes = mapper.search_cst("def $NAME($$$PARAMS) -> $RET: $$$BODY")
        assert ts_nodes
        ast_node = mapper.cst_to_ast(ts_nodes[0])
        assert isinstance(ast_node, (anodes.FunctionDef, anodes.AsyncFunctionDef))

    def test_returns_none_for_unnamed_node(self, mapper: "CSTASTMapper") -> None:
        """Should return None for unnamed (anonymous) tree-sitter nodes."""
        root = mapper.sg_root.root()
        # Find an unnamed child (punctuation etc.)
        for child in root.children():
            if not child.is_named():
                assert mapper.cst_to_ast(child) is None
                break

    def test_fallback_for_cst_only_node(self, mapper: "CSTASTMapper") -> None:
        """Should return a parent astroid node for CST-only nodes like argument_list."""
        from astroid import nodes as anodes

        # argument_list is a CST-only node with no direct astroid equivalent
        call_ts_nodes = mapper.search_cst("print($$$ARGS)")
        if not call_ts_nodes:
            pytest.skip("No print() call found in sample")

        # Find the argument_list child
        for child in call_ts_nodes[0].children():
            if child.kind() == "argument_list":
                result = mapper.cst_to_ast(child)
                # Should fall back to the parent Call or Expr node
                assert isinstance(result, (anodes.Call, anodes.Expr))
                break


# ---------------------------------------------------------------------------
# ast_to_cst
# ---------------------------------------------------------------------------


class TestASTToCST:
    """Tests for ast_to_cst method."""

    def test_maps_classdef_to_class_definition(self, mapper: "CSTASTMapper") -> None:
        """Should map ClassDef to class_definition."""
        from astroid import nodes as anodes

        class_defs = list(mapper.astroid_tree.nodes_of_class(anodes.ClassDef))
        assert class_defs
        ts_node = mapper.ast_to_cst(class_defs[0])
        assert ts_node is not None
        assert ts_node.kind() == "class_definition"

    def test_maps_functiondef_to_function_definition(self, mapper: "CSTASTMapper") -> None:
        """Should map FunctionDef to function_definition or decorated_definition."""
        from astroid import nodes as anodes

        func_defs = list(mapper.astroid_tree.nodes_of_class(anodes.FunctionDef))
        assert func_defs
        ts_node = mapper.ast_to_cst(func_defs[0])
        assert ts_node is not None
        assert ts_node.kind() in ("function_definition", "decorated_definition")

    def test_maps_assign_to_assignment(self, mapper: "CSTASTMapper") -> None:
        """Should map Assign to assignment."""
        from astroid import nodes as anodes

        assigns = list(mapper.astroid_tree.nodes_of_class(anodes.Assign))
        # Find a top-level assignment (data = [...])
        top_assigns = [a for a in assigns if isinstance(a.parent, anodes.Module)]
        assert top_assigns
        ts_node = mapper.ast_to_cst(top_assigns[0])
        assert ts_node is not None
        assert ts_node.kind() in ("assignment", "expression_statement")

    def test_handles_no_coords_node(self, mapper: "CSTASTMapper") -> None:
        """Should handle astroid nodes without coordinates (Arguments)."""
        from astroid import nodes as anodes

        func_defs = list(mapper.astroid_tree.nodes_of_class(anodes.FunctionDef))
        assert func_defs
        args_node = func_defs[0].args  # Arguments node (no coords)
        result = mapper.ast_to_cst(args_node)
        # Should fall back to a child or parent node
        assert result is not None

    def test_decorated_function_maps_to_decorated_definition(self, mapper: "CSTASTMapper") -> None:
        """Should map a decorated FunctionDef to decorated_definition."""
        from astroid import nodes as anodes

        func_defs = list(mapper.astroid_tree.nodes_of_class(anodes.FunctionDef))
        decorated = [f for f in func_defs if f.decorators is not None]
        assert decorated, "No decorated functions found in sample"
        ts_node = mapper.ast_to_cst(decorated[0])
        assert ts_node is not None
        assert ts_node.kind() in ("decorated_definition", "function_definition")


# ---------------------------------------------------------------------------
# Round-trip consistency
# ---------------------------------------------------------------------------


class TestRoundTrip:
    """Tests for round-trip consistency between cst_to_ast and ast_to_cst."""

    def test_class_round_trip(self, mapper: "CSTASTMapper") -> None:
        """CST -> AST -> CST should return a node with the same range."""
        ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        assert ts_nodes
        ts_node = ts_nodes[0]

        ast_node = mapper.cst_to_ast(ts_node)
        assert ast_node is not None

        ts_back = mapper.ast_to_cst(ast_node)
        assert ts_back is not None

        # The round-trip node should cover the same source range
        original_rng = mapper._ts_range(ts_node)
        back_rng = mapper._ts_range(ts_back)
        assert original_rng == back_rng

    def test_function_round_trip(self, mapper: "CSTASTMapper") -> None:
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
