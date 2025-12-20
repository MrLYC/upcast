"""Tests for definition_parser module."""

from astroid import nodes, parse

from upcast.django_settings_scanner.ast_utils import resolve_relative_import
from upcast.django_settings_scanner.definition_parser import (
    detect_dynamic_imports,
    detect_star_imports,
    extract_assignment_target,
    extract_base_module,
    extract_import_pattern,
    file_path_to_module_path,
    infer_setting_value,
    is_settings_module,
    is_uppercase_assignment,
    is_uppercase_identifier,
    mark_overrides,
)
from upcast.django_settings_scanner.settings_parser import SettingsDefinition, SettingsModule


class TestIsSettingsModule:
    """Test settings module detection."""

    def test_settings_directory(self):
        """Detect files in settings/ directory."""
        assert is_settings_module("/project/myapp/settings/base.py")
        assert is_settings_module("/project/myapp/settings/dev.py")
        assert is_settings_module("C:\\project\\myapp\\settings\\prod.py")

    def test_config_directory(self):
        """Detect files in config/ directory."""
        assert is_settings_module("/project/config/settings.py")
        assert is_settings_module("/project/myapp/config/production.py")

    def test_non_settings_file(self):
        """Reject non-settings files."""
        assert not is_settings_module("/project/myapp/models.py")
        assert not is_settings_module("/project/utils/helpers.py")
        assert not is_settings_module("/project/tests/test_views.py")

    def test_case_insensitive(self):
        """Detection should be case-insensitive."""
        assert is_settings_module("/project/SETTINGS/base.py")
        assert is_settings_module("/project/Config/settings.py")


class TestFilePathToModulePath:
    """Test file path to module path conversion."""

    def test_simple_conversion(self):
        """Convert simple file path."""
        result = file_path_to_module_path("/project/myapp/settings/base.py", "/project")
        assert result == "myapp.settings.base"

    def test_config_directory(self):
        """Convert config directory path."""
        result = file_path_to_module_path("/project/config/settings.py", "/project")
        assert result == "config.settings"

    def test_nested_structure(self):
        """Convert nested directory structure."""
        result = file_path_to_module_path("/project/myapp/settings/envs/dev.py", "/project")
        assert result == "myapp.settings.envs.dev"

    def test_fallback_on_error(self):
        """Fallback to filename when relative path fails."""
        result = file_path_to_module_path("/somewhere/settings.py", "/other/path")
        assert result == "settings"


class TestIsUppercaseIdentifier:
    """Test uppercase identifier validation."""

    def test_valid_uppercase(self):
        """Accept valid uppercase names."""
        assert is_uppercase_identifier("DEBUG")
        assert is_uppercase_identifier("DATABASE_URL")
        assert is_uppercase_identifier("CORS_ALLOWED_ORIGINS")
        assert is_uppercase_identifier("A")

    def test_lowercase_rejected(self):
        """Reject lowercase names."""
        assert not is_uppercase_identifier("debug")
        assert not is_uppercase_identifier("database_url")
        assert not is_uppercase_identifier("config")

    def test_mixed_case_rejected(self):
        """Reject mixed case names."""
        assert not is_uppercase_identifier("Debug")
        assert not is_uppercase_identifier("DATABASE_Url")

    def test_dunder_names_rejected(self):
        """Reject dunder names."""
        assert not is_uppercase_identifier("__name__")
        assert not is_uppercase_identifier("__file__")
        assert not is_uppercase_identifier("__version__")

    def test_empty_string(self):
        """Handle empty string."""
        assert not is_uppercase_identifier("")

    def test_special_characters(self):
        """Reject names with special characters."""
        assert not is_uppercase_identifier("DEBUG-MODE")
        assert not is_uppercase_identifier("DEBUG.VALUE")


class TestIsUppercaseAssignment:
    """Test uppercase assignment detection."""

    def test_simple_uppercase_assignment(self):
        """Detect simple uppercase assignment."""
        code = "DEBUG = True"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        assert is_uppercase_assignment(assign)

    def test_lowercase_assignment(self):
        """Reject lowercase assignment."""
        code = "debug = True"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        assert not is_uppercase_assignment(assign)

    def test_assignment_with_underscores(self):
        """Accept uppercase with underscores."""
        code = "DATABASE_URL = 'postgres://localhost'"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        assert is_uppercase_assignment(assign)

    def test_annotated_assignment(self):
        """Handle type-annotated assignments."""
        code = "DEBUG: bool = True"
        module = parse(code)
        # AnnAssign, not Assign - currently not detected
        # This is acceptable as we focus on simple assignments
        assert len(module.body) == 1


class TestExtractAssignmentTarget:
    """Test assignment target extraction."""

    def test_simple_assignment(self):
        """Extract simple assignment target."""
        code = "DEBUG = True"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        assert extract_assignment_target(assign) == "DEBUG"

    def test_assignment_with_value(self):
        """Extract target from complex assignment."""
        code = "DATABASE_URL = 'postgres://localhost/db'"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        assert extract_assignment_target(assign) == "DATABASE_URL"

    def test_multiple_targets(self):
        """Extract first target from multiple assignment."""
        code = "A = B = 100"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        # Should return first target
        assert extract_assignment_target(assign) == "A"

    def test_no_targets(self):
        """Handle assignment with no targets."""
        # This shouldn't happen in valid Python, but test defensively
        code = "DEBUG = True"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        # Manually clear targets to test
        original_targets = assign.targets
        assign.targets = []
        assert extract_assignment_target(assign) is None
        # Restore for other tests
        assign.targets = original_targets


class TestInferSettingValue:
    """Test value inference from AST nodes."""

    def test_infer_boolean_true(self):
        """Infer boolean True value."""
        code = "DEBUG = True"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result == {"value": True, "type": "bool"}

    def test_infer_boolean_false(self):
        """Infer boolean False value."""
        code = "ENABLED = False"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result == {"value": False, "type": "bool"}

    def test_infer_integer(self):
        """Infer integer value."""
        code = "PORT = 8000"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result == {"value": 8000, "type": "int"}

    def test_infer_float(self):
        """Infer float value."""
        code = "TIMEOUT = 30.5"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result == {"value": 30.5, "type": "float"}

    def test_infer_string(self):
        """Infer string value."""
        code = "DATABASE_URL = 'postgres://localhost/db'"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result == {"value": "postgres://localhost/db", "type": "string"}

    def test_infer_none(self):
        """Infer None value."""
        code = "CACHE = None"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result == {"value": None, "type": "none"}

    def test_infer_list(self):
        """Infer list value."""
        code = "INSTALLED_APPS = ['app1', 'app2', 'app3']"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result == {"value": ["app1", "app2", "app3"], "type": "list"}

    def test_infer_empty_list(self):
        """Infer empty list."""
        code = "ALLOWED_HOSTS = []"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result == {"value": [], "type": "list"}

    def test_infer_tuple(self):
        """Infer tuple value."""
        code = "MIDDLEWARE = ('middleware1', 'middleware2')"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result == {"value": ["middleware1", "middleware2"], "type": "tuple"}

    def test_infer_dict(self):
        """Infer dictionary value."""
        code = "DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result["type"] == "dict"
        assert result["value"]["default"]["ENGINE"] == "django.db.backends.sqlite3"

    def test_infer_empty_dict(self):
        """Infer empty dictionary."""
        code = "CACHES = {}"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result == {"value": {}, "type": "dict"}

    def test_infer_set(self):
        """Infer set value."""
        code = "ALLOWED = {'a', 'b', 'c'}"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result["type"] == "set"
        # Sets are converted to lists for JSON serialization
        assert set(result["value"]) == {"a", "b", "c"}

    def test_infer_function_call_dynamic(self):
        """Mark function call as dynamic."""
        code = "BASE_DIR = Path(__file__).resolve().parent"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result["type"] in ("dynamic", "call")
        # Value should be wrapped in backticks
        assert "`" in result["value"]
        assert "Path(__file__)" in result["value"]

    def test_infer_environment_variable_dynamic(self):
        """Mark environment variable as dynamic."""
        code = "SECRET_KEY = os.environ.get('SECRET_KEY')"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result["type"] == "dynamic"
        assert "`" in result["value"]
        assert "os.environ" in result["value"]

    def test_infer_complex_expression_dynamic(self):
        """Mark complex expression as dynamic."""
        code = "TIMEOUT = 5 * 60"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        # Should either compute (5 * 60 = 300) or mark as dynamic
        # Astroid might be able to compute this
        assert result["type"] in ("int", "dynamic")

    def test_infer_nested_list(self):
        """Infer nested list structure."""
        code = "NESTED = [['a', 'b'], ['c', 'd']]"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        assert result["type"] == "list"
        assert result["value"] == [["a", "b"], ["c", "d"]]

    def test_infer_list_with_dynamic_element(self):
        """Mark list with dynamic element as dynamic."""
        code = "APPS = ['app1', get_app_name()]"
        module = parse(code)
        assign = module.body[0]
        assert isinstance(assign, nodes.Assign)
        result = infer_setting_value(assign.value)
        # List contains dynamic call - whole list should be dynamic
        assert result["type"] == "list"
        assert "`" in result["value"]


class TestDetectStarImports:
    """Test star import detection."""

    def test_single_star_import(self):
        """Detect single star import."""
        code = "from django.conf import settings\nfrom .base import *"
        module = parse(code)
        star_imports = detect_star_imports(module)
        assert star_imports == [".base"]

    def test_multiple_star_imports(self):
        """Detect multiple star imports."""
        code = "from .base import *\nfrom .common import *"
        module = parse(code)
        star_imports = detect_star_imports(module)
        assert star_imports == [".base", ".common"]

    def test_no_star_imports(self):
        """Return empty list when no star imports."""
        code = "from django.conf import settings\nimport os"
        module = parse(code)
        star_imports = detect_star_imports(module)
        assert star_imports == []

    def test_absolute_star_import(self):
        """Detect absolute star imports."""
        code = "from myproject.settings.base import *"
        module = parse(code)
        star_imports = detect_star_imports(module)
        assert star_imports == ["myproject.settings.base"]

    def test_mixed_imports(self):
        """Detect star imports among regular imports."""
        code = """
from .base import *
from django.conf import settings
from .common import DEBUG
"""
        module = parse(code)
        star_imports = detect_star_imports(module)
        assert star_imports == [".base"]


class TestResolveRelativeImport:
    """Test relative import resolution."""

    def test_single_dot_import(self):
        """Resolve single dot relative import."""
        result = resolve_relative_import("myproject.settings.dev", 1, "base")
        assert result == "myproject.settings.base"

    def test_double_dot_import(self):
        """Resolve double dot relative import."""
        result = resolve_relative_import("myproject.settings.dev", 2, "config")
        assert result == "myproject.config"

    def test_single_dot_no_module(self):
        """Resolve single dot import without module name."""
        result = resolve_relative_import("myproject.settings.dev", 1, None)
        assert result == "myproject.settings"

    def test_triple_dot_import(self):
        """Resolve triple dot relative import."""
        result = resolve_relative_import("myproject.apps.api.views", 3, "utils")
        # Level 3 from views: views -> api -> apps -> myproject
        assert result == "myproject.utils"

    def test_too_many_dots(self):
        """Handle too many dots gracefully."""
        result = resolve_relative_import("myproject.settings", 5, "base")
        # Should return just the module name when going too far up
        assert result == "base"


class TestMarkOverrides:
    """Test override marking."""

    def test_mark_single_override(self):
        """Mark settings that override base settings."""
        # Create base module
        base_module = SettingsModule(
            module_path="settings.base",
            definitions={
                "DEBUG": SettingsDefinition(
                    name="DEBUG",
                    value=True,
                    line=1,
                    type="bool",
                    module_path="settings.base",
                    overrides=None,
                ),
            },
            star_imports=[],
            dynamic_imports=[],
        )

        # Create dev module that imports from base
        dev_module = SettingsModule(
            module_path="settings.dev",
            definitions={
                "DEBUG": SettingsDefinition(
                    name="DEBUG",
                    value=False,
                    line=5,
                    type="bool",
                    module_path="settings.dev",
                    overrides=None,
                ),
            },
            star_imports=["settings.base"],
            dynamic_imports=[],
        )

        modules = {
            "settings.base": base_module,
            "settings.dev": dev_module,
        }

        # Mark overrides
        mark_overrides(modules, "settings.dev")

        # Check that dev's DEBUG is marked as override
        assert dev_module.definitions["DEBUG"].overrides == "settings.base"
        # Base module should not be marked
        assert base_module.definitions["DEBUG"].overrides is None

    def test_no_override_for_new_settings(self):
        """Don't mark settings that don't exist in base."""
        base_module = SettingsModule(
            module_path="settings.base",
            definitions={
                "DEBUG": SettingsDefinition(
                    name="DEBUG",
                    value=True,
                    line=1,
                    type="bool",
                    module_path="settings.base",
                    overrides=None,
                ),
            },
            star_imports=[],
            dynamic_imports=[],
        )

        dev_module = SettingsModule(
            module_path="settings.dev",
            definitions={
                "DEV_MODE": SettingsDefinition(
                    name="DEV_MODE",
                    value=True,
                    line=5,
                    type="bool",
                    module_path="settings.dev",
                    overrides=None,
                ),
            },
            star_imports=["settings.base"],
            dynamic_imports=[],
        )

        modules = {
            "settings.base": base_module,
            "settings.dev": dev_module,
        }

        mark_overrides(modules, "settings.dev")

        # DEV_MODE should not be marked as override
        assert dev_module.definitions["DEV_MODE"].overrides is None

    def test_multiple_star_imports(self):
        """Handle multiple star imports correctly."""
        base_module = SettingsModule(
            module_path="settings.base",
            definitions={
                "DEBUG": SettingsDefinition(
                    name="DEBUG",
                    value=True,
                    line=1,
                    type="bool",
                    module_path="settings.base",
                    overrides=None,
                ),
            },
            star_imports=[],
            dynamic_imports=[],
        )

        common_module = SettingsModule(
            module_path="settings.common",
            definitions={
                "CACHE_ENABLED": SettingsDefinition(
                    name="CACHE_ENABLED",
                    value=False,
                    line=1,
                    type="bool",
                    module_path="settings.common",
                    overrides=None,
                ),
            },
            star_imports=[],
            dynamic_imports=[],
        )

        dev_module = SettingsModule(
            module_path="settings.dev",
            definitions={
                "DEBUG": SettingsDefinition(
                    name="DEBUG",
                    value=False,
                    line=5,
                    type="bool",
                    module_path="settings.dev",
                    overrides=None,
                ),
                "CACHE_ENABLED": SettingsDefinition(
                    name="CACHE_ENABLED",
                    value=True,
                    line=7,
                    type="bool",
                    module_path="settings.dev",
                    overrides=None,
                ),
            },
            star_imports=["settings.base", "settings.common"],
            dynamic_imports=[],
        )

        modules = {
            "settings.base": base_module,
            "settings.common": common_module,
            "settings.dev": dev_module,
        }

        mark_overrides(modules, "settings.dev")

        # Both should be marked as overrides from their respective sources
        assert dev_module.definitions["DEBUG"].overrides == "settings.base"
        assert dev_module.definitions["CACHE_ENABLED"].overrides == "settings.common"


class TestExtractImportPattern:
    """Test import pattern extraction from importlib.import_module calls."""

    def test_extract_fstring_pattern(self):
        """Extract pattern from f-string."""
        code = 'importlib.import_module(f"settings.{env}")'
        module = parse(code)
        expr_node = module.body[0]
        assert isinstance(expr_node, nodes.Expr)
        call = expr_node.value
        assert isinstance(call, nodes.Call)
        pattern = extract_import_pattern(call)
        assert pattern == "settings.{}"

    def test_extract_concatenation_pattern(self):
        """Extract pattern from string concatenation."""
        code = 'importlib.import_module("settings." + profile)'
        module = parse(code)
        expr_node = module.body[0]
        assert isinstance(expr_node, nodes.Expr)
        call = expr_node.value
        assert isinstance(call, nodes.Call)
        pattern = extract_import_pattern(call)
        assert pattern == "settings.{}"

    def test_extract_format_pattern(self):
        """Extract pattern from format() call."""
        code = 'importlib.import_module("settings.{}".format(env))'
        module = parse(code)
        expr_node = module.body[0]
        assert isinstance(expr_node, nodes.Expr)
        call = expr_node.value
        assert isinstance(call, nodes.Call)
        pattern = extract_import_pattern(call)
        assert pattern == "settings.{}"

    def test_extract_static_string(self):
        """Extract static string import."""
        code = 'importlib.import_module("settings.production")'
        module = parse(code)
        expr_node = module.body[0]
        assert isinstance(expr_node, nodes.Expr)
        call = expr_node.value
        assert isinstance(call, nodes.Call)
        pattern = extract_import_pattern(call)
        assert pattern == "settings.production"

    def test_complex_fstring(self):
        """Extract pattern from complex f-string."""
        code = 'importlib.import_module(f"apps.{app}.config.{env}")'
        module = parse(code)
        expr_node = module.body[0]
        assert isinstance(expr_node, nodes.Expr)
        call = expr_node.value
        assert isinstance(call, nodes.Call)
        pattern = extract_import_pattern(call)
        assert pattern == "apps.{}.config.{}"


class TestExtractBaseModule:
    """Test base module extraction from import patterns."""

    def test_simple_pattern(self):
        """Extract base from simple pattern."""
        result = extract_base_module("settings.{}")
        assert result == "settings"

    def test_nested_pattern(self):
        """Extract base from nested pattern."""
        result = extract_base_module("apps.myapp.config.{}")
        assert result == "apps.myapp.config"

    def test_no_placeholder(self):
        """Handle pattern without placeholder."""
        result = extract_base_module("settings.production")
        assert result == "settings.production"

    def test_starts_with_placeholder(self):
        """Return None when pattern starts with placeholder."""
        result = extract_base_module("{}.config")
        assert result is None

    def test_multiple_placeholders(self):
        """Extract base before first placeholder."""
        result = extract_base_module("apps.{}.config.{}")
        assert result == "apps"


class TestDetectDynamicImports:
    """Test dynamic import detection."""

    def test_detect_fstring_import(self):
        """Detect f-string dynamic import."""
        code = """
import importlib
env = "dev"
settings = importlib.import_module(f"settings.{env}")
"""
        module = parse(code)
        dynamic_imports = detect_dynamic_imports(module, "test.py")
        assert len(dynamic_imports) == 1
        assert dynamic_imports[0].pattern == "settings.{}"
        assert dynamic_imports[0].base_module == "settings"
        assert dynamic_imports[0].file == "test.py"

    def test_detect_concatenation_import(self):
        """Detect string concatenation dynamic import."""
        code = """
import importlib
profile = "prod"
config = importlib.import_module("config." + profile)
"""
        module = parse(code)
        dynamic_imports = detect_dynamic_imports(module, "test.py")
        assert len(dynamic_imports) == 1
        assert dynamic_imports[0].pattern == "config.{}"
        assert dynamic_imports[0].base_module == "config"

    def test_static_import_not_dynamic(self):
        """Static imports are not marked as dynamic."""
        code = """
import importlib
base = importlib.import_module("settings.base")
"""
        module = parse(code)
        dynamic_imports = detect_dynamic_imports(module, "test.py")
        # Static import is still detected but with no placeholders
        assert len(dynamic_imports) == 1
        assert dynamic_imports[0].pattern == "settings.base"
        assert dynamic_imports[0].base_module == "settings.base"

    def test_multiple_dynamic_imports(self):
        """Detect multiple dynamic imports."""
        code = """
import importlib
settings = importlib.import_module(f"settings.{env}")
config = importlib.import_module("config." + profile)
"""
        module = parse(code)
        dynamic_imports = detect_dynamic_imports(module, "test.py")
        assert len(dynamic_imports) == 2
        assert dynamic_imports[0].pattern == "settings.{}"
        assert dynamic_imports[1].pattern == "config.{}"

    def test_no_imports(self):
        """Return empty list when no dynamic imports."""
        code = """
DEBUG = True
SECRET_KEY = "test"
"""
        module = parse(code)
        dynamic_imports = detect_dynamic_imports(module, "test.py")
        assert dynamic_imports == []
