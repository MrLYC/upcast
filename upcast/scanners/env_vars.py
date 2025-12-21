"""Environment variable scanner with Pydantic models."""

import time
from pathlib import Path

from astroid import nodes

from upcast.common.ast_utils import get_import_info, safe_as_string, safe_infer_value
from upcast.common.file_utils import get_relative_path_str
from upcast.common.scanner_base import BaseScanner
from upcast.models.env_vars import EnvVarInfo, EnvVarLocation, EnvVarOutput, EnvVarSummary


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
            env_vars=self.env_vars,
            metadata={"scanner_name": "env_vars", "root_path": str(self.base_path)},
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
        func_name = safe_as_string(node.func)

        # Check for getenv or environ.get patterns
        if not ("getenv" in func_name or (func_name.endswith(".get") and "environ" in func_name)):
            return

        # Extract variable name
        if not node.args:
            return
        var_name = safe_infer_value(node.args[0])
        if not isinstance(var_name, str):
            return

        # Extract default value
        default_value = None
        required = True
        if len(node.args) >= 2:
            default_value = safe_infer_value(node.args[1], default="<dynamic>")
            required = False
        elif node.keywords:
            for kw in node.keywords:
                if kw.arg == "default":
                    default_value = safe_infer_value(kw.value, default="<dynamic>")
                    required = False
                    break

        # Create location and add to results
        location = EnvVarLocation(
            file=file_path,
            line=node.lineno,
            column=node.col_offset,
            pattern=f"{func_name}('{var_name}')",
            code=safe_as_string(node),
        )
        self._add_env_var(
            name=var_name,
            required=required,
            default_value=str(default_value) if default_value is not None else None,
            location=location,
        )

    def _check_environ_subscript(self, node: nodes.Subscript, file_path: str, imports: dict[str, str]) -> None:
        """Check if Subscript node is os.environ['KEY'] or similar."""
        value_str = safe_as_string(node.value)
        if "environ" not in value_str:
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
            column=node.col_offset,
            pattern=f"{value_str}['{node.slice.value}']",
            code=safe_as_string(node),
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
                locations=[],
            )

        self.env_vars[name].locations.append(location)

        # Update required status (if ANY usage is required, mark as required)
        if required:
            self.env_vars[name].required = True

        # Update default value if provided and not already set
        if default_value is not None and self.env_vars[name].default_value is None:
            self.env_vars[name].default_value = default_value

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
