"""Tests for CLI module."""

import tempfile
from pathlib import Path

import yaml
from click.testing import CliRunner

from upcast.http_request_scanner.cli import scan_http_requests


def test_scan_http_requests_basic():
    """Test basic CLI scanning."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a simple test file
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("""
import requests
requests.get('https://api.example.com/users')
""")

        result = runner.invoke(scan_http_requests, [tmpdir])

        assert result.exit_code == 0
        # Parse YAML output
        output = yaml.safe_load(result.output)
        assert "https://api.example.com/users" in output


def test_scan_http_requests_output_file():
    """Test CLI with output file."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test file
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("""
import requests
requests.get('https://api.example.com/data')
""")

        # Output file
        output_file = Path(tmpdir) / "output.yaml"

        result = runner.invoke(scan_http_requests, [tmpdir, "-o", str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()

        # Check output file content
        with output_file.open() as f:
            output = yaml.safe_load(f)
        assert "https://api.example.com/data" in output


def test_scan_http_requests_json_format():
    """Test CLI with JSON format."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("""
import requests
requests.get('https://example.com')
""")

        result = runner.invoke(scan_http_requests, [tmpdir, "--format", "json"])

        assert result.exit_code == 0
        # Output should be valid JSON
        import json

        output = json.loads(result.output)
        assert "https://example.com" in output


def test_scan_http_requests_verbose():
    """Test CLI with verbose flag."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("""
import requests
requests.get('https://example.com')
""")

        result = runner.invoke(scan_http_requests, [tmpdir, "-v"])

        assert result.exit_code == 0
        # Verbose mode should show scanning messages
        assert "Scanning" in result.output or "Processing" in result.output


def test_scan_http_requests_single_file():
    """Test CLI scanning a single file."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("""
import requests
requests.get('https://api.example.com/users')
""")

        result = runner.invoke(scan_http_requests, [str(test_file)])

        assert result.exit_code == 0
        output = yaml.safe_load(result.output)
        assert "https://api.example.com/users" in output


def test_scan_http_requests_no_requests():
    """Test CLI with file containing no HTTP requests."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("""
def hello():
    return "Hello, World!"
""")

        result = runner.invoke(scan_http_requests, [tmpdir])

        assert result.exit_code == 0
        output = yaml.safe_load(result.output)
        # Should have summary but no URLs
        assert "summary" in output
        assert output["summary"]["total_requests"] == 0


def test_scan_http_requests_multiple_files():
    """Test CLI scanning multiple files."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create multiple test files
        file1 = Path(tmpdir) / "file1.py"
        file1.write_text("""
import requests
requests.get('https://api.example.com/users')
""")

        file2 = Path(tmpdir) / "file2.py"
        file2.write_text("""
import requests
requests.post('https://api.example.com/login', json={'user': 'admin'})
""")

        result = runner.invoke(scan_http_requests, [tmpdir])

        assert result.exit_code == 0
        output = yaml.safe_load(result.output)
        assert "https://api.example.com/users" in output
        assert "https://api.example.com/login" in output
        assert output["summary"]["total_requests"] == 2
