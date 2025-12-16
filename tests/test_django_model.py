"""Tests for Django model scanner."""

from pathlib import Path
from textwrap import dedent

import pytest
import yaml

from upcast.django_model_scanner import scan_django_models


@pytest.fixture
def temp_django_project(tmp_path: Path) -> Path:
    """Create a temporary Django project with test models."""
    # Create models.py with test models
    models_file = tmp_path / "models.py"
    models_file.write_text(
        dedent(
            """
        from django.db import models


        class Author(models.Model):
            first_name = models.CharField(max_length=100)
            last_name = models.CharField(max_length=100)
            email = models.EmailField(unique=True)

            class Meta:
                db_table = "authors"
                unique_together = [("first_name", "last_name")]


        class Book(models.Model):
            title = models.CharField(max_length=200)
            author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="books")
            published_date = models.DateField()
            isbn = models.CharField(max_length=13, unique=True)

            class Meta:
                db_table = "books"
                ordering = ["-published_date"]
    """
        )
    )

    return tmp_path


@pytest.fixture
def temp_abstract_models(tmp_path: Path) -> Path:
    """Create temporary Django project with abstract models."""
    models_file = tmp_path / "models.py"
    models_file.write_text(
        dedent(
            """
        from django.db import models


        class TimeStampedModel(models.Model):
            created_at = models.DateTimeField(auto_now_add=True)
            updated_at = models.DateTimeField(auto_now=True)

            class Meta:
                abstract = True


        class Article(TimeStampedModel):
            title = models.CharField(max_length=200)
            content = models.TextField()

            class Meta:
                db_table = "articles"
    """
        )
    )

    return tmp_path


class TestDjangoModelScanner:
    """Test the Django model scanner functionality."""

    def test_basic_model_detection(self, temp_django_project: Path) -> None:
        """Test basic Django model detection."""
        result = scan_django_models(str(temp_django_project))
        models = yaml.safe_load(result)

        # Should find 2 models: Author and Book
        assert len(models) >= 2

        # Check Author model exists
        author_models = [k for k in models if k.endswith("Author")]
        assert len(author_models) == 1

        author_key = author_models[0]
        author = models[author_key]

        assert author["abstract"] is False
        assert "first_name" in author["fields"]
        assert "last_name" in author["fields"]
        assert "email" in author["fields"]

    def test_field_types_and_options(self, temp_django_project: Path) -> None:
        """Test field type detection and option extraction."""
        result = scan_django_models(str(temp_django_project))
        models = yaml.safe_load(result)

        author_models = [k for k in models if k.endswith("Author")]
        author = models[author_models[0]]

        # Check field types
        assert author["fields"]["first_name"]["type"] == "CharField"
        assert author["fields"]["email"]["type"] == "EmailField"

        # Check field options
        assert author["fields"]["first_name"]["max_length"] == 100
        assert author["fields"]["email"]["unique"] is True

    def test_relationship_fields(self, temp_django_project: Path) -> None:
        """Test relationship field detection."""
        result = scan_django_models(str(temp_django_project))
        models = yaml.safe_load(result)

        book_models = [k for k in models if k.endswith("Book")]
        book = models[book_models[0]]

        # Should have relationships section
        assert "relationships" in book
        assert "author" in book["relationships"]

        # Check relationship details
        author_rel = book["relationships"]["author"]
        assert author_rel["type"] == "ForeignKey"
        assert "Author" in author_rel["to"]
        assert author_rel["related_name"] == "books"

    def test_meta_class_options(self, temp_django_project: Path) -> None:
        """Test Meta class option extraction."""
        result = scan_django_models(str(temp_django_project))
        models = yaml.safe_load(result)

        author_models = [k for k in models if k.endswith("Author")]
        author = models[author_models[0]]

        # Check Meta options
        assert "meta" in author
        assert author["meta"]["db_table"] == "authors"
        assert author["meta"]["unique_together"] == [["first_name", "last_name"]]

    def test_abstract_model_inheritance(self, temp_abstract_models: Path) -> None:
        """Test abstract model inheritance and field merging."""
        result = scan_django_models(str(temp_abstract_models))
        models = yaml.safe_load(result)

        # Should find both abstract and concrete models
        timestamped_models = [k for k in models if k.endswith("TimeStampedModel")]
        article_models = [k for k in models if k.endswith("Article")]

        assert len(timestamped_models) == 1
        assert len(article_models) == 1

        # Check abstract model
        timestamped = models[timestamped_models[0]]
        assert timestamped["abstract"] is True
        assert "created_at" in timestamped["fields"]
        assert "updated_at" in timestamped["fields"]

        # Check concrete model has inherited fields
        article = models[article_models[0]]
        assert article["abstract"] is False
        assert "title" in article["fields"]
        assert "content" in article["fields"]
        # Abstract fields should be merged
        assert "created_at" in article["fields"]
        assert "updated_at" in article["fields"]

    def test_output_to_file(self, temp_django_project: Path, tmp_path: Path) -> None:
        """Test writing output to a file."""
        output_file = tmp_path / "models.yaml"
        result = scan_django_models(str(temp_django_project), output=str(output_file))

        # Should return empty string when writing to file
        assert result == ""

        # File should exist and contain valid YAML
        assert output_file.exists()

        with open(output_file) as f:
            models = yaml.safe_load(f)

        assert len(models) >= 2

    def test_nonexistent_path(self) -> None:
        """Test error handling for nonexistent path."""
        with pytest.raises(FileNotFoundError):
            scan_django_models("/nonexistent/path")

    def test_single_file_scan(self, temp_django_project: Path) -> None:
        """Test scanning a single Python file."""
        models_file = temp_django_project / "models.py"
        result = scan_django_models(str(models_file))
        models = yaml.safe_load(result)

        # Should find models in the single file
        assert len(models) >= 2
