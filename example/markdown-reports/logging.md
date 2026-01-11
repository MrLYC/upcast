# logging 扫描报告

## 元数据
- **scanner_name**: logging

## 概要信息
- **总数量**: 866
- **已扫描文件数**: 293
- **扫描耗时**: 21205 毫秒

- **日志调用总数**: 866
- **敏感调用数**: 23

### 按库统计调用
- **logging**: 866 次调用

### 按级别统计调用
- **info**: 260 次调用
- **warning**: 179 次调用
- **exception**: 275 次调用
- **debug**: 97 次调用
- **error**: 52 次调用
- **critical**: 3 次调用

## 结果详情

### 文件: apiserver/paasng/paas_wl/apis/admin/views/clusters.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 157 | info | apiserver.paasng.paas_wl.apis.admin.views.clusters | will generate state for [{region}/{cluster_name}]... | fstring | function | 否 |
| 160 | info | apiserver.paasng.paas_wl.apis.admin.views.clusters | generating state for [{region}/{cluster_name}]... | fstring | function | 否 |
| 163 | info | apiserver.paasng.paas_wl.apis.admin.views.clusters | syncing the state to nodes... | string | function | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/cnative/specs/addresses.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 135 | warning | apiserver.paasng.paas_wl.bk_app.cnative.specs.addresses | no valid cert can be found for domain: %s, disable HTTPS. | string | if | 否 |
| 140 | info | apiserver.paasng.paas_wl.bk_app.cnative.specs.addresses | created a secret %s for host %s | string | if | 是 |
| 157 | info | apiserver.paasng.paas_wl.bk_app.cnative.specs.addresses | created a secret %s for host %s | string | if | 是 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/cnative/specs/credentials.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 108 | warning | apiserver.paasng.paas_wl.bk_app.cnative.specs.credentials | %s, service instance %s cannot generate tls certs, skip... | string | if | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/cnative/specs/handlers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 45 | info | apiserver.paasng.paas_wl.bk_app.cnative.specs.handlers | Refreshing default entrances for {application.code}/{env.environment}/{module.na... | fstring | try | 否 |
| 49 | exception | apiserver.paasng.paas_wl.bk_app.cnative.specs.handlers | Error syncing default entrances for {application.code}/{env.environment}/{module... | fstring | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/cnative/specs/resource.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 64 | info | apiserver.paasng.paas_wl.bk_app.cnative.specs.resource | Resource BkApp not found in cluster | string | except | 否 |
| 67 | info | apiserver.paasng.paas_wl.bk_app.cnative.specs.resource | BkApp not found in %s, app: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/cnative/specs/svc_disc.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 48 | debug | apiserver.paasng.paas_wl.bk_app.cnative.specs.svc_disc | No service discovery config found, remove the ConfigMap if exists | string | if | 否 |
| 57 | info | apiserver.paasng.paas_wl.bk_app.cnative.specs.svc_disc | Writing the service discovery addresses to ConfigMap, bk_app_name: %s | string | function | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/cnative/specs/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 165 | exception | apiserver.paasng.paas_wl.bk_app.cnative.specs.views | unable to fetch repo info, may be the credential error or a network exception. | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/deploy/actions/delete.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 85 | warning | apiserver.paasng.paas_wl.bk_app.deploy.actions.delete | Error deleting app cluster resources, app: %s, error: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/deploy/actions/deploy.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 91 | exception | apiserver.paasng.paas_wl.bk_app.deploy.actions.deploy | An error occur when creating ServiceMonitor | string | except | 否 |
| 99 | exception | apiserver.paasng.paas_wl.bk_app.deploy.actions.deploy | An error occur when creating BkLogConfig | string | except | 否 |
| 126 | info | apiserver.paasng.paas_wl.bk_app.deploy.actions.deploy | Cleaning process %s, remove-svc: %s | string | try | 否 |
| 133 | exception | apiserver.paasng.paas_wl.bk_app.deploy.actions.deploy | clean up process Uninferable of  failed, error detail: Instance of builtins.Exce... | string | except | 否 |
| 148 | debug | apiserver.paasng.paas_wl.bk_app.deploy.actions.deploy | Finding obsolete procs, versions: %s <-> %s | string | function | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/deploy/actions/exec.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 83 | exception | apiserver.paasng.paas_wl.bk_app.deploy.actions.exec | Duplicate pre-release-hook Pod exists | string | except | 否 |
| 105 | exception | apiserver.paasng.paas_wl.bk_app.deploy.actions.exec | %s execute failed | string | else | 否 |
| 110 | exception | apiserver.paasng.paas_wl.bk_app.deploy.actions.exec | A critical error happened during execute[{self.command}] | fstring | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/deploy/app_res/controllers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 193 | exception | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | timeout while waiting for the default sa of %s to be created | string | except | 否 |
| 249 | info | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | Pod<{namespace}/{pod_name}> does not exist, maybe have been cleaned. | fstring | except | 否 |
| 255 | warning | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | trying to clean Pod<{namespace}/{pod_name}>, but it's still running. | fstring | if | 否 |
| 258 | debug | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | trying to clean pod<{namespace}/{pod_name}>. | fstring | else | 否 |
| 269 | debug | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | trying to clean slug pod<{pod_name}>. | fstring | function | 否 |
| 344 | info | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | build slug<%s/%s> does not exist, will create one | string | except | 否 |
| 354 | info | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | %s has running more than %s, delete it and re-create one | string | if | 否 |
| 412 | debug | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | interrupting slugbuilder pod:{pod_name}... | fstring | function | 否 |
| 416 | warning | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | Try to interrupt slugbuilder pod, but the pod have gone! | string | except | 否 |
| 419 | exception | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | Failed to interrupt slugbuilder pod! | string | except | 否 |
| 489 | info | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | Command Pod<%s/%s> does not exist, will create one | string | except | 否 |
| 500 | info | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | %s has running more than %s, delete it and re-create one | string | if | 否 |
| 516 | info | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | Command Pod<%s/%s> does not exist, skip delete | string | except | 否 |
| 520 | warning | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | trying to clean Pod<{namespace}/{command.name}>, but it's still running. | fstring | if | 否 |
| 534 | debug | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | interrupting command pod:{command.name}... | fstring | function | 否 |
| 539 | warning | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | Try to interrupt command pod, but the pod have gone! | string | except | 否 |
| 542 | exception | apiserver.paasng.paas_wl.bk_app.deploy.app_res.controllers | Failed to interrupt command pod! | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/deploy/management/commands/delete_slug.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 110 | info | apiserver.paasng.paas_wl.bk_app.deploy.management.commands.delete_slug | 正在删除构建产物 %s | string | function | 否 |
| 125 | info | apiserver.paasng.paas_wl.bk_app.deploy.management.commands.delete_slug | 文件 %s 不符合删除规则 %s, 跳过删除. | string | if | 否 |
| 130 | info | apiserver.paasng.paas_wl.bk_app.deploy.management.commands.delete_slug | 删除文件 %s, 将释放 %s bytes 空间 | string | try | 否 |
| 136 | exception | apiserver.paasng.paas_wl.bk_app.deploy.management.commands.delete_slug | 删除资源 %s 失败 | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/deploy/processes.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 129 | exception | apiserver.paasng.paas_wl.bk_app.deploy.processes | Failed to sync replicas to ModuleProcessSpec for app({self.env.application.code}... | fstring | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/monitoring/app_monitor/shim.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 32 | warning | apiserver.paasng.paas_wl.bk_app.monitoring.app_monitor.shim | BKMonitor is not ready, skip apply ServiceMonitor | string | if | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/monitoring/bklog/kres_entities.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 76 | info | apiserver.paasng.paas_wl.bk_app.monitoring.bklog.kres_entities | BkLogConfig<%s/%s> does not exist, will skip delete | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/monitoring/bklog/shim.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 32 | warning | apiserver.paasng.paas_wl.bk_app.monitoring.bklog.shim | BkLog is not ready, skip apply BkLogConfig | string | if | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/processes/apps.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 35 | warning | apiserver.paasng.paas_wl.bk_app.processes.apps | Can not initialize process spec plans: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/processes/controllers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 72 | debug | apiserver.paasng.paas_wl.bk_app.processes.controllers | Process %s have no instances | string | if | 否 |
| 108 | warning | apiserver.paasng.paas_wl.bk_app.processes.controllers | Not any available Release | string | except | 否 |
| 117 | warning | apiserver.paasng.paas_wl.bk_app.processes.controllers | Process %s in procfile missing in k8s cluster | string | if | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/processes/migrations/0007_auto_20231127_1756.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 28 | warning | apiserver.paasng.paas_wl.bk_app.processes.migrations.0007_auto_20231127_1756 | scaling_config(%s) of obj<%s> is invalid, set it to None | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/processes/models.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 331 | debug | apiserver.paasng.paas_wl.bk_app.processes.models | Plan: {name} already exists, skip initialization. | fstring | try | 否 |
| 333 | info | apiserver.paasng.paas_wl.bk_app.processes.models | Creating default plan: {name}... | fstring | except | 否 |
| 339 | debug | apiserver.paasng.paas_wl.bk_app.processes.models | Plan: {cnative_plan} already exists, skip initialization. | fstring | try | 否 |
| 341 | info | apiserver.paasng.paas_wl.bk_app.processes.models | Creating default plan: {cnative_plan}... | fstring | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/processes/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 103 | warning | apiserver.paasng.paas_wl.bk_app.processes.views | Unable to update process, environment %s has gone offline. | string | if | 否 |
| 289 | debug | apiserver.paasng.paas_wl.bk_app.processes.views | Start watching process, app code=%s, environment=%s, params=%s | string | function | 否 |
| 311 | info | apiserver.paasng.paas_wl.bk_app.processes.views | Watching finished, app code=%s, environment=%s, params=%s | string | function | 否 |
| 403 | debug | apiserver.paasng.paas_wl.bk_app.processes.views | Start watching process, app=%s, params=%s | string | function | 否 |
| 420 | info | apiserver.paasng.paas_wl.bk_app.processes.views | Watching finished, app=%s, params=%s | string | function | 否 |




---


### 文件: apiserver/paasng/paas_wl/bk_app/processes/watch.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 197 | warning | apiserver.paasng.paas_wl.bk_app.processes.watch | Watch resource error: %s | string | if | 否 |
| 200 | exception | apiserver.paasng.paas_wl.bk_app.processes.watch | Consuming generator error. | string | except | 否 |
| 203 | debug | apiserver.paasng.paas_wl.bk_app.processes.watch | generator stopped | string | finally | 否 |




---


### 文件: apiserver/paasng/paas_wl/infras/cluster/management/commands/initial_default_cluster.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 125 | info | apiserver.paasng.paas_wl.infras.cluster.management.commands.initial_default_cluster | The cluster(pk:%s) already exists and overwriting is not allowed, skip | string | if | 否 |
| 129 | info | apiserver.paasng.paas_wl.infras.cluster.management.commands.initial_default_cluster | DRY-RUN: preparing to initialize the cluster, data: %s | string | if | 否 |
| 137 | info | apiserver.paasng.paas_wl.infras.cluster.management.commands.initial_default_cluster | The cluster was initialized successfully | string | function | 否 |




---


### 文件: apiserver/paasng/paas_wl/infras/cluster/migrations/0009_encrypt_cluster_in_db.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 30 | info | apiserver.paasng.paas_wl.infras.cluster.migrations.0009_encrypt_cluster_in_db | start encrypt Cluster in database... | string | function | 否 |
| 34 | info | apiserver.paasng.paas_wl.infras.cluster.migrations.0009_encrypt_cluster_in_db | Cluster encrypt done! | string | function | 否 |




---


### 文件: apiserver/paasng/paas_wl/infras/cluster/models.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 367 | debug | apiserver.paasng.paas_wl.infras.cluster.models | Custom resolver record: %s | string | if | 否 |




---


### 文件: apiserver/paasng/paas_wl/infras/cluster/pools.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 47 | warning | apiserver.paasng.paas_wl.infras.cluster.pools | Can't find any configurations for cluster %s | string | else | 否 |




---


### 文件: apiserver/paasng/paas_wl/infras/resources/base/base.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 71 | debug | apiserver.paasng.paas_wl.infras.resources.base.base | Send request to Kubernetes API %s... | string | with | 否 |




---


### 文件: apiserver/paasng/paas_wl/infras/resources/base/kres.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 328 | info | apiserver.paasng.paas_wl.infras.resources.base.kres | Create {self.kres.kind} {name} failed, already existed, continue update | fstring | function | 否 |
| 357 | info | apiserver.paasng.paas_wl.infras.resources.base.kres | Unable to find %s %s, start creating. | string | function | 否 |
| 368 | info | apiserver.paasng.paas_wl.infras.resources.base.kres | Creating %s %s. | string | function | 否 |
| 405 | warning | apiserver.paasng.paas_wl.infras.resources.base.kres | Delete failed, resource %s %s does not exists anymore | string | if | 否 |
| 409 | info | apiserver.paasng.paas_wl.infras.resources.base.kres | Resource %s %s has been deleted | string | function | 否 |
| 567 | warning | apiserver.paasng.paas_wl.infras.resources.base.kres | No default ServiceAccount found in namespace %s | string | while | 否 |
| 650 | warning | apiserver.paasng.paas_wl.infras.resources.base.kres | Pod %s %s not found. | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/infras/resources/generation/mapper.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 120 | warning | apiserver.paasng.paas_wl.infras.resources.generation.mapper | Unable to get the deployment name of %s, app: %s | string | except | 否 |
| 142 | warning | apiserver.paasng.paas_wl.infras.resources.generation.mapper | Error getting mapper_proc_config object, process: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/infras/resources/kube_res/base.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 202 | warning | apiserver.paasng.paas_wl.infras.resources.kube_res.base | {child_type} does not match current gvk_config, skip. error: {e} | fstring | except | 否 |
| 358 | warning | apiserver.paasng.paas_wl.infras.resources.kube_res.base | failed to deserialize k8s resource %s, skip. | string | if | 否 |
| 388 | debug | apiserver.paasng.paas_wl.infras.resources.kube_res.base | Picked deserializer:%s from multi choices, gvk_config: %s | string | function | 否 |
| 498 | warning | apiserver.paasng.paas_wl.infras.resources.kube_res.base | failed to deserialize k8s resource %s, skip. | string | if | 否 |
| 528 | debug | apiserver.paasng.paas_wl.infras.resources.kube_res.base | Picked deserializer:%s from multi choices, gvk_config: %s | string | function | 否 |
| 597 | info | apiserver.paasng.paas_wl.infras.resources.kube_res.base | {res.Meta.kres_class.kind}<%s/%s> does not exist, will create one | fstring | except | 否 |
| 649 | debug | apiserver.paasng.paas_wl.infras.resources.kube_res.base | Picked serializer:%s from multi choices, gvk_config: %s | string | function | 否 |




---


### 文件: apiserver/paasng/paas_wl/infras/resources/utils/basic.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 148 | warning | apiserver.paasng.paas_wl.infras.resources.utils.basic | Unknown tolerations format, data: %s | string | else | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/configuration/configmap/kres_entities.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 52 | info | apiserver.paasng.paas_wl.workloads.configuration.configmap.kres_entities | ConfigMap<%s/%s> does not exist, will skip delete | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/images/kres_entities.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 97 | info | apiserver.paasng.paas_wl.workloads.images.kres_entities | Secret<%s/%s> does not exist, will skip delete | string | except | 是 |




---


### 文件: apiserver/paasng/paas_wl/workloads/images/kres_slzs.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 60 | warning | apiserver.paasng.paas_wl.workloads.images.kres_slzs | unexpected resource name, given is '{kube_data.metadata.name}', but expected is ... | fstring | if | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/images/migrations/0003_auto_20230313_1751.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 38 | info | apiserver.paasng.paas_wl.workloads.images.migrations.0003_auto_20230313_1751 | start encrypt image credential in database... | string | function | 否 |
| 46 | info | apiserver.paasng.paas_wl.workloads.images.migrations.0003_auto_20230313_1751 | all image credential encrypted! | string | function | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/egress/cluster_state.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 48 | info | apiserver.paasng.paas_wl.workloads.networking.egress.cluster_state | legacy state found in database, current cluster state has already been recorded | string | try | 否 |
| 123 | debug | apiserver.paasng.paas_wl.workloads.networking.egress.cluster_state | Patching node object {node_name} with labels {labels} | fstring | for | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/egress/management/commands/region_gen_state.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 104 | debug | commands | Make scheduler client from region: {region} | fstring | for | 否 |
| 109 | info | commands | Will generate state for [{region}/{cluster.name}]... | fstring | for | 否 |
| 116 | info | commands | Generating state for [{region} - {cluster.name}]... | fstring | try | 否 |
| 119 | info | commands | Syncing the state to nodes... | string | try | 否 |
| 122 | exception | commands | Unable to generate state | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/egress/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 75 | warning | apiserver.paasng.paas_wl.workloads.networking.egress.views | No cluster state can be found for region=%s | string | except | 否 |
| 80 | exception | apiserver.paasng.paas_wl.workloads.networking.egress.views | Unable to crate RCStateBinding instance | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/entrance/entrance.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 46 | error | apiserver.paasng.paas_wl.workloads.networking.entrance.entrance | cannot found builtin address, application: %s, module: %s(%s) | string | if | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/entrance/handlers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 39 | info | apiserver.paasng.paas_wl.workloads.networking.entrance.handlers | Refreshing domains and subpaths for {application.code}/{module.name}... | fstring | try | 否 |
| 43 | exception | apiserver.paasng.paas_wl.workloads.networking.entrance.handlers | Error syncing domains and subpaths for {application.code}/{module.name} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/entrance/shim.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 189 | warning | apiserver.paasng.paas_wl.workloads.networking.entrance.shim | No addresses found matching preferred root domain: %s | string | if | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/config.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 46 | warning | apiserver.paasng.paas_wl.workloads.networking.ingress.config | get CUSTOM_DOMAIN_CONFIG from region: %s failed, return a default value. | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/domains/independent.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 43 | warning | apiserver.paasng.paas_wl.workloads.networking.ingress.domains.independent | Exception happened in `restore_ingress_on_error` block, will sync ingress resour... | string | except | 否 |
| 104 | exception | apiserver.paasng.paas_wl.workloads.networking.ingress.domains.independent | replace ingress failed | string | except | 否 |
| 126 | warning | apiserver.paasng.paas_wl.workloads.networking.ingress.domains.independent | Persistent object was required for deleting ingress, obj=%s | string | except | 否 |
| 129 | exception | apiserver.paasng.paas_wl.workloads.networking.ingress.domains.independent | delete ingress failed | string | except | 否 |
| 149 | warning | apiserver.paasng.paas_wl.workloads.networking.ingress.domains.independent | AppDomain record: %s-%s no longer exists in database, skip deletion | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/domains/manager.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 99 | exception | apiserver.paasng.paas_wl.workloads.networking.ingress.domains.manager | create custom domain failed | string | except | 否 |
| 180 | exception | apiserver.paasng.paas_wl.workloads.networking.ingress.domains.manager | Create custom domain for c-native app failed | string | except | 否 |
| 200 | exception | apiserver.paasng.paas_wl.workloads.networking.ingress.domains.manager | Update custom domain for c-native app failed | string | except | 否 |
| 216 | exception | apiserver.paasng.paas_wl.workloads.networking.ingress.domains.manager | Delete custom domain for c-native app failed | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/management/commands/patch_legacy_ingresses.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 71 | info | commands | checking ingress for app {app.name} with pattern {pattern} | fstring | function | 否 |
| 72 | info | commands | app was created at {app.created} | fstring | function | 否 |
| 80 | exception | commands | list domains failed for app %s | string | except | 否 |
| 100 | exception | commands | sync ingresses failed for app %s | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/management/commands/shared_cert_tool.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 69 | error | commands | Error: %s | string | function | 否 |
| 91 | error | commands | Argument error: %s | string | if | 否 |
| 94 | info | commands | Creating shared cert: %s | string | function | 否 |
| 112 | info | commands | Modifying shared cert object... | string | function | 否 |
| 114 | info | commands | (dry-run mode) skipping updating... | string | if | 否 |
| 120 | info | commands | Certificate updated. | string | function | 否 |
| 121 | info | commands | Run "refresh_cert" command to fresh related resources. | string | function | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/managers/base.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 134 | debug | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.base | Plugin: %s not configured, skip processing. | string | except | 否 |
| 198 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.base | Creating new default ingress<%s> with service<%s> | string | except | 否 |
| 219 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.base | Restore service name to default, ingress: %s, current name: %s, new name: %s | string | if | 否 |
| 227 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.base | Updating existed ingress<%s> | string | else | 否 |
| 239 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.base | updating existed ingress<{ingress.name}>, set service_name={service_name} port_n... | fstring | function | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/managers/domain.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 47 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.domain | Syncing app %s's default ingress... | string | for | 否 |
| 157 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.domain | created a secret %s for host %s | string | if | 是 |
| 169 | warning | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.domain | no valid cert can be found for domain: %s, disable HTTPS. | string | else | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/managers/misc.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 59 | warning | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.misc | app({self.app.name}) has no ApplicationEnvironment queryset, skip custom domain ... | fstring | except | 否 |
| 91 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.misc | Ingress resource not found, skip updating target, manager: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/managers/subpath.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 43 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.subpath | Syncing app %s's subpaths ingress... | string | for | 否 |
| 86 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.subpath | sub-path domain was not configured for cluster, return empty result | string | if | 否 |
| 105 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.subpath | created a secret %s for host %s | string | if | 是 |
| 115 | warning | apiserver.paasng.paas_wl.workloads.networking.ingress.managers.subpath | no valid cert can be found for domain: %s, disable HTTPS. | string | else | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/migrations/0007_encrypt_appdominsharedcert_in_db.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 31 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.migrations.0007_encrypt_appdominsharedcert_in_db | start encrypt AppDomainSharedCert in database... | string | function | 否 |
| 35 | info | apiserver.paasng.paas_wl.workloads.networking.ingress.migrations.0007_encrypt_appdominsharedcert_in_db | AppDomainSharedCert encrypt done! | string | function | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/plugins/ingress.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 172 | warning | apiserver.paasng.paas_wl.workloads.networking.ingress.plugins.ingress | "bkpa_site_id" not found in metadata | string | if | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/networking/ingress/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 101 | exception | apiserver.paasng.paas_wl.workloads.networking.ingress.views | unable to update ingresses from view | string | except | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/release_controller/hooks/kres_slzs.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 58 | warning | apiserver.paasng.paas_wl.workloads.release_controller.hooks.kres_slzs | Pod<%s/%s> missing start_time field! | string | else | 否 |




---


### 文件: apiserver/paasng/paas_wl/workloads/volume/persistent_volume_claim/kres_entities.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 52 | info | apiserver.paasng.paas_wl.workloads.volume.persistent_volume_claim.kres_entities | PersistentVolumeClaim<%s/%s> does not exist, will skip delete | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/app_secret/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 171 | warning | apiserver.paasng.paasng.accessories.app_secret.views | Verification code is not currently supported, return app secret directly | string | else | 是 |




---


### 文件: apiserver/paasng/paasng/accessories/ci/apps.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 38 | debug | apiserver.paasng.paasng.accessories.ci.apps | failed to load ci apps extension | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/ci/clients/bk_ci.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 65 | exception | apiserver.paasng.paasng.accessories.ci.clients.bk_ci | trigger codecc pipeline error, resp:{resp} | fstring | if | 否 |
| 78 | exception | apiserver.paasng.paasng.accessories.ci.clients.bk_ci | get codecc defect tool counts error, resp:{resp} | fstring | if | 否 |
| 91 | exception | apiserver.paasng.paasng.accessories.ci.clients.bk_ci | get codecc task info, resp:{resp} | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/ci/handlers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 43 | info | apiserver.paasng.paasng.accessories.ci.handlers | AppEnv<%s> deploy failed, skipping | string | if | 否 |
| 47 | info | apiserver.paasng.paasng.accessories.ci.handlers | Already exists a job for deployment<%s> of AppEnv<%s>, skipping | string | if | 否 |
| 54 | info | apiserver.paasng.paasng.accessories.ci.handlers | the ci job of source<%s> revision<%s> has been executed before | string | if | 否 |
| 67 | info | apiserver.paasng.paasng.accessories.ci.handlers | source type<%s> is not support, ci skipping | string | except | 否 |
| 70 | info | apiserver.paasng.paasng.accessories.ci.handlers | cannot get a repository, skip running CI job. | string | except | 否 |
| 73 | info | apiserver.paasng.paasng.accessories.ci.handlers | AppEnv<{sender}> failed to execute ci job: Oauth2TokenHolder does not exist | fstring | except | 否 |
| 76 | exception | apiserver.paasng.paasng.accessories.ci.handlers | failed to execute ci job, unknown error. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/cloudapi/components/http.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 40 | exception | apiserver.paasng.paasng.accessories.cloudapi.components.http | http request error! method: %s, url: %s, kwargs: %s | string | except | 否 |
| 43 | debug | apiserver.paasng.paasng.accessories.cloudapi.components.http | request third-party api: %s | string | function | 否 |
| 48 | exception | apiserver.paasng.paasng.accessories.cloudapi.components.http | response json error! method: %s, url: %s, kwargs: %s, response.status_code: %s, ... | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/cloudapi/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 212 | debug | apiserver.paasng.paasng.accessories.cloudapi.views | [cloudapi] getting %s | string | function | 否 |
| 240 | debug | apiserver.paasng.paasng.accessories.cloudapi.views | [cloudapi] posting %s | string | function | 否 |
| 269 | exception | apiserver.paasng.paasng.accessories.cloudapi.views | An exception occurred in the operation record of adding cloud API permissions | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/dev_sandbox/management/commands/recycle_dev_sandbox.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 54 | info | apiserver.paasng.paasng.accessories.dev_sandbox.management.commands.recycle_dev_sandbox | No expired dev sandboxes to recycle | string | if | 否 |
| 57 | info | apiserver.paasng.paasng.accessories.dev_sandbox.management.commands.recycle_dev_sandbox | Recycling %d expired dev sandboxes | string | function | 否 |
| 60 | info | apiserver.paasng.paasng.accessories.dev_sandbox.management.commands.recycle_dev_sandbox | Recycle dev sandbox: %s (app: %s, module: %s) | string | for | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/dev_sandbox/management/commands/renew_dev_sandbox_expired_at.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 44 | warning | apiserver.paasng.paasng.accessories.dev_sandbox.management.commands.renew_dev_sandbox_expired_at | Failed to get detail of dev sandbox: %s. Error: %s | string | except | 否 |
| 59 | warning | apiserver.paasng.paasng.accessories.dev_sandbox.management.commands.renew_dev_sandbox_expired_at | Dev sandbox status check failed for URL: %s. Error: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/dev_sandbox/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 156 | warning | apiserver.paasng.paasng.accessories.dev_sandbox.views | Unsupported absolute path<%s>, force transform to relative_to path. | string | if | 否 |
| 282 | debug | apiserver.paasng.paasng.accessories.dev_sandbox.views | The current source code system does not support parsing the version unique ID fr... | string | except | 否 |
| 286 | exception | apiserver.paasng.paasng.accessories.dev_sandbox.views | Failed to parse version information. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/log/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 186 | error | apiserver.paasng.paasng.accessories.log.client | query bk log error: {resp['message']} | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/log/filters.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 122 | warning | apiserver.paasng.paasng.accessories.log.filters | Field<%s> got an unhashable value: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/log/shim/setup_bklog.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 313 | debug | apiserver.paasng.paasng.accessories.log.shim.setup_bklog | CustomCollectorConfig does not exits, skip fill persistence fields | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/log/shim/setup_elk.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 132 | info | apiserver.paasng.paasng.accessories.log.shim.setup_elk | unique constraint conflict in the database when creating ProcessLogQueryConfig, ... | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/log/utils.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 146 | warning | apiserver.paasng.paasng.accessories.log.utils | can't parse %s from mappings, return what it is | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/log/views/config.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 141 | warning | apiserver.paasng.paasng.accessories.log.views.config | CustomCollectorConfig<name_en=%d> is not existed in bk-log! | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/log/views/logs.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 138 | exception | apiserver.paasng.paasng.accessories.log.views.logs | error log query conditions | string | except | 否 |
| 223 | error | apiserver.paasng.paasng.accessories.log.views.logs | Request error when querying logs: %s | string | except | 否 |
| 226 | exception | apiserver.paasng.paasng.accessories.log.views.logs | failed to get logs | string | except | 否 |
| 269 | exception | apiserver.paasng.paasng.accessories.log.views.logs | scroll_id 失效, 日志查询失败 | string | except | 否 |
| 273 | error | apiserver.paasng.paasng.accessories.log.views.logs | request error when querying logs: %s | string | except | 否 |
| 276 | exception | apiserver.paasng.paasng.accessories.log.views.logs | failed to get logs | string | except | 否 |
| 313 | error | apiserver.paasng.paasng.accessories.log.views.logs | request error when aggregate time-based histogram: %s | string | except | 否 |
| 316 | exception | apiserver.paasng.paasng.accessories.log.views.logs | failed to aggregate time-based histogram | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/paas_analysis/clients.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 45 | exception | apiserver.paasng.paasng.accessories.paas_analysis.clients | Unable to fetch response from {request_info} | fstring | except | 否 |
| 50 | exception | apiserver.paasng.paasng.accessories.paas_analysis.clients | invalid json response: {e.doc} | fstring | except | 否 |
| 53 | exception | apiserver.paasng.paasng.accessories.paas_analysis.clients | invalid response({e.status_code}) from {e.request_url}.Detail: {e.response_text} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/paas_analysis/handlers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 33 | exception | apiserver.paasng.paasng.accessories.paas_analysis.handlers | unable to enable ingress tracking, will proceed release | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/paas_analysis/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 57 | exception | apiserver.paasng.paasng.accessories.paas_analysis.views | an error occurred | string | except | 否 |
| 60 | debug | apiserver.paasng.paasng.accessories.paas_analysis.views | paas-analysis is not configured | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/publish/entrance/preallocated.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 104 | warning | apiserver.paasng.paasng.accessories.publish.entrance.preallocated | Fail to get preallocated address for application: %s, module: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/publish/market/status.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 40 | warning | apiserver.paasng.paasng.accessories.publish.market.status | The product object missing for app: %s | string | if | 否 |
| 48 | exception | apiserver.paasng.paasng.accessories.publish.market.status | Unable to publish to market for app: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/publish/sync_market/engine.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 77 | info | apiserver.paasng.paasng.accessories.publish.sync_market.engine | 成功更新应用%s的数据, 影响记录%s条，更新数据:%s | string | function | 否 |
| 308 | warning | apiserver.paasng.paasng.accessories.publish.sync_market.engine | `{self.product.tag.name}` 未关联桌面标签 | fstring | except | 否 |
| 327 | warning | apiserver.paasng.paasng.accessories.publish.sync_market.engine | The env object does not exist, app: %s(%s). | string | except | 否 |
| 333 | warning | apiserver.paasng.paasng.accessories.publish.sync_market.engine | The mobile config object does not exist, app: %s(%s). | string | except | 否 |
| 425 | info | apiserver.paasng.paasng.accessories.publish.sync_market.engine | sync exposed url for {application} | fstring | function | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 73 | debug | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | product:%s state changed to %s | string | if | 否 |
| 138 | exception | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | 同步修改 Product 属性到桌面失败！product: %s | string | except | 否 |
| 162 | exception | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | 同步开发者信息到桌面失败！ | string | except | 否 |
| 171 | info | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | op role is not defined, skip synchronization | string | except | 否 |
| 173 | exception | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | 同步运营人员信息到桌面失败！ | string | except | 否 |
| 258 | exception | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | 同步应用开发者信息至桌面失败! | string | except | 否 |
| 320 | warning | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | 未创建 product, 不同步信息至市场 | string | if | 否 |
| 355 | exception | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | 同步修改 Product 属性到桌面失败！product: %s | string | except | 否 |
| 368 | warning | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | 未创建 product, 不同步信息至市场 | string | if | 否 |
| 378 | exception | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | 同步修改 Product 属性到桌面失败！product: %s | string | except | 否 |
| 397 | exception | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | Unable to sync deployment for {application.code} | fstring | except | 否 |
| 423 | exception | apiserver.paasng.paasng.accessories.publish.sync_market.handlers | Unable to sync application logo to market | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/publish/sync_market/managers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 84 | info | apiserver.paasng.paasng.accessories.publish.sync_market.managers | Tag name is updated from {old_name} to {tag.name} | fstring | if | 否 |
| 87 | info | apiserver.paasng.paasng.accessories.publish.sync_market.managers | add new tag, name is {tag.name} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/publish/sync_market/utils.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 35 | warning | apiserver.paasng.paasng.accessories.publish.sync_market.utils | BK_CONSOLE_DB_CONF not provided, skip running %s | string | if | 否 |
| 48 | info | apiserver.paasng.paasng.accessories.publish.sync_market.utils | 成功更新应用%s的迁移状态为: %s, 影响记录%s条 | string | with | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/apps.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 37 | info | apiserver.paasng.paasng.accessories.servicehub.apps | skip remote services setup: {e} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/local/manager.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 150 | warning | apiserver.paasng.paasng.accessories.servicehub.local.manager | local instance {self.db_obj.pk} already provisioned, skip | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/management/commands/sync_instance_config.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 63 | error | commands | Service named "{service_name}" not found, abort. | fstring | if | 否 |
| 67 | error | commands | Service {svc.name} does not supports feature: instance config, abort. | fstring | if | 否 |
| 73 | debug | commands | Ignore not provisioned instances | string | if | 否 |
| 78 | info | commands | Synced instance {rel_obj.service_instance_id} | fstring | for | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/manager.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 164 | info | apiserver.paasng.paasng.accessories.servicehub.manager | module<{module_id}> has no attachment with service<{service_id}>, try next mgr | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/remote/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 102 | debug | apiserver.paasng.paasng.accessories.servicehub.remote.client | [servicehub] calling remote service<%s> | string | try | 否 |
| 105 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.client | unable to fetch remote services from {client.config.index_url} | fstring | except | 否 |
| 108 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.client | invalid json response from {client.config.index_url} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/remote/collector.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 76 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.collector | service data from {self.config} validation failed | fstring | except | 否 |
| 164 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.collector | unable to load remote service. | string | except | 否 |
| 166 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.collector | unable to load remote service. | string | except | 否 |
| 168 | debug | apiserver.paasng.paasng.accessories.servicehub.remote.collector | successfully loaded {config}. | fstring | else | 否 |
| 177 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.collector | update service failed. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/remote/manager.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 183 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.manager | Can not get app cluster egress info | string | except | 否 |
| 224 | warning | apiserver.paasng.paasng.accessories.servicehub.remote.manager | remote instance {self.db_obj.pk} already provisioned, skip | fstring | if | 否 |
| 228 | warning | apiserver.paasng.paasng.accessories.servicehub.remote.manager | remote service {self.get_service().name} is not ready, skip | fstring | if | 否 |
| 238 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.manager | Error provisioning new instance for {self.db_application.name} | fstring | except | 否 |
| 278 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.manager | Error when updating instance config for {instance_id} | fstring | except | 否 |
| 286 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.manager | Error occurs during recycling | string | except | 否 |
| 397 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.manager | Error when updating instance config for {instance_id} | fstring | except | 否 |
| 417 | exception | apiserver.paasng.paasng.accessories.servicehub.remote.manager | Error bind instance for {self.db_application.name} | fstring | except | 否 |
| 438 | info | apiserver.paasng.paasng.accessories.servicehub.remote.manager | going to delete remote service attachment from db | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/remote/store.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 96 | warning | apiserver.paasng.paasng.accessories.servicehub.remote.store | bulk_get: can not find a service by uuid {uuid} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/services.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 206 | info | apiserver.paasng.paasng.accessories.servicehub.services | going to delete remote service attachment from db | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/sharing.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 97 | error | apiserver.paasng.paasng.accessories.servicehub.sharing | Can not find referenced information from shared attachment: %s, data might be br... | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/tasks.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 30 | info | apiserver.paasng.paasng.accessories.servicehub.tasks | nothing need to clean. | string | if | 否 |
| 39 | warning | apiserver.paasng.paasng.accessories.servicehub.tasks | remote service should implement delete logic | string | except | 否 |
| 43 | warning | apiserver.paasng.paasng.accessories.servicehub.tasks | delete service instance<{uuid}> failed: {e} | fstring | except | 否 |
| 46 | info | apiserver.paasng.paasng.accessories.servicehub.tasks | instance<{uuid}> cleaned.  | fstring | else | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/servicehub/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 134 | warning | apiserver.paasng.paasng.accessories.servicehub.views | No plans can be found for service %s, specs: %s, environment: %s. | string | except | 否 |
| 139 | exception | apiserver.paasng.paasng.accessories.servicehub.views | bind service %s to module %s error. | string | except | 否 |
| 239 | exception | apiserver.paasng.paasng.accessories.servicehub.views | Unable to get module relationship | string | except | 否 |
| 246 | exception | apiserver.paasng.paasng.accessories.servicehub.views | Unable to unbind service: %s | string | except | 否 |
| 305 | exception | apiserver.paasng.paasng.accessories.servicehub.views | Failed to get enhanced service <%s> preset in template <%s> | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/services/models.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 140 | info | apiserver.paasng.paasng.accessories.services.models | going to delete instance resource: {instance_data.credentials} | fstring | function | 否 |
| 143 | info | apiserver.paasng.paasng.accessories.services.models | going to delete service instance<{service_instance.uuid}> from db | fstring | function | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/services/providers/base.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 127 | warning | apiserver.paasng.paasng.accessories.services.providers.base | `__pk__` is missing, recreate a new PreCreatedInstance by given credentials and ... | string | else | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/services/providers/mysql/provider.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 86 | exception | apiserver.paasng.paasng.accessories.services.providers.mysql.provider | Revoke privileges FAIL: %s | string | except | 否 |
| 153 | exception | apiserver.paasng.paasng.accessories.services.providers.mysql.provider | CommonMySQLProvider CREATE FAIL! create database for %s FAIL | string | except | 否 |
| 197 | exception | apiserver.paasng.paasng.accessories.services.providers.mysql.provider | delete failed | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/services/providers/sentry/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 51 | exception | apiserver.paasng.paasng.accessories.services.providers.sentry.client | Request sentry failed, connection exception | string | except | 否 |
| 59 | exception | apiserver.paasng.paasng.accessories.services.providers.sentry.client | Failed to request sentry, failed to parse json | string | except | 否 |
| 63 | exception | apiserver.paasng.paasng.accessories.services.providers.sentry.client | Request sentry failed, return status is not 20X/409[method=%s, url=%s, data=%s, ... | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/services/providers/sentry/provider.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 113 | exception | apiserver.paasng.paasng.accessories.services.providers.sentry.provider | create member or add member to team fail | string | except | 否 |
| 148 | exception | apiserver.paasng.paasng.accessories.services.providers.sentry.provider | patch: create member or add member to team fail | string | except | 否 |
| 157 | exception | apiserver.paasng.paasng.accessories.services.providers.sentry.provider | patch: remove user from team fail | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/smart_advisor/tagging.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 95 | debug | apiserver.paasng.paasng.accessories.smart_advisor.tagging | Deployment failure pattern match found: %s | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/accessories/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 54 | exception | apiserver.paasng.paasng.accessories.views | Unable to create tag from module language | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/bk_plugins/apigw.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 42 | exception | apiserver.paasng.paasng.bk_plugins.bk_plugins.apigw | Unable to sync API Gateway resource for "%s" | string | except | 否 |
| 48 | info | apiserver.paasng.paasng.bk_plugins.bk_plugins.apigw | Granting permissions on distributer: %s, plugin: %s | string | try | 否 |
| 51 | exception | apiserver.paasng.paasng.bk_plugins.bk_plugins.apigw | grant permissions error on %s | string | except | 否 |
| 63 | exception | apiserver.paasng.paasng.bk_plugins.bk_plugins.apigw | Unable to update gateway status to %s for '%s' | string | except | 否 |
| 76 | info | apiserver.paasng.paasng.bk_plugins.bk_plugins.apigw | Syncing api-gw resource for %s, triggered by setting distributor. | string | if | 否 |
| 80 | error | apiserver.paasng.paasng.bk_plugins.bk_plugins.apigw | Unable to set distributor for "%s", no related API Gateway resource can be found | string | if | 否 |
| 93 | info | apiserver.paasng.paasng.bk_plugins.bk_plugins.apigw | Granting permissions on distributer: %s, plugin: %s | string | try | 否 |
| 101 | info | apiserver.paasng.paasng.bk_plugins.bk_plugins.apigw | Revoking permissions on distributer: %s, plugin: %s | string | try | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/bk_plugins/handlers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 38 | debug | apiserver.paasng.paasng.bk_plugins.bk_plugins.handlers | Initializing plugin: "%s" is not plugin type, will not proceed. | string | if | 否 |
| 54 | debug | apiserver.paasng.paasng.bk_plugins.bk_plugins.handlers | Syncing plugin's api-gw resource: "%s" is not plugin type, will not proceed. | string | if | 否 |
| 58 | info | apiserver.paasng.paasng.bk_plugins.bk_plugins.handlers | Syncing api-gw resource for %s, triggered by deployment. | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/bk_plugins/logging.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 80 | exception | apiserver.paasng.paasng.bk_plugins.bk_plugins.logging | failed to adaptor to bk-sops required log format, missing field `%s` | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/bk_plugins/tasks.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 49 | warning | apiserver.paasng.paasng.bk_plugins.bk_plugins.tasks | 该插件<%s>未曾部署，跳过该环境的下架操作 | string | except | 否 |
| 51 | exception | apiserver.paasng.paasng.bk_plugins.bk_plugins.tasks | _('存在正在进行的下架任务，请勿重复操作') | string | except | 否 |
| 53 | exception | apiserver.paasng.paasng.bk_plugins.bk_plugins.tasks | app offline error | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/bk_plugins/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 194 | exception | apiserver.paasng.paasng.bk_plugins.bk_plugins.views | Unable to set distributor for {plugin_app} | fstring | except | 否 |
| 254 | exception | apiserver.paasng.paasng.bk_plugins.bk_plugins.views | Unable to set distributor for {plugin_app} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/bk_devops/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 73 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.bk_devops.client | get stream ci metrics summary (id: {devops_project_id}) error, resp:{resp} | fstring | if | 否 |
| 94 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.bk_devops.client | retrieve plugin({plugin_id}) basic info error, resp: %(resp)s | string | if | 否 |
| 124 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.bk_devops.client | start build for pipeline(%(pipeline)s) error, resp: %(resp)s | string | if | 否 |
| 150 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.bk_devops.client | retrieve build(%(build)s) detail error, resp: %(resp)s | string | if | 否 |
| 174 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.bk_devops.client | retrieve build(%(build)s) status error, resp: %(resp)s | string | if | 否 |
| 198 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.bk_devops.client | stop build(%(build)s) error, resp: %(resp)s | string | if | 否 |
| 235 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.bk_devops.client | retrieve build(%(build)s) log error, resp: %(resp)s | string | if | 否 |
| 256 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.bk_devops.client | retrieve build(%(build)s) log num error, resp: %(resp)s | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/iam_adaptor/management/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 118 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.management.client | create iam grade managers error, message:{resp['message']} 
 data: {data} | fstring | if | 否 |
| 136 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.management.client | 'get grade manager members error, grade_manager_id: {}, message:{}'.format(grade... | format | if | 否 |
| 160 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.management.client | 'add grade manager (id: {}) members error, message:{} \n data: {}'.format(grade_... | format | if | 否 |
| 181 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.management.client | 'delete grade manager members error, message:{} \n id: {}, params: {}'.format(re... | format | if | 否 |
| 216 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.management.client | 'create user groups error, message:{} \n grade_manager_id: {}, data: {}'.format(... | format | if | 否 |
| 239 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.management.client | 'delete user group error, group_id: {}, message:{}'.format(group_id, resp['messa... | format | if | 否 |
| 258 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.management.client | 'get user group members error, message:{} \n id: {}, params: {}'.format(resp['me... | format | if | 否 |
| 287 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.management.client | 'add user group members error, message:{} \n id: {}, data: {}'.format(resp['mess... | format | if | 否 |
| 310 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.management.client | 'delete user group members error, message:{} \n id: {}, params: {}'.format(resp[... | format | if | 否 |
| 356 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.iam_adaptor.management.client | 'grant user groups policies error, message:{} \n user_group_id: {}, data: {}'.fo... | format | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/itsm_adaptor/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 72 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.client | search service catalogs from itsm error, message:{resp} | fstring | if | 否 |
| 85 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.client | the root catalog information cannot be queried from itsm, catalogs: {catalogs} | fstring | function | 否 |
| 103 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.client | the plugin_center catalog information cannot be queried from itsm, catalogs: {ca... | fstring | function | 否 |
| 122 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.client | create plugin_center catalog at itsm error, message:{resp} 
data: {data} | fstring | if | 否 |
| 140 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.client | Failed to query the services under the catalog(id:{catalog_id}) on itsm error:{r... | fstring | if | 否 |
| 174 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.client | import service({service_path}) to itsm error, message:{resp} | fstring | if | 否 |
| 199 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.client | create application ticket at itsm  error, message:{resp} 
data: {data} | fstring | if | 否 |
| 217 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.client | get application ticket status from itsm error, message:{resp} 
sn: {sn} | fstring | if | 否 |
| 244 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.client | withdraw application ticket status from itsm error, message:{resp} 
data: {data} | fstring | if | 否 |
| 262 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.client | verify token from itsm error, resp:{resp} 
token: {token} | fstring | if | 是 |
| 266 | exception | root | itsm token checksum fails, resp:{resp} 
token: {token} | fstring | if | 是 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/itsm_adaptor/open_apis/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 123 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.open_apis.views | Not the latest release strategy for the current version:{release_id} | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/log/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 123 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.log.client | query bk log error: {resp['message']} | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/management/commands/import_itsm_service.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 52 | info | apiserver.paasng.paasng.bk_plugins.pluginscenter.management.commands.import_itsm_service | service({service_name}) information is already stored in DB | string | if | 否 |
| 58 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.management.commands.import_itsm_service | Request ITSM error. | string | except | 否 |
| 66 | info | apiserver.paasng.paasng.bk_plugins.pluginscenter.management.commands.import_itsm_service | import service({service_name}) to itsm success, service_id: {service_id} | fstring | else | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/models/instances.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 109 | info | apiserver.paasng.paasng.bk_plugins.pluginscenter.models.instances | Unable to make logo url for plugin: %s/%s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/releases/stages.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 91 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.releases.stages | execute post command [plugin_id: {self.plugin.id}, version:{self.release.version... | fstring | if | 否 |
| 118 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.releases.stages | execute pre command [plugin_id: {self.plugin.id}, version:{self.release.version}... | fstring | if | 否 |
| 345 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.releases.stages | execute post command [plugin_id: {self.plugin.id}, data:{data}], error: {resp} | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/shim.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 70 | warning | apiserver.paasng.paasng.bk_plugins.pluginscenter.shim | 即将删除插件<%s/%s>的源码仓库<%s> | string | try | 否 |
| 78 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.shim | 删除插件仓库<%s>失败! | string | except | 否 |
| 105 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.shim | 同步插件信息至第三方系统失败, 请联系相应的平台管理员排查 | string | except | 否 |
| 108 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.shim | 同步插件信息至第三方系统失败, 请联系相应的平台管理员排查 | string | except | 否 |
| 135 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.shim | The callback to the third API fails when updating the visible range | string | if | 否 |
| 146 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.shim | 创建仓库返回异常, 异常信息: %s | string | except | 否 |
| 152 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.shim | 执行 git 指令异常, 请联系管理员排查 | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/sourcectl/tencent.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 72 | warning | apiserver.paasng.paasng.bk_plugins.pluginscenter.sourcectl.tencent | get url `{resp.url}` but 404 | fstring | if | 否 |
| 75 | warning | apiserver.paasng.paasng.bk_plugins.pluginscenter.sourcectl.tencent | get url `{resp.url}` but 401 | fstring | if | 否 |
| 78 | warning | root | get url `{resp.url}` but 403 | fstring | if | 否 |
| 81 | warning | root | get url `{resp.url}` but 504 | fstring | if | 否 |
| 84 | warning | root | get url `{resp.url}` but {resp.status_code}, raw resp: {resp} | fstring | if | 否 |
| 90 | warning | root | get url `{resp.url}` but resp is not ok, raw resp: {resp} | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/thirdparty/configuration.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 34 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.configuration | sync config error [plugin_id: {instance.id}, data:{data}], error: {resp} | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/thirdparty/instance.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 37 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.instance | create instance error [operator: {operator}, data:{data}], error: {resp} | fstring | if | 否 |
| 48 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.instance | upadte instance error [plugin_id: {instance.id}, data:{data}], error: {resp} | fstring | if | 否 |
| 57 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.instance | archive instance error [plugin_id: {instance.id}], error: {resp} | fstring | if | 否 |
| 73 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.instance | archive instance error [plugin_id: {instance.id}], error: {resp} | fstring | if | 否 |
| 87 | info | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.instance | Visible range update callback API not configured, skip callback | string | if | 否 |
| 91 | info | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.instance | The plugin (id: {instance.id}) has not set the visible range, skipping callback | fstring | if | 否 |
| 107 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.instance | update visible range error: {resp} | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/thirdparty/members.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 37 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.members | sync members error [plugin_id: {instance.id}, data:{data}], error: {resp} | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/thirdparty/release.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 34 | info | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.release | Callback API endpoint is not set, skip callback | string | if | 否 |
| 54 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.release | Callback to {api_endpoint.apiName} failed: {resp} | fstring | if | 否 |
| 65 | info | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.release | Callback API is not set, skip callback | string | if | 否 |
| 77 | info | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.release | Callback API is not set, skip callback | string | if | 否 |
| 86 | info | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.release | Callback API is not set, skip callback | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/thirdparty/subpage.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 41 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.subpage | get sub page status error: {resp.get('message')} | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/thirdparty/utils.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 98 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.utils | An unknown exception occurred while requesting a third-party API. | string | if | 否 |
| 121 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.thirdparty.utils | Request to third-party API failed. | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/bk_plugins/pluginscenter/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 416 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.views | plugin(id: {plugin_id}) is deleted by {request.user.username} | fstring | function | 否 |
| 1087 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.views | request error when querying stdout log: %s | string | except | 否 |
| 1090 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.views | Failed to query stdout log | string | except | 否 |
| 1125 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.views | request error when querying structure log: %s | string | except | 否 |
| 1128 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.views | Failed to query structure log | string | except | 否 |
| 1161 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.views | request error when querying ingress log: %s | string | except | 否 |
| 1164 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.views | Failed to query ingress log | string | except | 否 |
| 1198 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.views | failed to aggregate time-based histogram: %s | string | except | 否 |
| 1201 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.views | failed to aggregate time-based histogram | string | except | 否 |
| 1237 | error | apiserver.paasng.paasng.bk_plugins.pluginscenter.views | request error when aggregating log fields: %s | string | except | 否 |
| 1240 | exception | apiserver.paasng.paasng.bk_plugins.pluginscenter.views | Failed to aggregate log fields | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/core/core/protections/base.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 78 | info | apiserver.paasng.paasng.core.core.protections.base | %s is not prepare for %s | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/core/core/storages/dbrouter.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 64 | info | apiserver.paasng.paasng.core.core.storages.dbrouter | _('检测到重命名前的 migration 记录 {}, 跳过执行当前 migration').format(str(sentinel)) | format | if | 否 |




---


### 文件: apiserver/paasng/paasng/core/core/storages/utils.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 114 | debug | root | [sqlalchemy] Connecting to outer-db. | string | function | 否 |
| 122 | debug | root | [sqlalchemy] outer-db commit. | string | try | 否 |
| 125 | debug | root | [sqlalchemy] outer-db rollback. | string | except | 否 |
| 129 | debug | root | [sqlalchemy] outer-db close. | string | finally | 否 |
| 136 | debug | root | [sqlalchemy] auto mapping models. | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/infras/accounts/management/commands/create_authed_app_user.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 69 | info | commands | user: {user_db.username} created. | fstring | function | 否 |
| 74 | info | commands | profile: {user.pk}({user.username}) created. | fstring | function | 否 |
| 80 | info | commands | app-user relation: {bk_app_code}-{user.username} created. | fstring | function | 否 |




---


### 文件: apiserver/paasng/paasng/infras/accounts/middlewares.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 71 | info | apiserver.paasng.paasng.infras.accounts.middlewares | Authenticated user by PrivateToken, username: %s, ip: %s, path: %s | string | if | 否 |
| 91 | warning | apiserver.paasng.paasng.infras.accounts.middlewares | private token {token_string} does not exist in database | fstring | except | 是 |
| 95 | warning | apiserver.paasng.paasng.infras.accounts.middlewares | private token {token_string} has expired | fstring | if | 是 |
| 98 | debug | apiserver.paasng.paasng.infras.accounts.middlewares | private token {token_string} is valid, user is {token_obj.user.username} | fstring | function | 是 |
| 125 | warning | apiserver.paasng.paasng.infras.accounts.middlewares | Invalid token header. No private token provided. | string | if | 是 |
| 128 | warning | apiserver.paasng.paasng.infras.accounts.middlewares | Invalid token header. Token string should not contain spaces. | string | if | 是 |
| 156 | info | apiserver.paasng.paasng.infras.accounts.middlewares | Authenticated user by AuthenticatedApp, username: %s, ip: %s, path: %s | string | if | 否 |
| 251 | warning | apiserver.paasng.paasng.infras.accounts.middlewares | Invalid auth header: {user_data} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/infras/accounts/oauth/backends.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 197 | exception | apiserver.paasng.paasng.infras.accounts.oauth.backends | Unable to get user credentials | string | except | 否 |
| 218 | debug | apiserver.paasng.paasng.infras.accounts.oauth.backends | request bkapp oauth api: %s | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/infras/accounts/oauth/models.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 62 | warning | apiserver.paasng.paasng.infras.accounts.oauth.models | scope<{scope_str}> does not match regex | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/infras/accounts/permissions/application.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 141 | exception | apiserver.paasng.paasng.infras.accounts.permissions.application | check user has application perm error. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/infras/accounts/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 233 | exception | apiserver.paasng.paasng.infras.accounts.views | failed to get token from Uninferable | string | except | 是 |
| 244 | exception | apiserver.paasng.paasng.infras.accounts.views | failed to save access token(from Uninferable) to Uninferable | string | except | 是 |
| 269 | exception | apiserver.paasng.paasng.infras.accounts.views | failed to delete access token from Uninferable | string | except | 是 |




---


### 文件: apiserver/paasng/paasng/infras/bk_ci/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 177 | error | apiserver.paasng.paasng.infras.bk_ci.client | call bk ci api failed, resp: %s | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/infras/bkmonitorv3/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 79 | error | apiserver.paasng.paasng.infras.bkmonitorv3.client | Failed to create space on BK Monitor, resp:%s 
data: %s | string | if | 否 |
| 109 | info | apiserver.paasng.paasng.infras.bkmonitorv3.client | Failed to update app space on BK Monitor, resp:{resp} 
data: {data} | fstring | if | 否 |
| 134 | info | apiserver.paasng.paasng.infras.bkmonitorv3.client | Failed to get space detail of %s on BK Monitor, resp: %s | string | if | 否 |
| 274 | info | apiserver.paasng.paasng.infras.bkmonitorv3.client | quick_import_dashboard, resp:{resp}, bk_biz_id: {biz_or_space_id}, dash_name: {d... | fstring | try | 否 |




---


### 文件: apiserver/paasng/paasng/infras/iam/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 101 | exception | apiserver.paasng.paasng.infras.iam.client | create iam grade managers error, message:{resp['message']} 
 data: {data} | fstring | if | 否 |
| 122 | exception | apiserver.paasng.paasng.infras.iam.client | 'delete grade manager error, message:{} grade_manager_id: {}'.format(resp['messa... | format | if | 否 |
| 148 | exception | apiserver.paasng.paasng.infras.iam.client | fetch iam grade managers error, message:{resp['message']} | fstring | if | 否 |
| 172 | exception | apiserver.paasng.paasng.infras.iam.client | 'get grade manager members error, grade_manager_id: {}, message:{}'.format(grade... | format | if | 否 |
| 204 | exception | apiserver.paasng.paasng.infras.iam.client | 'add grade manager (id: {}) members error, message:{} \n data: {}'.format(grade_... | format | if | 否 |
| 229 | exception | apiserver.paasng.paasng.infras.iam.client | 'delete grade manager members error, message:{} \n id: {}, params: {}'.format(re... | format | if | 否 |
| 272 | exception | apiserver.paasng.paasng.infras.iam.client | 'create user groups error, message:{} \n grade_manager_id: {}, data: {}'.format(... | format | if | 否 |
| 304 | exception | apiserver.paasng.paasng.infras.iam.client | 'delete user group error, group_id: {}, message:{}'.format(group_id, resp['messa... | format | if | 否 |
| 323 | exception | apiserver.paasng.paasng.infras.iam.client | 'get user group members error, message:{} \n id: {}, params: {}'.format(resp['me... | format | if | 否 |
| 360 | exception | apiserver.paasng.paasng.infras.iam.client | 'add user group members error, message:{} \n id: {}, data: {}'.format(resp['mess... | format | if | 否 |
| 386 | exception | apiserver.paasng.paasng.infras.iam.client | 'delete user group members error, message:{} \n id: {}, params: {}'.format(resp[... | format | if | 否 |
| 414 | exception | apiserver.paasng.paasng.infras.iam.client | 'grant user groups policies error, message:{} \n user_group_id: {}, data: {}'.fo... | format | if | 否 |
| 440 | exception | apiserver.paasng.paasng.infras.iam.client | 'revoke user groups policies error, message:{} \n user_group_id: {}, data: {}'.f... | format | if | 否 |
| 491 | exception | apiserver.paasng.paasng.infras.iam.client | update iam grade managers error, message:{resp['message']} 
 data: {data} | fstring | if | 否 |
| 518 | exception | apiserver.paasng.paasng.infras.iam.client | 'grant user groups policies in bk monitor error, msg:{} \n user_group_id: {}, da... | format | if | 否 |
| 548 | exception | apiserver.paasng.paasng.infras.iam.client | 'grant user groups policies in bk log error, message:{} \n user_group_id: {}, da... | format | if | 否 |




---


### 文件: apiserver/paasng/paasng/infras/iam/legacy.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 50 | exception | apiserver.paasng.paasng.infras.iam.legacy | check is allowed to manage smart app error. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/infras/iam/permissions/apply_url.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 49 | error | apiserver.paasng.paasng.infras.iam.permissions.apply_url | generate_apply_url failed: %s | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/infras/iam/permissions/resources/application.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 220 | warning | apiserver.paasng.paasng.infras.iam.permissions.resources.application | generate user app filters failed: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/infras/legacydb/adaptors.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 105 | info | apiserver.paasng.paasng.infras.legacydb.adaptors | Application attribute {key} does not exist, skip synchronization | fstring | if | 否 |
| 186 | info | apiserver.paasng.paasng.infras.legacydb.adaptors | APP(code:{code}) oauth information does not exist, skip oauth synchronization | fstring | except | 否 |
| 196 | info | apiserver.paasng.paasng.infras.legacydb.adaptors | APP(code:{code}) does not exist, skip oauth synchronization | fstring | if | 否 |
| 325 | warning | apiserver.paasng.paasng.infras.legacydb.adaptors | App(code:{code}) does not exist, skip updating developers to console | fstring | if | 否 |
| 421 | info | apiserver.paasng.paasng.infras.legacydb.adaptors | app with code({code}) does not exists, skip create release record | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/infras/oauth2/api.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 55 | exception | apiserver.paasng.paasng.infras.oauth2.api | Unable to fetch response from {request_info}, curl: {curl_command} | fstring | except | 否 |
| 60 | exception | apiserver.paasng.paasng.infras.oauth2.api | invalid json response: {e.doc} | fstring | except | 否 |
| 63 | exception | apiserver.paasng.paasng.infras.oauth2.api | invalid response(%s) from %s ,request_id: %s ,Detail: %s | string | except | 否 |
| 82 | error | apiserver.paasng.paasng.infras.oauth2.api | request bkAuth api: %s | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/misc/audit/apps.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 33 | info | root | No bkaudit related config is provided, skip registering | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/misc/audit/service.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 67 | debug | apiserver.paasng.paasng.misc.audit.service | skip report to bk_audit, record:{record.uuid} | fstring | if | 否 |
| 84 | exception | apiserver.paasng.paasng.misc.audit.service | bk_audit add application event error: username: %s, action_id: %s, scope_id: %s,... | string | except | 否 |
| 92 | info | apiserver.paasng.paasng.misc.audit.service | bk_audit add application event: username: %s, action_id: %s, app_code: %s | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/misc/changelog/query.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 61 | exception | apiserver.paasng.paasng.misc.changelog.query | invalid changelog file {file.name}. | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/misc/metrics/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 45 | info | apiserver.paasng.paasng.misc.metrics.views | enable prometheus using multi processes mode | string | if | 否 |
| 50 | info | apiserver.paasng.paasng.misc.metrics.views | enable prometheus using single process mode | string | else | 否 |




---


### 文件: apiserver/paasng/paasng/misc/metrics/workloads/deployment.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 53 | exception | apiserver.paasng.paasng.misc.metrics.workloads.deployment | configuration of cluster<{cluster.name}> is not ready | fstring | except | 否 |
| 59 | exception | apiserver.paasng.paasng.misc.metrics.workloads.deployment | list unavailable deployments of cluster<{cluster.name}>  | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/metrics/clients/bkmonitor.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 49 | exception | apiserver.paasng.paasng.misc.monitoring.metrics.clients.bkmonitor | fetch metrics failed, query: %s. | string | except | 否 |
| 70 | info | apiserver.paasng.paasng.misc.monitoring.metrics.clients.bkmonitor | prometheus query_range promql: %s, start: %s, end: %s, step: %s | string | function | 否 |
| 77 | warning | apiserver.paasng.paasng.misc.monitoring.metrics.clients.bkmonitor | failed to get metric results: %s | string | except | 否 |
| 88 | warning | apiserver.paasng.paasng.misc.monitoring.metrics.clients.bkmonitor | fetch metrics failed, promql: %s, start: %s, end: %s, step: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/metrics/clients/prometheus.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 51 | exception | apiserver.paasng.paasng.misc.monitoring.metrics.clients.prometheus | fetch metrics failed, query: %s | string | except | 否 |
| 74 | info | apiserver.paasng.paasng.misc.monitoring.metrics.clients.prometheus | prometheus query_range: %s | string | function | 否 |
| 83 | warning | apiserver.paasng.paasng.misc.monitoring.metrics.clients.prometheus | failed to get metric results, for %s | string | except | 否 |
| 86 | exception | apiserver.paasng.paasng.misc.monitoring.metrics.clients.prometheus | failed to get metrics results | string | except | 否 |
| 94 | debug | apiserver.paasng.paasng.misc.monitoring.metrics.clients.prometheus | Prometheus client sending request to [{method}]{url}, kwargs={kwargs}. | fstring | function | 否 |
| 103 | warning | apiserver.paasng.paasng.misc.monitoring.metrics.clients.prometheus | fetch<%s> metrics failed | string | if | 否 |
| 108 | warning | apiserver.paasng.paasng.misc.monitoring.metrics.clients.prometheus | fetch<%s> metrics failed | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/metrics/management/commands/deploy_stats_diagnoser.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 76 | debug | commands | Generating stats for cluster: %s | string | for | 否 |
| 80 | warning | commands | Unable to make client for {cluster.name} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/metrics/models.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 82 | info | apiserver.paasng.paasng.misc.monitoring.metrics.models | %s type not exist in query tmpl | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/ascode/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 139 | exception | apiserver.paasng.paasng.misc.monitoring.monitor.alert_rules.ascode.client | ascode import alert rule configs of app_code({self.app_code}) error. | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/config/app_rule.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 154 | info | apiserver.paasng.paasng.misc.monitoring.monitor.alert_rules.config.app_rule | generate metric labels failed: {e} | fstring | except | 否 |
| 219 | info | apiserver.paasng.paasng.misc.monitoring.monitor.alert_rules.config.app_rule | generate metric labels failed: {e} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/config/metric_label.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 121 | info | apiserver.paasng.paasng.misc.monitoring.monitor.alert_rules.config.metric_label | `e` | string | except | 否 |
| 128 | info | apiserver.paasng.paasng.misc.monitoring.monitor.alert_rules.config.metric_label | service {service_name} not bounded with app: {app_code}, module: {module_name} | fstring | function | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/manager.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 157 | warning | apiserver.paasng.paasng.misc.monitoring.monitor.alert_rules.manager | bkmonitor in this edition not enabled, skip apply Monitor Rules | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/tasks.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 34 | exception | apiserver.paasng.paasng.misc.monitoring.monitor.alert_rules.tasks | Unable to create alert rules after release app(code: {app_code}, module: {module... | fstring | except | 否 |
| 46 | exception | apiserver.paasng.paasng.misc.monitoring.monitor.alert_rules.tasks | Unable to update notice group (code: {app_code}) | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/monitor/dashboards/handlers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 40 | exception | apiserver.paasng.paasng.misc.monitoring.monitor.dashboards.handlers | Unable to import builtin dashboards after release app(code: {app_code}) | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/monitor/dashboards/manager.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 83 | warning | apiserver.paasng.paasng.misc.monitoring.monitor.dashboards.manager | bkmonitor in this edition not enabled, skip the built-in dashboard | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/monitor/serializers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 109 | error | apiserver.paasng.paasng.misc.monitoring.monitor.serializers | Invalid type for 'alert_name': expected type 'str' | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/misc/monitoring/monitor/service_monitor/controller.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 40 | warning | apiserver.paasng.paasng.misc.monitoring.monitor.service_monitor.controller | BKMonitor is not ready, skip apply ServiceMonitor | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/misc/search/backends.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 63 | warning | apiserver.paasng.paasng.misc.search.backends | Got invalid status_code: %s from response | string | if | 否 |
| 69 | warning | apiserver.paasng.paasng.misc.search.backends | Response is not valid JSON string, response: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/plat_admin/admin42/serializers/accountmgr.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 47 | warning | apiserver.paasng.paasng.plat_admin.admin42.serializers.accountmgr | except a dirty userprofile, error: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/plat_admin/api_doc/generators.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 70 | warning | apiserver.paasng.paasng.plat_admin.api_doc.generators | nested var is unsupported! | string | if | 否 |
| 77 | warning | apiserver.paasng.paasng.plat_admin.api_doc.generators | var is not closed! | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/plat_admin/initialization/management/commands/init_bkrepo.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 74 | debug | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | 错误码: {e.code} | fstring | except | 否 |
| 78 | warning | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | [deprecated] 捕获到可能是旧版本的蓝鲸制品库(bkrepo)的错误码, 忽略. | string | if | 否 |
| 118 | info | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | init_enabled is set to {init_enabled}, skip init bkrepo | fstring | if | 否 |
| 123 | info | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | super_username or super_password is empty, skip init bkrepo | string | if | 否 |
| 126 | info | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | 开始初始化 bkrepo | string | function | 否 |
| 130 | info | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | 即将创建 bkrepo 项目: %s | string | function | 否 |
| 135 | info | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | 即将创建 bkrepo 项目: %s | string | function | 否 |
| 141 | info | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | 即将创建 bkrepo 用户: %s | string | function | 否 |
| 146 | info | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | 即将创建 bkrepo 用户: %s | string | function | 否 |
| 156 | info | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | 即将创建 bkrepo 的仓库: %s | string | for | 否 |
| 163 | info | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | 即将创建 bkrepo 用户: bklesscode | string | function | 否 |
| 175 | info | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | 即将上传开发框架模板至 %s | string | if | 否 |
| 178 | warning | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | 源码模板不存在! 请检查 %s | string | else | 否 |
| 180 | info | apiserver.paasng.paasng.plat_admin.initialization.management.commands.init_bkrepo | 初始化 bkrepo 成功 | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/plat_admin/numbers/app.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 260 | warning | apiserver.paasng.paasng.plat_admin.numbers.app | No source object found for application %s | string | if | 否 |
| 633 | warning | apiserver.paasng.paasng.plat_admin.numbers.app | app %s was duplicated | string | if | 否 |
| 754 | info | apiserver.paasng.paasng.plat_admin.numbers.app | start calculate_user_contribution_in_app for user:%s, app:%s | string | try | 否 |
| 756 | info | apiserver.paasng.paasng.plat_admin.numbers.app | finish calculate_user_contribution_in_app for user:%s, app:%s | string | try | 否 |
| 758 | exception | apiserver.paasng.paasng.plat_admin.numbers.app | Can't find Oauth2TokenHolder for user: %s | string | except | 否 |
| 760 | exception | apiserver.paasng.paasng.plat_admin.numbers.app | Unexpected exception | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/plat_admin/system/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 173 | info | apiserver.paasng.paasng.plat_admin.system.views | service named '%s' not found | string | except | 否 |
| 205 | exception | apiserver.paasng.paasng.plat_admin.system.views | bind service %s to module %s error. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/applications/cleaner.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 36 | info | apiserver.paasng.paasng.platform.applications.cleaner | going to delete iam resources for Application<%s> | string | function | 否 |
| 40 | info | apiserver.paasng.paasng.platform.applications.cleaner | going to delete Application<%s> | string | function | 否 |
| 46 | info | apiserver.paasng.paasng.platform.applications.cleaner | delete all builtin user groups for application(%s) | string | function | 否 |
| 50 | info | apiserver.paasng.paasng.platform.applications.cleaner | delete grade manager for application(%s) | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/applications/handlers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 62 | debug | apiserver.paasng.paasng.platform.applications.handlers | initialize members after create app: creator=%s app_code=%s | string | function | 否 |
| 85 | debug | apiserver.paasng.paasng.platform.applications.handlers | Increasing new application counter: application=%s | string | function | 否 |
| 105 | info | apiserver.paasng.paasng.platform.applications.handlers | application[%s] active state is setting to inactive | string | if | 否 |
| 119 | info | apiserver.paasng.paasng.platform.applications.handlers | application[%s] active state is setting to active | string | if | 否 |
| 147 | info | apiserver.paasng.paasng.platform.applications.handlers | Duplicating logo: %s to bucket: %s... | string | with | 否 |
| 176 | exception | apiserver.paasng.paasng.platform.applications.handlers | get logo object:%s failed, will not continue | string | except | 否 |
| 181 | debug | apiserver.paasng.paasng.platform.applications.handlers | CacheControl was already set on %s | string | if | 否 |
| 196 | exception | apiserver.paasng.paasng.platform.applications.handlers | update key: %s's metadata failed | string | except | 否 |
| 220 | debug | apiserver.paasng.paasng.platform.applications.handlers | turn on ENABLE_BK_LOG_COLLECTOR flag for application %s | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/applications/management/commands/create_3rd_party_apps.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 87 | info | apiserver.paasng.paasng.platform.applications.management.commands.create_3rd_party_apps | DRY-RUN: going to create App according to desc: %s | string | if | 否 |
| 93 | info | apiserver.paasng.paasng.platform.applications.management.commands.create_3rd_party_apps | app(code:%s) not exists in THIRD_APP_INIT_CODE_LIST, skip create | string | if | 否 |
| 100 | info | apiserver.paasng.paasng.platform.applications.management.commands.create_3rd_party_apps | app(code:%s) exists in PaaS2.0, skip create | string | if | 否 |
| 103 | info | apiserver.paasng.paasng.platform.applications.management.commands.create_3rd_party_apps | going to create App according to desc: %s | string | for | 否 |
| 131 | info | apiserver.paasng.paasng.platform.applications.management.commands.create_3rd_party_apps | create oauth app(code:%s) with an existing key | string | finally | 否 |
| 135 | info | apiserver.paasng.paasng.platform.applications.management.commands.create_3rd_party_apps | create oauth app(code:%s) with a new randomly generated key | string | else | 否 |
| 151 | info | apiserver.paasng.paasng.platform.applications.management.commands.create_3rd_party_apps | app(name:%s) exists, skip create | string | except | 否 |
| 158 | exception | apiserver.paasng.paasng.platform.applications.management.commands.create_3rd_party_apps | app initialize members failed, skip create: %s | string | except | 否 |
| 168 | error | apiserver.paasng.paasng.platform.applications.management.commands.create_3rd_party_apps | app with the same {e.field} field already exists in paas2.0, skip create. | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/applications/management/commands/force_del_app.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 85 | exception | apiserver.paasng.paasng.platform.applications.management.commands.force_del_app | {filter_key} 为 {filter_value} 从 PaaS2.0 中删除失败. | fstring | except | 否 |
| 96 | info | apiserver.paasng.paasng.platform.applications.management.commands.force_del_app | {filter_key} 为 {filter_value} 的应用鉴权信息已经从 Application 表中删除 | fstring | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/applications/models.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 429 | info | apiserver.paasng.paasng.platform.applications.models | Unable to make logo url for application: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/applications/specs.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 80 | warning | apiserver.paasng.paasng.platform.applications.specs | Unable to get metadata, invalid template name: "{module.source_init_template}" | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/applications/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 476 | exception | apiserver.paasng.paasng.platform.applications.views | unable to delete app<%s> related resources | string | except | 否 |
| 503 | exception | apiserver.paasng.paasng.platform.applications.views | unable to clean application related resources | string | except | 否 |
| 510 | exception | apiserver.paasng.paasng.platform.applications.views | unable to delete application {application.code} | fstring | except | 否 |
| 543 | info | apiserver.paasng.paasng.platform.applications.views | Failed to update app space on BK Monitor, {e} | fstring | except | 否 |
| 545 | exception | apiserver.paasng.paasng.platform.applications.views | Failed to update app space on BK Monitor | string | except | 否 |
| 819 | warning | apiserver.paasng.paasng.platform.applications.views | _('集群未配置默认的根域名, 请检查 region=%s 下的集群配置是否合理.') | string | except | 否 |
| 897 | exception | apiserver.paasng.paasng.platform.applications.views | Invalid app_desc.yaml cause create app failed | string | except | 否 |
| 900 | exception | apiserver.paasng.paasng.platform.applications.views | Controller error cause create app failed | string | except | 否 |
| 1173 | warning | apiserver.paasng.paasng.platform.applications.views | Verification code is not currently supported, return app secret directly | string | else | 是 |
| 1274 | exception | apiserver.paasng.paasng.platform.applications.views | Create lapp %s(%s) failed! | string | except | 否 |
| 1280 | exception | apiserver.paasng.paasng.platform.applications.views | save app base info fail. | string | except | 否 |
| 1290 | exception | apiserver.paasng.paasng.platform.applications.views | 同步开发者信息到桌面失败！ | string | except | 否 |
| 1313 | exception | apiserver.paasng.paasng.platform.applications.views | save app base info fail. | string | except | 否 |
| 1347 | exception | apiserver.paasng.paasng.platform.applications.views | save app base info fail. | string | except | 否 |
| 1356 | exception | apiserver.paasng.paasng.platform.applications.views | 同步开发者信息到桌面失败！ | string | except | 否 |
| 1429 | exception | apiserver.paasng.paasng.platform.applications.views | Fail to update logo cache. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/bk_lesscode/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 84 | exception | apiserver.paasng.paasng.platform.bk_lesscode.client | create lesscode app error, message:{resp['message']} 
 data: {data} | fstring | if | 否 |
| 96 | exception | apiserver.paasng.paasng.platform.bk_lesscode.client | Get lesscode app address path error. | string | except | 否 |
| 101 | exception | apiserver.paasng.paasng.platform.bk_lesscode.client | create lesscode app error, message:{resp['message']} 
 params: {params} | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/bkapp_model/entities_syncer/addons.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 37 | warning | apiserver.paasng.paasng.platform.bkapp_model.entities_syncer.addons | Import addons is not implemented, skip. | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/bkapp_model/entities_syncer/proc_env_overlays.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 134 | info | apiserver.paasng.paasng.platform.bkapp_model.entities_syncer.proc_env_overlays | Process spec not found, ignore, name: %s | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/bkapp_model/manifest.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 174 | warning | apiserver.paasng.paasng.platform.bkapp_model.manifest | 模块<%s> 未定义任何进程 | string | if | 否 |
| 182 | warning | apiserver.paasng.paasng.platform.bkapp_model.manifest | 模块<%s>的 %s 进程 未定义启动命令, 将使用镜像默认命令运行 | string | except | 否 |
| 255 | debug | apiserver.paasng.paasng.platform.bkapp_model.manifest | unknown ResQuotaPlan value `%s`, try to convert ProcessSpecPlan to ResQuotaPlan | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/bkapp_model/migrations/0010_auto_20231127_2039.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 29 | warning | apiserver.paasng.paasng.platform.bkapp_model.migrations.0010_auto_20231127_2039 | scaling_config(%s) of obj<%s> is invalid, set it to None | string | except | 否 |
| 55 | warning | apiserver.paasng.paasng.platform.bkapp_model.migrations.0010_auto_20231127_2039 | scaling_config(%s) of obj<%s> is invalid, set it to None | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/bkapp_model/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 89 | info | apiserver.paasng.paasng.platform.bkapp_model.views | access control only supported in te region, skip... | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/declarative/application/controller.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 170 | info | apiserver.paasng.paasng.platform.declarative.application.controller | Module named "%s" already exists, skip create! | string | if | 否 |
| 225 | info | apiserver.paasng.paasng.platform.declarative.application.controller | Switching default module for application[{application.code}], {old_default_modul... | fstring | function | 否 |
| 301 | warning | apiserver.paasng.paasng.platform.declarative.application.controller | Skip binding, service called "%s" not found | string | except | 否 |
| 307 | info | apiserver.paasng.paasng.platform.declarative.application.controller | Skip, service "%s" already created shared attachment | string | if | 否 |
| 314 | info | apiserver.paasng.paasng.platform.declarative.application.controller | Skip, service "%s" already bound | string | if | 否 |
| 317 | info | apiserver.paasng.paasng.platform.declarative.application.controller | Bind service "%s" to Module "%s". | string | else | 否 |




---


### 文件: apiserver/paasng/paasng/platform/declarative/application/fields.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 45 | warning | apiserver.paasng.paasng.platform.declarative.application.fields | 应用<%s> 的中文名将从 '%s' 修改成 '%s' | string | if | 否 |
| 52 | warning | apiserver.paasng.paasng.platform.declarative.application.fields | 应用<%s> 的英文名将从 '%s' 修改成 '%s' | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/declarative/deployment/svc_disc.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 114 | info | apiserver.paasng.paasng.platform.declarative.deployment.svc_disc | Module not found in system, no cluster for %s | string | else | 否 |




---


### 文件: apiserver/paasng/paasng/platform/declarative/utils.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 39 | debug | apiserver.paasng.paasng.platform.declarative.utils | unknown ResQuotaPlan value `%s`, try to convert ProcessSpecPlan to ResQuotaPlan | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/configurations/config_var.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 370 | warning | apiserver.paasng.paasng.platform.engine.configurations.config_var | {key}={envs[key]} is already defined in default builtin envs, will be overwritte... | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/configurations/source_file.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 176 | info | apiserver.paasng.paasng.platform.engine.configurations.source_file | Failed to read file, location: %s, unexpected error: %s. | string | except | 否 |
| 211 | debug | apiserver.paasng.paasng.platform.engine.configurations.source_file | [sourcectl] reading file from %s, version<%s> | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/bg_build/bg_build.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 71 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_build.bg_build | deployment %s, build process %s use bk_ci pipeline to build image | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/bg_build/executors.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 112 | exception | apiserver.paasng.paasng.platform.engine.deploy.bg_build.executors | builder pod did not reach the target status within the timeout period during dep... | fstring | except | 否 |
| 136 | exception | apiserver.paasng.paasng.platform.engine.deploy.bg_build.executors | builder pod exit not succeeded during deploy[{self.bp}] | fstring | else | 否 |
| 141 | exception | apiserver.paasng.paasng.platform.engine.deploy.bg_build.executors | A critical error happened during deploy[{self.bp}] | fstring | except | 否 |
| 158 | warning | apiserver.paasng.paasng.platform.engine.deploy.bg_build.executors | failed to watch build logs for App: %s | string | except | 否 |
| 186 | exception | apiserver.paasng.paasng.platform.engine.deploy.bg_build.executors | Duplicate slug-builder Pod exists | string | except | 否 |
| 190 | debug | apiserver.paasng.paasng.platform.engine.deploy.bg_build.executors | SlugBuilder created: %s | string | function | 否 |
| 237 | warning | apiserver.paasng.paasng.platform.engine.deploy.bg_build.executors | 清理应用 %s 的 slug builder 失败, 原因: %s | string | except | 否 |
| 289 | exception | apiserver.paasng.paasng.platform.engine.deploy.bg_build.executors | call bk_ci pipeline failed during deploy[{self.bp}] | fstring | except | 否 |
| 299 | exception | apiserver.paasng.paasng.platform.engine.deploy.bg_build.executors | critical error happened during deploy[{self.bp}] | fstring | except | 否 |
| 344 | exception | apiserver.paasng.paasng.platform.engine.deploy.bg_build.executors | call bk_ci pipeline for build status and logs failed during deploy[{self.bp}] | fstring | except | 否 |
| 353 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_build.executors | break poll loop with pipeline build status: %s | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/bg_build/utils.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 178 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_build.utils | build wl_app<{app.name}> with slugbuilder<{image}> | fstring | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/bg_command/bkapp_hook.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 86 | exception | apiserver.paasng.paasng.platform.engine.deploy.bg_command.bkapp_hook | A critical error happened during fetch logs from hook({hook_name}) | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/bg_wait/wait_bkapp.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 91 | warning | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_bkapp | Deployment was not provided for UserInterruptedPolicy, will not proceed. | string | if | 否 |
| 97 | warning | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_bkapp | Deployment not exists for UserInterruptedPolicy, will not proceed. | string | except | 否 |
| 120 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_bkapp | wait procedure started {already_waited} seconds, env: {self.env} | fstring | function | 否 |
| 125 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_bkapp | AbortPolicy: {policy_name} evaluated, got positive result, abort current procedu... | fstring | if | 否 |
| 224 | warning | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_bkapp | Error polling AppModelDeploy status, result: %s | string | if | 否 |
| 228 | warning | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_bkapp | polling AppModelDeploy is interrupted | string | if | 否 |
| 232 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_bkapp | Update AppModelDeploy status with data: %s | string | else | 否 |
| 247 | debug | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_bkapp | Step not found or duplicated, name: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/bg_wait/wait_deployment.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 123 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_deployment | wait procedure started {already_waited} seconds, env: {self.env} | fstring | function | 否 |
| 128 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_deployment | AbortPolicy: {policy_name} evaluated, got positive result, abort current procedu... | fstring | if | 否 |
| 171 | warning | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_deployment | Failed to get last processes, error: %s | string | except | 否 |
| 229 | warning | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_deployment | Deployment was not provided for UserInterruptedPolicy, will not proceed. | string | if | 否 |
| 235 | warning | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_deployment | Deployment not exists for UserInterruptedPolicy, will not proceed. | string | except | 否 |
| 250 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_deployment | Process {process.type} still have {count} instances | fstring | if | 否 |
| 253 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_deployment | No instances found, all processes has been stopped for env: {self.env} | fstring | function | 否 |
| 271 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_deployment | Process {process.type} was not updated to {self.release_version}, env: {self.env... | fstring | if | 否 |
| 274 | info | apiserver.paasng.paasng.platform.engine.deploy.bg_wait.wait_deployment | All processes has been updated to {self.release_version}, env: {self.env} | fstring | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/building.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 131 | info | apiserver.paasng.paasng.platform.engine.deploy.building | Uploading source files to {source_destination_path} | fstring | with | 否 |
| 164 | exception | apiserver.paasng.paasng.platform.engine.deploy.building | Error while handling app description file, deployment: %s. | string | except | 否 |
| 436 | warning | apiserver.paasng.paasng.platform.engine.deploy.building | Polling status of build process [%s] timed out, consider it failed, deployment: ... | string | if | 否 |
| 447 | info | apiserver.paasng.paasng.platform.engine.deploy.building | The status of build process [%s] is "%s", deployment: %s, build_id: %s | string | function | 否 |
| 465 | info | apiserver.paasng.paasng.platform.engine.deploy.building | Update deployment steps by log lines, deployment: %s | string | function | 否 |
| 472 | info | apiserver.paasng.paasng.platform.engine.deploy.building | Finished updating deployment steps, deployment: %s, cost: %s | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/image_release.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 144 | exception | apiserver.paasng.paasng.platform.engine.deploy.image_release | Error while handling s-mart app description file, deployment: %s. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/release/legacy.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 81 | debug | apiserver.paasng.paasng.platform.engine.deploy.release.legacy | Step not found or duplicated, name: %s | string | except | 否 |
| 98 | debug | apiserver.paasng.paasng.platform.engine.deploy.release.legacy | Step not found or duplicated, name: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/release/operator.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 81 | debug | apiserver.paasng.paasng.platform.engine.deploy.release.operator | Step not found or duplicated, name: %s | string | except | 否 |
| 124 | warning | apiserver.paasng.paasng.platform.engine.deploy.release.operator | Name conflicts when creating new AppModelDeploy object, name: %s. | string | except | 否 |
| 205 | exception | apiserver.paasng.paasng.platform.engine.deploy.release.operator | An error occur when creating BkLogConfig | string | except | 否 |
| 213 | exception | apiserver.paasng.paasng.platform.engine.deploy.release.operator | An error occur when sync ServiceMonitor | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/start.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 117 | debug | apiserver.paasng.paasng.platform.engine.deploy.start | Starting new deployment: %s for Module: %s... | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/deploy/version.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 43 | debug | apiserver.paasng.paasng.platform.engine.deploy.version | Module: %s Env: %s is not deployed | string | if | 否 |
| 47 | debug | apiserver.paasng.paasng.platform.engine.deploy.version | Module: %s Env: %s has been offline | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/handlers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 68 | info | apiserver.paasng.paasng.platform.engine.handlers | steps of engine_app<%s>'s phase<%s> is outdated, rebuilt... | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/management/commands/deploy_bkapp.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 74 | exception | commands | command error. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/management/commands/inject_engineapp_metadata.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 33 | info | apiserver.paasng.paasng.platform.engine.management.commands.inject_engineapp_metadata | Going to update all meta info... | string | function | 否 |
| 46 | exception | apiserver.paasng.paasng.platform.engine.management.commands.inject_engineapp_metadata | unable to get engine_app for %s:%s | string | except | 否 |
| 55 | info | apiserver.paasng.paasng.platform.engine.management.commands.inject_engineapp_metadata | update metadata{engine_app_meta_info} successful | fstring | try | 否 |
| 57 | exception | apiserver.paasng.paasng.platform.engine.management.commands.inject_engineapp_metadata | update meta info failed | string | except | 否 |
| 62 | info | apiserver.paasng.paasng.platform.engine.management.commands.inject_engineapp_metadata | update done. %s updated, %s failed %s skip. | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/management/commands/update_operations_pending_status.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 64 | info | apiserver.paasng.paasng.platform.engine.management.commands.update_operations_pending_status | DRY-RUN: 
 | string | if | 否 |
| 68 | info | apiserver.paasng.paasng.platform.engine.management.commands.update_operations_pending_status | going to update type<%s> count<%s> | string | function | 否 |
| 79 | info | apiserver.paasng.paasng.platform.engine.management.commands.update_operations_pending_status | update type<%s> done | string | try | 否 |
| 81 | exception | apiserver.paasng.paasng.platform.engine.management.commands.update_operations_pending_status | update type<%s> failed | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/models/deployment.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 151 | info | apiserver.paasng.paasng.platform.engine.models.deployment | update_fields, deployment_id: %s, fields: %s | string | function | 否 |
| 172 | info | apiserver.paasng.paasng.platform.engine.models.deployment | update_release {total_seconds} | fstring | if | 否 |
| 192 | warning | apiserver.paasng.paasng.platform.engine.models.deployment | Unsupported absolute path<%s>, force transform to relative_to path. | string | if | 否 |
| 214 | warning | apiserver.paasng.paasng.platform.engine.models.deployment | failed to get PREPARATION start time from deployment<%s> | string | except | 否 |
| 229 | warning | apiserver.paasng.paasng.platform.engine.models.deployment | failed to get complete status from deployment<%s> | string | except | 否 |
| 243 | warning | apiserver.paasng.paasng.platform.engine.models.deployment | failed to get complete status from deployment<%s> | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/models/managers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 140 | debug | apiserver.paasng.paasng.platform.engine.models.managers | Can't find existed config var. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/monitoring.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 46 | info | apiserver.paasng.paasng.platform.engine.monitoring | 'Start counting frozen deployments since {}'.format(edge_date.format()) | format | function | 否 |
| 52 | info | apiserver.paasng.paasng.platform.engine.monitoring | 'Frozen deployments count: {}'.format(frozen_deployments_cnt) | format | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/phases_steps/phases.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 67 | debug | apiserver.paasng.paasng.platform.engine.phases_steps.phases | choosing step set<%s>... | string | function | 否 |
| 92 | exception | apiserver.paasng.paasng.platform.engine.phases_steps.phases | failed to pick step set | string | except | 否 |
| 114 | warning | apiserver.paasng.paasng.platform.engine.phases_steps.phases | %s: step of deployment in page may stay empty | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/phases_steps/steps.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 109 | debug | root | Step not found or duplicated, name: %s | string | except | 否 |
| 116 | info | root | [%s] going to mark & write to stream | string | for | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/processes/handlers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 51 | debug | apiserver.paasng.paasng.platform.engine.processes.handlers | Render message for process update event: %s | string | for | 否 |
| 55 | exception | apiserver.paasng.paasng.platform.engine.processes.handlers | unable to render process event: {event} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/utils/source.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 288 | warning | apiserver.paasng.paasng.platform.engine.utils.source | The source_dir in deployment description is different from the one in deployment... | string | if | 否 |
| 302 | info | apiserver.paasng.paasng.platform.engine.utils.source | Skip Procfile patching for Dockerfile cnative application. | string | if | 否 |
| 306 | warning | apiserver.paasng.paasng.platform.engine.utils.source | skip the source patching process: %s | string | if | 否 |
| 323 | error | apiserver.paasng.paasng.platform.engine.utils.source | Engine app {engine_app.name}'s source is too big, size={size} | fstring | if | 否 |
| 332 | info | root | Tagging module[{module.pk}]: {tags} | fstring | try | 否 |
| 335 | exception | apiserver.paasng.paasng.platform.engine.utils.source | Unable to tagging module | string | except | 否 |
| 365 | info | apiserver.paasng.paasng.platform.engine.utils.source | Uploading source files to {source_destination_path} | fstring | with | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/views/deploy.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 189 | debug | apiserver.paasng.paasng.platform.engine.views.deploy | The current source code system does not support parsing the version unique ID fr... | string | except | 否 |
| 193 | exception | apiserver.paasng.paasng.platform.engine.views.deploy | Failed to parse version information. | string | except | 否 |
| 208 | exception | apiserver.paasng.paasng.platform.engine.views.deploy | Deploy request exception, please try again later | string | function | 否 |
| 324 | exception | apiserver.paasng.paasng.platform.engine.views.deploy | failed to get phase info | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/views/misc.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 102 | exception | apiserver.paasng.paasng.platform.engine.views.misc | app offline error | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/engine/workflow/flow.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 110 | exception | apiserver.paasng.paasng.platform.engine.workflow.flow | `msg` | string | if | 否 |
| 124 | debug | apiserver.paasng.paasng.platform.engine.workflow.flow | trying to get step by title<%s> | string | function | 否 |
| 128 | info | apiserver.paasng.paasng.platform.engine.workflow.flow | %s, skip | string | except | 否 |
| 190 | warning | apiserver.paasng.paasng.platform.engine.workflow.flow | Failed to release the deployment lock: %s | string | except | 否 |
| 345 | exception | apiserver.paasng.paasng.platform.engine.workflow.flow | A critical error happened during deploy[{deployment.pk}] | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/evaluation/collectors/resource.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 183 | warning | apiserver.paasng.paasng.platform.evaluation.collectors.resource | failed to get env {env} process metrics: {e} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/evaluation/collectors/user_visit.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 85 | exception | apiserver.paasng.paasng.platform.evaluation.collectors.user_visit | failed to get app %s module %s env %s pv & uv | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/evaluation/notifiers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 47 | info | apiserver.paasng.paasng.platform.evaluation.notifiers | no issue reports, skip notification... | string | if | 否 |
| 51 | warning | apiserver.paasng.paasng.platform.evaluation.notifiers | not receivers, skip notification... | string | if | 否 |
| 65 | info | apiserver.paasng.paasng.platform.evaluation.notifiers | no title or content, skip notification... | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/evaluation/tasks.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 146 | exception | apiserver.paasng.paasng.platform.evaluation.tasks | failed to collect app: %s operation report | string | except | 否 |
| 178 | info | apiserver.paasng.paasng.platform.evaluation.tasks | no idle app reports, skip current notification task | string | if | 否 |
| 212 | info | apiserver.paasng.paasng.platform.evaluation.tasks | no idle app reports, skip notification to %s | string | if | 否 |
| 219 | exception | apiserver.paasng.paasng.platform.evaluation.tasks | failed to send idle module envs email to %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/base.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 85 | exception | apiserver.paasng.paasng.platform.mgrlegacy.app_migrations.base | Apply %s failed. | string | except | 否 |
| 94 | critical | apiserver.paasng.paasng.platform.mgrlegacy.app_migrations.base | rollback app for LApplication[%s] is None 
 %s | string | if | 否 |
| 108 | exception | apiserver.paasng.paasng.platform.mgrlegacy.app_migrations.base | Apply %s %s failed. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/service.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 57 | warning | apiserver.paasng.paasng.platform.mgrlegacy.app_migrations.service | support {service_name} to migrate | fstring | if | 否 |
| 70 | debug | apiserver.paasng.paasng.platform.mgrlegacy.app_migrations.service | service_attachment for application:%s not exists! | string | except | 否 |
| 141 | warning | apiserver.paasng.paasng.platform.mgrlegacy.app_migrations.service | service rollback delete service_attachment delete fail | string | except | 否 |
| 283 | warning | apiserver.paasng.paasng.platform.mgrlegacy.app_migrations.service | 无法绑定至合适的 plan | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/sourcectl.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 48 | warning | apiserver.paasng.paasng.platform.mgrlegacy.app_migrations.sourcectl | app_secure_info module not found, skip migrate process. | string | if | 否 |
| 74 | warning | apiserver.paasng.paasng.platform.mgrlegacy.app_migrations.sourcectl | repo_type({secure_info.vcs_type}) not supported, skip migrate process. | fstring | else | 否 |




---


### 文件: apiserver/paasng/paasng/platform/mgrlegacy/cnative_migrations/base.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 72 | exception | apiserver.paasng.paasng.platform.mgrlegacy.cnative_migrations.base | migration_process(id={self.migration_process.id}) rollback failed | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/mgrlegacy/legacy_proxy.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 151 | exception | apiserver.paasng.paasng.platform.mgrlegacy.legacy_proxy | 从旧版本Paas获取应用Logo失败. | string | except | 否 |
| 153 | info | apiserver.paasng.paasng.platform.mgrlegacy.legacy_proxy | 尝试返回默认logo | string | function | 否 |
| 160 | exception | apiserver.paasng.paasng.platform.mgrlegacy.legacy_proxy | 从旧版本Paas获取应用默认Logo失败. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/mgrlegacy/migrate.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 57 | info | apiserver.paasng.paasng.platform.mgrlegacy.migrate | Skip migration %s... | string | if | 否 |
| 61 | info | apiserver.paasng.paasng.platform.mgrlegacy.migrate | Start migration %s for %s | string | function | 否 |
| 65 | exception | apiserver.paasng.paasng.platform.mgrlegacy.migrate | Error when running migration, %s | string | except | 否 |
| 97 | info | apiserver.paasng.paasng.platform.mgrlegacy.migrate | Skip migration %s... | string | if | 否 |
| 129 | info | apiserver.paasng.paasng.platform.mgrlegacy.migrate | Start rollback %s for %s | string | function | 否 |
| 133 | exception | apiserver.paasng.paasng.platform.mgrlegacy.migrate | rollback fail! | string | except | 否 |
| 149 | critical | apiserver.paasng.paasng.platform.mgrlegacy.migrate | rollback app for %s is None 
 %s | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/mgrlegacy/tasks.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 52 | exception | apiserver.paasng.paasng.platform.mgrlegacy.tasks | run_migration failed: migration_process_id=%s | string | except | 否 |
| 53 | info | apiserver.paasng.paasng.platform.mgrlegacy.tasks | auto to rollback: migration_process_id=%s | string | except | 否 |
| 57 | exception | apiserver.paasng.paasng.platform.mgrlegacy.tasks | run_rollback failed | string | except | 否 |
| 73 | exception | apiserver.paasng.paasng.platform.mgrlegacy.tasks | run_rollback failed: migration_process_id=%s | string | except | 否 |
| 90 | exception | apiserver.paasng.paasng.platform.mgrlegacy.tasks | run migration confirmed failed: migration_process_id=%s | string | except | 否 |
| 111 | exception | apiserver.paasng.paasng.platform.mgrlegacy.tasks | backup entrances failed: migration_process_id=%s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/mgrlegacy/utils.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 233 | warning | apiserver.paasng.paasng.platform.mgrlegacy.utils | Get mgrlegacy target cluster failed, return default instead, region: %s. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/modules/helpers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 265 | warning | apiserver.paasng.paasng.platform.modules.helpers | failed to get slug runner, maybe not bind | string | except | 否 |
| 268 | warning | apiserver.paasng.paasng.platform.modules.helpers | failed to get right runner and right label | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/modules/management/commands/push_smart_image.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 45 | warning | apiserver.paasng.paasng.platform.modules.management.commands.push_smart_image | SSL certificate verification is disabled. This should only be used with trusted ... | string | if | 否 |
| 101 | warning | apiserver.paasng.paasng.platform.modules.management.commands.push_smart_image | Skipped the step of pushing S-Mart base image to bkrepo! | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/modules/manager.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 174 | info | apiserver.paasng.paasng.platform.modules.manager | Skip initializing template for application:<%s>/<%s> | string | if | 否 |
| 247 | warning | apiserver.paasng.paasng.platform.modules.manager | skip runtime binding because default image is not found | string | except | 否 |
| 338 | exception | apiserver.paasng.paasng.platform.modules.manager | An exception occurred during `%s` | string | except | 否 |
| 450 | info | apiserver.paasng.paasng.platform.modules.manager | going to delete services related to Module<%s> | string | function | 否 |
| 453 | info | apiserver.paasng.paasng.platform.modules.manager | going to delete EngineApp related to Module<%s> | string | function | 否 |
| 457 | info | apiserver.paasng.paasng.platform.modules.manager | going to delete Module<%s> | string | function | 否 |
| 471 | info | apiserver.paasng.paasng.platform.modules.manager | service<{rel.db_obj.service_id}-{rel.db_obj.service_instance_id}> deleted.  | fstring | for | 否 |
| 528 | exception | apiserver.paasng.paasng.platform.modules.manager | 应用<%s>获取预设增强服务<%s>失败 | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/modules/models/runtime.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 49 | debug | apiserver.paasng.paasng.platform.modules.models.runtime | module %s 未初始化 BuildConfig | string | except | 否 |
| 122 | debug | apiserver.paasng.paasng.platform.modules.models.runtime | module %s 未初始化 BuildConfig | string | except | 否 |
| 219 | warning | apiserver.paasng.paasng.platform.modules.models.runtime | Unable to get default image for region: %s, will use %s by default | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/modules/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 203 | exception | apiserver.paasng.paasng.platform.modules.views | unable to clean module<%s> of application<%s> related resources | string | except | 否 |
| 258 | info | apiserver.paasng.paasng.platform.modules.views | Switching default module for application[{application.code}], {default_module.na... | fstring | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/scene_app/initializer.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 76 | exception | apiserver.paasng.paasng.platform.scene_app.initializer | _('加载应用描述文件失败') | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/scheduler/jobs.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 34 | debug | apiserver.paasng.paasng.platform.scheduler.jobs | Start updating remote services... | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/scheduler/management/commands/run_scheduler.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 29 | info | apiserver.paasng.paasng.platform.scheduler.management.commands.run_scheduler | shutdowning scheduler | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/smart_app/management/commands/smart_tool.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 50 | exception | commands | command error | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/smart_app/services/detector.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 96 | warning | apiserver.paasng.paasng.platform.smart_app.services.detector | Unable to list contents in the package file, path: %s. | string | except | 否 |
| 111 | warning | apiserver.paasng.paasng.platform.smart_app.services.detector | Invalid relative path detected: %s | string | if | 否 |
| 121 | exception | apiserver.paasng.paasng.platform.smart_app.services.detector | _('应用描述文件内容不是有效 YAML 格式') | string | except | 否 |
| 138 | warning | apiserver.paasng.paasng.platform.smart_app.services.detector | failed to extract version from app_desc, detail: %s | string | except | 否 |
| 159 | debug | apiserver.paasng.paasng.platform.smart_app.services.detector | parsing source package's stats object. | string | function | 否 |
| 185 | info | apiserver.paasng.paasng.platform.smart_app.services.detector | The logo.png does not exist, using default logo. | string | except | 否 |
| 187 | exception | apiserver.paasng.paasng.platform.smart_app.services.detector | Can't read logo.png. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/smart_app/services/dispatch.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 91 | debug | apiserver.paasng.paasng.platform.smart_app.services.dispatch | Patching module for module '%s' | string | function | 否 |
| 111 | debug | apiserver.paasng.paasng.platform.smart_app.services.dispatch | dispatching slug-image for module '%s', working at '%s' | string | function | 否 |
| 133 | debug | apiserver.paasng.paasng.platform.smart_app.services.dispatch | Start pushing Image. | string | function | 否 |
| 150 | debug | apiserver.paasng.paasng.platform.smart_app.services.dispatch | dispatching cnb-image for module '%s', working at '%s' | string | function | 否 |
| 184 | debug | apiserver.paasng.paasng.platform.smart_app.services.dispatch | Start pushing Image. | string | with | 否 |




---


### 文件: apiserver/paasng/paasng/platform/smart_app/services/patcher.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 65 | warning | apiserver.paasng.paasng.platform.smart_app.services.patcher | skip patching for adding Procfile: %s | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/smart_app/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 110 | debug | apiserver.paasng.paasng.platform.smart_app.views | [S-Mart] fetching remote services by region. | string | function | 否 |
| 135 | exception | apiserver.paasng.paasng.platform.smart_app.views | S-Mart package does not exist! | string | except | 否 |
| 152 | exception | apiserver.paasng.paasng.platform.smart_app.views | Create app error ! | string | except | 否 |
| 166 | exception | apiserver.paasng.paasng.platform.smart_app.views | Handling S-Mart Package Exceptions! | string | except | 否 |
| 169 | exception | apiserver.paasng.paasng.platform.smart_app.views | Failed to access container registry! | string | except | 否 |
| 289 | exception | apiserver.paasng.paasng.platform.smart_app.views | S-Mart package does not exist！ | string | except | 否 |
| 294 | error | apiserver.paasng.paasng.platform.smart_app.views | the provided digital signature is inconsistent with the digital signature of the... | string | if | 否 |
| 307 | exception | apiserver.paasng.paasng.platform.smart_app.views | Failed to update app info！ | string | except | 否 |
| 320 | exception | apiserver.paasng.paasng.platform.smart_app.views | Handling S-Mart Package Exceptions! | string | except | 否 |
| 323 | exception | apiserver.paasng.paasng.platform.smart_app.views | Failed to access container registry! | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 169 | warning | apiserver.paasng.paasng.platform.sourcectl.client | get url `{raw_resp.url}` but 404 | fstring | if | 否 |
| 172 | warning | apiserver.paasng.paasng.platform.sourcectl.client | get url `{raw_resp.url}` but 401 | fstring | if | 否 |
| 175 | warning | root | get url `{raw_resp.url}` but 403 | fstring | if | 否 |
| 178 | warning | root | get url `{raw_resp.url}` but 504 | fstring | if | 否 |
| 181 | warning | root | get url `{raw_resp.url}` but {raw_resp.status_code}, raw resp: {raw_resp} | fstring | if | 否 |
| 199 | info | apiserver.paasng.paasng.platform.sourcectl.client | try to refresh token for {holder.user.username} | fstring | function | 是 |
| 203 | error | apiserver.paasng.paasng.platform.sourcectl.client | failed to refresh token for {holder.user.username} | fstring | except | 是 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/connector.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 84 | exception | apiserver.paasng.paasng.platform.sourcectl.connector | unable to render app source template %s | string | except | 否 |
| 260 | debug | apiserver.paasng.paasng.platform.sourcectl.connector | Creating basic auth of repo<%s> | string | if | 否 |
| 311 | debug | apiserver.paasng.paasng.platform.sourcectl.connector | compressing templated source, key=%s... | string | with | 否 |
| 363 | exception | apiserver.paasng.paasng.platform.sourcectl.connector | unable to render app source template %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/controllers/bare_git.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 64 | warning | apiserver.paasng.paasng.platform.sourcectl.controllers.bare_git | repo<%s> has no basic auth, maybe missing | string | except | 否 |
| 88 | exception | apiserver.paasng.paasng.platform.sourcectl.controllers.bare_git | Failed to access the remote git repo, command error. | string | except | 否 |
| 91 | exception | apiserver.paasng.paasng.platform.sourcectl.controllers.bare_git | Failed to access the remote git repo, reason unknown. | string | except | 否 |
| 138 | debug | apiserver.paasng.paasng.platform.sourcectl.controllers.bare_git | version_name: %s, revision: %s | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/controllers/bare_svn.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 47 | warning | apiserver.paasng.paasng.platform.sourcectl.controllers.bare_svn | repo<%s> has no basic auth, maybe missing | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/controllers/bk_svn.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 70 | exception | apiserver.paasng.paasng.platform.sourcectl.controllers.bk_svn | Unable to list alternative versions for {self.repo_url} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/controllers/docker.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 54 | warning | apiserver.paasng.paasng.platform.sourcectl.controllers.docker | repo is missing `registry` part, using `default_registry` as endpoint | string | if | 否 |
| 77 | warning | apiserver.paasng.paasng.platform.sourcectl.controllers.docker | repo does not contain namespace, guess it as `library` | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/controllers/gitee.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 153 | exception | apiserver.paasng.paasng.platform.sourcectl.controllers.gitee | Can't get username from gitee, use namespace as fallback(only work for personal ... | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/controllers/github.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 95 | info | apiserver.paasng.paasng.platform.sourcectl.controllers.github | copy dir %s's content to dir %s during export github repo | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/controllers/package.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 57 | debug | apiserver.paasng.paasng.platform.sourcectl.controllers.package | [sourcectl] export files to %s, version<%s> | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/git/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 199 | warning | apiserver.paasng.paasng.platform.sourcectl.git.client | Failed to parse git branch from ls-remote output, line: "%s" | string | except | 否 |
| 234 | warning | apiserver.paasng.paasng.platform.sourcectl.git.client | failed to get commit info from %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/management/commands/clean_source_package.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 59 | info | apiserver.paasng.paasng.platform.sourcectl.management.commands.clean_source_package | APP %s module %s delete %s source packages | string | for | 否 |
| 69 | info | apiserver.paasng.paasng.platform.sourcectl.management.commands.clean_source_package | About to clean up the source package %s | string | for | 否 |
| 76 | info | apiserver.paasng.paasng.platform.sourcectl.management.commands.clean_source_package | Cleaned up source package %s, reclaimed %s bytes successfully. | string | if | 否 |
| 82 | info | apiserver.paasng.paasng.platform.sourcectl.management.commands.clean_source_package | [dry-run] %s bytes will be reclaimed after cleaning the source package %s. | string | else | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/migrations/0007_init_source_type_specs.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 29 | info | apiserver.paasng.paasng.platform.sourcectl.migrations.0007_init_source_type_specs | 初始化 BareGit 代码库配置 | string | function | 否 |
| 35 | info | apiserver.paasng.paasng.platform.sourcectl.migrations.0007_init_source_type_specs | 初始化 BareSVN 代码库配置 | string | function | 否 |
| 40 | info | apiserver.paasng.paasng.platform.sourcectl.migrations.0007_init_source_type_specs | 初始化代码库配置完成 | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/migrations/0009_encrypt_client_secret_in_db.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 35 | info | apiserver.paasng.paasng.platform.sourcectl.migrations.0009_encrypt_client_secret_in_db | start encrypt client secret in database... | string | function | 是 |
| 40 | info | apiserver.paasng.paasng.platform.sourcectl.migrations.0009_encrypt_client_secret_in_db | client secret encrypt done! | string | function | 是 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/models.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 206 | exception | apiserver.paasng.paasng.platform.sourcectl.models | failed to parse %s for getting alias name | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/models_utils.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 48 | warning | apiserver.paasng.paasng.platform.sourcectl.models_utils | Can't get source obj from %s | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/package/cleaner.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 35 | info | apiserver.paasng.paasng.platform.sourcectl.package.cleaner | Removing source packages %s | string | function | 否 |
| 42 | exception | apiserver.paasng.paasng.platform.sourcectl.package.cleaner | Source package %s failed to delete! | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/package/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 346 | exception | apiserver.paasng.paasng.platform.sourcectl.package.client | Can't handle a tar/zip file from remote path: {url} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/package/downloader.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 46 | debug | apiserver.paasng.paasng.platform.sourcectl.package.downloader | [sourcectl] downloading file via url<%s> to local_path<%s> | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/package/uploader.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 51 | debug | apiserver.paasng.paasng.platform.sourcectl.package.uploader | [BlobStore] uploading %s to BlobStore[%s] | string | function | 否 |
| 93 | warning | apiserver.paasng.paasng.platform.sourcectl.package.uploader | The version information parsed from the source package will be overwritten | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/source_types.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 114 | warning | apiserver.paasng.paasng.platform.sourcectl.source_types | The 'oauth_credentials' will be removed in the next version. | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/svn/admin.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 98 | warning | apiserver.paasng.paasng.platform.sourcectl.svn.admin | No bk svn sourcectl was configured | string | except | 否 |
| 109 | critical | apiserver.paasng.paasng.platform.sourcectl.svn.admin | response.content | string | if | 否 |
| 331 | debug | apiserver.paasng.paasng.platform.sourcectl.svn.admin | 'SvnAuthClient4Developer: mock call {func_name} with: ({args}, {kwargs})'.format... | format | function | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/svn/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 141 | info | apiserver.paasng.paasng.platform.sourcectl.svn.client | Skip init, %s already exists in svn server. | string | try | 否 |
| 455 | exception | apiserver.paasng.paasng.platform.sourcectl.svn.client | SVN add error | string | except | 否 |
| 467 | exception | apiserver.paasng.paasng.platform.sourcectl.svn.client | SVN update error | string | except | 否 |
| 490 | exception | apiserver.paasng.paasng.platform.sourcectl.svn.client | SVN delete error | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/utils.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 185 | debug | apiserver.paasng.paasng.platform.sourcectl.utils | Generating temp path: %s | string | try | 否 |
| 199 | debug | apiserver.paasng.paasng.platform.sourcectl.utils | Generating temp path: %s | string | try | 否 |




---


### 文件: apiserver/paasng/paasng/platform/sourcectl/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 223 | debug | apiserver.paasng.paasng.platform.sourcectl.views | User is not bound to token_holder of type: {source_control_type}, detail: TokenH... | fstring | except | 否 |
| 235 | exception | apiserver.paasng.paasng.platform.sourcectl.views | Unknown error occurred when getting repo list, user_id: %s, sourcectl_type: %s | string | except | 否 |
| 387 | exception | apiserver.paasng.paasng.platform.sourcectl.views | Fail to bind repo | string | except | 否 |
| 446 | exception | apiserver.paasng.paasng.platform.sourcectl.views | unable to fetch repo info, may be the credential error or a network exception. | string | except | 否 |
| 516 | exception | apiserver.paasng.paasng.platform.sourcectl.views | Unknown error occurred when getting compare url, user_id: %s | string | except | 否 |
| 546 | exception | apiserver.paasng.paasng.platform.sourcectl.views | App: %s, module: %s create svn tag error | string | except | 否 |
| 581 | exception | apiserver.paasng.paasng.platform.sourcectl.views | Unknown error occurred when inspecting version, user_id: %s, version: %s | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/templates/command.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 89 | debug | apiserver.paasng.paasng.platform.templates.command | File {rel_dst_filename} should be executable, change its attributes | fstring | if | 否 |




---


### 文件: apiserver/paasng/paasng/platform/templates/manager.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 48 | warning | apiserver.paasng.paasng.platform.templates.manager | default image is not found | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/platform/templates/templater.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 83 | debug | apiserver.paasng.paasng.platform.templates.templater | checkout template from [%s: %s] | string | function | 否 |
| 93 | warning | apiserver.paasng.paasng.platform.templates.templater | unknown protocol type: %s, url: %s | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/utils/api_middleware.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 57 | warning | apiserver.paasng.paasng.utils.api_middleware | api<{request.path}> resolve failed | fstring | except | 否 |
| 67 | warning | apiserver.paasng.paasng.utils.api_middleware | %s api log error: %s | string | if | 否 |
| 136 | warning | apiserver.paasng.paasng.utils.api_middleware | unable to dump api log data: {e} | fstring | except | 否 |




---


### 文件: apiserver/paasng/paasng/utils/blobstore.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 123 | warning | apiserver.paasng.paasng.utils.blobstore | Error getting bucket %s, error: %s, further actions on it might fail. | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/utils/datetime.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 117 | exception | root | app_log, trans_ts_to_local fail!. [ts=%s] | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/utils/error_message.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 70 | warning | apiserver.paasng.paasng.utils.error_message | Can't get error code from Exception<%s> | string | function | 否 |




---


### 文件: apiserver/paasng/paasng/utils/es_log/misc.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 107 | warning | apiserver.paasng.paasng.utils.es_log.misc | Field<%s> got an unhashable value: %s | string | except | 否 |
| 161 | debug | apiserver.paasng.paasng.utils.es_log.misc | some indexes is invalid, %s | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/utils/i18n/migrate.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 62 | info | apiserver.paasng.paasng.utils.i18n.migrate | Chunk<%d/%d> is updating | string | for | 否 |




---


### 文件: apiserver/paasng/paasng/utils/logging.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 50 | exception | console | LogstashRedisHandler push to redis error | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/utils/middlewares.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 90 | warning | apiserver.paasng.paasng.utils.middlewares | The language %s is not supported.  | string | except | 否 |




---


### 文件: apiserver/paasng/paasng/utils/notification_plugins.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 61 | exception | apiserver.paasng.paasng.utils.notification_plugins | request to tof failed. | string | except | 否 |
| 67 | warning | apiserver.paasng.paasng.utils.notification_plugins | 'send {method} to {receiver} failed: {code}/{reason}'.format(method=method, rece... | format | function | 否 |
| 92 | error | apiserver.paasng.paasng.utils.notification_plugins | The receivers of sending mail is empty, skipped | string | if | 否 |
| 109 | error | apiserver.paasng.paasng.utils.notification_plugins | The receivers of sending rtx is empty, skipped | string | if | 否 |
| 126 | error | apiserver.paasng.paasng.utils.notification_plugins | The receivers of sending weixin is empty, skipped | string | if | 否 |
| 143 | error | apiserver.paasng.paasng.utils.notification_plugins | The receivers of sending SMS is empty, skipped | string | if | 否 |




---


### 文件: apiserver/paasng/paasng/utils/notifier.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 45 | warning | apiserver.paasng.paasng.utils.notifier | Dummy notification backend invoked, receivers: %s | string | function | 否 |
| 89 | exception | apiserver.paasng.paasng.utils.notifier | 'sending sentry<{dsn}> failed'.format(dsn=dsn) | format | except | 否 |




---


### 文件: apiserver/paasng/paasng/utils/termcolors.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 107 | warning | apiserver.paasng.paasng.utils.termcolors | 输入不合法, 转换成黑色. | string | if | 否 |
| 124 | warning | apiserver.paasng.paasng.utils.termcolors | 输入不合法, 转换成黑色. | string | else | 否 |




---


### 文件: apiserver/paasng/paasng/utils/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 43 | exception | apiserver.paasng.paasng.utils.views | Error getting one line error from %s | string | except | 否 |
| 102 | exception | apiserver.paasng.paasng.utils.views | Unexpected OSError happened | string | if | 否 |




---


### 文件: apiserver/paasng/tests/api/test_market.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 160 | info | apiserver.paasng.tests.api.test_market | The extra attribute of the application does not exist, skip verification | string | except | 否 |
| 164 | info | apiserver.paasng.tests.api.test_market | The visiable_labels attribute of the application does not exist, skip verificati... | string | except | 否 |




---


### 文件: apiserver/paasng/tests/paas_wl/bk_app/monitoring/app_monitor/test_managers.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 103 | warning | apiserver.paasng.tests.paas_wl.bk_app.monitoring.app_monitor.test_managers | Unknown Exception raise from k8s client, but should be ignored. Detail: %s | string | except | 否 |




---


### 文件: apiserver/paasng/tests/paas_wl/conftest.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 102 | info | apiserver.paasng.tests.paas_wl.conftest | Configure CRD %s... | string | for | 否 |
| 108 | warning | apiserver.paasng.tests.paas_wl.conftest | Unknown Exception raise from k8s client, but should be ignored. Detail: %s | string | except | 否 |




---


### 文件: apiserver/paasng/tests/paasng/accessories/publish/sync_market/test_sync_console.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 80 | warning | apiserver.paasng.tests.paasng.accessories.publish.sync_market.test_sync_console | AppOpsManger get_ops_names not implemented , skip | string | except | 否 |
| 101 | warning | apiserver.paasng.tests.paasng.accessories.publish.sync_market.test_sync_console | AppOpsManger get_ops_names not implemented , skip | string | except | 否 |
| 121 | warning | apiserver.paasng.tests.paasng.accessories.publish.sync_market.test_sync_console | AppOpsManger get_ops_names not implemented , skip | string | except | 否 |




---


### 文件: apiserver/paasng/tests/utils/mocks/cluster.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 46 | warning | apiserver.paasng.tests.utils.mocks.cluster | No wl_app found when getting cluster, env: %s | string | except | 否 |




---


### 文件: svc-bkrepo/svc_bk_repo/monitoring/jobs.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 73 | info | svc-bkrepo.svc_bk_repo.monitoring.jobs | Scheduler should be running | string | if | 否 |
| 77 | info | svc-bkrepo.svc_bk_repo.monitoring.jobs | Start scheduler! | string | function | 否 |
| 83 | info | svc-bkrepo.svc_bk_repo.monitoring.jobs | clear scheduler.pid | string | function | 否 |
| 99 | info | svc-bkrepo.svc_bk_repo.monitoring.jobs | Starting update bkrepo quota. | string | function | 否 |
| 119 | info | svc-bkrepo.svc_bk_repo.monitoring.jobs | bkrepo quota updated. | string | function | 否 |




---


### 文件: svc-bkrepo/svc_bk_repo/vendor/actions.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 51 | warning | svc-bkrepo.svc_bk_repo.vendor.actions | unable to extend quota for {bucket}: usage too low = {quota.quota_used_rate} | fstring | if | 否 |
| 56 | warning | svc-bkrepo.svc_bk_repo.vendor.actions | unable to extend quota for {bucket}: exceeds max_size | fstring | if | 否 |




---


### 文件: svc-bkrepo/svc_bk_repo/vendor/helper.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 36 | info | svc-bkrepo.svc_bk_repo.vendor.helper | Equivalent curl command: %s | string | try | 否 |
| 43 | exception | svc-bkrepo.svc_bk_repo.vendor.helper | 未知错误, %s | string | except | 否 |




---


### 文件: svc-bkrepo/svc_bk_repo/vendor/views.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 113 | info | svc-bkrepo.svc_bk_repo.vendor.views | 仓库: %s 未配置容量配额, 无需扩容. | string | except | 否 |




---


### 文件: svc-mysql/svc_mysql/vendor/helper.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 80 | info | svc-mysql.svc_mysql.vendor.helper | Mysql 正在执行 {sql}... | fstring | with | 否 |
| 87 | exception | svc-mysql.svc_mysql.vendor.helper | MySQL 执行 % 失败 | string | except | 否 |
| 102 | exception | svc-mysql.svc_mysql.vendor.helper | MySQL创建连接失败: {(self.user, self.password, self.name)} | fstring | if | 是 |
| 104 | exception | svc-mysql.svc_mysql.vendor.helper | 未知数据库异常: %s | string | except | 否 |
| 131 | info | svc-mysql.svc_mysql.vendor.helper | Grant privileges to user<%s> | string | function | 否 |
| 145 | info | svc-mysql.svc_mysql.vendor.helper | Mysql 正在执行 `{create_user_sql.replace(password, '******')}`... | fstring | for | 是 |
| 154 | info | svc-mysql.svc_mysql.vendor.helper | Mysql 正在执行 `{grant_sql}`... | fstring | for | 否 |
| 156 | info | svc-mysql.svc_mysql.vendor.helper | Mysql 正在执行 `flush privileges;` | string | with | 否 |




---


### 文件: svc-mysql/svc_mysql/vendor/provider.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 100 | info | svc-mysql.svc_mysql.vendor.provider | start create mysql addons instance... | string | function | 否 |
| 141 | info | svc-mysql.svc_mysql.vendor.provider | create mysql addons instance %s success | string | with | 否 |
| 179 | info | svc-mysql.svc_mysql.vendor.provider | start delete mysql addons instance %s... | string | function | 否 |




---


### 文件: svc-otel/svc_otel/bkmonitorv3/client.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 79 | error | svc-otel.svc_otel.bkmonitorv3.client | Failed to create APM BK Monitor, resp:{resp} pm_name: {apm_name}, space_uid:{bk... | fstring | if | 否 |




---


### 文件: svc-otel/svc_otel/vendor/provider.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 61 | info | svc-otel.svc_otel.vendor.provider | 正在创建增强服务实例... | string | function | 否 |
| 85 | info | svc-otel.svc_otel.vendor.provider | 正在删除增强服务实例... | string | function | 否 |




---


### 文件: svc-rabbitmq/svc_rabbitmq/utils.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 31 | exception | svc-rabbitmq.svc_rabbitmq.utils | call %s with args(%r), kwargs(%r) failed: %s | string | except | 否 |




---


### 文件: svc-rabbitmq/tasks/__init__.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 41 | exception | svc-rabbitmq.tasks | `err` | string | except | 否 |




---


### 文件: svc-rabbitmq/tasks/management/commands/worker.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 61 | info | svc-rabbitmq.tasks.management.commands.worker | %s become leader | string | if | 否 |
| 64 | info | svc-rabbitmq.tasks.management.commands.worker | worker leader changed to %s | string | if | 否 |
| 68 | info | svc-rabbitmq.tasks.management.commands.worker | _('{} guarding cluster at {}').format(self.name, self.pid) | format | function | 否 |
| 71 | info | svc-rabbitmq.tasks.management.commands.worker | _('Q Cluster-{} running.').format(self.parent_pid) | format | function | 否 |




---


### 文件: svc-rabbitmq/tasks/models.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 143 | debug | svc-rabbitmq.tasks.models | prepared cron tasks %s | string | function | 否 |




---


### 文件: svc-rabbitmq/tasks/monitor.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 57 | exception | svc-rabbitmq.tasks.monitor | get metrics failed | string | except | 否 |
| 173 | debug | svc-rabbitmq.tasks.monitor | dlx queue of instance %s not found, skipped | string | if | 否 |




---


### 文件: svc-rabbitmq/tasks/scheduler.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 86 | info | svc-rabbitmq.tasks.scheduler | scheduler %s ready to handle %d cron tasks | string | function | 否 |
| 97 | exception | svc-rabbitmq.tasks.scheduler | scheduler monitor crash, dying | string | except | 否 |
| 150 | info | svc-rabbitmq.tasks.scheduler | scheduler %s:%s started, process pool: %s, master: %s | string | function | 否 |




---


### 文件: svc-rabbitmq/tasks/tasks.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 71 | info | svc-rabbitmq.tasks.tasks | checking clusters if is alive | string | function | 否 |
| 86 | debug | svc-rabbitmq.tasks.tasks | checking cluster %s if is alive | string | function | 否 |
| 92 | exception | svc-rabbitmq.tasks.tasks | `err` | string | except | 否 |
| 105 | debug | svc-rabbitmq.tasks.tasks | checking rabbitmq instance %s if is alive | string | function | 否 |
| 119 | info | svc-rabbitmq.tasks.tasks | checking instances task %s | string | function | 否 |
| 129 | exception | svc-rabbitmq.tasks.tasks | check instance %s alive failed | string | except | 否 |
| 201 | debug | svc-rabbitmq.tasks.tasks | checking rabbitmq instance %s queue status | string | function | 否 |
| 214 | exception | svc-rabbitmq.tasks.tasks | collecting queue status %s failed | string | except | 否 |
| 264 | debug | svc-rabbitmq.tasks.tasks | checking rabbitmq connections status for cluster %s | string | function | 否 |
| 307 | exception | svc-rabbitmq.tasks.tasks | check connection for cluster %s failed | string | except | 否 |
| 337 | debug | svc-rabbitmq.tasks.tasks | checking rabbitmq instance %s if is alive | string | function | 否 |




---


### 文件: svc-rabbitmq/vendor/management/commands/recovery_connections.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 40 | info | svc-rabbitmq.vendor.management.commands.recovery_connections | `msg` | string | function | 否 |




---


### 文件: svc-rabbitmq/vendor/provider.py

#### 标准库日志

| 行号 | 级别 | 日志器 | 消息 | 类型 | 代码块 | 敏感 |
|------|------|--------|------|------|--------|------|
| 270 | exception | svc-rabbitmq.vendor.provider | Failed to delete instance | string | except | 否 |
| 315 | exception | svc-rabbitmq.vendor.provider | Failed to delete instance | string | except | 否 |




---

