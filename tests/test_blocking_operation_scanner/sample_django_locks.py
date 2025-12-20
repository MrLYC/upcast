"""Sample Django code with select_for_update."""


class User:
    """Mock User model."""

    objects = None


def lock_user_row():
    """Function that locks a database row."""
    # Basic select_for_update
    user = User.objects.filter(id=1).select_for_update().first()

    # With timeout
    user = User.objects.filter(active=True).select_for_update(timeout=30).all()

    # With no_wait
    user = User.objects.select_for_update(nowait=True).get(id=5)

    return user
