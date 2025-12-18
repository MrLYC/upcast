"""Parser for test function analysis and metadata extraction."""

import hashlib
import logging
from dataclasses import dataclass, field

from astroid import nodes

logger = logging.getLogger(__name__)


@dataclass
class TargetModule:
    """Information about a module targeted by a test."""

    module: str
    symbols: list[str] = field(default_factory=list)


@dataclass
class UnitTestInfo:
    """Information about a single test function."""

    name: str
    location: str  # "file.py:line"
    file: str
    line: int
    line_range: tuple[int, int]  # (start_line, end_line)
    body_md5: str
    assert_count: int
    targets: list[TargetModule] = field(default_factory=list)


def normalize_code(code: str) -> str:
    """Normalize code for MD5 calculation.

    Strips comments and normalizes whitespace while preserving semantics.

    Args:
        code: Source code to normalize

    Returns:
        Normalized code string
    """
    lines = []
    for line in code.split("\n"):
        # Remove inline comments
        if "#" in line:
            # Simple approach: split on # (doesn't handle strings perfectly)
            line = line.split("#")[0]
        # Strip trailing whitespace
        line = line.rstrip()
        # Skip empty lines
        if line:
            lines.append(line)
    return "\n".join(lines)


def calculate_body_md5(func_node: nodes.FunctionDef) -> str:
    """Calculate MD5 hash of normalized function body.

    Args:
        func_node: Function definition node

    Returns:
        MD5 hash as hex string
    """
    # Get function body source
    body_code = func_node.as_string()

    # Normalize code
    normalized = normalize_code(body_code)

    # Calculate MD5
    md5_hash = hashlib.md5(normalized.encode("utf-8")).hexdigest()  # noqa: S324

    return md5_hash


def count_assertions(func_node: nodes.FunctionDef) -> int:
    """Count assertion statements in a test function.

    Counts both pytest-style assert statements and unittest-style self.assert* calls.

    Args:
        func_node: Function definition node

    Returns:
        Total assertion count
    """
    count = 0

    # Count pytest assert statements
    for _assert_node in func_node.nodes_of_class(nodes.Assert):
        count += 1

    # Count unittest style assertions (self.assertEqual, etc.)
    for call_node in func_node.nodes_of_class(nodes.Call):
        if (
            isinstance(call_node.func, nodes.Attribute)
            and isinstance(call_node.func.expr, nodes.Name)
            and call_node.func.expr.name == "self"
            and call_node.func.attrname.startswith("assert")
        ):
            count += 1

    # Count pytest.raises context managers
    for with_node in func_node.nodes_of_class(nodes.With):
        for item in with_node.items:
            if (
                isinstance(item[0], nodes.Call)
                and isinstance(item[0].func, nodes.Attribute)
                and item[0].func.attrname == "raises"
            ):
                count += 1

    return count


def extract_imports(module: nodes.Module) -> dict[str, str]:
    """Extract import mappings from module.

    Args:
        module: Module node

    Returns:
        Dictionary mapping local names to fully qualified module paths
    """
    imports = {}

    # Handle "import X" and "import X as Y"
    for import_node in module.nodes_of_class(nodes.Import):
        for name, alias in import_node.names:
            local_name = alias if alias else name
            imports[local_name] = name

    # Handle "from X import Y" and "from X import Y as Z"
    for import_from in module.nodes_of_class(nodes.ImportFrom):
        module_name = import_from.modname or ""
        for name, alias in import_from.names:
            local_name = alias if alias else name
            if name == "*":
                # Wildcard import - map to module
                imports[f"*from:{module_name}"] = module_name
            else:
                # Specific import
                full_name = f"{module_name}.{name}" if module_name else name
                imports[local_name] = full_name

    return imports


def resolve_targets(
    func_node: nodes.FunctionDef,
    module_imports: dict[str, str],
    root_modules: list[str] | None = None,
) -> list[TargetModule]:
    """Resolve test targets based on used names and root modules.

    Args:
        func_node: Function definition node
        module_imports: Import mapping (name -> module)
        root_modules: Root module prefixes to match (None = match all)

    Returns:
        List of target modules with symbols
    """
    # Collect all names used in the function
    used_names: set[str] = set()

    for name_node in func_node.nodes_of_class(nodes.Name):
        used_names.add(name_node.name)

    # Map names to modules
    targets: dict[str, set[str]] = {}
    for name in used_names:
        if name in module_imports:
            full_path = module_imports[name]
            # Extract module from full path (e.g., "app.math_utils.add" -> "app.math_utils")
            parts = full_path.rsplit(".", 1)
            if len(parts) == 2:
                module, symbol = parts
            else:
                module, symbol = full_path, name

            # If root_modules is None or empty, collect all imports
            if not root_modules:
                if module not in targets:
                    targets[module] = set()
                targets[module].add(symbol)
            else:
                # Check if module matches any root module prefix
                for root in root_modules:
                    if module.startswith(root):
                        if module not in targets:
                            targets[module] = set()
                        targets[module].add(symbol)
                        break

    # Convert to TargetModule list
    return [TargetModule(module=module, symbols=sorted(symbols)) for module, symbols in sorted(targets.items())]


def parse_test_function(
    func_node: nodes.FunctionDef,
    file_path: str,
    module_imports: dict[str, str],
    root_modules: list[str] | None = None,
) -> UnitTestInfo:
    """Parse a test function and extract metadata.

    Args:
        func_node: Function definition node
        file_path: Path to the test file
        module_imports: Import mappings
        root_modules: List of root module prefixes (None = match all)

    Returns:
        UnitTestInfo with all metadata
    """
    name = func_node.name
    line = func_node.lineno
    end_line = func_node.end_lineno or line
    location = f"{file_path}:{line}"

    # Calculate MD5
    body_md5 = calculate_body_md5(func_node)

    # Count assertions
    assert_count = count_assertions(func_node)

    # Resolve targets
    targets = resolve_targets(func_node, module_imports, root_modules)

    return UnitTestInfo(
        name=name,
        location=location,
        file=file_path,
        line=line,
        line_range=(line, end_line),
        body_md5=body_md5,
        assert_count=assert_count,
        targets=targets,
    )
