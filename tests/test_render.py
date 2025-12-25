"""Tests for markdown rendering module."""

import tempfile
from pathlib import Path

import pytest

from upcast.models.complexity import ComplexityOutput, ComplexityResult, ComplexitySummary
from upcast.models.django_models import DjangoField, DjangoModel, DjangoModelOutput, DjangoModelSummary
from upcast.models.env_vars import EnvVarInfo, EnvVarLocation, EnvVarOutput, EnvVarSummary
from upcast.models.http_requests import (
    HttpRequestInfo,
    HttpRequestOutput,
    HttpRequestSummary,
    HttpRequestUsage,
)
from upcast.models.signals import SignalInfo, SignalOutput, SignalSummary, SignalUsage
from upcast.render import create_jinja_env, get_template_name, render_to_file, render_to_markdown


class TestGetTemplateName:
    """Test get_template_name function."""

    def test_http_request_output(self):
        """Test template name for HttpRequestOutput."""
        output = HttpRequestOutput(
            summary=HttpRequestSummary(
                total_count=1, files_scanned=1, total_requests=1, unique_urls=1, by_library={"requests": 1}
            ),
            results={},
        )
        assert get_template_name(output) == "http_requests.md.jinja2"

    def test_django_model_output(self):
        """Test template name for DjangoModelOutput."""
        output = DjangoModelOutput(
            summary=DjangoModelSummary(total_count=1, files_scanned=1, total_models=1, total_fields=0, total_relationships=0),
            results={},
        )
        assert get_template_name(output) == "django_models.md.jinja2"

    def test_complexity_output(self):
        """Test template name for ComplexityOutput."""
        output = ComplexityOutput(
            summary=ComplexitySummary(total_count=1, files_scanned=1, high_complexity_count=0, by_severity={}),
            results={},
        )
        assert get_template_name(output) == "complexity.md.jinja2"


class TestCreateJinjaEnv:
    """Test create_jinja_env function."""

    def test_english_environment(self):
        """Test creating English environment."""
        env = create_jinja_env("en")
        assert env is not None
        assert "base.md.jinja2" in env.list_templates()

    def test_chinese_environment(self):
        """Test creating Chinese environment."""
        env = create_jinja_env("zh")
        assert env is not None
        assert "base.md.jinja2" in env.list_templates()

    def test_invalid_language(self):
        """Test creating environment with invalid language."""
        with pytest.raises(ValueError, match="Template directory not found"):
            create_jinja_env("invalid_lang")


class TestRenderToMarkdown:
    """Test render_to_markdown function."""

    def test_render_http_requests_en(self):
        """Test rendering HTTP requests in English."""
        output = HttpRequestOutput(
            summary=HttpRequestSummary(
                total_count=2,
                files_scanned=1,
                total_requests=2,
                unique_urls=1,
                by_library={"requests": 2},
            ),
            results={
                "https://api.example.com": HttpRequestInfo(
                    method="GET",
                    library="requests",
                    usages=[
                        HttpRequestUsage(
                            file="test.py",
                            line=10,
                            statement="requests.get('https://api.example.com')",
                            method="GET",
                            session_based=False,
                            is_async=False,
                        )
                    ],
                )
            },
            metadata={"scanner": "http_request"},
        )

        markdown = render_to_markdown(output, language="en", title="HTTP Requests Test")

        assert "HTTP Requests Test" in markdown
        assert "Total Requests" in markdown
        assert "https://api.example.com" in markdown
        assert "requests.get" in markdown
        assert "test.py" in markdown

    def test_render_django_models_zh(self):
        """Test rendering Django models in Chinese."""
        output = DjangoModelOutput(
            summary=DjangoModelSummary(
                total_count=1,
                files_scanned=1,
                total_models=1,
                total_fields=2,
                total_relationships=0,
            ),
            results={
                "app.models.User": DjangoModel(
                    name="User",
                    module="app.models",
                    bases=["models.Model"],
                    fields={
                        "username": DjangoField(
                            name="username",
                            type="CharField",
                            parameters={"max_length": 100},
                            line=5,
                        ),
                        "email": DjangoField(
                            name="email",
                            type="EmailField",
                            parameters={},
                            line=6,
                        ),
                    },
                    relationships=[],
                    line=3,
                )
            },
        )

        markdown = render_to_markdown(output, language="zh", title="Django 模型测试")

        assert "Django 模型测试" in markdown
        assert "模型总数" in markdown
        assert "User" in markdown
        assert "username" in markdown
        assert "email" in markdown

    def test_render_complexity_en(self):
        """Test rendering complexity results in English."""
        output = ComplexityOutput(
            summary=ComplexitySummary(
                total_count=1,
                files_scanned=1,
                high_complexity_count=1,
                by_severity={"warning": 1},
            ),
            results={
                "test/module.py": [
                    ComplexityResult(
                        name="complex_function",
                        line=10,
                        end_line=50,
                        complexity=15,
                        severity="warning",
                        message="Function has high complexity",
                        description="A complex function",
                        signature="def complex_function(x, y):",
                        code="def complex_function(x, y):\n    # code here\n    pass",
                        comment_lines=1,
                        code_lines=40,
                    )
                ]
            },
        )

        markdown = render_to_markdown(output, language="en", title="Complexity Analysis")

        assert "Complexity Analysis" in markdown
        assert "complex_function" in markdown
        assert "Complexity Score" in markdown
        assert "warning" in markdown

    def test_render_env_vars_en(self):
        """Test rendering environment variables in English."""
        output = EnvVarOutput(
            summary=EnvVarSummary(
                total_count=2,
                files_scanned=1,
                total_env_vars=2,
                required_count=1,
                optional_count=1,
            ),
            results={
                "DATABASE_URL": EnvVarInfo(
                    name="DATABASE_URL",
                    required=True,
                    default_value=None,
                    locations=[
                        EnvVarLocation(
                            file="settings.py",
                            line=10,
                            column=5,
                            pattern="os.environ['DATABASE_URL']",
                            code="db_url = os.environ['DATABASE_URL']",
                        )
                    ],
                ),
                "DEBUG": EnvVarInfo(
                    name="DEBUG",
                    required=False,
                    default_value="False",
                    locations=[
                        EnvVarLocation(
                            file="settings.py",
                            line=15,
                            column=5,
                            pattern="os.getenv('DEBUG', 'False')",
                            code="debug = os.getenv('DEBUG', 'False')",
                        )
                    ],
                ),
            },
        )

        markdown = render_to_markdown(output, language="en", title="Environment Variables")

        assert "Environment Variables" in markdown
        assert "DATABASE_URL" in markdown
        assert "DEBUG" in markdown
        assert "Required" in markdown

    def test_render_signals_zh(self):
        """Test rendering signals in Chinese."""
        output = SignalOutput(
            summary=SignalSummary(
                total_count=1,
                files_scanned=1,
                django_receivers=1,
                django_senders=0,
                celery_receivers=0,
                celery_senders=0,
                custom_signals_defined=0,
                unused_custom_signals=0,
            ),
            results=[
                SignalInfo(
                    signal="post_save",
                    type="django",
                    category="model_signals",
                    receivers=[
                        SignalUsage(
                            file="handlers.py",
                            line=20,
                            column=0,
                            handler="save_handler",
                            pattern="receiver_decorator",
                            code="@receiver(post_save)",
                        )
                    ],
                    senders=[],
                )
            ],
        )

        markdown = render_to_markdown(output, language="zh", title="信号分析")

        assert "信号分析" in markdown
        assert "post_save" in markdown
        assert "Django 接收器" in markdown
        assert "handlers.py" in markdown


class TestRenderToFile:
    """Test render_to_file function."""

    def test_render_to_file(self):
        """Test rendering to a file."""
        output = HttpRequestOutput(
            summary=HttpRequestSummary(
                total_count=1,
                files_scanned=1,
                total_requests=1,
                unique_urls=1,
                by_library={"requests": 1},
            ),
            results={},
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.md"
            render_to_file(output, output_path, language="en", title="Test Output")

            assert output_path.exists()
            content = output_path.read_text()
            assert "Test Output" in content
            assert "Total Requests" in content

    def test_render_to_file_creates_directory(self):
        """Test that render_to_file creates parent directories."""
        output = ComplexityOutput(
            summary=ComplexitySummary(
                total_count=0,
                files_scanned=0,
                high_complexity_count=0,
                by_severity={},
            ),
            results={},
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "nested" / "path" / "output.md"
            render_to_file(output, output_path, language="en", title="Nested Test")

            assert output_path.exists()
            assert output_path.parent.exists()
