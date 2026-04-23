"""Environment variable scanner with Pydantic models."""

import time
from pathlib import Path

from astroid import nodes

from upcast.common.ast_utils import get_import_info, safe_as_string
from upcast.common.file_utils import get_relative_path_str
from upcast.common.inference import infer_string_pattern, infer_type, infer_value
from upcast.common.scanner_base import BaseScanner
from upcast.models.env_vars import EnvVarInfo, EnvVarLocation, EnvVarOutput, EnvVarSummary

SUPPORTED_GETENV_MODULES = {"os"}
SUPPORTED_ENVIRON_MODULES = {"os"}


class EnvVarScanner(BaseScanner[EnvVarOutput]):
    """Scanner for environment variable usage (os.environ, os.getenv, etc.)."""

    def __init__(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ):
        """Initialize scanner."""
        super().__init__(include_patterns, exclude_patterns, verbose)
        self.base_path: Path | None = None
        self.env_vars: dict[str, EnvVarInfo] = {}

    def scan(self, path: Path) -> EnvVarOutput:
        """Scan for environment variable usage."""
        start_time = time.time()
        self.base_path = path.resolve() if path.is_dir() else path.parent.resolve()
        self.env_vars = {}

        files = self.get_files_to_scan(path)
        for file_path in files:
            self._scan_file(file_path)

        summary = self._calculate_summary(
            files_scanned=len(files),
            scan_duration_ms=int((time.time() - start_time) * 1000),
        )

        return EnvVarOutput(
            summary=summary,
            results=self.env_vars,
            metadata={"scanner_name": "env-vars"},
        )

    def scan_file(self, file_path: Path) -> None:
        """Scan a single file (compatibility method)."""
        self._scan_file(file_path)

    def _scan_file(self, file_path: Path) -> None:
        """Internal method to scan a single file."""
        module = self.parse_file(file_path)
        if not module:
            return

        # Get import information for this module
        imports = get_import_info(module)
        relative_path = get_relative_path_str(file_path, self.base_path or Path.cwd())

        # Visit all Call and Subscript nodes
        for node in module.nodes_of_class((nodes.Call, nodes.Subscript)):
            if isinstance(node, nodes.Call):
                self._check_getenv_call(node, relative_path, imports)
            elif isinstance(node, nodes.Subscript):
                self._check_environ_subscript(node, relative_path, imports)

    def _check_getenv_call(self, node: nodes.Call, file_path: str, imports: dict[str, str]) -> None:
        """Check if Call node is os.getenv() or similar."""
        if not self._is_supported_getenv_call(node.func, imports):
            return

        # Extract variable name
        if not node.args:
            return
        var_name = infer_value(node.args[0]).get_if_type(str)
        if var_name is None:
            return

        if not var_name:
            var_name = "..."

        # Extract default value
        is_environ_get = self._is_supported_environ_get(node.func, imports)
        default_value, required, inferred_type = self._extract_default_details(node, is_environ_get, imports)

        # Create location and add to results
        location = EnvVarLocation(
            file=file_path,
            line=node.lineno,
            column=getattr(node, "col_offset", None),
            statement=safe_as_string(node),
            pattern=safe_as_string(node),
            code=safe_as_string(node),
            type=inferred_type,
        )
        self._add_env_var(
            name=var_name,
            required=required,
            default_value=str(default_value) if default_value is not None else None,
            location=location,
        )

    def _check_environ_subscript(self, node: nodes.Subscript, file_path: str, imports: dict[str, str]) -> None:
        """Check if Subscript node is os.environ['KEY'] or similar."""
        if not self._is_supported_environ_value(node.value, imports):
            return

        # Skip Del statements
        parent = node.parent
        while parent:
            if isinstance(parent, nodes.Delete):
                return
            if isinstance(parent, (nodes.Module, nodes.FunctionDef, nodes.ClassDef)):
                break
            parent = parent.parent

        # Extract key (must be string literal)
        if not isinstance(node.slice, nodes.Const) or not isinstance(node.slice.value, str):
            return

        # Create location and add to results (always required)
        location = EnvVarLocation(
            file=file_path,
            line=node.lineno,
            column=getattr(node, "col_offset", None),
            statement=safe_as_string(node),
            pattern=safe_as_string(node),
            code=safe_as_string(node),
            type=self._infer_env_var_type(node),
        )
        self._add_env_var(
            name=node.slice.value,
            required=True,
            default_value=None,
            location=location,
        )

    def _add_env_var(
        self,
        name: str,
        required: bool,
        default_value: str | None,
        location: EnvVarLocation,
    ) -> None:
        """Add environment variable to results."""
        if name not in self.env_vars:
            self.env_vars[name] = EnvVarInfo(
                name=name,
                required=required,
                default_value=default_value,
                defaults=[],
                types=[],
                locations=[],
            )

        existing_info = self.env_vars[name]
        if not self._has_location(existing_info.locations, location):
            existing_info.locations.append(location)

        # Aggregate types from locations
        if location.type == "unknown" and any(existing_type != "unknown" for existing_type in existing_info.types):
            pass
        elif location.type and location.type not in existing_info.types:
            if location.type != "unknown":
                existing_info.types = [
                    existing_type for existing_type in existing_info.types if existing_type != "unknown"
                ]
            existing_info.types.append(location.type)

        # Update required status (if ANY usage is required, mark as required)
        if required:
            existing_info.required = True

        # Preserve all defaults while keeping first default_value as compatibility alias
        if default_value is not None:
            if default_value not in existing_info.defaults:
                existing_info.defaults.append(default_value)
            if existing_info.default_value is None:
                existing_info.default_value = default_value

    def _has_location(self, existing_locations: list[EnvVarLocation], location: EnvVarLocation) -> bool:
        """Return True when the exact same location record already exists."""
        for existing in existing_locations:
            if (
                existing.file == location.file
                and existing.line == location.line
                and existing.statement == location.statement
            ):
                return True
        return False

    def _infer_env_var_type(self, node: nodes.NodeNG) -> str:
        """Infer environment variable type from explicit conversion or exact default value."""
        parent = node.parent
        if isinstance(parent, nodes.Call) and node in parent.args:
            conversion_type = self._infer_conversion_type(parent.func)
            if conversion_type != "unknown":
                return conversion_type

        return "str"

    def _extract_default_details(
        self,
        node: nodes.Call,
        is_environ_get: bool = False,
        imports: dict[str, str] | None = None,
    ) -> tuple[object | None, bool, str]:
        """Extract default value metadata and inferred type for getenv-like calls."""
        inferred_type = self._infer_env_var_type(node)
        default_node = self._get_default_node(node)
        if default_node is None:
            if inferred_type == "unknown":
                inferred_type = "str"
            return None, not is_environ_get, inferred_type

        default_value = infer_value(default_node).get_exact("<dynamic>")
        if inferred_type == "unknown":
            inferred_type = self._infer_type_from_default(default_node, imports or {})

        return default_value, False, inferred_type

    def _get_default_node(self, node: nodes.Call) -> nodes.NodeNG | None:
        """Return the default-value node for getenv-like calls, if present."""
        if len(node.args) >= 2:
            return node.args[1]

        for kw in node.keywords:
            if kw.arg == "default":
                return kw.value

        return None

    def _infer_conversion_type(self, func: nodes.NodeNG) -> str:
        """Infer explicit conversion type from a call target."""
        conversion_name = safe_as_string(func)
        if conversion_name in {"str", "int", "bool", "float", "list", "dict", "tuple"}:
            return conversion_name
        return "unknown"

    def _infer_type_from_default(self, default_node: nodes.NodeNG, imports: dict[str, str]) -> str:
        """Infer environment variable type from an exact default value."""
        inferred_type, confidence = infer_type(default_node)
        if confidence == "exact" and inferred_type != "None":
            return inferred_type

        if isinstance(default_node, nodes.Call) and self._is_supported_getenv_call(default_node.func, imports):
            return "str"

        string_pattern = infer_string_pattern(default_node)
        if string_pattern.parts and string_pattern.parts != [...]:
            return "str"

        return "unknown"

    def _is_supported_getenv_call(
        self,
        func: nodes.NodeNG,
        imports: dict[str, str],
    ) -> bool:
        """Return True for supported os.getenv and os.environ.get calls only."""
        return self._is_supported_getenv_name(func, imports) or self._is_supported_environ_get(func, imports)

    def _is_supported_getenv_name(self, func: nodes.NodeNG, imports: dict[str, str]) -> bool:
        """Check supported getenv call names, including imported aliases."""
        if isinstance(func, nodes.Attribute):
            if func.attrname != "getenv":
                return False
            owner_name = safe_as_string(func.expr)
            owner_root = owner_name.split(".")[0] if owner_name else ""
            return owner_root in SUPPORTED_GETENV_MODULES or imports.get(owner_root) in SUPPORTED_GETENV_MODULES

        if isinstance(func, nodes.Name):
            qualified = imports.get(func.name, "")
            return qualified in {"os.getenv"}

        return False

    def _is_supported_environ_get(self, func: nodes.NodeNG, imports: dict[str, str]) -> bool:
        """Check supported environ.get call names, including imported aliases."""
        if not isinstance(func, nodes.Attribute):
            return False

        if func.attrname != "get":
            return False

        return self._is_supported_environ_value(func.expr, imports)

    def _is_supported_environ_value(self, value: nodes.NodeNG, imports: dict[str, str]) -> bool:
        """Check supported environ object references, including imported aliases."""
        value_str = safe_as_string(value)
        if value_str == "os.environ" or value_str == "environ":
            return True

        if isinstance(value, nodes.Attribute):
            if value.attrname != "environ":
                return False

            owner_name = safe_as_string(value.expr)
            owner_root = owner_name.split(".")[0] if owner_name else ""
            return owner_root in SUPPORTED_ENVIRON_MODULES or imports.get(owner_root) in SUPPORTED_ENVIRON_MODULES

        if isinstance(value, nodes.Name):
            qualified = imports.get(value.name, "")
            return qualified == "os.environ"

        return False

    def _calculate_summary(
        self,
        files_scanned: int,
        scan_duration_ms: int,
    ) -> EnvVarSummary:
        """Calculate summary statistics."""
        total_env_vars = len(self.env_vars)
        required_count = sum(1 for var in self.env_vars.values() if var.required)
        optional_count = total_env_vars - required_count

        return EnvVarSummary(
            total_count=total_env_vars,
            files_scanned=files_scanned,
            scan_duration_ms=scan_duration_ms,
            total_env_vars=total_env_vars,
            required_count=required_count,
            optional_count=optional_count,
        )
