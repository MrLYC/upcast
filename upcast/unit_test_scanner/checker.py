"""AST checker for detecting unit tests."""

import logging
from pathlib import Path

from astroid import MANAGER, nodes

from upcast.unit_test_scanner.test_parser import (
    UnitTestInfo,
    extract_imports,
    parse_test_function,
)

logger = logging.getLogger(__name__)


class UnitTestChecker:
    """AST checker for detecting and analyzing unit tests."""

    def __init__(self, file_path: str, root_modules: list[str] | None = None):
        """Initialize the checker.

        Args:
            file_path: Path to the file being checked
            root_modules: List of root module prefixes to match (None = match all)
        """
        self.file_path = file_path
        self.root_modules = root_modules
        self.tests: list[UnitTestInfo] = []
        self.module_imports: dict[str, str] = {}

    def check_module(self, module: nodes.Module) -> None:
        """Check module for test functions.

        Args:
            module: Module node to check
        """
        # Extract imports
        self.module_imports = extract_imports(module)

        # Visit all function definitions
        for func_node in module.nodes_of_class(nodes.FunctionDef):
            self._check_function(func_node)

    def _check_function(self, node: nodes.FunctionDef) -> None:
        """Check if a function is a test function.

        Args:
            node: Function definition node
        """
        # Check if this is a pytest test function
        if node.name.startswith("test_"):
            # Check if it's a top-level function or in a test class
            parent = node.parent
            if isinstance(parent, nodes.Module):
                # Top-level test function
                test = parse_test_function(
                    node,
                    self.file_path,
                    self.module_imports,
                    self.root_modules,
                )
                self.tests.append(test)
            elif isinstance(parent, nodes.ClassDef):
                # Test method in a class
                # Check if parent is a TestCase or has test_ pattern
                if parent.name.startswith("Test") or self._is_unittest_testcase(parent):
                    test = parse_test_function(
                        node,
                        self.file_path,
                        self.module_imports,
                        self.root_modules,
                    )
                    self.tests.append(test)

    def _is_unittest_testcase(self, class_node: nodes.ClassDef) -> bool:
        """Check if a class inherits from unittest.TestCase.

        Args:
            class_node: Class definition node

        Returns:
            True if it's a unittest.TestCase subclass
        """
        for base in class_node.bases:
            # Try to infer the base class
            try:
                for inferred in base.infer():
                    if hasattr(inferred, "qname"):
                        qname = inferred.qname()
                        if "unittest" in qname and "TestCase" in qname:
                            return True
            except Exception:
                # Inference failed, check name directly
                if isinstance(base, nodes.Name):
                    if base.name == "TestCase":
                        return True
                elif isinstance(base, nodes.Attribute) and base.attrname == "TestCase":
                    return True
        return False

    def get_tests(self) -> list[UnitTestInfo]:
        """Get all detected tests.

        Returns:
            List of test functions
        """
        return self.tests


def check_file(file_path: Path, root_modules: list[str] | None = None) -> list[UnitTestInfo]:
    """Check a single file for unit tests.

    Args:
        file_path: Path to the Python file
        root_modules: List of root module prefixes (None = match all)

    Returns:
        List of detected test functions
    """
    try:
        # Parse file with astroid
        module = MANAGER.ast_from_file(str(file_path))

        # Create checker and check module
        checker = UnitTestChecker(str(file_path), root_modules)
        checker.check_module(module)

        return checker.get_tests()

    except Exception as e:
        logger.warning(f"Failed to parse {file_path}: {e}")
        return []
