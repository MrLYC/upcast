"""Tests for Django model Pydantic models."""

from pathlib import Path

import pytest

from upcast.models.django_models import (
    DjangoField,
    DjangoModel,
    DjangoModelOutput,
    DjangoModelSummary,
    DjangoRelationship,
)


class TestDjangoField:
    """Test DjangoField model."""

    def test_basic_field(self) -> None:
        """Test creating a basic field."""
        field = DjangoField(
            name="title",
            type="CharField",
            parameters={"max_length": 100},
            line=5,
        )
        assert field.name == "title"
        assert field.type == "CharField"
        assert field.parameters["max_length"] == 100
        assert field.line == 5
        assert field.help_text is None
        assert field.verbose_name is None

    def test_field_with_help_text(self) -> None:
        """Test field with help text."""
        field = DjangoField(
            name="email",
            type="EmailField",
            help_text="User's email address",
            parameters={},
            line=10,
        )
        assert field.help_text == "User's email address"

    def test_field_with_verbose_name(self) -> None:
        """Test field with verbose name."""
        field = DjangoField(
            name="first_name",
            type="CharField",
            verbose_name="First Name",
            parameters={"max_length": 50},
            line=12,
        )
        assert field.verbose_name == "First Name"

    def test_field_line_validation(self) -> None:
        """Test that line number must be >= 1."""
        with pytest.raises(ValueError):
            DjangoField(
                name="field",
                type="CharField",
                parameters={},
                line=0,
            )


class TestDjangoRelationship:
    """Test DjangoRelationship model."""

    def test_foreign_key(self) -> None:
        """Test ForeignKey relationship."""
        rel = DjangoRelationship(
            type="ForeignKey",
            to="User",
            field="author",
            related_name="posts",
            on_delete="CASCADE",
        )
        assert rel.type == "ForeignKey"
        assert rel.to == "User"
        assert rel.field == "author"
        assert rel.related_name == "posts"
        assert rel.on_delete == "CASCADE"

    def test_many_to_many(self) -> None:
        """Test ManyToMany relationship."""
        rel = DjangoRelationship(
            type="ManyToManyField",
            to="Tag",
            field="tags",
            related_name="articles",
        )
        assert rel.type == "ManyToManyField"
        assert rel.to == "Tag"
        assert rel.field == "tags"
        assert rel.on_delete is None

    def test_one_to_one(self) -> None:
        """Test OneToOne relationship."""
        rel = DjangoRelationship(
            type="OneToOneField",
            to="Profile",
            field="profile",
            on_delete="CASCADE",
        )
        assert rel.type == "OneToOneField"
        assert rel.to == "Profile"


class TestDjangoModel:
    """Test DjangoModel model."""

    def test_basic_model(self) -> None:
        """Test creating a basic model."""
        model = DjangoModel(
            name="Article",
            module="blog.models",
            bases=["models.Model"],
            fields={},
            relationships=[],
            line=10,
        )
        assert model.name == "Article"
        assert model.module == "blog.models"
        assert model.bases == ["models.Model"]
        assert len(model.fields) == 0
        assert len(model.relationships) == 0

    def test_model_with_fields(self) -> None:
        """Test model with fields."""
        field = DjangoField(
            name="title",
            type="CharField",
            parameters={"max_length": 100},
            line=12,
        )
        model = DjangoModel(
            name="Article",
            module="blog.models",
            bases=["models.Model"],
            fields={"title": field},
            relationships=[],
            line=10,
        )
        assert len(model.fields) == 1
        assert "title" in model.fields
        assert model.fields["title"].type == "CharField"

    def test_model_with_relationships(self) -> None:
        """Test model with relationships."""
        rel = DjangoRelationship(
            type="ForeignKey",
            to="User",
            field="author",
            related_name="articles",
            on_delete="CASCADE",
        )
        model = DjangoModel(
            name="Article",
            module="blog.models",
            bases=["models.Model"],
            fields={},
            relationships=[rel],
            line=10,
        )
        assert len(model.relationships) == 1
        assert model.relationships[0].type == "ForeignKey"

    def test_model_with_meta(self) -> None:
        """Test model with Meta options."""
        model = DjangoModel(
            name="Article",
            module="blog.models",
            bases=["models.Model"],
            fields={},
            relationships=[],
            meta={"ordering": ["-created_at"], "verbose_name": "Article"},
            line=10,
        )
        assert model.meta is not None
        assert model.meta["ordering"] == ["-created_at"]
        assert model.meta["verbose_name"] == "Article"

    def test_model_with_description(self) -> None:
        """Test model with description."""
        model = DjangoModel(
            name="Article",
            module="blog.models",
            bases=["models.Model"],
            fields={},
            relationships=[],
            description="A blog article.",
            line=10,
        )
        assert model.description == "A blog article."


class TestDjangoModelSummary:
    """Test DjangoModelSummary model."""

    def test_summary(self) -> None:
        """Test creating a summary."""
        summary = DjangoModelSummary(
            total_count=5,
            files_scanned=3,
            scan_duration_ms=150,
            total_models=5,
            total_fields=20,
            total_relationships=8,
        )
        assert summary.total_count == 5
        assert summary.total_models == 5
        assert summary.total_fields == 20
        assert summary.total_relationships == 8

    def test_summary_validation(self) -> None:
        """Test that negative values are rejected."""
        with pytest.raises(ValueError):
            DjangoModelSummary(
                total_count=-1,
                files_scanned=0,
                scan_duration_ms=0,
                total_models=0,
                total_fields=0,
                total_relationships=0,
            )


class TestDjangoModelOutput:
    """Test DjangoModelOutput model."""

    def test_output_structure(self) -> None:
        """Test output structure."""
        model = DjangoModel(
            name="Article",
            module="blog.models",
            bases=["models.Model"],
            fields={},
            relationships=[],
            line=10,
        )
        summary = DjangoModelSummary(
            total_count=1,
            files_scanned=1,
            scan_duration_ms=100,
            total_models=1,
            total_fields=0,
            total_relationships=0,
        )
        output = DjangoModelOutput(
            summary=summary,
            results={"blog.models.Article": model},
        )
        assert len(output.results) == 1
        assert "blog.models.Article" in output.results
        assert output.summary.total_models == 1

    def test_output_serialization(self) -> None:
        """Test that output can be serialized."""
        model = DjangoModel(
            name="Article",
            module="blog.models",
            bases=["models.Model"],
            fields={},
            relationships=[],
            line=10,
        )
        summary = DjangoModelSummary(
            total_count=1,
            files_scanned=1,
            scan_duration_ms=100,
            total_models=1,
            total_fields=0,
            total_relationships=0,
        )
        output = DjangoModelOutput(
            summary=summary,
            results={"blog.models.Article": model},
        )
        data = output.model_dump()
        assert "summary" in data
        assert "results" in data
        assert "blog.models.Article" in data["results"]
