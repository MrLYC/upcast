# Extract Django Field Metadata from Parameters

## Problem

当前 Django 模型扫描器将字段的所有参数（包括描述性元数据）统一放在 `parameters` 字典中输出到 Markdown 报告里。这导致 `help_text`、`verbose_name` 等用户可读的描述信息被埋没在技术参数中，不便于阅读。

示例（当前输出）：

```markdown
| 字段名            | 类型                 | 行号 | 参数                                                                                              |
| ----------------- | -------------------- | ---- | ------------------------------------------------------------------------------------------------- |
| logs_was_ready_at | models.DateTimeField | 1    | {"help_text": "Pod 状态就绪允许读取日志的时间", "null": true}                                     |
| completed_at      | models.DateTimeField | 1    | {"help_text": "failed/successful/interrupted 都是完成", "null": true, "verbose_name": "完成时间"} |
```

## Proposed Solution

将字段的描述性元数据（`help_text`、`verbose_name`）从 `parameters` 中提取出来，作为 `DjangoField` 的独立属性，并在 Markdown 报告中单独展示为列。

期望输出：

```markdown
| 字段名            | 类型                 | 行号 | 说明                                   | 显示名称 | 参数           |
| ----------------- | -------------------- | ---- | -------------------------------------- | -------- | -------------- |
| logs_was_ready_at | models.DateTimeField | 1    | Pod 状态就绪允许读取日志的时间         | -        | {"null": true} |
| completed_at      | models.DateTimeField | 1    | failed/successful/interrupted 都是完成 | 完成时间 | {"null": true} |
```

## Benefits

1. **可读性提升**: 字段说明和显示名称一目了然
2. **信息层次清晰**: 区分描述性元数据和技术参数
3. **符合 Django 最佳实践**: 反映 Django 字段定义中 `help_text` 和 `verbose_name` 的重要性

## Scope

- 修改 `DjangoField` 数据模型，添加 `help_text` 和 `verbose_name` 属性
- 修改 Django 模型扫描器，从 parameters 中提取这两个字段
- 更新 Markdown 模板（中英文），增加对应的列
- 更新单元测试
- 保持 YAML/JSON 输出向后兼容

## Out of Scope

- 提取其他字段元数据（如 `choices`、`validators` 等）
- 修改其他扫描器

## Related Changes

- None
