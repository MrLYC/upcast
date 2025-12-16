"""Pylint checker for Django model scanning."""

from typing import Any

from astroid import nodes

from upcast.django_scanner.ast_utils import is_django_model
from upcast.django_scanner.model_parser import merge_abstract_fields, parse_model


class DjangoModelChecker:
    """Checker that scans Django models using Pylint's visitor pattern.

    This checker visits all ClassDef nodes and collects Django model information.
    After visiting all classes, it performs a second pass to merge abstract
    model fields into concrete models.
    """

    name = "django-model-scanner"

    def __init__(self) -> None:
        """Initialize the checker with empty model storage."""
        self.models: dict[str, dict[str, Any]] = {}

    def visit_classdef(self, node: nodes.ClassDef) -> None:
        """Visit a class definition node.

        Args:
            node: The ClassDef node to visit
        """
        # Check if this is a Django model
        if is_django_model(node):
            # Parse the model
            model_data = parse_model(node)

            # Store by qualified name
            qname = node.qname()
            self.models[qname] = model_data

    def close(self) -> None:
        """Perform second-pass processing after all nodes are visited.

        This merges abstract model fields into concrete models.
        """
        # Merge abstract model fields into concrete models
        for _qname, model in self.models.items():
            if not model.get("abstract", False):
                merge_abstract_fields(model, self.models)

    def get_models(self) -> dict[str, dict[str, Any]]:
        """Get all collected models.

        Returns:
            Dictionary of models keyed by qualified name
        """
        return self.models
