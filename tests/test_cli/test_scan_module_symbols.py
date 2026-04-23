"""Functional tests for the scan-module-symbols command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_module_symbols_project(tmp_project):
    return tmp_project({
        "app.py": """
PUBLIC_VALUE = 1
_PRIVATE_VALUE = 2


def public_function():
    return PUBLIC_VALUE


def _private_function():
    return _PRIVATE_VALUE


class PublicClass:
    pass


class _PrivateClass:
    pass
"""
    })


def test_scan_module_symbols_outputs_yaml(tmp_project):
    """The command should emit only public symbols by default."""
    project_dir = _create_module_symbols_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-module-symbols", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_symbols"] == 3

    file_info = output["results"]["app.py"]
    assert "PUBLIC_VALUE" in file_info["variables"]
    assert "public_function" in file_info["functions"]
    assert "PublicClass" in file_info["classes"]
    assert "_PRIVATE_VALUE" not in file_info["variables"]
    assert "_private_function" not in file_info["functions"]
    assert "_PrivateClass" not in file_info["classes"]


def test_scan_module_symbols_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_module_symbols_project(tmp_project)
    output_file = tmp_path / "module-symbols.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-module-symbols", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_symbols"] == 3
    assert "app.py" in output["results"]


def test_scan_module_symbols_includes_private_symbols(tmp_project):
    """The include-private option should expose private variables, functions, and classes."""
    project_dir = _create_module_symbols_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-module-symbols", str(project_dir), "--include-private"])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_symbols"] == 6

    file_info = output["results"]["app.py"]
    assert "_PRIVATE_VALUE" in file_info["variables"]
    assert "_private_function" in file_info["functions"]
    assert "_PrivateClass" in file_info["classes"]
