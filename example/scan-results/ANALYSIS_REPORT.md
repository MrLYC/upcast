# Project Analysis Report

Generated from static code analysis scan results.

## Executive Summary

- **Total Files Scanned**: 8205
- **Total Findings**: 4246
- **Scan Types**: 13

## Code Quality Analysis

### Cyclomatic Complexity

- **High Complexity Functions**: 88
- **Files Analyzed**: 75

**Distribution by Severity:**

| Severity | Count | Description |
|----------|-------|-------------|
| Warning | 43 | 11-15: Refactoring recommended |
| Acceptable | 33 | 6-10: Reasonable complexity |
| High Risk | 10 | 16-20: Significant maintenance cost |
| Critical | 2 | >20: Design issues likely |

#### Top 10 Most Complex Functions

| # | Function | Complexity | Severity | File | Lines |
|---|----------|------------|----------|------|-------|
| 1 | `test_save` | 21 | critical | `...aasng/tests/api/bkapp_model/test_bkapp_model.py:79` | 134 |
| 2 | `test_integrated` | 21 | critical | `...m/bkapp_model/entities_syncer/test_processes.py:37` | 63 |
| 3 | `_migrate_single` | 20 | high_risk | `...ers/management/commands/migrate_bkpaas3_perm.py:144` | 121 |
| 4 | `testlist_gen_cnative_process_specs` | 20 | high_risk | `...ests/paas_wl/bk_app/processes/test_processes.py:35` | 50 |
| 5 | `test_release_version` | 18 | high_risk | `...ng/bk_plugins/pluginscenter/test_integration.py:182` | 131 |
| 6 | `sync` | 17 | high_risk | `...erver/paasng/paas_wl/bk_app/processes/models.py:129` | 85 |
| 7 | `make_release_validator` | 17 | high_risk | `.../paasng/bk_plugins/pluginscenter/serializers.py:480` | 75 |
| 8 | `_update_or_create_operation_report` | 17 | high_risk | `...rver/paasng/paasng/platform/evaluation/tasks.py:52` | 73 |
| 9 | `_make_json_field` | 17 | high_risk | `apiserver/paasng/paasng/utils/models.py:290` | 93 |
| 10 | `check_pod_health_status` | 16 | high_risk | `apiserver/paasng/paas_wl/utils/kubestatus.py:89` | 62 |

### Blocking Operations

- **Total Operations**: 33
- **Files Scanned**: 21

**By Category:**

| Category | Count | Impact |
|----------|-------|--------|
| Time Based | 28 | May cause delays in async contexts |
| Database | 5 | Can cause deadlocks with improper locking |

#### Examples of Blocking Operations

**Time Based Operations:**

- `apiserver/paasng/paas_wl/bk_app/deploy/app_res/controllers.py:215` in `WaitPodDelete.wait()`
  - Operation: `time.sleep`
  - Statement: `time.sleep(self._check_interval)`

- `apiserver/paasng/paas_wl/bk_app/deploy/app_res/controllers.py:308` in `PodScheduleHandler._wait_pod_succeeded()`
  - Operation: `time.sleep`
  - Statement: `time.sleep(check_period)`

- `apiserver/paasng/paas_wl/bk_app/deploy/app_res/controllers.py:565` in `CommandHandler.wait_for_succeeded()`
  - Operation: `time.sleep`
  - Statement: `time.sleep(check_period)`

**Database Operations:**

- `apiserver/paasng/paas_wl/infras/cluster/models.py:216` in `ClusterManager.switch_default_cluster()`
  - Operation: `self.select_for_update`
  - Statement: `self.select_for_update()`

- `apiserver/paasng/paas_wl/infras/cluster/models.py:217` in `ClusterManager.switch_default_cluster()`
  - Operation: `self.select_for_update`
  - Statement: `self.select_for_update()`

- `apiserver/paasng/paasng/accessories/services/providers/base.py:72` in `ResourcePoolProvider.create()`
  - Operation: `select_for_update`
  - Statement: `PreCreatedInstance.objects.select_for_update()`

**Recommendations:**
- Consider using async alternatives for blocking I/O operations
- Review time.sleep() calls in async contexts
- Optimize database queries with select_for_update()
- Use asyncio.sleep() instead of time.sleep() in async functions

## Architecture & Patterns

### Django Models

- **Total Models**: 167
- **Total Fields**: 684
- **Total Relationships**: 148
- **Files Scanned**: 167
- **Average Fields per Model**: 4.1

**Models with Most Fields:**

| Model | Fields | Module |
|-------|--------|--------|
| `AppOperationReport` | 21 | `...sng.paasng.platform.evaluation.models` |
| `AppOperationRecord` | 14 | `...erver.paasng.paasng.misc.audit.models` |
| `PluginRelease` | 14 | `...lugins.pluginscenter.models.instances` |
| `Application` | 13 | `...g.paasng.platform.applications.models` |
| `BuildProcess` | 13 | `...s_wl.bk_app.applications.models.build` |
| `Build` | 13 | `...s_wl.bk_app.applications.models.build` |
| `Template` | 12 | `...asng.paasng.platform.templates.models` |
| `AdminOperationRecord` | 12 | `...erver.paasng.paasng.misc.audit.models` |
| `Module` | 11 | `...paasng.platform.modules.models.module` |
| `BaseOperation` | 11 | `...erver.paasng.paasng.misc.audit.models` |

**Models with Most Relationships:**

| Model | Relationships | Types |
|-------|---------------|-------|
| `BuildConfig` | 4 | ForeignKey, ManyToManyField, OneToOneField |
| `ServiceEngineAppAttachment` | 4 | ForeignKey |
| `ProcessLogQueryConfig` | 4 | ForeignKey |
| `Command` | 4 | ForeignKey, OneToOneField |
| `AppSlugBuilder` | 3 | ForeignKey, ManyToManyField |
| `ApplicationEnvironment` | 3 | ForeignKey, OneToOneField |
| `AppDomain` | 3 | ForeignKey |
| `Release` | 3 | ForeignKey |
| `BuildProcess` | 3 | ForeignKey, OneToOneField |
| `DeployStep` | 2 | ForeignKey |

#### Complete Model Field Details

Showing all models with their fields, types, and inheritance:

##### `APIServer`
**Module:** `apiserver.paasng.paas_wl.infras.cluster.models`
**Inherits from:** `paas_wl.utils.models.UuidAuditedModel`

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `host` | `models.CharField` | help_text='API Server 的后端地址', max_length=255 |
| `overridden_hostname` | `models.CharField` | blank=True, help_text='在请求该 APIServer 时, 使用该 hostn...', max_length=255... |

**Relationships (1):**
- `cluster`: models.ForeignKey → ``Cluster``

**Meta:**
- unique_together: `cluster`, `host`

##### `AccountFeatureFlag`
**Module:** `apiserver.paasng.paasng.infras.accounts.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `effect` | `models.BooleanField` | default=True |
| `name` | `models.CharField` | max_length=64 |

##### `AdminOperationRecord`
**Module:** `apiserver.paasng.paasng.misc.audit.models`
**Inherits from:** `apiserver.paasng.paasng.misc.audit.models.BaseOperation`
**Description:** 后台管理操作记录，用于记录平台管理员在 Admin 系统上的操作

**Fields (12):**

| Field | Type | Parameters |
|-------|------|------------|
| `access_type` | `models.IntegerField` | choices='`AccessType.get_choices()`', default='`AccessType.WEB`', verbose_name='访问方式' |
| `app_code` | `models.CharField` | blank=True, max_length=32, null=True... |
| `attribute` | `models.CharField` | blank=True, help_text='如增强服务的属性可以为：mysql、bkrepo', max_length=32... |
| `data_after` | `models.JSONField` | blank=True, null=True, verbose_name='操作后的数据' |
| `data_before` | `models.JSONField` | blank=True, null=True, verbose_name='操作前的数据' |
| `end_time` | `models.DateTimeField` | help_text='仅需要后台执行的的操作才需要记录结束时间', null=True |
| `environment` | `models.CharField` | blank=True, choices='`AppEnvName.get_choices()`', max_length=16... |
| `module_name` | `models.CharField` | blank=True, max_length=32, null=True... |
| `operation` | `models.CharField` | choices='`OperationEnum.get_choices()`', max_length=32, verbose_name='操作类型' |
| `result_code` | `models.IntegerField` | choices='`ResultCode.get_choices()`', default='`ResultCode.SUCCESS`', verbose_name='操作结果' |
| `start_time` | `models.DateTimeField` | auto_now_add=True, db_index=True, verbose_name='开始时间' |
| `target` | `models.CharField` | choices='`OperationTarget.get_choice...', max_length=32, verbose_name='操作对象' |

##### `ApmData`
**Module:** `svc-otel.svc_otel.vendor.models`
**Inherits from:** `paas_service.models.AuditedModel`

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `app_name` | `models.CharField` | max_length=64 |
| `bk_app_code` | `models.CharField` | max_length=64 |
| `data_token` | `models.CharField` | max_length=255 |
| `env` | `models.CharField` | max_length=64 |
| `is_delete` | `models.BooleanField` | default=False |

**Meta:**
- unique_together: `bk_app_code`, `env`

##### `App`
**Module:** `apiserver.paasng.paas_wl.bk_app.applications.models.app`
**Inherits from:** `paas_wl.bk_app.applications.models.UuidAuditedModel`
**Description:** App Model

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `name` | `models.SlugField` | max_length=64, validators=[1 items] |
| `owner` | `models.CharField` | max_length=64 |
| `region` | `models.CharField` | max_length=32 |
| `type` | `models.CharField` | db_index=True, default='`WlAppType.DEFAULT.value`', max_length=16... |

**Meta:**
- unique_together: `region`, `name`

##### `AppAddOn`
**Module:** `apiserver.paasng.paas_wl.infras.resource_templates.models`
**Inherits from:** `paas_wl.bk_app.applications.models.UuidAuditedModel`
**Description:** 应用挂件关联实例

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `enabled` | `models.BooleanField` | default=True |
| `spec` | `models.TextField` | - |

**Relationships (2):**
- `app`: models.ForeignKey → ``WlApp``
- `template`: models.ForeignKey → ``AppAddOnTemplate``

##### `AppAddOnTemplate`
**Module:** `apiserver.paasng.paas_wl.infras.resource_templates.models`
**Inherits from:** `paas_wl.bk_app.applications.models.UuidAuditedModel`
**Description:** 应用挂件模版

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `enabled` | `models.BooleanField` | default=True |
| `name` | `models.CharField` | max_length=64 |
| `region` | `models.CharField` | max_length=32 |
| `spec` | `models.TextField` | - |
| `type` | `models.IntegerField` | default='`AppAddOnType.SIMPLE_SIDECA...' |

**Meta:**
- unique_together: `region`, `name`

##### `AppAlertRule`
**Module:** `apiserver.paasng.paasng.misc.monitoring.monitor.models`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 记录 app 初始的告警规则配置

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `alert_code` | `models.CharField` | help_text='alert rule code e.g. high_c...', max_length=64 |
| `display_name` | `models.CharField` | max_length=512 |
| `enabled` | `models.BooleanField` | default=True |
| `environment` | `models.CharField` | max_length=16, verbose_name='部署环境' |
| `receivers` | `models.JSONField` | default='`list`' |
| `threshold_expr` | `models.CharField` | max_length=64 |

**Relationships (2):**
- `application`: models.ForeignKey → `applications.Application`
- `module`: models.ForeignKey → `modules.Module`

##### `AppBuildPack`
**Module:** `apiserver.paasng.paasng.platform.modules.models.runtime`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** buildpack 配置

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `address` | `models.CharField` | max_length=2048, verbose_name='地址' |
| `is_hidden` | `models.BooleanField` | default=False, verbose_name='是否隐藏' |
| `language` | `models.CharField` | max_length=32, verbose_name='编程语言' |
| `name` | `models.CharField` | max_length=64, verbose_name='名称' |
| `type` | `models.CharField` | choices='`BuildPackType.get_choices()`', max_length=32, verbose_name='引用类型' |
| `version` | `models.CharField` | max_length=32, verbose_name='版本' |

**Relationships (1):**
- `modules`: models.ManyToManyField → `modules.Module`

##### `AppDashboard`
**Module:** `apiserver.paasng.paasng.misc.monitoring.monitor.models`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 记录 APP 初始化的仪表盘信息

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `display_name` | `models.CharField` | help_text='仪表盘展示名称，如：Python 开发框架内置仪表盘', max_length=512 |
| `language` | `models.CharField` | max_length=32, verbose_name='仪表盘所属语言' |
| `name` | `models.CharField` | help_text='仪表盘名称，如：bksaas/framework-py...', max_length=64 |
| `template_version` | `models.CharField` | help_text='模板版本更新时，可以根据该字段作为批量刷新仪表盘', max_length=32 |

**Relationships (1):**
- `application`: models.ForeignKey → `applications.Application`

**Meta:**
- unique_together: `application`, `name`

##### `AppDashboardTemplate`
**Module:** `apiserver.paasng.paasng.misc.monitoring.monitor.models`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 仪表盘模板，只需要记录名称和版本号，模板的内容在蓝鲸监控侧维护

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `display_name` | `models.CharField` | help_text='仪表盘展示名称，如：Python 开发框架内置仪表盘', max_length=512 |
| `is_plugin_template` | `models.BooleanField` | default=False |
| `language` | `models.CharField` | max_length=32, verbose_name='仪表盘所属语言' |
| `name` | `models.CharField` | help_text='与蓝鲸监控约定的仪表盘名称，如：bksaas/fram...', max_length=64, unique=True |
| `version` | `models.CharField` | max_length=32 |

##### `AppDomain`
**Module:** `apiserver.paasng.paas_wl.workloads.networking.ingress.models`
**Inherits from:** `paas_wl.bk_app.applications.models.AuditedModel`
**Description:** Domains of applications, each object(entry) represents an (domain + path_prefix) pair.

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `host` | `models.CharField` | max_length=128 |
| `https_auto_redirection` | `models.BooleanField` | default=False |
| `https_enabled` | `models.BooleanField` | default=False |
| `path_prefix` | `models.CharField` | default='/', help_text='the accessable path for cur...', max_length=64 |
| `region` | `models.CharField` | max_length=32 |
| `source` | `models.IntegerField` | choices='`make_enum_choices(AppDomai...' |

**Relationships (3):**
- `app`: models.ForeignKey → ``WlApp``
- `cert`: models.ForeignKey → `AppDomainCert`
- `shared_cert`: models.ForeignKey → `AppDomainSharedCert`

**Meta:**
- db_table: `services_appdomain`
- unique_together: `region`, `host`, `path_prefix`

##### `AppDomainSharedCert`
**Module:** `apiserver.paasng.paas_wl.workloads.networking.ingress.models`
**Inherits from:** `apiserver.paasng.paas_wl.workloads.networking.ingress.models.BasicCert`
**Description:** Shared TLS Certifications for AppDomain, every app's domain may link to this certificate as

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `auto_match_cns` | `models.TextField` | max_length=2048 |
| `name` | `models.CharField` | max_length=128, unique=True, validators=[1 items] |
| `region` | `models.CharField` | max_length=32 |

**Meta:**
- db_table: `services_appdomainsharedcert`

##### `AppImage`
**Module:** `apiserver.paasng.paasng.platform.modules.models.runtime`
**Inherits from:** `paasng.utils.models.TimestampedModel`

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `image` | `models.CharField` | max_length=256, verbose_name='镜像' |
| `is_default` | `models.BooleanField` | default=False, null=True, verbose_name='是否为默认运行时' |
| `is_hidden` | `models.BooleanField` | default=False, verbose_name='是否隐藏' |
| `name` | `models.CharField` | max_length=64, unique=True, verbose_name='名称' |
| `tag` | `models.CharField` | max_length=32, verbose_name='标签' |
| `type` | `models.CharField` | choices='`AppImageType.get_choices()`', max_length=32, verbose_name='镜像类型' |

**Meta:**
- abstract: `True`

##### `AppImageCredential`
**Module:** `apiserver.paasng.paas_wl.workloads.images.models`
**Inherits from:** `paas_wl.bk_app.applications.models.UuidAuditedModel`
**Description:** ImageCredential of applications, each object(entry) represents an (username + password) pair for a registry

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `registry` | `models.CharField` | max_length=255 |
| `username` | `models.CharField` | blank=False, max_length=32 |

**Relationships (1):**
- `app`: models.ForeignKey → `api.App`

**Meta:**
- unique_together: `app`, `registry`

##### `AppLatestOperationRecord`
**Module:** `apiserver.paasng.paasng.misc.audit.models`
**Inherits from:** `models.Model`
**Description:** 应用最近操作的映射表，可方便快速查询应用的最近操作者，并按最近操作时间进行排序等操作

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `latest_operated_at` | `models.DateTimeField` | db_index=True |

**Relationships (2):**
- `application`: models.OneToOneField → ``Application``
- `operation`: models.OneToOneField → ``AppOperationRecord``

##### `AppMetricsMonitor`
**Module:** `...erver.paasng.paas_wl.bk_app.monitoring.app_monitor.models`
**Inherits from:** `paas_wl.bk_app.applications.models.AuditedModel`

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `is_enabled` | `models.BooleanField` | default=True, help_text='是否启动 AppMetrics' |
| `port` | `models.IntegerField` | help_text='Service 端口' |
| `target_port` | `models.IntegerField` | help_text='容器内的端口' |

**Relationships (1):**
- `app`: models.OneToOneField → ``WlApp``

##### `AppModelDeploy`
**Module:** `...r.paasng.paas_wl.bk_app.cnative.specs.models.app_resource`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** This model stores the cloud-native app's deployment histories.

**Fields (8):**

| Field | Type | Parameters |
|-------|------|------------|
| `application_id` | `models.UUIDField` | null=False, verbose_name='`_('所属应用')`' |
| `environment_name` | `models.CharField` | choices='`AppEnvName.get_choices()`', max_length=16, null=False... |
| `last_transition_time` | `models.DateTimeField` | null=True, verbose_name='`_('状态最近变更时间')`' |
| `message` | `models.TextField` | blank=True, null=True, verbose_name='`_('状态描述文字')`' |
| `module_id` | `models.UUIDField` | null=False, verbose_name='`_('所属模块')`' |
| `name` | `models.CharField` | max_length=64, verbose_name='`_('Deploy 名称')`' |
| `reason` | `models.CharField` | blank=True, max_length=128, null=True... |
| `status` | `models.CharField` | blank=True, choices='`DeployStatus.get_choices()`', max_length=32... |

**Relationships (1):**
- `revision`: models.ForeignKey → `AppModelRevision`

**Meta:**
- unique_together: `application_id`, `module_id`, `environment_name`, `name`

##### `AppModelResource`
**Module:** `...r.paasng.paas_wl.bk_app.cnative.specs.models.app_resource`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** Cloud-native Application's Model Resource

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `application_id` | `models.UUIDField` | null=False, verbose_name='`_('所属应用')`' |
| `module_id` | `models.UUIDField` | null=False, unique=True, verbose_name='`_('所属模块')`' |

**Relationships (1):**
- `revision`: models.OneToOneField → `AppModelRevision`

**Meta:**
- indexes: ``models.Index(fields=['application_id', 'module_id'])``

##### `AppModelRevision`
**Module:** `...r.paasng.paas_wl.bk_app.cnative.specs.models.app_resource`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** Revisions of cloud-native Application's Model Resource

**Fields (9):**

| Field | Type | Parameters |
|-------|------|------------|
| `application_id` | `models.UUIDField` | null=False, verbose_name='`_('所属应用')`' |
| `deployed_value` | `models.JSONField` | null=True, verbose_name='`_('已部署的应用模型（JSON 格式）')`' |
| `has_deployed` | `models.BooleanField` | default=False, verbose_name='`_('是否已部署')`' |
| `is_deleted` | `models.BooleanField` | default=False, verbose_name='`_('是否已删除')`' |
| `is_draft` | `models.BooleanField` | default=False, verbose_name='`_('是否草稿')`' |
| `json_value` | `models.JSONField` | verbose_name='`_('应用模型（JSON 格式）')`' |
| `module_id` | `models.UUIDField` | null=False, verbose_name='`_('所属模块')`' |
| `version` | `models.CharField` | max_length=64, verbose_name='`_('模型版本')`' |
| `yaml_value` | `models.TextField` | verbose_name='`_('应用模型（YAML 格式）')`' |

**Meta:**
- indexes: ``models.Index(fields=['application_id', 'module_id'])``

##### `AppModuleTagRel`
**Module:** `apiserver.paasng.paasng.accessories.smart_advisor.models`
**Inherits from:** `models.Model`
**Description:** A M2M relationship table for storing the relationship between application module and AppTag

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `created` | `models.DateTimeField` | auto_now_add=True |
| `source` | `models.CharField` | blank=False, max_length=32 |
| `tag_str` | `models.CharField` | blank=False, max_length=128 |

**Relationships (1):**
- `module`: models.ForeignKey → `modules.Module`

**Meta:**
- unique_together: `module`, `tag_str`

##### `AppOperationEmailNotificationTask`
**Module:** `apiserver.paasng.paasng.platform.evaluation.models`
**Inherits from:** `models.Model`
**Description:** 应用运营报告邮件通知任务

**Fields (8):**

| Field | Type | Parameters |
|-------|------|------------|
| `end_at` | `models.DateTimeField` | null=True, verbose_name='任务结束时间' |
| `failed_count` | `models.IntegerField` | default=0, verbose_name='采集失败数' |
| `failed_usernames` | `models.JSONField` | default='`list`', verbose_name='通知失败的应用数量' |
| `notification_type` | `models.CharField` | max_length=64, verbose_name='通知类型' |
| `start_at` | `models.DateTimeField` | auto_now_add=True, verbose_name='任务开始时间' |
| `status` | `models.CharField` | choices='`BatchTaskStatus.get_choice...', default='`BatchTaskStatus.RUNNING`', max_length=32... |
| `succeed_count` | `models.IntegerField` | default=0, verbose_name='采集成功数' |
| `total_count` | `models.IntegerField` | default=0, verbose_name='应用总数' |

##### `AppOperationRecord`
**Module:** `apiserver.paasng.paasng.misc.audit.models`
**Inherits from:** `apiserver.paasng.paasng.misc.audit.models.BaseOperation`
**Description:** 应用操作记录，用于记录应用开发者的操作，需要同步记录应用的权限数据，并可以选择是否将数据上报到审计中心

**Fields (14):**

| Field | Type | Parameters |
|-------|------|------------|
| `access_type` | `models.IntegerField` | choices='`AccessType.get_choices()`', default='`AccessType.WEB`', verbose_name='访问方式' |
| `action_id` | `models.CharField` | blank=True, choices='`AppAction.get_choices()`', help_text='action_id 为空则不会将数据上报到审计中心'... |
| `app_code` | `models.CharField` | max_length=32, verbose_name='应用ID, 必填' |
| `attribute` | `models.CharField` | blank=True, help_text='如增强服务的属性可以为：mysql、bkrepo', max_length=32... |
| `data_after` | `models.JSONField` | blank=True, null=True, verbose_name='操作后的数据' |
| `data_before` | `models.JSONField` | blank=True, null=True, verbose_name='操作前的数据' |
| `end_time` | `models.DateTimeField` | help_text='仅需要后台执行的的操作才需要记录结束时间', null=True |
| `environment` | `models.CharField` | blank=True, choices='`AppEnvName.get_choices()`', max_length=16... |
| `module_name` | `models.CharField` | blank=True, max_length=32, null=True... |
| `operation` | `models.CharField` | choices='`OperationEnum.get_choices()`', max_length=32, verbose_name='操作类型' |
| `resource_type_id` | `models.CharField` | choices='`ResourceType.get_choices()`', default='`ResourceType.Application`', help_text='开发者中心注册的资源都为蓝鲸应用'... |
| `result_code` | `models.IntegerField` | choices='`ResultCode.get_choices()`', default='`ResultCode.SUCCESS`', verbose_name='操作结果' |
| `start_time` | `models.DateTimeField` | auto_now_add=True, db_index=True, verbose_name='开始时间' |
| `target` | `models.CharField` | choices='`OperationTarget.get_choice...', max_length=32, verbose_name='操作对象' |

##### `AppOperationReport`
**Module:** `apiserver.paasng.paasng.platform.evaluation.models`
**Inherits from:** `models.Model`
**Description:** 应用运营报告（含资源使用，用户活跃，运维操作等）

**Fields (21):**

| Field | Type | Parameters |
|-------|------|------------|
| `administrators` | `models.JSONField` | default='`list`', verbose_name='应用管理员' |
| `collected_at` | `models.DateTimeField` | verbose_name='采集时间' |
| `cpu_limits` | `models.IntegerField` | default=0, verbose_name='CPU 限制' |
| `cpu_requests` | `models.IntegerField` | default=0, verbose_name='CPU 请求' |
| `cpu_usage_avg` | `models.FloatField` | default=0, verbose_name='CPU 平均使用率' |
| `deploy_summary` | `models.JSONField` | default='`dict`', verbose_name='部署详情汇总' |
| `developers` | `models.JSONField` | default='`list`', verbose_name='应用开发者' |
| `evaluate_result` | `models.JSONField` | default='`dict`', verbose_name='评估结果' |
| `issue_type` | `models.CharField` | default='`OperationIssueType.NONE`', max_length=32, verbose_name='问题类型' |
| `latest_deployed_at` | `models.DateTimeField` | null=True, verbose_name='最新部署时间' |
| `latest_deployer` | `models.CharField` | max_length=128, null=True, verbose_name='最新部署人' |
| `latest_operated_at` | `models.DateTimeField` | null=True, verbose_name='最新操作时间' |
| `latest_operation` | `models.CharField` | max_length=128, null=True, verbose_name='最新操作内容' |
| `latest_operator` | `models.CharField` | max_length=128, null=True, verbose_name='最新操作人' |
| `mem_limits` | `models.IntegerField` | default=0, verbose_name='内存限制' |
| `mem_requests` | `models.IntegerField` | default=0, verbose_name='内存请求' |
| `mem_usage_avg` | `models.FloatField` | default=0, verbose_name='内存平均使用率' |
| `pv` | `models.BigIntegerField` | default=0, verbose_name='近 30 天页面访问量' |
| `res_summary` | `models.JSONField` | default='`dict`', verbose_name='资源使用详情汇总' |
| `uv` | `models.BigIntegerField` | default=0, verbose_name='近 30 天访问用户数' |
| `visit_summary` | `models.JSONField` | default='`dict`', verbose_name='用户访问详情汇总' |

**Relationships (1):**
- `app`: models.OneToOneField → ``Application``

##### `AppOperationReportCollectionTask`
**Module:** `apiserver.paasng.paasng.platform.evaluation.models`
**Inherits from:** `models.Model`
**Description:** 应用运营报告采集任务

**Fields (7):**

| Field | Type | Parameters |
|-------|------|------------|
| `end_at` | `models.DateTimeField` | null=True, verbose_name='任务结束时间' |
| `failed_app_codes` | `models.JSONField` | default='`list`', verbose_name='采集失败应用 Code 列表' |
| `failed_count` | `models.IntegerField` | default=0, verbose_name='采集失败数' |
| `start_at` | `models.DateTimeField` | auto_now_add=True, verbose_name='任务开始时间' |
| `status` | `models.CharField` | choices='`BatchTaskStatus.get_choice...', default='`BatchTaskStatus.RUNNING`', max_length=32... |
| `succeed_count` | `models.IntegerField` | default=0, verbose_name='采集成功数' |
| `total_count` | `models.IntegerField` | default=0, verbose_name='应用总数' |

##### `AppSlugBuilder`
**Module:** `apiserver.paasng.paasng.platform.modules.models.runtime`
**Inherits from:** `apiserver.paasng.paasng.platform.modules.models.runtime.AppImage`
**Description:** 应用构建环境

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `image` | `models.CharField` | max_length=256, verbose_name='镜像' |
| `is_default` | `models.BooleanField` | default=False, null=True, verbose_name='是否为默认运行时' |
| `is_hidden` | `models.BooleanField` | default=False, verbose_name='是否隐藏' |
| `name` | `models.CharField` | max_length=64, unique=True, verbose_name='名称' |
| `tag` | `models.CharField` | max_length=32, verbose_name='标签' |
| `type` | `models.CharField` | choices='`AppImageType.get_choices()`', max_length=32, verbose_name='镜像类型' |

**Relationships (3):**
- `buildpacks`: models.ManyToManyField → ``AppBuildPack``
- `modules`: models.ManyToManyField → `modules.Module`
- `step_meta_set`: models.ForeignKey → `engine.StepMetaSet`

##### `AppSlugRunner`
**Module:** `apiserver.paasng.paasng.platform.modules.models.runtime`
**Inherits from:** `apiserver.paasng.paasng.platform.modules.models.runtime.AppImage`
**Description:** 应用运行环境

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `image` | `models.CharField` | max_length=256, verbose_name='镜像' |
| `is_default` | `models.BooleanField` | default=False, null=True, verbose_name='是否为默认运行时' |
| `is_hidden` | `models.BooleanField` | default=False, verbose_name='是否隐藏' |
| `name` | `models.CharField` | max_length=64, unique=True, verbose_name='名称' |
| `tag` | `models.CharField` | max_length=32, verbose_name='标签' |
| `type` | `models.CharField` | choices='`AppImageType.get_choices()`', max_length=32, verbose_name='镜像类型' |

**Relationships (1):**
- `modules`: models.ManyToManyField → `modules.Module`

##### `AppSubpath`
**Module:** `apiserver.paasng.paas_wl.workloads.networking.ingress.models`
**Inherits from:** `paas_wl.bk_app.applications.models.AuditedModel`
**Description:** stores application's subpaths

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `cluster_name` | `models.CharField` | max_length=32 |
| `region` | `models.CharField` | max_length=32 |
| `source` | `models.IntegerField` | - |
| `subpath` | `models.CharField` | max_length=128 |

**Relationships (1):**
- `app`: models.ForeignKey → ``WlApp``

**Meta:**
- db_table: `services_appsubpath`
- unique_together: `region`, `subpath`

##### `AppUserCredential`
**Module:** `apiserver.paasng.paas_wl.workloads.images.models`
**Inherits from:** `paas_wl.bk_app.applications.models.UuidAuditedModel`
**Description:** App owned UserCredential, aka (Username + Password) pair

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `application_id` | `models.UUIDField` | null=False, verbose_name='`_('所属应用')`' |
| `description` | `models.TextField` | help_text='描述' |
| `name` | `models.CharField` | help_text='凭证名称', max_length=32 |
| `username` | `models.CharField` | help_text='账号', max_length=64 |

**Meta:**
- unique_together: `application_id`, `name`

##### `Application`
**Module:** `apiserver.paasng.paasng.platform.applications.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** 蓝鲸应用

**Fields (13):**

| Field | Type | Parameters |
|-------|------|------------|
| `code` | `models.CharField` | max_length=20, unique=True, verbose_name='应用代号' |
| `id` | `models.UUIDField` | auto_created=True, default='`uuid.uuid4`', editable=False... |
| `is_active` | `models.BooleanField` | default=True, verbose_name='是否活跃' |
| `is_ai_agent_app` | `models.BooleanField` | default=False, verbose_name='是否为 AI Agent 插件应用' |
| `is_deleted` | `models.BooleanField` | default=False |
| `is_plugin_app` | `models.BooleanField` | default=False, help_text='蓝鲸应用插件：供标准运维、ITSM 等 SaaS 使用...', verbose_name='是否为插件应用' |
| `is_scene_app` | `models.BooleanField` | default=False, verbose_name='是否为场景 SaaS 应用' |
| `is_smart_app` | `models.BooleanField` | default=False, verbose_name='是否为 S-Mart 应用' |
| `language` | `models.CharField` | max_length=32, verbose_name='编程语言' |
| `last_deployed_date` | `models.DateTimeField` | null=True, verbose_name='最近部署时间' |
| `name` | `models.CharField` | max_length=20, unique=True, verbose_name='应用名称' |
| `name_en` | `models.CharField` | help_text='目前仅用于 S-Mart 应用', max_length=20, verbose_name='应用名称(英文)' |
| `type` | `models.CharField` | db_index=True, default='`ApplicationType.DEFAULT.va...', help_text='与应用部署方式相关的类型信息'... |

##### `ApplicationDeploymentModuleOrder`
**Module:** `apiserver.paasng.paasng.platform.applications.models`
**Inherits from:** `models.Model`

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `order` | `models.IntegerField` | verbose_name='顺序' |

**Relationships (1):**
- `module`: models.OneToOneField → ``Module``

**Meta:**
- verbose_name: `模块顺序`

##### `ApplicationDescription`
**Module:** `apiserver.paasng.paasng.platform.declarative.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** Application description object

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `code` | `models.CharField` | db_index=True, max_length=20, verbose_name='ID of application' |
| `is_creation` | `models.BooleanField` | default=False, verbose_name='whether current description...' |

**Relationships (1):**
- `application`: models.ForeignKey → ``Application``

##### `ApplicationEnvironment`
**Module:** `apiserver.paasng.paasng.platform.applications.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** 记录蓝鲸应用在不同部署环境下对应的 Engine App

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `environment` | `models.CharField` | max_length=16, verbose_name='部署环境' |
| `is_offlined` | `models.BooleanField` | default=False, help_text='是否已经下线，仅成功下线后变为False' |

**Relationships (3):**
- `application`: models.ForeignKey → ``Application``
- `module`: models.ForeignKey → `modules.Module`
- `engine_app`: models.OneToOneField → `engine.EngineApp`

**Meta:**
- unique_together: `module`, `environment`

##### `ApplicationFeatureFlag`
**Module:** `apiserver.paasng.paasng.platform.applications.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `effect` | `models.BooleanField` | default=True |
| `name` | `models.CharField` | max_length=30 |

**Relationships (1):**
- `application`: models.ForeignKey → ``Application``

##### `ApplicationGradeManager`
**Module:** `apiserver.paasng.paasng.infras.iam.members.models`
**Inherits from:** `paasng.utils.models.AuditedModel`

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `app_code` | `models.CharField` | help_text='应用代号', max_length=20 |
| `grade_manager_id` | `models.IntegerField` | help_text='分级管理员 ID' |

**Meta:**
- unique_together: `app_code`, `grade_manager_id`

##### `ApplicationLatestOp`
**Module:** `apiserver.paasng.paasng.misc.operations.models`
**Inherits from:** `models.Model`
**Description:** A mapper table which saves application's latest operation

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `latest_operated_at` | `models.DateTimeField` | db_index=True |
| `operation_type` | `models.SmallIntegerField` | help_text='操作类型' |

**Relationships (2):**
- `application`: models.OneToOneField → ``Application``
- `operation`: models.OneToOneField → ``Operation``

##### `ApplicationMembership`
**Module:** `apiserver.paasng.paasng.platform.applications.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** [deprecated] 切换为权限中心用户组存储用户信息

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `role` | `models.IntegerField` | default='`ApplicationRole.DEVELOPER....' |

**Relationships (1):**
- `application`: models.ForeignKey → ``Application``

**Meta:**
- unique_together: `user`, `application`, `role`

##### `ApplicationUserGroup`
**Module:** `apiserver.paasng.paasng.infras.iam.members.models`
**Inherits from:** `paasng.utils.models.AuditedModel`

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `app_code` | `models.CharField` | help_text='应用代号', max_length=20 |
| `role` | `models.IntegerField` | default='`ApplicationRole.DEVELOPER....' |
| `user_group_id` | `models.IntegerField` | help_text='权限中心用户组 ID' |

**Meta:**
- unique_together: `app_code`, `role`

##### `ApprovalService`
**Module:** `...r.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`
**Description:** 审批服务信息

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `service_id` | `models.IntegerField` | help_text='用于在 ITSM 上提申请单据', verbose_name='审批服务ID' |
| `service_name` | `models.CharField` | max_length=64, unique=True, verbose_name='审批服务名称' |

##### `AuditedModel`
**Module:** `apiserver.paasng.paas_wl.utils.models`
**Inherits from:** `models.Model`
**Description:** Audited model with 'created' and 'updated' fields.

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `created` | `models.DateTimeField` | auto_now_add=True |
| `updated` | `models.DateTimeField` | auto_now=True |

**Meta:**
- abstract: `True`

##### `AuditedModel`
**Module:** `apiserver.paasng.paasng.utils.models`
**Inherits from:** `models.Model`
**Description:** Audited model with 'created' and 'updated' fields.

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `created` | `models.DateTimeField` | auto_now_add=True |
| `updated` | `models.DateTimeField` | auto_now=True |

**Meta:**
- abstract: `True`

##### `AuthenticatedAppAsUser`
**Module:** `apiserver.paasng.paasng.infras.accounts.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** Store relationships which treat an authenticated(by API Gateway) app as an regular user,

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `bk_app_code` | `models.CharField` | max_length=64, unique=True |
| `is_active` | `models.BooleanField` | default=True |

**Relationships (1):**
- `user`: models.ForeignKey → ``User``

##### `BKMonitorSpace`
**Module:** `apiserver.paasng.paasng.infras.bkmonitorv3.models`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `extra_info` | `models.JSONField` | help_text='蓝鲸监控API-metadata_get_space_...' |
| `id` | `models.IntegerField` | verbose_name='蓝鲸监控空间 id' |
| `space_id` | `models.CharField` | help_text='同一空间类型下唯一', max_length=48, verbose_name='空间id' |
| `space_name` | `models.CharField` | max_length=64, verbose_name='空间名称' |
| `space_type_id` | `models.CharField` | max_length=48, verbose_name='空间类型id' |
| `space_uid` | `models.CharField` | help_text='{space_type_id}__{space_id}', max_length=48, verbose_name='蓝鲸监控空间 uid' |

**Relationships (1):**
- `application`: models.OneToOneField → ``Application``

**Meta:**
- unique_together: `space_type_id`, `space_id`

##### `BaseOperation`
**Module:** `apiserver.paasng.paasng.misc.audit.models`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`

**Fields (11):**

| Field | Type | Parameters |
|-------|------|------------|
| `access_type` | `models.IntegerField` | choices='`AccessType.get_choices()`', default='`AccessType.WEB`', verbose_name='访问方式' |
| `attribute` | `models.CharField` | blank=True, help_text='如增强服务的属性可以为：mysql、bkrepo', max_length=32... |
| `data_after` | `models.JSONField` | blank=True, null=True, verbose_name='操作后的数据' |
| `data_before` | `models.JSONField` | blank=True, null=True, verbose_name='操作前的数据' |
| `end_time` | `models.DateTimeField` | help_text='仅需要后台执行的的操作才需要记录结束时间', null=True |
| `environment` | `models.CharField` | blank=True, choices='`AppEnvName.get_choices()`', max_length=16... |
| `module_name` | `models.CharField` | blank=True, max_length=32, null=True... |
| `operation` | `models.CharField` | choices='`OperationEnum.get_choices()`', max_length=32, verbose_name='操作类型' |
| `result_code` | `models.IntegerField` | choices='`ResultCode.get_choices()`', default='`ResultCode.SUCCESS`', verbose_name='操作结果' |
| `start_time` | `models.DateTimeField` | auto_now_add=True, db_index=True, verbose_name='开始时间' |
| `target` | `models.CharField` | choices='`OperationTarget.get_choice...', max_length=32, verbose_name='操作对象' |

**Meta:**
- abstract: `True`

##### `BasicCert`
**Module:** `apiserver.paasng.paas_wl.workloads.networking.ingress.models`
**Inherits from:** `paas_wl.bk_app.applications.models.AuditedModel`

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `name` | `models.CharField` | max_length=128, unique=True, validators=[1 items] |
| `region` | `models.CharField` | max_length=32 |

**Meta:**
- abstract: `True`

##### `BkAppManagedFields`
**Module:** `apiserver.paasng.paasng.platform.bkapp_model.models`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** This model stores the management status of the fields of a module's bkapp model, it's

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `fields` | `models.JSONField` | default=[0 items], help_text='所管理的字段' |
| `manager` | `models.CharField` | help_text='管理者类型', max_length=20 |

**Relationships (1):**
- `module`: models.ForeignKey → `modules.Module`

**Meta:**
- unique_together: `module`, `manager`

##### `BkAppSecretInEnvVar`
**Module:** `apiserver.paasng.paasng.infras.oauth2.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `bk_app_code` | `models.CharField` | max_length=20, unique=True |
| `bk_app_secret_id` | `models.IntegerField` | help_text='不存储密钥的信息，仅存储密钥 ID', verbose_name='应用密钥的 ID' |

##### `BkPluginDistributor`
**Module:** `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** A "Distributor" is responsible for providing a collection of BkPlugins to a group of users,

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `bk_app_code` | `models.CharField` | help_text='插件使用方所绑定的蓝鲸应用代号', max_length=20, unique=True |
| `code_name` | `models.CharField` | help_text='插件使用方的英文代号，可替代主键使用', max_length=32, unique=True |
| `introduction` | `models.CharField` | blank=True, max_length=512, null=True |
| `name` | `models.CharField` | help_text='插件使用方名称', max_length=32, unique=True |

**Relationships (1):**
- `plugins`: models.ManyToManyField → ``Application``

##### `BkPluginProfile`
**Module:** `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** Profile which storing extra information for BkPlugins

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `api_gw_id` | `models.IntegerField` | null=True |
| `api_gw_last_synced_at` | `models.DateTimeField` | null=True |
| `api_gw_name` | `models.CharField` | blank=True, help_text='为空时表示从未成功同步过，暂无已绑定网关', max_length=32... |
| `contact` | `models.CharField` | blank=True, help_text='使用 ; 分隔的用户名', max_length=128... |
| `introduction` | `models.CharField` | blank=True, help_text='插件简介', max_length=512... |
| `pre_distributor_codes` | `models.JSONField` | blank=True, null=True |

**Relationships (2):**
- `application`: models.OneToOneField → ``Application``
- `tag`: models.ForeignKey → `BkPluginTag`

##### `BkPluginTag`
**Module:** `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** Plugins and applications use different markets, and plugins should have their own separate tags

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `code_name` | `models.CharField` | help_text='分类英文名称，可替代主键使用', max_length=32, unique=True |
| `name` | `models.CharField` | help_text='插件使用方名称', max_length=32, unique=True |
| `priority` | `models.IntegerField` | default=0, help_text='数字越大，优先级越高' |

**Meta:**
- ordering: `-priority`, `name`

##### `Build`
**Module:** `apiserver.paasng.paas_wl.bk_app.applications.models.build`
**Inherits from:** `paas_wl.utils.models.UuidAuditedModel`

**Fields (13):**

| Field | Type | Parameters |
|-------|------|------------|
| `application_id` | `models.UUIDField` | null=True, verbose_name='所属应用' |
| `artifact_deleted` | `models.BooleanField` | default=False, help_text='slug/镜像是否已被清理' |
| `artifact_detail` | `models.JSONField` | help_text='构件详情(展示信息)' |
| `artifact_metadata` | `models.JSONField` | help_text='构件元信息, 包括 entrypoint/use_cn...' |
| `artifact_type` | `models.CharField` | default='`ArtifactType.SLUG`', help_text='构件类型', max_length=16 |
| `bkapp_revision_id` | `models.IntegerField` | help_text='与本次构建关联的 BkApp Revision id', null=True |
| `branch` | `models.CharField` | help_text='readable version, such as t...', max_length=128, null=True |
| `image` | `models.TextField` | help_text='运行 Build 的镜像地址. 如果构件类型为 ima...', null=True |
| `module_id` | `models.UUIDField` | null=True, verbose_name='所属模块' |
| `owner` | `models.CharField` | max_length=64 |
| `revision` | `models.CharField` | help_text='unique version, such as sha256', max_length=128, null=True |
| `slug_path` | `models.TextField` | help_text='slug path 形如 {region}/home/...', null=True |
| `source_type` | `models.CharField` | max_length=128, null=True |

**Relationships (1):**
- `app`: models.ForeignKey → `App`

**Meta:**
- get_latest_by: `created`
- ordering: `-created`

##### `BuildConfig`
**Module:** `apiserver.paasng.paasng.platform.modules.models.build_cfg`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `build_method` | `models.CharField` | default='`RuntimeType.BUILDPACK`', max_length=32, verbose_name='`_('构建方式')`' |
| `dockerfile_path` | `models.CharField` | help_text='`_('Dockerfile文件路径, 必须保证 Do...', max_length=512, null=True |
| `image_credential_name` | `models.CharField` | max_length=32, null=True, verbose_name='`_('镜像凭证名称')`' |
| `image_repository` | `models.TextField` | null=True, verbose_name='`_('镜像仓库')`' |
| `use_bk_ci_pipeline` | `models.BooleanField` | default=False, help_text='是否使用蓝盾流水线构建' |

**Relationships (4):**
- `module`: models.OneToOneField → `modules.Module`
- `buildpacks`: models.ManyToManyField → `modules.AppBuildPack`
- `buildpack_builder`: models.ForeignKey → `modules.AppSlugBuilder`
- `buildpack_runner`: models.ForeignKey → `modules.AppSlugRunner`

##### `BuildProcess`
**Module:** `apiserver.paasng.paas_wl.bk_app.applications.models.build`
**Inherits from:** `paas_wl.utils.models.UuidAuditedModel`
**Description:** This Build Process was invoked via a source tarball or anything similar

**Fields (13):**

| Field | Type | Parameters |
|-------|------|------------|
| `application_id` | `models.UUIDField` | null=True, verbose_name='所属应用' |
| `branch` | `models.CharField` | max_length=128, null=True |
| `completed_at` | `models.DateTimeField` | help_text='failed/successful/interrupt...', null=True, verbose_name='完成时间' |
| `generation` | `models.PositiveBigIntegerField` | help_text='每个应用独立的自增ID', verbose_name='自增ID' |
| `image` | `models.CharField` | help_text='builder image', max_length=512, null=True |
| `int_requested_at` | `models.DateTimeField` | help_text='用户请求中断的时间', null=True |
| `invoke_message` | `models.CharField` | blank=True, help_text='触发信息', max_length=255... |
| `logs_was_ready_at` | `models.DateTimeField` | help_text='Pod 状态就绪允许读取日志的时间', null=True |
| `module_id` | `models.UUIDField` | null=True, verbose_name='所属模块' |
| `owner` | `models.CharField` | max_length=64 |
| `revision` | `models.CharField` | max_length=128, null=True |
| `source_tar_path` | `models.CharField` | max_length=2048 |
| `status` | `models.CharField` | choices='`make_enum_choices(BuildSta...', default='`BuildStatus.PENDING.value`', max_length=12 |

**Relationships (3):**
- `app`: models.ForeignKey → `App`
- `output_stream`: models.OneToOneField → `OutputStream`
- `build`: models.OneToOneField → `Build`

**Meta:**
- get_latest_by: `created`
- ordering: `-created`

##### `BuiltinConfigVar`
**Module:** `apiserver.paasng.paasng.platform.engine.models.config_var`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** Default config vars for global, can be added or edited in admin42.

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `description` | `models.CharField` | max_length=512, null=False, verbose_name='描述' |
| `key` | `models.CharField` | max_length=128, null=False, unique=True... |
| `value` | `models.TextField` | max_length=512, null=False, verbose_name='环境变量值' |

##### `CIResourceAppEnvRelation`
**Module:** `apiserver.paasng.paasng.accessories.ci.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** CI 资源

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `backend` | `models.CharField` | choices='`CIBackend.get_django_choic...', max_length=32, verbose_name='CI引擎' |
| `enabled` | `models.BooleanField` | default=True, verbose_name='是否启用' |

**Relationships (1):**
- `env`: models.ForeignKey → `applications.ApplicationEnvironment`

**Meta:**
- get_latest_by: `created`

##### `CIResourceAtom`
**Module:** `apiserver.paasng.paasng.accessories.ci.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** CI 资源原子

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `backend` | `models.CharField` | choices='`CIBackend.get_django_choic...', max_length=32, verbose_name='CI引擎' |
| `enabled` | `models.BooleanField` | default=True, verbose_name='是否启用' |
| `id` | `models.CharField` | db_index=True, max_length=64, primary_key=True... |
| `name` | `models.CharField` | max_length=32 |

**Relationships (2):**
- `env`: models.ForeignKey → `applications.ApplicationEnvironment`
- `resource`: models.ForeignKey → ``CIResourceAppEnvRelation``

**Meta:**
- unique_together: `env`, `name`, `backend`

##### `CNativeMigrationProcess`
**Module:** `apiserver.paasng.paasng.platform.mgrlegacy.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `confirm_at` | `models.DateTimeField` | help_text='用户确认的时间', null=True |
| `created_at` | `models.DateTimeField` | auto_now_add=True, help_text='操作记录的创建时间' |
| `status` | `models.CharField` | choices='`CNativeMigrationStatus.get...', default='`CNativeMigrationStatus.DEF...', max_length=20 |

**Relationships (1):**
- `app`: models.ForeignKey → ``Application``

**Meta:**
- get_latest_by: `created_at`
- ordering: `created_at`

##### `Cluster`
**Module:** `apiserver.paasng.paas_wl.infras.cluster.models`
**Inherits from:** `paas_wl.utils.models.UuidAuditedModel`
**Description:** 应用集群

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `description` | `models.TextField` | blank=True, help_text='描述信息' |
| `is_default` | `models.BooleanField` | default=False, help_text='是否为默认集群', null=True |
| `name` | `models.CharField` | help_text='name of the cluster', max_length=32, unique=True |
| `region` | `models.CharField` | db_index=True, max_length=32 |
| `token_type` | `models.IntegerField` | null=True |
| `type` | `models.CharField` | default='`ClusterType.NORMAL`', help_text='cluster type', max_length=32 |

##### `Cluster`
**Module:** `svc-rabbitmq.vendor.models`
**Inherits from:** `paas_service.models.AuditedModel`

**Fields (7):**

| Field | Type | Parameters |
|-------|------|------------|
| `admin` | `models.CharField` | max_length=64 |
| `enable` | `models.BooleanField` | default=True |
| `host` | `models.CharField` | max_length=64 |
| `management_api` | `models.TextField` | - |
| `name` | `models.CharField` | max_length=64 |
| `port` | `models.IntegerField` | default=5672 |
| `version` | `models.CharField` | max_length=16 |

##### `ClusterTag`
**Module:** `svc-rabbitmq.vendor.models`
**Inherits from:** `svc-rabbitmq.vendor.models.Tag`
**Description:** 集群标签，用于分配和分组

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `key` | `models.CharField` | max_length=64 |
| `value` | `models.CharField` | max_length=128 |

**Relationships (1):**
- `instance`: models.ForeignKey → ``Cluster``

##### `CodeEditor`
**Module:** `apiserver.paasng.paasng.accessories.dev_sandbox.models`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`
**Description:** CodeEditor Model

**Relationships (1):**
- `dev_sandbox`: models.OneToOneField → ``DevSandbox``

##### `Command`
**Module:** `....paasng.paas_wl.workloads.release_controller.hooks.models`
**Inherits from:** `paas_wl.utils.models.UuidAuditedModel`
**Description:** The Command Model, which will be used to schedule a container running `command`,

**Fields (8):**

| Field | Type | Parameters |
|-------|------|------------|
| `command` | `models.TextField` | - |
| `exit_code` | `models.SmallIntegerField` | help_text='容器结束状态码, -1 表示未知', null=True |
| `int_requested_at` | `models.DateTimeField` | help_text='用户请求中断的时间', null=True |
| `logs_was_ready_at` | `models.DateTimeField` | help_text='Pod 状态就绪允许读取日志的时间', null=True |
| `operator` | `models.CharField` | help_text='操作者(被编码的 username), 目前该字段无意义', max_length=64 |
| `status` | `models.CharField` | choices='`CommandStatus.get_choices()`', default='`CommandStatus.PENDING.value`', max_length=12 |
| `type` | `models.CharField` | choices='`CommandType.get_choices()`', max_length=32 |
| `version` | `models.PositiveIntegerField` | - |

**Relationships (4):**
- `app`: models.ForeignKey → `api.App`
- `output_stream`: models.OneToOneField → `api.OutputStream`
- `build`: models.ForeignKey → `api.Build`
- `config`: models.ForeignKey → `api.Config`

**Meta:**
- get_latest_by: `created`
- ordering: `-created`

##### `Config`
**Module:** `apiserver.paasng.paas_wl.bk_app.applications.models.config`
**Inherits from:** `paas_wl.bk_app.applications.models.UuidAuditedModel`
**Description:** App configs, includes env variables and resource limits

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `cluster` | `models.CharField` | blank=True, default='', max_length=64 |
| `domain` | `models.CharField` | default='', max_length=64 |
| `image` | `models.CharField` | max_length=256, null=True |
| `mount_log_to_host` | `models.BooleanField` | default=True, help_text='Whether mount app logs to host' |
| `owner` | `models.CharField` | max_length=64 |

**Relationships (1):**
- `app`: models.ForeignKey → `App`

**Meta:**
- get_latest_by: `created`
- ordering: `-created`
- unique_together: `['app', 'uuid']`

##### `ConfigMapSource`
**Module:** `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.mount`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** ConfigMap 类型的挂载资源

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `application_id` | `models.UUIDField` | null=False, verbose_name='`_('所属应用')`' |
| `data` | `models.JSONField` | default='`dict`' |
| `display_name` | `models.CharField` | help_text='`_('挂载资源展示名称')`', max_length=63, null=True |
| `environment_name` | `models.CharField` | choices='`MountEnvName.get_choices()`', max_length=16, null=False... |
| `module_id` | `models.UUIDField` | null=True, verbose_name='`_('所属模块')`' |
| `name` | `models.CharField` | help_text='`_('挂载资源名')`', max_length=63 |

**Meta:**
- unique_together: `name`, `application_id`, `environment_name`

##### `ConfigVar`
**Module:** `apiserver.paasng.paasng.platform.engine.models.config_var`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** Config vars for application

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `description` | `models.CharField` | max_length=200, null=True |
| `is_builtin` | `models.BooleanField` | default=False |
| `is_global` | `models.BooleanField` | default=False |
| `key` | `models.CharField` | max_length=128, null=False |
| `value` | `models.TextField` | null=False |

**Relationships (2):**
- `module`: models.ForeignKey → `modules.Module`
- `environment`: models.ForeignKey → `applications.ApplicationEnvironment`

**Meta:**
- unique_together: `module`, `is_global`, `environment`, `key`

##### `CronTask`
**Module:** `svc-rabbitmq.tasks.models`
**Inherits from:** `models.Model`

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `enabled` | `models.BooleanField` | default=False |
| `interval` | `models.DurationField` | - |
| `last_run_time` | `models.DateTimeField` | blank=True, null=True |
| `name` | `models.CharField` | max_length=255, unique=True |
| `next_run_time` | `models.DateTimeField` | blank=True, db_index=True, default='`get_now`'... |

**Meta:**
- ordering: `next_run_time`, `name`

##### `CustomCollectorConfig`
**Module:** `apiserver.paasng.paasng.accessories.log.models`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`
**Description:** 日志平台自定义采集项配置

**Fields (8):**

| Field | Type | Parameters |
|-------|------|------------|
| `bk_data_id` | `models.BigIntegerField` | - |
| `collector_config_id` | `models.BigIntegerField` | db_index=True, help_text='采集配置ID' |
| `index_set_id` | `models.BigIntegerField` | help_text='查询时使用', null=True |
| `is_builtin` | `models.BooleanField` | default=False |
| `is_enabled` | `models.BooleanField` | default=True |
| `log_paths` | `models.JSONField` | - |
| `log_type` | `models.CharField` | max_length=32 |
| `name_en` | `models.CharField` | db_index=True, help_text='5-50个字符，仅包含字母数字下划线, 查询索引是 n...', max_length=50 |

**Relationships (1):**
- `module`: models.ForeignKey → ``Module``

**Meta:**
- unique_together: `module`, `name_en`

##### `DeployConfig`
**Module:** `...erver.paasng.paasng.platform.modules.models.deploy_config`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`

**Relationships (1):**
- `module`: models.OneToOneField → `modules.Module`

##### `DeployFailurePattern`
**Module:** `apiserver.paasng.paasng.accessories.smart_advisor.models`
**Inherits from:** `models.Model`
**Description:** Stores common failure patterns for failed deployments

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `created` | `models.DateTimeField` | default='`timezone.now`' |
| `tag_str` | `models.CharField` | blank=False, max_length=128 |
| `type` | `models.IntegerField` | default='`DeployFailurePatternType.R...' |
| `value` | `models.CharField` | blank=False, max_length=2048 |

##### `DeployPhase`
**Module:** `apiserver.paasng.paasng.platform.engine.models.phases`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`, `paasng.platform.engine.models.MarkStatusMixin`
**Description:** 部署阶段

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `complete_time` | `models.DateTimeField` | null=True |
| `start_time` | `models.DateTimeField` | null=True |
| `status` | `models.CharField` | choices='`JobStatus.get_choices()`', max_length=32, null=True |
| `type` | `models.CharField` | choices='`DeployPhaseTypes.get_choic...', max_length=32 |

**Relationships (2):**
- `engine_app`: models.ForeignKey → ``EngineApp``
- `deployment`: models.ForeignKey → ``Deployment``

**Meta:**
- ordering: `created`

##### `DeployStep`
**Module:** `apiserver.paasng.paasng.platform.engine.models.steps`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`, `paasng.platform.engine.models.base.MarkStatusMixin`
**Description:** 部署步骤

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `complete_time` | `models.DateTimeField` | null=True |
| `name` | `models.CharField` | db_index=True, max_length=32 |
| `skipped` | `models.BooleanField` | default=False |
| `start_time` | `models.DateTimeField` | null=True |
| `status` | `models.CharField` | choices='`JobStatus.get_choices()`', max_length=32, null=True |

**Relationships (2):**
- `phase`: models.ForeignKey → ``DeployPhase``
- `meta`: models.ForeignKey → ``DeployStepMeta``

**Meta:**
- ordering: `created`

##### `DeployStepMeta`
**Module:** `apiserver.paasng.paasng.platform.engine.models.steps`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 部署步骤元信息

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `name` | `models.CharField` | db_index=True, max_length=32 |
| `phase` | `models.CharField` | choices='`DeployPhaseTypes.get_choic...', max_length=16, verbose_name='`_('关联阶段')`' |

**Meta:**
- ordering: `id`

##### `DeploymentDescription`
**Module:** `apiserver.paasng.paasng.platform.declarative.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** Config objects which describes deployment objects.

**Relationships (1):**
- `deployment`: models.OneToOneField → ``Deployment``

##### `DevSandbox`
**Module:** `apiserver.paasng.paasng.accessories.dev_sandbox.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** DevSandbox Model

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `code` | `models.CharField` | help_text='沙箱标识', max_length=8, unique=True |
| `expired_at` | `models.DateTimeField` | help_text='到期时间', null=True |
| `status` | `models.CharField` | choices='`DevSandboxStatus.get_choic...', max_length=32, verbose_name='沙箱状态' |

**Relationships (1):**
- `module`: models.ForeignKey → ``Module``

**Meta:**
- unique_together: `module`, `owner`

##### `DisplayOptions`
**Module:** `apiserver.paasng.paasng.accessories.publish.market.models`
**Inherits from:** `models.Model`
**Description:** app展示相关的属性

**Fields (8):**

| Field | Type | Parameters |
|-------|------|------------|
| `contact` | `models.CharField` | blank=True, max_length=128, null=True |
| `height` | `models.IntegerField` | default=550, help_text='应用页面高度，必须为整数，单位为px' |
| `is_win_maximize` | `models.BooleanField` | default=False |
| `open_mode` | `models.CharField` | choices='`constant.OpenMode.get_djan...', default='`constant.OpenMode.NEW_TAB....', max_length=20 |
| `resizable` | `models.BooleanField` | default=True, help_text='选项：true(可以拉伸)，false(不可以拉伸)' |
| `visible` | `models.BooleanField` | default=True, help_text='选项: true(是)，false(否)' |
| `width` | `models.IntegerField` | default=890, help_text='应用页面宽度，必须为整数，单位为px' |
| `win_bars` | `models.BooleanField` | default=True, help_text='选项: true(on)，false(off)' |

**Relationships (1):**
- `product`: models.OneToOneField → ``Product``

##### `DockerRepository`
**Module:** `apiserver.paasng.paasng.platform.sourcectl.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`, `apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin`
**Description:** 容器镜像仓库

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `repo_url` | `models.CharField` | help_text='形如 registry.hub.docker.com/...', max_length=2048, verbose_name='项目地址' |
| `server_name` | `models.CharField` | max_length=32, verbose_name='DockerRegistry 服务名称' |
| `source_dir` | `models.CharField` | max_length=2048, null=True, verbose_name='源码目录' |

##### `DocumentaryLink`
**Module:** `apiserver.paasng.paasng.accessories.smart_advisor.models`
**Inherits from:** `models.Model`
**Description:** Links from document systems including blueking doc and other opensource documentations

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `created` | `models.DateTimeField` | default='`timezone.now`' |
| `location` | `models.CharField` | blank=False, max_length=256 |
| `priority` | `models.IntegerField` | default=1 |

##### `Domain`
**Module:** `apiserver.paasng.paas_wl.workloads.networking.ingress.models`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** custom domain for application

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `environment_id` | `models.BigIntegerField` | help_text='关联的环境 ID', null=False |
| `https_enabled` | `models.BooleanField` | default=False, help_text='该域名是否开启 https', null=True |
| `module_id` | `models.UUIDField` | help_text='关联的模块 ID', null=False |
| `name` | `models.CharField` | help_text='域名', max_length=253, null=False |
| `path_prefix` | `models.CharField` | default='/', help_text='the accessable path for cur...', max_length=64 |

**Meta:**
- db_table: `services_domain`
- unique_together: `name`, `path_prefix`, `module_id`, `environment_id`

##### `DomainResolution`
**Module:** `apiserver.paasng.paasng.platform.bkapp_model.models`
**Inherits from:** `paas_wl.utils.models.AuditedModel`
**Description:** 域名解析配置

**Relationships (1):**
- `application`: models.ForeignKey → ``Application``

##### `EgressRule`
**Module:** `apiserver.paasng.paas_wl.workloads.networking.egress.models`
**Inherits from:** `paas_wl.bk_app.applications.models.AuditedModel`
**Description:** BCS Egress.spec.rules

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `dst_port` | `models.IntegerField` | - |
| `host` | `models.CharField` | max_length=128 |
| `protocol` | `models.CharField` | choices='`NetworkProtocol.get_django...', max_length=32 |
| `service` | `models.CharField` | max_length=128 |
| `src_port` | `models.IntegerField` | - |

**Relationships (1):**
- `spec`: models.ForeignKey → ``EgressSpec``

##### `EgressSpec`
**Module:** `apiserver.paasng.paas_wl.workloads.networking.egress.models`
**Inherits from:** `paas_wl.bk_app.applications.models.AuditedModel`

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `cpu_limit` | `models.CharField` | max_length=16 |
| `memory_limit` | `models.CharField` | max_length=16 |
| `replicas` | `models.IntegerField` | default=1 |

**Relationships (1):**
- `wl_app`: models.OneToOneField → ``WlApp``

##### `ElasticSearchConfig`
**Module:** `apiserver.paasng.paasng.accessories.log.models`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`
**Description:** ES查询配置

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `backend_type` | `models.CharField` | help_text='日志后端类型, 可选 'es', 'bkLog' ', max_length=16 |
| `collector_config_id` | `models.CharField` | help_text='采集配置ID', max_length=64, unique=True |

##### `EngineApp`
**Module:** `apiserver.paasng.paasng.platform.engine.models.base`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** 蓝鲸应用引擎应用

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `id` | `models.UUIDField` | auto_created=True, default='`uuid.uuid4`', editable=False... |
| `is_active` | `models.BooleanField` | default=True, verbose_name='是否活跃' |
| `name` | `models.CharField` | max_length=64, unique=True |
| `region` | `models.CharField` | max_length=32 |

##### `EnvRoleProtection`
**Module:** `apiserver.paasng.paasng.platform.environments.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** 模块环境角色保护

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `allowed_role` | `models.IntegerField` | choices='`ApplicationRole.get_django...' |
| `operation` | `models.CharField` | choices='`EnvRoleOperation.get_choic...', max_length=64 |

**Relationships (1):**
- `module_env`: models.ForeignKey → ``ModuleEnvironment``

##### `GitRepository`
**Module:** `apiserver.paasng.paasng.platform.sourcectl.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`, `apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin`
**Description:** 基于 Git 的软件存储库

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `repo_url` | `models.CharField` | max_length=2048, verbose_name='项目地址' |
| `server_name` | `models.CharField` | max_length=32, verbose_name='GIT 服务名称' |
| `source_dir` | `models.CharField` | max_length=2048, null=True, verbose_name='源码目录' |

##### `IdleAppNotificationMuteRule`
**Module:** `apiserver.paasng.paasng.platform.evaluation.models`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 闲置应用通知屏蔽规则

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `app_code` | `models.CharField` | max_length=32 |
| `environment` | `models.CharField` | max_length=32 |
| `expired_at` | `models.DateTimeField` | - |
| `module_name` | `models.CharField` | max_length=32 |

**Meta:**
- unique_together: `user`, `app_code`, `module_name`, `environment`

##### `InstanceBill`
**Module:** `svc-rabbitmq.vendor.models`
**Inherits from:** `paas_service.models.UuidAuditedModel`
**Description:** 实例单据，保存申请上下文，方便重入

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `action` | `models.CharField` | max_length=32 |
| `name` | `models.CharField` | max_length=128 |

##### `LimitPolicy`
**Module:** `svc-rabbitmq.vendor.models`
**Inherits from:** `svc-rabbitmq.vendor.models.LinkableModel`
**Description:** 集群下创建 vhost 限制机制，和具体 vhost 无关

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `cluster_id` | `models.IntegerField` | blank=True |
| `enable` | `models.BooleanField` | default=True |
| `limit` | `models.CharField` | blank=True, choices='`[(i.value, i.name) for i i...', max_length=64... |
| `link_type` | `models.IntegerField` | choices='`[(i.value, i.name) for i i...', default='`LinkType.empty.value`' |
| `name` | `models.CharField` | max_length=64, null=True |
| `value` | `models.IntegerField` | blank=True, null=True |

**Relationships (1):**
- `linked`: models.ForeignKey → `self`

##### `LimitPolicyTag`
**Module:** `svc-rabbitmq.vendor.models`
**Inherits from:** `svc-rabbitmq.vendor.models.Tag`
**Description:** 表示绑定关系

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `key` | `models.CharField` | max_length=64 |
| `value` | `models.CharField` | max_length=128 |

**Relationships (1):**
- `instance`: models.ForeignKey → ``LimitPolicy``

##### `LinkableModel`
**Module:** `svc-rabbitmq.vendor.models`
**Inherits from:** `paas_service.models.AuditedModel`

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `link_type` | `models.IntegerField` | choices='`[(i.value, i.name) for i i...', default='`LinkType.empty.value`' |

**Relationships (1):**
- `linked`: models.ForeignKey → `self`

**Meta:**
- abstract: `True`

##### `MarketConfig`
**Module:** `apiserver.paasng.paasng.accessories.publish.market.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** 应用市场相关功能配置

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `auto_enable_when_deploy` | `models.BooleanField` | null=True, verbose_name='成功部署主模块正式环境后, 是否自动打开市场' |
| `custom_domain_url` | `models.URLField` | blank=True, null=True, verbose_name='绑定的独立域名访问地址' |
| `enabled` | `models.BooleanField` | verbose_name='是否开启' |
| `prefer_https` | `models.BooleanField` | null=True, verbose_name='[deprecated] 仅为 False 时强制使用...' |
| `source_tp_url` | `models.URLField` | blank=True, null=True, verbose_name='第三方访问地址' |
| `source_url_type` | `models.SmallIntegerField` | verbose_name='访问地址类型' |

**Relationships (2):**
- `application`: models.OneToOneField → ``Application``
- `source_module`: models.ForeignKey → ``Module``

##### `MigrationProcess`
**Module:** `apiserver.paasng.paasng.platform.mgrlegacy.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** An migration process

**Fields (10):**

| Field | Type | Parameters |
|-------|------|------------|
| `confirmed_date` | `models.DateTimeField` | null=True |
| `failed_date` | `models.DateTimeField` | null=True |
| `legacy_app_has_all_deployed` | `models.BooleanField` | default=True |
| `legacy_app_id` | `models.IntegerField` | - |
| `legacy_app_is_already_online` | `models.BooleanField` | default=True |
| `legacy_app_logo` | `models.CharField` | max_length=500, null=True |
| `legacy_app_state` | `models.IntegerField` | default=4 |
| `migrated_date` | `models.DateTimeField` | null=True |
| `rollbacked_date` | `models.DateTimeField` | null=True |
| `status` | `models.IntegerField` | choices='`MigrationStatus.get_choice...', default='`MigrationStatus.DEFAULT.va...' |

**Relationships (1):**
- `app`: models.ForeignKey → ``Application``

##### `MobileConfig`
**Module:** `apiserver.paasng.paasng.platform.engine.models.mobile_config`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** Mobile config switcher for application

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `access_url` | `models.URLField` | blank=True, default='', null=True |
| `is_enabled` | `models.BooleanField` | default=False |
| `lb_plan` | `models.CharField` | choices='`LBPlans.get_choices()`', default='`LBPlans.LBDefaultPlan.value`', help_text='which one-level load balanc...'... |

**Relationships (1):**
- `environment`: models.OneToOneField → `applications.ApplicationEnvironment`

##### `Module`
**Module:** `apiserver.paasng.paasng.platform.modules.models.module`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** Module for Application

**Fields (11):**

| Field | Type | Parameters |
|-------|------|------------|
| `exposed_url_type` | `models.IntegerField` | null=True, verbose_name='访问 URL 版本' |
| `id` | `models.UUIDField` | auto_created=True, default='`uuid.uuid4`', editable=False... |
| `is_default` | `models.BooleanField` | default=False, verbose_name='是否为默认模块' |
| `language` | `models.CharField` | max_length=32, verbose_name='编程语言' |
| `last_deployed_date` | `models.DateTimeField` | null=True, verbose_name='最近部署时间' |
| `name` | `models.CharField` | max_length=20, verbose_name='模块名称' |
| `source_init_template` | `models.CharField` | max_length=32, verbose_name='初始化模板类型' |
| `source_origin` | `models.SmallIntegerField` | null=True, verbose_name='源码来源' |
| `source_repo_id` | `models.IntegerField` | null=True, verbose_name='源码 ID' |
| `source_type` | `models.CharField` | max_length=16, null=True, verbose_name='源码托管类型' |
| `user_preferred_root_domain` | `models.CharField` | max_length=255, null=True, verbose_name='用户偏好的根域名' |

**Relationships (1):**
- `application`: models.ForeignKey → `applications.Application`

**Meta:**
- unique_together: `application`, `name`

##### `ModuleDeployHook`
**Module:** `apiserver.paasng.paasng.platform.bkapp_model.models`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** 钩子命令

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `enabled` | `models.BooleanField` | default=False, help_text='是否已开启' |
| `proc_command` | `models.TextField` | help_text='进程启动命令(包含完整命令和参数的字符串), 只能与 ...', null=True |
| `type` | `models.CharField` | choices='`DeployHookType.get_choices()`', help_text='钩子类型', max_length=20 |

**Relationships (1):**
- `module`: models.ForeignKey → `modules.Module`

**Meta:**
- unique_together: `module`, `type`

##### `ModuleEnvironmentOperations`
**Module:** `apiserver.paasng.paasng.platform.engine.models.operations`
**Inherits from:** `paasng.utils.models.TimestampedModel`

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `id` | `models.UUIDField` | auto_created=True, default='`uuid.uuid4`', editable=False... |
| `object_uid` | `models.UUIDField` | default='`uuid.uuid4`', editable=False |
| `operation_type` | `models.CharField` | choices='`OperationTypes.get_choices()`', max_length=32 |
| `status` | `models.CharField` | choices='`JobStatus.get_choices()`', default='`JobStatus.PENDING.value`', max_length=16 |

**Relationships (2):**
- `application`: models.ForeignKey → `applications.Application`
- `app_environment`: models.ForeignKey → `applications.ApplicationEnvironment`

##### `ModuleProcessSpec`
**Module:** `apiserver.paasng.paasng.platform.bkapp_model.models`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** 模块维度的进程定义, 表示模块当前所定义的进程, 该模型只通过 API 变更

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `autoscaling` | `models.BooleanField` | default=False |
| `name` | `models.CharField` | max_length=32 |
| `plan_name` | `models.CharField` | help_text='仅存储方案名称', max_length=32 |
| `port` | `models.IntegerField` | help_text='[deprecated] 容器端口', null=True |
| `proc_command` | `models.TextField` | help_text='进程启动命令(包含完整命令和参数的字符串), 只能与 ...', null=True |
| `target_replicas` | `models.IntegerField` | default=1 |

**Relationships (1):**
- `module`: models.ForeignKey → `modules.Module`

**Meta:**
- ordering: `id`
- unique_together: `module`, `name`

##### `Mount`
**Module:** `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.mount`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** 挂载配置

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `environment_name` | `models.CharField` | choices='`MountEnvName.get_choices()`', max_length=16, null=False... |
| `module_id` | `models.UUIDField` | null=False, verbose_name='`_('所属模块')`' |
| `mount_path` | `models.CharField` | max_length=128 |
| `name` | `models.CharField` | help_text='`_('挂载点的名称')`', max_length=63 |
| `source_type` | `models.CharField` | choices='`VolumeSourceType.get_choic...', max_length=32 |

**Meta:**
- unique_together: `module_id`, `mount_path`, `environment_name`

##### `OAuth2Client`
**Module:** `apiserver.paasng.paasng.infras.oauth2.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** OAuth2 体系中的基本单位：Client

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `client_id` | `models.CharField` | max_length=20, unique=True, verbose_name='应用编码' |

##### `Oauth2TokenHolder`
**Module:** `apiserver.paasng.paasng.infras.accounts.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** OAuth2 Token for sourcectl

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `expire_at` | `models.DateTimeField` | blank=True, null=True |
| `provider` | `models.CharField` | max_length=32 |
| `token_type` | `models.CharField` | max_length=16 |

**Relationships (1):**
- `user`: models.ForeignKey → ``UserProfile``

##### `ObservabilityConfig`
**Module:** `apiserver.paasng.paasng.platform.bkapp_model.models`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`

**Relationships (1):**
- `module`: models.OneToOneField → `modules.Module`

##### `Operation`
**Module:** `apiserver.paasng.paasng.misc.operations.models`
**Inherits from:** `models.Model`

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `created` | `models.DateTimeField` | auto_now_add=True, db_index=True |
| `is_hidden` | `models.BooleanField` | default=False, help_text='隐藏起来' |
| `module_name` | `models.CharField` | max_length=20, null=True, verbose_name='关联 Module' |
| `region` | `models.CharField` | help_text='部署区域', max_length=32 |
| `source_object_id` | `models.CharField` | blank=True, default='', help_text='事件来源对象ID，具体指向需要根据操作类型解析'... |
| `type` | `models.SmallIntegerField` | db_index=True, help_text='操作类型' |

**Relationships (1):**
- `application`: models.ForeignKey → ``Application``

##### `OperationRecord`
**Module:** `...r.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 插件操作记录

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `action` | `models.CharField` | choices='`constants.ActionTypes.get_...', max_length=32 |
| `specific` | `models.CharField` | max_length=255, null=True |
| `subject` | `models.CharField` | choices='`constants.SubjectTypes.get...', max_length=32 |

**Relationships (1):**
- `plugin`: models.ForeignKey → ``PluginInstance``

##### `OperationVersionBase`
**Module:** `apiserver.paasng.paasng.platform.engine.models.base`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** 带操作版本信息的BaseModel

**Fields (7):**

| Field | Type | Parameters |
|-------|------|------------|
| `id` | `models.UUIDField` | auto_created=True, default='`uuid.uuid4`', editable=False... |
| `source_comment` | `models.TextField` | - |
| `source_location` | `models.CharField` | max_length=2048 |
| `source_revision` | `models.CharField` | max_length=128, null=True |
| `source_type` | `models.CharField` | max_length=16, null=True, verbose_name='源码托管类型' |
| `source_version_name` | `models.CharField` | max_length=64 |
| `source_version_type` | `models.CharField` | max_length=64 |

**Meta:**
- abstract: `True`

##### `OutputStreamLine`
**Module:** `apiserver.paasng.paas_wl.bk_app.applications.models.misc`
**Inherits from:** `models.Model`

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `created` | `models.DateTimeField` | auto_now_add=True |
| `line` | `models.TextField` | - |
| `stream` | `models.CharField` | max_length=16 |
| `updated` | `models.DateTimeField` | auto_now=True |

**Relationships (1):**
- `output_stream`: models.ForeignKey → `OutputStream`

**Meta:**
- ordering: `created`

##### `OwnerTimestampedModel`
**Module:** `apiserver.paasng.paasng.utils.models`
**Inherits from:** `apiserver.paasng.paasng.utils.models.TimestampedModel`
**Description:** Model with 'created' and 'updated' fields.

**Meta:**
- abstract: `True`

##### `PersistentStorageSource`
**Module:** `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.mount`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** 持久存储类型的挂载资源

**Fields (7):**

| Field | Type | Parameters |
|-------|------|------------|
| `application_id` | `models.UUIDField` | null=False, verbose_name='`_('所属应用')`' |
| `display_name` | `models.CharField` | help_text='`_('挂载资源展示名称')`', max_length=63, null=True |
| `environment_name` | `models.CharField` | choices='`MountEnvName.get_choices()`', max_length=16, null=False... |
| `module_id` | `models.UUIDField` | null=True, verbose_name='`_('所属模块')`' |
| `name` | `models.CharField` | help_text='`_('挂载资源名')`', max_length=63 |
| `storage_class_name` | `models.CharField` | max_length=63 |
| `storage_size` | `models.CharField` | max_length=63 |

**Meta:**
- unique_together: `name`, `application_id`, `environment_name`

##### `Plan`
**Module:** `apiserver.paasng.paasng.accessories.services.models`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `description` | `models.CharField` | blank=True, max_length=1024, verbose_name='方案简介' |
| `is_active` | `models.BooleanField` | default=True, verbose_name='是否可用' |
| `name` | `models.CharField` | max_length=64 |

**Relationships (1):**
- `service`: models.ForeignKey → `Service`

**Meta:**
- unique_together: `service`, `name`

##### `PluginBasicInfoDefinition`
**Module:** `...paasng.paasng.bk_plugins.pluginscenter.models.definitions`
**Inherits from:** `paasng.utils.models.AuditedModel`

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `access_mode` | `models.CharField` | default='`PluginBasicInfoAccessMode....', max_length=16, verbose_name='基本信息查看模式' |
| `extra_fields_order` | `models.JSONField` | default='`list`' |
| `release_method` | `models.CharField` | max_length=16, verbose_name='发布方式' |
| `repository_group` | `models.CharField` | max_length=255, verbose_name='插件代码初始化仓库组' |

**Relationships (1):**
- `pd`: models.OneToOneField → ``PluginDefinition``

##### `PluginConfig`
**Module:** `...r.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 插件配置

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `row` | `models.JSONField` | default='`dict`', verbose_name='配置内容(1行), 格式 {'column_key':...' |
| `unique_key` | `models.CharField` | max_length=64, verbose_name='唯一标识' |

**Relationships (1):**
- `plugin`: models.ForeignKey → ``PluginInstance``

**Meta:**
- unique_together: `plugin`, `unique_key`

##### `PluginConfigInfoDefinition`
**Module:** `...paasng.paasng.bk_plugins.pluginscenter.models.definitions`
**Inherits from:** `paasng.utils.models.AuditedModel`

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `docs` | `models.CharField` | default='', max_length=255 |

**Relationships (1):**
- `pd`: models.OneToOneField → ``PluginDefinition``

##### `PluginDefinition`
**Module:** `...paasng.paasng.bk_plugins.pluginscenter.models.definitions`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `administrator` | `models.JSONField` | - |
| `docs` | `models.CharField` | max_length=255 |
| `identifier` | `models.CharField` | max_length=64, unique=True |
| `logo` | `models.CharField` | max_length=255 |

##### `PluginGradeManager`
**Module:** `...paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.models`
**Inherits from:** `paasng.utils.models.AuditedModel`

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `grade_manager_id` | `models.IntegerField` | help_text='分级管理员 ID' |
| `pd_id` | `models.CharField` | help_text='插件类型标识', max_length=64 |
| `plugin_id` | `models.CharField` | help_text='插件标识', max_length=32 |

**Meta:**
- unique_together: `pd_id`, `plugin_id`, `grade_manager_id`

##### `PluginInstance`
**Module:** `...r.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`
**Description:** 插件实例

**Fields (8):**

| Field | Type | Parameters |
|-------|------|------------|
| `extra_fields` | `models.JSONField` | verbose_name='额外字段' |
| `id` | `models.CharField` | help_text='插件id', max_length=32 |
| `is_deleted` | `models.BooleanField` | default=False, help_text='是否已删除' |
| `language` | `models.CharField` | help_text='冗余字段, 用于减少查询次数', max_length=16, verbose_name='开发语言' |
| `publisher` | `models.CharField` | default='', max_length=64, verbose_name='插件发布者' |
| `repo_type` | `models.CharField` | max_length=16, null=True, verbose_name='源码托管类型' |
| `repository` | `models.CharField` | max_length=255 |
| `status` | `models.CharField` | choices='`constants.PluginStatus.get...', default='`constants.PluginStatus.WAI...', max_length=16... |

**Relationships (1):**
- `pd`: models.ForeignKey → `PluginDefinition`

**Meta:**
- unique_together: `pd`, `id`

##### `PluginMarketInfo`
**Module:** `...r.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 插件市场信息

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `category` | `models.CharField` | db_index=True, max_length=64, verbose_name='分类' |
| `contact` | `models.TextField` | help_text='以分号(;)分割', verbose_name='联系人' |
| `extra_fields` | `models.JSONField` | verbose_name='额外字段' |

**Relationships (1):**
- `plugin`: models.OneToOneField → ``PluginInstance``

##### `PluginMarketInfoDefinition`
**Module:** `...paasng.paasng.bk_plugins.pluginscenter.models.definitions`
**Inherits from:** `paasng.utils.models.AuditedModel`

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `extra_fields_order` | `models.JSONField` | default='`list`' |
| `storage` | `models.CharField` | max_length=16, verbose_name='存储方式' |

**Relationships (1):**
- `pd`: models.OneToOneField → ``PluginDefinition``

##### `PluginRelease`
**Module:** `...r.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 插件发布版本

**Fields (14):**

| Field | Type | Parameters |
|-------|------|------------|
| `comment` | `models.TextField` | verbose_name='版本日志' |
| `extra_fields` | `models.JSONField` | verbose_name='额外字段' |
| `gray_status` | `models.CharField` | default='`constants.GrayReleaseStatu...', max_length=32, verbose_name='灰度发布状态' |
| `is_rolled_back` | `models.BooleanField` | default=False, help_text='是否已回滚' |
| `retryable` | `models.BooleanField` | default=True, help_text='失败后是否可重试' |
| `semver_type` | `models.CharField` | help_text='该字段只用于自动生成版本号的插件', max_length=16, null=True... |
| `source_hash` | `models.CharField` | max_length=128, verbose_name='代码提交哈希' |
| `source_location` | `models.CharField` | max_length=2048, verbose_name='代码仓库地址' |
| `source_version_name` | `models.CharField` | max_length=128, null=True, verbose_name='代码分支名/tag名' |
| `source_version_type` | `models.CharField` | max_length=128, null=True, verbose_name='代码版本类型(branch/tag)' |
| `status` | `models.CharField` | default='`constants.PluginReleaseSta...', max_length=16 |
| `tag` | `models.CharField` | db_index=True, max_length=16, null=True... |
| `type` | `models.CharField` | choices='`constants.PluginReleaseTyp...', max_length=16, verbose_name='版本类型(正式/测试)' |
| `version` | `models.CharField` | max_length=255, verbose_name='版本号' |

**Relationships (2):**
- `plugin`: models.ForeignKey → ``PluginInstance``
- `current_stage`: models.OneToOneField → `PluginReleaseStage`

##### `PluginReleaseStage`
**Module:** `...r.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 插件发布阶段

**Fields (9):**

| Field | Type | Parameters |
|-------|------|------------|
| `api_detail` | `models.JSONField` | help_text='该字段仅 invoke_method = api 时可用', null=True, verbose_name='API 详情' |
| `fail_message` | `models.TextField` | verbose_name='错误原因' |
| `invoke_method` | `models.CharField` | help_text='冗余字段, 用于减少查询次数', max_length=16, verbose_name='触发方式' |
| `operator` | `models.CharField` | max_length=32, null=True, verbose_name='操作人' |
| `pipeline_detail` | `models.JSONField` | help_text='该字段仅 invoke_method = pipeli...', null=True, verbose_name='流水线构建详情' |
| `stage_id` | `models.CharField` | max_length=32, verbose_name='阶段标识' |
| `stage_name` | `models.CharField` | help_text='冗余字段, 用于减少查询次数', max_length=16, verbose_name='阶段名称' |
| `status` | `models.CharField` | default='`constants.PluginReleaseSta...', max_length=16, verbose_name='发布状态' |
| `status_polling_method` | `models.CharField` | default='`constants.StatusPollingMet...', help_text='冗余字段, 用于减少查询次数', max_length=16... |

**Relationships (2):**
- `release`: models.ForeignKey → ``PluginRelease``
- `next_stage`: models.OneToOneField → `PluginReleaseStage`

**Meta:**
- unique_together: `release`, `stage_id`

##### `PluginReleaseStrategy`
**Module:** `...r.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 插件版本的发布策略

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `bkci_project` | `models.JSONField` | blank=True, help_text='格式：['1111', '222222']', null=True... |
| `organization` | `models.JSONField` | blank=True, null=True, verbose_name='组织架构' |
| `strategy` | `models.CharField` | choices='`constants.ReleaseStrategy....', max_length=32, verbose_name='发布策略' |

**Relationships (1):**
- `release`: models.ForeignKey → ``PluginRelease``

##### `PluginUserGroup`
**Module:** `...paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.models`
**Inherits from:** `paasng.utils.models.AuditedModel`

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `pd_id` | `models.CharField` | help_text='插件类型标识', max_length=64 |
| `plugin_id` | `models.CharField` | help_text='插件标识', max_length=32 |
| `role` | `models.IntegerField` | default='`PluginRole.DEVELOPER.value`' |
| `user_group_id` | `models.IntegerField` | help_text='权限中心用户组 ID' |

**Meta:**
- unique_together: `pd_id`, `plugin_id`, `role`

##### `PluginVisibleRange`
**Module:** `...r.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 插件可见范围

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `bkci_project` | `models.JSONField` | default='`list`', verbose_name='蓝盾项目ID' |
| `is_in_approval` | `models.BooleanField` | default=False, verbose_name='是否在审批中' |
| `organization` | `models.JSONField` | blank=True, null=True, verbose_name='组织架构' |

**Relationships (1):**
- `plugin`: models.OneToOneField → ``PluginInstance``

##### `PluginVisibleRangeDefinition`
**Module:** `...paasng.paasng.bk_plugins.pluginscenter.models.definitions`
**Inherits from:** `paasng.utils.models.AuditedModel`

**Relationships (1):**
- `pd`: models.OneToOneField → ``PluginDefinition``

##### `PreCreatedInstance`
**Module:** `apiserver.paasng.paasng.accessories.services.models`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`
**Description:** 预创建的服务实例

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `is_allocated` | `models.BooleanField` | default=False, help_text='实例是否已被分配' |

**Relationships (1):**
- `plan`: models.ForeignKey → `Plan`

##### `PresetEnvVariable`
**Module:** `...erver.paasng.paasng.platform.engine.models.preset_envvars`
**Inherits from:** `paas_wl.utils.models.AuditedModel`
**Description:** 应用描述文件中预定义的环境变量

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `environment_name` | `models.CharField` | choices='`ConfigVarEnvName.get_choic...', max_length=16, verbose_name='`_('环境名称')`' |
| `key` | `models.CharField` | max_length=128, null=False |

**Relationships (1):**
- `module`: models.ForeignKey → ``Module``

**Meta:**
- unique_together: `module`, `environment_name`, `key`

##### `PrivateTokenHolder`
**Module:** `apiserver.paasng.paasng.infras.accounts.models`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** Private Token for sourcectl

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `expire_at` | `models.DateTimeField` | blank=True, null=True |
| `provider` | `models.CharField` | max_length=32 |

**Relationships (1):**
- `user`: models.ForeignKey → ``UserProfile``

##### `ProcessLogQueryConfig`
**Module:** `apiserver.paasng.paasng.accessories.log.models`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`
**Description:** 进程日志查询配置

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `process_type` | `models.CharField` | blank=True, max_length=16, null=True |

**Relationships (4):**
- `env`: models.ForeignKey → ``ModuleEnvironment``
- `stdout`: models.ForeignKey → ``ElasticSearchConfig``
- `json`: models.ForeignKey → ``ElasticSearchConfig``
- `ingress`: models.ForeignKey → ``ElasticSearchConfig``

**Meta:**
- unique_together: `env`, `process_type`

##### `ProcessProbe`
**Module:** `apiserver.paasng.paas_wl.bk_app.processes.models`
**Inherits from:** `models.Model`

**Fields (7):**

| Field | Type | Parameters |
|-------|------|------------|
| `failure_threshold` | `models.PositiveIntegerField` | default=3 |
| `initial_delay_seconds` | `models.IntegerField` | default=0 |
| `period_seconds` | `models.PositiveIntegerField` | default=10 |
| `probe_type` | `models.CharField` | choices='`ProbeType.get_django_choic...', max_length=255 |
| `process_type` | `models.CharField` | max_length=255 |
| `success_threshold` | `models.PositiveIntegerField` | default=1 |
| `timeout_seconds` | `models.PositiveIntegerField` | default=1 |

**Relationships (1):**
- `app`: models.ForeignKey → `api.App`

**Meta:**
- unique_together: `app`, `process_type`, `probe_type`

##### `ProcessServicesFlag`
**Module:** `apiserver.paasng.paasng.platform.bkapp_model.models`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** ProcessServicesFlag 主要用途是标记是否隐式需要 process services 配置

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `implicit_needed` | `models.BooleanField` | default=False |

**Relationships (1):**
- `app_environment`: models.OneToOneField → ``ApplicationEnvironment``

##### `ProcessSpec`
**Module:** `apiserver.paasng.paas_wl.bk_app.processes.models`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`

**Fields (7):**

| Field | Type | Parameters |
|-------|------|------------|
| `autoscaling` | `models.BooleanField` | default=False |
| `name` | `models.CharField` | max_length=32 |
| `port` | `models.IntegerField` | help_text='容器端口', null=True |
| `proc_command` | `models.TextField` | help_text='进程启动命令(包含完整命令和参数的字符串), 只能与 ...', null=True |
| `target_replicas` | `models.IntegerField` | default=1 |
| `target_status` | `models.CharField` | default='start', max_length=32 |
| `type` | `models.CharField` | max_length=32 |

**Relationships (2):**
- `engine_app`: models.ForeignKey → `api.App`
- `plan`: models.ForeignKey → ``ProcessSpecPlan``

##### `ProcessSpecEnvOverlay`
**Module:** `apiserver.paasng.paasng.platform.bkapp_model.models`
**Inherits from:** `paas_wl.utils.models.TimestampedModel`
**Description:** 进程定义中允许按环境覆盖的配置

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `autoscaling` | `models.BooleanField` | null=True |
| `environment_name` | `models.CharField` | choices='`AppEnvName.get_choices()`', max_length=16, null=False... |
| `plan_name` | `models.CharField` | blank=True, help_text='仅存储方案名称', max_length=32... |
| `target_replicas` | `models.IntegerField` | null=True |

**Relationships (1):**
- `proc_spec`: models.ForeignKey → ``ModuleProcessSpec``

**Meta:**
- unique_together: `proc_spec`, `environment_name`

##### `ProcessSpecPlan`
**Module:** `apiserver.paasng.paas_wl.bk_app.processes.models`
**Inherits from:** `models.Model`

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `created` | `models.DateTimeField` | auto_now_add=True |
| `is_active` | `models.BooleanField` | default=True, verbose_name='是否可用' |
| `max_replicas` | `models.IntegerField` | - |
| `name` | `models.CharField` | db_index=True, max_length=32 |
| `updated` | `models.DateTimeField` | auto_now=True |

**Meta:**
- get_latest_by: `created`

##### `ProcessStructureLogCollectorConfig`
**Module:** `apiserver.paasng.paasng.accessories.log.models`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 进程结构化日志采集配置

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `collector_config_id` | `models.BigAutoField` | primary_key=True |
| `process_type` | `models.CharField` | help_text='进程类型(名称)', max_length=16 |

**Relationships (2):**
- `application`: models.ForeignKey → ``Application``
- `env`: models.ForeignKey → ``ModuleEnvironment``

##### `Product`
**Module:** `apiserver.paasng.paasng.accessories.publish.market.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** 蓝鲸应用: 开发者中心的编辑属性

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `code` | `models.CharField` | help_text='应用编码', max_length=64, unique=True |
| `state` | `models.SmallIntegerField` | choices='`constant.AppState.get_choi...', default=1, help_text='应用状态' |
| `type` | `models.SmallIntegerField` | choices='`constant.AppType.get_choic...', help_text='按实现方式分类' |

**Relationships (2):**
- `application`: models.OneToOneField → ``Application``
- `tag`: models.ForeignKey → ``Tag``

##### `RCStateAppBinding`
**Module:** `apiserver.paasng.paas_wl.workloads.networking.egress.models`
**Inherits from:** `paas_wl.bk_app.applications.models.AuditedModel`
**Description:** If an app was bind with one RegionClusterState instance, it means that the app will not be

**Relationships (2):**
- `app`: models.OneToOneField → ``WlApp``
- `state`: models.ForeignKey → ``RegionClusterState``

##### `RegionClusterState`
**Module:** `apiserver.paasng.paas_wl.workloads.networking.egress.models`
**Inherits from:** `paas_wl.bk_app.applications.models.AuditedModel`
**Description:** A RegionClusterState is a state which describes what the cluster is in a specified moment. it

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `cluster_name` | `models.CharField` | max_length=32, null=True |
| `name` | `models.CharField` | max_length=64 |
| `nodes_cnt` | `models.IntegerField` | default=0 |
| `nodes_digest` | `models.CharField` | db_index=True, max_length=64 |
| `region` | `models.CharField` | max_length=32 |

**Meta:**
- get_latest_by: `created`
- ordering: `-created`
- unique_together: `region`, `cluster_name`, `name`

##### `Release`
**Module:** `apiserver.paasng.paas_wl.bk_app.applications.models.release`
**Inherits from:** `paas_wl.bk_app.applications.models.UuidAuditedModel`

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `failed` | `models.BooleanField` | default=False |
| `owner` | `models.CharField` | max_length=64 |
| `summary` | `models.TextField` | blank=True, null=True |
| `version` | `models.PositiveIntegerField` | - |

**Relationships (3):**
- `app`: models.ForeignKey → `App`
- `config`: models.ForeignKey → `Config`
- `build`: models.ForeignKey → `Build`

**Meta:**
- get_latest_by: `created`
- ordering: `-created`
- unique_together: `['app', 'version']`

##### `RemoteServiceEngineAppAttachment`
**Module:** `apiserver.paasng.paasng.accessories.servicehub.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** Binding relationship of engine app <-> remote service plan

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `credentials_enabled` | `models.BooleanField` | default=True, verbose_name='是否使用凭证' |
| `plan_id` | `models.UUIDField` | verbose_name='远程增强服务 Plan ID' |
| `service_id` | `models.UUIDField` | verbose_name='远程增强服务 ID' |
| `service_instance_id` | `models.UUIDField` | null=True |

**Relationships (1):**
- `engine_app`: models.ForeignKey → `engine.EngineApp`

**Meta:**
- unique_together: `service_id`, `engine_app`

##### `RemoteServiceModuleAttachment`
**Module:** `apiserver.paasng.paasng.accessories.servicehub.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** Binding relationship of module <-> remote service

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `service_id` | `models.UUIDField` | verbose_name='远程增强服务 ID' |

**Relationships (1):**
- `module`: models.ForeignKey → `modules.Module`

**Meta:**
- unique_together: `service_id`, `module`

##### `RepoBasicAuthHolder`
**Module:** `apiserver.paasng.paasng.platform.sourcectl.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** Repo 鉴权

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `repo_id` | `models.IntegerField` | verbose_name='关联仓库' |
| `repo_type` | `models.CharField` | max_length=32, verbose_name='仓库类型' |
| `username` | `models.CharField` | max_length=64, verbose_name='仓库用户名' |

**Relationships (1):**
- `module`: models.ForeignKey → `modules.Module`

##### `RepoQuotaStatistics`
**Module:** `svc-bkrepo.svc_bk_repo.monitoring.models`
**Inherits from:** `models.Model`

**Fields (4):**

| Field | Type | Parameters |
|-------|------|------------|
| `max_size` | `models.BigIntegerField` | help_text='单位字节，值为 nul 时表示未设置仓库配额', null=True, verbose_name='仓库最大配额' |
| `repo_name` | `models.CharField` | max_length=64, verbose_name='仓库名称' |
| `updated` | `models.DateTimeField` | auto_now=True |
| `used` | `models.BigIntegerField` | default=0, help_text='单位字节', verbose_name='仓库已使用容量' |

**Relationships (1):**
- `instance`: models.ForeignKey → `paas_service.ServiceInstance`

##### `ResourceId`
**Module:** `apiserver.paasng.paasng.accessories.services.models`
**Inherits from:** `models.Model`

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `namespace` | `models.CharField` | max_length=32 |
| `uid` | `models.CharField` | db_index=True, max_length=64, null=False... |

**Meta:**
- unique_together: `namespace`, `uid`

##### `Service`
**Module:** `apiserver.paasng.paasng.accessories.services.models`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`

**Fields (6):**

| Field | Type | Parameters |
|-------|------|------------|
| `available_languages` | `models.CharField` | blank=True, max_length=1024, null=True... |
| `is_active` | `models.BooleanField` | default=True, verbose_name='是否可用' |
| `is_visible` | `models.BooleanField` | default=True, verbose_name='是否可见' |
| `logo_b64` | `models.TextField` | blank=True, null=True, verbose_name='服务 logo 的地址, 支持base64格式' |
| `name` | `models.CharField` | max_length=64, verbose_name='服务名称' |
| `region` | `models.CharField` | max_length=32 |

**Relationships (1):**
- `category`: models.ForeignKey → ``ServiceCategory``

**Meta:**
- unique_together: `region`, `name`

##### `ServiceCategory`
**Module:** `apiserver.paasng.paasng.accessories.services.models`
**Inherits from:** `models.Model`

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `sort_priority` | `models.IntegerField` | default=0 |

##### `ServiceEngineAppAttachment`
**Module:** `apiserver.paasng.paasng.accessories.servicehub.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `credentials_enabled` | `models.BooleanField` | default=True, verbose_name='是否使用凭证' |

**Relationships (4):**
- `engine_app`: models.ForeignKey → `engine.EngineApp`
- `service`: models.ForeignKey → ``Service``
- `plan`: models.ForeignKey → ``Plan``
- `service_instance`: models.ForeignKey → ``ServiceInstance``

**Meta:**
- unique_together: `service`, `engine_app`

##### `ServiceInstance`
**Module:** `apiserver.paasng.paasng.accessories.services.models`
**Inherits from:** `paasng.utils.models.UuidAuditedModel`

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `to_be_deleted` | `models.BooleanField` | default=False |

**Relationships (2):**
- `service`: models.ForeignKey → `Service`
- `plan`: models.ForeignKey → `Plan`

##### `ServiceModuleAttachment`
**Module:** `apiserver.paasng.paasng.accessories.servicehub.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** Module <-> Local Service relationship

**Relationships (2):**
- `module`: models.ForeignKey → `modules.Module`
- `service`: models.ForeignKey → ``Service``

**Meta:**
- unique_together: `service`, `module`

##### `SharedServiceAttachment`
**Module:** `apiserver.paasng.paasng.accessories.servicehub.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** Share a service binding relationship from other modules

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `ref_attachment_pk` | `models.IntegerField` | verbose_name='被共享的服务绑定关系主键' |
| `service_id` | `models.UUIDField` | verbose_name='增强服务 ID' |
| `service_type` | `models.CharField` | max_length=16, verbose_name='增强服务类型' |

**Relationships (1):**
- `module`: models.ForeignKey → `modules.Module`

**Meta:**
- unique_together: `module`, `service_type`, `service_id`

##### `SourcePackage`
**Module:** `apiserver.paasng.paasng.platform.sourcectl.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`
**Description:** 源码包存储信息

**Fields (9):**

| Field | Type | Parameters |
|-------|------|------------|
| `is_deleted` | `models.BooleanField` | default=False, help_text='如果 SourcePackage 指向的源码包已被清理...', verbose_name='源码包是否已被清理' |
| `package_name` | `models.CharField` | max_length=128, verbose_name='源码包原始文件名' |
| `package_size` | `models.BigIntegerField` | verbose_name='源码包大小, bytes' |
| `relative_path` | `models.CharField` | help_text='如果压缩时将目录也打包进来, 入目录名是 foo, 那...', max_length=255, verbose_name='源码入口的相对路径' |
| `sha256_signature` | `models.CharField` | max_length=64, null=True, verbose_name='sha256数字签名' |
| `storage_engine` | `models.CharField` | help_text='源码包真实存放的存储服务类型', max_length=64, verbose_name='存储引擎' |
| `storage_path` | `models.CharField` | help_text='[deprecated] 源码包在存储服务中存放的位置', max_length=1024, verbose_name='存储路径' |
| `storage_url` | `models.CharField` | help_text='可获取到源码包的 URL 地址', max_length=1024, verbose_name='存储地址' |
| `version` | `models.CharField` | max_length=128, verbose_name='版本号' |

**Relationships (1):**
- `module`: models.ForeignKey → `modules.Module`

**Meta:**
- unique_together: `module`, `version`

##### `SourceTypeSpecConfig`
**Module:** `apiserver.paasng.paasng.platform.sourcectl.models`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** SourceTypeSpec 数据存储

**Fields (8):**

| Field | Type | Parameters |
|-------|------|------------|
| `authorization_base_url` | `models.CharField` | blank=True, default='', max_length=256... |
| `client_id` | `models.CharField` | blank=True, default='', max_length=256... |
| `enabled` | `models.BooleanField` | default=False, verbose_name='是否启用' |
| `name` | `models.CharField` | max_length=32, unique=True, verbose_name='`_('服务名称')`' |
| `redirect_uri` | `models.CharField` | blank=True, default='', max_length=256... |
| `server_config` | `models.JSONField` | blank=True, default='`dict`', verbose_name='服务配置' |
| `spec_cls` | `models.CharField` | max_length=128, verbose_name='配置类路径' |
| `token_base_url` | `models.CharField` | blank=True, default='', max_length=256... |

##### `StepMetaSet`
**Module:** `apiserver.paasng.paasng.platform.engine.models.steps`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 部署步骤元信息集

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `is_default` | `models.BooleanField` | default=False |
| `name` | `models.CharField` | max_length=32 |

**Relationships (1):**
- `metas`: models.ManyToManyField → ``DeployStepMeta``

**Meta:**
- ordering: `id`

##### `SvcDiscConfig`
**Module:** `apiserver.paasng.paasng.platform.bkapp_model.models`
**Inherits from:** `paas_wl.utils.models.AuditedModel`
**Description:** 服务发现配置

**Relationships (1):**
- `application`: models.ForeignKey → ``Application``

##### `SvnAccount`
**Module:** `apiserver.paasng.paasng.platform.sourcectl.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** svn account for developer

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `account` | `models.CharField` | help_text='目前仅支持固定格式', max_length=64, unique=True |
| `synced_from_paas20` | `models.BooleanField` | default=False, help_text='账户信息是否从 PaaS 2.0 同步过来' |

##### `SvnRepository`
**Module:** `apiserver.paasng.paasng.platform.sourcectl.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`, `apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin`
**Description:** 基于 Svn 的软件存储库

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `repo_url` | `models.CharField` | max_length=2048, verbose_name='项目地址' |
| `server_name` | `models.CharField` | max_length=32, verbose_name='SVN 服务名称' |
| `source_dir` | `models.CharField` | max_length=2048, null=True, verbose_name='源码目录' |

##### `Tag`
**Module:** `apiserver.paasng.paasng.accessories.publish.market.models`
**Inherits from:** `models.Model`

**Fields (5):**

| Field | Type | Parameters |
|-------|------|------------|
| `enabled` | `models.BooleanField` | default=True, help_text='创建应用时是否可选择该分类' |
| `index` | `models.IntegerField` | default=0, help_text='显示排序字段' |
| `name` | `models.CharField` | help_text='分类名称', max_length=64 |
| `region` | `models.CharField` | help_text='部署区域', max_length=32 |
| `remark` | `models.CharField` | blank=True, help_text='备注', max_length=255... |

**Relationships (1):**
- `parent`: models.ForeignKey → `self`

**Meta:**
- ordering: `index`, `id`

##### `Tag`
**Module:** `svc-rabbitmq.vendor.models`
**Inherits from:** `paas_service.models.AuditedModel`

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `key` | `models.CharField` | max_length=64 |
| `value` | `models.CharField` | max_length=128 |

**Meta:**
- abstract: `True`

##### `TagMap`
**Module:** `...rver.paasng.paasng.accessories.publish.sync_market.models`
**Inherits from:** `django_models.Model`

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `remote_id` | `django_models.IntegerField` | db_index=True |

**Relationships (1):**
- `tag`: django_models.OneToOneField → ``market_models.Tag``

##### `Template`
**Module:** `apiserver.paasng.paasng.platform.templates.models`
**Inherits from:** `paasng.utils.models.AuditedModel`
**Description:** 开发模板配置

**Fields (12):**

| Field | Type | Parameters |
|-------|------|------------|
| `blob_url` | `models.JSONField` | verbose_name='`_('不同版本二进制包存储路径')`' |
| `enabled_regions` | `models.JSONField` | blank=True, default='`list`', verbose_name='`_('允许被使用的版本')`' |
| `language` | `models.CharField` | max_length=32, verbose_name='`_('开发语言')`' |
| `market_ready` | `models.BooleanField` | default=False, verbose_name='`_('能否发布到应用集市')`' |
| `name` | `models.CharField` | max_length=64, unique=True, verbose_name='`_('模板名称')`' |
| `preset_services_config` | `models.JSONField` | blank=True, default='`dict`', verbose_name='`_('预设增强服务配置')`' |
| `processes` | `models.JSONField` | blank=True, default='`dict`', verbose_name='`_('进程配置')`' |
| `repo_url` | `models.CharField` | blank=True, default='', max_length=256... |
| `required_buildpacks` | `models.JSONField` | blank=True, default='`list`', verbose_name='`_('必须的构建工具')`' |
| `runtime_type` | `models.CharField` | default='`RuntimeType.BUILDPACK`', max_length=32, verbose_name='`_('运行时类型')`' |
| `tags` | `models.JSONField` | blank=True, default='`list`', verbose_name='`_('标签')`' |
| `type` | `models.CharField` | choices='`TemplateType.get_django_ch...', max_length=16, verbose_name='`_('模板类型')`' |

**Meta:**
- ordering: `created`

##### `TimestampedModel`
**Module:** `apiserver.paasng.paas_wl.utils.models`
**Inherits from:** `models.Model`
**Description:** Model with 'created' and 'updated' fields.

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `created` | `models.DateTimeField` | auto_now_add=True |
| `region` | `models.CharField` | help_text='部署区域', max_length=32 |
| `updated` | `models.DateTimeField` | auto_now=True |

**Meta:**
- abstract: `True`

##### `TimestampedModel`
**Module:** `apiserver.paasng.paasng.utils.models`
**Inherits from:** `models.Model`
**Description:** Model with 'created' and 'updated' fields.

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `created` | `models.DateTimeField` | auto_now_add=True |
| `region` | `models.CharField` | help_text='部署区域', max_length=32 |
| `updated` | `models.DateTimeField` | auto_now=True |

**Meta:**
- abstract: `True`

##### `UserMarkedApplication`
**Module:** `apiserver.paasng.paasng.platform.applications.models`
**Inherits from:** `paasng.utils.models.OwnerTimestampedModel`

**Relationships (1):**
- `application`: models.ForeignKey → ``Application``

**Meta:**
- unique_together: `application`, `owner`

##### `UserPolicy`
**Module:** `svc-rabbitmq.vendor.models`
**Inherits from:** `svc-rabbitmq.vendor.models.LinkableModel`
**Description:** 集群下创建 vhost 默认策略，和具体 vhost 无关

**Fields (7):**

| Field | Type | Parameters |
|-------|------|------------|
| `apply_to` | `models.CharField` | blank=True, choices='`[(i.value, i.name) for i i...', max_length=64... |
| `cluster_id` | `models.IntegerField` | blank=True |
| `enable` | `models.BooleanField` | default=True |
| `link_type` | `models.IntegerField` | choices='`[(i.value, i.name) for i i...', default='`LinkType.empty.value`' |
| `name` | `models.CharField` | max_length=64, null=True |
| `pattern` | `models.CharField` | blank=True, max_length=128, null=True |
| `priority` | `models.IntegerField` | blank=True, null=True |

**Relationships (1):**
- `linked`: models.ForeignKey → `self`

##### `UserPolicyTag`
**Module:** `svc-rabbitmq.vendor.models`
**Inherits from:** `svc-rabbitmq.vendor.models.Tag`
**Description:** 表示绑定关系

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `key` | `models.CharField` | max_length=64 |
| `value` | `models.CharField` | max_length=128 |

**Relationships (1):**
- `instance`: models.ForeignKey → ``UserPolicy``

##### `UserPrivateToken`
**Module:** `apiserver.paasng.paasng.infras.accounts.models`
**Inherits from:** `models.Model`
**Description:** Private token can be used to authenticate an user, these tokens usually have very long

**Fields (3):**

| Field | Type | Parameters |
|-------|------|------------|
| `expires_at` | `models.DateTimeField` | blank=True, null=True |
| `is_active` | `models.BooleanField` | default=True |
| `token` | `models.CharField` | max_length=64, unique=True |

**Relationships (1):**
- `user`: models.ForeignKey → ``User``

##### `UserProfile`
**Module:** `apiserver.paasng.paasng.infras.accounts.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** Profile field for user

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `feature_flags` | `models.TextField` | blank=True, null=True |
| `role` | `models.IntegerField` | default='`SiteRole.USER.value`' |

##### `UuidAuditedModel`
**Module:** `apiserver.paasng.paas_wl.utils.models`
**Inherits from:** `apiserver.paasng.paas_wl.utils.models.AuditedModel`
**Description:** Add a UUID primary key to an class`AuditedModel`.

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `uuid` | `models.UUIDField` | auto_created=True, default='`uuid.uuid4`', editable=False... |

**Meta:**
- abstract: `True`

##### `UuidAuditedModel`
**Module:** `apiserver.paasng.paasng.utils.models`
**Inherits from:** `apiserver.paasng.paasng.utils.models.AuditedModel`
**Description:** Add a UUID primary key to an :class:`AuditedModel`.

**Fields (1):**

| Field | Type | Parameters |
|-------|------|------------|
| `uuid` | `models.UUIDField` | auto_created=True, default='`uuid.uuid4`', editable=False... |

**Meta:**
- abstract: `True`

##### `WlAppBackupRel`
**Module:** `apiserver.paasng.paasng.platform.mgrlegacy.models`
**Inherits from:** `paasng.utils.models.TimestampedModel`
**Description:** WlApp 的备份关系表

**Fields (2):**

| Field | Type | Parameters |
|-------|------|------------|
| `backup_id` | `models.UUIDField` | verbose_name='对应备份的 WlApp uuid' |
| `original_id` | `models.UUIDField` | verbose_name='原 WlApp uuid' |

**Relationships (1):**
- `app_environment`: models.OneToOneField → ``ApplicationEnvironment``

### Django URL Patterns

- **Total URL Patterns**: 533
- **URL Configuration Files**: 59

- **Path Patterns**: 99

- **Include Patterns**: 58

#### Complete URL to View Mapping

Showing all 99 URL patterns with their corresponding view implementations:

| URL Pattern | View Implementation | Name |
|-------------|---------------------|------|
| `` | `PluginCallBackApiViewSet` | - |
| `` | `PluginReleaseViewSet` | - |
| `api/bkapps/applications/<str:code>/image_credentials/` | `AppUserCredentialViewSet` | api.applications.image_cred... |
| `api/bkapps/applications/<str:code>/image_credentials/<str...` | `AppUserCredentialViewSet` | api.applications.image_cred... |
| `api/bkplugins/<str:pd_id>/plugins/` | `PluginInstanceViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/` | `PluginInstanceViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/archive/` | `PluginInstanceViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/basic_i...` | `PluginInstanceViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/code_st...` | `PluginInstanceViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/configu...` | `PluginConfigViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/configu...` | `PluginConfigViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/extra_f...` | `PluginInstanceViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/feature...` | `PluginInstanceViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logo/` | `PluginInstanceViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/ag...` | `PluginLogViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/ag...` | `PluginLogViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/in...` | `PluginLogViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/st...` | `PluginLogViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/st...` | `PluginLogViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/market/` | `PluginMarketViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members/` | `PluginMembersViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members...` | `PluginMembersViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members...` | `PluginMembersViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members...` | `PluginMembersViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members...` | `PluginMembersViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/operati...` | `OperationRecordViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/overview/` | `PluginInstanceViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/publisher/` | `PluginInstanceViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/reactiv...` | `PluginInstanceViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/` | `PluginReleaseViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/release...` | `PluginReleaseViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/release...` | `PluginReleaseViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/release...` | `PluginReleaseViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/release...` | `PluginReleaseViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/release...` | `PluginReleaseViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/release...` | `PluginReleaseViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/release...` | `PluginReleaseStageViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/release...` | `PluginReleaseStageViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/release...` | `PluginReleaseStageViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/release...` | `PluginReleaseStrategyViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/release...` | `PluginReleaseViewSet` | - |
| `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/visible...` | `PluginVisibleRangeViewSet` | - |
| `api/bkplugins/filter_params/` | `PluginInstanceViewSet` | - |
| `api/bkplugins/lists/` | `PluginInstanceViewSet` | - |
| `api/bkplugins/plugin_definitions/<str:pd_id>/basic_info_s...` | `SchemaViewSet` | - |
| `api/bkplugins/plugin_definitions/<str:pd_id>/configuratio...` | `SchemaViewSet` | - |
| `api/bkplugins/plugin_definitions/<str:pd_id>/market_schema/` | `SchemaViewSet` | - |
| `api/bkplugins/plugin_definitions/schemas/` | `SchemaViewSet` | - |
| `api/bkplugins/shim/iam/selection/plugin_view/` | `PluginSelectionView` | - |
| `api/changelogs/` | `ChangelogViewSet` | - |
| `api/cloudapi/apps/<slug:app_code>/apis/` | `CloudAPIViewSet` | api.cloudapi.v1.apis |
| `api/cloudapi/apps/<slug:app_code>/apis/<int:api_id>/permi...` | `CloudAPIViewSet` | api.cloudapi.v1.allow_apply... |
| `api/cloudapi/apps/<slug:app_code>/apis/<int:api_id>/permi...` | `CloudAPIViewSet` | api.cloudapi.v1.apply_resou... |
| `api/cloudapi/apps/<slug:app_code>/apis/<int:api_id>/permi...` | `CloudAPIViewSet` | api.cloudapi.v1.resource_pe... |
| `api/cloudapi/apps/<slug:app_code>/apis/permissions/app-pe...` | `CloudAPIViewSet` | api.cloudapi.v1.list_app_re... |
| `api/cloudapi/apps/<slug:app_code>/apis/permissions/apply-...` | `CloudAPIViewSet` | api.cloudapi.v1.list_resour... |
| `api/cloudapi/apps/<slug:app_code>/apis/permissions/apply-...` | `CloudAPIViewSet` | api.cloudapi.v1.retrieve_re... |
| `api/cloudapi/apps/<slug:app_code>/apis/permissions/apply/` | `CloudAPIViewSet` | api.cloudapi.v1.batch_apply... |
| `api/cloudapi/apps/<slug:app_code>/apis/permissions/renew/` | `CloudAPIViewSet` | api.cloudapi.v1.renew_resou... |
| `api/cloudapi/apps/<slug:app_code>/esb/systems/` | `CloudAPIViewSet` | api.cloudapi.v1.systems |
| `api/cloudapi/apps/<slug:app_code>/esb/systems/<int:system...` | `CloudAPIViewSet` | api.cloudapi.v1.apply_compo... |
| `api/cloudapi/apps/<slug:app_code>/esb/systems/<int:system...` | `CloudAPIViewSet` | api.cloudapi.v1.component_p... |
| `api/cloudapi/apps/<slug:app_code>/esb/systems/permissions...` | `CloudAPIViewSet` | api.cloudapi.v1.list_app_co... |
| `api/cloudapi/apps/<slug:app_code>/esb/systems/permissions...` | `CloudAPIViewSet` | api.cloudapi.v1.list_compon... |
| `api/cloudapi/apps/<slug:app_code>/esb/systems/permissions...` | `CloudAPIViewSet` | api.cloudapi.v1.retrieve_co... |
| `api/cloudapi/apps/<slug:app_code>/esb/systems/permissions...` | `CloudAPIViewSet` | api.cloudapi.v1.renew_compo... |
| `api/monitor/applications/<slug:code>/alarm_strategies/` | `ListAlarmStrategiesView` | - |
| `api/monitor/applications/<slug:code>/alert_rules/init/` | `AlertRulesView` | - |
| `api/monitor/applications/<slug:code>/alerts/` | `ListAlertsView` | - |
| `api/monitor/applications/<slug:code>/builtin_dashboards/` | `GetDashboardInfoView` | api.modules.monitor.builtin... |
| `api/monitor/applications/<slug:code>/dashboard_info/` | `GetDashboardInfoView` | - |
| `api/monitor/applications/<slug:code>/modules/<slug:module...` | `AlertRulesView` | - |
| `api/monitor/supported_alert_rules/` | `AlertRulesView` | - |
| `api/monitor/user/alerts/` | `ListAlertsView` | - |
| `api/platform/frontend_features/` | `FrontendFeatureViewSet` | - |
| `api/usermanage/departments/<str:dept_id>/` | `BkPluginUserManageView` | - |
| `open/api/itsm/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/` | `PluginCallBackApiViewSet` | - |
| `open/api/itsm/bkplugins/<str:pd_id>/plugins/<str:plugin_i...` | `PluginCallBackApiViewSet` | - |
| `open/api/itsm/bkplugins/<str:pd_id>/plugins/<str:plugin_i...` | `PluginCallBackApiViewSet` | - |
| `wl_api/applications/<str:code>/domains/` | `paas_wl.apis.admin.views.domain.AppDomainsViewSet` | wl_api.application.domains |
| `wl_api/applications/<str:code>/domains/<int:id>/` | `paas_wl.apis.admin.views.domain.AppDomainsViewSet` | wl_api.application.domain_b... |
| `wl_api/applications/<str:code>/log_config/` | `paas_wl.apis.admin.views.logs.AppLogConfigViewSet` | wl_api.application.log_config |
| `wl_api/platform/app_certs/shared/` | `...s.admin.views.certs.AppDomainSharedCertsViewSet` | wl_api.shared_app_certs |
| `wl_api/platform/app_certs/shared/<str:name>` | `...s.admin.views.certs.AppDomainSharedCertsViewSet` | wl_api.shared_app_cert_by_name |
| `wl_api/platform/clusters/` | `paas_wl.apis.admin.views.clusters.ClusterViewSet` | wl_api.clusters |
| `wl_api/platform/clusters/<str:cluster_name>/components/` | `...is.admin.views.clusters.ClusterComponentViewSet` | wl_api.cluster.components |
| `wl_api/platform/clusters/<str:cluster_name>/components/<s...` | `...is.admin.views.clusters.ClusterComponentViewSet` | wl_api.cluster.component_by... |
| `wl_api/platform/clusters/<str:cluster_name>/node_state/` | `paas_wl.apis.admin.views.clusters.ClusterViewSet` | wl_api.cluster.node_state |
| `wl_api/platform/clusters/<str:cluster_name>/operator_info/` | `...is.admin.views.clusters.ClusterComponentViewSet` | wl_api.cluster.operator_info |
| `wl_api/platform/clusters/<str:pk>/` | `paas_wl.apis.admin.views.clusters.ClusterViewSet` | wl_api.cluster_by_id |
| `wl_api/platform/clusters/<str:pk>/api_servers` | `paas_wl.apis.admin.views.clusters.ClusterViewSet` | wl_api.cluster.api_servers |
| `wl_api/platform/clusters/<str:pk>/api_servers/<str:api_se...` | `paas_wl.apis.admin.views.clusters.ClusterViewSet` | wl_api.cluster.api_server_b... |
| `wl_api/platform/clusters/<str:pk>/set_default/` | `paas_wl.apis.admin.views.clusters.ClusterViewSet` | wl_api.cluster.set_default |
| `wl_api/platform/process_spec_plan/` | `...in.views.processes.ProcessSpecPlanManageViewSet` | wl_api.process_spec_plan |
| `wl_api/platform/process_spec_plan/id/<int:id>/` | `...in.views.processes.ProcessSpecPlanManageViewSet` | wl_api.process_spec_plan_by_id |
| `wl_api/platform/process_spec_plan/manage/` | `...in.views.processes.ProcessSpecPlanManageViewSet` | - |
| `wl_api/regions/<str:region>/apps/<str:name>/processes/<st...` | `...is.admin.views.processes.ProcessInstanceViewSet` | wl_api.application.process_... |
| `wl_api/regions/<str:region>/apps/<str:name>/processes/<st...` | `....admin.views.processes.ProcessSpecManageViewSet` | wl_api.application.process_... |
| `wl_api/regions/<str:region>/apps/<str:name>/processes/<st...` | `....admin.views.processes.ProcessSpecManageViewSet` | wl_api.application.process_... |

**Files with Most URL Patterns:**

| File | Pattern Count |
|------|---------------|
| `apiserver.paasng.paasng.plat_admin.admin42.urls` | 78 |
| `apiserver.paasng.paasng.urls` | 50 |
| `apiserver.paasng.paasng.bk_plugins.pluginscenter.urls` | 47 |
| `apiserver.paasng.paasng.platform.engine.urls` | 26 |
| `apiserver.paasng.paas_wl.apis.admin.urls` | 20 |
| `apiserver.paasng.paasng.accessories.servicehub.urls` | 20 |
| `apiserver.paasng.paasng.accessories.paas_analysis.urls` | 19 |
| `apiserver.paasng.paasng.bk_plugins.bk_plugins.urls` | 18 |
| `apiserver.paasng.paasng.platform.applications.urls` | 18 |
| `apiserver.paasng.paasng.accessories.log.urls` | 17 |

### Concurrency Patterns

- **Total Patterns**: 4
- **Files Scanned**: 4

**By Category:**

| Category | Count | Use Case |
|----------|-------|----------|
| Multiprocessing | 1 | CPU-bound operations, parallel processing |
| Threading | 3 | I/O-bound operations, concurrent tasks |

**Performance Tips:**
- Use asyncio for I/O-bound operations (network, file I/O)
- Use multiprocessing for CPU-bound operations
- Threading is suitable for I/O-bound with GIL limitations

### Signal Usage

- **Total Signals**: 39
- **Files Scanned**: 2368
- **Django Receivers**: 54
- **Celery Receivers**: 1
- **Custom Signals Defined**: 20

**Most Used Signals:**

| Signal | Receiver Count |
|--------|----------------|
| `post_save` | 8 |
| `post_create_application` | 8 |
| `post_appenv_deploy` | 6 |
| `application_default_module_switch` | 3 |
| `before_finishing_application_creation` | 3 |
| `module_environment_offline_success` | 3 |
| `application_logo_updated` | 3 |
| `application_member_updated` | 2 |
| `prepare_change_application_name` | 2 |
| `pre_appenv_deploy` | 2 |

## Infrastructure

### Environment Variables

- **Total Variables**: 9
- **Required Variables**: 6
- **Optional Variables**: 3

#### Complete Environment Variable Definitions

Showing all environment variables with their definitions, default values, and reference counts:

| Variable | Required | Default Value | Reference Count | Access Pattern |
|----------|----------|---------------|-----------------|----------------|
| `DATABASE_URL` | ✓ Yes | - | 3 | getenv() |
| `(dynamic)` | No | `<dynamic>` | 1 | getenv() |
| `BKPAAS_BUILD_VERSION` | No | `unset` | 1 | getenv() |
| `CELERY_TASK_DEFAULT_QUEUE` | No | `celery` | 1 | environ.get() |
| `OAUTHLIB_INSECURE_TRANSPORT` | ✓ Yes | - | 1 | environ[] |
| `OAUTHLIB_RELAX_TOKEN_SCOPE` | ✓ Yes | - | 1 | environ[] |
| `PAAS_WL_CLUSTER_API_SERVER_URLS` | ✓ Yes | - | 1 | environ.get() |
| `PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT` | ✓ Yes | - | 1 | environ[] |
| `prometheus_multiproc_dir` | ✓ Yes | - | 1 | environ.get() |

#### Detailed Usage Locations

Showing where each environment variable is referenced in the codebase:

##### `DATABASE_URL` (3 references)
**Status:** ✓ Required

**References:**
- `svc-bkrepo/svc_bk_repo/settings/__init__.py:140`
  ```python
  os.getenv('DATABASE_URL')
  ```
- `svc-mysql/svc_mysql/settings/__init__.py:139`
  ```python
  os.getenv('DATABASE_URL')
  ```
- `svc-otel/svc_otel/settings/__init__.py:139`
  ```python
  os.getenv('DATABASE_URL')
  ```

##### `(dynamic)` (1 references)
**Status:** Optional (default: `<dynamic>`)

**References:**
- `apiserver/paasng/paasng/utils/configs.py:101`
  ```python
  os.getenv(env_key, default)
  ```

##### `BKPAAS_BUILD_VERSION` (1 references)
**Status:** Optional (default: `unset`)

**References:**
- `...er/paasng/paasng/plat_admin/admin42/context_processors.py:24`
  ```python
  os.getenv('BKPAAS_BUILD_VERSION', 'unset')
  ```

##### `CELERY_TASK_DEFAULT_QUEUE` (1 references)
**Status:** Optional (default: `celery`)

**References:**
- `apiserver/paasng/paasng/settings/__init__.py:656`
  ```python
  os.environ.get('CELERY_TASK_DEFAULT_QUEUE', 'celery')
  ```

##### `OAUTHLIB_INSECURE_TRANSPORT` (1 references)
**Status:** ✓ Required

**References:**
- `apiserver/paasng/paasng/infras/accounts/oauth/backends.py:35`
  ```python
  os.environ['OAUTHLIB_INSECURE_TRANSPORT']
  ```

##### `OAUTHLIB_RELAX_TOKEN_SCOPE` (1 references)
**Status:** ✓ Required

**References:**
- `apiserver/paasng/paasng/infras/accounts/oauth/backends.py:38`
  ```python
  os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE']
  ```

##### `PAAS_WL_CLUSTER_API_SERVER_URLS` (1 references)
**Status:** ✓ Required

**References:**
- `...as/cluster/management/commands/initial_default_cluster.py:114`
  ```python
  os.environ.get('PAAS_WL_CLUSTER_API_SERVER_URLS')
  ```

##### `PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT` (1 references)
**Status:** ✓ Required

**References:**
- `...rver/paasng/tests/paas_wl/infras/cluster/test_commands.py:56`
  ```python
  os.environ['PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT']
  ```

##### `prometheus_multiproc_dir` (1 references)
**Status:** ✓ Required

**References:**
- `apiserver/paasng/paasng/__init__.py:33`
  ```python
  os.environ.get('prometheus_multiproc_dir')
  ```

### Redis Usage

- **Total Usages**: 5
- **Files Scanned**: 3

**By Category:**

| Category | Count | Purpose |
|----------|-------|---------|
| Direct Client | 3 | Direct Redis operations |
| Celery Broker | 1 | Task queue message broker |
| Celery Result | 1 | Task result storage |

**Redis Operations:**

- `apiserver/paasng/paasng/misc/metrics/workloads/deployment.py:40`
  - Operation: `get`
  - Key pattern: `metrics:unavailable_deployments_total`

- `apiserver/paasng/paasng/misc/metrics/workloads/deployment.py:67`
  - Operation: `set`
  - Key pattern: `metrics:unavailable_deployments_total`
  - ✓ Has TTL

- `svc-rabbitmq/tasks/management/commands/worker.py:59`
  - Operation: `get_or_set`
  - Key pattern: `...`

### Prometheus Metrics

- **Total Metrics**: 42
- **Files Scanned**: 5

**Metrics by Type:**

| Type | Count | Use Case |
|------|-------|----------|
| Gauge | 33 | Values that can go up and down (memory, connections) |
| Counter | 7 | Monotonically increasing values (requests, errors) |
| Histogram | 2 | Observations and distributions (latency, sizes) |

**Sample Metrics:**

- **`api_visited_counter`** (Counter)
  - 

- **`api_visited_time_consumed`** (Histogram)
  - 

- **`bkrepo_quota_used_rate_metrics`** (Gauge)
  - bkrepo Quota Used Rate Metrics
  - Labels: `service_id`, `instance_id`, `repo_name`

- **`deploy_operation`** (Counter)
  - 

- **`monitor_task_collect_duration_seconds`** (Gauge)
  - duration to collect monitor task metrics

### Django Settings

- **Total Settings References**: 474
- **Files Scanned**: 2368

**Most Referenced Settings:**

| Setting | Reference Count |
|---------|-----------------|
| `_SMART_TAG_SUFFIX` | 0 |
| `WSGI_APPLICATION` | 0 |
| `WEBPACK_LOADER` | 0 |
| `VOLUME_NAME_APP_LOGGING` | 0 |
| `VOLUME_MOUNT_APP_LOGGING_DIR` | 0 |
| `VOLUME_HOST_PATH_APP_LOGGING_DIR` | 0 |
| `USE_TZ` | 0 |
| `USE_LEGACY_SUB_PATH_PATTERN` | 0 |
| `USE_L10N` | 0 |
| `USE_I18N` | 0 |
| `USER_TYPE` | 0 |
| `USER_SELECTOR_LIST_API` | 0 |
| `UNIQUE_ID_GEN_FUNC` | 0 |
| `ULTIMATE_PROC_SPEC_PLAN` | 0 |
| `TOKEN_REFRESH_ENDPOINT` | 0 |

## Testing & Reliability

### Unit Tests

- **Total Test Files**: 0
- **Total Tests**: 1607

### Exception Handlers

- **Total Handlers**: 1189
- **Files Scanned**: 422

**Handler Analysis:**
- Handlers with logging: 327
- Handlers that reraise: 554

**Top Exception Types Caught:**

| Exception Type | Count |
|----------------|-------|
| `Exception` | 285 |
| `ValueError` | 81 |
| `KeyError` | 65 |
| `APIGatewayResponseError` | 61 |
| `ImportError` | 51 |
| `ObjectDoesNotExist` | 47 |
| `AppEntityNotFound` | 35 |
| `ResourceMissing` | 18 |
| `TypeError` | 17 |
| `ServiceObjNotFound` | 15 |

**Best Practices:**
- ✓ Log exceptions before handling
- ✓ Catch specific exception types
- ✗ Avoid bare except clauses
- ✓ Re-raise exceptions when appropriate

## External Dependencies

### HTTP Requests

- **Total Requests**: 56
- **Unique URLs**: 8
- **Files Scanned**: 14

**By Library:**

| Library | Count | Notes |
|---------|-------|-------|
| `requests` | 56 | Synchronous |

**Top External APIs:**

| URL | Calls | Method | Library |
|-----|-------|--------|---------|
| `https://example.com/api` | 3 | POST | requests |
| `https://example.com/api?BK_PASSWORD=123456&api_...` | 1 | GET | requests |

**Internal/Dynamic URL Patterns:**
- Pattern `.../sites/register`: 2 usages
- Pattern `.../api/v1/apps/.../access-keys/...`: 2 usages
- Pattern `.../api/v1/apps/.../access-keys`: 2 usages
- Pattern `.../api/v1/apps`: 1 usages
- Pattern `.../api/overview`: 1 usages

**Recommendations:**
- Consider using connection pooling for frequently called APIs
- Implement retry logic with exponential backoff
- Add timeout configuration for all HTTP requests
- Monitor external API response times and failures

## Summary & Key Recommendations

### Key Findings

- **High Priority**: 88 high-complexity functions need review
- **Performance**: 33 blocking operations detected
- **Reliability**: 1189 exception handlers analyzed

### Priority Recommendations

#### 🔴 High Priority
- **Refactor complex functions**: Focus on functions with complexity > 15
  - Break down large functions into smaller, testable units
  - Consider using design patterns (Strategy, Command, etc.)

#### 🟡 Medium Priority
- **Optimize blocking operations**:
  - Replace `time.sleep()` with `asyncio.sleep()` in async code
  - Review database operations with `select_for_update()`
  - Consider async alternatives for I/O operations

#### 🟢 Low Priority / Best Practices
- **Code quality improvements**:
  - Add logging to exception handlers
  - Avoid bare except clauses
  - Document complex business logic
- **Monitoring & Observability**:
  - Add metrics for critical operations
  - Implement distributed tracing for external API calls
  - Monitor Redis usage and set appropriate TTLs

### Next Steps

1. **Review Critical Issues**: Address high-complexity functions and blocking operations
2. **Improve Test Coverage**: Focus on untested complex functions
3. **Performance Optimization**: Profile and optimize hot paths
4. **Documentation**: Document architecture decisions and complex logic
5. **Continuous Monitoring**: Set up alerts for performance regressions