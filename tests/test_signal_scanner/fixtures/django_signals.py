"""Django signal patterns for testing."""

from django.core.signals import request_finished, request_started
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver


# Single signal with @receiver
@receiver(post_save, sender="Order")
def order_created(sender, instance, created, **kwargs):
    """Handle order creation."""
    if created:
        print(f"Order {instance.id} created")


# Multiple signals with @receiver
@receiver([pre_delete, post_delete], sender="Product")
def product_deleted(sender, instance, **kwargs):
    """Handle product deletion."""
    print(f"Product {instance.name} deleted")


# Request signals
@receiver(request_started)
def on_request_start(sender, environ, **kwargs):
    """Log request start."""
    print("Request started")


@receiver(request_finished)
def on_request_finished(sender, **kwargs):
    """Log request finished."""
    print("Request finished")


# M2M changed signal
@receiver(m2m_changed, sender="Order.products.through")
def order_products_changed(sender, instance, action, **kwargs):
    """Handle order products change."""
    if action == "post_add":
        print(f"Products added to order {instance.id}")


# Class with signal handler methods
class SignalHandlers:
    """Container for signal handlers."""

    @receiver(pre_save, sender="User")
    def on_user_save(self, sender, instance, **kwargs):
        """Handle user pre-save."""
        print(f"Saving user {instance.username}")


# .connect() method pattern
def save_handler(sender, instance, created, **kwargs):
    """Generic save handler."""
    print("Model saved")


# Connect using method call
post_save.connect(save_handler, sender="Article")
