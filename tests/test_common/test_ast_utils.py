"""Tests for AST utilities."""

import astroid

from upcast.common.ast_utils import (
    extract_decorator_info,
    find_function_calls,
    get_import_info,
    get_qualified_name,
    infer_type_with_fallback,
    infer_value_with_fallback,
    safe_as_string,
    safe_infer_value,
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
        value, _success = infer_value_with_fallback(assign.value)
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


class TestFindFunctionCalls:
    """Tests for find_function_calls function."""

    def test_finds_all_calls_when_no_filter(self) -> None:
        """Should find all function calls when no filter provided."""
        code = """
sleep(10)
print("hello")
time.sleep(5)
"""
        module = astroid.parse(code)
        calls = find_function_calls(module)
        assert len(calls) == 3

    def test_finds_specific_function_calls(self) -> None:
        """Should find only specified function calls."""
        code = """
sleep(10)
print("hello")
time.sleep(5)
getenv("PATH")
"""
        module = astroid.parse(code)
        calls = find_function_calls(module, {"sleep", "getenv"})
        assert len(calls) == 3  # sleep, time.sleep, getenv

    def test_handles_empty_module(self) -> None:
        """Should return empty list for module with no calls."""
        code = "x = 42"
        module = astroid.parse(code)
        calls = find_function_calls(module, {"sleep"})
        assert len(calls) == 0

    def test_finds_method_calls(self) -> None:
        """Should find method calls like time.sleep."""
        code = """
import time
time.sleep(10)
time.time()
"""
        module = astroid.parse(code)
        calls = find_function_calls(module, {"sleep"})
        assert len(calls) == 1


class TestExtractDecoratorInfo:
    """Tests for extract_decorator_info function."""

    def test_extracts_simple_decorator(self) -> None:
        """Should extract simple decorator without arguments."""
        code = """
@property
def my_func():
    pass
"""
        module = astroid.parse(code)
        func = module.body[0]
        decorators = extract_decorator_info(func)
        assert len(decorators) == 1
        assert decorators[0]["name"] == "property"
        assert decorators[0]["args"] == []
        assert decorators[0]["kwargs"] == {}

    def test_extracts_decorator_with_args(self) -> None:
        """Should extract decorator with positional arguments."""
        code = """
@receiver(post_save)
def my_func():
    pass
"""
        module = astroid.parse(code)
        func = module.body[0]
        decorators = extract_decorator_info(func)
        assert len(decorators) == 1
        assert decorators[0]["name"] == "receiver"
        assert len(decorators[0]["args"]) == 1

    def test_extracts_decorator_with_kwargs(self) -> None:
        """Should extract decorator with keyword arguments."""
        code = """
@receiver(post_save, sender=User)
def my_func():
    pass
"""
        module = astroid.parse(code)
        func = module.body[0]
        decorators = extract_decorator_info(func)
        assert len(decorators) == 1
        assert decorators[0]["name"] == "receiver"
        assert "sender" in decorators[0]["kwargs"]

    def test_extracts_multiple_decorators(self) -> None:
        """Should extract multiple decorators."""
        code = """
@staticmethod
@cache
def my_func():
    pass
"""
        module = astroid.parse(code)
        func = module.body[0]
        decorators = extract_decorator_info(func)
        assert len(decorators) == 2
        names = [d["name"] for d in decorators]
        assert "staticmethod" in names
        assert "cache" in names

    def test_returns_empty_for_no_decorators(self) -> None:
        """Should return empty list for function without decorators."""
        code = """
def my_func():
    pass
"""
        module = astroid.parse(code)
        func = module.body[0]
        decorators = extract_decorator_info(func)
        assert decorators == []

    def test_extracts_from_class(self) -> None:
        """Should extract decorators from class definitions."""
        code = """
@dataclass
class MyClass:
    pass
"""
        module = astroid.parse(code)
        cls = module.body[0]
        decorators = extract_decorator_info(cls)
        assert len(decorators) == 1
        assert decorators[0]["name"] == "dataclass"


class TestGetImportInfo:
    """Tests for get_import_info function."""

    def test_extracts_simple_import(self) -> None:
        """Should extract simple import."""
        code = "import time"
        module = astroid.parse(code)
        imports = get_import_info(module)
        assert "time" in imports
        assert imports["time"] == "time"

    def test_extracts_import_with_alias(self) -> None:
        """Should extract import with alias."""
        code = "import numpy as np"
        module = astroid.parse(code)
        imports = get_import_info(module)
        assert "np" in imports
        assert imports["np"] == "numpy"

    def test_extracts_from_import(self) -> None:
        """Should extract from...import statement."""
        code = "from time import sleep"
        module = astroid.parse(code)
        imports = get_import_info(module)
        assert "sleep" in imports
        assert imports["sleep"] == "time.sleep"

    def test_extracts_from_import_with_alias(self) -> None:
        """Should extract from...import with alias."""
        code = "from time import sleep as delay"
        module = astroid.parse(code)
        imports = get_import_info(module)
        assert "delay" in imports
        assert imports["delay"] == "time.sleep"

    def test_extracts_multiple_imports(self) -> None:
        """Should extract multiple imports from one statement."""
        code = "from os import path, environ"
        module = astroid.parse(code)
        imports = get_import_info(module)
        assert "path" in imports
        assert "environ" in imports
        assert imports["path"] == "os.path"
        assert imports["environ"] == "os.environ"

    def test_handles_module_with_no_imports(self) -> None:
        """Should return empty dict for module without imports."""
        code = "x = 42"
        module = astroid.parse(code)
        imports = get_import_info(module)
        assert imports == {}


class TestSafeInferValue:
    """Tests for safe_infer_value function."""

    def test_infers_constant_value(self) -> None:
        """Should infer constant value."""
        code = "x = 42"
        module = astroid.parse(code)
        assign = module.body[0]
        value = safe_infer_value(assign.value)
        assert value == 42

    def test_returns_default_on_failure(self) -> None:
        """Should return default value on inference failure."""
        code = "x = unknown_func()"
        module = astroid.parse(code)
        assign = module.body[0]
        value = safe_infer_value(assign.value, default="N/A")
        assert value == "N/A"

    def test_returns_none_default_on_failure(self) -> None:
        """Should return None by default on failure."""
        code = "x = unknown_var"
        module = astroid.parse(code)
        assign = module.body[0]
        value = safe_infer_value(assign.value)
        assert value is None
