# django-models 扫描报告

## 元数据
- **scanner_name**: django-models

## 概要信息
- **总数量**: 167
- **已扫描文件数**: 2368
- **扫描耗时**: 40822 毫秒

- **模型总数**: 167
- **字段总数**: 684
- **关系总数**: 148

## 结果详情

### App

**模块**: `apiserver.paasng.paas_wl.bk_app.applications.models.app`
**行号**: 32
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel
**描述**: App Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| owner | models.CharField | 35 | - | - | {"max_length": 64} |
| region | models.CharField | 36 | - | - | {"max_length": 32} |
| name | models.SlugField | 37 | - | - | {"max_length": 64, "validators": "`[validate_app_name]`"} |
| type | models.CharField | 40 | - | 应用类型 | {"db_index": true, "default": "`WlAppType.DEFAULT.value`", "max_length": 16} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('region', 'name') |

---


### Build

**模块**: `apiserver.paasng.paas_wl.bk_app.applications.models.build`
**行号**: 53
**基类**: paas_wl.utils.models.UuidAuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| application_id | models.UUIDField | 54 | - | 所属应用 | {"null": true} |
| module_id | models.UUIDField | 55 | - | 所属模块 | {"null": true} |
| owner | models.CharField | 57 | - | - | {"max_length": 64} |
| slug_path | models.TextField | 61 | slug path 形如 {region}/home/{name}:{branch}:{revision}/push | - | {"null": true} |
| image | models.TextField | 62 | 运行 Build 的镜像地址. 如果构件类型为 image，该值即构建产物; 如果构建产物是 Slug, 则返回 SlugRunner 的镜像 | - | {"null": true} |
| source_type | models.CharField | 68 | - | - | {"max_length": 128, "null": true} |
| branch | models.CharField | 69 | readable version, such as trunk/master | - | {"max_length": 128, "null": true} |
| revision | models.CharField | 70 | unique version, such as sha256 | - | {"max_length": 128, "null": true} |
| bkapp_revision_id | models.IntegerField | 76 | 与本次构建关联的 BkApp Revision id | - | {"null": true} |
| artifact_type | models.CharField | 78 | 构件类型 | - | {"default": "`ArtifactType.SLUG`", "max_length": 16} |
| artifact_detail | models.JSONField | 79 | 构件详情(展示信息) | - | {"default": {}} |
| artifact_deleted | models.BooleanField | 80 | slug/镜像是否已被清理 | - | {"default": false} |
| artifact_metadata | models.JSONField | 81 | 构件元信息, 包括 entrypoint/use_cnb/use_dockerfile 等信息 | - | {"default": {}} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | App | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| get_latest_by | created |
| ordering | ['-created'] |

---


### BuildProcess

**模块**: `apiserver.paasng.paas_wl.bk_app.applications.models.build`
**行号**: 259
**基类**: paas_wl.utils.models.UuidAuditedModel
**描述**: This Build Process was invoked via a source tarball or anything similar

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| application_id | models.UUIDField | 262 | - | 所属应用 | {"null": true} |
| module_id | models.UUIDField | 263 | - | 所属模块 | {"null": true} |
| owner | models.CharField | 265 | - | - | {"max_length": 64} |
| image | models.CharField | 267 | builder image | - | {"max_length": 512, "null": true} |
| generation | models.PositiveBigIntegerField | 270 | 每个应用独立的自增ID | 自增ID | {} |
| invoke_message | models.CharField | 271 | 触发信息 | - | {"blank": true, "max_length": 255, "null": true} |
| source_tar_path | models.CharField | 272 | - | - | {"max_length": 2048} |
| branch | models.CharField | 273 | - | - | {"max_length": 128, "null": true} |
| revision | models.CharField | 274 | - | - | {"max_length": 128, "null": true} |
| logs_was_ready_at | models.DateTimeField | 275 | Pod 状态就绪允许读取日志的时间 | - | {"null": true} |
| int_requested_at | models.DateTimeField | 276 | 用户请求中断的时间 | - | {"null": true} |
| completed_at | models.DateTimeField | 277 | failed/successful/interrupted 都是完成 | 完成时间 | {"null": true} |
| status | models.CharField | 281 | - | - | {"choices": "`make_enum_choices(BuildStatus)`", "default": "`BuildStatus.PENDING.value`", "max_length": 12} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | App | 不适用 | `models.CASCADE` |
| output_stream | models.OneToOneField | OutputStream | 不适用 | `models.CASCADE` |
| build | models.OneToOneField | Build | build_process | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| get_latest_by | created |
| ordering | ['-created'] |

---


### Config

**模块**: `apiserver.paasng.paas_wl.bk_app.applications.models.config`
**行号**: 55
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel
**描述**: App configs, includes env variables and resource limits

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| owner | models.CharField | 58 | - | - | {"max_length": 64} |
| domain | models.CharField | 63 | - | - | {"default": "", "max_length": 64} |
| cluster | models.CharField | 65 | - | - | {"blank": true, "default": "", "max_length": 64} |
| image | models.CharField | 66 | - | - | {"max_length": 256, "null": true} |
| mount_log_to_host | models.BooleanField | 70 | Whether mount app logs to host | - | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | App | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| get_latest_by | created |
| ordering | ['-created'] |
| unique_together | (('app', 'uuid'),) |

---


### OutputStreamLine

**模块**: `apiserver.paasng.paas_wl.bk_app.applications.models.misc`
**行号**: 30
**基类**: models.Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| stream | models.CharField | 32 | - | - | {"max_length": 16} |
| line | models.TextField | 33 | - | - | {} |
| created | models.DateTimeField | 34 | - | - | {"auto_now_add": true} |
| updated | models.DateTimeField | 35 | - | - | {"auto_now": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| output_stream | models.ForeignKey | OutputStream | lines | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ['created'] |

---


### Release

**模块**: `apiserver.paasng.paas_wl.bk_app.applications.models.release`
**行号**: 104
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| owner | models.CharField | 111 | - | - | {"max_length": 64} |
| version | models.PositiveIntegerField | 113 | - | - | {} |
| summary | models.TextField | 114 | - | - | {"blank": true, "null": true} |
| failed | models.BooleanField | 115 | - | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | App | 不适用 | `models.CASCADE` |
| config | models.ForeignKey | Config | 不适用 | `models.CASCADE` |
| build | models.ForeignKey | Build | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| get_latest_by | created |
| ordering | ['-created'] |
| unique_together | (('app', 'version'),) |

---


### AppModelResource

**模块**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.app_resource`
**行号**: 82
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: Cloud-native Application's Model Resource

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| application_id | models.UUIDField | 85 | - | `_('所属应用')` | {"null": false} |
| module_id | models.UUIDField | 86 | - | `_('所属模块')` | {"null": false, "unique": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| revision | models.OneToOneField | AppModelRevision | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| indexes | `[models.Index(fields=['application_id', 'module_id'])]` |

---


### AppModelRevision

**模块**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.app_resource`
**行号**: 111
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: Revisions of cloud-native Application's Model Resource

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| application_id | models.UUIDField | 114 | - | `_('所属应用')` | {"null": false} |
| module_id | models.UUIDField | 115 | - | `_('所属模块')` | {"null": false} |
| version | models.CharField | 119 | - | `_('模型版本')` | {"max_length": 64} |
| yaml_value | models.TextField | 120 | - | `_('应用模型（YAML 格式）')` | {} |
| json_value | models.JSONField | 122 | - | `_('应用模型（JSON 格式）')` | {} |
| deployed_value | models.JSONField | 125 | - | `_('已部署的应用模型（JSON 格式）')` | {"null": true} |
| has_deployed | models.BooleanField | 126 | - | `_('是否已部署')` | {"default": false} |
| is_draft | models.BooleanField | 127 | - | `_('是否草稿')` | {"default": false} |
| is_deleted | models.BooleanField | 128 | - | `_('是否已删除')` | {"default": false} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| indexes | `[models.Index(fields=['application_id', 'module_id'])]` |

---


### AppModelDeploy

**模块**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.app_resource`
**行号**: 158
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: This model stores the cloud-native app's deployment histories.

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| application_id | models.UUIDField | 165 | - | `_('所属应用')` | {"null": false} |
| module_id | models.UUIDField | 166 | - | `_('所属模块')` | {"null": false} |
| environment_name | models.CharField | 168 | - | `_('环境名称')` | {"choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": false} |
| name | models.CharField | 173 | - | `_('Deploy 名称')` | {"max_length": 64} |
| status | models.CharField | 177 | - | `_('状态')` | {"blank": true, "choices": "`DeployStatus.get_choices()`", "max_length": 32, "null": true} |
| reason | models.CharField | 180 | - | `_('状态原因')` | {"blank": true, "max_length": 128, "null": true} |
| message | models.TextField | 181 | - | `_('状态描述文字')` | {"blank": true, "null": true} |
| last_transition_time | models.DateTimeField | 182 | - | `_('状态最近变更时间')` | {"null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| revision | models.ForeignKey | AppModelRevision | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('application_id', 'module_id', 'environment_name', 'name') |

---


### ConfigMapSource

**模块**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.mount`
**行号**: 33
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: ConfigMap 类型的挂载资源

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| application_id | models.UUIDField | 36 | - | `_('所属应用')` | {"null": false} |
| module_id | models.UUIDField | 37 | - | `_('所属模块')` | {"null": true} |
| environment_name | models.CharField | 38 | - | `_('环境名称')` | {"choices": "`MountEnvName.get_choices()`", "max_length": 16, "null": false} |
| name | models.CharField | 41 | `_('挂载资源名')` | - | {"max_length": 63} |
| data | models.JSONField | 42 | - | - | {"default": "`dict`"} |
| display_name | models.CharField | 43 | `_('挂载资源展示名称')` | - | {"max_length": 63, "null": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('name', 'application_id', 'environment_name') |

---


### PersistentStorageSource

**模块**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.mount`
**行号**: 52
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: 持久存储类型的挂载资源

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| application_id | models.UUIDField | 55 | - | `_('所属应用')` | {"null": false} |
| module_id | models.UUIDField | 56 | - | `_('所属模块')` | {"null": true} |
| environment_name | models.CharField | 57 | - | `_('环境名称')` | {"choices": "`MountEnvName.get_choices()`", "max_length": 16, "null": false} |
| name | models.CharField | 60 | `_('挂载资源名')` | - | {"max_length": 63} |
| storage_size | models.CharField | 61 | - | - | {"max_length": 63} |
| storage_class_name | models.CharField | 62 | - | - | {"max_length": 63} |
| display_name | models.CharField | 63 | `_('挂载资源展示名称')` | - | {"max_length": 63, "null": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('name', 'application_id', 'environment_name') |

---


### Mount

**模块**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.mount`
**行号**: 72
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: 挂载配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| module_id | models.UUIDField | 75 | - | `_('所属模块')` | {"null": false} |
| environment_name | models.CharField | 78 | - | `_('环境名称')` | {"choices": "`MountEnvName.get_choices()`", "max_length": 16, "null": false} |
| name | models.CharField | 81 | `_('挂载点的名称')` | - | {"max_length": 63} |
| mount_path | models.CharField | 82 | - | - | {"max_length": 128} |
| source_type | models.CharField | 83 | - | - | {"choices": "`VolumeSourceType.get_choices()`", "max_length": 32} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module_id', 'mount_path', 'environment_name') |

---


### AppMetricsMonitor

**模块**: `apiserver.paasng.paas_wl.bk_app.monitoring.app_monitor.models`
**行号**: 23
**基类**: paas_wl.bk_app.applications.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| is_enabled | models.BooleanField | 25 | 是否启动 AppMetrics | - | {"default": true} |
| port | models.IntegerField | 26 | Service 端口 | - | {} |
| target_port | models.IntegerField | 27 | 容器内的端口 | - | {} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.OneToOneField | `WlApp` | 不适用 | `models.CASCADE` |


---


### ProcessSpecPlan

**模块**: `apiserver.paasng.paas_wl.bk_app.processes.models`
**行号**: 59
**基类**: models.Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 60 | - | - | {"db_index": true, "max_length": 32} |
| max_replicas | models.IntegerField | 61 | - | - | {} |
| is_active | models.BooleanField | 64 | - | 是否可用 | {"default": true} |
| created | models.DateTimeField | 65 | - | - | {"auto_now_add": true} |
| updated | models.DateTimeField | 66 | - | - | {"auto_now": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| get_latest_by | created |

---


### ProcessSpec

**模块**: `apiserver.paasng.paas_wl.bk_app.processes.models`
**行号**: 80
**基类**: paas_wl.utils.models.TimestampedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 81 | - | - | {"max_length": 32} |
| type | models.CharField | 82 | - | - | {"max_length": 32} |
| proc_command | models.TextField | 87 | 进程启动命令(包含完整命令和参数的字符串), 只能与 command/args 二选一 | - | {"null": true} |
| port | models.IntegerField | 92 | 容器端口 | - | {"null": true} |
| target_replicas | models.IntegerField | 94 | - | - | {"default": 1} |
| target_status | models.CharField | 95 | - | - | {"default": "start", "max_length": 32} |
| autoscaling | models.BooleanField | 97 | - | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| engine_app | models.ForeignKey | api.App | process_specs | `models.DO_NOTHING` |
| plan | models.ForeignKey | `ProcessSpecPlan` | 不适用 | `models.CASCADE` |


---


### ProcessProbe

**模块**: `apiserver.paasng.paas_wl.bk_app.processes.models`
**行号**: 276
**基类**: models.Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| process_type | models.CharField | 279 | - | - | {"max_length": 255} |
| probe_type | models.CharField | 280 | - | - | {"choices": "`ProbeType.get_django_choices()`", "max_length": 255} |
| initial_delay_seconds | models.IntegerField | 283 | - | - | {"default": 0} |
| timeout_seconds | models.PositiveIntegerField | 284 | - | - | {"default": 1} |
| period_seconds | models.PositiveIntegerField | 285 | - | - | {"default": 10} |
| success_threshold | models.PositiveIntegerField | 286 | - | - | {"default": 1} |
| failure_threshold | models.PositiveIntegerField | 287 | - | - | {"default": 3} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | api.App | process_probe | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('app', 'process_type', 'probe_type') |

---


### Cluster

**模块**: `apiserver.paasng.paas_wl.infras.cluster.models`
**行号**: 236
**基类**: paas_wl.utils.models.UuidAuditedModel
**描述**: 应用集群

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| region | models.CharField | 239 | - | - | {"db_index": true, "max_length": 32} |
| name | models.CharField | 240 | name of the cluster | - | {"max_length": 32, "unique": true} |
| type | models.CharField | 241 | cluster type | - | {"default": "`ClusterType.NORMAL`", "max_length": 32} |
| description | models.TextField | 242 | 描述信息 | - | {"blank": true} |
| is_default | models.BooleanField | 243 | 是否为默认集群 | - | {"default": false, "null": true} |
| token_type | models.IntegerField | 253 | - | - | {"null": true} |



---


### APIServer

**模块**: `apiserver.paasng.paas_wl.infras.cluster.models`
**行号**: 291
**基类**: paas_wl.utils.models.UuidAuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| host | models.CharField | 293 | API Server 的后端地址 | - | {"max_length": 255} |
| overridden_hostname | models.CharField | 294 | 在请求该 APIServer 时, 使用该 hostname 替换具体的 backend 中的 hostname | - | {"blank": true, "default": null, "max_length": 255, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| cluster | models.ForeignKey | `Cluster` | api_servers | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('cluster', 'host') |

---


### AppAddOnTemplate

**模块**: `apiserver.paasng.paas_wl.infras.resource_templates.models`
**行号**: 28
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel
**描述**: 应用挂件模版

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| region | models.CharField | 31 | - | - | {"max_length": 32} |
| name | models.CharField | 32 | - | - | {"max_length": 64} |
| spec | models.TextField | 33 | - | - | {} |
| enabled | models.BooleanField | 34 | - | - | {"default": true} |
| type | models.IntegerField | 35 | - | - | {"default": "`AppAddOnType.SIMPLE_SIDECAR.value`"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('region', 'name') |

---


### AppAddOn

**模块**: `apiserver.paasng.paas_wl.infras.resource_templates.models`
**行号**: 55
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel
**描述**: 应用挂件关联实例

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| enabled | models.BooleanField | 60 | - | - | {"default": true} |
| spec | models.TextField | 61 | - | - | {} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | `WlApp` | add_ons | `models.CASCADE` |
| template | models.ForeignKey | `AppAddOnTemplate` | instances | `models.CASCADE` |


---


### AuditedModel

**模块**: `apiserver.paasng.paas_wl.utils.models`
**行号**: 31
**基类**: models.Model
**描述**: Audited model with 'created' and 'updated' fields.

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| created | models.DateTimeField | 34 | - | - | {"auto_now_add": true} |
| updated | models.DateTimeField | 35 | - | - | {"auto_now": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### UuidAuditedModel

**模块**: `apiserver.paasng.paas_wl.utils.models`
**行号**: 41
**基类**: apiserver.paasng.paas_wl.utils.models.AuditedModel
**描述**: Add a UUID primary key to an class`AuditedModel`.

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| uuid | models.UUIDField | 44 | - | - | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### TimestampedModel

**模块**: `apiserver.paasng.paas_wl.utils.models`
**行号**: 52
**基类**: models.Model
**描述**: Model with 'created' and 'updated' fields.

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| region | models.CharField | 55 | 部署区域 | - | {"max_length": 32} |
| created | models.DateTimeField | 56 | - | - | {"auto_now_add": true} |
| updated | models.DateTimeField | 57 | - | - | {"auto_now": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### AppImageCredential

**模块**: `apiserver.paasng.paas_wl.workloads.images.models`
**行号**: 46
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel
**描述**: ImageCredential of applications, each object(entry) represents an (username + password) pair for a registry

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| registry | models.CharField | 51 | - | - | {"max_length": 255} |
| username | models.CharField | 52 | - | - | {"blank": false, "max_length": 32} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | api.App | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('app', 'registry') |

---


### AppUserCredential

**模块**: `apiserver.paasng.paas_wl.workloads.images.models`
**行号**: 66
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel
**描述**: App owned UserCredential, aka (Username + Password) pair

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| application_id | models.UUIDField | 69 | - | `_('所属应用')` | {"null": false} |
| name | models.CharField | 71 | 凭证名称 | - | {"max_length": 32} |
| username | models.CharField | 72 | 账号 | - | {"max_length": 64} |
| description | models.TextField | 74 | 描述 | - | {} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('application_id', 'name') |

---


### RegionClusterState

**模块**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`
**行号**: 32
**基类**: paas_wl.bk_app.applications.models.AuditedModel
**描述**: A RegionClusterState is a state which describes what the cluster is in a specified moment. it

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| region | models.CharField | 41 | - | - | {"max_length": 32} |
| cluster_name | models.CharField | 42 | - | - | {"max_length": 32, "null": true} |
| name | models.CharField | 43 | - | - | {"max_length": 64} |
| nodes_digest | models.CharField | 44 | - | - | {"db_index": true, "max_length": 64} |
| nodes_cnt | models.IntegerField | 45 | - | - | {"default": 0} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('region', 'cluster_name', 'name') |
| get_latest_by | created |
| ordering | ['-created'] |

---


### RCStateAppBinding

**模块**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`
**行号**: 61
**基类**: paas_wl.bk_app.applications.models.AuditedModel
**描述**: If an app was bind with one RegionClusterState instance, it means that the app will not be

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.OneToOneField | `WlApp` | 不适用 | `models.CASCADE` |
| state | models.ForeignKey | `RegionClusterState` | 不适用 | `models.CASCADE` |


---


### EgressSpec

**模块**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`
**行号**: 70
**基类**: paas_wl.bk_app.applications.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| replicas | models.IntegerField | 72 | - | - | {"default": 1} |
| cpu_limit | models.CharField | 73 | - | - | {"max_length": 16} |
| memory_limit | models.CharField | 74 | - | - | {"max_length": 16} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| wl_app | models.OneToOneField | `WlApp` | 不适用 | `models.CASCADE` |


---


### EgressRule

**模块**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`
**行号**: 114
**基类**: paas_wl.bk_app.applications.models.AuditedModel
**描述**: BCS Egress.spec.rules

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| dst_port | models.IntegerField | 120 | - | - | {} |
| host | models.CharField | 121 | - | - | {"max_length": 128} |
| protocol | models.CharField | 123 | - | - | {"choices": "`NetworkProtocol.get_django_choices()`", "max_length": 32} |
| src_port | models.IntegerField | 127 | - | - | {} |
| service | models.CharField | 128 | - | - | {"max_length": 128} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| spec | models.ForeignKey | `EgressSpec` | rules | `models.CASCADE` |


---


### AppDomain

**模块**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`
**行号**: 33
**基类**: paas_wl.bk_app.applications.models.AuditedModel
**描述**: Domains of applications, each object(entry) represents an (domain + path_prefix) pair.

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| region | models.CharField | 37 | - | - | {"max_length": 32} |
| host | models.CharField | 38 | - | - | {"max_length": 128} |
| path_prefix | models.CharField | 43 | the accessable path for current domain | - | {"default": "/", "max_length": 64} |
| https_enabled | models.BooleanField | 46 | - | - | {"default": false} |
| https_auto_redirection | models.BooleanField | 47 | - | - | {"default": false} |
| source | models.IntegerField | 52 | - | - | {"choices": "`make_enum_choices(AppDomainSource)`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | `WlApp` | 不适用 | `models.CASCADE` |
| cert | models.ForeignKey | AppDomainCert | 不适用 | `models.SET_NULL` |
| shared_cert | models.ForeignKey | AppDomainSharedCert | 不适用 | `models.SET_NULL` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('region', 'host', 'path_prefix') |
| db_table | services_appdomain |

---


### BasicCert

**模块**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`
**行号**: 66
**基类**: paas_wl.bk_app.applications.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| region | models.CharField | 67 | - | - | {"max_length": 32} |
| name | models.CharField | 68 | - | - | {"max_length": 128, "unique": true, "validators": "`[RegexValidator(DNS_SAFE_PATTERN)]`"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### AppDomainSharedCert

**模块**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`
**行号**: 90
**基类**: apiserver.paasng.paas_wl.workloads.networking.ingress.models.BasicCert
**描述**: Shared TLS Certifications for AppDomain, every app's domain may link to this certificate as

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| auto_match_cns | models.TextField | 96 | - | - | {"max_length": 2048} |
| region | models.CharField | 67 | - | - | {"max_length": 32} |
| name | models.CharField | 68 | - | - | {"max_length": 128, "unique": true, "validators": "`[RegexValidator(DNS_SAFE_PATTERN)]`"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| db_table | services_appdomainsharedcert |

---


### AppSubpath

**模块**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`
**行号**: 129
**基类**: paas_wl.bk_app.applications.models.AuditedModel
**描述**: stores application's subpaths

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| region | models.CharField | 133 | - | - | {"max_length": 32} |
| cluster_name | models.CharField | 134 | - | - | {"max_length": 32} |
| subpath | models.CharField | 135 | - | - | {"max_length": 128} |
| source | models.IntegerField | 136 | - | - | {} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | `WlApp` | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('region', 'subpath') |
| db_table | services_appsubpath |

---


### Domain

**模块**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`
**行号**: 151
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: custom domain for application

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 154 | 域名 | - | {"max_length": 253, "null": false} |
| path_prefix | models.CharField | 155 | the accessable path for current domain | - | {"default": "/", "max_length": 64} |
| module_id | models.UUIDField | 156 | 关联的模块 ID | - | {"null": false} |
| environment_id | models.BigIntegerField | 157 | 关联的环境 ID | - | {"null": false} |
| https_enabled | models.BooleanField | 158 | 该域名是否开启 https | - | {"default": false, "null": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('name', 'path_prefix', 'module_id', 'environment_id') |
| db_table | services_domain |

---


### Command

**模块**: `apiserver.paasng.paas_wl.workloads.release_controller.hooks.models`
**行号**: 80
**基类**: paas_wl.utils.models.UuidAuditedModel
**描述**: The Command Model, which will be used to schedule a container running `command`,

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| type | models.CharField | 84 | - | - | {"choices": "`CommandType.get_choices()`", "max_length": 32} |
| version | models.PositiveIntegerField | 87 | - | - | {} |
| command | models.TextField | 88 | - | - | {} |
| exit_code | models.SmallIntegerField | 89 | 容器结束状态码, -1 表示未知 | - | {"null": true} |
| status | models.CharField | 90 | - | - | {"choices": "`CommandStatus.get_choices()`", "default": "`CommandStatus.PENDING.value`", "max_length": 12} |
| logs_was_ready_at | models.DateTimeField | 91 | Pod 状态就绪允许读取日志的时间 | - | {"null": true} |
| int_requested_at | models.DateTimeField | 92 | 用户请求中断的时间 | - | {"null": true} |
| operator | models.CharField | 97 | 操作者(被编码的 username), 目前该字段无意义 | - | {"max_length": 64} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | api.App | 不适用 | `models.CASCADE` |
| output_stream | models.OneToOneField | api.OutputStream | 不适用 | `models.CASCADE` |
| build | models.ForeignKey | api.Build | 不适用 | `models.CASCADE` |
| config | models.ForeignKey | api.Config | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| get_latest_by | created |
| ordering | ['-created'] |

---


### CIResourceAppEnvRelation

**模块**: `apiserver.paasng.paasng.accessories.ci.models`
**行号**: 35
**基类**: paasng.utils.models.TimestampedModel
**描述**: CI 资源

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| enabled | models.BooleanField | 42 | - | 是否启用 | {"default": true} |
| backend | models.CharField | 43 | - | CI引擎 | {"choices": "`CIBackend.get_django_choices()`", "max_length": 32} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| env | models.ForeignKey | applications.ApplicationEnvironment | ci_resources | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| get_latest_by | created |

---


### CIResourceAtom

**模块**: `apiserver.paasng.paasng.accessories.ci.models`
**行号**: 49
**基类**: paasng.utils.models.TimestampedModel
**描述**: CI 资源原子

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| id | models.CharField | 52 | - | - | {"db_index": true, "max_length": 64, "primary_key": true, "unique": true} |
| name | models.CharField | 53 | - | - | {"max_length": 32} |
| enabled | models.BooleanField | 57 | - | 是否启用 | {"default": true} |
| backend | models.CharField | 59 | - | CI引擎 | {"choices": "`CIBackend.get_django_choices()`", "max_length": 32} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| env | models.ForeignKey | applications.ApplicationEnvironment | ci_resource_atoms | `models.CASCADE` |
| resource | models.ForeignKey | `CIResourceAppEnvRelation` | related_atoms | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('env', 'name', 'backend') |

---


### DevSandbox

**模块**: `apiserver.paasng.paasng.accessories.dev_sandbox.models`
**行号**: 42
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: DevSandbox Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| code | models.CharField | 45 | 沙箱标识 | - | {"max_length": 8, "unique": true} |
| status | models.CharField | 47 | - | 沙箱状态 | {"choices": "`DevSandboxStatus.get_choices()`", "max_length": 32} |
| expired_at | models.DateTimeField | 48 | 到期时间 | - | {"null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | `Module` | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module', 'owner') |

---


### CodeEditor

**模块**: `apiserver.paasng.paasng.accessories.dev_sandbox.models`
**行号**: 59
**基类**: paasng.utils.models.UuidAuditedModel
**描述**: CodeEditor Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| dev_sandbox | models.OneToOneField | `DevSandbox` | code_editor | `models.CASCADE` |


---


### ProcessStructureLogCollectorConfig

**模块**: `apiserver.paasng.paasng.accessories.log.models`
**行号**: 88
**基类**: paasng.utils.models.AuditedModel
**描述**: 进程结构化日志采集配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| collector_config_id | models.BigAutoField | 91 | - | - | {"primary_key": true} |
| process_type | models.CharField | 96 | 进程类型(名称) | - | {"max_length": 16} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |
| env | models.ForeignKey | `ModuleEnvironment` | 不适用 | `models.CASCADE` |


---


### ElasticSearchConfig

**模块**: `apiserver.paasng.paasng.accessories.log.models`
**行号**: 101
**基类**: paasng.utils.models.UuidAuditedModel
**描述**: ES查询配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| collector_config_id | models.CharField | 104 | 采集配置ID | - | {"max_length": 64, "unique": true} |
| backend_type | models.CharField | 105 | 日志后端类型, 可选 'es', 'bkLog'  | - | {"max_length": 16} |



---


### ProcessLogQueryConfig

**模块**: `apiserver.paasng.paasng.accessories.log.models`
**行号**: 126
**基类**: paasng.utils.models.UuidAuditedModel
**描述**: 进程日志查询配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| process_type | models.CharField | 131 | - | - | {"blank": true, "max_length": 16, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| env | models.ForeignKey | `ModuleEnvironment` | 不适用 | `models.CASCADE` |
| stdout | models.ForeignKey | `ElasticSearchConfig` | related_stdout | `models.SET_NULL` |
| json | models.ForeignKey | `ElasticSearchConfig` | related_json | `models.SET_NULL` |
| ingress | models.ForeignKey | `ElasticSearchConfig` | related_ingress | `models.SET_NULL` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('env', 'process_type') |

---


### CustomCollectorConfig

**模块**: `apiserver.paasng.paasng.accessories.log.models`
**行号**: 164
**基类**: paasng.utils.models.UuidAuditedModel
**描述**: 日志平台自定义采集项配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name_en | models.CharField | 169 | 5-50个字符，仅包含字母数字下划线, 查询索引是 name_en-* | - | {"db_index": true, "max_length": 50} |
| collector_config_id | models.BigIntegerField | 175 | 采集配置ID | - | {"db_index": true} |
| index_set_id | models.BigIntegerField | 176 | 查询时使用 | - | {"null": true} |
| bk_data_id | models.BigIntegerField | 177 | - | - | {} |
| log_paths | models.JSONField | 179 | - | - | {} |
| log_type | models.CharField | 180 | - | - | {"max_length": 32} |
| is_builtin | models.BooleanField | 182 | - | - | {"default": false} |
| is_enabled | models.BooleanField | 183 | - | - | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | `Module` | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module', 'name_en') |

---


### Tag

**模块**: `apiserver.paasng.paasng.accessories.publish.market.models`
**行号**: 53
**基类**: models.Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 66 | 分类名称 | - | {"max_length": 64} |
| remark | models.CharField | 67 | 备注 | - | {"blank": true, "max_length": 255, "null": true} |
| index | models.IntegerField | 68 | 显示排序字段 | - | {"default": 0} |
| enabled | models.BooleanField | 69 | 创建应用时是否可选择该分类 | - | {"default": true} |
| region | models.CharField | 70 | 部署区域 | - | {"max_length": 32} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| parent | models.ForeignKey | self | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ('index', 'id') |

---


### Product

**模块**: `apiserver.paasng.paasng.accessories.publish.market.models`
**行号**: 122
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: 蓝鲸应用: 开发者中心的编辑属性

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| code | models.CharField | 130 | 应用编码 | - | {"max_length": 64, "unique": true} |
| type | models.SmallIntegerField | 156 | 按实现方式分类 | - | {"choices": "`constant.AppType.get_choices()`"} |
| state | models.SmallIntegerField | 157 | 应用状态 | - | {"choices": "`constant.AppState.get_choices()`", "default": 1} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.OneToOneField | `Application` | 不适用 | `models.CASCADE` |
| tag | models.ForeignKey | `Tag` | 不适用 | `models.SET_NULL` |


---


### DisplayOptions

**模块**: `apiserver.paasng.paasng.accessories.publish.market.models`
**行号**: 205
**基类**: models.Model
**描述**: app展示相关的属性

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| visible | models.BooleanField | 210 | 选项: true(是)，false(否) | - | {"default": true} |
| width | models.IntegerField | 212 | 应用页面宽度，必须为整数，单位为px | - | {"default": 890} |
| height | models.IntegerField | 213 | 应用页面高度，必须为整数，单位为px | - | {"default": 550} |
| is_win_maximize | models.BooleanField | 215 | - | - | {"default": false} |
| win_bars | models.BooleanField | 216 | 选项: true(on)，false(off) | - | {"default": true} |
| resizable | models.BooleanField | 217 | 选项：true(可以拉伸)，false(不可以拉伸) | - | {"default": true} |
| contact | models.CharField | 222 | - | - | {"blank": true, "max_length": 128, "null": true} |
| open_mode | models.CharField | 223 | - | - | {"choices": "`constant.OpenMode.get_django_choices()`", "default": "`constant.OpenMode.NEW_TAB.value`", "max_length": 20} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| product | models.OneToOneField | `Product` | 不适用 | `models.CASCADE` |


---


### MarketConfig

**模块**: `apiserver.paasng.paasng.accessories.publish.market.models`
**行号**: 268
**基类**: paasng.utils.models.TimestampedModel
**描述**: 应用市场相关功能配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| enabled | models.BooleanField | 274 | - | 是否开启 | {} |
| auto_enable_when_deploy | models.BooleanField | 275 | - | 成功部署主模块正式环境后, 是否自动打开市场 | {"null": true} |
| source_url_type | models.SmallIntegerField | 276 | - | 访问地址类型 | {} |
| source_tp_url | models.URLField | 278 | - | 第三方访问地址 | {"blank": true, "null": true} |
| custom_domain_url | models.URLField | 279 | - | 绑定的独立域名访问地址 | {"blank": true, "null": true} |
| prefer_https | models.BooleanField | 280 | - | [deprecated] 仅为 False 时强制使用 http, 否则保持与集群 https_enabled 状态一致 | {"null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.OneToOneField | `Application` | market_config | `models.CASCADE` |
| source_module | models.ForeignKey | `Module` | 不适用 | `models.CASCADE` |


---


### TagMap

**模块**: `apiserver.paasng.paasng.accessories.publish.sync_market.models`
**行号**: 36
**基类**: django_models.Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| remote_id | django_models.IntegerField | 38 | - | - | {"db_index": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| tag | django_models.OneToOneField | `market_models.Tag` | 不适用 | `django_models.CASCADE` |


---


### ServiceModuleAttachment

**模块**: `apiserver.paasng.paasng.accessories.servicehub.models`
**行号**: 35
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: Module <-> Local Service relationship

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | modules.Module | 不适用 | `models.CASCADE` |
| service | models.ForeignKey | `Service` | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('service', 'module') |

---


### ServiceEngineAppAttachment

**模块**: `apiserver.paasng.paasng.accessories.servicehub.models`
**行号**: 48
**基类**: paasng.utils.models.OwnerTimestampedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| credentials_enabled | models.BooleanField | 59 | - | 是否使用凭证 | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| engine_app | models.ForeignKey | engine.EngineApp | service_attachment | `models.CASCADE` |
| service | models.ForeignKey | `Service` | 不适用 | `models.CASCADE` |
| plan | models.ForeignKey | `Plan` | 不适用 | `models.CASCADE` |
| service_instance | models.ForeignKey | `ServiceInstance` | service_attachment | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('service', 'engine_app') |

---


### RemoteServiceModuleAttachment

**模块**: `apiserver.paasng.paasng.accessories.servicehub.models`
**行号**: 126
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: Binding relationship of module <-> remote service

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| service_id | models.UUIDField | 130 | - | 远程增强服务 ID | {} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | modules.Module | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('service_id', 'module') |

---


### RemoteServiceEngineAppAttachment

**模块**: `apiserver.paasng.paasng.accessories.servicehub.models`
**行号**: 139
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: Binding relationship of engine app <-> remote service plan

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| service_id | models.UUIDField | 145 | - | 远程增强服务 ID | {} |
| plan_id | models.UUIDField | 146 | - | 远程增强服务 Plan ID | {} |
| service_instance_id | models.UUIDField | 147 | - | - | {"null": true} |
| credentials_enabled | models.BooleanField | 148 | - | 是否使用凭证 | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| engine_app | models.ForeignKey | engine.EngineApp | remote_service_attachment | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('service_id', 'engine_app') |

---


### SharedServiceAttachment

**模块**: `apiserver.paasng.paasng.accessories.servicehub.models`
**行号**: 192
**基类**: paasng.utils.models.TimestampedModel
**描述**: Share a service binding relationship from other modules

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| service_type | models.CharField | 196 | - | 增强服务类型 | {"max_length": 16} |
| service_id | models.UUIDField | 197 | - | 增强服务 ID | {} |
| ref_attachment_pk | models.IntegerField | 198 | - | 被共享的服务绑定关系主键 | {} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | modules.Module | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module', 'service_type', 'service_id') |

---


### ServiceCategory

**模块**: `apiserver.paasng.paasng.accessories.services.models`
**行号**: 36
**基类**: models.Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| sort_priority | models.IntegerField | 42 | - | - | {"default": 0} |



---


### Service

**模块**: `apiserver.paasng.paasng.accessories.services.models`
**行号**: 53
**基类**: paasng.utils.models.UuidAuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| region | models.CharField | 58 | - | - | {"max_length": 32} |
| name | models.CharField | 59 | - | 服务名称 | {"max_length": 64} |
| logo_b64 | models.TextField | 62 | - | 服务 logo 的地址, 支持base64格式 | {"blank": true, "null": true} |
| available_languages | models.CharField | 67 | - | 支持编程语言 | {"blank": true, "max_length": 1024, "null": true} |
| is_active | models.BooleanField | 69 | - | 是否可用 | {"default": true} |
| is_visible | models.BooleanField | 73 | - | 是否可见 | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| category | models.ForeignKey | `ServiceCategory` | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('region', 'name') |

---


### ServiceInstance

**模块**: `apiserver.paasng.paasng.accessories.services.models`
**行号**: 161
**基类**: paasng.utils.models.UuidAuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| to_be_deleted | models.BooleanField | 170 | - | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| service | models.ForeignKey | Service | 不适用 | `models.CASCADE` |
| plan | models.ForeignKey | Plan | 不适用 | `models.CASCADE` |


---


### PreCreatedInstance

**模块**: `apiserver.paasng.paasng.accessories.services.models`
**行号**: 176
**基类**: paasng.utils.models.UuidAuditedModel
**描述**: 预创建的服务实例

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| is_allocated | models.BooleanField | 182 | 实例是否已被分配 | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plan | models.ForeignKey | Plan | 不适用 | `models.SET_NULL` |


---


### Plan

**模块**: `apiserver.paasng.paasng.accessories.services.models`
**行号**: 196
**基类**: paasng.utils.models.UuidAuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 203 | - | - | {"max_length": 64} |
| description | models.CharField | 204 | - | 方案简介 | {"blank": true, "max_length": 1024} |
| is_active | models.BooleanField | 206 | - | 是否可用 | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| service | models.ForeignKey | Service | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('service', 'name') |

---


### ResourceId

**模块**: `apiserver.paasng.paasng.accessories.services.models`
**行号**: 227
**基类**: models.Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| namespace | models.CharField | 228 | - | - | {"max_length": 32} |
| uid | models.CharField | 229 | - | - | {"db_index": true, "max_length": 64, "null": false, "unique": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('namespace', 'uid') |

---


### AppModuleTagRel

**模块**: `apiserver.paasng.paasng.accessories.smart_advisor.models`
**行号**: 46
**基类**: models.Model
**描述**: A M2M relationship table for storing the relationship between application module and AppTag

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| tag_str | models.CharField | 52 | - | - | {"blank": false, "max_length": 128} |
| source | models.CharField | 53 | - | - | {"blank": false, "max_length": 32} |
| created | models.DateTimeField | 54 | - | - | {"auto_now_add": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | modules.Module | tag_rels | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module', 'tag_str') |

---


### DocumentaryLink

**模块**: `apiserver.paasng.paasng.accessories.smart_advisor.models`
**行号**: 67
**基类**: models.Model
**描述**: Links from document systems including blueking doc and other opensource documentations

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| location | models.CharField | 72 | - | - | {"blank": false, "max_length": 256} |
| priority | models.IntegerField | 75 | - | - | {"default": 1} |
| created | models.DateTimeField | 76 | - | - | {"default": "`timezone.now`"} |



---


### DeployFailurePattern

**模块**: `apiserver.paasng.paasng.accessories.smart_advisor.models`
**行号**: 92
**基类**: models.Model
**描述**: Stores common failure patterns for failed deployments

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| type | models.IntegerField | 95 | - | - | {"default": "`DeployFailurePatternType.REGULAR_EXPRESSION`"} |
| value | models.CharField | 96 | - | - | {"blank": false, "max_length": 2048} |
| tag_str | models.CharField | 97 | - | - | {"blank": false, "max_length": 128} |
| created | models.DateTimeField | 98 | - | - | {"default": "`timezone.now`"} |



---


### BkPluginProfile

**模块**: `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`
**行号**: 62
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: Profile which storing extra information for BkPlugins

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| introduction | models.CharField | 68 | 插件简介 | - | {"blank": true, "max_length": 512, "null": true} |
| contact | models.CharField | 69 | 使用 ; 分隔的用户名 | - | {"blank": true, "max_length": 128, "null": true} |
| api_gw_name | models.CharField | 81 | 为空时表示从未成功同步过，暂无已绑定网关 | - | {"blank": true, "max_length": 32, "null": true} |
| api_gw_id | models.IntegerField | 88 | - | - | {"null": true} |
| api_gw_last_synced_at | models.DateTimeField | 89 | - | - | {"null": true} |
| pre_distributor_codes | models.JSONField | 93 | - | - | {"blank": true, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.OneToOneField | `Application` | bk_plugin_profile | `models.CASCADE` |
| tag | models.ForeignKey | BkPluginTag | 不适用 | `models.SET_NULL` |


---


### BkPluginDistributor

**模块**: `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`
**行号**: 130
**基类**: paasng.utils.models.TimestampedModel
**描述**: A "Distributor" is responsible for providing a collection of BkPlugins to a group of users,

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 135 | 插件使用方名称 | - | {"max_length": 32, "unique": true} |
| code_name | models.CharField | 136 | 插件使用方的英文代号，可替代主键使用 | - | {"max_length": 32, "unique": true} |
| bk_app_code | models.CharField | 139 | 插件使用方所绑定的蓝鲸应用代号 | - | {"max_length": 20, "unique": true} |
| introduction | models.CharField | 142 | - | - | {"blank": true, "max_length": 512, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plugins | models.ManyToManyField | `Application` | distributors | 不适用 |


---


### BkPluginTag

**模块**: `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`
**行号**: 150
**基类**: paasng.utils.models.AuditedModel
**描述**: Plugins and applications use different markets, and plugins should have their own separate tags

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 153 | 插件使用方名称 | - | {"max_length": 32, "unique": true} |
| code_name | models.CharField | 154 | 分类英文名称，可替代主键使用 | - | {"max_length": 32, "unique": true} |
| priority | models.IntegerField | 155 | 数字越大，优先级越高 | - | {"default": 0} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ['-priority', 'name'] |

---


### PluginGradeManager

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.models`
**行号**: 34
**基类**: paasng.utils.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| pd_id | models.CharField | 41 | 插件类型标识 | - | {"max_length": 64} |
| plugin_id | models.CharField | 42 | 插件标识 | - | {"max_length": 32} |
| grade_manager_id | models.IntegerField | 43 | 分级管理员 ID | - | {} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('pd_id', 'plugin_id', 'grade_manager_id') |

---


### PluginUserGroup

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.models`
**行号**: 51
**基类**: paasng.utils.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| pd_id | models.CharField | 58 | 插件类型标识 | - | {"max_length": 64} |
| plugin_id | models.CharField | 59 | 插件标识 | - | {"max_length": 32} |
| role | models.IntegerField | 60 | - | - | {"default": "`PluginRole.DEVELOPER.value`"} |
| user_group_id | models.IntegerField | 61 | 权限中心用户组 ID | - | {} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('pd_id', 'plugin_id', 'role') |

---


### PluginDefinition

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`
**行号**: 57
**基类**: paasng.utils.models.UuidAuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| identifier | models.CharField | 58 | - | - | {"max_length": 64, "unique": true} |
| docs | models.CharField | 61 | - | - | {"max_length": 255} |
| logo | models.CharField | 63 | - | - | {"max_length": 255} |
| administrator | models.JSONField | 65 | - | - | {} |



---


### PluginBasicInfoDefinition

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`
**行号**: 88
**基类**: paasng.utils.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| access_mode | models.CharField | 95 | - | 基本信息查看模式 | {"default": "`PluginBasicInfoAccessMode.READWRITE`", "max_length": 16} |
| release_method | models.CharField | 98 | - | 发布方式 | {"max_length": 16} |
| repository_group | models.CharField | 99 | - | 插件代码初始化仓库组 | {"max_length": 255} |
| extra_fields_order | models.JSONField | 104 | - | - | {"default": "`list`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| pd | models.OneToOneField | `PluginDefinition` | basic_info_definition | `models.CASCADE` |


---


### PluginMarketInfoDefinition

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`
**行号**: 122
**基类**: paasng.utils.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| storage | models.CharField | 126 | - | 存储方式 | {"max_length": 16} |
| extra_fields_order | models.JSONField | 131 | - | - | {"default": "`list`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| pd | models.OneToOneField | `PluginDefinition` | market_info_definition | `models.CASCADE` |


---


### PluginConfigInfoDefinition

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`
**行号**: 134
**基类**: paasng.utils.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| docs | models.CharField | 141 | - | - | {"default": "", "max_length": 255} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| pd | models.OneToOneField | `PluginDefinition` | config_definition | `models.CASCADE` |


---


### PluginVisibleRangeDefinition

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`
**行号**: 146
**基类**: paasng.utils.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| pd | models.OneToOneField | `PluginDefinition` | visible_range_definition | `models.CASCADE` |


---


### PluginInstance

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**行号**: 69
**基类**: paasng.utils.models.UuidAuditedModel
**描述**: 插件实例

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| id | models.CharField | 73 | 插件id | - | {"max_length": 32} |
| extra_fields | models.JSONField | 76 | - | 额外字段 | {} |
| language | models.CharField | 78 | 冗余字段, 用于减少查询次数 | 开发语言 | {"max_length": 16} |
| repo_type | models.CharField | 79 | - | 源码托管类型 | {"max_length": 16, "null": true} |
| repository | models.CharField | 80 | - | - | {"max_length": 255} |
| status | models.CharField | 81 | - | 插件状态 | {"choices": "`constants.PluginStatus.get_choices()`", "default": "`constants.PluginStatus.WAITING_APPROVAL`", "max_length": 16} |
| publisher | models.CharField | 87 | - | 插件发布者 | {"default": "", "max_length": 64} |
| is_deleted | models.BooleanField | 90 | 是否已删除 | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| pd | models.ForeignKey | PluginDefinition | 不适用 | `models.SET_NULL` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('pd', 'id') |

---


### PluginMarketInfo

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**行号**: 151
**基类**: paasng.utils.models.AuditedModel
**描述**: 插件市场信息

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| category | models.CharField | 156 | - | 分类 | {"db_index": true, "max_length": 64} |
| contact | models.TextField | 159 | 以分号(;)分割 | 联系人 | {} |
| extra_fields | models.JSONField | 160 | - | 额外字段 | {} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plugin | models.OneToOneField | `PluginInstance` | 不适用 | `models.CASCADE` |


---


### PluginRelease

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**行号**: 227
**基类**: paasng.utils.models.AuditedModel
**描述**: 插件发布版本

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| type | models.CharField | 233 | - | 版本类型(正式/测试) | {"choices": "`constants.PluginReleaseType.get_choices()`", "max_length": 16} |
| version | models.CharField | 236 | - | 版本号 | {"max_length": 255} |
| comment | models.TextField | 237 | - | 版本日志 | {} |
| extra_fields | models.JSONField | 238 | - | 额外字段 | {} |
| semver_type | models.CharField | 239 | 该字段只用于自动生成版本号的插件 | 语义化版本类型 | {"max_length": 16, "null": true} |
| source_location | models.CharField | 243 | - | 代码仓库地址 | {"max_length": 2048} |
| source_version_type | models.CharField | 244 | - | 代码版本类型(branch/tag) | {"max_length": 128, "null": true} |
| source_version_name | models.CharField | 245 | - | 代码分支名/tag名 | {"max_length": 128, "null": true} |
| source_hash | models.CharField | 246 | - | 代码提交哈希 | {"max_length": 128} |
| status | models.CharField | 254 | - | - | {"default": "`constants.PluginReleaseStatus.INITIAL`", "max_length": 16} |
| tag | models.CharField | 255 | - | 标签 | {"db_index": true, "max_length": 16, "null": true} |
| retryable | models.BooleanField | 256 | 失败后是否可重试 | - | {"default": true} |
| is_rolled_back | models.BooleanField | 257 | 是否已回滚 | - | {"default": false} |
| gray_status | models.CharField | 260 | - | 灰度发布状态 | {"default": "`constants.GrayReleaseStatus.IN_GRAY`", "max_length": 32} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plugin | models.ForeignKey | `PluginInstance` | all_versions | `models.CASCADE` |
| current_stage | models.OneToOneField | PluginReleaseStage | 不适用 | `models.SET_NULL` |


---


### PluginReleaseStage

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**行号**: 324
**基类**: paasng.utils.models.AuditedModel
**描述**: 插件发布阶段

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| stage_id | models.CharField | 331 | - | 阶段标识 | {"max_length": 32} |
| stage_name | models.CharField | 332 | 冗余字段, 用于减少查询次数 | 阶段名称 | {"max_length": 16} |
| invoke_method | models.CharField | 333 | 冗余字段, 用于减少查询次数 | 触发方式 | {"max_length": 16} |
| status_polling_method | models.CharField | 334 | 冗余字段, 用于减少查询次数 | 阶段的状态轮询方式 | {"default": "`constants.StatusPollingMethod.API`", "max_length": 16} |
| status | models.CharField | 341 | - | 发布状态 | {"default": "`constants.PluginReleaseStatus.INITIAL`", "max_length": 16} |
| fail_message | models.TextField | 342 | - | 错误原因 | {} |
| api_detail | models.JSONField | 344 | 该字段仅 invoke_method = api 时可用 | API 详情 | {"null": true} |
| pipeline_detail | models.JSONField | 345 | 该字段仅 invoke_method = pipeline 时可用 | 流水线构建详情 | {"default": null, "null": true} |
| operator | models.CharField | 348 | - | 操作人 | {"max_length": 32, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| release | models.ForeignKey | `PluginRelease` | all_stages | `models.CASCADE` |
| next_stage | models.OneToOneField | PluginReleaseStage | 不适用 | `models.SET_NULL` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('release', 'stage_id') |

---


### PluginReleaseStrategy

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**行号**: 375
**基类**: paasng.utils.models.AuditedModel
**描述**: 插件版本的发布策略

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| strategy | models.CharField | 381 | - | 发布策略 | {"choices": "`constants.ReleaseStrategy.get_choices()`", "max_length": 32} |
| bkci_project | models.JSONField | 384 | 格式：['1111', '222222'] | 蓝盾项目ID | {"blank": true, "null": true} |
| organization | models.JSONField | 402 | - | 组织架构 | {"blank": true, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| release | models.ForeignKey | `PluginRelease` | release_strategies | `models.CASCADE` |


---


### ApprovalService

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**行号**: 430
**基类**: paasng.utils.models.UuidAuditedModel
**描述**: 审批服务信息

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| service_name | models.CharField | 433 | - | 审批服务名称 | {"max_length": 64, "unique": true} |
| service_id | models.IntegerField | 434 | 用于在 ITSM 上提申请单据 | 审批服务ID | {} |



---


### PluginConfig

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**行号**: 437
**基类**: paasng.utils.models.AuditedModel
**描述**: 插件配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| unique_key | models.CharField | 441 | - | 唯一标识 | {"max_length": 64} |
| row | models.JSONField | 442 | - | 配置内容(1行), 格式 {'column_key': 'value'} | {"default": "`dict`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plugin | models.ForeignKey | `PluginInstance` | configs | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('plugin', 'unique_key') |

---


### PluginVisibleRange

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**行号**: 448
**基类**: paasng.utils.models.AuditedModel
**描述**: 插件可见范围

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| bkci_project | models.JSONField | 454 | - | 蓝盾项目ID | {"default": "`list`"} |
| organization | models.JSONField | 455 | - | 组织架构 | {"blank": true, "null": true} |
| is_in_approval | models.BooleanField | 456 | - | 是否在审批中 | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plugin | models.OneToOneField | `PluginInstance` | visible_range | `models.CASCADE` |


---


### OperationRecord

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`
**行号**: 498
**基类**: paasng.utils.models.AuditedModel
**描述**: 插件操作记录

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| action | models.CharField | 510 | - | - | {"choices": "`constants.ActionTypes.get_choices()`", "max_length": 32} |
| specific | models.CharField | 511 | - | - | {"max_length": 255, "null": true} |
| subject | models.CharField | 512 | - | - | {"choices": "`constants.SubjectTypes.get_choices()`", "max_length": 32} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plugin | models.ForeignKey | `PluginInstance` | 不适用 | `models.CASCADE` |


---


### UserPrivateToken

**模块**: `apiserver.paasng.paasng.infras.accounts.models`
**行号**: 110
**基类**: models.Model
**描述**: Private token can be used to authenticate an user, these tokens usually have very long

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| token | models.CharField | 116 | - | - | {"max_length": 64, "unique": true} |
| expires_at | models.DateTimeField | 117 | - | - | {"blank": true, "null": true} |
| is_active | models.BooleanField | 118 | - | - | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| user | models.ForeignKey | `User` | 不适用 | `models.CASCADE` |


---


### UserProfile

**模块**: `apiserver.paasng.paasng.infras.accounts.models`
**行号**: 159
**基类**: paasng.utils.models.TimestampedModel
**描述**: Profile field for user

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| role | models.IntegerField | 163 | - | - | {"default": "`SiteRole.USER.value`"} |
| feature_flags | models.TextField | 164 | - | - | {"blank": true, "null": true} |



---


### Oauth2TokenHolder

**模块**: `apiserver.paasng.paasng.infras.accounts.models`
**行号**: 236
**基类**: paasng.utils.models.TimestampedModel
**描述**: OAuth2 Token for sourcectl

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| provider | models.CharField | 239 | - | - | {"max_length": 32} |
| token_type | models.CharField | 241 | - | - | {"max_length": 16} |
| expire_at | models.DateTimeField | 244 | - | - | {"blank": true, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| user | models.ForeignKey | `UserProfile` | token_holder | `models.CASCADE` |


---


### PrivateTokenHolder

**模块**: `apiserver.paasng.paasng.infras.accounts.models`
**行号**: 275
**基类**: paasng.utils.models.AuditedModel
**描述**: Private Token for sourcectl

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| provider | models.CharField | 278 | - | - | {"max_length": 32} |
| expire_at | models.DateTimeField | 280 | - | - | {"blank": true, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| user | models.ForeignKey | `UserProfile` | private_token_holder | `models.CASCADE` |


---


### AccountFeatureFlag

**模块**: `apiserver.paasng.paasng.infras.accounts.models`
**行号**: 320
**基类**: paasng.utils.models.TimestampedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| effect | models.BooleanField | 326 | - | - | {"default": true} |
| name | models.CharField | 327 | - | - | {"max_length": 64} |



---


### AuthenticatedAppAsUser

**模块**: `apiserver.paasng.paasng.infras.accounts.models`
**行号**: 336
**基类**: paasng.utils.models.TimestampedModel
**描述**: Store relationships which treat an authenticated(by API Gateway) app as an regular user,

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| bk_app_code | models.CharField | 341 | - | - | {"max_length": 64, "unique": true} |
| is_active | models.BooleanField | 342 | - | - | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| user | models.ForeignKey | `User` | 不适用 | `models.CASCADE` |


---


### BKMonitorSpace

**模块**: `apiserver.paasng.paasng.infras.bkmonitorv3.models`
**行号**: 25
**基类**: paasng.utils.models.UuidAuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| id | models.IntegerField | 38 | - | 蓝鲸监控空间 id | {} |
| space_type_id | models.CharField | 39 | - | 空间类型id | {"max_length": 48} |
| space_id | models.CharField | 40 | 同一空间类型下唯一 | 空间id | {"max_length": 48} |
| space_name | models.CharField | 41 | - | 空间名称 | {"max_length": 64} |
| space_uid | models.CharField | 42 | {space_type_id}__{space_id} | 蓝鲸监控空间 uid | {"max_length": 48} |
| extra_info | models.JSONField | 45 | 蓝鲸监控API-metadata_get_space_detail 的原始返回值 | - | {} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.OneToOneField | `Application` | bk_monitor_space | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('space_type_id', 'space_id') |

---


### ApplicationGradeManager

**模块**: `apiserver.paasng.paasng.infras.iam.members.models`
**行号**: 28
**基类**: paasng.utils.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| app_code | models.CharField | 35 | 应用代号 | - | {"max_length": 20} |
| grade_manager_id | models.IntegerField | 36 | 分级管理员 ID | - | {} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('app_code', 'grade_manager_id') |

---


### ApplicationUserGroup

**模块**: `apiserver.paasng.paasng.infras.iam.members.models`
**行号**: 45
**基类**: paasng.utils.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| app_code | models.CharField | 52 | 应用代号 | - | {"max_length": 20} |
| role | models.IntegerField | 53 | - | - | {"default": "`ApplicationRole.DEVELOPER.value`"} |
| user_group_id | models.IntegerField | 54 | 权限中心用户组 ID | - | {} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('app_code', 'role') |

---


### OAuth2Client

**模块**: `apiserver.paasng.paasng.infras.oauth2.models`
**行号**: 34
**基类**: paasng.utils.models.TimestampedModel
**描述**: OAuth2 体系中的基本单位：Client

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| client_id | models.CharField | 40 | - | 应用编码 | {"max_length": 20, "unique": true} |



---


### BkAppSecretInEnvVar

**模块**: `apiserver.paasng.paasng.infras.oauth2.models`
**行号**: 44
**基类**: paasng.utils.models.TimestampedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| bk_app_code | models.CharField | 49 | - | - | {"max_length": 20, "unique": true} |
| bk_app_secret_id | models.IntegerField | 50 | 不存储密钥的信息，仅存储密钥 ID | 应用密钥的 ID | {} |



---


### BaseOperation

**模块**: `apiserver.paasng.paasng.misc.audit.models`
**行号**: 31
**基类**: paasng.utils.models.UuidAuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| start_time | models.DateTimeField | 34 | - | 开始时间 | {"auto_now_add": true, "db_index": true} |
| end_time | models.DateTimeField | 35 | 仅需要后台执行的的操作才需要记录结束时间 | - | {"null": true} |
| access_type | models.IntegerField | 36 | - | 访问方式 | {"choices": "`AccessType.get_choices()`", "default": "`AccessType.WEB`"} |
| result_code | models.IntegerField | 39 | - | 操作结果 | {"choices": "`ResultCode.get_choices()`", "default": "`ResultCode.SUCCESS`"} |
| data_before | models.JSONField | 42 | - | 操作前的数据 | {"blank": true, "null": true} |
| data_after | models.JSONField | 43 | - | 操作后的数据 | {"blank": true, "null": true} |
| operation | models.CharField | 45 | - | 操作类型 | {"choices": "`OperationEnum.get_choices()`", "max_length": 32} |
| target | models.CharField | 46 | - | 操作对象 | {"choices": "`OperationTarget.get_choices()`", "max_length": 32} |
| attribute | models.CharField | 47 | 如增强服务的属性可以为：mysql、bkrepo | 对象属性 | {"blank": true, "max_length": 32, "null": true} |
| module_name | models.CharField | 56 | - | 模块名，非必填 | {"blank": true, "max_length": 32, "null": true} |
| environment | models.CharField | 57 | - | 环境，非必填 | {"blank": true, "choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### AdminOperationRecord

**模块**: `apiserver.paasng.paasng.misc.audit.models`
**行号**: 135
**基类**: apiserver.paasng.paasng.misc.audit.models.BaseOperation
**描述**: 后台管理操作记录，用于记录平台管理员在 Admin 系统上的操作

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| app_code | models.CharField | 138 | - | 应用ID, 非必填 | {"blank": true, "max_length": 32, "null": true} |
| start_time | models.DateTimeField | 34 | - | 开始时间 | {"auto_now_add": true, "db_index": true} |
| end_time | models.DateTimeField | 35 | 仅需要后台执行的的操作才需要记录结束时间 | - | {"null": true} |
| access_type | models.IntegerField | 36 | - | 访问方式 | {"choices": "`AccessType.get_choices()`", "default": "`AccessType.WEB`"} |
| result_code | models.IntegerField | 39 | - | 操作结果 | {"choices": "`ResultCode.get_choices()`", "default": "`ResultCode.SUCCESS`"} |
| data_before | models.JSONField | 42 | - | 操作前的数据 | {"blank": true, "null": true} |
| data_after | models.JSONField | 43 | - | 操作后的数据 | {"blank": true, "null": true} |
| operation | models.CharField | 45 | - | 操作类型 | {"choices": "`OperationEnum.get_choices()`", "max_length": 32} |
| target | models.CharField | 46 | - | 操作对象 | {"choices": "`OperationTarget.get_choices()`", "max_length": 32} |
| attribute | models.CharField | 47 | 如增强服务的属性可以为：mysql、bkrepo | 对象属性 | {"blank": true, "max_length": 32, "null": true} |
| module_name | models.CharField | 56 | - | 模块名，非必填 | {"blank": true, "max_length": 32, "null": true} |
| environment | models.CharField | 57 | - | 环境，非必填 | {"blank": true, "choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": true} |



---


### AppOperationRecord

**模块**: `apiserver.paasng.paasng.misc.audit.models`
**行号**: 141
**基类**: apiserver.paasng.paasng.misc.audit.models.BaseOperation
**描述**: 应用操作记录，用于记录应用开发者的操作，需要同步记录应用的权限数据，并可以选择是否将数据上报到审计中心

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| app_code | models.CharField | 145 | - | 应用ID, 必填 | {"max_length": 32} |
| action_id | models.CharField | 148 | action_id 为空则不会将数据上报到审计中心 | - | {"blank": true, "choices": "`AppAction.get_choices()`", "max_length": 32, "null": true} |
| resource_type_id | models.CharField | 155 | 开发者中心注册的资源都为蓝鲸应用 | - | {"choices": "`ResourceType.get_choices()`", "default": "`ResourceType.Application`", "max_length": 32} |
| start_time | models.DateTimeField | 34 | - | 开始时间 | {"auto_now_add": true, "db_index": true} |
| end_time | models.DateTimeField | 35 | 仅需要后台执行的的操作才需要记录结束时间 | - | {"null": true} |
| access_type | models.IntegerField | 36 | - | 访问方式 | {"choices": "`AccessType.get_choices()`", "default": "`AccessType.WEB`"} |
| result_code | models.IntegerField | 39 | - | 操作结果 | {"choices": "`ResultCode.get_choices()`", "default": "`ResultCode.SUCCESS`"} |
| data_before | models.JSONField | 42 | - | 操作前的数据 | {"blank": true, "null": true} |
| data_after | models.JSONField | 43 | - | 操作后的数据 | {"blank": true, "null": true} |
| operation | models.CharField | 45 | - | 操作类型 | {"choices": "`OperationEnum.get_choices()`", "max_length": 32} |
| target | models.CharField | 46 | - | 操作对象 | {"choices": "`OperationTarget.get_choices()`", "max_length": 32} |
| attribute | models.CharField | 47 | 如增强服务的属性可以为：mysql、bkrepo | 对象属性 | {"blank": true, "max_length": 32, "null": true} |
| module_name | models.CharField | 56 | - | 模块名，非必填 | {"blank": true, "max_length": 32, "null": true} |
| environment | models.CharField | 57 | - | 环境，非必填 | {"blank": true, "choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": true} |



---


### AppLatestOperationRecord

**模块**: `apiserver.paasng.paasng.misc.audit.models`
**行号**: 167
**基类**: models.Model
**描述**: 应用最近操作的映射表，可方便快速查询应用的最近操作者，并按最近操作时间进行排序等操作

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| latest_operated_at | models.DateTimeField | 176 | - | - | {"db_index": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.OneToOneField | `Application` | latest_op_record | `models.CASCADE` |
| operation | models.OneToOneField | `AppOperationRecord` | 不适用 | `models.CASCADE` |


---


### AppAlertRule

**模块**: `apiserver.paasng.paasng.misc.monitoring.monitor.models`
**行号**: 44
**基类**: paasng.utils.models.AuditedModel
**描述**: 记录 app 初始的告警规则配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| alert_code | models.CharField | 47 | alert rule code e.g. high_cpu_usage | - | {"max_length": 64} |
| display_name | models.CharField | 48 | - | - | {"max_length": 512} |
| enabled | models.BooleanField | 49 | - | - | {"default": true} |
| threshold_expr | models.CharField | 50 | - | - | {"max_length": 64} |
| receivers | models.JSONField | 51 | - | - | {"default": "`list`"} |
| environment | models.CharField | 55 | - | 部署环境 | {"max_length": 16} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | applications.Application | alert_rules | `models.CASCADE` |
| module | models.ForeignKey | modules.Module | alert_rules | `models.CASCADE` |


---


### AppDashboardTemplate

**模块**: `apiserver.paasng.paasng.misc.monitoring.monitor.models`
**行号**: 65
**基类**: paasng.utils.models.AuditedModel
**描述**: 仪表盘模板，只需要记录名称和版本号，模板的内容在蓝鲸监控侧维护

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 68 | 与蓝鲸监控约定的仪表盘名称，如：bksaas/framework-python，需要提前将仪表盘的 JSON 文件内置到监控的代码目录中 | - | {"max_length": 64, "unique": true} |
| display_name | models.CharField | 73 | 仪表盘展示名称，如：Python 开发框架内置仪表盘 | - | {"max_length": 512} |
| version | models.CharField | 74 | - | - | {"max_length": 32} |
| language | models.CharField | 75 | - | 仪表盘所属语言 | {"max_length": 32} |
| is_plugin_template | models.BooleanField | 76 | - | - | {"default": false} |



---


### AppDashboard

**模块**: `apiserver.paasng.paasng.misc.monitoring.monitor.models`
**行号**: 79
**基类**: paasng.utils.models.AuditedModel
**描述**: 记录 APP 初始化的仪表盘信息

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 85 | 仪表盘名称，如：bksaas/framework-python | - | {"max_length": 64} |
| display_name | models.CharField | 86 | 仪表盘展示名称，如：Python 开发框架内置仪表盘 | - | {"max_length": 512} |
| template_version | models.CharField | 87 | 模板版本更新时，可以根据该字段作为批量刷新仪表盘 | - | {"max_length": 32} |
| language | models.CharField | 88 | - | 仪表盘所属语言 | {"max_length": 32} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | applications.Application | dashboards | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('application', 'name') |

---


### Operation

**模块**: `apiserver.paasng.paasng.misc.operations.models`
**行号**: 41
**基类**: models.Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| region | models.CharField | 42 | 部署区域 | - | {"max_length": 32} |
| created | models.DateTimeField | 43 | - | - | {"auto_now_add": true, "db_index": true} |
| type | models.SmallIntegerField | 48 | 操作类型 | - | {"db_index": true} |
| is_hidden | models.BooleanField | 49 | 隐藏起来 | - | {"default": false} |
| source_object_id | models.CharField | 50 | 事件来源对象ID，具体指向需要根据操作类型解析 | - | {"blank": true, "default": "", "max_length": 32, "null": true} |
| module_name | models.CharField | 54 | - | 关联 Module | {"max_length": 20, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |


---


### ApplicationLatestOp

**模块**: `apiserver.paasng.paasng.misc.operations.models`
**行号**: 67
**基类**: models.Model
**描述**: A mapper table which saves application's latest operation

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| operation_type | models.SmallIntegerField | 73 | 操作类型 | - | {} |
| latest_operated_at | models.DateTimeField | 75 | - | - | {"db_index": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.OneToOneField | `Application` | latest_op | `models.CASCADE` |
| operation | models.OneToOneField | `Operation` | 不适用 | `models.CASCADE` |


---


### Application

**模块**: `apiserver.paasng.paasng.platform.applications.models`
**行号**: 280
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: 蓝鲸应用

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| id | models.UUIDField | 283 | - | - | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |
| code | models.CharField | 284 | - | 应用代号 | {"max_length": 20, "unique": true} |
| name | models.CharField | 285 | - | 应用名称 | {"max_length": 20, "unique": true} |
| name_en | models.CharField | 286 | 目前仅用于 S-Mart 应用 | 应用名称(英文) | {"max_length": 20} |
| type | models.CharField | 288 | 与应用部署方式相关的类型信息 | 应用类型 | {"db_index": true, "default": "`ApplicationType.DEFAULT.value`", "max_length": 16} |
| is_smart_app | models.BooleanField | 295 | - | 是否为 S-Mart 应用 | {"default": false} |
| is_scene_app | models.BooleanField | 296 | - | 是否为场景 SaaS 应用 | {"default": false} |
| is_plugin_app | models.BooleanField | 297 | 蓝鲸应用插件：供标准运维、ITSM 等 SaaS 使用，有特殊逻辑 | 是否为插件应用 | {"default": false} |
| is_ai_agent_app | models.BooleanField | 302 | - | 是否为 AI Agent 插件应用 | {"default": false} |
| language | models.CharField | 306 | - | 编程语言 | {"max_length": 32} |
| is_active | models.BooleanField | 309 | - | 是否活跃 | {"default": true} |
| is_deleted | models.BooleanField | 310 | - | - | {"default": false} |
| last_deployed_date | models.DateTimeField | 311 | - | 最近部署时间 | {"null": true} |



---


### ApplicationMembership

**模块**: `apiserver.paasng.paasng.platform.applications.models`
**行号**: 442
**基类**: paasng.utils.models.TimestampedModel
**描述**: [deprecated] 切换为权限中心用户组存储用户信息

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| role | models.IntegerField | 450 | - | - | {"default": "`ApplicationRole.DEVELOPER.value`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('user', 'application', 'role') |

---


### ApplicationEnvironment

**模块**: `apiserver.paasng.paasng.platform.applications.models`
**行号**: 461
**基类**: paasng.utils.models.TimestampedModel
**描述**: 记录蓝鲸应用在不同部署环境下对应的 Engine App

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| environment | models.CharField | 467 | - | 部署环境 | {"max_length": 16} |
| is_offlined | models.BooleanField | 468 | 是否已经下线，仅成功下线后变为False | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | envs | `models.CASCADE` |
| module | models.ForeignKey | modules.Module | envs | `models.CASCADE` |
| engine_app | models.OneToOneField | engine.EngineApp | env | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module', 'environment') |

---


### ApplicationFeatureFlag

**模块**: `apiserver.paasng.paasng.platform.applications.models`
**行号**: 581
**基类**: paasng.utils.models.TimestampedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| effect | models.BooleanField | 587 | - | - | {"default": true} |
| name | models.CharField | 588 | - | - | {"max_length": 30} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | feature_flag | `models.CASCADE` |


---


### UserMarkedApplication

**模块**: `apiserver.paasng.paasng.platform.applications.models`
**行号**: 593
**基类**: paasng.utils.models.OwnerTimestampedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('application', 'owner') |

---


### ApplicationDeploymentModuleOrder

**模块**: `apiserver.paasng.paasng.platform.applications.models`
**行号**: 608
**基类**: models.Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| order | models.IntegerField | 610 | - | 顺序 | {} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.OneToOneField | `Module` | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| verbose_name | 模块顺序 |

---


### ModuleProcessSpec

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`
**行号**: 69
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: 模块维度的进程定义, 表示模块当前所定义的进程, 该模型只通过 API 变更

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 77 | - | - | {"max_length": 32} |
| proc_command | models.TextField | 79 | 进程启动命令(包含完整命令和参数的字符串), 只能与 command/args 二选一 | - | {"null": true} |
| port | models.IntegerField | 84 | [deprecated] 容器端口 | - | {"null": true} |
| target_replicas | models.IntegerField | 88 | - | - | {"default": 1} |
| plan_name | models.CharField | 89 | 仅存储方案名称 | - | {"max_length": 32} |
| autoscaling | models.BooleanField | 90 | - | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | modules.Module | process_specs | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module', 'name') |
| ordering | ['id'] |

---


### ProcessSpecEnvOverlay

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`
**行号**: 175
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: 进程定义中允许按环境覆盖的配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| environment_name | models.CharField | 181 | - | `_('环境名称')` | {"choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": false} |
| target_replicas | models.IntegerField | 185 | - | - | {"null": true} |
| plan_name | models.CharField | 186 | 仅存储方案名称 | - | {"blank": true, "max_length": 32, "null": true} |
| autoscaling | models.BooleanField | 187 | - | - | {"null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| proc_spec | models.ForeignKey | `ModuleProcessSpec` | env_overlays | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('proc_spec', 'environment_name') |

---


### ProcessServicesFlag

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`
**行号**: 196
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: ProcessServicesFlag 主要用途是标记是否隐式需要 process services 配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| implicit_needed | models.BooleanField | 201 | - | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app_environment | models.OneToOneField | `ApplicationEnvironment` | 不适用 | `models.CASCADE` |


---


### ModuleDeployHook

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`
**行号**: 262
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: 钩子命令

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| type | models.CharField | 268 | 钩子类型 | - | {"choices": "`DeployHookType.get_choices()`", "max_length": 20} |
| proc_command | models.TextField | 270 | 进程启动命令(包含完整命令和参数的字符串), 只能与 command/args 二选一 | - | {"null": true} |
| enabled | models.BooleanField | 275 | 是否已开启 | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | modules.Module | deploy_hooks | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module', 'type') |

---


### SvcDiscConfig

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`
**行号**: 304
**基类**: paas_wl.utils.models.AuditedModel
**描述**: 服务发现配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |


---


### DomainResolution

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`
**行号**: 312
**基类**: paas_wl.utils.models.AuditedModel
**描述**: 域名解析配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |


---


### ObservabilityConfig

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`
**行号**: 354
**基类**: paas_wl.utils.models.TimestampedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.OneToOneField | modules.Module | observability | `models.CASCADE` |


---


### BkAppManagedFields

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`
**行号**: 387
**基类**: paas_wl.utils.models.TimestampedModel
**描述**: This model stores the management status of the fields of a module's bkapp model, it's

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| manager | models.CharField | 395 | 管理者类型 | - | {"max_length": 20} |
| fields | models.JSONField | 396 | 所管理的字段 | - | {"default": []} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | modules.Module | managed_fields | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module', 'manager') |

---


### ApplicationDescription

**模块**: `apiserver.paasng.paasng.platform.declarative.models`
**行号**: 40
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: Application description object

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| code | models.CharField | 46 | - | ID of application | {"db_index": true, "max_length": 20} |
| is_creation | models.BooleanField | 52 | - | whether current description creates an application | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | declarative_config | `models.CASCADE` |


---


### DeploymentDescription

**模块**: `apiserver.paasng.paasng.platform.declarative.models`
**行号**: 62
**基类**: paasng.utils.models.TimestampedModel
**描述**: Config objects which describes deployment objects.

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| deployment | models.OneToOneField | `Deployment` | declarative_config | `models.CASCADE` |


---


### OperationVersionBase

**模块**: `apiserver.paasng.paasng.platform.engine.models.base`
**行号**: 35
**基类**: paasng.utils.models.TimestampedModel
**描述**: 带操作版本信息的BaseModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| id | models.UUIDField | 38 | - | - | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |
| source_type | models.CharField | 41 | - | 源码托管类型 | {"max_length": 16, "null": true} |
| source_location | models.CharField | 42 | - | - | {"max_length": 2048} |
| source_version_type | models.CharField | 43 | - | - | {"max_length": 64} |
| source_version_name | models.CharField | 44 | - | - | {"max_length": 64} |
| source_revision | models.CharField | 45 | - | - | {"max_length": 128, "null": true} |
| source_comment | models.TextField | 46 | - | - | {} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### EngineApp

**模块**: `apiserver.paasng.paasng.platform.engine.models.base`
**行号**: 52
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: 蓝鲸应用引擎应用

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| id | models.UUIDField | 55 | - | - | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |
| name | models.CharField | 56 | - | - | {"max_length": 64, "unique": true} |
| region | models.CharField | 58 | - | - | {"max_length": 32} |
| is_active | models.BooleanField | 59 | - | 是否活跃 | {"default": true} |



---


### ConfigVar

**模块**: `apiserver.paasng.paasng.platform.engine.models.config_var`
**行号**: 68
**基类**: paasng.utils.models.TimestampedModel
**描述**: Config vars for application

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| is_global | models.BooleanField | 73 | - | - | {"default": false} |
| key | models.CharField | 80 | - | - | {"max_length": 128, "null": false} |
| value | models.TextField | 81 | - | - | {"null": false} |
| description | models.CharField | 82 | - | - | {"max_length": 200, "null": true} |
| is_builtin | models.BooleanField | 83 | - | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | modules.Module | 不适用 | `models.CASCADE` |
| environment | models.ForeignKey | applications.ApplicationEnvironment | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module', 'is_global', 'environment', 'key') |

---


### BuiltinConfigVar

**模块**: `apiserver.paasng.paasng.platform.engine.models.config_var`
**行号**: 154
**基类**: paasng.utils.models.AuditedModel
**描述**: Default config vars for global, can be added or edited in admin42.

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| key | models.CharField | 157 | - | 环境变量名 | {"max_length": 128, "null": false, "unique": true} |
| value | models.TextField | 158 | - | 环境变量值 | {"max_length": 512, "null": false} |
| description | models.CharField | 159 | - | 描述 | {"max_length": 512, "null": false} |



---


### MobileConfig

**模块**: `apiserver.paasng.paasng.platform.engine.models.mobile_config`
**行号**: 27
**基类**: paasng.utils.models.TimestampedModel
**描述**: Mobile config switcher for application

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| is_enabled | models.BooleanField | 36 | - | - | {"default": false} |
| lb_plan | models.CharField | 37 | which one-level load balancer plan the domain use | - | {"choices": "`LBPlans.get_choices()`", "default": "`LBPlans.LBDefaultPlan.value`", "max_length": 64} |
| access_url | models.URLField | 44 | - | - | {"blank": true, "default": "", "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| environment | models.OneToOneField | applications.ApplicationEnvironment | mobile_config | `models.CASCADE` |


---


### ModuleEnvironmentOperations

**模块**: `apiserver.paasng.paasng.platform.engine.models.operations`
**行号**: 39
**基类**: paasng.utils.models.TimestampedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| id | models.UUIDField | 40 | - | - | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |
| operation_type | models.CharField | 48 | - | - | {"choices": "`OperationTypes.get_choices()`", "max_length": 32} |
| object_uid | models.UUIDField | 49 | - | - | {"default": "`uuid.uuid4`", "editable": false} |
| status | models.CharField | 50 | - | - | {"choices": "`JobStatus.get_choices()`", "default": "`JobStatus.PENDING.value`", "max_length": 16} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | applications.Application | module_operations | `models.CASCADE` |
| app_environment | models.ForeignKey | applications.ApplicationEnvironment | module_operations | `models.CASCADE` |


---


### DeployPhase

**模块**: `apiserver.paasng.paasng.platform.engine.models.phases`
**行号**: 52
**基类**: paasng.utils.models.UuidAuditedModel, paasng.platform.engine.models.MarkStatusMixin
**描述**: 部署阶段

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| type | models.CharField | 55 | - | - | {"choices": "`DeployPhaseTypes.get_choices()`", "max_length": 32} |
| status | models.CharField | 58 | - | - | {"choices": "`JobStatus.get_choices()`", "max_length": 32, "null": true} |
| start_time | models.DateTimeField | 59 | - | - | {"null": true} |
| complete_time | models.DateTimeField | 60 | - | - | {"null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| engine_app | models.ForeignKey | `EngineApp` | 不适用 | `models.CASCADE` |
| deployment | models.ForeignKey | `Deployment` | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ['created'] |

---


### PresetEnvVariable

**模块**: `apiserver.paasng.paasng.platform.engine.models.preset_envvars`
**行号**: 27
**基类**: paas_wl.utils.models.AuditedModel
**描述**: 应用描述文件中预定义的环境变量

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| environment_name | models.CharField | 31 | - | `_('环境名称')` | {"choices": "`ConfigVarEnvName.get_choices()`", "max_length": 16} |
| key | models.CharField | 34 | - | - | {"max_length": 128, "null": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | `Module` | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module', 'environment_name', 'key') |

---


### DeployStepMeta

**模块**: `apiserver.paasng.paasng.platform.engine.models.steps`
**行号**: 52
**基类**: paasng.utils.models.AuditedModel
**描述**: 部署步骤元信息

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| phase | models.CharField | 55 | - | `_('关联阶段')` | {"choices": "`DeployPhaseTypes.get_choices()`", "max_length": 16} |
| name | models.CharField | 56 | - | - | {"db_index": true, "max_length": 32} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ['id'] |

---


### StepMetaSet

**模块**: `apiserver.paasng.paasng.platform.engine.models.steps`
**行号**: 79
**基类**: paasng.utils.models.AuditedModel
**描述**: 部署步骤元信息集

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 85 | - | - | {"max_length": 32} |
| is_default | models.BooleanField | 87 | - | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| metas | models.ManyToManyField | `DeployStepMeta` | 不适用 | 不适用 |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ['id'] |

---


### DeployStep

**模块**: `apiserver.paasng.paasng.platform.engine.models.steps`
**行号**: 132
**基类**: paasng.utils.models.UuidAuditedModel, paasng.platform.engine.models.base.MarkStatusMixin
**描述**: 部署步骤

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 135 | - | - | {"db_index": true, "max_length": 32} |
| skipped | models.BooleanField | 138 | - | - | {"default": false} |
| status | models.CharField | 139 | - | - | {"choices": "`JobStatus.get_choices()`", "max_length": 32, "null": true} |
| start_time | models.DateTimeField | 140 | - | - | {"null": true} |
| complete_time | models.DateTimeField | 141 | - | - | {"null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| phase | models.ForeignKey | `DeployPhase` | steps | `models.CASCADE` |
| meta | models.ForeignKey | `DeployStepMeta` | instances | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ['created'] |

---


### EnvRoleProtection

**模块**: `apiserver.paasng.paasng.platform.environments.models`
**行号**: 26
**基类**: paasng.utils.models.TimestampedModel
**描述**: 模块环境角色保护

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| allowed_role | models.IntegerField | 29 | - | - | {"choices": "`ApplicationRole.get_django_choices()`"} |
| operation | models.CharField | 31 | - | - | {"choices": "`EnvRoleOperation.get_choices()`", "max_length": 64} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module_env | models.ForeignKey | `ModuleEnvironment` | role_protections | `models.CASCADE` |


---


### AppOperationReportCollectionTask

**模块**: `apiserver.paasng.paasng.platform.evaluation.models`
**行号**: 25
**基类**: models.Model
**描述**: 应用运营报告采集任务

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| start_at | models.DateTimeField | 28 | - | 任务开始时间 | {"auto_now_add": true} |
| end_at | models.DateTimeField | 29 | - | 任务结束时间 | {"null": true} |
| total_count | models.IntegerField | 30 | - | 应用总数 | {"default": 0} |
| succeed_count | models.IntegerField | 31 | - | 采集成功数 | {"default": 0} |
| failed_count | models.IntegerField | 32 | - | 采集失败数 | {"default": 0} |
| failed_app_codes | models.JSONField | 33 | - | 采集失败应用 Code 列表 | {"default": "`list`"} |
| status | models.CharField | 34 | - | 任务状态 | {"choices": "`BatchTaskStatus.get_choices()`", "default": "`BatchTaskStatus.RUNNING`", "max_length": 32} |



---


### AppOperationReport

**模块**: `apiserver.paasng.paasng.platform.evaluation.models`
**行号**: 42
**基类**: models.Model
**描述**: 应用运营报告（含资源使用，用户活跃，运维操作等）

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| cpu_requests | models.IntegerField | 47 | - | CPU 请求 | {"default": 0} |
| mem_requests | models.IntegerField | 48 | - | 内存请求 | {"default": 0} |
| cpu_limits | models.IntegerField | 49 | - | CPU 限制 | {"default": 0} |
| mem_limits | models.IntegerField | 50 | - | 内存限制 | {"default": 0} |
| cpu_usage_avg | models.FloatField | 51 | - | CPU 平均使用率 | {"default": 0} |
| mem_usage_avg | models.FloatField | 52 | - | 内存平均使用率 | {"default": 0} |
| res_summary | models.JSONField | 53 | - | 资源使用详情汇总 | {"default": "`dict`"} |
| pv | models.BigIntegerField | 55 | - | 近 30 天页面访问量 | {"default": 0} |
| uv | models.BigIntegerField | 56 | - | 近 30 天访问用户数 | {"default": 0} |
| visit_summary | models.JSONField | 57 | - | 用户访问详情汇总 | {"default": "`dict`"} |
| latest_deployed_at | models.DateTimeField | 59 | - | 最新部署时间 | {"null": true} |
| latest_deployer | models.CharField | 60 | - | 最新部署人 | {"max_length": 128, "null": true} |
| latest_operated_at | models.DateTimeField | 61 | - | 最新操作时间 | {"null": true} |
| latest_operator | models.CharField | 62 | - | 最新操作人 | {"max_length": 128, "null": true} |
| latest_operation | models.CharField | 63 | - | 最新操作内容 | {"max_length": 128, "null": true} |
| deploy_summary | models.JSONField | 64 | - | 部署详情汇总 | {"default": "`dict`"} |
| administrators | models.JSONField | 66 | - | 应用管理员 | {"default": "`list`"} |
| developers | models.JSONField | 67 | - | 应用开发者 | {"default": "`list`"} |
| issue_type | models.CharField | 69 | - | 问题类型 | {"default": "`OperationIssueType.NONE`", "max_length": 32} |
| evaluate_result | models.JSONField | 70 | - | 评估结果 | {"default": "`dict`"} |
| collected_at | models.DateTimeField | 71 | - | 采集时间 | {} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.OneToOneField | `Application` | 不适用 | `models.CASCADE` |


---


### AppOperationEmailNotificationTask

**模块**: `apiserver.paasng.paasng.platform.evaluation.models`
**行号**: 74
**基类**: models.Model
**描述**: 应用运营报告邮件通知任务

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| start_at | models.DateTimeField | 77 | - | 任务开始时间 | {"auto_now_add": true} |
| end_at | models.DateTimeField | 78 | - | 任务结束时间 | {"null": true} |
| total_count | models.IntegerField | 79 | - | 应用总数 | {"default": 0} |
| succeed_count | models.IntegerField | 80 | - | 采集成功数 | {"default": 0} |
| failed_count | models.IntegerField | 81 | - | 采集失败数 | {"default": 0} |
| failed_usernames | models.JSONField | 82 | - | 通知失败的应用数量 | {"default": "`list`"} |
| notification_type | models.CharField | 83 | - | 通知类型 | {"max_length": 64} |
| status | models.CharField | 84 | - | 任务状态 | {"choices": "`BatchTaskStatus.get_choices()`", "default": "`BatchTaskStatus.RUNNING`", "max_length": 32} |



---


### IdleAppNotificationMuteRule

**模块**: `apiserver.paasng.paasng.platform.evaluation.models`
**行号**: 92
**基类**: paasng.utils.models.AuditedModel
**描述**: 闲置应用通知屏蔽规则

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| app_code | models.CharField | 96 | - | - | {"max_length": 32} |
| module_name | models.CharField | 97 | - | - | {"max_length": 32} |
| environment | models.CharField | 98 | - | - | {"max_length": 32} |
| expired_at | models.DateTimeField | 99 | - | - | {} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('user', 'app_code', 'module_name', 'environment') |

---


### MigrationProcess

**模块**: `apiserver.paasng.paasng.platform.mgrlegacy.models`
**行号**: 71
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: An migration process

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| legacy_app_id | models.IntegerField | 74 | - | - | {} |
| status | models.IntegerField | 77 | - | - | {"choices": "`MigrationStatus.get_choices()`", "default": "`MigrationStatus.DEFAULT.value`"} |
| failed_date | models.DateTimeField | 79 | - | - | {"null": true} |
| migrated_date | models.DateTimeField | 80 | - | - | {"null": true} |
| confirmed_date | models.DateTimeField | 81 | - | - | {"null": true} |
| rollbacked_date | models.DateTimeField | 82 | - | - | {"null": true} |
| legacy_app_logo | models.CharField | 90 | - | - | {"default": null, "max_length": 500, "null": true} |
| legacy_app_is_already_online | models.BooleanField | 91 | - | - | {"default": true} |
| legacy_app_state | models.IntegerField | 92 | - | - | {"default": 4} |
| legacy_app_has_all_deployed | models.BooleanField | 93 | - | - | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |


---


### CNativeMigrationProcess

**模块**: `apiserver.paasng.paasng.platform.mgrlegacy.models`
**行号**: 231
**基类**: paasng.utils.models.OwnerTimestampedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| status | models.CharField | 233 | - | - | {"choices": "`CNativeMigrationStatus.get_choices()`", "default": "`CNativeMigrationStatus.DEFAULT.value`", "max_length": 20} |
| created_at | models.DateTimeField | 240 | 操作记录的创建时间 | - | {"auto_now_add": true} |
| confirm_at | models.DateTimeField | 241 | 用户确认的时间 | - | {"null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| get_latest_by | created_at |
| ordering | ['created_at'] |

---


### WlAppBackupRel

**模块**: `apiserver.paasng.paasng.platform.mgrlegacy.models`
**行号**: 323
**基类**: paasng.utils.models.TimestampedModel
**描述**: WlApp 的备份关系表

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| original_id | models.UUIDField | 327 | - | 原 WlApp uuid | {} |
| backup_id | models.UUIDField | 328 | - | 对应备份的 WlApp uuid | {} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app_environment | models.OneToOneField | `ApplicationEnvironment` | 不适用 | `models.CASCADE` |


---


### BuildConfig

**模块**: `apiserver.paasng.paasng.platform.modules.models.build_cfg`
**行号**: 52
**基类**: paasng.utils.models.UuidAuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| build_method | models.CharField | 56 | - | `_('构建方式')` | {"default": "`RuntimeType.BUILDPACK`", "max_length": 32} |
| dockerfile_path | models.CharField | 68 | `_('Dockerfile文件路径, 必须保证 Dockerfile 在构建目录下, 填写时无需包含构建目录')` | - | {"max_length": 512, "null": true} |
| image_repository | models.TextField | 77 | - | `_('镜像仓库')` | {"null": true} |
| image_credential_name | models.CharField | 78 | - | `_('镜像凭证名称')` | {"max_length": 32, "null": true} |
| use_bk_ci_pipeline | models.BooleanField | 84 | 是否使用蓝盾流水线构建 | - | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.OneToOneField | modules.Module | build_config | `models.CASCADE` |
| buildpacks | models.ManyToManyField | modules.AppBuildPack | related_build_configs | 不适用 |
| buildpack_builder | models.ForeignKey | modules.AppSlugBuilder | 不适用 | `models.SET_NULL` |
| buildpack_runner | models.ForeignKey | modules.AppSlugRunner | 不适用 | `models.SET_NULL` |


---


### DeployConfig

**模块**: `apiserver.paasng.paasng.platform.modules.models.deploy_config`
**行号**: 112
**基类**: paasng.utils.models.UuidAuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.OneToOneField | modules.Module | deploy_config | `models.CASCADE` |


---


### Module

**模块**: `apiserver.paasng.paasng.platform.modules.models.module`
**行号**: 34
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: Module for Application

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| id | models.UUIDField | 40 | - | - | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |
| name | models.CharField | 43 | - | 模块名称 | {"max_length": 20} |
| is_default | models.BooleanField | 44 | - | 是否为默认模块 | {"default": false} |
| language | models.CharField | 46 | - | 编程语言 | {"max_length": 32} |
| source_init_template | models.CharField | 47 | - | 初始化模板类型 | {"max_length": 32} |
| source_origin | models.SmallIntegerField | 48 | - | 源码来源 | {"null": true} |
| source_type | models.CharField | 49 | - | 源码托管类型 | {"max_length": 16, "null": true} |
| source_repo_id | models.IntegerField | 50 | - | 源码 ID | {"null": true} |
| exposed_url_type | models.IntegerField | 51 | - | 访问 URL 版本 | {"null": true} |
| user_preferred_root_domain | models.CharField | 52 | - | 用户偏好的根域名 | {"max_length": 255, "null": true} |
| last_deployed_date | models.DateTimeField | 54 | - | 最近部署时间 | {"null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | applications.Application | modules | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('application', 'name') |

---


### AppBuildPack

**模块**: `apiserver.paasng.paasng.platform.modules.models.runtime`
**行号**: 73
**基类**: paasng.utils.models.TimestampedModel
**描述**: buildpack 配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| language | models.CharField | 76 | - | 编程语言 | {"max_length": 32} |
| type | models.CharField | 77 | - | 引用类型 | {"choices": "`BuildPackType.get_choices()`", "max_length": 32} |
| name | models.CharField | 78 | - | 名称 | {"max_length": 64} |
| address | models.CharField | 82 | - | 地址 | {"max_length": 2048} |
| version | models.CharField | 84 | - | 版本 | {"max_length": 32} |
| is_hidden | models.BooleanField | 87 | - | 是否隐藏 | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| modules | models.ManyToManyField | modules.Module | buildpacks | 不适用 |


---


### AppImage

**模块**: `apiserver.paasng.paasng.platform.modules.models.runtime`
**行号**: 229
**基类**: paasng.utils.models.TimestampedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 231 | - | 名称 | {"max_length": 64, "unique": true} |
| type | models.CharField | 235 | - | 镜像类型 | {"choices": "`AppImageType.get_choices()`", "max_length": 32} |
| image | models.CharField | 237 | - | 镜像 | {"max_length": 256} |
| tag | models.CharField | 238 | - | 标签 | {"max_length": 32} |
| is_hidden | models.BooleanField | 240 | - | 是否隐藏 | {"default": false} |
| is_default | models.BooleanField | 241 | - | 是否为默认运行时 | {"default": false, "null": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### AppSlugRunner

**模块**: `apiserver.paasng.paasng.platform.modules.models.runtime`
**行号**: 273
**基类**: apiserver.paasng.paasng.platform.modules.models.runtime.AppImage
**描述**: 应用运行环境

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 231 | - | 名称 | {"max_length": 64, "unique": true} |
| type | models.CharField | 235 | - | 镜像类型 | {"choices": "`AppImageType.get_choices()`", "max_length": 32} |
| image | models.CharField | 237 | - | 镜像 | {"max_length": 256} |
| tag | models.CharField | 238 | - | 标签 | {"max_length": 32} |
| is_hidden | models.BooleanField | 240 | - | 是否隐藏 | {"default": false} |
| is_default | models.BooleanField | 241 | - | 是否为默认运行时 | {"default": false, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| modules | models.ManyToManyField | modules.Module | slugrunners | 不适用 |


---


### AppSlugBuilder

**模块**: `apiserver.paasng.paasng.platform.modules.models.runtime`
**行号**: 282
**基类**: apiserver.paasng.paasng.platform.modules.models.runtime.AppImage
**描述**: 应用构建环境

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 231 | - | 名称 | {"max_length": 64, "unique": true} |
| type | models.CharField | 235 | - | 镜像类型 | {"choices": "`AppImageType.get_choices()`", "max_length": 32} |
| image | models.CharField | 237 | - | 镜像 | {"max_length": 256} |
| tag | models.CharField | 238 | - | 标签 | {"max_length": 32} |
| is_hidden | models.BooleanField | 240 | - | 是否隐藏 | {"default": false} |
| is_default | models.BooleanField | 241 | - | 是否为默认运行时 | {"default": false, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| buildpacks | models.ManyToManyField | `AppBuildPack` | slugbuilders | 不适用 |
| modules | models.ManyToManyField | modules.Module | slugbuilders | 不适用 |
| step_meta_set | models.ForeignKey | engine.StepMetaSet | slugbuilders | `models.SET_NULL` |


---


### SvnRepository

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`
**行号**: 103
**基类**: paasng.utils.models.OwnerTimestampedModel, apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin
**描述**: 基于 Svn 的软件存储库

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| server_name | models.CharField | 106 | - | SVN 服务名称 | {"max_length": 32} |
| repo_url | models.CharField | 107 | - | 项目地址 | {"max_length": 2048} |
| source_dir | models.CharField | 108 | - | 源码目录 | {"max_length": 2048, "null": true} |



---


### SvnAccount

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`
**行号**: 182
**基类**: paasng.utils.models.TimestampedModel
**描述**: svn account for developer

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| account | models.CharField | 185 | 目前仅支持固定格式 | - | {"max_length": 64, "unique": true} |
| synced_from_paas20 | models.BooleanField | 187 | 账户信息是否从 PaaS 2.0 同步过来 | - | {"default": false} |



---


### GitRepository

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`
**行号**: 195
**基类**: paasng.utils.models.OwnerTimestampedModel, apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin
**描述**: 基于 Git 的软件存储库

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| server_name | models.CharField | 198 | - | GIT 服务名称 | {"max_length": 32} |
| repo_url | models.CharField | 199 | - | 项目地址 | {"max_length": 2048} |
| source_dir | models.CharField | 200 | - | 源码目录 | {"max_length": 2048, "null": true} |



---


### DockerRepository

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`
**行号**: 219
**基类**: paasng.utils.models.OwnerTimestampedModel, apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin
**描述**: 容器镜像仓库

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| server_name | models.CharField | 222 | - | DockerRegistry 服务名称 | {"max_length": 32} |
| repo_url | models.CharField | 223 | 形如 registry.hub.docker.com/library/python, 也可省略 registry 地址 | 项目地址 | {"max_length": 2048} |
| source_dir | models.CharField | 228 | - | 源码目录 | {"max_length": 2048, "null": true} |



---


### SourcePackage

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`
**行号**: 308
**基类**: paasng.utils.models.OwnerTimestampedModel
**描述**: 源码包存储信息

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| version | models.CharField | 314 | - | 版本号 | {"max_length": 128} |
| package_name | models.CharField | 315 | - | 源码包原始文件名 | {"max_length": 128} |
| package_size | models.BigIntegerField | 316 | - | 源码包大小, bytes | {} |
| storage_engine | models.CharField | 317 | 源码包真实存放的存储服务类型 | 存储引擎 | {"max_length": 64} |
| storage_path | models.CharField | 318 | [deprecated] 源码包在存储服务中存放的位置 | 存储路径 | {"max_length": 1024} |
| storage_url | models.CharField | 321 | 可获取到源码包的 URL 地址 | 存储地址 | {"max_length": 1024} |
| sha256_signature | models.CharField | 324 | - | sha256数字签名 | {"max_length": 64, "null": true} |
| relative_path | models.CharField | 325 | 如果压缩时将目录也打包进来, 入目录名是 foo, 那么 relative_path = 'foo/' | 源码入口的相对路径 | {"max_length": 255} |
| is_deleted | models.BooleanField | 330 | 如果 SourcePackage 指向的源码包已被清理, 则设置该值为 True | 源码包是否已被清理 | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | modules.Module | packages | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module', 'version') |

---


### RepoBasicAuthHolder

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`
**行号**: 566
**基类**: paasng.utils.models.TimestampedModel
**描述**: Repo 鉴权

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| username | models.CharField | 569 | - | 仓库用户名 | {"max_length": 64} |
| repo_id | models.IntegerField | 572 | - | 关联仓库 | {} |
| repo_type | models.CharField | 573 | - | 仓库类型 | {"max_length": 32} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | modules.Module | 不适用 | `models.CASCADE` |


---


### SourceTypeSpecConfig

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`
**行号**: 598
**基类**: paasng.utils.models.AuditedModel
**描述**: SourceTypeSpec 数据存储

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 602 | - | `_('服务名称')` | {"max_length": 32, "unique": true} |
| enabled | models.BooleanField | 604 | - | 是否启用 | {"default": false} |
| spec_cls | models.CharField | 605 | - | 配置类路径 | {"max_length": 128} |
| server_config | models.JSONField | 606 | - | 服务配置 | {"blank": true, "default": "`dict`"} |
| authorization_base_url | models.CharField | 609 | - | OAuth 授权链接 | {"blank": true, "default": "", "max_length": 256} |
| client_id | models.CharField | 610 | - | OAuth App Client ID | {"blank": true, "default": "", "max_length": 256} |
| redirect_uri | models.CharField | 612 | - | 重定向（回调）地址 | {"blank": true, "default": "", "max_length": 256} |
| token_base_url | models.CharField | 613 | - | 获取 Token 链接 | {"blank": true, "default": "", "max_length": 256} |



---


### Template

**模块**: `apiserver.paasng.paasng.platform.templates.models`
**行号**: 38
**基类**: paasng.utils.models.AuditedModel
**描述**: 开发模板配置

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 41 | - | `_('模板名称')` | {"max_length": 64, "unique": true} |
| type | models.CharField | 42 | - | `_('模板类型')` | {"choices": "`TemplateType.get_django_choices()`", "max_length": 16} |
| language | models.CharField | 45 | - | `_('开发语言')` | {"max_length": 32} |
| market_ready | models.BooleanField | 46 | - | `_('能否发布到应用集市')` | {"default": false} |
| preset_services_config | models.JSONField | 47 | - | `_('预设增强服务配置')` | {"blank": true, "default": "`dict`"} |
| blob_url | models.JSONField | 48 | - | `_('不同版本二进制包存储路径')` | {} |
| enabled_regions | models.JSONField | 49 | - | `_('允许被使用的版本')` | {"blank": true, "default": "`list`"} |
| required_buildpacks | models.JSONField | 50 | - | `_('必须的构建工具')` | {"blank": true, "default": "`list`"} |
| processes | models.JSONField | 51 | - | `_('进程配置')` | {"blank": true, "default": "`dict`"} |
| tags | models.JSONField | 52 | - | `_('标签')` | {"blank": true, "default": "`list`"} |
| repo_url | models.CharField | 53 | - | `_('代码仓库信息')` | {"blank": true, "default": "", "max_length": 256} |
| runtime_type | models.CharField | 54 | - | `_('运行时类型')` | {"default": "`RuntimeType.BUILDPACK`", "max_length": 32} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ['created'] |

---


### TimestampedModel

**模块**: `apiserver.paasng.paasng.utils.models`
**行号**: 209
**基类**: models.Model
**描述**: Model with 'created' and 'updated' fields.

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| region | models.CharField | 212 | 部署区域 | - | {"max_length": 32} |
| created | models.DateTimeField | 213 | - | - | {"auto_now_add": true} |
| updated | models.DateTimeField | 214 | - | - | {"auto_now": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### OwnerTimestampedModel

**模块**: `apiserver.paasng.paasng.utils.models`
**行号**: 223
**基类**: apiserver.paasng.paasng.utils.models.TimestampedModel
**描述**: Model with 'created' and 'updated' fields.

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### AuditedModel

**模块**: `apiserver.paasng.paasng.utils.models`
**行号**: 245
**基类**: models.Model
**描述**: Audited model with 'created' and 'updated' fields.

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| created | models.DateTimeField | 248 | - | - | {"auto_now_add": true} |
| updated | models.DateTimeField | 249 | - | - | {"auto_now": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### UuidAuditedModel

**模块**: `apiserver.paasng.paasng.utils.models`
**行号**: 255
**基类**: apiserver.paasng.paasng.utils.models.AuditedModel
**描述**: Add a UUID primary key to an :class:`AuditedModel`.

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| uuid | models.UUIDField | 258 | - | - | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### RepoQuotaStatistics

**模块**: `svc-bkrepo.svc_bk_repo.monitoring.models`
**行号**: 22
**基类**: models.Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| repo_name | models.CharField | 24 | - | 仓库名称 | {"max_length": 64} |
| max_size | models.BigIntegerField | 25 | 单位字节，值为 nul 时表示未设置仓库配额 | 仓库最大配额 | {"null": true} |
| used | models.BigIntegerField | 26 | 单位字节 | 仓库已使用容量 | {"default": 0} |
| updated | models.DateTimeField | 27 | - | - | {"auto_now": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| instance | models.ForeignKey | paas_service.ServiceInstance | 不适用 | `models.CASCADE` |


---


### ApmData

**模块**: `svc-otel.svc_otel.vendor.models`
**行号**: 23
**基类**: paas_service.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| bk_app_code | models.CharField | 24 | - | - | {"max_length": 64} |
| env | models.CharField | 25 | - | - | {"max_length": 64} |
| app_name | models.CharField | 26 | - | - | {"max_length": 64} |
| data_token | models.CharField | 27 | - | - | {"max_length": 255} |
| is_delete | models.BooleanField | 28 | - | - | {"default": false} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('bk_app_code', 'env') |

---


### CronTask

**模块**: `svc-rabbitmq.tasks.models`
**行号**: 147
**基类**: models.Model

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 148 | - | - | {"max_length": 255, "unique": true} |
| interval | models.DurationField | 149 | - | - | {} |
| next_run_time | models.DateTimeField | 150 | - | - | {"blank": true, "db_index": true, "default": "`get_now`", "null": true} |
| last_run_time | models.DateTimeField | 151 | - | - | {"blank": true, "null": true} |
| enabled | models.BooleanField | 152 | - | - | {"default": false} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ('next_run_time', 'name') |

---


### Tag

**模块**: `svc-rabbitmq.vendor.models`
**行号**: 34
**基类**: paas_service.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| key | models.CharField | 39 | - | - | {"max_length": 64} |
| value | models.CharField | 40 | - | - | {"max_length": 128} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### Cluster

**模块**: `svc-rabbitmq.vendor.models`
**行号**: 43
**基类**: paas_service.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 44 | - | - | {"max_length": 64} |
| host | models.CharField | 45 | - | - | {"max_length": 64} |
| port | models.IntegerField | 46 | - | - | {"default": 5672} |
| management_api | models.TextField | 47 | - | - | {} |
| admin | models.CharField | 48 | - | - | {"max_length": 64} |
| version | models.CharField | 50 | - | - | {"max_length": 16} |
| enable | models.BooleanField | 51 | - | - | {"default": true} |



---


### ClusterTag

**模块**: `svc-rabbitmq.vendor.models`
**行号**: 58
**基类**: svc-rabbitmq.vendor.models.Tag
**描述**: 集群标签，用于分配和分组

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| key | models.CharField | 39 | - | - | {"max_length": 64} |
| value | models.CharField | 40 | - | - | {"max_length": 128} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| instance | models.ForeignKey | `Cluster` | tags | `models.CASCADE` |


---


### LinkableModel

**模块**: `svc-rabbitmq.vendor.models`
**行号**: 64
**基类**: paas_service.models.AuditedModel

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| link_type | models.IntegerField | 68 | - | - | {"choices": "`[(i.value, i.name) for i in LinkType]`", "default": "`LinkType.empty.value`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| linked | models.ForeignKey | self | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### UserPolicy

**模块**: `svc-rabbitmq.vendor.models`
**行号**: 103
**基类**: svc-rabbitmq.vendor.models.LinkableModel
**描述**: 集群下创建 vhost 默认策略，和具体 vhost 无关

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 108 | - | - | {"max_length": 64, "null": true} |
| enable | models.BooleanField | 109 | - | - | {"default": true} |
| pattern | models.CharField | 110 | - | - | {"blank": true, "max_length": 128, "null": true} |
| apply_to | models.CharField | 111 | - | - | {"blank": true, "choices": "`[(i.value, i.name) for i in PolicyTarget]`", "max_length": 64, "null": true} |
| priority | models.IntegerField | 114 | - | - | {"blank": true, "null": true} |
| cluster_id | models.IntegerField | 116 | - | - | {"blank": true, "default": null} |
| link_type | models.IntegerField | 68 | - | - | {"choices": "`[(i.value, i.name) for i in LinkType]`", "default": "`LinkType.empty.value`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| linked | models.ForeignKey | self | 不适用 | `models.CASCADE` |


---


### UserPolicyTag

**模块**: `svc-rabbitmq.vendor.models`
**行号**: 142
**基类**: svc-rabbitmq.vendor.models.Tag
**描述**: 表示绑定关系

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| key | models.CharField | 39 | - | - | {"max_length": 64} |
| value | models.CharField | 40 | - | - | {"max_length": 128} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| instance | models.ForeignKey | `UserPolicy` | tags | `models.CASCADE` |


---


### LimitPolicy

**模块**: `svc-rabbitmq.vendor.models`
**行号**: 153
**基类**: svc-rabbitmq.vendor.models.LinkableModel
**描述**: 集群下创建 vhost 限制机制，和具体 vhost 无关

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 158 | - | - | {"max_length": 64, "null": true} |
| enable | models.BooleanField | 159 | - | - | {"default": true} |
| limit | models.CharField | 160 | - | - | {"blank": true, "choices": "`[(i.value, i.name) for i in LimitType]`", "max_length": 64, "null": true} |
| value | models.IntegerField | 163 | - | - | {"blank": true, "null": true} |
| cluster_id | models.IntegerField | 164 | - | - | {"blank": true, "default": null} |
| link_type | models.IntegerField | 68 | - | - | {"choices": "`[(i.value, i.name) for i in LinkType]`", "default": "`LinkType.empty.value`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| linked | models.ForeignKey | self | 不适用 | `models.CASCADE` |


---


### LimitPolicyTag

**模块**: `svc-rabbitmq.vendor.models`
**行号**: 174
**基类**: svc-rabbitmq.vendor.models.Tag
**描述**: 表示绑定关系

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| key | models.CharField | 39 | - | - | {"max_length": 64} |
| value | models.CharField | 40 | - | - | {"max_length": 128} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| instance | models.ForeignKey | `LimitPolicy` | tags | `models.CASCADE` |


---


### InstanceBill

**模块**: `svc-rabbitmq.vendor.models`
**行号**: 180
**基类**: paas_service.models.UuidAuditedModel
**描述**: 实例单据，保存申请上下文，方便重入

#### 字段

| 字段名 | 类型 | 行号 | 说明 | 显示名称 | 参数 |
|--------|------|------|------|----------|------|
| name | models.CharField | 183 | - | - | {"max_length": 128} |
| action | models.CharField | 184 | - | - | {"max_length": 32} |



---
