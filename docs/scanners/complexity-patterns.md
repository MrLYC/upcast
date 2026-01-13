# 复杂度模式扫描器

## 概述

复杂度模式扫描器用于分析 Python 代码的圈复杂度（Cyclomatic Complexity）。它能够识别过于复杂的函数，帮助开发者发现需要重构的代码。

该扫描器对于以下场景特别有用：

- 识别需要重构的复杂函数
- 代码质量评估
- 技术债务分析
- 制定重构优先级
- 代码审查指导

## 命令用法

```bash
upcast scan-complexity-patterns [OPTIONS] [PATH]
```

### 参数

- `PATH` - 要扫描的 Python 文件或目录路径（可选，默认为当前目录 `.`）

### 选项

- `-o, --output PATH` - 输出文件路径
- `-v, --verbose` - 启用详细输出
- `--format [yaml|json|markdown]` - 输出格式（默认：yaml）
- `--markdown-language [en|zh]` - Markdown 输出语言（默认：zh）
- `--markdown-title TEXT` - Markdown 输出标题
- `--threshold INTEGER` - 最小复杂度阈值（默认：11）
- `--include PATTERN` - 包含的文件模式（可多次指定）
- `--exclude PATTERN` - 排除的文件模式（可多次指定）
- `--no-default-excludes` - 禁用默认排除模式
- `--critical-level INTEGER` - 严重复杂度阈值（默认：21）
- `--high-risk-level INTEGER` - 高风险复杂度阈值（默认：16）
- `--warning-level INTEGER` - 警告复杂度阈值（默认：11）

### 使用示例

```bash
# 扫描当前目录，使用默认阈值 11
upcast scan-complexity-patterns .

# 设置更低的阈值以发现更多复杂函数
upcast scan-complexity-patterns ./src --threshold 5

# 保存结果到文件
upcast scan-complexity-patterns ./myproject --output complexity.yaml

# 输出为 JSON 格式
upcast scan-complexity-patterns ./app --format json
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

| 字段名                | 类型             | 必填 | 说明               |
| --------------------- | ---------------- | ---- | ------------------ |
| high_complexity_count | integer          | 是   | 高复杂度函数数量   |
| by_severity           | map[string, int] | 是   | 按严重程度分组统计 |
| files_scanned         | integer          | 是   | 扫描的文件总数     |
| scan_duration_ms      | integer          | 是   | 扫描耗时（毫秒）   |
| total_count           | integer          | 是   | 高复杂度函数数量   |

#### by_severity 字段

按复杂度严重程度分组：

- `critical` - 严重，必须重构（复杂度 >= 21，可被 `--critical-level` 参数调整）
- `high_risk` - 高风险，建议重构（复杂度 16-20，可被 `--high-risk-level` 参数调整）
- `warning` - 警告，考虑重构（复杂度 11-15，可被 `--warning-level` 参数调整）
- `acceptable` - 可接受（复杂度 < 11）

### results 字段

`results` 是一个字典，键为文件路径，值为该文件中的复杂函数列表。

#### 复杂函数对象（ComplexFunction）

| 字段名        | 类型    | 必填 | 说明                                                    |
| ------------- | ------- | ---- | ------------------------------------------------------- |
| name          | string  | 是   | 函数名称                                                |
| line          | integer | 是   | 函数定义起始行号                                        |
| end_line      | integer | 是   | 函数定义结束行号                                        |
| complexity    | integer | 是   | 圈复杂度值                                              |
| signature     | string  | 是   | 函数签名                                                |
| description   | string  | 否   | 函数描述（来自 docstring ）                             |
| code          | string  | 是   | 完整的函数源代码                                        |
| code_lines    | integer | 是   | 代码行数（不含注释）                                    |
| comment_lines | integer | 是   | 注释行数                                                |
| severity      | string  | 是   | 严重程度（`acceptable`, `warning`, `high`, `critical`） |
| message       | string  | 是   | 描述信息                                                |

## Examples

以下是扫描结果的示例：

```yaml
metadata:
   scanner_name: complexity-patterns
   command_args:
      - scan-complexity-patterns
      - --format yaml
      - ./src
summary:
   high_complexity_count: 4
   by_severity:
      critical: 1
      high_risk: 1
      warning: 1
      acceptable: 1
   files_scanned: 12
   scan_duration_ms: 180
   total_count: 4
results:
   apiserver/paasng/paas_wl/bk_app/cnative/specs/resource.py:
      - name: detect_state
         line: 183
         end_line: 204
         complexity: 10
         signature: "def detect_state(self) -> ModelResState:"
         description: Detect the final state from status.conditions
         code: |
            def detect_state(self) -> ModelResState:
                  """Detect the final state from status.conditions"""
                  if not self.mres.status.conditions:
                        return ModelResState(DeployStatus.PENDING, 'Pending', 'state not initialized')
                  if self.mres.status.phase == MResPhaseType.AppRunning:
                        available = self._find_condition(MResConditionType.APP_AVAILABLE)
                        if available and available.status == ConditionStatus.TRUE:
                              return ModelResState(DeployStatus.READY, available.reason, available.message)
                  if self.mres.status.phase == MResPhaseType.AppFailed:
                        reasons: List[str] = []
                        messages: List[str] = []
                        for cond in self.mres.status.conditions:
                              if cond.status == ConditionStatus.FALSE and cond.message:
                                    reasons.append(cond.reason)
                                    messages.append(cond.message)
                        if messages:
                              return ModelResState(DeployStatus.ERROR, '\n'.join(reasons), '\n'.join(messages))
                        return ModelResState(DeployStatus.ERROR, 'Unknown', '')
                  return ModelResState(DeployStatus.PROGRESSING, 'Progressing', 'progressing')
         code_lines: 22
         comment_lines: 0
         severity: acceptable
         message: Complexity 10 is acceptable
   apiserver/paasng/paas_wl/bk_app/dev_sandbox/kres_slzs/ingress.py:
      - name: serialize
         line: 89
         end_line: 145
         complexity: 15
         signature: "def serialize(self, obj: 'DevSandboxIngress', ...) -> Dict:"
         description: serialize obj into Ingress(networking.k8s.io/v1)
         code: |
            def serialize(self, obj: 'DevSandboxIngress', ...) -> Dict:
                  # ...function body...
         code_lines: 57
         comment_lines: 3
         severity: warning
         message: Complexity 15 exceeds warning threshold
   apiserver/paasng/paas_wl/bk_app/utils/critical_func.py:
      - name: process_all
         line: 10
         end_line: 80
         complexity: 22
         signature: "def process_all(self, items: List[Any]) -> None:"
         description: Process all items with error handling and logging
         code: |
            def process_all(self, items: List[Any]) -> None:
                  # ...critical logic...
         code_lines: 65
         comment_lines: 5
         severity: critical
         message: Complexity 22 exceeds critical threshold
   apiserver/paasng/paas_wl/bk_app/utils/high_risk_func.py:
      - name: calculate_metrics
         line: 20
         end_line: 70
         complexity: 18
         signature: "def calculate_metrics(self, data: Dict) -> Dict:"
         description: Calculate metrics from input data
         code: |
            def calculate_metrics(self, data: Dict) -> Dict:
                  # ...high risk logic...
         code_lines: 45
         comment_lines: 2
         severity: high_risk
         message: Complexity 18 exceeds high risk threshold
```

## Notes

1. **圈复杂度** - 衡量代码路径数量的指标：

   - 每个决策点（if, elif, for, while, except, and, or 等）增加 1
   - 基础复杂度为 1
   - 值越高，代码越难理解和测试

2. **代码统计**：

   - `code_lines` - 实际代码行数（不含空行和注释）
   - `comment_lines` - 注释行数
   - 长函数通常也是复杂函数的特征

3. **函数签名** - `signature` 字段显示函数定义：

   - 包含参数名、类型提示、返回类型和装饰器
   - 有助于理解函数接口

4. **描述信息** - `description` 来自 docstring ：

   - 帮助快速了解函数用途
   - 如果没有 docstring 则为空

5. **完整代码** - `code` 字段包含完整源代码：

   - 便于直接查看问题代码
   - 可以用于生成报告
   - 对于非常长的函数，可能截断显示
