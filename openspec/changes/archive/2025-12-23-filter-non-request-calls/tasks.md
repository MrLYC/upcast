# Tasks: Filter Non-Request Calls

## Implementation Tasks

- [ ] 修改 `upcast/scanners/http_requests.py`

  - [ ] 添加 `EXCLUDED_PATTERNS` 类变量定义黑名单
  - [ ] 修改 `_identify_request()` 方法，添加黑名单检查
  - [ ] 确保白名单（HTTP 方法）优先级高于黑名单

- [ ] 添加测试用例

  - [ ] `test_scanner_excludes_request_exception`：测试异常不被识别
  - [ ] `test_scanner_excludes_response_class`：测试 Response 不被识别
  - [ ] `test_scanner_excludes_auth_classes`：测试认证类不被识别
  - [ ] `test_scanner_excludes_instrumentor`：测试工具类不被识别
  - [ ] 确保现有测试通过（真实请求仍被识别）

- [ ] 重新生成示例输出

  - [ ] 运行 `uv run upcast scan-http-requests example/blueking-paas --format yaml > example/scan-results/http-requests.yaml`
  - [ ] 验证不再有 `faked requests exception` 等非请求条目
  - [ ] 验证 `RequestException`、`Response`、`Adapter` 等不被识别

- [ ] 验证和归档
  - [ ] 运行完整测试套件 `uv run pytest`
  - [ ] 确保 ruff check 通过
  - [ ] 归档变更
