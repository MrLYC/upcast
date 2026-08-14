# Django 视图扫描器 (django-views)

`scan-django-views` 是独立于 `scan-django-urls` 的静态分析命令。它从视图定义和 URL/DRF Router 引用两侧建立证据，输出 Django/DRF 视图、ViewSet action、模型使用以及认证、授权、CSRF 相关的源码位置。

它不会执行 Django，也不会修改 `scan-django-urls` 的输出结构。

## 适用场景

- 审阅 API 或 Django 视图的路由入口、ViewSet action 和直接模型访问。
- 排查认证类、权限类、`AllowAny`、`csrf_exempt` 与自定义装饰器的静态证据。
- 将视图扫描结果与现有 URL 扫描结果按规范化视图标识合并。
- 为后续工具保留无法判定的装饰器、认证类和权限表达式，而不是把它们误判为开放访问。

## 使用方法

```bash
# 扫描项目中所有符合过滤条件的 Python 文件
upcast scan-django-views ./myproject

# 仅扫描指定源码范围
upcast scan-django-views ./myproject --include '**/api/*.py'

# 排除测试和迁移文件并写入 JSON
upcast scan-django-views ./myproject \
  --exclude 'tests/**' \
  --exclude 'migrations/**' \
  --format json \
  --output django-views.json

# 渲染中文 Markdown 报告
upcast scan-django-views ./myproject --format markdown --markdown-language zh
```

默认扫描所有可用的 Python 文件；视图是否被识别由框架语义和路由证据决定，不由 `views.py` 文件名决定。

## 识别与路由规则

- 已解析的 Django `View`、DRF `APIView`、`ViewSet`/`ModelViewSet` 等祖先会确认类视图。
- 已解析的 `@api_view` 会确认函数视图。
- 直接 `path()`/`re_path()` 指向的普通函数会成为已确认的函数视图。
- 支持 `ClassView.as_view()`、`router.register()`，以及 `include(router.urls)` 和 `urlpatterns = router.urls` 挂载证据。
- Router 注册未找到 `.urls` 挂载时保留为 `partial`，不会声称它是已确认端点，也不会虚构 Router 的完整 URL。
- 路由引用到无法确认框架祖先的类时，记录为 `partial` 候选；其中的装饰器和认证类仍会保留。

## 输出结构

结果以规范化视图 ID 为键；常见格式为 `package.module.ViewName`，action 以 `#action_name` 附在父视图 ID 后。

```yaml
summary:
  total_views: 2
  total_actions: 7
results:
  myapp.views.OrderViewSet:
    kind: drf_viewset
    recognition:
      status: confirmed
      evidence: []
    route_refs:
      - kind: router
        status: confirmed
        prefix: orders
        basename: order
        router_type: DefaultRouter
    security:
      authentication: { state: unknown }
      authorization: { state: configured }
      csrf: { state: unknown }
      raw_signals: []
    model_usages:
      - model: myapp.models.Order
        role: queryset
        operation: read
    actions:
      - id: myapp.views.OrderViewSet#archive
        origin: decorator
        methods: [post]
        detail: true
```

### 核心字段

| 字段                          | 含义                                                                     |
| ----------------------------- | ------------------------------------------------------------------------ |
| `recognition`                 | 视图识别依据及其解析状态。                                               |
| `route_refs`                  | 直接 URL 或 DRF Router 的反向引用；保留注册和挂载位置。                  |
| `unresolved_route_references` | 无法解析为规范化视图 ID 的直接路由目标；保留原始表达式但不伪造视图记录。 |
| `security.authentication`     | 认证类、`login_required` 或默认认证的静态证据。                          |
| `security.authorization`      | 权限类、布尔权限表达式和一跳权限定义的静态证据。                         |
| `security.csrf`               | `csrf_exempt`/`csrf_protect` 等 CSRF 信号。                              |
| `security.raw_signals`        | 无法按通用框架规则分类的装饰器或控制表达式。                             |
| `model_usages`                | `queryset`、`model`、serializer `Meta.model` 和已知直接 ORM 调用。       |
| `actions`                     | 显式 `@action` 与安全派生的标准 ViewSet CRUD action。                    |

## 证据状态与边界

所有依赖解析的事实使用以下状态：

- `confirmed`：已由静态源码证据解析。
- `partial`：发现了候选或不完整链路，例如未挂载 Router 注册或无法确认祖先的路由类。
- `unknown`：表达式动态、未绑定或属于未解释的自定义逻辑。

`AllowAny` 只表示授权层的信号；`csrf_exempt` 只表示 CSRF 信号。二者都不会被扫描器当作 Django 登录豁免。自定义装饰器、认证类、权限类和 service/IAM 调用不会被硬编码映射：原始表达式与位置会保留，供后续工具或人工解释。

权限定义最多追踪一跳，记录其定义、直接基类和 `has_permission`/`has_object_permission` 方法位置；扫描器不会递归解释这些方法中的任意调用。模型使用也仅覆盖明确声明、serializer 元数据和已知直接 ORM 方法；动态模型、服务层和自定义 manager 保持 `unknown`。
