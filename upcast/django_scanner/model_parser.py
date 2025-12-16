"""Django model field and metadata parser."""

from typing import Any, Optional

from astroid import nodes

from upcast.django_scanner.ast_utils import infer_literal_value, is_django_field, safe_as_string


def parse_model(class_node: nodes.ClassDef) -> dict[str, Any]:
    """Parse a Django model class and extract all information.

    Args:
        class_node: The model class definition node

    Returns:
        Dictionary containing model information with keys:
        - name: Model class name
        - qname: Fully qualified name
        - module: Module path
        - bases: List of base class qualified names
        - abstract: Whether the model is abstract
        - fields: Dictionary of field definitions
        - relationships: Dictionary of relationship field definitions
        - meta: Dictionary of Meta class options
    """
    result: dict[str, Any] = {
        "name": class_node.name,
        "qname": class_node.qname(),
        "module": class_node.root().name,
        "bases": [],
        "abstract": False,
        "fields": {},
        "relationships": {},
        "meta": {},
    }

    # Extract base classes
    for base in class_node.bases:
        base_str = safe_as_string(base)  # type: ignore[arg-type]  # base is NodeNG
        try:
            inferred_list = list(base.infer())
            for inferred in inferred_list:
                if hasattr(inferred, "qname"):
                    result["bases"].append(inferred.qname())  # type: ignore[attr-defined]
                    break
            else:
                # No qname found, use string representation
                result["bases"].append(base_str)
        except Exception:
            result["bases"].append(base_str)

    # Parse Meta class
    result["meta"] = parse_meta_class(class_node)
    result["abstract"] = result["meta"].get("abstract", False)

    # Parse fields
    for item in class_node.body:
        if isinstance(item, nodes.Assign) and is_django_field(item):
            field_info = parse_field(item)
            if field_info:
                field_name, field_type, field_options = field_info

                # Check if it's a relationship field
                if _is_relationship_field(field_type):
                    result["relationships"][field_name] = {
                        "type": field_type,
                        **field_options,
                    }
                else:
                    result["fields"][field_name] = {
                        "type": field_type,
                        **field_options,
                    }

    return result


def parse_field(assign_node: nodes.Assign) -> Optional[tuple[str, str, dict[str, Any]]]:
    """Parse a Django field assignment.

    Args:
        assign_node: The field assignment node

    Returns:
        Tuple of (field_name, field_type, options) or None if parsing fails
    """
    try:
        # Get field name from assignment target
        if not assign_node.targets:
            return None

        target = assign_node.targets[0]
        if isinstance(target, nodes.AssignName):
            field_name = target.name
        else:
            return None

        # Get field type and options from the call
        if not isinstance(assign_node.value, nodes.Call):
            return None

        call = assign_node.value

        # Extract field type
        field_type = _extract_field_type(call)
        if not field_type:
            return None

        # Extract field options
        options = _extract_field_options(call)
    except Exception:
        return None
    else:
        return field_name, field_type, options


def _extract_field_type(call: nodes.Call) -> Optional[str]:
    """Extract the field type from a field call node.

    Args:
        call: The Call node representing the field instantiation

    Returns:
        Field type string (e.g., "CharField") or None
    """
    try:
        if isinstance(call.func, nodes.Attribute):
            # Pattern: models.CharField
            return call.func.attrname
        elif isinstance(call.func, nodes.Name):
            # Pattern: CharField (direct import)
            return call.func.name
    except Exception:  # noqa: S110
        pass
    return None


def _extract_field_options(call: nodes.Call) -> dict[str, Any]:
    """Extract field options from keyword arguments.

    Args:
        call: The Call node representing the field instantiation

    Returns:
        Dictionary of field options
    """
    options: dict[str, Any] = {}

    # Parse positional arguments (e.g., ForeignKey('Model', ...))
    if call.args:
        # First positional arg is usually 'to' for relationship fields
        func_name = _extract_field_type(call)
        if func_name and _is_relationship_field(func_name):
            options["to"] = infer_literal_value(call.args[0])

    # Parse keyword arguments
    for keyword in call.keywords:
        if keyword.arg:
            options[keyword.arg] = infer_literal_value(keyword.value)

    return options


def _is_relationship_field(field_type: str) -> bool:
    """Check if a field type is a relationship field.

    Args:
        field_type: The field type string

    Returns:
        True if it's a relationship field
    """
    return field_type in {"ForeignKey", "OneToOneField", "ManyToManyField"}


def parse_meta_class(class_node: nodes.ClassDef) -> dict[str, Any]:
    """Parse the Meta class of a Django model.

    Args:
        class_node: The model class definition node

    Returns:
        Dictionary of Meta class options
    """
    meta_options: dict[str, Any] = {}

    for item in class_node.body:
        if isinstance(item, nodes.ClassDef) and item.name == "Meta":
            # Parse all assignments in Meta class
            for meta_item in item.body:
                if isinstance(meta_item, nodes.Assign):
                    for target in meta_item.targets:
                        if isinstance(target, nodes.AssignName):
                            option_name = target.name
                            option_value = get_meta_option(meta_item)
                            if option_value is not None:
                                meta_options[option_name] = option_value

    return meta_options


def get_meta_option(assign_node: nodes.Assign) -> Any:
    """Extract the value of a Meta class option.

    Args:
        assign_node: The assignment node in Meta class

    Returns:
        The option value (literal or string representation)
    """
    try:
        return infer_literal_value(assign_node.value)
    except Exception:
        return None


def merge_abstract_fields(model: dict[str, Any], all_models: dict[str, dict[str, Any]]) -> None:  # noqa: C901
    """Merge fields from abstract base models into a concrete model.

    This function modifies the model dictionary in-place, adding fields
    and relationships from abstract parent models.

    Args:
        model: The model dictionary to update
        all_models: Dictionary of all parsed models (keyed by qname)
    """
    # Track processed bases to avoid infinite recursion
    processed: set[str] = set()

    def _merge_from_base(base_qname: str) -> None:  # noqa: C901
        """Recursively merge fields from an abstract base."""
        if base_qname in processed:
            return
        processed.add(base_qname)

        base_model = all_models.get(base_qname)
        if not base_model:
            return

        # Only merge from abstract models
        if not base_model.get("abstract", False):
            return

        # Recursively merge grandparent fields first
        for grandparent_qname in base_model.get("bases", []):
            _merge_from_base(grandparent_qname)

        # Merge fields (don't override existing fields)
        for field_name, field_info in base_model.get("fields", {}).items():
            if field_name not in model["fields"]:
                model["fields"][field_name] = field_info.copy()

        # Merge relationships
        for rel_name, rel_info in base_model.get("relationships", {}).items():
            if rel_name not in model["relationships"]:
                model["relationships"][rel_name] = rel_info.copy()

        # Merge Meta options (model's own Meta takes precedence)
        for meta_key, meta_value in base_model.get("meta", {}).items():
            if meta_key not in model["meta"]:
                model["meta"][meta_key] = meta_value

    # Merge from all base classes
    for base_qname in model.get("bases", []):
        _merge_from_base(base_qname)


def normalize_relation(relation_str: str) -> str:
    """Normalize a relation string to a consistent format.

    Args:
        relation_str: Raw relation string (e.g., "'app.Model'", "Model", etc.)

    Returns:
        Normalized relation string
    """
    # Remove quotes if present
    relation_str = relation_str.strip("'\"")
    return relation_str
