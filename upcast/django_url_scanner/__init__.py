"""Django URL pattern scanner.

This module provides tools to extract and analyze URL routing configurations
from Django applications using static code analysis. Includes support for
Django REST Framework (DRF) routers.
"""

from upcast.django_url_scanner.checker import UrlPatternChecker
from upcast.django_url_scanner.cli import scan_django_urls
from upcast.django_url_scanner.router_parser import parse_router_registrations

__all__ = ["UrlPatternChecker", "parse_router_registrations", "scan_django_urls"]
