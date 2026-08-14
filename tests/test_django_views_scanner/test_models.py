"""Tests for Django view scanner output models."""

from upcast.models.django_views import (
    DjangoView,
    DjangoViewAction,
    DjangoViewOutput,
    DjangoViewSummary,
    ModelUsage,
    Recognition,
    ResolutionStatus,
    RouteReference,
    SourceEvidence,
    ViewSecurity,
)


def test_django_view_output_preserves_view_action_security_and_model_evidence():
    """A view result keeps the evidence needed for downstream audit tooling."""
    base_evidence = SourceEvidence(
        file="pkg/views.py",
        line=10,
        expression="ModelViewSet",
        kind="base_class",
        status=ResolutionStatus.CONFIRMED,
        qualified_name="rest_framework.viewsets.ModelViewSet",
    )
    action = DjangoViewAction(
        id="pkg.views.OrderViewSet#archive",
        name="archive",
        origin="decorator",
        methods=["post"],
        detail=True,
        line=21,
        security=ViewSecurity(raw_signals=[base_evidence]),
        model_usages=[
            ModelUsage(
                model="pkg.models.Order",
                role="orm_call",
                operation="write",
                evidence=base_evidence,
            )
        ],
    )
    view = DjangoView(
        id="pkg.views.OrderViewSet",
        name="OrderViewSet",
        kind="drf_viewset",
        file="pkg/views.py",
        line=10,
        recognition=Recognition(status=ResolutionStatus.CONFIRMED, evidence=[base_evidence]),
        route_refs=[
            RouteReference(
                kind="router",
                status=ResolutionStatus.CONFIRMED,
                target_id="pkg.views.OrderViewSet",
                prefix="orders",
                basename="order",
                evidence=[base_evidence],
            )
        ],
        security=ViewSecurity(raw_signals=[base_evidence]),
        model_usages=[],
        actions=[action],
    )

    output = DjangoViewOutput(
        summary=DjangoViewSummary(
            total_count=1,
            files_scanned=1,
            scan_duration_ms=0,
            total_views=1,
            total_actions=1,
        ),
        results={view.id: view},
        metadata={"scanner_name": "django-views"},
    )

    assert output.results[view.id].actions[0].model_usages[0].operation == "write"
    assert output.results[view.id].route_refs[0].target_id == view.id
    assert output.model_dump(mode="json")["metadata"]["scanner_name"] == "django-views"
