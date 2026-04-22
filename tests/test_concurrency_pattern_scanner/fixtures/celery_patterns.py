"""Test fixtures for Celery concurrency patterns."""

from celery import Celery, shared_task


app = Celery("demo")


@shared_task(name="send-email")
def send_email(user_id: int):
    """Celery task declared with shared_task."""
    return user_id


@app.task(bind=True, autoretry_for=(Exception,))
def rebuild_index(self, index_name: str):
    """Celery task declared on an app instance."""
    return index_name


def trigger_background_jobs():
    """Invoke Celery tasks using common task APIs."""
    send_email.delay(1)
    rebuild_index.apply_async(args=("products",), countdown=5)
