# signals 扫描报告

## 元数据
- **scanner_name**: signal

## 概要信息
- **总数量**: 39
- **已扫描文件数**: 2368
- **扫描耗时**: 21212 毫秒

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
| apiserver/paasng/paas_wl/bk_app/applications/handlers.py |  | on_app_created | 不适用 | WlApp | 不适用 |
| apiserver/paasng/paas_wl/infras/resources/generation/handlers.py |  | set_default_version | 不适用 | WlApp | 不适用 |
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py |  | application_oauth_handler | 不适用 | OAuth2Client | 不适用 |
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py |  | market_config_update_handler | 不适用 | MarketConfig | 不适用 |
| apiserver/paasng/paasng/bk_plugins/pluginscenter/handlers.py |  | update_release_status_when_stage_status_change | 不适用 | PluginReleaseStage | 不适用 |
| apiserver/paasng/paasng/misc/audit/handlers.py |  | on_app_operation_created | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/misc/audit/handlers.py |  | on_model_post_save | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py |  | on_model_post_save | 不适用 | Deployment | 不适用 |


---


### cnative_custom_domain_updated

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paas_wl/bk_app/cnative/specs/handlers.py |  | on_custom_domain_updated | 不适用 | 不适用 | 不适用 |


---


### application_default_module_switch

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paas_wl/bk_app/cnative/specs/handlers.py |  | sync_default_entrances_for_cnative_module_switching | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paas_wl/workloads/networking/entrance/handlers.py |  | sync_default_entrances_for_module_switching | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/accessories/publish/market/handlers.py |  | update_market_config_source_module | 不适用 | 不适用 | 不适用 |


---


### post_appenv_deploy

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/ci/handlers.py |  | start_ci_job | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py |  | sync_release_record | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/misc/audit/handlers.py |  | on_deploy_finished | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/handlers.py |  | create_rules_after_deploy | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/misc/monitoring/monitor/dashboards/handlers.py |  | import_dashboard_after_deploy | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/engine/handlers.py |  | update_last_deployed_date | 不适用 | 不适用 | 不适用 |


---


### on_release_created

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/paas_analysis/handlers.py |  | on_release_created_callback | 不适用 | 不适用 | 不适用 |


---


### application_member_updated

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py |  | update_console_members | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/handlers.py |  | update_notice_group | 不适用 | 不适用 | 不适用 |


---


### prepare_use_application_code

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py |  | validate_app_code_uniquely | 不适用 | 不适用 | 不适用 |


---


### prepare_use_application_name

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py |  | validate_app_name_uniquely | 不适用 | 不适用 | 不适用 |


---


### before_finishing_application_creation

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py |  | register_app_core_data | 不适用 | 不适用 | 不适用 |


---


### prepare_change_application_name

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py |  | on_change_application_name | 不适用 | 不适用 | 不适用 |


---


### module_environment_offline_success

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py |  | offline_handler | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py |  | on_environment_offlined | 不适用 | 不适用 | 不适用 |


---


### application_logo_updated

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py |  | sync_logo | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py |  | extra_setup_logo | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py |  | duplicate_logo_to_extra_bucket | 不适用 | 不适用 | 不适用 |


---


### post_create_application

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/bk_plugins/bk_plugins/handlers.py |  | on_plugin_app_created | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py |  | initialize_application_members | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py |  | turn_on_bk_log_feature_for_app | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py |  | extra_setup_tasks | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/applications/handlers.py |  | update_app_counter | 不适用 | 不适用 | 不适用 |


---


### pre_appenv_deploy

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/bk_plugins/bk_plugins/handlers.py |  | on_pre_deployment | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/paasng/platform/engine/handlers.py |  | attach_all_phases | 不适用 | 不适用 | 不适用 |


---


### pre_phase_start

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/handlers.py |  | start_phase | 不适用 | 不适用 | 不适用 |


---


### post_phase_end

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/handlers.py |  | end_phase | 不适用 | 不适用 | 不适用 |


---


### processes_updated

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/processes/handlers.py |  | _on_processes_updated | 不适用 | 不适用 | 不适用 |


---


### setting_changed

**类型**: django
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/source_types.py |  | reload_settings | 不适用 | 不适用 | 不适用 |


---


### product_create_or_update_by_operator

**类型**: django
**类别**: custom_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py |  | on_product_create_or_updated | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/applications/management/commands/create_3rd_party_apps.py |  | 不适用 | product | 不适用 |
| apiserver/paasng/paasng/platform/declarative/application/controller.py |  | 不适用 | self.__class__ | 不适用 |
| apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/product.py |  | 不适用 | self.__class__ | 不适用 |

---


### post_cnative_env_deploy

**类型**: django
**类别**: custom_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/misc/audit/handlers.py |  | on_cnative_deploy_finished | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/deploy/bg_wait/wait_bkapp.py |  | 不适用 | 不适用 | 不适用 |

---


### post_create_application

**类型**: django
**类别**: custom_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/tests/api/test_applications.py |  | turn_on_bk_log_feature_for_app | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/tests/conftest.py |  | turn_on_bk_log_feature_for_app | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/tests/conftest.py |  | turn_on_bk_log_feature_for_app | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/applications/utils.py |  | 不适用 | create_third_app | 不适用 |
| apiserver/paasng/paasng/platform/applications/views.py |  | 不适用 | self.__class__ | 不适用 |
| apiserver/paasng/paasng/platform/applications/views.py |  | 不适用 | self.__class__ | 不适用 |
| apiserver/paasng/paasng/platform/declarative/application/controller.py |  | 不适用 | self.__class__ | 不适用 |
| apiserver/paasng/tests/utils/helpers.py |  | 不适用 | create_app | 不适用 |
| apiserver/paasng/tests/utils/helpers.py |  | 不适用 | create_app | 不适用 |

---


### application_member_updated

**类型**: django
**类别**: custom_signals


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/applications/views.py |  | 不适用 | application | 不适用 |
| apiserver/paasng/paasng/platform/applications/views.py |  | 不适用 | application | 不适用 |
| apiserver/paasng/paasng/platform/applications/views.py |  | 不适用 | application | 不适用 |
| apiserver/paasng/paasng/platform/applications/views.py |  | 不适用 | application | 不适用 |

---


### application_default_module_switch

**类型**: django
**类别**: custom_signals


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/declarative/application/controller.py |  | 不适用 | application | 不适用 |
| apiserver/paasng/paasng/platform/modules/views.py |  | 不适用 | application | 不适用 |

---


### application_logo_updated

**类型**: django
**类别**: custom_signals


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/declarative/application/controller.py |  | 不适用 | application | 不适用 |

---


### prepare_change_application_name

**类型**: django
**类别**: custom_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/tests/paasng/platform/declarative/application/conftest.py |  | on_change_application_name | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/declarative/application/fields.py |  | 不适用 | self.application | 不适用 |

---


### module_environment_offline_success

**类型**: django
**类别**: custom_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/evaluation/handlers.py |  | on_environment_offline_succeed | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/deploy/archive/base.py |  | 不适用 | OfflineOperation | 不适用 |

---


### post_phase_end

**类型**: django
**类别**: custom_signals


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/workflow/flow.py |  | 不适用 | 不适用 | 不适用 |

---


### post_appenv_deploy

**类型**: django
**类别**: custom_signals


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/engine/workflow/flow.py |  | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/tests/paasng/platform/engine/test_handlers.py |  | 不适用 | 不适用 | 不适用 |

---


### post_change_app_router

**类型**: django
**类别**: custom_signals


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/entrance.py |  | 不适用 | self | 不适用 |

---


### rollback_change_app_router

**类型**: django
**类别**: custom_signals


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/entrance.py |  | 不适用 | self | 不适用 |

---


### on_module_initialized

**类型**: django
**类别**: custom_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/platform/modules/handlers.py |  | async_setup_module_log_model | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/modules/manager.py |  | 不适用 | initialize_smart_module | 不适用 |
| apiserver/paasng/paasng/platform/modules/manager.py |  | 不适用 | initialize_module | 不适用 |

---


### empty_svn_accounts_fetched

**类型**: django
**类别**: custom_signals


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/views.py |  | 不适用 | self | 不适用 |

---


### svn_account_updated

**类型**: django
**类别**: custom_signals


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/views.py |  | 不适用 | self | 不适用 |

---


### repo_updated

**类型**: django
**类别**: custom_signals


#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/views.py |  | 不适用 | self | 不适用 |

---


### before_finishing_application_creation

**类型**: django
**类别**: custom_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/tests/conftest.py |  | register_app_core_data | 不适用 | 不适用 | 不适用 |
| apiserver/paasng/tests/conftest.py |  | register_app_core_data | 不适用 | 不适用 | 不适用 |


---


### processes_updated

**类型**: django
**类别**: custom_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/tests/paasng/platform/engine/processes/test_wait.py |  | _on_updated | 不适用 | 不适用 | 不适用 |


---


### sig_task_pre_call

**类型**: django
**类别**: custom_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| svc-rabbitmq/tasks/scheduler.py |  | close_old_connections | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| svc-rabbitmq/tasks/models.py |  | 不适用 | 不适用 | 不适用 |

---


### sig_task_post_call

**类型**: django
**类别**: custom_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| svc-rabbitmq/tasks/scheduler.py |  | close_old_connections | 不适用 | 不适用 | 不适用 |

#### 发送器

| 文件 | 行号 | 模式 | 发送器 | 代码 |
|------|------|------|--------|------|
| svc-rabbitmq/tasks/models.py |  | 不适用 | 不适用 | 不适用 |

---


### setup_logging

**类型**: celery
**类别**: other_signals

#### 接收器

| 文件 | 行号 | 处理器 | 模式 | 发送器 | 代码 |
|------|------|--------|------|--------|------|
| apiserver/paasng/paasng/celery.py |  | config_loggers | 不适用 | 不适用 | 不适用 |


---

