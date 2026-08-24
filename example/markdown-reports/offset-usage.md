# offset-usage 扫描报告

## 元数据
- **scanner_name**: offset-usage
- **static_analysis**: True
- **runtime_limit**: Findings do not prove SQL plans or database latency.

## 概要信息
- **总数量**: 12
- **已扫描文件数**: 2368
- **扫描耗时**: 138513 毫秒

- **直接 Offset 发现数**: 5
- **间接分页发现数**: 7
- **动态参数发现数**: 5

### 按模式统计
- **queryset_slice**: 5
- **drf_limit_offset**: 7

### 按框架统计
- **django**: 5
- **django-rest-framework**: 7

## 结果详情

### queryset_slice

| 框架 | 操作 | 文件 | 行号 | 函数 | 类 | 硬编码状态 | 告警 | 语句 |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| django | slice | apiserver/paasng/paasng/bk_plugins/pluginscenter/iam_adaptor/management/providers.py | 41 | list_instance | PluginProvider | dynamic | May generate SQL OFFSET; validate with a runtime query plan. | `qs[page.slice_from:page.slice_to]` |
| django | slice | apiserver/paasng/paasng/bk_plugins/pluginscenter/iam_adaptor/management/providers.py | 73 | search_instance | PluginProvider | dynamic | May generate SQL OFFSET; validate with a runtime query plan. | `qs[page.slice_from:page.slice_to]` |
| django | slice | apiserver/paasng/paasng/infras/iam/open_apis/providers/application.py | 38 | list_instance | ApplicationProvider | dynamic | May generate SQL OFFSET; validate with a runtime query plan. | `applications[page_obj.slice_from:page_obj.slice_to]` |
| django | slice | apiserver/paasng/paasng/infras/iam/open_apis/providers/application.py | 78 | search_instance | ApplicationProvider | dynamic | May generate SQL OFFSET; validate with a runtime query plan. | `applications[page_obj.slice_from:page_obj.slice_to]` |
| django | slice | apiserver/paasng/paasng/plat_admin/admin42/views/applications.py | 106 | get_app_resource_context_data | ApplicationListView | partially_hardcoded | May generate SQL OFFSET; validate with a runtime query plan. | `queryset[offset:offset + limit]` |

#### 参数（apiserver/paasng/paasng/bk_plugins/pluginscenter/iam_adaptor/management/providers.py:41）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| offset | `page.slice_from` | 无 | configuration | 否 |
| limit | `page.slice_to` | 无 | configuration | 否 |
#### 参数（apiserver/paasng/paasng/bk_plugins/pluginscenter/iam_adaptor/management/providers.py:73）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| offset | `page.slice_from` | 无 | configuration | 否 |
| limit | `page.slice_to` | 无 | configuration | 否 |
#### 参数（apiserver/paasng/paasng/infras/iam/open_apis/providers/application.py:38）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| offset | `page_obj.slice_from` | 无 | configuration | 否 |
| limit | `page_obj.slice_to` | 无 | configuration | 否 |
#### 参数（apiserver/paasng/paasng/infras/iam/open_apis/providers/application.py:78）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| offset | `page_obj.slice_from` | 无 | configuration | 否 |
| limit | `page_obj.slice_to` | 无 | configuration | 否 |
#### 参数（apiserver/paasng/paasng/plat_admin/admin42/views/applications.py:106）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| offset | `offset` | 无 | runtime | 否 |
| limit | `offset + limit` | 无 | expression | 未知 |

### django_paginator

| 框架 | 操作 | 文件 | 行号 | 函数 | 类 | 硬编码状态 | 告警 | 语句 |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |


### drf_page_number

| 框架 | 操作 | 文件 | 行号 | 函数 | 类 | 硬编码状态 | 告警 | 语句 |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |


### drf_limit_offset

| 框架 | 操作 | 文件 | 行号 | 函数 | 类 | 硬编码状态 | 告警 | 语句 |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| django-rest-framework | configure | apiserver/paasng/paas_wl/bk_app/cnative/specs/views.py | 172 | 无 | VolumeMountViewSet | unknown | May generate SQL OFFSET; validate with a runtime query plan. | `pagination_class = LimitOffsetPagination` |
| django-rest-framework | configure | apiserver/paasng/paasng/bk_plugins/pluginscenter/views.py | 194 | 无 | PluginInstanceViewSet | unknown | May generate SQL OFFSET; validate with a runtime query plan. | `pagination_class = LimitOffsetPagination` |
| django-rest-framework | configure | apiserver/paasng/paasng/bk_plugins/pluginscenter/views.py | 526 | 无 | OperationRecordViewSet | unknown | May generate SQL OFFSET; validate with a runtime query plan. | `pagination_class = LimitOffsetPagination` |
| django-rest-framework | configure | apiserver/paasng/paasng/bk_plugins/pluginscenter/views.py | 569 | 无 | PluginReleaseViewSet | unknown | May generate SQL OFFSET; validate with a runtime query plan. | `pagination_class = LimitOffsetPagination` |
| django-rest-framework | declare | apiserver/paasng/paasng/plat_admin/system/utils.py | 21 | 无 | 无 | fully_hardcoded | May generate SQL OFFSET; validate with a runtime query plan. | `

class MaxLimitOffsetPagination(LimitOffsetPagination):
    """限制最大分页数"""
    max_limit = 100
    max_offset = 900

    def get_offset(self, request):
        """LimitOffsetPagination 的 get_limit() 中处理了 max_limit"""
        try:
            return _positive_int(request.query_params[self.offset_query_param], strict=True, cutoff=self.max_offset)
        except (KeyError, ValueError):
            return 0
` |
| django-rest-framework | declare | apiserver/paasng/paasng/platform/applications/pagination.py | 24 | 无 | 无 | fully_hardcoded | May generate SQL OFFSET; validate with a runtime query plan. | `

class ApplicationListPagination(LimitOffsetPagination):
    """应用列表分页器，用于添加各种应用类型数量等参数"""
    default_limit = 12

    def get_paginated_response(self, data, extra_data):
        return Response(OrderedDict([('count', self.count), ('next', self.get_next_link()), ('previous', self.get_previous_link()), ('extra_data', extra_data), ('results', data)]))
` |
| django-rest-framework | configure | apiserver/paasng/paasng/settings/__init__.py | 364 | 无 | 无 | fully_hardcoded | May generate SQL OFFSET; validate with a runtime query plan. | `REST_FRAMEWORK = {'EXCEPTION_HANDLER': 'paasng.utils.views.custom_exception_handler', 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ), 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination', 'PAGE_SIZE': 100, 'TEST_REQUEST_DEFAULT_FORMAT': 'json', 'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.SessionAuthentication', ), 'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S', 'SEARCH_PARAM': 'search_term', 'ORDERING_PARAM': 'order_by', 'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer', 'paasng.utils.views.BkStandardApiJSONRenderer']}` |

#### 参数（apiserver/paasng/paasng/plat_admin/system/utils.py:21）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| max_limit | `100` | 100 | literal | 是 |
#### 参数（apiserver/paasng/paasng/platform/applications/pagination.py:24）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| default_limit | `12` | 12 | literal | 是 |
#### 参数（apiserver/paasng/paasng/settings/__init__.py:364）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| page_size | `100` | 100 | literal | 是 |

### raw_sql

| 框架 | 操作 | 文件 | 行号 | 函数 | 类 | 硬编码状态 | 告警 | 语句 |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
