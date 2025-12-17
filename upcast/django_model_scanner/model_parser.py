"""Django model field and metadata parser."""

import inspect
from typing import Any, Optional

from astroid import nodes

from upcast.common.ast_utils import (
    get_qualified_name as common_get_qualified_name,
)
from upcast.common.ast_utils import (
    infer_value_with_fallback,
)
from upcast.django_model_scanner.ast_utils import is_django_field, safe_as_string


# Local inference for backward compatibility
def infer_literal_value(node: nodes.NodeNG) -> Any:
    """Extract literal value from node using common utilities.

    Args:
        node: AST node to infer

    Returns:
        Inferred value (with backticks if inference failed)
    """
    value, _ = infer_value_with_fallback(node)
    return value


def parse_model(class_node: nodes.ClassDef, root_path: Optional[str] = None) -> dict[str, Any] | None:
    """Parse a Django model class and extract all information.

    Args:
        class_node: The model class definition node
        root_path: Unused, kept for backward compatibility

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
    # Extract module path from qname
    # qname format: "module.path.ClassName"
    qname = class_node.qname()
    qname_parts = qname.split(".")

    # Module is everything except the last part (class name)
    module_path = ".".join(qname_parts[:-1]) if len(qname_parts) > 1 else ""

    result: dict[str, Any] = {
        "name": class_node.name,
        "qname": qname,
        "module": module_path,
        "bases": [],
        "fields": {},
        "relationships": {},
        "meta": {},
    }

    # Extract docstring as description if available
    if class_node.doc_node and class_node.doc_node.value:
        # Use inspect.cleandoc to remove leading/trailing whitespace and normalize indentation
        result["description"] = inspect.cleandoc(class_node.doc_node.value)

    # Extract base classes
    for base in class_node.bases:
        base_qname = _extract_base_qname(base, class_node)
        if base_qname:
            result["bases"].append(base_qname)

    # Parse Meta class
    result["meta"] = parse_meta_class(class_node)

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

    # Keep the model if:
    # 1. It has fields or relationships, OR
    # 2. It's abstract (fields will be inherited by children), OR
    # 3. It's a proxy model (modifies behavior without new fields)
    is_abstract = result["meta"].get("abstract", False)
    is_proxy = result["meta"].get("proxy", False)
    has_content = bool(result["fields"] or result["relationships"])

    if has_content or is_abstract or is_proxy:
        return result

    # Skip only empty non-abstract/non-proxy models
    return None


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


def _infer_qname_from_node(node: nodes.NodeNG) -> Optional[str]:
    """Try to infer the qualified name from a node.

    Args:
        node: The node to infer from

    Returns:
        Qualified name or None if inference fails
    """
    try:
        inferred_list = list(node.infer())
        for inferred in inferred_list:
            # Use common get_qualified_name for consistency
            qname, success = common_get_qualified_name(inferred)
            if success and qname and "." in qname and not qname.startswith("builtins."):
                return qname
    except Exception:  # noqa: S110
        pass
    return None


def _extract_field_type_from_attribute(call_func: nodes.Attribute) -> Optional[str]:
    """Extract field type from an Attribute node (e.g., models.CharField).

    Args:
        call_func: The Attribute node

    Returns:
        Field type string or None
    """
    attr_name = call_func.attrname

    # Try to infer the full qualified name
    qname = _infer_qname_from_node(call_func)
    if qname:
        return qname

    # Fallback: construct from expr.name + attr_name
    if hasattr(call_func, "expr") and isinstance(call_func.expr, nodes.Name):
        return f"{call_func.expr.name}.{attr_name}"

    # Final fallback to short name
    return attr_name


def _extract_field_type_from_name(call_func: nodes.Name) -> Optional[str]:
    """Extract field type from a Name node (e.g., CharField).

    Args:
        call_func: The Name node

    Returns:
        Field type string or None
    """
    field_name = call_func.name

    # Try to infer the full qualified name
    qname = _infer_qname_from_node(call_func)
    if qname:
        return qname

    # Fallback to short name
    return field_name


def _extract_field_type(call: nodes.Call) -> Optional[str]:
    """Extract the field type from a field call node.

    Args:
        call: The Call node representing the field instantiation

    Returns:
        Field type string with full module path (e.g., "django.db.models.CharField") or None
    """
    try:
        if isinstance(call.func, nodes.Attribute):
            return _extract_field_type_from_attribute(call.func)
        elif isinstance(call.func, nodes.Name):
            return _extract_field_type_from_name(call.func)
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
    # Check both short names and full paths
    relationship_types = {"ForeignKey", "OneToOneField", "ManyToManyField"}
    # Check if field_type ends with one of the relationship types
    return field_type in relationship_types or any(field_type.endswith(rt) for rt in relationship_types)


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


def _parse_constraint_list(list_node: nodes.List) -> list[dict[str, Any]]:
    """Parse constraints from a list node.

    Args:
        list_node: The List node containing constraints

    Returns:
        List of constraint dictionaries
    """
    constraints = []
    for item in list_node.elts:
        constraint = _parse_single_constraint(item)
        if constraint:
            constraints.append(constraint)
    return constraints


def _parse_constraints(value_node: nodes.NodeNG) -> list[dict[str, Any]]:
    """Parse Django model constraints from Meta.constraints.

    Args:
        value_node: The value node of the constraints assignment

    Returns:
        List of constraint dictionaries with 'type', 'fields', and 'name'
    """
    try:
        # Handle list of constraints
        if isinstance(value_node, nodes.List):
            return _parse_constraint_list(value_node)

        # Handle variable reference - try to infer the value
        if isinstance(value_node, nodes.Name):
            try:
                inferred_list = list(value_node.infer())
                for inferred in inferred_list:
                    if isinstance(inferred, nodes.List):
                        return _parse_constraint_list(inferred)
            except Exception:  # noqa: S110
                pass
    except Exception:  # noqa: S110
        pass

    return []


def _parse_single_constraint(node: nodes.NodeNG) -> Optional[dict[str, Any]]:
    """Parse a single constraint from a Call node.

    Args:
        node: The constraint Call node

    Returns:
        Dictionary with constraint information or None
    """
    if not isinstance(node, nodes.Call):
        return None

    constraint_info: dict[str, Any] = {}

    try:
        # Get constraint type (e.g., UniqueConstraint, CheckConstraint)
        if isinstance(node.func, nodes.Attribute):
            constraint_info["type"] = node.func.attrname
        elif isinstance(node.func, nodes.Name):
            constraint_info["type"] = node.func.name
        else:
            return None

        # Extract fields and name from keyword arguments
        for keyword in node.keywords:
            if keyword.arg == "fields":
                # Parse fields list
                fields = _extract_constraint_fields(keyword.value)
                if fields:
                    constraint_info["fields"] = fields
            elif keyword.arg == "name":
                # Parse name string
                name = _extract_constraint_name(keyword.value)
                if name:
                    constraint_info["name"] = name

        return constraint_info if constraint_info.get("type") else None
    except Exception:
        return None


def _extract_string_list_from_list_node(list_node: nodes.List) -> Optional[list[str]]:
    """Extract string values from a list node.

    Args:
        list_node: The List node

    Returns:
        List of string values or None if empty
    """
    fields = []
    for elt in list_node.elts:
        if isinstance(elt, nodes.Const) and isinstance(elt.value, str):
            fields.append(elt.value)
    return fields if fields else None


def _extract_constraint_fields(node: nodes.NodeNG) -> Optional[list[str]]:
    """Extract field names from constraint fields argument.

    Args:
        node: The node representing the fields argument

    Returns:
        List of field name strings or None
    """
    try:
        # Handle list literal
        if isinstance(node, nodes.List):
            return _extract_string_list_from_list_node(node)

        # Handle variable reference - try to infer
        if isinstance(node, nodes.Name):
            try:
                inferred_list = list(node.infer())
                for inferred in inferred_list:
                    if isinstance(inferred, nodes.List):
                        return _extract_string_list_from_list_node(inferred)
            except Exception:  # noqa: S110
                pass
    except Exception:  # noqa: S110
        pass

    return None


def _extract_constraint_name(node: nodes.NodeNG) -> Optional[str]:
    """Extract constraint name from name argument.

    Args:
        node: The node representing the name argument

    Returns:
        Constraint name string or None
    """
    try:
        # Handle string literal
        if isinstance(node, nodes.Const) and isinstance(node.value, str):
            return node.value

        # Handle variable reference - try to infer
        elif isinstance(node, nodes.Name):
            try:
                inferred_list = list(node.infer())
                for inferred in inferred_list:
                    if isinstance(inferred, nodes.Const) and isinstance(inferred.value, str):
                        return inferred.value
            except Exception:  # noqa: S110
                pass
    except Exception:  # noqa: S110
        pass

    return None


def get_meta_option(assign_node: nodes.Assign) -> Any:
    """Extract the value of a Meta class option.

    Args:
        assign_node: The assignment node in Meta class

    Returns:
        The option value (literal or string representation)
    """
    try:
        # Check if this is a constraints assignment
        if (
            assign_node.targets
            and isinstance(assign_node.targets[0], nodes.AssignName)
            and assign_node.targets[0].name == "constraints"
        ):
            return _parse_constraints(assign_node.value)

        return infer_literal_value(assign_node.value)
    except Exception:
        return None


def _extract_base_qname(base: Any, class_node: nodes.ClassDef) -> Optional[str]:  # noqa: C901
    """Extract the qualified name of a base class with full module path.

    Args:
        base: The base class node
        class_node: The class definition node (for accessing module imports)

    Returns:
        Full qualified name of the base class (e.g., "django.db.models.Model")
    """
    base_str = safe_as_string(base)  # type: ignore[arg-type]

    try:
        # Try to infer the base class to get its qname
        try:
            inferred_list = list(base.infer())
            for inferred in inferred_list:
                if hasattr(inferred, "qname"):
                    qname = inferred.qname()  # type: ignore[attr-defined]
                    # Return valid qname if it contains module path
                    if qname and "." in qname and not qname.startswith("builtins."):
                        return qname
        except Exception:
            return base_str

        # Fallback: Try to get from import statement
        base_name = None
        if isinstance(base, nodes.Attribute):
            # Pattern: models.Model
            base_name = base.attrname
            # Try to find where 'models' is imported from
            if isinstance(base.expr, nodes.Name):
                module_name = base.expr.name
                # Look up the import to get the full module path
                try:
                    module_root = class_node.root()
                    for import_node in module_root.nodes_of_class(nodes.Import):
                        for name, alias in import_node.names:
                            if (alias or name) == module_name:
                                return f"{name}.{base_name}"
                    for import_node in module_root.nodes_of_class(nodes.ImportFrom):
                        if import_node.modname and (import_node.level == 0):
                            for name, alias in import_node.names:
                                if (alias or name) == module_name:
                                    return f"{import_node.modname}.{name}.{base_name}"
                except Exception:
                    return base_str
        elif isinstance(base, nodes.Name):
            # Pattern: Model (direct import)
            base_name = base.name
            # Try to find where the base class is imported from
            try:
                module_root = class_node.root()
                for import_node in module_root.nodes_of_class(nodes.ImportFrom):
                    if import_node.modname:
                        for name, alias in import_node.names:
                            if (alias or name) == base_name:
                                return f"{import_node.modname}.{name}"
            except Exception:
                return base_str

    except Exception:
        return base_str

    return base_str


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
        if not base_model.get("meta", {}).get("abstract", False):
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
        # Skip 'abstract' flag as it should not be inherited
        for meta_key, meta_value in base_model.get("meta", {}).items():
            if meta_key not in model["meta"] and meta_key != "abstract":
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
