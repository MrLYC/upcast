"""Tests for direct Django model-use evidence."""

import astroid

from upcast.common.django.view_model_usage import ModelModule, extract_class_model_usages


MODELS_SOURCE = """
class Order:
    pass
"""

SERIALIZERS_SOURCE = """
from .models import Order


class OrderSerializer:
    class Meta:
        model = Order
"""

VIEWS_SOURCE = """
from .models import Order
from .serializers import OrderSerializer


class OrdersViewSet:
    queryset = Order.objects.all()
    model = Order
    serializer_class = OrderSerializer

    def search(self):
        return Order.objects.filter(active=True)

    def create_order(self):
        return Order.objects.create()

    def purge(self):
        return Order.objects.filter(stale=True).delete()

    def ensure(self):
        return Order.objects.get_or_create(number="1")


class DynamicOrdersView:
    queryset = get_queryset()

    def custom_manager(self):
        return Order.special_manager.lookup()

    def schema_call(self):
        return cls.input_class.schema()
"""


def test_model_usage_reports_only_direct_declarations_serializer_metadata_and_known_orm_operations():
    """Dynamic/custom-manager expressions stay unknown instead of fabricating model behavior."""
    models_module = astroid.parse(MODELS_SOURCE, module_name="pkg.models")
    serializers_module = astroid.parse(SERIALIZERS_SOURCE, module_name="pkg.serializers")
    views_module = astroid.parse(VIEWS_SOURCE, module_name="pkg.views")
    modules = [
        ModelModule(models_module, "pkg.models", "pkg/models.py"),
        ModelModule(serializers_module, "pkg.serializers", "pkg/serializers.py"),
        ModelModule(views_module, "pkg.views", "pkg/views.py"),
    ]
    class_node = views_module.locals["OrdersViewSet"][0]
    dynamic_class_node = views_module.locals["DynamicOrdersView"][0]

    usages = extract_class_model_usages(
        class_node,
        file="pkg/views.py",
        module_name="pkg.views",
        modules=modules,
    )
    usages.extend(
        extract_class_model_usages(
            dynamic_class_node,
            file="pkg/views.py",
            module_name="pkg.views",
            modules=modules,
        )
    )

    observed = {(usage.role, usage.model, usage.operation, usage.evidence.status) for usage in usages}

    assert ("queryset", "pkg.models.Order", "read", "confirmed") in observed
    assert ("model", "pkg.models.Order", "unknown", "confirmed") in observed
    assert ("serializer", "pkg.models.Order", "unknown", "confirmed") in observed
    assert ("orm_call", "pkg.models.Order", "read", "confirmed") in observed
    assert ("orm_call", "pkg.models.Order", "write", "confirmed") in observed
    assert ("orm_call", "pkg.models.Order", "delete", "confirmed") in observed
    assert ("orm_call", "pkg.models.Order", "read_write", "confirmed") in observed
    assert ("queryset", None, "unknown", "unknown") in observed
    assert ("orm_call", None, "unknown", "unknown") in observed
    assert all("input_class.schema" not in usage.evidence.expression for usage in usages)
