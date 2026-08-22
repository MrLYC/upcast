"""Static scanner for queue construction and message/task queue operations."""

import re
import time
from pathlib import Path
from typing import Any, ClassVar

from astroid import nodes

from upcast.common.ast_utils import get_import_info, safe_as_string
from upcast.common.file_utils import get_relative_path_str
from upcast.common.inference import infer_value
from upcast.common.scanner_base import BaseScanner
from upcast.models.queue_usage import QueueParameter, QueueUsage, QueueUsageOutput, QueueUsageSummary

Binding = tuple[str, str]


class QueueUsageScanner(BaseScanner[QueueUsageOutput]):
    """Detect supported queue APIs without importing application dependencies."""

    CATEGORIES: ClassVar[tuple[str, ...]] = ("in_process", "task_queue", "redis", "kafka", "rabbitmq")

    CONSTRUCTORS: ClassVar[dict[str, Binding]] = {
        # In-process queues
        "queue.Queue": ("in_process", "queue"),
        "queue.LifoQueue": ("in_process", "queue"),
        "queue.PriorityQueue": ("in_process", "queue"),
        "asyncio.Queue": ("in_process", "asyncio"),
        "asyncio.LifoQueue": ("in_process", "asyncio"),
        "asyncio.PriorityQueue": ("in_process", "asyncio"),
        "multiprocessing.Queue": ("in_process", "multiprocessing"),
        "multiprocessing.JoinableQueue": ("in_process", "multiprocessing"),
        "multiprocessing.SimpleQueue": ("in_process", "multiprocessing"),
        # Task queues
        "celery.Celery": ("task_queue", "celery"),
        "rq.Queue": ("task_queue", "rq"),
        "huey.Huey": ("task_queue", "huey"),
        "dramatiq.Actor": ("task_queue", "dramatiq"),
        # Redis clients and queue-like data structures
        "redis.Redis": ("redis", "redis"),
        "redis.StrictRedis": ("redis", "redis"),
        "redis.asyncio.Redis": ("redis", "redis"),
        "redis.asyncio.StrictRedis": ("redis", "redis"),
        # Kafka clients
        "kafka.KafkaProducer": ("kafka", "kafka-python"),
        "kafka.KafkaConsumer": ("kafka", "kafka-python"),
        "confluent_kafka.Producer": ("kafka", "confluent-kafka"),
        "confluent_kafka.Consumer": ("kafka", "confluent-kafka"),
        # RabbitMQ/Kombu clients and declarations
        "pika.BlockingConnection": ("rabbitmq", "pika"),
        "pika.ConnectionParameters": ("rabbitmq", "pika"),
        "pika.SelectConnection": ("rabbitmq", "pika"),
        "kombu.Connection": ("rabbitmq", "kombu"),
        "kombu.Queue": ("rabbitmq", "kombu"),
        "kombu.Exchange": ("rabbitmq", "kombu"),
        "kombu.Producer": ("rabbitmq", "kombu"),
    }

    CONSTRUCTOR_PARAMETER_NAMES: ClassVar[dict[str, tuple[str, ...]]] = {
        "queue.Queue": ("maxsize",),
        "queue.LifoQueue": ("maxsize",),
        "queue.PriorityQueue": ("maxsize",),
        "asyncio.Queue": ("maxsize",),
        "asyncio.LifoQueue": ("maxsize",),
        "asyncio.PriorityQueue": ("maxsize",),
        "multiprocessing.Queue": ("maxsize",),
        "multiprocessing.JoinableQueue": ("maxsize",),
        "multiprocessing.SimpleQueue": (),
        "celery.Celery": ("name", "broker", "backend"),
        "rq.Queue": ("name", "connection", "default_timeout"),
        "huey.Huey": ("name", "url", "blocking", "connection_pool"),
        "pika.ConnectionParameters": ("host", "port", "virtual_host", "credentials"),
        "kombu.Connection": ("hostname", "userid", "password", "virtual_host"),
        "kombu.Queue": ("name", "exchange", "routing_key", "queue_arguments"),
        "kombu.Exchange": ("name", "type", "durable", "auto_delete"),
    }

    METHOD_PARAMETER_NAMES: ClassVar[dict[str, tuple[str, ...]]] = {
        "put": ("item", "block", "timeout"),
        "put_nowait": ("item",),
        "get": ("block", "timeout"),
        "get_nowait": (),
        "send_task": ("task_name", "args", "kwargs"),
        "apply_async": ("args", "kwargs"),
        "delay": ("args",),
        "enqueue": ("func",),
        "enqueue_at": ("enqueue_at", "func"),
        "enqueue_in": ("time_delta", "func"),
        "send": ("topic", "key", "value", "partition"),
        "produce": ("topic", "value", "key"),
        "xadd": ("name", "fields"),
        "xread": ("streams", "count", "block"),
        "xreadgroup": ("groupname", "consumername", "streams", "count", "block"),
        "queue_declare": ("queue", "passive", "durable", "exclusive", "auto_delete", "arguments"),
        "exchange_declare": ("exchange", "exchange_type", "passive", "durable", "auto_delete", "arguments"),
        "basic_publish": ("exchange", "routing_key", "body", "properties", "mandatory"),
        "basic_get": ("queue", "auto_ack"),
        "basic_consume": ("queue", "on_message_callback", "auto_ack"),
        "basic_qos": ("prefetch_size", "prefetch_count", "global"),
    }

    IN_PROCESS_METHODS: ClassVar[set[str]] = {
        "put",
        "put_nowait",
        "get",
        "get_nowait",
        "task_done",
        "join",
        "empty",
        "full",
        "qsize",
    }
    TASK_METHODS: ClassVar[dict[str, set[str]]] = {
        "celery": {"send_task", "delay", "apply_async", "retry", "add_periodic_task", "send"},
        "rq": {"enqueue", "enqueue_at", "enqueue_in", "enqueue_call", "fetch_job", "count"},
        "dramatiq": {"send", "send_with_options"},
        "huey": {"enqueue", "schedule", "dequeue"},
    }
    REDIS_METHODS: ClassVar[dict[str, str]] = {
        "lpush": "publish",
        "rpush": "publish",
        "lpushx": "publish",
        "rpushx": "publish",
        "blpop": "consume",
        "brpop": "consume",
        "brpoplpush": "consume",
        "lpop": "consume",
        "rpop": "consume",
        "xadd": "publish",
        "xread": "consume",
        "xreadgroup": "consume",
        "xack": "ack",
        "xgroup_create": "configure",
        "xgroup_set_id": "configure",
        "llen": "inspect",
        "xlen": "inspect",
    }
    KAFKA_METHODS: ClassVar[dict[str, str]] = {
        "send": "publish",
        "produce": "publish",
        "poll": "consume",
        "consume": "consume",
        "subscribe": "configure",
        "assign": "configure",
        "commit": "ack",
    }
    RABBIT_METHODS: ClassVar[dict[str, str]] = {
        "queue_declare": "configure",
        "exchange_declare": "configure",
        "queue_bind": "configure",
        "exchange_bind": "configure",
        "basic_qos": "configure",
        "basic_publish": "publish",
        "publish": "publish",
        "basic_get": "consume",
        "basic_consume": "consume",
        "consume": "consume",
        "basic_ack": "ack",
        "ack": "ack",
        "basic_nack": "reject",
        "reject": "reject",
    }
    DECORATORS: ClassVar[dict[str, Binding]] = {
        "celery.shared_task": ("task_queue", "celery"),
        "celery.task": ("task_queue", "celery"),
        "dramatiq.actor": ("task_queue", "dramatiq"),
        "huey.task": ("task_queue", "huey"),
    }
    SENSITIVE_NAME_PARTS: ClassVar[tuple[str, ...]] = (
        "password",
        "passwd",
        "secret",
        "token",
        "credential",
        "api_key",
        "access_key",
        "private_key",
    )
    URL_USERINFO_RE: ClassVar[re.Pattern[str]] = re.compile(r"(://[^/\s:@]+:)[^/\s@]+(@)")

    def scan(self, path: Path) -> QueueUsageOutput:
        """Scan Python files for queue construction and operations."""
        start_time = time.perf_counter()
        files = self.get_files_to_scan(path)
        base_path = path if path.is_dir() else path.parent
        findings: list[QueueUsage] = []

        for file_path in files:
            module = self.parse_file(file_path)
            if module is None:
                continue
            findings.extend(self._scan_module(module, get_relative_path_str(file_path, base_path)))

        findings.sort(
            key=lambda item: (item.file, item.line, item.column, item.category, item.framework, item.operation)
        )
        results: dict[str, list[QueueUsage]] = {category: [] for category in self.CATEGORIES}
        for finding in findings:
            results[finding.category].append(finding)

        by_category = {category: len(results[category]) for category in self.CATEGORIES if results[category]}
        by_framework: dict[str, int] = {}
        hardcoded_parameters = dynamic_parameters = unknown_parameters = 0
        for finding in findings:
            by_framework[finding.framework] = by_framework.get(finding.framework, 0) + 1
            for parameter in finding.parameters:
                if parameter.hardcoded is True:
                    hardcoded_parameters += 1
                elif parameter.hardcoded is False:
                    dynamic_parameters += 1
                else:
                    unknown_parameters += 1

        duration_ms = int((time.perf_counter() - start_time) * 1000)
        summary = QueueUsageSummary(
            total_count=len(findings),
            total_usages=len(findings),
            files_scanned=len(files),
            scan_duration_ms=duration_ms,
            by_category=by_category,
            by_framework=dict(sorted(by_framework.items())),
            hardcoded_parameters=hardcoded_parameters,
            dynamic_parameters=dynamic_parameters,
            unknown_parameters=unknown_parameters,
        )
        return QueueUsageOutput(
            summary=summary,
            results=results,
            metadata={"scanner_name": "queue-usage", "static_analysis": True},
        )

    def _scan_module(self, module: nodes.Module, rel_path: str) -> list[QueueUsage]:
        imports = get_import_info(module)
        bindings = self._collect_bindings(module, imports)
        bindings.update(self._collect_decorated_bindings(module, imports, bindings))
        findings: list[QueueUsage] = []

        for node in module.nodes_of_class(nodes.Call):
            finding = self._finding_from_call(node, rel_path, imports, bindings)
            if finding is not None:
                findings.append(finding)

        for function in module.nodes_of_class((nodes.FunctionDef, nodes.AsyncFunctionDef)):
            findings.extend(self._findings_from_decorators(function, rel_path, imports, bindings))

        return findings

    def _collect_decorated_bindings(
        self,
        module: nodes.Module,
        imports: dict[str, str],
        bindings: dict[str, Binding],
    ) -> dict[str, Binding]:
        decorated_bindings: dict[str, Binding] = {}
        for function in module.nodes_of_class((nodes.FunctionDef, nodes.AsyncFunctionDef)):
            if function.decorators is None:
                continue
            for decorator in function.decorators.nodes:
                binding = self._decorator_binding(decorator, imports, bindings)
                if binding is not None:
                    decorated_bindings[function.name] = binding
                    break
        return decorated_bindings

    def _collect_bindings(self, module: nodes.Module, imports: dict[str, str]) -> dict[str, Binding]:
        bindings: dict[str, Binding] = {}
        assignments = list(module.nodes_of_class((nodes.Assign, nodes.AnnAssign)))

        # A few passes resolve ordinary constructor assignments and one-hop
        # objects such as ``channel = connection.channel()``.
        for _ in range(3):
            changed = False
            for assignment in assignments:
                value = assignment.value
                if not isinstance(value, nodes.Call):
                    continue
                binding = self._binding_from_call(value, imports, bindings)
                if binding is None:
                    continue
                for target in self._assignment_names(assignment):
                    if bindings.get(target) != binding:
                        bindings[target] = binding
                        changed = True
            if not changed:
                break
        return bindings

    @staticmethod
    def _assignment_names(assignment: nodes.Assign | nodes.AnnAssign) -> list[str]:
        targets: list[nodes.NodeNG] = (
            assignment.targets if isinstance(assignment, nodes.Assign) else [assignment.target]
        )
        return [target.name for target in targets if isinstance(target, nodes.AssignName)]

    def _binding_from_call(
        self,
        call: nodes.Call,
        imports: dict[str, str],
        bindings: dict[str, Binding],
    ) -> Binding | None:
        qualified_name = self._qualified_name(call.func, imports)
        if qualified_name in self.CONSTRUCTORS:
            return self.CONSTRUCTORS[qualified_name]

        if not isinstance(call.func, nodes.Attribute):
            return None
        receiver = self._binding_for_expr(call.func.expr, imports, bindings)
        if receiver is None:
            return None
        category, framework = receiver
        if category == "rabbitmq" and call.func.attrname == "channel":
            return receiver
        if framework in self.TASK_METHODS and call.func.attrname in self.TASK_METHODS[framework]:
            return receiver
        if category == "redis" and call.func.attrname in self.REDIS_METHODS:
            return receiver
        if category == "kafka" and call.func.attrname in self.KAFKA_METHODS:
            return receiver
        if category == "rabbitmq" and call.func.attrname in self.RABBIT_METHODS:
            return receiver
        if category == "in_process" and call.func.attrname in self.IN_PROCESS_METHODS:
            return receiver
        return None

    def _finding_from_call(
        self,
        call: nodes.Call,
        rel_path: str,
        imports: dict[str, str],
        bindings: dict[str, Binding],
    ) -> QueueUsage | None:
        qualified_name = self._qualified_name(call.func, imports)
        constructor_binding = self.CONSTRUCTORS.get(qualified_name or "")
        if constructor_binding is not None:
            parameters = self._parameters(
                call,
                imports,
                self.CONSTRUCTOR_PARAMETER_NAMES.get(qualified_name or "", ()),
            )
            return self._make_finding(
                call,
                rel_path,
                constructor_binding,
                "construct",
                parameters,
            )

        if not isinstance(call.func, nodes.Attribute):
            return None
        receiver = self._binding_for_expr(call.func.expr, imports, bindings)
        if receiver is None:
            return None
        category, framework = receiver
        method = call.func.attrname
        operation = self._method_operation(category, framework, method)
        if operation is None:
            return None
        parameters = self._parameters(call, imports, self.METHOD_PARAMETER_NAMES.get(method, ()))
        return self._make_finding(call, rel_path, receiver, operation, parameters)

    def _findings_from_decorators(
        self,
        function: nodes.FunctionDef | nodes.AsyncFunctionDef,
        rel_path: str,
        imports: dict[str, str],
        bindings: dict[str, Binding],
    ) -> list[QueueUsage]:
        if function.decorators is None:
            return []
        findings: list[QueueUsage] = []
        for decorator in function.decorators.nodes:
            call = decorator if isinstance(decorator, nodes.Call) else None
            binding = self._decorator_binding(decorator, imports, bindings)
            if binding is None:
                continue
            if call is None:
                parameters: list[QueueParameter] = []
                line = decorator.lineno
                column = decorator.col_offset
                statement = safe_as_string(decorator)
            else:
                parameters = self._parameters(call, imports, ())
                line = call.lineno
                column = call.col_offset
                statement = self._redact_statement(safe_as_string(call))
            findings.append(
                self._make_finding_from_location(
                    function,
                    rel_path,
                    binding,
                    "register",
                    parameters,
                    line=line,
                    column=column,
                    statement=statement,
                )
            )
        return findings

    def _decorator_binding(
        self,
        decorator: nodes.NodeNG,
        imports: dict[str, str],
        bindings: dict[str, Binding],
    ) -> Binding | None:
        target = decorator.func if isinstance(decorator, nodes.Call) else decorator
        qualified_name = self._qualified_name(target, imports)
        binding = self.DECORATORS.get(qualified_name or "")
        if binding is not None:
            return binding
        if not isinstance(target, nodes.Attribute) or target.attrname not in {"task", "actor", "shared_task"}:
            return None
        receiver = self._binding_for_expr(target.expr, imports, bindings)
        return receiver if receiver is not None and receiver[0] == "task_queue" else None

    def _method_operation(self, category: str, framework: str, method: str) -> str | None:
        if category == "in_process":
            if method in self.IN_PROCESS_METHODS:
                return method
            return None
        if category == "task_queue":
            if method in self.TASK_METHODS.get(framework, set()):
                return method
            return None
        if category == "redis":
            return method if method in self.REDIS_METHODS else None
        if category == "kafka":
            return method if method in self.KAFKA_METHODS else None
        if category == "rabbitmq":
            return method if method in self.RABBIT_METHODS else None
        return None

    def _parameters(
        self,
        call: nodes.Call,
        imports: dict[str, str],
        positional_names: tuple[str, ...],
    ) -> list[QueueParameter]:
        parameters: list[QueueParameter] = []
        for index, argument in enumerate(call.args):
            name = positional_names[index] if index < len(positional_names) else f"arg{index}"
            parameters.append(self._parameter(name, argument, imports))
        for keyword in call.keywords:
            name = keyword.arg if keyword.arg is not None else "**kwargs"
            parameters.append(self._parameter(name, keyword.value, imports))
        return parameters

    def _parameter(self, name: str, expression_node: nodes.NodeNG, imports: dict[str, str]) -> QueueParameter:
        expression = safe_as_string(expression_node)
        inferred = infer_value(expression_node)
        sensitive = self._is_sensitive(name, inferred.value)
        if inferred.confidence == "exact":
            value = "<redacted>" if sensitive else inferred.value
            source_kind = "literal" if isinstance(expression_node, nodes.Const) else "static_constant"
            hardcoded: bool | None = True
        elif self._is_known_dynamic(expression_node, imports):
            value = None
            source_kind = "runtime"
            hardcoded = False
        elif self._looks_like_configuration(expression_node):
            value = None
            source_kind = "configuration"
            hardcoded = False
        elif isinstance(expression_node, (nodes.BinOp, nodes.JoinedStr, nodes.Call)):
            value = None
            source_kind = "expression"
            hardcoded = None
        else:
            value = None
            source_kind = "unknown"
            hardcoded = None

        expression = "<redacted>" if sensitive else self._redact_url(expression)
        return QueueParameter(
            name=name,
            expression=expression,
            value=value,
            source_kind=source_kind,
            hardcoded=hardcoded,
        )

    def _make_finding(
        self,
        node: nodes.NodeNG,
        rel_path: str,
        binding: Binding,
        operation: str,
        parameters: list[QueueParameter],
    ) -> QueueUsage:
        return self._make_finding_from_location(
            node,
            rel_path,
            binding,
            operation,
            parameters,
            line=node.lineno,
            column=node.col_offset,
            statement=self._redact_statement(safe_as_string(node)),
        )

    def _make_finding_from_location(
        self,
        node: nodes.NodeNG,
        rel_path: str,
        binding: Binding,
        operation: str,
        parameters: list[QueueParameter],
        *,
        line: int,
        column: int,
        statement: str,
    ) -> QueueUsage:
        function, class_name = self._context(node)
        return QueueUsage(
            category=binding[0],
            framework=binding[1],
            operation=operation,
            file=rel_path,
            line=line,
            column=column,
            statement=statement or None,
            function=function,
            class_name=class_name,
            parameters=parameters,
            hardcoding_status=self._hardcoding_status(parameters),
        )

    @staticmethod
    def _hardcoding_status(parameters: list[QueueParameter]) -> str:
        statuses = [parameter.hardcoded for parameter in parameters]
        if not statuses:
            return "unknown"
        if all(status is True for status in statuses):
            return "fully_hardcoded"
        if all(status is False for status in statuses):
            return "dynamic"
        if all(status is None for status in statuses):
            return "unknown"
        return "partially_hardcoded"

    def _binding_for_expr(
        self,
        expression: nodes.NodeNG,
        imports: dict[str, str],
        bindings: dict[str, Binding],
    ) -> Binding | None:
        if isinstance(expression, nodes.Name):
            return bindings.get(expression.name)
        if isinstance(expression, nodes.Attribute):
            return bindings.get(expression.attrname) or self._binding_for_expr(expression.expr, imports, bindings)
        return None

    def _qualified_name(self, node: nodes.NodeNG, imports: dict[str, str]) -> str | None:
        if isinstance(node, nodes.Name):
            return imports.get(node.name, node.name)
        if isinstance(node, nodes.Attribute):
            prefix = self._qualified_name(node.expr, imports)
            return f"{prefix}.{node.attrname}" if prefix else node.attrname
        return None

    def _is_known_dynamic(self, node: nodes.NodeNG, imports: dict[str, str]) -> bool:
        if not isinstance(node, nodes.Call):
            return False
        qualified_name = self._qualified_name(node.func, imports) or ""
        return qualified_name in {
            "os.getenv",
            "os.environ.get",
            "os.environ.setdefault",
            "environ.get",
            "getenv",
        }

    @staticmethod
    def _looks_like_configuration(node: nodes.NodeNG) -> bool:
        if isinstance(node, nodes.Attribute):
            return True
        if isinstance(node, nodes.Subscript):
            return True
        return isinstance(node, nodes.Name) and node.name.lower() in {
            "settings",
            "config",
            "configuration",
            "options",
        }

    def _is_sensitive(self, name: str, value: Any) -> bool:
        lowered = name.lower()
        if any(part in lowered for part in self.SENSITIVE_NAME_PARTS):
            return True
        return isinstance(value, str) and self.URL_USERINFO_RE.search(value) is not None

    def _redact_url(self, text: str) -> str:
        return self.URL_USERINFO_RE.sub(r"\1<redacted>\2", text)

    def _redact_statement(self, statement: str) -> str:
        if not statement:
            return statement
        redacted = re.sub(
            r"(?i)(password|passwd|secret|token|credential|api_key|access_key|private_key)\s*=\s*(['\"]).*?\2",
            r"\1=<redacted>",
            statement,
        )
        return self._redact_url(redacted)

    @staticmethod
    def _context(node: nodes.NodeNG) -> tuple[str | None, str | None]:
        function: str | None = None
        class_name: str | None = None
        current = node.parent
        while current is not None:
            if function is None and isinstance(current, (nodes.FunctionDef, nodes.AsyncFunctionDef)):
                function = current.name
            if class_name is None and isinstance(current, nodes.ClassDef):
                class_name = current.name
            if function is not None and class_name is not None:
                break
            current = current.parent
        return function, class_name
