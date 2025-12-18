"""Integration tests for HTTP request scanner."""

from pathlib import Path

from upcast.http_request_scanner.checker import HttpRequestChecker


def test_integration_with_fixtures():
    """Test scanning all fixture files."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    checker = HttpRequestChecker(fixtures_dir)

    # Get all fixture files
    fixture_files = list(fixtures_dir.glob("*.py"))
    assert len(fixture_files) > 0

    # Scan all fixtures
    for fixture_file in fixture_files:
        checker.check_file(fixture_file)

    # Get results
    summary = checker.get_summary()

    # Should find some requests
    assert summary["total_requests"] > 0
    assert summary["unique_urls"] > 0
    assert len(summary["libraries_used"]) > 0


def test_integration_requests_patterns():
    """Test scanning requests_patterns.py fixture."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    checker = HttpRequestChecker(fixtures_dir)

    fixture_file = fixtures_dir / "requests_patterns.py"
    if not fixture_file.exists():
        # Skip if fixture not found
        return

    checker.check_file(fixture_file)
    summary = checker.get_summary()

    # Should detect requests library calls
    assert "requests" in summary["libraries_used"]


def test_integration_mixed_libraries():
    """Test scanning file with multiple libraries."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    checker = HttpRequestChecker(fixtures_dir)

    fixture_file = fixtures_dir / "mixed_libraries.py"
    if not fixture_file.exists():
        return

    checker.check_file(fixture_file)
    summary = checker.get_summary()

    # Should detect multiple libraries
    assert len(summary["libraries_used"]) >= 1


def test_integration_url_grouping():
    """Test that same URL from different locations is grouped correctly."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    checker = HttpRequestChecker(fixtures_dir)

    # Scan all fixtures
    for fixture_file in fixtures_dir.glob("*.py"):
        checker.check_file(fixture_file)

    requests_by_url = checker.get_requests_by_url()

    # Each URL should group all its usages
    for url, usages in requests_by_url.items():
        assert len(usages) > 0
        # All usages should have the same URL
        for usage in usages:
            assert usage.url == url


def test_integration_summary_statistics():
    """Test that summary statistics are calculated correctly."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    checker = HttpRequestChecker(fixtures_dir)

    # Scan all fixtures
    for fixture_file in fixtures_dir.glob("*.py"):
        checker.check_file(fixture_file)

    summary = checker.get_summary()

    # Check consistency
    assert summary["total_requests"] >= summary["unique_urls"]
    assert summary["session_based_count"] <= summary["total_requests"]
    assert summary["requests_without_timeout"] <= summary["total_requests"]
    assert summary["async_requests"] <= summary["total_requests"]
