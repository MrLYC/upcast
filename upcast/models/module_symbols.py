"""Data models for module symbol scanner.

This module defines Pydantic models for representing Python module symbols,
including imports, variables, functions, and classes.
"""

from pydantic import BaseModel, ConfigDict, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class ImportedModule(BaseModel):
    """Represents a complete module import (e.g., `import xxx` or `import xxx.yyy`)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    module_path: str = Field(..., description="Module path like 'os' or 'xxx.yyy'")
    attributes: list[str] = Field(default_factory=list, description="Accessed attributes on this module")
    blocks: list[str] = Field(default_factory=list, description="Block contexts where import occurs")


class ImportedSymbol(BaseModel):
    """Represents a symbol imported from a module (e.g., `from xxx import yyy`)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    module_path: str = Field(..., description="Source module path like 'xxx.yyy'")
    attributes: list[str] = Field(default_factory=list, description="Accessed attributes on this symbol")
    lineno: int = Field(..., description="Line number where import statement occurs")
    statement: str = Field(..., description="Import statement source code")
    blocks: list[str] = Field(default_factory=list, description="Block contexts where import occurs")


class StarImport(BaseModel):
    """Represents a star import (e.g., `from xxx import *`)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    module_path: str = Field(..., description="Source module path")
    blocks: list[str] = Field(default_factory=list, description="Block contexts where import occurs")


class Variable(BaseModel):
    """Represents a module-level variable."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    module_path: str = Field(..., description="Variable's module path like 'path.to.file'")
    attributes: list[str] = Field(default_factory=list, description="Accessed attributes on this variable")
    lineno: int = Field(..., description="Line number where variable is defined")
    value: str | None = Field(None, description="String representation of value (for simple types)")
    statement: str = Field(..., description="Assignment statement source code")
    blocks: list[str] = Field(default_factory=list, description="Block contexts where variable is defined")


class Decorator(BaseModel):
    """Represents a decorator applied to a function or class."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(..., description="Decorator name")
    lineno: int = Field(..., description="Line number where decorator is applied")
    args: list[str] = Field(default_factory=list, description="Positional arguments")
    kwargs: dict[str, str] = Field(default_factory=dict, description="Keyword arguments")


class Function(BaseModel):
    """Represents a module-level function."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    lineno: int = Field(..., description="Line number where function is defined")
    is_async: bool = Field(..., description="Whether function is async")
    signature: str = Field(..., description="Function signature like 'def func(arg1: int) -> bool'")
    docstring: str | None = Field(None, description="Function's docstring")
    body_md5: str = Field(..., description="MD5 hash of function body")
    attributes: list[str] = Field(default_factory=list, description="Accessed attributes on this function")
    decorators: list[Decorator] = Field(default_factory=list, description="Applied decorators")
    blocks: list[str] = Field(default_factory=list, description="Block contexts where function is defined")


class Class(BaseModel):
    """Represents a module-level class."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    lineno: int = Field(..., description="Line number where class is defined")
    docstring: str | None = Field(None, description="Class's docstring")
    body_md5: str = Field(..., description="MD5 hash of class body")
    attributes: list[str] = Field(default_factory=list, description="Class attribute names")
    methods: list[str] = Field(default_factory=list, description="Method names")
    bases: list[str] = Field(default_factory=list, description="Base class names")
    decorators: list[Decorator] = Field(default_factory=list, description="Applied decorators")
    blocks: list[str] = Field(default_factory=list, description="Block contexts where class is defined")


class ModuleSymbols(BaseModel):
    """Represents all symbols extracted from a single Python module."""

    model_config = ConfigDict(extra="forbid")

    imported_modules: dict[str, ImportedModule] = Field(
        default_factory=dict, description="Complete module imports keyed by module name"
    )
    imported_symbols: dict[str, ImportedSymbol] = Field(
        default_factory=dict, description="Imported symbols keyed by symbol name"
    )
    star_imported: list[StarImport] = Field(default_factory=list, description="Star imports")
    variables: dict[str, Variable] = Field(default_factory=dict, description="Module-level variables keyed by name")
    functions: dict[str, Function] = Field(default_factory=dict, description="Module-level functions keyed by name")
    classes: dict[str, Class] = Field(default_factory=dict, description="Module-level classes keyed by name")


class ModuleSymbolSummary(ScannerSummary):
    """Summary statistics for module symbol scanner."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    total_modules: int = Field(ge=0, description="Number of modules scanned")
    total_imports: int = Field(ge=0, description="Total number of imports (all types)")
    total_symbols: int = Field(ge=0, description="Total number of symbols (variables + functions + classes)")


class ModuleSymbolOutput(ScannerOutput[dict[str, ModuleSymbols]]):
    """Output model for module symbol scanner.

    Attributes:
        summary: Summary statistics with counts
        results: Dictionary mapping file paths to ModuleSymbols
        metadata: Scanner metadata
    """

    summary: ModuleSymbolSummary
