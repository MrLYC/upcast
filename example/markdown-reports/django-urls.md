# django-urls 扫描报告

## 元数据
- **scanner_name**: django-urls

## 概要信息
- **总数量**: 533
- **已扫描文件数**: 59
- **扫描耗时**: 643 毫秒

- **URL配置模块总数**: 59
- **URL模式总数**: 533

## 结果详情

### URL配置模块: apiserver.paasng.paas_wl.apis.admin.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| path | wl_api/platform/process_spec_plan/manage/ | paas_wl.apis.admin.views.processes.ProcessSpecPlanManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| path | wl_api/platform/process_spec_plan/ | paas_wl.apis.admin.views.processes.ProcessSpecPlanManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.process_spec_plan | 不适用 |  |
| path | wl_api/platform/process_spec_plan/id/<int:id>/ | paas_wl.apis.admin.views.processes.ProcessSpecPlanManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.process_spec_plan_by_id | 不适用 | 转换器: id:int |
| path | wl_api/regions/<str:region>/apps/<str:name>/processes/<str:process_type>/plan | paas_wl.apis.admin.views.processes.ProcessSpecManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.application.process_plan | 不适用 | 转换器: region:str, name:str, process_type:str |
| path | wl_api/regions/<str:region>/apps/<str:name>/processes/<str:process_type>/scale | paas_wl.apis.admin.views.processes.ProcessSpecManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.application.process_scale | 不适用 | 转换器: region:str, name:str, process_type:str |
| path | wl_api/regions/<str:region>/apps/<str:name>/processes/<str:process_type>/instances/<str:instance_name>/ | paas_wl.apis.admin.views.processes.ProcessInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.application.process_instance | 不适用 | 转换器: region:str, name:str, process_type:str, instance_name:str |
| path | wl_api/applications/<str:code>/domains/ | paas_wl.apis.admin.views.domain.AppDomainsViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.application.domains | 不适用 | 转换器: code:str |
| path | wl_api/applications/<str:code>/domains/<int:id>/ | paas_wl.apis.admin.views.domain.AppDomainsViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.application.domain_by_id | 不适用 | 转换器: code:str, id:int |
| path | wl_api/platform/app_certs/shared/ | paas_wl.apis.admin.views.certs.AppDomainSharedCertsViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.shared_app_certs | 不适用 |  |
| path | wl_api/platform/app_certs/shared/<str:name> | paas_wl.apis.admin.views.certs.AppDomainSharedCertsViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.shared_app_cert_by_name | 不适用 | 转换器: name:str |
| path | wl_api/applications/<str:code>/log_config/ | paas_wl.apis.admin.views.logs.AppLogConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.application.log_config | 不适用 | 转换器: code:str |
| path | wl_api/platform/clusters/ | paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.clusters | 不适用 |  |
| path | wl_api/platform/clusters/<str:cluster_name>/node_state/ | paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.cluster.node_state | 不适用 | 转换器: cluster_name:str |
| path | wl_api/platform/clusters/<str:cluster_name>/operator_info/ | paas_wl.apis.admin.views.clusters.ClusterComponentViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.cluster.operator_info | 不适用 | 转换器: cluster_name:str |
| path | wl_api/platform/clusters/<str:cluster_name>/components/ | paas_wl.apis.admin.views.clusters.ClusterComponentViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.cluster.components | 不适用 | 转换器: cluster_name:str |
| path | wl_api/platform/clusters/<str:cluster_name>/components/<str:component_name>/ | paas_wl.apis.admin.views.clusters.ClusterComponentViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.cluster.component_by_name | 不适用 | 转换器: cluster_name:str, component_name:str |
| path | wl_api/platform/clusters/<str:pk>/ | paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.cluster_by_id | 不适用 | 转换器: pk:str |
| path | wl_api/platform/clusters/<str:pk>/api_servers | paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.cluster.api_servers | 不适用 | 转换器: pk:str |
| path | wl_api/platform/clusters/<str:pk>/set_default/ | paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.cluster.set_default | 不适用 | 转换器: pk:str |
| path | wl_api/platform/clusters/<str:pk>/api_servers/<str:api_server_id> | paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else (pattern.include_module or '不适用') | wl_api.cluster.api_server_by_id | 不适用 | 转换器: pk:str, api_server_id:str |

#### 模式详情

**path**: `wl_api/platform/process_spec_plan/manage/`
- 视图: paas_wl.apis.admin.views.processes.ProcessSpecPlanManageViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/process_spec_plan/`
- 视图: paas_wl.apis.admin.views.processes.ProcessSpecPlanManageViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/process_spec_plan/id/<int:id>/`
- 视图: paas_wl.apis.admin.views.processes.ProcessSpecPlanManageViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/regions/<str:region>/apps/<str:name>/processes/<str:process_type>/plan`
- 视图: paas_wl.apis.admin.views.processes.ProcessSpecManageViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/regions/<str:region>/apps/<str:name>/processes/<str:process_type>/scale`
- 视图: paas_wl.apis.admin.views.processes.ProcessSpecManageViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/regions/<str:region>/apps/<str:name>/processes/<str:process_type>/instances/<str:instance_name>/`
- 视图: paas_wl.apis.admin.views.processes.ProcessInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/applications/<str:code>/domains/`
- 视图: paas_wl.apis.admin.views.domain.AppDomainsViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/applications/<str:code>/domains/<int:id>/`
- 视图: paas_wl.apis.admin.views.domain.AppDomainsViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/app_certs/shared/`
- 视图: paas_wl.apis.admin.views.certs.AppDomainSharedCertsViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/app_certs/shared/<str:name>`
- 视图: paas_wl.apis.admin.views.certs.AppDomainSharedCertsViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/applications/<str:code>/log_config/`
- 视图: paas_wl.apis.admin.views.logs.AppLogConfigViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/clusters/`
- 视图: paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/clusters/<str:cluster_name>/node_state/`
- 视图: paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/clusters/<str:cluster_name>/operator_info/`
- 视图: paas_wl.apis.admin.views.clusters.ClusterComponentViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/clusters/<str:cluster_name>/components/`
- 视图: paas_wl.apis.admin.views.clusters.ClusterComponentViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/clusters/<str:cluster_name>/components/<str:component_name>/`
- 视图: paas_wl.apis.admin.views.clusters.ClusterComponentViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/clusters/<str:pk>/`
- 视图: paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/clusters/<str:pk>/api_servers`
- 视图: paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/clusters/<str:pk>/set_default/`
- 视图: paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else pattern.include_module

**path**: `wl_api/platform/clusters/<str:pk>/api_servers/<str:api_server_id>`
- 视图: paas_wl.apis.admin.views.clusters.ClusterViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paas_wl.bk_app.cnative.specs.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.MresVersionViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.mres.revision.singular | 不适用 |  |
| re_path | 不适用 | None.ImageRepositoryView if pattern.view_name else (pattern.include_module or '不适用') | api.mres.image_tags.list | 不适用 |  |
| re_path | api/mres/quota_plans/$ | None.ResQuotaPlanOptionsView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | 不适用 | None.VolumeMountViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.mres.volume_mount | 不适用 |  |
| re_path | 不适用 | None.VolumeMountViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.mres.volume_mount.detail | 不适用 |  |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/mres/mount_sources/$ | None.MountSourceViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.mres.mount_source | 不适用 | 分组: code |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/mres/storage_class/$ | None.StorageClassViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.mres.storage_class | 不适用 | 分组: code |

#### 模式详情

**re_path**: `不适用`
- 视图: None.MresVersionViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ImageRepositoryView if pattern.view_name else pattern.include_module

**re_path**: `api/mres/quota_plans/$`
- 视图: None.ResQuotaPlanOptionsView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.VolumeMountViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.VolumeMountViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/mres/mount_sources/$`
- 视图: None.MountSourceViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/mres/storage_class/$`
- 视图: None.StorageClassViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paas_wl.bk_app.processes.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.ProcessesViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.processes.update | 不适用 |  |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/envs/(?P<environment>stag|prod)/processes/list/$ | None.CNativeListAndWatchProcsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.list_processes.namespace_scoped | 不适用 | 分组: code, environment |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/envs/(?P<environment>stag|prod)/processes/watch/$ | None.CNativeListAndWatchProcsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.watch_processes.namespace_scoped | 不适用 | 分组: code, environment |
| re_path | 不适用 | None.ListAndWatchProcsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.list_processes | 不适用 |  |
| re_path | 不适用 | None.ListAndWatchProcsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.watch_processes | 不适用 |  |
| re_path | 不适用 | None.InstanceEventsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.list_instance_events | 不适用 |  |
| re_path | 不适用 | None.InstanceManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.instances.previous_logs | 不适用 |  |
| re_path | 不适用 | None.InstanceManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.instances.previous_logs_download | 不适用 |  |
| re_path | 不适用 | None.InstanceManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.instances.restart | 不适用 |  |
| re_path | 不适用 | None.ProcessesViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.process.restart | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.ProcessesViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/envs/(?P<environment>stag|prod)/processes/list/$`
- 视图: None.CNativeListAndWatchProcsViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/envs/(?P<environment>stag|prod)/processes/watch/$`
- 视图: None.CNativeListAndWatchProcsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ListAndWatchProcsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ListAndWatchProcsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.InstanceEventsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.InstanceManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.InstanceManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.InstanceManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ProcessesViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paas_wl.workloads.images.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| path | api/bkapps/applications/<str:code>/image_credentials/ | None.AppUserCredentialViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.image_credentials | 不适用 | 转换器: code:str |
| path | api/bkapps/applications/<str:code>/image_credentials/<str:name> | None.AppUserCredentialViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.image_credentials.detail | 不适用 | 转换器: code:str, name:str |

#### 模式详情

**path**: `api/bkapps/applications/<str:code>/image_credentials/`
- 视图: None.AppUserCredentialViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkapps/applications/<str:code>/image_credentials/<str:name>`
- 视图: None.AppUserCredentialViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paas_wl.workloads.networking.egress.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.EgressGatewayInfosViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.egress_gateway_infos | 不适用 |  |
| re_path | 不适用 | None.EgressGatewayInfosViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.egress_gateway_infos.default | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.EgressGatewayInfosViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.EgressGatewayInfosViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paas_wl.workloads.networking.entrance.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | api/bkapps/applications/(?P<code>[^/]+)/domains/$ | None.AppDomainsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.app_domains | 不适用 | 分组: code |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/domains/(?P<id>\d+)/$ | None.AppDomainsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.app_domains.singular | 不适用 | 分组: code, id |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/domains/configs/$ | None.AppDomainsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.app_domains.configs | 不适用 | 分组: code |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/entrances/$ | None.AppEntranceViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.entrances.all_entrances | 不适用 | 分组: code |

#### 模式详情

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/domains/$`
- 视图: None.AppDomainsViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/domains/(?P<id>\d+)/$`
- 视图: None.AppDomainsViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/domains/configs/$`
- 视图: None.AppDomainsViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/entrances/$`
- 视图: None.AppEntranceViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paas_wl.workloads.networking.ingress.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.ProcessServicesViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.process_services | 不适用 |  |
| re_path | 不适用 | None.ProcessServicesViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.process_services.single | 不适用 |  |
| re_path | 不适用 | None.ProcessIngressesViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.process_ingresses.default | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.ProcessServicesViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ProcessServicesViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ProcessIngressesViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.accessories.app_secret.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/secrets/$ | paasng.accessories.app_secret.views.BkAuthSecretViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.app_secret.secrets | 不适用 | 分组: code |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/secrets/(?P<bk_app_secret_id>\d+)/$ | paasng.accessories.app_secret.views.BkAuthSecretViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.app_secret.secret | 不适用 | 分组: code, bk_app_secret_id |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/secret_verification/(?P<bk_app_secret_id>\d+)/$ | paasng.accessories.app_secret.views.BkAuthSecretViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.app_secret.secret_verification | 不适用 | 分组: code, bk_app_secret_id |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/default_secret/$ | paasng.accessories.app_secret.views.BkAppSecretInEnvVaViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.app_secret.default_secret | 不适用 | 分组: code |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/deployed_secret/$ | paasng.accessories.app_secret.views.BkAppSecretInEnvVaViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.app_secret.deployed_secret | 不适用 | 分组: code |

#### 模式详情

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/secrets/$`
- 视图: paasng.accessories.app_secret.views.BkAuthSecretViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/secrets/(?P<bk_app_secret_id>\d+)/$`
- 视图: paasng.accessories.app_secret.views.BkAuthSecretViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/secret_verification/(?P<bk_app_secret_id>\d+)/$`
- 视图: paasng.accessories.app_secret.views.BkAuthSecretViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/default_secret/$`
- 视图: paasng.accessories.app_secret.views.BkAppSecretInEnvVaViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/deployed_secret/$`
- 视图: paasng.accessories.app_secret.views.BkAppSecretInEnvVaViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.accessories.ci.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.CIInfoViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.ci.info | 不适用 |  |
| re_path | 不适用 | None.CIInfoViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.ci.detail | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.CIInfoViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.CIInfoViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.accessories.cloudapi.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| path | api/cloudapi/apps/<slug:app_code>/apis/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.apis | 不适用 | 转换器: app_code:slug |
| path | api/cloudapi/apps/<slug:app_code>/apis/<int:api_id>/permissions/resources/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.resource_permissions | 不适用 | 转换器: app_code:slug, api_id:int |
| path | api/cloudapi/apps/<slug:app_code>/apis/<int:api_id>/permissions/apply/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.apply_resource_permissions | 不适用 | 转换器: app_code:slug, api_id:int |
| path | api/cloudapi/apps/<slug:app_code>/apis/permissions/apply/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.batch_apply_resource_permissions | 不适用 | 转换器: app_code:slug |
| path | api/cloudapi/apps/<slug:app_code>/apis/permissions/renew/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.renew_resource_permissions | 不适用 | 转换器: app_code:slug |
| path | api/cloudapi/apps/<slug:app_code>/apis/<int:api_id>/permissions/allow-apply-by-api/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.allow_apply_by_api | 不适用 | 转换器: app_code:slug, api_id:int |
| path | api/cloudapi/apps/<slug:app_code>/apis/permissions/app-permissions/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.list_app_resource_permissions | 不适用 | 转换器: app_code:slug |
| path | api/cloudapi/apps/<slug:app_code>/apis/permissions/apply-records/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.list_resource_permission_apply_records | 不适用 | 转换器: app_code:slug |
| path | api/cloudapi/apps/<slug:app_code>/apis/permissions/apply-records/<int:record_id>/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.retrieve_resource_permission_apply_record | 不适用 | 转换器: app_code:slug, record_id:int |
| path | api/cloudapi/apps/<slug:app_code>/esb/systems/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.systems | 不适用 | 转换器: app_code:slug |
| path | api/cloudapi/apps/<slug:app_code>/esb/systems/<int:system_id>/permissions/components/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.component_permissions | 不适用 | 转换器: app_code:slug, system_id:int |
| path | api/cloudapi/apps/<slug:app_code>/esb/systems/<int:system_id>/permissions/apply/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.apply_component_permissions | 不适用 | 转换器: app_code:slug, system_id:int |
| path | api/cloudapi/apps/<slug:app_code>/esb/systems/permissions/renew/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.renew_component_permissions | 不适用 | 转换器: app_code:slug |
| path | api/cloudapi/apps/<slug:app_code>/esb/systems/permissions/app-permissions/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.list_app_component_permissions | 不适用 | 转换器: app_code:slug |
| path | api/cloudapi/apps/<slug:app_code>/esb/systems/permissions/apply-records/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.list_component_permission_apply_records | 不适用 | 转换器: app_code:slug |
| path | api/cloudapi/apps/<slug:app_code>/esb/systems/permissions/apply-records/<int:record_id>/ | None.CloudAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.cloudapi.v1.retrieve_component_permission_apply_record | 不适用 | 转换器: app_code:slug, record_id:int |

#### 模式详情

**path**: `api/cloudapi/apps/<slug:app_code>/apis/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/apis/<int:api_id>/permissions/resources/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/apis/<int:api_id>/permissions/apply/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/apis/permissions/apply/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/apis/permissions/renew/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/apis/<int:api_id>/permissions/allow-apply-by-api/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/apis/permissions/app-permissions/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/apis/permissions/apply-records/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/apis/permissions/apply-records/<int:record_id>/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/esb/systems/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/esb/systems/<int:system_id>/permissions/components/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/esb/systems/<int:system_id>/permissions/apply/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/esb/systems/permissions/renew/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/esb/systems/permissions/app-permissions/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/esb/systems/permissions/apply-records/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module

**path**: `api/cloudapi/apps/<slug:app_code>/esb/systems/permissions/apply-records/<int:record_id>/`
- 视图: None.CloudAPIViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.accessories.dev_sandbox.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.DevSandboxViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | 不适用 | None.DevSandboxWithCodeEditorViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/user/dev_sandbox_with_code_editors/pre_deploy_check/$ | None.DevSandboxWithCodeEditorViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/user/dev_sandbox_with_code_editors/lists/$ | None.DevSandboxWithCodeEditorViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code |
| re_path | 不适用 | None.DevSandboxWithCodeEditorViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.DevSandboxViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DevSandboxWithCodeEditorViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/user/dev_sandbox_with_code_editors/pre_deploy_check/$`
- 视图: None.DevSandboxWithCodeEditorViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/user/dev_sandbox_with_code_editors/lists/$`
- 视图: None.DevSandboxWithCodeEditorViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DevSandboxWithCodeEditorViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.accessories.log.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | views.logs.StructuredLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.structured.query_logs | 不适用 |  |
| re_path | 不适用 | views.logs.StructuredLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.structured.aggregate_date_histogram | 不适用 |  |
| re_path | 不适用 | views.logs.StructuredLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.structured.aggregate_fields_filters | 不适用 |  |
| re_path | 不适用 | views.logs.StdoutLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.stdout.query_logs | 不适用 |  |
| re_path | 不适用 | views.logs.StdoutLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.stdout.aggregate_fields_filters | 不适用 |  |
| re_path | 不适用 | views.logs.IngressLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.ingress.query_logs | 不适用 |  |
| re_path | 不适用 | views.logs.IngressLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.ingress.aggregate_date_histogram | 不适用 |  |
| re_path | 不适用 | views.logs.IngressLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.ingress.aggregate_fields_filters | 不适用 |  |
| re_path | 不适用 | views.logs.ModuleStructuredLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.structured.query_logs.legacy | 不适用 |  |
| re_path | 不适用 | views.logs.ModuleStructuredLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.structured.aggregate_date_histogram.legacy | 不适用 |  |
| re_path | 不适用 | views.logs.ModuleStructuredLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.structured.aggregate_fields_filters.legacy | 不适用 |  |
| re_path | 不适用 | views.logs.ModuleStdoutLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.stdout.query_logs.legacy | 不适用 |  |
| re_path | 不适用 | views.logs.ModuleStdoutLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.stdout.aggregate_fields_filters.legacy | 不适用 |  |
| re_path | 不适用 | views.logs.ModuleIngressLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.ingress.query_logs.legacy | 不适用 |  |
| re_path | 不适用 | views.logs.ModuleIngressLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.ingress.aggregate_date_histogram.legacy | 不适用 |  |
| re_path | 不适用 | views.logs.ModuleIngressLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.logs.ingress.aggregate_fields_filters.legacy | 不适用 |  |
| re_path | sys/api/log/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/envs/(?P<environment>stag|prod)/structured/list/$ | views.logs.SysStructuredLogAPIView if pattern.view_name else (pattern.include_module or '不适用') | sys.api.logs.structured | 不适用 | 分组: code, module_name, environment |

#### 模式详情

**re_path**: `不适用`
- 视图: views.logs.StructuredLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.StructuredLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.StructuredLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.StdoutLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.StdoutLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.IngressLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.IngressLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.IngressLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.ModuleStructuredLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.ModuleStructuredLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.ModuleStructuredLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.ModuleStdoutLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.ModuleStdoutLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.ModuleIngressLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.ModuleIngressLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.logs.ModuleIngressLogAPIView if pattern.view_name else pattern.include_module

**re_path**: `sys/api/log/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/envs/(?P<environment>stag|prod)/structured/list/$`
- 视图: views.logs.SysStructuredLogAPIView if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.accessories.paas_analysis.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.PageViewConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.config | 不适用 |  |
| re_path | 不适用 | None.PageViewMetricTrendViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.metrics.aggregate_by_interval$ | 不适用 |  |
| re_path | 不适用 | None.PageViewTotalMetricsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.metrics.total | 不适用 |  |
| re_path | 不适用 | None.DimensionMetricsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.metrics.group_by_dimension | 不适用 |  |
| re_path | 不适用 | None.CustomEventConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.event.config | 不适用 |  |
| re_path | 不适用 | None.CustomEventTotalMetricsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.metrics.event.total | 不适用 |  |
| re_path | 不适用 | None.CustomEventOverviewViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.metrics.event.overview | 不适用 |  |
| re_path | 不适用 | None.CustomEventDetailViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.metrics.event.detail | 不适用 |  |
| re_path | 不适用 | None.CustomEventTrendViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.metrics.event.aggregate_by_interval | 不适用 |  |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/config$ | None.PageViewConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.custom_site.metrics.config | 不适用 | 分组: code, site_name |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/metrics/aggregate_by_interval$ | None.PageViewMetricTrendViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.custom_site.metrics.aggregate_by_interval$ | 不适用 | 分组: code, site_name |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/metrics/total$ | None.PageViewTotalMetricsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.custom_site.metrics.total | 不适用 | 分组: code, site_name |
| re_path | 不适用 | None.DimensionMetricsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.custom_site.metrics.group_by_dimension | 不适用 |  |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/event/config$ | None.CustomEventConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.custom_site.event.config | 不适用 | 分组: code, site_name |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/event/metrics/total$ | None.CustomEventTotalMetricsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.custom_site.metrics.event.total | 不适用 | 分组: code, site_name |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/event/metrics/overview | None.CustomEventOverviewViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.custom_site.metrics.event.overview | 不适用 | 分组: code, site_name |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/event/metrics/c/(?P<category>[^/]+)/d/(?P<dimension>[^/]+)/detail | None.CustomEventDetailViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.custom_site.metrics.event.detail | 不适用 | 分组: code, site_name, category, dimension |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/event/metrics/aggregate_by_interval | None.CustomEventTrendViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.custom_site.metrics.event.aggregate_by_interval | 不适用 | 分组: code, site_name |
| re_path | 不适用 | None.IngressConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.analysis.ingress.tracking_status | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.PageViewConfigViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.PageViewMetricTrendViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.PageViewTotalMetricsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DimensionMetricsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.CustomEventConfigViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.CustomEventTotalMetricsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.CustomEventOverviewViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.CustomEventDetailViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.CustomEventTrendViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/config$`
- 视图: None.PageViewConfigViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/metrics/aggregate_by_interval$`
- 视图: None.PageViewMetricTrendViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/metrics/total$`
- 视图: None.PageViewTotalMetricsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DimensionMetricsViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/event/config$`
- 视图: None.CustomEventConfigViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/event/metrics/total$`
- 视图: None.CustomEventTotalMetricsViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/event/metrics/overview`
- 视图: None.CustomEventOverviewViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/event/metrics/c/(?P<category>[^/]+)/d/(?P<dimension>[^/]+)/detail`
- 视图: None.CustomEventDetailViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/analysis/site/(?P<site_name>default)/event/metrics/aggregate_by_interval`
- 视图: None.CustomEventTrendViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.IngressConfigViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.accessories.publish.entrance.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.ExposedURLTypeViewset if pattern.view_name else (pattern.include_module or '不适用') | api.entrance.exposed_url_type | 不适用 |  |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/default_entrance/$ | None.ApplicationAvailableAddressViewset if pattern.view_name else (pattern.include_module or '不适用') | api.entrance.default_entrance | 不适用 | 分组: code |
| re_path | 不适用 | None.ApplicationAvailableAddressViewset if pattern.view_name else (pattern.include_module or '不适用') | api.entrance.module.default_entrances | 不适用 |  |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/custom_domain_entrance/$ | None.ApplicationAvailableAddressViewset if pattern.view_name else (pattern.include_module or '不适用') | api.entrance.custom_domain_entrance | 不适用 | 分组: code |
| re_path | 不适用 | None.ModuleRootDomainsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.entrance.module.root_domain | 不适用 |  |
| re_path | 不适用 | None.ModuleRootDomainsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.entrance.module.preferred_root_domain | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.ExposedURLTypeViewset if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/default_entrance/$`
- 视图: None.ApplicationAvailableAddressViewset if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ApplicationAvailableAddressViewset if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/custom_domain_entrance/$`
- 视图: None.ApplicationAvailableAddressViewset if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleRootDomainsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleRootDomainsViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.accessories.publish.market.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/market/tags/(?P<id>[^/]+)$ | None.TagViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.market.tags.detail | 不适用 | 分组: id |
| re_path | ^api/market/tags$ | None.TagViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.market.tags | 不适用 |  |
| re_path | ^api/market/products/(?P<code>[^/]+)/state/?$ | None.ProductStateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.market.products.state | 不适用 | 分组: code |
| re_path | ^api/market/products/(?P<code>[^/]+)/?$ | None.ProductCombinedViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.market.products.detail | 不适用 | 分组: code |
| re_path | ^api/market/products/?$ | None.ProductCreateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.market.products.list | 不适用 |  |
| re_path | ^api/market/corp_products/$ | None.CorpProductViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.market.corp_products | 不适用 |  |

#### 模式详情

**re_path**: `^api/market/tags/(?P<id>[^/]+)$`
- 视图: None.TagViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/market/tags$`
- 视图: None.TagViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/market/products/(?P<code>[^/]+)/state/?$`
- 视图: None.ProductStateViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/market/products/(?P<code>[^/]+)/?$`
- 视图: None.ProductCombinedViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/market/products/?$`
- 视图: None.ProductCreateViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/market/corp_products/$`
- 视图: None.CorpProductViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.accessories.publish.sync_market.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/bkapps/applications/statistics/pv/top5 | None.StatisticsPVAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.global.statistics.pv.top5 | 不适用 |  |

#### 模式详情

**re_path**: `^api/bkapps/applications/statistics/pv/top5`
- 视图: None.StatisticsPVAPIView if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.accessories.servicehub.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.ServiceViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.get_service_detail | 不适用 |  |
| re_path | 不适用 | None.ServiceViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.list_service_by_region | 不适用 |  |
| re_path | 不适用 | None.ServiceViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.list_service_by_template | 不适用 |  |
| re_path | 不适用 | None.ServiceViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.list_application | 不适用 |  |
| re_path | 不适用 | None.ServicePlanViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.get_specifications | 不适用 |  |
| re_path | 不适用 | None.ServiceSetViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.list_service_by_category | 不适用 |  |
| re_path | ^api/services/name/(?P<service_name>[\w-]+)/application-attachments/$ | None.ServiceSetViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.list_service_with_application | 不适用 | 分组: service_name |
| re_path | 不适用 | None.ServiceViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.list_by_application | 不适用 |  |
| re_path | 不适用 | None.ServiceViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.list_by_module | 不适用 |  |
| re_path | 不适用 | None.ModuleServiceAttachmentsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.modules.services.attachments | 不适用 |  |
| re_path | 不适用 | None.ModuleServiceAttachmentsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.modules.services.info | 不适用 |  |
| re_path | 不适用 | None.ModuleServicesViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.list_provisioned_env_keys | 不适用 |  |
| re_path | 不适用 | None.ModuleServicesViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.list_specs_by_application | 不适用 |  |
| re_path | 不适用 | None.ModuleServicesViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.list_by_application | 不适用 |  |
| re_path | ^api/services/service-attachments/$ | None.ModuleServicesViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.service_application_attachments.bind | 不适用 |  |
| re_path | 不适用 | None.ServiceEngineAppAttachmentViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.credentials_enabled | 不适用 |  |
| re_path | 不适用 | None.ServiceSharingViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.list_shareable_modules | 不适用 |  |
| re_path | 不适用 | None.ServiceSharingViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.shared_attachment | 不适用 |  |
| re_path | 不适用 | None.SharingReferencesViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.sharing_references.list_related_modules | 不适用 |  |
| re_path | ^sys/api/services/mysql/(?P<db_name>[^/]+)/related_applications_info/$ | None.RelatedApplicationsInfoViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.services.mysql.retrieve_related_applications_info | 不适用 | 分组: db_name |

#### 模式详情

**re_path**: `不适用`
- 视图: None.ServiceViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ServiceViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ServiceViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ServiceViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ServicePlanViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ServiceSetViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/services/name/(?P<service_name>[\w-]+)/application-attachments/$`
- 视图: None.ServiceSetViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ServiceViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ServiceViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleServiceAttachmentsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleServiceAttachmentsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleServicesViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleServicesViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleServicesViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/services/service-attachments/$`
- 视图: None.ModuleServicesViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ServiceEngineAppAttachmentViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ServiceSharingViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ServiceSharingViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.SharingReferencesViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/services/mysql/(?P<db_name>[^/]+)/related_applications_info/$`
- 视图: None.RelatedApplicationsInfoViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.accessories.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.AdvisedDocumentaryLinksViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.advisor.advised_links | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.AdvisedDocumentaryLinksViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.bk_plugins.bk_plugins.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^sys/api/bk_plugins/$ | None.SysBkPluginsViewset if pattern.view_name else (pattern.include_module or '不适用') | sys.api.bk_plugins.list | 不适用 |  |
| re_path | ^sys/api/bk_plugins/(?P<code>[^/]+)/$ | None.SysBkPluginsViewset if pattern.view_name else (pattern.include_module or '不适用') | sys.api.bk_plugins.retrieve | 不适用 | 分组: code |
| re_path | ^sys/api/bk_plugins/(?P<code>[^/]+)/logs/$ | None.SysBkPluginLogsViewset if pattern.view_name else (pattern.include_module or '不适用') | sys.api.bk_plugins.logs.list | 不适用 | 分组: code |
| re_path | ^sys/api/bk_plugin_tags/$ | None.SysBkPluginTagsViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.bk_plugin_tags | 不适用 |  |
| re_path | ^sys/api/bk_plugins/batch/detailed/$ | None.SysBkPluginsBatchViewset if pattern.view_name else (pattern.include_module or '不适用') | sys.api.bk_plugins.list_detailed | 不适用 |  |
| re_path | ^sys/api/plugins_center/bk_plugins/$ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.plugins_center.bk_plugins.create | 不适用 |  |
| re_path | ^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/$ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.plugins_center.bk_plugins.detail | 不适用 | 分组: code |
| re_path | ^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/deploy/$ | None.PluginDeployViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.plugins_center.bk_plugins.deploy | 不适用 | 分组: code |
| re_path | ^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/deploy/(?P<deploy_id>[^/]+)/status/$ | None.PluginDeployViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.plugins_center.bk_plugins.deploy.status | 不适用 | 分组: code, deploy_id |
| re_path | ^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/deploy/(?P<deploy_id>[^/]+)/logs/$ | None.PluginDeployViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.plugins_center.bk_plugins.deploy.logs | 不适用 | 分组: code, deploy_id |
| re_path | ^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/market/$ | None.PluginMarketViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.plugins_center.bk_plugins.market.upsert | 不适用 | 分组: code |
| re_path | ^sys/api/plugins_center/bk_plugins/market/category/$ | None.PluginMarketViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.plugins_center.bk_plugins.market.list_category | 不适用 |  |
| re_path | ^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/members/$ | None.PluginMembersViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.plugins_center.bk_plugins.members.sync | 不适用 | 分组: code |
| re_path | ^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/configuration/$ | None.PluginConfigurationViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.plugins_center.bk_plugins.configurations.sync | 不适用 | 分组: code |
| re_path | ^api/bk_plugins/(?P<code>[^/]+)/profile/$ | None.BkPluginProfileViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.bk_plugins.profile | 不适用 | 分组: code |
| re_path | ^api/bk_plugins/(?P<code>[^/]+)/distributors/$ | None.DistributorRelsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.bk_plugins.distributor_rels | 不适用 | 分组: code |
| re_path | ^api/bk_plugin_distributors/$ | None.DistributorsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.bk_plugin_distributors | 不适用 |  |
| re_path | ^api/bk_plugin_tags/$ | None.BkPluginTagsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.bk_plugin_tags | 不适用 |  |

#### 模式详情

**re_path**: `^sys/api/bk_plugins/$`
- 视图: None.SysBkPluginsViewset if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/bk_plugins/(?P<code>[^/]+)/$`
- 视图: None.SysBkPluginsViewset if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/bk_plugins/(?P<code>[^/]+)/logs/$`
- 视图: None.SysBkPluginLogsViewset if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/bk_plugin_tags/$`
- 视图: None.SysBkPluginTagsViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/bk_plugins/batch/detailed/$`
- 视图: None.SysBkPluginsBatchViewset if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/plugins_center/bk_plugins/$`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/$`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/deploy/$`
- 视图: None.PluginDeployViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/deploy/(?P<deploy_id>[^/]+)/status/$`
- 视图: None.PluginDeployViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/deploy/(?P<deploy_id>[^/]+)/logs/$`
- 视图: None.PluginDeployViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/market/$`
- 视图: None.PluginMarketViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/plugins_center/bk_plugins/market/category/$`
- 视图: None.PluginMarketViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/members/$`
- 视图: None.PluginMembersViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/plugins_center/bk_plugins/(?P<code>[^/]+)/configuration/$`
- 视图: None.PluginConfigurationViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bk_plugins/(?P<code>[^/]+)/profile/$`
- 视图: None.BkPluginProfileViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bk_plugins/(?P<code>[^/]+)/distributors/$`
- 视图: None.DistributorRelsViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bk_plugin_distributors/$`
- 视图: None.DistributorsViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bk_plugin_tags/$`
- 视图: None.BkPluginTagsViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.bk_plugins.pluginscenter.itsm_adaptor.open_apis.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| path | open/api/itsm/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/ | None.PluginCallBackApiViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | open/api/itsm/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/stages/<str:stage_id>/ | None.PluginCallBackApiViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, release_id:str, stage_id:str |
| path | open/api/itsm/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/visible_range/ | None.PluginCallBackApiViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | 不适用 | None.PluginCallBackApiViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**path**: `open/api/itsm/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/`
- 视图: None.PluginCallBackApiViewSet if pattern.view_name else pattern.include_module

**path**: `open/api/itsm/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/stages/<str:stage_id>/`
- 视图: None.PluginCallBackApiViewSet if pattern.view_name else pattern.include_module

**path**: `open/api/itsm/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/visible_range/`
- 视图: None.PluginCallBackApiViewSet if pattern.view_name else pattern.include_module

**path**: `不适用`
- 视图: None.PluginCallBackApiViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.bk_plugins.pluginscenter.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| path | api/bkplugins/filter_params/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| path | api/bkplugins/lists/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| path | api/bkplugins/<str:pd_id>/plugins/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/basic_info/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/extra_fields/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/publisher/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/visible_range/ | None.PluginVisibleRangeViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logo/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/overview/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/archive/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/reactivate/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | 不适用 | None.PluginReleaseViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/code_statistics/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/feature_flags/ | None.PluginInstanceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/ | None.PluginReleaseViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/schema/ | None.PluginReleaseViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/ | None.PluginReleaseViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, release_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/next/ | None.PluginReleaseViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, release_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/back/ | None.PluginReleaseViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, release_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/cancel/ | None.PluginReleaseViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, release_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/reset/ | None.PluginReleaseViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, release_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/rollback/ | None.PluginReleaseViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, release_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/stages/<str:stage_id>/ | None.PluginReleaseStageViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, release_id:str, stage_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/stages/<str:stage_id>/rerun/ | None.PluginReleaseStageViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, release_id:str, stage_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/stages/<str:stage_id>/status/ | None.PluginReleaseStageViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, release_id:str, stage_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/strategy/ | None.PluginReleaseStrategyViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, release_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/market/ | None.PluginMarketViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/standard_output/ | None.PluginLogViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/structure_logs/ | None.PluginLogViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/ingress_logs/ | None.PluginLogViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/aggregate_date_histogram/<str:log_type>/ | None.PluginLogViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, log_type:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/aggregate_fields_filters/<str:log_type>/ | None.PluginLogViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, log_type:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members/ | None.PluginMembersViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members/leave/ | None.PluginMembersViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members/<str:username>/ | None.PluginMembersViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, username:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/configurations/ | None.PluginConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/configurations/<str:config_id>/ | None.PluginConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, config_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members/leave/ | None.PluginMembersViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members/<str:username>/ | None.PluginMembersViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str, username:str |
| path | api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/operations/ | None.OperationRecordViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str, plugin_id:str |
| path | api/bkplugins/plugin_definitions/schemas/ | None.SchemaViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| path | api/bkplugins/plugin_definitions/<str:pd_id>/market_schema/ | None.SchemaViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str |
| path | api/bkplugins/plugin_definitions/<str:pd_id>/basic_info_schema/ | None.SchemaViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str |
| path | api/bkplugins/plugin_definitions/<str:pd_id>/configuration_schema/ | None.SchemaViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: pd_id:str |
| path | api/bkplugins/shim/iam/selection/plugin_view/ | None.PluginSelectionView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| path | api/usermanage/departments/<str:dept_id>/ | None.BkPluginUserManageView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: dept_id:str |

#### 模式详情

**path**: `api/bkplugins/filter_params/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/lists/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/basic_info/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/extra_fields/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/publisher/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/visible_range/`
- 视图: None.PluginVisibleRangeViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logo/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/overview/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/archive/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/reactivate/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `不适用`
- 视图: None.PluginReleaseViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/code_statistics/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/feature_flags/`
- 视图: None.PluginInstanceViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/`
- 视图: None.PluginReleaseViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/schema/`
- 视图: None.PluginReleaseViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/`
- 视图: None.PluginReleaseViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/next/`
- 视图: None.PluginReleaseViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/back/`
- 视图: None.PluginReleaseViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/cancel/`
- 视图: None.PluginReleaseViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/reset/`
- 视图: None.PluginReleaseViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/rollback/`
- 视图: None.PluginReleaseViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/stages/<str:stage_id>/`
- 视图: None.PluginReleaseStageViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/stages/<str:stage_id>/rerun/`
- 视图: None.PluginReleaseStageViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/stages/<str:stage_id>/status/`
- 视图: None.PluginReleaseStageViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/releases/<str:release_id>/strategy/`
- 视图: None.PluginReleaseStrategyViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/market/`
- 视图: None.PluginMarketViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/standard_output/`
- 视图: None.PluginLogViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/structure_logs/`
- 视图: None.PluginLogViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/ingress_logs/`
- 视图: None.PluginLogViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/aggregate_date_histogram/<str:log_type>/`
- 视图: None.PluginLogViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/logs/aggregate_fields_filters/<str:log_type>/`
- 视图: None.PluginLogViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members/`
- 视图: None.PluginMembersViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members/leave/`
- 视图: None.PluginMembersViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members/<str:username>/`
- 视图: None.PluginMembersViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/configurations/`
- 视图: None.PluginConfigViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/configurations/<str:config_id>/`
- 视图: None.PluginConfigViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members/leave/`
- 视图: None.PluginMembersViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/members/<str:username>/`
- 视图: None.PluginMembersViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/<str:pd_id>/plugins/<str:plugin_id>/operations/`
- 视图: None.OperationRecordViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/plugin_definitions/schemas/`
- 视图: None.SchemaViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/plugin_definitions/<str:pd_id>/market_schema/`
- 视图: None.SchemaViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/plugin_definitions/<str:pd_id>/basic_info_schema/`
- 视图: None.SchemaViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/plugin_definitions/<str:pd_id>/configuration_schema/`
- 视图: None.SchemaViewSet if pattern.view_name else pattern.include_module

**path**: `api/bkplugins/shim/iam/selection/plugin_view/`
- 视图: None.PluginSelectionView if pattern.view_name else pattern.include_module

**path**: `api/usermanage/departments/<str:dept_id>/`
- 视图: None.BkPluginUserManageView if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.core.region.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.RegionViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.regions.retrieve | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.RegionViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.infras.accounts.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/user/$ | None.UserInfoViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.accounts.user | 不适用 |  |
| re_path | ^api/accounts/feature_flags/$ | None.AccountFeatureFlagViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.accounts.feature_flags | 不适用 |  |
| re_path | ^api/accounts/userinfo/$ | None.UserInfoViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.accounts.userinfo | 不适用 |  |
| re_path | ^api/accounts/verification/generation/$ | None.UserVerificationGenerationView if pattern.view_name else (pattern.include_module or '不适用') | api.accounts.verification.generation | 不适用 |  |
| re_path | ^api/accounts/verification/validation/$ | None.UserVerificationValidationView if pattern.view_name else (pattern.include_module or '不适用') | api.accounts.verification.validation | 不适用 |  |
| re_path | ^api/accounts/oauth/token/$ | None.OauthTokenViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.accounts.oauth.token | 不适用 |  |
| re_path | ^api/oauth/backends/$ | None.Oauth2BackendsViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | ^api/oauth/backends/(?P<backend>[^/]+)/(?P<pk>[^/]+)/$ | None.Oauth2BackendsViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: backend, pk |
| re_path | ^api/oauth/complete/(?P<backend>[^/]+)/?$ | None.Oauth2BackendsViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: backend |
| re_path | ^api/bkapps/regions/specs | None.RegionSpecsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.region.specs | 不适用 |  |

#### 模式详情

**re_path**: `^api/user/$`
- 视图: None.UserInfoViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/accounts/feature_flags/$`
- 视图: None.AccountFeatureFlagViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/accounts/userinfo/$`
- 视图: None.UserInfoViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/accounts/verification/generation/$`
- 视图: None.UserVerificationGenerationView if pattern.view_name else pattern.include_module

**re_path**: `^api/accounts/verification/validation/$`
- 视图: None.UserVerificationValidationView if pattern.view_name else pattern.include_module

**re_path**: `^api/accounts/oauth/token/$`
- 视图: None.OauthTokenViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/oauth/backends/$`
- 视图: None.Oauth2BackendsViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/oauth/backends/(?P<backend>[^/]+)/(?P<pk>[^/]+)/$`
- 视图: None.Oauth2BackendsViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/oauth/complete/(?P<backend>[^/]+)/?$`
- 视图: None.Oauth2BackendsViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/regions/specs`
- 视图: None.RegionSpecsViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.infras.iam.open_apis.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.ResourceAPIView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.ResourceAPIView if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.misc.audit.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/bkapps/applications/lists/latest/ | None.LatestApplicationsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.latest | 不适用 |  |
| re_path | 不适用 | None.ApplicationAuditRecordViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.bkapps.application.audit.records | 不适用 |  |

#### 模式详情

**re_path**: `^api/bkapps/applications/lists/latest/`
- 视图: None.LatestApplicationsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ApplicationAuditRecordViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.misc.changelog.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| path | api/changelogs/ | None.ChangelogViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**path**: `api/changelogs/`
- 视图: None.ChangelogViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.misc.metrics.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^metrics$ | None.ExportToDjangoView if pattern.view_name else (pattern.include_module or '不适用') | prometheus-django-metrics | 不适用 |  |

#### 模式详情

**re_path**: `^metrics$`
- 视图: None.ExportToDjangoView if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.misc.monitoring.healthz.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | healthz/$ | None.HealthViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.healthz | 不适用 |  |
| re_path | readyz/$ | None.HealthViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.readyz | 不适用 |  |

#### 模式详情

**re_path**: `healthz/$`
- 视图: None.HealthViewSet if pattern.view_name else pattern.include_module

**re_path**: `readyz/$`
- 视图: None.HealthViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.misc.monitoring.monitor.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | api/monitor/applications/(?P<code>[^/]+)/record/query/$ | None.EventRecordView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code |
| re_path | api/monitor/applications/(?P<code>[^/]+)/record/(?P<record>[^/]+)/$ | None.EventRecordDetailsView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code, record |
| re_path | api/monitor/applications/(?P<code>[^/]+)/record_metrics/(?P<record>[^/]+)/$ | None.EventRecordMetricsView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code, record |
| re_path | api/monitor/applications/(?P<code>[^/]+)/genre/$ | None.EventGenreView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code |
| re_path | api/monitor/record/applications/summary/$ | None.EventRecordView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| path | api/monitor/applications/<slug:code>/modules/<slug:module_name>/alert_rules/ | None.AlertRulesView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: code:slug, module_name:slug |
| path | api/monitor/applications/<slug:code>/alert_rules/init/ | None.AlertRulesView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: code:slug |
| path | api/monitor/supported_alert_rules/ | None.AlertRulesView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| path | api/monitor/applications/<slug:code>/alerts/ | None.ListAlertsView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: code:slug |
| path | api/monitor/user/alerts/ | None.ListAlertsView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| path | api/monitor/applications/<slug:code>/alarm_strategies/ | None.ListAlarmStrategiesView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: code:slug |
| path | api/monitor/applications/<slug:code>/dashboard_info/ | None.GetDashboardInfoView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 转换器: code:slug |
| path | api/monitor/applications/<slug:code>/builtin_dashboards/ | None.GetDashboardInfoView if pattern.view_name else (pattern.include_module or '不适用') | api.modules.monitor.builtin_dashboards | 不适用 | 转换器: code:slug |

#### 模式详情

**re_path**: `api/monitor/applications/(?P<code>[^/]+)/record/query/$`
- 视图: None.EventRecordView if pattern.view_name else pattern.include_module

**re_path**: `api/monitor/applications/(?P<code>[^/]+)/record/(?P<record>[^/]+)/$`
- 视图: None.EventRecordDetailsView if pattern.view_name else pattern.include_module

**re_path**: `api/monitor/applications/(?P<code>[^/]+)/record_metrics/(?P<record>[^/]+)/$`
- 视图: None.EventRecordMetricsView if pattern.view_name else pattern.include_module

**re_path**: `api/monitor/applications/(?P<code>[^/]+)/genre/$`
- 视图: None.EventGenreView if pattern.view_name else pattern.include_module

**re_path**: `api/monitor/record/applications/summary/$`
- 视图: None.EventRecordView if pattern.view_name else pattern.include_module

**path**: `api/monitor/applications/<slug:code>/modules/<slug:module_name>/alert_rules/`
- 视图: None.AlertRulesView if pattern.view_name else pattern.include_module

**path**: `api/monitor/applications/<slug:code>/alert_rules/init/`
- 视图: None.AlertRulesView if pattern.view_name else pattern.include_module

**path**: `api/monitor/supported_alert_rules/`
- 视图: None.AlertRulesView if pattern.view_name else pattern.include_module

**path**: `api/monitor/applications/<slug:code>/alerts/`
- 视图: None.ListAlertsView if pattern.view_name else pattern.include_module

**path**: `api/monitor/user/alerts/`
- 视图: None.ListAlertsView if pattern.view_name else pattern.include_module

**path**: `api/monitor/applications/<slug:code>/alarm_strategies/`
- 视图: None.ListAlarmStrategiesView if pattern.view_name else pattern.include_module

**path**: `api/monitor/applications/<slug:code>/dashboard_info/`
- 视图: None.GetDashboardInfoView if pattern.view_name else pattern.include_module

**path**: `api/monitor/applications/<slug:code>/builtin_dashboards/`
- 视图: None.GetDashboardInfoView if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.misc.operations.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/bkapps/applications/lists/latest/deprecated/ | None.LatestApplicationsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.latest.deprecated | 不适用 |  |
| re_path | 不适用 | None.ApplicationOperationsViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.bkapps.application.operations | 不适用 |  |

#### 模式详情

**re_path**: `^api/bkapps/applications/lists/latest/deprecated/`
- 视图: None.LatestApplicationsViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ApplicationOperationsViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.misc.plat_config.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| path | api/platform/frontend_features/ | None.FrontendFeatureViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**path**: `api/platform/frontend_features/`
- 视图: None.FrontendFeatureViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.misc.search.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/document/search/$ | None.MixDocumentSearch if pattern.view_name else (pattern.include_module or '不适用') | document-search | 不适用 |  |
| re_path | ^api/search/applications/$ | None.ApplicationsSearchViewset if pattern.view_name else (pattern.include_module or '不适用') | search.applications | 不适用 |  |
| re_path | ^api/search/bk_docs/$ | None.BkDocsSearchViewset if pattern.view_name else (pattern.include_module or '不适用') | search.bk_docs | 不适用 |  |

#### 模式详情

**re_path**: `^api/document/search/$`
- 视图: None.MixDocumentSearch if pattern.view_name else pattern.include_module

**re_path**: `^api/search/applications/$`
- 视图: None.ApplicationsSearchViewset if pattern.view_name else pattern.include_module

**re_path**: `^api/search/bk_docs/$`
- 视图: None.BkDocsSearchViewset if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.misc.tools.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/tools/app_desc/transform/ | None.AppDescTransformAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.tools.app_desc.transform | 不适用 |  |

#### 模式详情

**re_path**: `^api/tools/app_desc/transform/`
- 视图: None.AppDescTransformAPIView if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.plat_admin.admin42.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^$ | None.FrontPageView if pattern.view_name else (pattern.include_module or '不适用') | admin.front_page | 不适用 |  |
| re_path | ^platform/$ | views.applications.ApplicationListView if pattern.view_name else (pattern.include_module or '不适用') | admin.platform.index | 不适用 |  |
| re_path | ^platform/process_spec_plan/manage/$ | views.engine.proc_spec.ProcessSpecPlanManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.process_spec_plan.manage | 不适用 |  |
| re_path | ^platform/services/manage$ | views.services.PlatformServicesView if pattern.view_name else (pattern.include_module or '不适用') | admin.services.manage | 不适用 |  |
| re_path | ^platform/services/$ | views.services.PlatformServicesManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.services | 不适用 |  |
| re_path | ^platform/services/(?P<pk>[^/]+)/$ | views.services.PlatformServicesManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.services.detail | 不适用 | 分组: pk |
| re_path | ^platform/plans/manage$ | views.services.PlatformPlanView if pattern.view_name else (pattern.include_module or '不适用') | admin.plans.manage | 不适用 |  |
| re_path | ^platform/plans/$ | views.services.PlatformPlanManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.plans.list | 不适用 |  |
| re_path | ^platform/services/(?P<service_id>[^/]+)/plans/$ | views.services.PlatformPlanManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.plans.create | 不适用 | 分组: service_id |
| re_path | ^platform/services/(?P<service_id>[^/]+)/plans/(?P<plan_id>[^/]+)/$ | views.services.PlatformPlanManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.plans.detail | 不适用 | 分组: service_id, plan_id |
| re_path | ^platform/pre-created-instances/manage$ | views.services.PreCreatedInstanceView if pattern.view_name else (pattern.include_module or '不适用') | admin.pre_created_instances.manage | 不适用 |  |
| re_path | ^platform/pre-created-instances/$ | views.services.PreCreatedInstanceManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.pre_created_instances | 不适用 |  |
| re_path | ^platform/pre-created-instances/(?P<plan_id>[^/]+)/(?P<uuid>[^/]+)/$ | views.services.PreCreatedInstanceManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.pre_created_instances.detail | 不适用 | 分组: plan_id, uuid |
| re_path | ^platform/smart-advisor/documents/manage$ | views.smart_advisor.DocumentaryLinkView if pattern.view_name else (pattern.include_module or '不适用') | admin.smart_advisor.documents.manage | 不适用 |  |
| re_path | ^platform/smart-advisor/documents/$ | views.smart_advisor.DocumentaryLinkManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.smart_advisor.documents | 不适用 |  |
| re_path | ^platform/smart-advisor/documents/(?P<pk>[^/]+)/$ | views.smart_advisor.DocumentaryLinkManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.smart_advisor.documents.detail | 不适用 | 分组: pk |
| re_path | ^platform/smart-advisor/deploy_failure_tips/manage$ | views.smart_advisor.DeployFailurePatternView if pattern.view_name else (pattern.include_module or '不适用') | admin.smart_advisor.deploy_failure_tips.manage | 不适用 |  |
| re_path | ^platform/smart-advisor/deploy_failure_tips/$ | views.smart_advisor.DeployFailurePatternManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.smart_advisor.deploy_failure_tips | 不适用 |  |
| re_path | ^platform/smart-advisor/deploy_failure_tips/(?P<pk>[^/]+)/ | views.smart_advisor.DeployFailurePatternManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.smart_advisor.deploy_failure_tips.detail | 不适用 | 分组: pk |
| re_path | ^platform/runtimes/buildpack/manage/$ | views.runtimes.BuildPackManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.runtimes.buildpack.manage | 不适用 |  |
| re_path | ^platform/runtimes/buildpack/$ | views.runtimes.BuildPackAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.runtimes.buildpack | 不适用 |  |
| re_path | ^platform/runtimes/buildpack/(?P<pk>[^/]+)/$ | views.runtimes.BuildPackAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.runtimes.buildpack.detail | 不适用 | 分组: pk |
| re_path | ^platform/runtimes/buildpack/(?P<pk>[^/]+)/bind/$ | views.runtimes.BuildPackAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.runtimes.buildpack.detail.bind | 不适用 | 分组: pk |
| re_path | ^platform/runtimes/slugbuilder/manage/$ | views.runtimes.SlugBuilderManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.runtimes.slugbuilder.manage | 不适用 |  |
| re_path | ^platform/runtimes/slugbuilder/$ | views.runtimes.SlugBuilderAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.runtimes.slugbuilder | 不适用 |  |
| re_path | ^platform/runtimes/slugbuilder/(?P<pk>[^/]+)/$ | views.runtimes.SlugBuilderAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.runtimes.slugbuilder.detail | 不适用 | 分组: pk |
| re_path | ^platform/runtime/slugbuilder/(?P<pk>[^/]+)/bind/$ | views.runtimes.SlugBuilderAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.runtimes.slugbuilder.detail.bind | 不适用 | 分组: pk |
| re_path | ^platform/runtimes/slugrunner/manage$ | views.runtimes.AppSlugRunnerManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.runtimes.slugrunner.manage | 不适用 |  |
| re_path | ^platform/runtimes/slugrunner/$ | views.runtimes.SlugRunnerAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.runtimes.slugrunner | 不适用 |  |
| re_path | ^platform/runtimes/slugrunner/(?P<pk>[^/]+)/$ | views.runtimes.SlugRunnerAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.runtimes.slugrunner.detail | 不适用 | 分组: pk |
| re_path | ^platform/clusters/manage/$ | views.engine.clusters.ClusterManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.clusters.manage | 不适用 |  |
| re_path | ^platform/clusters/components/manage/$ | views.engine.clusters.ClusterComponentManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.cluster_components.manage | 不适用 |  |
| re_path | ^platform/operators/manage/$ | views.engine.operator.OperatorManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.operators.manage | 不适用 |  |
| re_path | ^platform/certs/shared/manage/$ | views.engine.certs.SharedCertsManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.shared.certs.manage | 不适用 |  |
| re_path | ^platform/sourcectl/source_type_spec/manage/$ | views.sourcectl.SourceTypeSpecManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.sourcectl.source_type_spec.manage | 不适用 |  |
| re_path | ^platform/sourcectl/source_type_spec/$ | views.sourcectl.SourceTypeSpecViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.sourcectl.source_type_spec | 不适用 |  |
| re_path | ^platform/sourcectl/source_type_spec/(?P<pk>[^/]+)/ | views.sourcectl.SourceTypeSpecViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.sourcectl.source_type_spec.detail | 不适用 | 分组: pk |
| re_path | ^applications/$ | views.applications.ApplicationListView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.list | 不适用 |  |
| re_path | ^applications/evaluations/$ | views.applications.ApplicationOperationEvaluationView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.operation_evaluation.list | 不适用 |  |
| re_path | ^applications/evaluations/export/$ | views.applications.ApplicationOperationReportExportView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.operation_evaluation.export | 不适用 |  |
| re_path | ^applications/(?P<code>[^/]+)/overview/$ | views.applications.ApplicationOverviewView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.detail.overview | 不适用 | 分组: code |
| re_path | 不适用 | views.applications.AppEnvConfManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.env_conf.bind_cluster | 不适用 |  |
| re_path | ^applications/(?P<code>[^/]+)/engine/process_specs/$ | views.engine.proc_spec.ProcessSpecManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.process_specs | 不适用 | 分组: code |
| re_path | ^applications/(?P<code>[^/]+)/engine/source_packages/manage/$ | views.engine.package.SourcePackageManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.source_packages.manage | 不适用 | 分组: code |
| re_path | ^applications/(?P<code>[^/]+)/engine/source_packages/$ | views.engine.package.SourcePackageManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.source_packages.list | 不适用 | 分组: code |
| re_path | 不适用 | views.engine.package.SourcePackageManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.source_packages.detail | 不适用 |  |
| re_path | ^applications/(?P<code>[^/]+)/engine/egress/manage/$ | views.engine.egress.EgressManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.egress.manage | 不适用 | 分组: code |
| re_path | 不适用 | views.engine.egress.EgressManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.egress.detail | 不适用 |  |
| re_path | 不适用 | views.engine.egress.EgressManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.egress.ips | 不适用 |  |
| re_path | ^applications/(?P<code>[^/]+)/engine/config_vars/manage/$ | views.engine.config_vars.ConfigVarManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.config_vars.manage | 不适用 | 分组: code |
| re_path | ^application/(?P<code>[^/]+)/engine/config_vars$ | views.engine.config_vars.ConfigVarViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.config_vars.list | 不适用 | 分组: code |
| re_path | 不适用 | views.engine.config_vars.ConfigVarViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.config_vars.create | 不适用 |  |
| re_path | 不适用 | views.engine.config_vars.ConfigVarViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.config_vars.detail | 不适用 |  |
| re_path | ^applications/(?P<code>[^/]+)/engine/runtime/manage/$ | views.engine.runtime.RuntimeManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.runtime.manage | 不适用 | 分组: code |
| re_path | ^applications/(?P<code>[^/]+)/engine/runtime/$ | views.engine.runtime.RuntimeManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.runtime.list | 不适用 | 分组: code |
| re_path | 不适用 | views.engine.runtime.RuntimeManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.runtime.bind | 不适用 |  |
| re_path | ^applications/(?P<code>[^/]+)/services/$ | views.services.ApplicationServicesView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.services | 不适用 | 分组: code |
| re_path | ^api/applications/(?P<code>[^/]+)/services/$ | views.services.ApplicationServicesManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.services.list | 不适用 | 分组: code |
| re_path | ^api/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/env/(?P<environment>[^/]+)/services/(?P<service_id>[^/]+)/provision/$ | views.services.ApplicationServicesManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.services.provision | 不适用 | 分组: code, module_name, environment, service_id |
| re_path | ^api/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/services/(?P<service_id>[^/]+)/instances/(?P<instance_id>[^/]+)/$ | views.services.ApplicationServicesManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.services.recycle_resource | 不适用 | 分组: code, module_name, service_id, instance_id |
| re_path | ^applications/(?P<code>[^/]+)/base_info/memberships/$ | views.applications.ApplicationMembersManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.detail.base_info.members | 不适用 | 分组: code |
| re_path | ^api/applications/(?P<code>[^/]+)/base_info/memberships/$ | views.applications.ApplicationMembersManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.detail.base_info.members.api | 不适用 | 分组: code |
| re_path | ^api/applications/(?P<code>[^/]+)/base_info/memberships/(?P<username>[^/]+)/$ | views.applications.ApplicationMembersManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.detail.base_info.members.api | 不适用 | 分组: code, username |
| re_path | ^api/applications/(?P<code>[^/]+)/base_info/plugin/memberships/$ | views.bk_plugins.BKPluginMembersManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.detail.base_info.plugin.members.api | 不适用 | 分组: code |
| re_path | ^applications/(?P<code>[^/]+)/base_info/feature_flags/$ | views.applications.ApplicationFeatureFlagsView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.detail.base_info.feature_flags | 不适用 | 分组: code |
| re_path | ^api/applications/(?P<code>[^/]+)/base_info/feature_flags/$ | views.applications.ApplicationFeatureFlagsViewset if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.detail.base_info.feature_flags.api | 不适用 | 分组: code |
| re_path | ^applications/(?P<code>[^/]+)/engine/custom_domain/$ | views.engine.custom_domain.CustomDomainManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.custom_domain | 不适用 | 分组: code |
| re_path | ^applications/(?P<code>[^/]+)/engine/log_config/$ | views.engine.log_config.LogConfigView if pattern.view_name else (pattern.include_module or '不适用') | admin.applications.engine.log_config.manage | 不适用 | 分组: code |
| re_path | ^accountmgr/$ | views.accountmgr.UserProfilesManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.accountmgr.index | 不适用 |  |
| re_path | ^accountmgr/userprofiles/$ | views.accountmgr.UserProfilesManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.accountmgr.userprofiles.index | 不适用 |  |
| re_path | ^api/accountmgr/userprofiles/$ | views.accountmgr.UserProfilesManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.accountmgr.userprofile.api | 不适用 |  |
| re_path | ^accountmgr/account_feature_flags/$ | views.accountmgr.AccountFeatureFlagManageView if pattern.view_name else (pattern.include_module or '不适用') | admin.accountmgr.account_feature_flags.index | 不适用 |  |
| re_path | ^api/accountmgr/account_feature_flags/$ | views.accountmgr.AccountFeatureFlagManageViewSet if pattern.view_name else (pattern.include_module or '不适用') | admin.accountmgr.account_feature_flags.api | 不适用 |  |
| re_path | ^deployments/$ | views.engine.deployments.DeploymentListView if pattern.view_name else (pattern.include_module or '不适用') | admin.deployments.list | 不适用 |  |
| re_path | ^operation/statistics/deploy/apps/$ | views.operation.deploy.AppDeployStatisticsView if pattern.view_name else (pattern.include_module or '不适用') | admin.operation.statistics.deploy.apps | 不适用 |  |
| re_path | ^operation/statistics/deploy/apps/export/$ | views.operation.deploy.AppDeployStatisticsView if pattern.view_name else (pattern.include_module or '不适用') | admin.operation.statistics.deploy.apps.export | 不适用 |  |
| re_path | ^operation/statistics/deploy/developers/$ | views.operation.deploy.DevelopersDeployStatisticsView if pattern.view_name else (pattern.include_module or '不适用') | admin.operation.statistics.deploy.developers | 不适用 |  |
| re_path | ^operation/statistics/deploy/developers/export/$ | views.operation.deploy.DevelopersDeployStatisticsView if pattern.view_name else (pattern.include_module or '不适用') | admin.operation.statistics.deploy.developers.export | 不适用 |  |

#### 模式详情

**re_path**: `^$`
- 视图: None.FrontPageView if pattern.view_name else pattern.include_module

**re_path**: `^platform/$`
- 视图: views.applications.ApplicationListView if pattern.view_name else pattern.include_module

**re_path**: `^platform/process_spec_plan/manage/$`
- 视图: views.engine.proc_spec.ProcessSpecPlanManageView if pattern.view_name else pattern.include_module

**re_path**: `^platform/services/manage$`
- 视图: views.services.PlatformServicesView if pattern.view_name else pattern.include_module

**re_path**: `^platform/services/$`
- 视图: views.services.PlatformServicesManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/services/(?P<pk>[^/]+)/$`
- 视图: views.services.PlatformServicesManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/plans/manage$`
- 视图: views.services.PlatformPlanView if pattern.view_name else pattern.include_module

**re_path**: `^platform/plans/$`
- 视图: views.services.PlatformPlanManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/services/(?P<service_id>[^/]+)/plans/$`
- 视图: views.services.PlatformPlanManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/services/(?P<service_id>[^/]+)/plans/(?P<plan_id>[^/]+)/$`
- 视图: views.services.PlatformPlanManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/pre-created-instances/manage$`
- 视图: views.services.PreCreatedInstanceView if pattern.view_name else pattern.include_module

**re_path**: `^platform/pre-created-instances/$`
- 视图: views.services.PreCreatedInstanceManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/pre-created-instances/(?P<plan_id>[^/]+)/(?P<uuid>[^/]+)/$`
- 视图: views.services.PreCreatedInstanceManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/smart-advisor/documents/manage$`
- 视图: views.smart_advisor.DocumentaryLinkView if pattern.view_name else pattern.include_module

**re_path**: `^platform/smart-advisor/documents/$`
- 视图: views.smart_advisor.DocumentaryLinkManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/smart-advisor/documents/(?P<pk>[^/]+)/$`
- 视图: views.smart_advisor.DocumentaryLinkManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/smart-advisor/deploy_failure_tips/manage$`
- 视图: views.smart_advisor.DeployFailurePatternView if pattern.view_name else pattern.include_module

**re_path**: `^platform/smart-advisor/deploy_failure_tips/$`
- 视图: views.smart_advisor.DeployFailurePatternManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/smart-advisor/deploy_failure_tips/(?P<pk>[^/]+)/`
- 视图: views.smart_advisor.DeployFailurePatternManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/runtimes/buildpack/manage/$`
- 视图: views.runtimes.BuildPackManageView if pattern.view_name else pattern.include_module

**re_path**: `^platform/runtimes/buildpack/$`
- 视图: views.runtimes.BuildPackAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/runtimes/buildpack/(?P<pk>[^/]+)/$`
- 视图: views.runtimes.BuildPackAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/runtimes/buildpack/(?P<pk>[^/]+)/bind/$`
- 视图: views.runtimes.BuildPackAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/runtimes/slugbuilder/manage/$`
- 视图: views.runtimes.SlugBuilderManageView if pattern.view_name else pattern.include_module

**re_path**: `^platform/runtimes/slugbuilder/$`
- 视图: views.runtimes.SlugBuilderAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/runtimes/slugbuilder/(?P<pk>[^/]+)/$`
- 视图: views.runtimes.SlugBuilderAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/runtime/slugbuilder/(?P<pk>[^/]+)/bind/$`
- 视图: views.runtimes.SlugBuilderAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/runtimes/slugrunner/manage$`
- 视图: views.runtimes.AppSlugRunnerManageView if pattern.view_name else pattern.include_module

**re_path**: `^platform/runtimes/slugrunner/$`
- 视图: views.runtimes.SlugRunnerAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/runtimes/slugrunner/(?P<pk>[^/]+)/$`
- 视图: views.runtimes.SlugRunnerAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/clusters/manage/$`
- 视图: views.engine.clusters.ClusterManageView if pattern.view_name else pattern.include_module

**re_path**: `^platform/clusters/components/manage/$`
- 视图: views.engine.clusters.ClusterComponentManageView if pattern.view_name else pattern.include_module

**re_path**: `^platform/operators/manage/$`
- 视图: views.engine.operator.OperatorManageView if pattern.view_name else pattern.include_module

**re_path**: `^platform/certs/shared/manage/$`
- 视图: views.engine.certs.SharedCertsManageView if pattern.view_name else pattern.include_module

**re_path**: `^platform/sourcectl/source_type_spec/manage/$`
- 视图: views.sourcectl.SourceTypeSpecManageView if pattern.view_name else pattern.include_module

**re_path**: `^platform/sourcectl/source_type_spec/$`
- 视图: views.sourcectl.SourceTypeSpecViewSet if pattern.view_name else pattern.include_module

**re_path**: `^platform/sourcectl/source_type_spec/(?P<pk>[^/]+)/`
- 视图: views.sourcectl.SourceTypeSpecViewSet if pattern.view_name else pattern.include_module

**re_path**: `^applications/$`
- 视图: views.applications.ApplicationListView if pattern.view_name else pattern.include_module

**re_path**: `^applications/evaluations/$`
- 视图: views.applications.ApplicationOperationEvaluationView if pattern.view_name else pattern.include_module

**re_path**: `^applications/evaluations/export/$`
- 视图: views.applications.ApplicationOperationReportExportView if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/overview/$`
- 视图: views.applications.ApplicationOverviewView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.applications.AppEnvConfManageView if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/engine/process_specs/$`
- 视图: views.engine.proc_spec.ProcessSpecManageView if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/engine/source_packages/manage/$`
- 视图: views.engine.package.SourcePackageManageView if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/engine/source_packages/$`
- 视图: views.engine.package.SourcePackageManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.engine.package.SourcePackageManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/engine/egress/manage/$`
- 视图: views.engine.egress.EgressManageView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.engine.egress.EgressManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.engine.egress.EgressManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/engine/config_vars/manage/$`
- 视图: views.engine.config_vars.ConfigVarManageView if pattern.view_name else pattern.include_module

**re_path**: `^application/(?P<code>[^/]+)/engine/config_vars$`
- 视图: views.engine.config_vars.ConfigVarViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.engine.config_vars.ConfigVarViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.engine.config_vars.ConfigVarViewSet if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/engine/runtime/manage/$`
- 视图: views.engine.runtime.RuntimeManageView if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/engine/runtime/$`
- 视图: views.engine.runtime.RuntimeManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: views.engine.runtime.RuntimeManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/services/$`
- 视图: views.services.ApplicationServicesView if pattern.view_name else pattern.include_module

**re_path**: `^api/applications/(?P<code>[^/]+)/services/$`
- 视图: views.services.ApplicationServicesManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/env/(?P<environment>[^/]+)/services/(?P<service_id>[^/]+)/provision/$`
- 视图: views.services.ApplicationServicesManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/services/(?P<service_id>[^/]+)/instances/(?P<instance_id>[^/]+)/$`
- 视图: views.services.ApplicationServicesManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/base_info/memberships/$`
- 视图: views.applications.ApplicationMembersManageView if pattern.view_name else pattern.include_module

**re_path**: `^api/applications/(?P<code>[^/]+)/base_info/memberships/$`
- 视图: views.applications.ApplicationMembersManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/applications/(?P<code>[^/]+)/base_info/memberships/(?P<username>[^/]+)/$`
- 视图: views.applications.ApplicationMembersManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/applications/(?P<code>[^/]+)/base_info/plugin/memberships/$`
- 视图: views.bk_plugins.BKPluginMembersManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/base_info/feature_flags/$`
- 视图: views.applications.ApplicationFeatureFlagsView if pattern.view_name else pattern.include_module

**re_path**: `^api/applications/(?P<code>[^/]+)/base_info/feature_flags/$`
- 视图: views.applications.ApplicationFeatureFlagsViewset if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/engine/custom_domain/$`
- 视图: views.engine.custom_domain.CustomDomainManageView if pattern.view_name else pattern.include_module

**re_path**: `^applications/(?P<code>[^/]+)/engine/log_config/$`
- 视图: views.engine.log_config.LogConfigView if pattern.view_name else pattern.include_module

**re_path**: `^accountmgr/$`
- 视图: views.accountmgr.UserProfilesManageView if pattern.view_name else pattern.include_module

**re_path**: `^accountmgr/userprofiles/$`
- 视图: views.accountmgr.UserProfilesManageView if pattern.view_name else pattern.include_module

**re_path**: `^api/accountmgr/userprofiles/$`
- 视图: views.accountmgr.UserProfilesManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^accountmgr/account_feature_flags/$`
- 视图: views.accountmgr.AccountFeatureFlagManageView if pattern.view_name else pattern.include_module

**re_path**: `^api/accountmgr/account_feature_flags/$`
- 视图: views.accountmgr.AccountFeatureFlagManageViewSet if pattern.view_name else pattern.include_module

**re_path**: `^deployments/$`
- 视图: views.engine.deployments.DeploymentListView if pattern.view_name else pattern.include_module

**re_path**: `^operation/statistics/deploy/apps/$`
- 视图: views.operation.deploy.AppDeployStatisticsView if pattern.view_name else pattern.include_module

**re_path**: `^operation/statistics/deploy/apps/export/$`
- 视图: views.operation.deploy.AppDeployStatisticsView if pattern.view_name else pattern.include_module

**re_path**: `^operation/statistics/deploy/developers/$`
- 视图: views.operation.deploy.DevelopersDeployStatisticsView if pattern.view_name else pattern.include_module

**re_path**: `^operation/statistics/deploy/developers/export/$`
- 视图: views.operation.deploy.DevelopersDeployStatisticsView if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.plat_admin.api_doc.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^docs/$ | None.with_ui if pattern.view_name else (pattern.include_module or '不适用') | full-swagger-ui | 不适用 |  |
| re_path | ^docs/swagger/$ | None.with_ui if pattern.view_name else (pattern.include_module or '不适用') | full-swagger-ui | 不适用 |  |
| re_path | ^docs/redoc/$ | None.with_ui if pattern.view_name else (pattern.include_module or '不适用') | full-redoc | 不适用 |  |
| re_path | ^docs/swagger(?P<format>\.json|\.yaml)$ | None.without_ui if pattern.view_name else (pattern.include_module or '不适用') | full-schema | 不适用 | 分组: format |
| re_path | ^docs/auto/swagger(?P<format>\.json|\.yaml)$ | None.without_ui if pattern.view_name else (pattern.include_module or '不适用') | schema | 不适用 | 分组: format |
| re_path | ^docs/auto/swagger/$ | None.with_ui if pattern.view_name else (pattern.include_module or '不适用') | schema-swagger-ui | 不适用 |  |
| re_path | ^docs/auto/redoc/$ | None.with_ui if pattern.view_name else (pattern.include_module or '不适用') | schema-redoc | 不适用 |  |

#### 模式详情

**re_path**: `^docs/$`
- 视图: None.with_ui if pattern.view_name else pattern.include_module

**re_path**: `^docs/swagger/$`
- 视图: None.with_ui if pattern.view_name else pattern.include_module

**re_path**: `^docs/redoc/$`
- 视图: None.with_ui if pattern.view_name else pattern.include_module

**re_path**: `^docs/swagger(?P<format>\.json|\.yaml)$`
- 视图: None.without_ui if pattern.view_name else pattern.include_module

**re_path**: `^docs/auto/swagger(?P<format>\.json|\.yaml)$`
- 视图: None.without_ui if pattern.view_name else pattern.include_module

**re_path**: `^docs/auto/swagger/$`
- 视图: None.with_ui if pattern.view_name else pattern.include_module

**re_path**: `^docs/auto/redoc/$`
- 视图: None.with_ui if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.plat_admin.system.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^sys/api/uni_applications/query/by_id/$ | None.SysUniApplicationViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.uni_applications.list_by_ids | 不适用 |  |
| re_path | ^sys/api/uni_applications/query/by_username/$ | None.SysUniApplicationViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.uni_applications.list_by_username | 不适用 |  |
| re_path | ^sys/api/uni_applications/list/minimal/$ | None.SysUniApplicationViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.uni_applications.list_minimal_app | 不适用 |  |
| re_path | ^sys/api/bkapps/applications/(?P<code>[^/]+)/cluster_namespaces/$ | None.ClusterNamespaceInfoView if pattern.view_name else (pattern.include_module or '不适用') | sys.api.applications.cluster_namespace.list_by_app_code | 不适用 | 分组: code |
| re_path | 不适用 | None.LessCodeSystemAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.lesscode.query_db_credentials | 不适用 |  |
| re_path | 不适用 | None.LessCodeSystemAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.lesscode.bind_db_service | 不适用 |  |
| re_path | 不适用 | None.SysAddonsAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.applications.addons | 不适用 |  |
| re_path | 不适用 | None.SysAddonsAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.applications.list_addons | 不适用 |  |
| re_path | 不适用 | None.SysAddonsAPIViewSet if pattern.view_name else (pattern.include_module or '不适用') | sys.api.applications.retrieve_specs_by_uuid | 不适用 |  |

#### 模式详情

**re_path**: `^sys/api/uni_applications/query/by_id/$`
- 视图: None.SysUniApplicationViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/uni_applications/query/by_username/$`
- 视图: None.SysUniApplicationViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/uni_applications/list/minimal/$`
- 视图: None.SysUniApplicationViewSet if pattern.view_name else pattern.include_module

**re_path**: `^sys/api/bkapps/applications/(?P<code>[^/]+)/cluster_namespaces/$`
- 视图: None.ClusterNamespaceInfoView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.LessCodeSystemAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.LessCodeSystemAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.SysAddonsAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.SysAddonsAPIViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.SysAddonsAPIViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.applications.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/bkapps/applications/v2/$ | None.ApplicationCreateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.create_v2 | 不适用 |  |
| re_path | ^api/bkapps/third-party/$ | None.ApplicationCreateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.create.third_party | 不适用 |  |
| re_path | ^api/bkapps/cloud-native/$ | None.ApplicationCreateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.create.cloud_native | 不适用 |  |
| re_path | ^api/bkapps/applications/creation/options/$ | None.ApplicationCreateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.creation.options | 不适用 |  |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/$ | None.ApplicationViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.detail | 不适用 | 分组: code |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/overview/$ | None.ApplicationViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.overview | 不适用 | 分组: code |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/logo/$ | None.ApplicationLogoViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.logo | 不适用 | 分组: code |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/secret_verifications/$ | None.ApplicationExtraInfoViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.detail.secret | 不适用 | 分组: code |
| re_path | ^api/bkapps/applications/lists/detailed$ | None.ApplicationListViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.lists.detailed | 不适用 |  |
| re_path | ^api/bkapps/applications/lists/minimal$ | None.ApplicationListViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.lists.minimal | 不适用 |  |
| re_path | ^api/bkapps/applications/lists/search$ | None.ApplicationListViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.lists.search | 不适用 |  |
| re_path | ^api/bkapps/applications/lists/evaluation/$ | None.ApplicationListViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.lists.evaluation | 不适用 |  |
| re_path | ^api/bkapps/applications/lists/evaluation/issue_count/$ | None.ApplicationListViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.lists.evaluation.issue_count | 不适用 |  |
| re_path | ^api/bkapps/applications/lists/idle/$ | None.ApplicationListViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.lists.idle | 不适用 |  |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/members/$ | None.ApplicationMembersViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.members | 不适用 | 分组: code |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/members/(?P<user_id>[0-9a-z]+)/?$ | None.ApplicationMembersViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.members.detail | 不适用 | 分组: code, user_id |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/leave/?$ | None.ApplicationMembersViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.members.leave | 不适用 | 分组: code |
| re_path | ^api/bkapps/applications/members/roles/$ | None.ApplicationMembersViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.members.get_roles | 不适用 |  |

#### 模式详情

**re_path**: `^api/bkapps/applications/v2/$`
- 视图: None.ApplicationCreateViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/third-party/$`
- 视图: None.ApplicationCreateViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/cloud-native/$`
- 视图: None.ApplicationCreateViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/creation/options/$`
- 视图: None.ApplicationCreateViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/$`
- 视图: None.ApplicationViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/overview/$`
- 视图: None.ApplicationViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/logo/$`
- 视图: None.ApplicationLogoViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/secret_verifications/$`
- 视图: None.ApplicationExtraInfoViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/lists/detailed$`
- 视图: None.ApplicationListViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/lists/minimal$`
- 视图: None.ApplicationListViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/lists/search$`
- 视图: None.ApplicationListViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/lists/evaluation/$`
- 视图: None.ApplicationListViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/lists/evaluation/issue_count/$`
- 视图: None.ApplicationListViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/lists/idle/$`
- 视图: None.ApplicationListViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/members/$`
- 视图: None.ApplicationMembersViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/members/(?P<user_id>[0-9a-z]+)/?$`
- 视图: None.ApplicationMembersViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/leave/?$`
- 视图: None.ApplicationMembersViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/members/roles/$`
- 视图: None.ApplicationMembersViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.bk_lesscode.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/bkapps/lesscode/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/$ | None.LesscodeModuleViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.lesscode.info | 不适用 | 分组: code, module_name |

#### 模式详情

**re_path**: `^api/bkapps/lesscode/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/$`
- 视图: None.LesscodeModuleViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.bkapp_model.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.CNativeAppManifestExtViewset if pattern.view_name else (pattern.include_module or '不适用') | api.cnative.retrieve_manifest_ext | 不适用 |  |
| re_path | 不适用 | None.BkAppModelManifestsViewset if pattern.view_name else (pattern.include_module or '不适用') | api.bkapp_model.current_manifests | 不适用 |  |
| re_path | 不适用 | None.ModuleProcessSpecViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.bkapp_model.process_specs | 不适用 |  |
| re_path | 不适用 | None.ModuleDeployHookViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.bkapp_model.deploy_hooks | 不适用 |  |
| re_path | 不适用 | None.ModuleDeployHookViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.bkapp_model.deploy_hooks.detail | 不适用 |  |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/svc_disc/$ | None.SvcDiscConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.svc_disc | 不适用 | 分组: code |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/domain_resolution/$ | None.DomainResolutionViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.domain_resolution | 不适用 | 分组: code |

#### 模式详情

**re_path**: `不适用`
- 视图: None.CNativeAppManifestExtViewset if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.BkAppModelManifestsViewset if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleProcessSpecViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleDeployHookViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleDeployHookViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/svc_disc/$`
- 视图: None.SvcDiscConfigViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/domain_resolution/$`
- 视图: None.DomainResolutionViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.engine.processes.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.ApplicationProcessWebConsoleViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.webconsole | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.ApplicationProcessWebConsoleViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.engine.streaming.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^streams/(?P<channel_id>[0-9a-f-]{32,36})$ | None.StreamViewSet if pattern.view_name else (pattern.include_module or '不适用') | streaming.stream | 不适用 | 分组: channel_id |
| re_path | ^streams/(?P<channel_id>[0-9a-f-]{32,36})/history_events$ | None.StreamViewSet if pattern.view_name else (pattern.include_module or '不适用') | streaming.stream.history_events | 不适用 | 分组: channel_id |
| re_path | ^streams/__debugger__$ | None.StreamDebuggerView if pattern.view_name else (pattern.include_module or '不适用') | streaming.debugger | 不适用 |  |
| re_path | ^streams/__void__$ | None.VoidViewset if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | ^streams/__void_with_content__$ | None.VoidViewset if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**re_path**: `^streams/(?P<channel_id>[0-9a-f-]{32,36})$`
- 视图: None.StreamViewSet if pattern.view_name else pattern.include_module

**re_path**: `^streams/(?P<channel_id>[0-9a-f-]{32,36})/history_events$`
- 视图: None.StreamViewSet if pattern.view_name else pattern.include_module

**re_path**: `^streams/__debugger__$`
- 视图: None.StreamDebuggerView if pattern.view_name else pattern.include_module

**re_path**: `^streams/__void__$`
- 视图: None.VoidViewset if pattern.view_name else pattern.include_module

**re_path**: `^streams/__void_with_content__$`
- 视图: None.VoidViewset if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.engine.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.ReleasedInfoViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.released_info.get_current_info | 不适用 |  |
| re_path | 不适用 | None.ReleasedInfoViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.released_info.get_current_state | 不适用 |  |
| re_path | 不适用 | None.ReleasesViewset if pattern.view_name else (pattern.include_module or '不适用') | api.releases.release | 不适用 |  |
| re_path | 不适用 | None.ConfigVarViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.config_vars | 不适用 |  |
| re_path | 不适用 | None.ConfigVarViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.config_vars.single | 不适用 |  |
| re_path | 不适用 | None.ConfigVarViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.config_vars.clone | 不适用 |  |
| re_path | 不适用 | None.ConfigVarViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.config_vars.batch | 不适用 |  |
| re_path | 不适用 | None.ConfigVarImportExportViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.config_vars.import_by_file | 不适用 |  |
| re_path | 不适用 | None.ConfigVarImportExportViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.config_vars.export_to_file | 不适用 |  |
| re_path | 不适用 | None.ConfigVarImportExportViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.config_vars.template | 不适用 |  |
| re_path | 不适用 | None.PresetConfigVarViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.preset_config_vars | 不适用 |  |
| re_path | 不适用 | None.ConfigVarViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.config_vars_by_key | 不适用 |  |
| re_path | 不适用 | None.DeploymentViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.deploy.result | 不适用 |  |
| re_path | 不适用 | None.DeploymentViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.deploy.export_log | 不适用 |  |
| re_path | 不适用 | None.DeploymentViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.deploy.release_interruptions | 不适用 |  |
| re_path | 不适用 | None.DeploymentViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.deploy.lists | 不适用 |  |
| re_path | 不适用 | None.DeploymentViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.deploy | 不适用 |  |
| re_path | 不适用 | None.DeploymentViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.deploy.resumable | 不适用 |  |
| re_path | 不适用 | None.DeploymentViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.deploy.check_preparations | 不适用 |  |
| re_path | 不适用 | None.OfflineViewset if pattern.view_name else (pattern.include_module or '不适用') | api.offline | 不适用 |  |
| re_path | 不适用 | None.OfflineViewset if pattern.view_name else (pattern.include_module or '不适用') | api.offline.resumable | 不适用 |  |
| re_path | 不适用 | None.OfflineViewset if pattern.view_name else (pattern.include_module or '不适用') | api.deploy.result | 不适用 |  |
| re_path | 不适用 | None.OperationsViewset if pattern.view_name else (pattern.include_module or '不适用') | api.deploy_operation.lists | 不适用 |  |
| re_path | 不适用 | None.ImageArtifactViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.build.image.list | 不适用 |  |
| re_path | 不适用 | None.ImageArtifactViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.build.image.detail | 不适用 |  |
| re_path | 不适用 | None.BuildProcessViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.build_process.list | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.ReleasedInfoViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ReleasedInfoViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ReleasesViewset if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ConfigVarViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ConfigVarViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ConfigVarViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ConfigVarViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ConfigVarImportExportViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ConfigVarImportExportViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ConfigVarImportExportViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.PresetConfigVarViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ConfigVarViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DeploymentViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DeploymentViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DeploymentViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DeploymentViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DeploymentViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DeploymentViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DeploymentViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.OfflineViewset if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.OfflineViewset if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.OfflineViewset if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.OperationsViewset if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ImageArtifactViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ImageArtifactViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.BuildProcessViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.environments.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.ModuleEnvRoleProtectionViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.environments.role_restricts | 不适用 |  |
| re_path | 不适用 | None.ModuleEnvRoleProtectionViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.environments.role_restricts_batch | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.ModuleEnvRoleProtectionViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleEnvRoleProtectionViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.evaluation.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | 不适用 | None.IdleAppNotificationMuteRuleViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.evaluation.idle_notification_mute_rules | 不适用 |  |

#### 模式详情

**re_path**: `不适用`
- 视图: None.IdleAppNotificationMuteRuleViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.mgrlegacy.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/mgrlegacy/applications/$ | None.LegacyAppViewset if pattern.view_name else (pattern.include_module or '不适用') | api.mgrlegacy.applications.list | 不适用 |  |
| re_path | 不适用 | None.LegacyAppViewset if pattern.view_name else (pattern.include_module or '不适用') | api.mgrlegacy.applications.exposed_url_info | 不适用 |  |
| re_path | ^api/mgrlegacy/migrations/progress/$ | None.MigrationCreateViewset if pattern.view_name else (pattern.include_module or '不适用') | api.mgrlegacy.migrations.progress.create | 不适用 |  |
| re_path | ^api/mgrlegacy/migrations/progress/(?P<id>\d+)/state | None.MigrationDetailViewset if pattern.view_name else (pattern.include_module or '不适用') | api.mgrlegacy.migrations.progress.state | 不适用 | 分组: id |
| re_path | ^api/mgrlegacy/migrations/progress/(?P<id>\d+)/old_state | None.MigrationDetailViewset if pattern.view_name else (pattern.include_module or '不适用') | api.mgrlegacy.migrations.progress.old_state | 不适用 | 分组: id |
| re_path | ^api/mgrlegacy/migrations/progress/(?P<id>\d+)/confirm | None.MigrationConfirmViewset if pattern.view_name else (pattern.include_module or '不适用') | api.mgrlegacy.migrations.progress.confirm | 不适用 | 分组: id |
| re_path | ^api/mgrlegacy/migrations/progress/(?P<id>\d+)/rollback | None.MigrationDetailViewset if pattern.view_name else (pattern.include_module or '不适用') | api.mgrlegacy.migrations.progress.rollback | 不适用 | 分组: id |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/migration/info$ | None.ApplicationMigrationInfoAPIView if pattern.view_name else (pattern.include_module or '不适用') | api.applications.migration.info | 不适用 | 分组: code |
| re_path | ^api/mgrlegacy/cloud-native/applications/(?P<code>[^/]+)/migrate/$ | None.CNativeMigrationViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code |
| re_path | ^api/mgrlegacy/cloud-native/applications/(?P<code>[^/]+)/rollback/$ | None.CNativeMigrationViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code |
| re_path | ^api/mgrlegacy/cloud-native/applications/(?P<code>[^/]+)/migration_processes/$ | None.CNativeMigrationViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code |
| re_path | ^api/mgrlegacy/cloud-native/applications/(?P<code>[^/]+)/migration_processes/latest/$ | None.CNativeMigrationViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code |
| re_path | ^api/mgrlegacy/cloud-native/migration_processes/(?P<process_id>\d+)/$ | None.CNativeMigrationViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: process_id |
| re_path | ^api/mgrlegacy/cloud-native/migration_processes/(?P<process_id>\d+)/confirm/$ | None.CNativeMigrationViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: process_id |
| re_path | 不适用 | None.DefaultAppProcessViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | ^api/mgrlegacy/applications/(?P<code>[^/]+)/entrances/$ | None.DefaultAppEntranceViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code |
| re_path | ^api/mgrlegacy/applications/(?P<code>[^/]+)/checklist_info/$ | None.RetrieveChecklistInfoViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: code |

#### 模式详情

**re_path**: `^api/mgrlegacy/applications/$`
- 视图: None.LegacyAppViewset if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.LegacyAppViewset if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/migrations/progress/$`
- 视图: None.MigrationCreateViewset if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/migrations/progress/(?P<id>\d+)/state`
- 视图: None.MigrationDetailViewset if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/migrations/progress/(?P<id>\d+)/old_state`
- 视图: None.MigrationDetailViewset if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/migrations/progress/(?P<id>\d+)/confirm`
- 视图: None.MigrationConfirmViewset if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/migrations/progress/(?P<id>\d+)/rollback`
- 视图: None.MigrationDetailViewset if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/migration/info$`
- 视图: None.ApplicationMigrationInfoAPIView if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/cloud-native/applications/(?P<code>[^/]+)/migrate/$`
- 视图: None.CNativeMigrationViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/cloud-native/applications/(?P<code>[^/]+)/rollback/$`
- 视图: None.CNativeMigrationViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/cloud-native/applications/(?P<code>[^/]+)/migration_processes/$`
- 视图: None.CNativeMigrationViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/cloud-native/applications/(?P<code>[^/]+)/migration_processes/latest/$`
- 视图: None.CNativeMigrationViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/cloud-native/migration_processes/(?P<process_id>\d+)/$`
- 视图: None.CNativeMigrationViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/cloud-native/migration_processes/(?P<process_id>\d+)/confirm/$`
- 视图: None.CNativeMigrationViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.DefaultAppProcessViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/applications/(?P<code>[^/]+)/entrances/$`
- 视图: None.DefaultAppEntranceViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/mgrlegacy/applications/(?P<code>[^/]+)/checklist_info/$`
- 视图: None.RetrieveChecklistInfoViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.modules.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/modules/$ | None.ModuleViewSet if pattern.view_name else (pattern.include_module or '不适用') | modules | 不适用 | 分组: code |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/$ | None.ModuleViewSet if pattern.view_name else (pattern.include_module or '不适用') | module.actions | 不适用 | 分组: code, module_name |
| re_path | 不适用 | None.ModuleViewSet if pattern.view_name else (pattern.include_module or '不适用') | module.set_default | 不适用 |  |
| re_path | ^api/bkapps/cloud-native/(?P<code>[^/]+)/modules/$ | None.ModuleViewSet if pattern.view_name else (pattern.include_module or '不适用') | module.create.cloud_native | 不适用 | 分组: code |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/runtime/list/$ | None.ModuleRuntimeViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.modules.runtime.available_list | 不适用 | 分组: code, module_name |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/runtime/$ | None.ModuleRuntimeViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.modules.runtime | 不适用 | 分组: code, module_name |
| re_path | 不适用 | None.ModuleRuntimeOverviewView if pattern.view_name else (pattern.include_module or '不适用') | api.modules.deployment.meta_info | 不适用 |  |
| re_path | 不适用 | None.ModuleBuildConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.modules.build_config | 不适用 |  |
| re_path | 不适用 | None.ModuleBuildConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.modules.bp_runtime.available_list | 不适用 |  |
| re_path | 不适用 | None.ModuleDeployConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.modules.deploy_config | 不适用 |  |
| re_path | 不适用 | None.ModuleDeployConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.modules.deploy_config.hooks.upsert | 不适用 |  |
| re_path | 不适用 | None.ModuleDeployConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.modules.deploy_config.hooks.disable | 不适用 |  |
| re_path | 不适用 | None.ModuleDeployConfigViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.modules.deploy_config.procfile.update | 不适用 |  |
| re_path | ^api/bkapps/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/template/$ | None.ModuleTemplateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.modules.template | 不适用 | 分组: code, module_name |

#### 模式详情

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/modules/$`
- 视图: None.ModuleViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/$`
- 视图: None.ModuleViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/cloud-native/(?P<code>[^/]+)/modules/$`
- 视图: None.ModuleViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/runtime/list/$`
- 视图: None.ModuleRuntimeViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/runtime/$`
- 视图: None.ModuleRuntimeViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleRuntimeOverviewView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleBuildConfigViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleBuildConfigViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleDeployConfigViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleDeployConfigViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleDeployConfigViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleDeployConfigViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/applications/(?P<code>[^/]+)/modules/(?P<module_name>[^/]+)/template/$`
- 视图: None.ModuleTemplateViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.smart_app.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/sourcectl/smart_packages/$ | None.SMartPackageCreatorViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.smart_packages | 不适用 |  |
| re_path | ^api/sourcectl/smart_packages/prepared/$ | None.SMartPackageCreatorViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.smart_packages.prepared | 不适用 |  |
| re_path | ^api/bkapps/s-mart/$ | None.SMartPackageCreatorViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.create.smart_packages.upload | 不适用 |  |
| re_path | ^api/bkapps/s-mart/confirm/$ | None.SMartPackageCreatorViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.applications.create.smart_packages.confirm | 不适用 |  |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/source_package/$ | None.SMartPackageManagerViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.source_package.s-mart.list | 不适用 | 分组: code |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/source_package/stash/$ | None.SMartPackageManagerViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.source_package.s-mart.stash | 不适用 | 分组: code |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/source_package/commit/(?P<signature>[^/]+)/$ | None.SMartPackageManagerViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.source_package.s-mart.commit | 不适用 | 分组: code, signature |
| re_path | api/bkapps/applications/(?P<code>[^/]+)/source_package/(?P<pk>[^/]+)/$ | None.SMartPackageManagerViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.source_package.s-mart.detail | 不适用 | 分组: code, pk |

#### 模式详情

**re_path**: `^api/sourcectl/smart_packages/$`
- 视图: None.SMartPackageCreatorViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/sourcectl/smart_packages/prepared/$`
- 视图: None.SMartPackageCreatorViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/s-mart/$`
- 视图: None.SMartPackageCreatorViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/bkapps/s-mart/confirm/$`
- 视图: None.SMartPackageCreatorViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/source_package/$`
- 视图: None.SMartPackageManagerViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/source_package/stash/$`
- 视图: None.SMartPackageManagerViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/source_package/commit/(?P<signature>[^/]+)/$`
- 视图: None.SMartPackageManagerViewSet if pattern.view_name else pattern.include_module

**re_path**: `api/bkapps/applications/(?P<code>[^/]+)/source_package/(?P<pk>[^/]+)/$`
- 视图: None.SMartPackageManagerViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.sourcectl.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/sourcectl/bksvn/accounts/$ | None.SvnAccountViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.bksvn.accounts | 不适用 |  |
| re_path | ^api/sourcectl/bksvn/accounts/(?P<id>\d+)/reset/$ | None.SvnAccountViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.bksvn.accounts.reset | 不适用 | 分组: id |
| re_path | ^api/sourcectl/(?P<source_control_type>.+)/repos/ | None.GitRepoViewSet if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: source_control_type |
| re_path | ^api/sourcectl/providers/$ | None.AccountAllowAppSourceControlView if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.providers.list | 不适用 |  |
| re_path | 不适用 | None.ModuleSourceProvidersViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.module_providers.list | 不适用 |  |
| re_path | ^api/sourcectl/init_templates/(?P<code>[^/]+)/$ | None.ModuleInitTemplateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.template.generator | 不适用 | 分组: code |
| re_path | 不适用 | None.ModuleInitTemplateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.init_template | 不适用 |  |
| re_path | 不适用 | None.RepoBackendControlViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.repo.modify | 不适用 |  |
| re_path | 不适用 | None.ModuleSourcePackageViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.source_package.create_via_url | 不适用 |  |
| re_path | 不适用 | None.ModuleSourcePackageViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.sourcectl.source_package | 不适用 |  |

#### 模式详情

**re_path**: `^api/sourcectl/bksvn/accounts/$`
- 视图: None.SvnAccountViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/sourcectl/bksvn/accounts/(?P<id>\d+)/reset/$`
- 视图: None.SvnAccountViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/sourcectl/(?P<source_control_type>.+)/repos/`
- 视图: None.GitRepoViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/sourcectl/providers/$`
- 视图: None.AccountAllowAppSourceControlView if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleSourceProvidersViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/sourcectl/init_templates/(?P<code>[^/]+)/$`
- 视图: None.ModuleInitTemplateViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleInitTemplateViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.RepoBackendControlViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleSourcePackageViewSet if pattern.view_name else pattern.include_module

**re_path**: `不适用`
- 视图: None.ModuleSourcePackageViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.platform.templates.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | ^api/bkapps/(?P<tpl_type>[^/]+)/tmpls/$ | None.TemplateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.templates.list_tmpls | 不适用 | 分组: tpl_type |
| re_path | ^api/tmpls/(?P<tpl_type>[^/]+)/region/(?P<region>[^/]+)/$ | None.RegionTemplateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.templates.list | 不适用 | 分组: tpl_type, region |
| re_path | ^api/tmpls/(?P<tpl_type>[^/]+)/region/(?P<region>[^/]+)/template/(?P<tpl_name>[^/]+)$ | None.RegionTemplateViewSet if pattern.view_name else (pattern.include_module or '不适用') | api.templates.detail | 不适用 | 分组: tpl_type, region, tpl_name |

#### 模式详情

**re_path**: `^api/bkapps/(?P<tpl_type>[^/]+)/tmpls/$`
- 视图: None.TemplateViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/tmpls/(?P<tpl_type>[^/]+)/region/(?P<region>[^/]+)/$`
- 视图: None.RegionTemplateViewSet if pattern.view_name else pattern.include_module

**re_path**: `^api/tmpls/(?P<tpl_type>[^/]+)/region/(?P<region>[^/]+)/template/(?P<tpl_name>[^/]+)$`
- 视图: None.RegionTemplateViewSet if pattern.view_name else pattern.include_module


---


### URL配置模块: apiserver.paasng.paasng.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^admin42/ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^admin42/ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | ^i18n/setlang/$ | django.views.i18n.set_language if pattern.view_name else (pattern.include_module or '不适用') | set_language | 不适用 |  |
| include | 不适用 | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | 不适用 | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | 不适用 | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | 不适用 | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | 不适用 | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | 不适用 | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | 不适用 | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | 不适用 | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | 不适用 | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^notice/ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | notice |  |

#### 模式详情

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^admin42/`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^admin42/`
- 视图: None.None if pattern.view_name else pattern.include_module

**re_path**: `^i18n/setlang/$`
- 视图: django.views.i18n.set_language if pattern.view_name else pattern.include_module

**include**: `不适用`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `不适用`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `不适用`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `不适用`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `不适用`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `不适用`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `不适用`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `不适用`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `不适用`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^notice/`
- 视图: None.None if pattern.view_name else pattern.include_module


---


### URL配置模块: svc-bkrepo.svc_bk_repo.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | ^admin/ | None.urls if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**re_path**: `^admin/`
- 视图: None.urls if pattern.view_name else pattern.include_module


---


### URL配置模块: svc-bkrepo.svc_bk_repo.vendor.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | healthz/$ | svc_bk_repo.vendor.views.HealthzView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | web/instances/(?P<instance_id>[^/]+)/$ | svc_bk_repo.vendor.views.BKRepoIndexView if pattern.view_name else (pattern.include_module or '不适用') | instance.index | 不适用 | 分组: instance_id |
| re_path | web/instances/(?P<instance_id>[^/]+)/(?P<bucket>[^/]+)/$ | svc_bk_repo.vendor.views.BKRepoManageView if pattern.view_name else (pattern.include_module or '不适用') | instance.manage | 不适用 | 分组: instance_id, bucket |

#### 模式详情

**re_path**: `healthz/$`
- 视图: svc_bk_repo.vendor.views.HealthzView if pattern.view_name else pattern.include_module

**re_path**: `web/instances/(?P<instance_id>[^/]+)/$`
- 视图: svc_bk_repo.vendor.views.BKRepoIndexView if pattern.view_name else pattern.include_module

**re_path**: `web/instances/(?P<instance_id>[^/]+)/(?P<bucket>[^/]+)/$`
- 视图: svc_bk_repo.vendor.views.BKRepoManageView if pattern.view_name else pattern.include_module


---


### URL配置模块: svc-mysql.svc_mysql.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | ^admin/ | None.urls if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**re_path**: `^admin/`
- 视图: None.urls if pattern.view_name else pattern.include_module


---


### URL配置模块: svc-mysql.svc_mysql.vendor.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | healthz/ | svc_mysql.vendor.views.HealthzView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | web/instances/(?P<instance_id>[^/]*)/$ | svc_mysql.vendor.views.MySQLIndexView if pattern.view_name else (pattern.include_module or '不适用') | instance.index | 不适用 | 分组: instance_id |

#### 模式详情

**re_path**: `healthz/`
- 视图: svc_mysql.vendor.views.HealthzView if pattern.view_name else pattern.include_module

**re_path**: `web/instances/(?P<instance_id>[^/]*)/$`
- 视图: svc_mysql.vendor.views.MySQLIndexView if pattern.view_name else pattern.include_module


---


### URL配置模块: svc-otel.svc_otel.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | ^admin/ | None.urls if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**re_path**: `^admin/`
- 视图: None.urls if pattern.view_name else pattern.include_module


---


### URL配置模块: svc-otel.svc_otel.vendor.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | healthz/ | None.HealthzView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**re_path**: `healthz/`
- 视图: None.HealthzView if pattern.view_name else pattern.include_module


---


### URL配置模块: svc-rabbitmq.monitor.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | metrics | None.AuthenticatedMetricsView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**re_path**: `metrics`
- 视图: None.AuthenticatedMetricsView if pattern.view_name else pattern.include_module


---


### URL配置模块: svc-rabbitmq.svc_rabbitmq.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| include | ^ | None.None if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | ^admin/ | None.urls if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | ^accounts/login/ | None.RedirectView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |

#### 模式详情

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**include**: `^`
- 视图: None.None if pattern.view_name else pattern.include_module

**re_path**: `^admin/`
- 视图: None.urls if pattern.view_name else pattern.include_module

**re_path**: `^accounts/login/`
- 视图: None.RedirectView if pattern.view_name else pattern.include_module


---


### URL配置模块: svc-rabbitmq.vendor.urls

| 类型 | 模式 | 视图 | 名称 | 命名空间 | 详情 |
|------|------|------|------|---------|------|
| re_path | healthz/ | vendor.views.healthz if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 |  |
| re_path | cluster/(?P<cluster_id>\d+)/metrics | vendor.views.ClusterMinimalMetricsView if pattern.view_name else (pattern.include_module or '不适用') | 不适用 | 不适用 | 分组: cluster_id |

#### 模式详情

**re_path**: `healthz/`
- 视图: vendor.views.healthz if pattern.view_name else pattern.include_module

**re_path**: `cluster/(?P<cluster_id>\d+)/metrics`
- 视图: vendor.views.ClusterMinimalMetricsView if pattern.view_name else pattern.include_module


---

