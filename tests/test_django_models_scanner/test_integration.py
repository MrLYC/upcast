"""Integration tests for Django model scanner."""

from pathlib import Path

import pytest

from upcast.scanners.django_models import DjangoModelScanner


class TestDjangoModelScanner:
    """Test DjangoModelScanner integration."""

    def test_scan_simple_model(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning a simple Django model."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 1
        assert result.summary.total_fields == 2
        assert len(result.results) == 1

        # Check model
        model_key = list(result.results.keys())[0]
        model = result.results[model_key]
        assert model.name == "Article"
        assert len(model.fields) == 2
        assert "title" in model.fields
        assert "content" in model.fields

    def test_scan_model_with_foreign_key(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning model with ForeignKey."""
        code = """
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 2
        assert result.summary.total_relationships >= 1

        # Find Article model
        article = None
        for model in result.results.values():
            if model.name == "Article":
                article = model
                break

        assert article is not None
        assert len(article.relationships) >= 1
        assert any(rel.field == "author" for rel in article.relationships)

    def test_scan_model_with_many_to_many(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning model with ManyToManyField."""
        code = """
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Article(models.Model):
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name='articles')
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 2

        # Find Article model
        article = None
        for model in result.results.values():
            if model.name == "Article":
                article = model
                break

        assert article is not None
        assert len(article.relationships) >= 1
        m2m_rel = next((rel for rel in article.relationships if rel.field == "tags"), None)
        assert m2m_rel is not None
        assert m2m_rel.type == "models.ManyToManyField"

    def test_scan_model_with_meta(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning model with Meta class."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 1

        model = list(result.results.values())[0]
        assert model.meta is not None
        assert "ordering" in model.meta
        assert model.meta["verbose_name"] == "Article"

    def test_scan_abstract_model(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning abstract base model."""
        code = """
from django.db import models

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Article(TimestampedModel):
    title = models.CharField(max_length=100)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        # Should find both models
        assert result.summary.total_models >= 1

        # Find Article model
        article = None
        for model in result.results.values():
            if model.name == "Article":
                article = model
                break

        assert article is not None
        # Article should inherit fields from TimestampedModel
        assert "title" in article.fields

    def test_scan_model_with_docstring(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning model with docstring."""
        code = '''
from django.db import models

class Article(models.Model):
    """A blog article."""
    title = models.CharField(max_length=100)
'''
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        model = list(result.results.values())[0]
        assert model.description == "A blog article."

    def test_scan_multiple_models(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning multiple models."""
        code = """
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)

class Article(models.Model):
    title = models.CharField(max_length=100)

class Comment(models.Model):
    text = models.TextField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 3
        model_names = [model.name for model in result.results.values()]
        assert "User" in model_names
        assert "Article" in model_names
        assert "Comment" in model_names

    def test_scan_empty_file(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning empty file."""
        models_file = tmp_path / "models.py"
        models_file.write_text("")

        result = scanner.scan(models_file)

        assert result.summary.total_models == 0
        assert len(result.results) == 0

    def test_scan_file_without_models(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning file without Django models."""
        code = """
class NotAModel:
    pass

def some_function():
    pass
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 0

    def test_scan_directory(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning a directory."""
        # Create multiple model files
        app1 = tmp_path / "app1"
        app1.mkdir()
        (app1 / "models.py").write_text("""
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
""")

        app2 = tmp_path / "app2"
        app2.mkdir()
        (app2 / "models.py").write_text("""
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
""")

        result = scanner.scan(tmp_path)

        assert result.summary.total_models == 2

    def test_file_filtering(self, tmp_path: Path) -> None:
        """Test file pattern filtering."""
        # Create files
        (tmp_path / "models.py").write_text("""
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
""")
        (tmp_path / "views.py").write_text("""
def index():
    pass
""")

        scanner = DjangoModelScanner(include_patterns=["**/models.py"])
        result = scanner.scan(tmp_path)

        # Should only scan models.py
        assert result.summary.total_models == 1

    def test_invalid_syntax(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test handling of invalid Python syntax."""
        code = """
from django.db import models

class Article(models.Model
    # Missing colon and closing paren
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        # Should handle gracefully
        assert result.summary.total_models == 0

    def test_summary_statistics(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test summary statistics are calculated correctly."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)

class User(models.Model):
    username = models.CharField(max_length=50)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 2
        assert result.summary.total_fields >= 3  # At least title, content, username
        assert result.summary.total_relationships >= 1  # author ForeignKey
        assert result.summary.scan_duration_ms >= 0
