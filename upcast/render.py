"""Rendering module for scanner outputs.

This module provides functionality to render scanner output models to markdown
and HTML formats using Jinja2 templates. Supports multiple languages (en, zh).

Usage:
    from upcast.render import render_to_markdown, render_to_html
    from upcast.models import HttpRequestOutput

    output = HttpRequestOutput(...)
    markdown = render_to_markdown(output, language='en', title='HTTP Requests')
    html = render_to_html(output, language='en', title='HTTP Requests')
"""

from pathlib import Path
from typing import Any

import markdown as md
from jinja2 import Environment, FileSystemLoader, select_autoescape

from upcast.common.export import export_to_yaml_string
from upcast.models.base import ScannerOutput
from upcast.models.blocking_operations import BlockingOperationsOutput
from upcast.models.complexity import ComplexityOutput
from upcast.models.concurrency import ConcurrencyPatternOutput
from upcast.models.django_models import DjangoModelOutput
from upcast.models.django_settings import DjangoSettingsOutput
from upcast.models.django_urls import DjangoUrlOutput
from upcast.models.env_vars import EnvVarOutput
from upcast.models.exceptions import ExceptionHandlerOutput
from upcast.models.http_requests import HttpRequestOutput
from upcast.models.logging import LoggingOutput
from upcast.models.metrics import PrometheusMetricOutput
from upcast.models.module_symbols import ModuleSymbolOutput
from upcast.models.redis_usage import RedisUsageOutput
from upcast.models.signals import SignalOutput
from upcast.models.unit_tests import UnitTestOutput

# Template directory path
TEMPLATES_DIR = Path(__file__).parent / "templates"

# Mapping of model types to markdown template names
MODEL_TEMPLATE_MAP = {
    HttpRequestOutput: "http_requests.md.jinja2",
    DjangoModelOutput: "django_models.md.jinja2",
    ComplexityOutput: "complexity.md.jinja2",
    EnvVarOutput: "env_vars.md.jinja2",
    SignalOutput: "signals.md.jinja2",
    BlockingOperationsOutput: "blocking_operations.md.jinja2",
    ConcurrencyPatternOutput: "base.md.jinja2",
    DjangoSettingsOutput: "django_settings.md.jinja2",
    DjangoUrlOutput: "django_urls.md.jinja2",
    ExceptionHandlerOutput: "exception_handlers.md.jinja2",
    PrometheusMetricOutput: "metrics.md.jinja2",
    RedisUsageOutput: "redis_usage.md.jinja2",
    UnitTestOutput: "unit_tests.md.jinja2",
    ModuleSymbolOutput: "module_symbols.md.jinja2",
    LoggingOutput: "logging.md.jinja2",
}

HTML_TEMPLATE_MAP: dict[type, str] = {}


def get_template_name(output: ScannerOutput) -> str:
    """Get the markdown template name for a given scanner output.

    Args:
        output: Scanner output instance

    Returns:
        Template file name

    Raises:
        ValueError: If no template is found for the output type
    """
    output_type = type(output)
    template_name = MODEL_TEMPLATE_MAP.get(output_type)

    if not template_name:
        # Try to find a matching base class
        for model_type, template in MODEL_TEMPLATE_MAP.items():
            if isinstance(output, model_type):
                template_name = template
                break

    if not template_name:
        raise ValueError(f"No template found for output type: {output_type.__name__}")

    return template_name


def get_html_template_name(output: ScannerOutput) -> str:
    """Get the HTML template name for a given scanner output.

    Args:
        output: Scanner output instance

    Returns:
        HTML template file name (defaults to base.html.jinja2)
    """
    output_type = type(output)
    template_name = HTML_TEMPLATE_MAP.get(output_type)

    if not template_name:
        # Try to find a matching base class
        for model_type, template in HTML_TEMPLATE_MAP.items():
            if isinstance(output, model_type):
                template_name = template
                break

    # Default to base HTML template
    return template_name or "base.html.jinja2"


def create_jinja_env(language: str = "en") -> Environment:
    """Create a Jinja2 environment for the specified language (markdown templates).

    Args:
        language: Language code (en, zh, etc.)

    Returns:
        Configured Jinja2 Environment

    Raises:
        ValueError: If language directory doesn't exist
    """
    lang_dir = TEMPLATES_DIR / language
    if not lang_dir.exists():
        raise ValueError(f"Template directory not found for language: {language}")

    env = Environment(
        loader=FileSystemLoader(lang_dir),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    return env


def create_jinja_env_html(language: str = "en") -> Environment:
    """Create a Jinja2 environment for HTML templates.

    The loader searches in multiple directories to support template inheritance:
    - Language-specific directory (e.g., templates/en/)
    - Root templates directory (for _base.html.jinja2)
    - _macros directory (for shared macros)

    Args:
        language: Language code (en, zh, etc.)

    Returns:
        Configured Jinja2 Environment

    Raises:
        ValueError: If language directory doesn't exist
    """
    lang_dir = TEMPLATES_DIR / language
    if not lang_dir.exists():
        raise ValueError(f"Template directory not found for language: {language}")

    search_paths = [
        lang_dir,
        TEMPLATES_DIR,
    ]

    env = Environment(
        loader=FileSystemLoader(search_paths),
        autoescape=select_autoescape(["html", "xml", "jinja2"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    return env


def render_to_markdown(
    output: ScannerOutput,
    language: str = "en",
    title: str | None = None,
    **extra_context: Any,
) -> str:
    """Render a scanner output to markdown.

    Args:
        output: Scanner output instance
        language: Language code (en, zh, etc.)
        title: Optional title for the document
        **extra_context: Additional context variables for the template

    Returns:
        Rendered markdown string

    Raises:
        ValueError: If template not found or language not supported
    """
    # Get template name based on output type
    template_name = get_template_name(output)

    # Create Jinja2 environment
    env = create_jinja_env(language)

    # Load template
    template = env.get_template(template_name)

    # Prepare context
    context = {
        "title": title or "Scanner Output",
        "summary": output.summary,
        "results": output.results,
        "metadata": output.metadata,
        **extra_context,
    }

    # Render template
    markdown_content = template.render(**context)

    return markdown_content


def render_to_html(
    output: ScannerOutput,
    language: str = "en",
    title: str | None = None,
    **extra_context: Any,
) -> str:
    """Render a scanner output to a standalone HTML report.

    The HTML report includes:
    - Rendered markdown content as HTML
    - Embedded YAML data (downloadable)
    - Embedded JSON data (downloadable)
    - Interactive features via inline JavaScript

    Args:
        output: Scanner output instance
        language: Language code (en, zh, etc.)
        title: Optional title for the document
        **extra_context: Additional context variables for the template

    Returns:
        Complete HTML document as string

    Raises:
        ValueError: If template not found or language not supported
    """
    markdown_content = render_to_markdown(output, language=language, title=title)

    rendered_markdown = md.markdown(
        markdown_content,
        extensions=["tables", "fenced_code"],
    )

    json_data = output.model_dump(mode="json", exclude_none=False)
    yaml_data = export_to_yaml_string(json_data)

    template_name = get_html_template_name(output)
    env = create_jinja_env_html(language)
    template = env.get_template(template_name)

    html_content = template.render(
        title=title or "Scanner Report",
        language=language,
        rendered_markdown=rendered_markdown,
        yaml_data=yaml_data,
        json_data=json_data,
        summary=output.summary,
        results=output.results,
        metadata=output.metadata,
        **extra_context,
    )

    return html_content


def render_to_file(
    output: ScannerOutput,
    output_path: str | Path,
    language: str = "en",
    title: str | None = None,
    format: str = "markdown",  # noqa: A002
    **extra_context: Any,
) -> None:
    """Render a scanner output to a file (markdown or HTML).

    Args:
        output: Scanner output instance
        output_path: Path to output file
        language: Language code (en, zh, etc.)
        title: Optional title for the document
        format: Output format ("markdown" or "html")
        **extra_context: Additional context variables for the template

    Raises:
        ValueError: If template not found, language not supported, or invalid format
        IOError: If file cannot be written
    """
    if format.lower() == "html":
        content = render_to_html(output, language=language, title=title, **extra_context)
    elif format.lower() == "markdown":
        content = render_to_markdown(output, language=language, title=title, **extra_context)
    else:
        raise ValueError(f"Invalid format: {format}. Must be 'markdown' or 'html'.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


__all__ = [
    "create_jinja_env",
    "create_jinja_env_html",
    "get_html_template_name",
    "get_template_name",
    "render_to_file",
    "render_to_html",
    "render_to_markdown",
]
