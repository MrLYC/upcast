# Design: Use Git Diff for CI Baseline Comparison

## Overview

替换基于文件系统的 baseline 对比机制为基于 Git diff 的对比机制，简化 CI 集成测试流程。

## Current Implementation

### Baseline 目录结构

```
example/
├── scan-results/              # 扫描输出
│   ├── blocking-operations.yaml
│   ├── complexity-patterns.yaml
│   └── ...
└── scan-results-baseline/     # 基线（需要手动维护）
    ├── blocking-operations.yaml
    ├── complexity-patterns.yaml
    └── ...
```

### 当前工作流

1. CI checkout 代码
2. 运行 `make test-integration` 生成 `example/scan-results/*.yaml`
3. 对比 `scan-results` 和 `scan-results-baseline` 目录
4. 如果不匹配，CI 失败
5. 开发者需要手动更新 baseline：
   ```bash
   make test-integration
   cp -r example/scan-results/* example/scan-results-baseline/
   git add example/scan-results-baseline/
   git commit -m 'Update scanner baseline'
   ```

### 问题分析

- **状态不一致**：`scan-results` 可能与 `scan-results-baseline` 不同步
- **手动操作**：更新 baseline 需要多个命令
- **磁盘占用**：重复存储相同数据
- **Git 历史**：baseline 变更会产生大量提交

## Proposed Design

### 新的工作流

1. CI checkout 代码（包含已提交的 `example/scan-results/*.yaml`）
2. 在临时目录运行 `make test-integration`
3. 使用 `yq` 提取新旧结果的 `results` 部分
4. 使用 `git diff` 对比 `example/scan-results/` 的变化
5. 如果有变化：
   - 显示 diff
   - 提供建议（可能是扫描器改进或 bug）
   - 说明如何接受：直接 commit 新结果

### 目录结构

```
example/
├── scan-results/              # 唯一的扫描结果（版本控制）
│   ├── blocking-operations.yaml
│   ├── complexity-patterns.yaml
│   └── ...
└── blueking-paas/             # 测试项目
```

### Git Diff 实现

#### 选项 1：直接 diff YAML 文件（简单但不精确）

```bash
git diff example/scan-results/
```

**问题**：会包含 metadata 变化（scan_duration_ms、timestamp 等）

#### 选项 2：提取 results 后 diff（推荐）

```bash
#!/bin/bash
set -e

RESULTS_DIR="example/scan-results"
DIFF_FOUND=0

echo "📊 Checking for scan result changes..."

for file in "$RESULTS_DIR"/*.yaml; do
  filename=$(basename "$file")

  # 提取 committed version 的 results 部分
  git show "HEAD:$file" | yq '.results' > /tmp/old-results.yaml 2>/dev/null || echo "null" > /tmp/old-results.yaml

  # 提取 current version 的 results 部分
  yq '.results' "$file" > /tmp/new-results.yaml 2>/dev/null || echo "null" > /tmp/new-results.yaml

  # 对比
  if ! diff -u /tmp/old-results.yaml /tmp/new-results.yaml > /tmp/diff-$filename 2>&1; then
    echo "⚠️  Results changed in $filename:"
    echo "----------------------------------------"
    cat /tmp/diff-$filename | head -50
    echo "----------------------------------------"
    DIFF_FOUND=1
  else
    echo "✅ $filename: no changes"
  fi
done

if [ $DIFF_FOUND -eq 1 ]; then
  echo ""
  echo "::warning::Scanner results changed. Review diffs above."
  echo ""
  echo "If changes are intentional (scanner improvements):"
  echo "  1. Review the diffs to ensure they are correct"
  echo "  2. Run: make test-integration"
  echo "  3. Commit: git add example/scan-results/ && git commit -m 'Update scan results'"
  echo ""
  echo "If changes are unexpected (possible bugs):"
  echo "  1. Investigate which code change caused the diff"
  echo "  2. Fix the scanner or revert the problematic change"
  exit 1
fi

echo "✅ All scan results match committed baseline"
```

#### 选项 3：使用 Git worktree（更复杂但更健壮）

```bash
# 创建临时 worktree
git worktree add /tmp/baseline HEAD

# 在临时目录运行扫描
cd /tmp/baseline
make test-integration

# 对比
diff -ur /tmp/baseline/example/scan-results example/scan-results

# 清理
git worktree remove /tmp/baseline
```

**选择**：使用选项 2（提取 results 后 diff），因为：

- 不需要额外的 worktree
- 可以精确过滤 metadata
- 实现简单，容易理解

### 处理首次运行

当某个扫描器是新的（文件不存在于 Git 历史中）：

```bash
if ! git ls-files --error-unmatch "$file" >/dev/null 2>&1; then
  echo "⚠️  $filename is new (not in git history yet)"
  echo "    This is expected for new scanners."
  echo "    Commit the file to establish baseline."
  continue
fi
```

### 处理文件缺失

如果扫描器被移除或重命名：

```bash
# 检查 git 中有但文件系统中没有的文件
for committed_file in $(git ls-files "example/scan-results/*.yaml"); do
  if [ ! -f "$committed_file" ]; then
    echo "⚠️  $(basename $committed_file) was removed or renamed"
  fi
done
```

## Implementation Strategy

### Phase 1: 修改 CI 工作流

1. 更新 `.github/workflows/scanner-integration.yml`
2. 移除 baseline 目录相关逻辑
3. 添加 Git diff 对比逻辑
4. 测试 CI 行为

### Phase 2: 清理仓库

1. 如果存在 `example/scan-results-baseline/`，删除它
2. 更新 `.gitignore`（如果有相关条目）
3. 提交清理

### Phase 3: 更新文档

1. 更新 README.md 中的集成测试说明
2. 更新 `testing-infrastructure` spec
3. 移除所有关于 baseline 目录的引用

## Testing Plan

1. **本地测试**

   - 修改一个扫描器的输出
   - 运行修改后的 CI 脚本
   - 验证能正确检测到变化

2. **CI 测试**

   - 创建测试 PR
   - 修改扫描结果文件
   - 验证 CI 报告变化
   - 验证 diff 输出清晰

3. **新扫描器测试**
   - 添加新扫描器（不在 Git 中）
   - 验证 CI 正确处理新文件

## Rollback Plan

如果新方案有问题：

1. Revert CI workflow 到旧版本
2. 恢复 `example/scan-results-baseline/` 目录（从 Git 历史）
3. 运行 `make test-integration`
4. 复制结果到 baseline

## Success Criteria

- ✅ CI 能正确检测扫描结果变化
- ✅ Diff 输出清晰易懂
- ✅ 不需要 baseline 目录
- ✅ 新扫描器能正常工作
- ✅ 文档准确反映新流程
