"""AST utilities for Django model detection."""

from typing import Any

from astroid import nodes


def is_django_model(class_node: nodes.ClassDef) -> bool:
    """Check if a class is a Django model through type inference.

    Args:
        class_node: The class definition node to check

    Returns:
        True if the class inherits from django.db.models.Model
    """
    try:
        # Check all ancestors (including indirect inheritance)
        for ancestor in class_node.ancestors():
            if ancestor.qname() == "django.db.models.base.Model":
                return True
    except Exception:  # noqa: S110
        pass

    # Fallback: check direct bases with pattern matching
    return _check_direct_bases_for_django(class_node)


def _check_base_is_django_model(base: nodes.ClassDef) -> bool:
    """Check if a base class is django.db.models.Model.

    Args:
        base: The base class node to check

    Returns:
        True if the base is django.db.models.Model
    """
    try:
        return base.qname() == "django.db.models.base.Model"
    except (AttributeError, Exception):
        return False


def _check_direct_bases_for_django(class_node: nodes.ClassDef) -> bool:
    """Fallback: check direct base classes for Django model patterns.

    Args:
        class_node: The class definition node to check

    Returns:
        True if any direct base matches Django model pattern
    """
    try:
        for base in class_node.bases:
            base_str = base.as_string()
            # Check common patterns: models.Model, Model, etc.
            if any(pattern in base_str for pattern in ["models.Model", "Model", "db.models.Model"]):
                # Check if Django is imported in this module
                if _check_django_imports(class_node):
                    return True

                # Try to infer the base
                try:
                    inferred_list = list(base.infer())
                    for inferred in inferred_list:
                        # Check if it's Uninferable
                        if inferred.__class__.__name__ in ("Uninferable", "UninferableBase"):
                            # Django not installed, but pattern matches - likely a Django model
                            return True
                        # Check if it has qname attribute (ClassDef, Module, etc.)
                        elif hasattr(inferred, "qname"):
                            qname = inferred.qname()  # type: ignore[attr-defined]
                            if "django.db.models" in qname:
                                return True
                except Exception:  # noqa: S110
                    # If inference fails but pattern matches and Django is imported, assume it's a model
                    pass
    except Exception:  # noqa: S110
        pass
    return False


def _check_django_imports(class_node: nodes.ClassDef) -> bool:
    """Check if the module imports Django models.

    Args:
        class_node: The class node to check

    Returns:
        True if Django models are imported
    """
    try:
        root = class_node.root()
        for node in root.body:
            if isinstance(node, nodes.ImportFrom):
                if node.modname and "django.db.models" in node.modname:
                    return True
            elif isinstance(node, nodes.Import):
                for name, _ in node.names:
                    if "django" in name:
                        return True
    except Exception:  # noqa: S110
        pass
    return False


def is_abstract_model(class_node: nodes.ClassDef) -> bool:
    """Check if a Django model is abstract (Meta.abstract = True).

    Args:
        class_node: The class definition node to check

    Returns:
        True if the model has Meta.abstract = True
    """
    for item in class_node.body:
        if isinstance(item, nodes.ClassDef) and item.name == "Meta":
            # Look for abstract = True assignment
            for meta_item in item.body:
                if isinstance(meta_item, nodes.Assign):
                    for target in meta_item.targets:
                        if (
                            isinstance(target, nodes.AssignName)
                            and target.name == "abstract"
                            and isinstance(meta_item.value, nodes.Const)
                        ):
                            return bool(meta_item.value.value)
    return False


def is_concrete_model(class_node: nodes.ClassDef) -> bool:
    """Check if a Django model is concrete (not abstract).

    Args:
        class_node: The class definition node to check

    Returns:
        True if the model is a Django model and not abstract
    """
    return is_django_model(class_node) and not is_abstract_model(class_node)


def is_django_field(node: nodes.Assign) -> bool:
    """Check if an assignment is a Django model field.

    Args:
        node: The assignment node to check

    Returns:
        True if the assignment creates a Django field
    """
    if not isinstance(node.value, nodes.Call):
        return False

    # Try type inference first
    try:
        inferred_list = list(node.value.func.infer())
        for inferred in inferred_list:
            if hasattr(inferred, "qname"):
                qname = inferred.qname()  # type: ignore[attr-defined]
                # Check if it's from django.db.models.fields
                if "django.db.models.fields" in qname:
                    return True
    except Exception:  # noqa: S110
        pass

    # Fallback: pattern matching for field names
    try:
        func_str = node.value.func.as_string()
        if "Field" in func_str and _is_field_pattern(func_str):
            return True
    except Exception:  # noqa: S110
        pass

    return False


def _is_field_pattern(func_str: str) -> bool:
    """Check if a function string matches Django field patterns.

    Args:
        func_str: The function string (e.g., "models.CharField")

    Returns:
        True if it matches Django field patterns
    """
    field_patterns = [
        "models.",
        "fields.",
    ]
    return any(pattern in func_str for pattern in field_patterns) and "Field" in func_str


def safe_as_string(node: nodes.NodeNG) -> str:
    """Safely convert an astroid node to string representation.

    Args:
        node: Astroid node to convert

    Returns:
        String representation, or empty string on failure
    """
    try:
        return node.as_string()
    except Exception:
        return ""


def infer_literal_value(node: nodes.NodeNG) -> Any:  # noqa: C901
    """Safely infer a literal value from an AST node using astroid inference.

    Args:
        node: Astroid node to infer

    Returns:
        Inferred Python literal value, or string representation as fallback
    """
    try:
        # Try to infer the value
        inferred_list = list(node.infer())

        # Skip if inference failed or returned multiple values
        if not inferred_list or len(inferred_list) != 1:
            return safe_as_string(node)

        inferred_value = inferred_list[0]

        # Handle Uninferable nodes
        if inferred_value.__class__.__name__ in ("Uninferable", "UninferableBase"):
            return safe_as_string(node)

        # Handle Const nodes (strings, numbers, booleans, None)
        if isinstance(inferred_value, nodes.Const):
            return inferred_value.value

        # Handle List nodes recursively
        if isinstance(inferred_value, nodes.List):
            result = []
            for elem in inferred_value.elts:
                if isinstance(elem, nodes.NodeNG):
                    result.append(infer_literal_value(elem))
                else:
                    result.append(safe_as_string(node))
            return result

        # Handle Tuple nodes recursively
        if isinstance(inferred_value, nodes.Tuple):
            result = []
            for elem in inferred_value.elts:
                if isinstance(elem, nodes.NodeNG):
                    result.append(infer_literal_value(elem))
                else:
                    result.append(safe_as_string(node))
            return result

        # Handle Dict nodes recursively
        if isinstance(inferred_value, nodes.Dict):
            result = {}
            for key_node, value_node in zip(inferred_value.keys, inferred_value.values):
                if isinstance(key_node, nodes.NodeNG) and isinstance(value_node, nodes.NodeNG):
                    key = infer_literal_value(key_node)
                    value = infer_literal_value(value_node)
                    # Only add if key is hashable
                    if isinstance(key, (str, int, float, bool, type(None))):
                        result[key] = value
            return result

        # For other types, fall back to string
        return safe_as_string(node)

    except Exception:
        # On any error, fall back to string representation
        return safe_as_string(node)
