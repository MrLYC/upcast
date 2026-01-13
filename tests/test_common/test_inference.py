"""Tests for the structured inference module."""

import astroid
import pytest
from astroid import nodes

from upcast.common.inference import (
    DYNAMIC,
    InferenceResult,
    StringPattern,
    infer_string_pattern,
    infer_type,
    infer_value,
)


class TestInferenceResult:
    """Tests for InferenceResult dataclass."""

    def test_exact_inference_result(self) -> None:
        """Should create exact inference result."""
        node = astroid.parse("x = 42").body[0].value
        result = InferenceResult(value=42, confidence="exact", is_static=True, node=node)
        assert result.value == 42
        assert result.confidence == "exact"
        assert result.is_static is True
        assert result.is_dynamic is False
        assert result.node is node

    def test_partial_inference_result(self) -> None:
        """Should create partial inference result."""
        node = astroid.parse("x = [1, var]").body[0].value
        result = InferenceResult(value=[1, None], confidence="partial", is_static=False, node=node)
        assert result.value == [1, None]
        assert result.confidence == "partial"
        assert result.is_static is False
        assert result.is_dynamic is True

    def test_unknown_inference_result(self) -> None:
        """Should create unknown inference result."""
        node = astroid.parse("x = func()").body[0].value
        result = InferenceResult(value=None, confidence="unknown", is_static=False, node=node)
        assert result.value is None
        assert result.confidence == "unknown"
        assert result.is_static is False

    def test_repr_exact(self) -> None:
        """Should have readable repr for exact results."""
        node = astroid.parse('x = "hello"').body[0].value
        result = InferenceResult(value="hello", confidence="exact", is_static=True, node=node)
        assert repr(result) == "InferenceResult('hello', exact)"

    def test_repr_partial(self) -> None:
        """Should have readable repr for partial results."""
        node = astroid.parse("x = [1, 2]").body[0].value
        result = InferenceResult(value=[1, 2], confidence="partial", is_static=False, node=node)
        assert repr(result) == "InferenceResult([1, 2], partial)"

    def test_repr_unknown(self) -> None:
        """Should have readable repr for unknown results."""
        node = astroid.parse("x = func()").body[0].value
        result = InferenceResult(value=None, confidence="unknown", is_static=False, node=node)
        assert "unknown" in repr(result)
        assert "func()" in repr(result)

    def test_is_exact_property(self) -> None:
        """Should check if result is exact."""
        node = astroid.parse("x = 42").body[0].value
        exact_result = InferenceResult(value=42, confidence="exact", is_static=True, node=node)
        assert exact_result.is_exact is True

        partial_result = InferenceResult(value=[1, None], confidence="partial", is_static=False, node=node)
        assert partial_result.is_exact is False

        unknown_result = InferenceResult(value=None, confidence="unknown", is_static=False, node=node)
        assert unknown_result.is_exact is False

    def test_get_exact_returns_value_when_exact(self) -> None:
        """Should return value when confidence is exact."""
        node = astroid.parse("x = 42").body[0].value
        result = InferenceResult(value=42, confidence="exact", is_static=True, node=node)
        assert result.get_exact() == 42

    def test_get_exact_returns_default_when_not_exact(self) -> None:
        """Should return default when confidence is not exact."""
        node = astroid.parse("x = func()").body[0].value
        result = InferenceResult(value=None, confidence="unknown", is_static=False, node=node)
        assert result.get_exact() is None
        assert result.get_exact(default=999) == 999

    def test_get_if_type_returns_value_when_type_matches(self) -> None:
        """Should return value when type matches and confidence is exact."""
        node = astroid.parse("x = 42").body[0].value
        result = InferenceResult(value=42, confidence="exact", is_static=True, node=node)
        assert result.get_if_type(int) == 42
        assert result.get_if_type((int, str)) == 42

    def test_get_if_type_returns_default_when_type_mismatch(self) -> None:
        """Should return default when type doesn't match."""
        node = astroid.parse("x = 42").body[0].value
        result = InferenceResult(value=42, confidence="exact", is_static=True, node=node)
        assert result.get_if_type(str) is None
        assert result.get_if_type(str, default="N/A") == "N/A"

    def test_get_if_type_returns_default_when_not_exact(self) -> None:
        """Should return default when confidence is not exact."""
        node = astroid.parse("x = func()").body[0].value
        result = InferenceResult(value=None, confidence="unknown", is_static=False, node=node)
        assert result.get_if_type(int) is None
        assert result.get_if_type(int, default=0) == 0


class TestStringPattern:
    """Tests for StringPattern dataclass."""

    def test_static_pattern(self) -> None:
        """Should recognize fully static pattern."""
        node = astroid.parse('x = "hello"').body[0].value
        pattern = StringPattern(parts=["hello"], node=node)
        assert pattern.is_static is True
        assert pattern.is_dynamic is False
        assert pattern.to_pattern() == "hello"

    def test_dynamic_pattern(self) -> None:
        """Should recognize pattern with dynamic parts."""
        node = astroid.parse('x = f"hello {name}"').body[0].value
        pattern = StringPattern(parts=["hello ", ...], node=node)
        assert pattern.is_static is False
        assert pattern.is_dynamic is True
        assert pattern.to_pattern() == "hello ..."

    def test_mixed_pattern(self) -> None:
        """Should handle pattern with mixed static and dynamic parts."""
        node = astroid.parse('x = f"api/{version}/users"').body[0].value
        pattern = StringPattern(parts=["api/", ..., "/users"], node=node)
        assert pattern.is_dynamic is True
        assert pattern.to_pattern() == "api/.../users"

    def test_static_prefix(self) -> None:
        """Should extract static prefix."""
        node = astroid.parse('x = f"https://api.example.com/{path}"').body[0].value
        pattern = StringPattern(parts=["https://api.example.com/", ...], node=node)
        assert pattern.static_prefix() == "https://api.example.com/"

    def test_static_prefix_empty(self) -> None:
        """Should return empty string when no static prefix."""
        node = astroid.parse('x = f"{proto}://example.com"').body[0].value
        pattern = StringPattern(parts=[..., "://example.com"], node=node)
        assert pattern.static_prefix() == ""

    def test_static_suffix(self) -> None:
        """Should extract static suffix."""
        node = astroid.parse('x = f"https://{host}/api/v1"').body[0].value
        pattern = StringPattern(parts=["https://", ..., "/api/v1"], node=node)
        assert pattern.static_suffix() == "/api/v1"

    def test_static_suffix_empty(self) -> None:
        """Should return empty string when no static suffix."""
        node = astroid.parse('x = f"https://example.com/{path}"').body[0].value
        pattern = StringPattern(parts=["https://example.com/", ...], node=node)
        assert pattern.static_suffix() == ""

    def test_static_parts(self) -> None:
        """Should extract all static parts."""
        node = astroid.parse('x = f"api/{version}/users/{id}"').body[0].value
        pattern = StringPattern(parts=["api/", ..., "/users/", ...], node=node)
        assert pattern.static_parts() == ["api/", "/users/"]

    def test_dynamic_count(self) -> None:
        """Should count dynamic parts."""
        node = astroid.parse('x = f"{a}/{b}/{c}"').body[0].value
        pattern = StringPattern(parts=[..., "/", ..., "/", ...], node=node)
        assert pattern.dynamic_count() == 3

    def test_dynamic_count_zero(self) -> None:
        """Should return zero for static pattern."""
        node = astroid.parse('x = "static"').body[0].value
        pattern = StringPattern(parts=["static"], node=node)
        assert pattern.dynamic_count() == 0

    def test_to_inference_result_static(self) -> None:
        """Should convert static pattern to exact inference result."""
        node = astroid.parse('x = "hello"').body[0].value
        pattern = StringPattern(parts=["hello"], node=node)
        result = pattern.to_inference_result()
        assert result.value == "hello"
        assert result.confidence == "exact"
        assert result.is_static is True

    def test_to_inference_result_dynamic(self) -> None:
        """Should convert dynamic pattern to partial inference result."""
        node = astroid.parse('x = f"hello {name}"').body[0].value
        pattern = StringPattern(parts=["hello ", ...], node=node)
        result = pattern.to_inference_result()
        assert result.value == "hello ..."
        assert result.confidence == "partial"
        assert result.is_static is False

    def test_repr(self) -> None:
        """Should have readable repr."""
        node = astroid.parse('x = f"api/{ver}/users"').body[0].value
        pattern = StringPattern(parts=["api/", ..., "/users"], node=node)
        assert repr(pattern) == "StringPattern(['api/', ..., '/users'])"

    def test_dynamic_constant(self) -> None:
        """DYNAMIC should be Ellipsis."""
        assert DYNAMIC is ...


class TestInferValue:
    """Tests for infer_value function."""

    def test_infer_string(self) -> None:
        """Should infer string constant."""
        node = astroid.parse('x = "hello"').body[0].value
        result = infer_value(node)
        assert result.value == "hello"
        assert result.confidence == "exact"
        assert result.is_static is True

    def test_infer_integer(self) -> None:
        """Should infer integer constant."""
        node = astroid.parse("x = 42").body[0].value
        result = infer_value(node)
        assert result.value == 42
        assert result.confidence == "exact"
        assert result.is_static is True

    def test_infer_float(self) -> None:
        """Should infer float constant."""
        node = astroid.parse("x = 3.14").body[0].value
        result = infer_value(node)
        assert result.value == 3.14
        assert result.confidence == "exact"
        assert result.is_static is True

    def test_infer_boolean(self) -> None:
        """Should infer boolean constant."""
        node = astroid.parse("x = True").body[0].value
        result = infer_value(node)
        assert result.value is True
        assert result.confidence == "exact"
        assert result.is_static is True

    def test_infer_none(self) -> None:
        """Should infer None constant."""
        node = astroid.parse("x = None").body[0].value
        result = infer_value(node)
        assert result.value is None
        assert result.confidence == "exact"
        assert result.is_static is True

    def test_infer_list(self) -> None:
        """Should infer list literal."""
        node = astroid.parse("x = [1, 2, 3]").body[0].value
        result = infer_value(node)
        assert result.value == [1, 2, 3]
        assert result.confidence == "exact"
        assert result.is_static is True

    def test_infer_tuple(self) -> None:
        """Should infer tuple literal."""
        node = astroid.parse('x = (1, "a", True)').body[0].value
        result = infer_value(node)
        assert result.value == (1, "a", True)
        assert result.confidence == "exact"
        assert result.is_static is True

    def test_infer_dict(self) -> None:
        """Should infer dict literal."""
        node = astroid.parse('x = {"key": "value", "num": 42}').body[0].value
        result = infer_value(node)
        assert result.value == {"key": "value", "num": 42}
        assert result.confidence == "exact"
        assert result.is_static is True

    def test_infer_nested_list(self) -> None:
        """Should infer nested list."""
        node = astroid.parse("x = [[1, 2], [3, 4]]").body[0].value
        result = infer_value(node)
        assert result.value == [[1, 2], [3, 4]]
        assert result.confidence == "exact"

    def test_infer_list_with_unknown(self) -> None:
        """Should return partial for list with unknown elements."""
        code = """
unknown = func()
x = [1, unknown, 3]
"""
        module = astroid.parse(code)
        node = module.body[1].value
        result = infer_value(node)
        assert result.confidence == "partial"
        assert result.is_static is False
        # List still contains the inferable values
        assert result.value[0] == 1
        assert result.value[2] == 3

    def test_infer_dict_with_unknown(self) -> None:
        """Should return partial for dict with unknown values."""
        code = """
unknown = func()
x = {"a": 1, "b": unknown}
"""
        module = astroid.parse(code)
        node = module.body[1].value
        result = infer_value(node)
        assert result.confidence == "partial"
        assert result.is_static is False
        assert result.value["a"] == 1

    def test_infer_unknown_function_call(self) -> None:
        """Should return unknown for function calls."""
        node = astroid.parse("x = func()").body[0].value
        result = infer_value(node)
        assert result.value is None
        assert result.confidence == "unknown"
        assert result.is_static is False

    def test_infer_unknown_variable(self) -> None:
        """Should return unknown for undefined variables."""
        node = astroid.parse("x = unknown_var").body[0].value
        result = infer_value(node)
        assert result.confidence == "unknown"
        assert result.is_static is False

    def test_infer_empty_list(self) -> None:
        """Should infer empty list."""
        node = astroid.parse("x = []").body[0].value
        result = infer_value(node)
        assert result.value == []
        assert result.confidence == "exact"

    def test_infer_empty_dict(self) -> None:
        """Should infer empty dict."""
        node = astroid.parse("x = {}").body[0].value
        result = infer_value(node)
        assert result.value == {}
        assert result.confidence == "exact"


class TestInferStringPattern:
    """Tests for infer_string_pattern function."""

    def test_simple_string(self) -> None:
        """Should handle simple string literal."""
        node = astroid.parse('x = "hello world"').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.parts == ["hello world"]
        assert pattern.is_static is True
        assert pattern.to_pattern() == "hello world"

    def test_fstring_static(self) -> None:
        """Should handle f-string with static content only."""
        node = astroid.parse('x = f"hello world"').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_static is True
        assert pattern.to_pattern() == "hello world"

    def test_fstring_with_variable(self) -> None:
        """Should handle f-string with variable."""
        node = astroid.parse('x = f"hello {name}"').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True
        assert pattern.to_pattern() == "hello ..."

    def test_fstring_multiple_variables(self) -> None:
        """Should handle f-string with multiple variables."""
        node = astroid.parse('x = f"{greeting} {name}!"').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True
        # Consecutive dynamics should be normalized
        assert pattern.dynamic_count() >= 1

    def test_fstring_url_pattern(self) -> None:
        """Should extract URL pattern from f-string."""
        node = astroid.parse('x = f"https://api.example.com/users/{user_id}/posts"').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.static_prefix() == "https://api.example.com/users/"
        assert pattern.static_suffix() == "/posts"

    def test_percent_format_simple(self) -> None:
        """Should handle percent formatting."""
        node = astroid.parse('x = "Hello %s" % name').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True
        assert "Hello " in pattern.static_prefix()

    def test_percent_format_multiple(self) -> None:
        """Should handle multiple percent placeholders."""
        node = astroid.parse('x = "%s-%d" % (a, b)').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True
        assert "-" in pattern.to_pattern()

    def test_percent_format_named(self) -> None:
        """Should handle named percent placeholders."""
        node = astroid.parse('x = "%(name)s is %(age)d" % data').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True
        assert " is " in pattern.to_pattern()

    def test_percent_escaped(self) -> None:
        """Should handle escaped percent signs."""
        node = astroid.parse('x = "100%% complete" % ()').body[0].value
        pattern = infer_string_pattern(node)
        # %% should become literal %
        assert "%" in pattern.to_pattern() or "100" in pattern.to_pattern()

    def test_format_method_simple(self) -> None:
        """Should handle .format() method."""
        node = astroid.parse('x = "Hello {}".format(name)').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True
        assert pattern.static_prefix() == "Hello "

    def test_format_method_numbered(self) -> None:
        """Should handle numbered .format() placeholders."""
        node = astroid.parse('x = "{0} and {1}".format(a, b)').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True
        assert " and " in pattern.to_pattern()

    def test_format_method_named(self) -> None:
        """Should handle named .format() placeholders."""
        node = astroid.parse('x = "{name} is {age}".format(name=n, age=a)').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True
        assert " is " in pattern.to_pattern()

    def test_string_concatenation(self) -> None:
        """Should handle string concatenation."""
        node = astroid.parse('x = "hello" + " " + "world"').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_static is True
        assert pattern.to_pattern() == "hello world"

    def test_string_concat_with_variable(self) -> None:
        """Should handle concatenation with variable."""
        code = """
prefix = "api/"
x = prefix + path
"""
        module = astroid.parse(code)
        node = module.body[1].value
        pattern = infer_string_pattern(node)
        # prefix is resolvable, path is not
        assert pattern.is_dynamic is True

    def test_concat_fstring(self) -> None:
        """Should handle concatenation of f-strings."""
        node = astroid.parse('x = f"hello " + f"{name}"').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True
        assert "hello " in pattern.static_prefix()

    def test_unknown_variable(self) -> None:
        """Should return dynamic for unknown variable."""
        node = astroid.parse("x = unknown_string").body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True
        assert pattern.to_pattern() == "..."

    def test_fstring_with_inferable_constant(self) -> None:
        """Should inline inferable f-string values."""
        code = """
VERSION = "v1"
x = f"api/{VERSION}/users"
"""
        module = astroid.parse(code)
        node = module.body[1].value
        pattern = infer_string_pattern(node)
        # VERSION should be inferred as "v1"
        assert "api/" in pattern.static_prefix()

    def test_empty_string(self) -> None:
        """Should handle empty string."""
        node = astroid.parse('x = ""').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_static is True
        assert pattern.to_pattern() == ""


class TestInferType:
    """Tests for infer_type function."""

    def test_infer_str_type(self) -> None:
        """Should infer str type."""
        node = astroid.parse('x = "hello"').body[0].value
        type_name, confidence = infer_type(node)
        assert type_name == "str"
        assert confidence == "exact"

    def test_infer_int_type(self) -> None:
        """Should infer int type."""
        node = astroid.parse("x = 42").body[0].value
        type_name, confidence = infer_type(node)
        assert type_name == "int"
        assert confidence == "exact"

    def test_infer_float_type(self) -> None:
        """Should infer float type."""
        node = astroid.parse("x = 3.14").body[0].value
        type_name, confidence = infer_type(node)
        assert type_name == "float"
        assert confidence == "exact"

    def test_infer_bool_type(self) -> None:
        """Should infer bool type."""
        node = astroid.parse("x = True").body[0].value
        type_name, confidence = infer_type(node)
        assert type_name == "bool"
        assert confidence == "exact"

    def test_infer_none_type(self) -> None:
        """Should infer None type."""
        node = astroid.parse("x = None").body[0].value
        type_name, confidence = infer_type(node)
        assert type_name == "None"
        assert confidence == "exact"

    def test_infer_list_type(self) -> None:
        """Should infer list type."""
        node = astroid.parse("x = [1, 2, 3]").body[0].value
        type_name, confidence = infer_type(node)
        assert type_name == "list"
        assert confidence == "exact"

    def test_infer_dict_type(self) -> None:
        """Should infer dict type."""
        node = astroid.parse('x = {"a": 1}').body[0].value
        type_name, confidence = infer_type(node)
        assert type_name == "dict"
        assert confidence == "exact"

    def test_infer_tuple_type(self) -> None:
        """Should infer tuple type."""
        node = astroid.parse("x = (1, 2, 3)").body[0].value
        type_name, confidence = infer_type(node)
        assert type_name == "tuple"
        assert confidence == "exact"

    def test_infer_unknown_type(self) -> None:
        """Should return unknown for uninferable types."""
        node = astroid.parse("x = func()").body[0].value
        type_name, confidence = infer_type(node)
        assert type_name == "unknown"
        assert confidence == "unknown"


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_infer_value_handles_inference_error(self) -> None:
        """Should handle InferenceError gracefully."""
        # Create a node that will cause inference issues
        node = astroid.parse("x = undefined_module.func()").body[0].value
        result = infer_value(node)
        assert result.confidence == "unknown"

    def test_infer_string_pattern_handles_non_string(self) -> None:
        """Should handle non-string nodes."""
        node = astroid.parse("x = 42").body[0].value
        pattern = infer_string_pattern(node)
        # Integer cannot be a string pattern
        assert pattern.is_dynamic is True

    def test_percent_format_non_string_left(self) -> None:
        """Should handle percent format with non-string left operand."""
        node = astroid.parse("x = unknown % values").body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True

    def test_nested_fstring_in_concat(self) -> None:
        """Should handle nested f-strings in concatenation."""
        node = astroid.parse('x = f"a{b}" + f"c{d}"').body[0].value
        pattern = infer_string_pattern(node)
        assert pattern.is_dynamic is True
        # Should have both 'a' and 'c' somewhere in the pattern
        pattern_str = pattern.to_pattern()
        assert "a" in pattern_str
        assert "c" in pattern_str

    def test_dict_with_non_hashable_key(self) -> None:
        """Should handle dict inference with complex keys."""
        # This will have a list as key which isn't hashable
        code = """
unknown = func()
x = {unknown: 1}
"""
        module = astroid.parse(code)
        node = module.body[1].value
        result = infer_value(node)
        # Should still work, but may be partial
        assert result.confidence in ("partial", "unknown")

    def test_tuple_with_unknown_elements(self) -> None:
        """Should handle tuple with unknown elements."""
        code = """
unknown = func()
x = (1, unknown, 3)
"""
        module = astroid.parse(code)
        node = module.body[1].value
        result = infer_value(node)
        assert result.confidence == "partial"
        assert result.value[0] == 1
        assert result.value[2] == 3
