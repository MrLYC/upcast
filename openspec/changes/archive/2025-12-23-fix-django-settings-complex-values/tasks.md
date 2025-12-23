# Tasks: Fix Django Settings Complex Values

## Implementation Tasks

- [x] 改进 `upcast/scanners/django_settings.py` 中的 `_infer_value()` 方法

  - [x] 添加辅助方法 `_extract_value()` 用于递归提取值
  - [x] 支持字典类型的提取
  - [x] 支持嵌套列表的提取
  - [x] 改进语句生成逻辑

- [x] 更新测试

  - [x] 在 `tests/test_scanners/test_django_settings.py` 添加复杂值测试用例
  - [x] 验证包含字典的列表
  - [x] 验证嵌套结构
  - [x] 确保覆盖率不低于 80%

- [x] 重新生成示例输出

  - [x] 运行 `uv run upcast scan-django-settings example/blueking-paas --format yaml > example/scan-results/django-settings.yaml`
  - [x] 验证 `AUTH_PASSWORD_VALIDATORS` 等复杂配置正确显示

- [x] 验证和归档
  - [x] 运行 `openspec validate fix-django-settings-complex-values --strict`
  - [x] 运行完整测试套件 `uv run pytest`
  - [x] 确保 ruff check 通过
