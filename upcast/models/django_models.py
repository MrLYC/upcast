"""Data models for Django model scanner."""

from typing import Any

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class DjangoField(BaseModel):
    """A field in a Django model.

    Attributes:
        name: Field name
        type: Field type (e.g., CharField, ForeignKey)
        parameters: Field parameters (max_length, null, blank, etc.)
        line: Line number where field is defined
    """

    name: str = Field(description="Field name")
    type: str = Field(description="Field type (e.g., CharField, ForeignKey)")
    parameters: dict[str, Any] = Field(description="Field parameters")
    line: int = Field(ge=1, description="Line number")


class DjangoRelationship(BaseModel):
    """A relationship field in a Django model.

    Attributes:
        type: Relationship type (ForeignKey, ManyToManyField, OneToOneField)
        to: Target model
        field: Field name
        related_name: Related name for reverse relations
        on_delete: on_delete strategy for ForeignKey/OneToOne
    """

    type: str = Field(description="Relationship type (ForeignKey, ManyToMany, etc)")
    to: str = Field(description="Target model")
    field: str = Field(description="Field name")
    related_name: str | None = Field(None, description="Related name")
    on_delete: str | None = Field(None, description="on_delete strategy")


class DjangoModel(BaseModel):
    """A Django model definition.

    Attributes:
        name: Model class name
        module: Module path
        bases: Base classes
        fields: Model fields keyed by name
        relationships: Relationship fields
        meta: Meta class options
        description: First line of model docstring
        line: Line number where model is defined
    """

    name: str = Field(description="Model class name")
    module: str = Field(description="Module path")
    bases: list[str] = Field(description="Base classes")
    fields: dict[str, DjangoField] = Field(description="Model fields")
    relationships: list[DjangoRelationship] = Field(description="Relationship fields")
    meta: dict[str, Any] | None = Field(None, description="Meta class options")
    description: str | None = Field(None, description="First line of model docstring")
    line: int = Field(ge=1, description="Line number")


class DjangoModelSummary(ScannerSummary):
    """Summary statistics for Django models.

    Attributes:
        total_models: Number of models found
        total_fields: Total number of fields across all models
        total_relationships: Total number of relationships
    """

    total_models: int = Field(ge=0, description="Number of models")
    total_fields: int = Field(ge=0, description="Total fields")
    total_relationships: int = Field(ge=0, description="Total relationships")


class DjangoModelOutput(ScannerOutput[dict[str, DjangoModel]]):
    """Complete output from Django model scanner.

    Attributes:
        summary: Summary statistics
        results: Models keyed by qualified name (app.models.ModelName)
    """

    summary: DjangoModelSummary
    results: dict[str, DjangoModel] = Field(description="Models keyed by model name")
