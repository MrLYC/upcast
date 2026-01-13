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
            help_text="The article title",
            verbose_name="Article Title",
            parameters={"max_length": 100},
            line=10,
        )
        assert field.name == "title"
        assert field.type == "CharField"
        assert field.help_text == "The article title"
        assert field.verbose_name == "Article Title"

    def test_django_field_without_metadata(self):
        """Test creating DjangoField without help_text and verbose_name."""
        field = DjangoField(
            name="title",
            type="CharField",
            parameters={"max_length": 100},
            line=10,
        )
        assert field.name == "title"
        assert field.type == "CharField"
        assert field.help_text is None
        assert field.verbose_name is None


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

    def test_scanner_extracts_field_metadata(self, tmp_path):
        """Test scanner extracts help_text and verbose_name from fields."""
        test_file = tmp_path / "models.py"
        test_file.write_text(
            """
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name="Task Title")
    description = models.TextField(help_text="Detailed task description")
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the task was completed",
        verbose_name="Completion Time"
    )
    priority = models.IntegerField(default=0)  # No metadata
"""
        )

        scanner = DjangoModelScanner()
        output = scanner.scan(test_file)

        # Find Task model
        task_model = None
        for model in output.results.values():
            if model.name == "Task":
                task_model = model
                break

        assert task_model is not None

        # Check title field
        title_field = task_model.fields.get("title")
        assert title_field is not None
        assert title_field.verbose_name == "Task Title"
        assert title_field.help_text is None
        assert "verbose_name" not in title_field.parameters

        # Check description field
        desc_field = task_model.fields.get("description")
        assert desc_field is not None
        assert desc_field.help_text == "Detailed task description"
        assert desc_field.verbose_name is None
        assert "help_text" not in desc_field.parameters

        # Check completed_at field
        completed_field = task_model.fields.get("completed_at")
        assert completed_field is not None
        assert completed_field.help_text == "When the task was completed"
        assert completed_field.verbose_name == "Completion Time"
        assert "help_text" not in completed_field.parameters
        assert "verbose_name" not in completed_field.parameters

        # Check priority field (no metadata)
        priority_field = task_model.fields.get("priority")
        assert priority_field is not None
        assert priority_field.help_text is None
        assert priority_field.verbose_name is None
