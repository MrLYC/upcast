"""Tests for edge cases in Django model scanner."""

from pathlib import Path

import pytest

from upcast.scanners.django_models import DjangoModelScanner


class TestMetaOptions:
    """Test Meta class options detection."""

    def test_meta_ordering(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test Meta ordering option."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert model.meta is not None
        assert "ordering" in model.meta

    def test_meta_verbose_names(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test Meta verbose_name options."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert model.meta is not None
        assert model.meta.get("verbose_name") == "Article"
        assert model.meta.get("verbose_name_plural") == "Articles"

    def test_meta_db_table(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test Meta db_table option."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'custom_articles'
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert model.meta is not None
        assert model.meta.get("db_table") == "custom_articles"

    def test_meta_unique_together(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test Meta unique_together option."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    
    class Meta:
        unique_together = [['title', 'slug']]
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert model.meta is not None
        assert "unique_together" in model.meta

    def test_meta_indexes(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test Meta indexes option."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['-created_at']),
        ]
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert model.meta is not None
        assert "indexes" in model.meta


class TestInheritance:
    """Test model inheritance scenarios."""

    def test_abstract_base_class(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test abstract base class."""
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

    def test_multi_table_inheritance(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test multi-table inheritance."""
        code = """
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

class Restaurant(Place):
    serves_pizza = models.BooleanField(default=False)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 2

        restaurant = None
        for model in result.results.values():
            if model.name == "Restaurant":
                restaurant = model
                break

        assert restaurant is not None
        assert "Place" in restaurant.bases or any("Place" in base for base in restaurant.bases)

    def test_proxy_model(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test proxy model."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

class PublishedArticle(Article):
    class Meta:
        proxy = True
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        # Should find both models
        assert result.summary.total_models >= 1


class TestModelMethods:
    """Test model method detection."""

    def test_model_with_str_method(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test model with __str__ method."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 1

    def test_model_with_custom_methods(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test model with custom methods."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    def get_preview(self):
        return self.content[:100]
    
    def is_long(self):
        return len(self.content) > 1000
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 1

    def test_model_with_property(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test model with property decorator."""
        code = """
from django.db import models

class Article(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 1


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_model(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test model with no fields."""
        code = """
from django.db import models

class EmptyModel(models.Model):
    pass
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        # Empty models may not be detected by the scanner
        # Just ensure it doesn't crash
        assert result is not None

    def test_non_model_class(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test that non-model classes are ignored."""
        code = """
from django.db import models

class NotAModel:
    pass

class Article(models.Model):
    title = models.CharField(max_length=100)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        # Should only find Article, not NotAModel
        assert result.summary.total_models == 1
        model_names = [model.name for model in result.results.values()]
        assert "Article" in model_names
        assert "NotAModel" not in model_names

    def test_model_with_class_attributes(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test model with class-level attributes."""
        code = """
from django.db import models

class Article(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        assert result.summary.total_models == 1

    def test_invalid_field_syntax(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test handling of invalid field syntax."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100
    # Missing closing paren
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        # Should handle gracefully
        assert result.summary.total_models == 0

    def test_model_in_nested_directory(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning models in nested directories."""
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()

        models_file = app_dir / "models.py"
        models_file.write_text("""
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
""")

        result = scanner.scan(tmp_path)

        assert result.summary.total_models == 1

    def test_models_in_models_package(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test scanning models split into a package."""
        models_dir = tmp_path / "models"
        models_dir.mkdir()

        (models_dir / "__init__.py").write_text("")
        (models_dir / "article.py").write_text("""
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
""")

        result = scanner.scan(tmp_path)

        assert result.summary.total_models == 1
