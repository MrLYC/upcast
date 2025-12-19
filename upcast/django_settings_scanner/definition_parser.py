"""Settings definition parsing and detection."""

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

import astroid
from astroid import nodes

if TYPE_CHECKING:
    from upcast.django_settings_scanner.settings_parser import SettingsModule


def is_settings_module(file_path: str) -> bool:
    """Check if a file is likely a settings module based on path patterns.

    Detects files in directories named 'settings/' or 'config/'.

    Args:
        file_path: Absolute or relative file path

    Returns:
        True if file is likely a settings module

    Examples:
        >>> is_settings_module("/project/myapp/settings/base.py")
        True
        >>> is_settings_module("/project/config/settings.py")
        True
        >>> is_settings_module("/project/myapp/models.py")
        False
    """
    path_lower = file_path.lower().replace("\\", "/")
    return "/settings/" in path_lower or "/config/" in path_lower


def file_path_to_module_path(file_path: str, base_path: str) -> str:
    """Convert file path to Python module path.

    Args:
        file_path: Absolute file path
        base_path: Project root path

    Returns:
        Python module path (e.g., "myproject.settings.base")

    Examples:
        >>> file_path_to_module_path("/project/myapp/settings/base.py", "/project")
        "myapp.settings.base"
        >>> file_path_to_module_path("/project/config/settings.py", "/project")
        "config.settings"
    """
    try:
        # Get relative path from base
        file_path_obj = Path(file_path)
        base_path_obj = Path(base_path)
        rel_path = file_path_obj.relative_to(base_path_obj)

        # Remove .py extension
        module_path = rel_path.with_suffix("")

        # Convert path separators to dots
        return str(module_path).replace(os.sep, ".")
    except (ValueError, Exception):
        # Fallback: just use filename without extension
        return Path(file_path).stem


def is_uppercase_identifier(name: str) -> bool:
    """Check if a name follows uppercase settings naming convention.

    Args:
        name: Variable name to check

    Returns:
        True if name is all uppercase (underscores allowed), excluding dunder names

    Examples:
        >>> is_uppercase_identifier("DEBUG")
        True
        >>> is_uppercase_identifier("DATABASE_URL")
        True
        >>> is_uppercase_identifier("debug")
        False
        >>> is_uppercase_identifier("__name__")
        False
    """
    if not name:
        return False

    # Exclude dunder names
    if name.startswith("__") and name.endswith("__"):
        return False

    # Check if all characters are uppercase or underscore
    return name.isupper() and name.replace("_", "").isalnum()


def is_uppercase_assignment(node: nodes.Assign) -> bool:
    """Check if an assignment node assigns to an uppercase variable.

    Args:
        node: Assignment AST node

    Returns:
        True if assigns to an uppercase identifier

    Examples:
        Assignment nodes for:
        - "DEBUG = True" -> True
        - "debug = True" -> False
        - "A = B = True" -> True (multiple targets)
    """
    if not node.targets:
        return False

    # Check first target (most common case)
    target = node.targets[0]

    if isinstance(target, nodes.AssignName):
        return is_uppercase_identifier(target.name)

    return False


def extract_assignment_target(node: nodes.Assign) -> str | None:
    """Extract variable name from an assignment node.

    Args:
        node: Assignment AST node

    Returns:
        Variable name or None if cannot extract

    Examples:
        - "DEBUG = True" -> "DEBUG"
        - "A = B = C" -> "A" (first target)
    """
    if not node.targets:
        return None

    target = node.targets[0]

    if isinstance(target, nodes.AssignName):
        return target.name

    return None


def infer_setting_value(node: nodes.NodeNG) -> dict[str, Any]:  # noqa: C901
    """Infer value and type from an AST node.

    Uses astroid inference to extract literal values safely without evaluation.
    Complex expressions that cannot be resolved are marked as dynamic with
    the expression wrapped in backticks.

    Args:
        node: AST node representing the value

    Returns:
        Dictionary with 'value' and 'type' keys

    Examples:
        >>> # DEBUG = True
        >>> infer_setting_value(const_true_node)
        {'value': True, 'type': 'bool'}

        >>> # PORT = 8000
        >>> infer_setting_value(const_8000_node)
        {'value': 8000, 'type': 'int'}

        >>> # SECRET = os.environ.get("KEY")
        >>> infer_setting_value(call_node)
        {'value': '`os.environ.get("KEY")`', 'type': 'dynamic'}
    """
    try:
        # Try to infer the value using astroid
        inferred_values = list(node.infer())

        # Filter out Uninferable
        inferred_values = [v for v in inferred_values if v is not astroid.Uninferable]

        if not inferred_values:
            # Cannot infer - mark as dynamic
            return {"value": f"`{node.as_string()}`", "type": "dynamic"}

        # Use first inferred value
        inferred = inferred_values[0]

        # Handle Const nodes (literals)
        if isinstance(inferred, nodes.Const):
            value = inferred.value
            if value is None:
                return {"value": None, "type": "none"}
            elif isinstance(value, bool):
                return {"value": value, "type": "bool"}
            elif isinstance(value, int):
                return {"value": value, "type": "int"}
            elif isinstance(value, float):
                return {"value": value, "type": "float"}
            elif isinstance(value, str):
                return {"value": value, "type": "string"}
            else:
                # Other const types - wrap in backticks
                return {"value": f"`{node.as_string()}`", "type": "literal"}

        # Handle List nodes
        if isinstance(inferred, nodes.List):
            try:
                elements = []
                for elt in inferred.elts:
                    elt_result = infer_setting_value(elt)
                    if elt_result["type"] in ("dynamic", "call"):
                        # Contains dynamic elements - mark whole list as dynamic
                        return {"value": f"`{node.as_string()}`", "type": "list"}
                    elements.append(elt_result["value"])
            except Exception:
                return {"value": f"`{node.as_string()}`", "type": "list"}
            else:
                return {"value": elements, "type": "list"}

        # Handle Tuple nodes
        if isinstance(inferred, nodes.Tuple):
            try:
                elements = []
                for elt in inferred.elts:
                    elt_result = infer_setting_value(elt)
                    if elt_result["type"] in ("dynamic", "call"):
                        return {"value": f"`{node.as_string()}`", "type": "tuple"}
                    elements.append(elt_result["value"])
            except Exception:
                return {"value": f"`{node.as_string()}`", "type": "tuple"}
            else:
                return {"value": elements, "type": "tuple"}

        # Handle Dict nodes
        if isinstance(inferred, nodes.Dict):
            try:
                result = {}
                if inferred.items:
                    for key_node, value_node in inferred.items:
                        key_result = infer_setting_value(key_node)
                        value_result = infer_setting_value(value_node)

                        if key_result["type"] in ("dynamic", "call") or value_result["type"] in ("dynamic", "call"):
                            # Contains dynamic - mark whole dict as dynamic
                            return {"value": f"`{node.as_string()}`", "type": "dict"}

                        # Use key value as dict key (must be hashable)
                        key = key_result["value"]
                        if isinstance(key, (str, int, float, bool, type(None))):
                            result[key] = value_result["value"]
                        else:
                            # Non-hashable key - mark as dynamic
                            return {"value": f"`{node.as_string()}`", "type": "dict"}
            except Exception:
                return {"value": f"`{node.as_string()}`", "type": "dict"}
            else:
                return {"value": result, "type": "dict"}

        # Handle Set nodes
        if isinstance(inferred, nodes.Set):
            try:
                elements = []
                for elt in inferred.elts:
                    elt_result = infer_setting_value(elt)
                    if elt_result["type"] in ("dynamic", "call"):
                        return {"value": f"`{node.as_string()}`", "type": "set"}
                    elements.append(elt_result["value"])
            except Exception:
                return {"value": f"`{node.as_string()}`", "type": "set"}
            else:
                # Convert to list for JSON serialization (sets aren't JSON-serializable)
                return {"value": elements, "type": "set"}

        # If we reach here, it's some other type we can't handle
        # Mark as dynamic
        return {"value": f"`{node.as_string()}`", "type": "dynamic"}

    except Exception:
        # Any error during inference - mark as dynamic
        return {"value": f"`{node.as_string()}`", "type": "dynamic"}


def detect_star_imports(module: nodes.Module) -> list[str]:
    """Detect star imports (from X import *) in a module.

    Args:
        module: Parsed AST module

    Returns:
        List of module paths that are star-imported (including relative import dots)
    """
    star_imports = []

    for node in module.body:
        # Look for ImportFrom nodes
        if not isinstance(node, nodes.ImportFrom):
            continue

        # Check if it's a star import
        if not any(name == "*" for name, _ in node.names):
            continue

        # Build the import path including relative dots
        if node.level:
            # Relative import - add dots
            import_path = "." * node.level
            if node.modname:
                import_path += node.modname
        else:
            # Absolute import
            import_path = node.modname

        if import_path:
            star_imports.append(import_path)

    return star_imports


def mark_overrides(modules: dict[str, "SettingsModule"], current_module_path: str) -> None:
    """Mark settings definitions that override imported base settings.

    Args:
        modules: Dictionary of all parsed settings modules
        current_module_path: Module path being processed

    This function:
    1. Looks at star imports in the current module
    2. For each setting defined in current module
    3. If that setting exists in a star-imported module, mark as override
    """
    if current_module_path not in modules:
        return

    current_module = modules[current_module_path]

    # For each star import, check if definitions override base settings
    for star_import in current_module.star_imports:
        # Skip if base module not found
        if star_import not in modules:
            continue

        base_module = modules[star_import]

        # For each setting in current module
        for setting_name, setting_def in current_module.definitions.items():
            # If this setting exists in the base module
            if setting_name in base_module.definitions:
                # Mark as override
                setting_def.overrides = star_import


def extract_import_pattern(call_node: nodes.Call) -> str | None:  # noqa: C901
    """Extract import pattern string from importlib.import_module() call.

    Args:
        call_node: Call node for importlib.import_module()

    Returns:
        Pattern string or None if cannot extract
    """
    if not call_node.args:
        return None

    arg = call_node.args[0]

    # Handle f-strings (JoinedStr)
    if isinstance(arg, nodes.JoinedStr):
        # Reconstruct the pattern with {placeholders}
        parts = []
        for value in arg.values:
            if isinstance(value, nodes.Const):
                # String literal part
                parts.append(value.value)
            elif isinstance(value, nodes.FormattedValue):
                # Dynamic part - use placeholder
                parts.append("{}")
        return "".join(parts)

    # Handle string concatenation (BinOp with +)
    if isinstance(arg, nodes.BinOp) and arg.op == "+":
        # Try to extract the pattern
        parts = []
        if isinstance(arg.left, nodes.Const):
            parts.append(arg.left.value)
        else:
            parts.append("{}")

        if isinstance(arg.right, nodes.Const):
            parts.append(arg.right.value)
        else:
            parts.append("{}")

        return "".join(parts)

    # Handle .format() calls
    if (
        isinstance(arg, nodes.Call)
        and isinstance(arg.func, nodes.Attribute)
        and arg.func.attrname == "format"
        and isinstance(arg.func.expr, nodes.Const)
    ):
        # Get the string being formatted
        return arg.func.expr.value

    # Handle simple string literal
    if isinstance(arg, nodes.Const) and isinstance(arg.value, str):
        return arg.value

    return None


def extract_base_module(pattern: str) -> str | None:
    """Extract base module from dynamic import pattern.

    Args:
        pattern: Import pattern (e.g., "settings.{env}")

    Returns:
        Base module path before dynamic part, or None if too dynamic
    """
    # Find the first dynamic placeholder
    placeholder_pos = pattern.find("{}")
    if placeholder_pos == -1:
        # No placeholder, return the whole thing
        return pattern

    if placeholder_pos == 0:
        # Starts with placeholder - too dynamic
        return None

    # Get everything before the placeholder
    base = pattern[:placeholder_pos]

    # Remove trailing dot if present
    if base.endswith("."):
        base = base[:-1]

    # Return base if it looks like a module path
    if base and not base.startswith("."):
        return base

    return None


def detect_dynamic_imports(module: nodes.Module, file_path: str) -> list:
    """Detect dynamic import patterns using importlib.import_module.

    Args:
        module: Parsed AST module
        file_path: File path for context

    Returns:
        List of detected dynamic imports
    """
    # Import at function level to avoid circular import
    from upcast.django_settings_scanner.settings_parser import DynamicImport

    dynamic_imports = []

    for node in module.nodes_of_class(nodes.Call):
        # Check if it's importlib.import_module call
        if not isinstance(node.func, nodes.Attribute):
            continue

        # Check for importlib.import_module pattern
        if not (
            node.func.attrname == "import_module"
            and isinstance(node.func.expr, nodes.Name)
            and node.func.expr.name == "importlib"
        ):
            continue

        # Extract the pattern
        pattern = extract_import_pattern(node)
        if not pattern:
            continue

        base_module = extract_base_module(pattern)

        # Create DynamicImport record
        dynamic_imports.append(
            DynamicImport(
                pattern=pattern,
                base_module=base_module,
                file=file_path,
                line=node.lineno,
            )
        )

    return dynamic_imports


def parse_settings_module(file_path: str, base_path: str) -> "SettingsModule":
    """Parse a settings module file and extract all definitions.

    Args:
        file_path: Absolute path to the settings file
        base_path: Project root path for module path calculation

    Returns:
        SettingsModule with all definitions, imports, and metadata
    """
    from upcast.django_settings_scanner.settings_parser import SettingsDefinition, SettingsModule

    # Read and parse the file
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    module = astroid.parse(content, path=file_path)

    # Get module path for this file
    module_path = file_path_to_module_path(file_path, base_path)

    # Initialize collections
    definitions: dict[str, SettingsDefinition] = {}

    # Scan for uppercase assignments
    for node in module.body:
        if not isinstance(node, nodes.Assign):
            continue

        if not is_uppercase_assignment(node):
            continue

        # Extract variable name
        var_name = extract_assignment_target(node)
        if not var_name:
            continue

        # Infer value
        value_info = infer_setting_value(node.value)

        # Create definition
        definitions[var_name] = SettingsDefinition(
            name=var_name,
            value=value_info["value"],
            line=node.lineno,
            type=value_info["type"],
            module_path=module_path,
            overrides=None,  # Will be set by mark_overrides
        )

    # Detect star imports
    star_imports_raw = detect_star_imports(module)

    # Resolve relative imports to absolute paths
    star_imports = []
    for import_path in star_imports_raw:
        if import_path.startswith("."):
            # Relative import - resolve it
            from upcast.django_settings_scanner.ast_utils import resolve_relative_import

            # Count dots
            level = len(import_path) - len(import_path.lstrip("."))
            # Get module name after dots
            import_module = import_path.lstrip(".") if import_path.lstrip(".") else None

            resolved = resolve_relative_import(module_path, level, import_module)
            star_imports.append(resolved)
        else:
            # Absolute import
            star_imports.append(import_path)

    # Detect dynamic imports
    dynamic_imports = detect_dynamic_imports(module, file_path)

    # Build and return SettingsModule
    return SettingsModule(
        module_path=module_path,
        definitions=definitions,
        star_imports=star_imports,
        dynamic_imports=dynamic_imports,
    )
