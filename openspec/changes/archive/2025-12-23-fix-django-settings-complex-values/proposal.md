# Change Proposal: Fix Django Settings Complex Values

## Overview

修复 Django settings 扫描器对复杂值的处理，正确序列化包含字典、元组等复杂类型的列表，而不是简单地用 `...` 占位符替代。

## Problem

当前 `DjangoSettingsScanner._infer_value()` 方法在处理列表时，只能正确提取 `Const` 类型的简单元素。对于字典、元组等复杂类型，直接使用 `...` 作为占位符，导致输出信息不完整。

例如 `AUTH_PASSWORD_VALIDATORS` 配置：

```python
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]
```

当前输出为：

```yaml
value:
  - "..."
  - "..."
```

期望输出应该是完整的字典结构。

## Solution

改进 `_infer_value()` 方法，递归处理复杂数据结构：

- 对于列表元素，递归处理每个元素
- 对于字典，尝试提取键值对
- 对于其他复杂类型，提供更有意义的表示

## Impact

- **受影响组件**: Django settings scanner
- **向后兼容性**: 输出格式兼容，但内容更完整
- **测试更新**: 需要更新测试用例以验证复杂值处理

## Alternatives Considered

1. **保持现状**: 继续使用 `...`，但信息不完整
2. **完全序列化**: 使用 `ast.literal_eval`，但可能失败
3. **渐进增强**: 先支持字典，后续扩展其他类型（采用）
