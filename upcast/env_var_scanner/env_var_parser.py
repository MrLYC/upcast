"""Core parsing logic for environment variable patterns."""

from dataclasses import dataclass, field
from typing import Any, Optional

from astroid import nodes

from upcast.env_var_scanner.ast_utils import (
    infer_literal_value,
    infer_type_from_value,
    is_env_var_call,
    resolve_string_concat,
    safe_as_string,
)


@dataclass
class EnvVarUsage:
    """Represents a single usage of an environment variable."""

    name: str
    location: str  # Format: "file.py:line"
    statement: str
    type: Optional[str] = None
    default: Optional[Any] = None
    required: bool = False
    node: Optional[nodes.NodeNG] = field(default=None, repr=False)


@dataclass
class EnvVarInfo:
    """Aggregated information about an environment variable."""

    name: str
    types: list[str] = field(default_factory=list)
    defaults: list[Any] = field(default_factory=list)
    usages: list[EnvVarUsage] = field(default_factory=list)
    required: bool = False  # True if ANY usage is required

    def add_usage(self, usage: EnvVarUsage) -> None:
        """Add a usage and update aggregated fields."""
        self.usages.append(usage)

        if usage.type and usage.type not in self.types:
            self.types.append(usage.type)

        # Add default if present (including None) and not a dynamic expression
        # Skip backtick-wrapped dynamic expressions
        is_dynamic = isinstance(usage.default, str) and usage.default.startswith("`") and usage.default.endswith("`")
        if not is_dynamic:
            # Use identity and type checking for precise duplicate detection
            # This ensures False != 0, True != 1, etc.
            already_present = any(
                default is usage.default or (default == usage.default and type(default) is type(usage.default))
                for default in self.defaults
            )
            if not already_present:
                self.defaults.append(usage.default)

        if usage.required:
            self.required = True


def parse_env_var_usage(node: nodes.Call, file_path: str) -> Optional[EnvVarUsage]:  # noqa: C901
    """Parse a Call node to extract environment variable usage information.

    Args:
        node: An astroid Call node
        file_path: Path to the file being analyzed

    Returns:
        EnvVarUsage object or None if not an env var call
    """
    # First, check if this is actually an env var call
    if not is_env_var_call(node):
        return None

    func_str = safe_as_string(node.func)

    # Extract variable name from first argument
    if not node.args:
        return None

    name_arg = node.args[0]
    var_name = None

    # Try to extract string literal or resolve concatenation
    var_name = name_arg.value if isinstance(name_arg, nodes.Const) else resolve_string_concat(name_arg)

    if not var_name or not isinstance(var_name, str):
        return None

    # Determine location
    location = f"{file_path}:{node.lineno}"
    statement = safe_as_string(node)

    # Detect pattern type and extract metadata
    var_type: Optional[str] = None
    default: Optional[str] = None
    required = False

    # Check for os.environ[KEY] pattern (required, no default)
    if "os.environ[" in func_str or "environ[" in func_str:
        # This is actually a subscript, not a call - but we'll handle it in checker
        return None

    # Check for os.getenv patterns
    if "getenv" in func_str:
        # os.getenv(KEY) - not required (implicit None default)
        # os.getenv(KEY, default) - not required
        if len(node.args) > 1:
            default_node = node.args[1]
            default = infer_literal_value(default_node)
            var_type = infer_type_from_value(default_node)
        else:
            var_type = "str"  # Default type for getenv without conversion
        required = False

    # Check for os.environ.get patterns
    elif "environ.get" in func_str:
        if len(node.args) > 1:
            default_node = node.args[1]
            default = infer_literal_value(default_node)
            var_type = infer_type_from_value(default_node)
        else:
            var_type = "str"
        required = False

    # Check for django-environ patterns: env.TYPE(KEY)
    elif "env." in func_str:
        # Extract type from method name
        parts = func_str.split(".")
        if len(parts) >= 2:
            method_name = parts[-1].split("(")[0]
            if method_name in ["str", "int", "bool", "float", "list", "dict", "json"]:
                var_type = method_name

        # Check for default parameter
        if node.keywords:
            for keyword in node.keywords:
                if keyword.arg == "default":
                    default = infer_literal_value(keyword.value)
                    if not var_type:
                        var_type = infer_type_from_value(keyword.value)
        elif len(node.args) > 1:
            default_node = node.args[1]
            default = infer_literal_value(default_node)
            if not var_type:
                var_type = infer_type_from_value(default_node)

        required = default is None

    # Check for env(KEY) without type method
    elif func_str == "env" or func_str.endswith("env("):
        # Check for default
        if node.keywords:
            for keyword in node.keywords:
                if keyword.arg == "default":
                    default = infer_literal_value(keyword.value)
                    var_type = infer_type_from_value(keyword.value)
        elif len(node.args) > 1:
            default_node = node.args[1]
            default = infer_literal_value(default_node)
            var_type = infer_type_from_value(default_node)

        required = default is None

    # Check if wrapped in type conversion: int(os.getenv(...))
    parent = node.parent
    if isinstance(parent, nodes.Call):
        parent_func = safe_as_string(parent.func)
        if parent_func in ["int", "float", "bool", "str", "list", "dict"]:
            var_type = parent_func

    # Check for 'or' expression: env('X') or default
    if isinstance(parent, nodes.BoolOp) and parent.op == "or":
        # Find the default value (right operand)
        for value in parent.values:
            if value != node:
                default = infer_literal_value(value)
                var_type = infer_type_from_value(value)
                required = False
                break

    return EnvVarUsage(
        name=var_name,
        location=location,
        statement=statement,
        type=var_type,
        default=default,
        required=required,
        node=node,
    )
