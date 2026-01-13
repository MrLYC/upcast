"""Tests for Django model relationships."""

from pathlib import Path

import pytest

from upcast.scanners.django_models import DjangoModelScanner


class TestForeignKey:
    """Test ForeignKey relationship detection."""

    def test_basic_foreign_key(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test basic ForeignKey."""
        code = """
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        article = None
        for model in result.results.values():
            if model.name == "Article":
                article = model
                break

        assert article is not None
        assert len(article.relationships) >= 1
        fk_rel = next((r for r in article.relationships if r.field == "author"), None)
        assert fk_rel is not None
        assert fk_rel.type == "models.ForeignKey"
        assert fk_rel.on_delete == "`models.CASCADE`"

    def test_foreign_key_with_string_reference(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test ForeignKey with string reference."""
        code = """
from django.db import models

class Article(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)

class User(models.Model):
    username = models.CharField(max_length=50)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        article = None
        for model in result.results.values():
            if model.name == "Article":
                article = model
                break

        assert article is not None
        assert len(article.relationships) >= 1

    def test_foreign_key_with_related_name(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test ForeignKey with related_name."""
        code = """
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        article = None
        for model in result.results.values():
            if model.name == "Article":
                article = model
                break

        assert article is not None
        fk_rel = next((r for r in article.relationships if r.field == "author"), None)
        assert fk_rel is not None
        assert fk_rel.related_name == "articles"

    def test_foreign_key_on_delete_options(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test different on_delete options."""
        code = """
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        article = None
        for model in result.results.values():
            if model.name == "Article":
                article = model
                break

        assert article is not None
        fk_rel = next((r for r in article.relationships if r.field == "author"), None)
        assert fk_rel is not None
        assert fk_rel.on_delete == "`models.SET_NULL`"


class TestManyToMany:
    """Test ManyToManyField detection."""

    def test_basic_many_to_many(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test basic ManyToManyField."""
        code = """
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Article(models.Model):
    tags = models.ManyToManyField(Tag)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        article = None
        for model in result.results.values():
            if model.name == "Article":
                article = model
                break

        assert article is not None
        assert len(article.relationships) >= 1
        m2m_rel = next((r for r in article.relationships if r.field == "tags"), None)
        assert m2m_rel is not None
        assert m2m_rel.type == "models.ManyToManyField"

    def test_many_to_many_with_related_name(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test ManyToManyField with related_name."""
        code = """
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Article(models.Model):
    tags = models.ManyToManyField(Tag, related_name='articles')
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        article = None
        for model in result.results.values():
            if model.name == "Article":
                article = model
                break

        assert article is not None
        m2m_rel = next((r for r in article.relationships if r.field == "tags"), None)
        assert m2m_rel is not None
        assert m2m_rel.related_name == "articles"

    def test_self_referencing_many_to_many(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test self-referencing ManyToManyField."""
        code = """
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    friends = models.ManyToManyField('self', blank=True)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        user = None
        for model in result.results.values():
            if model.name == "User":
                user = model
                break

        assert user is not None
        assert len(user.relationships) >= 1


class TestOneToOne:
    """Test OneToOneField detection."""

    def test_basic_one_to_one(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test basic OneToOneField."""
        code = """
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        profile = None
        for model in result.results.values():
            if model.name == "Profile":
                profile = model
                break

        assert profile is not None
        assert len(profile.relationships) >= 1
        o2o_rel = next((r for r in profile.relationships if r.field == "user"), None)
        assert o2o_rel is not None
        assert o2o_rel.type == "models.OneToOneField"

    def test_one_to_one_with_related_name(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test OneToOneField with related_name."""
        code = """
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        profile = None
        for model in result.results.values():
            if model.name == "Profile":
                profile = model
                break

        assert profile is not None
        o2o_rel = next((r for r in profile.relationships if r.field == "user"), None)
        assert o2o_rel is not None
        assert o2o_rel.related_name == "profile"


class TestComplexRelationships:
    """Test complex relationship scenarios."""

    def test_multiple_foreign_keys(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test model with multiple ForeignKeys."""
        code = """
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)

class Category(models.Model):
    name = models.CharField(max_length=50)

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        article = None
        for model in result.results.values():
            if model.name == "Article":
                article = model
                break

        assert article is not None
        assert len(article.relationships) >= 2

    def test_mixed_relationship_types(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test model with different relationship types."""
        code = """
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)

        article = None
        for model in result.results.values():
            if model.name == "Article":
                article = model
                break

        assert article is not None
        assert len(article.relationships) >= 2
        rel_types = [r.type for r in article.relationships]
        assert "models.ForeignKey" in rel_types
        assert "models.ManyToManyField" in rel_types
