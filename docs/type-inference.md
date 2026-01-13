# Upcast 类型推导机制文档

## 概述

Upcast 的类型推导系统基于 **astroid** 静态分析库构建，通过 AST（抽象语法树）分析实现**无需执行代码**的类型和值推导。本文档详细说明推导能力、实现机制和使用场景。

**设计原则**：
- ✅ **安全优先**：不执行任何代码，完全静态分析
- ✅ **实用主义**：不追求 100% 精确，但覆盖常见场景
- ✅ **结构化返回**：使用数据类封装推导结果，便于编程处理
  - `InferenceResult` - 通用推导结果（值 + 置信度 + 静态标记）
  - `StringPattern` - 字符串模式（静态部分 + 动态标记）
- ✅ **优雅降级**：
  - **完全静态**：`InferenceResult(42, "exact", True)`
  - **部分推导**：`StringPattern(["api/", ..., "/users"])` → `"api/.../users"`
  - **完全动态**：`InferenceResult(None, "unknown", False)`

---

## 推导能力分级

本文档使用统一的分级语义：

| 级别       | 含义                                      | 返回结果                                          |
| ---------- | ----------------------------------------- | ------------------------------------------------- |
| ✅ 可推导  | 在静态分析下**稳定、确定**                | `InferenceResult(42, "exact", True)`              |
| ⚠️ 部分推导 | 类型可推导，但值包含动态部分              | `InferenceResult("api/...", "partial", False)`    |
| ❌ 不可推导 | 必须退化为 unknown                        | `InferenceResult(None, "unknown", False)`         |

**结构化返回的优势**：
- ✅ 调用方可以明确判断推导质量（通过 `confidence` 字段）
- ✅ 可以区分完全静态和包含动态部分（通过 `is_static` 字段）
- ✅ 保留原始 AST 节点（通过 `node` 字段），便于调试和进一步分析
- ✅ 字符串模式可以提取静态前缀、命名空间等有用信息

---

## 核心 API

Upcast 在 `upcast.common.ast_utils` 模块提供以下核心推导函数：

### 1. 结构化推导 API（推荐）

#### `InferenceResult` - 推导结果数据类

```python
@dataclass
class InferenceResult:
    """类型/值推导结果（结构化返回值）"""
    value: Any  # 推导出的值
    confidence: Literal["exact", "partial", "unknown"]  # 推导置信度
    is_static: bool  # 是否完全静态（无动态部分）
    node: nodes.NodeNG  # 原始 AST 节点

    @property
    def is_dynamic(self) -> bool:
        """是否包含动态部分"""
        return not self.is_static
```

**置信度说明**：

| 置信度 | 含义 | 示例 |
|--------|------|------|
| `exact` | 完全静态，值确定 | `x = 42` → `InferenceResult(42, "exact", True)` |
| `partial` | 部分推导，包含动态部分 | `f"api/{id}"` → `InferenceResult("api/...", "partial", False)` |
| `unknown` | 完全无法推导 | `func()` → `InferenceResult(None, "unknown", False)` |

**使用示例**：
```python
from upcast.common.ast_utils import infer_value_structured

result = infer_value_structured(node)

if result.confidence == "exact":
    # 完全静态值，可以直接使用
    url = result.value  # "https://api.com/users"
    print(f"Static URL: {url}")

elif result.confidence == "partial":
    # 部分推导，包含动态标记
    pattern = result.value  # "https://api.com/users/..."
    print(f"URL pattern: {pattern}")

    # 可以提取静态前缀
    if isinstance(pattern, str):
        static_prefix = pattern.split("...")[0]
        print(f"Base URL: {static_prefix}")

else:  # unknown
    # 无法推导，记录原始表达式
    expr = result.node.as_string()
    print(f"Dynamic expression: {expr}")
```

---

#### `StringPattern` - 字符串模式数据类

```python
@dataclass
class StringPattern:
    """字符串模式推导结果（专门用于字符串推导）"""
    parts: list[str | Ellipsis]  # 静态部分和动态部分（Ellipsis 表示 ...）

    @property
    def is_static(self) -> bool:
        """是否完全静态"""
        return ... not in self.parts

    def to_pattern(self) -> str:
        """转换为模式字符串（用 ... 标记动态部分）"""
        return "".join("..." if p is ... else p for p in self.parts)

    def static_prefix(self) -> str:
        """获取静态前缀"""
        for i, part in enumerate(self.parts):
            if part is ...:
                return "".join(self.parts[:i])
        return "".join(self.parts)

    def static_parts(self) -> list[str]:
        """获取所有静态部分"""
        return [p for p in self.parts if p is not ...]
```

**使用示例**：
```python
from upcast.common.ast_utils import infer_string_pattern

# f"https://api.com/users/{user_id}/posts/{post_id}"
result = infer_string_pattern(node)

print(result.parts)
# ["https://api.com/users/", ..., "/posts/", ..., ""]

print(result.to_pattern())
# "https://api.com/users/.../posts/..."

print(result.static_prefix())
# "https://api.com/users/"

print(result.static_parts())
# ["https://api.com/users/", "/posts/", ""]

print(result.is_static)
# False
```

**应用场景**：
- **HTTP 请求扫描**：提取 URL 模式和基础 URL
- **Redis 使用扫描**：提取 key 模式和命名空间
- **日志消息分析**：区分静态文本和动态插值

---

### 2. 兼容性 API（现有接口）

#### `infer_value_with_fallback(node) -> tuple[Any, bool]`

**用途**：推导节点的字面量值，失败时返回反引号包裹的表达式。

**返回值**：
- `(value, True)` - 成功推导出字面量值
- `("`expression`", False)` - 失败时返回表达式字符串（用反引号包裹）

**示例**：
```python
from upcast.common.ast_utils import infer_value_with_fallback

# 成功推导
value, success = infer_value_with_fallback(Const(42))
# value = 42, success = True

# 推导失败
value, success = infer_value_with_fallback(Call(...))
# value = "`some_func()`", success = False
```

**注意**：建议使用 `infer_value_structured()` 获得更清晰的结构化结果。

---

#### `infer_type_with_fallback(node) -> tuple[str, bool]`

**用途**：推导节点的 Python 类型。

**返回值**：
- `("int"|"str"|"bool"|"float"|"None", True)` - 成功推导类型
- `("unknown", False)` - 失败时返回 "unknown"

**示例**：
```python
from upcast.common.ast_utils import infer_type_with_fallback

# 字面量
type_name, success = infer_type_with_fallback(Const(42))
# type_name = "int", success = True

# 复杂表达式
type_name, success = infer_type_with_fallback(Call(...))
# type_name = "unknown", success = False
```

---

#### `safe_infer_value(node, default=None) -> Any`

**用途**：简化版值推导，失败时返回默认值（而非反引号表达式）。

**示例**：
```python
from upcast.common.ast_utils import safe_infer_value

value = safe_infer_value(Const(42))
# value = 42

value = safe_infer_value(Name("unknown"), default="N/A")
# value = "N/A"
```

---

#### `get_qualified_name(node) -> tuple[str, bool]`

**用途**：获取类或函数的完全限定名（包括模块路径）。

**示例**：
```python
from upcast.common.ast_utils import get_qualified_name

# Django CharField
qname, success = get_qualified_name(CharField_node)
# qname = "django.db.models.fields.CharField", success = True

# 未知类型
qname, success = get_qualified_name(unknown_node)
# qname = "`UnknownType`", success = False
```

---

## 推导能力详解

### 一、基础值与常量表达式

#### 1.1 字面量（100% 可推导）

```python
a = 1          # ✅ 类型: int,  值: 1
b = 1.5        # ✅ 类型: float, 值: 1.5
c = "hello"    # ✅ 类型: str,  值: "hello"
d = True       # ✅ 类型: bool, 值: True
e = None       # ✅ 类型: None, 值: None
```

**实现**：直接从 `nodes.Const` 节点读取 `.value` 属性。

---

#### 1.2 容器字面量（类型和值都可推导）

```python
a = [1, 2, 3]           # ✅ 类型: list[int], 值: [1, 2, 3]
b = {"x": 1, "y": 2}    # ✅ 类型: dict[str, int], 值: {"x": 1, "y": 2}
c = (1, "x", True)      # ✅ 类型: tuple[int, str, bool], 值: (1, "x", True)
d = {1, 2, 3}           # ✅ 类型: set[int], 值: {1, 2, 3}
```

**实现**：
- `nodes.List` → 递归推导每个元素
- `nodes.Dict` → 递归推导 key-value 对
- `nodes.Tuple` / `nodes.Set` 同理

**代码位置**：`upcast/common/ast_utils.py:66-106`

---

#### 1.3 常量折叠表达式

```python
a = 1 + 2          # ✅ 类型: int, 值: 3
b = 2 * 3          # ✅ 类型: int, 值: 6
c = "a" + "b"      # ✅ 类型: str, 值: "ab"
d = "x" * 3        # ✅ 类型: str, 值: "xxx"
e = True and False # ✅ 类型: bool, 值: False
```

**实现**：依赖 astroid 的常量折叠（Constant Folding）机制。

---

### 二、动态字符串构造（Upcast 扩展）

Upcast 在 astroid 基础上扩展了**字符串模式推导**能力，用于 URL、Redis key 等场景。

**关键规则**：
- ✅ **字符串静态部分**：保留原样
- ✅ **字符串动态部分**：用 `...` 代替
- ❌ **非字符串无法推导**：用 `<dynamic>` 标记

**为什么区分 `...` 和 `<dynamic>`？**
- `...` 仅用于字符串模板，表示"这里有动态内容"，但静态部分仍然可读
- `<dynamic>` 表示"完全不知道这个值是什么"，适用于非字符串类型

#### 2.1 f-string（部分推导）

```python
# 完全静态
url = f"https://api.example.com/users"
# ✅ 推导为: "https://api.example.com/users"

# 包含动态变量
url = f"https://api.example.com/users/{user_id}"
# ⚠️ 推导为: "https://api.example.com/users/..."  # 动态部分用 ...

# 完全动态
url = f"{protocol}://{host}/{path}"
# ⚠️ 推导为 "...://.../..."  # 只有静态空格，其他都是 ...
```

**实现原理**：
遍历 f-string 的各个部分，对于常量节点保留其字面量值，对于变量或表达式节点用 `...` 替代，最后拼接成完整字符串。这样可以保留 URL、Redis key 等字符串模板的静态部分，同时标记出动态部分。

**应用场景**：
- HTTP 请求扫描器：`upcast/scanners/http_requests.py:231-243`
- Redis 使用扫描器：`upcast/scanners/redis_usage.py:133-142`

---

#### 2.2 字符串 format() 方法

```python
# 模板静态，参数动态
url = "https://api.example.com/users/{}".format(user_id)
# ⚠️ 推导为: "https://api.example.com/users/..."  # {} 替换为 ...

key = "cache:{app}:{module}".format(app=app_name, module=mod)
# ⚠️ 推导为: "cache:...:..."  # 多个 {} 都替换为 ...
```

**实现原理**：
从 format() 调用中提取模板字符串，使用正则表达式将所有的占位符（如 `{}`、`{name}` 等）替换为 `...`，保留模板的静态部分。

---

#### 2.3 字符串拼接（BinOp +）

```python
# 完全静态
BASE_URL = "https://api.example.com"
url = BASE_URL + "/users"
# ✅ 推导为: "https://api.example.com/users"

# 部分动态
url = BASE_URL + f"/{endpoint}"
# ⚠️ 推导为: "https://api.example.com/..."  # /endpoint 用 ... 替换
```

**实现原理**：
对于加法运算符（+），递归推导左右两个操作数的值。如果两侧都能成功推导（可能是静态字符串或包含 `...` 的模式），则将它们连接起来；如果任一侧推导失败，则整个表达式返回 None。

---

#### 2.4 百分号格式化（% formatting）

```python
key = "user:%s:session:%d" % (username, session_id)
# ⚠️ 推导为: "user:...:session:..."  # %s, %d 都替换为 ...
```

**实现原理**：
检测到百分号运算符（%）且左侧是常量字符串时，提取模板字符串，使用正则表达式将所有格式化占位符（`%s`、`%d`、`%r` 等）替换为 `...`。

---

### 三、控制流与类型合并

#### 3.1 if / else 分支合并

```python
if condition:
    x = 1
else:
    x = "hello"
```

| 类型                  | 值  |
| --------------------- | --- |
| ✅ `Union[int, str]`   | ❌  |

**实现**：astroid 自动合并多个赋值路径的类型。

---

#### 3.2 单分支 if（可能未定义）

```python
if condition:
    x = 42
# x 可能未定义
```

| 类型                | 值  |
| ------------------- | --- |
| ✅ `Optional[int]`   | ❌  |

---

#### 3.3 三元表达式

```python
x = 1 if flag else "no"
```

| 类型                  | 值  |
| --------------------- | --- |
| ✅ `Union[int, str]`   | ❌  |

---

#### 3.4 and / or 表达式

```python
x = a or 0        # 常见模式：提供默认值
y = a and b       # 短路求值
```

| 表达式  | 类型                           | 值  |
| ------- | ------------------------------ | --- |
| `a or 0` | ✅ `Union[type(a), int]`        | ❌  |
| `a and b` | ✅ `Union[type(a), type(b)]`    | ❌  |

---

### 四、函数与调用

#### 4.1 单一返回值

```python
def get_port():
    return 8080

port = get_port()
```

| 类型    | 值  |
| ------- | --- |
| ✅ `int` | ❌  |

---

#### 4.2 多返回值合并

```python
def get_value(flag):
    if flag:
        return 42
    return "default"

x = get_value(True)
```

| 类型                  | 值  |
| --------------------- | --- |
| ✅ `Union[int, str]`   | ❌  |

---

#### 4.3 无返回值（隐式 None）

```python
def log_message(msg):
    print(msg)

result = log_message("hello")
```

| 类型         | 值       |
| ------------ | -------- |
| ✅ `NoneType` | ✅ `None` |

---

#### 4.4 参数透传（有限推导）

```python
def identity(x):
    return x

a = identity(42)
b = identity("hello")
```

| 变量  | 类型           | 值  |
| ----- | -------------- | --- |
| `a`   | ✅ `int`        | ❌  |
| `b`   | ✅ `str`        | ❌  |
| `identity()` | ⚠️ `Any` / `Union` | ❌  |

**说明**：需要进行**调用点分析**（Call-site Analysis），astroid 有限支持。

---

### 五、类型注解参与推导

#### 5.1 函数签名注解

```python
def fetch_user(user_id: int) -> dict:
    return {"id": user_id}

result = fetch_user(123)
```

| 类型    | 值  |
| ------- | --- |
| ✅ `dict` | ❌  |

**实现**：优先使用 `.returns` 注解，其次推导 `return` 语句。

---

#### 5.2 变量注解

```python
port: int = 8080
name: str = "app"
```

| 类型    | 值      |
| ------- | ------- |
| ✅ `int` | ✅ `8080` |
| ✅ `str` | ✅ `"app"` |

---

### 六、容器构造与推导式

#### 6.1 容器构造函数

```python
a = list([1, 2, 3])
b = dict([("x", 1), ("y", 2)])
c = set([1, 2, 2])
```

| 变量  | 类型                  | 值  |
| ----- | --------------------- | --- |
| `a`   | ✅ `list[int]`         | ❌  |
| `b`   | ✅ `dict[str, int]`    | ❌  |
| `c`   | ✅ `set[int]`          | ❌  |

---

#### 6.2 列表推导式

```python
squares = [x**2 for x in range(10)]
```

| 类型         | 值  |
| ------------ | --- |
| ✅ `list[int]` | ❌  |

---

#### 6.3 字典推导式

```python
mapping = {i: str(i) for i in range(3)}
```

| 类型                  | 值  |
| --------------------- | --- |
| ✅ `dict[int, str]`    | ❌  |

---

### 七、下标与切片

#### 7.1 下标访问

```python
a = [1, 2, 3][0]
```

| 类型    | 值              |
| ------- | --------------- |
| ✅ `int` | ⚠️ `1` (可选实现) |

**说明**：字面量容器的下标**理论上可推导值**，但当前实现未启用。

---

#### 7.2 切片

```python
b = [1, 2, 3][1:]
```

| 类型         | 值  |
| ------------ | --- |
| ✅ `list[int]` | ❌  |

---

### 八、内置函数（白名单）

```python
a = len([1, 2, 3])
b = str(42)
c = int("123")
d = bool(0)
```

| 函数    | 类型     | 值  |
| ------- | -------- | --- |
| `len()` | ✅ `int`  | ❌  |
| `str()` | ✅ `str`  | ❌  |
| `int()` | ✅ `int`  | ❌  |
| `bool()` | ✅ `bool` | ❌  |

---

### 九、类与对象

#### 9.1 实例属性

```python
class User:
    def __init__(self):
        self.id = 1
        self.name = "Alice"

user = User()
uid = user.id
```

| 变量   | 类型    | 值  |
| ------ | ------- | --- |
| `uid`  | ✅ `int` | ❌  |

---

#### 9.2 方法调用

```python
class Calculator:
    def add(self, a, b):
        return a + b

result = Calculator().add(1, 2)
```

| 类型    | 值  |
| ------- | --- |
| ✅ `int` | ❌  |

---

### 十、解构赋值

#### 10.1 元组解包（字面量）

```python
a, b = (1, "hello")
```

| 变量  | 类型    | 值        |
| ----- | ------- | --------- |
| `a`   | ✅ `int` | ✅ `1`     |
| `b`   | ✅ `str` | ✅ `"hello"` |

---

#### 10.2 带 * 的解包

```python
a, *rest = [1, 2, 3, 4]
```

| 变量    | 类型         | 值  |
| ------- | ------------ | --- |
| `a`     | ✅ `int`      | ⚠️  |
| `rest`  | ✅ `list[int]` | ❌  |

---

## 实际应用场景

### 场景 1：HTTP 请求 URL 推导

**代码示例**（来自 `http_requests.py`）：
```python
BASE_URL = "https://api.example.com"

# 情况 1：完全静态
url = BASE_URL + "/users"
# ✅ 推导为: "https://api.example.com/users"

# 情况 2：部分动态
user_id = get_user_id()
url = f"{BASE_URL}/users/{user_id}"
# ⚠️ 推导为: "https://api.example.com/users/..."

# 情况 3：完全动态
url = build_url(endpoint, params)
# ❌ 推导为: "..."
```

**实现位置**：`upcast/scanners/http_requests.py:231-280`

---

### 场景 2：Redis Key 模式推导

**代码示例**（来自 `redis_usage.py`）：
```python
APP_NAME = "myapp"

# 情况 1：静态 key
cache_key = "user:settings"
# ✅ 推导为: "user:settings"

# 情况 2：f-string 模式
cache_key = f"user:{user_id}:session"
# ⚠️ 推导为: "user:...:session"  # user_id 替换为 ...

# 情况 3：format() 调用
cache_key = "cache:{app}:{module}".format(app=APP_NAME, module=mod)
# ⚠️ 推导为: "cache:myapp:..."  # APP_NAME 可推导，module 不可推导

# 情况 4：字符串拼接
cache_key = APP_NAME + ":" + module_name + ":cache"
# ⚠️ 推导为: "myapp:...:cache"  # module_name 替换为 ...
```

**实现位置**：`upcast/scanners/redis_usage.py:99-169`

---

### 场景 3：环境变量默认值推导

**代码示例**（来自 `env_var_scanner.py`）：
```python
# 情况 1：字面量默认值
port = os.getenv("PORT", "8080")
# ✅ 类型: str, 默认值: "8080"

# 情况 2：类型转换 + 默认值
port = int(os.getenv("PORT", "8080"))
# ✅ 类型: int, 默认值: 8080

# 情况 3：动态默认值
port = os.getenv("PORT", get_default_port())
# ⚠️ 类型: str, 默认值: <dynamic> (或 `` `get_default_port()` `` )
```

**实现**：使用 `infer_value_with_fallback()` 推导第二个参数。

---

### 场景 4：日志消息格式推导

**代码示例**（来自 `logging_scanner.py`）：
```python
# 情况 1：字符串字面量
logger.info("User logged in")
# ✅ 消息: "User logged in"

# 情况 2：f-string
logger.info(f"User {username} logged in")
# ⚠️ 消息: "User ... logged in"  # username 替换为 ...

# 情况 3：% 格式化
logger.warning("Failed login for %s", username)
# ✅ 消息: "Failed login for %s"  # 保留占位符
# ✅ 参数: ["username"]
```

---

## 限制与未来改进

### 当前限制

1. **跨模块推导**：无法跟踪导入的函数返回值
   ```python
   from utils import get_config
   config = get_config()  # ❌ 值: <dynamic>
   ```

2. **循环变量**：无法推导循环迭代中的值
   ```python
   for i in range(10):
       x = i * 2  # ✅ 类型: int, ❌ 值: <dynamic>
   ```

3. **递归调用**：可能导致推导失败
   ```python
   def factorial(n):
       if n == 0:
           return 1
       return n * factorial(n - 1)  # ⚠️ 值: <dynamic>
   ```

4. **复杂容器**：嵌套深度过大时性能下降
   ```python
   data = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]  # 推导慢
   ```

5. **混合推导**：函数返回值参与运算时推导受限
   ```python
   def get_base():
       return "https://api.example.com"
   url = get_base() + "/users"  # ⚠️ 值: "...", 而非完整 URL
   ```

---

### 未来改进方向

1. **表达式混合运算**：
   ```python
   # 支持单返回路径的函数参与运算
   def get_base_url():
       return "https://api.example.com"

    url = get_base_url() + "/users"
    # 当前: <dynamic>
    # 期望: "https://api.example.com/users"
   ```

2. **更智能的字符串推导**：
   ```python
   # 支持多级拼接
   url = f"{protocol}://{host}" + f"/{path}/{resource}"
   # 当前: "...://.../.../..."
   # 期望: 更精确的静态部分保留
   ```

3. **类型注解驱动推导**：
   ```python
   from typing import Literal

   def get_env() -> Literal["dev", "prod"]:
       return "dev"

   env = get_env()
   # 当前: 值 <dynamic>
   # 期望: 类型: Literal["dev", "prod"], 可能的值: "dev" or "prod"
   ```

4. **数据流分析**：
   ```python
   x = 1
   y = x + 2  # 当前: 值 <dynamic>, 期望: 值 3
   ```

---

## 测试用例参考

### 基础推导测试

**文件**：`tests/test_prometheus_metrics_scanner/test_ast_utils.py`

测试覆盖：
- 字面量推导
- 容器推导
- 函数签名推导
- 装饰器提取

---

### 环境变量推导测试

**文件**：`tests/test_env_var_scanner/test_default_values.py`

测试覆盖：
- `os.getenv()` 默认值推导
- 类型转换推导（`int()`, `bool()`）
- 复杂默认值（字典、列表）

---

### 字符串模式推导测试

**文件**：`tests/test_scanners/test_redis_usage.py`

测试覆盖：
- f-string 模式
- `format()` 方法
- 字符串拼接（`+` 运算符）
- `%` 格式化

---

## 最佳实践

### 1. 优先使用结构化 API

```python
# ✅ 好：使用结构化返回
result = infer_value_structured(node)
if result.confidence == "exact":
    use_static_value(result.value)

# ❌ 差：使用旧 API 并手动解析
value, success = infer_value_with_fallback(node)
if success and not isinstance(value, str) or not value.startswith("`"):
    use_static_value(value)
```

---

### 2. 字符串模式用 `StringPattern`

```python
# ✅ 好：使用 StringPattern
pattern = infer_string_pattern(node)
base_url = pattern.static_prefix()
if not pattern.is_static:
    log_warning(f"Dynamic URL: {pattern.to_pattern()}")

# ❌ 差：手动解析字符串
url = infer_url(node)
if "..." in url:
    base_url = url.split("...")[0]
    log_warning(f"Dynamic URL: {url}")
```

---

### 3. 优先使用字面量（代码层面）

```python
# ✅ 好：推导成功
PORT = 8080
timeout = 30

# ❌ 差：无法推导
PORT = os.getenv("PORT")  # 运行时才知道
timeout = calculate_timeout()
```

---

### 4. 使用类型注解

```python
# ✅ 好：明确类型
def get_port() -> int:
    return 8080

# ❌ 差：需要推导 return 语句
def get_port():
    return 8080
```

---

### 5. 避免复杂表达式

```python
# ✅ 好：分步推导
base = "https://api.example.com"
path = "/users"
url = base + path

# ❌ 差：难以推导
url = (get_protocol() + "://" + get_host() + "/" + get_path())
```

---

### 6. 收集推导统计

```python
# ✅ 好：监控推导质量
from collections import Counter

confidence_stats = Counter()
for node in all_nodes:
    result = infer_value_structured(node)
    confidence_stats[result.confidence] += 1

total = sum(confidence_stats.values())
print(f"推导成功率: {confidence_stats['exact'] / total * 100:.1f}%")
print(f"部分推导: {confidence_stats['partial']} 个")
print(f"完全动态: {confidence_stats['unknown']} 个")
```

---

## 常见问题

### Q1: 为什么要使用结构化返回值？

**A**: 结构化返回值（`InferenceResult` 和 `StringPattern`）提供了更清晰的语义：

**之前的问题**：
```python
# 旧 API：无法区分推导质量
value = "https://api.com/..."  # 部分推导
value = "<dynamic>"             # 完全动态
value = "`func()`"              # 原始表达式

# 调用方需要字符串解析才能判断
if "..." in value:
    # 部分推导？
elif value.startswith("`"):
    # 表达式？
elif value == "<dynamic>":
    # 完全动态？
```

**现在的方案**：
```python
# 新 API：结构化返回
result = infer_value_structured(node)

if result.confidence == "exact":
    # 完全静态
    use_value(result.value)
elif result.confidence == "partial":
    # 部分推导
    pattern = result.value
    prefix = pattern.split("...")[0]
else:
    # 完全动态
    log_unknown(result.node.as_string())
```

**优势**：
- ✅ 类型安全（不需要解析字符串）
- ✅ 语义明确（`confidence` 字段直接表达推导质量）
- ✅ 易于扩展（可以添加更多元数据字段）

---

### Q2: `InferenceResult` 和 `StringPattern` 有什么区别？

**A**: 两者服务于不同的使用场景：

| 特性 | `InferenceResult` | `StringPattern` |
|------|-------------------|-----------------|
| **用途** | 通用值推导 | 专门用于字符串模式 |
| **返回值** | `Any` 类型 | `list[str \| Ellipsis]` |
| **适用场景** | 环境变量、配置项、数值 | URL、Redis key、日志消息 |
| **动态标记** | `confidence` 字段 | `parts` 中的 `...` |

**示例对比**：
```python
# InferenceResult：通用推导
result = infer_value_structured(node)
# 返回: InferenceResult(value=42, confidence="exact", is_static=True)

# StringPattern：字符串模式
pattern = infer_string_pattern(node)
# 返回: StringPattern(parts=["api/", ..., "/users"])
print(pattern.to_pattern())  # "api/.../users"
print(pattern.static_prefix())  # "api/"
```

---

### Q3: 旧 API（`infer_value_with_fallback`）还能用吗？

**A**: 可以，旧 API 会保留以保证兼容性，但推荐迁移到新 API：

**迁移指南**：

```python
# 旧 API
value, success = infer_value_with_fallback(node)
if success:
    print(f"Value: {value}")
else:
    print(f"Failed: {value}")  # value 是反引号包裹的表达式

# 新 API（推荐）
result = infer_value_structured(node)
if result.confidence == "exact":
    print(f"Value: {result.value}")
elif result.confidence == "partial":
    print(f"Pattern: {result.value}")
else:
    print(f"Unknown: {result.node.as_string()}")
```

**迁移收益**：
- 更清晰的语义
- 更好的类型提示
- 更容易编程处理

---

### Q4: 如何处理字符串模式中的动态部分？

**A**: `StringPattern` 提供了多种方法处理动态部分：

```python
# f"https://api.com/users/{user_id}/posts/{post_id}"
pattern = infer_string_pattern(node)

# 1. 提取完整模式
print(pattern.to_pattern())
# "https://api.com/users/.../posts/..."

# 2. 提取静态前缀（用于 URL 分组）
print(pattern.static_prefix())
# "https://api.com/users/"

# 3. 获取所有静态部分（用于关键词提取）
print(pattern.static_parts())
# ["https://api.com/users/", "/posts/", ""]

# 4. 判断是否完全静态
if pattern.is_static:
    print("完全静态 URL")
else:
    print("包含动态参数")
```

**应用场景**：
- **HTTP 请求分析**：按基础 URL 分组请求
- **Redis key 分析**：提取命名空间和模式
- **日志分析**：识别日志模板

---

### Q5: 推导失败时应该怎么办？

**A**: 推导器提供了优雅降级机制：

**1. 字符串场景**：使用 `StringPattern` 保留静态部分
```python
# f"{protocol}://{host}/{path}"
pattern = infer_string_pattern(node)
print(pattern.to_pattern())  # "...://.../..."

# 至少知道有三个动态部分，可以记录模式
if pattern.parts.count(...) > 2:
    log_warning("URL 包含多个动态部分")
```

**2. 非字符串场景**：检查 `confidence` 字段
```python
result = infer_value_structured(node)
if result.confidence == "unknown":
    # 记录原始表达式供人工审查
    report_dynamic_value(
        expr=result.node.as_string(),
        location=f"{result.node.root().file}:{result.node.lineno}"
    )
```

**3. 收集推导统计**：
```python
stats = {"exact": 0, "partial": 0, "unknown": 0}
for node in nodes:
    result = infer_value_structured(node)
    stats[result.confidence] += 1

print(f"推导成功率: {stats['exact'] / sum(stats.values()) * 100:.1f}%")
```

---

## 迁移指南

### 从旧 API 迁移到结构化 API

**为什么要迁移？**
- ✅ 更清晰的语义（不需要解析字符串判断推导结果）
- ✅ 更好的类型安全（IDE 自动补全和类型检查）
- ✅ 更强大的功能（字符串模式提取、静态前缀等）

---

### 迁移步骤 1：更新值推导

**旧代码**：
```python
from upcast.common.ast_utils import infer_value_with_fallback

value, success = infer_value_with_fallback(node)
if success:
    # 推导成功
    process_value(value)
else:
    # 推导失败，value 是 "`expression`"
    log_error(f"Cannot infer: {value}")
```

**新代码**：
```python
from upcast.common.ast_utils import infer_value_structured

result = infer_value_structured(node)
if result.confidence == "exact":
    # 完全静态
    process_value(result.value)
elif result.confidence == "partial":
    # 部分推导（字符串包含 ...）
    process_pattern(result.value)
else:
    # 完全动态
    log_error(f"Cannot infer: {result.node.as_string()}")
```

---

### 迁移步骤 2：更新字符串模式处理

**旧代码**：
```python
# HTTP 请求扫描器
url = infer_url_pattern(node)  # 返回 "https://api.com/..."

# 手动解析静态前缀
if "..." in url:
    base_url = url.split("...")[0]
    has_dynamic = True
else:
    base_url = url
    has_dynamic = False
```

**新代码**：
```python
from upcast.common.ast_utils import infer_string_pattern

pattern = infer_string_pattern(node)

# 直接使用结构化方法
base_url = pattern.static_prefix()
has_dynamic = not pattern.is_static

# 或者按需使用不同格式
full_pattern = pattern.to_pattern()  # "https://api.com/..."
static_parts = pattern.static_parts()  # ["https://api.com/", ...]
```

---

### 迁移步骤 3：更新扫描器输出

**旧代码**：
```python
# 扫描器返回字符串，包含特殊标记
results = {
    "url": "https://api.com/...",  # 包含 ...
    "timeout": "<dynamic>",         # 特殊标记
    "port": 8080                    # 静态值
}
```

**新代码**：
```python
from upcast.common.ast_utils import infer_value_structured

# 扫描器返回结构化结果
results = []
for node in nodes:
    result = infer_value_structured(node)
    results.append({
        "value": result.value,
        "confidence": result.confidence,
        "is_static": result.is_static,
        "location": f"{node.lineno}:{node.col_offset}"
    })

# 调用方可以轻松过滤
static_values = [r for r in results if r["confidence"] == "exact"]
dynamic_values = [r for r in results if r["confidence"] == "unknown"]
```

---

### 迁移兼容性

旧 API 会继续保留，但标记为 **deprecated**：

```python
# 仍然可用，但会有 DeprecationWarning
from upcast.common.ast_utils import infer_value_with_fallback

# 推荐使用新 API
from upcast.common.ast_utils import infer_value_structured
```

**迁移时间表**（建议）：
- **v0.4.0**: 引入新 API，旧 API 正常工作
- **v0.5.0**: 旧 API 标记为 deprecated
- **v0.6.0**: 移除旧 API（或保留但仅用于兼容性）

---

## 参考资源

- **astroid 文档**：https://astroid.readthedocs.io/
- **Upcast 源码**：
  - 核心推导：`upcast/common/ast_utils.py`
  - HTTP 推导：`upcast/scanners/http_requests.py`
  - Redis 推导：`upcast/scanners/redis_usage.py`
  - 环境变量：`upcast/scanners/env_var_scanner.py`
- **测试用例**：`tests/test_*_scanner/`
