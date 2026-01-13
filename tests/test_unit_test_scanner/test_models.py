"""Tests for unit test scanner models."""

import pytest
from pydantic import ValidationError

from upcast.models.unit_tests import (
    TargetModule,
    UnitTestInfo,
    UnitTestSummary,
    UnitTestOutput,
)


class TestTargetModuleModel:
    """Test TargetModule model."""

    def test_target_module_valid(self):
        """Test valid TargetModule creation."""
        target = TargetModule(module_path="myapp.models", symbols=["User", "Post"])
        assert target.module_path == "myapp.models"
        assert len(target.symbols) == 2


class TestUnitTestInfoModel:
    """Test UnitTestInfo model."""

    def test_unit_test_info_valid(self):
        """Test valid UnitTestInfo creation."""
        test = UnitTestInfo(
            name="test_addition",
            file="test_math.py",
            line_range=(10, 12),
            body_md5="abc123",
            assert_count=1,
            targets=[],
        )
        assert test.name == "test_addition"
        assert test.line_range == (10, 12)

    def test_unit_test_info_with_targets(self):
        """Test UnitTestInfo with targets."""
        test = UnitTestInfo(
            name="test_user",
            file="test_models.py",
            line_range=(5, 10),
            body_md5="def456",
            assert_count=2,
            targets=[TargetModule(module_path="myapp.models", symbols=["User"])],
        )
        assert len(test.targets) == 1


class TestUnitTestSummaryModel:
    """Test UnitTestSummary model."""

    def test_summary_valid(self):
        """Test valid UnitTestSummary creation."""
        summary = UnitTestSummary(
            total_count=10,
            files_scanned=3,
            scan_duration_ms=100,
            total_tests=10,
            total_files=3,
            total_assertions=25,
        )
        assert summary.total_tests == 10
        assert summary.total_assertions == 25


class TestUnitTestOutputModel:
    """Test UnitTestOutput model."""

    def test_output_valid(self):
        """Test valid UnitTestOutput creation."""
        test = UnitTestInfo(
            name="test_example",
            file="test_file.py",
            line_range=(1, 3),
            body_md5="hash",
            assert_count=1,
            targets=[],
        )
        output = UnitTestOutput(
            summary=UnitTestSummary(
                total_count=1,
                files_scanned=1,
                scan_duration_ms=50,
                total_tests=1,
                total_files=1,
                total_assertions=1,
            ),
            results={"test_file.py": [test]},
        )
        assert len(output.results) == 1
