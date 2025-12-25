# django-models 扫描报告

## 元数据
暂无元数据。

## 概要信息
- **总数量**: 167
- **已扫描文件数**: 167
- **扫描耗时**: 2093 毫秒

- **模型总数**: 167
- **字段总数**: 684
- **关系总数**: 148

## 结果详情

### App

**模块**: `apiserver.paasng.paas_wl.bk_app.applications.models.app`  
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**描述**: App Model

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| owner | models.CharField | 1 | {"max_length": 64} |
| region | models.CharField | 1 | {"max_length": 32} |
| name | models.SlugField | 1 | {"max_length": 64, "validators": ["`validate_app_name`"]} |
| type | models.CharField | 1 | {"db_index": true, "default": "`WlAppType.DEFAULT.value`", "max_length": 16, "verbose_name": "\u5e94\u7528\u7c7b\u578b"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('region', 'name') |

---


### Build

**模块**: `apiserver.paasng.paas_wl.bk_app.applications.models.build`  
**行号**: 1  
**基类**: paas_wl.utils.models.UuidAuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| application_id | models.UUIDField | 1 | {"null": true, "verbose_name": "\u6240\u5c5e\u5e94\u7528"} |
| module_id | models.UUIDField | 1 | {"null": true, "verbose_name": "\u6240\u5c5e\u6a21\u5757"} |
| owner | models.CharField | 1 | {"max_length": 64} |
| slug_path | models.TextField | 1 | {"help_text": "slug path \u5f62\u5982 {region}/home/{name}:{branch}:{revision}/push", "null": true} |
| image | models.TextField | 1 | {"help_text": "\u8fd0\u884c Build \u7684\u955c\u50cf\u5730\u5740. \u5982\u679c\u6784\u4ef6\u7c7b\u578b\u4e3a image\uff0c\u8be5\u503c\u5373\u6784\u5efa\u4ea7\u7269; \u5982\u679c\u6784\u5efa\u4ea7\u7269\u662f Slug, \u5219\u8fd4\u56de SlugRunner \u7684\u955c\u50cf", "null": true} |
| source_type | models.CharField | 1 | {"max_length": 128, "null": true} |
| branch | models.CharField | 1 | {"help_text": "readable version, such as trunk/master", "max_length": 128, "null": true} |
| revision | models.CharField | 1 | {"help_text": "unique version, such as sha256", "max_length": 128, "null": true} |
| bkapp_revision_id | models.IntegerField | 1 | {"help_text": "\u4e0e\u672c\u6b21\u6784\u5efa\u5173\u8054\u7684 BkApp Revision id", "null": true} |
| artifact_type | models.CharField | 1 | {"default": "`ArtifactType.SLUG`", "help_text": "\u6784\u4ef6\u7c7b\u578b", "max_length": 16} |
| artifact_detail | models.JSONField | 1 | {"default": {}, "help_text": "\u6784\u4ef6\u8be6\u60c5(\u5c55\u793a\u4fe1\u606f)"} |
| artifact_deleted | models.BooleanField | 1 | {"default": false, "help_text": "slug/\u955c\u50cf\u662f\u5426\u5df2\u88ab\u6e05\u7406"} |
| artifact_metadata | models.JSONField | 1 | {"default": {}, "help_text": "\u6784\u4ef6\u5143\u4fe1\u606f, \u5305\u62ec entrypoint/use_cnb/use_dockerfile \u7b49\u4fe1\u606f"} |

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
**行号**: 1  
**基类**: paas_wl.utils.models.UuidAuditedModel  
**描述**: This Build Process was invoked via a source tarball or anything similar

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| application_id | models.UUIDField | 1 | {"null": true, "verbose_name": "\u6240\u5c5e\u5e94\u7528"} |
| module_id | models.UUIDField | 1 | {"null": true, "verbose_name": "\u6240\u5c5e\u6a21\u5757"} |
| owner | models.CharField | 1 | {"max_length": 64} |
| image | models.CharField | 1 | {"help_text": "builder image", "max_length": 512, "null": true} |
| generation | models.PositiveBigIntegerField | 1 | {"help_text": "\u6bcf\u4e2a\u5e94\u7528\u72ec\u7acb\u7684\u81ea\u589eID", "verbose_name": "\u81ea\u589eID"} |
| invoke_message | models.CharField | 1 | {"blank": true, "help_text": "\u89e6\u53d1\u4fe1\u606f", "max_length": 255, "null": true} |
| source_tar_path | models.CharField | 1 | {"max_length": 2048} |
| branch | models.CharField | 1 | {"max_length": 128, "null": true} |
| revision | models.CharField | 1 | {"max_length": 128, "null": true} |
| logs_was_ready_at | models.DateTimeField | 1 | {"help_text": "Pod \u72b6\u6001\u5c31\u7eea\u5141\u8bb8\u8bfb\u53d6\u65e5\u5fd7\u7684\u65f6\u95f4", "null": true} |
| int_requested_at | models.DateTimeField | 1 | {"help_text": "\u7528\u6237\u8bf7\u6c42\u4e2d\u65ad\u7684\u65f6\u95f4", "null": true} |
| completed_at | models.DateTimeField | 1 | {"help_text": "failed/successful/interrupted \u90fd\u662f\u5b8c\u6210", "null": true, "verbose_name": "\u5b8c\u6210\u65f6\u95f4"} |
| status | models.CharField | 1 | {"choices": "`make_enum_choices(BuildStatus)`", "default": "`BuildStatus.PENDING.value`", "max_length": 12} |

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
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**描述**: App configs, includes env variables and resource limits

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| owner | models.CharField | 1 | {"max_length": 64} |
| domain | models.CharField | 1 | {"default": "", "max_length": 64} |
| cluster | models.CharField | 1 | {"blank": true, "default": "", "max_length": 64} |
| image | models.CharField | 1 | {"max_length": 256, "null": true} |
| mount_log_to_host | models.BooleanField | 1 | {"default": true, "help_text": "Whether mount app logs to host"} |

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
**行号**: 1  
**基类**: models.Model  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| stream | models.CharField | 1 | {"max_length": 16} |
| line | models.TextField | 1 | {} |
| created | models.DateTimeField | 1 | {"auto_now_add": true} |
| updated | models.DateTimeField | 1 | {"auto_now": true} |

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
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| owner | models.CharField | 1 | {"max_length": 64} |
| version | models.PositiveIntegerField | 1 | {} |
| summary | models.TextField | 1 | {"blank": true, "null": true} |
| failed | models.BooleanField | 1 | {"default": false} |

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
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: Cloud-native Application's Model Resource

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| application_id | models.UUIDField | 1 | {"null": false, "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| module_id | models.UUIDField | 1 | {"null": false, "unique": true, "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| revision | models.OneToOneField | AppModelRevision | 不适用 | `models.CASCADE` |

#### Meta 选项

| 选项 | 值 |
|------|-----|
| indexes | ["`models.Index(fields=['application_id', 'module_id'])`"] |

---


### AppModelRevision

**模块**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.app_resource`  
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: Revisions of cloud-native Application's Model Resource

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| application_id | models.UUIDField | 1 | {"null": false, "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| module_id | models.UUIDField | 1 | {"null": false, "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |
| version | models.CharField | 1 | {"max_length": 64, "verbose_name": "`_(\u0027\u6a21\u578b\u7248\u672c\u0027)`"} |
| yaml_value | models.TextField | 1 | {"verbose_name": "`_(\u0027\u5e94\u7528\u6a21\u578b\uff08YAML \u683c\u5f0f\uff09\u0027)`"} |
| json_value | models.JSONField | 1 | {"verbose_name": "`_(\u0027\u5e94\u7528\u6a21\u578b\uff08JSON \u683c\u5f0f\uff09\u0027)`"} |
| deployed_value | models.JSONField | 1 | {"null": true, "verbose_name": "`_(\u0027\u5df2\u90e8\u7f72\u7684\u5e94\u7528\u6a21\u578b\uff08JSON \u683c\u5f0f\uff09\u0027)`"} |
| has_deployed | models.BooleanField | 1 | {"default": false, "verbose_name": "`_(\u0027\u662f\u5426\u5df2\u90e8\u7f72\u0027)`"} |
| is_draft | models.BooleanField | 1 | {"default": false, "verbose_name": "`_(\u0027\u662f\u5426\u8349\u7a3f\u0027)`"} |
| is_deleted | models.BooleanField | 1 | {"default": false, "verbose_name": "`_(\u0027\u662f\u5426\u5df2\u5220\u9664\u0027)`"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| indexes | ["`models.Index(fields=['application_id', 'module_id'])`"] |

---


### AppModelDeploy

**模块**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.app_resource`  
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: This model stores the cloud-native app's deployment histories.

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| application_id | models.UUIDField | 1 | {"null": false, "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| module_id | models.UUIDField | 1 | {"null": false, "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |
| environment_name | models.CharField | 1 | {"choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": false, "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| name | models.CharField | 1 | {"max_length": 64, "verbose_name": "`_(\u0027Deploy \u540d\u79f0\u0027)`"} |
| status | models.CharField | 1 | {"blank": true, "choices": "`DeployStatus.get_choices()`", "max_length": 32, "null": true, "verbose_name": "`_(\u0027\u72b6\u6001\u0027)`"} |
| reason | models.CharField | 1 | {"blank": true, "max_length": 128, "null": true, "verbose_name": "`_(\u0027\u72b6\u6001\u539f\u56e0\u0027)`"} |
| message | models.TextField | 1 | {"blank": true, "null": true, "verbose_name": "`_(\u0027\u72b6\u6001\u63cf\u8ff0\u6587\u5b57\u0027)`"} |
| last_transition_time | models.DateTimeField | 1 | {"null": true, "verbose_name": "`_(\u0027\u72b6\u6001\u6700\u8fd1\u53d8\u66f4\u65f6\u95f4\u0027)`"} |

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
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: ConfigMap 类型的挂载资源

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| application_id | models.UUIDField | 1 | {"null": false, "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| module_id | models.UUIDField | 1 | {"null": true, "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |
| environment_name | models.CharField | 1 | {"choices": "`MountEnvName.get_choices()`", "max_length": 16, "null": false, "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| name | models.CharField | 1 | {"help_text": "`_(\u0027\u6302\u8f7d\u8d44\u6e90\u540d\u0027)`", "max_length": 63} |
| data | models.JSONField | 1 | {"default": "`dict`"} |
| display_name | models.CharField | 1 | {"help_text": "`_(\u0027\u6302\u8f7d\u8d44\u6e90\u5c55\u793a\u540d\u79f0\u0027)`", "max_length": 63, "null": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('name', 'application_id', 'environment_name') |

---


### PersistentStorageSource

**模块**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.mount`  
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: 持久存储类型的挂载资源

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| application_id | models.UUIDField | 1 | {"null": false, "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| module_id | models.UUIDField | 1 | {"null": true, "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |
| environment_name | models.CharField | 1 | {"choices": "`MountEnvName.get_choices()`", "max_length": 16, "null": false, "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| name | models.CharField | 1 | {"help_text": "`_(\u0027\u6302\u8f7d\u8d44\u6e90\u540d\u0027)`", "max_length": 63} |
| storage_size | models.CharField | 1 | {"max_length": 63} |
| storage_class_name | models.CharField | 1 | {"max_length": 63} |
| display_name | models.CharField | 1 | {"help_text": "`_(\u0027\u6302\u8f7d\u8d44\u6e90\u5c55\u793a\u540d\u79f0\u0027)`", "max_length": 63, "null": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('name', 'application_id', 'environment_name') |

---


### Mount

**模块**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.mount`  
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: 挂载配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| module_id | models.UUIDField | 1 | {"null": false, "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |
| environment_name | models.CharField | 1 | {"choices": "`MountEnvName.get_choices()`", "max_length": 16, "null": false, "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| name | models.CharField | 1 | {"help_text": "`_(\u0027\u6302\u8f7d\u70b9\u7684\u540d\u79f0\u0027)`", "max_length": 63} |
| mount_path | models.CharField | 1 | {"max_length": 128} |
| source_type | models.CharField | 1 | {"choices": "`VolumeSourceType.get_choices()`", "max_length": 32} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('module_id', 'mount_path', 'environment_name') |

---


### AppMetricsMonitor

**模块**: `apiserver.paasng.paas_wl.bk_app.monitoring.app_monitor.models`  
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| is_enabled | models.BooleanField | 1 | {"default": true, "help_text": "\u662f\u5426\u542f\u52a8 AppMetrics"} |
| port | models.IntegerField | 1 | {"help_text": "Service \u7aef\u53e3"} |
| target_port | models.IntegerField | 1 | {"help_text": "\u5bb9\u5668\u5185\u7684\u7aef\u53e3"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.OneToOneField | `WlApp` | 不适用 | `models.CASCADE` |


---


### ProcessSpecPlan

**模块**: `apiserver.paasng.paas_wl.bk_app.processes.models`  
**行号**: 1  
**基类**: models.Model  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"db_index": true, "max_length": 32} |
| max_replicas | models.IntegerField | 1 | {} |
| is_active | models.BooleanField | 1 | {"default": true, "verbose_name": "\u662f\u5426\u53ef\u7528"} |
| created | models.DateTimeField | 1 | {"auto_now_add": true} |
| updated | models.DateTimeField | 1 | {"auto_now": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| get_latest_by | created |

---


### ProcessSpec

**模块**: `apiserver.paasng.paas_wl.bk_app.processes.models`  
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 32} |
| type | models.CharField | 1 | {"max_length": 32} |
| proc_command | models.TextField | 1 | {"help_text": "\u8fdb\u7a0b\u542f\u52a8\u547d\u4ee4(\u5305\u542b\u5b8c\u6574\u547d\u4ee4\u548c\u53c2\u6570\u7684\u5b57\u7b26\u4e32), \u53ea\u80fd\u4e0e command/args \u4e8c\u9009\u4e00", "null": true} |
| port | models.IntegerField | 1 | {"help_text": "\u5bb9\u5668\u7aef\u53e3", "null": true} |
| target_replicas | models.IntegerField | 1 | {"default": 1} |
| target_status | models.CharField | 1 | {"default": "start", "max_length": 32} |
| autoscaling | models.BooleanField | 1 | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| engine_app | models.ForeignKey | api.App | process_specs | `models.DO_NOTHING` |
| plan | models.ForeignKey | `ProcessSpecPlan` | 不适用 | `models.CASCADE` |


---


### ProcessProbe

**模块**: `apiserver.paasng.paas_wl.bk_app.processes.models`  
**行号**: 1  
**基类**: models.Model  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| process_type | models.CharField | 1 | {"max_length": 255} |
| probe_type | models.CharField | 1 | {"choices": "`ProbeType.get_django_choices()`", "max_length": 255} |
| initial_delay_seconds | models.IntegerField | 1 | {"default": 0} |
| timeout_seconds | models.PositiveIntegerField | 1 | {"default": 1} |
| period_seconds | models.PositiveIntegerField | 1 | {"default": 10} |
| success_threshold | models.PositiveIntegerField | 1 | {"default": 1} |
| failure_threshold | models.PositiveIntegerField | 1 | {"default": 3} |

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
**行号**: 1  
**基类**: paas_wl.utils.models.UuidAuditedModel  
**描述**: 应用集群

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| region | models.CharField | 1 | {"db_index": true, "max_length": 32} |
| name | models.CharField | 1 | {"help_text": "name of the cluster", "max_length": 32, "unique": true} |
| type | models.CharField | 1 | {"default": "`ClusterType.NORMAL`", "help_text": "cluster type", "max_length": 32} |
| description | models.TextField | 1 | {"blank": true, "help_text": "\u63cf\u8ff0\u4fe1\u606f"} |
| is_default | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u4e3a\u9ed8\u8ba4\u96c6\u7fa4", "null": true} |
| token_type | models.IntegerField | 1 | {"null": true} |



---


### APIServer

**模块**: `apiserver.paasng.paas_wl.infras.cluster.models`  
**行号**: 1  
**基类**: paas_wl.utils.models.UuidAuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| host | models.CharField | 1 | {"help_text": "API Server \u7684\u540e\u7aef\u5730\u5740", "max_length": 255} |
| overridden_hostname | models.CharField | 1 | {"blank": true, "default": null, "help_text": "\u5728\u8bf7\u6c42\u8be5 APIServer \u65f6, \u4f7f\u7528\u8be5 hostname \u66ff\u6362\u5177\u4f53\u7684 backend \u4e2d\u7684 hostname", "max_length": 255, "null": true} |

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
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**描述**: 应用挂件模版

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| region | models.CharField | 1 | {"max_length": 32} |
| name | models.CharField | 1 | {"max_length": 64} |
| spec | models.TextField | 1 | {} |
| enabled | models.BooleanField | 1 | {"default": true} |
| type | models.IntegerField | 1 | {"default": "`AppAddOnType.SIMPLE_SIDECAR.value`"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('region', 'name') |

---


### AppAddOn

**模块**: `apiserver.paasng.paas_wl.infras.resource_templates.models`  
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**描述**: 应用挂件关联实例

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| enabled | models.BooleanField | 1 | {"default": true} |
| spec | models.TextField | 1 | {} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | `WlApp` | add_ons | `models.CASCADE` |
| template | models.ForeignKey | `AppAddOnTemplate` | instances | `models.CASCADE` |


---


### AuditedModel

**模块**: `apiserver.paasng.paas_wl.utils.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: Audited model with 'created' and 'updated' fields.

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| created | models.DateTimeField | 1 | {"auto_now_add": true} |
| updated | models.DateTimeField | 1 | {"auto_now": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### UuidAuditedModel

**模块**: `apiserver.paasng.paas_wl.utils.models`  
**行号**: 1  
**基类**: apiserver.paasng.paas_wl.utils.models.AuditedModel  
**描述**: Add a UUID primary key to an class`AuditedModel`.

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| uuid | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### TimestampedModel

**模块**: `apiserver.paasng.paas_wl.utils.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: Model with 'created' and 'updated' fields.

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| region | models.CharField | 1 | {"help_text": "\u90e8\u7f72\u533a\u57df", "max_length": 32} |
| created | models.DateTimeField | 1 | {"auto_now_add": true} |
| updated | models.DateTimeField | 1 | {"auto_now": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### AppImageCredential

**模块**: `apiserver.paasng.paas_wl.workloads.images.models`  
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**描述**: ImageCredential of applications, each object(entry) represents an (username + password) pair for a registry

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| registry | models.CharField | 1 | {"max_length": 255} |
| username | models.CharField | 1 | {"blank": false, "max_length": 32} |

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
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**描述**: App owned UserCredential, aka (Username + Password) pair

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| application_id | models.UUIDField | 1 | {"null": false, "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| name | models.CharField | 1 | {"help_text": "\u51ed\u8bc1\u540d\u79f0", "max_length": 32} |
| username | models.CharField | 1 | {"help_text": "\u8d26\u53f7", "max_length": 64} |
| description | models.TextField | 1 | {"help_text": "\u63cf\u8ff0"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('application_id', 'name') |

---


### RegionClusterState

**模块**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`  
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.AuditedModel  
**描述**: A RegionClusterState is a state which describes what the cluster is in a specified moment. it

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| region | models.CharField | 1 | {"max_length": 32} |
| cluster_name | models.CharField | 1 | {"max_length": 32, "null": true} |
| name | models.CharField | 1 | {"max_length": 64} |
| nodes_digest | models.CharField | 1 | {"db_index": true, "max_length": 64} |
| nodes_cnt | models.IntegerField | 1 | {"default": 0} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('region', 'cluster_name', 'name') |
| get_latest_by | created |
| ordering | ['-created'] |

---


### RCStateAppBinding

**模块**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`  
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.AuditedModel  
**描述**: If an app was bind with one RegionClusterState instance, it means that the app will not be

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.OneToOneField | `WlApp` | 不适用 | `models.CASCADE` |
| state | models.ForeignKey | `RegionClusterState` | 不适用 | `models.CASCADE` |


---


### EgressSpec

**模块**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`  
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| replicas | models.IntegerField | 1 | {"default": 1} |
| cpu_limit | models.CharField | 1 | {"max_length": 16} |
| memory_limit | models.CharField | 1 | {"max_length": 16} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| wl_app | models.OneToOneField | `WlApp` | 不适用 | `models.CASCADE` |


---


### EgressRule

**模块**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`  
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.AuditedModel  
**描述**: BCS Egress.spec.rules

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| dst_port | models.IntegerField | 1 | {} |
| host | models.CharField | 1 | {"max_length": 128} |
| protocol | models.CharField | 1 | {"choices": "`NetworkProtocol.get_django_choices()`", "max_length": 32} |
| src_port | models.IntegerField | 1 | {} |
| service | models.CharField | 1 | {"max_length": 128} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| spec | models.ForeignKey | `EgressSpec` | rules | `models.CASCADE` |


---


### AppDomain

**模块**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`  
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.AuditedModel  
**描述**: Domains of applications, each object(entry) represents an (domain + path_prefix) pair.

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| region | models.CharField | 1 | {"max_length": 32} |
| host | models.CharField | 1 | {"max_length": 128} |
| path_prefix | models.CharField | 1 | {"default": "/", "help_text": "the accessable path for current domain", "max_length": 64} |
| https_enabled | models.BooleanField | 1 | {"default": false} |
| https_auto_redirection | models.BooleanField | 1 | {"default": false} |
| source | models.IntegerField | 1 | {"choices": "`make_enum_choices(AppDomainSource)`"} |

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
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| region | models.CharField | 1 | {"max_length": 32} |
| name | models.CharField | 1 | {"max_length": 128, "unique": true, "validators": ["`RegexValidator(DNS_SAFE_PATTERN)`"]} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### AppDomainSharedCert

**模块**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`  
**行号**: 1  
**基类**: apiserver.paasng.paas_wl.workloads.networking.ingress.models.BasicCert  
**描述**: Shared TLS Certifications for AppDomain, every app's domain may link to this certificate as

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| auto_match_cns | models.TextField | 1 | {"max_length": 2048} |
| region | models.CharField | 1 | {"max_length": 32} |
| name | models.CharField | 1 | {"max_length": 128, "unique": true, "validators": ["`RegexValidator(DNS_SAFE_PATTERN)`"]} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| db_table | services_appdomainsharedcert |

---


### AppSubpath

**模块**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`  
**行号**: 1  
**基类**: paas_wl.bk_app.applications.models.AuditedModel  
**描述**: stores application's subpaths

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| region | models.CharField | 1 | {"max_length": 32} |
| cluster_name | models.CharField | 1 | {"max_length": 32} |
| subpath | models.CharField | 1 | {"max_length": 128} |
| source | models.IntegerField | 1 | {} |

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
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: custom domain for application

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"help_text": "\u57df\u540d", "max_length": 253, "null": false} |
| path_prefix | models.CharField | 1 | {"default": "/", "help_text": "the accessable path for current domain", "max_length": 64} |
| module_id | models.UUIDField | 1 | {"help_text": "\u5173\u8054\u7684\u6a21\u5757 ID", "null": false} |
| environment_id | models.BigIntegerField | 1 | {"help_text": "\u5173\u8054\u7684\u73af\u5883 ID", "null": false} |
| https_enabled | models.BooleanField | 1 | {"default": false, "help_text": "\u8be5\u57df\u540d\u662f\u5426\u5f00\u542f https", "null": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('name', 'path_prefix', 'module_id', 'environment_id') |
| db_table | services_domain |

---


### Command

**模块**: `apiserver.paasng.paas_wl.workloads.release_controller.hooks.models`  
**行号**: 1  
**基类**: paas_wl.utils.models.UuidAuditedModel  
**描述**: The Command Model, which will be used to schedule a container running `command`,

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| type | models.CharField | 1 | {"choices": "`CommandType.get_choices()`", "max_length": 32} |
| version | models.PositiveIntegerField | 1 | {} |
| command | models.TextField | 1 | {} |
| exit_code | models.SmallIntegerField | 1 | {"help_text": "\u5bb9\u5668\u7ed3\u675f\u72b6\u6001\u7801, -1 \u8868\u793a\u672a\u77e5", "null": true} |
| status | models.CharField | 1 | {"choices": "`CommandStatus.get_choices()`", "default": "`CommandStatus.PENDING.value`", "max_length": 12} |
| logs_was_ready_at | models.DateTimeField | 1 | {"help_text": "Pod \u72b6\u6001\u5c31\u7eea\u5141\u8bb8\u8bfb\u53d6\u65e5\u5fd7\u7684\u65f6\u95f4", "null": true} |
| int_requested_at | models.DateTimeField | 1 | {"help_text": "\u7528\u6237\u8bf7\u6c42\u4e2d\u65ad\u7684\u65f6\u95f4", "null": true} |
| operator | models.CharField | 1 | {"help_text": "\u64cd\u4f5c\u8005(\u88ab\u7f16\u7801\u7684 username), \u76ee\u524d\u8be5\u5b57\u6bb5\u65e0\u610f\u4e49", "max_length": 64} |

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
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: CI 资源

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| enabled | models.BooleanField | 1 | {"default": true, "verbose_name": "\u662f\u5426\u542f\u7528"} |
| backend | models.CharField | 1 | {"choices": "`CIBackend.get_django_choices()`", "max_length": 32, "verbose_name": "CI\u5f15\u64ce"} |

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
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: CI 资源原子

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| id | models.CharField | 1 | {"db_index": true, "max_length": 64, "primary_key": true, "unique": true} |
| name | models.CharField | 1 | {"max_length": 32} |
| enabled | models.BooleanField | 1 | {"default": true, "verbose_name": "\u662f\u5426\u542f\u7528"} |
| backend | models.CharField | 1 | {"choices": "`CIBackend.get_django_choices()`", "max_length": 32, "verbose_name": "CI\u5f15\u64ce"} |

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
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: DevSandbox Model

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| code | models.CharField | 1 | {"help_text": "\u6c99\u7bb1\u6807\u8bc6", "max_length": 8, "unique": true} |
| status | models.CharField | 1 | {"choices": "`DevSandboxStatus.get_choices()`", "max_length": 32, "verbose_name": "\u6c99\u7bb1\u72b6\u6001"} |
| expired_at | models.DateTimeField | 1 | {"help_text": "\u5230\u671f\u65f6\u95f4", "null": true} |

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
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  
**描述**: CodeEditor Model

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| dev_sandbox | models.OneToOneField | `DevSandbox` | code_editor | `models.CASCADE` |


---


### ProcessStructureLogCollectorConfig

**模块**: `apiserver.paasng.paasng.accessories.log.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 进程结构化日志采集配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| collector_config_id | models.BigAutoField | 1 | {"primary_key": true} |
| process_type | models.CharField | 1 | {"help_text": "\u8fdb\u7a0b\u7c7b\u578b(\u540d\u79f0)", "max_length": 16} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |
| env | models.ForeignKey | `ModuleEnvironment` | 不适用 | `models.CASCADE` |


---


### ElasticSearchConfig

**模块**: `apiserver.paasng.paasng.accessories.log.models`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  
**描述**: ES查询配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| collector_config_id | models.CharField | 1 | {"help_text": "\u91c7\u96c6\u914d\u7f6eID", "max_length": 64, "unique": true} |
| backend_type | models.CharField | 1 | {"help_text": "\u65e5\u5fd7\u540e\u7aef\u7c7b\u578b, \u53ef\u9009 \u0027es\u0027, \u0027bkLog\u0027 ", "max_length": 16} |



---


### ProcessLogQueryConfig

**模块**: `apiserver.paasng.paasng.accessories.log.models`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  
**描述**: 进程日志查询配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| process_type | models.CharField | 1 | {"blank": true, "max_length": 16, "null": true} |

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
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  
**描述**: 日志平台自定义采集项配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name_en | models.CharField | 1 | {"db_index": true, "help_text": "5-50\u4e2a\u5b57\u7b26\uff0c\u4ec5\u5305\u542b\u5b57\u6bcd\u6570\u5b57\u4e0b\u5212\u7ebf, \u67e5\u8be2\u7d22\u5f15\u662f name_en-*", "max_length": 50} |
| collector_config_id | models.BigIntegerField | 1 | {"db_index": true, "help_text": "\u91c7\u96c6\u914d\u7f6eID"} |
| index_set_id | models.BigIntegerField | 1 | {"help_text": "\u67e5\u8be2\u65f6\u4f7f\u7528", "null": true} |
| bk_data_id | models.BigIntegerField | 1 | {} |
| log_paths | models.JSONField | 1 | {} |
| log_type | models.CharField | 1 | {"max_length": 32} |
| is_builtin | models.BooleanField | 1 | {"default": false} |
| is_enabled | models.BooleanField | 1 | {"default": true} |

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
**行号**: 1  
**基类**: models.Model  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"help_text": "\u5206\u7c7b\u540d\u79f0", "max_length": 64} |
| remark | models.CharField | 1 | {"blank": true, "help_text": "\u5907\u6ce8", "max_length": 255, "null": true} |
| index | models.IntegerField | 1 | {"default": 0, "help_text": "\u663e\u793a\u6392\u5e8f\u5b57\u6bb5"} |
| enabled | models.BooleanField | 1 | {"default": true, "help_text": "\u521b\u5efa\u5e94\u7528\u65f6\u662f\u5426\u53ef\u9009\u62e9\u8be5\u5206\u7c7b"} |
| region | models.CharField | 1 | {"help_text": "\u90e8\u7f72\u533a\u57df", "max_length": 32} |

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
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: 蓝鲸应用: 开发者中心的编辑属性

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| code | models.CharField | 1 | {"help_text": "\u5e94\u7528\u7f16\u7801", "max_length": 64, "unique": true} |
| type | models.SmallIntegerField | 1 | {"choices": "`constant.AppType.get_choices()`", "help_text": "\u6309\u5b9e\u73b0\u65b9\u5f0f\u5206\u7c7b"} |
| state | models.SmallIntegerField | 1 | {"choices": "`constant.AppState.get_choices()`", "default": 1, "help_text": "\u5e94\u7528\u72b6\u6001"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.OneToOneField | `Application` | 不适用 | `models.CASCADE` |
| tag | models.ForeignKey | `Tag` | 不适用 | `models.SET_NULL` |


---


### DisplayOptions

**模块**: `apiserver.paasng.paasng.accessories.publish.market.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: app展示相关的属性

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| visible | models.BooleanField | 1 | {"default": true, "help_text": "\u9009\u9879: true(\u662f)\uff0cfalse(\u5426)"} |
| width | models.IntegerField | 1 | {"default": 890, "help_text": "\u5e94\u7528\u9875\u9762\u5bbd\u5ea6\uff0c\u5fc5\u987b\u4e3a\u6574\u6570\uff0c\u5355\u4f4d\u4e3apx"} |
| height | models.IntegerField | 1 | {"default": 550, "help_text": "\u5e94\u7528\u9875\u9762\u9ad8\u5ea6\uff0c\u5fc5\u987b\u4e3a\u6574\u6570\uff0c\u5355\u4f4d\u4e3apx"} |
| is_win_maximize | models.BooleanField | 1 | {"default": false} |
| win_bars | models.BooleanField | 1 | {"default": true, "help_text": "\u9009\u9879: true(on)\uff0cfalse(off)"} |
| resizable | models.BooleanField | 1 | {"default": true, "help_text": "\u9009\u9879\uff1atrue(\u53ef\u4ee5\u62c9\u4f38)\uff0cfalse(\u4e0d\u53ef\u4ee5\u62c9\u4f38)"} |
| contact | models.CharField | 1 | {"blank": true, "max_length": 128, "null": true} |
| open_mode | models.CharField | 1 | {"choices": "`constant.OpenMode.get_django_choices()`", "default": "`constant.OpenMode.NEW_TAB.value`", "max_length": 20} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| product | models.OneToOneField | `Product` | 不适用 | `models.CASCADE` |


---


### MarketConfig

**模块**: `apiserver.paasng.paasng.accessories.publish.market.models`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: 应用市场相关功能配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| enabled | models.BooleanField | 1 | {"verbose_name": "\u662f\u5426\u5f00\u542f"} |
| auto_enable_when_deploy | models.BooleanField | 1 | {"null": true, "verbose_name": "\u6210\u529f\u90e8\u7f72\u4e3b\u6a21\u5757\u6b63\u5f0f\u73af\u5883\u540e, \u662f\u5426\u81ea\u52a8\u6253\u5f00\u5e02\u573a"} |
| source_url_type | models.SmallIntegerField | 1 | {"verbose_name": "\u8bbf\u95ee\u5730\u5740\u7c7b\u578b"} |
| source_tp_url | models.URLField | 1 | {"blank": true, "null": true, "verbose_name": "\u7b2c\u4e09\u65b9\u8bbf\u95ee\u5730\u5740"} |
| custom_domain_url | models.URLField | 1 | {"blank": true, "null": true, "verbose_name": "\u7ed1\u5b9a\u7684\u72ec\u7acb\u57df\u540d\u8bbf\u95ee\u5730\u5740"} |
| prefer_https | models.BooleanField | 1 | {"null": true, "verbose_name": "[deprecated] \u4ec5\u4e3a False \u65f6\u5f3a\u5236\u4f7f\u7528 http, \u5426\u5219\u4fdd\u6301\u4e0e\u96c6\u7fa4 https_enabled \u72b6\u6001\u4e00\u81f4"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.OneToOneField | `Application` | market_config | `models.CASCADE` |
| source_module | models.ForeignKey | `Module` | 不适用 | `models.CASCADE` |


---


### TagMap

**模块**: `apiserver.paasng.paasng.accessories.publish.sync_market.models`  
**行号**: 1  
**基类**: django_models.Model  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| remote_id | django_models.IntegerField | 1 | {"db_index": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| tag | django_models.OneToOneField | `market_models.Tag` | 不适用 | `django_models.CASCADE` |


---


### ServiceModuleAttachment

**模块**: `apiserver.paasng.paasng.accessories.servicehub.models`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: Module <-> Local Service relationship

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|

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
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| credentials_enabled | models.BooleanField | 1 | {"default": true, "verbose_name": "\u662f\u5426\u4f7f\u7528\u51ed\u8bc1"} |

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
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: Binding relationship of module <-> remote service

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| service_id | models.UUIDField | 1 | {"verbose_name": "\u8fdc\u7a0b\u589e\u5f3a\u670d\u52a1 ID"} |

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
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: Binding relationship of engine app <-> remote service plan

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| service_id | models.UUIDField | 1 | {"verbose_name": "\u8fdc\u7a0b\u589e\u5f3a\u670d\u52a1 ID"} |
| plan_id | models.UUIDField | 1 | {"verbose_name": "\u8fdc\u7a0b\u589e\u5f3a\u670d\u52a1 Plan ID"} |
| service_instance_id | models.UUIDField | 1 | {"null": true} |
| credentials_enabled | models.BooleanField | 1 | {"default": true, "verbose_name": "\u662f\u5426\u4f7f\u7528\u51ed\u8bc1"} |

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
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: Share a service binding relationship from other modules

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| service_type | models.CharField | 1 | {"max_length": 16, "verbose_name": "\u589e\u5f3a\u670d\u52a1\u7c7b\u578b"} |
| service_id | models.UUIDField | 1 | {"verbose_name": "\u589e\u5f3a\u670d\u52a1 ID"} |
| ref_attachment_pk | models.IntegerField | 1 | {"verbose_name": "\u88ab\u5171\u4eab\u7684\u670d\u52a1\u7ed1\u5b9a\u5173\u7cfb\u4e3b\u952e"} |

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
**行号**: 1  
**基类**: models.Model  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| sort_priority | models.IntegerField | 1 | {"default": 0} |



---


### Service

**模块**: `apiserver.paasng.paasng.accessories.services.models`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| region | models.CharField | 1 | {"max_length": 32} |
| name | models.CharField | 1 | {"max_length": 64, "verbose_name": "\u670d\u52a1\u540d\u79f0"} |
| logo_b64 | models.TextField | 1 | {"blank": true, "null": true, "verbose_name": "\u670d\u52a1 logo \u7684\u5730\u5740, \u652f\u6301base64\u683c\u5f0f"} |
| available_languages | models.CharField | 1 | {"blank": true, "max_length": 1024, "null": true, "verbose_name": "\u652f\u6301\u7f16\u7a0b\u8bed\u8a00"} |
| is_active | models.BooleanField | 1 | {"default": true, "verbose_name": "\u662f\u5426\u53ef\u7528"} |
| is_visible | models.BooleanField | 1 | {"default": true, "verbose_name": "\u662f\u5426\u53ef\u89c1"} |

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
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| to_be_deleted | models.BooleanField | 1 | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| service | models.ForeignKey | Service | 不适用 | `models.CASCADE` |
| plan | models.ForeignKey | Plan | 不适用 | `models.CASCADE` |


---


### PreCreatedInstance

**模块**: `apiserver.paasng.paasng.accessories.services.models`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  
**描述**: 预创建的服务实例

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| is_allocated | models.BooleanField | 1 | {"default": false, "help_text": "\u5b9e\u4f8b\u662f\u5426\u5df2\u88ab\u5206\u914d"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plan | models.ForeignKey | Plan | 不适用 | `models.SET_NULL` |


---


### Plan

**模块**: `apiserver.paasng.paasng.accessories.services.models`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 64} |
| description | models.CharField | 1 | {"blank": true, "max_length": 1024, "verbose_name": "\u65b9\u6848\u7b80\u4ecb"} |
| is_active | models.BooleanField | 1 | {"default": true, "verbose_name": "\u662f\u5426\u53ef\u7528"} |

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
**行号**: 1  
**基类**: models.Model  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| namespace | models.CharField | 1 | {"max_length": 32} |
| uid | models.CharField | 1 | {"db_index": true, "max_length": 64, "null": false, "unique": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('namespace', 'uid') |

---


### AppModuleTagRel

**模块**: `apiserver.paasng.paasng.accessories.smart_advisor.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: A M2M relationship table for storing the relationship between application module and AppTag

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| tag_str | models.CharField | 1 | {"blank": false, "max_length": 128} |
| source | models.CharField | 1 | {"blank": false, "max_length": 32} |
| created | models.DateTimeField | 1 | {"auto_now_add": true} |

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
**行号**: 1  
**基类**: models.Model  
**描述**: Links from document systems including blueking doc and other opensource documentations

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| location | models.CharField | 1 | {"blank": false, "max_length": 256} |
| priority | models.IntegerField | 1 | {"default": 1} |
| created | models.DateTimeField | 1 | {"default": "`timezone.now`"} |



---


### DeployFailurePattern

**模块**: `apiserver.paasng.paasng.accessories.smart_advisor.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: Stores common failure patterns for failed deployments

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| type | models.IntegerField | 1 | {"default": "`DeployFailurePatternType.REGULAR_EXPRESSION`"} |
| value | models.CharField | 1 | {"blank": false, "max_length": 2048} |
| tag_str | models.CharField | 1 | {"blank": false, "max_length": 128} |
| created | models.DateTimeField | 1 | {"default": "`timezone.now`"} |



---


### BkPluginProfile

**模块**: `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: Profile which storing extra information for BkPlugins

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| introduction | models.CharField | 1 | {"blank": true, "help_text": "\u63d2\u4ef6\u7b80\u4ecb", "max_length": 512, "null": true} |
| contact | models.CharField | 1 | {"blank": true, "help_text": "\u4f7f\u7528 ; \u5206\u9694\u7684\u7528\u6237\u540d", "max_length": 128, "null": true} |
| api_gw_name | models.CharField | 1 | {"blank": true, "help_text": "\u4e3a\u7a7a\u65f6\u8868\u793a\u4ece\u672a\u6210\u529f\u540c\u6b65\u8fc7\uff0c\u6682\u65e0\u5df2\u7ed1\u5b9a\u7f51\u5173", "max_length": 32, "null": true} |
| api_gw_id | models.IntegerField | 1 | {"null": true} |
| api_gw_last_synced_at | models.DateTimeField | 1 | {"null": true} |
| pre_distributor_codes | models.JSONField | 1 | {"blank": true, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.OneToOneField | `Application` | bk_plugin_profile | `models.CASCADE` |
| tag | models.ForeignKey | BkPluginTag | 不适用 | `models.SET_NULL` |


---


### BkPluginDistributor

**模块**: `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: A "Distributor" is responsible for providing a collection of BkPlugins to a group of users,

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u4f7f\u7528\u65b9\u540d\u79f0", "max_length": 32, "unique": true} |
| code_name | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u4f7f\u7528\u65b9\u7684\u82f1\u6587\u4ee3\u53f7\uff0c\u53ef\u66ff\u4ee3\u4e3b\u952e\u4f7f\u7528", "max_length": 32, "unique": true} |
| bk_app_code | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u4f7f\u7528\u65b9\u6240\u7ed1\u5b9a\u7684\u84dd\u9cb8\u5e94\u7528\u4ee3\u53f7", "max_length": 20, "unique": true} |
| introduction | models.CharField | 1 | {"blank": true, "max_length": 512, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plugins | models.ManyToManyField | `Application` | distributors | 不适用 |


---


### BkPluginTag

**模块**: `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: Plugins and applications use different markets, and plugins should have their own separate tags

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u4f7f\u7528\u65b9\u540d\u79f0", "max_length": 32, "unique": true} |
| code_name | models.CharField | 1 | {"help_text": "\u5206\u7c7b\u82f1\u6587\u540d\u79f0\uff0c\u53ef\u66ff\u4ee3\u4e3b\u952e\u4f7f\u7528", "max_length": 32, "unique": true} |
| priority | models.IntegerField | 1 | {"default": 0, "help_text": "\u6570\u5b57\u8d8a\u5927\uff0c\u4f18\u5148\u7ea7\u8d8a\u9ad8"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ['-priority', 'name'] |

---


### PluginGradeManager

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| pd_id | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u7c7b\u578b\u6807\u8bc6", "max_length": 64} |
| plugin_id | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u6807\u8bc6", "max_length": 32} |
| grade_manager_id | models.IntegerField | 1 | {"help_text": "\u5206\u7ea7\u7ba1\u7406\u5458 ID"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('pd_id', 'plugin_id', 'grade_manager_id') |

---


### PluginUserGroup

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| pd_id | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u7c7b\u578b\u6807\u8bc6", "max_length": 64} |
| plugin_id | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u6807\u8bc6", "max_length": 32} |
| role | models.IntegerField | 1 | {"default": "`PluginRole.DEVELOPER.value`"} |
| user_group_id | models.IntegerField | 1 | {"help_text": "\u6743\u9650\u4e2d\u5fc3\u7528\u6237\u7ec4 ID"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('pd_id', 'plugin_id', 'role') |

---


### PluginDefinition

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| identifier | models.CharField | 1 | {"max_length": 64, "unique": true} |
| docs | models.CharField | 1 | {"max_length": 255} |
| logo | models.CharField | 1 | {"max_length": 255} |
| administrator | models.JSONField | 1 | {} |



---


### PluginBasicInfoDefinition

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| access_mode | models.CharField | 1 | {"default": "`PluginBasicInfoAccessMode.READWRITE`", "max_length": 16, "verbose_name": "\u57fa\u672c\u4fe1\u606f\u67e5\u770b\u6a21\u5f0f"} |
| release_method | models.CharField | 1 | {"max_length": 16, "verbose_name": "\u53d1\u5e03\u65b9\u5f0f"} |
| repository_group | models.CharField | 1 | {"max_length": 255, "verbose_name": "\u63d2\u4ef6\u4ee3\u7801\u521d\u59cb\u5316\u4ed3\u5e93\u7ec4"} |
| extra_fields_order | models.JSONField | 1 | {"default": "`list`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| pd | models.OneToOneField | `PluginDefinition` | basic_info_definition | `models.CASCADE` |


---


### PluginMarketInfoDefinition

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| storage | models.CharField | 1 | {"max_length": 16, "verbose_name": "\u5b58\u50a8\u65b9\u5f0f"} |
| extra_fields_order | models.JSONField | 1 | {"default": "`list`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| pd | models.OneToOneField | `PluginDefinition` | market_info_definition | `models.CASCADE` |


---


### PluginConfigInfoDefinition

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| docs | models.CharField | 1 | {"default": "", "max_length": 255} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| pd | models.OneToOneField | `PluginDefinition` | config_definition | `models.CASCADE` |


---


### PluginVisibleRangeDefinition

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| pd | models.OneToOneField | `PluginDefinition` | visible_range_definition | `models.CASCADE` |


---


### PluginInstance

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  
**描述**: 插件实例

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| id | models.CharField | 1 | {"help_text": "\u63d2\u4ef6id", "max_length": 32} |
| extra_fields | models.JSONField | 1 | {"verbose_name": "\u989d\u5916\u5b57\u6bb5"} |
| language | models.CharField | 1 | {"help_text": "\u5197\u4f59\u5b57\u6bb5, \u7528\u4e8e\u51cf\u5c11\u67e5\u8be2\u6b21\u6570", "max_length": 16, "verbose_name": "\u5f00\u53d1\u8bed\u8a00"} |
| repo_type | models.CharField | 1 | {"max_length": 16, "null": true, "verbose_name": "\u6e90\u7801\u6258\u7ba1\u7c7b\u578b"} |
| repository | models.CharField | 1 | {"max_length": 255} |
| status | models.CharField | 1 | {"choices": "`constants.PluginStatus.get_choices()`", "default": "`constants.PluginStatus.WAITING_APPROVAL`", "max_length": 16, "verbose_name": "\u63d2\u4ef6\u72b6\u6001"} |
| publisher | models.CharField | 1 | {"default": "", "max_length": 64, "verbose_name": "\u63d2\u4ef6\u53d1\u5e03\u8005"} |
| is_deleted | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u5df2\u5220\u9664"} |

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
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 插件市场信息

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| category | models.CharField | 1 | {"db_index": true, "max_length": 64, "verbose_name": "\u5206\u7c7b"} |
| contact | models.TextField | 1 | {"help_text": "\u4ee5\u5206\u53f7(;)\u5206\u5272", "verbose_name": "\u8054\u7cfb\u4eba"} |
| extra_fields | models.JSONField | 1 | {"verbose_name": "\u989d\u5916\u5b57\u6bb5"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plugin | models.OneToOneField | `PluginInstance` | 不适用 | `models.CASCADE` |


---


### PluginRelease

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 插件发布版本

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| type | models.CharField | 1 | {"choices": "`constants.PluginReleaseType.get_choices()`", "max_length": 16, "verbose_name": "\u7248\u672c\u7c7b\u578b(\u6b63\u5f0f/\u6d4b\u8bd5)"} |
| version | models.CharField | 1 | {"max_length": 255, "verbose_name": "\u7248\u672c\u53f7"} |
| comment | models.TextField | 1 | {"verbose_name": "\u7248\u672c\u65e5\u5fd7"} |
| extra_fields | models.JSONField | 1 | {"verbose_name": "\u989d\u5916\u5b57\u6bb5"} |
| semver_type | models.CharField | 1 | {"help_text": "\u8be5\u5b57\u6bb5\u53ea\u7528\u4e8e\u81ea\u52a8\u751f\u6210\u7248\u672c\u53f7\u7684\u63d2\u4ef6", "max_length": 16, "null": true, "verbose_name": "\u8bed\u4e49\u5316\u7248\u672c\u7c7b\u578b"} |
| source_location | models.CharField | 1 | {"max_length": 2048, "verbose_name": "\u4ee3\u7801\u4ed3\u5e93\u5730\u5740"} |
| source_version_type | models.CharField | 1 | {"max_length": 128, "null": true, "verbose_name": "\u4ee3\u7801\u7248\u672c\u7c7b\u578b(branch/tag)"} |
| source_version_name | models.CharField | 1 | {"max_length": 128, "null": true, "verbose_name": "\u4ee3\u7801\u5206\u652f\u540d/tag\u540d"} |
| source_hash | models.CharField | 1 | {"max_length": 128, "verbose_name": "\u4ee3\u7801\u63d0\u4ea4\u54c8\u5e0c"} |
| status | models.CharField | 1 | {"default": "`constants.PluginReleaseStatus.INITIAL`", "max_length": 16} |
| tag | models.CharField | 1 | {"db_index": true, "max_length": 16, "null": true, "verbose_name": "\u6807\u7b7e"} |
| retryable | models.BooleanField | 1 | {"default": true, "help_text": "\u5931\u8d25\u540e\u662f\u5426\u53ef\u91cd\u8bd5"} |
| is_rolled_back | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u5df2\u56de\u6eda"} |
| gray_status | models.CharField | 1 | {"default": "`constants.GrayReleaseStatus.IN_GRAY`", "max_length": 32, "verbose_name": "\u7070\u5ea6\u53d1\u5e03\u72b6\u6001"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plugin | models.ForeignKey | `PluginInstance` | all_versions | `models.CASCADE` |
| current_stage | models.OneToOneField | PluginReleaseStage | 不适用 | `models.SET_NULL` |


---


### PluginReleaseStage

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 插件发布阶段

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| stage_id | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u9636\u6bb5\u6807\u8bc6"} |
| stage_name | models.CharField | 1 | {"help_text": "\u5197\u4f59\u5b57\u6bb5, \u7528\u4e8e\u51cf\u5c11\u67e5\u8be2\u6b21\u6570", "max_length": 16, "verbose_name": "\u9636\u6bb5\u540d\u79f0"} |
| invoke_method | models.CharField | 1 | {"help_text": "\u5197\u4f59\u5b57\u6bb5, \u7528\u4e8e\u51cf\u5c11\u67e5\u8be2\u6b21\u6570", "max_length": 16, "verbose_name": "\u89e6\u53d1\u65b9\u5f0f"} |
| status_polling_method | models.CharField | 1 | {"default": "`constants.StatusPollingMethod.API`", "help_text": "\u5197\u4f59\u5b57\u6bb5, \u7528\u4e8e\u51cf\u5c11\u67e5\u8be2\u6b21\u6570", "max_length": 16, "verbose_name": "\u9636\u6bb5\u7684\u72b6\u6001\u8f6e\u8be2\u65b9\u5f0f"} |
| status | models.CharField | 1 | {"default": "`constants.PluginReleaseStatus.INITIAL`", "max_length": 16, "verbose_name": "\u53d1\u5e03\u72b6\u6001"} |
| fail_message | models.TextField | 1 | {"verbose_name": "\u9519\u8bef\u539f\u56e0"} |
| api_detail | models.JSONField | 1 | {"help_text": "\u8be5\u5b57\u6bb5\u4ec5 invoke_method = api \u65f6\u53ef\u7528", "null": true, "verbose_name": "API \u8be6\u60c5"} |
| pipeline_detail | models.JSONField | 1 | {"default": null, "help_text": "\u8be5\u5b57\u6bb5\u4ec5 invoke_method = pipeline \u65f6\u53ef\u7528", "null": true, "verbose_name": "\u6d41\u6c34\u7ebf\u6784\u5efa\u8be6\u60c5"} |
| operator | models.CharField | 1 | {"max_length": 32, "null": true, "verbose_name": "\u64cd\u4f5c\u4eba"} |

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
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 插件版本的发布策略

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| strategy | models.CharField | 1 | {"choices": "`constants.ReleaseStrategy.get_choices()`", "max_length": 32, "verbose_name": "\u53d1\u5e03\u7b56\u7565"} |
| bkci_project | models.JSONField | 1 | {"blank": true, "help_text": "\u683c\u5f0f\uff1a[\u00271111\u0027, \u0027222222\u0027]", "null": true, "verbose_name": "\u84dd\u76fe\u9879\u76eeID"} |
| organization | models.JSONField | 1 | {"blank": true, "null": true, "verbose_name": "\u7ec4\u7ec7\u67b6\u6784"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| release | models.ForeignKey | `PluginRelease` | release_strategies | `models.CASCADE` |


---


### ApprovalService

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  
**描述**: 审批服务信息

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| service_name | models.CharField | 1 | {"max_length": 64, "unique": true, "verbose_name": "\u5ba1\u6279\u670d\u52a1\u540d\u79f0"} |
| service_id | models.IntegerField | 1 | {"help_text": "\u7528\u4e8e\u5728 ITSM \u4e0a\u63d0\u7533\u8bf7\u5355\u636e", "verbose_name": "\u5ba1\u6279\u670d\u52a1ID"} |



---


### PluginConfig

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 插件配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| unique_key | models.CharField | 1 | {"max_length": 64, "verbose_name": "\u552f\u4e00\u6807\u8bc6"} |
| row | models.JSONField | 1 | {"default": "`dict`", "verbose_name": "\u914d\u7f6e\u5185\u5bb9(1\u884c), \u683c\u5f0f {\u0027column_key\u0027: \u0027value\u0027}"} |

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
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 插件可见范围

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| bkci_project | models.JSONField | 1 | {"default": "`list`", "verbose_name": "\u84dd\u76fe\u9879\u76eeID"} |
| organization | models.JSONField | 1 | {"blank": true, "null": true, "verbose_name": "\u7ec4\u7ec7\u67b6\u6784"} |
| is_in_approval | models.BooleanField | 1 | {"default": false, "verbose_name": "\u662f\u5426\u5728\u5ba1\u6279\u4e2d"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plugin | models.OneToOneField | `PluginInstance` | visible_range | `models.CASCADE` |


---


### OperationRecord

**模块**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 插件操作记录

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| action | models.CharField | 1 | {"choices": "`constants.ActionTypes.get_choices()`", "max_length": 32} |
| specific | models.CharField | 1 | {"max_length": 255, "null": true} |
| subject | models.CharField | 1 | {"choices": "`constants.SubjectTypes.get_choices()`", "max_length": 32} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| plugin | models.ForeignKey | `PluginInstance` | 不适用 | `models.CASCADE` |


---


### UserPrivateToken

**模块**: `apiserver.paasng.paasng.infras.accounts.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: Private token can be used to authenticate an user, these tokens usually have very long

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| token | models.CharField | 1 | {"max_length": 64, "unique": true} |
| expires_at | models.DateTimeField | 1 | {"blank": true, "null": true} |
| is_active | models.BooleanField | 1 | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| user | models.ForeignKey | `User` | 不适用 | `models.CASCADE` |


---


### UserProfile

**模块**: `apiserver.paasng.paasng.infras.accounts.models`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: Profile field for user

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| role | models.IntegerField | 1 | {"default": "`SiteRole.USER.value`"} |
| feature_flags | models.TextField | 1 | {"blank": true, "null": true} |



---


### Oauth2TokenHolder

**模块**: `apiserver.paasng.paasng.infras.accounts.models`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: OAuth2 Token for sourcectl

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| provider | models.CharField | 1 | {"max_length": 32} |
| token_type | models.CharField | 1 | {"max_length": 16} |
| expire_at | models.DateTimeField | 1 | {"blank": true, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| user | models.ForeignKey | `UserProfile` | token_holder | `models.CASCADE` |


---


### PrivateTokenHolder

**模块**: `apiserver.paasng.paasng.infras.accounts.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: Private Token for sourcectl

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| provider | models.CharField | 1 | {"max_length": 32} |
| expire_at | models.DateTimeField | 1 | {"blank": true, "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| user | models.ForeignKey | `UserProfile` | private_token_holder | `models.CASCADE` |


---


### AccountFeatureFlag

**模块**: `apiserver.paasng.paasng.infras.accounts.models`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| effect | models.BooleanField | 1 | {"default": true} |
| name | models.CharField | 1 | {"max_length": 64} |



---


### AuthenticatedAppAsUser

**模块**: `apiserver.paasng.paasng.infras.accounts.models`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: Store relationships which treat an authenticated(by API Gateway) app as an regular user,

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| bk_app_code | models.CharField | 1 | {"max_length": 64, "unique": true} |
| is_active | models.BooleanField | 1 | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| user | models.ForeignKey | `User` | 不适用 | `models.CASCADE` |


---


### BKMonitorSpace

**模块**: `apiserver.paasng.paasng.infras.bkmonitorv3.models`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| id | models.IntegerField | 1 | {"verbose_name": "\u84dd\u9cb8\u76d1\u63a7\u7a7a\u95f4 id"} |
| space_type_id | models.CharField | 1 | {"max_length": 48, "verbose_name": "\u7a7a\u95f4\u7c7b\u578bid"} |
| space_id | models.CharField | 1 | {"help_text": "\u540c\u4e00\u7a7a\u95f4\u7c7b\u578b\u4e0b\u552f\u4e00", "max_length": 48, "verbose_name": "\u7a7a\u95f4id"} |
| space_name | models.CharField | 1 | {"max_length": 64, "verbose_name": "\u7a7a\u95f4\u540d\u79f0"} |
| space_uid | models.CharField | 1 | {"help_text": "{space_type_id}__{space_id}", "max_length": 48, "verbose_name": "\u84dd\u9cb8\u76d1\u63a7\u7a7a\u95f4 uid"} |
| extra_info | models.JSONField | 1 | {"help_text": "\u84dd\u9cb8\u76d1\u63a7API-metadata_get_space_detail \u7684\u539f\u59cb\u8fd4\u56de\u503c"} |

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
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| app_code | models.CharField | 1 | {"help_text": "\u5e94\u7528\u4ee3\u53f7", "max_length": 20} |
| grade_manager_id | models.IntegerField | 1 | {"help_text": "\u5206\u7ea7\u7ba1\u7406\u5458 ID"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('app_code', 'grade_manager_id') |

---


### ApplicationUserGroup

**模块**: `apiserver.paasng.paasng.infras.iam.members.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| app_code | models.CharField | 1 | {"help_text": "\u5e94\u7528\u4ee3\u53f7", "max_length": 20} |
| role | models.IntegerField | 1 | {"default": "`ApplicationRole.DEVELOPER.value`"} |
| user_group_id | models.IntegerField | 1 | {"help_text": "\u6743\u9650\u4e2d\u5fc3\u7528\u6237\u7ec4 ID"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('app_code', 'role') |

---


### OAuth2Client

**模块**: `apiserver.paasng.paasng.infras.oauth2.models`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: OAuth2 体系中的基本单位：Client

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| client_id | models.CharField | 1 | {"max_length": 20, "unique": true, "verbose_name": "\u5e94\u7528\u7f16\u7801"} |



---


### BkAppSecretInEnvVar

**模块**: `apiserver.paasng.paasng.infras.oauth2.models`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| bk_app_code | models.CharField | 1 | {"max_length": 20, "unique": true} |
| bk_app_secret_id | models.IntegerField | 1 | {"help_text": "\u4e0d\u5b58\u50a8\u5bc6\u94a5\u7684\u4fe1\u606f\uff0c\u4ec5\u5b58\u50a8\u5bc6\u94a5 ID", "verbose_name": "\u5e94\u7528\u5bc6\u94a5\u7684 ID"} |



---


### BaseOperation

**模块**: `apiserver.paasng.paasng.misc.audit.models`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| start_time | models.DateTimeField | 1 | {"auto_now_add": true, "db_index": true, "verbose_name": "\u5f00\u59cb\u65f6\u95f4"} |
| end_time | models.DateTimeField | 1 | {"help_text": "\u4ec5\u9700\u8981\u540e\u53f0\u6267\u884c\u7684\u7684\u64cd\u4f5c\u624d\u9700\u8981\u8bb0\u5f55\u7ed3\u675f\u65f6\u95f4", "null": true} |
| access_type | models.IntegerField | 1 | {"choices": "`AccessType.get_choices()`", "default": "`AccessType.WEB`", "verbose_name": "\u8bbf\u95ee\u65b9\u5f0f"} |
| result_code | models.IntegerField | 1 | {"choices": "`ResultCode.get_choices()`", "default": "`ResultCode.SUCCESS`", "verbose_name": "\u64cd\u4f5c\u7ed3\u679c"} |
| data_before | models.JSONField | 1 | {"blank": true, "null": true, "verbose_name": "\u64cd\u4f5c\u524d\u7684\u6570\u636e"} |
| data_after | models.JSONField | 1 | {"blank": true, "null": true, "verbose_name": "\u64cd\u4f5c\u540e\u7684\u6570\u636e"} |
| operation | models.CharField | 1 | {"choices": "`OperationEnum.get_choices()`", "max_length": 32, "verbose_name": "\u64cd\u4f5c\u7c7b\u578b"} |
| target | models.CharField | 1 | {"choices": "`OperationTarget.get_choices()`", "max_length": 32, "verbose_name": "\u64cd\u4f5c\u5bf9\u8c61"} |
| attribute | models.CharField | 1 | {"blank": true, "help_text": "\u5982\u589e\u5f3a\u670d\u52a1\u7684\u5c5e\u6027\u53ef\u4ee5\u4e3a\uff1amysql\u3001bkrepo", "max_length": 32, "null": true, "verbose_name": "\u5bf9\u8c61\u5c5e\u6027"} |
| module_name | models.CharField | 1 | {"blank": true, "max_length": 32, "null": true, "verbose_name": "\u6a21\u5757\u540d\uff0c\u975e\u5fc5\u586b"} |
| environment | models.CharField | 1 | {"blank": true, "choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": true, "verbose_name": "\u73af\u5883\uff0c\u975e\u5fc5\u586b"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### AdminOperationRecord

**模块**: `apiserver.paasng.paasng.misc.audit.models`  
**行号**: 1  
**基类**: apiserver.paasng.paasng.misc.audit.models.BaseOperation  
**描述**: 后台管理操作记录，用于记录平台管理员在 Admin 系统上的操作

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| app_code | models.CharField | 1 | {"blank": true, "max_length": 32, "null": true, "verbose_name": "\u5e94\u7528ID, \u975e\u5fc5\u586b"} |
| start_time | models.DateTimeField | 1 | {"auto_now_add": true, "db_index": true, "verbose_name": "\u5f00\u59cb\u65f6\u95f4"} |
| end_time | models.DateTimeField | 1 | {"help_text": "\u4ec5\u9700\u8981\u540e\u53f0\u6267\u884c\u7684\u7684\u64cd\u4f5c\u624d\u9700\u8981\u8bb0\u5f55\u7ed3\u675f\u65f6\u95f4", "null": true} |
| access_type | models.IntegerField | 1 | {"choices": "`AccessType.get_choices()`", "default": "`AccessType.WEB`", "verbose_name": "\u8bbf\u95ee\u65b9\u5f0f"} |
| result_code | models.IntegerField | 1 | {"choices": "`ResultCode.get_choices()`", "default": "`ResultCode.SUCCESS`", "verbose_name": "\u64cd\u4f5c\u7ed3\u679c"} |
| data_before | models.JSONField | 1 | {"blank": true, "null": true, "verbose_name": "\u64cd\u4f5c\u524d\u7684\u6570\u636e"} |
| data_after | models.JSONField | 1 | {"blank": true, "null": true, "verbose_name": "\u64cd\u4f5c\u540e\u7684\u6570\u636e"} |
| operation | models.CharField | 1 | {"choices": "`OperationEnum.get_choices()`", "max_length": 32, "verbose_name": "\u64cd\u4f5c\u7c7b\u578b"} |
| target | models.CharField | 1 | {"choices": "`OperationTarget.get_choices()`", "max_length": 32, "verbose_name": "\u64cd\u4f5c\u5bf9\u8c61"} |
| attribute | models.CharField | 1 | {"blank": true, "help_text": "\u5982\u589e\u5f3a\u670d\u52a1\u7684\u5c5e\u6027\u53ef\u4ee5\u4e3a\uff1amysql\u3001bkrepo", "max_length": 32, "null": true, "verbose_name": "\u5bf9\u8c61\u5c5e\u6027"} |
| module_name | models.CharField | 1 | {"blank": true, "max_length": 32, "null": true, "verbose_name": "\u6a21\u5757\u540d\uff0c\u975e\u5fc5\u586b"} |
| environment | models.CharField | 1 | {"blank": true, "choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": true, "verbose_name": "\u73af\u5883\uff0c\u975e\u5fc5\u586b"} |



---


### AppOperationRecord

**模块**: `apiserver.paasng.paasng.misc.audit.models`  
**行号**: 1  
**基类**: apiserver.paasng.paasng.misc.audit.models.BaseOperation  
**描述**: 应用操作记录，用于记录应用开发者的操作，需要同步记录应用的权限数据，并可以选择是否将数据上报到审计中心

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| app_code | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u5e94\u7528ID, \u5fc5\u586b"} |
| action_id | models.CharField | 1 | {"blank": true, "choices": "`AppAction.get_choices()`", "help_text": "action_id \u4e3a\u7a7a\u5219\u4e0d\u4f1a\u5c06\u6570\u636e\u4e0a\u62a5\u5230\u5ba1\u8ba1\u4e2d\u5fc3", "max_length": 32, "null": true} |
| resource_type_id | models.CharField | 1 | {"choices": "`ResourceType.get_choices()`", "default": "`ResourceType.Application`", "help_text": "\u5f00\u53d1\u8005\u4e2d\u5fc3\u6ce8\u518c\u7684\u8d44\u6e90\u90fd\u4e3a\u84dd\u9cb8\u5e94\u7528", "max_length": 32} |
| start_time | models.DateTimeField | 1 | {"auto_now_add": true, "db_index": true, "verbose_name": "\u5f00\u59cb\u65f6\u95f4"} |
| end_time | models.DateTimeField | 1 | {"help_text": "\u4ec5\u9700\u8981\u540e\u53f0\u6267\u884c\u7684\u7684\u64cd\u4f5c\u624d\u9700\u8981\u8bb0\u5f55\u7ed3\u675f\u65f6\u95f4", "null": true} |
| access_type | models.IntegerField | 1 | {"choices": "`AccessType.get_choices()`", "default": "`AccessType.WEB`", "verbose_name": "\u8bbf\u95ee\u65b9\u5f0f"} |
| result_code | models.IntegerField | 1 | {"choices": "`ResultCode.get_choices()`", "default": "`ResultCode.SUCCESS`", "verbose_name": "\u64cd\u4f5c\u7ed3\u679c"} |
| data_before | models.JSONField | 1 | {"blank": true, "null": true, "verbose_name": "\u64cd\u4f5c\u524d\u7684\u6570\u636e"} |
| data_after | models.JSONField | 1 | {"blank": true, "null": true, "verbose_name": "\u64cd\u4f5c\u540e\u7684\u6570\u636e"} |
| operation | models.CharField | 1 | {"choices": "`OperationEnum.get_choices()`", "max_length": 32, "verbose_name": "\u64cd\u4f5c\u7c7b\u578b"} |
| target | models.CharField | 1 | {"choices": "`OperationTarget.get_choices()`", "max_length": 32, "verbose_name": "\u64cd\u4f5c\u5bf9\u8c61"} |
| attribute | models.CharField | 1 | {"blank": true, "help_text": "\u5982\u589e\u5f3a\u670d\u52a1\u7684\u5c5e\u6027\u53ef\u4ee5\u4e3a\uff1amysql\u3001bkrepo", "max_length": 32, "null": true, "verbose_name": "\u5bf9\u8c61\u5c5e\u6027"} |
| module_name | models.CharField | 1 | {"blank": true, "max_length": 32, "null": true, "verbose_name": "\u6a21\u5757\u540d\uff0c\u975e\u5fc5\u586b"} |
| environment | models.CharField | 1 | {"blank": true, "choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": true, "verbose_name": "\u73af\u5883\uff0c\u975e\u5fc5\u586b"} |



---


### AppLatestOperationRecord

**模块**: `apiserver.paasng.paasng.misc.audit.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: 应用最近操作的映射表，可方便快速查询应用的最近操作者，并按最近操作时间进行排序等操作

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| latest_operated_at | models.DateTimeField | 1 | {"db_index": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.OneToOneField | `Application` | latest_op_record | `models.CASCADE` |
| operation | models.OneToOneField | `AppOperationRecord` | 不适用 | `models.CASCADE` |


---


### AppAlertRule

**模块**: `apiserver.paasng.paasng.misc.monitoring.monitor.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 记录 app 初始的告警规则配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| alert_code | models.CharField | 1 | {"help_text": "alert rule code e.g. high_cpu_usage", "max_length": 64} |
| display_name | models.CharField | 1 | {"max_length": 512} |
| enabled | models.BooleanField | 1 | {"default": true} |
| threshold_expr | models.CharField | 1 | {"max_length": 64} |
| receivers | models.JSONField | 1 | {"default": "`list`"} |
| environment | models.CharField | 1 | {"max_length": 16, "verbose_name": "\u90e8\u7f72\u73af\u5883"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | applications.Application | alert_rules | `models.CASCADE` |
| module | models.ForeignKey | modules.Module | alert_rules | `models.CASCADE` |


---


### AppDashboardTemplate

**模块**: `apiserver.paasng.paasng.misc.monitoring.monitor.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 仪表盘模板，只需要记录名称和版本号，模板的内容在蓝鲸监控侧维护

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"help_text": "\u4e0e\u84dd\u9cb8\u76d1\u63a7\u7ea6\u5b9a\u7684\u4eea\u8868\u76d8\u540d\u79f0\uff0c\u5982\uff1abksaas/framework-python\uff0c\u9700\u8981\u63d0\u524d\u5c06\u4eea\u8868\u76d8\u7684 JSON \u6587\u4ef6\u5185\u7f6e\u5230\u76d1\u63a7\u7684\u4ee3\u7801\u76ee\u5f55\u4e2d", "max_length": 64, "unique": true} |
| display_name | models.CharField | 1 | {"help_text": "\u4eea\u8868\u76d8\u5c55\u793a\u540d\u79f0\uff0c\u5982\uff1aPython \u5f00\u53d1\u6846\u67b6\u5185\u7f6e\u4eea\u8868\u76d8", "max_length": 512} |
| version | models.CharField | 1 | {"max_length": 32} |
| language | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u4eea\u8868\u76d8\u6240\u5c5e\u8bed\u8a00"} |
| is_plugin_template | models.BooleanField | 1 | {"default": false} |



---


### AppDashboard

**模块**: `apiserver.paasng.paasng.misc.monitoring.monitor.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 记录 APP 初始化的仪表盘信息

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"help_text": "\u4eea\u8868\u76d8\u540d\u79f0\uff0c\u5982\uff1abksaas/framework-python", "max_length": 64} |
| display_name | models.CharField | 1 | {"help_text": "\u4eea\u8868\u76d8\u5c55\u793a\u540d\u79f0\uff0c\u5982\uff1aPython \u5f00\u53d1\u6846\u67b6\u5185\u7f6e\u4eea\u8868\u76d8", "max_length": 512} |
| template_version | models.CharField | 1 | {"help_text": "\u6a21\u677f\u7248\u672c\u66f4\u65b0\u65f6\uff0c\u53ef\u4ee5\u6839\u636e\u8be5\u5b57\u6bb5\u4f5c\u4e3a\u6279\u91cf\u5237\u65b0\u4eea\u8868\u76d8", "max_length": 32} |
| language | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u4eea\u8868\u76d8\u6240\u5c5e\u8bed\u8a00"} |

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
**行号**: 1  
**基类**: models.Model  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| region | models.CharField | 1 | {"help_text": "\u90e8\u7f72\u533a\u57df", "max_length": 32} |
| created | models.DateTimeField | 1 | {"auto_now_add": true, "db_index": true} |
| type | models.SmallIntegerField | 1 | {"db_index": true, "help_text": "\u64cd\u4f5c\u7c7b\u578b"} |
| is_hidden | models.BooleanField | 1 | {"default": false, "help_text": "\u9690\u85cf\u8d77\u6765"} |
| source_object_id | models.CharField | 1 | {"blank": true, "default": "", "help_text": "\u4e8b\u4ef6\u6765\u6e90\u5bf9\u8c61ID\uff0c\u5177\u4f53\u6307\u5411\u9700\u8981\u6839\u636e\u64cd\u4f5c\u7c7b\u578b\u89e3\u6790", "max_length": 32, "null": true} |
| module_name | models.CharField | 1 | {"max_length": 20, "null": true, "verbose_name": "\u5173\u8054 Module"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |


---


### ApplicationLatestOp

**模块**: `apiserver.paasng.paasng.misc.operations.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: A mapper table which saves application's latest operation

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| operation_type | models.SmallIntegerField | 1 | {"help_text": "\u64cd\u4f5c\u7c7b\u578b"} |
| latest_operated_at | models.DateTimeField | 1 | {"db_index": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.OneToOneField | `Application` | latest_op | `models.CASCADE` |
| operation | models.OneToOneField | `Operation` | 不适用 | `models.CASCADE` |


---


### Application

**模块**: `apiserver.paasng.paasng.platform.applications.models`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: 蓝鲸应用

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| id | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |
| code | models.CharField | 1 | {"max_length": 20, "unique": true, "verbose_name": "\u5e94\u7528\u4ee3\u53f7"} |
| name | models.CharField | 1 | {"max_length": 20, "unique": true, "verbose_name": "\u5e94\u7528\u540d\u79f0"} |
| name_en | models.CharField | 1 | {"help_text": "\u76ee\u524d\u4ec5\u7528\u4e8e S-Mart \u5e94\u7528", "max_length": 20, "verbose_name": "\u5e94\u7528\u540d\u79f0(\u82f1\u6587)"} |
| type | models.CharField | 1 | {"db_index": true, "default": "`ApplicationType.DEFAULT.value`", "help_text": "\u4e0e\u5e94\u7528\u90e8\u7f72\u65b9\u5f0f\u76f8\u5173\u7684\u7c7b\u578b\u4fe1\u606f", "max_length": 16, "verbose_name": "\u5e94\u7528\u7c7b\u578b"} |
| is_smart_app | models.BooleanField | 1 | {"default": false, "verbose_name": "\u662f\u5426\u4e3a S-Mart \u5e94\u7528"} |
| is_scene_app | models.BooleanField | 1 | {"default": false, "verbose_name": "\u662f\u5426\u4e3a\u573a\u666f SaaS \u5e94\u7528"} |
| is_plugin_app | models.BooleanField | 1 | {"default": false, "help_text": "\u84dd\u9cb8\u5e94\u7528\u63d2\u4ef6\uff1a\u4f9b\u6807\u51c6\u8fd0\u7ef4\u3001ITSM \u7b49 SaaS \u4f7f\u7528\uff0c\u6709\u7279\u6b8a\u903b\u8f91", "verbose_name": "\u662f\u5426\u4e3a\u63d2\u4ef6\u5e94\u7528"} |
| is_ai_agent_app | models.BooleanField | 1 | {"default": false, "verbose_name": "\u662f\u5426\u4e3a AI Agent \u63d2\u4ef6\u5e94\u7528"} |
| language | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u7f16\u7a0b\u8bed\u8a00"} |
| is_active | models.BooleanField | 1 | {"default": true, "verbose_name": "\u662f\u5426\u6d3b\u8dc3"} |
| is_deleted | models.BooleanField | 1 | {"default": false} |
| last_deployed_date | models.DateTimeField | 1 | {"null": true, "verbose_name": "\u6700\u8fd1\u90e8\u7f72\u65f6\u95f4"} |



---


### ApplicationMembership

**模块**: `apiserver.paasng.paasng.platform.applications.models`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: [deprecated] 切换为权限中心用户组存储用户信息

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| role | models.IntegerField | 1 | {"default": "`ApplicationRole.DEVELOPER.value`"} |

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
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: 记录蓝鲸应用在不同部署环境下对应的 Engine App

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| environment | models.CharField | 1 | {"max_length": 16, "verbose_name": "\u90e8\u7f72\u73af\u5883"} |
| is_offlined | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u5df2\u7ecf\u4e0b\u7ebf\uff0c\u4ec5\u6210\u529f\u4e0b\u7ebf\u540e\u53d8\u4e3aFalse"} |

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
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| effect | models.BooleanField | 1 | {"default": true} |
| name | models.CharField | 1 | {"max_length": 30} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | feature_flag | `models.CASCADE` |


---


### UserMarkedApplication

**模块**: `apiserver.paasng.paasng.platform.applications.models`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|

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
**行号**: 1  
**基类**: models.Model  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| order | models.IntegerField | 1 | {"verbose_name": "\u987a\u5e8f"} |

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
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: 模块维度的进程定义, 表示模块当前所定义的进程, 该模型只通过 API 变更

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 32} |
| proc_command | models.TextField | 1 | {"help_text": "\u8fdb\u7a0b\u542f\u52a8\u547d\u4ee4(\u5305\u542b\u5b8c\u6574\u547d\u4ee4\u548c\u53c2\u6570\u7684\u5b57\u7b26\u4e32), \u53ea\u80fd\u4e0e command/args \u4e8c\u9009\u4e00", "null": true} |
| port | models.IntegerField | 1 | {"help_text": "[deprecated] \u5bb9\u5668\u7aef\u53e3", "null": true} |
| target_replicas | models.IntegerField | 1 | {"default": 1} |
| plan_name | models.CharField | 1 | {"help_text": "\u4ec5\u5b58\u50a8\u65b9\u6848\u540d\u79f0", "max_length": 32} |
| autoscaling | models.BooleanField | 1 | {"default": false} |

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
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: 进程定义中允许按环境覆盖的配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| environment_name | models.CharField | 1 | {"choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": false, "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| target_replicas | models.IntegerField | 1 | {"null": true} |
| plan_name | models.CharField | 1 | {"blank": true, "help_text": "\u4ec5\u5b58\u50a8\u65b9\u6848\u540d\u79f0", "max_length": 32, "null": true} |
| autoscaling | models.BooleanField | 1 | {"null": true} |

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
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: ProcessServicesFlag 主要用途是标记是否隐式需要 process services 配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| implicit_needed | models.BooleanField | 1 | {"default": false} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app_environment | models.OneToOneField | `ApplicationEnvironment` | 不适用 | `models.CASCADE` |


---


### ModuleDeployHook

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: 钩子命令

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| type | models.CharField | 1 | {"choices": "`DeployHookType.get_choices()`", "help_text": "\u94a9\u5b50\u7c7b\u578b", "max_length": 20} |
| proc_command | models.TextField | 1 | {"help_text": "\u8fdb\u7a0b\u542f\u52a8\u547d\u4ee4(\u5305\u542b\u5b8c\u6574\u547d\u4ee4\u548c\u53c2\u6570\u7684\u5b57\u7b26\u4e32), \u53ea\u80fd\u4e0e command/args \u4e8c\u9009\u4e00", "null": true} |
| enabled | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u5df2\u5f00\u542f"} |

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
**行号**: 1  
**基类**: paas_wl.utils.models.AuditedModel  
**描述**: 服务发现配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |


---


### DomainResolution

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**行号**: 1  
**基类**: paas_wl.utils.models.AuditedModel  
**描述**: 域名解析配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |


---


### ObservabilityConfig

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.OneToOneField | modules.Module | observability | `models.CASCADE` |


---


### BkAppManagedFields

**模块**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**行号**: 1  
**基类**: paas_wl.utils.models.TimestampedModel  
**描述**: This model stores the management status of the fields of a module's bkapp model, it's

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| manager | models.CharField | 1 | {"help_text": "\u7ba1\u7406\u8005\u7c7b\u578b", "max_length": 20} |
| fields | models.JSONField | 1 | {"default": [], "help_text": "\u6240\u7ba1\u7406\u7684\u5b57\u6bb5"} |

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
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: Application description object

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| code | models.CharField | 1 | {"db_index": true, "max_length": 20, "verbose_name": "ID of application"} |
| is_creation | models.BooleanField | 1 | {"default": false, "verbose_name": "whether current description creates an application"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | `Application` | declarative_config | `models.CASCADE` |


---


### DeploymentDescription

**模块**: `apiserver.paasng.paasng.platform.declarative.models`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: Config objects which describes deployment objects.

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| deployment | models.OneToOneField | `Deployment` | declarative_config | `models.CASCADE` |


---


### OperationVersionBase

**模块**: `apiserver.paasng.paasng.platform.engine.models.base`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: 带操作版本信息的BaseModel

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| id | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |
| source_type | models.CharField | 1 | {"max_length": 16, "null": true, "verbose_name": "\u6e90\u7801\u6258\u7ba1\u7c7b\u578b"} |
| source_location | models.CharField | 1 | {"max_length": 2048} |
| source_version_type | models.CharField | 1 | {"max_length": 64} |
| source_version_name | models.CharField | 1 | {"max_length": 64} |
| source_revision | models.CharField | 1 | {"max_length": 128, "null": true} |
| source_comment | models.TextField | 1 | {} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### EngineApp

**模块**: `apiserver.paasng.paasng.platform.engine.models.base`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: 蓝鲸应用引擎应用

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| id | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |
| name | models.CharField | 1 | {"max_length": 64, "unique": true} |
| region | models.CharField | 1 | {"max_length": 32} |
| is_active | models.BooleanField | 1 | {"default": true, "verbose_name": "\u662f\u5426\u6d3b\u8dc3"} |



---


### ConfigVar

**模块**: `apiserver.paasng.paasng.platform.engine.models.config_var`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: Config vars for application

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| is_global | models.BooleanField | 1 | {"default": false} |
| key | models.CharField | 1 | {"max_length": 128, "null": false} |
| value | models.TextField | 1 | {"null": false} |
| description | models.CharField | 1 | {"max_length": 200, "null": true} |
| is_builtin | models.BooleanField | 1 | {"default": false} |

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
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: Default config vars for global, can be added or edited in admin42.

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| key | models.CharField | 1 | {"max_length": 128, "null": false, "unique": true, "verbose_name": "\u73af\u5883\u53d8\u91cf\u540d"} |
| value | models.TextField | 1 | {"max_length": 512, "null": false, "verbose_name": "\u73af\u5883\u53d8\u91cf\u503c"} |
| description | models.CharField | 1 | {"max_length": 512, "null": false, "verbose_name": "\u63cf\u8ff0"} |



---


### MobileConfig

**模块**: `apiserver.paasng.paasng.platform.engine.models.mobile_config`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: Mobile config switcher for application

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| is_enabled | models.BooleanField | 1 | {"default": false} |
| lb_plan | models.CharField | 1 | {"choices": "`LBPlans.get_choices()`", "default": "`LBPlans.LBDefaultPlan.value`", "help_text": "which one-level load balancer plan the domain use", "max_length": 64} |
| access_url | models.URLField | 1 | {"blank": true, "default": "", "null": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| environment | models.OneToOneField | applications.ApplicationEnvironment | mobile_config | `models.CASCADE` |


---


### ModuleEnvironmentOperations

**模块**: `apiserver.paasng.paasng.platform.engine.models.operations`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| id | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |
| operation_type | models.CharField | 1 | {"choices": "`OperationTypes.get_choices()`", "max_length": 32} |
| object_uid | models.UUIDField | 1 | {"default": "`uuid.uuid4`", "editable": false} |
| status | models.CharField | 1 | {"choices": "`JobStatus.get_choices()`", "default": "`JobStatus.PENDING.value`", "max_length": 16} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| application | models.ForeignKey | applications.Application | module_operations | `models.CASCADE` |
| app_environment | models.ForeignKey | applications.ApplicationEnvironment | module_operations | `models.CASCADE` |


---


### DeployPhase

**模块**: `apiserver.paasng.paasng.platform.engine.models.phases`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel, paasng.platform.engine.models.MarkStatusMixin  
**描述**: 部署阶段

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| type | models.CharField | 1 | {"choices": "`DeployPhaseTypes.get_choices()`", "max_length": 32} |
| status | models.CharField | 1 | {"choices": "`JobStatus.get_choices()`", "max_length": 32, "null": true} |
| start_time | models.DateTimeField | 1 | {"null": true} |
| complete_time | models.DateTimeField | 1 | {"null": true} |

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
**行号**: 1  
**基类**: paas_wl.utils.models.AuditedModel  
**描述**: 应用描述文件中预定义的环境变量

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| environment_name | models.CharField | 1 | {"choices": "`ConfigVarEnvName.get_choices()`", "max_length": 16, "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| key | models.CharField | 1 | {"max_length": 128, "null": false} |

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
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 部署步骤元信息

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| phase | models.CharField | 1 | {"choices": "`DeployPhaseTypes.get_choices()`", "max_length": 16, "verbose_name": "`_(\u0027\u5173\u8054\u9636\u6bb5\u0027)`"} |
| name | models.CharField | 1 | {"db_index": true, "max_length": 32} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ['id'] |

---


### StepMetaSet

**模块**: `apiserver.paasng.paasng.platform.engine.models.steps`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 部署步骤元信息集

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 32} |
| is_default | models.BooleanField | 1 | {"default": false} |

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
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel, paasng.platform.engine.models.base.MarkStatusMixin  
**描述**: 部署步骤

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"db_index": true, "max_length": 32} |
| skipped | models.BooleanField | 1 | {"default": false} |
| status | models.CharField | 1 | {"choices": "`JobStatus.get_choices()`", "max_length": 32, "null": true} |
| start_time | models.DateTimeField | 1 | {"null": true} |
| complete_time | models.DateTimeField | 1 | {"null": true} |

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
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: 模块环境角色保护

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| allowed_role | models.IntegerField | 1 | {"choices": "`ApplicationRole.get_django_choices()`"} |
| operation | models.CharField | 1 | {"choices": "`EnvRoleOperation.get_choices()`", "max_length": 64} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module_env | models.ForeignKey | `ModuleEnvironment` | role_protections | `models.CASCADE` |


---


### AppOperationReportCollectionTask

**模块**: `apiserver.paasng.paasng.platform.evaluation.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: 应用运营报告采集任务

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| start_at | models.DateTimeField | 1 | {"auto_now_add": true, "verbose_name": "\u4efb\u52a1\u5f00\u59cb\u65f6\u95f4"} |
| end_at | models.DateTimeField | 1 | {"null": true, "verbose_name": "\u4efb\u52a1\u7ed3\u675f\u65f6\u95f4"} |
| total_count | models.IntegerField | 1 | {"default": 0, "verbose_name": "\u5e94\u7528\u603b\u6570"} |
| succeed_count | models.IntegerField | 1 | {"default": 0, "verbose_name": "\u91c7\u96c6\u6210\u529f\u6570"} |
| failed_count | models.IntegerField | 1 | {"default": 0, "verbose_name": "\u91c7\u96c6\u5931\u8d25\u6570"} |
| failed_app_codes | models.JSONField | 1 | {"default": "`list`", "verbose_name": "\u91c7\u96c6\u5931\u8d25\u5e94\u7528 Code \u5217\u8868"} |
| status | models.CharField | 1 | {"choices": "`BatchTaskStatus.get_choices()`", "default": "`BatchTaskStatus.RUNNING`", "max_length": 32, "verbose_name": "\u4efb\u52a1\u72b6\u6001"} |



---


### AppOperationReport

**模块**: `apiserver.paasng.paasng.platform.evaluation.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: 应用运营报告（含资源使用，用户活跃，运维操作等）

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| cpu_requests | models.IntegerField | 1 | {"default": 0, "verbose_name": "CPU \u8bf7\u6c42"} |
| mem_requests | models.IntegerField | 1 | {"default": 0, "verbose_name": "\u5185\u5b58\u8bf7\u6c42"} |
| cpu_limits | models.IntegerField | 1 | {"default": 0, "verbose_name": "CPU \u9650\u5236"} |
| mem_limits | models.IntegerField | 1 | {"default": 0, "verbose_name": "\u5185\u5b58\u9650\u5236"} |
| cpu_usage_avg | models.FloatField | 1 | {"default": 0, "verbose_name": "CPU \u5e73\u5747\u4f7f\u7528\u7387"} |
| mem_usage_avg | models.FloatField | 1 | {"default": 0, "verbose_name": "\u5185\u5b58\u5e73\u5747\u4f7f\u7528\u7387"} |
| res_summary | models.JSONField | 1 | {"default": "`dict`", "verbose_name": "\u8d44\u6e90\u4f7f\u7528\u8be6\u60c5\u6c47\u603b"} |
| pv | models.BigIntegerField | 1 | {"default": 0, "verbose_name": "\u8fd1 30 \u5929\u9875\u9762\u8bbf\u95ee\u91cf"} |
| uv | models.BigIntegerField | 1 | {"default": 0, "verbose_name": "\u8fd1 30 \u5929\u8bbf\u95ee\u7528\u6237\u6570"} |
| visit_summary | models.JSONField | 1 | {"default": "`dict`", "verbose_name": "\u7528\u6237\u8bbf\u95ee\u8be6\u60c5\u6c47\u603b"} |
| latest_deployed_at | models.DateTimeField | 1 | {"null": true, "verbose_name": "\u6700\u65b0\u90e8\u7f72\u65f6\u95f4"} |
| latest_deployer | models.CharField | 1 | {"max_length": 128, "null": true, "verbose_name": "\u6700\u65b0\u90e8\u7f72\u4eba"} |
| latest_operated_at | models.DateTimeField | 1 | {"null": true, "verbose_name": "\u6700\u65b0\u64cd\u4f5c\u65f6\u95f4"} |
| latest_operator | models.CharField | 1 | {"max_length": 128, "null": true, "verbose_name": "\u6700\u65b0\u64cd\u4f5c\u4eba"} |
| latest_operation | models.CharField | 1 | {"max_length": 128, "null": true, "verbose_name": "\u6700\u65b0\u64cd\u4f5c\u5185\u5bb9"} |
| deploy_summary | models.JSONField | 1 | {"default": "`dict`", "verbose_name": "\u90e8\u7f72\u8be6\u60c5\u6c47\u603b"} |
| administrators | models.JSONField | 1 | {"default": "`list`", "verbose_name": "\u5e94\u7528\u7ba1\u7406\u5458"} |
| developers | models.JSONField | 1 | {"default": "`list`", "verbose_name": "\u5e94\u7528\u5f00\u53d1\u8005"} |
| issue_type | models.CharField | 1 | {"default": "`OperationIssueType.NONE`", "max_length": 32, "verbose_name": "\u95ee\u9898\u7c7b\u578b"} |
| evaluate_result | models.JSONField | 1 | {"default": "`dict`", "verbose_name": "\u8bc4\u4f30\u7ed3\u679c"} |
| collected_at | models.DateTimeField | 1 | {"verbose_name": "\u91c7\u96c6\u65f6\u95f4"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.OneToOneField | `Application` | 不适用 | `models.CASCADE` |


---


### AppOperationEmailNotificationTask

**模块**: `apiserver.paasng.paasng.platform.evaluation.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: 应用运营报告邮件通知任务

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| start_at | models.DateTimeField | 1 | {"auto_now_add": true, "verbose_name": "\u4efb\u52a1\u5f00\u59cb\u65f6\u95f4"} |
| end_at | models.DateTimeField | 1 | {"null": true, "verbose_name": "\u4efb\u52a1\u7ed3\u675f\u65f6\u95f4"} |
| total_count | models.IntegerField | 1 | {"default": 0, "verbose_name": "\u5e94\u7528\u603b\u6570"} |
| succeed_count | models.IntegerField | 1 | {"default": 0, "verbose_name": "\u91c7\u96c6\u6210\u529f\u6570"} |
| failed_count | models.IntegerField | 1 | {"default": 0, "verbose_name": "\u91c7\u96c6\u5931\u8d25\u6570"} |
| failed_usernames | models.JSONField | 1 | {"default": "`list`", "verbose_name": "\u901a\u77e5\u5931\u8d25\u7684\u5e94\u7528\u6570\u91cf"} |
| notification_type | models.CharField | 1 | {"max_length": 64, "verbose_name": "\u901a\u77e5\u7c7b\u578b"} |
| status | models.CharField | 1 | {"choices": "`BatchTaskStatus.get_choices()`", "default": "`BatchTaskStatus.RUNNING`", "max_length": 32, "verbose_name": "\u4efb\u52a1\u72b6\u6001"} |



---


### IdleAppNotificationMuteRule

**模块**: `apiserver.paasng.paasng.platform.evaluation.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 闲置应用通知屏蔽规则

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| app_code | models.CharField | 1 | {"max_length": 32} |
| module_name | models.CharField | 1 | {"max_length": 32} |
| environment | models.CharField | 1 | {"max_length": 32} |
| expired_at | models.DateTimeField | 1 | {} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('user', 'app_code', 'module_name', 'environment') |

---


### MigrationProcess

**模块**: `apiserver.paasng.paasng.platform.mgrlegacy.models`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: An migration process

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| legacy_app_id | models.IntegerField | 1 | {} |
| status | models.IntegerField | 1 | {"choices": "`MigrationStatus.get_choices()`", "default": "`MigrationStatus.DEFAULT.value`"} |
| failed_date | models.DateTimeField | 1 | {"null": true} |
| migrated_date | models.DateTimeField | 1 | {"null": true} |
| confirmed_date | models.DateTimeField | 1 | {"null": true} |
| rollbacked_date | models.DateTimeField | 1 | {"null": true} |
| legacy_app_logo | models.CharField | 1 | {"default": null, "max_length": 500, "null": true} |
| legacy_app_is_already_online | models.BooleanField | 1 | {"default": true} |
| legacy_app_state | models.IntegerField | 1 | {"default": 4} |
| legacy_app_has_all_deployed | models.BooleanField | 1 | {"default": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app | models.ForeignKey | `Application` | 不适用 | `models.CASCADE` |


---


### CNativeMigrationProcess

**模块**: `apiserver.paasng.paasng.platform.mgrlegacy.models`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| status | models.CharField | 1 | {"choices": "`CNativeMigrationStatus.get_choices()`", "default": "`CNativeMigrationStatus.DEFAULT.value`", "max_length": 20} |
| created_at | models.DateTimeField | 1 | {"auto_now_add": true, "help_text": "\u64cd\u4f5c\u8bb0\u5f55\u7684\u521b\u5efa\u65f6\u95f4"} |
| confirm_at | models.DateTimeField | 1 | {"help_text": "\u7528\u6237\u786e\u8ba4\u7684\u65f6\u95f4", "null": true} |

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
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: WlApp 的备份关系表

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| original_id | models.UUIDField | 1 | {"verbose_name": "\u539f WlApp uuid"} |
| backup_id | models.UUIDField | 1 | {"verbose_name": "\u5bf9\u5e94\u5907\u4efd\u7684 WlApp uuid"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| app_environment | models.OneToOneField | `ApplicationEnvironment` | 不适用 | `models.CASCADE` |


---


### BuildConfig

**模块**: `apiserver.paasng.paasng.platform.modules.models.build_cfg`  
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| build_method | models.CharField | 1 | {"default": "`RuntimeType.BUILDPACK`", "max_length": 32, "verbose_name": "`_(\u0027\u6784\u5efa\u65b9\u5f0f\u0027)`"} |
| dockerfile_path | models.CharField | 1 | {"help_text": "`_(\u0027Dockerfile\u6587\u4ef6\u8def\u5f84, \u5fc5\u987b\u4fdd\u8bc1 Dockerfile \u5728\u6784\u5efa\u76ee\u5f55\u4e0b, \u586b\u5199\u65f6\u65e0\u9700\u5305\u542b\u6784\u5efa\u76ee\u5f55\u0027)`", "max_length": 512, "null": true} |
| image_repository | models.TextField | 1 | {"null": true, "verbose_name": "`_(\u0027\u955c\u50cf\u4ed3\u5e93\u0027)`"} |
| image_credential_name | models.CharField | 1 | {"max_length": 32, "null": true, "verbose_name": "`_(\u0027\u955c\u50cf\u51ed\u8bc1\u540d\u79f0\u0027)`"} |
| use_bk_ci_pipeline | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u4f7f\u7528\u84dd\u76fe\u6d41\u6c34\u7ebf\u6784\u5efa"} |

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
**行号**: 1  
**基类**: paasng.utils.models.UuidAuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.OneToOneField | modules.Module | deploy_config | `models.CASCADE` |


---


### Module

**模块**: `apiserver.paasng.paasng.platform.modules.models.module`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: Module for Application

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| id | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |
| name | models.CharField | 1 | {"max_length": 20, "verbose_name": "\u6a21\u5757\u540d\u79f0"} |
| is_default | models.BooleanField | 1 | {"default": false, "verbose_name": "\u662f\u5426\u4e3a\u9ed8\u8ba4\u6a21\u5757"} |
| language | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u7f16\u7a0b\u8bed\u8a00"} |
| source_init_template | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u521d\u59cb\u5316\u6a21\u677f\u7c7b\u578b"} |
| source_origin | models.SmallIntegerField | 1 | {"null": true, "verbose_name": "\u6e90\u7801\u6765\u6e90"} |
| source_type | models.CharField | 1 | {"max_length": 16, "null": true, "verbose_name": "\u6e90\u7801\u6258\u7ba1\u7c7b\u578b"} |
| source_repo_id | models.IntegerField | 1 | {"null": true, "verbose_name": "\u6e90\u7801 ID"} |
| exposed_url_type | models.IntegerField | 1 | {"null": true, "verbose_name": "\u8bbf\u95ee URL \u7248\u672c"} |
| user_preferred_root_domain | models.CharField | 1 | {"max_length": 255, "null": true, "verbose_name": "\u7528\u6237\u504f\u597d\u7684\u6839\u57df\u540d"} |
| last_deployed_date | models.DateTimeField | 1 | {"null": true, "verbose_name": "\u6700\u8fd1\u90e8\u7f72\u65f6\u95f4"} |

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
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: buildpack 配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| language | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u7f16\u7a0b\u8bed\u8a00"} |
| type | models.CharField | 1 | {"choices": "`BuildPackType.get_choices()`", "max_length": 32, "verbose_name": "\u5f15\u7528\u7c7b\u578b"} |
| name | models.CharField | 1 | {"max_length": 64, "verbose_name": "\u540d\u79f0"} |
| address | models.CharField | 1 | {"max_length": 2048, "verbose_name": "\u5730\u5740"} |
| version | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u7248\u672c"} |
| is_hidden | models.BooleanField | 1 | {"default": false, "verbose_name": "\u662f\u5426\u9690\u85cf"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| modules | models.ManyToManyField | modules.Module | buildpacks | 不适用 |


---


### AppImage

**模块**: `apiserver.paasng.paasng.platform.modules.models.runtime`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 64, "unique": true, "verbose_name": "\u540d\u79f0"} |
| type | models.CharField | 1 | {"choices": "`AppImageType.get_choices()`", "max_length": 32, "verbose_name": "\u955c\u50cf\u7c7b\u578b"} |
| image | models.CharField | 1 | {"max_length": 256, "verbose_name": "\u955c\u50cf"} |
| tag | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u6807\u7b7e"} |
| is_hidden | models.BooleanField | 1 | {"default": false, "verbose_name": "\u662f\u5426\u9690\u85cf"} |
| is_default | models.BooleanField | 1 | {"default": false, "null": true, "verbose_name": "\u662f\u5426\u4e3a\u9ed8\u8ba4\u8fd0\u884c\u65f6"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### AppSlugRunner

**模块**: `apiserver.paasng.paasng.platform.modules.models.runtime`  
**行号**: 1  
**基类**: apiserver.paasng.paasng.platform.modules.models.runtime.AppImage  
**描述**: 应用运行环境

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 64, "unique": true, "verbose_name": "\u540d\u79f0"} |
| type | models.CharField | 1 | {"choices": "`AppImageType.get_choices()`", "max_length": 32, "verbose_name": "\u955c\u50cf\u7c7b\u578b"} |
| image | models.CharField | 1 | {"max_length": 256, "verbose_name": "\u955c\u50cf"} |
| tag | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u6807\u7b7e"} |
| is_hidden | models.BooleanField | 1 | {"default": false, "verbose_name": "\u662f\u5426\u9690\u85cf"} |
| is_default | models.BooleanField | 1 | {"default": false, "null": true, "verbose_name": "\u662f\u5426\u4e3a\u9ed8\u8ba4\u8fd0\u884c\u65f6"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| modules | models.ManyToManyField | modules.Module | slugrunners | 不适用 |


---


### AppSlugBuilder

**模块**: `apiserver.paasng.paasng.platform.modules.models.runtime`  
**行号**: 1  
**基类**: apiserver.paasng.paasng.platform.modules.models.runtime.AppImage  
**描述**: 应用构建环境

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 64, "unique": true, "verbose_name": "\u540d\u79f0"} |
| type | models.CharField | 1 | {"choices": "`AppImageType.get_choices()`", "max_length": 32, "verbose_name": "\u955c\u50cf\u7c7b\u578b"} |
| image | models.CharField | 1 | {"max_length": 256, "verbose_name": "\u955c\u50cf"} |
| tag | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u6807\u7b7e"} |
| is_hidden | models.BooleanField | 1 | {"default": false, "verbose_name": "\u662f\u5426\u9690\u85cf"} |
| is_default | models.BooleanField | 1 | {"default": false, "null": true, "verbose_name": "\u662f\u5426\u4e3a\u9ed8\u8ba4\u8fd0\u884c\u65f6"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| buildpacks | models.ManyToManyField | `AppBuildPack` | slugbuilders | 不适用 |
| modules | models.ManyToManyField | modules.Module | slugbuilders | 不适用 |
| step_meta_set | models.ForeignKey | engine.StepMetaSet | slugbuilders | `models.SET_NULL` |


---


### SvnRepository

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel, apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin  
**描述**: 基于 Svn 的软件存储库

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| server_name | models.CharField | 1 | {"max_length": 32, "verbose_name": "SVN \u670d\u52a1\u540d\u79f0"} |
| repo_url | models.CharField | 1 | {"max_length": 2048, "verbose_name": "\u9879\u76ee\u5730\u5740"} |
| source_dir | models.CharField | 1 | {"max_length": 2048, "null": true, "verbose_name": "\u6e90\u7801\u76ee\u5f55"} |



---


### SvnAccount

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: svn account for developer

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| account | models.CharField | 1 | {"help_text": "\u76ee\u524d\u4ec5\u652f\u6301\u56fa\u5b9a\u683c\u5f0f", "max_length": 64, "unique": true} |
| synced_from_paas20 | models.BooleanField | 1 | {"default": false, "help_text": "\u8d26\u6237\u4fe1\u606f\u662f\u5426\u4ece PaaS 2.0 \u540c\u6b65\u8fc7\u6765"} |



---


### GitRepository

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel, apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin  
**描述**: 基于 Git 的软件存储库

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| server_name | models.CharField | 1 | {"max_length": 32, "verbose_name": "GIT \u670d\u52a1\u540d\u79f0"} |
| repo_url | models.CharField | 1 | {"max_length": 2048, "verbose_name": "\u9879\u76ee\u5730\u5740"} |
| source_dir | models.CharField | 1 | {"max_length": 2048, "null": true, "verbose_name": "\u6e90\u7801\u76ee\u5f55"} |



---


### DockerRepository

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel, apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin  
**描述**: 容器镜像仓库

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| server_name | models.CharField | 1 | {"max_length": 32, "verbose_name": "DockerRegistry \u670d\u52a1\u540d\u79f0"} |
| repo_url | models.CharField | 1 | {"help_text": "\u5f62\u5982 registry.hub.docker.com/library/python, \u4e5f\u53ef\u7701\u7565 registry \u5730\u5740", "max_length": 2048, "verbose_name": "\u9879\u76ee\u5730\u5740"} |
| source_dir | models.CharField | 1 | {"max_length": 2048, "null": true, "verbose_name": "\u6e90\u7801\u76ee\u5f55"} |



---


### SourcePackage

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**行号**: 1  
**基类**: paasng.utils.models.OwnerTimestampedModel  
**描述**: 源码包存储信息

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| version | models.CharField | 1 | {"max_length": 128, "verbose_name": "\u7248\u672c\u53f7"} |
| package_name | models.CharField | 1 | {"max_length": 128, "verbose_name": "\u6e90\u7801\u5305\u539f\u59cb\u6587\u4ef6\u540d"} |
| package_size | models.BigIntegerField | 1 | {"verbose_name": "\u6e90\u7801\u5305\u5927\u5c0f, bytes"} |
| storage_engine | models.CharField | 1 | {"help_text": "\u6e90\u7801\u5305\u771f\u5b9e\u5b58\u653e\u7684\u5b58\u50a8\u670d\u52a1\u7c7b\u578b", "max_length": 64, "verbose_name": "\u5b58\u50a8\u5f15\u64ce"} |
| storage_path | models.CharField | 1 | {"help_text": "[deprecated] \u6e90\u7801\u5305\u5728\u5b58\u50a8\u670d\u52a1\u4e2d\u5b58\u653e\u7684\u4f4d\u7f6e", "max_length": 1024, "verbose_name": "\u5b58\u50a8\u8def\u5f84"} |
| storage_url | models.CharField | 1 | {"help_text": "\u53ef\u83b7\u53d6\u5230\u6e90\u7801\u5305\u7684 URL \u5730\u5740", "max_length": 1024, "verbose_name": "\u5b58\u50a8\u5730\u5740"} |
| sha256_signature | models.CharField | 1 | {"max_length": 64, "null": true, "verbose_name": "sha256\u6570\u5b57\u7b7e\u540d"} |
| relative_path | models.CharField | 1 | {"help_text": "\u5982\u679c\u538b\u7f29\u65f6\u5c06\u76ee\u5f55\u4e5f\u6253\u5305\u8fdb\u6765, \u5165\u76ee\u5f55\u540d\u662f foo, \u90a3\u4e48 relative_path = \u0027foo/\u0027", "max_length": 255, "verbose_name": "\u6e90\u7801\u5165\u53e3\u7684\u76f8\u5bf9\u8def\u5f84"} |
| is_deleted | models.BooleanField | 1 | {"default": false, "help_text": "\u5982\u679c SourcePackage \u6307\u5411\u7684\u6e90\u7801\u5305\u5df2\u88ab\u6e05\u7406, \u5219\u8bbe\u7f6e\u8be5\u503c\u4e3a True", "verbose_name": "\u6e90\u7801\u5305\u662f\u5426\u5df2\u88ab\u6e05\u7406"} |

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
**行号**: 1  
**基类**: paasng.utils.models.TimestampedModel  
**描述**: Repo 鉴权

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| username | models.CharField | 1 | {"max_length": 64, "verbose_name": "\u4ed3\u5e93\u7528\u6237\u540d"} |
| repo_id | models.IntegerField | 1 | {"verbose_name": "\u5173\u8054\u4ed3\u5e93"} |
| repo_type | models.CharField | 1 | {"max_length": 32, "verbose_name": "\u4ed3\u5e93\u7c7b\u578b"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| module | models.ForeignKey | modules.Module | 不适用 | `models.CASCADE` |


---


### SourceTypeSpecConfig

**模块**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: SourceTypeSpec 数据存储

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 32, "unique": true, "verbose_name": "`_(\u0027\u670d\u52a1\u540d\u79f0\u0027)`"} |
| enabled | models.BooleanField | 1 | {"default": false, "verbose_name": "\u662f\u5426\u542f\u7528"} |
| spec_cls | models.CharField | 1 | {"max_length": 128, "verbose_name": "\u914d\u7f6e\u7c7b\u8def\u5f84"} |
| server_config | models.JSONField | 1 | {"blank": true, "default": "`dict`", "verbose_name": "\u670d\u52a1\u914d\u7f6e"} |
| authorization_base_url | models.CharField | 1 | {"blank": true, "default": "", "max_length": 256, "verbose_name": "OAuth \u6388\u6743\u94fe\u63a5"} |
| client_id | models.CharField | 1 | {"blank": true, "default": "", "max_length": 256, "verbose_name": "OAuth App Client ID"} |
| redirect_uri | models.CharField | 1 | {"blank": true, "default": "", "max_length": 256, "verbose_name": "\u91cd\u5b9a\u5411\uff08\u56de\u8c03\uff09\u5730\u5740"} |
| token_base_url | models.CharField | 1 | {"blank": true, "default": "", "max_length": 256, "verbose_name": "\u83b7\u53d6 Token \u94fe\u63a5"} |



---


### Template

**模块**: `apiserver.paasng.paasng.platform.templates.models`  
**行号**: 1  
**基类**: paasng.utils.models.AuditedModel  
**描述**: 开发模板配置

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 64, "unique": true, "verbose_name": "`_(\u0027\u6a21\u677f\u540d\u79f0\u0027)`"} |
| type | models.CharField | 1 | {"choices": "`TemplateType.get_django_choices()`", "max_length": 16, "verbose_name": "`_(\u0027\u6a21\u677f\u7c7b\u578b\u0027)`"} |
| language | models.CharField | 1 | {"max_length": 32, "verbose_name": "`_(\u0027\u5f00\u53d1\u8bed\u8a00\u0027)`"} |
| market_ready | models.BooleanField | 1 | {"default": false, "verbose_name": "`_(\u0027\u80fd\u5426\u53d1\u5e03\u5230\u5e94\u7528\u96c6\u5e02\u0027)`"} |
| preset_services_config | models.JSONField | 1 | {"blank": true, "default": "`dict`", "verbose_name": "`_(\u0027\u9884\u8bbe\u589e\u5f3a\u670d\u52a1\u914d\u7f6e\u0027)`"} |
| blob_url | models.JSONField | 1 | {"verbose_name": "`_(\u0027\u4e0d\u540c\u7248\u672c\u4e8c\u8fdb\u5236\u5305\u5b58\u50a8\u8def\u5f84\u0027)`"} |
| enabled_regions | models.JSONField | 1 | {"blank": true, "default": "`list`", "verbose_name": "`_(\u0027\u5141\u8bb8\u88ab\u4f7f\u7528\u7684\u7248\u672c\u0027)`"} |
| required_buildpacks | models.JSONField | 1 | {"blank": true, "default": "`list`", "verbose_name": "`_(\u0027\u5fc5\u987b\u7684\u6784\u5efa\u5de5\u5177\u0027)`"} |
| processes | models.JSONField | 1 | {"blank": true, "default": "`dict`", "verbose_name": "`_(\u0027\u8fdb\u7a0b\u914d\u7f6e\u0027)`"} |
| tags | models.JSONField | 1 | {"blank": true, "default": "`list`", "verbose_name": "`_(\u0027\u6807\u7b7e\u0027)`"} |
| repo_url | models.CharField | 1 | {"blank": true, "default": "", "max_length": 256, "verbose_name": "`_(\u0027\u4ee3\u7801\u4ed3\u5e93\u4fe1\u606f\u0027)`"} |
| runtime_type | models.CharField | 1 | {"default": "`RuntimeType.BUILDPACK`", "max_length": 32, "verbose_name": "`_(\u0027\u8fd0\u884c\u65f6\u7c7b\u578b\u0027)`"} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ['created'] |

---


### TimestampedModel

**模块**: `apiserver.paasng.paasng.utils.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: Model with 'created' and 'updated' fields.

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| region | models.CharField | 1 | {"help_text": "\u90e8\u7f72\u533a\u57df", "max_length": 32} |
| created | models.DateTimeField | 1 | {"auto_now_add": true} |
| updated | models.DateTimeField | 1 | {"auto_now": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### OwnerTimestampedModel

**模块**: `apiserver.paasng.paasng.utils.models`  
**行号**: 1  
**基类**: apiserver.paasng.paasng.utils.models.TimestampedModel  
**描述**: Model with 'created' and 'updated' fields.

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### AuditedModel

**模块**: `apiserver.paasng.paasng.utils.models`  
**行号**: 1  
**基类**: models.Model  
**描述**: Audited model with 'created' and 'updated' fields.

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| created | models.DateTimeField | 1 | {"auto_now_add": true} |
| updated | models.DateTimeField | 1 | {"auto_now": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### UuidAuditedModel

**模块**: `apiserver.paasng.paasng.utils.models`  
**行号**: 1  
**基类**: apiserver.paasng.paasng.utils.models.AuditedModel  
**描述**: Add a UUID primary key to an :class:`AuditedModel`.

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| uuid | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "unique": true} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### RepoQuotaStatistics

**模块**: `svc-bkrepo.svc_bk_repo.monitoring.models`  
**行号**: 1  
**基类**: models.Model  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| repo_name | models.CharField | 1 | {"max_length": 64, "verbose_name": "\u4ed3\u5e93\u540d\u79f0"} |
| max_size | models.BigIntegerField | 1 | {"help_text": "\u5355\u4f4d\u5b57\u8282\uff0c\u503c\u4e3a nul \u65f6\u8868\u793a\u672a\u8bbe\u7f6e\u4ed3\u5e93\u914d\u989d", "null": true, "verbose_name": "\u4ed3\u5e93\u6700\u5927\u914d\u989d"} |
| used | models.BigIntegerField | 1 | {"default": 0, "help_text": "\u5355\u4f4d\u5b57\u8282", "verbose_name": "\u4ed3\u5e93\u5df2\u4f7f\u7528\u5bb9\u91cf"} |
| updated | models.DateTimeField | 1 | {"auto_now": true} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| instance | models.ForeignKey | paas_service.ServiceInstance | 不适用 | `models.CASCADE` |


---


### ApmData

**模块**: `svc-otel.svc_otel.vendor.models`  
**行号**: 1  
**基类**: paas_service.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| bk_app_code | models.CharField | 1 | {"max_length": 64} |
| env | models.CharField | 1 | {"max_length": 64} |
| app_name | models.CharField | 1 | {"max_length": 64} |
| data_token | models.CharField | 1 | {"max_length": 255} |
| is_delete | models.BooleanField | 1 | {"default": false} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| unique_together | ('bk_app_code', 'env') |

---


### CronTask

**模块**: `svc-rabbitmq.tasks.models`  
**行号**: 1  
**基类**: models.Model  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 255, "unique": true} |
| interval | models.DurationField | 1 | {} |
| next_run_time | models.DateTimeField | 1 | {"blank": true, "db_index": true, "default": "`get_now`", "null": true} |
| last_run_time | models.DateTimeField | 1 | {"blank": true, "null": true} |
| enabled | models.BooleanField | 1 | {"default": false} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| ordering | ('next_run_time', 'name') |

---


### Tag

**模块**: `svc-rabbitmq.vendor.models`  
**行号**: 1  
**基类**: paas_service.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| key | models.CharField | 1 | {"max_length": 64} |
| value | models.CharField | 1 | {"max_length": 128} |


#### Meta 选项

| 选项 | 值 |
|------|-----|
| abstract | True |

---


### Cluster

**模块**: `svc-rabbitmq.vendor.models`  
**行号**: 1  
**基类**: paas_service.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 64} |
| host | models.CharField | 1 | {"max_length": 64} |
| port | models.IntegerField | 1 | {"default": 5672} |
| management_api | models.TextField | 1 | {} |
| admin | models.CharField | 1 | {"max_length": 64} |
| version | models.CharField | 1 | {"max_length": 16} |
| enable | models.BooleanField | 1 | {"default": true} |



---


### ClusterTag

**模块**: `svc-rabbitmq.vendor.models`  
**行号**: 1  
**基类**: svc-rabbitmq.vendor.models.Tag  
**描述**: 集群标签，用于分配和分组

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| key | models.CharField | 1 | {"max_length": 64} |
| value | models.CharField | 1 | {"max_length": 128} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| instance | models.ForeignKey | `Cluster` | tags | `models.CASCADE` |


---


### LinkableModel

**模块**: `svc-rabbitmq.vendor.models`  
**行号**: 1  
**基类**: paas_service.models.AuditedModel  

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| link_type | models.IntegerField | 1 | {"choices": "`[(i.value, i.name) for i in LinkType]`", "default": "`LinkType.empty.value`"} |

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
**行号**: 1  
**基类**: svc-rabbitmq.vendor.models.LinkableModel  
**描述**: 集群下创建 vhost 默认策略，和具体 vhost 无关

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 64, "null": true} |
| enable | models.BooleanField | 1 | {"default": true} |
| pattern | models.CharField | 1 | {"blank": true, "max_length": 128, "null": true} |
| apply_to | models.CharField | 1 | {"blank": true, "choices": "`[(i.value, i.name) for i in PolicyTarget]`", "max_length": 64, "null": true} |
| priority | models.IntegerField | 1 | {"blank": true, "null": true} |
| cluster_id | models.IntegerField | 1 | {"blank": true, "default": null} |
| link_type | models.IntegerField | 1 | {"choices": "`[(i.value, i.name) for i in LinkType]`", "default": "`LinkType.empty.value`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| linked | models.ForeignKey | self | 不适用 | `models.CASCADE` |


---


### UserPolicyTag

**模块**: `svc-rabbitmq.vendor.models`  
**行号**: 1  
**基类**: svc-rabbitmq.vendor.models.Tag  
**描述**: 表示绑定关系

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| key | models.CharField | 1 | {"max_length": 64} |
| value | models.CharField | 1 | {"max_length": 128} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| instance | models.ForeignKey | `UserPolicy` | tags | `models.CASCADE` |


---


### LimitPolicy

**模块**: `svc-rabbitmq.vendor.models`  
**行号**: 1  
**基类**: svc-rabbitmq.vendor.models.LinkableModel  
**描述**: 集群下创建 vhost 限制机制，和具体 vhost 无关

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 64, "null": true} |
| enable | models.BooleanField | 1 | {"default": true} |
| limit | models.CharField | 1 | {"blank": true, "choices": "`[(i.value, i.name) for i in LimitType]`", "max_length": 64, "null": true} |
| value | models.IntegerField | 1 | {"blank": true, "null": true} |
| cluster_id | models.IntegerField | 1 | {"blank": true, "default": null} |
| link_type | models.IntegerField | 1 | {"choices": "`[(i.value, i.name) for i in LinkType]`", "default": "`LinkType.empty.value`"} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| linked | models.ForeignKey | self | 不适用 | `models.CASCADE` |


---


### LimitPolicyTag

**模块**: `svc-rabbitmq.vendor.models`  
**行号**: 1  
**基类**: svc-rabbitmq.vendor.models.Tag  
**描述**: 表示绑定关系

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| key | models.CharField | 1 | {"max_length": 64} |
| value | models.CharField | 1 | {"max_length": 128} |

#### 关系

| 字段 | 类型 | 目标模型 | 关联名 | 删除策略 |
|------|------|----------|--------|----------|
| instance | models.ForeignKey | `LimitPolicy` | tags | `models.CASCADE` |


---


### InstanceBill

**模块**: `svc-rabbitmq.vendor.models`  
**行号**: 1  
**基类**: paas_service.models.UuidAuditedModel  
**描述**: 实例单据，保存申请上下文，方便重入

#### 字段

| 字段名 | 类型 | 行号 | 参数 |
|--------|------|------|------|
| name | models.CharField | 1 | {"max_length": 128} |
| action | models.CharField | 1 | {"max_length": 32} |



---

