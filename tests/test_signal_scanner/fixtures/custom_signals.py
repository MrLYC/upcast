"""Custom Django signal definitions for testing."""

from django.dispatch import Signal, receiver

# Custom signals
order_paid = Signal()
payment_failed = Signal()
shipment_dispatched = Signal()

# Unused custom signal
user_deactivated = Signal()


# Handler for custom signal
@receiver(order_paid)
def process_payment(sender, order, user, **kwargs):
    """Process completed payment."""
    print(f"Processing payment for order {order.id}")


@receiver(payment_failed)
def handle_payment_failure(sender, order, error, **kwargs):
    """Handle payment failure."""
    print(f"Payment failed for order {order.id}: {error}")


# Connect using method
def dispatch_shipment(sender, order, **kwargs):
    """Handle shipment dispatch."""
    print(f"Dispatching order {order.id}")


shipment_dispatched.connect(dispatch_shipment)
