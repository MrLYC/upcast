"""Tests for AST utilities."""

import astroid

from upcast.common.ast_utils import (
    get_qualified_name,
    infer_type_with_fallback,
    infer_value_with_fallback,
    safe_as_string,
)


class TestSafeAsString:
    """Tests for safe_as_string function."""

    def test_converts_simple_value(self) -> None:
        """Should convert simple values to strings."""
        assert safe_as_string(42) == "42"
        assert safe_as_string("test") == "test"
        assert safe_as_string(True) == "True"

    def test_handles_none(self) -> None:
        """Should handle None value."""
        assert safe_as_string(None) == "None"

    def test_handles_complex_objects(self) -> None:
        """Should handle objects with __str__."""
        assert safe_as_string([1, 2, 3]) == "[1, 2, 3]"
        assert safe_as_string({"key": "value"}) == "{'key': 'value'}"


class TestInferValueWithFallback:
    """Tests for infer_value_with_fallback function."""

    def test_infers_string_constant(self) -> None:
        """Should infer string constant."""
        code = 'x = "hello"'
        module = astroid.parse(code)
        assign = module.body[0]
        value, success = infer_value_with_fallback(assign.value)
        assert success
        assert value == "hello"

    def test_infers_integer_constant(self) -> None:
        """Should infer integer constant."""
        code = "x = 42"
        module = astroid.parse(code)
        assign = module.body[0]
        value, success = infer_value_with_fallback(assign.value)
        assert success
        assert value == 42

    def test_infers_boolean_constant(self) -> None:
        """Should infer boolean constant."""
        code = "x = True"
        module = astroid.parse(code)
        assign = module.body[0]
        value, success = infer_value_with_fallback(assign.value)
        assert success
        assert value is True

    def test_infers_list_literal(self) -> None:
        """Should infer list literal."""
        code = "x = [1, 2, 3]"
        module = astroid.parse(code)
        assign = module.body[0]
        value, success = infer_value_with_fallback(assign.value)
        assert success
        assert value == [1, 2, 3]

    def test_infers_dict_literal(self) -> None:
        """Should infer dict literal."""
        code = 'x = {"key": "value"}'
        module = astroid.parse(code)
        assign = module.body[0]
        value, success = infer_value_with_fallback(assign.value)
        assert success
        assert value == {"key": "value"}

    def test_wraps_uninferable_in_backticks(self) -> None:
        """Should wrap uninferable values in backticks."""
        code = "x = some_function()"
        module = astroid.parse(code)
        assign = module.body[0]
        value, success = infer_value_with_fallback(assign.value)
        assert not success
        assert value.startswith("`")
        assert value.endswith("`")

    def test_wraps_variable_reference_in_backticks(self) -> None:
        """Should wrap variable references in backticks."""
        code = "x = unknown_var"
        module = astroid.parse(code)
        assign = module.body[0]
        value, success = infer_value_with_fallback(assign.value)
        assert not success
        assert "`" in value

    def test_handles_nested_list_with_uninferable(self) -> None:
        """Should handle lists with mixed inferable/uninferable items."""
        code = "x = [1, unknown_var, 3]"
        module = astroid.parse(code)
        assign = module.body[0]
        value, success = infer_value_with_fallback(assign.value)
        # List is partially inferable
        assert isinstance(value, list)
        assert value[0] == 1
        assert "`" in str(value[1])  # uninferable wrapped
        assert value[2] == 3


class TestInferTypeWithFallback:
    """Tests for infer_type_with_fallback function."""

    def test_infers_string_type(self) -> None:
        """Should infer str type."""
        code = 'x = "hello"'
        module = astroid.parse(code)
        assign = module.body[0]
        type_name, success = infer_type_with_fallback(assign.value)
        assert success
        assert type_name == "str"

    def test_infers_int_type(self) -> None:
        """Should infer int type."""
        code = "x = 42"
        module = astroid.parse(code)
        assign = module.body[0]
        type_name, success = infer_type_with_fallback(assign.value)
        assert success
        assert type_name == "int"

    def test_infers_bool_type(self) -> None:
        """Should infer bool type."""
        code = "x = True"
        module = astroid.parse(code)
        assign = module.body[0]
        type_name, success = infer_type_with_fallback(assign.value)
        assert success
        assert type_name == "bool"

    def test_infers_float_type(self) -> None:
        """Should infer float type."""
        code = "x = 3.14"
        module = astroid.parse(code)
        assign = module.body[0]
        type_name, success = infer_type_with_fallback(assign.value)
        assert success
        assert type_name == "float"

    def test_returns_unknown_for_uninferable(self) -> None:
        """Should return 'unknown' for uninferable types."""
        code = "x = some_function()"
        module = astroid.parse(code)
        assign = module.body[0]
        type_name, success = infer_type_with_fallback(assign.value)
        assert not success
        assert type_name == "unknown"

    def test_handles_none_type(self) -> None:
        """Should handle None type."""
        code = "x = None"
        module = astroid.parse(code)
        assign = module.body[0]
        type_name, success = infer_type_with_fallback(assign.value)
        # None has type None in astroid
        assert success
        assert type_name == "None"


class TestGetQualifiedName:
    """Tests for get_qualified_name function."""

    def test_gets_builtin_type_name(self) -> None:
        """Should get qualified name for builtin types."""
        code = "x = 42"
        module = astroid.parse(code)
        assign = module.body[0]
        inferred = next(assign.value.infer())
        name, success = get_qualified_name(inferred)
        assert success
        # Builtin types have 'builtins.' prefix
        assert name == "builtins.int"

    def test_gets_custom_class_name(self) -> None:
        """Should get qualified name for custom classes."""
        code = """
class MyClass:
    pass

x = MyClass()
"""
        module = astroid.parse(code)
        assign = module.body[1]
        inferred = next(assign.value.infer())
        name, success = get_qualified_name(inferred)
        assert success
        # Module is unnamed, so just class name
        assert "MyClass" in name

    def test_handles_uninferable(self) -> None:
        """Should handle uninferable nodes."""
        code = "x = unknown_func()"
        module = astroid.parse(code)
        assign = module.body[0]
        try:
            inferred = next(assign.value.infer())
            name, success = get_qualified_name(inferred)
            assert not success
            assert "`" in name
        except astroid.exceptions.InferenceError:
            # This is also acceptable behavior
            pass
