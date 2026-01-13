"""Redis usage scanner implementation."""

import re
import time
from collections import defaultdict
from pathlib import Path
from typing import ClassVar

from astroid import nodes

from upcast.common.ast_utils import get_import_info, safe_as_string
from upcast.common.file_utils import get_relative_path_str
from upcast.common.inference import infer_value
from upcast.common.scanner_base import BaseScanner
from upcast.models.redis_usage import (
    RedisConfig,
    RedisUsage,
    RedisUsageOutput,
    RedisUsageSummary,
    RedisUsageType,
)


class RedisUsageScanner(BaseScanner[RedisUsageOutput]):
    """Scanner for Redis usage patterns in Django projects."""

    # Configuration variable names to detect
    REDIS_CONFIG_VARS: ClassVar[dict[str, RedisUsageType]] = {
        "CACHES": RedisUsageType.CACHE_BACKEND,
        "SESSION_ENGINE": RedisUsageType.SESSION_STORAGE,
        "CELERY_BROKER_URL": RedisUsageType.CELERY_BROKER,
        "BROKER_URL": RedisUsageType.CELERY_BROKER,  # Legacy
        "CELERY_RESULT_BACKEND": RedisUsageType.CELERY_RESULT,
        "CHANNEL_LAYERS": RedisUsageType.CHANNELS,
        "REST_FRAMEWORK": RedisUsageType.RATE_LIMITING,
    }

    # Redis-related backend/engine identifiers
    REDIS_IDENTIFIERS: ClassVar[list[str]] = [
        "redis",
        "django_redis",
        "channels_redis",
    ]

    def scan(self, path: Path) -> RedisUsageOutput:
        """Scan for Redis usage patterns."""
        start_time = time.time()
        files = self.get_files_to_scan(path)
        base_path = path if path.is_dir() else path.parent

        usages_by_type: dict[str, list[RedisUsage]] = defaultdict(list)
        warnings: list[str] = []

        for file_path in files:
            module = self.parse_file(file_path)
            if not module:
                continue

            rel_path = get_relative_path_str(file_path, base_path)
            imports = get_import_info(module)

            # Check if this is a settings file
            if self._is_settings_file(file_path):
                config_usages = self._scan_settings_file(module, rel_path)
                for usage in config_usages:
                    usages_by_type[usage.type].append(usage)

            # Scan for Django cache API usage
            cache_usages, cache_warnings = self._scan_cache_api(module, rel_path, imports)
            for usage in cache_usages:
                usages_by_type[usage.type].append(usage)
            warnings.extend(cache_warnings)

            # Scan for direct redis-py usage
            redis_usages, redis_warnings = self._scan_direct_redis(module, rel_path, imports)
            for usage in redis_usages:
                usages_by_type[usage.type].append(usage)
            warnings.extend(redis_warnings)

        # Convert defaultdict to regular dict and filter empty lists
        results = {k: v for k, v in usages_by_type.items() if v}

        # Calculate summary
        scan_duration_ms = int((time.time() - start_time) * 1000)
        summary = self._calculate_summary(results, scan_duration_ms, warnings)

        return RedisUsageOutput(summary=summary, results=results, metadata={"scanner_name": "redis-usage"})

    def _is_settings_file(self, file_path: Path) -> bool:
        """Check if file is a Django settings file."""
        path_str = str(file_path)
        return (
            "/settings/" in path_str
            or "/config/" in path_str
            or file_path.name == "settings.py"
            or file_path.name.startswith("settings_")
            or file_path.name == "celery.py"
        )

    def _infer_key_pattern(self, node: nodes.NodeNG) -> str | None:
        """Infer Redis key pattern from an expression, using ... for dynamic parts."""
        try:
            # Handle f-strings first
            if isinstance(node, nodes.JoinedStr):
                return self._handle_fstring(node)

            const_value = infer_value(node).get_if_type(str)
            if const_value is not None:
                return const_value

            # If we can't infer the value, return ...
            if isinstance(node, nodes.Name):
                return "..."

            # Handle format calls
            if self._is_format_call(node):
                return self._handle_format_call(node)

            # Handle binary operations
            if isinstance(node, nodes.BinOp):
                return self._handle_binop(node)

            # Handle attribute access and function calls
            if isinstance(node, (nodes.Attribute, nodes.Call)):
                return "..."

        except Exception:  # noqa: S110
            # Fail silently and return None for unparseable patterns
            pass

        return None

    def _handle_fstring(self, node: nodes.JoinedStr) -> str:
        """Handle f-string pattern inference."""
        parts = []
        for value in node.values:
            if isinstance(value, nodes.Const):
                parts.append(str(value.value))
            else:
                # Dynamic parts (FormattedValue or other)
                parts.append("...")
        return "".join(parts)

    def _is_format_call(self, node: nodes.NodeNG) -> bool:
        """Check if node is a format() method call."""
        return (
            isinstance(node, nodes.Call)
            and isinstance(node.func, nodes.Attribute)
            and node.func.attrname == "format"
            and isinstance(node.func.expr, nodes.Const)
        )

    def _handle_format_call(self, node: nodes.Call) -> str:
        """Handle format() method call pattern inference."""
        template = str(node.func.expr.value)  # type: ignore[attr-defined]
        # Replace format placeholders with ...
        return re.sub(r"\{[^}]*\}", "...", template)

    def _handle_binop(self, node: nodes.BinOp) -> str | None:
        """Handle binary operation pattern inference."""
        if node.op == "+":
            left = self._infer_key_pattern(node.left)
            right = self._infer_key_pattern(node.right)
            if left and right:
                return left + right
        elif node.op == "%" and isinstance(node.left, nodes.Const):
            template = str(node.left.value)
            return re.sub(r"%[sdr]", "...", template)
        return None

    def _clean_key_pattern(self, key: str | None) -> str | None:
        """Clean up key pattern by replacing Uninferable with ...."""
        if key is None:
            return None
        # Replace any occurrence of "Uninferable" with "..."
        return re.sub(r"Uninferable", "...", key)

    def _scan_settings_file(self, module: nodes.Module, rel_path: str) -> list[RedisUsage]:
        """Scan settings file for Redis configurations."""
        usages = []

        for node in module.body:
            if not isinstance(node, nodes.Assign):
                continue

            for target in node.targets:
                if not isinstance(target, nodes.AssignName):
                    continue

                var_name = target.name
                if var_name not in self.REDIS_CONFIG_VARS:
                    continue

                extracted = self._extract_config_by_var_name(node, rel_path, var_name)
                usages.extend(extracted)

        return usages

    def _extract_config_by_var_name(self, node: nodes.Assign, rel_path: str, var_name: str) -> list[RedisUsage]:
        """Extract configuration based on variable name."""
        usage_type = self.REDIS_CONFIG_VARS[var_name]

        if var_name == "CACHES":
            return self._extract_caches_config(node, rel_path)
        elif var_name == "CHANNEL_LAYERS":
            return self._extract_channel_layers_config(node, rel_path)
        elif var_name in ("SESSION_ENGINE", "CELERY_BROKER_URL", "BROKER_URL", "CELERY_RESULT_BACKEND"):
            usage = self._extract_simple_config(node, rel_path, usage_type, var_name)
            return [usage] if usage else []
        elif var_name == "REST_FRAMEWORK":
            usage = self._extract_rest_framework_config(node, rel_path)
            return [usage] if usage else []
        return []

    def _extract_caches_config(self, node: nodes.Assign, rel_path: str) -> list[RedisUsage]:
        """Extract CACHES configuration."""
        usages: list[RedisUsage] = []
        value = node.value

        if not isinstance(value, nodes.Dict):
            return usages

        for key, val in value.items:
            if not isinstance(val, nodes.Dict):
                continue

            cache_alias = safe_as_string(key) if key else "default"
            config = self._parse_cache_config_dict(val)

            if config.backend:  # Only add if it's a Redis backend
                usage = RedisUsage(
                    type=RedisUsageType.CACHE_BACKEND,
                    file=rel_path,
                    line=node.lineno,
                    library="django_redis" if "django_redis" in config.backend.lower() else "redis",
                    config=config,
                    statement=f"CACHES['{cache_alias}'] = ...",
                )
                usages.append(usage)

        return usages

    def _parse_cache_config_dict(self, val: nodes.Dict) -> RedisConfig:
        """Parse cache configuration dictionary."""
        config = RedisConfig()

        for k, v in val.items:
            key_str = safe_as_string(k)
            if key_str == "BACKEND":
                backend = safe_as_string(v)
                if backend and any(rid in backend.lower() for rid in self.REDIS_IDENTIFIERS):
                    config.backend = backend
            elif key_str == "LOCATION":
                config.location = safe_as_string(v)
            elif key_str == "OPTIONS" and isinstance(v, nodes.Dict):
                for ok, ov in v.items:
                    opt_key = safe_as_string(ok)
                    if opt_key == "CLIENT_CLASS":
                        config.client_class = safe_as_string(ov)

        return config

    def _extract_simple_config(
        self, node: nodes.Assign, rel_path: str, usage_type: RedisUsageType, var_name: str
    ) -> RedisUsage | None:
        """Extract simple string configuration like CELERY_BROKER_URL."""
        value_str = safe_as_string(node.value)

        if not value_str or "redis" not in value_str.lower():
            return None

        config = RedisConfig(location=value_str)

        # Try to parse redis:// URL
        match = re.match(r"redis://([^:]+):(\d+)/(\d+)", value_str)
        if match:
            config.host = match.group(1)
            config.port = int(match.group(2))
            config.db = int(match.group(3))

        return RedisUsage(
            type=usage_type,
            file=rel_path,
            line=node.lineno,
            library="redis",
            config=config,
            statement=f"{var_name} = {value_str!r}",
        )

    def _extract_channel_layers_config(self, node: nodes.Assign, rel_path: str) -> list[RedisUsage]:
        """Extract CHANNEL_LAYERS configuration."""
        usages: list[RedisUsage] = []
        value = node.value

        if not isinstance(value, nodes.Dict):
            return usages

        for _key, val in value.items:
            if not isinstance(val, nodes.Dict):
                continue

            config = self._parse_channel_layer_config_dict(val)

            if config.backend:
                usage = RedisUsage(
                    type=RedisUsageType.CHANNELS,
                    file=rel_path,
                    line=node.lineno,
                    library="channels_redis",
                    config=config,
                    statement="CHANNEL_LAYERS = ...",
                )
                usages.append(usage)

        return usages

    def _parse_channel_layer_config_dict(self, val: nodes.Dict) -> RedisConfig:
        """Parse channel layer configuration dictionary."""
        config = RedisConfig()

        for k, v in val.items:
            key_str = safe_as_string(k)
            if key_str == "BACKEND":
                backend = safe_as_string(v)
                if backend and "redis" in backend.lower():
                    config.backend = backend
            elif key_str == "CONFIG" and isinstance(v, nodes.Dict):
                self._extract_channel_layer_hosts(v, config)

        return config

    def _extract_channel_layer_hosts(self, config_dict: nodes.Dict, config: RedisConfig) -> None:
        """Extract hosts configuration from channel layer CONFIG."""
        for ck, cv in config_dict.items:
            if safe_as_string(ck) == "hosts" and isinstance(cv, nodes.List) and cv.elts:
                first_host = cv.elts[0]
                if isinstance(first_host, (nodes.Tuple, nodes.List)) and len(first_host.elts) >= 2:
                    config.host = safe_as_string(first_host.elts[0])
                    port = infer_value(first_host.elts[1]).get_if_type(int)
                    if port is not None:
                        config.port = port

    def _extract_rest_framework_config(self, node: nodes.Assign, rel_path: str) -> RedisUsage | None:
        """Extract REST_FRAMEWORK throttling configuration."""
        value = node.value

        if not isinstance(value, nodes.Dict):
            return None

        has_throttle = False
        throttle_classes = []
        throttle_rates = {}

        for k, v in value.items:
            key_str = safe_as_string(k)
            if key_str == "DEFAULT_THROTTLE_CLASSES" and isinstance(v, nodes.List):
                has_throttle = True
                for item in v.elts:
                    throttle_classes.append(safe_as_string(item))
            elif key_str == "DEFAULT_THROTTLE_RATES" and isinstance(v, nodes.Dict):
                for rk, rv in v.items:
                    rate_key = safe_as_string(rk)
                    rate_val = safe_as_string(rv)
                    if rate_key and rate_val:
                        throttle_rates[rate_key] = rate_val

        if has_throttle:
            config = RedisConfig(
                options={
                    "throttle_classes": throttle_classes,
                    "throttle_rates": throttle_rates,
                }
            )
            return RedisUsage(
                type=RedisUsageType.RATE_LIMITING,
                file=rel_path,
                line=node.lineno,
                library="rest_framework",
                config=config,
                statement="REST_FRAMEWORK throttling configured",
            )

        return None

    def _scan_cache_api(
        self, module: nodes.Module, rel_path: str, imports: dict[str, str]
    ) -> tuple[list[RedisUsage], list[str]]:
        """Scan for Django cache API usage."""
        usages: list[RedisUsage] = []
        warnings: list[str] = []

        # Check if cache is imported
        cache_imported = "cache" in imports or any("cache" in imp for imp in imports.values())

        if not cache_imported:
            return usages, warnings

        for node in module.nodes_of_class(nodes.Call):
            func = node.func
            if not isinstance(func, nodes.Attribute):
                continue

            # Check for cache.* calls
            if isinstance(func.expr, nodes.Name) and func.expr.name == "cache":
                method = func.attrname
                usage = self._parse_cache_call(node, rel_path, method)
                if usage:
                    usages.append(usage)
                    if usage.warning:
                        warnings.append(f"{usage.warning} in {rel_path}:{node.lineno}")

        return usages, warnings

    def _parse_cache_call(self, node: nodes.Call, rel_path: str, method: str) -> RedisUsage | None:
        """Parse a cache API call."""
        # Determine operation type
        if method == "lock":
            return self._parse_lock_call(node, rel_path)
        elif method in ("get", "set", "delete", "incr", "decr", "get_or_set"):
            return self._parse_basic_cache_call(node, rel_path, method)

        return None

    def _parse_lock_call(self, node: nodes.Call, rel_path: str) -> RedisUsage:
        """Parse cache.lock() call."""
        timeout = None
        key = None

        if node.args:
            key = self._clean_key_pattern(self._infer_key_pattern(node.args[0]))

        for keyword in node.keywords:
            if keyword.arg == "timeout":
                timeout = infer_value(keyword.value).get_if_type((int, float))
                if timeout is not None:
                    timeout = int(timeout)

        return RedisUsage(
            type=RedisUsageType.DISTRIBUTED_LOCK,
            file=rel_path,
            line=node.lineno,
            library="django_redis",
            operation="lock",
            key=key,
            statement=safe_as_string(node),
            timeout=timeout,
            pattern="cache_lock",
        )

    def _parse_basic_cache_call(self, node: nodes.Call, rel_path: str, method: str) -> RedisUsage:
        """Parse basic cache operation (get, set, etc.)."""
        has_ttl = False
        timeout = None
        warning = None
        key = None

        # Extract key (first argument)
        if node.args:
            key = self._clean_key_pattern(self._infer_key_pattern(node.args[0]))

        if method == "set":
            if len(node.args) >= 3:
                timeout_val = infer_value(node.args[2]).get_if_type((int, float))
                if timeout_val is not None:
                    timeout = int(timeout_val)
                    has_ttl = True

            for keyword in node.keywords:
                if keyword.arg in ("timeout", "ttl"):
                    timeout_val = infer_value(keyword.value).get_if_type((int, float))
                    if timeout_val is not None:
                        timeout = int(timeout_val)
                        has_ttl = True

            if not has_ttl:
                warning = "No TTL specified for cache.set"

        return RedisUsage(
            type=RedisUsageType.DIRECT_CLIENT,
            file=rel_path,
            line=node.lineno,
            library="django_redis",
            operation=method,
            key=key,
            statement=safe_as_string(node),
            has_ttl=has_ttl if method == "set" else None,
            timeout=timeout,
            warning=warning,
        )

    def _scan_direct_redis(
        self, module: nodes.Module, rel_path: str, imports: dict[str, str]
    ) -> tuple[list[RedisUsage], list[str]]:
        """Scan for direct redis-py usage."""
        usages: list[RedisUsage] = []
        warnings: list[str] = []

        # Check if redis is imported
        redis_imported = "redis" in imports or any("redis" in imp.lower() for imp in imports.values())

        if not redis_imported:
            return usages, warnings

        # Track Redis client instances and pipeline instances
        redis_vars, pipeline_vars = self._collect_redis_variables(module)

        # Scan for Redis operations
        for node in module.nodes_of_class(nodes.Call):
            func = node.func
            if isinstance(func, nodes.Attribute) and isinstance(func.expr, nodes.Name):
                is_pipeline = func.expr.name in pipeline_vars
                is_redis_client = func.expr.name in redis_vars

                if is_redis_client or is_pipeline:
                    usage = self._parse_redis_operation(node, rel_path, func.attrname, is_pipeline=is_pipeline)
                    if usage:
                        usages.append(usage)
                        if usage.warning:
                            warnings.append(f"{usage.warning} in {rel_path}:{node.lineno}")

        return usages, warnings

    def _collect_redis_variables(self, module: nodes.Module) -> tuple[set[str], set[str]]:
        """Collect Redis client and pipeline variable names."""
        redis_vars = set()
        pipeline_vars = set()

        for node in module.nodes_of_class(nodes.Call):
            func = node.func

            # Find Redis() instantiation
            if isinstance(func, nodes.Name) and func.name in ("Redis", "StrictRedis"):
                parent = node.parent
                if isinstance(parent, nodes.Assign):
                    for target in parent.targets:
                        if isinstance(target, nodes.AssignName):
                            redis_vars.add(target.name)

            # Check for pipeline creation
            if (
                isinstance(func, nodes.Attribute)
                and func.attrname == "pipeline"
                and isinstance(func.expr, nodes.Name)
                and func.expr.name in redis_vars
            ):
                parent = node.parent
                if isinstance(parent, nodes.Assign):
                    for target in parent.targets:
                        if isinstance(target, nodes.AssignName):
                            pipeline_vars.add(target.name)

        return redis_vars, pipeline_vars

    def _parse_redis_operation(
        self, node: nodes.Call, rel_path: str, operation: str, is_pipeline: bool = False
    ) -> RedisUsage | None:
        """Parse a redis-py operation."""
        # Skip pipeline() and execute() calls
        if operation in ("pipeline", "execute"):
            return None

        # Extract key
        key = self._extract_redis_key(node, operation)

        # Check for TTL-related operations
        has_ttl, timeout, warning = self._analyze_redis_ttl(node, operation, is_pipeline)

        return RedisUsage(
            type=RedisUsageType.DIRECT_CLIENT,
            file=rel_path,
            line=node.lineno,
            library="redis",
            operation=operation,
            key=key,
            statement=safe_as_string(node),
            has_ttl=has_ttl if operation in ("set", "setex", "psetex") else None,
            timeout=timeout,
            warning=warning,
            is_pipeline=is_pipeline,
        )

    def _extract_redis_key(self, node: nodes.Call, operation: str) -> str | None:
        """Extract Redis key from operation call."""
        # Skip operations without keys
        if operation in ("keys", "flushdb", "flushall", "scan"):
            return None

        if node.args:
            return self._clean_key_pattern(self._infer_key_pattern(node.args[0]))

        return None

    def _analyze_redis_ttl(
        self, node: nodes.Call, operation: str, is_pipeline: bool
    ) -> tuple[bool, int | None, str | None]:
        """Analyze TTL settings for Redis operation."""
        has_ttl = False
        timeout = None
        warning = None

        if operation == "setex":
            has_ttl = True
            if len(node.args) >= 2:
                timeout_val = infer_value(node.args[1]).get_if_type((int, float))
                if timeout_val is not None:
                    timeout = int(timeout_val)

        elif operation == "set":
            for keyword in node.keywords:
                if keyword.arg in ("ex", "px", "exat", "pxat"):
                    has_ttl = True
                    timeout_val = infer_value(keyword.value).get_if_type((int, float))
                    if timeout_val is not None:
                        timeout = int(timeout_val)

            if not has_ttl and not is_pipeline:
                warning = "No TTL specified for Redis set operation"

        elif operation in ("incr", "decr", "append", "lpush", "rpush", "sadd", "zadd", "hset") and not is_pipeline:
            warning = f"No TTL specified for Redis {operation} operation"

        return has_ttl, timeout, warning

    def _calculate_summary(
        self, results: dict[str, list[RedisUsage]], scan_duration_ms: int, warnings: list[str]
    ) -> RedisUsageSummary:
        """Calculate summary statistics."""
        categories = {}
        total_usages = 0

        for usage_type, usages in results.items():
            categories[usage_type] = len(usages)
            total_usages += len(usages)

        files_scanned = len({usage.file for usages in results.values() for usage in usages})

        return RedisUsageSummary(
            total_count=total_usages,
            total_usages=total_usages,
            categories=categories,
            files_scanned=files_scanned,
            scan_duration_ms=scan_duration_ms,
            warnings=warnings,
        )
