# Proposal: Use Git Diff for CI Baseline Comparison

## Why

当前 CI 集成测试需要维护一个独立的 `example/scan-results-baseline/` 目录来存储扫描结果基线，这带来了以下问题：

1. **维护负担**：每次扫描器行为变化时，需要手动复制文件并提交 baseline 目录
2. **仓库膨胀**：扫描结果文件会被双份存储（scan-results 和 scan-results-baseline）
3. **容易出错**：开发者可能忘记更新 baseline，导致 CI 失败
4. **首次运行问题**：新扫描器没有 baseline 时会产生警告，需要额外步骤建立 baseline

实际上，Git 本身就提供了变更对比功能。我们可以：

- 在 CI 中先 checkout 代码到临时目录
- 运行扫描生成新的结果
- 使用 `git diff` 对比 `example/scan-results/` 目录的变化
- 如果有变化，说明扫描结果被修改了，需要人工审查

这样就不需要单独的 baseline 目录了。

## What Changes

### 核心修改

修改 `.github/workflows/scanner-integration.yml` 工作流：

1. **移除 baseline 目录依赖**

   - 不再使用 `example/scan-results-baseline/` 目录
   - 移除所有关于复制和提交 baseline 的说明

2. **使用 Git diff 对比**

   - 扫描前记录 `example/scan-results/` 的 Git 状态
   - 运行扫描后使用 `git diff` 检查文件变化
   - 只对比 `results` 部分（排除 metadata 如 scan_duration_ms）

3. **改进输出信息**
   - 如果有变化，显示完整的 diff 内容
   - 提供清晰的说明：变化可能是预期的（扫描器改进）或非预期的（bug）
   - 说明如何接受变化：简单地 commit 新的结果即可

### 工作流程

```yaml
- name: Run integration tests
  run: make test-integration

- name: Check for scan result changes
  run: |
    # 只对比 results 部分，忽略 metadata
    for file in example/scan-results/*.yaml; do
      # 提取 results 部分进行对比
      if git diff --exit-code "$file" -- | grep -v 'scan_duration_ms\|timestamp'; then
        echo "✅ $file: no changes"
      else
        echo "⚠️  $file: results changed"
        git diff "$file"
      fi
    done

    # 如果有任何变化，提示审查
    if ! git diff --quiet example/scan-results/; then
      echo "::warning::Scanner results changed. Review diffs above."
      echo "If changes are intentional, commit them to accept the new baseline."
    fi
```

### 影响范围

- **文件修改**：`.github/workflows/scanner-integration.yml`
- **目录移除**：`example/scan-results-baseline/`（如果存在）
- **文档更新**：`README.md` 中关于 baseline 的说明

## Benefits

1. **简化维护**：不需要手动管理 baseline 目录
2. **减少仓库大小**：移除重复的扫描结果文件
3. **更清晰的变更追踪**：通过 Git 历史可以看到扫描结果的演变
4. **降低门槛**：新贡献者不需要理解 baseline 机制
5. **自动化**：接受新的扫描结果只需要 commit，无需额外步骤

## Risks & Mitigations

| Risk                                        | Mitigation                                                        |
| ------------------------------------------- | ----------------------------------------------------------------- |
| Git diff 可能不够精确（包含 metadata 变化） | 使用 yq 提取 results 部分再对比，或在 diff 时过滤掉 metadata 字段 |
| 首次运行时 example/scan-results/ 可能不存在 | 在 Makefile 中确保目录存在，或在 CI 中初始化                      |
| 开发者可能不理解为什么 CI 报告变化          | 在输出中提供清晰的说明和文档链接                                  |

## Alternatives Considered

1. **保持当前 baseline 目录方案**

   - ❌ 维护负担重，容易出错

2. **使用外部服务存储 baseline**

   - ❌ 增加复杂度，引入外部依赖

3. **完全不对比，只运行测试**

   - ❌ 失去回归检测能力

4. **使用 Git diff（推荐）**
   - ✅ 简单、可靠、零额外成本
