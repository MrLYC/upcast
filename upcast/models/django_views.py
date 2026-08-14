"""Typed output models for Django view scanning."""

from enum import Enum

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class ResolutionStatus(str, Enum):
    """Confidence state for a statically discovered fact."""

    CONFIRMED = "confirmed"
    PARTIAL = "partial"
    UNKNOWN = "unknown"


class SourceEvidence(BaseModel):
    """A source-located expression used to support a scanner finding."""

    file: str = Field(description="Source file relative to the scan root")
    line: int = Field(ge=1, description="One-based source line")
    expression: str = Field(description="Original source expression")
    kind: str = Field(description="Evidence role, such as base_class or decorator")
    status: ResolutionStatus = Field(description="Static resolution status")
    qualified_name: str | None = Field(None, description="Resolved qualified name when available")
    column: int | None = Field(None, ge=0, description="Zero-based source column when available")


class Recognition(BaseModel):
    """How a view was classified as a request handler."""

    status: ResolutionStatus = Field(description="Overall recognition status")
    evidence: list[SourceEvidence] = Field(default_factory=list, description="Supporting recognition evidence")


class RouteReference(BaseModel):
    """A direct URL or DRF Router reference to a view."""

    kind: str = Field(description="Route reference kind, such as direct or router")
    status: ResolutionStatus = Field(description="Whether the reference is confirmed")
    target_id: str | None = Field(None, description="Canonical target view identifier")
    pattern: str | None = Field(None, description="Direct URL pattern when available")
    prefix: str | None = Field(None, description="Router registration prefix when available")
    basename: str | None = Field(None, description="Router basename when available")
    router_type: str | None = Field(None, description="Resolved Router type when available")
    evidence: list[SourceEvidence] = Field(default_factory=list, description="Registration and mount evidence")


class PermissionExpression(BaseModel):
    """A statically represented DRF permission expression tree."""

    expression: str = Field(description="Original permission expression")
    status: ResolutionStatus = Field(description="Static resolution status")
    operator: str | None = Field(None, description="Boolean operator for a composite expression")
    qualified_name: str | None = Field(None, description="Resolved permission name for a leaf")
    children: list["PermissionExpression"] = Field(default_factory=list)
    evidence: SourceEvidence = Field(description="Source expression evidence")


class PermissionDefinition(BaseModel):
    """One-hop source information for a referenced custom permission."""

    qualified_name: str = Field(description="Canonical permission identifier")
    status: ResolutionStatus = Field(description="Whether the definition was found in scanned source")
    definition: SourceEvidence = Field(description="Permission class or function definition evidence")
    bases: list[SourceEvidence] = Field(default_factory=list, description="Direct inheritance evidence")
    check_methods: list[SourceEvidence] = Field(
        default_factory=list, description="Direct permission-check method evidence"
    )
    docstring: str | None = Field(None, description="Direct permission definition docstring")


class SecurityControl(BaseModel):
    """Evidence for one security control category."""

    state: str = Field(default="unknown", description="Bounded static conclusion for the control")
    declarations: list[SourceEvidence] = Field(default_factory=list, description="Declared control expressions")
    effective_evidence: list[SourceEvidence] = Field(
        default_factory=list,
        description="Evidence contributing to the effective static conclusion",
    )
    permission_expressions: list[PermissionExpression] = Field(
        default_factory=list,
        description="Permission expressions when this is the authorization control",
    )
    permission_definitions: list[PermissionDefinition] = Field(
        default_factory=list,
        description="One-hop custom permission definitions when resolvable",
    )


class ViewSecurity(BaseModel):
    """Separate authentication, authorization, CSRF, and raw security evidence."""

    authentication: SecurityControl = Field(default_factory=SecurityControl)
    authorization: SecurityControl = Field(default_factory=SecurityControl)
    csrf: SecurityControl = Field(default_factory=SecurityControl)
    raw_signals: list[SourceEvidence] = Field(
        default_factory=list,
        description="Unclassified decorators or control expressions retained verbatim",
    )


class ModelUsage(BaseModel):
    """A statically observed model relationship from a view or action."""

    model: str | None = Field(None, description="Resolved model qualified name when available")
    role: str = Field(description="Evidence role, such as queryset, serializer, or orm_call")
    operation: str = Field(description="Conservative operation category")
    evidence: SourceEvidence = Field(description="Source evidence for the model relationship")


class DjangoViewAction(BaseModel):
    """A method-level action exposed by a Django/DRF view."""

    id: str = Field(description="Canonical action identifier")
    name: str = Field(description="Action method name")
    origin: str = Field(description="Action origin, such as decorator or framework_derived")
    methods: list[str] = Field(default_factory=list, description="Declared HTTP methods")
    detail: bool | None = Field(None, description="Whether a DRF action is detail-scoped")
    url_path: str | None = Field(None, description="Explicit DRF action URL path when statically declared")
    url_name: str | None = Field(None, description="Explicit DRF action URL name when statically declared")
    line: int | None = Field(None, ge=1, description="Action definition line")
    security: ViewSecurity = Field(default_factory=ViewSecurity)
    model_usages: list[ModelUsage] = Field(default_factory=list)
    evidence: list[SourceEvidence] = Field(default_factory=list)


class DjangoView(BaseModel):
    """A discovered Django function, class-based view, or DRF ViewSet."""

    id: str = Field(description="Canonical qualified view identifier")
    name: str = Field(description="View symbol name")
    kind: str = Field(description="View kind")
    file: str = Field(description="View source file relative to the scan root")
    line: int = Field(ge=1, description="View definition line")
    recognition: Recognition = Field(description="Recognition result and evidence")
    route_refs: list[RouteReference] = Field(default_factory=list)
    security: ViewSecurity = Field(default_factory=ViewSecurity)
    model_usages: list[ModelUsage] = Field(default_factory=list)
    actions: list[DjangoViewAction] = Field(default_factory=list)


class DjangoViewSummary(ScannerSummary):
    """Summary counts for a Django-view scan."""

    total_views: int = Field(ge=0, description="Number of discovered view records")
    total_actions: int = Field(ge=0, description="Number of nested action records")


class DjangoViewOutput(ScannerOutput[DjangoViewSummary, dict[str, DjangoView]]):
    """Complete typed output for the Django view scanner."""

    summary: DjangoViewSummary
    results: dict[str, DjangoView] = Field(description="Views keyed by canonical identifiers")
    unresolved_route_references: list[RouteReference] = Field(
        default_factory=list,
        description="Unresolved direct route targets retained without fabricating a view record",
    )
