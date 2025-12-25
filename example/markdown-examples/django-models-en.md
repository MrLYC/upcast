# Django Models Analysis

## Metadata
No metadata available.

## Summary
- **Total Count**: 167
- **Files Scanned**: 167
- **Scan Duration**: 1942 ms

- **Total Models**: 167
- **Total Fields**: 684
- **Total Relationships**: 148

## Results

### App

**Module**: `apiserver.paasng.paas_wl.bk_app.applications.models.app`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**Description**: App Model

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| name | models.SlugField | 1 | {"max_length": 64, "type": "models.SlugField", "validators": ["`validate_app_name`"]} |
| owner | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| region | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| type | models.CharField | 1 | {"db_index": true, "default": "`WlAppType.DEFAULT.value`", "max_length": 16, "type": "models.CharField", "verbose_name": "\u5e94\u7528\u7c7b\u578b"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['region', 'name'] |

---


### Build

**Module**: `apiserver.paasng.paas_wl.bk_app.applications.models.build`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.UuidAuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| application_id | models.UUIDField | 1 | {"null": true, "type": "models.UUIDField", "verbose_name": "\u6240\u5c5e\u5e94\u7528"} |
| artifact_deleted | models.BooleanField | 1 | {"default": false, "help_text": "slug/\u955c\u50cf\u662f\u5426\u5df2\u88ab\u6e05\u7406", "type": "models.BooleanField"} |
| artifact_detail | models.JSONField | 1 | {"default": {}, "help_text": "\u6784\u4ef6\u8be6\u60c5(\u5c55\u793a\u4fe1\u606f)", "type": "models.JSONField"} |
| artifact_metadata | models.JSONField | 1 | {"default": {}, "help_text": "\u6784\u4ef6\u5143\u4fe1\u606f, \u5305\u62ec entrypoint/use_cnb/use_dockerfile \u7b49\u4fe1\u606f", "type": "models.JSONField"} |
| artifact_type | models.CharField | 1 | {"default": "`ArtifactType.SLUG`", "help_text": "\u6784\u4ef6\u7c7b\u578b", "max_length": 16, "type": "models.CharField"} |
| bkapp_revision_id | models.IntegerField | 1 | {"help_text": "\u4e0e\u672c\u6b21\u6784\u5efa\u5173\u8054\u7684 BkApp Revision id", "null": true, "type": "models.IntegerField"} |
| branch | models.CharField | 1 | {"help_text": "readable version, such as trunk/master", "max_length": 128, "null": true, "type": "models.CharField"} |
| image | models.TextField | 1 | {"help_text": "\u8fd0\u884c Build \u7684\u955c\u50cf\u5730\u5740. \u5982\u679c\u6784\u4ef6\u7c7b\u578b\u4e3a image\uff0c\u8be5\u503c\u5373\u6784\u5efa\u4ea7\u7269; \u5982\u679c\u6784\u5efa\u4ea7\u7269\u662f Slug, \u5219\u8fd4\u56de SlugRunner \u7684\u955c\u50cf", "null": true, "type": "models.TextField"} |
| module_id | models.UUIDField | 1 | {"null": true, "type": "models.UUIDField", "verbose_name": "\u6240\u5c5e\u6a21\u5757"} |
| owner | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| revision | models.CharField | 1 | {"help_text": "unique version, such as sha256", "max_length": 128, "null": true, "type": "models.CharField"} |
| slug_path | models.TextField | 1 | {"help_text": "slug path \u5f62\u5982 {region}/home/{name}:{branch}:{revision}/push", "null": true, "type": "models.TextField"} |
| source_type | models.CharField | 1 | {"max_length": 128, "null": true, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | App | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| get_latest_by | created |
| ordering | ['-created'] |

---


### BuildProcess

**Module**: `apiserver.paasng.paas_wl.bk_app.applications.models.build`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.UuidAuditedModel  
**Description**: This Build Process was invoked via a source tarball or anything similar

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| application_id | models.UUIDField | 1 | {"null": true, "type": "models.UUIDField", "verbose_name": "\u6240\u5c5e\u5e94\u7528"} |
| branch | models.CharField | 1 | {"max_length": 128, "null": true, "type": "models.CharField"} |
| completed_at | models.DateTimeField | 1 | {"help_text": "failed/successful/interrupted \u90fd\u662f\u5b8c\u6210", "null": true, "type": "models.DateTimeField", "verbose_name": "\u5b8c\u6210\u65f6\u95f4"} |
| generation | models.PositiveBigIntegerField | 1 | {"help_text": "\u6bcf\u4e2a\u5e94\u7528\u72ec\u7acb\u7684\u81ea\u589eID", "type": "models.PositiveBigIntegerField", "verbose_name": "\u81ea\u589eID"} |
| image | models.CharField | 1 | {"help_text": "builder image", "max_length": 512, "null": true, "type": "models.CharField"} |
| int_requested_at | models.DateTimeField | 1 | {"help_text": "\u7528\u6237\u8bf7\u6c42\u4e2d\u65ad\u7684\u65f6\u95f4", "null": true, "type": "models.DateTimeField"} |
| invoke_message | models.CharField | 1 | {"blank": true, "help_text": "\u89e6\u53d1\u4fe1\u606f", "max_length": 255, "null": true, "type": "models.CharField"} |
| logs_was_ready_at | models.DateTimeField | 1 | {"help_text": "Pod \u72b6\u6001\u5c31\u7eea\u5141\u8bb8\u8bfb\u53d6\u65e5\u5fd7\u7684\u65f6\u95f4", "null": true, "type": "models.DateTimeField"} |
| module_id | models.UUIDField | 1 | {"null": true, "type": "models.UUIDField", "verbose_name": "\u6240\u5c5e\u6a21\u5757"} |
| owner | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| revision | models.CharField | 1 | {"max_length": 128, "null": true, "type": "models.CharField"} |
| source_tar_path | models.CharField | 1 | {"max_length": 2048, "type": "models.CharField"} |
| status | models.CharField | 1 | {"choices": "`make_enum_choices(BuildStatus)`", "default": "`BuildStatus.PENDING.value`", "max_length": 12, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | App | N/A | `models.CASCADE` |
| output_stream | models.OneToOneField | OutputStream | N/A | `models.CASCADE` |
| build | models.OneToOneField | Build | build_process | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| get_latest_by | created |
| ordering | ['-created'] |

---


### Config

**Module**: `apiserver.paasng.paas_wl.bk_app.applications.models.config`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**Description**: App configs, includes env variables and resource limits

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| cluster | models.CharField | 1 | {"blank": true, "default": "", "max_length": 64, "type": "models.CharField"} |
| domain | models.CharField | 1 | {"default": "", "max_length": 64, "type": "models.CharField"} |
| image | models.CharField | 1 | {"max_length": 256, "null": true, "type": "models.CharField"} |
| mount_log_to_host | models.BooleanField | 1 | {"default": true, "help_text": "Whether mount app logs to host", "type": "models.BooleanField"} |
| owner | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | App | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| get_latest_by | created |
| ordering | ['-created'] |
| unique_together | [['app', 'uuid']] |

---


### OutputStreamLine

**Module**: `apiserver.paasng.paas_wl.bk_app.applications.models.misc`  
**Line**: 1  
**Base Classes**: models.Model  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| created | models.DateTimeField | 1 | {"auto_now_add": true, "type": "models.DateTimeField"} |
| line | models.TextField | 1 | {"type": "models.TextField"} |
| stream | models.CharField | 1 | {"max_length": 16, "type": "models.CharField"} |
| updated | models.DateTimeField | 1 | {"auto_now": true, "type": "models.DateTimeField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| output_stream | models.ForeignKey | OutputStream | lines | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| ordering | ['created'] |

---


### Release

**Module**: `apiserver.paasng.paas_wl.bk_app.applications.models.release`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.UuidAuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| failed | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| owner | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| summary | models.TextField | 1 | {"blank": true, "null": true, "type": "models.TextField"} |
| version | models.PositiveIntegerField | 1 | {"type": "models.PositiveIntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | App | N/A | `models.CASCADE` |
| config | models.ForeignKey | Config | N/A | `models.CASCADE` |
| build | models.ForeignKey | Build | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| get_latest_by | created |
| ordering | ['-created'] |
| unique_together | [['app', 'version']] |

---


### AppModelDeploy

**Module**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.app_resource`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: This model stores the cloud-native app's deployment histories.

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| application_id | models.UUIDField | 1 | {"null": false, "type": "models.UUIDField", "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| environment_name | models.CharField | 1 | {"choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": false, "type": "models.CharField", "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| last_transition_time | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField", "verbose_name": "`_(\u0027\u72b6\u6001\u6700\u8fd1\u53d8\u66f4\u65f6\u95f4\u0027)`"} |
| message | models.TextField | 1 | {"blank": true, "null": true, "type": "models.TextField", "verbose_name": "`_(\u0027\u72b6\u6001\u63cf\u8ff0\u6587\u5b57\u0027)`"} |
| module_id | models.UUIDField | 1 | {"null": false, "type": "models.UUIDField", "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "verbose_name": "`_(\u0027Deploy \u540d\u79f0\u0027)`"} |
| reason | models.CharField | 1 | {"blank": true, "max_length": 128, "null": true, "type": "models.CharField", "verbose_name": "`_(\u0027\u72b6\u6001\u539f\u56e0\u0027)`"} |
| status | models.CharField | 1 | {"blank": true, "choices": "`DeployStatus.get_choices()`", "max_length": 32, "null": true, "type": "models.CharField", "verbose_name": "`_(\u0027\u72b6\u6001\u0027)`"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| revision | models.ForeignKey | AppModelRevision | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['application_id', 'module_id', 'environment_name', 'name'] |

---


### AppModelResource

**Module**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.app_resource`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: Cloud-native Application's Model Resource

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| application_id | models.UUIDField | 1 | {"null": false, "type": "models.UUIDField", "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| module_id | models.UUIDField | 1 | {"null": false, "type": "models.UUIDField", "unique": true, "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| revision | models.OneToOneField | AppModelRevision | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| indexes | ["`models.Index(fields=['application_id', 'module_id'])`"] |

---


### AppModelRevision

**Module**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.app_resource`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: Revisions of cloud-native Application's Model Resource

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| application_id | models.UUIDField | 1 | {"null": false, "type": "models.UUIDField", "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| deployed_value | models.JSONField | 1 | {"null": true, "type": "models.JSONField", "verbose_name": "`_(\u0027\u5df2\u90e8\u7f72\u7684\u5e94\u7528\u6a21\u578b\uff08JSON \u683c\u5f0f\uff09\u0027)`"} |
| has_deployed | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "`_(\u0027\u662f\u5426\u5df2\u90e8\u7f72\u0027)`"} |
| is_deleted | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "`_(\u0027\u662f\u5426\u5df2\u5220\u9664\u0027)`"} |
| is_draft | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "`_(\u0027\u662f\u5426\u8349\u7a3f\u0027)`"} |
| json_value | models.JSONField | 1 | {"type": "models.JSONField", "verbose_name": "`_(\u0027\u5e94\u7528\u6a21\u578b\uff08JSON \u683c\u5f0f\uff09\u0027)`"} |
| module_id | models.UUIDField | 1 | {"null": false, "type": "models.UUIDField", "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |
| version | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "verbose_name": "`_(\u0027\u6a21\u578b\u7248\u672c\u0027)`"} |
| yaml_value | models.TextField | 1 | {"type": "models.TextField", "verbose_name": "`_(\u0027\u5e94\u7528\u6a21\u578b\uff08YAML \u683c\u5f0f\uff09\u0027)`"} |


#### Meta Options

| Option | Value |
|--------|-------|
| indexes | ["`models.Index(fields=['application_id', 'module_id'])`"] |

---


### ConfigMapSource

**Module**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.mount`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: ConfigMap 类型的挂载资源

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| application_id | models.UUIDField | 1 | {"null": false, "type": "models.UUIDField", "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| data | models.JSONField | 1 | {"default": "`dict`", "type": "models.JSONField"} |
| display_name | models.CharField | 1 | {"help_text": "`_(\u0027\u6302\u8f7d\u8d44\u6e90\u5c55\u793a\u540d\u79f0\u0027)`", "max_length": 63, "null": true, "type": "models.CharField"} |
| environment_name | models.CharField | 1 | {"choices": "`MountEnvName.get_choices()`", "max_length": 16, "null": false, "type": "models.CharField", "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| module_id | models.UUIDField | 1 | {"null": true, "type": "models.UUIDField", "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |
| name | models.CharField | 1 | {"help_text": "`_(\u0027\u6302\u8f7d\u8d44\u6e90\u540d\u0027)`", "max_length": 63, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['name', 'application_id', 'environment_name'] |

---


### Mount

**Module**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.mount`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: 挂载配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| environment_name | models.CharField | 1 | {"choices": "`MountEnvName.get_choices()`", "max_length": 16, "null": false, "type": "models.CharField", "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| module_id | models.UUIDField | 1 | {"null": false, "type": "models.UUIDField", "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |
| mount_path | models.CharField | 1 | {"max_length": 128, "type": "models.CharField"} |
| name | models.CharField | 1 | {"help_text": "`_(\u0027\u6302\u8f7d\u70b9\u7684\u540d\u79f0\u0027)`", "max_length": 63, "type": "models.CharField"} |
| source_type | models.CharField | 1 | {"choices": "`VolumeSourceType.get_choices()`", "max_length": 32, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['module_id', 'mount_path', 'environment_name'] |

---


### PersistentStorageSource

**Module**: `apiserver.paasng.paas_wl.bk_app.cnative.specs.models.mount`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: 持久存储类型的挂载资源

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| application_id | models.UUIDField | 1 | {"null": false, "type": "models.UUIDField", "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| display_name | models.CharField | 1 | {"help_text": "`_(\u0027\u6302\u8f7d\u8d44\u6e90\u5c55\u793a\u540d\u79f0\u0027)`", "max_length": 63, "null": true, "type": "models.CharField"} |
| environment_name | models.CharField | 1 | {"choices": "`MountEnvName.get_choices()`", "max_length": 16, "null": false, "type": "models.CharField", "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| module_id | models.UUIDField | 1 | {"null": true, "type": "models.UUIDField", "verbose_name": "`_(\u0027\u6240\u5c5e\u6a21\u5757\u0027)`"} |
| name | models.CharField | 1 | {"help_text": "`_(\u0027\u6302\u8f7d\u8d44\u6e90\u540d\u0027)`", "max_length": 63, "type": "models.CharField"} |
| storage_class_name | models.CharField | 1 | {"max_length": 63, "type": "models.CharField"} |
| storage_size | models.CharField | 1 | {"max_length": 63, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['name', 'application_id', 'environment_name'] |

---


### AppMetricsMonitor

**Module**: `apiserver.paasng.paas_wl.bk_app.monitoring.app_monitor.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| is_enabled | models.BooleanField | 1 | {"default": true, "help_text": "\u662f\u5426\u542f\u52a8 AppMetrics", "type": "models.BooleanField"} |
| port | models.IntegerField | 1 | {"help_text": "Service \u7aef\u53e3", "type": "models.IntegerField"} |
| target_port | models.IntegerField | 1 | {"help_text": "\u5bb9\u5668\u5185\u7684\u7aef\u53e3", "type": "models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.OneToOneField | `WlApp` | N/A | `models.CASCADE` |


---


### ProcessProbe

**Module**: `apiserver.paasng.paas_wl.bk_app.processes.models`  
**Line**: 1  
**Base Classes**: models.Model  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| failure_threshold | models.PositiveIntegerField | 1 | {"default": 3, "type": "models.PositiveIntegerField"} |
| initial_delay_seconds | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField"} |
| period_seconds | models.PositiveIntegerField | 1 | {"default": 10, "type": "models.PositiveIntegerField"} |
| probe_type | models.CharField | 1 | {"choices": "`ProbeType.get_django_choices()`", "max_length": 255, "type": "models.CharField"} |
| process_type | models.CharField | 1 | {"max_length": 255, "type": "models.CharField"} |
| success_threshold | models.PositiveIntegerField | 1 | {"default": 1, "type": "models.PositiveIntegerField"} |
| timeout_seconds | models.PositiveIntegerField | 1 | {"default": 1, "type": "models.PositiveIntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | api.App | process_probe | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['app', 'process_type', 'probe_type'] |

---


### ProcessSpec

**Module**: `apiserver.paasng.paas_wl.bk_app.processes.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| autoscaling | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| name | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| port | models.IntegerField | 1 | {"help_text": "\u5bb9\u5668\u7aef\u53e3", "null": true, "type": "models.IntegerField"} |
| proc_command | models.TextField | 1 | {"help_text": "\u8fdb\u7a0b\u542f\u52a8\u547d\u4ee4(\u5305\u542b\u5b8c\u6574\u547d\u4ee4\u548c\u53c2\u6570\u7684\u5b57\u7b26\u4e32), \u53ea\u80fd\u4e0e command/args \u4e8c\u9009\u4e00", "null": true, "type": "models.TextField"} |
| target_replicas | models.IntegerField | 1 | {"default": 1, "type": "models.IntegerField"} |
| target_status | models.CharField | 1 | {"default": "start", "max_length": 32, "type": "models.CharField"} |
| type | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| engine_app | models.ForeignKey | api.App | process_specs | `models.DO_NOTHING` |
| plan | models.ForeignKey | `ProcessSpecPlan` | N/A | `models.CASCADE` |


---


### ProcessSpecPlan

**Module**: `apiserver.paasng.paas_wl.bk_app.processes.models`  
**Line**: 1  
**Base Classes**: models.Model  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| created | models.DateTimeField | 1 | {"auto_now_add": true, "type": "models.DateTimeField"} |
| is_active | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u53ef\u7528"} |
| max_replicas | models.IntegerField | 1 | {"type": "models.IntegerField"} |
| name | models.CharField | 1 | {"db_index": true, "max_length": 32, "type": "models.CharField"} |
| updated | models.DateTimeField | 1 | {"auto_now": true, "type": "models.DateTimeField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| get_latest_by | created |

---


### APIServer

**Module**: `apiserver.paasng.paas_wl.infras.cluster.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.UuidAuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| host | models.CharField | 1 | {"help_text": "API Server \u7684\u540e\u7aef\u5730\u5740", "max_length": 255, "type": "models.CharField"} |
| overridden_hostname | models.CharField | 1 | {"blank": true, "default": null, "help_text": "\u5728\u8bf7\u6c42\u8be5 APIServer \u65f6, \u4f7f\u7528\u8be5 hostname \u66ff\u6362\u5177\u4f53\u7684 backend \u4e2d\u7684 hostname", "max_length": 255, "null": true, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| cluster | models.ForeignKey | `Cluster` | api_servers | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['cluster', 'host'] |

---


### Cluster

**Module**: `apiserver.paasng.paas_wl.infras.cluster.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.UuidAuditedModel  
**Description**: 应用集群

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| description | models.TextField | 1 | {"blank": true, "help_text": "\u63cf\u8ff0\u4fe1\u606f", "type": "models.TextField"} |
| is_default | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u4e3a\u9ed8\u8ba4\u96c6\u7fa4", "null": true, "type": "models.BooleanField"} |
| name | models.CharField | 1 | {"help_text": "name of the cluster", "max_length": 32, "type": "models.CharField", "unique": true} |
| region | models.CharField | 1 | {"db_index": true, "max_length": 32, "type": "models.CharField"} |
| token_type | models.IntegerField | 1 | {"null": true, "type": "models.IntegerField"} |
| type | models.CharField | 1 | {"default": "`ClusterType.NORMAL`", "help_text": "cluster type", "max_length": 32, "type": "models.CharField"} |



---


### AppAddOn

**Module**: `apiserver.paasng.paas_wl.infras.resource_templates.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**Description**: 应用挂件关联实例

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| enabled | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| spec | models.TextField | 1 | {"type": "models.TextField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | `WlApp` | add_ons | `models.CASCADE` |
| template | models.ForeignKey | `AppAddOnTemplate` | instances | `models.CASCADE` |


---


### AppAddOnTemplate

**Module**: `apiserver.paasng.paas_wl.infras.resource_templates.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**Description**: 应用挂件模版

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| enabled | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| region | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| spec | models.TextField | 1 | {"type": "models.TextField"} |
| type | models.IntegerField | 1 | {"default": "`AppAddOnType.SIMPLE_SIDECAR.value`", "type": "models.IntegerField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['region', 'name'] |

---


### AuditedModel

**Module**: `apiserver.paasng.paas_wl.utils.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: Audited model with 'created' and 'updated' fields.

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| created | models.DateTimeField | 1 | {"auto_now_add": true, "type": "models.DateTimeField"} |
| updated | models.DateTimeField | 1 | {"auto_now": true, "type": "models.DateTimeField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### TimestampedModel

**Module**: `apiserver.paasng.paas_wl.utils.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: Model with 'created' and 'updated' fields.

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| created | models.DateTimeField | 1 | {"auto_now_add": true, "type": "models.DateTimeField"} |
| region | models.CharField | 1 | {"help_text": "\u90e8\u7f72\u533a\u57df", "max_length": 32, "type": "models.CharField"} |
| updated | models.DateTimeField | 1 | {"auto_now": true, "type": "models.DateTimeField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### UuidAuditedModel

**Module**: `apiserver.paasng.paas_wl.utils.models`  
**Line**: 1  
**Base Classes**: apiserver.paasng.paas_wl.utils.models.AuditedModel  
**Description**: Add a UUID primary key to an class`AuditedModel`.

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| uuid | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "type": "models.UUIDField", "unique": true} |


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### AppImageCredential

**Module**: `apiserver.paasng.paas_wl.workloads.images.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**Description**: ImageCredential of applications, each object(entry) represents an (username + password) pair for a registry

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| registry | models.CharField | 1 | {"max_length": 255, "type": "models.CharField"} |
| username | models.CharField | 1 | {"blank": false, "max_length": 32, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | api.App | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['app', 'registry'] |

---


### AppUserCredential

**Module**: `apiserver.paasng.paas_wl.workloads.images.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.UuidAuditedModel  
**Description**: App owned UserCredential, aka (Username + Password) pair

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| application_id | models.UUIDField | 1 | {"null": false, "type": "models.UUIDField", "verbose_name": "`_(\u0027\u6240\u5c5e\u5e94\u7528\u0027)`"} |
| description | models.TextField | 1 | {"help_text": "\u63cf\u8ff0", "type": "models.TextField"} |
| name | models.CharField | 1 | {"help_text": "\u51ed\u8bc1\u540d\u79f0", "max_length": 32, "type": "models.CharField"} |
| username | models.CharField | 1 | {"help_text": "\u8d26\u53f7", "max_length": 64, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['application_id', 'name'] |

---


### EgressRule

**Module**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.AuditedModel  
**Description**: BCS Egress.spec.rules

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| dst_port | models.IntegerField | 1 | {"type": "models.IntegerField"} |
| host | models.CharField | 1 | {"max_length": 128, "type": "models.CharField"} |
| protocol | models.CharField | 1 | {"choices": "`NetworkProtocol.get_django_choices()`", "max_length": 32, "type": "models.CharField"} |
| service | models.CharField | 1 | {"max_length": 128, "type": "models.CharField"} |
| src_port | models.IntegerField | 1 | {"type": "models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| spec | models.ForeignKey | `EgressSpec` | rules | `models.CASCADE` |


---


### EgressSpec

**Module**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| cpu_limit | models.CharField | 1 | {"max_length": 16, "type": "models.CharField"} |
| memory_limit | models.CharField | 1 | {"max_length": 16, "type": "models.CharField"} |
| replicas | models.IntegerField | 1 | {"default": 1, "type": "models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| wl_app | models.OneToOneField | `WlApp` | N/A | `models.CASCADE` |


---


### RCStateAppBinding

**Module**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.AuditedModel  
**Description**: If an app was bind with one RegionClusterState instance, it means that the app will not be

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.OneToOneField | `WlApp` | N/A | `models.CASCADE` |
| state | models.ForeignKey | `RegionClusterState` | N/A | `models.CASCADE` |


---


### RegionClusterState

**Module**: `apiserver.paasng.paas_wl.workloads.networking.egress.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.AuditedModel  
**Description**: A RegionClusterState is a state which describes what the cluster is in a specified moment. it

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| cluster_name | models.CharField | 1 | {"max_length": 32, "null": true, "type": "models.CharField"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| nodes_cnt | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField"} |
| nodes_digest | models.CharField | 1 | {"db_index": true, "max_length": 64, "type": "models.CharField"} |
| region | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| get_latest_by | created |
| ordering | ['-created'] |
| unique_together | ['region', 'cluster_name', 'name'] |

---


### AppDomain

**Module**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.AuditedModel  
**Description**: Domains of applications, each object(entry) represents an (domain + path_prefix) pair.

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| host | models.CharField | 1 | {"max_length": 128, "type": "models.CharField"} |
| https_auto_redirection | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| https_enabled | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| path_prefix | models.CharField | 1 | {"default": "/", "help_text": "the accessable path for current domain", "max_length": 64, "type": "models.CharField"} |
| region | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| source | models.IntegerField | 1 | {"choices": "`make_enum_choices(AppDomainSource)`", "type": "models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | `WlApp` | N/A | `models.CASCADE` |
| cert | models.ForeignKey | AppDomainCert | N/A | `models.SET_NULL` |
| shared_cert | models.ForeignKey | AppDomainSharedCert | N/A | `models.SET_NULL` |

#### Meta Options

| Option | Value |
|--------|-------|
| db_table | services_appdomain |
| unique_together | ['region', 'host', 'path_prefix'] |

---


### AppDomainSharedCert

**Module**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`  
**Line**: 1  
**Base Classes**: apiserver.paasng.paas_wl.workloads.networking.ingress.models.BasicCert  
**Description**: Shared TLS Certifications for AppDomain, every app's domain may link to this certificate as

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| auto_match_cns | models.TextField | 1 | {"max_length": 2048, "type": "models.TextField"} |
| name | models.CharField | 1 | {"max_length": 128, "type": "models.CharField", "unique": true, "validators": ["`RegexValidator(DNS_SAFE_PATTERN)`"]} |
| region | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| db_table | services_appdomainsharedcert |

---


### AppSubpath

**Module**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.AuditedModel  
**Description**: stores application's subpaths

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| cluster_name | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| region | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| source | models.IntegerField | 1 | {"type": "models.IntegerField"} |
| subpath | models.CharField | 1 | {"max_length": 128, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | `WlApp` | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| db_table | services_appsubpath |
| unique_together | ['region', 'subpath'] |

---


### BasicCert

**Module**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`  
**Line**: 1  
**Base Classes**: paas_wl.bk_app.applications.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| name | models.CharField | 1 | {"max_length": 128, "type": "models.CharField", "unique": true, "validators": ["`RegexValidator(DNS_SAFE_PATTERN)`"]} |
| region | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### Domain

**Module**: `apiserver.paasng.paas_wl.workloads.networking.ingress.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: custom domain for application

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| environment_id | models.BigIntegerField | 1 | {"help_text": "\u5173\u8054\u7684\u73af\u5883 ID", "null": false, "type": "models.BigIntegerField"} |
| https_enabled | models.BooleanField | 1 | {"default": false, "help_text": "\u8be5\u57df\u540d\u662f\u5426\u5f00\u542f https", "null": true, "type": "models.BooleanField"} |
| module_id | models.UUIDField | 1 | {"help_text": "\u5173\u8054\u7684\u6a21\u5757 ID", "null": false, "type": "models.UUIDField"} |
| name | models.CharField | 1 | {"help_text": "\u57df\u540d", "max_length": 253, "null": false, "type": "models.CharField"} |
| path_prefix | models.CharField | 1 | {"default": "/", "help_text": "the accessable path for current domain", "max_length": 64, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| db_table | services_domain |
| unique_together | ['name', 'path_prefix', 'module_id', 'environment_id'] |

---


### Command

**Module**: `apiserver.paasng.paas_wl.workloads.release_controller.hooks.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.UuidAuditedModel  
**Description**: The Command Model, which will be used to schedule a container running `command`,

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| command | models.TextField | 1 | {"type": "models.TextField"} |
| exit_code | models.SmallIntegerField | 1 | {"help_text": "\u5bb9\u5668\u7ed3\u675f\u72b6\u6001\u7801, -1 \u8868\u793a\u672a\u77e5", "null": true, "type": "models.SmallIntegerField"} |
| int_requested_at | models.DateTimeField | 1 | {"help_text": "\u7528\u6237\u8bf7\u6c42\u4e2d\u65ad\u7684\u65f6\u95f4", "null": true, "type": "models.DateTimeField"} |
| logs_was_ready_at | models.DateTimeField | 1 | {"help_text": "Pod \u72b6\u6001\u5c31\u7eea\u5141\u8bb8\u8bfb\u53d6\u65e5\u5fd7\u7684\u65f6\u95f4", "null": true, "type": "models.DateTimeField"} |
| operator | models.CharField | 1 | {"help_text": "\u64cd\u4f5c\u8005(\u88ab\u7f16\u7801\u7684 username), \u76ee\u524d\u8be5\u5b57\u6bb5\u65e0\u610f\u4e49", "max_length": 64, "type": "models.CharField"} |
| status | models.CharField | 1 | {"choices": "`CommandStatus.get_choices()`", "default": "`CommandStatus.PENDING.value`", "max_length": 12, "type": "models.CharField"} |
| type | models.CharField | 1 | {"choices": "`CommandType.get_choices()`", "max_length": 32, "type": "models.CharField"} |
| version | models.PositiveIntegerField | 1 | {"type": "models.PositiveIntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | api.App | N/A | `models.CASCADE` |
| output_stream | models.OneToOneField | api.OutputStream | N/A | `models.CASCADE` |
| build | models.ForeignKey | api.Build | N/A | `models.CASCADE` |
| config | models.ForeignKey | api.Config | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| get_latest_by | created |
| ordering | ['-created'] |

---


### CIResourceAppEnvRelation

**Module**: `apiserver.paasng.paasng.accessories.ci.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: CI 资源

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| backend | models.CharField | 1 | {"choices": "`CIBackend.get_django_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "CI\u5f15\u64ce"} |
| enabled | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u542f\u7528"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| env | models.ForeignKey | applications.ApplicationEnvironment | ci_resources | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| get_latest_by | created |

---


### CIResourceAtom

**Module**: `apiserver.paasng.paasng.accessories.ci.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: CI 资源原子

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| backend | models.CharField | 1 | {"choices": "`CIBackend.get_django_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "CI\u5f15\u64ce"} |
| enabled | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u542f\u7528"} |
| id | models.CharField | 1 | {"db_index": true, "max_length": 64, "primary_key": true, "type": "models.CharField", "unique": true} |
| name | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| env | models.ForeignKey | applications.ApplicationEnvironment | ci_resource_atoms | `models.CASCADE` |
| resource | models.ForeignKey | `CIResourceAppEnvRelation` | related_atoms | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['env', 'name', 'backend'] |

---


### CodeEditor

**Module**: `apiserver.paasng.paasng.accessories.dev_sandbox.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  
**Description**: CodeEditor Model

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| dev_sandbox | models.OneToOneField | `DevSandbox` | code_editor | `models.CASCADE` |


---


### DevSandbox

**Module**: `apiserver.paasng.paasng.accessories.dev_sandbox.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: DevSandbox Model

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| code | models.CharField | 1 | {"help_text": "\u6c99\u7bb1\u6807\u8bc6", "max_length": 8, "type": "models.CharField", "unique": true} |
| expired_at | models.DateTimeField | 1 | {"help_text": "\u5230\u671f\u65f6\u95f4", "null": true, "type": "models.DateTimeField"} |
| status | models.CharField | 1 | {"choices": "`DevSandboxStatus.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u6c99\u7bb1\u72b6\u6001"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | `Module` | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['module', 'owner'] |

---


### CustomCollectorConfig

**Module**: `apiserver.paasng.paasng.accessories.log.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  
**Description**: 日志平台自定义采集项配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| bk_data_id | models.BigIntegerField | 1 | {"type": "models.BigIntegerField"} |
| collector_config_id | models.BigIntegerField | 1 | {"db_index": true, "help_text": "\u91c7\u96c6\u914d\u7f6eID", "type": "models.BigIntegerField"} |
| index_set_id | models.BigIntegerField | 1 | {"help_text": "\u67e5\u8be2\u65f6\u4f7f\u7528", "null": true, "type": "models.BigIntegerField"} |
| is_builtin | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| is_enabled | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| log_paths | models.JSONField | 1 | {"type": "models.JSONField"} |
| log_type | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| name_en | models.CharField | 1 | {"db_index": true, "help_text": "5-50\u4e2a\u5b57\u7b26\uff0c\u4ec5\u5305\u542b\u5b57\u6bcd\u6570\u5b57\u4e0b\u5212\u7ebf, \u67e5\u8be2\u7d22\u5f15\u662f name_en-*", "max_length": 50, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | `Module` | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['module', 'name_en'] |

---


### ElasticSearchConfig

**Module**: `apiserver.paasng.paasng.accessories.log.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  
**Description**: ES查询配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| backend_type | models.CharField | 1 | {"help_text": "\u65e5\u5fd7\u540e\u7aef\u7c7b\u578b, \u53ef\u9009 \u0027es\u0027, \u0027bkLog\u0027 ", "max_length": 16, "type": "models.CharField"} |
| collector_config_id | models.CharField | 1 | {"help_text": "\u91c7\u96c6\u914d\u7f6eID", "max_length": 64, "type": "models.CharField", "unique": true} |



---


### ProcessLogQueryConfig

**Module**: `apiserver.paasng.paasng.accessories.log.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  
**Description**: 进程日志查询配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| process_type | models.CharField | 1 | {"blank": true, "max_length": 16, "null": true, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| env | models.ForeignKey | `ModuleEnvironment` | N/A | `models.CASCADE` |
| stdout | models.ForeignKey | `ElasticSearchConfig` | related_stdout | `models.SET_NULL` |
| json | models.ForeignKey | `ElasticSearchConfig` | related_json | `models.SET_NULL` |
| ingress | models.ForeignKey | `ElasticSearchConfig` | related_ingress | `models.SET_NULL` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['env', 'process_type'] |

---


### ProcessStructureLogCollectorConfig

**Module**: `apiserver.paasng.paasng.accessories.log.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 进程结构化日志采集配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| collector_config_id | models.BigAutoField | 1 | {"primary_key": true, "type": "models.BigAutoField"} |
| process_type | models.CharField | 1 | {"help_text": "\u8fdb\u7a0b\u7c7b\u578b(\u540d\u79f0)", "max_length": 16, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | `Application` | N/A | `models.CASCADE` |
| env | models.ForeignKey | `ModuleEnvironment` | N/A | `models.CASCADE` |


---


### DisplayOptions

**Module**: `apiserver.paasng.paasng.accessories.publish.market.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: app展示相关的属性

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| contact | models.CharField | 1 | {"blank": true, "max_length": 128, "null": true, "type": "models.CharField"} |
| height | models.IntegerField | 1 | {"default": 550, "help_text": "\u5e94\u7528\u9875\u9762\u9ad8\u5ea6\uff0c\u5fc5\u987b\u4e3a\u6574\u6570\uff0c\u5355\u4f4d\u4e3apx", "type": "models.IntegerField"} |
| is_win_maximize | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| open_mode | models.CharField | 1 | {"choices": "`constant.OpenMode.get_django_choices()`", "default": "`constant.OpenMode.NEW_TAB.value`", "max_length": 20, "type": "models.CharField"} |
| resizable | models.BooleanField | 1 | {"default": true, "help_text": "\u9009\u9879\uff1atrue(\u53ef\u4ee5\u62c9\u4f38)\uff0cfalse(\u4e0d\u53ef\u4ee5\u62c9\u4f38)", "type": "models.BooleanField"} |
| visible | models.BooleanField | 1 | {"default": true, "help_text": "\u9009\u9879: true(\u662f)\uff0cfalse(\u5426)", "type": "models.BooleanField"} |
| width | models.IntegerField | 1 | {"default": 890, "help_text": "\u5e94\u7528\u9875\u9762\u5bbd\u5ea6\uff0c\u5fc5\u987b\u4e3a\u6574\u6570\uff0c\u5355\u4f4d\u4e3apx", "type": "models.IntegerField"} |
| win_bars | models.BooleanField | 1 | {"default": true, "help_text": "\u9009\u9879: true(on)\uff0cfalse(off)", "type": "models.BooleanField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| product | models.OneToOneField | `Product` | N/A | `models.CASCADE` |


---


### MarketConfig

**Module**: `apiserver.paasng.paasng.accessories.publish.market.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: 应用市场相关功能配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| auto_enable_when_deploy | models.BooleanField | 1 | {"null": true, "type": "models.BooleanField", "verbose_name": "\u6210\u529f\u90e8\u7f72\u4e3b\u6a21\u5757\u6b63\u5f0f\u73af\u5883\u540e, \u662f\u5426\u81ea\u52a8\u6253\u5f00\u5e02\u573a"} |
| custom_domain_url | models.URLField | 1 | {"blank": true, "null": true, "type": "models.URLField", "verbose_name": "\u7ed1\u5b9a\u7684\u72ec\u7acb\u57df\u540d\u8bbf\u95ee\u5730\u5740"} |
| enabled | models.BooleanField | 1 | {"type": "models.BooleanField", "verbose_name": "\u662f\u5426\u5f00\u542f"} |
| prefer_https | models.BooleanField | 1 | {"null": true, "type": "models.BooleanField", "verbose_name": "[deprecated] \u4ec5\u4e3a False \u65f6\u5f3a\u5236\u4f7f\u7528 http, \u5426\u5219\u4fdd\u6301\u4e0e\u96c6\u7fa4 https_enabled \u72b6\u6001\u4e00\u81f4"} |
| source_tp_url | models.URLField | 1 | {"blank": true, "null": true, "type": "models.URLField", "verbose_name": "\u7b2c\u4e09\u65b9\u8bbf\u95ee\u5730\u5740"} |
| source_url_type | models.SmallIntegerField | 1 | {"type": "models.SmallIntegerField", "verbose_name": "\u8bbf\u95ee\u5730\u5740\u7c7b\u578b"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.OneToOneField | `Application` | market_config | `models.CASCADE` |
| source_module | models.ForeignKey | `Module` | N/A | `models.CASCADE` |


---


### Product

**Module**: `apiserver.paasng.paasng.accessories.publish.market.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: 蓝鲸应用: 开发者中心的编辑属性

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| code | models.CharField | 1 | {"help_text": "\u5e94\u7528\u7f16\u7801", "max_length": 64, "type": "models.CharField", "unique": true} |
| state | models.SmallIntegerField | 1 | {"choices": "`constant.AppState.get_choices()`", "default": 1, "help_text": "\u5e94\u7528\u72b6\u6001", "type": "models.SmallIntegerField"} |
| type | models.SmallIntegerField | 1 | {"choices": "`constant.AppType.get_choices()`", "help_text": "\u6309\u5b9e\u73b0\u65b9\u5f0f\u5206\u7c7b", "type": "models.SmallIntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.OneToOneField | `Application` | N/A | `models.CASCADE` |
| tag | models.ForeignKey | `Tag` | N/A | `models.SET_NULL` |


---


### Tag

**Module**: `apiserver.paasng.paasng.accessories.publish.market.models`  
**Line**: 1  
**Base Classes**: models.Model  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| enabled | models.BooleanField | 1 | {"default": true, "help_text": "\u521b\u5efa\u5e94\u7528\u65f6\u662f\u5426\u53ef\u9009\u62e9\u8be5\u5206\u7c7b", "type": "models.BooleanField"} |
| index | models.IntegerField | 1 | {"default": 0, "help_text": "\u663e\u793a\u6392\u5e8f\u5b57\u6bb5", "type": "models.IntegerField"} |
| name | models.CharField | 1 | {"help_text": "\u5206\u7c7b\u540d\u79f0", "max_length": 64, "type": "models.CharField"} |
| region | models.CharField | 1 | {"help_text": "\u90e8\u7f72\u533a\u57df", "max_length": 32, "type": "models.CharField"} |
| remark | models.CharField | 1 | {"blank": true, "help_text": "\u5907\u6ce8", "max_length": 255, "null": true, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| parent | models.ForeignKey | self | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| ordering | ['index', 'id'] |

---


### TagMap

**Module**: `apiserver.paasng.paasng.accessories.publish.sync_market.models`  
**Line**: 1  
**Base Classes**: django_models.Model  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| remote_id | django_models.IntegerField | 1 | {"db_index": true, "type": "django_models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| tag | django_models.OneToOneField | `market_models.Tag` | N/A | `django_models.CASCADE` |


---


### RemoteServiceEngineAppAttachment

**Module**: `apiserver.paasng.paasng.accessories.servicehub.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: Binding relationship of engine app <-> remote service plan

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| credentials_enabled | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u4f7f\u7528\u51ed\u8bc1"} |
| plan_id | models.UUIDField | 1 | {"type": "models.UUIDField", "verbose_name": "\u8fdc\u7a0b\u589e\u5f3a\u670d\u52a1 Plan ID"} |
| service_id | models.UUIDField | 1 | {"type": "models.UUIDField", "verbose_name": "\u8fdc\u7a0b\u589e\u5f3a\u670d\u52a1 ID"} |
| service_instance_id | models.UUIDField | 1 | {"null": true, "type": "models.UUIDField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| engine_app | models.ForeignKey | engine.EngineApp | remote_service_attachment | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['service_id', 'engine_app'] |

---


### RemoteServiceModuleAttachment

**Module**: `apiserver.paasng.paasng.accessories.servicehub.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: Binding relationship of module <-> remote service

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| service_id | models.UUIDField | 1 | {"type": "models.UUIDField", "verbose_name": "\u8fdc\u7a0b\u589e\u5f3a\u670d\u52a1 ID"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | modules.Module | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['service_id', 'module'] |

---


### ServiceEngineAppAttachment

**Module**: `apiserver.paasng.paasng.accessories.servicehub.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| credentials_enabled | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u4f7f\u7528\u51ed\u8bc1"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| engine_app | models.ForeignKey | engine.EngineApp | service_attachment | `models.CASCADE` |
| service | models.ForeignKey | `Service` | N/A | `models.CASCADE` |
| plan | models.ForeignKey | `Plan` | N/A | `models.CASCADE` |
| service_instance | models.ForeignKey | `ServiceInstance` | service_attachment | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['service', 'engine_app'] |

---


### ServiceModuleAttachment

**Module**: `apiserver.paasng.paasng.accessories.servicehub.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: Module <-> Local Service relationship

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | modules.Module | N/A | `models.CASCADE` |
| service | models.ForeignKey | `Service` | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['service', 'module'] |

---


### SharedServiceAttachment

**Module**: `apiserver.paasng.paasng.accessories.servicehub.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: Share a service binding relationship from other modules

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| ref_attachment_pk | models.IntegerField | 1 | {"type": "models.IntegerField", "verbose_name": "\u88ab\u5171\u4eab\u7684\u670d\u52a1\u7ed1\u5b9a\u5173\u7cfb\u4e3b\u952e"} |
| service_id | models.UUIDField | 1 | {"type": "models.UUIDField", "verbose_name": "\u589e\u5f3a\u670d\u52a1 ID"} |
| service_type | models.CharField | 1 | {"max_length": 16, "type": "models.CharField", "verbose_name": "\u589e\u5f3a\u670d\u52a1\u7c7b\u578b"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | modules.Module | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['module', 'service_type', 'service_id'] |

---


### Plan

**Module**: `apiserver.paasng.paasng.accessories.services.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| description | models.CharField | 1 | {"blank": true, "max_length": 1024, "type": "models.CharField", "verbose_name": "\u65b9\u6848\u7b80\u4ecb"} |
| is_active | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u53ef\u7528"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| service | models.ForeignKey | Service | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['service', 'name'] |

---


### PreCreatedInstance

**Module**: `apiserver.paasng.paasng.accessories.services.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  
**Description**: 预创建的服务实例

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| is_allocated | models.BooleanField | 1 | {"default": false, "help_text": "\u5b9e\u4f8b\u662f\u5426\u5df2\u88ab\u5206\u914d", "type": "models.BooleanField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| plan | models.ForeignKey | Plan | N/A | `models.SET_NULL` |


---


### ResourceId

**Module**: `apiserver.paasng.paasng.accessories.services.models`  
**Line**: 1  
**Base Classes**: models.Model  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| namespace | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| uid | models.CharField | 1 | {"db_index": true, "max_length": 64, "null": false, "type": "models.CharField", "unique": true} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['namespace', 'uid'] |

---


### Service

**Module**: `apiserver.paasng.paasng.accessories.services.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| available_languages | models.CharField | 1 | {"blank": true, "max_length": 1024, "null": true, "type": "models.CharField", "verbose_name": "\u652f\u6301\u7f16\u7a0b\u8bed\u8a00"} |
| is_active | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u53ef\u7528"} |
| is_visible | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u53ef\u89c1"} |
| logo_b64 | models.TextField | 1 | {"blank": true, "null": true, "type": "models.TextField", "verbose_name": "\u670d\u52a1 logo \u7684\u5730\u5740, \u652f\u6301base64\u683c\u5f0f"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "verbose_name": "\u670d\u52a1\u540d\u79f0"} |
| region | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| category | models.ForeignKey | `ServiceCategory` | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['region', 'name'] |

---


### ServiceCategory

**Module**: `apiserver.paasng.paasng.accessories.services.models`  
**Line**: 1  
**Base Classes**: models.Model  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| sort_priority | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField"} |



---


### ServiceInstance

**Module**: `apiserver.paasng.paasng.accessories.services.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| to_be_deleted | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| service | models.ForeignKey | Service | N/A | `models.CASCADE` |
| plan | models.ForeignKey | Plan | N/A | `models.CASCADE` |


---


### AppModuleTagRel

**Module**: `apiserver.paasng.paasng.accessories.smart_advisor.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: A M2M relationship table for storing the relationship between application module and AppTag

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| created | models.DateTimeField | 1 | {"auto_now_add": true, "type": "models.DateTimeField"} |
| source | models.CharField | 1 | {"blank": false, "max_length": 32, "type": "models.CharField"} |
| tag_str | models.CharField | 1 | {"blank": false, "max_length": 128, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | modules.Module | tag_rels | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['module', 'tag_str'] |

---


### DeployFailurePattern

**Module**: `apiserver.paasng.paasng.accessories.smart_advisor.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: Stores common failure patterns for failed deployments

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| created | models.DateTimeField | 1 | {"default": "`timezone.now`", "type": "models.DateTimeField"} |
| tag_str | models.CharField | 1 | {"blank": false, "max_length": 128, "type": "models.CharField"} |
| type | models.IntegerField | 1 | {"default": "`DeployFailurePatternType.REGULAR_EXPRESSION`", "type": "models.IntegerField"} |
| value | models.CharField | 1 | {"blank": false, "max_length": 2048, "type": "models.CharField"} |



---


### DocumentaryLink

**Module**: `apiserver.paasng.paasng.accessories.smart_advisor.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: Links from document systems including blueking doc and other opensource documentations

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| created | models.DateTimeField | 1 | {"default": "`timezone.now`", "type": "models.DateTimeField"} |
| location | models.CharField | 1 | {"blank": false, "max_length": 256, "type": "models.CharField"} |
| priority | models.IntegerField | 1 | {"default": 1, "type": "models.IntegerField"} |



---


### BkPluginDistributor

**Module**: `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: A "Distributor" is responsible for providing a collection of BkPlugins to a group of users,

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| bk_app_code | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u4f7f\u7528\u65b9\u6240\u7ed1\u5b9a\u7684\u84dd\u9cb8\u5e94\u7528\u4ee3\u53f7", "max_length": 20, "type": "models.CharField", "unique": true} |
| code_name | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u4f7f\u7528\u65b9\u7684\u82f1\u6587\u4ee3\u53f7\uff0c\u53ef\u66ff\u4ee3\u4e3b\u952e\u4f7f\u7528", "max_length": 32, "type": "models.CharField", "unique": true} |
| introduction | models.CharField | 1 | {"blank": true, "max_length": 512, "null": true, "type": "models.CharField"} |
| name | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u4f7f\u7528\u65b9\u540d\u79f0", "max_length": 32, "type": "models.CharField", "unique": true} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| plugins | models.ManyToManyField | `Application` | distributors | N/A |


---


### BkPluginProfile

**Module**: `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: Profile which storing extra information for BkPlugins

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| api_gw_id | models.IntegerField | 1 | {"null": true, "type": "models.IntegerField"} |
| api_gw_last_synced_at | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField"} |
| api_gw_name | models.CharField | 1 | {"blank": true, "help_text": "\u4e3a\u7a7a\u65f6\u8868\u793a\u4ece\u672a\u6210\u529f\u540c\u6b65\u8fc7\uff0c\u6682\u65e0\u5df2\u7ed1\u5b9a\u7f51\u5173", "max_length": 32, "null": true, "type": "models.CharField"} |
| contact | models.CharField | 1 | {"blank": true, "help_text": "\u4f7f\u7528 ; \u5206\u9694\u7684\u7528\u6237\u540d", "max_length": 128, "null": true, "type": "models.CharField"} |
| introduction | models.CharField | 1 | {"blank": true, "help_text": "\u63d2\u4ef6\u7b80\u4ecb", "max_length": 512, "null": true, "type": "models.CharField"} |
| pre_distributor_codes | models.JSONField | 1 | {"blank": true, "null": true, "type": "models.JSONField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.OneToOneField | `Application` | bk_plugin_profile | `models.CASCADE` |
| tag | models.ForeignKey | BkPluginTag | N/A | `models.SET_NULL` |


---


### BkPluginTag

**Module**: `apiserver.paasng.paasng.bk_plugins.bk_plugins.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: Plugins and applications use different markets, and plugins should have their own separate tags

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| code_name | models.CharField | 1 | {"help_text": "\u5206\u7c7b\u82f1\u6587\u540d\u79f0\uff0c\u53ef\u66ff\u4ee3\u4e3b\u952e\u4f7f\u7528", "max_length": 32, "type": "models.CharField", "unique": true} |
| name | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u4f7f\u7528\u65b9\u540d\u79f0", "max_length": 32, "type": "models.CharField", "unique": true} |
| priority | models.IntegerField | 1 | {"default": 0, "help_text": "\u6570\u5b57\u8d8a\u5927\uff0c\u4f18\u5148\u7ea7\u8d8a\u9ad8", "type": "models.IntegerField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| ordering | ['-priority', 'name'] |

---


### PluginGradeManager

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| grade_manager_id | models.IntegerField | 1 | {"help_text": "\u5206\u7ea7\u7ba1\u7406\u5458 ID", "type": "models.IntegerField"} |
| pd_id | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u7c7b\u578b\u6807\u8bc6", "max_length": 64, "type": "models.CharField"} |
| plugin_id | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u6807\u8bc6", "max_length": 32, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['pd_id', 'plugin_id', 'grade_manager_id'] |

---


### PluginUserGroup

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| pd_id | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u7c7b\u578b\u6807\u8bc6", "max_length": 64, "type": "models.CharField"} |
| plugin_id | models.CharField | 1 | {"help_text": "\u63d2\u4ef6\u6807\u8bc6", "max_length": 32, "type": "models.CharField"} |
| role | models.IntegerField | 1 | {"default": "`PluginRole.DEVELOPER.value`", "type": "models.IntegerField"} |
| user_group_id | models.IntegerField | 1 | {"help_text": "\u6743\u9650\u4e2d\u5fc3\u7528\u6237\u7ec4 ID", "type": "models.IntegerField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['pd_id', 'plugin_id', 'role'] |

---


### PluginBasicInfoDefinition

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| access_mode | models.CharField | 1 | {"default": "`PluginBasicInfoAccessMode.READWRITE`", "max_length": 16, "type": "models.CharField", "verbose_name": "\u57fa\u672c\u4fe1\u606f\u67e5\u770b\u6a21\u5f0f"} |
| extra_fields_order | models.JSONField | 1 | {"default": "`list`", "type": "models.JSONField"} |
| release_method | models.CharField | 1 | {"max_length": 16, "type": "models.CharField", "verbose_name": "\u53d1\u5e03\u65b9\u5f0f"} |
| repository_group | models.CharField | 1 | {"max_length": 255, "type": "models.CharField", "verbose_name": "\u63d2\u4ef6\u4ee3\u7801\u521d\u59cb\u5316\u4ed3\u5e93\u7ec4"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| pd | models.OneToOneField | `PluginDefinition` | basic_info_definition | `models.CASCADE` |


---


### PluginConfigInfoDefinition

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| docs | models.CharField | 1 | {"default": "", "max_length": 255, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| pd | models.OneToOneField | `PluginDefinition` | config_definition | `models.CASCADE` |


---


### PluginDefinition

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| administrator | models.JSONField | 1 | {"type": "models.JSONField"} |
| docs | models.CharField | 1 | {"max_length": 255, "type": "models.CharField"} |
| identifier | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "unique": true} |
| logo | models.CharField | 1 | {"max_length": 255, "type": "models.CharField"} |



---


### PluginMarketInfoDefinition

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| extra_fields_order | models.JSONField | 1 | {"default": "`list`", "type": "models.JSONField"} |
| storage | models.CharField | 1 | {"max_length": 16, "type": "models.CharField", "verbose_name": "\u5b58\u50a8\u65b9\u5f0f"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| pd | models.OneToOneField | `PluginDefinition` | market_info_definition | `models.CASCADE` |


---


### PluginVisibleRangeDefinition

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.definitions`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| pd | models.OneToOneField | `PluginDefinition` | visible_range_definition | `models.CASCADE` |


---


### ApprovalService

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  
**Description**: 审批服务信息

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| service_id | models.IntegerField | 1 | {"help_text": "\u7528\u4e8e\u5728 ITSM \u4e0a\u63d0\u7533\u8bf7\u5355\u636e", "type": "models.IntegerField", "verbose_name": "\u5ba1\u6279\u670d\u52a1ID"} |
| service_name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "unique": true, "verbose_name": "\u5ba1\u6279\u670d\u52a1\u540d\u79f0"} |



---


### OperationRecord

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 插件操作记录

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| action | models.CharField | 1 | {"choices": "`constants.ActionTypes.get_choices()`", "max_length": 32, "type": "models.CharField"} |
| specific | models.CharField | 1 | {"max_length": 255, "null": true, "type": "models.CharField"} |
| subject | models.CharField | 1 | {"choices": "`constants.SubjectTypes.get_choices()`", "max_length": 32, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| plugin | models.ForeignKey | `PluginInstance` | N/A | `models.CASCADE` |


---


### PluginConfig

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 插件配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| row | models.JSONField | 1 | {"default": "`dict`", "type": "models.JSONField", "verbose_name": "\u914d\u7f6e\u5185\u5bb9(1\u884c), \u683c\u5f0f {\u0027column_key\u0027: \u0027value\u0027}"} |
| unique_key | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "verbose_name": "\u552f\u4e00\u6807\u8bc6"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| plugin | models.ForeignKey | `PluginInstance` | configs | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['plugin', 'unique_key'] |

---


### PluginInstance

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  
**Description**: 插件实例

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| extra_fields | models.JSONField | 1 | {"type": "models.JSONField", "verbose_name": "\u989d\u5916\u5b57\u6bb5"} |
| id | models.CharField | 1 | {"help_text": "\u63d2\u4ef6id", "max_length": 32, "type": "models.CharField"} |
| is_deleted | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u5df2\u5220\u9664", "type": "models.BooleanField"} |
| language | models.CharField | 1 | {"help_text": "\u5197\u4f59\u5b57\u6bb5, \u7528\u4e8e\u51cf\u5c11\u67e5\u8be2\u6b21\u6570", "max_length": 16, "type": "models.CharField", "verbose_name": "\u5f00\u53d1\u8bed\u8a00"} |
| publisher | models.CharField | 1 | {"default": "", "max_length": 64, "type": "models.CharField", "verbose_name": "\u63d2\u4ef6\u53d1\u5e03\u8005"} |
| repo_type | models.CharField | 1 | {"max_length": 16, "null": true, "type": "models.CharField", "verbose_name": "\u6e90\u7801\u6258\u7ba1\u7c7b\u578b"} |
| repository | models.CharField | 1 | {"max_length": 255, "type": "models.CharField"} |
| status | models.CharField | 1 | {"choices": "`constants.PluginStatus.get_choices()`", "default": "`constants.PluginStatus.WAITING_APPROVAL`", "max_length": 16, "type": "models.CharField", "verbose_name": "\u63d2\u4ef6\u72b6\u6001"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| pd | models.ForeignKey | PluginDefinition | N/A | `models.SET_NULL` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['pd', 'id'] |

---


### PluginMarketInfo

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 插件市场信息

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| category | models.CharField | 1 | {"db_index": true, "max_length": 64, "type": "models.CharField", "verbose_name": "\u5206\u7c7b"} |
| contact | models.TextField | 1 | {"help_text": "\u4ee5\u5206\u53f7(;)\u5206\u5272", "type": "models.TextField", "verbose_name": "\u8054\u7cfb\u4eba"} |
| extra_fields | models.JSONField | 1 | {"type": "models.JSONField", "verbose_name": "\u989d\u5916\u5b57\u6bb5"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| plugin | models.OneToOneField | `PluginInstance` | N/A | `models.CASCADE` |


---


### PluginRelease

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 插件发布版本

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| comment | models.TextField | 1 | {"type": "models.TextField", "verbose_name": "\u7248\u672c\u65e5\u5fd7"} |
| extra_fields | models.JSONField | 1 | {"type": "models.JSONField", "verbose_name": "\u989d\u5916\u5b57\u6bb5"} |
| gray_status | models.CharField | 1 | {"default": "`constants.GrayReleaseStatus.IN_GRAY`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u7070\u5ea6\u53d1\u5e03\u72b6\u6001"} |
| is_rolled_back | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u5df2\u56de\u6eda", "type": "models.BooleanField"} |
| retryable | models.BooleanField | 1 | {"default": true, "help_text": "\u5931\u8d25\u540e\u662f\u5426\u53ef\u91cd\u8bd5", "type": "models.BooleanField"} |
| semver_type | models.CharField | 1 | {"help_text": "\u8be5\u5b57\u6bb5\u53ea\u7528\u4e8e\u81ea\u52a8\u751f\u6210\u7248\u672c\u53f7\u7684\u63d2\u4ef6", "max_length": 16, "null": true, "type": "models.CharField", "verbose_name": "\u8bed\u4e49\u5316\u7248\u672c\u7c7b\u578b"} |
| source_hash | models.CharField | 1 | {"max_length": 128, "type": "models.CharField", "verbose_name": "\u4ee3\u7801\u63d0\u4ea4\u54c8\u5e0c"} |
| source_location | models.CharField | 1 | {"max_length": 2048, "type": "models.CharField", "verbose_name": "\u4ee3\u7801\u4ed3\u5e93\u5730\u5740"} |
| source_version_name | models.CharField | 1 | {"max_length": 128, "null": true, "type": "models.CharField", "verbose_name": "\u4ee3\u7801\u5206\u652f\u540d/tag\u540d"} |
| source_version_type | models.CharField | 1 | {"max_length": 128, "null": true, "type": "models.CharField", "verbose_name": "\u4ee3\u7801\u7248\u672c\u7c7b\u578b(branch/tag)"} |
| status | models.CharField | 1 | {"default": "`constants.PluginReleaseStatus.INITIAL`", "max_length": 16, "type": "models.CharField"} |
| tag | models.CharField | 1 | {"db_index": true, "max_length": 16, "null": true, "type": "models.CharField", "verbose_name": "\u6807\u7b7e"} |
| type | models.CharField | 1 | {"choices": "`constants.PluginReleaseType.get_choices()`", "max_length": 16, "type": "models.CharField", "verbose_name": "\u7248\u672c\u7c7b\u578b(\u6b63\u5f0f/\u6d4b\u8bd5)"} |
| version | models.CharField | 1 | {"max_length": 255, "type": "models.CharField", "verbose_name": "\u7248\u672c\u53f7"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| plugin | models.ForeignKey | `PluginInstance` | all_versions | `models.CASCADE` |
| current_stage | models.OneToOneField | PluginReleaseStage | N/A | `models.SET_NULL` |


---


### PluginReleaseStage

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 插件发布阶段

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| api_detail | models.JSONField | 1 | {"help_text": "\u8be5\u5b57\u6bb5\u4ec5 invoke_method = api \u65f6\u53ef\u7528", "null": true, "type": "models.JSONField", "verbose_name": "API \u8be6\u60c5"} |
| fail_message | models.TextField | 1 | {"type": "models.TextField", "verbose_name": "\u9519\u8bef\u539f\u56e0"} |
| invoke_method | models.CharField | 1 | {"help_text": "\u5197\u4f59\u5b57\u6bb5, \u7528\u4e8e\u51cf\u5c11\u67e5\u8be2\u6b21\u6570", "max_length": 16, "type": "models.CharField", "verbose_name": "\u89e6\u53d1\u65b9\u5f0f"} |
| operator | models.CharField | 1 | {"max_length": 32, "null": true, "type": "models.CharField", "verbose_name": "\u64cd\u4f5c\u4eba"} |
| pipeline_detail | models.JSONField | 1 | {"default": null, "help_text": "\u8be5\u5b57\u6bb5\u4ec5 invoke_method = pipeline \u65f6\u53ef\u7528", "null": true, "type": "models.JSONField", "verbose_name": "\u6d41\u6c34\u7ebf\u6784\u5efa\u8be6\u60c5"} |
| stage_id | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u9636\u6bb5\u6807\u8bc6"} |
| stage_name | models.CharField | 1 | {"help_text": "\u5197\u4f59\u5b57\u6bb5, \u7528\u4e8e\u51cf\u5c11\u67e5\u8be2\u6b21\u6570", "max_length": 16, "type": "models.CharField", "verbose_name": "\u9636\u6bb5\u540d\u79f0"} |
| status | models.CharField | 1 | {"default": "`constants.PluginReleaseStatus.INITIAL`", "max_length": 16, "type": "models.CharField", "verbose_name": "\u53d1\u5e03\u72b6\u6001"} |
| status_polling_method | models.CharField | 1 | {"default": "`constants.StatusPollingMethod.API`", "help_text": "\u5197\u4f59\u5b57\u6bb5, \u7528\u4e8e\u51cf\u5c11\u67e5\u8be2\u6b21\u6570", "max_length": 16, "type": "models.CharField", "verbose_name": "\u9636\u6bb5\u7684\u72b6\u6001\u8f6e\u8be2\u65b9\u5f0f"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| release | models.ForeignKey | `PluginRelease` | all_stages | `models.CASCADE` |
| next_stage | models.OneToOneField | PluginReleaseStage | N/A | `models.SET_NULL` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['release', 'stage_id'] |

---


### PluginReleaseStrategy

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 插件版本的发布策略

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| bkci_project | models.JSONField | 1 | {"blank": true, "help_text": "\u683c\u5f0f\uff1a[\u00271111\u0027, \u0027222222\u0027]", "null": true, "type": "models.JSONField", "verbose_name": "\u84dd\u76fe\u9879\u76eeID"} |
| organization | models.JSONField | 1 | {"blank": true, "null": true, "type": "models.JSONField", "verbose_name": "\u7ec4\u7ec7\u67b6\u6784"} |
| strategy | models.CharField | 1 | {"choices": "`constants.ReleaseStrategy.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u53d1\u5e03\u7b56\u7565"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| release | models.ForeignKey | `PluginRelease` | release_strategies | `models.CASCADE` |


---


### PluginVisibleRange

**Module**: `apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 插件可见范围

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| bkci_project | models.JSONField | 1 | {"default": "`list`", "type": "models.JSONField", "verbose_name": "\u84dd\u76fe\u9879\u76eeID"} |
| is_in_approval | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u5728\u5ba1\u6279\u4e2d"} |
| organization | models.JSONField | 1 | {"blank": true, "null": true, "type": "models.JSONField", "verbose_name": "\u7ec4\u7ec7\u67b6\u6784"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| plugin | models.OneToOneField | `PluginInstance` | visible_range | `models.CASCADE` |


---


### AccountFeatureFlag

**Module**: `apiserver.paasng.paasng.infras.accounts.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| effect | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |



---


### AuthenticatedAppAsUser

**Module**: `apiserver.paasng.paasng.infras.accounts.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: Store relationships which treat an authenticated(by API Gateway) app as an regular user,

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| bk_app_code | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "unique": true} |
| is_active | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| user | models.ForeignKey | `User` | N/A | `models.CASCADE` |


---


### Oauth2TokenHolder

**Module**: `apiserver.paasng.paasng.infras.accounts.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: OAuth2 Token for sourcectl

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| expire_at | models.DateTimeField | 1 | {"blank": true, "null": true, "type": "models.DateTimeField"} |
| provider | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| token_type | models.CharField | 1 | {"max_length": 16, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| user | models.ForeignKey | `UserProfile` | token_holder | `models.CASCADE` |


---


### PrivateTokenHolder

**Module**: `apiserver.paasng.paasng.infras.accounts.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: Private Token for sourcectl

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| expire_at | models.DateTimeField | 1 | {"blank": true, "null": true, "type": "models.DateTimeField"} |
| provider | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| user | models.ForeignKey | `UserProfile` | private_token_holder | `models.CASCADE` |


---


### UserPrivateToken

**Module**: `apiserver.paasng.paasng.infras.accounts.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: Private token can be used to authenticate an user, these tokens usually have very long

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| expires_at | models.DateTimeField | 1 | {"blank": true, "null": true, "type": "models.DateTimeField"} |
| is_active | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| token | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "unique": true} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| user | models.ForeignKey | `User` | N/A | `models.CASCADE` |


---


### UserProfile

**Module**: `apiserver.paasng.paasng.infras.accounts.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: Profile field for user

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| feature_flags | models.TextField | 1 | {"blank": true, "null": true, "type": "models.TextField"} |
| role | models.IntegerField | 1 | {"default": "`SiteRole.USER.value`", "type": "models.IntegerField"} |



---


### BKMonitorSpace

**Module**: `apiserver.paasng.paasng.infras.bkmonitorv3.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| extra_info | models.JSONField | 1 | {"help_text": "\u84dd\u9cb8\u76d1\u63a7API-metadata_get_space_detail \u7684\u539f\u59cb\u8fd4\u56de\u503c", "type": "models.JSONField"} |
| id | models.IntegerField | 1 | {"type": "models.IntegerField", "verbose_name": "\u84dd\u9cb8\u76d1\u63a7\u7a7a\u95f4 id"} |
| space_id | models.CharField | 1 | {"help_text": "\u540c\u4e00\u7a7a\u95f4\u7c7b\u578b\u4e0b\u552f\u4e00", "max_length": 48, "type": "models.CharField", "verbose_name": "\u7a7a\u95f4id"} |
| space_name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "verbose_name": "\u7a7a\u95f4\u540d\u79f0"} |
| space_type_id | models.CharField | 1 | {"max_length": 48, "type": "models.CharField", "verbose_name": "\u7a7a\u95f4\u7c7b\u578bid"} |
| space_uid | models.CharField | 1 | {"help_text": "{space_type_id}__{space_id}", "max_length": 48, "type": "models.CharField", "verbose_name": "\u84dd\u9cb8\u76d1\u63a7\u7a7a\u95f4 uid"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.OneToOneField | `Application` | bk_monitor_space | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['space_type_id', 'space_id'] |

---


### ApplicationGradeManager

**Module**: `apiserver.paasng.paasng.infras.iam.members.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| app_code | models.CharField | 1 | {"help_text": "\u5e94\u7528\u4ee3\u53f7", "max_length": 20, "type": "models.CharField"} |
| grade_manager_id | models.IntegerField | 1 | {"help_text": "\u5206\u7ea7\u7ba1\u7406\u5458 ID", "type": "models.IntegerField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['app_code', 'grade_manager_id'] |

---


### ApplicationUserGroup

**Module**: `apiserver.paasng.paasng.infras.iam.members.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| app_code | models.CharField | 1 | {"help_text": "\u5e94\u7528\u4ee3\u53f7", "max_length": 20, "type": "models.CharField"} |
| role | models.IntegerField | 1 | {"default": "`ApplicationRole.DEVELOPER.value`", "type": "models.IntegerField"} |
| user_group_id | models.IntegerField | 1 | {"help_text": "\u6743\u9650\u4e2d\u5fc3\u7528\u6237\u7ec4 ID", "type": "models.IntegerField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['app_code', 'role'] |

---


### BkAppSecretInEnvVar

**Module**: `apiserver.paasng.paasng.infras.oauth2.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| bk_app_code | models.CharField | 1 | {"max_length": 20, "type": "models.CharField", "unique": true} |
| bk_app_secret_id | models.IntegerField | 1 | {"help_text": "\u4e0d\u5b58\u50a8\u5bc6\u94a5\u7684\u4fe1\u606f\uff0c\u4ec5\u5b58\u50a8\u5bc6\u94a5 ID", "type": "models.IntegerField", "verbose_name": "\u5e94\u7528\u5bc6\u94a5\u7684 ID"} |



---


### OAuth2Client

**Module**: `apiserver.paasng.paasng.infras.oauth2.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: OAuth2 体系中的基本单位：Client

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| client_id | models.CharField | 1 | {"max_length": 20, "type": "models.CharField", "unique": true, "verbose_name": "\u5e94\u7528\u7f16\u7801"} |



---


### AdminOperationRecord

**Module**: `apiserver.paasng.paasng.misc.audit.models`  
**Line**: 1  
**Base Classes**: apiserver.paasng.paasng.misc.audit.models.BaseOperation  
**Description**: 后台管理操作记录，用于记录平台管理员在 Admin 系统上的操作

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| access_type | models.IntegerField | 1 | {"choices": "`AccessType.get_choices()`", "default": "`AccessType.WEB`", "type": "models.IntegerField", "verbose_name": "\u8bbf\u95ee\u65b9\u5f0f"} |
| app_code | models.CharField | 1 | {"blank": true, "max_length": 32, "null": true, "type": "models.CharField", "verbose_name": "\u5e94\u7528ID, \u975e\u5fc5\u586b"} |
| attribute | models.CharField | 1 | {"blank": true, "help_text": "\u5982\u589e\u5f3a\u670d\u52a1\u7684\u5c5e\u6027\u53ef\u4ee5\u4e3a\uff1amysql\u3001bkrepo", "max_length": 32, "null": true, "type": "models.CharField", "verbose_name": "\u5bf9\u8c61\u5c5e\u6027"} |
| data_after | models.JSONField | 1 | {"blank": true, "null": true, "type": "models.JSONField", "verbose_name": "\u64cd\u4f5c\u540e\u7684\u6570\u636e"} |
| data_before | models.JSONField | 1 | {"blank": true, "null": true, "type": "models.JSONField", "verbose_name": "\u64cd\u4f5c\u524d\u7684\u6570\u636e"} |
| end_time | models.DateTimeField | 1 | {"help_text": "\u4ec5\u9700\u8981\u540e\u53f0\u6267\u884c\u7684\u7684\u64cd\u4f5c\u624d\u9700\u8981\u8bb0\u5f55\u7ed3\u675f\u65f6\u95f4", "null": true, "type": "models.DateTimeField"} |
| environment | models.CharField | 1 | {"blank": true, "choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": true, "type": "models.CharField", "verbose_name": "\u73af\u5883\uff0c\u975e\u5fc5\u586b"} |
| module_name | models.CharField | 1 | {"blank": true, "max_length": 32, "null": true, "type": "models.CharField", "verbose_name": "\u6a21\u5757\u540d\uff0c\u975e\u5fc5\u586b"} |
| operation | models.CharField | 1 | {"choices": "`OperationEnum.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u64cd\u4f5c\u7c7b\u578b"} |
| result_code | models.IntegerField | 1 | {"choices": "`ResultCode.get_choices()`", "default": "`ResultCode.SUCCESS`", "type": "models.IntegerField", "verbose_name": "\u64cd\u4f5c\u7ed3\u679c"} |
| start_time | models.DateTimeField | 1 | {"auto_now_add": true, "db_index": true, "type": "models.DateTimeField", "verbose_name": "\u5f00\u59cb\u65f6\u95f4"} |
| target | models.CharField | 1 | {"choices": "`OperationTarget.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u64cd\u4f5c\u5bf9\u8c61"} |



---


### AppLatestOperationRecord

**Module**: `apiserver.paasng.paasng.misc.audit.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: 应用最近操作的映射表，可方便快速查询应用的最近操作者，并按最近操作时间进行排序等操作

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| latest_operated_at | models.DateTimeField | 1 | {"db_index": true, "type": "models.DateTimeField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.OneToOneField | `Application` | latest_op_record | `models.CASCADE` |
| operation | models.OneToOneField | `AppOperationRecord` | N/A | `models.CASCADE` |


---


### AppOperationRecord

**Module**: `apiserver.paasng.paasng.misc.audit.models`  
**Line**: 1  
**Base Classes**: apiserver.paasng.paasng.misc.audit.models.BaseOperation  
**Description**: 应用操作记录，用于记录应用开发者的操作，需要同步记录应用的权限数据，并可以选择是否将数据上报到审计中心

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| access_type | models.IntegerField | 1 | {"choices": "`AccessType.get_choices()`", "default": "`AccessType.WEB`", "type": "models.IntegerField", "verbose_name": "\u8bbf\u95ee\u65b9\u5f0f"} |
| action_id | models.CharField | 1 | {"blank": true, "choices": "`AppAction.get_choices()`", "help_text": "action_id \u4e3a\u7a7a\u5219\u4e0d\u4f1a\u5c06\u6570\u636e\u4e0a\u62a5\u5230\u5ba1\u8ba1\u4e2d\u5fc3", "max_length": 32, "null": true, "type": "models.CharField"} |
| app_code | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u5e94\u7528ID, \u5fc5\u586b"} |
| attribute | models.CharField | 1 | {"blank": true, "help_text": "\u5982\u589e\u5f3a\u670d\u52a1\u7684\u5c5e\u6027\u53ef\u4ee5\u4e3a\uff1amysql\u3001bkrepo", "max_length": 32, "null": true, "type": "models.CharField", "verbose_name": "\u5bf9\u8c61\u5c5e\u6027"} |
| data_after | models.JSONField | 1 | {"blank": true, "null": true, "type": "models.JSONField", "verbose_name": "\u64cd\u4f5c\u540e\u7684\u6570\u636e"} |
| data_before | models.JSONField | 1 | {"blank": true, "null": true, "type": "models.JSONField", "verbose_name": "\u64cd\u4f5c\u524d\u7684\u6570\u636e"} |
| end_time | models.DateTimeField | 1 | {"help_text": "\u4ec5\u9700\u8981\u540e\u53f0\u6267\u884c\u7684\u7684\u64cd\u4f5c\u624d\u9700\u8981\u8bb0\u5f55\u7ed3\u675f\u65f6\u95f4", "null": true, "type": "models.DateTimeField"} |
| environment | models.CharField | 1 | {"blank": true, "choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": true, "type": "models.CharField", "verbose_name": "\u73af\u5883\uff0c\u975e\u5fc5\u586b"} |
| module_name | models.CharField | 1 | {"blank": true, "max_length": 32, "null": true, "type": "models.CharField", "verbose_name": "\u6a21\u5757\u540d\uff0c\u975e\u5fc5\u586b"} |
| operation | models.CharField | 1 | {"choices": "`OperationEnum.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u64cd\u4f5c\u7c7b\u578b"} |
| resource_type_id | models.CharField | 1 | {"choices": "`ResourceType.get_choices()`", "default": "`ResourceType.Application`", "help_text": "\u5f00\u53d1\u8005\u4e2d\u5fc3\u6ce8\u518c\u7684\u8d44\u6e90\u90fd\u4e3a\u84dd\u9cb8\u5e94\u7528", "max_length": 32, "type": "models.CharField"} |
| result_code | models.IntegerField | 1 | {"choices": "`ResultCode.get_choices()`", "default": "`ResultCode.SUCCESS`", "type": "models.IntegerField", "verbose_name": "\u64cd\u4f5c\u7ed3\u679c"} |
| start_time | models.DateTimeField | 1 | {"auto_now_add": true, "db_index": true, "type": "models.DateTimeField", "verbose_name": "\u5f00\u59cb\u65f6\u95f4"} |
| target | models.CharField | 1 | {"choices": "`OperationTarget.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u64cd\u4f5c\u5bf9\u8c61"} |



---


### BaseOperation

**Module**: `apiserver.paasng.paasng.misc.audit.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| access_type | models.IntegerField | 1 | {"choices": "`AccessType.get_choices()`", "default": "`AccessType.WEB`", "type": "models.IntegerField", "verbose_name": "\u8bbf\u95ee\u65b9\u5f0f"} |
| attribute | models.CharField | 1 | {"blank": true, "help_text": "\u5982\u589e\u5f3a\u670d\u52a1\u7684\u5c5e\u6027\u53ef\u4ee5\u4e3a\uff1amysql\u3001bkrepo", "max_length": 32, "null": true, "type": "models.CharField", "verbose_name": "\u5bf9\u8c61\u5c5e\u6027"} |
| data_after | models.JSONField | 1 | {"blank": true, "null": true, "type": "models.JSONField", "verbose_name": "\u64cd\u4f5c\u540e\u7684\u6570\u636e"} |
| data_before | models.JSONField | 1 | {"blank": true, "null": true, "type": "models.JSONField", "verbose_name": "\u64cd\u4f5c\u524d\u7684\u6570\u636e"} |
| end_time | models.DateTimeField | 1 | {"help_text": "\u4ec5\u9700\u8981\u540e\u53f0\u6267\u884c\u7684\u7684\u64cd\u4f5c\u624d\u9700\u8981\u8bb0\u5f55\u7ed3\u675f\u65f6\u95f4", "null": true, "type": "models.DateTimeField"} |
| environment | models.CharField | 1 | {"blank": true, "choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": true, "type": "models.CharField", "verbose_name": "\u73af\u5883\uff0c\u975e\u5fc5\u586b"} |
| module_name | models.CharField | 1 | {"blank": true, "max_length": 32, "null": true, "type": "models.CharField", "verbose_name": "\u6a21\u5757\u540d\uff0c\u975e\u5fc5\u586b"} |
| operation | models.CharField | 1 | {"choices": "`OperationEnum.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u64cd\u4f5c\u7c7b\u578b"} |
| result_code | models.IntegerField | 1 | {"choices": "`ResultCode.get_choices()`", "default": "`ResultCode.SUCCESS`", "type": "models.IntegerField", "verbose_name": "\u64cd\u4f5c\u7ed3\u679c"} |
| start_time | models.DateTimeField | 1 | {"auto_now_add": true, "db_index": true, "type": "models.DateTimeField", "verbose_name": "\u5f00\u59cb\u65f6\u95f4"} |
| target | models.CharField | 1 | {"choices": "`OperationTarget.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u64cd\u4f5c\u5bf9\u8c61"} |


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### AppAlertRule

**Module**: `apiserver.paasng.paasng.misc.monitoring.monitor.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 记录 app 初始的告警规则配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| alert_code | models.CharField | 1 | {"help_text": "alert rule code e.g. high_cpu_usage", "max_length": 64, "type": "models.CharField"} |
| display_name | models.CharField | 1 | {"max_length": 512, "type": "models.CharField"} |
| enabled | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| environment | models.CharField | 1 | {"max_length": 16, "type": "models.CharField", "verbose_name": "\u90e8\u7f72\u73af\u5883"} |
| receivers | models.JSONField | 1 | {"default": "`list`", "type": "models.JSONField"} |
| threshold_expr | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | applications.Application | alert_rules | `models.CASCADE` |
| module | models.ForeignKey | modules.Module | alert_rules | `models.CASCADE` |


---


### AppDashboard

**Module**: `apiserver.paasng.paasng.misc.monitoring.monitor.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 记录 APP 初始化的仪表盘信息

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| display_name | models.CharField | 1 | {"help_text": "\u4eea\u8868\u76d8\u5c55\u793a\u540d\u79f0\uff0c\u5982\uff1aPython \u5f00\u53d1\u6846\u67b6\u5185\u7f6e\u4eea\u8868\u76d8", "max_length": 512, "type": "models.CharField"} |
| language | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u4eea\u8868\u76d8\u6240\u5c5e\u8bed\u8a00"} |
| name | models.CharField | 1 | {"help_text": "\u4eea\u8868\u76d8\u540d\u79f0\uff0c\u5982\uff1abksaas/framework-python", "max_length": 64, "type": "models.CharField"} |
| template_version | models.CharField | 1 | {"help_text": "\u6a21\u677f\u7248\u672c\u66f4\u65b0\u65f6\uff0c\u53ef\u4ee5\u6839\u636e\u8be5\u5b57\u6bb5\u4f5c\u4e3a\u6279\u91cf\u5237\u65b0\u4eea\u8868\u76d8", "max_length": 32, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | applications.Application | dashboards | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['application', 'name'] |

---


### AppDashboardTemplate

**Module**: `apiserver.paasng.paasng.misc.monitoring.monitor.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 仪表盘模板，只需要记录名称和版本号，模板的内容在蓝鲸监控侧维护

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| display_name | models.CharField | 1 | {"help_text": "\u4eea\u8868\u76d8\u5c55\u793a\u540d\u79f0\uff0c\u5982\uff1aPython \u5f00\u53d1\u6846\u67b6\u5185\u7f6e\u4eea\u8868\u76d8", "max_length": 512, "type": "models.CharField"} |
| is_plugin_template | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| language | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u4eea\u8868\u76d8\u6240\u5c5e\u8bed\u8a00"} |
| name | models.CharField | 1 | {"help_text": "\u4e0e\u84dd\u9cb8\u76d1\u63a7\u7ea6\u5b9a\u7684\u4eea\u8868\u76d8\u540d\u79f0\uff0c\u5982\uff1abksaas/framework-python\uff0c\u9700\u8981\u63d0\u524d\u5c06\u4eea\u8868\u76d8\u7684 JSON \u6587\u4ef6\u5185\u7f6e\u5230\u76d1\u63a7\u7684\u4ee3\u7801\u76ee\u5f55\u4e2d", "max_length": 64, "type": "models.CharField", "unique": true} |
| version | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |



---


### ApplicationLatestOp

**Module**: `apiserver.paasng.paasng.misc.operations.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: A mapper table which saves application's latest operation

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| latest_operated_at | models.DateTimeField | 1 | {"db_index": true, "type": "models.DateTimeField"} |
| operation_type | models.SmallIntegerField | 1 | {"help_text": "\u64cd\u4f5c\u7c7b\u578b", "type": "models.SmallIntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.OneToOneField | `Application` | latest_op | `models.CASCADE` |
| operation | models.OneToOneField | `Operation` | N/A | `models.CASCADE` |


---


### Operation

**Module**: `apiserver.paasng.paasng.misc.operations.models`  
**Line**: 1  
**Base Classes**: models.Model  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| created | models.DateTimeField | 1 | {"auto_now_add": true, "db_index": true, "type": "models.DateTimeField"} |
| is_hidden | models.BooleanField | 1 | {"default": false, "help_text": "\u9690\u85cf\u8d77\u6765", "type": "models.BooleanField"} |
| module_name | models.CharField | 1 | {"max_length": 20, "null": true, "type": "models.CharField", "verbose_name": "\u5173\u8054 Module"} |
| region | models.CharField | 1 | {"help_text": "\u90e8\u7f72\u533a\u57df", "max_length": 32, "type": "models.CharField"} |
| source_object_id | models.CharField | 1 | {"blank": true, "default": "", "help_text": "\u4e8b\u4ef6\u6765\u6e90\u5bf9\u8c61ID\uff0c\u5177\u4f53\u6307\u5411\u9700\u8981\u6839\u636e\u64cd\u4f5c\u7c7b\u578b\u89e3\u6790", "max_length": 32, "null": true, "type": "models.CharField"} |
| type | models.SmallIntegerField | 1 | {"db_index": true, "help_text": "\u64cd\u4f5c\u7c7b\u578b", "type": "models.SmallIntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | `Application` | N/A | `models.CASCADE` |


---


### Application

**Module**: `apiserver.paasng.paasng.platform.applications.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: 蓝鲸应用

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| code | models.CharField | 1 | {"max_length": 20, "type": "models.CharField", "unique": true, "verbose_name": "\u5e94\u7528\u4ee3\u53f7"} |
| id | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "type": "models.UUIDField", "unique": true} |
| is_active | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u6d3b\u8dc3"} |
| is_ai_agent_app | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u4e3a AI Agent \u63d2\u4ef6\u5e94\u7528"} |
| is_deleted | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| is_plugin_app | models.BooleanField | 1 | {"default": false, "help_text": "\u84dd\u9cb8\u5e94\u7528\u63d2\u4ef6\uff1a\u4f9b\u6807\u51c6\u8fd0\u7ef4\u3001ITSM \u7b49 SaaS \u4f7f\u7528\uff0c\u6709\u7279\u6b8a\u903b\u8f91", "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u4e3a\u63d2\u4ef6\u5e94\u7528"} |
| is_scene_app | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u4e3a\u573a\u666f SaaS \u5e94\u7528"} |
| is_smart_app | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u4e3a S-Mart \u5e94\u7528"} |
| language | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u7f16\u7a0b\u8bed\u8a00"} |
| last_deployed_date | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField", "verbose_name": "\u6700\u8fd1\u90e8\u7f72\u65f6\u95f4"} |
| name | models.CharField | 1 | {"max_length": 20, "type": "models.CharField", "unique": true, "verbose_name": "\u5e94\u7528\u540d\u79f0"} |
| name_en | models.CharField | 1 | {"help_text": "\u76ee\u524d\u4ec5\u7528\u4e8e S-Mart \u5e94\u7528", "max_length": 20, "type": "models.CharField", "verbose_name": "\u5e94\u7528\u540d\u79f0(\u82f1\u6587)"} |
| type | models.CharField | 1 | {"db_index": true, "default": "`ApplicationType.DEFAULT.value`", "help_text": "\u4e0e\u5e94\u7528\u90e8\u7f72\u65b9\u5f0f\u76f8\u5173\u7684\u7c7b\u578b\u4fe1\u606f", "max_length": 16, "type": "models.CharField", "verbose_name": "\u5e94\u7528\u7c7b\u578b"} |



---


### ApplicationDeploymentModuleOrder

**Module**: `apiserver.paasng.paasng.platform.applications.models`  
**Line**: 1  
**Base Classes**: models.Model  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| order | models.IntegerField | 1 | {"type": "models.IntegerField", "verbose_name": "\u987a\u5e8f"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.OneToOneField | `Module` | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| verbose_name | 模块顺序 |

---


### ApplicationEnvironment

**Module**: `apiserver.paasng.paasng.platform.applications.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: 记录蓝鲸应用在不同部署环境下对应的 Engine App

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| environment | models.CharField | 1 | {"max_length": 16, "type": "models.CharField", "verbose_name": "\u90e8\u7f72\u73af\u5883"} |
| is_offlined | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u5df2\u7ecf\u4e0b\u7ebf\uff0c\u4ec5\u6210\u529f\u4e0b\u7ebf\u540e\u53d8\u4e3aFalse", "type": "models.BooleanField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | `Application` | envs | `models.CASCADE` |
| module | models.ForeignKey | modules.Module | envs | `models.CASCADE` |
| engine_app | models.OneToOneField | engine.EngineApp | env | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['module', 'environment'] |

---


### ApplicationFeatureFlag

**Module**: `apiserver.paasng.paasng.platform.applications.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| effect | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| name | models.CharField | 1 | {"max_length": 30, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | `Application` | feature_flag | `models.CASCADE` |


---


### ApplicationMembership

**Module**: `apiserver.paasng.paasng.platform.applications.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: [deprecated] 切换为权限中心用户组存储用户信息

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| role | models.IntegerField | 1 | {"default": "`ApplicationRole.DEVELOPER.value`", "type": "models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | `Application` | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['user', 'application', 'role'] |

---


### UserMarkedApplication

**Module**: `apiserver.paasng.paasng.platform.applications.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | `Application` | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['application', 'owner'] |

---


### BkAppManagedFields

**Module**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: This model stores the management status of the fields of a module's bkapp model, it's

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| fields | models.JSONField | 1 | {"default": [], "help_text": "\u6240\u7ba1\u7406\u7684\u5b57\u6bb5", "type": "models.JSONField"} |
| manager | models.CharField | 1 | {"help_text": "\u7ba1\u7406\u8005\u7c7b\u578b", "max_length": 20, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | modules.Module | managed_fields | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['module', 'manager'] |

---


### DomainResolution

**Module**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.AuditedModel  
**Description**: 域名解析配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | `Application` | N/A | `models.CASCADE` |


---


### ModuleDeployHook

**Module**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: 钩子命令

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| enabled | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u5df2\u5f00\u542f", "type": "models.BooleanField"} |
| proc_command | models.TextField | 1 | {"help_text": "\u8fdb\u7a0b\u542f\u52a8\u547d\u4ee4(\u5305\u542b\u5b8c\u6574\u547d\u4ee4\u548c\u53c2\u6570\u7684\u5b57\u7b26\u4e32), \u53ea\u80fd\u4e0e command/args \u4e8c\u9009\u4e00", "null": true, "type": "models.TextField"} |
| type | models.CharField | 1 | {"choices": "`DeployHookType.get_choices()`", "help_text": "\u94a9\u5b50\u7c7b\u578b", "max_length": 20, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | modules.Module | deploy_hooks | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['module', 'type'] |

---


### ModuleProcessSpec

**Module**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: 模块维度的进程定义, 表示模块当前所定义的进程, 该模型只通过 API 变更

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| autoscaling | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| name | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| plan_name | models.CharField | 1 | {"help_text": "\u4ec5\u5b58\u50a8\u65b9\u6848\u540d\u79f0", "max_length": 32, "type": "models.CharField"} |
| port | models.IntegerField | 1 | {"help_text": "[deprecated] \u5bb9\u5668\u7aef\u53e3", "null": true, "type": "models.IntegerField"} |
| proc_command | models.TextField | 1 | {"help_text": "\u8fdb\u7a0b\u542f\u52a8\u547d\u4ee4(\u5305\u542b\u5b8c\u6574\u547d\u4ee4\u548c\u53c2\u6570\u7684\u5b57\u7b26\u4e32), \u53ea\u80fd\u4e0e command/args \u4e8c\u9009\u4e00", "null": true, "type": "models.TextField"} |
| target_replicas | models.IntegerField | 1 | {"default": 1, "type": "models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | modules.Module | process_specs | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| ordering | ['id'] |
| unique_together | ['module', 'name'] |

---


### ObservabilityConfig

**Module**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.OneToOneField | modules.Module | observability | `models.CASCADE` |


---


### ProcessServicesFlag

**Module**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: ProcessServicesFlag 主要用途是标记是否隐式需要 process services 配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| implicit_needed | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app_environment | models.OneToOneField | `ApplicationEnvironment` | N/A | `models.CASCADE` |


---


### ProcessSpecEnvOverlay

**Module**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.TimestampedModel  
**Description**: 进程定义中允许按环境覆盖的配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| autoscaling | models.BooleanField | 1 | {"null": true, "type": "models.BooleanField"} |
| environment_name | models.CharField | 1 | {"choices": "`AppEnvName.get_choices()`", "max_length": 16, "null": false, "type": "models.CharField", "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| plan_name | models.CharField | 1 | {"blank": true, "help_text": "\u4ec5\u5b58\u50a8\u65b9\u6848\u540d\u79f0", "max_length": 32, "null": true, "type": "models.CharField"} |
| target_replicas | models.IntegerField | 1 | {"null": true, "type": "models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| proc_spec | models.ForeignKey | `ModuleProcessSpec` | env_overlays | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['proc_spec', 'environment_name'] |

---


### SvcDiscConfig

**Module**: `apiserver.paasng.paasng.platform.bkapp_model.models`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.AuditedModel  
**Description**: 服务发现配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | `Application` | N/A | `models.CASCADE` |


---


### ApplicationDescription

**Module**: `apiserver.paasng.paasng.platform.declarative.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: Application description object

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| code | models.CharField | 1 | {"db_index": true, "max_length": 20, "type": "models.CharField", "verbose_name": "ID of application"} |
| is_creation | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "whether current description creates an application"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | `Application` | declarative_config | `models.CASCADE` |


---


### DeploymentDescription

**Module**: `apiserver.paasng.paasng.platform.declarative.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: Config objects which describes deployment objects.

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| deployment | models.OneToOneField | `Deployment` | declarative_config | `models.CASCADE` |


---


### EngineApp

**Module**: `apiserver.paasng.paasng.platform.engine.models.base`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: 蓝鲸应用引擎应用

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| id | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "type": "models.UUIDField", "unique": true} |
| is_active | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u6d3b\u8dc3"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "unique": true} |
| region | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |



---


### OperationVersionBase

**Module**: `apiserver.paasng.paasng.platform.engine.models.base`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: 带操作版本信息的BaseModel

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| id | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "type": "models.UUIDField", "unique": true} |
| source_comment | models.TextField | 1 | {"type": "models.TextField"} |
| source_location | models.CharField | 1 | {"max_length": 2048, "type": "models.CharField"} |
| source_revision | models.CharField | 1 | {"max_length": 128, "null": true, "type": "models.CharField"} |
| source_type | models.CharField | 1 | {"max_length": 16, "null": true, "type": "models.CharField", "verbose_name": "\u6e90\u7801\u6258\u7ba1\u7c7b\u578b"} |
| source_version_name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| source_version_type | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### BuiltinConfigVar

**Module**: `apiserver.paasng.paasng.platform.engine.models.config_var`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: Default config vars for global, can be added or edited in admin42.

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| description | models.CharField | 1 | {"max_length": 512, "null": false, "type": "models.CharField", "verbose_name": "\u63cf\u8ff0"} |
| key | models.CharField | 1 | {"max_length": 128, "null": false, "type": "models.CharField", "unique": true, "verbose_name": "\u73af\u5883\u53d8\u91cf\u540d"} |
| value | models.TextField | 1 | {"max_length": 512, "null": false, "type": "models.TextField", "verbose_name": "\u73af\u5883\u53d8\u91cf\u503c"} |



---


### ConfigVar

**Module**: `apiserver.paasng.paasng.platform.engine.models.config_var`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: Config vars for application

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| description | models.CharField | 1 | {"max_length": 200, "null": true, "type": "models.CharField"} |
| is_builtin | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| is_global | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| key | models.CharField | 1 | {"max_length": 128, "null": false, "type": "models.CharField"} |
| value | models.TextField | 1 | {"null": false, "type": "models.TextField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | modules.Module | N/A | `models.CASCADE` |
| environment | models.ForeignKey | applications.ApplicationEnvironment | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['module', 'is_global', 'environment', 'key'] |

---


### MobileConfig

**Module**: `apiserver.paasng.paasng.platform.engine.models.mobile_config`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: Mobile config switcher for application

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| access_url | models.URLField | 1 | {"blank": true, "default": "", "null": true, "type": "models.URLField"} |
| is_enabled | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| lb_plan | models.CharField | 1 | {"choices": "`LBPlans.get_choices()`", "default": "`LBPlans.LBDefaultPlan.value`", "help_text": "which one-level load balancer plan the domain use", "max_length": 64, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| environment | models.OneToOneField | applications.ApplicationEnvironment | mobile_config | `models.CASCADE` |


---


### ModuleEnvironmentOperations

**Module**: `apiserver.paasng.paasng.platform.engine.models.operations`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| id | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "type": "models.UUIDField", "unique": true} |
| object_uid | models.UUIDField | 1 | {"default": "`uuid.uuid4`", "editable": false, "type": "models.UUIDField"} |
| operation_type | models.CharField | 1 | {"choices": "`OperationTypes.get_choices()`", "max_length": 32, "type": "models.CharField"} |
| status | models.CharField | 1 | {"choices": "`JobStatus.get_choices()`", "default": "`JobStatus.PENDING.value`", "max_length": 16, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | applications.Application | module_operations | `models.CASCADE` |
| app_environment | models.ForeignKey | applications.ApplicationEnvironment | module_operations | `models.CASCADE` |


---


### DeployPhase

**Module**: `apiserver.paasng.paasng.platform.engine.models.phases`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel, paasng.platform.engine.models.MarkStatusMixin  
**Description**: 部署阶段

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| complete_time | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField"} |
| start_time | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField"} |
| status | models.CharField | 1 | {"choices": "`JobStatus.get_choices()`", "max_length": 32, "null": true, "type": "models.CharField"} |
| type | models.CharField | 1 | {"choices": "`DeployPhaseTypes.get_choices()`", "max_length": 32, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| engine_app | models.ForeignKey | `EngineApp` | N/A | `models.CASCADE` |
| deployment | models.ForeignKey | `Deployment` | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| ordering | ['created'] |

---


### PresetEnvVariable

**Module**: `apiserver.paasng.paasng.platform.engine.models.preset_envvars`  
**Line**: 1  
**Base Classes**: paas_wl.utils.models.AuditedModel  
**Description**: 应用描述文件中预定义的环境变量

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| environment_name | models.CharField | 1 | {"choices": "`ConfigVarEnvName.get_choices()`", "max_length": 16, "type": "models.CharField", "verbose_name": "`_(\u0027\u73af\u5883\u540d\u79f0\u0027)`"} |
| key | models.CharField | 1 | {"max_length": 128, "null": false, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | `Module` | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['module', 'environment_name', 'key'] |

---


### DeployStep

**Module**: `apiserver.paasng.paasng.platform.engine.models.steps`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel, paasng.platform.engine.models.base.MarkStatusMixin  
**Description**: 部署步骤

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| complete_time | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField"} |
| name | models.CharField | 1 | {"db_index": true, "max_length": 32, "type": "models.CharField"} |
| skipped | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| start_time | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField"} |
| status | models.CharField | 1 | {"choices": "`JobStatus.get_choices()`", "max_length": 32, "null": true, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| phase | models.ForeignKey | `DeployPhase` | steps | `models.CASCADE` |
| meta | models.ForeignKey | `DeployStepMeta` | instances | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| ordering | ['created'] |

---


### DeployStepMeta

**Module**: `apiserver.paasng.paasng.platform.engine.models.steps`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 部署步骤元信息

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| name | models.CharField | 1 | {"db_index": true, "max_length": 32, "type": "models.CharField"} |
| phase | models.CharField | 1 | {"choices": "`DeployPhaseTypes.get_choices()`", "max_length": 16, "type": "models.CharField", "verbose_name": "`_(\u0027\u5173\u8054\u9636\u6bb5\u0027)`"} |


#### Meta Options

| Option | Value |
|--------|-------|
| ordering | ['id'] |

---


### StepMetaSet

**Module**: `apiserver.paasng.paasng.platform.engine.models.steps`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 部署步骤元信息集

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| is_default | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| name | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| metas | models.ManyToManyField | `DeployStepMeta` | N/A | N/A |

#### Meta Options

| Option | Value |
|--------|-------|
| ordering | ['id'] |

---


### EnvRoleProtection

**Module**: `apiserver.paasng.paasng.platform.environments.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: 模块环境角色保护

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| allowed_role | models.IntegerField | 1 | {"choices": "`ApplicationRole.get_django_choices()`", "type": "models.IntegerField"} |
| operation | models.CharField | 1 | {"choices": "`EnvRoleOperation.get_choices()`", "max_length": 64, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module_env | models.ForeignKey | `ModuleEnvironment` | role_protections | `models.CASCADE` |


---


### AppOperationEmailNotificationTask

**Module**: `apiserver.paasng.paasng.platform.evaluation.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: 应用运营报告邮件通知任务

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| end_at | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField", "verbose_name": "\u4efb\u52a1\u7ed3\u675f\u65f6\u95f4"} |
| failed_count | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField", "verbose_name": "\u91c7\u96c6\u5931\u8d25\u6570"} |
| failed_usernames | models.JSONField | 1 | {"default": "`list`", "type": "models.JSONField", "verbose_name": "\u901a\u77e5\u5931\u8d25\u7684\u5e94\u7528\u6570\u91cf"} |
| notification_type | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "verbose_name": "\u901a\u77e5\u7c7b\u578b"} |
| start_at | models.DateTimeField | 1 | {"auto_now_add": true, "type": "models.DateTimeField", "verbose_name": "\u4efb\u52a1\u5f00\u59cb\u65f6\u95f4"} |
| status | models.CharField | 1 | {"choices": "`BatchTaskStatus.get_choices()`", "default": "`BatchTaskStatus.RUNNING`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u4efb\u52a1\u72b6\u6001"} |
| succeed_count | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField", "verbose_name": "\u91c7\u96c6\u6210\u529f\u6570"} |
| total_count | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField", "verbose_name": "\u5e94\u7528\u603b\u6570"} |



---


### AppOperationReport

**Module**: `apiserver.paasng.paasng.platform.evaluation.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: 应用运营报告（含资源使用，用户活跃，运维操作等）

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| administrators | models.JSONField | 1 | {"default": "`list`", "type": "models.JSONField", "verbose_name": "\u5e94\u7528\u7ba1\u7406\u5458"} |
| collected_at | models.DateTimeField | 1 | {"type": "models.DateTimeField", "verbose_name": "\u91c7\u96c6\u65f6\u95f4"} |
| cpu_limits | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField", "verbose_name": "CPU \u9650\u5236"} |
| cpu_requests | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField", "verbose_name": "CPU \u8bf7\u6c42"} |
| cpu_usage_avg | models.FloatField | 1 | {"default": 0, "type": "models.FloatField", "verbose_name": "CPU \u5e73\u5747\u4f7f\u7528\u7387"} |
| deploy_summary | models.JSONField | 1 | {"default": "`dict`", "type": "models.JSONField", "verbose_name": "\u90e8\u7f72\u8be6\u60c5\u6c47\u603b"} |
| developers | models.JSONField | 1 | {"default": "`list`", "type": "models.JSONField", "verbose_name": "\u5e94\u7528\u5f00\u53d1\u8005"} |
| evaluate_result | models.JSONField | 1 | {"default": "`dict`", "type": "models.JSONField", "verbose_name": "\u8bc4\u4f30\u7ed3\u679c"} |
| issue_type | models.CharField | 1 | {"default": "`OperationIssueType.NONE`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u95ee\u9898\u7c7b\u578b"} |
| latest_deployed_at | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField", "verbose_name": "\u6700\u65b0\u90e8\u7f72\u65f6\u95f4"} |
| latest_deployer | models.CharField | 1 | {"max_length": 128, "null": true, "type": "models.CharField", "verbose_name": "\u6700\u65b0\u90e8\u7f72\u4eba"} |
| latest_operated_at | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField", "verbose_name": "\u6700\u65b0\u64cd\u4f5c\u65f6\u95f4"} |
| latest_operation | models.CharField | 1 | {"max_length": 128, "null": true, "type": "models.CharField", "verbose_name": "\u6700\u65b0\u64cd\u4f5c\u5185\u5bb9"} |
| latest_operator | models.CharField | 1 | {"max_length": 128, "null": true, "type": "models.CharField", "verbose_name": "\u6700\u65b0\u64cd\u4f5c\u4eba"} |
| mem_limits | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField", "verbose_name": "\u5185\u5b58\u9650\u5236"} |
| mem_requests | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField", "verbose_name": "\u5185\u5b58\u8bf7\u6c42"} |
| mem_usage_avg | models.FloatField | 1 | {"default": 0, "type": "models.FloatField", "verbose_name": "\u5185\u5b58\u5e73\u5747\u4f7f\u7528\u7387"} |
| pv | models.BigIntegerField | 1 | {"default": 0, "type": "models.BigIntegerField", "verbose_name": "\u8fd1 30 \u5929\u9875\u9762\u8bbf\u95ee\u91cf"} |
| res_summary | models.JSONField | 1 | {"default": "`dict`", "type": "models.JSONField", "verbose_name": "\u8d44\u6e90\u4f7f\u7528\u8be6\u60c5\u6c47\u603b"} |
| uv | models.BigIntegerField | 1 | {"default": 0, "type": "models.BigIntegerField", "verbose_name": "\u8fd1 30 \u5929\u8bbf\u95ee\u7528\u6237\u6570"} |
| visit_summary | models.JSONField | 1 | {"default": "`dict`", "type": "models.JSONField", "verbose_name": "\u7528\u6237\u8bbf\u95ee\u8be6\u60c5\u6c47\u603b"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.OneToOneField | `Application` | N/A | `models.CASCADE` |


---


### AppOperationReportCollectionTask

**Module**: `apiserver.paasng.paasng.platform.evaluation.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: 应用运营报告采集任务

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| end_at | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField", "verbose_name": "\u4efb\u52a1\u7ed3\u675f\u65f6\u95f4"} |
| failed_app_codes | models.JSONField | 1 | {"default": "`list`", "type": "models.JSONField", "verbose_name": "\u91c7\u96c6\u5931\u8d25\u5e94\u7528 Code \u5217\u8868"} |
| failed_count | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField", "verbose_name": "\u91c7\u96c6\u5931\u8d25\u6570"} |
| start_at | models.DateTimeField | 1 | {"auto_now_add": true, "type": "models.DateTimeField", "verbose_name": "\u4efb\u52a1\u5f00\u59cb\u65f6\u95f4"} |
| status | models.CharField | 1 | {"choices": "`BatchTaskStatus.get_choices()`", "default": "`BatchTaskStatus.RUNNING`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u4efb\u52a1\u72b6\u6001"} |
| succeed_count | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField", "verbose_name": "\u91c7\u96c6\u6210\u529f\u6570"} |
| total_count | models.IntegerField | 1 | {"default": 0, "type": "models.IntegerField", "verbose_name": "\u5e94\u7528\u603b\u6570"} |



---


### IdleAppNotificationMuteRule

**Module**: `apiserver.paasng.paasng.platform.evaluation.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 闲置应用通知屏蔽规则

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| app_code | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| environment | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| expired_at | models.DateTimeField | 1 | {"type": "models.DateTimeField"} |
| module_name | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['user', 'app_code', 'module_name', 'environment'] |

---


### CNativeMigrationProcess

**Module**: `apiserver.paasng.paasng.platform.mgrlegacy.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| confirm_at | models.DateTimeField | 1 | {"help_text": "\u7528\u6237\u786e\u8ba4\u7684\u65f6\u95f4", "null": true, "type": "models.DateTimeField"} |
| created_at | models.DateTimeField | 1 | {"auto_now_add": true, "help_text": "\u64cd\u4f5c\u8bb0\u5f55\u7684\u521b\u5efa\u65f6\u95f4", "type": "models.DateTimeField"} |
| status | models.CharField | 1 | {"choices": "`CNativeMigrationStatus.get_choices()`", "default": "`CNativeMigrationStatus.DEFAULT.value`", "max_length": 20, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | `Application` | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| get_latest_by | created_at |
| ordering | ['created_at'] |

---


### MigrationProcess

**Module**: `apiserver.paasng.paasng.platform.mgrlegacy.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: An migration process

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| confirmed_date | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField"} |
| failed_date | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField"} |
| legacy_app_has_all_deployed | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| legacy_app_id | models.IntegerField | 1 | {"type": "models.IntegerField"} |
| legacy_app_is_already_online | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| legacy_app_logo | models.CharField | 1 | {"default": null, "max_length": 500, "null": true, "type": "models.CharField"} |
| legacy_app_state | models.IntegerField | 1 | {"default": 4, "type": "models.IntegerField"} |
| migrated_date | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField"} |
| rollbacked_date | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField"} |
| status | models.IntegerField | 1 | {"choices": "`MigrationStatus.get_choices()`", "default": "`MigrationStatus.DEFAULT.value`", "type": "models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app | models.ForeignKey | `Application` | N/A | `models.CASCADE` |


---


### WlAppBackupRel

**Module**: `apiserver.paasng.paasng.platform.mgrlegacy.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: WlApp 的备份关系表

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| backup_id | models.UUIDField | 1 | {"type": "models.UUIDField", "verbose_name": "\u5bf9\u5e94\u5907\u4efd\u7684 WlApp uuid"} |
| original_id | models.UUIDField | 1 | {"type": "models.UUIDField", "verbose_name": "\u539f WlApp uuid"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| app_environment | models.OneToOneField | `ApplicationEnvironment` | N/A | `models.CASCADE` |


---


### BuildConfig

**Module**: `apiserver.paasng.paasng.platform.modules.models.build_cfg`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| build_method | models.CharField | 1 | {"default": "`RuntimeType.BUILDPACK`", "max_length": 32, "type": "models.CharField", "verbose_name": "`_(\u0027\u6784\u5efa\u65b9\u5f0f\u0027)`"} |
| dockerfile_path | models.CharField | 1 | {"help_text": "`_(\u0027Dockerfile\u6587\u4ef6\u8def\u5f84, \u5fc5\u987b\u4fdd\u8bc1 Dockerfile \u5728\u6784\u5efa\u76ee\u5f55\u4e0b, \u586b\u5199\u65f6\u65e0\u9700\u5305\u542b\u6784\u5efa\u76ee\u5f55\u0027)`", "max_length": 512, "null": true, "type": "models.CharField"} |
| image_credential_name | models.CharField | 1 | {"max_length": 32, "null": true, "type": "models.CharField", "verbose_name": "`_(\u0027\u955c\u50cf\u51ed\u8bc1\u540d\u79f0\u0027)`"} |
| image_repository | models.TextField | 1 | {"null": true, "type": "models.TextField", "verbose_name": "`_(\u0027\u955c\u50cf\u4ed3\u5e93\u0027)`"} |
| use_bk_ci_pipeline | models.BooleanField | 1 | {"default": false, "help_text": "\u662f\u5426\u4f7f\u7528\u84dd\u76fe\u6d41\u6c34\u7ebf\u6784\u5efa", "type": "models.BooleanField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.OneToOneField | modules.Module | build_config | `models.CASCADE` |
| buildpacks | models.ManyToManyField | modules.AppBuildPack | related_build_configs | N/A |
| buildpack_builder | models.ForeignKey | modules.AppSlugBuilder | N/A | `models.SET_NULL` |
| buildpack_runner | models.ForeignKey | modules.AppSlugRunner | N/A | `models.SET_NULL` |


---


### DeployConfig

**Module**: `apiserver.paasng.paasng.platform.modules.models.deploy_config`  
**Line**: 1  
**Base Classes**: paasng.utils.models.UuidAuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.OneToOneField | modules.Module | deploy_config | `models.CASCADE` |


---


### Module

**Module**: `apiserver.paasng.paasng.platform.modules.models.module`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: Module for Application

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| exposed_url_type | models.IntegerField | 1 | {"null": true, "type": "models.IntegerField", "verbose_name": "\u8bbf\u95ee URL \u7248\u672c"} |
| id | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "type": "models.UUIDField", "unique": true} |
| is_default | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u4e3a\u9ed8\u8ba4\u6a21\u5757"} |
| language | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u7f16\u7a0b\u8bed\u8a00"} |
| last_deployed_date | models.DateTimeField | 1 | {"null": true, "type": "models.DateTimeField", "verbose_name": "\u6700\u8fd1\u90e8\u7f72\u65f6\u95f4"} |
| name | models.CharField | 1 | {"max_length": 20, "type": "models.CharField", "verbose_name": "\u6a21\u5757\u540d\u79f0"} |
| source_init_template | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u521d\u59cb\u5316\u6a21\u677f\u7c7b\u578b"} |
| source_origin | models.SmallIntegerField | 1 | {"null": true, "type": "models.SmallIntegerField", "verbose_name": "\u6e90\u7801\u6765\u6e90"} |
| source_repo_id | models.IntegerField | 1 | {"null": true, "type": "models.IntegerField", "verbose_name": "\u6e90\u7801 ID"} |
| source_type | models.CharField | 1 | {"max_length": 16, "null": true, "type": "models.CharField", "verbose_name": "\u6e90\u7801\u6258\u7ba1\u7c7b\u578b"} |
| user_preferred_root_domain | models.CharField | 1 | {"max_length": 255, "null": true, "type": "models.CharField", "verbose_name": "\u7528\u6237\u504f\u597d\u7684\u6839\u57df\u540d"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| application | models.ForeignKey | applications.Application | modules | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['application', 'name'] |

---


### AppBuildPack

**Module**: `apiserver.paasng.paasng.platform.modules.models.runtime`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: buildpack 配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| address | models.CharField | 1 | {"max_length": 2048, "type": "models.CharField", "verbose_name": "\u5730\u5740"} |
| is_hidden | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u9690\u85cf"} |
| language | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u7f16\u7a0b\u8bed\u8a00"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "verbose_name": "\u540d\u79f0"} |
| type | models.CharField | 1 | {"choices": "`BuildPackType.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u5f15\u7528\u7c7b\u578b"} |
| version | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u7248\u672c"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| modules | models.ManyToManyField | modules.Module | buildpacks | N/A |


---


### AppImage

**Module**: `apiserver.paasng.paasng.platform.modules.models.runtime`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| image | models.CharField | 1 | {"max_length": 256, "type": "models.CharField", "verbose_name": "\u955c\u50cf"} |
| is_default | models.BooleanField | 1 | {"default": false, "null": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u4e3a\u9ed8\u8ba4\u8fd0\u884c\u65f6"} |
| is_hidden | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u9690\u85cf"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "unique": true, "verbose_name": "\u540d\u79f0"} |
| tag | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u6807\u7b7e"} |
| type | models.CharField | 1 | {"choices": "`AppImageType.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u955c\u50cf\u7c7b\u578b"} |


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### AppSlugBuilder

**Module**: `apiserver.paasng.paasng.platform.modules.models.runtime`  
**Line**: 1  
**Base Classes**: apiserver.paasng.paasng.platform.modules.models.runtime.AppImage  
**Description**: 应用构建环境

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| image | models.CharField | 1 | {"max_length": 256, "type": "models.CharField", "verbose_name": "\u955c\u50cf"} |
| is_default | models.BooleanField | 1 | {"default": false, "null": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u4e3a\u9ed8\u8ba4\u8fd0\u884c\u65f6"} |
| is_hidden | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u9690\u85cf"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "unique": true, "verbose_name": "\u540d\u79f0"} |
| tag | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u6807\u7b7e"} |
| type | models.CharField | 1 | {"choices": "`AppImageType.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u955c\u50cf\u7c7b\u578b"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| buildpacks | models.ManyToManyField | `AppBuildPack` | slugbuilders | N/A |
| modules | models.ManyToManyField | modules.Module | slugbuilders | N/A |
| step_meta_set | models.ForeignKey | engine.StepMetaSet | slugbuilders | `models.SET_NULL` |


---


### AppSlugRunner

**Module**: `apiserver.paasng.paasng.platform.modules.models.runtime`  
**Line**: 1  
**Base Classes**: apiserver.paasng.paasng.platform.modules.models.runtime.AppImage  
**Description**: 应用运行环境

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| image | models.CharField | 1 | {"max_length": 256, "type": "models.CharField", "verbose_name": "\u955c\u50cf"} |
| is_default | models.BooleanField | 1 | {"default": false, "null": true, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u4e3a\u9ed8\u8ba4\u8fd0\u884c\u65f6"} |
| is_hidden | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u9690\u85cf"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "unique": true, "verbose_name": "\u540d\u79f0"} |
| tag | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u6807\u7b7e"} |
| type | models.CharField | 1 | {"choices": "`AppImageType.get_choices()`", "max_length": 32, "type": "models.CharField", "verbose_name": "\u955c\u50cf\u7c7b\u578b"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| modules | models.ManyToManyField | modules.Module | slugrunners | N/A |


---


### DockerRepository

**Module**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel, apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin  
**Description**: 容器镜像仓库

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| repo_url | models.CharField | 1 | {"help_text": "\u5f62\u5982 registry.hub.docker.com/library/python, \u4e5f\u53ef\u7701\u7565 registry \u5730\u5740", "max_length": 2048, "type": "models.CharField", "verbose_name": "\u9879\u76ee\u5730\u5740"} |
| server_name | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "DockerRegistry \u670d\u52a1\u540d\u79f0"} |
| source_dir | models.CharField | 1 | {"max_length": 2048, "null": true, "type": "models.CharField", "verbose_name": "\u6e90\u7801\u76ee\u5f55"} |



---


### GitRepository

**Module**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel, apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin  
**Description**: 基于 Git 的软件存储库

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| repo_url | models.CharField | 1 | {"max_length": 2048, "type": "models.CharField", "verbose_name": "\u9879\u76ee\u5730\u5740"} |
| server_name | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "GIT \u670d\u52a1\u540d\u79f0"} |
| source_dir | models.CharField | 1 | {"max_length": 2048, "null": true, "type": "models.CharField", "verbose_name": "\u6e90\u7801\u76ee\u5f55"} |



---


### RepoBasicAuthHolder

**Module**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: Repo 鉴权

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| repo_id | models.IntegerField | 1 | {"type": "models.IntegerField", "verbose_name": "\u5173\u8054\u4ed3\u5e93"} |
| repo_type | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "\u4ed3\u5e93\u7c7b\u578b"} |
| username | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "verbose_name": "\u4ed3\u5e93\u7528\u6237\u540d"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | modules.Module | N/A | `models.CASCADE` |


---


### SourcePackage

**Module**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel  
**Description**: 源码包存储信息

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| is_deleted | models.BooleanField | 1 | {"default": false, "help_text": "\u5982\u679c SourcePackage \u6307\u5411\u7684\u6e90\u7801\u5305\u5df2\u88ab\u6e05\u7406, \u5219\u8bbe\u7f6e\u8be5\u503c\u4e3a True", "type": "models.BooleanField", "verbose_name": "\u6e90\u7801\u5305\u662f\u5426\u5df2\u88ab\u6e05\u7406"} |
| package_name | models.CharField | 1 | {"max_length": 128, "type": "models.CharField", "verbose_name": "\u6e90\u7801\u5305\u539f\u59cb\u6587\u4ef6\u540d"} |
| package_size | models.BigIntegerField | 1 | {"type": "models.BigIntegerField", "verbose_name": "\u6e90\u7801\u5305\u5927\u5c0f, bytes"} |
| relative_path | models.CharField | 1 | {"help_text": "\u5982\u679c\u538b\u7f29\u65f6\u5c06\u76ee\u5f55\u4e5f\u6253\u5305\u8fdb\u6765, \u5165\u76ee\u5f55\u540d\u662f foo, \u90a3\u4e48 relative_path = \u0027foo/\u0027", "max_length": 255, "type": "models.CharField", "verbose_name": "\u6e90\u7801\u5165\u53e3\u7684\u76f8\u5bf9\u8def\u5f84"} |
| sha256_signature | models.CharField | 1 | {"max_length": 64, "null": true, "type": "models.CharField", "verbose_name": "sha256\u6570\u5b57\u7b7e\u540d"} |
| storage_engine | models.CharField | 1 | {"help_text": "\u6e90\u7801\u5305\u771f\u5b9e\u5b58\u653e\u7684\u5b58\u50a8\u670d\u52a1\u7c7b\u578b", "max_length": 64, "type": "models.CharField", "verbose_name": "\u5b58\u50a8\u5f15\u64ce"} |
| storage_path | models.CharField | 1 | {"help_text": "[deprecated] \u6e90\u7801\u5305\u5728\u5b58\u50a8\u670d\u52a1\u4e2d\u5b58\u653e\u7684\u4f4d\u7f6e", "max_length": 1024, "type": "models.CharField", "verbose_name": "\u5b58\u50a8\u8def\u5f84"} |
| storage_url | models.CharField | 1 | {"help_text": "\u53ef\u83b7\u53d6\u5230\u6e90\u7801\u5305\u7684 URL \u5730\u5740", "max_length": 1024, "type": "models.CharField", "verbose_name": "\u5b58\u50a8\u5730\u5740"} |
| version | models.CharField | 1 | {"max_length": 128, "type": "models.CharField", "verbose_name": "\u7248\u672c\u53f7"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| module | models.ForeignKey | modules.Module | packages | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['module', 'version'] |

---


### SourceTypeSpecConfig

**Module**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: SourceTypeSpec 数据存储

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| authorization_base_url | models.CharField | 1 | {"blank": true, "default": "", "max_length": 256, "type": "models.CharField", "verbose_name": "OAuth \u6388\u6743\u94fe\u63a5"} |
| client_id | models.CharField | 1 | {"blank": true, "default": "", "max_length": 256, "type": "models.CharField", "verbose_name": "OAuth App Client ID"} |
| enabled | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "\u662f\u5426\u542f\u7528"} |
| name | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "unique": true, "verbose_name": "`_(\u0027\u670d\u52a1\u540d\u79f0\u0027)`"} |
| redirect_uri | models.CharField | 1 | {"blank": true, "default": "", "max_length": 256, "type": "models.CharField", "verbose_name": "\u91cd\u5b9a\u5411\uff08\u56de\u8c03\uff09\u5730\u5740"} |
| server_config | models.JSONField | 1 | {"blank": true, "default": "`dict`", "type": "models.JSONField", "verbose_name": "\u670d\u52a1\u914d\u7f6e"} |
| spec_cls | models.CharField | 1 | {"max_length": 128, "type": "models.CharField", "verbose_name": "\u914d\u7f6e\u7c7b\u8def\u5f84"} |
| token_base_url | models.CharField | 1 | {"blank": true, "default": "", "max_length": 256, "type": "models.CharField", "verbose_name": "\u83b7\u53d6 Token \u94fe\u63a5"} |



---


### SvnAccount

**Module**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.TimestampedModel  
**Description**: svn account for developer

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| account | models.CharField | 1 | {"help_text": "\u76ee\u524d\u4ec5\u652f\u6301\u56fa\u5b9a\u683c\u5f0f", "max_length": 64, "type": "models.CharField", "unique": true} |
| synced_from_paas20 | models.BooleanField | 1 | {"default": false, "help_text": "\u8d26\u6237\u4fe1\u606f\u662f\u5426\u4ece PaaS 2.0 \u540c\u6b65\u8fc7\u6765", "type": "models.BooleanField"} |



---


### SvnRepository

**Module**: `apiserver.paasng.paasng.platform.sourcectl.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.OwnerTimestampedModel, apiserver.paasng.paasng.platform.sourcectl.models.RepositoryMixin  
**Description**: 基于 Svn 的软件存储库

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| repo_url | models.CharField | 1 | {"max_length": 2048, "type": "models.CharField", "verbose_name": "\u9879\u76ee\u5730\u5740"} |
| server_name | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "SVN \u670d\u52a1\u540d\u79f0"} |
| source_dir | models.CharField | 1 | {"max_length": 2048, "null": true, "type": "models.CharField", "verbose_name": "\u6e90\u7801\u76ee\u5f55"} |



---


### Template

**Module**: `apiserver.paasng.paasng.platform.templates.models`  
**Line**: 1  
**Base Classes**: paasng.utils.models.AuditedModel  
**Description**: 开发模板配置

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| blob_url | models.JSONField | 1 | {"type": "models.JSONField", "verbose_name": "`_(\u0027\u4e0d\u540c\u7248\u672c\u4e8c\u8fdb\u5236\u5305\u5b58\u50a8\u8def\u5f84\u0027)`"} |
| enabled_regions | models.JSONField | 1 | {"blank": true, "default": "`list`", "type": "models.JSONField", "verbose_name": "`_(\u0027\u5141\u8bb8\u88ab\u4f7f\u7528\u7684\u7248\u672c\u0027)`"} |
| language | models.CharField | 1 | {"max_length": 32, "type": "models.CharField", "verbose_name": "`_(\u0027\u5f00\u53d1\u8bed\u8a00\u0027)`"} |
| market_ready | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField", "verbose_name": "`_(\u0027\u80fd\u5426\u53d1\u5e03\u5230\u5e94\u7528\u96c6\u5e02\u0027)`"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "unique": true, "verbose_name": "`_(\u0027\u6a21\u677f\u540d\u79f0\u0027)`"} |
| preset_services_config | models.JSONField | 1 | {"blank": true, "default": "`dict`", "type": "models.JSONField", "verbose_name": "`_(\u0027\u9884\u8bbe\u589e\u5f3a\u670d\u52a1\u914d\u7f6e\u0027)`"} |
| processes | models.JSONField | 1 | {"blank": true, "default": "`dict`", "type": "models.JSONField", "verbose_name": "`_(\u0027\u8fdb\u7a0b\u914d\u7f6e\u0027)`"} |
| repo_url | models.CharField | 1 | {"blank": true, "default": "", "max_length": 256, "type": "models.CharField", "verbose_name": "`_(\u0027\u4ee3\u7801\u4ed3\u5e93\u4fe1\u606f\u0027)`"} |
| required_buildpacks | models.JSONField | 1 | {"blank": true, "default": "`list`", "type": "models.JSONField", "verbose_name": "`_(\u0027\u5fc5\u987b\u7684\u6784\u5efa\u5de5\u5177\u0027)`"} |
| runtime_type | models.CharField | 1 | {"default": "`RuntimeType.BUILDPACK`", "max_length": 32, "type": "models.CharField", "verbose_name": "`_(\u0027\u8fd0\u884c\u65f6\u7c7b\u578b\u0027)`"} |
| tags | models.JSONField | 1 | {"blank": true, "default": "`list`", "type": "models.JSONField", "verbose_name": "`_(\u0027\u6807\u7b7e\u0027)`"} |
| type | models.CharField | 1 | {"choices": "`TemplateType.get_django_choices()`", "max_length": 16, "type": "models.CharField", "verbose_name": "`_(\u0027\u6a21\u677f\u7c7b\u578b\u0027)`"} |


#### Meta Options

| Option | Value |
|--------|-------|
| ordering | ['created'] |

---


### AuditedModel

**Module**: `apiserver.paasng.paasng.utils.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: Audited model with 'created' and 'updated' fields.

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| created | models.DateTimeField | 1 | {"auto_now_add": true, "type": "models.DateTimeField"} |
| updated | models.DateTimeField | 1 | {"auto_now": true, "type": "models.DateTimeField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### OwnerTimestampedModel

**Module**: `apiserver.paasng.paasng.utils.models`  
**Line**: 1  
**Base Classes**: apiserver.paasng.paasng.utils.models.TimestampedModel  
**Description**: Model with 'created' and 'updated' fields.

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### TimestampedModel

**Module**: `apiserver.paasng.paasng.utils.models`  
**Line**: 1  
**Base Classes**: models.Model  
**Description**: Model with 'created' and 'updated' fields.

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| created | models.DateTimeField | 1 | {"auto_now_add": true, "type": "models.DateTimeField"} |
| region | models.CharField | 1 | {"help_text": "\u90e8\u7f72\u533a\u57df", "max_length": 32, "type": "models.CharField"} |
| updated | models.DateTimeField | 1 | {"auto_now": true, "type": "models.DateTimeField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### UuidAuditedModel

**Module**: `apiserver.paasng.paasng.utils.models`  
**Line**: 1  
**Base Classes**: apiserver.paasng.paasng.utils.models.AuditedModel  
**Description**: Add a UUID primary key to an :class:`AuditedModel`.

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| uuid | models.UUIDField | 1 | {"auto_created": true, "default": "`uuid.uuid4`", "editable": false, "primary_key": true, "type": "models.UUIDField", "unique": true} |


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### RepoQuotaStatistics

**Module**: `svc-bkrepo.svc_bk_repo.monitoring.models`  
**Line**: 1  
**Base Classes**: models.Model  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| max_size | models.BigIntegerField | 1 | {"help_text": "\u5355\u4f4d\u5b57\u8282\uff0c\u503c\u4e3a nul \u65f6\u8868\u793a\u672a\u8bbe\u7f6e\u4ed3\u5e93\u914d\u989d", "null": true, "type": "models.BigIntegerField", "verbose_name": "\u4ed3\u5e93\u6700\u5927\u914d\u989d"} |
| repo_name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField", "verbose_name": "\u4ed3\u5e93\u540d\u79f0"} |
| updated | models.DateTimeField | 1 | {"auto_now": true, "type": "models.DateTimeField"} |
| used | models.BigIntegerField | 1 | {"default": 0, "help_text": "\u5355\u4f4d\u5b57\u8282", "type": "models.BigIntegerField", "verbose_name": "\u4ed3\u5e93\u5df2\u4f7f\u7528\u5bb9\u91cf"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| instance | models.ForeignKey | paas_service.ServiceInstance | N/A | `models.CASCADE` |


---


### ApmData

**Module**: `svc-otel.svc_otel.vendor.models`  
**Line**: 1  
**Base Classes**: paas_service.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| app_name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| bk_app_code | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| data_token | models.CharField | 1 | {"max_length": 255, "type": "models.CharField"} |
| env | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| is_delete | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| unique_together | ['bk_app_code', 'env'] |

---


### CronTask

**Module**: `svc-rabbitmq.tasks.models`  
**Line**: 1  
**Base Classes**: models.Model  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| enabled | models.BooleanField | 1 | {"default": false, "type": "models.BooleanField"} |
| interval | models.DurationField | 1 | {"type": "models.DurationField"} |
| last_run_time | models.DateTimeField | 1 | {"blank": true, "null": true, "type": "models.DateTimeField"} |
| name | models.CharField | 1 | {"max_length": 255, "type": "models.CharField", "unique": true} |
| next_run_time | models.DateTimeField | 1 | {"blank": true, "db_index": true, "default": "`get_now`", "null": true, "type": "models.DateTimeField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| ordering | ['next_run_time', 'name'] |

---


### Cluster

**Module**: `svc-rabbitmq.vendor.models`  
**Line**: 1  
**Base Classes**: paas_service.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| admin | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| enable | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| host | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| management_api | models.TextField | 1 | {"type": "models.TextField"} |
| name | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| port | models.IntegerField | 1 | {"default": 5672, "type": "models.IntegerField"} |
| version | models.CharField | 1 | {"max_length": 16, "type": "models.CharField"} |



---


### ClusterTag

**Module**: `svc-rabbitmq.vendor.models`  
**Line**: 1  
**Base Classes**: svc-rabbitmq.vendor.models.Tag  
**Description**: 集群标签，用于分配和分组

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| key | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| value | models.CharField | 1 | {"max_length": 128, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| instance | models.ForeignKey | `Cluster` | tags | `models.CASCADE` |


---


### InstanceBill

**Module**: `svc-rabbitmq.vendor.models`  
**Line**: 1  
**Base Classes**: paas_service.models.UuidAuditedModel  
**Description**: 实例单据，保存申请上下文，方便重入

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| action | models.CharField | 1 | {"max_length": 32, "type": "models.CharField"} |
| name | models.CharField | 1 | {"max_length": 128, "type": "models.CharField"} |



---


### LimitPolicy

**Module**: `svc-rabbitmq.vendor.models`  
**Line**: 1  
**Base Classes**: svc-rabbitmq.vendor.models.LinkableModel  
**Description**: 集群下创建 vhost 限制机制，和具体 vhost 无关

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| cluster_id | models.IntegerField | 1 | {"blank": true, "default": null, "type": "models.IntegerField"} |
| enable | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| limit | models.CharField | 1 | {"blank": true, "choices": "`[(i.value, i.name) for i in LimitType]`", "max_length": 64, "null": true, "type": "models.CharField"} |
| link_type | models.IntegerField | 1 | {"choices": "`[(i.value, i.name) for i in LinkType]`", "default": "`LinkType.empty.value`", "type": "models.IntegerField"} |
| name | models.CharField | 1 | {"max_length": 64, "null": true, "type": "models.CharField"} |
| value | models.IntegerField | 1 | {"blank": true, "null": true, "type": "models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| linked | models.ForeignKey | self | N/A | `models.CASCADE` |


---


### LimitPolicyTag

**Module**: `svc-rabbitmq.vendor.models`  
**Line**: 1  
**Base Classes**: svc-rabbitmq.vendor.models.Tag  
**Description**: 表示绑定关系

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| key | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| value | models.CharField | 1 | {"max_length": 128, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| instance | models.ForeignKey | `LimitPolicy` | tags | `models.CASCADE` |


---


### LinkableModel

**Module**: `svc-rabbitmq.vendor.models`  
**Line**: 1  
**Base Classes**: paas_service.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| link_type | models.IntegerField | 1 | {"choices": "`[(i.value, i.name) for i in LinkType]`", "default": "`LinkType.empty.value`", "type": "models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| linked | models.ForeignKey | self | N/A | `models.CASCADE` |

#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### Tag

**Module**: `svc-rabbitmq.vendor.models`  
**Line**: 1  
**Base Classes**: paas_service.models.AuditedModel  

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| key | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| value | models.CharField | 1 | {"max_length": 128, "type": "models.CharField"} |


#### Meta Options

| Option | Value |
|--------|-------|
| abstract | True |

---


### UserPolicy

**Module**: `svc-rabbitmq.vendor.models`  
**Line**: 1  
**Base Classes**: svc-rabbitmq.vendor.models.LinkableModel  
**Description**: 集群下创建 vhost 默认策略，和具体 vhost 无关

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| apply_to | models.CharField | 1 | {"blank": true, "choices": "`[(i.value, i.name) for i in PolicyTarget]`", "max_length": 64, "null": true, "type": "models.CharField"} |
| cluster_id | models.IntegerField | 1 | {"blank": true, "default": null, "type": "models.IntegerField"} |
| enable | models.BooleanField | 1 | {"default": true, "type": "models.BooleanField"} |
| link_type | models.IntegerField | 1 | {"choices": "`[(i.value, i.name) for i in LinkType]`", "default": "`LinkType.empty.value`", "type": "models.IntegerField"} |
| name | models.CharField | 1 | {"max_length": 64, "null": true, "type": "models.CharField"} |
| pattern | models.CharField | 1 | {"blank": true, "max_length": 128, "null": true, "type": "models.CharField"} |
| priority | models.IntegerField | 1 | {"blank": true, "null": true, "type": "models.IntegerField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| linked | models.ForeignKey | self | N/A | `models.CASCADE` |


---


### UserPolicyTag

**Module**: `svc-rabbitmq.vendor.models`  
**Line**: 1  
**Base Classes**: svc-rabbitmq.vendor.models.Tag  
**Description**: 表示绑定关系

#### Fields

| Field Name | Type | Line | Parameters |
|------------|------|------|------------|
| key | models.CharField | 1 | {"max_length": 64, "type": "models.CharField"} |
| value | models.CharField | 1 | {"max_length": 128, "type": "models.CharField"} |

#### Relationships

| Field | Type | Target Model | Related Name | On Delete |
|-------|------|--------------|--------------|-----------|
| instance | models.ForeignKey | `UserPolicy` | tags | `models.CASCADE` |


---

