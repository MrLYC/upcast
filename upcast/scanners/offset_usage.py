"""Static scanner for Django ORM and pagination patterns that can use OFFSET."""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import ClassVar

from astroid import nodes

from upcast.common.ast_utils import get_import_info, safe_as_string
from upcast.common.file_utils import get_relative_path_str
from upcast.common.inference import infer_string_pattern, infer_value
from upcast.common.scanner_base import BaseScanner
from upcast.models.offset_usage import OffsetParameter, OffsetUsage, OffsetUsageOutput, OffsetUsageSummary


class OffsetUsageScanner(BaseScanner[OffsetUsageOutput]):
    """Find source patterns that can translate into SQL offset pagination."""

    PATTERNS: ClassVar[tuple[str, ...]] = (
        "queryset_slice",
        "django_paginator",
        "drf_page_number",
        "drf_limit_offset",
        "raw_sql",
    )
    QUERYSET_METHODS: ClassVar[set[str]] = {
        "all",
        "annotate",
        "alias",
        "complex_filter",
        "defer",
        "difference",
        "distinct",
        "earliest",
        "exclude",
        "filter",
        "filter_queryset",
        "intersection",
        "latest",
        "none",
        "only",
        "order_by",
        "prefetch_related",
        "reverse",
        "select_for_update",
        "select_related",
        "union",
        "using",
        "values",
        "values_list",
    }
    PAGINATOR_QNAME = "django.core.paginator.Paginator"
    PAGINATION_QNAMES: ClassVar[dict[str, str]] = {
        "rest_framework.pagination.PageNumberPagination": "drf_page_number",
        "rest_framework.pagination.LimitOffsetPagination": "drf_limit_offset",
    }
    CURSOR_QNAME = "rest_framework.pagination.CursorPagination"
    RAW_SQL_QNAME = "django.db.models.expressions.RawSQL"
    QUERYSET_QNAME = "django.db.models.query.QuerySet"
    CONNECTION_QNAME = "django.db.connection"
    SQL_OFFSET_RE: ClassVar[re.Pattern[str]] = re.compile(r"""\boffset\s+(?P<value>[^\s,;)'\"}]+)""", re.IGNORECASE)
    SQL_LIMIT_RE: ClassVar[re.Pattern[str]] = re.compile(r"""\blimit\s+(?P<value>[^\s,;)'\"}]+)""", re.IGNORECASE)
    SQL_BRACED_OFFSET_RE: ClassVar[re.Pattern[str]] = re.compile(r"\boffset\s+\{(?P<value>[^}]+)\}", re.IGNORECASE)
    SQL_BRACED_LIMIT_RE: ClassVar[re.Pattern[str]] = re.compile(r"\blimit\s+\{(?P<value>[^}]+)\}", re.IGNORECASE)
    SQL_PLACEHOLDER_RE: ClassVar[re.Pattern[str]] = re.compile(r"%s|\?|:[A-Za-z_]\w*|\$\d+")
    PARAMETER_NAMES: ClassVar[set[str]] = {
        "offset",
        "limit",
        "page",
        "page_number",
        "page_size",
        "per_page",
        "default_limit",
        "max_limit",
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

    def scan(self, path: Path) -> OffsetUsageOutput:
        """Scan Python files for offset-producing source patterns."""
        start_time = time.perf_counter()
        files = self.get_files_to_scan(path)
        base_path = path if path.is_dir() else path.parent
        findings: list[OffsetUsage] = []

        for file_path in files:
            module = self.parse_file(file_path)
            if module is None:
                continue
            relative_path = get_relative_path_str(file_path, base_path)
            findings.extend(self._scan_module(module, relative_path))

        findings.sort(key=lambda item: (item.file, item.line, item.column, item.pattern, item.operation))
        results: dict[str, list[OffsetUsage]] = {pattern: [] for pattern in self.PATTERNS}
        for finding in findings:
            results[finding.pattern].append(finding)

        by_pattern = {pattern: len(results[pattern]) for pattern in self.PATTERNS if results[pattern]}
        by_framework: dict[str, int] = {}
        direct_count = indirect_count = dynamic_count = 0
        for finding in findings:
            by_framework[finding.framework] = by_framework.get(finding.framework, 0) + 1
            if finding.pattern in {"queryset_slice", "raw_sql"}:
                direct_count += 1
            else:
                indirect_count += 1
            if any(parameter.hardcoded is False for parameter in finding.parameters):
                dynamic_count += 1

        summary = OffsetUsageSummary(
            total_count=len(findings),
            files_scanned=len(files),
            scan_duration_ms=int((time.perf_counter() - start_time) * 1000),
            by_pattern=by_pattern,
            by_framework=dict(sorted(by_framework.items())),
            direct_offset_count=direct_count,
            indirect_pagination_count=indirect_count,
            dynamic_count=dynamic_count,
        )
        return OffsetUsageOutput(
            summary=summary,
            results=results,
            metadata={
                "scanner_name": "offset-usage",
                "static_analysis": True,
                "runtime_limit": "Findings do not prove SQL plans or database latency.",
            },
        )

    def _scan_module(self, module: nodes.Module, relative_path: str) -> list[OffsetUsage]:
        imports = get_import_info(module)
        queryset_names = self._collect_queryset_names(module, imports)
        paginator_bindings = self._collect_paginator_bindings(module, imports, queryset_names)
        cursor_names = self._collect_cursor_names(module, imports)
        findings: list[OffsetUsage] = []

        for subscript in module.nodes_of_class(nodes.Subscript):
            finding = self._finding_from_slice(subscript, relative_path, imports, queryset_names)
            if finding is not None:
                findings.append(finding)

        for call in module.nodes_of_class(nodes.Call):
            paginator_finding = self._finding_from_paginator_call(
                call, relative_path, imports, queryset_names, paginator_bindings
            )
            if paginator_finding is not None:
                findings.append(paginator_finding)

            raw_finding = self._finding_from_raw_sql(call, relative_path, imports, queryset_names, cursor_names)
            if raw_finding is not None:
                findings.append(raw_finding)

        findings.extend(self._findings_from_drf_classes(module, relative_path, imports))
        findings.extend(self._findings_from_drf_assignments(module, relative_path, imports))
        findings.extend(self._findings_from_drf_settings(module, relative_path, imports))
        return findings

    def _collect_queryset_names(self, module: nodes.Module, imports: dict[str, str]) -> set[str]:  # noqa: C901
        names: set[str] = set()

        for function in module.nodes_of_class((nodes.FunctionDef, nodes.AsyncFunctionDef)):
            if function.args is None:
                continue
            for argument in [*function.args.args, *function.args.kwonlyargs]:
                annotation = getattr(argument, "annotation", None)
                if annotation is not None and self._qualified_name(annotation, imports) == self.QUERYSET_QNAME:
                    names.add(argument.name)

        assignments = list(module.nodes_of_class((nodes.Assign, nodes.AnnAssign)))
        for _ in range(3):
            changed = False
            for assignment in assignments:
                value = assignment.value
                if not self._is_queryset_expr(value, imports, names):
                    continue
                for name in self._assignment_names(assignment):
                    if name not in names:
                        names.add(name)
                        changed = True
            if not changed:
                break
        return names

    def _collect_paginator_bindings(
        self,
        module: nodes.Module,
        imports: dict[str, str],
        queryset_names: set[str],
    ) -> dict[str, nodes.Call]:
        bindings: dict[str, nodes.Call] = {}
        for assignment in module.nodes_of_class((nodes.Assign, nodes.AnnAssign)):
            value = assignment.value
            if not isinstance(value, nodes.Call) or self._qualified_name(value.func, imports) != self.PAGINATOR_QNAME:
                continue
            if value.args and not self._is_queryset_expr(value.args[0], imports, queryset_names):
                continue
            for name in self._assignment_names(assignment):
                bindings[name] = value
        return bindings

    def _collect_cursor_names(self, module: nodes.Module, imports: dict[str, str]) -> set[str]:
        names: set[str] = set()
        for assignment in module.nodes_of_class((nodes.Assign, nodes.AnnAssign)):
            value = assignment.value
            if isinstance(value, nodes.Call) and self._is_connection_cursor(value, imports):
                names.update(self._assignment_names(assignment))

        for with_node in module.nodes_of_class(nodes.With):
            for context_expr, optional_vars in with_node.items:
                if self._is_connection_cursor(context_expr, imports) and isinstance(optional_vars, nodes.AssignName):
                    names.add(optional_vars.name)
        return names

    def _finding_from_slice(
        self,
        subscript: nodes.Subscript,
        relative_path: str,
        imports: dict[str, str],
        queryset_names: set[str],
    ) -> OffsetUsage | None:
        if not isinstance(subscript.slice, nodes.Slice) or subscript.slice.lower is None:
            return None
        if not self._is_queryset_expr(subscript.value, imports, queryset_names):
            return None

        offset = self._parameter("offset", subscript.slice.lower, imports)
        limit = self._parameter("limit", subscript.slice.upper, imports) if subscript.slice.upper is not None else None
        parameters = [offset, limit] if limit is not None else [offset]
        return self._make_finding(
            subscript,
            relative_path,
            pattern="queryset_slice",
            framework="django",
            operation="slice",
            parameters=parameters,
            offset=offset,
            limit=limit,
            hardcoding_status=self._hardcoding_status(parameters),
        )

    def _finding_from_paginator_call(
        self,
        call: nodes.Call,
        relative_path: str,
        imports: dict[str, str],
        queryset_names: set[str],
        paginator_bindings: dict[str, nodes.Call],
    ) -> OffsetUsage | None:
        qualified_name = self._qualified_name(call.func, imports)
        if qualified_name == self.PAGINATOR_QNAME:
            if call.args and not self._is_queryset_expr(call.args[0], imports, queryset_names):
                return None
            page_size_node = self._call_argument(call, "per_page", 1)
            page_size = self._parameter("page_size", page_size_node, imports) if page_size_node else None
            parameters = [page_size] if page_size is not None else []
            return self._make_finding(
                call,
                relative_path,
                pattern="django_paginator",
                framework="django",
                operation="construct",
                parameters=parameters,
                page_size=page_size,
                hardcoding_status=self._hardcoding_status(parameters),
            )

        if not isinstance(call.func, nodes.Attribute) or call.func.attrname not in {"page", "get_page"}:
            return None
        constructor = self._paginator_constructor(call.func.expr, paginator_bindings)
        if constructor is None:
            return None
        page_node = self._call_argument(call, "number", 0)
        page = self._parameter("page", page_node, imports) if page_node else None
        page_size_node = self._call_argument(constructor, "per_page", 1)
        page_size = self._parameter("page_size", page_size_node, imports) if page_size_node else None
        parameters = [parameter for parameter in (page, page_size) if parameter is not None]
        return self._make_finding(
            call,
            relative_path,
            pattern="django_paginator",
            framework="django",
            operation="page",
            parameters=parameters,
            page=page,
            page_size=page_size,
            hardcoding_status=self._hardcoding_status(parameters),
        )

    def _finding_from_raw_sql(
        self,
        call: nodes.Call,
        relative_path: str,
        imports: dict[str, str],
        queryset_names: set[str],
        cursor_names: set[str],
    ) -> OffsetUsage | None:
        operation: str | None = None
        sql_node: nodes.NodeNG | None = None

        qualified_name = self._qualified_name(call.func, imports)
        if qualified_name == self.RAW_SQL_QNAME:
            operation = "raw_sql"
            sql_node = call.args[0] if call.args else None
        elif isinstance(call.func, nodes.Attribute) and call.func.attrname == "raw":
            if self._is_queryset_expr(call.func.expr, imports, queryset_names):
                operation = "raw"
                sql_node = call.args[0] if call.args else None
        elif isinstance(call.func, nodes.Attribute) and call.func.attrname == "execute":
            if self._is_cursor_receiver(call.func.expr, imports, cursor_names):
                operation = "execute"
                sql_node = call.args[0] if call.args else None

        if operation is None or sql_node is None:
            return None
        return self._raw_sql_finding(call, sql_node, relative_path, imports, operation)

    def _raw_sql_finding(
        self,
        call: nodes.Call,
        sql_node: nodes.NodeNG,
        relative_path: str,
        imports: dict[str, str],
        operation: str,
    ) -> OffsetUsage | None:
        sql_pattern = infer_string_pattern(sql_node).to_pattern()
        source_text = safe_as_string(sql_node)
        if not re.search(r"\boffset\b", sql_pattern, re.IGNORECASE) and not re.search(
            r"\boffset\b", source_text, re.IGNORECASE
        ):
            return None

        offset = self._sql_parameter("offset", sql_node, source_text, self.SQL_OFFSET_RE, call, imports)
        limit = self._sql_parameter("limit", sql_node, source_text, self.SQL_LIMIT_RE, call, imports)
        parameters = [parameter for parameter in (limit, offset) if parameter is not None]
        return self._make_finding(
            call,
            relative_path,
            pattern="raw_sql",
            framework="django",
            operation=operation,
            parameters=parameters,
            offset=offset,
            limit=limit,
            hardcoding_status=self._hardcoding_status(parameters),
        )

    def _sql_parameter(
        self,
        name: str,
        sql_node: nodes.NodeNG,
        source_text: str,
        token_pattern: re.Pattern[str],
        call: nodes.Call,
        imports: dict[str, str],
    ) -> OffsetParameter | None:
        match = token_pattern.search(source_text)
        braced_pattern = self.SQL_BRACED_OFFSET_RE if name == "offset" else self.SQL_BRACED_LIMIT_RE
        braced_match = braced_pattern.search(source_text)
        if braced_match is not None:
            return self._parameter_from_text(name, braced_match.group("value"), imports)

        pattern_text = infer_string_pattern(sql_node).to_pattern()
        match = token_pattern.search(pattern_text)
        if match is None:
            return None
        sql_value = match.group("value")
        if sql_value in {"%s", "?"} or sql_value.startswith(":") or sql_value.startswith("$") or sql_value == "...":
            placeholder = self._sql_placeholder_node(name, source_text, call)
            if placeholder is not None:
                return self._parameter(name, placeholder, imports)
            return OffsetParameter(
                name=name,
                expression=sql_value,
                value=None,
                source_kind="runtime",
                hardcoded=False,
            )
        return self._parameter_from_text(name, sql_value, imports)

    def _sql_placeholder_node(self, name: str, source_text: str, call: nodes.Call) -> nodes.NodeNG | None:
        if len(call.args) < 2:
            return None
        params = call.args[1]
        if not isinstance(params, (nodes.List, nodes.Tuple)):
            return None
        placeholders = list(self.SQL_PLACEHOLDER_RE.finditer(source_text))
        clause_match = (self.SQL_OFFSET_RE if name == "offset" else self.SQL_LIMIT_RE).search(source_text)
        if clause_match is None:
            return None
        before_clause = source_text[: clause_match.start()]
        placeholder_index = len(self.SQL_PLACEHOLDER_RE.findall(before_clause))
        if placeholder_index >= len(params.elts):
            return None
        if not placeholders or placeholder_index >= len(placeholders):
            return None
        return params.elts[placeholder_index]

    def _findings_from_drf_classes(
        self,
        module: nodes.Module,
        relative_path: str,
        imports: dict[str, str],
    ) -> list[OffsetUsage]:
        findings: list[OffsetUsage] = []
        for class_node in module.nodes_of_class(nodes.ClassDef):
            pattern = self._drf_pattern_from_bases(class_node.bases, imports)
            if pattern is None:
                continue
            parameters = self._drf_class_parameters(class_node, pattern, imports)
            finding = self._make_finding(
                class_node,
                relative_path,
                pattern=pattern,
                framework="django-rest-framework",
                operation="declare",
                parameters=parameters,
                page_size=self._parameter_named(parameters, "page_size"),
                limit=self._parameter_named(parameters, "default_limit"),
                hardcoding_status=self._hardcoding_status(parameters),
            )
            findings.append(finding)
        return findings

    def _findings_from_drf_assignments(
        self,
        module: nodes.Module,
        relative_path: str,
        imports: dict[str, str],
    ) -> list[OffsetUsage]:
        findings: list[OffsetUsage] = []
        for assignment in module.nodes_of_class((nodes.Assign, nodes.AnnAssign)):
            target_names = self._assignment_names(assignment)
            if "pagination_class" not in target_names:
                continue
            pattern = self._drf_pattern_from_node(assignment.value, imports)
            if pattern is None:
                continue
            findings.append(
                self._make_finding(
                    assignment,
                    relative_path,
                    pattern=pattern,
                    framework="django-rest-framework",
                    operation="configure",
                    parameters=[],
                    hardcoding_status="unknown",
                )
            )
        return findings

    def _findings_from_drf_settings(
        self,
        module: nodes.Module,
        relative_path: str,
        imports: dict[str, str],
    ) -> list[OffsetUsage]:
        findings: list[OffsetUsage] = []
        for assignment in module.nodes_of_class((nodes.Assign, nodes.AnnAssign)):
            if "REST_FRAMEWORK" not in self._assignment_names(assignment) or not isinstance(
                assignment.value, nodes.Dict
            ):
                continue
            settings = {safe_as_string(key): value for key, value in assignment.value.items if key is not None}
            paginator_node = settings.get("'DEFAULT_PAGINATION_CLASS'") or settings.get('"DEFAULT_PAGINATION_CLASS"')
            if paginator_node is None:
                continue
            pattern = self._drf_pattern_from_node(paginator_node, imports, string_value=True)
            if pattern is None:
                continue
            page_size_node = settings.get("'PAGE_SIZE'") or settings.get('"PAGE_SIZE"')
            page_size = self._parameter("page_size", page_size_node, imports) if page_size_node else None
            parameters = [page_size] if page_size is not None else []
            findings.append(
                self._make_finding(
                    assignment,
                    relative_path,
                    pattern=pattern,
                    framework="django-rest-framework",
                    operation="configure",
                    parameters=parameters,
                    page_size=page_size,
                    hardcoding_status=self._hardcoding_status(parameters),
                )
            )
        return findings

    def _drf_class_parameters(
        self,
        class_node: nodes.ClassDef,
        pattern: str,
        imports: dict[str, str],
    ) -> list[OffsetParameter]:
        names = (
            ("page_size", "page_query_param")
            if pattern == "drf_page_number"
            else (
                "default_limit",
                "max_limit",
                "offset_query_param",
                "limit_query_param",
            )
        )
        parameters: list[OffsetParameter] = []
        for assignment in class_node.body:
            if not isinstance(assignment, (nodes.Assign, nodes.AnnAssign)):
                continue
            targets = self._assignment_names(assignment)
            for name in names:
                if name in targets:
                    parameters.append(self._parameter(name, assignment.value, imports))
        return parameters

    def _drf_pattern_from_bases(self, bases: list[nodes.NodeNG], imports: dict[str, str]) -> str | None:
        for base in bases:
            pattern = self._drf_pattern_from_node(base, imports)
            if pattern is not None:
                return pattern
        return None

    def _drf_pattern_from_node(
        self,
        node: nodes.NodeNG,
        imports: dict[str, str],
        *,
        string_value: bool = False,
    ) -> str | None:
        qualified_name = self._qualified_name(node, imports)
        if qualified_name in self.PAGINATION_QNAMES:
            return self.PAGINATION_QNAMES[qualified_name]
        if qualified_name == self.CURSOR_QNAME:
            return None
        if string_value:
            value = infer_value(node).get_if_type(str)
            if value in {
                "rest_framework.pagination.PageNumberPagination",
                "rest_framework.pagination.LimitOffsetPagination",
            }:
                return "drf_page_number" if value.endswith("PageNumberPagination") else "drf_limit_offset"
        return None

    def _is_queryset_expr(
        self,
        expression: nodes.NodeNG,
        imports: dict[str, str],
        queryset_names: set[str],
    ) -> bool:
        if isinstance(expression, nodes.Name):
            return expression.name in queryset_names
        if isinstance(expression, nodes.Attribute):
            if expression.attrname in {"objects", "all_objects", "queryset"}:
                return self._looks_like_model_expr(expression.expr, imports)
            return expression.attrname in {"get_queryset", "filter_queryset"}
        if isinstance(expression, nodes.Call) and isinstance(expression.func, nodes.Attribute):
            method = expression.func.attrname
            if method in {"get_queryset", "filter_queryset"}:
                return True
            if method in self.QUERYSET_METHODS:
                return self._is_queryset_expr(expression.func.expr, imports, queryset_names)
            if method == "raw":
                return self._is_queryset_expr(expression.func.expr, imports, queryset_names)
        if isinstance(expression, nodes.Subscript):
            return self._is_queryset_expr(expression.value, imports, queryset_names)
        return False

    def _looks_like_model_expr(self, expression: nodes.NodeNG, imports: dict[str, str]) -> bool:
        if isinstance(expression, nodes.Name):
            qualified_name = imports.get(expression.name, "")
            return (
                expression.name == "self"
                or expression.name[:1].isupper()
                or ".models." in qualified_name
                or qualified_name.endswith(".models")
            )
        return isinstance(expression, nodes.Attribute)

    def _paginator_constructor(
        self,
        expression: nodes.NodeNG,
        paginator_bindings: dict[str, nodes.Call],
    ) -> nodes.Call | None:
        if isinstance(expression, nodes.Name):
            return paginator_bindings.get(expression.name)
        if isinstance(expression, nodes.Call):
            return expression
        return None

    def _is_connection_cursor(self, expression: nodes.NodeNG, imports: dict[str, str]) -> bool:
        if not isinstance(expression, nodes.Call) or not isinstance(expression.func, nodes.Attribute):
            return False
        return expression.func.attrname == "cursor" and self._qualified_name(expression.func.expr, imports) in {
            self.CONNECTION_QNAME,
            "django.db.connections",
        }

    def _is_cursor_receiver(
        self,
        expression: nodes.NodeNG,
        imports: dict[str, str],
        cursor_names: set[str],
    ) -> bool:
        if isinstance(expression, nodes.Name):
            return expression.name in cursor_names or expression.name.lower() in {"cursor", "cur"}
        return self._is_connection_cursor(expression, imports)

    @staticmethod
    def _assignment_names(assignment: nodes.Assign | nodes.AnnAssign) -> list[str]:
        targets: list[nodes.NodeNG] = (
            assignment.targets if isinstance(assignment, nodes.Assign) else [assignment.target]
        )
        return [target.name for target in targets if isinstance(target, nodes.AssignName)]

    @staticmethod
    def _call_argument(call: nodes.Call, keyword_name: str, positional_index: int) -> nodes.NodeNG | None:
        for keyword in call.keywords:
            if keyword.arg == keyword_name:
                return keyword.value
        return call.args[positional_index] if positional_index < len(call.args) else None

    def _parameter(self, name: str, expression_node: nodes.NodeNG, imports: dict[str, str]) -> OffsetParameter:
        expression = safe_as_string(expression_node)
        inferred = infer_value(expression_node)
        if inferred.confidence == "exact":
            value = inferred.value
            source_kind = "literal" if isinstance(expression_node, nodes.Const) else "static_constant"
            hardcoded: bool | None = True
        elif self._is_known_dynamic(expression_node, imports) or (
            isinstance(expression_node, nodes.Name) and expression_node.name.lower() in self.PARAMETER_NAMES
        ):
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
        return OffsetParameter(
            name=name,
            expression=expression or None,
            value=value,
            source_kind=source_kind,
            hardcoded=hardcoded,
        )

    def _parameter_from_text(self, name: str, text: str, imports: dict[str, str]) -> OffsetParameter:
        stripped = text.strip().strip(",")
        if stripped.isdigit():
            return OffsetParameter(
                name=name,
                expression=stripped,
                value=int(stripped),
                source_kind="literal",
                hardcoded=True,
            )
        if stripped.lower() in {"null", "none"}:
            return OffsetParameter(
                name=name,
                expression=stripped,
                value=None,
                source_kind="unknown",
                hardcoded=None,
            )
        if stripped.isidentifier():
            return OffsetParameter(
                name=name,
                expression=stripped,
                value=None,
                source_kind="runtime",
                hardcoded=False,
            )
        return OffsetParameter(
            name=name,
            expression=stripped or None,
            value=None,
            source_kind="expression",
            hardcoded=None,
        )

    @staticmethod
    def _parameter_named(parameters: list[OffsetParameter], name: str) -> OffsetParameter | None:
        return next((parameter for parameter in parameters if parameter.name == name), None)

    def _make_finding(
        self,
        node: nodes.NodeNG,
        relative_path: str,
        *,
        pattern: str,
        framework: str,
        operation: str,
        parameters: list[OffsetParameter],
        offset: OffsetParameter | None = None,
        limit: OffsetParameter | None = None,
        page: OffsetParameter | None = None,
        page_size: OffsetParameter | None = None,
        hardcoding_status: str,
    ) -> OffsetUsage:
        function, class_name = self._context(node)
        return OffsetUsage(
            pattern=pattern,
            framework=framework,
            operation=operation,
            file=relative_path,
            line=node.lineno,
            column=node.col_offset,
            statement=self._redact_statement(safe_as_string(node)) or None,
            function=function,
            class_name=class_name,
            parameters=parameters,
            offset=offset,
            limit=limit,
            page=page,
            page_size=page_size,
            hardcoding_status=hardcoding_status,
            warning="May generate SQL OFFSET; validate with a runtime query plan.",
        )

    @staticmethod
    def _hardcoding_status(parameters: list[OffsetParameter]) -> str:
        statuses = [parameter.hardcoded for parameter in parameters]
        if not statuses or all(status is None for status in statuses):
            return "unknown"
        if all(status is True for status in statuses):
            return "fully_hardcoded"
        if all(status is False for status in statuses):
            return "dynamic"
        return "partially_hardcoded"

    @staticmethod
    def _qualified_name(node: nodes.NodeNG, imports: dict[str, str]) -> str | None:
        if isinstance(node, nodes.Name):
            return imports.get(node.name, node.name)
        if isinstance(node, nodes.Attribute):
            prefix = OffsetUsageScanner._qualified_name(node.expr, imports)
            return f"{prefix}.{node.attrname}" if prefix else node.attrname
        return None

    @staticmethod
    def _is_known_dynamic(node: nodes.NodeNG, imports: dict[str, str]) -> bool:
        if not isinstance(node, nodes.Call):
            return False
        qualified_name = OffsetUsageScanner._qualified_name(node.func, imports) or ""
        return qualified_name in {
            "os.getenv",
            "os.environ.get",
            "os.environ.setdefault",
            "request.GET.get",
            "request.query_params.get",
            "request.query_params.getlist",
        }

    @staticmethod
    def _looks_like_configuration(node: nodes.NodeNG) -> bool:
        if isinstance(node, (nodes.Attribute, nodes.Subscript)):
            return True
        return isinstance(node, nodes.Name) and node.name.lower() in {"settings", "config", "configuration"}

    @staticmethod
    def _redact_statement(statement: str) -> str:
        if not statement:
            return statement
        return re.sub(
            r"(?i)(password|passwd|secret|token|credential|api_key|access_key|private_key)\s*=\s*(['\"]).*?\2",
            r"\1=<redacted>",
            statement,
        )

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
