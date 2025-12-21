"""Data models for Django URL scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class UrlPattern(BaseModel):
    """A Django URL pattern.

    Attributes:
        type: Pattern type (path, re_path, include, etc)
        pattern: URL pattern string
        view_module: View module path
        view_name: View function/class name
        include_module: Included URLconf module
        namespace: URL namespace
        name: URL pattern name
        converters: Path converters used
        named_groups: Named regex groups
        viewset_module: ViewSet module for router patterns
        viewset_name: ViewSet class name
        basename: Router basename
        router_type: Router type (DefaultRouter, SimpleRouter)
        is_partial: Whether pattern is incomplete
        is_conditional: Whether pattern is conditional
        description: Pattern description
        note: Note for dynamic patterns
    """

    type: str = Field(..., description="Pattern type (path, re_path, include, etc)")
    pattern: str | None = Field(None, description="URL pattern string")
    view_module: str | None = Field(None, description="View module path")
    view_name: str | None = Field(None, description="View function/class name")
    include_module: str | None = Field(None, description="Included URLconf module")
    namespace: str | None = Field(None, description="URL namespace")
    name: str | None = Field(None, description="URL pattern name")
    converters: list[str] = Field(default_factory=list, description="Path converters")
    named_groups: list[str] = Field(default_factory=list, description="Named regex groups")
    viewset_module: str | None = Field(None, description="ViewSet module")
    viewset_name: str | None = Field(None, description="ViewSet class name")
    basename: str | None = Field(None, description="Router basename")
    router_type: str | None = Field(None, description="Router type")
    is_partial: bool = Field(default=False, description="Pattern is incomplete")
    is_conditional: bool = Field(default=False, description="Pattern is conditional")
    description: str | None = Field(None, description="Pattern description")
    note: str | None = Field(None, description="Note for dynamic patterns")


class UrlModule(BaseModel):
    """URL patterns in a module.

    Attributes:
        urlpatterns: List of URL patterns
    """

    urlpatterns: list[UrlPattern] = Field(..., description="URL patterns")


class DjangoUrlSummary(ScannerSummary):
    """Summary statistics for Django URLs.

    Attributes:
        total_modules: Number of URLconf modules
        total_patterns: Total number of URL patterns
    """

    total_modules: int = Field(ge=0, description="Number of URLconf modules")
    total_patterns: int = Field(ge=0, description="Total URL patterns")


class DjangoUrlOutput(ScannerOutput[dict[str, UrlModule]]):
    """Complete output from Django URL scanner.

    Attributes:
        summary: Summary statistics
        results: URL modules keyed by module path
    """

    summary: DjangoUrlSummary
    results: dict[str, UrlModule] = Field(..., alias="url_modules", description="URL modules")
