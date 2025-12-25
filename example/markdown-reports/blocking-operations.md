# blocking-operations 扫描报告

## 元数据
暂无元数据。

## 概要信息
- **总数量**: 33
- **已扫描文件数**: 21
- **扫描耗时**: 10957 毫秒


### 按类别统计操作
- **time_based**: 28 个操作
- **database**: 5 个操作

## 结果详情

### 类别: time_based

| 文件 | 行号 | 操作 | 语句 | 函数 | 类 |
|------|------|------|------|------|-----|
| apiserver/paasng/paas_wl/bk_app/deploy/app_res/controllers.py | 215 | time.sleep | time.sleep(self._check_interval) | wait | WaitPodDelete |
| apiserver/paasng/paas_wl/bk_app/deploy/app_res/controllers.py | 308 | time.sleep | time.sleep(check_period) | _wait_pod_succeeded | PodScheduleHandler |
| apiserver/paasng/paas_wl/bk_app/deploy/app_res/controllers.py | 565 | time.sleep | time.sleep(check_period) | wait_for_succeeded | CommandHandler |
| apiserver/paasng/paas_wl/bk_app/deploy/app_res/controllers.py | 573 | time.sleep | time.sleep(check_period) | wait_for_succeeded | CommandHandler |
| apiserver/paasng/paas_wl/infras/resources/base/kres.py | 568 | time.sleep | time.sleep(check_period) | wait_for_default_sa | KNamespace |
| apiserver/paasng/paas_wl/infras/resources/base/kres.py | 594 | time.sleep | time.sleep(check_period) | wait_until_removed | KNamespace |
| apiserver/paasng/paas_wl/infras/resources/base/kres.py | 654 | time.sleep | time.sleep(check_period) | wait_for_status | KPod |
| apiserver/paasng/paas_wl/infras/resources/kube_res/base.py | 681 | time.sleep | time.sleep(self._check_interval) | wait | WaitDelete |
| apiserver/paasng/paasng/misc/monitoring/monitor/management/commands/init_alert_rules.py | 49 | time.sleep | time.sleep(1) | handle | Command |
| apiserver/paasng/paasng/misc/monitoring/monitor/management/commands/init_dashboards.py | 49 | time.sleep | time.sleep(1) | handle | Command |
| apiserver/paasng/paasng/plat_admin/admin_cli/deploy.py | 56 | time.sleep | time.sleep(1) | wait_for_release | 不适用 |
| apiserver/paasng/paasng/platform/engine/deploy/bg_build/executors.py | 338 | time.sleep | time.sleep(self.polling_result_interval) | _start_following_logs | PipelineBuildProcessExecutor |
| apiserver/paasng/tests/paas_wl/e2e/ingress/conftest.py | 57 | time.sleep | time.sleep(5) | sleep_only | 不适用 |
| apiserver/paasng/tests/paas_wl/e2e/ingress/utils.py | 127 | time.sleep | time.sleep(1) | get_ingress_nginx_pod | 不适用 |
| apiserver/paasng/tests/paas_wl/e2e/ingress/utils.py | 149 | time.sleep | time.sleep(0.2) | check_keyword_from_logs | IngressNginxReloadChecker |
| apiserver/paasng/tests/paas_wl/e2e/ingress/utils.py | 151 | time.sleep | time.sleep(1) | check_keyword_from_logs | IngressNginxReloadChecker |
| apiserver/paasng/tests/paas_wl/infras/resources/base/test_kres.py | 175 | time.sleep | time.sleep(1) | test_delete_collection | TestBatchOps |
| apiserver/paasng/tests/paas_wl/infras/resources/base/test_kres.py | 193 | time.sleep | time.sleep(1) | test_delete_individual | TestBatchOps |
| apiserver/paasng/tests/paasng/platform/engine/workflow/test_flow.py | 114 | time.sleep | time.sleep(0.2) | test_lock_timeout | TestDeploymentCoordinator |
| apiserver/paasng/tests/paasng/test_utils/test_rate_limit.py | 45 | time.sleep | time.sleep(window_size) | test_UserActionRateLimiter | 不适用 |
| apiserver/paasng/tests/paasng/test_utils/test_rate_limit.py | 68 | time.sleep | time.sleep(window_size) | test_rate_limits_on_view_func | 不适用 |
| svc-rabbitmq/tasks/management/commands/worker.py | 100 | time.sleep | sleep(cycle) | guard | Sentinel |
| svc-rabbitmq/tasks/management/commands/worker.py | 134 | time.sleep | sleep(0.1) | start | Cluster |
| svc-rabbitmq/vendor/management/commands/consumer.py | 68 | time.sleep | time.sleep(delay) | on_message | Command |
| svc-rabbitmq/vendor/management/commands/evict_connections.py | 152 | time.sleep | time.sleep(interval) | run | Command |
| svc-rabbitmq/vendor/management/commands/producer.py | 116 | time.sleep | time.sleep(delay) | publish | Command |
| svc-rabbitmq/vendor/management/commands/recovery_connections.py | 190 | time.sleep | time.sleep(sleep) | handle | Command |
| svc-rabbitmq/vendor/management/commands/sync_user_policies.py | 99 | time.sleep | time.sleep(sleep) | handle | Command |

---


### 类别: database

| 文件 | 行号 | 操作 | 语句 | 函数 | 类 |
|------|------|------|------|------|-----|
| apiserver/paasng/paas_wl/infras/cluster/models.py | 216 | self.select_for_update | self.select_for_update() | switch_default_cluster | ClusterManager |
| apiserver/paasng/paas_wl/infras/cluster/models.py | 217 | self.select_for_update | self.select_for_update() | switch_default_cluster | ClusterManager |
| apiserver/paasng/paasng/accessories/services/providers/base.py | 72 | select_for_update | PreCreatedInstance.objects.select_for_update() | create | ResourcePoolProvider |
| apiserver/paasng/paasng/platform/applications/models.py | 363 | select_for_update | self.modules.select_for_update() | get_module_with_lock | Application |
| apiserver/paasng/paasng/platform/applications/models.py | 367 | select_for_update | self.modules.select_for_update() | get_default_module_with_lock | Application |

---


### 类别: synchronization

| 文件 | 行号 | 操作 | 语句 | 函数 | 类 |
|------|------|------|------|------|-----|

---


### 类别: subprocess

| 文件 | 行号 | 操作 | 语句 | 函数 | 类 |
|------|------|------|------|------|-----|

---

