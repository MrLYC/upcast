"""Test multi-line function signature extraction."""

from textwrap import dedent

from astroid import parse

from upcast.cyclomatic_complexity_scanner.checker import ComplexityChecker


class TestMultilineSignature:
    """Tests for multi-line function signatures."""

    def test_multiline_signature_merged(self):
        """Test that multi-line signatures are merged into one line."""
        source = dedent(
            '''
            def complex_function(
                arg1: str,
                arg2: int,
                arg3: dict,
                optional: bool = True
            ) -> dict:
                """A function with multi-line signature."""
                if arg2 > 0:
                    return {"result": arg1}
                return {}
        '''
        )

        # Parse and check
        module = parse(source)
        func_node = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))

        checker = ComplexityChecker(threshold=1)
        result = checker._extract_function_metadata(func_node)

        assert result is not None
        assert result.name == "complex_function"

        # Check signature is merged to single line
        assert "\n" not in result.signature, "Signature should not contain newlines"
        assert "def complex_function" in result.signature
        assert "arg1: str" in result.signature
        assert "arg2: int" in result.signature
        assert "arg3: dict" in result.signature
        assert "optional: bool = True" in result.signature
        assert "-> dict:" in result.signature

    def test_multiline_signature_with_many_params(self):
        """Test multi-line signature with many parameters."""
        source = dedent(
            '''
            def function_with_many_params(
                param1: str,
                param2: int,
                param3: float,
                param4: bool,
                param5: list,
                param6: dict,
                optional1: str = "default",
                optional2: int = 0
            ) -> tuple:
                """Many parameters."""
                return (param1, param2)
        '''
        )

        module = parse(source)
        func_node = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))

        checker = ComplexityChecker(threshold=1)
        result = checker._extract_function_metadata(func_node)

        assert result is not None
        assert "\n" not in result.signature
        assert "param1: str" in result.signature
        assert "param8" not in result.signature  # Should only have 8 params

    def test_multiline_signature_with_generic_types(self):
        """Test multi-line signature with generic types."""
        source = dedent(
            '''
            def complex_generic(
                items: list[dict[str, int]],
                mapping: dict[str, list[str]],
                optional: str | None = None
            ) -> dict[str, list[int]]:
                """Complex generic types."""
                return {}
        '''
        )

        module = parse(source)
        func_node = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))

        checker = ComplexityChecker(threshold=1)
        result = checker._extract_function_metadata(func_node)

        assert result is not None
        assert "\n" not in result.signature
        assert "list[dict[str, int]]" in result.signature or "List[" in result.signature

    def test_simple_signature_unchanged(self):
        """Test that simple single-line signatures work correctly."""
        source = dedent(
            '''
            def simple_function(x: int, y: str) -> bool:
                """Simple function."""
                return x > 0
        '''
        )

        module = parse(source)
        func_node = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))

        checker = ComplexityChecker(threshold=1)
        result = checker._extract_function_metadata(func_node)

        assert result is not None
        assert "\n" not in result.signature
        assert result.signature == "def simple_function(x: int, y: str) -> bool:"

    def test_async_multiline_signature(self):
        """Test async function with multi-line signature."""
        source = dedent(
            '''
            async def async_complex(
                param1: str,
                param2: int,
                callback: callable
            ) -> str:
                """Async with multi-line."""
                if param2 > 0:
                    return param1
                return ""
        '''
        )

        module = parse(source)
        func_node = next(iter(module.nodes_of_class(parse("async def f(): pass").body[0].__class__)))

        checker = ComplexityChecker(threshold=1)
        result = checker._extract_function_metadata(func_node)

        assert result is not None
        assert result.is_async
        assert "\n" not in result.signature
        assert "async def async_complex" in result.signature

    def test_signature_skips_decorators(self):
        """Test that decorators are not included in signatures."""
        source = dedent(
            '''
            class MyClass:
                @classmethod
                def class_method(
                    cls,
                    param1: str,
                    param2: int
                ) -> dict:
                    """Class method with decorator."""
                    if param1:
                        return {"result": param2}
                    return {}
        '''
        )

        module = parse(source)
        func_node = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))

        checker = ComplexityChecker(threshold=1)
        result = checker._extract_function_metadata(func_node, parent_class="MyClass")

        assert result is not None
        assert result.name == "class_method"
        assert "\n" not in result.signature
        # Signature should not start with decorator
        assert not result.signature.startswith("@")
        assert result.signature.startswith("def class_method")
        assert "cls" in result.signature
        assert "param1: str" in result.signature
        assert "param2: int" in result.signature
        assert "@classmethod" not in result.signature

    def test_signature_skips_multiple_decorators(self):
        """Test that multiple decorators are all skipped."""
        source = dedent(
            '''
            @decorator1
            @decorator2
            @decorator3
            def decorated_function(x: int, y: str) -> bool:
                """Multiple decorators."""
                if x > 0:
                    return True
                return False
        '''
        )

        module = parse(source)
        func_node = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))

        checker = ComplexityChecker(threshold=1)
        result = checker._extract_function_metadata(func_node)

        assert result is not None
        assert "\n" not in result.signature
        assert not result.signature.startswith("@")
        assert result.signature.startswith("def decorated_function")
        assert "@decorator1" not in result.signature
        assert "@decorator2" not in result.signature
        assert "@decorator3" not in result.signature
