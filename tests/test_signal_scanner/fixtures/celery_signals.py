"""Celery signal patterns for testing."""

from celery.signals import (
    task_failure,
    task_postrun,
    task_prerun,
    task_retry,
    worker_ready,
    worker_shutdown,
)


# Task lifecycle signals with @connect decorator
@task_prerun.connect
def task_start(task_id, task, args, kwargs, **extra):
    """Handle task start."""
    print(f"Task starting: {task.name}")


@task_postrun.connect
def task_end(task_id, task, retval, **extra):
    """Handle task completion."""
    print(f"Task finished: {task.name}")


@task_failure.connect
def task_fail(task_id, exception, traceback, einfo, **extra):
    """Handle task failure."""
    print(f"Task failed: {exception}")


@task_retry.connect
def task_retry_handler(request, reason, **extra):
    """Handle task retry."""
    print(f"Task retrying: {reason}")


# Worker signals
@worker_ready.connect
def on_worker_start(**kwargs):
    """Handle worker startup."""
    print("Worker ready")


@worker_shutdown.connect
def on_worker_shutdown(**kwargs):
    """Handle worker shutdown."""
    print("Worker shutting down")


# .connect() method pattern
def generic_task_handler(sender, **kwargs):
    """Generic task handler."""
    print("Task event occurred")


# Connect using method call
task_prerun.connect(generic_task_handler)


# Class-based handlers
class TaskMonitor:
    """Monitor task execution."""

    @task_prerun.connect
    def log_task_start(self, task_id, task, **kwargs):
        """Log task start."""
        print(f"Monitoring task: {task.name}")
