"""Django-related utility functions for scanners.

This package contains utility functions extracted from old scanner modules,
providing a centralized location for Django-related parsing and analysis utilities.

Available modules:
- model_utils.py: Django model detection and field analysis
- model_parser.py: Model parsing with inheritance and Meta options
- router_parser.py: Django REST Framework router registration parsing
- url_parser.py: URL pattern parsing for path() and regex patterns
- view_resolver.py: View reference resolution
- settings_utils.py: Settings detection and access patterns
- settings_parser.py: Settings definition parsing and module analysis
"""

# Export commonly used utilities for easier imports
from upcast.common.django.model_parser import merge_abstract_fields, parse_model
from upcast.common.django.model_utils import is_django_field, is_django_model
from upcast.common.django.router_parser import parse_router_registrations
from upcast.common.django.settings_parser import is_settings_module, parse_settings_module
from upcast.common.django.settings_utils import (
    extract_setting_name,
    is_settings_attribute_access,
    is_settings_getattr_call,
    is_settings_hasattr_call,
)
from upcast.common.django.url_parser import parse_url_pattern
from upcast.common.django.view_resolver import resolve_view

__all__ = [
    "extract_setting_name",
    "is_django_field",
    "is_django_model",
    "is_settings_attribute_access",
    "is_settings_getattr_call",
    "is_settings_hasattr_call",
    "is_settings_module",
    "merge_abstract_fields",
    "parse_model",
    "parse_router_registrations",
    "parse_settings_module",
    "parse_url_pattern",
    "resolve_view",
]
