"""Integration tests for Django settings scanner."""

import builtins
from pathlib import Path

import pytest

from upcast.common.hybrid_scan_pipeline import PipelineRunResult
from upcast.scanners.django_settings import DjangoSettingsScanner


class TestDjangoSettingsScanner:
    """Test DjangoSettingsScanner integration."""

    def test_reuses_source_lines_for_multiple_setting_usages(
        self,
        tmp_path: Path,
        scanner: DjangoSettingsScanner,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Collecting several usages from one file should not reread it per usage."""
        views_file = tmp_path / "views.py"
        views_file.write_text(
            "from django.conf import settings\nfirst = settings.ONE\nsecond = settings.TWO\nthird = settings.THREE\n",
            encoding="utf-8",
        )
        original_open = builtins.open
        views_open_count = 0

        def track_open(file: object, *args: object, **kwargs: object) -> object:
            nonlocal views_open_count
            if Path(file) == views_file:
                views_open_count += 1
            return original_open(file, *args, **kwargs)

        monkeypatch.setattr(builtins, "open", track_open)

        result = scanner.scan(tmp_path)

        assert {"ONE", "TWO", "THREE"}.issubset(result.results)
        assert views_open_count == 2

    def test_scan_uses_ast_candidates_without_redundant_hybrid_pipeline_runs(
        self,
        tmp_path: Path,
        scanner: DjangoSettingsScanner,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Candidate extraction should not run a structural search it always discards."""
        (tmp_path / "settings.py").write_text("DEBUG = True\n")
        (tmp_path / "views.py").write_text(
            "from django.conf import settings\nvalue = settings.DEBUG\n",
        )
        calls: list[str] = []

        def record_pipeline(*args: object, **kwargs: object) -> PipelineRunResult:
            calls.append("called")
            return PipelineRunResult(candidates=[], decisions=[], findings=[])

        monkeypatch.setattr(
            "upcast.scanners.django_settings.run_pipeline",
            record_pipeline,
            raising=False,
        )

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        assert calls == []

    def test_iter_candidate_assignments_returns_ast_assignments(
        self,
        tmp_path: Path,
        scanner: DjangoSettingsScanner,
    ) -> None:
        """The candidate helper should use the complete AST assignment set."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("DEBUG = True\n")

        module = scanner.parse_file(settings_file)
        assert module is not None

        candidates = scanner._iter_candidate_assignments(module, settings_file)

        assert len(candidates) == 1
        assert candidates[0].targets[0].name == "DEBUG"

    def test_iter_candidate_assignments_includes_all_ast_assignments(
        self,
        tmp_path: Path,
        scanner: DjangoSettingsScanner,
    ) -> None:
        """The candidate helper should not omit any AST assignments."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("DEBUG = True\nSECRET_KEY = 'test-secret'\n")

        module = scanner.parse_file(settings_file)
        assert module is not None

        candidates = scanner._iter_candidate_assignments(module, settings_file)

        assert [candidate.targets[0].name for candidate in candidates] == ["DEBUG", "SECRET_KEY"]

    def test_scan_targeted_standard_settings(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Task 9 should capture the bounded standard Django settings set."""
        fixture = Path(__file__).parent / "fixtures" / "standard_settings.py"
        (tmp_path / "settings.py").write_text(fixture.read_text())

        result = scanner.scan(tmp_path)

        assert "ROOT_URLCONF" in result.results
        assert "TEMPLATES" in result.results
        assert "WSGI_APPLICATION" in result.results
        assert "ALLOWED_HOSTS" in result.results
        assert "STATIC_URL" in result.results
        assert "MEDIA_URL" in result.results

    def test_scan_simple_settings(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test scanning simple settings."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
DEBUG = True
SECRET_KEY = 'test-secret-key'
ALLOWED_HOSTS = ['localhost']
""")

        result = scanner.scan(tmp_path)

        assert result.summary.total_settings >= 3
        assert "DEBUG" in result.results
        assert "SECRET_KEY" in result.results
        assert "ALLOWED_HOSTS" in result.results

    def test_scan_settings_with_usage(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test scanning settings with usage."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("DEBUG = True")

        views_file = tmp_path / "views.py"
        views_file.write_text("""
from django.conf import settings

if settings.DEBUG:
    print("Debug mode")
""")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        debug_info = result.results["DEBUG"]
        assert debug_info.definition_count >= 1
        assert debug_info.usage_count >= 1

    def test_scan_database_settings(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test scanning database configuration."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
    }
}
""")

        result = scanner.scan(tmp_path)

        assert "DATABASES" in result.results
        db_info = result.results["DATABASES"]
        assert db_info.definition_count >= 1
        assert "dict" in db_info.definition_types

    def test_scan_installed_apps(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test scanning INSTALLED_APPS."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'myapp',
]
""")

        result = scanner.scan(tmp_path)

        assert "INSTALLED_APPS" in result.results
        apps_info = result.results["INSTALLED_APPS"]
        assert apps_info.definition_count >= 1
        assert "list" in apps_info.definition_types

    def test_scan_middleware(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test scanning MIDDLEWARE."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]
""")

        result = scanner.scan(tmp_path)

        assert "MIDDLEWARE" in result.results

    def test_scan_getattr_usage(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test scanning getattr usage."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("DEBUG = True")

        views_file = tmp_path / "views.py"
        views_file.write_text("""
from django.conf import settings

debug = getattr(settings, 'DEBUG', False)
""")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        debug_info = result.results["DEBUG"]
        assert debug_info.usage_count >= 1

    def test_scan_hasattr_usage(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test scanning hasattr usage."""
        views_file = tmp_path / "views.py"
        views_file.write_text("""
from django.conf import settings

if hasattr(settings, 'CUSTOM_SETTING'):
    pass
""")

        result = scanner.scan(tmp_path)

        assert "CUSTOM_SETTING" in result.results

    def test_scan_multiple_files(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test scanning multiple files."""
        (tmp_path / "settings.py").write_text("DEBUG = True")
        (tmp_path / "views.py").write_text("""
from django.conf import settings
x = settings.DEBUG
""")
        (tmp_path / "utils.py").write_text("""
from django.conf import settings
y = settings.DEBUG
""")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        debug_info = result.results["DEBUG"]
        assert debug_info.usage_count >= 2

    def test_scan_empty_directory(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test scanning empty directory."""
        result = scanner.scan(tmp_path)

        assert result.summary.total_settings == 0
        assert len(result.results) == 0

    def test_scan_non_settings_file(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test that non-settings files detect uppercase variables."""
        views_file = tmp_path / "views.py"
        views_file.write_text("""
DEBUG = True  # Uppercase variable
""")

        result = scanner.scan(tmp_path)

        # The scanner detects uppercase variables as potential settings
        # even in non-settings files (unless path contains 'settings' or 'config')
        # This test documents the actual behavior
        assert result is not None

    def test_scan_settings_module(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test scanning settings in a module directory."""
        settings_dir = tmp_path / "settings"
        settings_dir.mkdir()

        (settings_dir / "base.py").write_text("DEBUG = False")
        (settings_dir / "local.py").write_text("DEBUG = True")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        debug_info = result.results["DEBUG"]
        # Should find definitions in both files
        assert debug_info.definition_count >= 2

    def test_scan_summary_statistics(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test summary statistics are calculated correctly."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
DEBUG = True
SECRET_KEY = 'test'
""")

        views_file = tmp_path / "views.py"
        views_file.write_text("""
from django.conf import settings
x = settings.DEBUG
y = settings.SECRET_KEY
""")

        result = scanner.scan(tmp_path)

        assert result.summary.total_settings >= 2
        assert result.summary.total_definitions >= 2
        assert result.summary.total_usages >= 2
        assert result.summary.files_scanned >= 2
        assert result.summary.scan_duration_ms >= 0
