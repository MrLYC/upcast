"""Tests for Django model field detection."""

from pathlib import Path

import pytest

from upcast.scanners.django_models import DjangoModelScanner


class TestBasicFields:
    """Test basic field type detection."""

    def test_char_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test CharField detection."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "title" in model.fields
        assert model.fields["title"].type == "models.CharField"
        assert model.fields["title"].parameters.get("max_length") == 100

    def test_text_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test TextField detection."""
        code = """
from django.db import models

class Article(models.Model):
    content = models.TextField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "content" in model.fields
        assert model.fields["content"].type == "models.TextField"

    def test_integer_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test IntegerField detection."""
        code = """
from django.db import models

class Product(models.Model):
    quantity = models.IntegerField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "quantity" in model.fields
        assert model.fields["quantity"].type == "models.IntegerField"

    def test_boolean_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test BooleanField detection."""
        code = """
from django.db import models

class Article(models.Model):
    published = models.BooleanField(default=False)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "published" in model.fields
        assert model.fields["published"].type == "models.BooleanField"

    def test_datetime_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test DateTimeField detection."""
        code = """
from django.db import models

class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "created_at" in model.fields
        assert model.fields["created_at"].type == "models.DateTimeField"

    def test_email_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test EmailField detection."""
        code = """
from django.db import models

class User(models.Model):
    email = models.EmailField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "email" in model.fields
        assert model.fields["email"].type == "models.EmailField"


class TestFieldParameters:
    """Test field parameter extraction."""

    def test_field_with_null(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test field with null parameter."""
        code = """
from django.db import models

class Article(models.Model):
    subtitle = models.CharField(max_length=200, null=True)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "subtitle" in model.fields
        assert model.fields["subtitle"].parameters.get("null") is True

    def test_field_with_blank(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test field with blank parameter."""
        code = """
from django.db import models

class Article(models.Model):
    subtitle = models.CharField(max_length=200, blank=True)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "subtitle" in model.fields
        assert model.fields["subtitle"].parameters.get("blank") is True

    def test_field_with_default(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test field with default value."""
        code = """
from django.db import models

class Article(models.Model):
    status = models.CharField(max_length=20, default='draft')
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "status" in model.fields
        assert "default" in model.fields["status"].parameters

    def test_field_with_choices(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test field with choices."""
        code = """
from django.db import models

class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "status" in model.fields

    def test_field_with_help_text(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test field with help_text."""
        code = """
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100, help_text='Enter article title')
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "title" in model.fields
        assert model.fields["title"].help_text == "Enter article title"

    def test_field_with_verbose_name(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test field with verbose_name."""
        code = """
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='First Name')
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "first_name" in model.fields
        assert model.fields["first_name"].verbose_name == "First Name"


class TestNumericFields:
    """Test numeric field types."""

    def test_decimal_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test DecimalField detection."""
        code = """
from django.db import models

class Product(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "price" in model.fields
        assert model.fields["price"].type == "models.DecimalField"

    def test_float_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test FloatField detection."""
        code = """
from django.db import models

class Measurement(models.Model):
    value = models.FloatField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "value" in model.fields
        assert model.fields["value"].type == "models.FloatField"

    def test_positive_integer_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test PositiveIntegerField detection."""
        code = """
from django.db import models

class Product(models.Model):
    quantity = models.PositiveIntegerField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "quantity" in model.fields
        assert model.fields["quantity"].type == "models.PositiveIntegerField"


class TestSpecialFields:
    """Test special field types."""

    def test_json_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test JSONField detection."""
        code = """
from django.db import models

class Config(models.Model):
    data = models.JSONField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "data" in model.fields
        assert model.fields["data"].type == "models.JSONField"

    def test_uuid_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test UUIDField detection."""
        code = """
from django.db import models
import uuid

class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "id" in model.fields
        assert model.fields["id"].type == "models.UUIDField"

    def test_slug_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test SlugField detection."""
        code = """
from django.db import models

class Article(models.Model):
    slug = models.SlugField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "slug" in model.fields
        assert model.fields["slug"].type == "models.SlugField"

    def test_url_field(self, tmp_path: Path, scanner: DjangoModelScanner) -> None:
        """Test URLField detection."""
        code = """
from django.db import models

class Article(models.Model):
    website = models.URLField()
"""
        models_file = tmp_path / "models.py"
        models_file.write_text(code)

        result = scanner.scan(models_file)
        model = list(result.results.values())[0]

        assert "website" in model.fields
        assert model.fields["website"].type == "models.URLField"
