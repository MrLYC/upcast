"""Scanner-level regression tests for structured Django view output."""

from pathlib import Path

import astroid

from upcast.models.django_views import ResolutionStatus
from upcast.scanners.django_views import DjangoViewScanner, _ModuleContext


def test_scanner_emits_structured_view_security_and_action_evidence(tmp_path):
    views_file = tmp_path / "demo" / "views.py"
    views_file.parent.mkdir()
    views_file.write_text(
        """
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet


class UserViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    @action(methods=["post"], detail=False, url_path="sync", permission_classes=[AllowAny])
    @custom_audit
    def sync(self, request):
        return None


@csrf_exempt
@api_view(["GET"])
def health(request):
    return None
"""
    )

    output = DjangoViewScanner().scan(tmp_path)

    assert list(output.results) == sorted(output.results)
    viewset = output.results["demo.views.UserViewSet"]
    health = output.results["demo.views.health"]
    action = next(item for item in viewset.actions if item.name == "sync")

    assert viewset.kind == "drf_viewset"
    assert viewset.recognition.status is ResolutionStatus.CONFIRMED
    assert viewset.security.authorization.state == "configured"
    assert action.origin == "decorator"
    assert action.methods == ["post"]
    assert [signal.expression for signal in action.security.raw_signals] == ["custom_audit"]
    assert health.kind == "drf_function_view"
    assert health.security.csrf.state == "exempt"


def test_scanner_links_module_level_direct_routes_and_ignores_helpers(tmp_path):
    views_file = tmp_path / "demo" / "views.py"
    urls_file = tmp_path / "demo" / "urls.py"
    views_file.parent.mkdir()
    views_file.write_text("def health(request):\n    return None\n")
    urls_file.write_text(
        """
from django.urls import path
from .views import health

urlpatterns = [path("health/", health)]

def build_patterns():
    return [path("helper/", health)]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    view = output.results["demo.views.health"]

    assert view.recognition.status is ResolutionStatus.CONFIRMED
    assert [reference.pattern for reference in view.route_refs] == ["health/"]


def test_scanner_keeps_unmounted_router_registration_as_partial(tmp_path):
    views_file = tmp_path / "app" / "views.py"
    urls_file = tmp_path / "app" / "urls.py"
    views_file.parent.mkdir()
    views_file.write_text(
        """
from rest_framework.viewsets import ViewSet

class UserViewSet(ViewSet):
    pass
"""
    )
    urls_file.write_text(
        """
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    reference = output.results["app.views.UserViewSet"].route_refs[0]

    assert reference.status is ResolutionStatus.PARTIAL
    assert reference.prefix == "users"


def test_export_alias_propagation_uses_a_work_queue():
    """Long wildcard re-export chains remain linear in import-map traversals."""

    class CountingImports(dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.items_calls = 0

        def items(self):
            self.items_calls += 1
            return super().items()

    scanner = DjangoViewScanner()
    chain_length = 80
    contexts = []
    for index in range(chain_length):
        module_path = f"demo.module_{index}"
        source = (
            f"from demo.module_{index + 1} import *\n" if index + 1 < chain_length else "class HealthView:\n    pass\n"
        )
        module = astroid.parse(source, path=f"module_{index}.py")
        contexts.append(
            _ModuleContext(
                module_path=module_path,
                file_path=Path(f"module_{index}.py"),
                module=module,
                imports=CountingImports(scanner._collect_imports(module, module_path)),
                symbols=scanner._collect_symbols(module),
            )
        )

    aliases = scanner._build_export_aliases(contexts, scanner._build_module_aliases(contexts))

    assert aliases[("demo.module_0", "HealthView")] == (f"demo.module_{chain_length - 1}", "HealthView")
    assert sum(context.imports.items_calls for context in contexts) <= chain_length * 2
