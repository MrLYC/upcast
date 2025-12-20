"""Mixed Django and Celery signal patterns for testing."""

from celery.signals import task_failure, task_postrun
from django.db.models.signals import post_save
from django.dispatch import receiver


class MixedSignalApp:
    """Application with both Django and Celery signals."""

    @receiver(post_save, sender="Order")
    def on_order_save(self, sender, instance, created, **kwargs):
        """Handle order save - Django signal."""
        if created:
            # Trigger async task
            from .tasks import process_order

            process_order.delay(instance.id)

    @task_postrun.connect
    def on_task_complete(self, task_id, task, retval, **extra):
        """Handle task completion - Celery signal."""
        print(f"Task {task.name} completed")

    @task_failure.connect
    def on_task_failure(self, task_id, exception, **extra):
        """Handle task failure - Celery signal."""
        print(f"Task failed: {exception}")


# Module-level handlers
@receiver(post_save, sender="User")
def sync_user_to_cache(sender, instance, **kwargs):
    """Sync user to cache - Django signal."""
    print(f"Syncing user {instance.id} to cache")


@task_postrun.connect
def log_task_metrics(task_id, task, **kwargs):
    """Log task metrics - Celery signal."""
    print(f"Logged metrics for {task.name}")


# Nested function as handler
def register_handlers():
    """Register signal handlers dynamically."""

    @receiver(post_save, sender="Product")
    def product_saved(sender, instance, **kwargs):
        """Handle product save."""
        print(f"Product {instance.name} saved")

    return product_saved
