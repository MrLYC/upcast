# env-vars 扫描报告

## 元数据
- **scanner_name**: env-vars

## 概要信息
- **总数量**: 9
- **已扫描文件数**: 2368
- **扫描耗时**: 20561 毫秒

- **环境变量总数**: 9
- **必需变量**: 4
- **可选变量**: 5

## 结果详情

### PAAS_WL_CLUSTER_API_SERVER_URLS

**是否必需**: 否

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paas_wl/infras/cluster/management/commands/initial_default_cluster.py | 114 | 不适用 |  | 不适用 |

---


### prometheus_multiproc_dir

**是否必需**: 否

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/__init__.py | 33 | 不适用 |  | 不适用 |

---


### OAUTHLIB_INSECURE_TRANSPORT

**是否必需**: 是

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 35 | 不适用 |  | 不适用 |

---


### OAUTHLIB_RELAX_TOKEN_SCOPE

**是否必需**: 是

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 38 | 不适用 |  | 不适用 |

---


### BKPAAS_BUILD_VERSION

**是否必需**: 否
**默认值**: `unset`

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/plat_admin/admin42/context_processors.py | 24 | 不适用 |  | 不适用 |

---


### CELERY_TASK_DEFAULT_QUEUE

**是否必需**: 否
**默认值**: `celery`

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/settings/__init__.py | 656 | 不适用 |  | 不适用 |

---


### ...

**是否必需**: 否

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/utils/configs.py | 101 | 不适用 |  | 不适用 |

---


### PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT

**是否必需**: 是

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/tests/paas_wl/infras/cluster/test_commands.py | 56 | 不适用 |  | 不适用 |

---


### DATABASE_URL

**是否必需**: 是

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| svc-bkrepo/svc_bk_repo/settings/__init__.py | 140 | 不适用 |  | 不适用 |
| svc-mysql/svc_mysql/settings/__init__.py | 139 | 不适用 |  | 不适用 |
| svc-otel/svc_otel/settings/__init__.py | 139 | 不适用 |  | 不适用 |

---

