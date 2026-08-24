"""Integration tests for queue usage AST scanning."""

from pathlib import Path

import pytest


def _scanner():
    try:
        from upcast.scanners.queue_usage import QueueUsageScanner
    except ModuleNotFoundError as exc:
        pytest.fail(f"queue usage scanner is missing: {exc}")
    return QueueUsageScanner


def _parameter(usage, name):
    return next(parameter for parameter in usage.parameters if parameter.name == name)


def test_scans_in_process_queues_and_parameters(tmp_path: Path):
    source = tmp_path / "queues.py"
    source.write_text(
        """
from queue import Queue
import asyncio
from multiprocessing import Queue as ProcessQueue

fixed = Queue(maxsize=10)
fixed.put("item", block=False, timeout=2)
async_queue = asyncio.PriorityQueue(maxsize=20)
process_queue = ProcessQueue(5)
""",
        encoding="utf-8",
    )

    output = _scanner()().scan(tmp_path)
    findings = output.results["in_process"]

    assert {finding.framework for finding in findings} == {"queue", "asyncio", "multiprocessing"}
    put = next(finding for finding in findings if finding.operation == "put")
    assert _parameter(put, "block").value is False
    assert _parameter(put, "block").hardcoded is True
    assert _parameter(put, "timeout").value == 2
    assert _parameter(put, "timeout").hardcoded is True
    assert output.summary.by_category["in_process"] == len(findings)


def test_scans_task_queue_redis_kafka_and_rabbitmq_parameters(tmp_path: Path):
    source = tmp_path / "messaging.py"
    source.write_text(
        """
import redis
import pika
from celery import Celery
from rq import Queue as RQQueue
from kafka import KafkaProducer

app = Celery("worker")
rq = RQQueue("jobs", connection=redis.Redis(host="localhost"), default_timeout=300)
app.send_task("tasks.run", queue="fixed", routing_key=settings.ROUTING_KEY, countdown=30)
producer = KafkaProducer(bootstrap_servers=["broker:9092"], acks="all", retries=3)
producer.send("events", key=b"fixed", value=payload, partition=0)
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue="fixed", durable=True)
channel.basic_publish(exchange="events", routing_key=settings.ROUTE, body=payload)
""",
        encoding="utf-8",
    )

    output = _scanner()().scan(tmp_path)

    assert output.results["task_queue"]
    assert {finding.framework for finding in output.results["task_queue"]} >= {"celery", "rq"}
    celery = next(
        finding
        for finding in output.results["task_queue"]
        if finding.framework == "celery" and finding.operation == "send_task"
    )
    assert _parameter(celery, "queue").value == "fixed"
    assert _parameter(celery, "queue").hardcoded is True
    assert _parameter(celery, "routing_key").hardcoded is False

    assert output.results["redis"]
    assert output.results["kafka"]
    assert output.results["rabbitmq"]
    assert output.summary.by_category["kafka"] >= 1
    assert output.summary.by_category["rabbitmq"] >= 1


def test_marks_dynamic_and_unknown_parameters_without_false_hardcoding(tmp_path: Path):
    source = tmp_path / "dynamic.py"
    source.write_text(
        """
import os
from queue import Queue

fixed_size = 10
fixed = Queue(fixed_size)
from_env = Queue(os.getenv("QUEUE_SIZE"))
from_config = Queue(settings.QUEUE_SIZE)
""",
        encoding="utf-8",
    )

    output = _scanner()().scan(tmp_path)
    constructors = [finding for finding in output.results["in_process"] if finding.operation == "construct"]

    fixed = next(finding for finding in constructors if _parameter(finding, "maxsize").value == 10)
    env = next(finding for finding in constructors if "os.getenv" in _parameter(finding, "maxsize").expression)
    config = next(
        finding for finding in constructors if "settings.QUEUE_SIZE" in _parameter(finding, "maxsize").expression
    )
    assert _parameter(fixed, "maxsize").hardcoded is True
    assert _parameter(env, "maxsize").hardcoded is False
    assert _parameter(config, "maxsize").hardcoded is False


def test_ignores_unrelated_same_name_queue(tmp_path: Path):
    source = tmp_path / "unrelated.py"
    source.write_text(
        """
class Queue:
    def __init__(self, name):
        self.name = name

queue = Queue("not-a-framework-queue")
""",
        encoding="utf-8",
    )

    output = _scanner()().scan(tmp_path)

    assert output.summary.total_usages == 0


def test_redacts_credential_bearing_parameter_values(tmp_path: Path):
    source = tmp_path / "secrets.py"
    source.write_text(
        """
from kafka import KafkaProducer

producer = KafkaProducer(sasl_password="super-secret", bootstrap_servers=["broker:9092"])
""",
        encoding="utf-8",
    )

    output = _scanner()().scan(tmp_path)
    password = next(
        parameter
        for finding in output.results["kafka"]
        for parameter in finding.parameters
        if parameter.name == "sasl_password"
    )

    assert "super-secret" not in (password.expression or "")
    assert password.value == "<redacted>"


def test_scans_additional_task_stream_and_kombu_apis(tmp_path: Path):
    source = tmp_path / "additional.py"
    source.write_text(
        """
import dramatiq
from huey import Huey
from redis import Redis
from confluent_kafka import Producer, Consumer
from kombu import Queue as KombuQueue

@dramatiq.actor(queue_name="critical")
def handle(message):
    return message

huey = Huey("tasks")
redis_client = Redis()
redis_client.xadd("events", {"kind": "created"}, maxlen=100)
producer = Producer({"bootstrap.servers": "broker:9092"})
producer.produce("events", value=payload, key="fixed")
consumer = Consumer({"group.id": "workers"})
consumer.subscribe(["events"])
consumer.poll(1.0)
kombu_queue = KombuQueue("jobs", routing_key="jobs")
""",
        encoding="utf-8",
    )

    output = _scanner()().scan(tmp_path)

    assert {finding.framework for finding in output.results["task_queue"]} >= {"dramatiq", "huey"}
    assert any(finding.operation == "xadd" for finding in output.results["redis"])
    assert {finding.framework for finding in output.results["kafka"]} >= {"confluent-kafka"}
    assert any(finding.framework == "kombu" for finding in output.results["rabbitmq"])


def test_scans_in_process_observation_and_kombu_ack_operations(tmp_path: Path):
    source = tmp_path / "operations.py"
    source.write_text(
        """
from queue import Queue
from kombu import Connection

local_queue = Queue()
local_queue.empty()
local_queue.full()
local_queue.get(block=False)

connection = Connection("memory://")
channel = connection.channel()
channel.basic_get("jobs")
channel.basic_ack(delivery_tag)
""",
        encoding="utf-8",
    )

    output = _scanner()().scan(tmp_path)

    in_process = output.results["in_process"]
    assert {finding.operation for finding in in_process} >= {"empty", "full", "get"}

    rabbitmq = output.results["rabbitmq"]
    assert {finding.operation for finding in rabbitmq} >= {"basic_get", "basic_ack"}


def test_marks_unresolved_expression_as_unknown(tmp_path: Path):
    source = tmp_path / "unknown.py"
    source.write_text(
        """
from queue import Queue

queue = Queue(make_queue_size())
""",
        encoding="utf-8",
    )

    output = _scanner()().scan(tmp_path)
    parameter = _parameter(output.results["in_process"][0], "maxsize")

    assert parameter.hardcoded is None
    assert parameter.source_kind == "expression"


def test_tracks_decorated_task_objects_when_they_are_sent(tmp_path: Path):
    source = tmp_path / "decorated_tasks.py"
    source.write_text(
        """
import dramatiq
from celery import Celery, shared_task

app = Celery("worker")

@shared_task
def celery_task(value):
    return value

@app.task(queue="critical")
def app_task(value):
    return value

@dramatiq.actor
def dramatiq_task(value):
    return value

celery_task.apply_async(queue="fixed", countdown=10)
app_task.delay(1)
dramatiq_task.send_with_options(queue_name="critical", delay=1000)
""",
        encoding="utf-8",
    )

    output = _scanner()().scan(tmp_path)
    task_findings = output.results["task_queue"]

    assert any(finding.framework == "celery" and finding.operation == "apply_async" for finding in task_findings)
    assert any(finding.framework == "celery" and finding.operation == "delay" for finding in task_findings)
    assert any(
        finding.framework == "celery"
        and finding.operation == "register"
        and any(parameter.name == "queue" for parameter in finding.parameters)
        for finding in task_findings
    )
    assert any(
        finding.framework == "dramatiq" and finding.operation == "send_with_options" for finding in task_findings
    )
