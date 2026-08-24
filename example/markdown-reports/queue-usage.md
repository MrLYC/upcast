# queue-usage 扫描报告

## 元数据
- **scanner_name**: queue-usage
- **static_analysis**: True

## 概要信息
- **总数量**: 27
- **已扫描文件数**: 2368
- **扫描耗时**: 138572 毫秒

- **队列使用总数**: 27
- **硬编码参数数**: 1
- **动态参数数**: 1
- **未知参数数**: 6

### 按类别统计
- **in_process**: 1
- **task_queue**: 25
- **redis**: 1

### 按框架统计
- **celery**: 25
- **queue**: 1
- **redis**: 1

## 结果详情

### in_process

| 框架 | 操作 | 文件 | 行号 | 函数 | 类 | 硬编码状态 | 语句 |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| queue | construct | apiserver/paasng/paas_wl/bk_app/processes/watch.py | 177 | __init__ | ParallelChainedGenerator | unknown | `queue.Queue()` |


### task_queue

| 框架 | 操作 | 文件 | 行号 | 函数 | 类 | 硬编码状态 | 语句 |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| celery | register | apiserver/paasng/paasng/accessories/log/tasks.py | 24 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/bk_plugins/bk_plugins/tasks.py | 32 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/bk_plugins/pluginscenter/tasks.py | 45 | 无 | 无 | unknown | `shared_task` |
| celery | construct | apiserver/paasng/paasng/celery.py | 27 | 无 | 无 | fully_hardcoded | `Celery('paasng')` |
| celery | register | apiserver/paasng/paasng/infras/iam/tasks.py | 24 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/tasks.py | 28 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/tasks.py | 40 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/applications/tasks.py | 33 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/applications/tasks.py | 60 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/engine/deploy/archive/tasks.py | 27 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/engine/deploy/bg_build/bg_build.py | 45 | 无 | 无 | unknown | `shared_task` |
| celery | delay | apiserver/paasng/paasng/platform/engine/deploy/bg_command/tasks.py | 53 | exec_command | 无 | partially_hardcoded | `execute_bg_command.delay(cmd_obj.uuid, stream_channel_id=stream_channel_id, extra_envs=extra_envs or {})` |
| celery | register | apiserver/paasng/paasng/platform/engine/deploy/bg_command/tasks.py | 57 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/engine/deploy/bg_command/tasks.py | 81 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/engine/deploy/building.py | 84 | 无 | 无 | unknown | `shared_task(base=I18nTask)` |
| celery | register | apiserver/paasng/paasng/platform/engine/deploy/building.py | 100 | 无 | 无 | unknown | `shared_task(base=I18nTask)` |
| celery | register | apiserver/paasng/paasng/platform/engine/deploy/image_release.py | 51 | 无 | 无 | unknown | `shared_task(base=I18nTask)` |
| celery | register | apiserver/paasng/paasng/platform/evaluation/tasks.py | 127 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/evaluation/tasks.py | 168 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/mgrlegacy/tasks.py | 40 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/mgrlegacy/tasks.py | 61 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/mgrlegacy/tasks.py | 77 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/mgrlegacy/tasks.py | 100 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/mgrlegacy/tasks.py | 117 | 无 | 无 | unknown | `shared_task` |
| celery | register | apiserver/paasng/paasng/platform/mgrlegacy/tasks.py | 134 | 无 | 无 | unknown | `shared_task` |

#### 参数（apiserver/paasng/paasng/celery.py:27）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| name | `'paasng'` | paasng | literal | 是 |
#### 参数（apiserver/paasng/paasng/platform/engine/deploy/bg_command/tasks.py:53）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| args | `cmd_obj.uuid` | 无 | configuration | 否 |
| stream_channel_id | `stream_channel_id` | 无 | unknown | 未知 |
| extra_envs | `extra_envs or {}` | 无 | unknown | 未知 |
#### 参数（apiserver/paasng/paasng/platform/engine/deploy/building.py:84）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| base | `I18nTask` | 无 | unknown | 未知 |
#### 参数（apiserver/paasng/paasng/platform/engine/deploy/building.py:100）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| base | `I18nTask` | 无 | unknown | 未知 |
#### 参数（apiserver/paasng/paasng/platform/engine/deploy/image_release.py:51）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| base | `I18nTask` | 无 | unknown | 未知 |

### redis

| 框架 | 操作 | 文件 | 行号 | 函数 | 类 | 硬编码状态 | 语句 |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| redis | construct | apiserver/paasng/paasng/utils/logging.py | 38 | __init__ | LogstashRedisHandler | unknown | `redis.Redis(connection_pool=pool)` |

#### 参数（apiserver/paasng/paasng/utils/logging.py:38）

| 名称 | 表达式 | 值 | 来源类型 | 是否硬编码 |
| --- | --- | --- | --- | --- |
| connection_pool | `pool` | 无 | unknown | 未知 |

### kafka

| 框架 | 操作 | 文件 | 行号 | 函数 | 类 | 硬编码状态 | 语句 |
| --- | --- | --- | ---: | --- | --- | --- | --- |


### rabbitmq

| 框架 | 操作 | 文件 | 行号 | 函数 | 类 | 硬编码状态 | 语句 |
| --- | --- | --- | ---: | --- | --- | --- | --- |
