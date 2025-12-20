# Proposal: Enhance Signal Scanner with Send Detection and Usage Tracking

**Status**: Draft
**Created**: 2025-12-18
**Change ID**: enhance-signal-scanner-with-send-and-usages

## Problem Statement

当前的 signal scanner 实现存在两个重要缺失：

1. **只检测接收，不检测发送**：目前只检测 `@receiver` 和 `.connect()` 模式，但没有检测 `.send()` 和 `.send_robust()` 调用。这导致无法完整了解信号的使用流程。

2. **缺少具体的 usages 信息**：当前输出只是简单列出信号和处理器，但没有提供每个使用点的详细信息（如具体的代码位置、使用模式等）。这与项目中其他 scanner（如 django-settings-scanner）的模式不一致。

信号有两个关键场景：

- **发送**（Sending）：代码中调用 `signal.send()` 或 `signal.send_robust()` 来触发信号
- **接收**（Receiving）：使用 `@receiver` 装饰器或 `.connect()` 方法来注册处理器

当前实现只覆盖了接收场景，这使得用户无法：

- 追踪信号在哪里被触发
- 了解信号的完整生命周期（从发送到接收）
- 分析信号的使用模式和频率

## Proposed Solution

增强 signal scanner 以支持：

1. **检测信号发送调用（带严格验证）**：

   - Django: `signal_name.send(sender=..., **kwargs)`
   - Django: `signal_name.send_robust(sender=..., **kwargs)`
   - Celery: `signal_name.send(sender=..., **kwargs)`
   - **关键**：只检测已知信号的 `.send()` 调用，避免误判 `mail.send()`、`message.send()` 等

2. **已知信号白名单验证**：

   - 从 Django/Celery imports 收集内置信号（如 `post_save`, `task_sent`）
   - 从第一遍扫描收集自定义信号（如 `order_paid = Signal()`）
   - 从第二遍扫描收集有接收器的信号名称
   - 只有在白名单中的对象调用 `.send()` 才被识别为信号发送

   **防止误判示例**：

   ```python
   # ✅ 会被检测（在白名单中）
   from django.db.models.signals import post_save
   post_save.send(sender=Order, instance=order)

   # ❌ 不会被检测（不在白名单中）
   from django.core.mail import EmailMessage
   mail = EmailMessage()
   mail.send()  # 这是发送邮件，不是信号
   ```

3. **使用 Usage 模式记录所有使用点**：

   - 为每个信号维护 `usages` 列表
   - 每个 usage 包含：file、line、column、pattern、code
   - Pattern 类型：
     - `"receiver_decorator"`: @receiver装饰器
     - `"connect_method"`: .connect()方法
     - `"send_method"`: .send()方法（仅限已知信号）
     - `"send_robust_method"`: .send_robust()方法（仅限已知信号）

4. **重构数据结构**：
   ```python
   {
     "django": {
       "model_signals": {
         "post_save": {
           "receivers": [  # 接收器列表
             {
               "handler": "order_created",
               "file": "handlers.py",
               "line": 10,
               "sender": "Order"
             }
           ],
           "senders": [  # 发送器列表
             {
               "file": "views.py",
               "line": 25,
               "sender": "Order",
               "pattern": "send_method"
             }
           ],
           "usages": [  # 所有使用点
             {
               "file": "handlers.py",
               "line": 10,
               "column": 0,
               "pattern": "receiver_decorator",
               "code": "@receiver(post_save, sender=Order)"
             },
             {
               "file": "views.py",
               "line": 25,
               "column": 4,
               "pattern": "send_method",
               "code": "post_save.send(sender=Order, instance=order)"
             }
           ]
         }
       }
     }
   }
   ```

## Benefits

1. **完整的信号流追踪**：用户可以看到信号从哪里发送，在哪里被接收
2. **高精度检测**：通过白名单验证避免将 `mail.send()`、`message.send()` 等误判为信号
3. **一致的数据模型**：与 django-settings-scanner 等其他 scanner 使用相同的 Usage 模式
4. **更好的代码理解**：通过 usages 列表可以快速定位所有相关代码
5. **支持重构和分析**：可以识别未使用的信号、过度使用的信号等

## Scope

### In Scope

- 检测 Django 信号的 `.send()` 和 `.send_robust()` 调用
- 检测 Celery 信号的 `.send()` 调用
- 添加 SignalUsage dataclass 和相关解析函数
- 重构数据结构以包含 receivers、senders、usages 三个列表
- 更新 YAML 导出格式
- 添加对应的测试用例

### Out of Scope

- 信号的实际执行追踪（运行时分析）
- 信号处理器的性能分析
- 信号链路的可视化（可作为未来增强）

## Implementation Considerations

1. **向后兼容性**：新的输出格式应该保持向后兼容，或提供迁移指南
2. **性能**：send() 检测不应显著增加扫描时间
3. **测试覆盖**：需要添加 send/send_robust 的测试 fixtures
4. **文档更新**：更新 CLI 帮助和示例输出

## Success Criteria

- [ ] 能够检测所有 `.send()` 和 `.send_robust()` 调用
- [ ] 输出包含 receivers、senders、usages 三个部分
- [ ] 所有现有测试继续通过
- [ ] 新增测试覆盖发送场景
- [ ] YAML 输出格式清晰易读
- [ ] 文档反映新功能

## Alternatives Considered

### Alternative 1: 只添加 send 检测，不改变数据结构

**Pros**: 改动较小，风险低
**Cons**: 不解决 usages 缺失的问题，数据结构不一致

### Alternative 2: 创建独立的 signal-send-scanner

**Pros**: 职责分离，不影响现有 scanner
**Cons**: 用户需要运行两个命令，信号信息被分割

### Alternative 3: 采用当前方案（推荐）

**Pros**: 完整的信号视图，统一的数据模型，符合项目模式
**Cons**: 需要重构现有代码，输出格式有变化

## Questions & Risks

**Questions:**

1. 是否需要区分 `send()` 和 `send_robust()` 在输出中？
   - 建议：在 pattern 中区分，在统计中可以合并
2. 是否需要保留当前的简化格式作为选项？
3. 如何处理动态信号引用（如变量赋值后再调用）？
   - 建议：采用保守策略，优先精确度而非召回率，不检测过于复杂的情况

**Risks:**

1. **输出格式变更**：可能影响依赖现有输出的工具
   - 缓解：提供向后兼容选项或版本标识
2. **性能影响**：增加 send 检测可能增加扫描时间
   - 缓解：优化 AST 遍历，仅在需要时进行额外分析
3. **漏检边缘案例**：复杂的信号引用可能无法检测
   - 缓解：文档说明最佳实践（直接导入信号），提供 verbose 模式显示被拒绝的 send 调用
4. **误判风险**：虽然有白名单，但仍可能有边缘情况
   - 缓解：严格的验证逻辑，保守的检测策略，完善的测试覆盖间
   - 缓解：优化 AST 遍历，仅在需要时进行额外分析

## Dependencies

- 依赖当前的 signal scanner 实现（implement-signal-scanner）
- 可参考 django-settings-scanner 的 Usage 模式

## Timeline Estimate

- Proposal & Design: 0.5 天
- Implementation: 1.5 天
- Testing: 0.5 天
- Documentation: 0.5 天
- **Total**: ~3 天

## References

- django-settings-scanner Usage 模式
- Django 信号文档: https://docs.djangoproject.com/en/stable/topics/signals/
- Celery 信号文档: https://docs.celeryq.dev/en/stable/userguide/signals.html
