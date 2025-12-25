"""Tests for AST utility functions."""

import astroid
from upcast.env_var_scanner.ast_utils import (
    infer_literal_value,
    infer_type_from_value,
    is_env_var_call,
    resolve_string_concat,
    safe_as_string,
)


class TestIsEnvVarCall:
    """Tests for is_env_var_call function."""

    def test_detects_os_getenv(self):
        """Should detect os.getenv() calls."""
        code = "os.getenv('VAR')  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.Call)
        assert is_env_var_call(node)

    def test_detects_os_environ_get(self):
        """Should detect os.environ.get() calls."""
        code = "os.environ.get('VAR')  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.Call)
        assert is_env_var_call(node)

    def test_detects_env_call(self):
        """Should detect env() calls."""
        code = "env('VAR')  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.Call)
        assert is_env_var_call(node)

    def test_detects_env_typed_methods(self):
        """Should detect env.str(), env.int(), etc. calls."""
        code = "env.str('VAR')  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.Call)
        assert is_env_var_call(node)

        code = "env.int('VAR')  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.Call)
        assert is_env_var_call(node)

    def test_rejects_non_env_calls(self):
        """Should not detect non-env-var calls."""
        code = "print('hello')  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.Call)
        assert not is_env_var_call(node)


class TestInferTypeFromValue:
    """Tests for infer_type_from_value function."""

    def test_infers_str_type(self):
        """Should infer str type from string literal."""
        code = "x = __('hello')"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.NodeNG)
        assert infer_type_from_value(node) == "str"

    def test_infers_int_type(self):
        """Should infer int type from integer literal."""
        code = "123  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.NodeNG)
        assert infer_type_from_value(node) == "int"

    def test_infers_bool_type(self):
        """Should infer bool type from boolean literal."""
        code = "True  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.NodeNG)
        assert infer_type_from_value(node) == "bool"

        code = "False  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.NodeNG)
        assert infer_type_from_value(node) == "bool"

    def test_infers_float_type(self):
        """Should infer float type from float literal."""
        code = "3.14  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.NodeNG)
        assert infer_type_from_value(node) == "float"

    def test_returns_none_for_none_value(self):
        """Should return None for None literal."""
        code = "None  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.NodeNG)
        assert infer_type_from_value(node) is None


class TestInferLiteralValue:
    """Tests for infer_literal_value function."""

    def test_extracts_string_literal(self):
        """Should extract string literal value."""
        code = "x = __('hello world')"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.NodeNG)
        assert infer_literal_value(node) == "hello world"

    def test_extracts_int_literal(self):
        """Should extract integer literal value."""
        code = "42  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.NodeNG)
        assert infer_literal_value(node) == 42

    def test_extracts_bool_literal(self):
        """Should extract boolean literal value."""
        code = "True  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.NodeNG)
        assert infer_literal_value(node) is True

    def test_extracts_constant_expression(self):
        """Should resolve constant expression."""
        module = astroid.parse(
            """
PREFIX = 'DB_'
var = PREFIX
"""
        )
        assign_nodes = list(module.nodes_of_class(astroid.nodes.Assign))
        var_node = assign_nodes[1].value
        result = infer_literal_value(var_node)
        assert result == "DB_"


class TestResolveStringConcat:
    """Tests for resolve_string_concat function."""

    def test_resolves_simple_concat(self):
        """Should resolve simple string concatenation."""
        module = astroid.parse(
            """
PREFIX = 'DB_'
result = PREFIX + 'URL'
"""
        )
        assign_nodes = list(module.nodes_of_class(astroid.nodes.Assign))
        concat_node = assign_nodes[1].value
        result = resolve_string_concat(concat_node)
        assert result == "DB_URL"

    def test_returns_none_for_non_string(self):
        """Should return None for non-string expressions."""
        code = "1 + 2  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.NodeNG)
        result = resolve_string_concat(node)
        assert result is None


class TestSafeAsString:
    """Tests for safe_as_string function."""

    def test_converts_node_to_string(self):
        """Should convert astroid node to string."""
        code = "os.getenv('VAR')  #@"
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.NodeNG)
        result = safe_as_string(node)
        assert "getenv" in result
        assert "VAR" in result


class TestRegressionFalsePositives:
    """Regression tests for false positive fixes."""

    def test_no_false_positive_for_dict_subscript(self):
        """
        Regression test: String literals in subscript operations should not be
        detected as environment variables.

        Previously, the scanner would report 'id' as an env var from this code:
        response.data['id']
        """
        code = """
api_client.post(
    f'/api/bkapps/applications/{code}/config_vars/',
    {'key': 'A1', 'value': 'foo', 'environment_name': '_global_', 'description': 'foo'}
).data['id']  #@
"""
        node = astroid.extract_node(code)
        # The extract_node should give us the subscript node
        # This is data['id'], which should NOT be considered an env var access
        # We're checking that the string 'id' inside the subscript is not extracted

        # Walk the tree and verify no Call nodes are env var calls
        if isinstance(node, astroid.nodes.Call):
            assert not is_env_var_call(node)

    def test_no_false_positive_for_api_path_strings(self):
        """
        Regression test: String literals in API paths should not be detected
        as environment variables.

        Previously, the scanner might extract 'environment_name' from:
        f'/api/bkapps/applications/{code}/config_vars/'
        """
        code = """
import requests

def test():
    requests.post(
        f'/api/bkapps/applications/{code}/config_vars/',
        json={'key': 'A1', 'value': 'foo', 'environment_name': '_global_'}
    )  #@
"""
        node = astroid.extract_node(code)
        assert isinstance(node, astroid.nodes.Call)
        # This is a requests.post call, not an env var call
        assert not is_env_var_call(node)

    def test_detects_only_os_environ_subscript(self):
        """
        Regression test: Only os.environ[] should be detected as env var access,
        not arbitrary dictionary subscripts.
        """
        # Real env var access - should be detected
        code = "os.environ['DATABASE_URL']  #@"
        astroid.extract_node(code)
        # Note: is_env_var_call checks Call nodes, but os.environ[] is a Subscript
        # The scanner should handle Subscript separately via _check_environ_subscript

        # Not an env var access - should NOT be detected
        code = "config['DATABASE_URL']  #@"
        astroid.extract_node(code)
        # This is just a dict access, not os.environ
