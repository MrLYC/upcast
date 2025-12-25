# Environment Variables Analysis

## Metadata
- **scanner_name**: env_vars

## Summary
- **Total Count**: 9
- **Files Scanned**: 2368
- **Scan Duration**: 10495 ms

- **Total Environment Variables**: 9
- **Required Variables**: 6
- **Optional Variables**: 3

## Results

### 

**Required**: No  
**Default Value**: `<dynamic>`

#### Usage Locations

| File | Line | Column | Pattern | Code |
|------|------|--------|---------|------|
| apiserver/paasng/paasng/utils/configs.py | 101 | 20 | os.getenv('') | os.getenv(env_key, default) |

---


### BKPAAS_BUILD_VERSION

**Required**: No  
**Default Value**: `unset`

#### Usage Locations

| File | Line | Column | Pattern | Code |
|------|------|--------|---------|------|
| apiserver/paasng/paasng/plat_admin/admin42/context_processors.py | 24 | 23 | os.getenv('BKPAAS_BUILD_VERSION') | os.getenv('BKPAAS_BUILD_VERSION', 'unset') |

---


### CELERY_TASK_DEFAULT_QUEUE

**Required**: No  
**Default Value**: `celery`

#### Usage Locations

| File | Line | Column | Pattern | Code |
|------|------|--------|---------|------|
| apiserver/paasng/paasng/settings/__init__.py | 656 | 28 | os.environ.get('CELERY_TASK_DEFAULT_QUEUE') | os.environ.get('CELERY_TASK_DEFAULT_QUEUE', 'celery') |

---


### DATABASE_URL

**Required**: Yes  

#### Usage Locations

| File | Line | Column | Pattern | Code |
|------|------|--------|---------|------|
| svc-bkrepo/svc_bk_repo/settings/__init__.py | 140 | 3 | os.getenv('DATABASE_URL') | os.getenv('DATABASE_URL') |
| svc-mysql/svc_mysql/settings/__init__.py | 139 | 3 | os.getenv('DATABASE_URL') | os.getenv('DATABASE_URL') |
| svc-otel/svc_otel/settings/__init__.py | 139 | 3 | os.getenv('DATABASE_URL') | os.getenv('DATABASE_URL') |

---


### OAUTHLIB_INSECURE_TRANSPORT

**Required**: Yes  

#### Usage Locations

| File | Line | Column | Pattern | Code |
|------|------|--------|---------|------|
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 35 | N/A | os.environ['OAUTHLIB_INSECURE_TRANSPORT'] | os.environ['OAUTHLIB_INSECURE_TRANSPORT'] |

---


### OAUTHLIB_RELAX_TOKEN_SCOPE

**Required**: Yes  

#### Usage Locations

| File | Line | Column | Pattern | Code |
|------|------|--------|---------|------|
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 38 | N/A | os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] | os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] |

---


### PAAS_WL_CLUSTER_API_SERVER_URLS

**Required**: Yes  

#### Usage Locations

| File | Line | Column | Pattern | Code |
|------|------|--------|---------|------|
| apiserver/paasng/paas_wl/infras/cluster/management/commands/initial_default_cluster.py | 114 | 26 | os.environ.get('PAAS_WL_CLUSTER_API_SERVER_URLS') | os.environ.get('PAAS_WL_CLUSTER_API_SERVER_URLS') |

---


### PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT

**Required**: Yes  

#### Usage Locations

| File | Line | Column | Pattern | Code |
|------|------|--------|---------|------|
| apiserver/paasng/tests/paas_wl/infras/cluster/test_commands.py | 56 | 4 | os.environ['PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT'] | os.environ['PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT'] |

---


### prometheus_multiproc_dir

**Required**: Yes  

#### Usage Locations

| File | Line | Column | Pattern | Code |
|------|------|--------|---------|------|
| apiserver/paasng/paasng/__init__.py | 33 | 11 | os.environ.get('prometheus_multiproc_dir') | os.environ.get('prometheus_multiproc_dir') |

---

