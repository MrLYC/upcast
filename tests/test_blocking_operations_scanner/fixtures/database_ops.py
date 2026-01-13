"""Fixture: Database blocking operations (Django)."""

# Note: This is a mock of Django ORM patterns
# Actual Django imports would be: from django.db import models, transaction


class MockQuerySet:
    """Mock QuerySet for testing."""

    def select_for_update(self, nowait=False, skip_locked=False, of=()):
        """Mock select_for_update method."""
        return self


class MockManager:
    """Mock Manager for testing."""

    def select_for_update(self):
        """Mock select_for_update on manager."""
        return MockQuerySet()


# Mock models module
class models:
    Model = object
    Manager = MockManager


# Mock transaction module
class transaction:
    @staticmethod
    def atomic(using=None, savepoint=True, durable=False):
        """Mock atomic context manager."""

        def decorator(func):
            return func

        return decorator if callable(using) else decorator


def function_with_select_for_update():
    """Function with select_for_update."""
    qs = MockQuerySet()
    qs.select_for_update()


def function_with_select_for_update_nowait():
    """Function with select_for_update(nowait=True)."""
    qs = MockQuerySet()
    qs.select_for_update(nowait=True)


def function_with_select_for_update_skip_locked():
    """Function with select_for_update(skip_locked=True)."""
    qs = MockQuerySet()
    qs.select_for_update(skip_locked=True)


def function_with_select_for_update_timeout():
    """Function with select_for_update with timeout."""
    qs = MockQuerySet()
    # Some databases support timeout parameter
    qs.select_for_update()


class ModelWithLocking:
    """Mock model with locking operations."""

    objects = MockManager()

    @classmethod
    def get_with_lock(cls, pk):
        """Get object with lock."""
        return cls.objects.select_for_update().get(pk=pk)


def function_with_transaction_atomic():
    """Function with transaction.atomic."""

    @transaction.atomic
    def inner():
        pass

    inner()


def function_with_atomic_context():
    """Function using atomic as context manager."""
    with transaction.atomic():
        pass


class ClassWithDatabaseLocking:
    """Class with database locking operations."""

    def method_with_select_for_update(self):
        """Method with select_for_update."""
        qs = MockQuerySet()
        return qs.select_for_update()

    def method_with_atomic(self):
        """Method with atomic decorator."""

        @transaction.atomic
        def update_records():
            pass

        update_records()


def select_for_update_in_if():
    """select_for_update inside if block."""
    if True:
        qs = MockQuerySet()
        qs.select_for_update()


def select_for_update_in_try():
    """select_for_update inside try block."""
    try:
        qs = MockQuerySet()
        qs.select_for_update()
    except Exception:
        pass
