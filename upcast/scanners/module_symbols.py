"""Module symbol scanner for Python modules.

This scanner analyzes Python modules to extract imports, variables, functions,
and classes with their metadata.
"""

import hashlib
import time
from pathlib import Path

from astroid import nodes

from upcast.common.ast_utils import safe_as_string
from upcast.common.file_utils import get_relative_path_str
from upcast.common.inference import infer_value
from upcast.common.scanner_base import BaseScanner
from upcast.models.module_symbols import (
    Class,
    Decorator,
    Function,
    ImportedModule,
    ImportedSymbol,
    ModuleSymbolOutput,
    ModuleSymbols,
    ModuleSymbolSummary,
    StarImport,
    Variable,
)


class ModuleSymbolScanner(BaseScanner[ModuleSymbolOutput]):
    """Scanner for analyzing module symbols and imports."""

    def __init__(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
        include_private: bool = False,
    ):
        """Initialize scanner.

        Args:
            include_patterns: File patterns to include
            exclude_patterns: File patterns to exclude
            verbose: Enable verbose logging
            include_private: Include private symbols (starting with _)
        """
        super().__init__(include_patterns, exclude_patterns, verbose)
        self.include_private = include_private
        self.base_path: Path | None = None
        self.results: dict[str, ModuleSymbols] = {}
        self.symbol_usage: dict[str, list[str]] = {}  # Track attribute access per symbol

    def scan(self, path: Path) -> ModuleSymbolOutput:
        """Scan path for module symbols.

        Args:
            path: Directory or file path to scan

        Returns:
            Complete scan output with summary, results, and metadata
        """
        start_time = time.time()
        self.base_path = path.resolve() if path.is_dir() else path.parent.resolve()
        self.results = {}

        files = self.get_files_to_scan(path)
        for file_path in files:
            self._scan_file(file_path)

        summary = self._calculate_summary(
            files_scanned=len(files),
            scan_duration_ms=int((time.time() - start_time) * 1000),
        )

        filtered_results = {
            file_path: symbols
            for file_path, symbols in self.results.items()
            if (
                symbols.imported_modules
                or symbols.imported_symbols
                or symbols.star_imported
                or symbols.variables
                or symbols.functions
                or symbols.classes
            )
        }

        return ModuleSymbolOutput(
            summary=summary,
            results=filtered_results,
            metadata={"scanner_name": "module_symbols"},
        )

    def scan_file(self, file_path: Path) -> ModuleSymbols | None:
        """Scan a single file for module symbols.

        Args:
            file_path: Path to Python file

        Returns:
            ModuleSymbols if successful, None if parsing fails
        """
        return self._scan_file(file_path)

    def _scan_file(self, file_path: Path) -> ModuleSymbols | None:
        """Internal method to scan a single file.

        Args:
            file_path: Path to Python file

        Returns:
            ModuleSymbols if successful, None if parsing fails
        """
        module = self.parse_file(file_path)
        if not module:
            return None

        relative_path = get_relative_path_str(file_path, self.base_path or Path.cwd())
        self.symbol_usage = {}  # Reset for each file

        # Extract module path from file path
        module_path = self._get_module_path(file_path)

        # Calculate package path for relative import resolution
        # For __init__.py, module_path is already the package path
        # For other files, package_path is the parent package
        package_path = module_path if file_path.stem == "__init__" else ".".join(module_path.split(".")[:-1])

        # Initialize results structure
        symbols = ModuleSymbols()

        # Track block context
        block_stack: list[str] = ["module"]

        # Phase 1: Extract imports
        self._extract_imports(module, symbols, package_path, block_stack)

        # Phase 2: Analyze attribute access for all symbols
        self._analyze_attribute_access(module)

        # Phase 3: Extract symbols (variables, functions, classes)
        self._extract_symbols(module, symbols, module_path, block_stack)

        # Phase 4: Apply attribute access data
        self._apply_attribute_access(symbols)

        self.results[relative_path] = symbols
        return symbols

    def _get_module_path(self, file_path: Path) -> str:
        """Convert file path to Python module path.

        Args:
            file_path: Path to Python file

        Returns:
            Module path like 'package.module'
        """
        if not self.base_path:
            return file_path.stem if file_path.stem != "__init__" else ""

        try:
            # Resolve both paths to handle symlinks and relative paths consistently
            resolved_file = file_path.resolve()
            relative = resolved_file.relative_to(self.base_path)
            # For __init__.py, use the directory path as module path
            if relative.stem == "__init__":
                parts = list(relative.parts[:-1])
            else:
                parts = [*list(relative.parts[:-1]), relative.stem]
            return ".".join(parts)
        except ValueError:
            return file_path.stem if file_path.stem != "__init__" else ""

    def _extract_imports(
        self, module: nodes.Module, symbols: ModuleSymbols, package_path: str, block_stack: list[str]
    ) -> None:
        """Extract import statements from module.

        Args:
            module: Parsed AST module
            symbols: ModuleSymbols to populate
            package_path: Package path of the current file (for resolving relative imports)
            block_stack: Current block context stack
        """
        for node in module.nodes_of_class((nodes.Import, nodes.ImportFrom)):
            current_blocks = block_stack.copy()

            if isinstance(node, nodes.Import):
                # Handle: import xxx, import xxx.yyy
                for name, _ in node.names:
                    # Use the first part as the key (e.g., "os" from "os.path")
                    key = name.split(".")[0]
                    if key not in symbols.imported_modules:
                        symbols.imported_modules[key] = ImportedModule(
                            module_path=name, attributes=[], blocks=current_blocks
                        )

            elif isinstance(node, nodes.ImportFrom) and node.modname:
                # Resolve relative imports to absolute paths
                level = node.level if node.level is not None else 0
                resolved_modname = self._resolve_relative_import(node.modname, level, package_path)

                # Handle: from xxx import *
                if "*" in [n[0] for n in node.names]:
                    symbols.star_imported.append(StarImport(module_path=resolved_modname, blocks=current_blocks))
                else:
                    # Handle: from xxx import yyy, zzz
                    for name, _ in node.names:
                        # Use full path including the imported symbol name
                        full_module_path = f"{resolved_modname}.{name}"
                        symbols.imported_symbols[name] = ImportedSymbol(
                            module_path=full_module_path,
                            attributes=[],
                            lineno=node.lineno or 0,
                            statement=safe_as_string(node) or "",
                            blocks=current_blocks,
                        )

    def _resolve_relative_import(self, modname: str, level: int, package_path: str) -> str:
        """Resolve relative import to absolute module path.

        Args:
            modname: Module name from import statement
            level: Number of dots in relative import (0 = absolute, 1 = current package, 2 = parent, etc.)
            package_path: Package path of the current file (already excludes module name for non-__init__ files)

        Returns:
            Absolute module path
        """
        if level == 0:
            # Absolute import
            return modname

        # Split package path into parts
        parts = package_path.split(".") if package_path else []

        # For level=1 (from .xxx), we stay in the current package
        # For level=2 (from ..xxx), we go to parent package, etc.
        # So we need to go up (level - 1) levels
        for _ in range(level - 1):
            if parts:
                parts.pop()

        # Append the relative module name
        if modname:
            parts.append(modname)

        return ".".join(parts) if parts else modname

    def _resolve_symbol_name(self, symbol_name: str, symbols: ModuleSymbols) -> str:
        """Resolve a symbol name to its full module path.

        For example, if 'serializers' is imported from 'rest_framework',
        then 'serializers.Serializer' will be resolved to 'rest_framework.serializers.Serializer'.

        Args:
            symbol_name: Symbol name like 'serializers.Serializer' or 'MyClass'
            symbols: Current module's symbols (to look up imports)

        Returns:
            Resolved full module path or original symbol name if not resolvable
        """
        # Split the symbol name (e.g., "serializers.Serializer" -> ["serializers", "Serializer"])
        parts = symbol_name.split(".", 1)
        base_name = parts[0]

        # Check if the base name is an imported module
        if base_name in symbols.imported_modules:
            module_path = symbols.imported_modules[base_name].module_path
            if len(parts) > 1:
                # Append the rest of the path
                return f"{module_path}.{parts[1]}"
            return module_path

        # Check if the base name is an imported symbol
        if base_name in symbols.imported_symbols:
            module_path = symbols.imported_symbols[base_name].module_path
            # The module_path now includes the symbol itself (e.g., rest_framework.serializers)
            # So we just need to append the remaining parts
            if len(parts) > 1:
                # Append only the remaining path (not the whole symbol_name)
                return f"{module_path}.{parts[1]}"
            return module_path

        # If not found in imports, return as-is
        return symbol_name

    def _analyze_attribute_access(self, module: nodes.Module) -> None:
        """Analyze attribute access patterns in the module.

        Args:
            module: Parsed AST module
        """
        for node in module.nodes_of_class(nodes.Attribute):
            # Get the base name (e.g., "os" from "os.path")
            base = node.expr
            while isinstance(base, nodes.Attribute):
                base = base.expr

            base_name = safe_as_string(base)
            if not base_name:
                continue

            # Record the first-level attribute access
            attr = node.attrname
            if base_name not in self.symbol_usage:
                self.symbol_usage[base_name] = []
            if attr not in self.symbol_usage[base_name]:
                self.symbol_usage[base_name].append(attr)

    def _extract_symbols(
        self, module: nodes.Module, symbols: ModuleSymbols, module_path: str, block_stack: list[str]
    ) -> None:
        """Extract module-level variables, functions, and classes.

        Args:
            module: Parsed AST module
            symbols: ModuleSymbols to populate
            module_path: Module path string
            block_stack: Current block context stack
        """
        for node in module.body:
            self._extract_node_symbols(node, symbols, module_path, block_stack)

    def _extract_node_symbols(  # noqa: C901
        self, node: nodes.NodeNG, symbols: ModuleSymbols, module_path: str, block_stack: list[str]
    ) -> None:
        """Extract symbols from a node recursively.

        Args:
            node: AST node to process
            symbols: ModuleSymbols to populate
            module_path: Module path string
            block_stack: Current block context stack
        """
        if isinstance(node, nodes.Assign):
            self._extract_variables(node, symbols, module_path, block_stack)

        elif isinstance(node, nodes.FunctionDef):
            self._extract_function(node, symbols, block_stack)

        elif isinstance(node, nodes.ClassDef):
            self._extract_class(node, symbols, block_stack)

        elif isinstance(node, (nodes.If, nodes.Try, nodes.ExceptHandler)):
            # Handle nested blocks
            block_type = "if" if isinstance(node, nodes.If) else "try" if isinstance(node, nodes.Try) else "except"
            new_stack = [*block_stack, block_type]

            # Process child nodes
            if isinstance(node, nodes.If):
                for child in node.body:
                    self._extract_node_symbols(child, symbols, module_path, new_stack)
                for child in node.orelse:
                    self._extract_node_symbols(child, symbols, module_path, new_stack)
            elif isinstance(node, nodes.Try):
                for child in node.body:
                    self._extract_node_symbols(child, symbols, module_path, new_stack)
                for handler in node.handlers:
                    self._extract_node_symbols(handler, symbols, module_path, new_stack)
            elif isinstance(node, nodes.ExceptHandler):
                for child in node.body:
                    self._extract_node_symbols(child, symbols, module_path, new_stack)

    def _extract_variables(
        self, node: nodes.Assign, symbols: ModuleSymbols, module_path: str, block_stack: list[str]
    ) -> None:
        """Extract variable assignments.

        Args:
            node: Assignment node
            symbols: ModuleSymbols to populate
            module_path: Module path string
            block_stack: Current block context stack
        """
        for target in node.targets:
            if isinstance(target, nodes.AssignName):
                var_name = target.name

                # Skip private variables unless explicitly included
                if not self.include_private and var_name.startswith("_"):
                    continue

                # Extract value
                value_obj = infer_value(node.value).get_exact()
                value_str = str(value_obj) if value_obj is not None else None
                statement = safe_as_string(node) or ""

                symbols.variables[var_name] = Variable(
                    module_path=module_path,
                    attributes=[],
                    lineno=node.lineno or 0,
                    value=value_str,
                    statement=statement,
                    blocks=block_stack.copy(),
                )

    def _extract_function(self, node: nodes.FunctionDef, symbols: ModuleSymbols, block_stack: list[str]) -> None:
        """Extract function definition.

        Args:
            node: Function definition node
            symbols: ModuleSymbols to populate
            block_stack: Current block context stack
        """
        func_name = node.name

        # Skip private functions unless explicitly included
        if not self.include_private and func_name.startswith("_"):
            return

        # Extract signature - get the definition line only
        full_source = safe_as_string(node) or ""
        if full_source:
            # Split by newlines and take the first non-empty line (the def line)
            lines = [line for line in full_source.split("\n") if line.strip()]
            if lines:
                signature = lines[0].rstrip()
                if not signature.endswith(":"):
                    signature += ":"
            else:
                signature = f"def {func_name}(...):"
        else:
            signature = f"def {func_name}(...):"

        # Extract docstring
        docstring = node.doc_node.value if node.doc_node else None

        # Compute body MD5
        body_str = safe_as_string(node) or ""
        body_md5 = hashlib.md5(body_str.encode()).hexdigest()  # noqa: S324

        # Extract decorators
        decorators = self._extract_decorators(node.decorators)

        symbols.functions[func_name] = Function(
            lineno=node.lineno or 0,
            is_async=isinstance(node, nodes.AsyncFunctionDef),
            signature=signature,
            docstring=docstring,
            body_md5=body_md5,
            attributes=[],
            decorators=decorators,
            blocks=block_stack.copy(),
        )

    def _extract_class(self, node: nodes.ClassDef, symbols: ModuleSymbols, block_stack: list[str]) -> None:
        """Extract class definition.

        Args:
            node: Class definition node
            symbols: ModuleSymbols to populate
            block_stack: Current block context stack
        """
        class_name = node.name

        # Skip private classes unless explicitly included
        if not self.include_private and class_name.startswith("_"):
            return

        # Extract docstring
        docstring = node.doc_node.value if node.doc_node else None

        # Compute body MD5
        body_str = safe_as_string(node) or ""
        body_md5 = hashlib.md5(body_str.encode()).hexdigest()  # noqa: S324

        # Extract base classes
        bases = [safe_as_string(base) or "" for base in node.bases]
        bases = [b for b in bases if b]  # Remove empty strings

        # Resolve base class names to full module paths
        resolved_bases = []
        for base_name in bases:
            resolved = self._resolve_symbol_name(base_name, symbols)
            resolved_bases.append(resolved)
        bases = resolved_bases

        # Extract class attributes and methods
        class_attrs: list[str] = []
        methods: list[str] = []

        for child in node.body:
            if isinstance(child, nodes.Assign):
                for target in child.targets:
                    if isinstance(target, nodes.AssignName):
                        class_attrs.append(target.name)
            elif isinstance(child, nodes.FunctionDef):
                methods.append(child.name)

        # Extract decorators
        decorators = self._extract_decorators(node.decorators)

        symbols.classes[class_name] = Class(
            lineno=node.lineno or 0,
            docstring=docstring,
            body_md5=body_md5,
            attributes=class_attrs,
            methods=methods,
            bases=bases,
            decorators=decorators,
            blocks=block_stack.copy(),
        )

    def _extract_decorators(self, decorator_nodes: nodes.Decorators | None) -> list[Decorator]:
        """Extract decorator information.

        Args:
            decorator_nodes: Decorators node from AST

        Returns:
            List of Decorator objects
        """
        if not decorator_nodes:
            return []

        decorators: list[Decorator] = []

        for node in decorator_nodes.nodes:
            if isinstance(node, nodes.Name):
                # Simple decorator: @decorator
                decorators.append(Decorator(name=node.name, lineno=node.lineno or 0, args=[], kwargs={}))
            elif isinstance(node, nodes.Call):
                # Decorator with arguments: @decorator(args, kwargs)
                func_name = safe_as_string(node.func) or "unknown"

                # Extract args - ensure all values are strings
                args = []
                for arg in node.args:
                    result = infer_value(arg)
                    value = result.value if result.value is not None else (safe_as_string(arg) or "")
                    # Convert to string if not already
                    args.append(str(value) if not isinstance(value, str) else value)

                # Extract kwargs - ensure all values are strings
                kwargs = {}
                for keyword in node.keywords:
                    if keyword.arg:
                        result = infer_value(keyword.value)
                        value = result.value if result.value is not None else (safe_as_string(keyword.value) or "")
                        # Convert to string if not already
                        kwargs[keyword.arg] = str(value) if not isinstance(value, str) else value

                decorators.append(Decorator(name=func_name, lineno=node.lineno or 0, args=args, kwargs=kwargs))
            else:
                # Complex decorator, just extract as string
                name = safe_as_string(node) or "unknown"
                decorators.append(Decorator(name=name, lineno=node.lineno or 0, args=[], kwargs={}))

        return decorators

    def _apply_attribute_access(self, symbols: ModuleSymbols) -> None:  # noqa: C901
        """Apply collected attribute access data to symbols.

        Args:
            symbols: ModuleSymbols to update
        """
        # Apply to imported modules
        for name, module in symbols.imported_modules.items():
            if name in self.symbol_usage:
                symbols.imported_modules[name] = ImportedModule(
                    module_path=module.module_path,
                    attributes=self.symbol_usage[name],
                    blocks=module.blocks,
                )

        # Apply to imported symbols
        for name, symbol in symbols.imported_symbols.items():
            if name in self.symbol_usage:
                symbols.imported_symbols[name] = ImportedSymbol(
                    module_path=symbol.module_path,
                    attributes=self.symbol_usage[name],
                    lineno=symbol.lineno,
                    statement=symbol.statement,
                    blocks=symbol.blocks,
                )

        # Apply to variables
        for name, var in symbols.variables.items():
            if name in self.symbol_usage:
                symbols.variables[name] = Variable(
                    module_path=var.module_path,
                    attributes=self.symbol_usage[name],
                    lineno=var.lineno,
                    value=var.value,
                    statement=var.statement,
                    blocks=var.blocks,
                )

        # Apply to functions
        for name, func in symbols.functions.items():
            if name in self.symbol_usage:
                symbols.functions[name] = Function(
                    lineno=func.lineno,
                    is_async=func.is_async,
                    signature=func.signature,
                    docstring=func.docstring,
                    body_md5=func.body_md5,
                    attributes=self.symbol_usage[name],
                    decorators=func.decorators,
                    blocks=func.blocks,
                )

        # Apply to classes
        for name, cls in symbols.classes.items():
            if name in self.symbol_usage:
                symbols.classes[name] = Class(
                    lineno=cls.lineno,
                    docstring=cls.docstring,
                    body_md5=cls.body_md5,
                    attributes=cls.attributes,
                    methods=cls.methods,
                    bases=cls.bases,
                    decorators=cls.decorators,
                    blocks=cls.blocks,
                )

    def _calculate_summary(self, files_scanned: int, scan_duration_ms: int) -> ModuleSymbolSummary:
        """Calculate summary statistics.

        Args:
            files_scanned: Number of files scanned
            scan_duration_ms: Duration in milliseconds

        Returns:
            Summary statistics
        """
        total_imports = 0
        total_symbols = 0

        for symbols in self.results.values():
            total_imports += len(symbols.imported_modules) + len(symbols.imported_symbols) + len(symbols.star_imported)
            total_symbols += len(symbols.variables) + len(symbols.functions) + len(symbols.classes)

        return ModuleSymbolSummary(
            total_count=total_symbols,
            files_scanned=files_scanned,
            scan_duration_ms=scan_duration_ms,
            total_modules=len(self.results),
            total_imports=total_imports,
            total_symbols=total_symbols,
        )
