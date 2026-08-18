"""Data models for Django and Django REST Framework view scanning."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class ViewRouteLink(BaseModel):
    """A statically discovered URL or router reference to a view."""

    type: str = Field(description="URL reference type")
    url_module: str | None = Field(None, description="URLconf module containing the reference")
    pattern: str | None = Field(None, description="Route prefix or pattern")
    full_path: str | None = Field(None, description="Reconstructed route path")
    name: str | None = Field(None, description="URL name or router basename")
    file: str | None = Field(None, description="Source file containing the reference")
    line: int | None = Field(None, description="Source line containing the reference")


class ViewAction(BaseModel):
    """A DRF ``@action`` method and its local evidence."""

    name: str
    methods: list[str] = Field(default_factory=list)
    detail: bool | None = None
    url_path: str | None = None
    url_name: str | None = None
    decorators: list[str] = Field(default_factory=list)
    permission_classes: list[str] = Field(default_factory=list)
    authentication_classes: list[str] = Field(default_factory=list)
    login_exempt: bool | None = None
    csrf_exempt: bool | None = None
    file: str | None = None
    line: int | None = None


class DjangoView(BaseModel):
    """A Django function-based or class-based view."""

    module: str
    name: str
    qualname: str
    kind: str = Field(description="function, class, or method")
    status: str = Field(description="confirmed or unknown")
    identified_by: list[str] = Field(default_factory=list)
    route_linkage: list[ViewRouteLink] = Field(default_factory=list)
    bases: list[str] = Field(default_factory=list)
    decorators: list[str] = Field(default_factory=list)
    http_methods: list[str] = Field(default_factory=list)
    actions: list[ViewAction] = Field(default_factory=list)
    permission_classes: list[str] = Field(default_factory=list)
    authentication_classes: list[str] = Field(default_factory=list)
    login_exempt: bool | None = None
    csrf_exempt: bool | None = None
    model_references: list[str] = Field(default_factory=list)
    serializer_class: str | None = None
    file: str | None = None
    line: int | None = None


class DjangoViewSummary(ScannerSummary):
    """Summary statistics for Django views."""

    total_modules: int = Field(ge=0, description="Number of modules containing views")
    total_views: int = Field(ge=0, description="Total number of views")


class DjangoViewOutput(ScannerOutput[DjangoViewSummary, dict[str, list[DjangoView]]]):
    """Complete output from the Django view scanner."""

    summary: DjangoViewSummary
    results: dict[str, list[DjangoView]] = Field(description="Views grouped by module")
