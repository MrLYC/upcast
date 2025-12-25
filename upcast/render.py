"""Markdown rendering module for scanner outputs.

This module provides functionality to render scanner output models to markdown
format using Jinja2 templates. Supports multiple languages (en, zh).

Usage:
    from upcast.render import render_to_markdown
    from upcast.models import HttpRequestOutput

    output = HttpRequestOutput(...)
    markdown = render_to_markdown(output, language='en', title='HTTP Requests')
"""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

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
from upcast.models.metrics import PrometheusMetricOutput
from upcast.models.redis_usage import RedisUsageOutput
from upcast.models.signals import SignalOutput
from upcast.models.unit_tests import UnitTestOutput

# Template directory path
TEMPLATES_DIR = Path(__file__).parent / "templates"

# Mapping of model types to template names
MODEL_TEMPLATE_MAP = {
    HttpRequestOutput: "http_requests.md.jinja2",
    DjangoModelOutput: "django_models.md.jinja2",
    ComplexityOutput: "complexity.md.jinja2",
    EnvVarOutput: "env_vars.md.jinja2",
    SignalOutput: "signals.md.jinja2",
    BlockingOperationsOutput: "base.md.jinja2",  # Use base template for now
    ConcurrencyPatternOutput: "base.md.jinja2",
    DjangoSettingsOutput: "base.md.jinja2",
    DjangoUrlOutput: "base.md.jinja2",
    ExceptionHandlerOutput: "base.md.jinja2",
    PrometheusMetricOutput: "base.md.jinja2",
    RedisUsageOutput: "base.md.jinja2",
    UnitTestOutput: "base.md.jinja2",
}


def get_template_name(output: ScannerOutput) -> str:
    """Get the template name for a given scanner output.

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


def create_jinja_env(language: str = "en") -> Environment:
    """Create a Jinja2 environment for the specified language.

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
    markdown = template.render(**context)

    return markdown


def render_to_file(
    output: ScannerOutput,
    output_path: str | Path,
    language: str = "en",
    title: str | None = None,
    **extra_context: Any,
) -> None:
    """Render a scanner output to a markdown file.

    Args:
        output: Scanner output instance
        output_path: Path to output markdown file
        language: Language code (en, zh, etc.)
        title: Optional title for the document
        **extra_context: Additional context variables for the template

    Raises:
        ValueError: If template not found or language not supported
        IOError: If file cannot be written
    """
    markdown = render_to_markdown(output, language=language, title=title, **extra_context)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)


__all__ = [
    "create_jinja_env",
    "get_template_name",
    "render_to_file",
    "render_to_markdown",
]
