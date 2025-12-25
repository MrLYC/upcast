# Change Proposal: Filter Non-Request Calls

## Overview

修复 HTTP request scanner 将非请求类（如 `RequestException`、`Response`、`Adapter` 等）误识别为 HTTP 请求的问题。

## Why

当前扫描器使用过于宽泛的模式匹配，导致任何包含 "Request"、"Response" 等关键字的类都被识别为 HTTP 请求，包括：

1. **异常类**：`RequestException`、`HTTPError` 等
2. **响应类**：`Response`、`PreparedRequest` 等
3. **辅助类**：`Adapter`、`HTTPBasicAuth`、`OAuth2Session` 等
4. **工具类**：`RequestsInstrumentor` 等

这导致输出中出现大量不相关的条目，例如：

```yaml
faked requests exception: # 这是异常，不是请求
  method: REQUESTEXCEPTION
  statement: RequestException('faked requests exception')
```

## What Changes

### 核心修改

在 `_identify_request()` 方法中添加黑名单过滤：

1. **定义黑名单**：列出不应该被识别为请求的类名

   - 异常类：`Exception`, `Error`
   - 响应/配置类：`Response`, `Session`, `Adapter`, `Auth`
   - 工具类：`Instrumentor`

2. **过滤逻辑**：在识别到可能的请求调用时，检查是否在黑名单中

3. **白名单优先**：保留明确的 HTTP 方法（get, post, put, delete 等）

### 影响范围

- **文件**：`upcast/scanners/http_requests.py`
- **方法**：`_identify_request()`
- **向后兼容**：输出会变少（移除误报），但真实请求不受影响

## Implementation Plan

1. 添加 `EXCLUDED_PATTERNS` 类变量定义黑名单
2. 修改 `_identify_request()` 方法，在返回前检查黑名单
3. 添加测试用例覆盖：
   - `RequestException` 不被识别
   - `Response()` 不被识别
   - `HTTPBasicAuth()` 不被识别
   - 真实请求（`requests.get()`）仍然被识别
4. 重新生成示例输出

## Alternatives Considered

1. **精确匹配方法名**：只匹配 HTTP 方法，但会遗漏 `Request()` 构造器
2. **正则表达式**：复杂度高，维护困难
3. **黑名单过滤（推荐）**：简单、可扩展、向后兼容

## Testing Strategy

- 单元测试：验证黑名单类不被识别
- 回归测试：确保真实 HTTP 请求仍被正确识别
- 集成测试：验证 blueking-paas 示例的扫描结果
