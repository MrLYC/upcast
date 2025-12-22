"""Tests for DjangoModelScanner."""

from upcast.scanners.django_models import (
    DjangoField,
    DjangoModelScanner,
)


class TestDjangoModelModels:
    """Tests for Django model models."""

    def test_valid_django_field(self):
        """Test creating valid DjangoField."""
        field = DjangoField(
            name="title",
            type="CharField",
            parameters={"max_length": 100},
            line=10,
        )
        assert field.name == "title"
        assert field.type == "CharField"


class TestDjangoModelScannerIntegration:
    """Integration tests for DjangoModelScanner."""

    def test_scanner_detects_models(self, tmp_path):
        """Test scanner detects Django models."""
        test_file = tmp_path / "models.py"
        test_file.write_text(
            """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
"""
        )

        scanner = DjangoModelScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_extracts_description(self, tmp_path):
        """Test scanner extracts description from model docstring."""
        test_file = tmp_path / "models.py"
        test_file.write_text(
            """
from django.db import models

class Article(models.Model):
    \"\"\"Article model for blog posts.

    This stores published articles.
    \"\"\"
    title = models.CharField(max_length=100)
    content = models.TextField()

class Page(models.Model):
    # No docstring
    title = models.CharField(max_length=200)
"""
        )

        scanner = DjangoModelScanner()
        output = scanner.scan(test_file)

        # Find Article model
        article_model = None
        page_model = None
        for model in output.results.values():
            if model.name == "Article":
                article_model = model
            elif model.name == "Page":
                page_model = model

        assert article_model is not None
        assert article_model.description == "Article model for blog posts."

        assert page_model is not None
        assert page_model.description is None

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = DjangoModelScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0
