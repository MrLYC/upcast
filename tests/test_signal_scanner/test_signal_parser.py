"""Unit tests for signal parser functions."""

from pathlib import Path

from astroid import parse

from upcast.signal_scanner.signal_parser import (
    categorize_celery_signal,
    categorize_django_signal,
    parse_celery_connect_decorator,
    parse_custom_signal_definition,
    parse_receiver_decorator,
    parse_signal_connect_method,
)

# Add fixtures to path
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_parse_receiver_decorator_single_signal():
    """Test parsing @receiver with single signal."""
    code = """
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Order)
def handler(sender, instance, **kwargs):
    pass
"""
    module = parse(code)
    func = next(module.nodes_of_class(type(parse("def f(): pass").body[0])))

    handlers = parse_receiver_decorator(func)

    assert len(handlers) == 1
    assert handlers[0]["signal"] == "post_save"
    assert handlers[0]["handler"] == "handler"
    assert handlers[0]["sender"] == "Order"


def test_parse_receiver_decorator_multiple_signals():
    """Test parsing @receiver with multiple signals."""
    code = """
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver

@receiver([pre_delete, post_delete], sender=Product)
def handler(sender, instance, **kwargs):
    pass
"""
    module = parse(code)
    func = next(module.nodes_of_class(type(parse("def f(): pass").body[0])))

    handlers = parse_receiver_decorator(func)

    assert len(handlers) == 2
    assert handlers[0]["signal"] == "pre_delete"
    assert handlers[1]["signal"] == "post_delete"
    assert all(h["sender"] == "Product" for h in handlers)


def test_parse_celery_connect_decorator():
    """Test parsing @signal.connect decorator."""
    code = """
from celery.signals import task_prerun

@task_prerun.connect
def handler(task_id, task, **kwargs):
    pass
"""
    module = parse(code)
    func = next(module.nodes_of_class(type(parse("def f(): pass").body[0])))

    handlers = parse_celery_connect_decorator(func)

    assert len(handlers) == 1
    assert handlers[0]["signal"] == "task_prerun"
    assert handlers[0]["handler"] == "handler"


def test_parse_signal_connect_method_django():
    """Test parsing signal.connect() method for Django."""
    code = """
from django.db.models.signals import post_save

def my_handler(sender, instance, **kwargs):
    pass

post_save.connect(my_handler, sender=Article)
"""
    module = parse(code)
    call = next(module.nodes_of_class(type(parse("f()").body[0].value)))

    handler = parse_signal_connect_method(call)

    assert handler is not None
    assert handler["signal"] == "post_save"
    assert handler["handler"] == "my_handler"
    assert handler["sender"] == "Article"


def test_parse_signal_connect_method_celery():
    """Test parsing signal.connect() method for Celery."""
    code = """
from celery.signals import task_postrun

def generic_handler(task_id, **kwargs):
    pass

task_postrun.connect(generic_handler)
"""
    module = parse(code)
    call = next(module.nodes_of_class(type(parse("f()").body[0].value)))

    handler = parse_signal_connect_method(call)

    assert handler is not None
    assert handler["signal"] == "task_postrun"
    assert handler["handler"] == "generic_handler"
    assert "sender" not in handler


def test_parse_custom_signal_definition():
    """Test parsing custom Signal() definition."""
    code = """
from django.dispatch import Signal

order_paid = Signal()
"""
    module = parse(code)
    assign = next(module.nodes_of_class(type(parse("x = 1").body[0])))

    signal_def = parse_custom_signal_definition(assign)

    assert signal_def is not None
    assert signal_def["name"] == "order_paid"
    assert "line" in signal_def


def test_parse_custom_signal_with_providing_args():
    """Test parsing Signal() with providing_args."""
    code = """
from django.dispatch import Signal

payment_failed = Signal(providing_args=['order', 'error'])
"""
    module = parse(code)
    assign = next(module.nodes_of_class(type(parse("x = 1").body[0])))

    signal_def = parse_custom_signal_definition(assign)

    assert signal_def is not None
    assert signal_def["name"] == "payment_failed"
    assert "providing_args" in signal_def
    assert signal_def["providing_args"] == ["order", "error"]


def test_categorize_django_signal():
    """Test Django signal categorization."""
    assert categorize_django_signal("post_save") == "model_signals"
    assert categorize_django_signal("pre_delete") == "model_signals"
    assert categorize_django_signal("request_started") == "request_signals"
    assert categorize_django_signal("pre_migrate") == "management_signals"
    assert categorize_django_signal("custom_signal") == "other_signals"


def test_categorize_celery_signal():
    """Test Celery signal categorization."""
    assert categorize_celery_signal("task_prerun") == "task_signals"
    assert categorize_celery_signal("task_failure") == "task_signals"
    assert categorize_celery_signal("worker_ready") == "worker_signals"
    assert categorize_celery_signal("beat_init") == "beat_signals"
    assert categorize_celery_signal("custom_signal") == "other_signals"


def test_parse_receiver_no_decorator():
    """Test function without @receiver returns empty list."""
    code = """
def handler(sender, instance, **kwargs):
    pass
"""
    module = parse(code)
    func = next(module.nodes_of_class(type(parse("def f(): pass").body[0])))

    handlers = parse_receiver_decorator(func)

    assert len(handlers) == 0


def test_parse_celery_connect_no_decorator():
    """Test function without @connect returns empty list."""
    code = """
def handler(task_id, **kwargs):
    pass
"""
    module = parse(code)
    func = next(module.nodes_of_class(type(parse("def f(): pass").body[0])))

    handlers = parse_celery_connect_decorator(func)

    assert len(handlers) == 0


def test_parse_signal_connect_method_wrong_method():
    """Test non-.connect() call returns None."""
    code = """
from django.db.models.signals import post_save

post_save.send(sender=Order)
"""
    module = parse(code)
    call = next(module.nodes_of_class(type(parse("f()").body[0].value)))

    handler = parse_signal_connect_method(call)

    assert handler is None


def test_parse_custom_signal_not_signal_call():
    """Test non-Signal() assignment returns None."""
    code = """
order_paid = "some_string"
"""
    module = parse(code)
    assign = next(module.nodes_of_class(type(parse("x = 1").body[0])))

    signal_def = parse_custom_signal_definition(assign)

    assert signal_def is None
