# Change Proposal: Fix Request Constructor URL Parsing

## Overview

修复 HTTP request scanner 中对 `Request()` 构造器的 URL 提取错误，正确识别 `Request(method, url)` 的参数顺序。

## Why

当前实现假设所有 HTTP 请求调用的第一个参数都是 URL，但 `requests.Request()` 构造器的签名是 `Request(method, url, ...)`，第一个参数是 HTTP method，第二个才是 URL。这导致：

1. **错误的 URL 识别**：将 HTTP method（如 "GET", "POST"）误识别为 URL
2. **分组混乱**：不同的请求被错误地分组到 "GET"、"POST" 等键下
3. **信息丢失**：真实的 URL 信息丢失

例如当前输出：

```yaml
GET: # 这应该是 URL，但实际是 method
  library: requests
  method: REQUEST
  usages:
    - statement: Request('GET', 'https://example.com/api?...')
```

期望输出：

```yaml
https://example.com/api?...:
  library: requests
  method: GET
  usages:
    - statement: Request('GET', 'https://example.com/api?...')
```

## What Changes

### 核心修改

修改 `HttpRequestsScanner._extract_url()` 方法：

1. **识别 Request 构造器**：检测是否为 `Request()` 调用
2. **正确的参数提取**：
   - 对于 `Request(method, url, ...)`：提取第二个位置参数作为 URL
   - 对于 `Request(method=..., url=...)`：从关键字参数提取
   - 对于其他 HTTP 方法（如 `requests.get(url, ...)`）：提取第一个位置参数
3. **同时提取 method**：从 Request 构造器的第一个参数提取 HTTP method

### 影响范围

- **文件**：`upcast/scanners/http_requests.py`
- **方法**：`_extract_url()`, `_check_request_call()`
- **向后兼容**：输出格式兼容，但分组键会变化（从错误的 method 变为正确的 URL）

## Implementation Plan

1. 添加 `_is_request_constructor()` 辅助方法检测 Request 构造器
2. 修改 `_extract_url()` 方法，根据调用类型选择正确的参数位置
3. 修改 `_check_request_call()` 方法，从 Request 构造器提取 method
4. 添加测试用例覆盖：
   - `Request(method, url)` 位置参数
   - `Request(method='GET', url='...')` 命名参数
   - 混合形式 `Request('GET', url='...')`
5. 重新生成示例输出

## Alternatives Considered

1. **特殊处理所有构造器**：复杂度高，维护困难
2. **统一使用 method 参数**：需要修改数据模型，影响范围大
3. **当前方案（推荐）**：针对性修复，最小化影响

## Testing Strategy

- 单元测试：覆盖 Request 构造器的各种调用形式
- 集成测试：验证 blueking-paas 示例的扫描结果
- 回归测试：确保其他 HTTP 库的识别不受影响
