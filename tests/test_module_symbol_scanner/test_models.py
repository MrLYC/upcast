"""Tests for module symbol scanner data models."""

import pytest
from pydantic import ValidationError

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


class TestImportedModule:
    """Tests for ImportedModule model."""

    def test_basic_import(self):
        """Test basic module import."""
        module = ImportedModule(module_path="os", attributes=[], blocks=["module"])
        assert module.module_path == "os"
        assert module.attributes == []
        assert module.blocks == ["module"]

    def test_with_attributes(self):
        """Test module with attribute access."""
        module = ImportedModule(module_path="os", attributes=["path"], blocks=["module"])
        assert "path" in module.attributes

    def test_frozen(self):
        """Test model is frozen."""
        module = ImportedModule(module_path="os", attributes=[], blocks=["module"])
        with pytest.raises(ValidationError):
            module.module_path = "sys"  # type: ignore


class TestImportedSymbol:
    """Tests for ImportedSymbol model."""

    def test_basic_symbol(self):
        """Test basic symbol import."""
        symbol = ImportedSymbol(module_path="pathlib", attributes=[], blocks=["module"])
        assert symbol.module_path == "pathlib"

    def test_with_attributes(self):
        """Test symbol with attribute access."""
        symbol = ImportedSymbol(module_path="pathlib", attributes=["home"], blocks=["module"])
        assert "home" in symbol.attributes


class TestStarImport:
    """Tests for StarImport model."""

    def test_star_import(self):
        """Test star import."""
        star = StarImport(module_path="typing", blocks=["module"])
        assert star.module_path == "typing"
        assert star.blocks == ["module"]


class TestVariable:
    """Tests for Variable model."""

    def test_basic_variable(self):
        """Test basic variable."""
        var = Variable(
            module_path="test.module",
            attributes=[],
            value="True",
            statement="DEBUG = True",
            blocks=["module"],
        )
        assert var.module_path == "test.module"
        assert var.value == "True"
        assert var.statement == "DEBUG = True"

    def test_variable_without_value(self):
        """Test variable without inferred value."""
        var = Variable(
            module_path="test.module", attributes=[], value=None, statement="X = compute()", blocks=["module"]
        )
        assert var.value is None


class TestDecorator:
    """Tests for Decorator model."""

    def test_simple_decorator(self):
        """Test simple decorator without arguments."""
        dec = Decorator(name="decorator", args=[], kwargs={})
        assert dec.name == "decorator"
        assert dec.args == []
        assert dec.kwargs == {}

    def test_decorator_with_args(self):
        """Test decorator with arguments."""
        dec = Decorator(name="decorator", args=["arg1"], kwargs={"key": "value"})
        assert dec.args == ["arg1"]
        assert dec.kwargs == {"key": "value"}


class TestFunction:
    """Tests for Function model."""

    def test_basic_function(self):
        """Test basic function."""
        func = Function(
            signature="def test() -> None",
            docstring="Test function",
            body_md5="abc123",
            attributes=[],
            decorators=[],
            blocks=["module"],
        )
        assert func.signature == "def test() -> None"
        assert func.docstring == "Test function"
        assert func.body_md5 == "abc123"

    def test_function_with_decorator(self):
        """Test function with decorators."""
        func = Function(
            signature="def test() -> None",
            docstring=None,
            body_md5="abc123",
            attributes=[],
            decorators=[Decorator(name="staticmethod", args=[], kwargs={})],
            blocks=["module"],
        )
        assert len(func.decorators) == 1
        assert func.decorators[0].name == "staticmethod"


class TestClass:
    """Tests for Class model."""

    def test_basic_class(self):
        """Test basic class."""
        cls = Class(
            docstring="Test class",
            body_md5="def456",
            attributes=["attr1"],
            methods=["method1"],
            bases=[],
            decorators=[],
            blocks=["module"],
        )
        assert cls.docstring == "Test class"
        assert cls.body_md5 == "def456"
        assert "attr1" in cls.attributes
        assert "method1" in cls.methods

    def test_class_with_bases(self):
        """Test class with base classes."""
        cls = Class(
            docstring=None,
            body_md5="def456",
            attributes=[],
            methods=[],
            bases=["Base1", "Base2"],
            decorators=[],
            blocks=["module"],
        )
        assert cls.bases == ["Base1", "Base2"]


class TestModuleSymbols:
    """Tests for ModuleSymbols model."""

    def test_empty_module(self):
        """Test empty module symbols."""
        symbols = ModuleSymbols()
        assert symbols.imported_modules == {}
        assert symbols.imported_symbols == {}
        assert symbols.star_imported == []
        assert symbols.variables == {}
        assert symbols.functions == {}
        assert symbols.classes == {}

    def test_with_imports(self):
        """Test module with imports."""
        symbols = ModuleSymbols(
            imported_modules={"os": ImportedModule(module_path="os", attributes=[], blocks=["module"])},
            imported_symbols={"Path": ImportedSymbol(module_path="pathlib", attributes=[], blocks=["module"])},
        )
        assert "os" in symbols.imported_modules
        assert "Path" in symbols.imported_symbols


class TestModuleSymbolSummary:
    """Tests for ModuleSymbolSummary model."""

    def test_summary(self):
        """Test summary statistics."""
        summary = ModuleSymbolSummary(
            total_count=100,
            files_scanned=10,
            scan_duration_ms=150,
            total_modules=10,
            total_imports=50,
            total_symbols=100,
        )
        assert summary.total_modules == 10
        assert summary.total_imports == 50
        assert summary.total_symbols == 100
        assert summary.files_scanned == 10

    def test_negative_values_rejected(self):
        """Test that negative values are rejected."""
        with pytest.raises(ValidationError):
            ModuleSymbolSummary(
                total_count=-1,
                files_scanned=10,
                scan_duration_ms=150,
                total_modules=10,
                total_imports=50,
                total_symbols=100,
            )


class TestModuleSymbolOutput:
    """Tests for ModuleSymbolOutput model."""

    def test_output_structure(self):
        """Test output model structure."""
        summary = ModuleSymbolSummary(
            total_count=0,
            files_scanned=1,
            scan_duration_ms=10,
            total_modules=0,
            total_imports=0,
            total_symbols=0,
        )
        output = ModuleSymbolOutput(summary=summary, results={}, metadata={"scanner_name": "module_symbols"})
        assert output.summary.files_scanned == 1
        assert output.results == {}
        assert output.metadata["scanner_name"] == "module_symbols"

    def test_serialization(self):
        """Test model serialization."""
        summary = ModuleSymbolSummary(
            total_count=0,
            files_scanned=1,
            scan_duration_ms=10,
            total_modules=0,
            total_imports=0,
            total_symbols=0,
        )
        output = ModuleSymbolOutput(summary=summary, results={}, metadata={"scanner_name": "module_symbols"})
        data = output.to_dict()
        assert isinstance(data, dict)
        assert "summary" in data
        assert "results" in data
        assert "metadata" in data
