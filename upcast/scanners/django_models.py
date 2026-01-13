"""Django model scanner.

This scanner analyzes Django model definitions to extract model classes,
fields, relationships, and Meta options.
"""

import logging
import time
from pathlib import Path
from typing import Any

from astroid import nodes

from upcast.common.code_utils import extract_description
from upcast.common.django.model_parser import merge_abstract_fields, parse_model
from upcast.common.django.model_utils import is_django_model
from upcast.common.scanner_base import BaseScanner
from upcast.models.django_models import (
    DjangoField,
    DjangoModel,
    DjangoModelOutput,
    DjangoModelSummary,
    DjangoRelationship,
)

logger = logging.getLogger(__name__)


class DjangoModelScanner(BaseScanner[DjangoModelOutput]):
    """Scanner for Django model definitions."""

    def __init__(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ):
        """Initialize Django model scanner.

        Args:
            include_patterns: File patterns to include (default: models.py files)
            exclude_patterns: File patterns to exclude
            verbose: Enable verbose logging
        """
        # Default to scanning models.py files
        default_includes = ["**/models.py", "models.py", "**/models/*.py"]
        include_patterns = include_patterns or default_includes

        super().__init__(
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            verbose=verbose,
        )

        # Root path for module calculation (set during scan)
        self.root_path: Path | None = None

    def scan(self, path: Path) -> DjangoModelOutput:
        """Scan path for Django models.

        Args:
            path: Directory or file to scan

        Returns:
            DjangoModelOutput with all detected models
        """
        start_time = time.perf_counter()

        # Store root path for module calculation
        self.root_path = path if path.is_dir() else path.parent

        files = self.get_files_to_scan(path)

        # First pass: collect all models
        raw_models: dict[str, dict[str, Any]] = {}
        for file_path in files:
            file_models = self._scan_file(file_path)
            raw_models.update(file_models)

        # Second pass: merge abstract fields
        for _qname, model_data in raw_models.items():
            if not model_data.get("meta", {}).get("abstract", False):
                merge_abstract_fields(model_data, raw_models)

        # Convert to Pydantic models
        models: dict[str, DjangoModel] = {}
        for qname, model_data in raw_models.items():
            django_model = self._convert_to_pydantic(model_data)
            if django_model:
                models[qname] = django_model

        scan_duration_ms = int((time.perf_counter() - start_time) * 1000)
        summary = self._calculate_summary(models, scan_duration_ms)

        return DjangoModelOutput(summary=summary, results=models, metadata={"scanner_name": "django-models"})

    def _scan_file(self, file_path: Path) -> dict[str, dict[str, Any]]:
        """Scan a single file for Django models.

        Args:
            file_path: Path to the Python file

        Returns:
            Dictionary of models keyed by qualified name
        """
        module = self.parse_file(file_path)
        if not module:
            return {}

        models: dict[str, dict[str, Any]] = {}

        # Visit all class definitions
        for class_node in module.nodes_of_class(nodes.ClassDef):
            if not is_django_model(class_node):
                continue

            # Parse the model with file context for module path calculation
            model_data = parse_model(
                class_node,
                root_path=self.root_path,
                file_path=file_path,
            )
            if model_data:
                # Extract description from docstring
                description = extract_description(class_node)
                model_data["description"] = description

                qname = model_data["qname"]  # Use qname from parsed data
                models[qname] = model_data

        if self.verbose and models:
            logger.info(f"Found {len(models)} models in {file_path}")

        return models

    def _convert_to_pydantic(self, model_data: dict[str, Any]) -> DjangoModel | None:
        """Convert raw model data to Pydantic model.

        Args:
            model_data: Raw model dictionary from parser

        Returns:
            DjangoModel instance or None if conversion fails
        """
        try:
            # Convert fields
            fields: dict[str, DjangoField] = {}
            for field_name, field_info in model_data.get("fields", {}).items():
                # Get line number from field_info or default to model line
                line = field_info.get("line", model_data.get("line", 1))

                # Extract metadata fields
                help_text = field_info.get("help_text")
                verbose_name = field_info.get("verbose_name")

                # Extract parameters, excluding fields that are already DjangoField attributes
                parameters = {
                    k: v
                    for k, v in field_info.items()
                    if k not in ("type", "name", "line", "help_text", "verbose_name")
                }

                fields[field_name] = DjangoField(
                    name=field_name,
                    type=field_info.get("type", "Unknown"),
                    help_text=help_text,
                    verbose_name=verbose_name,
                    parameters=parameters,
                    line=line,
                )

            # Convert relationships
            relationships: list[DjangoRelationship] = []
            for rel_name, rel_info in model_data.get("relationships", {}).items():
                relationships.append(
                    DjangoRelationship(
                        type=rel_info.get("type", "Unknown"),
                        to=str(rel_info.get("to", "")),
                        field=rel_name,
                        related_name=rel_info.get("related_name"),
                        on_delete=rel_info.get("on_delete"),
                    )
                )

            # Get line number
            line = 1
            if "line" in model_data:
                line = model_data["line"]
            elif "lineno" in model_data:
                line = model_data["lineno"]

            return DjangoModel(
                name=model_data.get("name", ""),
                module=model_data.get("module", ""),
                bases=model_data.get("bases", []),
                fields=fields,
                relationships=relationships,
                meta=model_data.get("meta"),
                description=model_data.get("description"),
                line=line,
            )
        except Exception as e:
            if self.verbose:
                logger.warning(f"Failed to convert model {model_data.get('name')}: {e}")
            return None

    def _calculate_summary(
        self,
        models: dict[str, DjangoModel],
        scan_duration_ms: int,
    ) -> DjangoModelSummary:
        """Calculate summary statistics.

        Args:
            models: Models dictionary
            scan_duration_ms: Time taken to scan in milliseconds

        Returns:
            Summary statistics
        """
        total_models = len(models)
        total_fields = sum(len(model.fields) for model in models.values())
        total_relationships = sum(len(model.relationships) for model in models.values())

        return DjangoModelSummary(
            total_count=total_models,
            files_scanned=total_models,  # Approximation
            scan_duration_ms=scan_duration_ms,
            total_models=total_models,
            total_fields=total_fields,
            total_relationships=total_relationships,
        )
