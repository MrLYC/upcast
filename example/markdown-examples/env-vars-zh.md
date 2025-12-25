# 环境变量分析

## 元数据
- **scanner_name**: env_vars

## 概要信息
- **总数量**: 9
- **已扫描文件数**: 2368
- **扫描耗时**: 10495 毫秒

- **环境变量总数**: 9
- **必需变量**: 6
- **可选变量**: 3

## 结果详情

### 

**是否必需**: 否  
**默认值**: `<dynamic>`

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/utils/configs.py | 101 | 20 | os.getenv('') | os.getenv(env_key, default) |

---


### BKPAAS_BUILD_VERSION

**是否必需**: 否  
**默认值**: `unset`

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/plat_admin/admin42/context_processors.py | 24 | 23 | os.getenv('BKPAAS_BUILD_VERSION') | os.getenv('BKPAAS_BUILD_VERSION', 'unset') |

---


### CELERY_TASK_DEFAULT_QUEUE

**是否必需**: 否  
**默认值**: `celery`

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/settings/__init__.py | 656 | 28 | os.environ.get('CELERY_TASK_DEFAULT_QUEUE') | os.environ.get('CELERY_TASK_DEFAULT_QUEUE', 'celery') |

---


### DATABASE_URL

**是否必需**: 是  

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| svc-bkrepo/svc_bk_repo/settings/__init__.py | 140 | 3 | os.getenv('DATABASE_URL') | os.getenv('DATABASE_URL') |
| svc-mysql/svc_mysql/settings/__init__.py | 139 | 3 | os.getenv('DATABASE_URL') | os.getenv('DATABASE_URL') |
| svc-otel/svc_otel/settings/__init__.py | 139 | 3 | os.getenv('DATABASE_URL') | os.getenv('DATABASE_URL') |

---


### OAUTHLIB_INSECURE_TRANSPORT

**是否必需**: 是  

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 35 | 不适用 | os.environ['OAUTHLIB_INSECURE_TRANSPORT'] | os.environ['OAUTHLIB_INSECURE_TRANSPORT'] |

---


### OAUTHLIB_RELAX_TOKEN_SCOPE

**是否必需**: 是  

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 38 | 不适用 | os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] | os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] |

---


### PAAS_WL_CLUSTER_API_SERVER_URLS

**是否必需**: 是  

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paas_wl/infras/cluster/management/commands/initial_default_cluster.py | 114 | 26 | os.environ.get('PAAS_WL_CLUSTER_API_SERVER_URLS') | os.environ.get('PAAS_WL_CLUSTER_API_SERVER_URLS') |

---


### PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT

**是否必需**: 是  

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/tests/paas_wl/infras/cluster/test_commands.py | 56 | 4 | os.environ['PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT'] | os.environ['PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT'] |

---


### prometheus_multiproc_dir

**是否必需**: 是  

#### 使用位置

| 文件 | 行号 | 列号 | 模式 | 代码 |
|------|------|------|------|------|
| apiserver/paasng/paasng/__init__.py | 33 | 11 | os.environ.get('prometheus_multiproc_dir') | os.environ.get('prometheus_multiproc_dir') |

---

