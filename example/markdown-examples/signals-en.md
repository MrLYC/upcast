# Signal Usage Analysis

## Metadata
- **scanner_name**: signal

## Summary
- **Total Count**: 39
- **Files Scanned**: 2368
- **Scan Duration**: 11490 ms

- **Django Receivers**: 54
- **Django Senders**: 31
- **Celery Receivers**: 1
- **Celery Senders**: 0
- **Custom Signals Defined**: 20
- **Unused Custom Signals**: 0

## Results

### post_save

**Type**: django  
**Category**: model_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paas_wl/bk_app/applications/handlers.py | 24 | on_app_created | N/A | WlApp | N/A |
| apiserver/paasng/paas_wl/infras/resources/generation/handlers.py | 24 | set_default_version | N/A | WlApp | N/A |
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 262 | application_oauth_handler | N/A | OAuth2Client | N/A |
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 305 | market_config_update_handler | N/A | MarketConfig | N/A |
| apiserver/paasng/paasng/bk_plugins/pluginscenter/handlers.py | 27 | update_release_status_when_stage_status_change | N/A | PluginReleaseStage | N/A |
| apiserver/paasng/paasng/misc/audit/handlers.py | 57 | on_app_operation_created | N/A | N/A | N/A |
| apiserver/paasng/paasng/misc/audit/handlers.py | 77 | on_model_post_save | N/A | N/A | N/A |
| apiserver/paasng/paasng/platform/applications/handlers.py | 110 | on_model_post_save | N/A | Deployment | N/A |


---


### cnative_custom_domain_updated

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paas_wl/bk_app/cnative/specs/handlers.py | 30 | on_custom_domain_updated | N/A | N/A | N/A |


---


### application_default_module_switch

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paas_wl/bk_app/cnative/specs/handlers.py | 36 | sync_default_entrances_for_cnative_module_switching | N/A | N/A | N/A |
| apiserver/paasng/paas_wl/workloads/networking/entrance/handlers.py | 31 | sync_default_entrances_for_module_switching | N/A | N/A | N/A |
| apiserver/paasng/paasng/accessories/publish/market/handlers.py | 24 | update_market_config_source_module | N/A | N/A | N/A |


---


### post_appenv_deploy

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/accessories/ci/handlers.py | 39 | start_ci_job | N/A | N/A | N/A |
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 381 | sync_release_record | N/A | N/A | N/A |
| apiserver/paasng/paasng/misc/audit/handlers.py | 102 | on_deploy_finished | N/A | N/A | N/A |
| apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/handlers.py | 32 | create_rules_after_deploy | N/A | N/A | N/A |
| apiserver/paasng/paasng/misc/monitoring/monitor/dashboards/handlers.py | 30 | import_dashboard_after_deploy | N/A | N/A | N/A |
| apiserver/paasng/paasng/platform/engine/handlers.py | 76 | update_last_deployed_date | N/A | N/A | N/A |


---


### on_release_created

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/accessories/paas_analysis/handlers.py | 28 | on_release_created_callback | N/A | N/A | N/A |


---


### application_member_updated

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 145 | update_console_members | N/A | N/A | N/A |
| apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/handlers.py | 40 | update_notice_group | N/A | N/A | N/A |


---


### prepare_use_application_code

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 176 | validate_app_code_uniquely | N/A | N/A | N/A |


---


### prepare_use_application_name

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 186 | validate_app_name_uniquely | N/A | N/A | N/A |


---


### before_finishing_application_creation

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 201 | register_app_core_data | N/A | N/A | N/A |


---


### prepare_change_application_name

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 226 | on_change_application_name | N/A | N/A | N/A |


---


### module_environment_offline_success

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 273 | offline_handler | N/A | N/A | N/A |
| apiserver/paasng/paasng/platform/applications/handlers.py | 97 | on_environment_offlined | N/A | N/A | N/A |


---


### application_logo_updated

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 407 | sync_logo | N/A | N/A | N/A |
| apiserver/paasng/paasng/platform/applications/handlers.py | 124 | extra_setup_logo | N/A | N/A | N/A |
| apiserver/paasng/paasng/platform/applications/handlers.py | 135 | duplicate_logo_to_extra_bucket | N/A | N/A | N/A |


---


### post_create_application

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/bk_plugins/bk_plugins/handlers.py | 34 | on_plugin_app_created | N/A | N/A | N/A |
| apiserver/paasng/paasng/platform/applications/handlers.py | 56 | initialize_application_members | N/A | N/A | N/A |
| apiserver/paasng/paasng/platform/applications/handlers.py | 69 | turn_on_bk_log_feature_for_app | N/A | N/A | N/A |
| apiserver/paasng/paasng/platform/applications/handlers.py | 75 | extra_setup_tasks | N/A | N/A | N/A |
| apiserver/paasng/paasng/platform/applications/handlers.py | 82 | update_app_counter | N/A | N/A | N/A |


---


### pre_appenv_deploy

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/bk_plugins/bk_plugins/handlers.py | 49 | on_pre_deployment | N/A | N/A | N/A |
| apiserver/paasng/paasng/platform/engine/handlers.py | 60 | attach_all_phases | N/A | N/A | N/A |


---


### pre_phase_start

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/platform/engine/handlers.py | 39 | start_phase | N/A | N/A | N/A |


---


### post_phase_end

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/platform/engine/handlers.py | 46 | end_phase | N/A | N/A | N/A |


---


### processes_updated

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/platform/engine/processes/handlers.py | 38 | _on_processes_updated | N/A | N/A | N/A |


---


### setting_changed

**Type**: django  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/source_types.py | 389 | reload_settings | N/A | N/A | N/A |


---


### product_create_or_update_by_operator

**Type**: django  
**Category**: custom_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py | 108 | on_product_create_or_updated | N/A | N/A | N/A |

#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/applications/management/commands/create_3rd_party_apps.py | 217 | send_method | product | N/A |
| apiserver/paasng/paasng/platform/declarative/application/controller.py | 277 | send_method | self.__class__ | N/A |
| apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/product.py | 81 | send_method | self.__class__ | N/A |

---


### post_cnative_env_deploy

**Type**: django  
**Category**: custom_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/misc/audit/handlers.py | 121 | on_cnative_deploy_finished | N/A | N/A | N/A |

#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/engine/deploy/bg_wait/wait_bkapp.py | 252 | send_method | N/A | N/A |

---


### post_create_application

**Type**: django  
**Category**: custom_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/tests/api/test_applications.py | 65 | turn_on_bk_log_feature_for_app | N/A | N/A | N/A |
| apiserver/paasng/tests/conftest.py | 407 | turn_on_bk_log_feature_for_app | N/A | N/A | N/A |
| apiserver/paasng/tests/conftest.py | 412 | turn_on_bk_log_feature_for_app | N/A | N/A | N/A |

#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/applications/utils.py | 144 | send_method | create_third_app | N/A |
| apiserver/paasng/paasng/platform/applications/views.py | 748 | send_method | self.__class__ | N/A |
| apiserver/paasng/paasng/platform/applications/views.py | 873 | send_method | self.__class__ | N/A |
| apiserver/paasng/paasng/platform/declarative/application/controller.py | 113 | send_method | self.__class__ | N/A |
| apiserver/paasng/tests/utils/helpers.py | 180 | send_method | create_app | N/A |
| apiserver/paasng/tests/utils/helpers.py | 549 | send_method | create_app | N/A |

---


### application_member_updated

**Type**: django  
**Category**: custom_signals  


#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/applications/views.py | 952 | send_method | application | N/A |
| apiserver/paasng/paasng/platform/applications/views.py | 972 | send_method | application | N/A |
| apiserver/paasng/paasng/platform/applications/views.py | 989 | send_method | application | N/A |
| apiserver/paasng/paasng/platform/applications/views.py | 1007 | send_method | application | N/A |

---


### application_default_module_switch

**Type**: django  
**Category**: custom_signals  


#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/declarative/application/controller.py | 234 | send_method | application | N/A |
| apiserver/paasng/paasng/platform/modules/views.py | 267 | send_method | application | N/A |

---


### application_logo_updated

**Type**: django  
**Category**: custom_signals  


#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/declarative/application/controller.py | 267 | send_method | application | N/A |

---


### prepare_change_application_name

**Type**: django  
**Category**: custom_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/tests/paasng/platform/declarative/application/conftest.py | 31 | on_change_application_name | N/A | N/A | N/A |

#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/declarative/application/fields.py | 59 | send_method | self.application | N/A |

---


### module_environment_offline_success

**Type**: django  
**Category**: custom_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/platform/evaluation/handlers.py | 26 | on_environment_offline_succeed | N/A | N/A | N/A |

#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/engine/deploy/archive/base.py | 119 | send_method | OfflineOperation | N/A |

---


### post_phase_end

**Type**: django  
**Category**: custom_signals  


#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/engine/workflow/flow.py | 176 | send_method | N/A | N/A |

---


### post_appenv_deploy

**Type**: django  
**Category**: custom_signals  


#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/engine/workflow/flow.py | 193 | send_method | N/A | N/A |
| apiserver/paasng/tests/paasng/platform/engine/test_handlers.py | 37 | send_method | N/A | N/A |

---


### post_change_app_router

**Type**: django  
**Category**: custom_signals  


#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/entrance.py | 42 | send_method | self | N/A |

---


### rollback_change_app_router

**Type**: django  
**Category**: custom_signals  


#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/entrance.py | 55 | send_method | self | N/A |

---


### on_module_initialized

**Type**: django  
**Category**: custom_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/platform/modules/handlers.py | 27 | async_setup_module_log_model | N/A | N/A | N/A |

#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/modules/manager.py | 370 | send_method | initialize_smart_module | N/A |
| apiserver/paasng/paasng/platform/modules/manager.py | 440 | send_method | initialize_module | N/A |

---


### empty_svn_accounts_fetched

**Type**: django  
**Category**: custom_signals  


#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/views.py | 103 | send_method | self | N/A |

---


### svn_account_updated

**Type**: django  
**Category**: custom_signals  


#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/views.py | 131 | send_method | self | N/A |

---


### repo_updated

**Type**: django  
**Category**: custom_signals  


#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| apiserver/paasng/paasng/platform/sourcectl/views.py | 390 | send_method | self | N/A |

---


### before_finishing_application_creation

**Type**: django  
**Category**: custom_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/tests/conftest.py | 406 | register_app_core_data | N/A | N/A | N/A |
| apiserver/paasng/tests/conftest.py | 419 | register_app_core_data | N/A | N/A | N/A |


---


### processes_updated

**Type**: django  
**Category**: custom_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/tests/paasng/platform/engine/processes/test_wait.py | 111 | _on_updated | N/A | N/A | N/A |


---


### sig_task_pre_call

**Type**: django  
**Category**: custom_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| svc-rabbitmq/tasks/scheduler.py | 48 | close_old_connections | N/A | N/A | N/A |

#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| svc-rabbitmq/tasks/models.py | 177 | send_method | N/A | N/A |

---


### sig_task_post_call

**Type**: django  
**Category**: custom_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| svc-rabbitmq/tasks/scheduler.py | 49 | close_old_connections | N/A | N/A | N/A |

#### Senders

| File | Line | Pattern | Sender | Code |
|------|------|---------|--------|------|
| svc-rabbitmq/tasks/models.py | 184 | send_method | N/A | N/A |

---


### setup_logging

**Type**: celery  
**Category**: other_signals  

#### Receivers

| File | Line | Handler | Pattern | Sender | Code |
|------|------|---------|---------|--------|------|
| apiserver/paasng/paasng/celery.py | 32 | config_loggers | N/A | N/A | N/A |


---

