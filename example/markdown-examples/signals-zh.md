# 信号使用分析

## 元数据
- **scanner_name**: signal

## 概要信息
- **总数量**: 39
- **已扫描文件数**: 2368
- **扫描耗时**: 11490 毫秒

- **Django 接收器**: 54
- **Django 发送器**: 31
- **Celery 接收器**: 1
- **Celery 发送器**: 0
- **自定义信号定义**: 20
- **未使用的自定义信号**: 0

## 结果详情

### post_save

**类型**: django  
**类别**: model_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paas_wl/bk_app/applications/handlers.py | 24 | on_app_created | 不适用 | WlApp | 不适用 |
| apiserver/paasng/paas_wl/infras/resources/generation/handlers.py | 24 | set_default_version | 不适用 | WlApp | 不适用 |
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 262 | application_oauth_handler | 不适用 | OAuth2Client | 不适用 |
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 305 | market_config_update_handler | 不适用 | MarketConfig | 不适用 |
| apiserver/paasng/paasng/bk_plugins/pluginscenter/handlers.py | 27 | update_release_status_when_stage_status_change | 不适用 | PluginReleaseStage | 不适用 |
| apiserver/paasng/paasng/misc/audit/handlers.py | 57 | on_app_operation_created | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/misc/audit/handlers.py | 77 | on_model_post_save | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py | 110 | on_model_post_save | 不适用 | Deployment | 不适用 |


---


### cnative_custom_domain_updated

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paas_wl/bk_app/cnative/specs/handlers.py | 30 | on_custom_domain_updated | 不适用 | 不适用 | 不适用 |


---


### application_default_module_switch

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paas_wl/bk_app/cnative/specs/handlers.py | 36 | sync_default_entrances_for_cnative_module_switching | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paas_wl/workloads/networking/entrance/handlers.py | 31 | sync_default_entrances_for_module_switching | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/accessories/publish/market/handlers.py | 24 | update_market_config_source_module | 不适用 | 不适用 | 不适用 |


---


### post_appenv_deploy

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/ci/handlers.py | 39 | start_ci_job | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 381 | sync_release_record | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/misc/audit/handlers.py | 102 | on_deploy_finished | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/handlers.py | 32 | create_rules_after_deploy | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/misc/monitoring/monitor/dashboards/handlers.py | 30 | import_dashboard_after_deploy | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/engine/handlers.py | 76 | update_last_deployed_date | 不适用 | 不适用 | 不适用 |


---


### on_release_created

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/paas_analysis/handlers.py | 28 | on_release_created_callback | 不适用 | 不适用 | 不适用 |


---


### application_member_updated

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 145 | update_console_members | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/handlers.py | 40 | update_notice_group | 不适用 | 不适用 | 不适用 |


---


### prepare_use_application_code

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 176 | validate_app_code_uniquely | 不适用 | 不适用 | 不适用 |


---


### prepare_use_application_name

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 186 | validate_app_name_uniquely | 不适用 | 不适用 | 不适用 |


---


### before_finishing_application_creation

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 201 | register_app_core_data | 不适用 | 不适用 | 不适用 |


---


### prepare_change_application_name

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 226 | on_change_application_name | 不适用 | 不适用 | 不适用 |


---


### module_environment_offline_success

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 273 | offline_handler | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py | 97 | on_environment_offlined | 不适用 | 不适用 | 不适用 |


---


### application_logo_updated

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 407 | sync_logo | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py | 124 | extra_setup_logo | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py | 135 | duplicate_logo_to_extra_bucket | 不适用 | 不适用 | 不适用 |


---


### post_create_application

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/bk_plugins/bk_plugins/handlers.py | 34 | on_plugin_app_created | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py | 56 | initialize_application_members | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py | 69 | turn_on_bk_log_feature_for_app | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py | 75 | extra_setup_tasks | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py | 82 | update_app_counter | 不适用 | 不适用 | 不适用 |


---


### pre_appenv_deploy

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/bk_plugins/bk_plugins/handlers.py | 49 | on_pre_deployment | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/engine/handlers.py | 60 | attach_all_phases | 不适用 | 不适用 | 不适用 |


---


### pre_phase_start

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/handlers.py | 39 | start_phase | 不适用 | 不适用 | 不适用 |


---


### post_phase_end

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/handlers.py | 46 | end_phase | 不适用 | 不适用 | 不适用 |


---


### processes_updated

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/processes/handlers.py | 38 | _on_processes_updated | 不适用 | 不适用 | 不适用 |


---


### setting_changed

**类型**: django  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/source_types.py | 389 | reload_settings | 不适用 | 不适用 | 不适用 |


---


### product_create_or_update_by_operator

**类型**: django  
**类别**: custom_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 108 | on_product_create_or_updated | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/applications/management/commands/create_3rd_party_apps.py | 217 | send_method | product | 不适用 |
| apiserver/paasng/paasng/platform/declarative/application/controller.py | 277 | send_method | self.__class__ | 不适用 |
| apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/product.py | 81 | send_method | self.__class__ | 不适用 |

---


### post_cnative_env_deploy

**类型**: django  
**类别**: custom_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/misc/audit/handlers.py | 121 | on_cnative_deploy_finished | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/deploy/bg_wait/wait_bkapp.py | 252 | send_method | 不适用 | 不适用 |

---


### post_create_application

**类型**: django  
**类别**: custom_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/tests/api/test_applications.py | 65 | turn_on_bk_log_feature_for_app | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/tests/conftest.py | 407 | turn_on_bk_log_feature_for_app | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/tests/conftest.py | 412 | turn_on_bk_log_feature_for_app | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/applications/utils.py | 144 | send_method | create_third_app | 不适用 |
| apiserver/paasng/paasng/platform/applications/views.py | 748 | send_method | self.__class__ | 不适用 |
| apiserver/paasng/paasng/platform/applications/views.py | 873 | send_method | self.__class__ | 不适用 |
| apiserver/paasng/paasng/platform/declarative/application/controller.py | 113 | send_method | self.__class__ | 不适用 |
| apiserver/paasng/tests/utils/helpers.py | 180 | send_method | create_app | 不适用 |
| apiserver/paasng/tests/utils/helpers.py | 549 | send_method | create_app | 不适用 |

---


### application_member_updated

**类型**: django  
**类别**: custom_signals  


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/applications/views.py | 952 | send_method | application | 不适用 |
| apiserver/paasng/paasng/platform/applications/views.py | 972 | send_method | application | 不适用 |
| apiserver/paasng/paasng/platform/applications/views.py | 989 | send_method | application | 不适用 |
| apiserver/paasng/paasng/platform/applications/views.py | 1007 | send_method | application | 不适用 |

---


### application_default_module_switch

**类型**: django  
**类别**: custom_signals  


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/declarative/application/controller.py | 234 | send_method | application | 不适用 |
| apiserver/paasng/paasng/platform/modules/views.py | 267 | send_method | application | 不适用 |

---


### application_logo_updated

**类型**: django  
**类别**: custom_signals  


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/declarative/application/controller.py | 267 | send_method | application | 不适用 |

---


### prepare_change_application_name

**类型**: django  
**类别**: custom_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/tests/paasng/platform/declarative/application/conftest.py | 31 | on_change_application_name | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/declarative/application/fields.py | 59 | send_method | self.application | 不适用 |

---


### module_environment_offline_success

**类型**: django  
**类别**: custom_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/evaluation/handlers.py | 26 | on_environment_offline_succeed | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/deploy/archive/base.py | 119 | send_method | OfflineOperation | 不适用 |

---


### post_phase_end

**类型**: django  
**类别**: custom_signals  


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/workflow/flow.py | 176 | send_method | 不适用 | 不适用 |

---


### post_appenv_deploy

**类型**: django  
**类别**: custom_signals  


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/workflow/flow.py | 193 | send_method | 不适用 | 不适用 |
| apiserver/paasng/tests/paasng/platform/engine/test_handlers.py | 37 | send_method | 不适用 | 不适用 |

---


### post_change_app_router

**类型**: django  
**类别**: custom_signals  


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/entrance.py | 42 | send_method | self | 不适用 |

---


### rollback_change_app_router

**类型**: django  
**类别**: custom_signals  


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/entrance.py | 55 | send_method | self | 不适用 |

---


### on_module_initialized

**类型**: django  
**类别**: custom_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/modules/handlers.py | 27 | async_setup_module_log_model | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/modules/manager.py | 370 | send_method | initialize_smart_module | 不适用 |
| apiserver/paasng/paasng/platform/modules/manager.py | 440 | send_method | initialize_module | 不适用 |

---


### empty_svn_accounts_fetched

**类型**: django  
**类别**: custom_signals  


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/views.py | 103 | send_method | self | 不适用 |

---


### svn_account_updated

**类型**: django  
**类别**: custom_signals  


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/views.py | 131 | send_method | self | 不适用 |

---


### repo_updated

**类型**: django  
**类别**: custom_signals  


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/views.py | 390 | send_method | self | 不适用 |

---


### before_finishing_application_creation

**类型**: django  
**类别**: custom_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/tests/conftest.py | 406 | register_app_core_data | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/tests/conftest.py | 419 | register_app_core_data | 不适用 | 不适用 | 不适用 |


---


### processes_updated

**类型**: django  
**类别**: custom_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/tests/paasng/platform/engine/processes/test_wait.py | 111 | _on_updated | 不适用 | 不适用 | 不适用 |


---


### sig_task_pre_call

**类型**: django  
**类别**: custom_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| svc-rabbitmq/tasks/scheduler.py | 48 | close_old_connections | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| svc-rabbitmq/tasks/models.py | 177 | send_method | 不适用 | 不适用 |

---


### sig_task_post_call

**类型**: django  
**类别**: custom_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| svc-rabbitmq/tasks/scheduler.py | 49 | close_old_connections | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| svc-rabbitmq/tasks/models.py | 184 | send_method | 不适用 | 不适用 |

---


### setup_logging

**类型**: celery  
**类别**: other_signals  

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/celery.py | 32 | config_loggers | 不适用 | 不适用 | 不适用 |


---

