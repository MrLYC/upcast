## Why

Django ORM 的常见分页写法会把页码转换为 SQL `OFFSET`，当页码变大时数据库需要跳过越来越多的记录，容易形成慢查询。Upcast 目前没有静态盘点这类用法的能力，代码审查需要人工搜索多种 ORM、分页器和原生 SQL 写法。

## What Changes

- Add a `scan-offset-usage` command with the standard scanner CLI options.
- Detect common offset-producing Django patterns:
  - Django `QuerySet` slices with an offset expression.
  - `django.core.paginator.Paginator` construction and page retrieval.
  - Django REST Framework `PageNumberPagination` and `LimitOffsetPagination` declarations/configuration.
  - Django raw SQL/`RawSQL`/`QuerySet.raw()`/cursor execution containing `LIMIT` and/or `OFFSET`.
- Report the matched statement, pattern, framework, offset/limit/page expressions, and static-versus-dynamic evidence for each parameter.
- Distinguish direct offset use from indirect pagination that can generate offset, while excluding cursor pagination and ordinary Python list slicing.
- Keep scanning static and dependency-free: do not import Django, execute queries, or connect to a database.

## Impact

- Affected specs: new `offset-usage-scanner`, plus `cli-interface`, `data-models`, and `scanner-architecture` deltas.
- Affected code: a new typed model/scanner, CLI registration, and package exports.
- Affected tests/docs: dedicated model, scanner, CLI, and documentation coverage.
- Compatibility: existing commands and serialized outputs remain unchanged.
