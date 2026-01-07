# HTTP 请求扫描器 (http-requests)

## Overview

HTTP 请求扫描器用于分析 Python 代码中的 HTTP 请求调用。它支持多种流行的 HTTP 客户端库（requests、httpx、aiohttp），能够检测请求方法、URL、参数、超时设置等信息。

该扫描器对于以下场景特别有用：

- 审查外部 API 调用
- 识别同步/异步 HTTP 请求模式
- 检查超时和重试配置
- 分析 HTTP 请求的分布
- 性能优化和监控

## Command Usage

```bash
upcast scan-http-requests [OPTIONS] [PATH]
```

### 参数

- `PATH` - 要扫描的 Python 文件或目录路径（可选，默认为当前目录 `.`）

### 选项

- `-o, --output PATH` - 输出文件路径
- `-v, --verbose` - 启用详细输出
- `--format [yaml|json|markdown]` - 输出格式（默认：yaml）
- `--markdown-language [en|zh]` - Markdown 输出语言（默认：zh）
- `--markdown-title TEXT` - Markdown 输出标题
- `--include PATTERN` - 包含的文件模式（可多次指定）
- `--exclude PATTERN` - 排除的文件模式（可多次指定）
- `--no-default-excludes` - 禁用默认排除模式

### 使用示例

```bash
# 扫描当前目录
upcast scan-http-requests .

# 保存结果到文件
upcast scan-http-requests ./myproject --output http.yaml

# 输出为 JSON 格式
upcast scan-http-requests ./app --format json

# 启用详细模式
upcast scan-http-requests ./services --verbose
```

## 字段说明

### metadata 字段

存放扫描命令的参数和配置信息。

| 字段名       | 类型          | 必填 | 说明               |
| ------------ | ------------- | ---- | ------------------ |
| scanner_name | string        | 是   | 扫描器名称         |
| command_args | array[string] | 否   | 扫描命令的参数列表 |

### summary 字段

`summary` 包含扫描统计信息。

| 字段名           | 类型                 | 必填 | 说明                     |
| ---------------- | -------------------- | ---- | ------------------------ |
| total_requests   | integer              | 是   | HTTP 请求总数            |
| unique_urls      | integer              | 是   | 唯一 URL 数量            |
| by_library       | map[string, integer] | 是   | 按 HTTP 库分组的请求数量 |
| files_scanned    | integer              | 是   | 扫描的文件总数           |
| scan_duration_ms | integer              | 是   | 扫描耗时（毫秒）         |
| total_count      | integer              | 是   | HTTP 请求总数            |

### results 字段

`results` 是一个字典，键为 URL 模式，值为请求详情对象。

#### 请求详情对象

| 字段名  | 类型         | 必填 | 说明                                                  |
| ------- | ------------ | ---- | ----------------------------------------------------- |
| library | string       | 是   | 推导的 HTTP 库名称（`requests`, `httpx`, `aiohttp`）  |
| method  | string       | 是   | 推导的 HTTP 方法（`GET`, `POST`, `PUT`, `DELETE` 等） |
| usages  | array[Usage] | 是   | 使用位置列表                                          |

#### 使用对象（Usage）

| 字段名        | 类型                | 必填 | 说明                                 |
| ------------- | ------------------- | ---- | ------------------------------------ |
| file          | string              | 是   | 文件路径                             |
| line          | integer             | 是   | 行号                                 |
| method        | string              | 是   | HTTP 方法                            |
| statement     | string              | 是   | 完整的请求语句                       |
| is_async      | boolean             | 是   | 是否为异步请求                       |
| session_based | boolean             | 是   | 是否使用 Session                     |
| timeout       | string/integer/null | 是   | 推导的超时时间                       |
| headers       | any/null            | 是   | 推导的请求头，可以是字典或 `null`    |
| params        | any/null            | 是   | 推导的 URL 参数，可以是字典或 `null` |
| form          | any/null            | 是   | 推导的请求体数据（form data）        |
| json          | any/null            | 是   | 推导的请求体数据（JSON）             |

## 示例

以下是扫描结果的示例：

```yaml
metadata: {}
results:
  "https://api.example.com/v1/info":
    library: requests
    method: GET
    usages:
      - file: apiserver/paasng/paasng/accessories/cloudapi/components/http.py
        line: 38
        method: GET
        statement: requests.request(method, url, **kwargs)
        is_async: false
        session_based: false
        timeout: null
        headers: null
        params: null
        form: null
        json: null

  "https://api.example.com/analysis":
    library: requests
    method: GET
    usages:
      - file: apiserver/paasng/paasng/accessories/paas_analysis/clients.py
        line: 118
        method: GET
        statement: requests.get(self.base_url + url, auth=self.auth, timeout=30)
        is_async: false
        session_based: false
        timeout: 30
        headers: null
        params: null
        form: null
        json: null

      - file: apiserver/paasng/paasng/accessories/paas_analysis/clients.py
        line: 128
        method: GET
        statement: "requests.get(self.base_url + url, params={'start_time': start_time.isoformat(), 'end_time': end_time.isoformat()}, auth=self.auth)"
        is_async: false
        session_based: false
        timeout: null
        headers: null
        params:
          start_time: "<start_time.isoformat()>"
          end_time: "<end_time.isoformat()>"
        form: null
        json: null

  "https://metrics.example.com/v1/ingest":
    library: httpx
    method: POST
    usages:
      - file: apiserver/paasng/paasng/services/metrics/client.py
        line: 72
        method: POST
        statement: await client.post("https://metrics.example.com/v1/ingest", json=payload, timeout=timeout)
        is_async: true
        session_based: true
        timeout: "<timeout>"
        headers:
          X-Token: "<token>"
        params: null
        form: null
        json:
          key1: "value1"

  "https://.../tasks":
    library: aiohttp
    method: GET
    usages:
      - file: apiserver/paasng/paasng/tasks/client.py
        line: 40
        method: GET
        statement: 'async with session.get(f"https://{domain}/tasks", params={''limit'': 100}, timeout=10) as resp'
        is_async: true
        session_based: true
        timeout: 10
        headers: null
        params:
          limit: 100
        form: null
        json: null
```

## 注意事项

1. **支持的 HTTP 库**：

   - **requests** - 同步 HTTP 库
   - **httpx** - 支持同步和异步的现代 HTTP 库
   - **aiohttp** - 异步 HTTP 库

2. **HTTP 方法**：扫描器识别常见的 HTTP 方法

   - `GET` - 获取资源
   - `POST` - 创建资源
   - `PUT` - 更新资源
   - `PATCH` - 部分更新
   - `DELETE` - 删除资源
   - `HEAD`, `OPTIONS` 等其他方法

3. **URL 模式**：使用代码静态分析推导 URL 模式，对于不可推导的部分使用 `...` 表示

   - 如 `f"https://api.example.com/users/{user_id}/details"` ，如果 `user_id` 是动态不可推导的，则为 `https://api.example.com/users/.../details`
   - 如 `url = BASE_URL + "/data"` ，如果 `BASE_URL` 无法推导，则为 `.../data`
   - 如 `requests.get(urljoin(BASE_URL, "v1", "info"))`，如果 `BASE_URL` 在上下文为 `https://api.example.com/`，则推导为 `https://api.example.com/v1/info`
   - 对于完全动态的 URL，如 `requests.get(get_url())`，则推导为 `...`
   - 如果有多个连续不可推导部分，则合并为一个 `...`，如 `f"https://{domain}{version}/data"` 推导为 `https://.../data`，当然，如果能推导出部分内容，则保留已知部分，比如 `version` 可推导为 `/v1` 时，则结果为 `https://.../v1/data`

4. **异步检测**：`is_async` 字段标识是否为异步请求：

   - `aiohttp` 的请求始终是异步的
   - `httpx.AsyncClient` 的请求是异步的
   - `requests` 的请求是同步的

5. **Session 使用** ：`session_based` 标识是否使用 Session 对象

6. **超时时间**：`timeout` 字段推导请求的超时时间设置

   - 如果请求中明确设置了超时参数（如 `timeout=5`），则推导为具体值（整数），推导失败时为字符串表达式：`<complex expression>`
   - 如果使用默认超时配置（如 `httpx` 客户端有默认超时），则推导为字符串 `default`
   - 如果未设置超时，则为 `null`

7. **请求参数**：推导的请求参数，无法推导部分用尖括号包含代码片段表示，如 `<complex expression>`。

   - `headers` - 自定义请求头
   - `params` - URL 查询参数
   - `form` - 表单数据
   - `json` - JSON 数据
