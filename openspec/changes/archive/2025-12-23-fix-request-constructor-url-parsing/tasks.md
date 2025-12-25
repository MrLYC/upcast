# Tasks: Fix Request Constructor URL Parsing

## Implementation Tasks

- [x] 修改 `upcast/scanners/http_requests.py`

  - [x] 添加 `_is_request_constructor()` 方法检测 Request 构造器调用
  - [x] 修改 `_extract_url()` 方法，根据调用类型选择参数位置
  - [x] 修改 `_check_request_call()` 方法，正确提取 Request 的 method
  - [x] 处理命名参数场景（`url=...`, `method=...`）

- [x] 添加测试用例

  - [x] `test_request_constructor_positional_args`：测试 `Request('GET', 'url')`
  - [x] `test_request_constructor_keyword_args`：测试 `Request(method='GET', url='...')`
  - [x] `test_request_constructor_mixed_args`：测试 `Request('GET', url='...')`
  - [x] 确保现有测试通过（回归测试）

- [x] 重新生成示例输出

  - [x] 运行 `uv run upcast scan-http-requests example/blueking-paas --format yaml > example/scan-results/http-requests.yaml`
  - [x] 验证不再有 "GET", "POST" 作为 URL 键
  - [x] 验证 `Request()` 调用被正确分组

- [x] 验证和归档
  - [x] 运行完整测试套件 `uv run pytest`
  - [x] 确保 ruff check 通过
  - [x] 归档变更
