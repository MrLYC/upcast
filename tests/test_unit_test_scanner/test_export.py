"""Tests for export module."""

from upcast.unit_test_scanner.export import export_to_json, export_to_yaml, format_test_output
from upcast.unit_test_scanner.test_parser import TargetModule, UnitTestInfo


class TestFormatTestOutput:
    """Test output formatting."""

    def test_format_empty_tests(self):
        """Test formatting with no tests."""
        result = format_test_output([])
        assert result == {}

    def test_format_single_test(self):
        """Test formatting a single test."""
        test = UnitTestInfo(
            name="test_example",
            location="test_file.py:10",
            file="test_file.py",
            line=10,
            line_range=(10, 10),
            body_md5="abcd1234" * 4,
            assert_count=2,
            targets=[TargetModule(module="app.utils", symbols=["func1", "func2"])],
        )

        result = format_test_output([test])

        assert "test_file.py" in result
        assert len(result["test_file.py"]) == 1

        test_data = result["test_file.py"][0]
        assert test_data["name"] == "test_example"
        assert test_data["body_md5"] == "abcd1234" * 4
        assert test_data["assert_count"] == 2
        assert len(test_data["targets"]) == 1
        assert test_data["targets"][0]["module"] == "app.utils"
        assert set(test_data["targets"][0]["symbols"]) == {"func1", "func2"}

    def test_format_multiple_tests_same_file(self):
        """Test formatting multiple tests from same file."""
        tests = [
            UnitTestInfo(
                name="test_one",
                location="test_file.py:10",
                file="test_file.py",
                line=10,
                line_range=(10, 10),
                body_md5="a" * 32,
                assert_count=1,
                targets=[],
            ),
            UnitTestInfo(
                name="test_two",
                location="test_file.py:20",
                file="test_file.py",
                line=20,
                line_range=(20, 20),
                body_md5="b" * 32,
                assert_count=2,
                targets=[],
            ),
        ]

        result = format_test_output(tests)

        assert "test_file.py" in result
        assert len(result["test_file.py"]) == 2

        # Check sorting by line number
        assert result["test_file.py"][0]["name"] == "test_one"
        assert result["test_file.py"][1]["name"] == "test_two"

    def test_format_tests_multiple_files(self):
        """Test formatting tests from multiple files."""
        tests = [
            UnitTestInfo(
                name="test_a",
                location="a.py:10",
                file="a.py",
                line=10,
                line_range=(10, 10),
                body_md5="a" * 32,
                assert_count=1,
                targets=[],
            ),
            UnitTestInfo(
                name="test_b",
                location="b.py:10",
                file="b.py",
                line=10,
                line_range=(10, 10),
                body_md5="b" * 32,
                assert_count=1,
                targets=[],
            ),
        ]

        result = format_test_output(tests)

        assert "a.py" in result
        assert "b.py" in result
        assert len(result) == 2

    def test_format_empty_targets(self):
        """Test formatting test with no targets."""
        test = UnitTestInfo(
            name="test_example",
            location="test_file.py:10",
            file="test_file.py",
            line=10,
            line_range=(10, 10),
            body_md5="a" * 32,
            assert_count=1,
            targets=[],
        )

        result = format_test_output([test])

        test_data = result["test_file.py"][0]
        assert test_data["targets"] == []


class TestExportToYAML:
    """Test YAML export."""

    def test_export_to_string(self):
        """Test exporting to YAML string."""
        test = UnitTestInfo(
            name="test_example",
            location="test_file.py:10",
            file="test_file.py",
            line=10,
            line_range=(10, 10),
            body_md5="a" * 32,
            assert_count=2,
            targets=[],
        )

        yaml_str = export_to_yaml([test])

        assert "test_file.py:" in yaml_str
        assert "test_example" in yaml_str
        assert "body_md5:" in yaml_str
        assert "assert_count: 2" in yaml_str

    def test_export_to_file(self, tmp_path):
        """Test exporting to YAML file."""
        test = UnitTestInfo(
            name="test_example",
            location="test_file.py:10",
            file="test_file.py",
            line=10,
            line_range=(10, 10),
            body_md5="a" * 32,
            assert_count=2,
            targets=[],
        )

        output_file = tmp_path / "output.yaml"
        export_to_yaml([test], output_file)

        assert output_file.exists()
        content = output_file.read_text()
        assert "test_example" in content


class TestExportToJSON:
    """Test JSON export."""

    def test_export_to_string(self):
        """Test exporting to JSON string."""
        test = UnitTestInfo(
            name="test_example",
            location="test_file.py:10",
            file="test_file.py",
            line=10,
            line_range=(10, 10),
            body_md5="a" * 32,
            assert_count=2,
            targets=[],
        )

        json_str = export_to_json([test])

        assert '"test_file.py"' in json_str
        assert '"test_example"' in json_str
        assert '"assert_count": 2' in json_str

    def test_export_to_file(self, tmp_path):
        """Test exporting to JSON file."""
        test = UnitTestInfo(
            name="test_example",
            location="test_file.py:10",
            file="test_file.py",
            line=10,
            line_range=(10, 10),
            body_md5="a" * 32,
            assert_count=2,
            targets=[],
        )

        output_file = tmp_path / "output.json"
        export_to_json([test], output_file)

        assert output_file.exists()
        content = output_file.read_text()
        assert '"test_example"' in content
