# 单元测试扫描器 (unit-tests)

## 概述

单元测试扫描器用于分析 Python 代码中的单元测试。它支持 pytest 和 unittest 框架，能够检测测试函数、计算 MD5 哈希、统计断言数量、并根据导入和模块结构解析测试目标。

该扫描器对于以下场景特别有用：

- 评估测试覆盖度
- 识别测试目标和依赖
- 生成测试文档
- 追踪测试变更（通过 MD5）
- 测试质量分析

## 命令使用

```bash
upcast scan-unit-tests [OPTIONS] [PATH]
```

### 参数

- `PATH` - 要扫描的 Python 文件或目录路径（可选，默认为当前目录 `.`）

### 选项

- `-o, --output PATH` - 输出文件路径（YAML 或 JSON）
- `--format [yaml|json|markdown]` - 输出格式（默认：yaml）
- `--markdown-language [en|zh]` - Markdown 输出语言（默认：zh）
- `--markdown-title TEXT` - Markdown 输出标题
- `-v, --verbose` - 启用详细日志
- `--include PATTERN` - 包含的文件模式（例如：`test_*.py`）
- `--exclude PATTERN` - 排除的文件模式（例如：`__pycache__/**`）
- `--no-default-excludes` - 禁用默认排除模式
- `-r, --root-modules MODULE` - 根模块前缀（可多次指定，用于目标解析）
- `-e, --exclude-modules MODULE` - 排除的模块目标（可多次指定）

### 使用示例

```bash
# 扫描 tests 目录
upcast scan-unit-tests ./tests

# 指定根模块
upcast scan-unit-tests ./tests --root-modules app

# 指定多个根模块
upcast scan-unit-tests ./tests -r app -r mylib -v

# 保存结果到 JSON 文件
upcast scan-unit-tests ./tests --output results.json --format json

# 仅扫描特定模式的测试文件
upcast scan-unit-tests . --include "test_*.py"
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

| 字段名           | 类型    | 必填 | 说明             |
| ---------------- | ------- | ---- | ---------------- |
| total_tests      | integer | 是   | 测试函数总数     |
| total_assertions | integer | 是   | 断言总数         |
| total_files      | integer | 是   | 测试文件总数     |
| files_scanned    | integer | 是   | 扫描的文件总数   |
| scan_duration_ms | integer | 是   | 扫描耗时（毫秒） |
| total_count      | integer | 是   | 测试函数总数     |

### results 字段

`results` 是一个字典，键为测试文件路径，值为该文件中的测试函数列表。

#### 测试函数对象

| 字段名       | 类型           | 必填 | 说明                              |
| ------------ | -------------- | ---- | --------------------------------- |
| file         | string         | 是   | 测试文件路径                      |
| name         | string         | 是   | 测试函数名称                      |
| line_range   | array[integer] | 是   | 行号范围 `[start_line, end_line]` |
| assert_count | integer        | 是   | 断言语句数量                      |
| body_md5     | string         | 是   | 测试函数体的 MD5 哈希值           |
| targets      | array[Target]  | 是   | 测试目标列表（基于导入推断）      |

#### 测试目标对象（Target）

| 字段名      | 类型    | 必填 | 说明             |
| ----------- | ------- | ---- | ---------------- |
| module_path | string  | 是   | 目标模块路径     |
| lineno      | integer | 否   | 引用语句所在行号 |
| statement   | string  | 否   | 完整引用语句     |

## 使用示例

以下是扫描结果的示例：

```yaml
metadata:
  scanner_name: unit-tests
  command_args:
    - scan-unit-tests
    - /path/to/project/tests
    - --root-modules
    - myapp
    - --format
    - yaml

summary:
  total_tests: 8
  total_assertions: 25
  total_files: 3
  files_scanned: 45
  scan_duration_ms: 2345
  total_count: 8

results:
  tests/test_user_service.py:
    - assert_count: 3
      body_md5: a1b2c3d4e5f6789012345678abcdef01
      file: tests/test_user_service.py
      line_range:
        - 15
        - 28
      name: test_create_user_with_valid_data
      targets:
        - module_path: myapp.services.user_service.UserService
          lineno: 8
          statement: "service = UserService()"
        - module_path: myapp.models.user.User
          lineno: 9
          statement: "value = User.objects.create(...)"

    - assert_count: 2
      body_md5: b2c3d4e5f6789012345678abcdef0123
      file: tests/test_user_service.py
      line_range:
        - 30
        - 42
      name: test_update_user_email
      targets:
        - module_path: myapp.services.user_service
          lineno: 8
          statement: "user_service.update_email(user_id, new_email)"

    - assert_count: 1
      body_md5: c3d4e5f6789012345678abcdef012345
      file: tests/test_user_service.py
      line_range:
        - 44
        - 52
      name: test_delete_user
      targets:
        - module_path: myapp.services.user_service
          lineno: 8
          statement: "user_service.delete_user(user_id)"
        - module_path: myapp.exceptions.DomainErrors
          lineno: 10
          statement: "except DomainErrors.UserNotFound as e:"
```

## 注意事项

1. **测试框架支持**：

   **pytest**：

   - 测试函数以 `test_` 开头
   - 测试类以 `Test` 开头

   **unittest**：

   - 继承 `unittest.TestCase`
   - 测试方法以 `test_` 开头

2. **断言统计** - `assert_count` 统计以下断言：

   - `assert` 语句（pytest）
   - `self.assertEqual()`, `self.assertTrue()` 等（unittest）
   - 断言数量可以作为测试质量的一个指标
   - 过多或过少的断言都可能有问题

3. **MD5 哈希** - `body_md5` 用于：

   - 追踪测试代码变更
   - 检测重复或相似的测试
   - 版本控制和变更追踪
   - 计算范围是测试函数体（不含函数签名）

4. **目标解析** - `targets` 基于导入语句推断：

   - 列出测试目标引用的模块和符号
   - 通过 `--root-modules` 指定项目根模块提高精确度
   - 排除不相关模块，通过 `--exclude-modules` 参数指定
   - 帮助理解测试覆盖范围
   - 识别测试依赖

5. **根模块前缀** - `--root-modules` 参数：

   - 指定项目的根包名（如 `app`, `mylib`）
   - 帮助区分项目代码和第三方库
   - 提高目标解析的准确性
   - 可以指定多个根模块

6. **行号范围** - `line_range` 表示测试函数的代码范围：

   - 格式：`[起始行, 结束行]`
   - 包含函数签名到最后一行代码
   - 用于定位和代码跳转
