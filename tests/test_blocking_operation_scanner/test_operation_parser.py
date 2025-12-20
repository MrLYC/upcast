"""Tests for operation_parser module."""

from pathlib import Path

import astroid

from upcast.blocking_operation_scanner.operation_parser import (
    OperationType,
    extract_function_context,
    extract_imports,
    extract_literal_value,
    get_statement_code,
    parse_lock_acquire,
    parse_lock_context,
    parse_select_for_update,
    parse_sleep_operation,
    parse_subprocess_operation,
)


def test_get_statement_code():
    """Test extracting source code from AST node."""
    code = "time.sleep(5)"
    module = astroid.parse(code)
    call_node = next(iter(module.nodes_of_class(astroid.Call)))

    result = get_statement_code(call_node)
    assert "sleep" in result
    assert "5" in result


def test_extract_literal_value():
    """Test extracting literal values."""
    code = "5"
    module = astroid.parse(code)
    const_node = next(iter(module.nodes_of_class(astroid.Const)))

    result = extract_literal_value(const_node)
    assert result == 5


def test_extract_literal_value_non_const():
    """Test extracting non-literal values returns None."""
    code = "x"
    module = astroid.parse(code)
    name_node = next(iter(module.nodes_of_class(astroid.Name)))

    result = extract_literal_value(name_node)
    assert result is None


def test_extract_function_context():
    """Test extracting function and class context."""
    code = """
class MyClass:
    def my_method(self):
        time.sleep(1)
"""
    module = astroid.parse(code)
    call_node = next(iter(module.nodes_of_class(astroid.Call)))

    function, class_name, is_async = extract_function_context(call_node)
    assert function == "my_method"
    assert class_name == "MyClass"
    assert is_async is False


def test_extract_function_context_async():
    """Test extracting async function context."""
    code = """
async def async_func():
    time.sleep(1)
"""
    module = astroid.parse(code)
    call_node = next(iter(module.nodes_of_class(astroid.Call)))

    function, class_name, is_async = extract_function_context(call_node)
    assert function == "async_func"
    assert class_name is None
    assert is_async is True


def test_parse_sleep_operation():
    """Test parsing time.sleep() operations."""
    code = "time.sleep(5)"
    module = astroid.parse(code)
    call_node = next(iter(module.nodes_of_class(astroid.Call)))
    imports = {"time": "time"}

    result = parse_sleep_operation(call_node, Path("test.py"), imports)

    assert result is not None
    assert result.type == OperationType.TIME_SLEEP
    assert result.duration == 5


def test_parse_sleep_operation_imported():
    """Test parsing imported sleep()."""
    code = "sleep(10)"
    module = astroid.parse(code)
    call_node = next(iter(module.nodes_of_class(astroid.Call)))
    imports = {"sleep": "time"}

    result = parse_sleep_operation(call_node, Path("test.py"), imports)

    assert result is not None
    assert result.type == OperationType.TIME_SLEEP
    assert result.duration == 10


def test_parse_sleep_operation_variable_duration():
    """Test parsing sleep with variable duration."""
    code = "time.sleep(timeout)"
    module = astroid.parse(code)
    call_node = next(iter(module.nodes_of_class(astroid.Call)))
    imports = {"time": "time"}

    result = parse_sleep_operation(call_node, Path("test.py"), imports)

    assert result is not None
    assert result.type == OperationType.TIME_SLEEP
    assert result.duration == "timeout"


def test_parse_select_for_update():
    """Test parsing select_for_update() operations."""
    code = "Model.objects.filter().select_for_update()"
    module = astroid.parse(code)
    call_nodes = list(module.nodes_of_class(astroid.Call))
    sfu_call = next(n for n in call_nodes if hasattr(n.func, "attrname") and n.func.attrname == "select_for_update")

    result = parse_select_for_update(sfu_call, Path("test.py"))

    assert result is not None
    assert result.type == OperationType.DB_SELECT_FOR_UPDATE


def test_parse_select_for_update_with_timeout():
    """Test parsing select_for_update with timeout parameter."""
    code = "Model.objects.select_for_update(timeout=30)"
    module = astroid.parse(code)
    call_nodes = list(module.nodes_of_class(astroid.Call))
    sfu_call = next(n for n in call_nodes if hasattr(n.func, "attrname") and n.func.attrname == "select_for_update")

    result = parse_select_for_update(sfu_call, Path("test.py"))

    assert result is not None
    assert result.timeout == 30


def test_parse_lock_acquire():
    """Test parsing Lock().acquire() operations."""
    code = "threading.Lock().acquire()"
    module = astroid.parse(code)
    call_nodes = list(module.nodes_of_class(astroid.Call))
    acquire_call = next(n for n in call_nodes if hasattr(n.func, "attrname") and n.func.attrname == "acquire")
    imports = {"threading": "threading"}

    result = parse_lock_acquire(acquire_call, Path("test.py"), imports)

    assert result is not None
    assert result.type == OperationType.LOCK_ACQUIRE


def test_parse_lock_acquire_with_timeout():
    """Test parsing acquire with timeout."""
    code = "threading.Lock().acquire(timeout=5)"
    module = astroid.parse(code)
    call_nodes = list(module.nodes_of_class(astroid.Call))
    acquire_call = next(n for n in call_nodes if hasattr(n.func, "attrname") and n.func.attrname == "acquire")
    imports = {"threading": "threading"}

    result = parse_lock_acquire(acquire_call, Path("test.py"), imports)

    assert result is not None
    assert result.timeout == 5


def test_parse_lock_context():
    """Test parsing lock context managers."""
    code = "with threading.Lock(): pass"
    module = astroid.parse(code)
    with_node = next(iter(module.nodes_of_class(astroid.With)))
    imports = {"threading": "threading"}

    results = parse_lock_context(with_node, Path("test.py"), imports)

    assert len(results) == 1
    assert results[0].type == OperationType.LOCK_CONTEXT


def test_parse_subprocess_run():
    """Test parsing subprocess.run() operations."""
    code = "subprocess.run(['ls'])"
    module = astroid.parse(code)
    call_node = next(iter(module.nodes_of_class(astroid.Call)))
    imports = {"subprocess": "subprocess"}

    result = parse_subprocess_operation(call_node, Path("test.py"), imports)

    assert result is not None
    assert result.type == OperationType.SUBPROCESS_RUN


def test_parse_subprocess_run_with_timeout():
    """Test parsing subprocess.run with timeout."""
    code = "subprocess.run(['ls'], timeout=30)"
    module = astroid.parse(code)
    call_node = next(iter(module.nodes_of_class(astroid.Call)))
    imports = {"subprocess": "subprocess"}

    result = parse_subprocess_operation(call_node, Path("test.py"), imports)

    assert result is not None
    assert result.timeout == 30


def test_parse_subprocess_wait():
    """Test parsing Popen.wait() operations."""
    code = "proc.wait()"
    module = astroid.parse(code)
    call_node = next(iter(module.nodes_of_class(astroid.Call)))
    imports = {}

    result = parse_subprocess_operation(call_node, Path("test.py"), imports)

    assert result is not None
    assert result.type == OperationType.SUBPROCESS_WAIT


def test_parse_subprocess_communicate():
    """Test parsing Popen.communicate() operations."""
    code = "proc.communicate()"
    module = astroid.parse(code)
    call_node = next(iter(module.nodes_of_class(astroid.Call)))
    imports = {}

    result = parse_subprocess_operation(call_node, Path("test.py"), imports)

    assert result is not None
    assert result.type == OperationType.SUBPROCESS_COMMUNICATE


def test_extract_imports():
    """Test extracting import mappings."""
    code = """
import time
import subprocess
from threading import Lock
from time import sleep as sleeper
"""
    module = astroid.parse(code)

    result = extract_imports(module)

    assert result["time"] == "time"
    assert result["subprocess"] == "subprocess"
    assert result["Lock"] == "threading"
    assert result["sleeper"] == "time"
