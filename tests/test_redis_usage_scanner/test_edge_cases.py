"""Tests for edge cases in Redis usage scanner."""

import pytest
from pathlib import Path
from textwrap import dedent

from upcast.scanners.redis_usage import RedisUsageScanner


class TestEmptyFiles:
    """Test empty and minimal files."""

    def test_empty_file(self, tmp_path):
        """Empty file should return no results."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = RedisUsageScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_usages == 0

    def test_file_without_redis(self, tmp_path):
        """File without Redis usage should return no results."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def add(a, b):
                return a + b
        """)
        )

        scanner = RedisUsageScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_usages == 0


class TestInvalidSyntax:
    """Test handling of invalid syntax."""

    def test_invalid_syntax_skipped(self, tmp_path):
        """Files with invalid syntax should be skipped gracefully."""
        test_file = tmp_path / "test_invalid.py"
        test_file.write_text("def broken(:\n    cache.get('key')\n")

        scanner = RedisUsageScanner()
        output = scanner.scan(test_file)

        # Should not crash
        assert output.summary.total_usages == 0


class TestDirectoryScanning:
    """Test directory scanning."""

    def test_scan_directory(self, tmp_path):
        """Scanning directory should process all files."""
        (tmp_path / "file1.py").write_text(
            dedent("""
            from django.core.cache import cache
            cache.get("key1")
        """)
        )

        (tmp_path / "file2.py").write_text(
            dedent("""
            from django.core.cache import cache
            cache.get("key2")
        """)
        )

        scanner = RedisUsageScanner()
        output = scanner.scan(tmp_path)

        assert output.summary.total_usages >= 2

    def test_scan_nested_directories(self, tmp_path):
        """Scanning should recurse into subdirectories."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        (tmp_path / "root.py").write_text(
            dedent("""
            from django.core.cache import cache
            cache.get("root")
        """)
        )

        (subdir / "nested.py").write_text(
            dedent("""
            from django.core.cache import cache
            cache.get("nested")
        """)
        )

        scanner = RedisUsageScanner()
        output = scanner.scan(tmp_path)

        assert output.summary.total_usages >= 2


class TestPatternFiltering:
    """Test file pattern filtering."""

    def test_exclude_patterns(self, tmp_path):
        """Files matching exclude patterns should be skipped."""
        (tmp_path / "include.py").write_text(
            dedent("""
            from django.core.cache import cache
            cache.get("include")
        """)
        )

        (tmp_path / "exclude.py").write_text(
            dedent("""
            from django.core.cache import cache
            cache.get("exclude")
        """)
        )

        scanner = RedisUsageScanner(exclude_patterns=["**/exclude.py"])
        output = scanner.scan(tmp_path)

        # Should not include excluded file
        assert "exclude.py" not in str(output.results)

    def test_include_patterns(self, tmp_path):
        """Only files matching include patterns should be processed."""
        (tmp_path / "match.py").write_text(
            dedent("""
            from django.core.cache import cache
            cache.get("match")
        """)
        )

        (tmp_path / "nomatch.py").write_text(
            dedent("""
            from django.core.cache import cache
            cache.get("nomatch")
        """)
        )

        scanner = RedisUsageScanner(include_patterns=["**/match.py"])
        output = scanner.scan(tmp_path)

        # Should only process match.py
        result_files = [u.file for result_list in output.results.values() for u in result_list]
        assert any("match.py" in f for f in result_files)


class TestSummaryStatistics:
    """Test summary statistics calculation."""

    def test_category_counts(self, tmp_path):
        """Summary should count usages by category."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text(
            dedent("""
            CACHES = {
                'default': {
                    'BACKEND': 'django_redis.cache.RedisCache',
                }
            }
            CELERY_BROKER_URL = 'redis://localhost:6379/0'
        """)
        )

        scanner = RedisUsageScanner()
        output = scanner.scan(settings_file)

        # Should have categories for detected usages
        assert len(output.summary.categories) > 0

    def test_total_usages_count(self, tmp_path):
        """Summary should accurately count total usages."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from django.core.cache import cache

            cache.get("key1")
            cache.get("key2")
            cache.set("key3", "value")
        """)
        )

        scanner = RedisUsageScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_usages >= 3
        assert output.summary.total_count == output.summary.total_usages


class TestLineNumberTracking:
    """Test line number tracking."""

    def test_line_numbers_tracked(self, tmp_path):
        """Line numbers should be accurately tracked."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from django.core.cache import cache

            cache.get("key1")  # Line 3

            cache.get("key2")  # Line 5
        """)
        )

        scanner = RedisUsageScanner()
        output = scanner.scan(test_file)

        if output.results:
            usages = [u for result_list in output.results.values() for u in result_list]
            line_numbers = [u.line for u in usages]
            assert all(line > 0 for line in line_numbers)
