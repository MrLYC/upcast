# Offset 使用扫描器（offset-usage）

## 概述

`scan-offset-usage` 是一个静态 AST 扫描器，用于找出 Django ORM、Django REST Framework 和 Django 原生 SQL 中可能生成 SQL `OFFSET` 的常见写法。它帮助定位页码越大、数据库需要跳过越多记录而容易变慢的分页路径。

扫描过程不会导入 Django/DRF、初始化项目、执行查询或连接数据库。因此结果是源码证据，不是实际 SQL、执行计划或延迟证明。

## 命令用法

```bash
upcast scan-offset-usage [OPTIONS] [PATH]
```

示例：

```bash
# 扫描当前项目
upcast scan-offset-usage .

# 输出 JSON 文件
upcast scan-offset-usage ./src --format json --output offset-usage.json

# 只扫描业务代码并排除测试
upcast scan-offset-usage . --include "app/**" --exclude "tests/**"
```

支持标准选项：`-o/--output`、`--format`、`-v/--verbose`、`--include`、`--exclude`、`--no-default-excludes` 和 Markdown 输出选项。

## 支持的模式

| 模式               | 框架              | 典型写法                                                 | 说明                                                                          |
| ------------------ | ----------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `queryset_slice`   | Django ORM        | `queryset[offset:offset + limit]`                        | QuerySet 切片下界会成为 offset；`queryset[:limit]` 不报告，因为它只有 LIMIT。 |
| `django_paginator` | Django            | `Paginator(queryset, page_size)`、`paginator.page(page)` | Django Paginator 会把页码转换成 QuerySet 的切片。构造和取页分别报告。         |
| `drf_page_number`  | DRF               | `PageNumberPagination`、`DEFAULT_PAGINATION_CLASS`       | 页码分页通常通过 Django Paginator 访问 QuerySet。                             |
| `drf_limit_offset` | DRF               | `LimitOffsetPagination`                                  | 直接暴露 limit/offset 查询参数。                                              |
| `raw_sql`          | Django 数据库 API | `QuerySet.raw()`、`RawSQL()`、`cursor.execute()`         | SQL 文本中出现 `OFFSET` 时报告，支持静态值、占位符和部分动态字符串。          |

检测依赖导入证据、QuerySet 方法链或已确认的对象绑定。普通 Python 列表/元组切片不会被当成 ORM 分页。

## 输出结构

```yaml
metadata:
  scanner_name: offset-usage
  static_analysis: true
  runtime_limit: Findings do not prove SQL plans or database latency.

summary:
  total_count: 2
  files_scanned: 1
  scan_duration_ms: 4
  by_pattern:
    queryset_slice: 1
    drf_limit_offset: 1
  by_framework:
    django: 1
    django-rest-framework: 1
  direct_offset_count: 1
  indirect_pagination_count: 1
  dynamic_count: 1

results:
  queryset_slice:
    - pattern: queryset_slice
      framework: django
      operation: slice
      file: app/views.py
      line: 24
      column: 10
      statement: "users[(page - 1) * page_size : page * page_size]"
      offset:
        name: offset
        expression: (page - 1) * page_size
        value: null
        source_kind: expression
        hardcoded: null
      limit:
        name: limit
        expression: page * page_size
        value: null
        source_kind: expression
        hardcoded: null
      parameters:
        - name: offset
          expression: (page - 1) * page_size
          value: null
          source_kind: expression
          hardcoded: null
        - name: limit
          expression: page * page_size
          value: null
          source_kind: expression
          hardcoded: null
      hardcoding_status: unknown
      warning: May generate SQL OFFSET; validate with a runtime query plan.
```

## 字段参考

### Finding 字段

| 字段                                      | 说明                                                                                       |
| ----------------------------------------- | ------------------------------------------------------------------------------------------ |
| `pattern`                                 | `queryset_slice`、`django_paginator`、`drf_page_number`、`drf_limit_offset` 或 `raw_sql`。 |
| `framework`                               | `django` 或 `django-rest-framework`。                                                      |
| `operation`                               | `slice`、`construct`、`page`、`declare`、`configure`、`raw`、`raw_sql` 或 `execute`。      |
| `file` / `line` / `column`                | 相对文件路径和源码位置。                                                                   |
| `statement`                               | 命中的源码语句。                                                                           |
| `parameters`                              | 所有识别出的 offset、limit、page、page-size 参数证据。                                     |
| `offset` / `limit` / `page` / `page_size` | 按用途直接访问的参数证据；无法识别时为 `null`。                                            |
| `hardcoding_status`                       | 参数聚合状态：`fully_hardcoded`、`partially_hardcoded`、`dynamic` 或 `unknown`。           |
| `warning`                                 | 提醒需要用真实 SQL/执行计划验证。                                                          |

### 参数证据

| 字段          | 说明                                                                                  |
| ------------- | ------------------------------------------------------------------------------------- |
| `expression`  | 源码中的原始表达式。                                                                  |
| `value`       | 可以静态推导出的值，无法推导时为 `null`。                                             |
| `source_kind` | `literal`、`static_constant`、`configuration`、`runtime`、`expression` 或 `unknown`。 |
| `hardcoded`   | 字面量/静态常量为 `true`；配置或运行时输入为 `false`；无法判断为 `null`。             |

## 排除项和限制

- `CursorPagination` 不使用 offset，不会被报告。
- 普通 Python 列表或元组切片不会被报告。
- `QuerySet` 类型推导是保守的；动态导入、自定义管理器和跨文件类型流转可能无法识别。
- 扫描器不会判断 offset 是否一定大于零；`offset=0` 会作为源码用法保留，但通常只产生 LIMIT。
- 扫描器不会执行 SQL、读取数据库统计信息、比较索引、生成 `EXPLAIN` 或测量慢查询耗时。
- `dynamic_count` 表示发现了动态参数，不等于实际运行时一定产生慢查询。
