# unit-tests 扫描报告

## 元数据
暂无元数据。

## 概要信息
- **总数量**: 1607
- **已扫描文件数**: 331
- **扫描耗时**: 3308 毫秒

- **测试总数**: 1607
- **测试文件总数**: 331
- **断言总数**: 3658

## 结果详情

### 测试文件: apiserver/paasng/tests/api/apigw/test_ai_agent.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_ai_agent_app | 73-95 | 5 | 1bd12fa4... | django.conf (settings), paasng.platform.applications.constants (ApplicationType), paasng.platform.modules.constants (SourceOrigin), pytest (pytest) |
| test_upload_with_app_desc | 97-119 | 1 | e3f3dedd... | paasng.platform.modules.constants (SourceOrigin), pathlib (Path), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/api/apigw/test_lesscode.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_lesscode_api | 58-88 | 3 | 13b1d4b1... | django.conf (settings), django.test.utils (override_settings), paasng.platform.applications.constants (ApplicationType), paasng.platform.modules.constants (SourceOrigin), pytest (pytest) |
| test_upload_with_app_desc | 109-131 | 1 | 6268e2fc... | paasng.platform.modules.constants (SourceOrigin), pathlib (Path), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/api/apigw/test_log.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_dsl | 29-90 | 3 | 89362396... | elasticsearch_dsl.response (Response), elasticsearch_dsl.search (Search), json (json), unittest (mock) |
| test_complex | 92-150 | 3 | f7efef9f... | elasticsearch_dsl.response (Response), elasticsearch_dsl.search (Search), unittest (mock) |
| test_complex | 154-223 | 2 | b084f3a9... | elasticsearch_dsl.response (Hit), unittest (mock) |
| test_dsl | 227-261 | 2 | 31abbbc6... | elasticsearch_dsl.response (Response), elasticsearch_dsl.search (Search), json (json), unittest (mock) |
| test_list | 263-343 | 3 | d5354727... | elasticsearch_dsl.response (Response), elasticsearch_dsl.search (Search), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/api/apigw/test_modules.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_module | 46-76 | 3 | a02ac3dd... | django.conf (settings), paasng.platform.applications.constants (ApplicationType), paasng.platform.modules.constants (SourceOrigin), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/api/apigw/test_system_apis.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 54-60 | 2 | 494bda76... | django.conf (settings), paasng.plat_admin.system.applications (query_default_apps_by_ids) |
| test_include_inactive_apps | 62-75 | 3 | d194e674... | django.conf (settings), paasng.plat_admin.system.applications (query_default_apps_by_ids) |
| test_normal | 81-86 | 1 | 684e2916... | paasng.plat_admin.system.applications (query_legacy_apps_by_ids), tests.utils.helpers (create_legacy_application) |
| test_mixed_platforms | 92-103 | 6 | 4a2c57c8... | paasng.plat_admin.system.applications (query_uni_apps_by_ids), paasng.platform.applications.constants (ApplicationType), tests.utils.helpers (create_legacy_application) |
| test_query_by_keyword | 105-128 | 1 | e5b82b5b... | django.utils.translation (override), operator (attrgetter), paasng.plat_admin.system.applications (query_uni_apps_by_keyword), pytest (pytest), tests.utils.helpers (create_legacy_application) |
| test_normal | 134-137 | 2 | 8148398b... | paasng.platform.applications.operators (get_contact_info) |
| test_recent_deployment_operators | 139-168 | 1 | f34c1c87... | arrow (arrow), paasng.plat_admin.system.applications (str_username), paasng.platform.applications.operators (get_contact_info), paasng.platform.engine.constants (OperationTypes), paasng.platform.engine.models.operations (ModuleEnvironmentOperations), pytest (pytest), tests.paasng.platform.engine.setup_utils (create_fake_deployment), tests.utils.auth (create_user) |
| test_query_db_credentials | 177-208 | 2 | f665afeb... | pytest (pytest) |
| test_query_credentials | 253-259 | 2 | 002745c5... |  |
| test_query_credentials_404 | 261-266 | 1 | ffe115a1... | paasng.accessories.servicehub.manager (ServiceObjNotFound) |
| test_provision_service | 268-284 | 1 | 91a5df4f... | pytest (pytest), unittest (mock) |
| test_retrieve_specs | 286-298 | 2 | 33958fde... | django_dynamic_fixture (G), paasng.accessories.servicehub.models (ServiceEngineAppAttachment), paasng.accessories.services.models (Plan), unittest (mock) |
| test_retrieve_specs_but_unprovision | 300-306 | 2 | 7a9fa6a8... | unittest (mock) |
| test_list_by_code | 319-326 | 4 | cc413738... |  |

---


### 测试文件: apiserver/paasng/tests/api/bkapp_model/test_bkapp_model.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_retrieve | 53-77 | 13 | 956d58bf... |  |
| test_save | 79-212 | 20 | a47b123a... | django_dynamic_fixture (G), paasng.platform.bkapp_model.entities (AutoscalingConfig), paasng.platform.bkapp_model.models (ModuleProcessSpec, ProcessSpecEnvOverlay) |
| test_validate | 231-269 | 2 | ec36e91d... | pytest (pytest) |
| test_validate_duplicated_exposed_type | 271-312 | 2 | 6e13e124... | pytest (pytest) |
| test_save | 314-359 | 6 | a034c698... | paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_retrieve | 361-371 | 2 | 8e833608... |  |
| test_validate | 395-424 | 2 | 5d0bce3a... | pytest (pytest) |
| test_save | 426-463 | 3 | 9484d261... | paasng.platform.bkapp_model.entities (Metric), paasng.platform.bkapp_model.models (ObservabilityConfig) |
| test_retrieve | 465-471 | 1 | fa80cd2e... | pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/api/bkapp_model/test_manifest.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_import | 65-70 | 2 | adce4eee... |  |

---


### 测试文件: apiserver/paasng/tests/api/bkapp_model/test_network_config.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_url | 34-36 | 0 | cf152b78... | django.urls (reverse), pytest (pytest) |
| test_get_missing | 44-47 | 1 | eb040a48... |  |
| test_get_normal | 49-53 | 2 | 81df3c26... |  |
| test_upsert_normal | 55-59 | 2 | 18047e06... |  |
| test_upsert_module_absent | 61-65 | 2 | b79068f6... |  |
| test_upsert_invalid_module | 67-72 | 1 | d49af7a6... |  |
| test_upsert_duplicated_entries | 74-86 | 1 | fc4dc237... |  |
| test_url | 90-92 | 0 | beebeccb... | django.urls (reverse), pytest (pytest) |
| test_get_missing | 112-115 | 1 | eb040a48... |  |
| test_get | 117-130 | 3 | ee1bbf3c... |  |
| test_upsert | 132-163 | 2 | f1b94507... | pytest (pytest) |
| test_upsert_no_data | 165-168 | 1 | 11e94250... |  |

---


### 测试文件: apiserver/paasng/tests/api/extensions/test_bkplugins.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list | 40-43 | 2 | 421c1895... |  |
| test_update | 53-59 | 2 | c6e2cca2... |  |
| test_integrated | 61-69 | 2 | 88b34187... |  |
| test_sync | 75-97 | 10 | 875c5864... | paasng.platform.engine.models (ConfigVar) |

---


### 测试文件: apiserver/paasng/tests/api/test_app_secret.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_secret_perm | 93-105 | 1 | 2f3cc230... | pytest (pytest), rest_framework.reverse (reverse), unittest (mock) |
| test_create_secret | 107-132 | 1 | b04538ff... | pytest (pytest), rest_framework.reverse (reverse), unittest (mock) |
| test_toggle_secret_whit_no_db_default_secret | 134-156 | 1 | ee9a439c... | pytest (pytest), rest_framework.reverse (reverse), unittest (mock) |
| test_toggle_secret_whit_db_default_secret | 158-195 | 1 | c7b0a06b... | paasng.platform.applications.constants (ApplicationType), pytest (pytest), rest_framework.reverse (reverse), unittest (mock) |
| test_delete_secret | 197-245 | 1 | 0591bdf6... | paasng.platform.applications.constants (ApplicationType), pytest (pytest), rest_framework.reverse (reverse), unittest (mock) |
| test_rotate_secret | 247-279 | 1 | f427c5f6... | pytest (pytest), rest_framework.reverse (reverse), unittest (mock) |
| test_get_default_secret_perm | 281-295 | 1 | 6f4ad6d3... | pytest (pytest), rest_framework.reverse (reverse), unittest (mock) |
| test_get_deployed_secret_perm | 297-309 | 1 | 6e3aae7d... | pytest (pytest), rest_framework.reverse (reverse), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/api/test_applications.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_succeed | 71-74 | 1 | 547c961a... | django.urls (reverse) |
| test_list_with_another_user | 76-102 | 4 | 254a4e50... | django.urls (reverse), paasng.infras.iam.helpers (add_role_members), paasng.platform.applications.constants (ApplicationRole), paasng.utils.basic (get_username_by_bkpaas_user_id), pytest (pytest) |
| test_create | 104-131 | 1 | 1e4802d2... | django.urls (reverse), paasng.platform.applications.constants (ApplicationRole), pytest (pytest) |
| test_delete | 133-165 | 3 | 5ef67cdf... | django.urls (reverse), paasng.infras.iam.helpers (add_role_members, fetch_application_members), paasng.platform.applications.constants (ApplicationRole), paasng.utils.basic (get_username_by_bkpaas_user_id), pytest (pytest), tests.utils.auth (create_user) |
| test_level | 167-193 | 3 | 80211e4f... | django.urls (reverse), paasng.infras.iam.helpers (add_role_members, fetch_application_members), paasng.platform.applications.constants (ApplicationRole), paasng.utils.basic (get_username_by_bkpaas_user_id), pytest (pytest), tests.utils.auth (create_user) |
| test_level_last_admin | 195-208 | 3 | b45c4551... | django.urls (reverse), paasng.infras.iam.helpers (add_role_members, fetch_application_members, remove_user_all_roles), paasng.platform.applications.constants (ApplicationRole), paasng.utils.basic (get_username_by_bkpaas_user_id) |
| test_create_different_types | 214-257 | 4 | d6ae83b0... | django.conf (settings), paasng.platform.modules.constants (SourceOrigin), paasng.platform.sourcectl.connector (IntegratedSvnAppRepoConnector, SourceSyncResult), pytest (pytest), tests.utils.helpers (generate_random_string), unittest (mock) |
| test_create_non_default_origin | 259-299 | 1 | 6fb127db... | django.conf (settings), django.test.utils (override_settings), paasng.platform.modules.constants (SourceOrigin), pytest (pytest), tests.utils.helpers (generate_random_string) |
| test_create_non_engine | 305-319 | 2 | bce05ad9... | django.conf (settings), pytest (pytest), tests.utils.helpers (generate_random_string) |
| test_region_permission_control | 321-349 | 1 | 4b63ed19... | paasng.infras.accounts.models (UserProfile), pytest (pytest), tests.utils.helpers (configure_regions, generate_random_string) |
| test_normal | 355-362 | 2 | f90fd86c... | paasng.platform.applications.models (Application), pytest (pytest) |
| test_duplicated | 364-372 | 3 | 8b0cafe0... | django_dynamic_fixture (G), paasng.platform.applications.models (Application) |
| test_desc_app | 374-388 | 2 | f2244610... | paasng.platform.applications.models (Application), paasng.platform.declarative.handlers (get_desc_handler) |
| test_normal | 394-410 | 3 | f3ecefe0... | paasng.misc.audit.constants (OperationEnum, OperationTarget), paasng.misc.audit.models (AppOperationRecord), pytest (pytest), unittest (mock) |
| test_rollback | 412-434 | 3 | 18a84c8b... | paasng.misc.audit.constants (OperationEnum, OperationTarget, ResultCode), paasng.misc.audit.models (AppOperationRecord), paasng.utils.error_codes (error_codes), pytest (pytest), unittest (mock) |
| test_normal | 440-456 | 4 | 7d158190... | django.conf (settings), pytest (pytest) |
| test_forbidden_via_config | 458-462 | 1 | 05076583... | django.conf (settings) |
| test_create_with_image | 493-541 | 9 | 6313b571... | django.conf (settings), paasng.platform.bkapp_model.models (ModuleProcessSpec), paasng.platform.modules.constants (SourceOrigin), paasng.platform.modules.models (BuildConfig), paasng.platform.modules.models.module (Module), tests.utils.helpers (generate_random_string) |
| test_create_with_buildpack | 543-571 | 4 | a16a2500... | django.conf (settings), paasng.platform.modules.constants (SourceOrigin), pytest (pytest), tests.utils.helpers (generate_random_string), unittest (mock) |
| test_create_with_dockerfile | 573-596 | 4 | bd292503... | django.conf (settings), paasng.platform.modules.constants (SourceOrigin), pytest (pytest), tests.utils.helpers (generate_random_string) |
| test_create_with_bk_log_feature | 598-623 | 2 | 4a775a43... | django.conf (settings), paas_wl.infras.cluster.constants (ClusterFeatureFlag), paas_wl.infras.cluster.shim (RegionClusterService), paasng.platform.applications.constants (AppFeatureFlag), paasng.platform.applications.models (Application), paasng.platform.modules.constants (SourceOrigin), pytest (pytest), tests.utils.helpers (generate_random_string) |
| test_list_evaluation | 708-745 | 4 | 7be6285a... | datetime (datetime), django.urls (reverse), django.utils (timezone) |
| test_issue_count | 747-760 | 4 | cd8f9c3e... | django.urls (reverse) |
| test_module_order | 764-837 | 3 | 7b131b68... | django.urls (reverse), paasng.platform.modules.models.module (Module), tests.utils.helpers (initialize_module) |
| test_module_order_missing_module | 839-862 | 1 | 15957b90... | django.urls (reverse), paasng.platform.modules.models.module (Module), tests.utils.helpers (initialize_module) |
| test_module_order_extra_module | 864-891 | 1 | 25174cad... | django.urls (reverse), paasng.platform.modules.models.module (Module), tests.utils.helpers (initialize_module) |

---


### 测试文件: apiserver/paasng/tests/api/test_build.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list | 31-50 | 5 | 68232a1a... | paas_wl.bk_app.applications.constants (ArtifactType), paas_wl.utils.constants (BuildStatus), tests.paas_wl.utils.build (create_build, create_build_proc) |
| test_list_duplicated | 53-80 | 5 | dd61d63d... | paas_wl.bk_app.applications.constants (ArtifactType), paas_wl.utils.constants (BuildStatus), tests.paas_wl.utils.build (create_build, create_build_proc) |
| test_retrieve_image_detail | 82-109 | 5 | 3e98c782... | paas_wl.bk_app.applications.constants (ArtifactType), paas_wl.utils.constants (BuildStatus), tests.paas_wl.utils.build (create_build, create_build_proc) |
| test_list_pending | 113-122 | 5 | 93f18efb... | tests.paas_wl.utils.build (create_build_proc) |
| test_list_successful | 124-136 | 6 | 48177444... | paas_wl.bk_app.applications.constants (ArtifactType), paas_wl.utils.constants (BuildStatus), tests.paas_wl.utils.build (create_build, create_build_proc) |

---


### 测试文件: apiserver/paasng/tests/api/test_build_config.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_retrieve_legacy_bp | 85-96 | 1 | 4a1ca938... |  |
| test_retrieve_bp | 98-121 | 1 | b1876510... | paasng.platform.modules.helpers (ModuleRuntimeBinder) |
| test_retrieve_docker | 123-139 | 1 | 76196488... | paasng.platform.engine.constants (RuntimeType), paasng.platform.modules.models (BuildConfig) |
| test_retrieve_custom_image | 141-156 | 1 | 1a96a3ab... | paasng.platform.engine.constants (RuntimeType), paasng.platform.modules.models (BuildConfig) |
| test_modify_bp | 158-185 | 7 | f81ef91f... | paasng.platform.engine.constants (RuntimeType), paasng.platform.modules.helpers (ModuleRuntimeManager), paasng.platform.modules.models (BuildConfig), paasng.platform.modules.models.build_cfg (ImageTagOptions) |
| test_modify_dockerbuild | 187-200 | 4 | 98449468... | paasng.platform.engine.constants (RuntimeType), paasng.platform.modules.models (BuildConfig), paasng.platform.modules.models.build_cfg (ImageTagOptions) |
| test_modify_dockerbuild_with_emtpy_build_args | 202-215 | 4 | 67d1947f... | paasng.platform.engine.constants (RuntimeType), paasng.platform.modules.models (BuildConfig), paasng.platform.modules.models.build_cfg (ImageTagOptions) |
| test_modify_custom_image | 217-229 | 4 | 7ab44a9c... | paasng.platform.engine.constants (RuntimeType), paasng.platform.modules.models (BuildConfig) |
| test_modify_wrong_args | 231-274 | 1 | 06f1ccdc... | paasng.platform.engine.constants (RuntimeType), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/api/test_cnative.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_retrieve | 41-50 | 1 | b65c3fd4... | django.urls (reverse), paas_wl.bk_app.cnative.specs.constants (BKPAAS_ADDONS_ANNO_KEY) |

---


### 测试文件: apiserver/paasng/tests/api/test_cnative_migration.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_migrate | 42-50 | 2 | 50fc5b62... | paasng.platform.mgrlegacy.models (CNativeMigrationProcess), unittest (mock) |
| test_migrate_when_progress_is_active | 52-57 | 2 | 8b99cfbe... | paasng.platform.mgrlegacy.models (CNativeMigrationProcess) |
| test_rollback | 61-71 | 2 | 20293ee6... | paasng.platform.mgrlegacy.constants (CNativeMigrationStatus), paasng.platform.mgrlegacy.models (CNativeMigrationProcess), unittest (mock) |
| test_rollback_when_last_migration_failed | 73-80 | 2 | a6c7974c... | paasng.platform.mgrlegacy.constants (CNativeMigrationStatus), paasng.platform.mgrlegacy.models (CNativeMigrationProcess) |
| test_rollback_when_never_migrated | 82-85 | 2 | a0bf5abf... |  |
| test_get_process_by_id | 89-107 | 5 | 8e1e6369... | paasng.platform.mgrlegacy.constants (CNativeMigrationStatus), paasng.platform.mgrlegacy.entities (MigrationResult, ProcessDetails), paasng.platform.mgrlegacy.models (CNativeMigrationProcess) |
| test_get_process_by_id_404 | 109-111 | 1 | 29f232f9... |  |
| test_get_latest_process | 113-128 | 1 | c45c3695... | paasng.platform.mgrlegacy.constants (CNativeMigrationStatus), paasng.platform.mgrlegacy.models (CNativeMigrationProcess) |
| test_confirm | 158-170 | 1 | fa8e3717... | paasng.platform.mgrlegacy.constants (CNativeMigrationStatus), paasng.platform.mgrlegacy.models (CNativeMigrationProcess), pytest (pytest), unittest (mock) |
| test_confirm_failed | 172-177 | 1 | 5449feb8... | paasng.platform.mgrlegacy.constants (CNativeMigrationStatus), paasng.platform.mgrlegacy.models (CNativeMigrationProcess) |
| test_list | 198-203 | 1 | de476abc... | unittest (mock) |
| test_update | 205-215 | 1 | 372ea9b7... | unittest (mock) |
| test_list_all_entrances | 250-252 | 1 | 7e5da8fe... |  |
| test_get | 289-294 | 4 | c1674e99... |  |

---


### 测试文件: apiserver/paasng/tests/api/test_configvar_by_key.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_configvar_by_key | 32-92 | 6 | fb8fcc8c... | paasng.platform.applications.models (ApplicationEnvironment), paasng.platform.engine.models (ConfigVar), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/api/test_configvar_preset.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_preset_config_var | 27-40 | 1 | bd83026a... | django_dynamic_fixture (G), paasng.platform.engine.constants (ConfigVarEnvName), paasng.platform.engine.models.preset_envvars (PresetEnvVariable), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/api/test_dashboard.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_builtin_dashboards | 54-67 | 4 | 871e6de0... | django.urls (reverse), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/api/test_dev_sandbox.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_deploy | 31-35 | 1 | 8405070b... | paas_wl.bk_app.dev_sandbox.controller (DevSandboxController), unittest (mock) |
| test_deploy_when_already_exists | 37-41 | 1 | 2d86d290... | paas_wl.bk_app.dev_sandbox.controller (DevSandboxController), paas_wl.bk_app.dev_sandbox.exceptions (DevSandboxAlreadyExists), unittest (mock) |
| test_delete | 43-49 | 1 | ab1da45f... | paas_wl.bk_app.dev_sandbox.controller (DevSandboxController), unittest (mock) |
| test_get_container_detail | 51-64 | 2 | cba8a564... | paas_wl.bk_app.dev_sandbox.controller (DevSandboxController), paas_wl.bk_app.dev_sandbox.entities (DevSandboxDetail, HealthPhase), tests.utils.helpers (generate_random_string), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/api/test_engine.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal_create | 40-51 | 3 | d8bcdc6a... |  |
| test_normal_edit | 53-68 | 2 | a7216b22... |  |
| test_normal_delete | 70-87 | 2 | 51f64643... |  |
| test_normal_var_copy | 89-105 | 6 | 4e12a081... |  |
| test_list_order_by | 121-135 | 1 | 5771c7d5... | pytest (pytest) |
| test_list_filter_environment_name | 137-156 | 1 | 628cf72c... | pytest (pytest) |
| test_deploy_not_allow | 160-173 | 2 | 9c2da74c... | django.urls (reverse), django_dynamic_fixture (G), paasng.platform.applications.constants (ApplicationRole), paasng.platform.environments.constants (EnvRoleOperation), paasng.platform.environments.models (EnvRoleProtection) |
| test_deploy_no_revision | 175-179 | 2 | f8bead2b... | django.urls (reverse), paasng.platform.sourcectl.constants (VersionType) |
| test_deploy_with_image_type | 181-185 | 2 | 9a850023... | django.urls (reverse), paasng.platform.sourcectl.constants (VersionType) |
| test_deploy | 187-201 | 4 | 2becdb4f... | django.urls (reverse), paasng.platform.engine.models.deployment (Deployment), paasng.platform.engine.workflow (DeploymentCoordinator), paasng.platform.sourcectl.constants (VersionType), pytest (pytest), unittest (mock) |
| test_deploy_conflict | 203-217 | 3 | bd057418... | django.urls (reverse), paasng.platform.engine.workflow (DeploymentCoordinator), paasng.platform.sourcectl.constants (VersionType) |
| test_deploy_exception | 219-225 | 2 | ac78f430... | django.urls (reverse), paasng.platform.sourcectl.constants (VersionType) |

---


### 测试文件: apiserver/paasng/tests/api/test_evaluation.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create | 29-41 | 3 | f694242f... | datetime (timedelta), django.utils (timezone), paasng.platform.evaluation.models (IdleAppNotificationMuteRule), rest_framework (status) |

---


### 测试文件: apiserver/paasng/tests/api/test_log.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_dsl | 34-90 | 3 | b167cb84... | json (json), unittest (mock) |
| test_complex | 92-157 | 2 | e74bb813... | elasticsearch_dsl.response (Hit), unittest (mock) |
| test_list | 190-198 | 4 | 6f3af89c... |  |
| test_list_metadata | 205-253 | 8 | 19118e47... | paasng.accessories.log.shim.setup_bklog (build_custom_collector_config_name), unittest (mock) |
| test_insert_success | 255-276 | 3 | 7bb8a051... |  |
| test_insert_failed | 278-290 | 3 | a2ef173d... |  |
| test_update_success | 292-324 | 7 | 84208dc8... | paasng.accessories.log.models (CustomCollectorConfig) |

---


### 测试文件: apiserver/paasng/tests/api/test_market.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_name_conflicted_with_existed_app | 70-75 | 3 | 63683cf3... | rest_framework.reverse (reverse) |
| test_duplicated_creation | 77-85 | 3 | 9aeaaefa... | rest_framework.reverse (reverse) |
| test_normal | 87-97 | 5 | 22919fe5... | paasng.accessories.publish.market.constant (OpenMode), paasng.accessories.publish.market.models (DisplayOptions, Product), rest_framework.reverse (reverse) |
| test_get_market_app | 107-111 | 3 | 5afecad1... | paasng.accessories.publish.market.constant (OpenMode), rest_framework.reverse (reverse) |
| test_update_market_app | 113-164 | 9 | 67d845c3... | django.conf (settings), json (json), paasng.accessories.publish.market.constant (OpenMode), paasng.accessories.publish.market.models (Product), paasng.accessories.publish.sync_market.handlers (register_app_core_data), paasng.accessories.publish.sync_market.managers (AppManger), paasng.core.core.storages.sqlalchemy (console_db), rest_framework.reverse (reverse), uuid (uuid) |
| test_set_builtin_entrance | 170-184 | 2 | 66bf3b7b... | paasng.accessories.publish.market.constant (ProductSourceUrlType), paasng.accessories.publish.market.models (MarketConfig) |
| test_set_builtin_custom | 186-209 | 3 | 9fe936dd... | paas_wl.workloads.networking.ingress.models (Domain), paasng.accessories.publish.market.constant (ProductSourceUrlType), paasng.accessories.publish.market.models (MarketConfig) |
| test_set_failed | 211-227 | 2 | a0f1169e... |  |
| test_set_third_party_url | 229-245 | 3 | 30c8ec1d... | paasng.accessories.publish.market.constant (ProductSourceUrlType), paasng.accessories.publish.market.models (MarketConfig), paasng.platform.applications.constants (ApplicationType) |

---


### 测试文件: apiserver/paasng/tests/api/test_market_config.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_then_release | 40-119 | 6 | 112cb0cb... | django.conf (settings), django_dynamic_fixture (G), paasng.accessories.publish.market.models (Product), paasng.accessories.publish.market.protections (AppPublishPreparer), paasng.accessories.publish.market.status (publish_to_market_by_deployment), paasng.platform.applications.models (Application), paasng.platform.engine.models (Deployment), paasng.platform.modules.constants (SourceOrigin), paasng.platform.sourcectl.source_types (get_sourcectl_names), pytest (pytest), tests.utils.helpers (generate_random_string), unittest.mock (PropertyMock, patch) |

---


### 测试文件: apiserver/paasng/tests/api/test_modules.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_different_engine_params | 51-87 | 1 | db5f3e6b... | django.conf (settings), paasng.platform.modules.constants (SourceOrigin), paasng.platform.sourcectl.connector (IntegratedSvnAppRepoConnector, SourceSyncResult), pytest (pytest), tests.utils.helpers (generate_random_string), unittest (mock) |
| test_create_nondefault_origin | 89-112 | 1 | e3735e3e... | django.conf (settings), django.test.utils (override_settings), paasng.platform.modules.constants (SourceOrigin), paasng.platform.sourcectl.connector (IntegratedSvnAppRepoConnector, SourceSyncResult), pytest (pytest), tests.utils.helpers (generate_random_string), unittest (mock) |
| test_create_with_image | 120-171 | 10 | e587a30a... | paasng.platform.bkapp_model.models (ModuleDeployHook, ModuleProcessSpec), paasng.platform.modules.constants (DeployHookType, SourceOrigin), paasng.platform.modules.models (BuildConfig), paasng.platform.modules.models.module (Module), tests.utils.helpers (generate_random_string) |
| test_create_with_buildpack | 173-198 | 3 | fc56ee5a... | django.conf (settings), paasng.platform.modules.constants (SourceOrigin), pytest (pytest), tests.utils.helpers (generate_random_string), unittest (mock) |
| test_create_with_dockerfile | 200-225 | 3 | b54b9469... | paasng.platform.modules.constants (SourceOrigin), pytest (pytest), tests.utils.helpers (generate_random_string) |
| test_retrieve | 238-245 | 2 | d7545710... |  |
| test_upsert_hook | 247-268 | 3 | 6cbb073c... | pytest (pytest) |
| test_disable_hook | 270-279 | 3 | d3210788... | paasng.platform.modules.constants (DeployHookType) |
| test_update_procfile | 281-308 | 3 | 8fa86099... | paasng.platform.bkapp_model.models (ModuleProcessSpec), paasng.platform.modules.constants (SourceOrigin), pytest (pytest) |
| test_delete_main_module | 319-328 | 4 | 499e771a... | paasng.misc.audit.constants (OperationEnum, OperationTarget), paasng.misc.audit.models (AppOperationRecord) |
| test_delete_module | 330-347 | 2 | c3beba76... | paasng.misc.audit.constants (OperationEnum, OperationTarget), paasng.misc.audit.models (AppOperationRecord), paasng.platform.modules.models.module (Module), tests.utils.helpers (initialize_module), unittest (mock) |
| test_delete_rollback | 349-367 | 3 | 02fbe67e... | paasng.misc.audit.constants (OperationEnum, OperationTarget, ResultCode), paasng.misc.audit.models (AppOperationRecord), paasng.platform.modules.models.module (Module), tests.utils.helpers (initialize_module), unittest (mock) |
| test_source_module | 382-396 | 3 | a8347fc6... | paasng.accessories.publish.market.models (MarketConfig) |
| test_with_custom_domain | 398-435 | 4 | 9a72ea4d... | paas_wl.workloads.networking.ingress.models (Domain), paasng.accessories.publish.market.constant (ProductSourceUrlType), paasng.accessories.publish.market.models (MarketConfig) |

---


### 测试文件: apiserver/paasng/tests/api/test_monitor.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_alerts | 45-58 | 4 | fc972949... | datetime (datetime, timedelta), random (random) |
| test_list_alerts_by_user | 60-76 | 7 | ac094238... | datetime (datetime, timedelta), random (random) |
| test_list_alarm_strategies | 80-87 | 2 | 6cbcd283... | tests.utils.mocks.bkmonitor (StubBKMonitorClient), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/api/test_scene_app.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list | 39-49 | 1 | a8dccb4b... | django.conf (settings), django.urls (reverse), paasng.platform.templates.constants (TemplateType), pytest (pytest) |
| test_create | 62-85 | 3 | 53590af7... | django.conf (settings), django.urls (reverse), paasng.platform.modules.constants (SourceOrigin), pytest (pytest), string (string), tests.utils.helpers (generate_random_string) |

---


### 测试文件: apiserver/paasng/tests/api/test_servicehub.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list | 51-61 | 2 | 063264c3... | django_dynamic_fixture (G), paasng.accessories.services.models (Service), unittest (mock) |
| test_update | 63-75 | 3 | 32916d5d... | django_dynamic_fixture (G), paasng.accessories.services.models (Service), unittest (mock) |
| test_config_vars | 77-96 | 4 | 2f642768... | datetime (datetime), django_dynamic_fixture (G), paasng.accessories.services.models (Service), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/api/test_smart_app.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_upload_and_create | 48-83 | 5 | 797ee2f7... | unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/api/test_sourcectl.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_account | 48-57 | 1 | a361283c... | django.conf (settings), django.urls (reverse), unittest (mock) |
| test_reset_account_error | 59-71 | 2 | 42ab36b1... | django.conf (settings), django.test.utils (override_settings), django.urls (reverse) |
| test_reset_account_skip_verification_code | 73-80 | 1 | 8fee1379... | django.conf (settings), django.test.utils (override_settings), django.urls (reverse) |

---


### 测试文件: apiserver/paasng/tests/api/test_templates.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list | 111-122 | 1 | d3ea03d5... | django.conf (settings), django.urls (reverse), paasng.platform.templates.constants (TemplateType), pytest (pytest) |
| test_retrieve | 124-147 | 7 | eadfa64b... | django.conf (settings), django.urls (reverse), paasng.platform.templates.constants (TemplateType), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/api/test_tools.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_app_desc_transform | 27-539 | 2 | 2588834c... | django.conf (settings), django.urls (reverse), pytest (pytest), yaml (yaml) |
| test_app_desc_transform_exception | 541-554 | 1 | ea1d5398... | django.urls (reverse), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/api/test_entrance.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_all_entrances | 39-164 | 3 | 4854d391... | paas_wl.workloads.networking.ingress.models (AppDomain, Domain), paasng.platform.modules.constants (ExposedURLType), tests.paas_wl.utils.release (create_release) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/api/test_image_credential.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_destroy | 43-46 | 1 | f66932ed... |  |
| test_destroy_when_used | 48-52 | 1 | bc71abe8... |  |

---


### 测试文件: apiserver/paasng/tests/paas_wl/api/test_instance_events.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list | 54-63 | 4 | 4fb8e64b... |  |

---


### 测试文件: apiserver/paasng/tests/paas_wl/api/test_mounts.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list | 125-144 | 6 | c988e2e7... |  |
| test_create_configmap | 146-165 | 3 | 376f1381... | paas_wl.bk_app.cnative.specs.models (Mount), paas_wl.bk_app.cnative.specs.mounts (init_volume_source_controller) |
| test_create_pvc | 167-186 | 3 | 21ff8b9b... | paas_wl.bk_app.cnative.specs.models (Mount), paas_wl.bk_app.cnative.specs.mounts (init_volume_source_controller) |
| test_create_with_source_name | 188-200 | 2 | f0ddc2c4... | paas_wl.bk_app.cnative.specs.models (Mount) |
| test_create_error | 202-270 | 1 | ca9c4109... | pytest (pytest) |
| test_update_configmap | 272-299 | 6 | f3fbc7e4... | paas_wl.bk_app.cnative.specs.models (Mount), paas_wl.bk_app.cnative.specs.mounts (init_volume_source_controller), paas_wl.bk_app.cnative.specs.serializers (MountSLZ) |
| test_destroy_configmap | 301-309 | 2 | f0126f34... | paas_wl.bk_app.cnative.specs.models (Mount) |
| test_update_pvc | 311-321 | 3 | c8692ece... | paas_wl.bk_app.cnative.specs.models (Mount), paas_wl.bk_app.cnative.specs.serializers (MountSLZ) |
| test_destroy_pvc | 323-328 | 2 | 4a8e655c... | paas_wl.bk_app.cnative.specs.models (Mount) |
| test_destroy_error | 330-339 | 2 | 9fac2907... | paas_wl.bk_app.cnative.specs.models (Mount) |
| test_list | 368-378 | 4 | 87df0761... | pytest (pytest) |
| test_create | 380-402 | 6 | 4db9033f... | paasng.platform.applications.constants (AppFeatureFlag), paasng.platform.applications.models (ApplicationFeatureFlag), pytest (pytest), unittest (mock) |
| test_create_with_invalid_storage_size | 404-416 | 1 | 6d6e4806... | paasng.platform.applications.constants (AppFeatureFlag), paasng.platform.applications.models (ApplicationFeatureFlag), pytest (pytest), unittest (mock) |
| test_update | 418-428 | 2 | fea64e2f... | pytest (pytest) |
| test_destroy | 430-437 | 1 | 7b884b3b... | pytest (pytest) |
| test_destroy_with_bound | 439-456 | 1 | 37b3f23b... | paas_wl.bk_app.cnative.specs.constants (MountEnvName, VolumeSourceType), paas_wl.bk_app.cnative.specs.mounts (MountManager), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/apis/admin/test_helpers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_HelmReleaseParser | 66-85 | 1 | eef48999... | paas_wl.apis.admin.helpers.helm (DeployResult, HelmChart, HelmRelease, HelmReleaseParser) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/applications/models/test_app_managers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_empty_data | 26-29 | 1 | ce2a1865... | paas_wl.bk_app.applications.managers (WlAppMetadata), pytest (pytest) |
| test_valid_data | 31-33 | 1 | 96954f54... | paas_wl.bk_app.applications.managers (WlAppMetadata) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/applications/models/test_app_model.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_app_get_release | 28-36 | 2 | 33520496... | paas_wl.bk_app.applications.models (Release), tests.paas_wl.utils.release (create_release) |
| test_first_release | 38-40 | 1 | 68463c13... | django.core.exceptions (ObjectDoesNotExist), paas_wl.bk_app.applications.models (Release), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/applications/models/test_build.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_mark_as_latest_artifact | 27-37 | 4 | 03af09d1... | paas_wl.bk_app.applications.constants (ArtifactType), paas_wl.bk_app.applications.managers (mark_as_latest_artifact), paas_wl.bk_app.applications.models.build (Build), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/applications/models/test_command.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_new | 43-45 | 1 | 3d5ca7e7... |  |
| test_get_command | 47-60 | 1 | 2faeb2ef... | pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/applications/models/test_release.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_any_successful_empty | 26-27 | 1 | c38b9f5e... | paas_wl.bk_app.applications.models (Release) |
| test_any_successful_positive | 29-31 | 1 | e22bdb43... | paas_wl.bk_app.applications.models (Release) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/applications/test_api.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_app_ignore_duplicated | 33-45 | 4 | 0a70da5f... | django.conf (settings), paas_wl.bk_app.applications.api (create_app_ignore_duplicated), paas_wl.bk_app.applications.constants (WlAppType), pytest (pytest) |
| test_metadata_funcs | 48-52 | 2 | 6be3f443... | paas_wl.bk_app.applications.api (get_metadata_by_env, update_metadata_by_env), pytest (pytest) |
| test_delete_wl_resources | 55-59 | 2 | ba12d609... | paas_wl.bk_app.applications.api (delete_wl_resources), paas_wl.bk_app.applications.models (WlApp), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/cnative/specs/procs/test_replicas.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_scale_not_deployed | 39-41 | 1 | e81eb7da... | paas_wl.bk_app.cnative.specs.procs.exceptions (ProcNotDeployed), paas_wl.bk_app.cnative.specs.procs.replicas (BkAppProcScaler), pytest (pytest) |
| test_scale_proc_not_found | 43-46 | 1 | f322555e... | paas_wl.bk_app.cnative.specs.procs.exceptions (ProcNotFoundInRes), paas_wl.bk_app.cnative.specs.procs.replicas (BkAppProcScaler), pytest (pytest) |
| test_scale_integrated | 48-52 | 2 | 9ccb54b5... | paas_wl.bk_app.cnative.specs.procs.replicas (BkAppProcScaler), pytest (pytest) |
| test_set_autoscaling_not_deployed | 54-58 | 1 | 91b343d1... | paas_wl.bk_app.cnative.specs.procs.exceptions (ProcNotDeployed), paas_wl.bk_app.cnative.specs.procs.replicas (BkAppProcScaler), paas_wl.workloads.autoscaling.entities (AutoscalingConfig), pytest (pytest) |
| test_set_autoscaling_integrated | 60-86 | 4 | 3286293e... | paas_wl.bk_app.cnative.specs.procs.replicas (BkAppProcScaler), paas_wl.workloads.autoscaling.entities (AutoscalingConfig), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/cnative/specs/test_addresses.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_save_addresses | 31-49 | 4 | 7ce9dee3... | paas_wl.bk_app.cnative.specs.addresses (save_addresses), paas_wl.workloads.networking.ingress.models (AppDomain, AppSubpath), paasng.platform.modules.constants (ExposedURLType), tests.utils.helpers (override_region_configs), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_with_https | 54-79 | 3 | 4625d605... | paas_wl.bk_app.cnative.specs.addresses (to_domain), paas_wl.workloads.networking.ingress.constants (AppDomainSource), paas_wl.workloads.networking.ingress.models (AppDomain, AppDomainSharedCert), pytest (pytest) |
| test_normal | 84-95 | 3 | 6b7699a8... | paas_wl.bk_app.cnative.specs.addresses (Domain, to_shared_tls_domain), paas_wl.workloads.networking.ingress.models (AppDomainSharedCert) |
| test_integrated | 99-119 | 2 | 4ab2dfa1... | paas_wl.bk_app.cnative.specs.addresses (AddrResourceManager), paas_wl.workloads.networking.ingress.constants (AppDomainSource, AppSubpathSource), paas_wl.workloads.networking.ingress.models (AppDomain, AppSubpath, Domain) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/cnative/specs/test_configurations.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_global_envs | 29-43 | 1 | bfc85d4c... | paas_wl.bk_app.cnative.specs.configurations (EnvVarsReader), paas_wl.bk_app.cnative.specs.crd.bk_app (EnvVar), paas_wl.bk_app.cnative.specs.models (AppModelResource, create_app_resource), paasng.platform.engine.models.config_var (ENVIRONMENT_ID_FOR_GLOBAL), pytest (pytest) |
| test_overlay | 45-58 | 1 | a8ea5a10... | paas_wl.bk_app.cnative.specs.configurations (EnvVarsReader), paas_wl.bk_app.cnative.specs.crd.bk_app (EnvOverlay, EnvVarOverlay), paas_wl.bk_app.cnative.specs.models (AppModelResource, create_app_resource), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/cnative/specs/test_credentials.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_validate_references | 45-51 | 1 | 3fbf96aa... | django_dynamic_fixture (G), paas_wl.bk_app.cnative.specs.credentials (validate_references), paas_wl.bk_app.cnative.specs.exceptions (InvalidImageCredentials), paas_wl.workloads.images.entities (ImageCredentialRef), paas_wl.workloads.images.models (AppUserCredential), pytest (pytest) |
| test_save_image_credentials_missing | 54-57 | 1 | 444023ae... | django.db.models (ObjectDoesNotExist), paas_wl.workloads.images.entities (ImageCredentialRef), paas_wl.workloads.images.models (AppImageCredential), pytest (pytest) |
| test_save_image_credentials | 60-71 | 4 | 91caedb8... | django_dynamic_fixture (G), paas_wl.workloads.images.entities (ImageCredentialRef), paas_wl.workloads.images.models (AppImageCredential, AppUserCredential) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/cnative/specs/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_v1alpha2 | 78-80 | 1 | 5f201318... | paas_wl.bk_app.cnative.specs.models (create_app_resource) |
| test_filter_by_env | 122-125 | 2 | f2039b09... | paas_wl.bk_app.cnative.specs.models (AppModelDeploy), tests.paas_wl.bk_app.cnative.specs.utils (create_cnative_deploy) |
| test_any_successful | 127-131 | 2 | 188c90ae... | paas_wl.bk_app.cnative.specs.models (AppModelDeploy), tests.paas_wl.bk_app.cnative.specs.utils (create_cnative_deploy) |
| test_bkapp_name_with_default_module | 134-135 | 1 | 48d3abf7... | paas_wl.bk_app.cnative.specs.models (generate_bkapp_name) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/cnative/specs/test_mounts.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_deploy | 113-115 | 0 | 6a0dfadf... | paas_wl.bk_app.cnative.specs (mounts), pytest (pytest) |
| test_delete_configmap | 138-150 | 2 | ebb8079b... | paas_wl.bk_app.cnative.specs (mounts), paas_wl.bk_app.cnative.specs.mounts (init_volume_source_controller), paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.workloads.configuration.configmap.kres_entities (configmap_kmodel), pytest (pytest) |
| test_delete_pvc | 165-177 | 2 | 0588fd71... | paas_wl.bk_app.cnative.specs (mounts), paas_wl.bk_app.cnative.specs.mounts (init_volume_source_controller), paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.workloads.volume.persistent_volume_claim.kres_entities (pvc_kmodel), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/cnative/specs/test_resource.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_detect | 41-79 | 1 | 50d276dd... | paas_wl.bk_app.cnative.specs.constants (DeployStatus, MResConditionType, MResPhaseType), paas_wl.bk_app.cnative.specs.resource (MresConditionParser), pytest (pytest), tests.paas_wl.bk_app.cnative.specs.utils (create_condition, create_res, with_conds) |
| test_deploy_and_get_status_v1alpha2 | 86-114 | 3 | 21739eb2... | paas_wl.bk_app.cnative.specs.resource (deploy, get_mres_from_cluster), pytest (pytest), typing (Dict) |
| test_create_or_update_bkapp_with_retries | 116-147 | 2 | 16f4bffb... | kubernetes.client.exceptions (ApiException), paas_wl.bk_app.cnative.specs.resource (create_or_update_bkapp_with_retries), paas_wl.infras.resources.utils.basic (get_client_by_app), pytest (pytest), unittest (mock) |
| test_list | 152-176 | 3 | e31e5d1f... | paas_wl.bk_app.cnative.specs.resource (deploy, list_mres_by_env), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/cnative/specs/test_svc_disc.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 44-48 | 1 | 17876872... | paas_wl.bk_app.cnative.specs.svc_disc (ConfigMapManager, apply_configmap), pytest (pytest) |
| test_deletion | 50-59 | 2 | 1a68daf7... | paas_wl.bk_app.cnative.specs.svc_disc (ConfigMapManager, apply_configmap), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/cnative/specs/test_tasks.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_pending | 53-67 | 6 | ee2fea57... | blue_krill.async_utils.poll_task (PollingStatus), paas_wl.bk_app.cnative.specs.constants (DeployStatus), tests.paas_wl.bk_app.cnative.specs.utils (create_res, with_deploy_id), unittest.mock (patch) |
| test_progressing | 69-80 | 2 | 60a80d28... | blue_krill.async_utils.poll_task (PollingStatus), paas_wl.bk_app.cnative.specs.constants (DeployStatus, MResConditionType), tests.paas_wl.bk_app.cnative.specs.utils (create_condition, create_res, with_conds, with_deploy_id), unittest.mock (patch) |
| test_stable | 82-94 | 3 | 61c54e0c... | blue_krill.async_utils.poll_task (PollingStatus), paas_wl.bk_app.cnative.specs.constants (MResConditionType, MResPhaseType), tests.paas_wl.bk_app.cnative.specs.utils (create_condition, create_res, with_conds), unittest.mock (patch) |
| test_handle_failed | 98-102 | 2 | 9cf0895c... | blue_krill.async_utils.poll_task (CallbackResult, CallbackStatus), paas_wl.bk_app.cnative.specs.constants (DeployStatus), paasng.platform.engine.deploy.bg_wait.wait_bkapp (DeployStatusHandler) |
| test_handle_ready | 104-124 | 4 | c257e788... | arrow (arrow), blue_krill.async_utils.poll_task (CallbackResult, CallbackStatus), datetime (datetime), paas_wl.bk_app.cnative.specs.constants (DeployStatus), paas_wl.bk_app.cnative.specs.resource (ModelResState), paasng.platform.engine.deploy.bg_wait.wait_bkapp (AbortedDetails, DeployStatusHandler) |
| test_is_interrupted | 126-143 | 3 | 44c41f94... | blue_krill.async_utils.poll_task (CallbackResult, CallbackStatus), paas_wl.bk_app.cnative.specs.constants (DeployStatus), paasng.platform.engine.deploy.bg_wait.wait_bkapp (AbortedDetails, DeployStatusHandler) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/deploy/actions/test_delete.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 27-41 | 6 | 398f9d18... | paas_wl.bk_app.applications.models (Build, Release, WlApp), paas_wl.bk_app.deploy.actions.delete (delete_module_related_res), paas_wl.workloads.networking.ingress.models (Domain) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/deploy/actions/test_deploy.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_find_all_latest_mapper_v2 | 28-58 | 0 | f75badee... | paas_wl.bk_app.applications.managers (update_metadata), paas_wl.bk_app.deploy.actions.deploy (ObsoleteProcessesCleaner), pytest (pytest), tests.paas_wl.utils.wl_app (create_wl_release) |
| test_find_all_latest_mapper_v1 | 60-90 | 0 | def72689... | paas_wl.bk_app.applications.managers (update_metadata), paas_wl.bk_app.deploy.actions.deploy (ObsoleteProcessesCleaner), pytest (pytest), tests.paas_wl.utils.wl_app (create_wl_release) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/deploy/actions/test_exec.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_perform_successful | 59-79 | 3 | 7d3dd632... | paas_wl.bk_app.deploy.actions.exec (AppCommandExecutor), paas_wl.utils.constants (CommandStatus), pytest (pytest), unittest (mock) |
| test_perform_logs_unready | 81-96 | 3 | 6cae5855... | paas_wl.bk_app.deploy.actions.exec (AppCommandExecutor), paas_wl.utils.constants (CommandStatus), pytest (pytest), unittest (mock) |
| test_perform_but_pod_dead | 98-125 | 4 | e9051fa7... | paas_wl.bk_app.deploy.actions.exec (AppCommandExecutor), paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.utils.constants (CommandStatus), paas_wl.utils.kubestatus (HealthStatus, HealthStatusType), pytest (pytest), unittest (mock) |
| test_perform_but_be_interrupt | 127-159 | 3 | c11157b4... | datetime (datetime), paas_wl.bk_app.deploy.actions.exec (AppCommandExecutor), paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.utils.constants (CommandStatus), paas_wl.utils.kubestatus (HealthStatus, HealthStatusType), pytest (pytest), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/deploy/app_res/test_controllers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_run | 75-83 | 3 | 6e2b235b... | paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.workloads.release_controller.hooks.kres_entities (command_kmodel), pytest (pytest) |
| test_run_with_sidecar | 104-113 | 4 | 01fc25c9... | paas_wl.infras.resources.base.exceptions (PodTimeoutError), paas_wl.workloads.release_controller.hooks.kres_entities (command_kmodel), pytest (pytest) |
| test_delete_with_sidecar | 115-126 | 3 | bfaa6f20... | paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.workloads.release_controller.hooks.kres_entities (command_kmodel), pytest (pytest) |
| test_deploy_processes | 142-170 | 10 | 10a87b59... | paas_wl.bk_app.deploy.app_res.controllers (ProcessesHandler), paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), pytest (pytest), unittest.mock (patch) |
| test_scale_process | 172-187 | 4 | d2832a31... | paas_wl.bk_app.deploy.app_res.controllers (ProcessesHandler), paas_wl.infras.resources.generation.mapper (get_mapper_proc_config_latest), unittest.mock (patch) |
| test_shutdown_process | 189-212 | 4 | ebb0d2a5... | dataclasses (make_dataclass), paas_wl.bk_app.deploy.app_res.controllers (ProcessesHandler), paas_wl.infras.resources.generation.mapper (get_mapper_proc_config_latest), unittest.mock (Mock, patch) |
| test_shutdown_web_processes | 214-242 | 4 | 5da019d7... | dataclasses (make_dataclass), paas_wl.bk_app.deploy.app_res.controllers (ProcessesHandler), paas_wl.infras.resources.generation.mapper (get_mapper_proc_config_latest), unittest.mock (Mock, patch) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/deploy/app_res/test_controllers_builder.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_build_slug | 71-98 | 7 | 43c6746a... | kubernetes.dynamic.resource (ResourceInstance), paas_wl.utils.kubestatus (parse_pod), unittest.mock (Mock, patch) |
| test_build_slug_exist | 100-118 | 1 | d8f4455c... | django.utils (timezone), kubernetes.dynamic.resource (ResourceInstance), paas_wl.infras.resources.base.exceptions (ResourceDuplicate), pytest (pytest), unittest.mock (Mock, patch) |
| test_delete_builder_pod | 120-134 | 4 | b35c7919... | kubernetes.dynamic.resource (ResourceInstance), unittest.mock (Mock, patch) |
| test_delete_builder_pod_missing | 136-146 | 2 | 5d3536c5... | paas_wl.infras.resources.base.exceptions (ResourceMissing), unittest.mock (Mock, patch) |
| test_delete_builder_pod_running | 148-159 | 2 | ffebe990... | kubernetes.dynamic.resource (ResourceInstance), unittest.mock (Mock, patch) |
| test_interrupt_builder | 166-178 | 1 | eddf243c... | conftest (construct_foo_pod), paas_wl.bk_app.deploy.app_res.controllers (BuildHandler), paas_wl.infras.resources.base.kres (KPod), paasng.platform.engine.deploy.bg_build.utils (generate_builder_name) |
| test_interrupt_builder_non_existent | 180-187 | 1 | 6ca54206... | paasng.platform.engine.deploy.bg_build.utils (generate_builder_name) |
| test_wait_for_succeeded_no_pod | 189-191 | 1 | d96eb152... | paas_wl.infras.resources.base.exceptions (PodAbsentError), paasng.platform.engine.deploy.bg_build.utils (generate_builder_name), pytest (pytest) |
| test_wait_for_succeeded | 193-213 | 0 | 146f8e22... | blue_krill.contextlib (nullcontext), conftest (construct_foo_pod), paas_wl.bk_app.deploy.app_res.controllers (BuildHandler), paas_wl.infras.resources.base.exceptions (PodNotSucceededError, PodTimeoutError), paas_wl.infras.resources.base.kres (KPod, PatchType), paasng.platform.engine.deploy.bg_build.utils (generate_builder_name), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/deploy/test_engine_svc.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_build | 31-35 | 2 | 34e085d4... | paas_wl.bk_app.applications.models (Build), paasng.platform.engine.utils.client (EngineDeployClient) |
| test_upsert_image_credentials | 37-46 | 5 | c73b7dca... | paas_wl.workloads.images.models (AppImageCredential), paasng.platform.engine.utils.client (EngineDeployClient), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/deploy/test_processes.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_set_start | 45-53 | 3 | 83fb453f... | paas_wl.bk_app.deploy.processes (ProcSpecUpdater), paas_wl.bk_app.processes.constants (ProcessTargetStatus) |
| test_set_stop | 55-61 | 2 | d200b04c... | paas_wl.bk_app.deploy.processes (ProcSpecUpdater), paas_wl.bk_app.processes.constants (ProcessTargetStatus) |
| test_change_replicas_integrated | 63-74 | 4 | ce9d1908... | paas_wl.bk_app.deploy.processes (ProcSpecUpdater), paas_wl.bk_app.processes.constants (ProcessTargetStatus) |
| test_set_autoscaling_integrated | 76-99 | 6 | 6d5aab3c... | paas_wl.bk_app.deploy.processes (ProcSpecUpdater), paas_wl.bk_app.processes.constants (ProcessTargetStatus), paas_wl.workloads.autoscaling.entities (AutoscalingConfig) |
| test_scale_static_integrated | 123-136 | 4 | faeb9aae... | paas_wl.bk_app.cnative.specs.procs.replicas (BkAppProcScaler), paas_wl.bk_app.deploy.processes (CNativeProcController), pytest (pytest) |
| test_autoscaling_integrated | 138-153 | 3 | 970db252... | paas_wl.bk_app.cnative.specs.procs.replicas (BkAppProcScaler), paas_wl.bk_app.deploy.processes (CNativeProcController), paas_wl.infras.cluster.constants (ClusterFeatureFlag), paas_wl.infras.cluster.utils (get_cluster_by_app), paas_wl.workloads.autoscaling.entities (AutoscalingConfig), pytest (pytest) |
| test_scale_down_to_module_target_replicas | 155-168 | 3 | 93c578af... | paas_wl.bk_app.deploy.processes (CNativeProcController), paasng.platform.bkapp_model.models (ModuleProcessSpec), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/dev_sandbox/test_controller.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_deploy_success | 61-74 | 7 | 8ff3c23a... | paas_wl.bk_app.dev_sandbox.kres_entities (get_dev_sandbox_service_name, get_ingress_name, get_sub_domain_host), pytest (pytest) |
| test_deploy_when_already_exists | 76-79 | 1 | bd19bd4d... | paas_wl.bk_app.dev_sandbox.exceptions (DevSandboxAlreadyExists), pytest (pytest) |
| test_get_sandbox_detail | 81-86 | 3 | 764b3007... | paas_wl.bk_app.dev_sandbox.kres_entities (get_sub_domain_host), pytest (pytest) |
| test_deploy_success | 115-145 | 11 | 51be4293... | paas_wl.bk_app.dev_sandbox.kres_entities (get_dev_sandbox_service_name, get_ingress_name, get_sub_domain_host), paas_wl.bk_app.dev_sandbox.kres_entities.code_editor (get_code_editor_name), pytest (pytest) |
| test_deploy_when_already_exists | 147-163 | 1 | d814ead2... | paas_wl.bk_app.dev_sandbox.exceptions (DevSandboxAlreadyExists), paasng.platform.sourcectl.models (VersionInfo), pathlib (Path), pytest (pytest), unittest (mock) |
| test_get_sandbox_detail | 165-185 | 7 | 8b5e93b9... | django.conf (settings), paas_wl.bk_app.dev_sandbox.kres_entities (get_sub_domain_host), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/dev_sandbox/test_kres_slzs.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_serialize | 54-95 | 1 | 4315033c... | django.conf (settings), paas_wl.bk_app.dev_sandbox.kres_entities (DevSandbox), paas_wl.bk_app.dev_sandbox.kres_slzs (DevSandboxSerializer, get_dev_sandbox_labels) |
| test_serialize_with_source_code_config | 97-145 | 1 | 6eb60cc4... | django.conf (settings), paas_wl.bk_app.dev_sandbox.kres_entities (DevSandbox), paas_wl.bk_app.dev_sandbox.kres_slzs (DevSandboxSerializer, get_dev_sandbox_labels) |
| test_serialize | 158-181 | 1 | 2d9b5cfa... | django.conf (settings), paas_wl.bk_app.dev_sandbox.kres_entities (DevSandboxService, get_dev_sandbox_service_name), paas_wl.bk_app.dev_sandbox.kres_slzs (DevSandboxServiceSerializer, get_dev_sandbox_labels) |
| test_serialize | 194-247 | 3 | b8b6f89a... | paas_wl.bk_app.dev_sandbox.kres_entities (DevSandboxIngress, get_code_editor_service_name, get_dev_sandbox_service_name), paas_wl.bk_app.dev_sandbox.kres_slzs (DevSandboxIngressSerializer) |
| test_serialize_with_user | 249-311 | 3 | 498f21d6... | paas_wl.bk_app.dev_sandbox.kres_entities (DevSandboxIngress, get_code_editor_service_name, get_dev_sandbox_service_name), paas_wl.bk_app.dev_sandbox.kres_slzs (DevSandboxIngressSerializer) |
| test_serialize | 324-370 | 1 | eea2dede... | django.conf (settings), paas_wl.bk_app.dev_sandbox.kres_entities (CodeEditor), paas_wl.bk_app.dev_sandbox.kres_slzs (CodeEditorSerializer, get_code_editor_labels) |
| test_serialize | 383-405 | 1 | 73ee5170... | django.conf (settings), paas_wl.bk_app.dev_sandbox.kres_entities (CodeEditorService, get_code_editor_service_name), paas_wl.bk_app.dev_sandbox.kres_slzs (CodeEditorServiceSerializer, get_code_editor_labels) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/event/test_reader.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_query_events | 76-81 | 3 | c9ed3ada... | paas_wl.workloads.event.reader (event_kmodel) |
| test_query_events_without_count | 83-88 | 3 | e0c48744... | paas_wl.workloads.event.reader (event_kmodel) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/mgrlegacy/test_processes.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_processes_info | 27-38 | 3 | 433ef7b6... | paas_wl.bk_app.mgrlegacy.processes (get_processes_info), paas_wl.bk_app.processes.kres_entities (Instance), tests.paas_wl.bk_app.processes.test_controllers (make_process) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/monitoring/app_monitor/test_managers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 62-69 | 4 | 3fa73010... | django_dynamic_fixture (G), paas_wl.bk_app.monitoring.app_monitor (constants), paas_wl.bk_app.monitoring.app_monitor.managers (build_service_monitor), paas_wl.bk_app.monitoring.app_monitor.models (AppMetricsMonitor) |
| test_with_extra_field | 71-83 | 1 | 9d4a0567... | django_dynamic_fixture (G), dynaconf.utils.parse_conf (parse_conf_data), paas_wl.bk_app.monitoring.app_monitor.managers (build_service_monitor), paas_wl.bk_app.monitoring.app_monitor.models (AppMetricsMonitor) |
| test_normal | 116-130 | 4 | 31f7dd8f... | paas_wl.bk_app.monitoring.app_monitor.managers (build_service_monitor, service_monitor_kmodel), paas_wl.bk_app.monitoring.app_monitor.shim (make_bk_monitor_controller), paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), pytest (pytest), unittest (mock) |
| test_no_monitor | 132-137 | 2 | 6df24eb8... | paas_wl.bk_app.monitoring.app_monitor.shim (make_bk_monitor_controller), unittest (mock) |
| test_disable | 139-145 | 2 | 1bc1e683... | paas_wl.bk_app.monitoring.app_monitor.shim (make_bk_monitor_controller), unittest (mock) |
| test_global_disable | 147-152 | 1 | ff55d0f1... | paas_wl.bk_app.monitoring.app_monitor.shim (make_bk_monitor_controller), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/monitoring/app_monitor/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_build_monitor_port | 27-36 | 5 | 6221a49c... | django_dynamic_fixture (G), paas_wl.bk_app.monitoring.app_monitor.models (AppMetricsMonitor), paas_wl.bk_app.monitoring.app_monitor.utils (build_monitor_port) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/monitoring/bklog/test_kres_slzs.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_serialize | 79-91 | 1 | 02ee1021... | cattrs (cattrs), paas_wl.bk_app.monitoring.bklog.entities (LabelSelector), paas_wl.bk_app.monitoring.bklog.kres_entities (BkAppLogConfig), paas_wl.bk_app.monitoring.bklog.kres_slzs (BKLogConfigSerializer) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/processes/test_controllers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_processes | 48-61 | 1 | cccad756... | paas_wl.bk_app.processes.controllers (list_processes), paas_wl.bk_app.processes.kres_entities (Instance) |
| test_list_processes_with_dirty_release | 64-65 | 1 | 99269dc2... | paas_wl.bk_app.processes.controllers (list_processes) |
| test_list_processes_boundary_case | 68-87 | 1 | b97bc74d... | paas_wl.bk_app.processes.controllers (list_processes), paas_wl.bk_app.processes.kres_entities (Instance) |
| test_list_processes_without_release | 90-95 | 1 | 5a8ba4e0... | paas_wl.bk_app.processes.controllers (list_processes), paas_wl.bk_app.processes.kres_entities (Instance) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/processes/test_exceptions.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_string_representation | 26-35 | 1 | 7da97411... | paas_wl.bk_app.processes.exceptions (ScaleProcessError), pytest (pytest) |
| test_caused_by_not_found | 37-49 | 2 | dc7cacc9... | kubernetes.dynamic.exceptions (NotFoundError), paas_wl.bk_app.processes.exceptions (ScaleProcessError), unittest.mock (Mock) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/processes/test_managers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_query_instances | 91-98 | 5 | 494dc950... | paas_wl.bk_app.processes.readers (instance_kmodel) |
| test_query_instances_without_process_id_label | 100-110 | 1 | b94c2031... | paas_wl.bk_app.processes.readers (instance_kmodel), paas_wl.infras.resources.base.kres (KPod) |
| test_watch_from_rv0 | 112-121 | 1 | 73b8e769... | paas_wl.bk_app.processes.readers (instance_kmodel), paas_wl.infras.resources.base.kres (KPod) |
| test_watch_from_empty_rv | 123-131 | 2 | b0d27d40... | paas_wl.bk_app.processes.readers (instance_kmodel) |
| test_watch_unknown_res | 133-150 | 3 | e7916514... | paas_wl.bk_app.processes.readers (instance_kmodel), paas_wl.infras.resources.base.kres (KPod) |
| test_get_logs | 152-157 | 1 | a99fcda4... | paas_wl.bk_app.processes.readers (instance_kmodel), unittest (mock) |
| test_list_by_app_with_meta | 159-165 | 3 | e8e00e74... | paas_wl.bk_app.processes.readers (instance_kmodel) |
| test_list | 173-193 | 4 | 33eb8b05... | paas_wl.bk_app.processes.readers (instance_kmodel), tests.paas_wl.infras.resources.base.test_kres (ResourceInstance), tests.paas_wl.utils.basic (make_container_status), types (SimpleNamespace), unittest (mock) |
| test_query_instances | 204-215 | 4 | 5090894f... | paas_wl.bk_app.processes.readers (process_kmodel) |
| test_watch_from_rv0 | 217-223 | 4 | 17a5836f... | paas_wl.bk_app.processes.readers (process_kmodel) |
| test_main | 227-244 | 1 | 9a6e1ddb... | django.conf (settings), paas_wl.bk_app.processes.kres_slzs (extract_type_from_name), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/processes/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_sync | 38-55 | 8 | 1e874b49... | paas_wl.bk_app.processes.models (ProcessSpec, ProcessSpecManager), paasng.platform.engine.models.deployment (ProcessTmpl) |
| test_switch | 57-102 | 15 | 36ccafa8... | paas_wl.bk_app.processes.models (ProcessSpec, ProcessSpecManager), paasng.platform.bkapp_model.entities (AutoscalingConfig), paasng.platform.engine.models.deployment (ProcessTmpl) |
| test_sync | 106-156 | 10 | 40b0dae1... | paas_wl.bk_app.processes.constants (ProbeType), paas_wl.bk_app.processes.models (ProcessProbe, ProcessProbeManager), paasng.platform.bkapp_model.entities (ExecAction, HTTPGetAction, Probe, ProbeSet, TCPSocketAction), paasng.platform.engine.models.deployment (ProcessTmpl) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/processes/test_processes.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_cnative_module_processes_specs | 87-137 | 2 | 44ede6a0... | paas_wl.bk_app.cnative.specs.crd.bk_app (BkAppResource), paas_wl.bk_app.processes.processes (list_cnative_module_processes_specs), pytest (pytest), unittest (mock) |
| test_get_previous_logs | 141-157 | 1 | d2ada7c3... | paas_wl.bk_app.processes.processes (ProcessManager), paas_wl.infras.resources.base.kres (KPod), paas_wl.infras.resources.utils.basic (get_client_by_app), tests.paas_wl.infras.resources.base.test_kres (construct_foo_pod) |
| test_list_cnative_processes_specs | 159-177 | 1 | 0e037c0c... | paas_wl.bk_app.cnative.specs.crd.bk_app (BkAppResource), paas_wl.bk_app.processes.processes (ProcessManager), pytest (pytest), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/processes/test_watch.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 26-33 | 1 | 0f7de9a1... | paas_wl.bk_app.processes.watch (ParallelChainedGenerator, WatchEvent) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/bk_app/test_process.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_command_name_normal | 38-44 | 2 | 6af4ca7a... | paas_wl.bk_app.processes.managers (AppProcessManager), paas_wl.utils.command (get_command_name) |
| test_command_name_celery | 46-49 | 1 | 8ff08b5a... | paas_wl.bk_app.processes.managers (AppProcessManager), paas_wl.utils.command (get_command_name) |
| test_commnad_name_with_slash | 51-58 | 2 | 3f567dfa... | paas_wl.bk_app.processes.managers (AppProcessManager), paas_wl.utils.command (get_command_name) |
| test_assemble_process | 72-86 | 7 | 4031e813... | django.conf (settings), paas_wl.bk_app.processes.managers (AppProcessManager), paas_wl.utils.command (get_command_name), tests.paas_wl.utils.wl_app (create_wl_release) |
| test_assemble_processes | 88-101 | 1 | 8ce22b46... | paas_wl.bk_app.processes.managers (AppProcessManager), tests.paas_wl.utils.wl_app (create_wl_release) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/core/test_env.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_default_app_env_is_running | 28-41 | 4 | 3a110a92... | paas_wl.core.env (env_is_running), pytest (pytest), tests.paas_wl.workloads.conftest (create_release) |
| test_cnative_app_env_is_running | 43-52 | 3 | c6744679... | paas_wl.core.env (env_is_running), tests.paas_wl.bk_app.cnative.specs.utils (create_cnative_deploy) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/core/test_resource.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_process_selector | 25-28 | 2 | ec7c82ab... | paas_wl.core.resource (get_process_selector) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/e2e/ingress/v0_21_0/test_case.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get | 25-63 | 6 | 7002178a... | pytest (pytest), urllib.parse (urljoin) |
| test_post | 66-105 | 7 | 01c5d01c... | pytest (pytest), urllib.parse (urljoin) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/e2e/ingress/v0_22_0/test_case.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get | 25-63 | 6 | 631aed15... | pytest (pytest), urllib.parse (urljoin) |
| test_post | 66-105 | 7 | 1e8e0206... | pytest (pytest), urllib.parse (urljoin) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/e2e/ingress/v1_0_0/test_case.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get | 25-62 | 5 | 33a73f24... | pytest (pytest), urllib.parse (urljoin) |
| test_post | 65-103 | 6 | 04a5e53c... | pytest (pytest), urllib.parse (urljoin) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/cluster/test_commands.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_init_cluster | 47-74 | 9 | dc8ffe78... | django.core.management (call_command), os (os), paas_wl.infras.cluster.models (APIServer, Cluster), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/cluster/test_loader.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_all_cluster_names | 66-68 | 1 | 37aa36a9... | paas_wl.infras.cluster.loaders (DBConfigLoader) |
| test_list_configurations_by_name | 70-84 | 2 | 915ba314... | paas_wl.infras.cluster.loaders (DBConfigLoader), pytest (pytest), urllib.parse (urlparse) |
| test_auth_types | 88-101 | 1 | e1e0c3e6... | paas_wl.infras.cluster.loaders (DBConfigLoader), paas_wl.infras.cluster.models (Cluster), pytest (pytest) |
| test_get_all_tags | 107-109 | 1 | 04a389a4... | paas_wl.infras.cluster.loaders (LegacyKubeConfigLoader) |
| test_list_configurations_by_tag | 111-126 | 2 | f56ed6be... | paas_wl.infras.cluster.loaders (LegacyKubeConfigLoader), pytest (pytest), urllib.parse (urlparse) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/cluster/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_register | 51-61 | 0 | 1c7c19ef... | blue_krill.contextlib (nullcontext), django.utils.crypto (get_random_string), paas_wl.infras.cluster.exceptions (NoDefaultClusterError), paas_wl.infras.cluster.models (Cluster), pytest (pytest) |
| test_use_register_cluster_to_change_default_cluster | 63-71 | 1 | 5a006054... | paas_wl.infras.cluster.exceptions (SwitchDefaultClusterError), paas_wl.infras.cluster.models (Cluster), pytest (pytest) |
| test_register_duplicated_default_cluster | 73-76 | 1 | ccd0d51d... | paas_wl.infras.cluster.exceptions (DuplicatedDefaultClusterError), pytest (pytest) |
| test_register_duplicated_cluster_name | 78-85 | 1 | 58e8127d... | django.db.utils (IntegrityError), django.utils.crypto (get_random_string), paas_wl.infras.cluster.models (Cluster), pytest (pytest) |
| test_switch_default_cluster | 87-99 | 0 | b89442e4... | blue_krill.contextlib (nullcontext), paas_wl.infras.cluster.exceptions (SwitchDefaultClusterError), paas_wl.infras.cluster.models (Cluster), pytest (pytest) |
| test_token | 101-107 | 2 | b6b15cbf... | paas_wl.infras.cluster.constants (ClusterTokenType), paas_wl.infras.cluster.models (Cluster) |
| test_port_map | 111-128 | 7 | 83f31df8... | paas_wl.infras.cluster.models (Cluster, IngressConfig, PortMap) |
| test_domains | 130-143 | 9 | 1cb4e3aa... | paas_wl.infras.cluster.models (Cluster, Domain, IngressConfig) |
| test_find_app_root_domain | 145-158 | 4 | 67467f91... | cattr (cattr), paas_wl.infras.cluster.models (IngressConfig) |
| test_create_normal | 162-165 | 2 | f15bd7c5... | paas_wl.infras.cluster.models (EnhancedConfiguration) |
| test_create_force_hostname | 167-170 | 2 | 35b3527e... | paas_wl.infras.cluster.models (EnhancedConfiguration) |
| test_create_invalid_values | 172-174 | 1 | 5c39b434... | paas_wl.infras.cluster.models (EnhancedConfiguration), pytest (pytest) |
| test_extract_ip | 176-187 | 1 | 99a65b4a... | paas_wl.infras.cluster.models (EnhancedConfiguration), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/cluster/test_shim.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_empty_cluster_field | 38-44 | 1 | 1cb40f24... | paas_wl.infras.cluster.shim (EnvClusterService) |
| test_valid_cluster_field | 46-52 | 1 | fc3ec89f... | paas_wl.infras.cluster.shim (EnvClusterService) |
| test_invalid_cluster_field | 54-61 | 1 | 67bd22e7... | paas_wl.infras.cluster.shim (Cluster, EnvClusterService), pytest (pytest) |
| test_get_cluster | 64-70 | 4 | 2c8ba32e... | paas_wl.infras.cluster.shim (Cluster, RegionClusterService), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/cluster/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_cluster_by_app_normal | 53-56 | 1 | 19142fc0... | paas_wl.infras.cluster.utils (get_cluster_by_app), tests.paas_wl.utils.wl_app (create_wl_app) |
| test_get_cluster_by_app_cluster_configured | 58-65 | 1 | 63662f45... | paas_wl.infras.cluster.utils (get_cluster_by_app), tests.paas_wl.utils.wl_app (create_wl_app) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/resource_templates/test_addons.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_sidecar | 31-42 | 6 | 3afd3381... | cattr (cattr), paas_wl.infras.resource_templates.components.sidecar (Container), paas_wl.infras.resource_templates.managers (AddonManager), typing (List) |
| test_default_readiness_probe | 44-46 | 1 | 2183ca52... | paas_wl.infras.resource_templates.components.probe (get_default_readiness_probe), paas_wl.infras.resource_templates.managers (AddonManager) |
| test_user_readiness_probe | 48-55 | 4 | 37cf989c... | paas_wl.infras.resource_templates.components.probe (get_default_readiness_probe), paas_wl.infras.resource_templates.managers (AddonManager) |
| test_shm_mount_point | 57-66 | 4 | 905591bb... | paas_wl.infras.resource_templates.managers (AddonManager) |
| test_shm_volume | 68-79 | 6 | 830b8ce2... | paas_wl.infras.resource_templates.managers (AddonManager) |
| test_secret_volume | 81-95 | 9 | 46b464ad... | paas_wl.infras.resource_templates.managers (AddonManager) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/resource_templates/test_process_probe.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_process_probe_mgr | 28-52 | 7 | 53ed2392... | django.test (override_settings), paas_wl.bk_app.processes.constants (ProbeType), paas_wl.bk_app.processes.models (ProcessProbe), paas_wl.infras.resource_templates.managers (ProcessProbeManager) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/resources/base/test_credentials.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_empty | 44-49 | 3 | 887d6102... | paas_wl.bk_app.deploy.app_res.controllers (ensure_image_credentials_secret), paas_wl.utils.text (b64encode), paas_wl.workloads.images (constants), paas_wl.workloads.images.kres_entities (credentials_kmodel) |
| test_create | 51-66 | 3 | 1a3142ed... | django.utils.crypto (get_random_string), json (json), paas_wl.bk_app.deploy.app_res.controllers (ensure_image_credentials_secret), paas_wl.utils.text (b64decode, b64encode), paas_wl.workloads.images (constants), paas_wl.workloads.images.kres_entities (credentials_kmodel), paas_wl.workloads.images.models (AppImageCredential) |
| test_update | 68-76 | 2 | edb15eb4... | paas_wl.bk_app.deploy.app_res.controllers (ensure_image_credentials_secret), paas_wl.workloads.images.kres_entities (credentials_kmodel), paas_wl.workloads.images.models (AppImageCredential) |
| test_not_found | 78-80 | 1 | ef6f31ee... | paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.workloads.images.kres_entities (credentials_kmodel), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/resources/base/test_kres.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_versions | 44-46 | 2 | ef3f9f7e... | paas_wl.infras.resources.base.kres (KNamespace) |
| test_delete | 48-49 | 0 | 96f70160... | paas_wl.infras.resources.base.kres (KNamespace), tests.paas_wl.utils.basic (random_resource_name) |
| test_delete_non_silent | 51-53 | 1 | dee1ae90... | paas_wl.infras.resources.base.exceptions (ResourceMissing), paas_wl.infras.resources.base.kres (KNamespace), pytest (pytest), tests.paas_wl.utils.basic (random_resource_name) |
| test_delete_api_error | 55-59 | 1 | 2ae50d89... | kubernetes.client.rest (ApiException), paas_wl.infras.resources.base.kres (KNamespace), pytest (pytest), tests.paas_wl.utils.basic (random_resource_name), unittest (mock) |
| test_get_or_create | 61-69 | 4 | 4d8a5c2b... | tests.paas_wl.utils.basic (random_resource_name) |
| test_create_or_update | 71-89 | 8 | fda251ab... | paas_wl.infras.resources.base.kres (KDeployment), tests.paas_wl.utils.basic (random_resource_name) |
| test_replace_or_patch | 91-100 | 1 | 825c44d2... | paas_wl.infras.resources.base.kres (KDeployment) |
| test_patch | 102-112 | 1 | a6b9f80d... | paas_wl.infras.resources.base.kres (KDeployment) |
| test_create_watch_stream | 117-128 | 1 | a570a586... | paas_wl.infras.resources.base.kres (KPod) |
| test_filter_by_labels | 130-141 | 3 | cb40c5d9... | kubernetes.dynamic.resource (ResourceInstance), paas_wl.infras.resources.base.kres (KPod) |
| test_list_with_different_namespaces | 143-164 | 6 | 54286407... | paas_wl.infras.resources.base.kres (KPod), tests.paas_wl.utils.basic (random_resource_name) |
| test_delete_collection | 166-180 | 1 | 7074d747... | paas_wl.infras.resources.base.kres (KPod), pytest (pytest), time (time) |
| test_delete_individual | 182-198 | 1 | 1075c838... | paas_wl.infras.resources.base.kres (KPod), pytest (pytest), time (time) |
| test_make_fields_string | 200-213 | 1 | 825a3e3b... | paas_wl.infras.resources.base.kres (BatchOperations), pytest (pytest) |
| test_has_default_sa_with_or_without_secrets | 217-226 | 1 | 9c97c11f... | paas_wl.infras.resources.base.kres (KNamespace, KServiceAccount), typing (Any, Dict) |
| test_wait_for_default_sa_failed | 228-237 | 3 | fa3ba39f... | math (math), paas_wl.infras.resources.base.exceptions (CreateServiceAccountTimeout), paas_wl.infras.resources.base.kres (KNamespace), pytest (pytest), time (time), unittest (mock) |
| test_wait_for_default_sa_succeed | 239-251 | 3 | 97ecc506... | paas_wl.infras.resources.base.kres (KNamespace, KServiceAccount), typing (Any, Dict) |
| test_wait_for_status_no_resource | 256-267 | 3 | d8284443... | paas_wl.infras.resources.base.exceptions (ReadTargetStatusTimeout), paas_wl.infras.resources.base.kres (KPod), pytest (pytest), tests.paas_wl.utils.basic (random_resource_name), time (time) |
| test_wait_for_status_normal | 269-282 | 1 | 6d17fa8a... | paas_wl.infras.resources.base.kres (KPod) |
| test_get_logs | 284-291 | 1 | 2d0b40cd... | paas_wl.infras.resources.base.kres (KPod) |
| test_restart | 295-303 | 1 | 4410d3c3... | paas_wl.infras.resources.base.constants (KUBECTL_RESTART_RESOURCE_KEY), paas_wl.infras.resources.base.kres (KDeployment) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/resources/generation/test_generation.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_v1_pod_name | 49-60 | 2 | e90a1429... | paas_wl.utils.command (get_command_name) |
| test_preset_process_client | 62-67 | 1 | c9b2abc1... | paas_wl.utils.command (get_command_name) |
| test_v2_name | 69-77 | 2 | 6f0bbaf9... |  |
| test_get_proc_deployment_name | 80-81 | 1 | 1f0f8610... | paas_wl.infras.resources.generation.version (get_proc_deployment_name) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/resources/kube_res/test_base.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_initialize_non_applicable_type | 39-47 | 1 | 3a476254... | paas_wl.infras.resources.base.kres (KNamespace), paas_wl.infras.resources.kube_res.base (AppEntity, AppEntityManager, AppEntityReader), pytest (pytest) |
| test_watch_with_error_event | 74-89 | 4 | ff47e6f3... | kubernetes.client.exceptions (ApiException), unittest (mock) |
| test_watch_with_expired_exception | 91-95 | 1 | e5ea955c... | kubernetes.client.exceptions (ApiException), pytest (pytest), unittest (mock) |
| test_create | 102-105 | 0 | be7349c6... |  |
| test_version_incompatible | 108-125 | 1 | 4d5d7a45... | dataclasses (dataclass), paas_wl.infras.resources.base.kres (KNamespace), paas_wl.infras.resources.kube_res.base (AppEntity, AppEntityDeserializer, AppEntityReader), paas_wl.infras.resources.kube_res.exceptions (APIServerVersionIncompatible), pytest (pytest) |
| test_priority | 161-177 | 1 | 211142e4... | paas_wl.infras.resources.kube_res.base (EntitySerializerPicker), pytest (pytest) |
| test_api_version_not_supported | 179-191 | 1 | b3d2dbd9... | paas_wl.infras.resources.kube_res.base (EntitySerializerPicker), paas_wl.infras.resources.kube_res.exceptions (APIServerVersionIncompatible), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/resources/utils/test_app.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_update_process_deploy_info | 36-54 | 4 | b9412148... | paas_wl.bk_app.processes.managers (AppProcessManager) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/infras/resources/utils/test_basic.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_empty | 30-31 | 1 | fe83e532... | paas_wl.infras.resources.utils.basic (get_full_node_selector) |
| test_integrated | 33-42 | 1 | 8bb646d3... | paas_wl.infras.cluster.utils (get_cluster_by_app), paas_wl.infras.resources.utils.basic (get_full_node_selector) |
| test_with_cluster_state | 44-54 | 2 | 02a791a5... | django.conf (settings), django.core.management (call_command), paas_wl.infras.resources.utils.basic (get_full_node_selector), paas_wl.workloads.networking.egress.models (RCStateAppBinding, RegionClusterState) |
| test_empty | 58-59 | 1 | 9a0c9b32... | paas_wl.infras.resources.utils.basic (get_full_tolerations) |
| test_integrated | 61-74 | 1 | b98b760e... | paas_wl.infras.cluster.utils (get_cluster_by_app), paas_wl.infras.resources.utils.basic (get_full_tolerations) |
| test_condensed_list_valid | 80-88 | 1 | 926c51e2... | paas_wl.infras.resources.utils.basic (standardize_tolerations) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/test_utils/test_env_vars.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_render_vars_dict | 19-37 | 1 | 3962589a... | paas_wl.utils.env_vars (VarsRenderContext, render_vars_dict) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/test_utils/test_kubestatus.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_parse_pod | 38-53 | 1 | ba2da1cd... | kubernetes.client.models (V1Container, V1Pod, V1PodSpec), kubernetes.dynamic.resource (ResourceInstance), paas_wl.utils.kubestatus (parse_pod), pytest (pytest) |
| test_extract_exit_code | 56-66 | 1 | 3dd6dc21... | paas_wl.utils.kubestatus (extract_exit_code), pytest (pytest) |
| test_get_any_container_fail_message | 69-93 | 1 | 21246296... | kubernetes.dynamic.resource (ResourceInstance), paas_wl.utils.kubestatus (get_any_container_fail_message, parse_pod), pytest (pytest), tests.paas_wl.utils.basic (make_container_status) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/test_utils/test_main.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_make_enum_choices | 30-35 | 1 | 4a0eda41... | enum (Enum), paas_wl.utils.constants (make_enum_choices) |
| test_short_str | 39-41 | 2 | f551bb2a... | paas_wl.utils.basic (digest_if_length_exceeded) |
| test_long_str | 43-46 | 3 | e0b53785... | paas_wl.utils.basic (digest_if_length_exceeded) |
| test_make_json_field | 79-82 | 1 | 33ef9158... | django.utils.crypto (get_random_string), paas_wl.utils.models (make_json_field) |
| test_get_prep_value | 84-102 | 1 | b84b99a7... | pytest (pytest) |
| test_convert_key_to_camel | 106-136 | 1 | ba248352... | paas_wl.utils.basic (convert_key_to_camel), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/autoscaling/test_kres_slzs.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_ProcAutoscalingSerializer | 125-134 | 2 | 4f4be528... | paas_wl.bk_app.processes.kres_entities (Process), paas_wl.infras.resources.generation.version (get_mapper_version), paas_wl.workloads.autoscaling.kres_entities (ProcAutoscaling), paas_wl.workloads.autoscaling.kres_slzs (ProcAutoscalingSerializer) |
| test_ProcAutoscalingDeserializer | 137-139 | 1 | f240afaa... | kubernetes.dynamic (ResourceInstance), paas_wl.workloads.autoscaling.kres_entities (ProcAutoscaling), paas_wl.workloads.autoscaling.kres_slzs (ProcAutoscalingDeserializer) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/egress/test_region.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 73-87 | 4 | c134b4a4... | django.core.management (call_command), paas_wl.infras.resources.base.kres (KNode), paas_wl.workloads.networking.egress.models (RegionClusterState) |
| test_with_adding_node | 89-112 | 7 | 0e1d9613... | django.core.management (call_command), paas_wl.infras.resources.base.kres (KNode), paas_wl.workloads.networking.egress.models (RegionClusterState), tests.paas_wl.utils.basic (random_resource_name) |
| test_ignore_labels | 114-123 | 1 | 8b0aafdd... | django.core.management (call_command), paas_wl.workloads.networking.egress.models (RegionClusterState) |
| test_ignore_multi_labels | 125-136 | 1 | c5928887... | django.core.management (call_command), paas_wl.workloads.networking.egress.models (RegionClusterState), tests.paas_wl.utils.basic (random_resource_name) |
| test_ignore_masters | 138-152 | 1 | 70af5705... | django.core.management (call_command), paas_wl.workloads.networking.egress.models (RegionClusterState), tests.paas_wl.utils.basic (random_resource_name) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/domains/test_independent.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_invalid_input | 31-33 | 1 | 26558e87... | paas_wl.workloads.networking.ingress.domains.exceptions (ReplaceAppDomainFailed), paas_wl.workloads.networking.ingress.domains.independent (ReplaceAppDomainService), pytest (pytest) |
| test_integrated | 35-73 | 6 | 8bb57c3a... | django_dynamic_fixture (G), paas_wl.workloads.networking.ingress.domains.independent (ReplaceAppDomainService), paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (CustomDomainIngressMgr), paas_wl.workloads.networking.ingress.models (Domain), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/domains/test_manager.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_check_domain_used_by_market | 35-55 | 1 | d58e5a06... | paas_wl.workloads.networking.ingress.domains.manager (check_domain_used_by_market), paas_wl.workloads.networking.ingress.models (Domain), paasng.accessories.publish.market.models (MarketConfig), pytest (pytest) |
| test_create_no_deploys | 59-62 | 1 | 51691b24... | paas_wl.workloads.networking.ingress.domains.manager (CNativeCustomDomainManager), pytest (pytest), rest_framework.exceptions (ValidationError) |
| test_create_successfully | 64-72 | 2 | 246e98ed... | paas_wl.workloads.networking.ingress.domains.manager (CNativeCustomDomainManager), tests.paas_wl.bk_app.cnative.specs.utils (create_cnative_deploy), unittest (mock) |
| test_create_failed | 74-80 | 1 | af180126... | blue_krill.web.std_error (APIError), paas_wl.workloads.networking.ingress.domains.manager (CNativeCustomDomainManager), pytest (pytest), tests.paas_wl.bk_app.cnative.specs.utils (create_cnative_deploy), unittest (mock) |
| test_update | 92-99 | 3 | 8aa71689... | paas_wl.workloads.networking.ingress.domains.manager (CNativeCustomDomainManager), paas_wl.workloads.networking.ingress.models (Domain), unittest (mock) |
| test_delete | 101-106 | 3 | 185b2fb1... | paas_wl.workloads.networking.ingress.domains.manager (CNativeCustomDomainManager), paas_wl.workloads.networking.ingress.models (Domain), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/kres/test_ingress.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 68-86 | 3 | 381bac38... | paas_wl.workloads.networking.ingress.entities (PIngressDomain), paas_wl.workloads.networking.ingress.kres_entities.ingress (ProcessIngress, ingress_kmodel), pytest (pytest) |
| test_paths | 88-110 | 5 | d48d3c7f... | paas_wl.workloads.networking.ingress.entities (PIngressDomain), paas_wl.workloads.networking.ingress.kres_entities.ingress (ProcessIngress, ingress_kmodel), pytest (pytest) |
| test_serializer_ordering | 112-121 | 2 | 02646b3b... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.kres_slzs.ingress (IngressV1Beta1Serializer, IngressV1Serializer), pytest (pytest) |
| test_deserializer_ordering | 123-132 | 2 | 7ab91921... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.kres_slzs.ingress (IngressV1Beta1Deserializer, IngressV1Deserializer), pytest (pytest) |
| test_serialize | 323-326 | 1 | d5d1db7e... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ProcessIngress), paas_wl.workloads.networking.ingress.kres_slzs.ingress (IngressV1Beta1Serializer) |
| test_serialize_subpath | 328-331 | 1 | e2c8af83... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ProcessIngress), paas_wl.workloads.networking.ingress.kres_slzs.ingress (IngressV1Beta1Serializer) |
| test_deserialize | 341-344 | 1 | c48a2e57... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ProcessIngress), paas_wl.workloads.networking.ingress.kres_slzs.ingress (IngressV1Beta1Deserializer) |
| test_deserialize_subpath | 346-349 | 1 | 743d55a0... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ProcessIngress), paas_wl.workloads.networking.ingress.kres_slzs.ingress (IngressV1Beta1Deserializer) |
| test_serialize_subpath | 432-435 | 1 | 5e36a334... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ProcessIngress), paas_wl.workloads.networking.ingress.kres_slzs.ingress (IngressV1Serializer) |
| test_deserialize_subpath | 441-444 | 1 | b6048add... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ProcessIngress), paas_wl.workloads.networking.ingress.kres_slzs.ingress (IngressV1Deserializer) |
| test_deserialize | 588-606 | 1 | 06f41255... | kubernetes.dynamic.resource (ResourceInstance), paas_wl.infras.resources.kube_res.base (GVKConfig), paas_wl.workloads.networking.ingress.kres_entities.ingress (ProcessIngress), paas_wl.workloads.networking.ingress.kres_slzs.ingress (IngressV1Beta1Deserializer, IngressV1Deserializer), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/kres/test_service.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_integrated | 37-57 | 3 | 433f60cf... | paas_wl.workloads.networking.ingress.entities (PServicePortPair), paas_wl.workloads.networking.ingress.kres_entities.service (ProcessService, service_kmodel), pytest (pytest) |
| test_get_not_found | 59-61 | 1 | c50cf185... | paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.workloads.networking.ingress.kres_entities.service (service_kmodel), pytest (pytest) |
| test_get_normal | 63-74 | 1 | 7cd1e334... | paas_wl.workloads.networking.ingress.entities (PServicePortPair), paas_wl.workloads.networking.ingress.kres_entities.service (ProcessService, service_kmodel), pytest (pytest) |
| test_update_not_found | 76-84 | 1 | c15a3ba1... | paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.workloads.networking.ingress.entities (PServicePortPair), paas_wl.workloads.networking.ingress.kres_entities.service (ProcessService, service_kmodel), pytest (pytest) |
| test_update | 86-99 | 1 | e72edcd6... | paas_wl.workloads.networking.ingress.entities (PServicePortPair), paas_wl.workloads.networking.ingress.kres_entities.service (ProcessService, service_kmodel), pytest (pytest) |
| test_update_with_less_ports | 101-117 | 1 | 921b3812... | paas_wl.workloads.networking.ingress.entities (PServicePortPair), paas_wl.workloads.networking.ingress.kres_entities.service (ProcessService, service_kmodel), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/managers/test_domain.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_brand_new_domains | 53-69 | 2 | b2c9ba2b... | paas_wl.workloads.networking.ingress.entities (AutoGenDomain), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr, assign_custom_hosts), pytest (pytest) |
| test_create_https_domains | 71-86 | 2 | 7395ac6a... | paas_wl.workloads.networking.ingress.entities (AutoGenDomain), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr, assign_custom_hosts), paas_wl.workloads.networking.ingress.models (AppDomain), pytest (pytest) |
| test_domain_transfer_partially | 88-109 | 6 | 895cc8e4... | paas_wl.workloads.networking.ingress.entities (AutoGenDomain), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr, assign_custom_hosts) |
| test_domain_transfer_fully | 111-123 | 3 | 08accac3... | paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.workloads.networking.ingress.entities (AutoGenDomain), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr, assign_custom_hosts), pytest (pytest) |
| test_sync_no_domains | 136-140 | 1 | f1e2a0d1... | paas_wl.workloads.networking.ingress.exceptions (EmptyAppIngressError), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr), paas_wl.workloads.networking.ingress.models (AppDomain), pytest (pytest) |
| test_sync_creation_with_no_default_server_name | 142-145 | 1 | f354a766... | paas_wl.workloads.networking.ingress.exceptions (DefaultServiceNameRequired), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr), pytest (pytest) |
| test_sync_creation | 147-157 | 3 | bda54965... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr) |
| test_sync_update | 159-171 | 2 | de0c0373... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr) |
| test_delete_non_existed | 173-175 | 0 | 6ab456ed... | paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr) |
| test_integrated | 177-183 | 2 | 2825553b... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr) |
| test_update_target | 185-192 | 2 | ba066cad... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr) |
| test_rewrite_ingress_path_to_root | 194-204 | 1 | 8fb13d1c... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr), pytest (pytest), unittest.mock (patch) |
| test_list_desired_domains | 208-211 | 1 | 1b26c533... | paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr) |
| test_list_desired_domains_with_extra | 213-224 | 2 | 202592fe... | paas_wl.workloads.networking.ingress.constants (AppDomainSource), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr), paas_wl.workloads.networking.ingress.models (AppDomain) |
| test_list_desired_domains_with_wrong_source | 226-233 | 2 | 0c990ee4... | paas_wl.workloads.networking.ingress.constants (AppDomainSource), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr), paas_wl.workloads.networking.ingress.models (AppDomain) |
| test_create | 239-265 | 4 | 961210f6... | django_dynamic_fixture (G), paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (CustomDomainIngressMgr), paas_wl.workloads.networking.ingress.models (Domain), pytest (pytest) |
| test_normal_delete | 267-279 | 1 | 23424e60... | django_dynamic_fixture (G), paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (CustomDomainIngressMgr), paas_wl.workloads.networking.ingress.models (Domain), pytest (pytest) |
| test_get_ingress_class | 281-297 | 3 | b1cf08eb... | django.test.utils (override_settings), django_dynamic_fixture (G), paas_wl.workloads.networking.ingress.managers.domain (CustomDomainIngressMgr), paas_wl.workloads.networking.ingress.models (Domain) |
| test_assign_custom_hosts_affects_no_independent_domains | 304-315 | 2 | 32f1c389... | paas_wl.workloads.networking.ingress.constants (AppDomainSource), paas_wl.workloads.networking.ingress.entities (AutoGenDomain), paas_wl.workloads.networking.ingress.managers.domain (assign_custom_hosts), paas_wl.workloads.networking.ingress.models (AppDomain) |
| test_make_ingress_domain_with_http | 319-325 | 3 | ac4296a5... | paas_wl.workloads.networking.ingress.certs (DomainWithCert), paas_wl.workloads.networking.ingress.managers.domain (IngressDomainFactory) |
| test_https_cert_not_found | 327-331 | 1 | 0b53593b... | paas_wl.workloads.networking.ingress.certs (DomainWithCert), paas_wl.workloads.networking.ingress.exceptions (ValidCertNotFound), paas_wl.workloads.networking.ingress.managers.domain (IngressDomainFactory), pytest (pytest) |
| test_https_cert_not_found_no_exception | 333-337 | 1 | 006ca110... | paas_wl.workloads.networking.ingress.certs (DomainWithCert), paas_wl.workloads.networking.ingress.managers.domain (IngressDomainFactory) |
| test_https_cert_created | 339-352 | 3 | 78bd8954... | django_dynamic_fixture (G), paas_wl.workloads.networking.ingress.certs (DomainWithCert), paas_wl.workloads.networking.ingress.managers.domain (IngressDomainFactory), paas_wl.workloads.networking.ingress.models (AppDomainCert, AppDomainSharedCert), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/managers/test_https.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_domain_with_default_cert | 46-68 | 4 | c9304896... | paas_wl.workloads.networking.ingress.constants (AppDomainSource), paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr), paas_wl.workloads.networking.ingress.models (AppDomain) |
| test_domain_with_shared_cert | 70-84 | 2 | 54f09a45... | paas_wl.workloads.networking.ingress.constants (AppDomainSource), paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr), paas_wl.workloads.networking.ingress.models (AppDomain) |
| test_domain_with_not_matched_shared_cert | 86-98 | 1 | 95fbc35d... | paas_wl.workloads.networking.ingress.constants (AppDomainSource), paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr), paas_wl.workloads.networking.ingress.models (AppDomain) |
| test_domain_with_no_https | 100-113 | 2 | 9cfe6857... | paas_wl.workloads.networking.ingress.constants (AppDomainSource), paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (SubdomainAppIngressMgr), paas_wl.workloads.networking.ingress.models (AppDomain) |
| test_domain_with_shared_cert | 129-141 | 2 | 67c2eabb... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (CustomDomainIngressMgr), paas_wl.workloads.networking.ingress.models (Domain) |
| test_domain_with_not_matched_shared_cert | 143-154 | 1 | 174c1015... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (CustomDomainIngressMgr), paas_wl.workloads.networking.ingress.models (Domain) |
| test_domain_with_no_https | 156-168 | 2 | 6d4fa9b7... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.domain (CustomDomainIngressMgr), paas_wl.workloads.networking.ingress.models (Domain) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/managers/test_misc.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_desired_domains | 35-43 | 2 | 582854bb... | paas_wl.infras.cluster.utils (get_cluster_by_app), paas_wl.workloads.networking.ingress.managers.misc (LegacyAppIngressMgr) |
| test_set_header_x_script_name | 45-55 | 2 | 2dfa7739... | paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.misc (LegacyAppIngressMgr), pytest (pytest) |
| test_integrated | 61-83 | 7 | b0203ef2... | paas_wl.workloads.networking.ingress.constants (AppDomainSource), paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.misc (AppDefaultIngresses), paas_wl.workloads.networking.ingress.models (AppDomain) |
| test_set_header_x_script_name | 85-103 | 4 | 48333ce2... | paas_wl.workloads.networking.ingress.constants (AppDomainSource), paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.misc (AppDefaultIngresses, LegacyAppIngressMgr), paas_wl.workloads.networking.ingress.models (AppDomain) |
| test_restore_default_service | 105-126 | 3 | 9b12aff8... | cattr (cattr), paas_wl.bk_app.processes.models (ProcessSpecManager, ProcessTmpl), paas_wl.workloads.networking.ingress.kres_entities.ingress (ingress_kmodel), paas_wl.workloads.networking.ingress.managers.misc (AppDefaultIngresses), paas_wl.workloads.networking.ingress.utils (make_service_name), typing (List) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/managers/test_plugins.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_default_plugins | 49-66 | 2 | 4760b996... | paas_wl.workloads.networking.ingress.managers (AppIngressMgr), paas_wl.workloads.networking.ingress.plugins (override_plugins), pytest (pytest) |
| test_extra_plugins | 68-80 | 2 | e516b940... | paas_wl.workloads.networking.ingress.managers (AppIngressMgr), paas_wl.workloads.networking.ingress.plugins (override_plugins) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/managers/test_subpath.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_desired_domains_configured | 30-39 | 3 | f6f8bd31... | paas_wl.workloads.networking.ingress.managers.subpath (SubPathAppIngressMgr), paas_wl.workloads.networking.ingress.models (AppSubpath), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_list_desired_domains_not_configured | 41-45 | 1 | 5891f66a... | paas_wl.workloads.networking.ingress.managers.subpath (SubPathAppIngressMgr), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_brand_new_paths | 55-63 | 2 | 42e6b48c... | paas_wl.workloads.networking.ingress.managers.subpath (SubPathAppIngressMgr, assign_subpaths) |
| test_subpath_transfer_partally | 65-83 | 6 | 2fee3599... | paas_wl.workloads.networking.ingress.managers.subpath (SubPathAppIngressMgr, assign_subpaths) |
| test_subpath_transfer_fully | 85-99 | 5 | 47cc14c5... | paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.workloads.networking.ingress.managers.subpath (SubPathAppIngressMgr, assign_subpaths), pytest (pytest) |
| test_get_ingress_class | 101-104 | 1 | 3ab55b9c... | django.test.utils (override_settings), paas_wl.workloads.networking.ingress.managers.subpath (SubPathAppIngressMgr) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/test_addrs.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_not_deployed | 47-60 | 4 | 47ca7b4a... | paas_wl.workloads.networking.entrance.addrs (Address, AddressType), paas_wl.workloads.networking.entrance.shim (LiveEnvAddresses, PreAllocatedEnvAddresses) |
| test_integrated | 62-95 | 1 | 59027f2a... | paas_wl.infras.cluster.models (Domain, PortMap), paas_wl.workloads.networking.entrance.addrs (Address, AddressType), paas_wl.workloads.networking.entrance.shim (LiveEnvAddresses, get_legacy_url), paas_wl.workloads.networking.ingress.models (Domain), tests.paas_wl.utils.release (create_release) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_match_hostname | 26-37 | 1 | 82ea1133... | paas_wl.workloads.networking.ingress.models (AppDomainSharedCert), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/test_plugins.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_not_configured | 28-31 | 1 | 274b4d40... | paas_wl.workloads.networking.ingress.plugins.exceptions (PluginNotConfigured), paas_wl.workloads.networking.ingress.plugins.ingress (AccessControlPlugin), pytest (pytest) |
| test_acl_is_enabled_false | 33-36 | 1 | 8c911434... | paas_wl.bk_app.applications.managers (update_metadata), paas_wl.workloads.networking.ingress.plugins.ingress (AccessControlPlugin) |
| test_configured_with_region | 38-54 | 2 | 9b450f6c... | paas_wl.bk_app.applications.managers (update_metadata), paas_wl.workloads.networking.ingress.plugins.ingress (AccessControlPlugin) |
| test_configured_without_region | 56-63 | 2 | 7b7a8f6c... | paas_wl.bk_app.applications.managers (update_metadata), paas_wl.workloads.networking.ingress.plugins.ingress (AccessControlPlugin) |
| test_different_config | 72-86 | 2 | 9ce511f2... | paas_wl.workloads.networking.ingress.plugins.ingress (PaasAnalysisPlugin), pytest (pytest) |
| test_enabled_no_metadata | 88-92 | 1 | 3a5fc21b... | paas_wl.workloads.networking.ingress.plugins.ingress (PaasAnalysisPlugin) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/test_serializers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_path_prefix | 26-45 | 2 | 4f1e53ba... | paas_wl.workloads.networking.entrance.serializers (DomainEditableMixin), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/ingress/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_structure_with_web | 37-39 | 1 | 1fc54358... | paas_wl.workloads.networking.ingress.utils (guess_default_service_name) |
| test_structure_without_web | 41-43 | 1 | ad0c1cb3... | paas_wl.workloads.networking.ingress.utils (guess_default_service_name) |
| test_empty_structure | 45-46 | 1 | 090d79db... | paas_wl.workloads.networking.ingress.utils (guess_default_service_name) |
| test_normal | 50-66 | 2 | af928e36... | paas_wl.workloads.networking.ingress.entities (PIngressDomain), paas_wl.workloads.networking.ingress.kres_entities.ingress (ProcessIngress), paas_wl.workloads.networking.ingress.utils (get_main_process_service_name), unittest.mock (Mock, patch) |
| test_none | 68-74 | 3 | 4579b2e1... | paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paas_wl.workloads.networking.ingress.utils (get_main_process_service_name), pytest (pytest), unittest.mock (Mock, patch) |
| test_get_service_dns_name | 77-80 | 1 | 541f8baa... | paas_wl.workloads.networking.ingress.utils (get_service_dns_name) |
| test_parse_process_type | 83-85 | 1 | dc95c042... | paas_wl.workloads.networking.ingress.utils (make_service_name, parse_process_type) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/networking/test_api.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_sync_proc_ingresses | 27-29 | 0 | a8af4a74... | paas_wl.workloads.networking.sync (sync_proc_ingresses) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/release_controller/test_api.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_latest_build_id | 28-31 | 2 | 868b1d0a... | paas_wl.bk_app.applications.api (get_latest_build_id), paas_wl.bk_app.applications.models.build (Build) |

---


### 测试文件: apiserver/paasng/tests/paas_wl/workloads/release_controller/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_default | 27-28 | 1 | f909e93f... | paas_wl.bk_app.applications.models.build (BuildProcess) |
| test_set_true | 30-32 | 1 | 59d4c0fe... | paas_wl.bk_app.applications.models.build (BuildProcess) |
| test_finished_status | 34-38 | 1 | c079486e... | paas_wl.bk_app.applications.models.build (BuildProcess), paas_wl.utils.constants (BuildStatus) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/cloudapi/test_bk_apigateway_inner.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_prepare_headers | 26-68 | 1 | 5711e998... | json (json), paasng.accessories.cloudapi.components.bk_apigateway_inner (BkApigatewayInnerComponent), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/cloudapi/test_component.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_call_api | 25-63 | 2 | d8e3b72a... | blue_krill.web.std_error (APIError), paasng.accessories.cloudapi.components.component (BaseComponent), pytest (pytest) |
| test_urljoin | 65-89 | 1 | 660574a8... | paasng.accessories.cloudapi.components.component (BaseComponent), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/cloudapi/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_user_auth_type | 27-56 | 2 | 4b550093... | blue_krill.web.std_error (APIError), paasng.accessories.cloudapi (utils), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/cloudapi/test_views.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get | 32-66 | 1 | f5a50ee1... | paasng.accessories.cloudapi (views), paasng.platform.applications.models (Application), pytest (pytest), tests.utils.testing (get_response_json), unittest (mock) |
| test_post | 68-104 | 1 | 5b18c1e3... | paasng.accessories.cloudapi (views), paasng.misc.audit.constants (OperationEnum), paasng.platform.applications.models (Application), pytest (pytest), tests.utils.testing (get_response_json), unittest (mock) |
| test_get_bk_apigateway_inner_api_path | 106-146 | 2 | f0ed98c5... | blue_krill.web.std_error (APIError), paasng.accessories.cloudapi (views), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/dev_sandbox/test_config_var.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_generate_envs | 28-45 | 1 | c1a93373... | django.conf (settings), paasng.accessories.dev_sandbox.config_var (generate_envs), paasng.platform.engine.configurations.building (SlugbuilderInfo), paasng.platform.engine.constants (AppInfoBuiltinEnv) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/log/test_filter.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_count_filters_options_from_agg | 47-77 | 1 | aa4b6c8e... | paasng.accessories.log.filters (count_filters_options_from_agg), paasng.utils.es_log.models (FieldFilter), pytest (pytest) |
| test_count_filters_options_from_logs | 80-103 | 1 | e8c52793... | paasng.accessories.log.filters (count_filters_options_from_logs), paasng.utils.es_log.models (FieldFilter), pytest (pytest) |
| test_count_filters_options_from_logs_when_options_has_been_set | 106-113 | 1 | 8913aacc... | paasng.accessories.log.filters (count_filters_options_from_logs), paasng.utils.es_log.models (FieldFilter) |
| test_filter_by_builtin_filters | 145-177 | 1 | 514ee18c... | paasng.accessories.log.filters (ESFilter), paasng.accessories.log.models (ElasticSearchParams), pytest (pytest) |
| test_filter_by_builtin_excludes | 179-235 | 1 | d0997738... | paasng.accessories.log.filters (ESFilter), paasng.accessories.log.models (ElasticSearchParams), pytest (pytest) |
| test_filter_by_env | 247-303 | 1 | 1049d41f... | paasng.accessories.log.filters (EnvFilter), paasng.accessories.log.models (ElasticSearchParams), pytest (pytest) |
| test_filter_by_module | 323-367 | 1 | 4e75c65b... | paasng.accessories.log.filters (ModuleFilter), paasng.accessories.log.models (ElasticSearchParams), pytest (pytest) |
| test_render_failed | 369-372 | 1 | 90580ec5... | paasng.accessories.log.filters (ModuleFilter), paasng.accessories.log.models (ElasticSearchParams), pytest (pytest) |
| test_clean_property | 375-401 | 1 | 0f446761... | paasng.accessories.log.filters (_clean_property), paasng.utils.es_log.models (FieldFilter), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/log/test_responses.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_parse_raw_log | 81-114 | 1 | 8cb159d4... | cattr (cattr), paasng.accessories.log.responses (StructureLogLine), paasng.accessories.log.utils (clean_logs) |
| test_lacking_key_info | 116-130 | 1 | b3d68f85... | cattr (cattr), paasng.accessories.log.exceptions (LogLineInfoBrokenError), paasng.accessories.log.responses (StructureLogLine), paasng.accessories.log.utils (clean_logs), pytest (pytest) |
| test_parse_ingress_raw_log | 153-224 | 1 | d47e4cd5... | cattr (cattr), paasng.accessories.log.responses (IngressLogLine), paasng.accessories.log.utils (clean_logs), pytest (pytest) |
| test_ingress_lacking_key_info | 226-237 | 1 | f365e467... | cattr (cattr), paasng.accessories.log.exceptions (LogLineInfoBrokenError), paasng.accessories.log.responses (IngressLogLine), paasng.accessories.log.utils (clean_logs), pytest (pytest), typing (List) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/log/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_es_term | 43-119 | 1 | 742bba1a... | paasng.accessories.log.utils (get_es_term), pytest (pytest) |
| test_rename_log_fields | 133-172 | 1 | 87793e0d... | paasng.accessories.log.utils (NOT_SET, rename_log_fields), pytest (pytest) |
| test_parse_request_to_es_dsl | 175-230 | 1 | 46eb2834... | paasng.accessories.log.dsl (SearchRequestSchema), paasng.accessories.log.utils (parse_request_to_es_dsl), pytest (pytest) |
| test_legacy_ts_field | 235-245 | 1 | 280f7aa3... | paasng.utils.datetime (convert_timestamp_to_str), paasng.utils.es_log.misc (format_timestamp), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/paas_analysis/test_client.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_or_create_site_by_env | 36-42 | 2 | 992d6012... | paasng.accessories.paas_analysis.services (get_or_create_site_by_env), unittest (mock) |
| test_get_site_config | 44-59 | 3 | 1692c4dc... | paasng.accessories.paas_analysis.clients (SiteMetricsClient), paasng.accessories.paas_analysis.constants (MetricSourceType), pytest (pytest) |
| test_get_total_metric_about_site | 61-68 | 4 | fbd3659c... | datetime (datetime), paasng.accessories.paas_analysis.clients (SiteMetricsClient), paasng.accessories.paas_analysis.constants (MetricSourceType) |
| test_get_metrics_dimension | 70-92 | 5 | 759b1318... | datetime (datetime), paasng.accessories.paas_analysis.clients (SiteMetricsClient), paasng.accessories.paas_analysis.constants (MetricSourceType, MetricsDimensionType) |
| test_get_metrics_aggregate_by_interval_about_site | 94-108 | 5 | 10984dae... | datetime (datetime), paasng.accessories.paas_analysis.clients (SiteMetricsClient), paasng.accessories.paas_analysis.constants (MetricSourceType, MetricsInterval) |
| test_get_custom_event_overview | 114-134 | 4 | 845e3d2a... | datetime (datetime), paasng.accessories.paas_analysis.clients (SiteMetricsClient), paasng.accessories.paas_analysis.constants (MetricSourceType, MetricsInterval) |
| test_get_custom_event_trend_about_site | 160-174 | 5 | 94b61903... | datetime (datetime), paasng.accessories.paas_analysis.clients (SiteMetricsClient), paasng.accessories.paas_analysis.constants (MetricSourceType, MetricsInterval) |
| test_get_status | 178-185 | 1 | 0637bb9e... | paas_wl.bk_app.applications.managers (WlAppMetadata), paasng.accessories.paas_analysis.services (get_ingress_tracking_status), pytest (pytest), unittest (mock) |
| test_enable | 187-202 | 2 | 47102cde... | paas_wl.bk_app.applications.managers (WlAppMetadata), paasng.accessories.paas_analysis.services (enable_ingress_tracking), pytest (pytest), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/publish/entrance/test_domains.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_not_configured | 37-45 | 1 | 035081c1... | cattr (cattr), paas_wl.infras.cluster.models (IngressConfig), paasng.accessories.publish.entrance.domains (get_preallocated_domain) |
| test_enable_https | 47-68 | 2 | b2602448... | cattr (cattr), paas_wl.infras.cluster.models (IngressConfig), paasng.accessories.publish.entrance.domains (get_preallocated_domain), pytest (pytest) |
| test_without_module_name | 70-76 | 3 | c83ae19f... | cattr (cattr), paas_wl.infras.cluster.models (IngressConfig), paasng.accessories.publish.entrance.domains (get_preallocated_domain) |
| test_with_module_name | 78-86 | 3 | eded963c... | cattr (cattr), paas_wl.infras.cluster.models (IngressConfig), paasng.accessories.publish.entrance.domains (get_preallocated_domain) |
| test_prod_default | 105-111 | 1 | 107b4cd1... | paas_wl.workloads.networking.entrance.allocator.domains (ModuleEnvDomains) |
| test_stag_default | 113-118 | 1 | 3db35619... | paas_wl.workloads.networking.entrance.allocator.domains (ModuleEnvDomains) |
| test_stag_non_default | 120-127 | 1 | 7acd0819... | paas_wl.workloads.networking.entrance.allocator.domains (ModuleEnvDomains) |
| test_enable_https_by_default | 129-134 | 2 | 632e2ca7... | paas_wl.workloads.networking.entrance.allocator.domains (ModuleEnvDomains), pytest (pytest), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_prod_default | 144-151 | 1 | 77e0c6c9... | paas_wl.workloads.networking.entrance.allocator.domains (ModuleEnvDomains) |
| test_list_available_universal | 163-165 | 1 | ad411580... |  |
| test_list_available_default | 167-173 | 1 | 4a9ccc16... |  |
| test_get_highest_priority_universal | 175-179 | 3 | 5c853b8b... | paas_wl.workloads.networking.entrance.allocator.domains (DomainPriorityType) |
| test_get_highest_priority_default | 181-184 | 2 | 01a6f0e2... | paas_wl.workloads.networking.entrance.allocator.domains (DomainPriorityType) |
| test_get_highest_priority_default_prod | 186-189 | 2 | 2cfb5219... | paas_wl.workloads.networking.entrance.allocator.domains (DomainPriorityType) |
| test_default_prod_env | 206-214 | 1 | 956c31f5... | paasng.accessories.publish.entrance.domains (get_preallocated_domains_by_env) |
| test_non_default | 216-224 | 1 | c46b8e1f... | paasng.accessories.publish.entrance.domains (get_preallocated_domains_by_env) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/publish/entrance/test_exposer.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_env_is_deployed | 49-54 | 2 | a2a71752... | paasng.accessories.publish.entrance.exposer (env_is_deployed) |
| test_not_running | 58-60 | 1 | 6425a747... | paasng.accessories.publish.entrance.exposer (get_exposed_url) |
| test_preferred_root | 62-80 | 3 | 5861185f... | paasng.accessories.publish.entrance.exposer (get_exposed_url), paasng.platform.modules.constants (ExposedURLType), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/publish/entrance/test_preallocated.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_non_existent | 41-42 | 1 | f1721f4c... | paasng.accessories.publish.entrance.preallocated (get_exposed_url_type) |
| test_non_existent_module | 44-45 | 1 | 4715cb2e... | paasng.accessories.publish.entrance.preallocated (get_exposed_url_type) |
| test_normal | 47-58 | 3 | 2cde7c2c... | paasng.accessories.publish.entrance.preallocated (get_exposed_url_type), paasng.platform.modules.constants (ExposedURLType) |
| test_default_preallocated_urls_empty | 61-64 | 1 | 5077f53f... | paasng.accessories.publish.entrance.preallocated (_default_preallocated_urls), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_default_preallocated_urls_normal | 67-72 | 2 | ab6229d8... | json (json), paasng.accessories.publish.entrance.preallocated (_default_preallocated_urls), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_not_configured | 76-78 | 1 | e317ed48... | paasng.accessories.publish.entrance.preallocated (get_preallocated_address), pytest (pytest), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_normal | 80-93 | 1 | e2bda4b0... | paasng.accessories.publish.entrance.preallocated (get_preallocated_address), pytest (pytest), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_preferred_url_type | 95-107 | 1 | bb95d1df... | paasng.accessories.publish.entrance.preallocated (get_preallocated_address), paasng.platform.modules.constants (ExposedURLType), pytest (pytest), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_with_clusters | 109-192 | 2 | 7c6b3680... | paas_wl.infras.cluster.models (Cluster, Domain, IngressConfig), paasng.accessories.publish.entrance.preallocated (get_preallocated_address), paasng.platform.engine.constants (AppEnvName), pytest (pytest) |
| test_single_entrance | 208-216 | 2 | d3b40722... | paasng.accessories.publish.entrance.preallocated (get_preallocated_url), paasng.platform.modules.constants (ExposedURLType) |
| test_sub_domain | 218-228 | 1 | 68dced52... | paasng.accessories.publish.entrance.preallocated (get_preallocated_urls), paasng.platform.modules.constants (ExposedURLType) |
| test_get_preallocated_urls_legacy | 230-241 | 1 | 9c2b8e4b... | paasng.accessories.publish.entrance.preallocated (get_preallocated_urls), tests.utils.helpers (override_region_configs) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/publish/entrance/test_subpaths.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_prod_default | 56-72 | 3 | 9e9d995c... | paas_wl.workloads.networking.entrance.allocator.subpaths (ModuleEnvSubpaths), paasng.accessories.publish.entrance.subpaths (get_legacy_compatible_path) |
| test_stag_default | 74-85 | 1 | ed55d535... | paas_wl.workloads.networking.entrance.allocator.subpaths (ModuleEnvSubpaths), paasng.accessories.publish.entrance.subpaths (get_legacy_compatible_path) |
| test_stag_non_default | 87-99 | 1 | 86b44aaa... | paas_wl.workloads.networking.entrance.allocator.subpaths (ModuleEnvSubpaths), paasng.accessories.publish.entrance.subpaths (get_legacy_compatible_path) |
| test_disable_legacy_pattern | 101-109 | 1 | 92bc4efe... | django.test.utils (override_settings), paas_wl.workloads.networking.entrance.allocator.subpaths (ModuleEnvSubpaths) |
| test_prod_default | 118-121 | 1 | 930477e7... | paas_wl.workloads.networking.entrance.allocator.subpaths (ModuleEnvSubpaths) |
| test_no_module_name | 125-134 | 3 | 6dec14cf... | cattr (cattr), paas_wl.infras.cluster.models (IngressConfig), paasng.accessories.publish.entrance.subpaths (get_preallocated_path) |
| test_with_module_name | 136-146 | 3 | 59be9862... | cattr (cattr), paas_wl.infras.cluster.models (IngressConfig), paasng.accessories.publish.entrance.subpaths (get_preallocated_path) |
| test_https | 148-163 | 3 | 52cd6baf... | cattr (cattr), paas_wl.infras.cluster.models (IngressConfig), paasng.accessories.publish.entrance.subpaths (get_preallocated_path) |
| test_get_legacy_compatible_path | 166-168 | 1 | 3c67e227... | paasng.accessories.publish.entrance.subpaths (get_legacy_compatible_path) |
| test_list_available_universal | 180-182 | 1 | 6a819999... |  |
| test_list_available_default | 184-190 | 1 | d4e6ca91... |  |
| test_get_highest_priority_universal | 192-196 | 3 | 7c800201... | paas_wl.workloads.networking.entrance.allocator.subpaths (SubpathPriorityType) |
| test_get_highest_priority_default | 198-201 | 2 | deb46535... | paas_wl.workloads.networking.entrance.allocator.subpaths (SubpathPriorityType) |
| test_get_highest_priority_default_prod | 203-206 | 2 | bacd3d43... | paas_wl.workloads.networking.entrance.allocator.subpaths (SubpathPriorityType) |
| test_default_prod_env | 223-231 | 1 | 8a82fdc8... | paasng.accessories.publish.entrance.subpaths (get_preallocated_paths_by_env) |
| test_non_default | 233-241 | 1 | bf841926... | paasng.accessories.publish.entrance.subpaths (get_preallocated_paths_by_env) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/publish/entrance/test_triggers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_sync_default_entrances_for_module_switching | 29-34 | 2 | e75d5612... | paas_wl.workloads.networking.entrance.handlers (sync_default_entrances_for_module_switching), unittest (mock) |
| test_sync_default_entrances_for_cnative_module_switching | 37-44 | 1 | e49a4abc... | paas_wl.bk_app.cnative.specs.crd.bk_app (BkAppResource), paas_wl.bk_app.cnative.specs.handlers (sync_default_entrances_for_cnative_module_switching), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/publish/entrance/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_legacy_url | 24-27 | 2 | 0acb9277... | paas_wl.workloads.networking.entrance.utils (get_legacy_url) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/publish/market/test_publish.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_default_product | 31-33 | 1 | 417c8018... | paasng.accessories.publish.market.models (Product) |
| test_fresh_app | 55-62 | 3 | 3e683d6d... | paasng.accessories.publish.market.protections (AppPublishPreparer) |
| test_app_with_product | 64-72 | 3 | e81584b1... | django_dynamic_fixture (G), paasng.accessories.publish.market.models (Product), paasng.accessories.publish.market.protections (AppPublishPreparer) |
| test_app_with_product_prod_env | 74-83 | 1 | 0a6c9f24... | django_dynamic_fixture (G), paasng.accessories.publish.market.models (Product), paasng.accessories.publish.market.protections (AppPublishPreparer), paasng.platform.engine.constants (JobStatus), pytest (pytest), tests.paasng.platform.engine.setup_utils (create_fake_deployment) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/publish/market/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_filter_domain_address_not_found | 53-68 | 1 | a3236539... | paasng.accessories.publish.market.models (AvailableAddress, MarketConfig), paasng.accessories.publish.market.utils (MarketAvailableAddressHelper), paasng.platform.modules.constants (ExposedURLType), pytest (pytest) |
| test_access_entrance | 70-96 | 7 | b64153e5... | paas_wl.workloads.networking.entrance.addrs (Address), paas_wl.workloads.networking.entrance.constants (AddressType), paasng.accessories.publish.market.constant (ProductSourceUrlType), paasng.accessories.publish.market.models (MarketConfig), paasng.accessories.publish.market.utils (MarketAvailableAddressHelper) |
| test_access_entrance_for_custom_domain | 98-108 | 2 | 2a89711a... | paasng.accessories.publish.market.constant (ProductSourceUrlType), paasng.accessories.publish.market.models (MarketConfig), paasng.accessories.publish.market.utils (MarketAvailableAddressHelper) |
| test_different_access_entrance_url_type | 110-129 | 3 | 679c2f1b... | paasng.accessories.publish.market.constant (ProductSourceUrlType), paasng.accessories.publish.market.models (MarketConfig), paasng.accessories.publish.market.utils (MarketAvailableAddressHelper), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/publish/sync_market/test_app_tag.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_sync_tag | 29-31 | 1 | ed012ce8... | paasng.accessories.publish.market.models (Tag) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/publish/sync_market/test_sync_console.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_init_members | 71-80 | 2 | ec356c98... | paasng.accessories.publish.sync_market.managers (AppDeveloperManger, AppOpsManger), paasng.core.core.storages.sqlalchemy (console_db) |
| test_delete_members | 82-101 | 2 | 07694864... | paasng.accessories.publish.sync_market.handlers (sync_console_app_developers, sync_console_app_devopses), paasng.accessories.publish.sync_market.managers (AppDeveloperManger, AppOpsManger), paasng.core.core.storages.sqlalchemy (console_db), paasng.infras.iam.helpers (delete_role_members), paasng.platform.applications.constants (ApplicationRole) |
| test_add_members | 103-121 | 2 | e47726be... | paasng.accessories.publish.sync_market.handlers (sync_console_app_developers, sync_console_app_devopses), paasng.accessories.publish.sync_market.managers (AppDeveloperManger, AppOpsManger), paasng.core.core.storages.sqlalchemy (console_db), paasng.infras.iam.helpers (add_role_members), paasng.platform.applications.constants (ApplicationRole) |
| test_validate_app_code | 130-135 | 0 | bcc0e171... | paasng.accessories.publish.sync_market.handlers (validate_app_code_uniquely) |
| test_validate_app_name | 137-140 | 1 | f4ae4b7c... | paasng.accessories.publish.sync_market.handlers (validate_app_name_uniquely), paasng.platform.applications.exceptions (AppFieldValidationError), pytest (pytest), tests.utils.helpers (create_app) |
| test_change_app_name | 142-155 | 3 | bc24e9a3... | paasng.accessories.publish.sync_market.handlers (on_change_application_name), paasng.accessories.publish.sync_market.managers (AppManger), paasng.core.core.storages.sqlalchemy (console_db), paasng.platform.applications.exceptions (AppFieldValidationError, IntegrityError), pytest (pytest), tests.utils.helpers (create_app, generate_random_string) |
| test_register_app | 157-160 | 1 | 73cf4c62... | paasng.accessories.publish.sync_market.handlers (register_app_core_data), paasng.platform.applications.exceptions (IntegrityError), pytest (pytest) |
| test_app_state | 162-168 | 3 | 39eb67ff... | paasng.accessories.publish.sync_market.handlers (register_application_with_default), paasng.platform.mgrlegacy.constants (LegacyAppState) |
| test_create_release_record | 171-173 | 0 | 297016ca... | paasng.accessories.publish.sync_market.managers (AppReleaseRecordManger), paasng.core.core.storages.sqlalchemy (console_db) |
| test_sync_app_deploy_records | 177-179 | 0 | 07a37ef3... | django_dynamic_fixture (G), paasng.accessories.publish.sync_market.handlers (sync_release_record), paasng.platform.engine.constants (JobStatus), paasng.platform.engine.models.deployment (Deployment) |
| test_create_default_product | 183-194 | 4 | 50b80ead... | paasng.accessories.publish.market.models (Product), paasng.accessories.publish.sync_market.handlers (on_product_deploy_success), paasng.accessories.publish.sync_market.managers (AppManger), paasng.core.core.storages.sqlalchemy (console_db) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/publish/test_entrance.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 68-76 | 3 | 47eb5d8d... | paasng.accessories.publish.entrance.exposer (get_exposed_url, get_module_exposed_links) |
| test_get_module_exposed_links | 79-93 | 1 | 1b83ae85... | paas_wl.workloads.networking.entrance.addrs (Address, AddressType), paasng.accessories.publish.entrance.exposer (get_module_exposed_links), paasng.platform.modules.constants (ExposedURLType) |
| test_normal | 102-109 | 2 | e1c28240... | paasng.accessories.publish.entrance.exposer (update_exposed_url_type_to_subdomain), paasng.platform.modules.constants (ExposedURLType), unittest (mock) |
| test_with_legacy_market | 111-157 | 4 | 3404e475... | contextlib (contextmanager), django.conf (settings), paasng.accessories.publish.entrance.exposer (update_exposed_url_type_to_subdomain), paasng.accessories.publish.market.constant (AppType), paasng.accessories.publish.market.models (Product), paasng.accessories.publish.market.utils (MarketAvailableAddressHelper), paasng.accessories.publish.sync_market.handlers (register_application_with_default), paasng.accessories.publish.sync_market.managers (AppManger), paasng.core.core.storages.sqlalchemy (console_db), paasng.platform.modules.constants (ExposedURLType), pytest (pytest), translated_fields (to_attribute), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/servicehub/remote/test_api.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_retrieve_service | 25-34 | 2 | d932c80e... | unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/servicehub/remote/test_client.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_services_error | 36-40 | 1 | 477fcb99... | paasng.accessories.servicehub.remote.exceptions (RemoteClientError), pytest (pytest), requests (RequestException), unittest (mock) |
| test_list_services_status_code_error | 42-46 | 1 | 15e89bb1... | paasng.accessories.servicehub.remote.exceptions (RClientResponseError), pytest (pytest), tests.utils.api (mock_json_response), unittest (mock) |
| test_list_services_normal | 48-56 | 4 | def0ee2e... | blue_krill.auth.jwt (ClientJWTAuth), tests.paasng.accessories.servicehub (data_mocks), tests.utils.api (mock_json_response), unittest (mock) |
| test_retrieve_instance_normal | 58-67 | 4 | 80829351... | blue_krill.auth.jwt (ClientJWTAuth), tests.paasng.accessories.servicehub (data_mocks), tests.utils.api (mock_json_response), unittest (mock) |
| test_provision_instance_normal | 69-80 | 4 | ed5757bf... | blue_krill.auth.jwt (ClientJWTAuth), tests.paasng.accessories.servicehub (data_mocks), tests.utils.api (mock_json_response), unittest (mock) |
| test_retrieve_instance_has_created_field | 82-90 | 1 | 2cc97910... | arrow (arrow), tests.paasng.accessories.servicehub (data_mocks), tests.utils.api (mock_json_response), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/servicehub/remote/test_collector.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_improperly_configured | 32-35 | 1 | 658ff3e3... | django.core.exceptions (ImproperlyConfigured), django.test (override_settings), paasng.accessories.servicehub.remote.collector (initialize_remote_services), pytest (pytest) |
| test_normal | 37-48 | 3 | d31eb6df... | django.test (override_settings), paasng.accessories.servicehub.remote.collector (initialize_remote_services), tests.paasng.accessories.servicehub (data_mocks), tests.utils.api (mock_json_response), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/servicehub/remote/test_manager.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_from_data | 48-62 | 5 | 5fffec08... | paasng.accessories.servicehub.remote.manager (RemotePlanObj) |
| test_get_plan | 73-108 | 5 | 9e91b4d2... | django_dynamic_fixture (G), paasng.accessories.servicehub.models (RemoteServiceEngineAppAttachment), paasng.accessories.servicehub.remote.manager (RemoteEngineAppInstanceRel), pytest (pytest), unittest (mock), uuid (uuid) |
| test_provision | 110-147 | 8 | 0452928e... | paasng.accessories.servicehub.remote (RemoteServiceMgr), pytest (pytest), unittest (mock), utils (gen_plan) |
| test_render_params | 149-172 | 5 | c5aea78f... | paasng.accessories.servicehub.remote (RemoteServiceMgr), unittest (mock), utils (gen_plan) |
| test_find_by_name | 205-222 | 2 | 2da138a2... | paasng.accessories.servicehub.exceptions (ServiceObjNotFound), paasng.accessories.servicehub.remote (RemoteServiceMgr), pytest (pytest) |
| test_bind_with_specs | 224-248 | 5 | 6b7785dd... | paasng.accessories.servicehub.exceptions (BindServiceNoPlansError), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.remote (RemoteServiceMgr), pytest (pytest) |
| test_module_rebind_failed_after_provision | 250-266 | 3 | fe99507c... | paasng.accessories.servicehub.exceptions (CanNotModifyPlan), paasng.accessories.servicehub.remote (RemoteServiceMgr), pytest (pytest), unittest (mock) |
| test_bind_service | 277-287 | 0 | 50d04b50... | paasng.accessories.servicehub.remote (RemoteServiceMgr), pytest (pytest), utils (gen_plan) |
| test_bind_service_errors | 289-302 | 1 | 282d21ac... | paasng.accessories.servicehub.exceptions (BindServiceNoPlansError), paasng.accessories.servicehub.remote (RemoteServiceMgr), pytest (pytest), utils (gen_plan) |
| test_bind_service_mixed_plans | 304-332 | 2 | a6df2aa2... | dataclasses (asdict), paasng.accessories.servicehub.remote (RemoteServiceMgr), pytest (pytest), unittest (mock), utils (gen_plan) |
| test_bound_with_diff_app_zone | 334-396 | 5 | 6009ae6c... | dataclasses (asdict), django.test.utils (override_settings), paas_wl.infras.cluster.models (Cluster), paasng.accessories.servicehub.exceptions (BindServiceNoPlansError), paasng.accessories.servicehub.remote (RemoteServiceMgr), pytest (pytest), unittest (mock), utils (gen_plan) |
| test_list_binded | 417-428 | 5 | 008593b1... | paasng.accessories.servicehub.remote (RemoteServiceMgr) |
| test_get_instance_has_create_time_attr | 430-451 | 1 | 312d9a8d... | datetime (datetime), paasng.accessories.servicehub.remote (RemoteServiceMgr), tests.paasng.accessories.servicehub (data_mocks), unittest (mock) |
| test_get_instance | 453-478 | 4 | ac06af24... | paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.remote (RemoteServiceMgr), tests.paasng.accessories.servicehub (data_mocks), unittest (mock) |
| test_get_env_vars_with_exclude_disabled | 480-516 | 3 | 8c011193... | paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.remote (RemoteServiceMgr), tests.paasng.accessories.servicehub (data_mocks), unittest (mock) |
| test_get_attachment_by_instance_id | 534-554 | 1 | a13ceb14... | paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.models (RemoteServiceEngineAppAttachment), paasng.accessories.servicehub.remote (RemoteServiceMgr), typing (Dict), unittest (mock), uuid (uuid) |
| test_bind_service | 573-577 | 1 | 8d9efeef... | paasng.accessories.servicehub.remote (RemoteServiceMgr) |
| test_bind_service_wrong_region | 579-587 | 1 | 3e441732... | paasng.accessories.servicehub.exceptions (BindServiceNoPlansError), paasng.accessories.servicehub.remote (RemoteServiceMgr), paasng.platform.modules.models (Module), pytest (pytest) |
| test_list_binded | 589-599 | 5 | 3663f2a4... | paasng.accessories.servicehub.remote (RemoteServiceMgr) |
| test_module_rebind | 601-611 | 3 | b6aeea11... | paasng.accessories.servicehub.remote (RemoteServiceMgr) |
| test_module_rebind_failed_after_provision | 613-626 | 3 | 9fb678df... | paasng.accessories.servicehub.exceptions (CanNotModifyPlan), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.remote (RemoteServiceMgr), pytest (pytest), unittest (mock) |
| test_semantic_version_gte_none_version | 630-631 | 1 | e52617bf... | paasng.accessories.servicehub.remote.manager (MetaInfo) |
| test_semantic_version_gte_normal | 633-648 | 1 | 6c3eb70c... | paasng.accessories.servicehub.remote.manager (MetaInfo), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/servicehub/remote/test_store.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_non_exists | 46-48 | 1 | 4e99cc40... | paasng.accessories.servicehub.remote.exceptions (ServiceNotFound), pytest (pytest) |
| test_get_normal | 50-53 | 1 | 4ca425eb... | tests.paasng.accessories.servicehub (data_mocks) |
| test_list_all | 55-57 | 2 | 675f4abb... |  |
| test_list_by_category | 59-60 | 1 | 2ef830b8... | paasng.accessories.servicehub.constants (Category) |
| test_get_source_config | 62-64 | 1 | 1d424018... | tests.paasng.accessories.servicehub (data_mocks) |
| test_get_by_unsupported_region | 66-69 | 1 | 3a8a5516... | pytest (pytest), tests.paasng.accessories.servicehub (data_mocks) |
| test_bulk_get | 71-80 | 3 | 40f85dd3... | tests.paasng.accessories.servicehub (data_mocks) |
| test_bulk_get_unregistered_service | 82-88 | 3 | b71d14a2... | tests.paasng.accessories.servicehub (data_mocks) |
| test_bulk_get_by_unsupported_region | 90-93 | 1 | 9d7b7110... | pytest (pytest), tests.paasng.accessories.servicehub (data_mocks) |
| test_all | 95-98 | 1 | 70869b3b... | tests.paasng.accessories.servicehub (data_mocks) |
| test_empty | 100-111 | 3 | 7b2eef2d... | paasng.accessories.servicehub.remote.exceptions (ServiceConfigNotFound, ServiceNotFound), pytest (pytest), tests.paasng.accessories.servicehub (data_mocks) |
| test_bulk_update_conflict | 113-124 | 1 | d7872c7b... | copy (deepcopy), paasng.accessories.servicehub.remote (collector), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/servicehub/test_manager.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_by_category | 42-52 | 2 | 258d4703... | django_dynamic_fixture (G), paasng.accessories.servicehub.constants (Category), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.services.models (Service, ServiceCategory) |
| test_list_by_region | 54-64 | 2 | 3c18dbfc... | django_dynamic_fixture (G), paasng.accessories.servicehub.constants (Category), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.services.models (Service, ServiceCategory) |
| test_get_remote_found | 66-68 | 1 | 7397c624... | paasng.accessories.servicehub.manager (mixed_service_mgr), tests.paasng.accessories.servicehub (data_mocks) |
| test_get_local_found | 70-76 | 1 | 036aaa18... | django_dynamic_fixture (G), paasng.accessories.servicehub.constants (Category), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.services.models (Service, ServiceCategory) |
| test_get_not_found | 78-80 | 1 | a4346ed0... | paasng.accessories.servicehub.exceptions (ServiceObjNotFound), paasng.accessories.servicehub.manager (mixed_service_mgr), pytest (pytest) |
| test_find_by_name_local_found | 82-90 | 3 | aff01d2f... | django_dynamic_fixture (G), paasng.accessories.servicehub.constants (Category), paasng.accessories.servicehub.local (LocalServiceObj), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.remote (RemoteServiceObj), paasng.accessories.services.models (Service, ServiceCategory) |
| test_find_by_name_remote_found | 92-96 | 3 | c609d01d... | paasng.accessories.servicehub.local (LocalServiceObj), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.remote (RemoteServiceObj), tests.paasng.accessories.servicehub (data_mocks) |
| test_find_by_name_not_found | 98-100 | 1 | 6e0a0440... | paasng.accessories.servicehub.exceptions (ServiceObjNotFound), paasng.accessories.servicehub.manager (mixed_service_mgr), pytest (pytest) |
| test_get_env_vars_ordering | 102-118 | 1 | 54f77c62... | datetime (datetime), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.services (ServiceInstanceObj), unittest (mock) |
| test_bind_service | 155-159 | 1 | 66d9aea8... | paasng.accessories.servicehub.local (LocalServiceMgr) |
| test_list_binded | 161-172 | 5 | a563551c... | paasng.accessories.servicehub.local (LocalServiceMgr) |
| test_provision | 174-186 | 2 | 61c3cece... | paasng.accessories.servicehub.local (LocalServiceMgr), unittest (mock) |
| test_instance_has_create_time_attr | 188-198 | 1 | c75ce75d... | datetime (datetime), paasng.accessories.servicehub.local (LocalServiceMgr), unittest (mock) |
| test_get_instance | 200-220 | 6 | 20e88735... | paasng.accessories.servicehub.local (LocalServiceMgr), unittest (mock) |
| test_find_by_name_not_found | 222-225 | 1 | 15e515dc... | paasng.accessories.servicehub.exceptions (ServiceObjNotFound), paasng.accessories.servicehub.local (LocalServiceMgr), pytest (pytest) |
| test_find_by_name_normal | 227-230 | 1 | 00952368... | paasng.accessories.servicehub.local (LocalServiceMgr) |
| test_module_is_bound_with | 232-238 | 2 | 7c8873a0... | paasng.accessories.servicehub.local (LocalServiceMgr) |
| test_get_attachment_by_instance_id | 240-256 | 1 | a539c7d0... | paasng.accessories.servicehub.local (LocalServiceMgr), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.models (ServiceEngineAppAttachment), typing (Dict), uuid (UUID) |
| test_bind_service | 270-275 | 1 | 77654c54... | paasng.accessories.servicehub.exceptions (BindServiceNoPlansError), paasng.accessories.servicehub.local (LocalServiceMgr), pytest (pytest) |
| test_list_by_category | 277-287 | 1 | 4eb82ecc... | paasng.accessories.servicehub.constants (Category), paasng.accessories.servicehub.local (LocalServiceMgr) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/servicehub/test_services.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_init | 31-37 | 2 | 745fee31... | paasng.accessories.servicehub.services (ServiceSpecificationHelper), unittest (mock) |
| test_create | 39-85 | 5 | 1062805f... | paasng.accessories.servicehub.services (ServiceSpecificationHelper), pytest (pytest), unittest (mock), utils (generate_ssd) |
| test_create_from_duplicated_specifications | 87-104 | 2 | 7cac8460... | paasng.accessories.servicehub.services (ServiceSpecificationHelper), pytest (pytest), unittest (mock), utils (generate_ssd) |
| test_filter_plans | 106-129 | 1 | 76b5ac35... | paasng.accessories.servicehub.services (PlanObj, ServiceSpecificationHelper), pytest (pytest), typing (Dict), unittest (mock), utils (generate_ssd) |
| test_get_grouped_spec_values | 131-172 | 1 | dff49131... | paasng.accessories.servicehub.services (ServiceSpecificationHelper), pytest (pytest), unittest (mock), utils (gen_plan, generate_ssd) |
| test_get_recommended_spec | 174-211 | 1 | 83162633... | paasng.accessories.servicehub.services (ServiceSpecificationHelper), pytest (pytest), unittest (mock), utils (generate_ssd) |
| test_list_plans_spec_value | 213-254 | 1 | 2922e7a0... | paasng.accessories.servicehub.services (ServiceSpecificationHelper), pytest (pytest), unittest (mock), utils (gen_plan, generate_ssd) |
| test_validate_specs | 256-288 | 1 | 9e59e4aa... | paasng.accessories.servicehub.services (ServiceSpecificationHelper), pytest (pytest), unittest (mock), utils (generate_ssd) |
| test_parse_spec_values_tree | 290-302 | 1 | c436d832... | paasng.accessories.servicehub.services (ServiceSpecificationHelper), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/servicehub/test_sharing.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_shareable | 113-119 | 2 | 5a754a12... | paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.sharing (ServiceSharingManager) |
| test_create | 121-126 | 1 | 7e4ff0e5... | paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.sharing (ServiceSharingManager) |
| test_create_already_bound | 128-135 | 1 | e96df5a8... | paasng.accessories.servicehub.exceptions (DuplicatedServiceBoundError), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.sharing (ServiceSharingManager), pytest (pytest) |
| test_bind_already_shared | 137-144 | 1 | ace2ade1... | paasng.accessories.servicehub.exceptions (DuplicatedServiceBoundError), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.sharing (ServiceSharingManager), pytest (pytest) |
| test_create_with_other_app | 146-152 | 1 | cedb9550... | paasng.accessories.servicehub.exceptions (ReferencedAttachmentNotFound), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.sharing (ServiceSharingManager), pytest (pytest), tests.utils.helpers (create_app) |
| test_get_shared_info | 154-157 | 1 | 8c834e19... | paasng.accessories.servicehub.manager (SharedServiceInfo), paasng.accessories.servicehub.sharing (ServiceSharingManager) |
| test_list_shared_info | 159-169 | 5 | a68e0fd9... | paasng.accessories.servicehub.sharing (ServiceSharingManager) |
| test_list_related_modules | 173-175 | 1 | ed6c8210... | paasng.accessories.servicehub.sharing (SharingReferencesManager) |
| test_clear_related | 177-183 | 2 | 8b804c59... | paasng.accessories.servicehub.sharing (ServiceSharingManager, SharingReferencesManager) |
| test_local_integrated | 188-222 | 3 | fb62867f... | django_dynamic_fixture (G), json (json), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.models (ServiceInstance), paasng.accessories.servicehub.sharing (ServiceSharingManager), paasng.accessories.services.models (Plan, Service), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/services/test_import.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_import_single | 42-58 | 4 | 0dd9a916... | json (json), paasng.accessories.services.models (PreCreatedInstance), paasng.accessories.services.serializers (PreCreatedInstanceImportSLZ), pytest (pytest) |
| test_import_multi | 60-79 | 2 | 5e8379c4... | paasng.accessories.services.models (PreCreatedInstance), paasng.accessories.services.serializers (PreCreatedInstanceImportSLZ), pytest (pytest) |
| test_import_from_yaml | 81-129 | 2 | 477ff52d... | paasng.accessories.services.models (PreCreatedInstance), paasng.accessories.services.serializers (PreCreatedInstanceImportSLZ), pytest (pytest), textwrap (dedent), yaml (yaml) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/services/test_provider.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_provision | 41-47 | 4 | 7b922a24... | json (json), paasng.accessories.services.models (PreCreatedInstance) |
| test_provision_with_str_config | 49-62 | 4 | b13abc98... | django_dynamic_fixture (G), json (json), paasng.accessories.services.models (PreCreatedInstance) |
| test_delete | 64-73 | 5 | ebb142e7... | json (json), paasng.accessories.services.models (PreCreatedInstance) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/services/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_vendor_config | 32-39 | 1 | ae4021ba... | dataclasses (dataclass), paasng.accessories.services.utils (get_vendor_config) |
| test_get_vendor_config_not_configured | 42-45 | 2 | 6aedb88b... | django.core.exceptions (ImproperlyConfigured), paasng.accessories.services.utils (get_vendor_config), pytest (pytest) |
| test_normal | 49-51 | 1 | 120cede9... | paasng.accessories.services.utils (WRItemList) |
| test_no_weight | 53-55 | 1 | 2c6765fa... | paasng.accessories.services.utils (WRItemList), pytest (pytest) |
| test_weight_zero | 57-63 | 1 | 154dfd40... | paasng.accessories.services.utils (WRItemList) |
| test_multi_weighted | 65-80 | 2 | c65e014a... | paasng.accessories.services.utils (WRItemList) |
| test_normal | 97-99 | 1 | ffefbff2... | paasng.accessories.services.utils (Base36Handler, gen_unique_id) |
| test_max_length | 101-112 | 4 | bf6a65ba... | paasng.accessories.services.utils (Base36Handler, gen_unique_id) |
| test_divide_char | 114-116 | 1 | 634dbd7f... | paasng.accessories.services.utils (Base36Handler, gen_unique_id) |
| test_divide_char_max_length | 118-123 | 1 | 12ddbc10... | paasng.accessories.services.utils (Base36Handler, gen_unique_id) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/smart_advisor/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 33-35 | 1 | ec815a65... | paasng.accessories.smart_advisor (AppPLTag, AppSDKTag, force_tag), paasng.accessories.smart_advisor.models (get_tags, tag_module) |
| test_cleanup | 37-40 | 1 | 74e0141c... | paasng.accessories.smart_advisor (force_tag), paasng.accessories.smart_advisor.models (cleanup_module, get_tags, tag_module) |
| test_normal | 44-59 | 2 | 9e776014... | paasng.accessories.smart_advisor (AppPLTag), paasng.accessories.smart_advisor.tags (DeploymentFailureTag, get_dynamic_tag), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/smart_advisor/test_smart_advisor.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_search | 62-91 | 1 | c0bd1b66... | paasng.accessories.smart_advisor (AppPLTag, AppSDKTag, PlatPanelTag), paasng.accessories.smart_advisor.advisor (DocumentaryLinkAdvisor), pytest (pytest) |
| test_render_links | 95-102 | 1 | c6f00311... | paasng.accessories.smart_advisor.utils (DeploymentFailureHint) |
| test_not_found_docs | 106-112 | 1 | 28c1dae0... | paasng.accessories.smart_advisor.utils (get_failure_hint), tests.paasng.platform.engine.setup_utils (create_fake_deployment), unittest (mock) |
| test_found_docs | 114-123 | 2 | c4569c57... | dataclasses (asdict), django_dynamic_fixture (G), paasng.accessories.smart_advisor.models (DocumentaryLink), paasng.accessories.smart_advisor.utils (get_failure_hint), tests.paasng.platform.engine.setup_utils (create_fake_deployment), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/accessories/smart_advisor/test_tagging.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_tagging_python_using_different_encodings | 39-60 | 1 | 330988e3... | paasng.accessories.smart_advisor.tagging (dig_tags_local_repo), paasng.accessories.smart_advisor.tags (force_tag), pathlib (Path), pytest (pytest), tempfile (tempfile), textwrap (dedent) |
| test_tagging_php | 62-69 | 1 | 1915c3c1... | paasng.accessories.smart_advisor.tagging (dig_tags_local_repo), paasng.accessories.smart_advisor.tags (force_tag), pathlib (Path), tempfile (tempfile) |
| test_tagging_go | 71-78 | 1 | 9e696bff... | paasng.accessories.smart_advisor.tagging (dig_tags_local_repo), paasng.accessories.smart_advisor.tags (force_tag), pathlib (Path), tempfile (tempfile) |
| test_tagging_nodejs | 80-89 | 1 | f1bd0436... | paasng.accessories.smart_advisor.tagging (dig_tags_local_repo), paasng.accessories.smart_advisor.tags (force_tag), pathlib (Path), tempfile (tempfile) |
| test_normal | 102-117 | 1 | 00f7f58b... | paasng.accessories.smart_advisor.tagging (get_deployment_tags), paasng.accessories.smart_advisor.tags (DeploymentFailureTag), pytest (pytest), tests.paasng.platform.engine.setup_utils (create_fake_deployment), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/bk_plugins/test_apigw.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_sync_succeeded | 60-67 | 3 | 15cefb42... | paasng.bk_plugins.bk_plugins.apigw (PluginDefaultAPIGateway) |
| test_sync_failed | 69-72 | 1 | 62e31e72... | paasng.bk_plugins.bk_plugins.apigw (PluginDefaultAPIGateway), paasng.bk_plugins.bk_plugins.exceptions (PluginApiGatewayServiceError), pytest (pytest) |
| test_sync_reuse_apigw_name | 74-82 | 1 | 2feaa941... | paasng.bk_plugins.bk_plugins.apigw (PluginDefaultAPIGateway) |
| test_grant_succeeded | 84-88 | 1 | bbc6c02c... | django_dynamic_fixture (G), paasng.bk_plugins.bk_plugins.apigw (PluginDefaultAPIGateway), paasng.bk_plugins.bk_plugins.models (BkPluginDistributor) |
| test_revoke_succeeded | 90-94 | 1 | eea8b60a... | django_dynamic_fixture (G), paasng.bk_plugins.bk_plugins.apigw (PluginDefaultAPIGateway), paasng.bk_plugins.bk_plugins.models (BkPluginDistributor) |
| test_update_status_succeeded | 96-99 | 1 | f9c6ba99... | paasng.bk_plugins.bk_plugins.apigw (PluginDefaultAPIGateway) |
| test_safe_sync_apigw_succeeded | 102-108 | 1 | d9bda3b6... | paasng.bk_plugins.bk_plugins.apigw (safe_sync_apigw), unittest.mock (patch) |
| test_safe_sync_apigw_failed | 111-117 | 1 | 8ad0552f... | paasng.bk_plugins.bk_plugins.apigw (safe_sync_apigw), unittest.mock (patch) |
| test_integrated | 121-152 | 6 | bdc150a6... | django_dynamic_fixture (G), paasng.bk_plugins.bk_plugins.apigw (safe_sync_apigw, set_distributors), paasng.bk_plugins.bk_plugins.models (BkPluginDistributor), pytest (pytest), unittest.mock (patch) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/bk_plugins/test_handlers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_on_pre_deployment | 28-32 | 1 | f8857628... | paasng.bk_plugins.bk_plugins.handlers (on_pre_deployment), tests.paasng.platform.engine.setup_utils (create_fake_deployment), unittest.mock (patch) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/bk_plugins/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_from_application | 42-44 | 1 | 20f2267a... | paasng.bk_plugins.bk_plugins.models (BkPlugin) |
| test_get_deployed_statuses | 47-50 | 1 | 8d0a4de1... | paasng.bk_plugins.bk_plugins.models (BkPlugin, get_deployed_statuses), pytest (pytest) |
| test_make_bk_plugin_normal | 53-55 | 1 | c77f7def... | paasng.bk_plugins.bk_plugins.models (make_bk_plugin) |
| test_make_bk_plugin_wrong_type | 58-61 | 1 | 0e7a39e9... | paasng.bk_plugins.bk_plugins.models (make_bk_plugin), paasng.platform.applications.constants (ApplicationType), pytest (pytest) |
| test_get_or_create_by_application | 64-71 | 3 | 14977c13... | django_dynamic_fixture (G), paasng.bk_plugins.bk_plugins.models (BkPluginProfile, BkPluginTag) |
| test_plugin_to_detailed_default | 74-77 | 1 | 9a5cb36a... | paasng.bk_plugins.bk_plugins.models (plugin_to_detailed), pytest (pytest) |
| test_plugin_to_detailed_no_addresses | 80-83 | 1 | b81c3c44... | paasng.bk_plugins.bk_plugins.models (plugin_to_detailed), pytest (pytest) |
| test_get_plugin_env_variables | 86-92 | 1 | e09929e6... | paasng.bk_plugins.bk_plugins.models (get_plugin_env_variables) |
| test_distributor_code_name | 96-104 | 3 | b706d0a9... | django_dynamic_fixture (G), functools (partial), paasng.bk_plugins.bk_plugins.apigw (set_distributors), paasng.bk_plugins.bk_plugins.models (BkPluginAppQuerySet, BkPluginDistributor) |
| test_tag_id | 106-120 | 3 | 4c5fce60... | django_dynamic_fixture (G), functools (partial), paasng.bk_plugins.bk_plugins.constants (PluginTagIdType), paasng.bk_plugins.bk_plugins.models (BkPluginAppQuerySet, BkPluginTag) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/iam_adaptor/management/test_providers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_attr | 64-65 | 1 | 3d5d9400... | paasng.bk_plugins.pluginscenter.iam_adaptor.management.providers (PluginProvider) |
| test_list_attr_value | 67-68 | 1 | 6c8118d1... | iam.resource.utils (FancyDict, Page), paasng.bk_plugins.pluginscenter.iam_adaptor.management.providers (PluginProvider) |
| test_list_instance_by_policy | 70-74 | 1 | ac87d6e0... | iam.resource.utils (FancyDict, Page), paasng.bk_plugins.pluginscenter.iam_adaptor.management.providers (PluginProvider) |
| test_list_instance | 76-108 | 4 | 42accd9b... | django.utils.translation (override), iam.resource.utils (FancyDict, Page), paasng.bk_plugins.pluginscenter.iam_adaptor.definitions (gen_iam_resource_id), paasng.bk_plugins.pluginscenter.iam_adaptor.management.providers (PluginProvider) |
| test_fetch_instance_info | 110-147 | 2 | d1b77e86... | django.utils.translation (override), django_dynamic_fixture (G), iam.resource.utils (FancyDict), paasng.bk_plugins.pluginscenter.iam_adaptor.definitions (gen_iam_resource_id), paasng.bk_plugins.pluginscenter.iam_adaptor.management.providers (PluginProvider), paasng.bk_plugins.pluginscenter.iam_adaptor.models (PluginGradeManager) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/iam_adaptor/management/test_shim.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_fetch_grade_manager_members | 31-34 | 2 | 5b56b44e... | django_dynamic_fixture (G), paasng.bk_plugins.pluginscenter.iam_adaptor.management (shim), paasng.bk_plugins.pluginscenter.iam_adaptor.models (PluginGradeManager) |
| test_fetch_role_members | 37-50 | 6 | c07df403... | django_dynamic_fixture (G), paasng.bk_plugins.pluginscenter.constants (PluginRole), paasng.bk_plugins.pluginscenter.iam_adaptor.management (shim), paasng.bk_plugins.pluginscenter.iam_adaptor.models (PluginUserGroup), pytest (pytest) |
| test_add_role_members | 53-71 | 7 | ff82bd09... | django_dynamic_fixture (G), paasng.bk_plugins.pluginscenter.constants (PluginRole), paasng.bk_plugins.pluginscenter.iam_adaptor.management (shim), paasng.bk_plugins.pluginscenter.iam_adaptor.models (PluginGradeManager, PluginUserGroup), pytest (pytest) |
| test_delete_role_members | 74-92 | 7 | 6908e7e9... | django_dynamic_fixture (G), paasng.bk_plugins.pluginscenter.constants (PluginRole), paasng.bk_plugins.pluginscenter.iam_adaptor.management (shim), paasng.bk_plugins.pluginscenter.iam_adaptor.models (PluginGradeManager, PluginUserGroup), pytest (pytest) |
| test_fetch_user_roles | 95-107 | 5 | 30378e7f... | django_dynamic_fixture (G), paasng.bk_plugins.pluginscenter.constants (PluginRole), paasng.bk_plugins.pluginscenter.iam_adaptor.management (shim), paasng.bk_plugins.pluginscenter.iam_adaptor.models (PluginUserGroup) |
| test_remove_user_all_roles | 110-116 | 2 | c6f75929... | django_dynamic_fixture (G), paasng.bk_plugins.pluginscenter.constants (PluginRole), paasng.bk_plugins.pluginscenter.iam_adaptor.management (shim), paasng.bk_plugins.pluginscenter.iam_adaptor.models (PluginGradeManager, PluginUserGroup) |
| test_fetch_plugin_members | 119-147 | 2 | fcb94023... | cattr (cattr), django_dynamic_fixture (G), paasng.bk_plugins.pluginscenter.constants (PluginRole), paasng.bk_plugins.pluginscenter.iam_adaptor.management (shim), paasng.bk_plugins.pluginscenter.iam_adaptor.models (PluginUserGroup), typing (List) |
| test_setup_builtin_grade_manager | 150-157 | 2 | c2e28eb0... | django_dynamic_fixture (G), paasng.bk_plugins.pluginscenter.iam_adaptor.management (shim), paasng.bk_plugins.pluginscenter.iam_adaptor.models (PluginGradeManager) |
| test_setup_builtin_user_groups | 160-167 | 4 | 723206dc... | django_dynamic_fixture (G), paasng.bk_plugins.pluginscenter.constants (PluginRole), paasng.bk_plugins.pluginscenter.iam_adaptor.management (shim), paasng.bk_plugins.pluginscenter.iam_adaptor.models (PluginGradeManager, PluginUserGroup) |
| test_delete_builtin_user_groups | 170-177 | 3 | 6b7d48c6... | django_dynamic_fixture (G), paasng.bk_plugins.pluginscenter.constants (PluginRole), paasng.bk_plugins.pluginscenter.iam_adaptor.management (shim), paasng.bk_plugins.pluginscenter.iam_adaptor.models (PluginUserGroup) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/iam_adaptor/policy/test_converter.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_convert | 25-37 | 1 | e44146d7... | django.db.models (Q), paasng.bk_plugins.pluginscenter.iam_adaptor.policy.converter (PluginPolicyConverter), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/iam_adaptor/policy/test_permissions.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_single_action | 50-63 | 3 | 2dfeac54... | paasng.bk_plugins.pluginscenter.iam_adaptor.constants (PluginPermissionActions), pytest (pytest) |
| test_multi_actions | 65-94 | 1 | cd8f5d59... | paasng.bk_plugins.pluginscenter.iam_adaptor.constants (PluginPermissionActions), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/iam_adaptor/test_definitions.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_gen_iam_resource_name | 31-32 | 1 | fb3ebb19... | paasng.bk_plugins.pluginscenter.iam_adaptor.definitions (gen_iam_resource_name) |
| test_gen_iam_resource | 35-39 | 3 | a00bcc01... | paasng.bk_plugins.pluginscenter.iam_adaptor.definitions (gen_iam_resource, gen_iam_resource_name) |
| test_gen_iam_grade_manager | 42-48 | 2 | ef25f48f... | paasng.bk_plugins.pluginscenter.iam_adaptor.definitions (gen_iam_grade_manager, gen_iam_resource_name) |
| test_gen_plugin_user_group | 51-71 | 4 | 1eed0840... | paasng.bk_plugins.pluginscenter.iam_adaptor.constants (PluginRole), paasng.bk_plugins.pluginscenter.iam_adaptor.definitions (gen_plugin_user_group), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/iam_adaptor/test_migrator.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_invalid_template | 47-59 | 1 | f9933b63... | paasng.bk_plugins.pluginscenter.iam_adaptor.migrator (IAMPermissionTemplateRender), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/log/test_api.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_query_standard_output_logs | 58-78 | 3 | 60081ef2... | cattr (cattr), json (json), paasng.bk_plugins.pluginscenter.log (query_standard_output_logs) |
| test_query_structure_logs | 81-101 | 3 | b4296c58... | cattr (cattr), json (json), paasng.bk_plugins.pluginscenter.log (query_structure_logs) |
| test_query_ingress_logs | 104-189 | 1 | 91504d72... | cattr (cattr), paasng.bk_plugins.pluginscenter.log (query_ingress_logs) |
| test_aggregate_date_histogram | 192-207 | 2 | 9a021da1... | elasticsearch_dsl.aggs (DateHistogram), elasticsearch_dsl.response.aggs (FieldBucketData), elasticsearch_dsl.search (Search), paasng.bk_plugins.pluginscenter.log (aggregate_date_histogram) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/log/test_es_client.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_clean_property | 24-50 | 1 | bf049cd7... | paasng.bk_plugins.pluginscenter.log.client (ESLogClient), paasng.utils.es_log.models (FieldFilter), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/log/test_filter.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_filter_by_plugin | 42-78 | 1 | 9761addb... | paasng.bk_plugins.pluginscenter.definitions (ElasticSearchParams), paasng.bk_plugins.pluginscenter.log.filters (ElasticSearchFilter), pytest (pytest) |
| test_filter_by_builtin_filters | 80-112 | 1 | b3237caa... | paasng.bk_plugins.pluginscenter.definitions (ElasticSearchParams), paasng.bk_plugins.pluginscenter.log.filters (ElasticSearchFilter), pytest (pytest) |
| test_filter_by_builtin_excludes | 114-170 | 1 | ad9718c9... | paasng.bk_plugins.pluginscenter.definitions (ElasticSearchParams), paasng.bk_plugins.pluginscenter.log.filters (ElasticSearchFilter), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/release/test_executor.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_enter_next_stage | 115-135 | 8 | 05113edb... | blue_krill.web.std_error (APIError), django.utils.translation (gettext_lazy), paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.exceptions (error_codes), paasng.bk_plugins.pluginscenter.releases.executor (PluginReleaseExecutor), pytest (pytest) |
| test_rerun_current_stage | 137-152 | 7 | 4361a52b... | blue_krill.web.std_error (APIError), paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.exceptions (error_codes), paasng.bk_plugins.pluginscenter.releases.executor (PluginReleaseExecutor), pytest (pytest) |
| test_execute_current_stage | 154-177 | 10 | f08ef619... | blue_krill.web.std_error (APIError), django.utils.translation (gettext_lazy), paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.exceptions (error_codes), paasng.bk_plugins.pluginscenter.releases.executor (PluginReleaseExecutor), pytest (pytest) |
| test_rollback_current_stage_failed | 179-205 | 9 | e04ce5e1... | blue_krill.web.std_error (APIError), django.utils.translation (gettext_lazy), paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus, ReleaseStageInvokeMethod), paasng.bk_plugins.pluginscenter.exceptions (error_codes), paasng.bk_plugins.pluginscenter.releases.executor (PluginReleaseExecutor), pytest (pytest) |
| test_rollback_current_stage | 207-223 | 6 | 88e07081... | paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.releases.executor (PluginReleaseExecutor) |
| test_reset | 225-247 | 9 | bbfe9b4d... | blue_krill.web.std_error (APIError), django.utils.translation (gettext_lazy), paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.exceptions (error_codes), paasng.bk_plugins.pluginscenter.releases.executor (PluginReleaseExecutor), pytest (pytest) |
| test_cancel | 249-264 | 5 | 203ea4a4... | blue_krill.web.std_error (APIError), django.utils.translation (gettext_lazy), paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.exceptions (error_codes), paasng.bk_plugins.pluginscenter.releases.executor (PluginReleaseExecutor), pytest (pytest) |
| test_pre_command | 266-282 | 5 | 9c2db2f2... | blue_krill.web.std_error (APIError), paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.exceptions (error_codes), paasng.bk_plugins.pluginscenter.releases.executor (PluginReleaseExecutor), pytest (pytest) |
| test_post_command | 284-300 | 3 | 43af5bfd... | paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.releases.executor (PluginReleaseExecutor), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/release/test_stages.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_build_pipeline_params | 37-72 | 3 | 660ec44d... | paasng.bk_plugins.pluginscenter.constants (ReleaseStageInvokeMethod), paasng.bk_plugins.pluginscenter.definitions (find_stage_by_id), paasng.bk_plugins.pluginscenter.releases.stages (PipelineStage), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/release/test_steps.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_stage_types | 60-61 | 1 | 17058669... | paasng.bk_plugins.pluginscenter.releases (stages) |
| test_render_base_info | 64-70 | 4 | aafd4611... | paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.releases (stages) |
| test_execute | 87-114 | 2 | 034089b6... | paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus) |
| test_render_to_view | 116-153 | 3 | 6c3a1276... | paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/test_api.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_readonly_api | 60-66 | 2 | b3026265... | pytest (pytest) |
| test_update_api | 68-74 | 2 | 67f3f9ef... | paasng.bk_plugins.pluginscenter.exceptions (error_codes), pytest (pytest) |
| test_update_status | 78-108 | 2 | 786f3254... | paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), pytest (pytest) |
| test_update_publisher | 110-115 | 1 | f9e74f6f... | pytest (pytest) |
| test_update_visible_range | 117-156 | 2 | 00ccbdc4... | paasng.bk_plugins.pluginscenter.models.instances (ItsmDetail, PluginVisibleRange), pytest (pytest), unittest (mock) |
| test_upadate_release_strategy | 158-209 | 1 | d0c4cba0... | paasng.bk_plugins.pluginscenter.models.instances (ItsmDetail), pytest (pytest), unittest (mock) |
| test_rollback_release | 211-240 | 2 | 28e7de52... | paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), pytest (pytest) |
| test_itsm_online_callback | 244-270 | 3 | cb439b06... | paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.itsm_adaptor.constants (ItsmTicketStatus), pytest (pytest) |
| test_itsm_create_callback | 272-291 | 3 | e3af034a... | paasng.bk_plugins.pluginscenter.constants (PluginStatus), paasng.bk_plugins.pluginscenter.itsm_adaptor.constants (ItsmTicketStatus), pytest (pytest) |
| test_itsm_visible_range_callback | 293-348 | 7 | a92bb41a... | paasng.bk_plugins.pluginscenter.itsm_adaptor.constants (ItsmTicketStatus), paasng.bk_plugins.pluginscenter.models.instances (ItsmDetail, PluginVisibleRange), pytest (pytest) |
| test_itsm_canry_release_callback | 350-382 | 3 | 6415999c... | paasng.bk_plugins.pluginscenter.itsm_adaptor.constants (ItsmTicketStatus), paasng.bk_plugins.pluginscenter.models.instances (PluginRelease), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/test_configuration.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create | 34-39 | 4 | 870c365f... | hashlib (sha256), paasng.bk_plugins.pluginscenter.models (PluginConfig) |
| test_update | 41-47 | 2 | 5f13dbfc... | django_dynamic_fixture (G), hashlib (sha256), paasng.bk_plugins.pluginscenter.models (PluginConfig) |
| test_create_new_one | 49-56 | 3 | 3abf55f3... | django_dynamic_fixture (G), hashlib (sha256), paasng.bk_plugins.pluginscenter.models (PluginConfig) |
| test_delete | 58-62 | 2 | 089e24c8... | paasng.bk_plugins.pluginscenter.models (PluginConfig) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/test_integration.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_canry_release_version | 73-130 | 4 | ddbf16c7... | paasng.bk_plugins.pluginscenter.constants (PluginRevisionType), pytest (pytest), unittest (mock) |
| test_create_release_version | 132-180 | 3 | 9a82bf0e... | paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.models (PluginRelease), pytest (pytest), unittest (mock) |
| test_release_version | 182-312 | 15 | 009f9037... | django.utils.translation (gettext_lazy), paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.exceptions (error_codes), paasng.bk_plugins.pluginscenter.models (PluginRelease), pytest (pytest), unittest (mock) |
| test_record | 318-334 | 2 | 217dea0a... | paasng.bk_plugins.pluginscenter.constants (ActionTypes, SubjectTypes), paasng.bk_plugins.pluginscenter.models (OperationRecord) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/test_itsm.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_execute_itsm_stage | 42-54 | 3 | e3babc72... | paasng.bk_plugins.pluginscenter.constants (PluginReleaseStatus), paasng.bk_plugins.pluginscenter.itsm_adaptor.utils (submit_online_approval_ticket), pytest (pytest), requests (requests) |
| test_itsm_render | 57-84 | 3 | ce0bf49d... | json (json), paasng.bk_plugins.pluginscenter.itsm_adaptor.utils (get_ticket_status), pytest (pytest), requests (requests) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/test_serializers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_make_create_plugin_validator | 46-123 | 3 | 654d15c8... | cattr (cattr), django.utils.translation (gettext), paasng.bk_plugins.pluginscenter (serializers), paasng.bk_plugins.pluginscenter.definitions (PluginCodeTemplate), pytest (pytest), rest_framework.exceptions (ErrorDetail) |
| test_make_create_plugin_validator_conflict | 126-155 | 2 | aa8eb824... | paasng.bk_plugins.pluginscenter (serializers), pytest (pytest), rest_framework.exceptions (ErrorDetail) |
| test_validate_automatic_semver | 161-179 | 1 | 4915be62... | paasng.bk_plugins.pluginscenter (serializers), pytest (pytest) |
| test_validate_revision_eq_source_revision | 182-195 | 1 | b820163d... | paasng.bk_plugins.pluginscenter (serializers), pytest (pytest) |
| test_validate_revision_eq_commit_hash | 198-220 | 1 | 75c3b690... | paasng.bk_plugins.pluginscenter (serializers), pytest (pytest) |
| test_validate_tested_version | 223-242 | 1 | 428b177b... | paasng.bk_plugins.pluginscenter (serializers), paasng.bk_plugins.pluginscenter.constants (PluginRevisionType), pytest (pytest), unittest (mock) |
| test_validate_release_policy | 245-269 | 1 | c6a202d9... | blue_krill.web.std_error (APIError), paasng.bk_plugins.pluginscenter (serializers), pytest (pytest) |
| test_market_info_validator | 272-295 | 1 | 4d18428a... | paasng.bk_plugins.pluginscenter (serializers), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/test_shim.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_repo_failed | 62-67 | 2 | 0d688ee1... | paasng.bk_plugins.pluginscenter.shim (init_plugin_in_view), pytest (pytest) |
| test_initial_repo_failed | 69-76 | 3 | 0d80a19b... | paasng.bk_plugins.pluginscenter.shim (init_plugin_in_view), pytest (pytest) |
| test_thirdparty_exception | 78-85 | 3 | fbbdf742... | blue_krill.web.std_error (APIError), paasng.bk_plugins.pluginscenter.shim (init_plugin_in_view), pytest (pytest), unittest (mock) |
| test_iam_exception | 87-95 | 3 | a0d8c063... | paasng.bk_plugins.pluginscenter.shim (init_plugin_in_view), pytest (pytest), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/thirdparty/test_api.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_transform_exception | 39-71 | 4 | 6bda0f26... | bkapi_client_core.exceptions (ResponseError), blue_krill.web.std_error (APIError), paasng.bk_plugins.pluginscenter.thirdparty (market), pytest (pytest), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/thirdparty/test_instance.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_instance_upsert_api | 27-57 | 5 | 75ca2851... | paasng.bk_plugins.pluginscenter.thirdparty (instance), pytest (pytest) |
| test_instance_delete_api | 60-69 | 3 | 3de1dffb... | paasng.bk_plugins.pluginscenter.constants (PluginStatus), paasng.bk_plugins.pluginscenter.thirdparty (instance), requests (requests) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/thirdparty/test_market.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_market_upsert_api | 44-65 | 3 | 3f30ab2c... | paasng.bk_plugins.pluginscenter.thirdparty (market), pytest (pytest) |
| test_market_read_api | 68-83 | 5 | 54d3a767... | django.conf (settings), paasng.bk_plugins.pluginscenter.serializers (PluginMarketInfoSLZ), paasng.bk_plugins.pluginscenter.thirdparty (market), translated_fields (to_attribute) |

---


### 测试文件: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/thirdparty/test_release.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_release_upsert_api | 42-61 | 4 | 7953695f... | paasng.bk_plugins.pluginscenter.thirdparty (release), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/core/core/test_storages.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_make_sa_conn_string | 23-36 | 1 | ba2e5fbb... | paasng.core.core.storages.utils (make_sa_conn_string), pytest (pytest) |
| test_make_uni_key | 40-44 | 1 | 39d4b012... | paasng.core.core.storages.utils (SADBManager), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/infras/accounts/test_internal.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 35-43 | 2 | 76ab0b28... | blue_krill.auth.client (Client), paasng.infras.accounts.internal.user (SysUserFromVerifiedClientMiddleware) |

---


### 测试文件: apiserver/paasng/tests/paasng/infras/accounts/test_middlewares.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_no_token_provided | 38-43 | 1 | 86d509d3... | paasng.infras.accounts.middlewares (PrivateTokenAuthenticationMiddleware) |
| test_random_invalid_token | 45-50 | 1 | b469a234... | paasng.infras.accounts.middlewares (PrivateTokenAuthenticationMiddleware) |
| test_valid_token_provided | 52-62 | 2 | 4d3f0a00... | paasng.infras.accounts.middlewares (PrivateTokenAuthenticationMiddleware), paasng.infras.accounts.models (User, UserPrivateToken) |
| test_valid_token_provided_by_header | 64-74 | 2 | 0190b2aa... | paasng.infras.accounts.middlewares (PrivateTokenAuthenticationMiddleware), paasng.infras.accounts.models (User, UserPrivateToken) |
| test_verified_app_provided | 94-125 | 3 | f63f9c95... | paasng.infras.accounts.middlewares (AuthenticatedAppAsUserMiddleware), paasng.infras.accounts.models (AuthenticatedAppAsUser, User), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/infras/accounts/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_match_different_scope | 25-48 | 12 | 0dbf29c0... | paasng.infras.accounts.oauth.constants (ScopeType), paasng.infras.accounts.oauth.models (Scope) |
| test_error_match | 50-55 | 2 | bf88e9f0... | paasng.infras.accounts.oauth.models (Scope), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/infras/accounts/test_permissions.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_user_can_create_in_region | 26-33 | 2 | d9c7ea86... | paasng.infras.accounts.models (UserProfile), paasng.infras.accounts.permissions.user (user_can_create_in_region), tests.utils.helpers (configure_regions) |

---


### 测试文件: apiserver/paasng/tests/paasng/infras/bk_log/test_client.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_custom_collector_config | 39-188 | 5 | 155a1c78... | paasng.infras.bk_log.constatns (ETLType, FieldType), paasng.infras.bk_log.definitions (CustomCollectorConfig, ETLConfig, ETLField, ETLParams, StorageConfig), pytest (pytest) |
| test_databus_custom_update | 191-331 | 3 | 9050e388... | paasng.infras.bk_log.constatns (ETLType, FieldType), paasng.infras.bk_log.definitions (CustomCollectorConfig, ETLConfig, ETLField, ETLParams, StorageConfig), pytest (pytest) |
| test_databus_custom_update_failed | 333-335 | 1 | 1525663a... | paasng.infras.bk_log.definitions (CustomCollectorConfig), paasng.infras.bk_log.exceptions (CollectorConfigNotPersisted), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/infras/iam/permissions/test_application.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_can_view_basic_info | 39-48 | 3 | 4515e2bb... | paasng.infras.iam.permissions.resources.application (AppPermCtx), roles (roles) |
| test_can_delete_application | 50-71 | 5 | 4d2ad9ff... | paasng.infras.iam.constants (ResourceType), paasng.infras.iam.permissions.exceptions (PermissionDeniedError), paasng.infras.iam.permissions.perm (ActionResourcesRequest), paasng.infras.iam.permissions.resources.application (AppAction, AppPermCtx), pytest (pytest), roles (roles), tests.paasng.infras.iam.conftest (generate_apply_url) |
| test_can_manage_cloud_api | 73-82 | 3 | f88b9093... | paasng.infras.iam.permissions.resources.application (AppPermCtx), roles (roles) |
| test_can_manage_app_market | 84-93 | 3 | 393e63c3... | paasng.infras.iam.permissions.resources.application (AppPermCtx), roles (roles) |
| test_to_data | 97-105 | 1 | e8457ddb... | django.conf (settings), paasng.infras.iam.constants (ResourceType), paasng.infras.iam.permissions.resources.application (AppCreatorAction) |

---


### 测试文件: apiserver/paasng/tests/paasng/infras/oauth2/test_oauth_client.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_client | 33-48 | 2 | 2640a303... | blue_krill.contextlib (nullcontext), django.test.utils (override_settings), paasng.infras.oauth2.exceptions (BkOauthApiException), paasng.infras.oauth2.models (OAuth2Client), paasng.infras.oauth2.utils (create_oauth2_client, get_oauth2_client_secret), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/audit/test_api.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_latest_apps | 27-48 | 4 | c4574218... | paasng.misc.audit.service (add_app_audit_record) |
| test_latest_apps_filter_by_operator | 50-77 | 5 | 5c15ef77... | paasng.misc.audit.service (add_app_audit_record), tests.conftest (create_app, generate_random_string), tests.utils.auth (create_user) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/audit/test_model.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_opreation_record_display | 28-101 | 1 | c3ae9525... | paasng.misc.audit.constants (OperationEnum, OperationTarget, ResultCode), paasng.misc.audit.service (add_app_audit_record), pytest (pytest) |
| test_post_save_handler | 105-115 | 2 | 061b583d... | paasng.misc.audit.constants (OperationEnum, OperationTarget), paasng.misc.audit.models (AppLatestOperationRecord), paasng.misc.audit.service (add_app_audit_record) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/monitoring/alert_rules/test_api.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_rules | 37-46 | 2 | 1d9d751b... |  |
| test_list_supported_alert_rules | 48-51 | 1 | 11d4a385... | paasng.misc.monitoring.monitor.alert_rules.config.constants (DEFAULT_RULE_CONFIGS) |
| test_init_alert_rules | 55-57 | 1 | de9dd441... |  |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/monitoring/alert_rules/test_manager.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_init_rules | 31-50 | 3 | 4e6deac3... | django.test.utils (override_settings), importlib (importlib), paasng.misc.monitoring.monitor.alert_rules (manager), paasng.misc.monitoring.monitor.models (AppAlertRule) |
| test_create_rules | 52-66 | 3 | 8e6f1b61... | django.test.utils (override_settings), importlib (importlib), paasng.misc.monitoring.monitor.alert_rules (manager), paasng.misc.monitoring.monitor.alert_rules.config.constants (DEFAULT_RULE_CONFIGS), paasng.misc.monitoring.monitor.models (AppAlertRule) |
| test_update_notice_group | 68-74 | 0 | a86f2a6a... | django.test.utils (override_settings), importlib (importlib), paasng.misc.monitoring.monitor.alert_rules (manager) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/monitoring/metrics/test_client.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_from_dict | 65-71 | 4 | d9e4171d... | paasng.misc.monitoring.metrics.clients.prometheus (PromResult) |
| test_none | 73-92 | 3 | 67fa55e8... | paasng.misc.monitoring.metrics.clients.prometheus (PromResult), pytest (pytest) |
| test_get_by_container_name | 94-119 | 9 | 74fc32cc... | paasng.misc.monitoring.metrics.clients.prometheus (PromResult) |
| test_response_change | 121-153 | 2 | fa59128b... | paasng.misc.monitoring.metrics.clients.prometheus (PromResult) |
| test_from_series | 185-191 | 4 | e5894543... | paasng.misc.monitoring.metrics.clients (BkPromResult) |
| test_none | 193-196 | 1 | 292571c8... | paasng.misc.monitoring.metrics.clients (BkPromResult), pytest (pytest) |
| test_get_by_container_name | 198-224 | 9 | 428dc686... | paasng.misc.monitoring.metrics.clients (BkPromResult) |
| test_no_container_name | 226-246 | 2 | c9d754e0... | paasng.misc.monitoring.metrics.clients (BkPromResult) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/monitoring/metrics/test_metric_manager.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal_gen_series_query | 51-66 | 4 | 3598cd71... | paasng.misc.monitoring.metrics.constants (MetricsResourceType), paasng.misc.monitoring.metrics.models (ResourceMetricManager), paasng.misc.monitoring.metrics.utils (MetricSmartTimeRange), unittest.mock (Mock, patch) |
| test_empty_gen_series_query | 68-82 | 3 | 68e09f8b... | paasng.misc.monitoring.metrics.constants (MetricsResourceType), paasng.misc.monitoring.metrics.models (ResourceMetricManager), paasng.misc.monitoring.metrics.utils (MetricSmartTimeRange), typing (List), unittest.mock (Mock, patch) |
| test_exception_gen_series_query | 84-97 | 1 | 24f6fef4... | collections (namedtuple), paasng.misc.monitoring.metrics.constants (MetricsResourceType), paasng.misc.monitoring.metrics.exceptions (RequestMetricBackendError), paasng.misc.monitoring.metrics.models (ResourceMetricManager), paasng.misc.monitoring.metrics.utils (MetricSmartTimeRange), unittest.mock (Mock, patch) |
| test_gen_series_query | 99-114 | 2 | 18149690... | django.conf (settings), paasng.misc.monitoring.metrics.constants (MetricsResourceType, MetricsSeriesType), paasng.misc.monitoring.metrics.models (ResourceMetricManager), paasng.misc.monitoring.metrics.utils (MetricSmartTimeRange) |
| test_gen_all_series_query | 116-124 | 1 | 92b33df9... | paasng.misc.monitoring.metrics.constants (MetricsResourceType), paasng.misc.monitoring.metrics.models (ResourceMetricManager), paasng.misc.monitoring.metrics.utils (MetricSmartTimeRange) |
| test_simple_date_string | 128-132 | 2 | 209f0eb9... | paasng.misc.monitoring.metrics.utils (MetricSmartTimeRange) |
| test_to_now | 134-143 | 3 | b39dde3b... | datetime (datetime), paasng.misc.monitoring.metrics.utils (MetricSmartTimeRange) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/monitoring/service_monitor/test_controller.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_init_sync | 36-58 | 2 | 6b02cc37... | django_dynamic_fixture (G), paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paasng.misc.monitoring.monitor.service_monitor.controller (ServiceMonitorController), paasng.platform.bkapp_model.entities (Monitoring), paasng.platform.bkapp_model.models (ObservabilityConfig), unittest (mock) |
| test_sync_with_different_process | 60-96 | 3 | c58d88c1... | django_dynamic_fixture (G), paas_wl.bk_app.monitoring.app_monitor.kres_entities (Endpoint, ServiceMonitor, ServiceSelector), paas_wl.infras.resources.kube_res.exceptions (AppEntityNotFound), paasng.misc.monitoring.monitor.service_monitor.controller (ServiceMonitorController), paasng.platform.bkapp_model.entities (Monitoring), paasng.platform.bkapp_model.models (ObservabilityConfig), unittest (mock) |
| test_sync_with_same_process | 98-125 | 3 | c7db5371... | django_dynamic_fixture (G), paas_wl.bk_app.monitoring.app_monitor.kres_entities (Endpoint, ServiceMonitor, ServiceSelector), paasng.misc.monitoring.monitor.service_monitor.controller (ServiceMonitorController), paasng.platform.bkapp_model.entities (Monitoring), paasng.platform.bkapp_model.models (ObservabilityConfig), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/monitoring/test_alert.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_to_dict | 81-111 | 2 | d68cf6c9... | pytest (pytest) |
| test_to_dict | 115-146 | 2 | 2f4612e4... | pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/monitoring/test_dashboard.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_init_dashboard_command | 63-74 | 2 | eb0c7c1b... | paasng.infras.bkmonitorv3.client (BkMonitorClient), paasng.misc.monitoring.monitor.dashboards.manager (BkDashboardManager), paasng.misc.monitoring.monitor.models (AppDashboard), pytest (pytest), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/monitoring/test_metric_label.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_invalid_cluster_id | 38-56 | 1 | fb05881b... | paasng.misc.monitoring.monitor.alert_rules.config.metric_label (get_cluster_id), paasng.misc.monitoring.monitor.exceptions (BKMonitorNotSupportedError), pytest (pytest), tests.utils.helpers (generate_random_string), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/operations/test_operations.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 39-48 | 1 | 697f3d9b... | paasng.misc.operations.constant (OperationType), paasng.misc.operations.models (Operation) |
| test_normal | 52-70 | 1 | b8ca3f99... | paasng.misc.operations.constant (OperationType), paasng.misc.operations.models (Operation), pytest (pytest) |
| test_create_from_deployment | 74-88 | 1 | 7ae2f806... | paasng.misc.operations.models (AppDeploymentOperationObj), paasng.platform.engine.constants (JobStatus), pytest (pytest), tests.paasng.platform.engine.setup_utils (create_fake_deployment) |
| test_create_from_deploy | 92-103 | 1 | 29948e2d... | paas_wl.bk_app.cnative.specs.constants (DeployStatus), paasng.misc.operations.models (CNativeAppDeployOperationObj), pytest (pytest), tests.paas_wl.bk_app.cnative.specs.utils (create_cnative_deploy) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/test_changelog.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_logs | 45-56 | 6 | e2ff2c25... | paasng.misc.changelog.query (Changelog) |

---


### 测试文件: apiserver/paasng/tests/paasng/misc/tools/test_app_desc.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_service | 32-50 | 1 | cc38e96f... | django.conf (settings), paasng.misc.tools.app_desc (create_service), pytest (pytest) |
| test_transform_module_spec | 53-178 | 1 | e702e572... | collections (OrderedDict), django.conf (settings), paasng.misc.tools.app_desc (transform_module_spec), pytest (pytest), typing (Any) |
| test_transform_modules_section | 181-359 | 1 | 139e8215... | collections (OrderedDict), django.conf (settings), paasng.misc.tools.app_desc (transform_modules_section), pytest (pytest) |
| test_transform_app_desc_spec2_to_spec3 | 362-483 | 1 | 4c9b6c16... | collections (OrderedDict), django.conf (settings), paasng.misc.tools.app_desc (transform_app_desc_spec2_to_spec3), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/plat_admin/admin_cli/test_mapper_version.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 29-36 | 2 | f60228e7... | paasng.plat_admin.admin_cli.mapper_version (get_mapper_v1_envs) |
| test_multiple_configs | 38-44 | 2 | eee214cc... | paas_wl.bk_app.applications.models.config (Config), paasng.plat_admin.admin_cli.mapper_version (get_mapper_v1_envs) |

---


### 测试文件: apiserver/paasng/tests/paasng/plat_admin/test_numbers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 49-56 | 3 | 458d09ba... | paasng.plat_admin.numbers.app (DefaultAppDataBuilder, SimpleApp) |
| test_with_filter_developers | 58-66 | 2 | fac2130a... | paasng.plat_admin.numbers.app (DefaultAppDataBuilder) |
| test_normal | 70-79 | 2 | 7a491580... | paasng.plat_admin.numbers.app (LegacyAppDataBuilder, SimpleApp), tests.utils.helpers (create_legacy_application) |
| test_with_mock | 84-97 | 5 | 6cf4760a... | paasng.plat_admin.numbers.app (Contribution, calculate_user_contribution_in_app, group_apps_by_developers), unittest (mock) |
| test_with_filter_developers | 101-106 | 1 | 459997a6... | paasng.plat_admin.numbers.app (make_table_apps_grouped_by_developer) |
| test_without_filter_developers | 108-113 | 1 | f6d98d6f... | paasng.plat_admin.numbers.app (make_table_apps_grouped_by_developer) |
| test_with_filter_developers | 117-126 | 4 | 47f6caaf... | paasng.plat_admin.numbers.app (make_table_apps_grouped_by_developer_simple) |
| test_with_matched | 130-137 | 1 | 30f91b92... | paasng.plat_admin.numbers.app (make_table_apps_basic_info), tests.utils.helpers (create_legacy_application) |
| test_without_matched | 139-142 | 1 | 2df7f9fc... | paasng.plat_admin.numbers.app (make_table_apps_basic_info) |
| test_print_table | 145-151 | 0 | 1da926d7... | paasng.plat_admin.numbers.app (make_table_apps_grouped_by_developer, print_table) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/applications/test_applications.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_default_module | 40-49 | 3 | 4dc828a9... | django.conf (settings), django_dynamic_fixture (G), paasng.platform.applications.models (Application), paasng.platform.applications.utils (create_default_module), paasng.platform.modules.models (Module) |
| test_filter_by_user_normal | 104-106 | 1 | d66e3366... | paasng.platform.applications.models (Application) |
| test_filter_by_userremove | 108-113 | 1 | 59bff071... | paasng.infras.iam.helpers (fetch_application_members, remove_user_all_roles), paasng.platform.applications.models (Application) |
| test_filter_language | 115-124 | 2 | dd918ebf... | paasng.platform.applications.models (Application), paasng.platform.modules.models (Module) |
| test_active_only | 126-133 | 2 | 9355a6ae... | paasng.platform.applications.models (Application) |
| test_search_by_code_or_name | 135-137 | 1 | f912094a... | paasng.platform.applications.models (Application) |
| test_filter_by_user | 139-144 | 2 | a8f6788f... | paasng.platform.applications.models (Application) |
| test_filter_by_source_origin | 146-148 | 1 | 5dc9d7fc... | paasng.platform.applications.models (Application), paasng.platform.modules.constants (SourceOrigin) |
| test_filter | 152-155 | 2 | 30de08a5... | paasng.platform.applications.models (UserApplicationFilter) |
| test_filter_by_type_ | 157-163 | 1 | 8c304981... | paasng.platform.applications.constants (ApplicationType), paasng.platform.applications.models (UserApplicationFilter) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/applications/test_feature_flag.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_override | 27-132 | 1 | d9fc483a... | paasng.platform.applications.models (Application, get_default_feature_flags), pytest (pytest), tests.utils.helpers (override_region_configs), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/applications/test_lapp.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create | 66-130 | 7 | 548175cc... | pytest (pytest) |
| test_delete | 132-150 | 3 | 324249bc... | paasng.core.core.storages.sqlalchemy (legacy_db), paasng.infras.legacydb.adaptors (AppAdaptor), pytest (pytest) |
| test_query | 152-173 | 4 | 4e1e7f15... | paasng.core.core.storages.sqlalchemy (legacy_db), paasng.infras.legacydb.adaptors (AppAdaptor), pytest (pytest) |
| test_edit | 175-244 | 5 | 91902a03... | paasng.core.core.storages.sqlalchemy (legacy_db), paasng.infras.legacydb.adaptors (AppAdaptor), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/applications/test_protection.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_status_empty | 37-42 | 1 | d7537504... | paasng.platform.applications.protections (AppResProtector, ProtectedRes, ProtectionStatus) |
| test_smart_app | 44-53 | 1 | 32b5c55f... | paasng.platform.applications.protections (AppResProtector, ConditionNotMatched, ProtectedRes, ProtectionStatus) |
| test_list_status | 55-65 | 1 | 6bdcd8ad... | paasng.platform.applications.protections (AppResProtector, ConditionNotMatched, ProtectedRes, ProtectionStatus) |
| test_get_status | 67-71 | 1 | 0ba926de... | paasng.platform.applications.protections (AppResProtector, ConditionNotMatched, ProtectedRes, ProtectionStatus) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/applications/test_serializers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_normal | 36-38 | 1 | cb0a0343... |  |
| test_forbid_underscore | 40-42 | 1 | 3af3cd02... |  |
| test_create_existed_found | 44-46 | 1 | 952c440e... |  |
| test_create_existed_found_in_external | 48-52 | 1 | f3b84fd1... | paasng.platform.applications.exceptions (AppFieldValidationError), paasng.platform.applications.signals (prepare_use_application_code), unittest (mock) |
| test_update_same_code | 54-56 | 1 | bb43178e... |  |
| test_update_code_is_forbidden | 58-61 | 1 | 068c9e44... | tests.utils.helpers (create_app) |
| test_update_random_is_forbidden | 63-65 | 1 | 1a922d72... |  |
| test_max_length_is_20 | 73-78 | 2 | 65d8b0a5... |  |
| test_allow_underscore | 80-82 | 1 | a722d4ce... |  |
| test_create_existed_found_in_external | 90-94 | 1 | 0742a257... | paasng.platform.applications.exceptions (AppFieldValidationError), paasng.platform.applications.signals (prepare_use_application_name), unittest (mock) |
| test_update_different_name | 96-98 | 1 | c2b12b5a... |  |
| test_update_existed_found_in_external | 100-104 | 1 | 9bb8bc94... | paasng.platform.applications.exceptions (AppFieldValidationError), paasng.platform.applications.signals (prepare_use_application_name), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/applications/test_specs.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_engine_enabled | 30-41 | 1 | 521b4f80... | paasng.platform.applications.constants (ApplicationType), paasng.platform.applications.specs (AppSpecs), pytest (pytest) |
| test_can_create_extra_modules | 43-69 | 1 | be2a07f6... | paasng.platform.applications.constants (ApplicationType), paasng.platform.applications.specs (AppSpecs), pytest (pytest), tests.utils.helpers (override_region_configs) |
| test_confirm_required_when_publish_with_no_template | 71-73 | 1 | 25440c84... | paasng.platform.applications.specs (AppSpecs) |
| test_confirm_required_when_publish_with_template | 75-90 | 1 | 4e1bf567... | paasng.platform.applications.specs (AppSpecs), paasng.platform.templates.constants (TemplateType), paasng.platform.templates.models (Template), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_domain_resolution.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create | 29-42 | 5 | 88d1bb93... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (DomainResolution, HostAlias), paasng.platform.bkapp_model.entities_syncer (sync_domain_resolution), paasng.platform.bkapp_model.models (DomainResolution) |
| test_update | 44-66 | 5 | b0af6673... | django_dynamic_fixture (G), paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (DomainResolution, HostAlias), paasng.platform.bkapp_model.entities_syncer (sync_domain_resolution), paasng.platform.bkapp_model.models (DomainResolution) |
| test_delete | 68-83 | 2 | c89fee86... | django_dynamic_fixture (G), paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (DomainResolution, HostAlias), paasng.platform.bkapp_model.entities_syncer (sync_domain_resolution), paasng.platform.bkapp_model.models (DomainResolution) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_env_vars.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_integrated | 30-40 | 5 | fcacc8d1... | django_dynamic_fixture (G), paasng.platform.bkapp_model.entities (EnvVar, EnvVarOverlay), paasng.platform.bkapp_model.entities_syncer (sync_env_vars), paasng.platform.engine.constants (ConfigVarEnvName), paasng.platform.engine.models.preset_envvars (PresetEnvVariable) |
| test_notset_remove_all | 42-46 | 1 | e2c75edf... | django_dynamic_fixture (G), paasng.platform.bkapp_model.entities_syncer (sync_env_vars), paasng.platform.engine.constants (ConfigVarEnvName), paasng.platform.engine.models.preset_envvars (PresetEnvVariable), paasng.utils.structure (NOTSET) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_hooks.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create | 30-35 | 3 | eb807643... | paasng.platform.bkapp_model.entities (HookCmd, Hooks), paasng.platform.bkapp_model.entities_syncer (sync_hooks), paasng.platform.bkapp_model.fieldmgr.constants (FieldMgrName), paasng.platform.bkapp_model.models (ModuleDeployHook) |
| test_update | 37-45 | 4 | 324f2b5f... | django_dynamic_fixture (G), paasng.platform.bkapp_model.entities (HookCmd, Hooks), paasng.platform.bkapp_model.entities_syncer (sync_hooks), paasng.platform.bkapp_model.fieldmgr.constants (FieldMgrName), paasng.platform.bkapp_model.models (DeployHookType, ModuleDeployHook) |
| test_delete | 47-53 | 3 | cd7e7457... | django_dynamic_fixture (G), paasng.platform.bkapp_model.entities (Hooks), paasng.platform.bkapp_model.entities_syncer (sync_hooks), paasng.platform.bkapp_model.fieldmgr.constants (FieldMgrName), paasng.platform.bkapp_model.models (DeployHookType, ModuleDeployHook) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_mounts.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_integrated | 33-77 | 7 | 688544ec... | functools (functools), paas_wl.bk_app.cnative.specs.constants (MountEnvName, VolumeSourceType), paas_wl.bk_app.cnative.specs.crd (bk_app), paas_wl.bk_app.cnative.specs.models (Mount), paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (ConfigMapSource, Mount, MountOverlay, VolumeSource), paasng.platform.bkapp_model.entities_syncer (sync_mounts) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_observability.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create | 29-39 | 4 | 3a51f388... | paasng.platform.bkapp_model.entities (Metric, Observability), paasng.platform.bkapp_model.entities_syncer (sync_observability), paasng.platform.bkapp_model.models (ObservabilityConfig) |
| test_update | 41-65 | 7 | 69878a63... | django_dynamic_fixture (G), paasng.platform.bkapp_model.entities (Metric, Monitoring, Observability), paasng.platform.bkapp_model.entities_syncer (sync_observability), paasng.platform.bkapp_model.models (ObservabilityConfig) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_proc_env_overlays.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_integrated | 69-98 | 10 | 1c0a019f... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (ReplicasOverlay), paasng.platform.bkapp_model.entities_syncer (sync_env_overlays_replicas), paasng.utils.structure (NOTSET) |
| test_integrated_with_different_manager | 100-122 | 2 | 27eebeb4... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (ReplicasOverlay), paasng.platform.bkapp_model.entities_syncer (sync_env_overlays_replicas) |
| test_clean_empty | 124-136 | 2 | 070fc834... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (ReplicasOverlay), paasng.platform.bkapp_model.entities_syncer (clean_empty_overlays, sync_env_overlays_replicas), paasng.platform.bkapp_model.models (ProcessSpecEnvOverlay) |
| test_normal | 140-155 | 6 | 2cd5a186... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.constants (ResQuotaPlan), paasng.platform.bkapp_model.entities (ResQuotaOverlay), paasng.platform.bkapp_model.entities_syncer (sync_env_overlays_res_quotas) |
| test_normal | 159-185 | 9 | 17d85f4b... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (AutoscalingConfig, AutoscalingOverlay), paasng.platform.bkapp_model.entities_syncer (sync_env_overlays_autoscalings) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_processes.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_integrated | 37-99 | 20 | 17bc11a7... | paasng.platform.bkapp_model.entities (AutoscalingConfig, HTTPGetAction, Probe, ProbeSet, ProcService, Process, TCPSocketAction), paasng.platform.bkapp_model.entities_syncer (sync_processes), paasng.platform.bkapp_model.fieldmgr.constants (FieldMgrName), paasng.platform.bkapp_model.models (ModuleProcessSpec) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_svc_discovery.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create | 31-41 | 2 | b9f6c85c... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (SvcDiscConfig, SvcDiscEntryBkSaaS), paasng.platform.bkapp_model.entities_syncer (sync_svc_discovery), paasng.platform.bkapp_model.models (SvcDiscConfig) |
| test_update | 43-62 | 4 | 3b1e55d2... | django_dynamic_fixture (G), paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (SvcDiscConfig, SvcDiscEntryBkSaaS), paasng.platform.bkapp_model.entities_syncer (sync_svc_discovery), paasng.platform.bkapp_model.models (SvcDiscConfig) |
| test_delete | 64-74 | 2 | d730f2e4... | django_dynamic_fixture (G), paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (SvcDiscConfig, SvcDiscEntryBkSaaS), paasng.platform.bkapp_model.entities_syncer (sync_svc_discovery), paasng.platform.bkapp_model.models (SvcDiscConfig) |
| test_notset_value_different_manager | 76-90 | 3 | 8885ef32... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (SvcDiscConfig, SvcDiscEntryBkSaaS), paasng.platform.bkapp_model.entities_syncer (sync_svc_discovery), paasng.platform.bkapp_model.models (SvcDiscConfig), paasng.utils.structure (NOTSET) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/fieldmgr/test_fields.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_start_from_empty | 30-42 | 5 | 2d445e10... | paasng.platform.bkapp_model.fieldmgr.constants (FieldMgrName), paasng.platform.bkapp_model.fieldmgr.fields (F_SVC_DISCOVERY, ManagerFieldsRowGroup) |
| test_existed_rows | 45-64 | 5 | 02a85cdd... | paasng.platform.bkapp_model.fieldmgr.constants (FieldMgrName), paasng.platform.bkapp_model.fieldmgr.fields (F_DOMAIN_RESOLUTION, F_SVC_DISCOVERY, ManagerFieldsRow, ManagerFieldsRowGroup), pytest (pytest) |
| test_reset_manager | 66-75 | 2 | 3d6f1ef2... | paasng.platform.bkapp_model.fieldmgr.constants (FieldMgrName), paasng.platform.bkapp_model.fieldmgr.fields (F_DOMAIN_RESOLUTION, F_SVC_DISCOVERY, ManagerFieldsRow, ManagerFieldsRowGroup) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/fieldmgr/test_managers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_integrated | 26-40 | 5 | 863ec4f6... | paasng.platform.bkapp_model.fieldmgr.constants (FieldMgrName), paasng.platform.bkapp_model.fieldmgr.fields (F_SVC_DISCOVERY), paasng.platform.bkapp_model.fieldmgr.managers (FieldManager) |
| test_integrated | 44-49 | 2 | 261bff8a... | paasng.platform.bkapp_model.fieldmgr.constants (FieldMgrName), paasng.platform.bkapp_model.fieldmgr.fields (F_DOMAIN_RESOLUTION, F_SVC_DISCOVERY), paasng.platform.bkapp_model.fieldmgr.managers (FieldManager, MultiFieldsManager) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/test_importer.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_initialization | 67-71 | 1 | 0be41ec9... | paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_reset_by_notset | 73-80 | 2 | 02e22a4f... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_ignore_not_managed_when_notset | 82-88 | 1 | 008b278c... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.importer (import_manifest), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_set_to_zero | 90-98 | 1 | 87b60c25... | copy (copy), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_enable | 113-127 | 5 | 27a1e6ff... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_disable_by_notset | 129-138 | 3 | e695447b... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_ignore_not_managed_when_notset | 140-148 | 2 | f6c4c2ff... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.importer (import_manifest), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_import_with_enum_type | 151-168 | 2 | 83f2fed6... | paasng.platform.bkapp_model.constants (ResQuotaPlan, ScalingPolicy), paasng.platform.bkapp_model.entities (AutoscalingConfig), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_invalid_name_input | 172-178 | 2 | 3b235a67... | paasng.platform.bkapp_model.exceptions (ManifestImportError), pytest (pytest) |
| test_normal | 180-185 | 1 | d2b7d683... | paasng.platform.engine.models.preset_envvars (PresetEnvVariable) |
| test_invalid_value | 189-194 | 2 | 28bfedb4... | paasng.platform.bkapp_model.exceptions (ManifestImportError), pytest (pytest) |
| test_invalid_spec | 196-201 | 2 | 13f4377d... | paasng.platform.bkapp_model.exceptions (ManifestImportError), pytest (pytest) |
| test_normal | 203-205 | 0 | baf640d3... |  |
| test_invalid_mount_path_input | 210-218 | 2 | 6dacc38a... | paasng.platform.bkapp_model.exceptions (ManifestImportError), pytest (pytest) |
| test_normal | 220-236 | 1 | c5bed930... | paas_wl.bk_app.cnative.specs.models (Mount) |
| test_invalid_replicas_input | 246-253 | 2 | 29105875... | paasng.platform.bkapp_model.exceptions (ManifestImportError), pytest (pytest) |
| test_str | 255-258 | 1 | e1f2643e... | paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_reset_by_not_providing_value | 260-265 | 1 | 5896becf... | paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_not_reset_when_manager_different | 267-272 | 1 | 93ec801d... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.importer (import_manifest), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_not_reset_when_manager_different_and_overlay_subfield_notset | 274-288 | 1 | 854ed5cc... | copy (copy), paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.importer (import_manifest), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_proc_replicas_reset_overlay_managed_by_other | 290-300 | 2 | 6f72f71b... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.importer (import_manifest), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_normal | 304-322 | 2 | fb591a89... | paasng.platform.bkapp_model.constants (ScalingPolicy), paasng.platform.bkapp_model.entities (AutoscalingConfig), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_missing_policy | 324-341 | 2 | ffef98c8... | paasng.platform.bkapp_model.constants (ScalingPolicy), paasng.platform.bkapp_model.entities (AutoscalingConfig), paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_normal | 345-361 | 1 | 938f9eee... | paasng.platform.bkapp_model.entities (SvcDiscEntryBkSaaS), paasng.platform.bkapp_model.models (SvcDiscConfig) |
| test_normal | 370-378 | 1 | 8be9a3d4... | paasng.platform.bkapp_model.entities (Metric), paasng.platform.bkapp_model.models (ObservabilityConfig), paasng.utils.camel_converter (dict_to_camel) |
| test_with_no_monitoring | 380-383 | 1 | b5c8de61... | paasng.platform.bkapp_model.models (ObservabilityConfig) |
| test_invalid_spec | 385-392 | 2 | 37f0cf11... | paasng.platform.bkapp_model.exceptions (ManifestImportError), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/test_manager.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_set_replicas_integrated | 35-47 | 5 | 4c85b90b... | paasng.platform.bkapp_model.manager (ModuleProcessSpecManager), paasng.platform.bkapp_model.models (ProcessSpecEnvOverlay) |
| test_set_autoscaling_integrated | 49-70 | 7 | b129b015... | paas_wl.workloads.autoscaling.entities (AutoscalingConfig), paasng.platform.bkapp_model.entities (AutoscalingConfig), paasng.platform.bkapp_model.manager (ModuleProcessSpecManager), paasng.platform.bkapp_model.models (ProcessSpecEnvOverlay) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/test_manifest.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_empty | 134-137 | 1 | 587fcdf5... | paasng.platform.bkapp_model.manifest (AddonsManifestConstructor) |
| test_with_addons | 139-144 | 2 | 78b3d904... | paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.platform.bkapp_model.manifest (AddonsManifestConstructor) |
| test_with_shared_addons | 146-154 | 2 | 0b386910... | paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.sharing (ServiceSharingManager), paasng.platform.bkapp_model.manifest (AddonsManifestConstructor) |
| test_integrated | 158-174 | 2 | 63a02c1d... | paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (EnvVarsManifestConstructor), paasng.platform.engine.models.config_var (ConfigVar, ENVIRONMENT_ID_FOR_GLOBAL) |
| test_preset | 176-186 | 2 | ce1544b7... | django_dynamic_fixture (G), paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (EnvVarsManifestConstructor), paasng.platform.engine.constants (ConfigVarEnvName), paasng.platform.engine.models.preset_envvars (PresetEnvVariable) |
| test_override_preset | 188-209 | 2 | ea58b474... | django_dynamic_fixture (G), paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (EnvVarsManifestConstructor), paasng.platform.engine.constants (ConfigVarEnvName), paasng.platform.engine.models.config_var (ConfigVar, ENVIRONMENT_ID_FOR_GLOBAL), paasng.platform.engine.models.preset_envvars (PresetEnvVariable) |
| test_normal | 213-224 | 4 | b97bf552... | paas_wl.core.resource (generate_bkapp_name), paasng.platform.bkapp_model.manifest (BuiltinAnnotsManifestConstructor) |
| test_get_quota_plan | 251-264 | 1 | d8d381d4... | django.conf (settings), paas_wl.bk_app.processes.models (initialize_default_proc_spec_plans), paasng.platform.bkapp_model.constants (ResQuotaPlan), paasng.platform.bkapp_model.manifest (ProcessesManifestConstructor), pytest (pytest) |
| test_get_command_and_args | 266-279 | 1 | a925aaf0... | paasng.platform.bkapp_model.manifest (DEFAULT_SLUG_RUNNER_ENTRYPOINT, ProcessesManifestConstructor), paasng.platform.engine.constants (RuntimeType), paasng.platform.modules.models (BuildConfig), pytest (pytest), unittest (mock) |
| test_get_command_and_args_invalid_var_expr | 281-292 | 1 | 090c2b0e... | django_dynamic_fixture (G), paasng.platform.bkapp_model.manifest (ProcessesManifestConstructor), paasng.platform.bkapp_model.models (ModuleProcessSpec), paasng.platform.engine.constants (RuntimeType), paasng.platform.modules.models (BuildConfig) |
| test_integrated | 294-333 | 1 | 576742c6... | paas_wl.bk_app.processes.models (initialize_default_proc_spec_plans), paasng.platform.bkapp_model.manifest (ProcessesManifestConstructor) |
| test_integrated_autoscaling | 335-343 | 1 | c9852cef... | paas_wl.bk_app.processes.models (initialize_default_proc_spec_plans), paasng.platform.bkapp_model.manifest (ProcessesManifestConstructor) |
| test_integrated_proc_services | 345-351 | 1 | ebf58770... | django.conf (settings), paasng.platform.bkapp_model.manifest (ProcessesManifestConstructor) |
| test_normal | 355-383 | 2 | a791af68... | django_dynamic_fixture (G), functools (functools), paas_wl.bk_app.cnative.specs.constants (MountEnvName, VolumeSourceType), paas_wl.bk_app.cnative.specs.crd (bk_app), paas_wl.bk_app.cnative.specs.models (Mount), paasng.platform.bkapp_model.manifest (MountsManifestConstructor) |
| test_normal | 387-395 | 1 | 4b3958e0... | paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (HooksManifestConstructor), paasng.platform.modules.constants (DeployHookType) |
| test_proc_command | 397-405 | 1 | aaff06f5... | paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (HooksManifestConstructor), paasng.platform.modules.constants (DeployHookType) |
| test_not_found | 407-409 | 1 | 1910ac36... | paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (HooksManifestConstructor) |
| test_empty_command | 411-414 | 1 | 04b15057... | paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (HooksManifestConstructor), paasng.platform.modules.constants (DeployHookType) |
| test_normal | 418-436 | 1 | bbcb740d... | django_dynamic_fixture (G), paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (SvcDiscoveryManifestConstructor), paasng.platform.bkapp_model.models (SvcDiscConfig) |
| test_normal | 440-469 | 1 | 3836ada3... | django_dynamic_fixture (G), paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (DomainResolutionManifestConstructor), paasng.platform.bkapp_model.models (DomainResolution) |
| test_normal | 473-486 | 1 | 8e9f4980... | django_dynamic_fixture (G), paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (ObservabilityManifestConstructor), paasng.platform.bkapp_model.models (ObservabilityConfig) |
| test_with_no_observability | 488-490 | 1 | 356623c1... | paasng.platform.bkapp_model.manifest (ObservabilityManifestConstructor) |
| test_get_manifest | 493-496 | 2 | 4ec6cfec... | paasng.platform.bkapp_model.manifest (get_manifest) |
| test_apply_env_annots | 499-506 | 3 | a64158e2... | paasng.platform.bkapp_model.manifest (apply_env_annots), pytest (pytest) |
| test_apply_env_annots_with_deploy_id | 509-512 | 1 | 61a1a149... | paasng.platform.bkapp_model.manifest (apply_env_annots), pytest (pytest) |
| test_apply_builtin_env_vars | 515-548 | 4 | 6c988cff... | django_dynamic_fixture (G), paasng.platform.bkapp_model.manifest (apply_builtin_env_vars), paasng.platform.declarative.deployment.controller (DeploymentDescription), pytest (pytest) |
| test_builtin_env_has_high_priority | 551-565 | 2 | 9d667ecf... | paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (apply_builtin_env_vars), pytest (pytest), tests.utils.helpers (generate_random_string) |
| test_apply_proc_svc_if_implicit_needed_is_false | 568-570 | 1 | b48e5816... | paasng.platform.bkapp_model.manifest (apply_proc_svc_if_implicit_needed) |
| test_apply_proc_svc_if_implicit_needed_is_true | 573-580 | 5 | cd1ef9df... | paas_wl.bk_app.cnative.specs.crd (bk_app), paasng.platform.bkapp_model.manifest (apply_proc_svc_if_implicit_needed), paasng.platform.bkapp_model.models (ProcessServicesFlag) |
| test_apply_egress_annotations | 583-593 | 1 | fb3f7db8... | django.conf (settings), django.core.management (call_command), paas_wl.bk_app.cnative.specs.constants (EGRESS_CLUSTER_STATE_NAME_ANNO_KEY), paas_wl.workloads.networking.egress.models (RCStateAppBinding, RegionClusterState), paasng.platform.bkapp_model.manifest (apply_egress_annotations), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create | 32-45 | 3 | a33d65ed... | paasng.platform.bkapp_model.models (ProcessSpecEnvOverlay) |
| test_update | 47-67 | 2 | d4abeb63... | paasng.platform.bkapp_model.constants (ResQuotaPlan), paasng.platform.bkapp_model.models (ProcessSpecEnvOverlay) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/test_render_port.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_proc_service | 23-28 | 2 | 77531a9f... | django.conf (settings), paasng.platform.bkapp_model.entities (ProcService) |
| test_probes | 30-39 | 3 | c2f93340... | django.conf (settings), paasng.platform.bkapp_model.entities (ProbeSet) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/bkapp_model/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_merge_env_vars | 28-56 | 1 | 83582827... | paas_wl.bk_app.cnative.specs.crd.bk_app (EnvVar), paasng.platform.bkapp_model.utils (MergeStrategy, merge_env_vars), pytest (pytest) |
| test_merge_env_vars_overlay | 59-108 | 1 | 2b8804e0... | paas_wl.bk_app.cnative.specs.crd.bk_app (EnvVarOverlay), paasng.platform.bkapp_model.utils (MergeStrategy, merge_env_vars_overlay), pytest (pytest) |
| test_override_env_vars_overlay | 111-170 | 1 | e643c1bc... | paas_wl.bk_app.cnative.specs.crd.bk_app (EnvVarOverlay), paasng.platform.bkapp_model.utils (override_env_vars_overlay), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/application/v2/test_controller.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_run_invalid_input | 63-71 | 2 | 431c68be... | paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest) |
| test_app_code_length | 73-89 | 0 | 698843a7... | blue_krill.contextlib (nullcontext), paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator), tests.utils.helpers (generate_random_string) |
| test_name_is_duplicated | 91-99 | 2 | be7fbc59... | paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.utils.helpers (create_app) |
| test_invalid_module_name | 101-105 | 1 | e81ff3ba... | paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator) |
| test_region_perm_check | 107-132 | 2 | 8df6fbd0... | paasng.infras.accounts.models (UserProfile), paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator), tests.utils.helpers (configure_regions) |
| test_normal | 134-137 | 0 | f8ab5459... | paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator) |
| test_i18n | 139-154 | 4 | 46e8d029... | django.utils.translation (override), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator) |
| test_without_permission | 169-179 | 2 | fd1874ab... | paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator), tests.utils.auth (create_user) |
| test_region_modified | 181-196 | 2 | 6309d865... | paasng.core.region.models (get_all_regions), paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator) |
| test_name_modified | 198-213 | 2 | 2bb7f324... | paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator) |
| test_normal | 215-223 | 0 | c89f0d44... | paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator) |
| test_creation | 227-238 | 2 | 714846cb... | paasng.accessories.publish.market.models (Product), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator) |
| test_update_partial | 240-258 | 4 | 6b58f786... | paasng.accessories.publish.market.models (Product), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator) |
| test_creation_omitted | 262-276 | 7 | 76d1f632... | paasng.accessories.publish.market.models (Product), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator) |
| test_update_partial | 278-300 | 4 | d526474a... | paasng.accessories.publish.market.models (Product), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator) |
| test_creation | 334-340 | 1 | b9a50365... | django.conf (settings), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.platform.applications.models (Application), paasng.platform.declarative.application.controller (AppDeclarativeController) |
| test_update_add | 342-353 | 2 | 9b686816... | django.conf (settings), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.platform.applications.models (Application), paasng.platform.declarative.application.controller (AppDeclarativeController) |
| test_not_existed_service | 355-363 | 1 | 7ec29dfc... | paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.platform.applications.models (Application), paasng.platform.declarative.application.controller (AppDeclarativeController) |
| test_shared_service | 365-380 | 3 | b663010c... | django.conf (settings), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.sharing (ServiceSharingManager), paasng.platform.applications.models (Application), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV2Decorator) |
| test_shared_service_but_module_not_found | 382-387 | 1 | b09b7e87... | paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV2Decorator) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/application/v2/test_validations.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 51-56 | 0 | bd8ac5b8... | tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator), tests.utils.helpers (generate_random_string) |
| test_invalid_name_length | 58-64 | 1 | 44e71d50... | paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator), tests.utils.helpers (generate_random_string) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/application/v3/test_controller.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_run_invalid_input | 63-71 | 2 | 7d3ad4da... | paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest) |
| test_app_code_length | 73-89 | 0 | 698843a7... | blue_krill.contextlib (nullcontext), paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator), tests.utils.helpers (generate_random_string) |
| test_name_is_duplicated | 91-99 | 2 | bdf5b799... | paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.utils.helpers (create_app) |
| test_invalid_module_name | 101-105 | 1 | e81ff3ba... | paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator) |
| test_region_perm_check | 107-134 | 2 | 8df6fbd0... | paasng.infras.accounts.models (UserProfile), paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator), tests.utils.helpers (configure_regions) |
| test_normal | 136-139 | 0 | f8ab5459... | paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator) |
| test_i18n | 141-156 | 4 | 46e8d029... | django.utils.translation (override), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator) |
| test_without_permission | 171-181 | 2 | fd1874ab... | paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator), tests.utils.auth (create_user) |
| test_region_modified | 183-198 | 2 | 42607b33... | paasng.core.region.models (get_all_regions), paasng.platform.declarative.application.controller (AppDeclarativeController), paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator) |
| test_name_modified | 200-217 | 2 | 14cef16d... | paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator) |
| test_normal | 219-227 | 0 | 39acf2c0... | paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator) |
| test_creation | 231-242 | 2 | 714846cb... | paasng.accessories.publish.market.models (Product), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator) |
| test_update_partial | 244-262 | 4 | 6b58f786... | paasng.accessories.publish.market.models (Product), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator) |
| test_creation_omitted | 266-280 | 7 | 76d1f632... | paasng.accessories.publish.market.models (Product), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator) |
| test_update_partial | 282-304 | 4 | 6a7e0308... | paasng.accessories.publish.market.models (Product), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator) |
| test_creation | 338-344 | 1 | b9a50365... | django.conf (settings), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.platform.applications.models (Application), paasng.platform.declarative.application.controller (AppDeclarativeController) |
| test_update_add | 346-357 | 2 | 39d72e98... | django.conf (settings), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.platform.applications.models (Application), paasng.platform.declarative.application.controller (AppDeclarativeController) |
| test_not_existed_service | 359-367 | 1 | 5a68d9f8... | paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.platform.applications.models (Application), paasng.platform.declarative.application.controller (AppDeclarativeController) |
| test_shared_service | 369-386 | 3 | b62fb606... | django.conf (settings), paasng.accessories.servicehub.manager (mixed_service_mgr), paasng.accessories.servicehub.sharing (ServiceSharingManager), paasng.platform.applications.models (Application), paasng.platform.declarative.application.controller (AppDeclarativeController), tests.paasng.platform.declarative.utils (AppDescV3Decorator) |
| test_shared_service_but_module_not_found | 388-395 | 1 | cd730f59... | paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Decorator) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/application/v3/test_validations.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_one_module | 51-55 | 0 | d2fecd23... | tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator), tests.utils.helpers (generate_random_string) |
| test_invalid_name_length | 61-66 | 1 | 4b229a77... | paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder), tests.utils.helpers (generate_random_string) |
| test_missing_default_module | 68-73 | 1 | ba859de4... | paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator), tests.utils.helpers (generate_random_string) |
| test_multiple_default_module | 75-84 | 1 | 2fb11d81... | paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator), tests.utils.helpers (generate_random_string) |
| test_share_addon_error | 86-99 | 1 | e9ac6730... | paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator), tests.utils.helpers (generate_random_string) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/deployment/test_svc_disc.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_missing_app | 27-36 | 1 | a87b7624... | paasng.platform.bkapp_model.entities (SvcDiscEntryBkSaaS), paasng.platform.declarative.deployment.svc_disc (BkSaaSAddrDiscoverer) |
| test_existed_app | 38-47 | 1 | eac8bd7f... | paasng.platform.bkapp_model.entities (SvcDiscEntryBkSaaS), paasng.platform.declarative.deployment.svc_disc (BkSaaSAddrDiscoverer) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/deployment/v2/test_controller.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_python_framework_case | 47-54 | 1 | 7c6f611e... | paasng.platform.bkapp_model.models (ModuleProcessSpec), paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc) |
| test_known_cases | 56-77 | 3 | eafd2850... | paasng.platform.bkapp_model.models (ModuleProcessSpec), paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), pytest (pytest) |
| test_invalid_input | 81-86 | 2 | e121aac2... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.serializers (validate_desc), pytest (pytest) |
| test_spec | 88-99 | 1 | 55bff001... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), paasng.platform.engine.models.preset_envvars (PresetEnvVariable) |
| test_preset_environ_vars | 101-114 | 1 | 53f8714a... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), paasng.platform.engine.constants (ConfigVarEnvName), paasng.platform.engine.models.preset_envvars (PresetEnvVariable) |
| test_as_env_vars_domain | 136-153 | 5 | 2867c01f... | paasng.platform.bkapp_model.models (get_svc_disc_as_env_variables), paasng.platform.declarative.deployment.svc_disc (BkSaaSEnvVariableFactory), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_as_env_vars_subpath | 155-172 | 5 | 8592a096... | paasng.platform.bkapp_model.models (get_svc_disc_as_env_variables), paasng.platform.declarative.deployment.svc_disc (BkSaaSEnvVariableFactory), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_notset_should_reset | 176-188 | 2 | 5d4465d1... | paasng.platform.bkapp_model.models (SvcDiscConfig), paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc) |
| test_notset_should_skip_when_manager_different | 190-205 | 2 | db8292df... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities.svc_discovery (SvcDiscEntryBkSaaS), paasng.platform.bkapp_model.entities_syncer.svc_discovery (sync_svc_discovery), paasng.platform.bkapp_model.models (SvcDiscConfig), paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc) |
| test_field_not_set | 209-215 | 2 | acb942ec... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc) |
| test_field_set | 217-225 | 1 | e97f7cb5... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc) |
| test_not_set_should_not_touch_deployment | 227-247 | 4 | fcead596... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.models (DeploymentDescription), paasng.platform.declarative.serializers (validate_desc), paasng.platform.modules.constants (DeployHookType), paasng.platform.modules.models.deploy_config (HookList), pytest (pytest) |
| test_rewrite_the_hook | 249-261 | 1 | d9ddc3c5... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), paasng.platform.modules.constants (DeployHookType), pytest (pytest) |
| test_not_set_should_reset | 263-275 | 2 | 38759b9a... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc) |
| test_not_set_with_different_mgr_should_keep | 277-291 | 2 | 54a937f8... | paasng.platform.bkapp_model.entities.hooks (HookCmd, Hooks), paasng.platform.bkapp_model.entities_syncer.hooks (sync_hooks), paasng.platform.bkapp_model.fieldmgr.constants (FieldMgrName), paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v2 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), paasng.platform.modules.constants (DeployHookType) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/deployment/v2/test_validations.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 40-44 | 0 | 96869629... | tests.paasng.platform.declarative.utils (AppDescV2Builder), tests.utils.helpers (generate_random_string) |
| test_invalid_proc_type | 46-51 | 1 | f514d8fa... | paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV2Builder), tests.utils.helpers (generate_random_string) |
| test_invalid_probes | 53-60 | 1 | e52b4eaf... | paasng.platform.declarative.exceptions (DescriptionValidationError), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV2Builder), tests.utils.helpers (generate_random_string) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/deployment/v3/test_controller.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_python_framework_case | 53-91 | 2 | d3034ee0... | paasng.platform.bkapp_model.models (ModuleProcessSpec), paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v3 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_invalid_input | 95-111 | 1 | 8279c4af... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v3 (DeploymentDescSLZ), paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.serializers (validate_desc), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_preset_environ_vars | 113-141 | 4 | db29fc07... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v3 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), paasng.platform.engine.constants (ConfigVarEnvName), paasng.platform.engine.models.preset_envvars (PresetEnvVariable), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_as_env_vars_domain | 157-174 | 5 | 2867c01f... | paasng.platform.bkapp_model.models (get_svc_disc_as_env_variables), paasng.platform.declarative.deployment.svc_disc (BkSaaSEnvVariableFactory), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_as_env_vars_subpath | 176-193 | 5 | 8592a096... | paasng.platform.bkapp_model.models (get_svc_disc_as_env_variables), paasng.platform.declarative.deployment.svc_disc (BkSaaSEnvVariableFactory), tests.utils.mocks.cluster (cluster_ingress_config) |
| test_notset_should_reset | 197-213 | 2 | cbdffa20... | paasng.platform.bkapp_model.models (SvcDiscConfig), paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v3 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_notset_should_skip_when_manager_different | 215-228 | 2 | 21fa2e0a... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities.svc_discovery (SvcDiscEntryBkSaaS), paasng.platform.bkapp_model.entities_syncer.svc_discovery (sync_svc_discovery), paasng.platform.bkapp_model.models (SvcDiscConfig), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_field_not_set | 232-237 | 2 | f2ba6f66... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v3 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_field_set | 239-247 | 1 | 067bb436... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v3 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_not_set_should_not_touch_deployment | 249-268 | 4 | c1d59df8... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v3 (DeploymentDescSLZ), paasng.platform.declarative.models (DeploymentDescription), paasng.platform.declarative.serializers (validate_desc), paasng.platform.modules.constants (DeployHookType), paasng.platform.modules.models.deploy_config (HookList), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_rewrite_the_hook | 270-284 | 1 | dc4480fa... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v3 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), paasng.platform.modules.constants (DeployHookType), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_not_set_should_reset | 286-298 | 2 | 992dd31f... | paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v3 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_not_set_with_different_mgr_should_keep | 300-314 | 2 | 85107da2... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities.hooks (HookCmd, Hooks), paasng.platform.bkapp_model.entities_syncer.hooks (sync_hooks), paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v3 (DeploymentDescSLZ), paasng.platform.declarative.serializers (validate_desc), paasng.platform.modules.constants (DeployHookType), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_notset_should_reset | 337-348 | 2 | 80e74592... | paasng.platform.bkapp_model.models (DomainResolution), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_notset_should_skip_when_manager_different | 350-363 | 2 | 6e70b3b4... | paasng.platform.bkapp_model (fieldmgr), paasng.platform.bkapp_model.entities (DomainResolution), paasng.platform.bkapp_model.entities_syncer.domain_resolution (sync_domain_resolution), paasng.platform.bkapp_model.models (DomainResolution), tests.paasng.platform.declarative.utils (AppDescV3Builder) |
| test_default_app_with_ver_3 | 372-382 | 1 | b83c67a9... | paasng.platform.applications.constants (ApplicationType), paasng.platform.declarative.deployment.controller (DeploymentDeclarativeController), paasng.platform.declarative.deployment.validations.v3 (DeploymentDescSLZ), paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.serializers (validate_desc), pytest (pytest), tests.paasng.platform.declarative.utils (AppDescV3Builder) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/deployment/v3/test_validations.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 38-40 | 0 | 82616b5e... | tests.paasng.platform.declarative.utils (AppDescV3Builder) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/handlers/test_handlers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_ver_1 | 30-39 | 1 | 6ce304c8... | paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.handlers (get_desc_handler), pytest (pytest), textwrap (dedent), yaml (yaml) |
| test_ver_unspecified | 41-50 | 1 | e628e310... | paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.handlers (get_desc_handler), pytest (pytest), textwrap (dedent), yaml (yaml) |
| test_ver_unknown_number | 52-56 | 1 | 23e2d63f... | paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.handlers (get_desc_handler), pytest (pytest), yaml (yaml) |
| test_ver_unknown_string | 58-62 | 1 | 6549d78d... | paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.handlers (get_desc_handler), pytest (pytest), yaml (yaml) |
| test_ver_1 | 66-75 | 1 | f4129ed7... | paasng.platform.declarative.handlers (get_deploy_desc_handler), pytest (pytest), textwrap (dedent), yaml (yaml) |
| test_ver_unspecified | 77-86 | 1 | 6edb8e87... | paasng.platform.declarative.handlers (get_deploy_desc_handler), pytest (pytest), textwrap (dedent), yaml (yaml) |
| test_ver_unknown_number | 88-92 | 1 | 981fcb70... | paasng.platform.declarative.handlers (get_deploy_desc_handler), pytest (pytest), yaml (yaml) |
| test_ver_unknown_string | 94-98 | 1 | b5f98e30... | paasng.platform.declarative.handlers (get_deploy_desc_handler), pytest (pytest), yaml (yaml) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/handlers/v2/test_app.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_app_normal | 48-72 | 4 | b6d6c88c... | base64 (base64), paasng.platform.applications.models (Application), textwrap (dedent) |
| test_app_from_stat | 74-106 | 4 | ece599a5... | paasng.platform.applications.models (Application), paasng.platform.smart_app.services.detector (SourcePackageStatReader), paasng.platform.sourcectl.utils (generate_temp_file), tests.paasng.platform.sourcectl.packages.utils (gen_tar), textwrap (dedent), yaml (yaml) |
| test_integrated | 110-151 | 2 | eec6f62f... | django.conf (settings), django_dynamic_fixture (G), paas_wl.infras.cluster.models (Cluster), paasng.platform.modules.helpers (get_module_clusters), tests.utils.helpers (generate_random_string), textwrap (dedent, indent) |
| test_app_data_to_desc | 154-175 | 5 | 68e89c08... | paasng.platform.applications.constants (AppLanguage), paasng.platform.declarative.constants (AppDescPluginType), textwrap (dedent) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/handlers/v2/test_deployment.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_desc_getter_name | 99-110 | 2 | 9f790a49... | paasng.platform.declarative.handlers (get_deploy_desc_handler), pytest (pytest), yaml (yaml) |
| test_unsupported_version | 112-114 | 1 | 6ed50973... | paasng.platform.declarative.handlers (get_deploy_desc_handler), pytest (pytest), yaml (yaml) |
| test_normal | 125-159 | 4 | b46769c3... | base64 (base64), cattr (cattr), json (json), paasng.platform.bkapp_model.models (get_svc_disc_as_env_variables), paasng.platform.declarative.handlers (get_deploy_desc_handler), paasng.platform.engine.configurations.config_var (get_preset_env_variables), pytest (pytest), unittest (mock), yaml (yaml) |
| test_desc_and_procfile_same | 161-177 | 2 | 79dafede... | paasng.platform.declarative.handlers (get_deploy_desc_handler), textwrap (dedent), yaml (yaml) |
| test_desc_and_procfile_different | 179-196 | 1 | a17bcde0... | paasng.platform.declarative.handlers (get_deploy_desc_handler), textwrap (dedent), yaml (yaml) |
| test_procfile_only | 198-202 | 1 | 76ecaba8... | paasng.platform.declarative.handlers (get_deploy_desc_handler) |
| test_invalid_desc_and_valid_procfile | 204-209 | 1 | 9e61b908... | paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.handlers (get_deploy_desc_handler), pytest (pytest) |
| test_with_modules_found | 211-220 | 0 | 6143ed69... | paasng.platform.declarative.handlers (get_deploy_desc_handler), textwrap (dedent), yaml (yaml) |
| test_with_modules_not_found | 222-232 | 1 | b71e3bb0... | paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.handlers (get_deploy_desc_handler), pytest (pytest), textwrap (dedent), yaml (yaml) |
| test_with_modules_not_found_fallback_to_module | 234-245 | 0 | bc9fa1c3... | paasng.platform.declarative.handlers (get_deploy_desc_handler), textwrap (dedent), yaml (yaml) |
| test_with_module | 247-255 | 0 | c4790b05... | paasng.platform.declarative.handlers (get_deploy_desc_handler), textwrap (dedent), yaml (yaml) |
| test_with_module_and_modules_missing | 257-265 | 1 | aa83ab2d... | paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.handlers (get_deploy_desc_handler), pytest (pytest), textwrap (dedent), yaml (yaml) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/handlers/v2/test_probes.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_process_spec_should_have_probes | 96-102 | 2 | dbea78ff... | paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_probes_changes_after_handling_new_yaml | 104-122 | 3 | a2b41436... | paasng.platform.bkapp_model.models (ModuleProcessSpec) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/handlers/v3/test_app.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_app_normal | 43-71 | 4 | 68981947... | base64 (base64), paasng.platform.applications.models (Application), textwrap (dedent) |
| test_app_from_stat | 73-109 | 4 | 4553820d... | paasng.platform.applications.models (Application), paasng.platform.smart_app.services.detector (SourcePackageStatReader), paasng.platform.sourcectl.utils (generate_temp_file), tests.paasng.platform.sourcectl.packages.utils (gen_tar), textwrap (dedent), yaml (yaml) |
| test_app_data_to_desc | 112-136 | 5 | 230f0bdc... | paasng.platform.applications.constants (AppLanguage), paasng.platform.declarative.constants (AppDescPluginType), textwrap (dedent) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/handlers/v3/test_deployment.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_handle_normal | 76-125 | 7 | 2e02c6c0... | base64 (base64), json (json), paasng.platform.bkapp_model.entities (ProcService), paasng.platform.bkapp_model.models (ModuleProcessSpec, get_svc_disc_as_env_variables), paasng.platform.declarative.handlers (get_deploy_desc_handler), paasng.platform.engine.configurations.config_var (get_preset_env_variables), unittest (mock), yaml (yaml) |
| test_desc_and_procfile_different | 127-136 | 1 | ef4175dd... | paasng.platform.declarative.handlers (get_deploy_desc_handler), unittest (mock), yaml (yaml) |
| test_with_modules_found | 138-152 | 0 | 27946019... | paasng.platform.declarative.handlers (get_deploy_desc_handler), textwrap (dedent), yaml (yaml) |
| test_with_modules_not_found | 154-169 | 1 | 562dfbfe... | paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.handlers (get_deploy_desc_handler), pytest (pytest), textwrap (dedent), yaml (yaml) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/handlers/v3/test_probes.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_process_spec_should_have_probes | 99-105 | 2 | dbea78ff... | paasng.platform.bkapp_model.models (ModuleProcessSpec) |
| test_probes_changes_after_handling_new_yaml | 107-128 | 3 | 7db089aa... | paasng.platform.bkapp_model.models (ModuleProcessSpec), tests.paasng.platform.engine.setup_utils (create_fake_deployment) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/test_protection.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal_app | 29-30 | 0 | 5257ef3d... | paasng.platform.declarative.protections (modifications_not_allowed) |
| test_desc_app | 32-42 | 2 | b941477b... | paasng.core.core.protections.exceptions (ConditionNotMatched), paasng.platform.applications.models (Application), paasng.platform.declarative.handlers (get_desc_handler), paasng.platform.declarative.protections (modifications_not_allowed), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/declarative/test_slzs.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_v2 | 42-93 | 1 | f9494ba1... | paasng.platform.declarative.application.serializers (AppDescriptionSLZ), paasng.platform.declarative.application.validations (v2), tests.paasng.platform.declarative.utils (AppDescV2Builder, AppDescV2Decorator), tests.utils.helpers (generate_random_string) |
| test_v3 | 95-156 | 1 | 35ea6105... | paasng.platform.declarative.application.serializers (AppDescriptionSLZ), paasng.platform.declarative.application.validations (v3), tests.paasng.platform.declarative.utils (AppDescV3Builder, AppDescV3Decorator), tests.utils.helpers (generate_random_string) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/configurations/test_config_var.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_param_include_config_vars | 52-59 | 1 | 6b09fb54... | blue_krill.contextlib (nullcontext), paasng.platform.engine.configurations.config_var (get_env_variables), paasng.platform.engine.models.config_var (ConfigVar), pytest (pytest) |
| test_builtin_id_and_secret | 61-65 | 2 | e4cc2f5a... | paasng.platform.engine.configurations.config_var (get_env_variables) |
| test_wl_vars_exists | 67-71 | 2 | 92e0941b... | paasng.platform.engine.configurations.config_var (get_env_variables) |
| test_part_declarative | 73-126 | 2 | e341c9e3... | blue_krill.contextlib (nullcontext), paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.declarative.handlers (get_deploy_desc_handler), paasng.platform.engine.configurations.config_var (get_env_variables), paasng.platform.engine.models.config_var (ConfigVar), pytest (pytest), textwrap (dedent), yaml (yaml) |
| test_part_saas_services | 128-144 | 1 | eed78af8... | paasng.platform.declarative.handlers (get_deploy_desc_handler), paasng.platform.engine.configurations.config_var (get_env_variables), pytest (pytest), textwrap (dedent), yaml (yaml) |
| test_bk_platform_envs | 149-168 | 5 | ddd77fb8... | django.conf (settings), paasng.platform.engine.configurations.config_var (get_builtin_env_variables), pytest (pytest), tests.utils.helpers (override_region_configs) |
| test_builtin_env_keys | 170-183 | 2 | 416abcec... | django.conf (settings), paasng.platform.engine.configurations.config_var (get_builtin_env_variables), paasng.platform.engine.constants (AppRunTimeBuiltinEnv) |
| test_param_include_custom_builtin_config_vars | 185-191 | 2 | 9cf0ff99... | paasng.platform.engine.configurations.config_var (get_env_variables), paasng.platform.engine.models.config_var (BuiltinConfigVar) |
| test_generate_wl_builtin_env_vars | 194-202 | 5 | 496618a4... | django.conf (settings), paasng.platform.engine.configurations.config_var (_flatten_envs, generate_wl_builtin_env_vars), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/configurations/test_image.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_legacy_custom_image | 43-50 | 1 | 6c3814f2... | paasng.platform.engine.configurations.image (RuntimeImageInfo), paasng.platform.modules.constants (SourceOrigin), unittest (mock) |
| test_buildpack_runtime | 52-68 | 1 | 085a5340... | paasng.platform.engine.configurations.image (RuntimeImageInfo, get_image_repository_template), paasng.platform.engine.constants (RuntimeType), paasng.platform.modules.constants (SourceOrigin), pytest (pytest), unittest (mock) |
| test_dockerfile_runtime | 70-79 | 1 | c0bec24c... | paasng.platform.engine.configurations.image (RuntimeImageInfo, generate_image_repository), paasng.platform.engine.constants (RuntimeType), paasng.platform.modules.constants (SourceOrigin) |
| test_cnative | 81-99 | 1 | b6255242... | paasng.platform.engine.configurations.image (RuntimeImageInfo), paasng.platform.modules.constants (SourceOrigin), paasng.platform.modules.models (BuildConfig), pytest (pytest) |
| test_type | 101-110 | 1 | 529cda43... | paasng.platform.engine.configurations.image (RuntimeImageInfo), paasng.platform.modules.constants (SourceOrigin), pytest (pytest) |
| test_normal | 114-127 | 0 | f4419f52... | paas_wl.bk_app.applications.models (Build), paasng.platform.engine.configurations.image (update_image_runtime_config), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/configurations/test_ingress.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_as_env | 78-104 | 1 | e69cde92... | paasng.platform.engine.configurations.ingress (AppDefaultSubpaths), pytest (pytest) |
| test_get_env_variables | 106-128 | 1 | 4b600b4a... | paasng.platform.engine.configurations.config_var (get_env_variables), pytest (pytest) |
| test_sync | 130-134 | 1 | 5d26f01c... | paasng.platform.engine.configurations.ingress (AppDefaultSubpaths), pytest (pytest), unittest (mock) |
| test_sync | 138-142 | 1 | dc42d3a4... | paasng.platform.engine.configurations.ingress (AppDefaultDomains), pytest (pytest), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/configurations/test_provider.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_providers | 25-36 | 1 | 71eb0338... | paasng.platform.engine.configurations.provider (EnvVariablesProviders) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/controller/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_find_subdomain_domain | 23-33 | 3 | b373e22e... | cattr (cattr), paas_wl.infras.cluster.models (IngressConfig) |
| test_find_subpath_domain | 36-46 | 3 | 9a638ab4... | cattr (cattr), paas_wl.infras.cluster.models (IngressConfig) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/deploy/bg_build/test_executors.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_and_bind_build_instance | 40-47 | 3 | 47c48545... | paasng.platform.engine.constants (BuildStatus), paasng.platform.engine.deploy.bg_build.executors (DefaultBuildProcessExecutor), paasng.platform.engine.handlers (attach_all_phases), paasng.platform.engine.utils.output (NullStream) |
| test_execute | 49-60 | 1 | 23de46df... | paasng.platform.engine.constants (BuildStatus), paasng.platform.engine.deploy.bg_build.executors (DefaultBuildProcessExecutor), paasng.platform.engine.handlers (attach_all_phases), paasng.platform.engine.utils.output (NullStream), unittest (mock) |
| test_execute | 107-122 | 1 | bbbbca4f... | paasng.platform.engine.constants (BuildStatus), paasng.platform.engine.deploy.bg_build.executors (PipelineBuildProcessExecutor), paasng.platform.engine.handlers (attach_all_phases), paasng.platform.engine.utils.output (NullStream), unittest (mock) |
| test_build_env_vars_params | 124-133 | 2 | 731775f4... | base64 (base64), json (json), paasng.platform.engine.deploy.bg_build.executors (PipelineBuildProcessExecutor), paasng.platform.engine.handlers (attach_all_phases), paasng.platform.engine.utils.output (NullStream) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/deploy/bg_build/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_generate_env_vars_without_metadata | 39-51 | 5 | 217c46a4... | django.conf (settings), paasng.platform.engine.deploy.bg_build.utils (generate_builder_env_vars, generate_slug_path, get_envs_from_pypi_url) |
| test_update_env_vars_with_metadata | 53-64 | 2 | a2bd28bd... | paasng.platform.engine.deploy.bg_build.utils (update_env_vars_with_metadata), typing (Dict) |
| test_generate_slug_path | 68-70 | 1 | 2346bc46... | paasng.platform.engine.deploy.bg_build.utils (generate_slug_path) |
| test_prepare_slugbuilder_template_without_metadata | 73-95 | 7 | c712e39e... | django.conf (settings), paasng.platform.engine.deploy.bg_build.utils (generate_builder_env_vars, prepare_slugbuilder_template), types (SimpleNamespace), unittest (mock) |
| test_get_envs_from_pypi_url | 98-101 | 2 | 13eceea2... | paasng.platform.engine.deploy.bg_build.utils (get_envs_from_pypi_url) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/deploy/test_bkapp_hook.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_start | 39-58 | 1 | 569203fb... | paas_wl.utils.constants (PodPhase), paasng.platform.engine.deploy.bg_command.bkapp_hook (PreReleaseDummyExecutor), paasng.platform.engine.handlers (attach_all_phases), paasng.platform.engine.utils.output (Style), tests.utils.helpers (generate_random_string), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/deploy/test_building.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_failed_when_parsing_processes | 51-72 | 6 | c37dd01f... | paasng.platform.engine.constants (JobStatus), paasng.platform.engine.handlers (attach_all_phases), paasng.platform.engine.models (Deployment), paasng.platform.sourcectl.exceptions (GetProcfileError), unittest (mock) |
| test_failed_when_upload_source | 74-96 | 6 | f535455f... | paasng.platform.engine.constants (JobStatus), paasng.platform.engine.handlers (attach_all_phases), paasng.platform.engine.models (Deployment), unittest (mock) |
| test_start_normal | 98-138 | 9 | b16bdc2f... | paasng.platform.engine.constants (JobStatus), paasng.platform.engine.handlers (attach_all_phases), paasng.platform.engine.models (Deployment), unittest (mock), uuid (uuid) |
| test_start_build | 157-198 | 9 | 602ada0c... | paasng.platform.declarative.handlers (get_deploy_desc_handler), paasng.platform.engine.constants (JobStatus), paasng.platform.engine.handlers (attach_all_phases), paasng.platform.engine.models (Deployment), unittest (mock), uuid (uuid) |
| test_failed | 216-228 | 1 | d8e667eb... | blue_krill.async_utils.poll_task (CallbackResult, CallbackStatus), paasng.platform.engine.constants (JobStatus), paasng.platform.engine.deploy.building (BuildProcessResultHandler), pytest (pytest), tests.utils.mocks.poll_task (FakeTaskPoller) |
| test_succeeded | 230-241 | 2 | 9935e6dd... | blue_krill.async_utils.poll_task (CallbackResult, CallbackStatus), paasng.platform.engine.constants (JobStatus), paasng.platform.engine.deploy.building (BuildProcessResultHandler), tests.utils.mocks.poll_task (FakeTaskPoller), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/deploy/test_image_release.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_for_last_build | 61-68 | 2 | 56a5f45f... | paasng.platform.engine.deploy.image_release (ImageReleaseMgr), paasng.platform.engine.models.deployment (Deployment, ProcessTmpl) |
| test_for_smart_app | 70-84 | 1 | f8f42089... | paas_wl.bk_app.applications.models (Build), paasng.platform.applications.models (Application), paasng.platform.declarative.constants (AppSpecVersion), paasng.platform.declarative.entities (DeployHandleResult), paasng.platform.engine.deploy.image_release (ImageReleaseMgr), paasng.platform.engine.models.deployment (Deployment), pytest (pytest), unittest (mock) |
| test_for_image_app | 86-94 | 2 | 3fadc60f... | django_dynamic_fixture (G), paas_wl.bk_app.applications.models (Build), paasng.platform.bkapp_model.models (ModuleProcessSpec), paasng.platform.engine.deploy.image_release (ImageReleaseMgr), paasng.platform.engine.models.deployment (Deployment), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/deploy/test_interruptions.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_build_process_id | 32-47 | 1 | ea43e1f5... | paasng.platform.engine.deploy.interruptions (interrupt_deployment), pytest (pytest), tests.paasng.platform.engine.setup_utils (create_fake_deployment), unittest (mock), uuid (uuid) |
| test_failed_incorrect_user | 49-53 | 1 | 44e35661... | paasng.platform.engine.deploy.interruptions (interrupt_deployment), paasng.platform.engine.exceptions (DeployInterruptionFailed), pytest (pytest), tests.paasng.platform.engine.setup_utils (create_fake_deployment), tests.utils.auth (create_user) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/deploy/test_pre_release.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_hook_not_found | 54-77 | 5 | ed42d253... | paasng.platform.engine.deploy.bg_command.pre_release (ApplicationPreReleaseExecutor), paasng.platform.engine.handlers (attach_all_phases), paasng.platform.engine.utils.output (Style), paasng.platform.modules.constants (DeployHookType), paasng.platform.modules.models.deploy_config (Hook), pytest (pytest), tests.paasng.platform.engine.setup_utils (create_fake_deployment), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/deploy/test_release.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_failed_when_create_release | 47-65 | 4 | 86847b72... | paasng.platform.engine.constants (JobStatus), paasng.platform.engine.deploy.release.legacy (ApplicationReleaseMgr), paasng.platform.engine.models (Deployment), unittest (mock) |
| test_start_normal | 67-105 | 5 | d4ad0525... | paasng.platform.engine.constants (JobStatus), paasng.platform.engine.deploy.release.legacy (ApplicationReleaseMgr), paasng.platform.engine.models (Deployment), paasng.platform.engine.models.deployment (ProcessTmpl), unittest (mock), uuid (uuid) |
| test_failed | 115-160 | 2 | efb2d015... | blue_krill.async_utils.poll_task (CallbackResult, CallbackStatus), paasng.platform.engine.constants (ReleaseStatus), paasng.platform.engine.deploy.release.legacy (ReleaseResultHandler), pytest (pytest), tests.utils.mocks.poll_task (FakeTaskPoller), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/models/test_offline.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_set_failed | 26-29 | 1 | e562e813... | paasng.platform.engine.models.offline (OfflineOperation) |
| test_set_successful | 31-34 | 1 | c7a0a20d... | paasng.platform.engine.models.offline (OfflineOperation) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/phases_steps/test_phases.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_or_create | 32-38 | 2 | dee7f943... | paasng.platform.engine.models (DeployPhaseTypes) |
| test_attach | 40-50 | 2 | 3a24f4eb... | paasng.platform.engine.exceptions (NoUnlinkedDeployPhaseError), paasng.platform.engine.models (DeployPhaseTypes), pytest (pytest), tests.paasng.platform.engine.setup_utils (create_fake_deployment) |
| test_get_unattached | 52-56 | 1 | 9d948317... | paasng.platform.engine.models (DeployPhaseTypes) |
| test_rebuild_steps | 58-59 | 0 | 3e9b7652... |  |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/phases_steps/test_steps.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_pick | 69-128 | 1 | ddc491f5... | paasng.platform.engine.models (Deployment), paasng.platform.engine.phases_steps.steps (DeployStepPicker), paasng.platform.modules.models (AppSlugBuilder, AppSlugRunner), pytest (pytest) |
| test_pick_no_runtime | 130-133 | 2 | 51d5fa44... | paasng.platform.engine.phases_steps.steps (DeployStepPicker) |
| test_match_and_update | 161-253 | 1 | 37e96ec3... | paasng.platform.engine.constants (JobStatus), paasng.platform.engine.models (DeployPhaseTypes), paasng.platform.engine.phases_steps.steps (update_step_by_line), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/processes/test_events.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_process_added | 29-41 | 5 | b73a9250... | paas_wl.bk_app.processes.processes (PlainProcess), paasng.platform.engine.processes.events (ProcEventsProducer, ProcInstEventType, ProcessEventType), typing (List) |
| test_process_removed | 43-55 | 5 | 5880fe6f... | paas_wl.bk_app.processes.processes (PlainProcess), paasng.platform.engine.processes.events (ProcEventsProducer, ProcInstEventType, ProcessEventType), typing (List) |
| test_process_updated_replicas | 57-66 | 2 | 336e77e7... | copy (copy), paasng.platform.engine.processes.events (ProcEventsProducer, ProcessEventType) |
| test_process_updated_command | 68-78 | 3 | e2edd035... | copy (copy), paasng.platform.engine.processes.events (ProcEventsProducer, ProcessEventType) |
| test_proc_updated_instances_added | 80-92 | 3 | 374d2a4d... | copy (copy), paasng.platform.engine.processes.events (ProcEventsProducer, ProcInstEventType) |
| test_proc_updated_instances_removed | 94-104 | 3 | da26ed8c... | copy (copy), paasng.platform.engine.processes.events (ProcEventsProducer, ProcInstEventType) |
| test_proc_updated_instances_updated_restarted | 106-116 | 3 | f6eedfae... | copy (copy), paasng.platform.engine.processes.events (ProcEventsProducer, ProcInstEventType) |
| test_proc_updated_instances_updated_ready | 118-128 | 3 | f129ef21... | copy (copy), paasng.platform.engine.processes.events (ProcEventsProducer, ProcInstEventType) |
| test_proc_updated_instances_updated_not_ready | 130-140 | 3 | 876220d1... | copy (copy), paasng.platform.engine.processes.events (ProcEventsProducer, ProcInstEventType) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/processes/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_save_then_get | 41-44 | 1 | 0f09bd10... | paasng.platform.engine.processes.utils (ProcessesSnapshotStore) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/processes/test_wait.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_evaluate | 66-82 | 1 | 9a2896e5... | paasng.platform.engine.deploy.bg_wait.wait_deployment (DynamicReadyTimeoutPolicy), pytest (pytest) |
| test_still_running | 86-91 | 1 | 23644467... | blue_krill.async_utils.poll_task (PollingStatus), paasng.platform.engine.deploy.bg_wait.wait_deployment (WaitForAllStopped) |
| test_all_stopped | 93-99 | 1 | a46e9981... | blue_krill.async_utils.poll_task (PollingStatus), paasng.platform.engine.deploy.bg_wait.wait_deployment (WaitForAllStopped) |
| test_broadcast | 101-127 | 2 | 14a913f8... | copy (copy), django.dispatch (receiver), paasng.platform.engine.deploy.bg_wait.wait_deployment (WaitForAllStopped), paasng.platform.engine.signals (processes_updated), pytest (pytest) |
| test_not_ready | 131-136 | 1 | 98a55864... | blue_krill.async_utils.poll_task (PollingStatus), paasng.platform.engine.deploy.bg_wait.wait_deployment (WaitForReleaseAllReady) |
| test_ready | 138-146 | 1 | 074b1860... | blue_krill.async_utils.poll_task (PollingStatus), paasng.platform.engine.deploy.bg_wait.wait_deployment (WaitForReleaseAllReady) |
| test_aborted_by_dynamic_timeout | 148-156 | 3 | 0bb6044b... | blue_krill.async_utils.poll_task (PollingMetadata, PollingStatus), paasng.platform.engine.deploy.bg_wait.wait_deployment (WaitForReleaseAllReady) |
| test_evaluate | 160-172 | 1 | f6d3f111... | paasng.platform.engine.deploy.bg_wait.wait_deployment (TooManyRestartsPolicy), pytest (pytest) |
| test_no_deployment_id | 176-178 | 1 | a938e96d... | paasng.platform.engine.deploy.bg_wait.wait_deployment (UserInterruptedPolicy) |
| test_wrong_deployment_id | 180-182 | 1 | 547b0368... | paasng.platform.engine.deploy.bg_wait.wait_deployment (UserInterruptedPolicy), uuid (uuid) |
| test_int_requested | 184-188 | 1 | 41a07a7f... | datetime (datetime), paasng.platform.engine.deploy.bg_wait.wait_deployment (UserInterruptedPolicy) |
| test_truth_value | 192-198 | 1 | 4b14ed6e... | paasng.platform.engine.deploy.bg_wait.base (AbortedDetails, AbortedDetailsPolicy) |
| test_falsehood_value | 200-202 | 1 | 60f86187... | paasng.platform.engine.deploy.bg_wait.base (AbortedDetails) |
| test_invalid_value | 204-206 | 1 | bc609e3c... | paasng.platform.engine.deploy.bg_wait.base (AbortedDetails), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/test_config_var.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_config_vars_normal | 67-73 | 1 | 588c1b77... | paasng.platform.engine.models.config_var (get_config_vars) |
| test_get_config_vars_conflict_name | 75-87 | 2 | 4706d825... | paasng.platform.engine.models.config_var (get_config_vars) |
| test_invalid_env_name | 89-91 | 1 | 814e2355... | paasng.platform.engine.models.config_var (get_config_vars), pytest (pytest) |
| test_empty | 93-94 | 1 | 9c684035... | paasng.platform.engine.models.config_var (get_config_vars) |
| test_global | 100-116 | 2 | 56af0cde... | paasng.platform.engine.constants (ConfigVarEnvName), paasng.platform.engine.models.config_var (ConfigVar, ENVIRONMENT_NAME_FOR_GLOBAL), pytest (pytest), typing (List) |
| test_clone | 145-201 | 2 | 0138963d... | paasng.platform.engine.models.config_var (get_config_vars), paasng.platform.engine.models.managers (ConfigVarManager), pytest (pytest) |
| test_apply_vars_to_module | 203-236 | 3 | ba1c47c5... | django.utils.crypto (get_random_string), paasng.platform.engine.models.managers (ConfigVarManager), paasng.platform.engine.serializers (ConfigVarFormatSLZ), pytest (pytest) |
| test_export_config_vars | 238-288 | 1 | 98c091e1... | paasng.platform.engine.models.managers (ExportedConfigVars, PlainConfigVar), pytest (pytest) |
| test_batch_save | 290-344 | 2 | 8ce4289a... | django.forms.models (model_to_dict), paasng.platform.engine.models.config_var (CONFIG_VAR_INPUT_FIELDS), paasng.platform.engine.models.managers (ConfigVarManager), paasng.platform.engine.serializers (ConfigVarFormatWithIdSLZ), pytest (pytest) |
| test_remove_bulk | 346-354 | 4 | fb787f1f... | paasng.platform.engine.models.managers (ConfigVarManager) |
| test_key_error | 358-367 | 1 | d5505226... | paasng.platform.engine.serializers (ConfigVarFormatSLZ), pytest (pytest), rest_framework.exceptions (ValidationError) |
| test_to_file_content | 371-427 | 1 | 83aedd5b... | paasng.platform.engine.models.managers (ExportedConfigVars, PlainConfigVar), pytest (pytest), textwrap (dedent) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/test_deployment.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_source_code | 33-42 | 1 | 328f8150... | django_dynamic_fixture (G), paasng.platform.engine.models (Deployment), paasng.platform.sourcectl.models (VersionInfo) |
| test_s_mart | 44-56 | 1 | 2908e19a... | django_dynamic_fixture (G), paasng.platform.engine.models (Deployment), paasng.platform.modules.constants (SourceOrigin), paasng.platform.sourcectl.models (VersionInfo) |
| test_image | 58-80 | 1 | 2ec2c027... | django_dynamic_fixture (G), paasng.platform.engine.models (Deployment), paasng.platform.sourcectl.models (VersionInfo), uuid (uuid) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/test_handlers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_update_last_deployed_date | 28-41 | 2 | 43e37bce... | paasng.platform.engine.signals (post_appenv_deploy), setup_utils (create_fake_deployment) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/test_logs.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_make_channel_stream | 24-32 | 4 | 0d817dd9... | paasng.platform.engine.logs (make_channel_stream), pytest (pytest) |
| test_main_stream_obj | 36-45 | 3 | 6f506038... | paasng.platform.engine.logs (DeploymentLogStreams) |
| test_preparation_stream_obj | 47-53 | 2 | 5082fd9e... | paasng.platform.engine.logs (DeploymentLogStreams) |
| test_get_all_logs | 56-58 | 1 | 22dc9d4e... | paasng.platform.engine.logs (get_all_logs) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/test_managers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal_pending_exist | 28-35 | 2 | 5a4158ef... | paasng.platform.engine.models.deployment (Deployment), paasng.platform.engine.models.managers (DeployOperationManager), paasng.platform.engine.models.offline (OfflineOperation) |
| test_both_pending_exist | 37-42 | 1 | 6489d25c... | paasng.platform.engine.models.deployment (Deployment), paasng.platform.engine.models.managers (DeployOperationManager), paasng.platform.engine.models.offline (OfflineOperation) |
| test_none_pending_exist | 44-46 | 1 | 9765c45d... | paasng.platform.engine.models.managers (DeployOperationManager) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/test_monitoring.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_no_build_process_id | 46-49 | 1 | 417c2e5f... | paasng.platform.engine.monitoring (count_frozen_deployments) |
| test_different_log_lines | 51-79 | 1 | 992c9156... | paas_wl.bk_app.applications.models.misc (OutputStream, OutputStreamLine), paasng.platform.engine.monitoring (count_frozen_deployments), pytest (pytest), unittest (mock) |
| test_now_not_provided | 81-84 | 1 | 4a83ea1d... | arrow (arrow), paasng.platform.engine.monitoring (count_frozen_deployments) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/test_phases.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_mark | 44-55 | 6 | 8aaeaff6... | paasng.platform.engine.constants (JobStatus), pytest (pytest) |
| test_attach | 57-62 | 3 | 7d55e8ff... | paasng.platform.engine.models (DeployPhaseTypes) |
| test_mark_and_write_to_stream | 64-77 | 3 | e32d7352... | paasng.platform.engine.constants (JobStatus), pytest (pytest), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/test_serializers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_input | 37-57 | 1 | 18e1b666... | paasng.platform.engine (serializers), pytest (pytest), rest_framework.serializers (ValidationError) |
| test_output | 59-65 | 1 | 9c0c9c01... | paasng.platform.engine (serializers), pytest (pytest) |
| test_normal | 77-114 | 1 | 39fd745e... | django.core.files.base (ContentFile), paasng.platform.engine (serializers), pytest (pytest), rest_framework.serializers (ValidationError), yaml (yaml) |
| test_with_conment | 116-155 | 1 | f4e13d41... | django.core.files.base (ContentFile), paasng.platform.engine (serializers), paasng.platform.engine.models.config_var (ConfigVar), textwrap (dedent) |
| test_error | 157-178 | 1 | 8d6540d6... | blue_krill.web.std_error (APIError), django.core.files.base (ContentFile), paasng.platform.engine (serializers), pytest (pytest), textwrap (dedent) |
| test_key_error | 180-196 | 1 | ec51d418... | django.core.files.base (ContentFile), paasng.platform.engine (serializers), pytest (pytest), rest_framework.serializers (ValidationError), textwrap (dedent) |
| test_normal | 209-222 | 1 | f3f0ae5a... | paasng.platform.engine (serializers), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/utils/test_output.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_sanitize_message_removing | 27-31 | 1 | b0d892d9... | paasng.platform.engine.utils.output (sanitize_message) |
| test_sanitize_message_truncating | 34-36 | 1 | 4bd9c7f3... | paasng.platform.engine.utils.output (sanitize_message) |
| test_console_stream_stdout | 40-47 | 1 | fc0719fb... | paasng.platform.engine.utils.output (ConsoleStream), unittest (mock) |
| test_console_stream_stderr | 49-56 | 1 | dd498cbf... | paasng.platform.engine.utils.output (ConsoleStream), unittest (mock) |
| test_write_message | 60-68 | 2 | 72250624... | paasng.platform.engine.utils.output (RedisWithModelStream), unittest (mock) |
| test_write_title | 70-72 | 1 | 22f22e6a... | paasng.platform.engine.utils.output (RedisWithModelStream), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/utils/test_source.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_for_svn | 58-74 | 1 | dd8ff450... | paasng.platform.engine.models (Deployment), paasng.platform.engine.utils.source (get_source_package_path) |
| test_for_git | 76-92 | 1 | e07f68b1... | paasng.platform.engine.models (Deployment), paasng.platform.engine.utils.source (get_source_package_path) |
| test_no_patch_performed_if_process_empty | 120-126 | 1 | a2001258... | paasng.platform.engine.utils.source (download_source_to_dir), paasng.platform.modules.constants (SourceOrigin), paasng.platform.sourcectl.utils (generate_temp_dir) |
| test_add_procfile | 128-158 | 3 | b810de0b... | paasng.platform.engine.utils.source (download_source_to_dir), paasng.platform.modules.constants (SourceOrigin), paasng.platform.sourcectl.utils (generate_temp_dir), pytest (pytest), yaml (yaml) |
| test_normal | 164-172 | 1 | d679d6cb... | django.test.utils (override_settings), paasng.platform.engine.utils.output (ConsoleStream), paasng.platform.engine.utils.source (check_source_package), paasng.platform.sourcectl.utils (generate_temp_file), pathlib (pathlib) |
| test_big_package | 174-182 | 1 | f421e205... | django.test.utils (override_settings), paasng.platform.engine.utils.output (ConsoleStream), paasng.platform.engine.utils.source (check_source_package), paasng.platform.sourcectl.utils (generate_temp_file), pathlib (pathlib) |
| test_s_mart_desc_found | 189-199 | 1 | 757b0541... | paasng.platform.engine.utils.source (get_source_dir), paasng.platform.modules.constants (SourceOrigin), unittest (mock) |
| test_s_mart_desc_not_found | 201-211 | 1 | ac62c935... | paasng.platform.engine.utils.source (get_source_dir), paasng.platform.modules.constants (SourceOrigin), paasng.platform.sourcectl.exceptions (GetAppYamlError), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/workflow/test_flow.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 42-50 | 2 | d31d3c0a... | paasng.platform.engine.utils.output (ConsoleStream), paasng.platform.engine.workflow.flow (DeployProcedure), unittest (mock) |
| test_with_expected_error | 52-63 | 2 | 4e3e3e7d... | paasng.platform.engine.exceptions (DeployShouldAbortError), paasng.platform.engine.utils.output (ConsoleStream), paasng.platform.engine.workflow.flow (DeployProcedure), unittest (mock) |
| test_with_unexpected_error | 65-77 | 2 | 0d28c16f... | paasng.platform.engine.utils.output (ConsoleStream), paasng.platform.engine.workflow.flow (DeployProcedure), unittest (mock) |
| test_with_deployment | 79-93 | 3 | 6d41afea... | paasng.platform.engine.utils.output (ConsoleStream), paasng.platform.engine.workflow.flow (DeployProcedure), unittest (mock) |
| test_normal | 97-106 | 3 | 4cf0f7f4... | paasng.platform.engine.workflow.flow (DeploymentCoordinator) |
| test_lock_timeout | 108-116 | 3 | cd00575e... | paasng.platform.engine.workflow.flow (DeploymentCoordinator), time (time) |
| test_release_without_deployment | 118-127 | 2 | 7744e67e... | paasng.platform.engine.workflow.flow (DeploymentCoordinator) |
| test_release_with_deployment | 129-136 | 1 | 07a68d6f... | paasng.platform.engine.workflow.flow (DeploymentCoordinator) |
| test_release_with_wrong_deployment | 138-148 | 2 | 9a61ce87... | paasng.platform.engine.workflow.flow (DeploymentCoordinator), pytest (pytest), tests.paasng.platform.engine.setup_utils (create_fake_deployment) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/workflow/test_messaging.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_from_raw_normal | 26-35 | 4 | 0b57487c... | paasng.platform.engine.workflow.messaging (ServerSendEvent), pytest (pytest) |
| test_from_raw_message | 37-48 | 4 | 98d8f7d5... | paasng.platform.engine.workflow.messaging (ServerSendEvent), pytest (pytest) |
| test_from_raw_internal | 50-54 | 1 | 881d032f... | paasng.platform.engine.workflow.messaging (ServerSendEvent), pytest (pytest) |
| test_to_yield_str_list | 56-59 | 1 | 3fb48e95... | paasng.platform.engine.workflow.messaging (ServerSendEvent), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/engine/workflow/test_protections.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_validate | 57-74 | 2 | ddce45af... | django_dynamic_fixture (G), paasng.accessories.publish.market.models (Product), paasng.core.core.protections.exceptions (ConditionNotMatched), paasng.platform.engine.constants (DeployConditions), paasng.platform.engine.workflow.protections (ProductInfoCondition), pytest (pytest) |
| test_validate | 78-96 | 2 | af8ea593... | django_dynamic_fixture (G), paasng.bk_plugins.bk_plugins.models (BkPluginTag), paasng.core.core.protections.exceptions (ConditionNotMatched), paasng.platform.engine.constants (DeployConditions), paasng.platform.engine.workflow.protections (PluginTagValidationCondition), pytest (pytest) |
| test_validate | 100-133 | 2 | 5f601ab6... | paasng.core.core.protections.exceptions (ConditionNotMatched), paasng.infras.iam.helpers (add_role_members, remove_user_all_roles), paasng.platform.applications.constants (ApplicationRole), paasng.platform.engine.workflow.protections (EnvProtectionCondition, ModuleEnvDeployInspector), paasng.platform.environments.constants (EnvRoleOperation), paasng.platform.environments.models (EnvRoleProtection), pytest (pytest) |
| test_validate | 137-171 | 4 | a9f8c5fb... | django_dynamic_fixture (G), paasng.core.core.protections.exceptions (ConditionNotMatched), paasng.infras.accounts.models (Oauth2TokenHolder, UserProfile), paasng.platform.engine.constants (DeployConditions), paasng.platform.engine.workflow.protections (ModuleEnvDeployInspector, RepoAccessCondition), paasng.platform.sourcectl.source_types (get_sourcectl_names), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/environments/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_protection | 30-55 | 1 | a4d8b210... | paasng.platform.applications.constants (ApplicationRole), paasng.platform.environments.constants (EnvRoleOperation), paasng.platform.environments.exceptions (RoleNotAllowError), paasng.platform.environments.models (EnvRoleProtection), paasng.platform.environments.utils (env_role_protection_check), pytest (pytest) |
| test_batch_save_protections | 57-79 | 1 | 10499276... | paasng.platform.applications.constants (ApplicationRole), paasng.platform.environments.constants (EnvRoleOperation), paasng.platform.environments.models (EnvRoleProtection), paasng.platform.environments.utils (batch_save_protections), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/mgrlegacy/cnative/test_migrate.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_migrate_and_rollback | 41-67 | 8 | 7a689ae8... | conftest (CNATIVE_CLUSTER_NAME), paasng.platform.applications.constants (ApplicationType), paasng.platform.mgrlegacy.migrate (migrate_default_to_cnative, rollback_cnative_to_default), paasng.platform.mgrlegacy.task_data (MIGRATE_TO_CNATIVE_CLASSES_LIST), paasng.platform.modules.models (BuildConfig), pytest (pytest) |
| test_migrate_failed | 69-90 | 5 | 65e737f0... | paasng.platform.applications.constants (ApplicationType), paasng.platform.mgrlegacy.cnative_migrations.build_config (BuildConfigMigrator), paasng.platform.mgrlegacy.migrate (migrate_default_to_cnative), tests.conftest (CLUSTER_NAME_FOR_TESTING), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/mgrlegacy/cnative/test_migrators.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_migrate_and_rollback | 41-48 | 3 | 17a24fa7... | django.core.exceptions (ObjectDoesNotExist), paasng.platform.mgrlegacy.cnative_migrations.wl_app (WlAppBackupManager, WlAppBackupMigrator), paasng.platform.mgrlegacy.models (WlAppBackupRel), pytest (pytest) |
| test_migrate_and_rollback | 52-59 | 4 | 90207e7d... | paasng.platform.applications.constants (ApplicationType), paasng.platform.mgrlegacy.cnative_migrations.application (ApplicationTypeMigrator) |
| test_migrate_and_rollback | 69-74 | 2 | 615f9eb9... | conftest (CNATIVE_CLUSTER_NAME), paasng.platform.mgrlegacy.cnative_migrations.cluster (ApplicationClusterMigrator), tests.conftest (CLUSTER_NAME_FOR_TESTING) |
| test_migrate_and_rollback | 103-136 | 12 | 3a76f711... | paasng.platform.engine.constants (RuntimeType), paasng.platform.mgrlegacy.cnative_migrations.build_config (BuildConfigMigrator), paasng.platform.modules.constants (SourceOrigin), paasng.platform.modules.models (BuildConfig), paasng.platform.modules.models.module (Module) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/mgrlegacy/cnative/test_wl_app_backup.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_backup_manager | 26-36 | 6 | c5a0a5e1... | paasng.platform.mgrlegacy.cnative_migrations.wl_app (WlAppBackupManager), paasng.platform.mgrlegacy.models (WlAppBackupRel) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/mgrlegacy/test_envvar_migration.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_migrate | 41-83 | 2 | 89b58303... | paasng.infras.legacydb.entities (EnvItem), paasng.platform.engine.models.config_var (ConfigVar, ENVIRONMENT_ID_FOR_GLOBAL) |
| test_rollback | 85-89 | 1 | c91ec295... | paasng.platform.engine.models.config_var (ConfigVar) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/mgrlegacy/test_migration.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_set_log | 90-98 | 2 | 32d2233b... |  |
| test_update_ongoing | 100-106 | 2 | 978fe24a... |  |
| test_add_log | 108-115 | 3 | 06d5127a... |  |
| test_migrate_success | 117-120 | 1 | 5323cebe... |  |
| test_migrate_exception | 122-128 | 3 | ffd54b46... | paasng.platform.mgrlegacy.exceptions (MigrationFailed), pytest (pytest), tests.utils (mock) |
| test_rollback_success | 130-135 | 3 | 8ebfb39e... |  |
| test_rollback_exception | 137-144 | 4 | 886ccf57... | tests.utils (mock) |
| test_migrate | 150-157 | 3 | f538d919... |  |
| test_rollback | 159-164 | 3 | e46cadec... |  |
| test_migrate | 171-188 | 7 | 1829de7c... | django.core.exceptions (ObjectDoesNotExist), paasng.infras.iam.helpers (fetch_application_members), paasng.platform.modules.manager (ModuleInitializer), pytest (pytest), tests.paasng.platform.mgrlegacy.utils (global_mock) |
| test_rollback | 190-197 | 4 | d1fd192b... | paasng.infras.iam.helpers (fetch_application_members) |
| test_migrate | 204-211 | 3 | 8a1fbef9... |  |
| test_rollback | 213-219 | 2 | 09782385... | paasng.platform.sourcectl.models (SvnRepository) |
| test_migrate | 226-237 | 4 | bc14e843... | django.conf (settings), paasng.accessories.publish.market.models (DisplayOptions, Product) |
| test_migrate_when_released_to_market | 239-256 | 3 | 44e8e769... | paasng.accessories.publish.market.models (MarketConfig), pytest (pytest), tests.paasng.platform.mgrlegacy.utils (get_legacy_app) |
| test_migrate_before_release_to_market | 258-271 | 3 | 44308fe0... | paasng.accessories.publish.market.models (MarketConfig), pytest (pytest), tests.paasng.platform.mgrlegacy.utils (get_legacy_app) |
| test_rollback | 273-277 | 2 | 4f6b8d71... | paasng.accessories.publish.market.models (DisplayOptions, Product) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/mgrlegacy/test_service_migration.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_service | 68-69 | 1 | e7bb18b3... | paasng.platform.mgrlegacy.app_migrations.service (BaseServiceMigration) |
| test_bind_service_to_default_module | 85-91 | 3 | 78445ee2... | paasng.accessories.servicehub.models (RemoteServiceEngineAppAttachment, RemoteServiceModuleAttachment), paasng.platform.mgrlegacy.app_migrations.service (BaseRemoteServiceMigration) |
| test_bind_default_plan_as_fallback | 93-104 | 2 | d60f02da... | paasng.accessories.servicehub.models (RemoteServiceEngineAppAttachment), paasng.platform.engine.constants (AppEnvName), paasng.platform.mgrlegacy.app_migrations.service (BaseRemoteServiceMigration), uuid (uuid) |
| test_get_engine_app_attachment | 106-112 | 1 | be8197c8... | paasng.platform.engine.constants (AppEnvName), paasng.platform.mgrlegacy.app_migrations.service (BaseRemoteServiceMigration), uuid (uuid) |
| test_rollback_service_instance | 114-133 | 3 | 7696d2d9... | paasng.accessories.servicehub.models (RemoteServiceEngineAppAttachment, RemoteServiceModuleAttachment), paasng.platform.engine.constants (AppEnvName), paasng.platform.mgrlegacy.app_migrations.service (BaseRemoteServiceMigration), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/modules/test_deploy_config.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_add_hook | 35-40 | 4 | b6272784... | paasng.platform.modules.constants (DeployHookType) |
| test_disable_hook | 42-49 | 4 | 6bb16cfa... | paasng.platform.modules.constants (DeployHookType) |
| test_upsert | 51-58 | 4 | 60d6022c... | paasng.platform.modules.constants (DeployHookType), tests.utils.helpers (generate_random_string) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/modules/test_helpers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_bind_image | 35-69 | 7 | dd1d38c2... | paasng.platform.modules.exceptions (BindError), paasng.platform.modules.helpers (ModuleRuntimeBinder, ModuleRuntimeManager), pytest (pytest), tests.utils.helpers (generate_random_string) |
| test_bind_buildpack | 72-121 | 8 | dc9b96ba... | paasng.platform.modules.exceptions (BindError), paasng.platform.modules.helpers (ModuleRuntimeBinder, ModuleRuntimeManager), pytest (pytest), tests.utils.helpers (generate_random_string) |
| test_get_module_clusters | 124-125 | 1 | fb7230ed... | paasng.platform.modules.helpers (get_module_clusters) |
| test_get_module_clusters_engineless | 128-130 | 1 | 94fa6a8f... | paasng.platform.modules.helpers (get_module_clusters) |
| test_get_module_prod_env_root_domains | 133-167 | 1 | 18070c53... | paas_wl.infras.cluster.models (Domain), paasng.platform.modules.constants (ExposedURLType), paasng.platform.modules.helpers (get_module_prod_env_root_domains), pytest (pytest), tests.utils.mocks.cluster (cluster_ingress_config) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/modules/test_manager.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_engine_apps | 54-60 | 3 | 0795eaed... | paasng.platform.applications.models (ApplicationEnvironment), paasng.platform.engine.models (EngineApp), paasng.platform.modules.manager (ModuleInitializer) |
| test_bind_default_services | 62-93 | 2 | c4d9bb27... | django.conf (settings), paasng.platform.modules.manager (ModuleInitializer), paasng.platform.templates.models (Template), pytest (pytest), unittest (mock) |
| test_bind_default_runtime | 95-140 | 4 | 5e64a126... | django.conf (settings), django_dynamic_fixture (G), paasng.platform.modules.helpers (ModuleRuntimeManager), paasng.platform.modules.manager (ModuleInitializer), paasng.platform.modules.models (AppBuildPack, AppSlugBuilder, AppSlugRunner), paasng.platform.templates.models (Template), unittest (mock) |
| test_initialize_vcs | 142-162 | 3 | 46a39d88... | django.conf (settings), paasng.platform.modules.constants (SourceOrigin), paasng.platform.modules.manager (ModuleInitializer), pathlib (Path), pytest (pytest), tempfile (tempfile), unittest (mock) |
| test_external_package | 164-178 | 2 | 5b8b85fe... | django.conf (settings), paasng.platform.modules.constants (SourceOrigin), paasng.platform.modules.manager (ModuleInitializer), paasng.platform.modules.specs (ModuleSpecs), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/modules/test_protections.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_match | 37-38 | 0 | 1cd32644... | paasng.platform.modules.protections (NoPendingOperationsCondition) |
| test_pending_deployment | 40-43 | 1 | 2c8cc496... | django_dynamic_fixture (G), paasng.platform.engine.constants (JobStatus), paasng.platform.engine.models.deployment (Deployment), paasng.platform.modules.protections (ConditionNotMatched, NoPendingOperationsCondition), pytest (pytest) |
| test_pending_offline | 45-48 | 1 | 69e43a31... | django_dynamic_fixture (G), paasng.platform.engine.constants (JobStatus), paasng.platform.engine.models.offline (OfflineOperation), paasng.platform.modules.protections (ConditionNotMatched, NoPendingOperationsCondition), pytest (pytest) |
| test_undeploy | 52-53 | 0 | 71f31a6b... | paasng.platform.modules.protections (AllEnvsArchivedCondition) |
| test_deployed | 55-58 | 1 | f6c8c4fe... | django_dynamic_fixture (G), paasng.platform.engine.constants (JobStatus), paasng.platform.engine.models.deployment (Deployment), paasng.platform.modules.protections (AllEnvsArchivedCondition, ConditionNotMatched), pytest (pytest) |
| test_deploy_but_archived | 60-65 | 0 | fd4656c5... | django_dynamic_fixture (G), paasng.platform.engine.constants (JobStatus), paasng.platform.engine.models.deployment (Deployment), paasng.platform.engine.models.offline (OfflineOperation), paasng.platform.modules.protections (AllEnvsArchivedCondition) |
| test_redeploy | 67-72 | 1 | 4630ed5c... | django_dynamic_fixture (G), paasng.platform.engine.constants (JobStatus), paasng.platform.engine.models.deployment (Deployment), paasng.platform.engine.models.offline (OfflineOperation), paasng.platform.modules.protections (AllEnvsArchivedCondition, ConditionNotMatched), pytest (pytest) |
| test_no_domain | 81-83 | 0 | b700656d... | paasng.platform.modules.protections (CustomDomainUnBoundCondition) |
| test_any_domain | 85-88 | 1 | 00b03cb8... | paasng.platform.modules.protections (ConditionNotMatched, CustomDomainUnBoundCondition), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/modules/test_runtime_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_filter | 34-49 | 1 | 29dc926a... | django_dynamic_fixture (G), pytest (pytest) |
| test_filter_full_image | 51-62 | 1 | 5d9ac6f7... | django_dynamic_fixture (G), pytest (pytest) |
| test_filter_by_labels | 64-102 | 3 | fb251f20... | django_dynamic_fixture (G), paasng.platform.modules.constants (APP_CATEGORY, SourceOrigin), pytest (pytest) |
| test_select_default_runtime | 104-148 | 2 | f34254b2... | contextlib (nullcontext), django.conf (settings), django.core.exceptions (ObjectDoesNotExist), django.test (override_settings), django_dynamic_fixture (G), pytest (pytest) |
| test_get_buildpack_choices | 152-177 | 1 | 486625d1... | paasng.platform.modules.models (BuildConfig), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/modules/test_specs.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_templated_source_enabled | 29-53 | 1 | 4bc9b39a... | paasng.platform.applications.constants (ApplicationType), paasng.platform.modules.constants (SourceOrigin), paasng.platform.modules.specs (ModuleSpecs), pytest (pytest) |
| test_source_origin | 55-79 | 3 | 1e17b093... | paasng.platform.engine.constants (RuntimeType), paasng.platform.modules.constants (SourceOrigin), paasng.platform.modules.specs (ModuleSpecs), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/modules/test_views.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list | 30-47 | 5 | a97a01c2... | django.urls (reverse) |
| test_retrieve_empty | 49-62 | 4 | a1cb3a00... | django.urls (reverse) |
| test_retrieve | 64-82 | 5 | 8fae7ac1... | django.urls (reverse), paasng.platform.modules (serializers), paasng.platform.modules.helpers (ModuleRuntimeBinder) |
| test_bind | 84-106 | 5 | 23237875... | django.urls (reverse) |
| test_rebind | 108-139 | 5 | bdc57a81... | django.urls (reverse), django_dynamic_fixture (G), paasng.platform.modules.models (AppBuildPack) |
| test_bind_multi_buildpacks | 141-190 | 6 | 7388072d... | django.urls (reverse), django_dynamic_fixture (G), paasng.platform.modules.helpers (ModuleRuntimeManager), paasng.platform.modules.models (AppBuildPack) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/scene_app/test_initializer.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 48-66 | 4 | 1295eebd... | django.conf (settings), paasng.platform.scene_app.initializer (SceneAPPInitializer), string (string), tests.utils.helpers (generate_random_string) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/smart_app/test_detector.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_detect | 29-49 | 1 | d9b6417c... | paasng.platform.smart_app.services.detector (relative_path_of_app_desc), pytest (pytest) |
| test_get_meta_info_found_desc_file | 57-70 | 2 | f0bd03ac... | paasng.platform.smart_app.services.detector (SourcePackageStatReader), pytest (pytest) |
| test_get_meta_info_no_desc_file | 72-82 | 2 | 3198a47b... | paasng.platform.smart_app.services.detector (SourcePackageStatReader), pytest (pytest) |
| test_invalid_file_format | 84-87 | 1 | afbe6e9a... | paasng.platform.smart_app.services.detector (SourcePackageStatReader), pytest (pytest), rest_framework.exceptions (ValidationError) |
| test_read | 89-107 | 2 | 1e748133... | paasng.platform.smart_app.services.detector (SourcePackageStatReader), pytest (pytest), tests.paasng.platform.sourcectl.packages.utils (V2_APP_DESC_EXAMPLE), yaml (yaml) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/smart_app/test_dispatch.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_dispatch_slug_image_to_registry | 88-216 | 3 | e780d136... | hashlib (hashlib), paasng.platform.smart_app.services.detector (SourcePackageStatReader), paasng.platform.smart_app.services.dispatch (bksmart_settings, dispatch_slug_image_to_registry), paasng.platform.smart_app.services.image_mgr (SMartImageManager), paasng.platform.sourcectl.utils (compress_directory, generate_temp_dir, uncompress_directory), re (re) |
| test_dispatch_cnb_image_to_registry | 219-338 | 3 | da5a9412... | itertools (chain), paasng.platform.smart_app.services.detector (SourcePackageStatReader), paasng.platform.smart_app.services.dispatch (bksmart_settings, dispatch_cnb_image_to_registry), paasng.platform.smart_app.services.image_mgr (SMartImageManager), paasng.platform.sourcectl.utils (compress_directory, generate_temp_dir, uncompress_directory), re (re) |
| test_dispatch_package_to_modules | 341-360 | 1 | e1d09a6b... | paasng.platform.smart_app.services.detector (SourcePackageStatReader), paasng.platform.smart_app.services.dispatch (dispatch_package_to_modules), paasng.platform.sourcectl.utils (compress_directory, generate_temp_dir), pytest (pytest), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/smart_app/test_patcher.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_error_if_patch_unsupported_ver | 45-58 | 1 | 9a369b2b... | paasng.platform.declarative.exceptions (DescriptionValidationError), paasng.platform.modules.constants (SourceOrigin), paasng.platform.smart_app.services.detector (SourcePackageStatReader), paasng.platform.smart_app.services.patcher (patch_smart_tarball), pytest (pytest), tests.paasng.platform.sourcectl.packages.utils (V1_APP_DESC_EXAMPLE), yaml (yaml) |
| test_add_procfile | 60-140 | 3 | ab8744df... | pytest (pytest), tarfile (tarfile), yaml (yaml) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/docker/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_init_image_repo | 26-31 | 2 | 60a94221... | paasng.platform.sourcectl.docker.models (init_image_repo), paasng.platform.sourcectl.models (RepoBasicAuthHolder) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/git/test_git_client.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_to_command | 40-48 | 1 | 4a277265... |  |
| test_to_obscure_cmd | 50-58 | 1 | 21009ddb... |  |
| test_checkout | 66-71 | 2 | bdc2610c... | paasng.platform.sourcectl.git.client (GitCommand), pathlib (Path), unittest.mock (patch) |
| test_clone | 73-85 | 2 | 17dcbb6f... | paasng.platform.sourcectl.git.client (GitCloneCommand), pathlib (Path), pytest (pytest), unittest.mock (patch) |
| test_list_refs | 87-120 | 3 | f0b42657... | collections (defaultdict), paasng.platform.sourcectl.git.client (GitCommand), pathlib (Path), pytest (pytest), unittest.mock (patch) |
| test_list_remote | 122-137 | 1 | 916a4ffb... | pytest (pytest), unittest.mock (patch) |
| test_list_remote_with_warning_and_invalid | 139-149 | 1 | e6c20920... | textwrap (dedent), unittest.mock (patch) |
| test_get_commit_info | 151-173 | 3 | 96fac8c9... | datetime (datetime), paasng.platform.sourcectl.git.client (GitCommand), pathlib (Path), pytest (pytest), unittest.mock (patch) |
| test_err_stdout_as_exc | 175-187 | 2 | 64ccf50d... | blue_krill.data_types.url (MutableURL), paasng.platform.sourcectl.git.client (GitCloneCommand), textwrap (dedent) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/packages/test_client.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_tarfile_like | 61-64 | 1 | cbfb3a88... | paasng.platform.sourcectl.package.client (BinaryTarClient), tarfile (tarfile) |
| test_not_tarfile_like | 66-77 | 1 | 5d9f4a2c... | paasng.platform.sourcectl.package.client (BinaryTarClient), tarfile (tarfile) |
| test_read_invalid_file | 79-83 | 1 | 380adc58... | paasng.platform.sourcectl.exceptions (PackageInvalidFileFormatError), paasng.platform.sourcectl.package.client (BinaryTarClient), pathlib (Path), pytest (pytest) |
| test_list_invalid_file | 85-89 | 1 | bfb6c125... | paasng.platform.sourcectl.exceptions (PackageInvalidFileFormatError), paasng.platform.sourcectl.package.client (BinaryTarClient), pathlib (Path), pytest (pytest) |
| test_read_file | 102-115 | 1 | 8bc0a761... | blue_krill.contextlib (nullcontext), paasng.platform.sourcectl.exceptions (ReadFileNotFoundError), paasng.platform.sourcectl.package.client (BasePackageClient), paasng.platform.sourcectl.utils (generate_temp_file), pytest (pytest) |
| test_read_file_with_relative_path | 117-145 | 1 | fabf0701... | blue_krill.contextlib (nullcontext), paasng.platform.sourcectl.exceptions (ReadFileNotFoundError), paasng.platform.sourcectl.package.client (BasePackageClient), paasng.platform.sourcectl.utils (generate_temp_file), pytest (pytest) |
| test_export | 147-159 | 1 | 5174871b... | paasng.platform.sourcectl.utils (generate_temp_dir, generate_temp_file), pytest (pytest) |
| test_read_file_should_fail | 170-182 | 1 | 91bf81e4... | paasng.platform.sourcectl.exceptions (ReadFileNotFoundError), paasng.platform.sourcectl.package.client (BasePackageClient), paasng.platform.sourcectl.utils (generate_temp_file), pytest (pytest) |
| test_export_should_fail | 184-196 | 1 | 34fb70d4... | paasng.platform.sourcectl.exceptions (ReadLinkFileOutsideDirectoryError), paasng.platform.sourcectl.utils (generate_temp_dir, generate_temp_file), pytest (pytest) |
| test_read_file_should_read_target_only | 202-215 | 1 | e0a83e71... | paasng.platform.sourcectl.package.client (ZipClient), paasng.platform.sourcectl.utils (generate_temp_file), pytest (pytest), tests.paasng.platform.sourcectl.packages.utils (gen_zip) |
| test_export_should_produce_no_links | 217-236 | 2 | 97062d1a... | paasng.platform.sourcectl.package.client (ZipClient), paasng.platform.sourcectl.utils (generate_temp_dir, generate_temp_file), pytest (pytest), tests.paasng.platform.sourcectl.packages.utils (gen_zip) |
| test_read_file_should_fail | 240-252 | 1 | 0f12b7b6... | paasng.platform.sourcectl.exceptions (ReadLinkFileOutsideDirectoryError), paasng.platform.sourcectl.package.client (BinaryTarClient), paasng.platform.sourcectl.utils (generate_temp_file), pytest (pytest), tests.paasng.platform.sourcectl.packages.utils (gen_tar) |
| test_export_should_fail | 254-266 | 1 | ffc0a838... | paasng.platform.sourcectl.exceptions (ReadLinkFileOutsideDirectoryError), paasng.platform.sourcectl.package.client (BinaryTarClient), paasng.platform.sourcectl.utils (generate_temp_dir, generate_temp_file), pytest (pytest), tests.paasng.platform.sourcectl.packages.utils (gen_tar) |
| test_http_protocol | 271-286 | 1 | 8f4894b4... | blue_krill.contextlib (nullcontext), paasng.platform.sourcectl.exceptions (ReadFileNotFoundError), paasng.platform.sourcectl.package.client (GenericRemoteClient), paasng.platform.sourcectl.utils (generate_temp_file), pytest (pytest), tests.utils.helpers (generate_random_string) |
| test_blobstore_protocol | 288-304 | 1 | 8554af08... | blue_krill.contextlib (nullcontext), django.test.utils (override_settings), paasng.platform.sourcectl.exceptions (ReadFileNotFoundError), paasng.platform.sourcectl.package.client (GenericRemoteClient), paasng.platform.sourcectl.package.uploader (upload_to_blob_store), paasng.platform.sourcectl.utils (generate_temp_file), pytest (pytest), tests.utils.helpers (generate_random_string) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/packages/test_controller.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_read_file | 44-105 | 1 | 3560dc99... | blue_krill.contextlib (nullcontext), paasng.platform.engine.configurations.source_file (get_metadata_reader), paasng.platform.smart_app.services.detector (SourcePackageStatReader), paasng.platform.sourcectl.exceptions (GetProcfileError), paasng.platform.sourcectl.models (SPStoragePolicy, SourcePackage, VersionInfo), paasng.platform.sourcectl.utils (generate_temp_file), pytest (pytest), tests.paasng.platform.sourcectl.packages.utils (gen_tar, gen_zip), yaml (yaml) |
| test_export | 107-128 | 1 | a30c51e9... | paasng.platform.smart_app.services.detector (SourcePackageStatReader), paasng.platform.sourcectl.controllers.package (PackageController), paasng.platform.sourcectl.models (SPStoragePolicy, SourcePackage, VersionInfo), paasng.platform.sourcectl.utils (generate_temp_dir, generate_temp_file), pytest (pytest), tests.paasng.platform.sourcectl.packages.utils (gen_tar, gen_zip) |
| test_list_alternative_versions | 130-178 | 1 | ee9e0fc5... | paasng.platform.smart_app.services.detector (SourcePackageStatReader), paasng.platform.sourcectl.controllers.package (PackageController), paasng.platform.sourcectl.models (AlternativeVersion, SPStoragePolicy, SourcePackage, VersionInfo), pytest (pytest), tarfile (tarfile) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/packages/test_downloader.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_download_file_via_http | 25-44 | 2 | 5afbe9ec... | paasng.platform.sourcectl.package.downloader (download_file_via_http), paasng.platform.sourcectl.utils (generate_temp_file), pytest (pytest), tests.utils.helpers (generate_random_string) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/packages/test_prepared.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_generate_storage_path | 26-37 | 1 | d8227a45... | paasng.platform.smart_app.services.prepared (PreparedSourcePackage), pathlib (Path), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/packages/test_uploader.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_generate_storage_path | 26-42 | 1 | ef16a458... | paasng.platform.sourcectl.models (SPStat), paasng.platform.sourcectl.package.uploader (generate_storage_path), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/packages/test_utils.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_app_description | 29-57 | 3 | da61ec45... | django.utils.translation (override), paasng.platform.smart_app.services.app_desc (get_app_description), paasng.platform.sourcectl.models (SPStat), paasng.utils.i18n (gettext_lazy), pytest (pytest), rest_framework.exceptions (ValidationError) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/svn/test_server_config.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_base_path | 53-55 | 1 | 32cae5a7... | paasng.platform.sourcectl.svn.server_config (BkSvnServerConfig) |
| test_single_svn | 59-74 | 1 | 2c1f3f03... | paasng.platform.sourcectl.source_types (refresh_sourcectl_types), paasng.platform.sourcectl.svn.server_config (get_bksvn_config), pytest (pytest) |
| test_multi_svn | 76-91 | 2 | 81a7f664... | paasng.platform.sourcectl.source_types (refresh_sourcectl_types), paasng.platform.sourcectl.svn.server_config (get_bksvn_config) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/test_bare_git.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_init_by_module | 55-79 | 1 | 5b2f0a03... | paasng.platform.sourcectl.controllers.bare_git (BareGitRepoController), pytest (pytest), unittest (mock) |
| test_anonymize_url | 81-99 | 4 | 748c1ebe... | http.server (BaseHTTPRequestHandler, ThreadingHTTPServer), paasng.platform.sourcectl.controllers.bare_git (BareGitRepoController), paasng.platform.sourcectl.git.client (GitCommandExecutionError), paasng.platform.sourcectl.models (VersionInfo), paasng.platform.sourcectl.utils (generate_temp_dir), pytest (pytest), threading (threading) |
| test_read_files | 122-138 | 2 | b95d2e8d... | paasng.platform.sourcectl.exceptions (ReadLinkFileOutsideDirectoryError), paasng.platform.sourcectl.models (VersionInfo), paasng.platform.sourcectl.utils (generate_temp_dir), pytest (pytest), unittest (mock) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/test_connector.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 31-52 | 3 | f61fed12... | django.conf (settings), paasng.platform.sourcectl.connector (IntegratedSvnAppRepoConnector), paasng.platform.sourcectl.source_types (get_sourcectl_types), pytest (pytest), unittest (mock) |
| test_normal | 56-74 | 3 | 79c9fde3... | django.conf (settings), paasng.platform.sourcectl.connector (ExternalGitAppRepoConnector), paasng.utils.blobstore (detect_default_blob_store), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/test_dockerignore.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_parse | 26-49 | 1 | e7a38447... | paasng.platform.sourcectl.utils (DockerIgnore), pytest (pytest), textwrap (dedent) |
| test_should_ignore | 51-161 | 1 | 17245274... | paasng.platform.sourcectl.utils (DockerIgnore), pytest (pytest), textwrap (dedent) |
| test_whitelist | 163-171 | 1 | afa61d6a... | paasng.platform.sourcectl.utils (DockerIgnore, compress_directory_ext, generate_temp_dir, generate_temp_file), pytest (pytest), tarfile (tarfile) |
| test_compress_with_docker_ignore | 174-204 | 1 | 0bfd6a32... | paasng.platform.sourcectl.utils (DockerIgnore, compress_directory_ext, generate_temp_dir, generate_temp_file), tarfile (tarfile), textwrap (dedent) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_git_alias_name | 32-40 | 1 | 4dfc35e9... | django_dynamic_fixture (G), paasng.platform.sourcectl.models (GitRepository), pytest (pytest) |
| test_has_permission_for_user | 54-57 | 1 | 6997b2f8... | paasng.infras.accounts.models (Scope) |
| test_has_permission_for_group | 59-66 | 2 | 772ba8b0... | paasng.infras.accounts.models (Scope) |
| test_has_permission_for_project | 68-75 | 2 | a5cdd6f0... | paasng.infras.accounts.models (Scope) |
| test_store_package | 78-102 | 8 | c80c797d... | paasng.platform.sourcectl.models (SPStat, SPStoragePolicy, SourcePackage), pytest (pytest) |
| test_overwrite_package | 105-136 | 1 | c25feae9... | paasng.platform.sourcectl.exceptions (PackageAlreadyExists), paasng.platform.sourcectl.models (SPStat, SPStoragePolicy, SourcePackage), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/test_perm.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_list_availables | 30-41 | 1 | 83fa6a5a... | paasng.infras.accounts.constants (AccountFeatureFlag), paasng.infras.accounts.models (AccountFeatureFlag), paasng.platform.sourcectl.perm (UserSourceProviders), pytest (pytest) |
| test_list_module_availables | 43-54 | 3 | 4df8a717... | paasng.platform.sourcectl.perm (UserSourceProviders), pytest (pytest), unittest (mock) |
| test_render_providers | 57-60 | 2 | eb98a3a1... | paasng.platform.sourcectl.perm (render_providers) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/test_source_types.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_region | 65-68 | 2 | 8e19ec78... | paasng.platform.sourcectl.source_types (ServerConfig) |
| test_region_not_found_default | 70-72 | 1 | f6fd70f8... | paasng.platform.sourcectl.source_types (ServerConfig) |
| test_region_agonostic_error | 74-77 | 1 | 0fdacabd... | paasng.platform.sourcectl.source_types (ServerConfig), pytest (pytest) |
| test_region_agonostic_normal | 79-81 | 1 | 4e3605de... | paasng.platform.sourcectl.source_types (ServerConfig) |
| test_normal | 121-125 | 3 | 9f03a034... |  |
| test_non_region_server_config | 127-129 | 1 | b3286603... |  |
| test_oauth_credentials | 131-143 | 7 | 12daa31f... |  |
| test_oauth_backend_config | 145-155 | 6 | fefe92f1... |  |
| test_oauth_mixin | 157-171 | 6 | 272783f0... |  |
| test_partial_overwrite_display_info | 173-182 | 3 | 5ea6a508... |  |
| test_items | 202-204 | 2 | 01acc2f2... |  |
| test_get_by_name | 206-207 | 1 | e407daf3... |  |
| test_find_by_type | 209-212 | 2 | 4cc4f2cd... | pytest (pytest) |
| test_get_choices | 214-218 | 1 | a450a96b... |  |
| test_get_choice_label | 220-221 | 1 | 9ba99993... |  |
| test_get | 245-264 | 2 | e7ee7733... | paasng.platform.sourcectl.source_types (SourcectlTypeNames), pytest (pytest) |
| test_default | 266-268 | 1 | 9dccedb5... | paasng.platform.sourcectl.source_types (SourcectlTypeNames) |
| test_build_name_index | 270-276 | 1 | 9e8ed92e... | paasng.platform.sourcectl.source_types (SourcectlTypeNames) |
| test_build_type_name_index | 278-283 | 1 | 822d2dbd... | paasng.platform.sourcectl.source_types (SourcectlTypeNames) |
| test_build_shorter_type_name_index | 285-292 | 1 | ff01b864... | paasng.platform.sourcectl.source_types (SourcectlTypeNames) |
| test_getattr | 294-296 | 1 | b8ec85ef... | paasng.platform.sourcectl.source_types (SourcectlTypeNames) |
| test_filter_by_basic_type | 298-307 | 1 | ec7b765d... | paasng.platform.sourcectl.source_types (SourcectlTypeNames), pytest (pytest) |
| test_validate_svn | 309-312 | 2 | 896ae6e4... | paasng.platform.sourcectl.source_types (SourcectlTypeNames) |
| test_validate_git | 314-317 | 2 | 645e374b... | paasng.platform.sourcectl.source_types (SourcectlTypeNames) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/test_sourcectl_git.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_export_normal | 56-66 | 2 | 95ba5ec2... | os (os), paasng.platform.sourcectl.controllers.gitlab (GitlabRepoController), paasng.platform.sourcectl.utils (generate_temp_dir) |
| test_get_owner_and_repo | 68-71 | 2 | 4215ab46... | paasng.platform.sourcectl.controllers.gitlab (GitlabRepoController) |
| test_list_alternative_versions | 73-129 | 1 | 473bc63f... | datetime (datetime), dateutil.tz.tz (tzutc), paasng.platform.sourcectl.controllers.gitlab (GitlabRepoController), paasng.platform.sourcectl.models (AlternativeVersion) |
| test_extract_version_info | 131-133 | 1 | df48423a... | paasng.platform.sourcectl.controllers.gitlab (GitlabRepoController) |
| test_extract_smart_revision | 135-153 | 1 | 9a222b2b... | paasng.platform.sourcectl.controllers.gitlab (GitlabRepoController), pytest (pytest) |
| test_build_url | 155-157 | 1 | ed3d5489... | paasng.platform.sourcectl.controllers.gitlab (GitlabRepoController) |
| test_get_project | 169-172 | 2 | 9fc7a29d... | paasng.platform.sourcectl.controllers.github (GitHubRepoController) |
| test_list_all_repositories | 179-220 | 9 | d1e8819b... | datetime (datetime), dateutil.tz.tz (tzutc), paasng.platform.sourcectl.controllers.github (GitHubRepoController) |
| test_list_alternative_versions | 222-259 | 5 | f2762cdb... | paasng.platform.sourcectl.controllers.github (GitHubRepoController) |
| test_extract_smart_revision | 261-267 | 1 | fff28ac7... | paasng.platform.sourcectl.controllers.github (GitHubRepoController) |
| test_build_url | 269-271 | 1 | 2d6d0bf8... | paasng.platform.sourcectl.controllers.github (GitHubRepoController) |
| test_read_file | 273-279 | 1 | dde2bb44... | paasng.platform.sourcectl.controllers.github (GitHubRepoController) |
| test_get_project | 291-294 | 2 | 6af984ac... | paasng.platform.sourcectl.controllers.gitee (GiteeRepoController) |
| test_list_all_repositories | 301-327 | 5 | 822e1fe3... | datetime (datetime), dateutil.tz.tz (tzoffset), paasng.platform.sourcectl.controllers.gitee (GiteeRepoController) |
| test_list_alternative_versions | 329-366 | 5 | 0a635fdc... | paasng.platform.sourcectl.controllers.gitee (GiteeRepoController) |
| test_extract_smart_revision | 368-374 | 1 | 61f51960... | paasng.platform.sourcectl.controllers.gitee (GiteeRepoController) |
| test_build_url | 376-378 | 1 | c2f64c03... | paasng.platform.sourcectl.controllers.gitee (GiteeRepoController) |
| test_read_file | 380-386 | 1 | a5a276c2... | paasng.platform.sourcectl.controllers.gitee (GiteeRepoController) |
| test_branch_data_to_version_normal | 406-408 | 1 | 1facecf9... | datetime (datetime) |
| test_branch_data_to_version_other_timezone | 410-413 | 1 | 71cec2cf... | datetime (datetime) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/test_sourcectl_svn.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_provision | 48-67 | 3 | c05d52e7... | paasng.platform.sourcectl.svn.client (RepoProvider), pytest (pytest), svn.common (SvnException), tests.utils (mock) |
| test_download_template_from_svn | 71-92 | 0 | c5fcdca9... | django.conf (settings), paasng.platform.sourcectl.svn.client (SvnRepositoryClient), paasng.platform.sourcectl.utils (generate_temp_dir), paasng.platform.templates.constants (TemplateType), paasng.platform.templates.templater (Templater), pytest (pytest), tests.utils (mock) |
| test_export_normal | 98-101 | 1 | 29c6be19... | os (os), paasng.platform.sourcectl.utils (generate_temp_dir) |
| test_get_latest_revison | 103-104 | 0 | d3b7a143... |  |
| test_package | 106-109 | 1 | c1581d57... | os (os), tempfile (tempfile) |
| test_list_alternative_versions | 111-115 | 2 | ef44edb4... |  |
| test_extract_smart_revision | 117-121 | 2 | b9e9b3d7... | pytest (pytest) |
| test_create_repo | 125-135 | 1 | 2e4fced8... | django.conf (settings), django_dynamic_fixture (G), paasng.platform.sourcectl.models (SvnRepository), paasng.platform.sourcectl.serializers (RepositorySLZ), paasng.platform.sourcectl.source_types (get_sourcectl_names) |
| test_create_app | 140-154 | 2 | 21a98aef... | paasng.platform.sourcectl.svn.admin (get_svn_authorization_manager), unittest.mock (Mock, patch) |
| test_update_developers | 156-181 | 4 | dfd6f4bb... | paasng.infras.iam.helpers (add_role_members), paasng.platform.applications.constants (ApplicationRole), paasng.platform.sourcectl.svn.admin (get_svn_authorization_manager), pytest (pytest), unittest.mock (Mock, patch) |
| test_build_url_trunk | 192-194 | 1 | 3a3d971c... | paasng.platform.sourcectl.models (VersionInfo) |
| test_build_url_branch | 196-198 | 1 | 19a334a2... | paasng.platform.sourcectl.models (VersionInfo) |
| test_build_url_tag | 200-202 | 1 | c6afa780... | paasng.platform.sourcectl.models (VersionInfo) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/sourcectl/test_validators.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_validate_image_url | 24-37 | 1 | 49ce35e0... | django.test.utils (override_settings), paasng.platform.sourcectl.validators (validate_image_url), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/platform/test_lesscode.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_call_api_succeeded | 94-103 | 5 | 0a0c82dd... | paasng.platform.bk_lesscode.client (make_bk_lesscode_client) |
| test_call_api_failed | 105-108 | 1 | a509a0e9... | paasng.platform.bk_lesscode.client (make_bk_lesscode_client), paasng.platform.bk_lesscode.exceptions (LessCodeApiError), pytest (pytest) |
| test_get_address_succeeded | 110-114 | 1 | 5cf614af... | django.conf (settings), paasng.platform.bk_lesscode.client (make_bk_lesscode_client) |
| test_get_address_failed | 116-120 | 1 | 3ff2b067... | paasng.platform.bk_lesscode.client (make_bk_lesscode_client) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/es_log/test_misc.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_filter_indexes_by_time_range | 35-97 | 1 | 16013cfc... | arrow (arrow), paasng.utils.es_log.misc (filter_indexes_by_time_range), paasng.utils.es_log.time_range (SmartTimeRange), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/es_log/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_format_timestamp | 29-40 | 1 | 6dea4f3e... | datetime (datetime), paasng.utils.es_log.misc (format_timestamp), pytest (pytest), pytz (pytz) |
| test_count_filters_options | 43-72 | 1 | 15e15b9a... | paasng.utils.es_log.misc (count_filters_options), paasng.utils.es_log.models (FieldFilter), pytest (pytest) |
| test_flatten_structure | 75-105 | 1 | 4d9a0d50... | paasng.utils.es_log.misc (flatten_structure), pytest (pytest) |
| test_extra_field | 116-152 | 1 | 2db383ed... | attrs (converters, define), cattr (cattr), paasng.utils.es_log.models (LogLine, extra_field), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/es_log/test_time_range.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_epoch_milliseconds | 26-56 | 1 | 7fd0804e... | datetime (datetime), paasng.utils.es_log.time_range (get_epoch_milliseconds), pytest (pytest) |
| test_relative_time | 60-78 | 3 | 23706be7... | paasng.utils.es_log.time_range (SmartTimeRange), pytest (pytest) |
| test_absolute_time | 80-134 | 4 | 22ad02b3... | arrow (arrow), datetime (datetime), paasng.utils.es_log.time_range (SmartTimeRange), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/i18n/test_migrate.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 30-39 | 3 | 1f394efd... | django.apps.registry (apps), django.db (connection), django_dynamic_fixture (G), paasng.platform.engine.models.steps (DeployStep), paasng.utils.i18n.migrate (copy_field) |
| test_thousands | 41-57 | 2 | 1bdabf61... | django.apps.registry (apps), django.db (connection), django_dynamic_fixture (G), paasng.platform.engine.models.steps (DeployPhase, DeployStep), paasng.utils.i18n.migrate (copy_field) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/i18n/test_serializers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_validate | 47-60 | 1 | 4596b452... | contextlib (nullcontext), django.utils.translation (override), pytest (pytest) |
| test_to_representation | 62-74 | 1 | 3bab1f54... | contextlib (nullcontext), django.utils.translation (override), pytest (pytest) |
| test_valid | 88-105 | 1 | 71b493bf... | contextlib (nullcontext), django.utils.translation (override), pytest (pytest) |
| test_invalid | 107-127 | 3 | 9a841535... | contextlib (nullcontext), django.utils.translation (override), pytest (pytest), rest_framework.exceptions (ValidationError) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_basic.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_first_true | 25-34 | 1 | e1a0e4ad... | paasng.utils.basic (first_true), pytest (pytest) |
| test_unique_id_generator | 37-40 | 2 | 61f2fd0d... | paasng.utils.basic (unique_id_generator) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_blobstore.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_detect_default_blob_store | 42-57 | 1 | 47c67cb5... | django.test.utils (override_settings), paasng.utils.blobstore (detect_default_blob_store), pytest (pytest) |
| test_make_blob_store_env | 60-114 | 1 | 103ca1c6... | django.test.utils (override_settings), json (json), paasng.utils.blobstore (generate_s3cmd_conf, make_blob_store_env), pytest (pytest) |
| test_make_blob_store_encrypt_env | 117-158 | 1 | 5ec9de41... | django.test.utils (override_settings), paasng.utils.blobstore (make_blob_store_env), pytest (pytest), re (re) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_camel_converter.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_dict_to_camel | 23-66 | 1 | b01db448... | paasng.utils.camel_converter (dict_to_camel), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_command.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_command_name_normal | 37-43 | 2 | 6af4ca7a... | paas_wl.bk_app.processes.managers (AppProcessManager), paas_wl.utils.command (get_command_name) |
| test_command_name_celery | 45-48 | 1 | 8ff08b5a... | paas_wl.bk_app.processes.managers (AppProcessManager), paas_wl.utils.command (get_command_name) |
| test_commnad_name_with_slash | 50-57 | 2 | 3f567dfa... | paas_wl.bk_app.processes.managers (AppProcessManager), paas_wl.utils.command (get_command_name) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_configs.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_no_region | 34-43 | 1 | e4291af6... | paasng.utils.configs (RegionAwareConfig), pytest (pytest) |
| test_region | 45-48 | 2 | afa37dca... | paasng.utils.configs (RegionAwareConfig) |
| test_region_not_found | 50-53 | 1 | 18520769... | paasng.utils.configs (RegionAwareConfig), pytest (pytest) |
| test_region_not_found_default | 55-57 | 1 | 8bf86225... | paasng.utils.configs (RegionAwareConfig) |
| test_get_region_aware | 66-81 | 1 | 4a45b3d3... | paasng.utils.configs (get_region_aware), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_datetime.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_calculate_gap_seconds_interval | 24-36 | 1 | 77833f6a... | paasng.utils.datetime (calculate_gap_seconds_interval), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_dictx.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_items | 23-38 | 1 | edf42164... | paasng.utils.dictx (get_items), pytest (pytest) |
| test_get_items_exceptions | 41-51 | 1 | b194fabb... | paasng.utils.dictx (get_items), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_error_message.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_find_coded_error_message | 29-38 | 1 | 04e8ce8f... | paasng.accessories.servicehub.remote.exceptions (GetClusterEgressInfoError), paasng.utils.error_message (find_coded_error_message), pytest (pytest) |
| test_find_innermost_exception | 73-87 | 1 | 37c513f2... | paasng.utils.error_message (find_innermost_exception), pytest (pytest) |
| test_wrap_validation_error_dict | 90-94 | 3 | 7861e0af... | paasng.utils.error_message (wrap_validation_error), rest_framework.exceptions (ValidationError) |
| test_wrap_validation_error_list | 97-100 | 2 | bd19c138... | paasng.utils.error_message (wrap_validation_error), rest_framework.exceptions (ValidationError) |
| test_wrap_validation_error_str | 103-106 | 2 | 5e1a149e... | paasng.utils.error_message (wrap_validation_error), rest_framework.exceptions (ValidationError) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_file.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_path_may_escape | 22-37 | 1 | 4a4bd52d... | paasng.utils.file (path_may_escape), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_masked_curlify.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_mask_query_params | 27-34 | 2 | fe2ccf3e... | paasng.utils (masked_curlify), paasng.utils.masked_curlify (MASKED_CONTENT), requests (Request), urllib.parse (quote) |
| test_mask_json_data | 36-44 | 2 | bbf5d98b... | json (json), paasng.utils (masked_curlify), paasng.utils.masked_curlify (MASKED_CONTENT), requests (Request) |
| test_mask_form_data | 46-54 | 2 | 3f3a718b... | paasng.utils (masked_curlify), paasng.utils.masked_curlify (MASKED_CONTENT), requests (Request), urllib.parse (parse_qs) |
| test_mask_header_data | 56-65 | 2 | d8eda3dd... | paasng.utils (masked_curlify), paasng.utils.masked_curlify (MASKED_CONTENT), requests (Request) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_models.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_bk_user_field | 38-43 | 2 | 6c890936... | django_dynamic_fixture (G), paasng.infras.accounts.models (UserProfile) |
| test_from_string | 47-54 | 4 | a97fd28f... | paasng.utils.models (OrderByField) |
| test_replacing_name | 56-59 | 1 | 6a1dbe7d... | paasng.utils.models (OrderByField) |
| test_make_legacy_json_field | 62-69 | 2 | efa0c824... | attrs (define), paasng.utils.models (make_legacy_json_field) |
| test_make_json_field | 72-79 | 2 | 13e8b11b... | attrs (define), paasng.utils.models (make_json_field) |
| test_pickle | 94-104 | 0 | 4cce82b6... | blue_krill.contextlib (nullcontext), pickle (pickle), pytest (pytest) |
| test_set | 108-128 | 4 | 8cf0d1e8... | bkpaas_auth.core.constants (ProviderType), bkpaas_auth.core.encoder (user_id_encoder), django.db (models), paasng.utils.models (BkUserField) |
| test_integrated | 130-144 | 2 | 76426481... | bkpaas_auth.core.constants (ProviderType), bkpaas_auth.core.encoder (user_id_encoder), paasng.platform.applications.constants (ApplicationType), paasng.platform.applications.utils (create_application), tests.utils.helpers (generate_random_string) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_notification_plugins.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_mail | 37-39 | 1 | d0e1484c... | paasng.utils.notification_plugins (MailNotificationPlugin) |
| test_sms | 41-43 | 1 | 17f13521... | paasng.utils.notification_plugins (SMSNotificationPlugin) |
| test_wechat | 45-47 | 1 | f3fbde86... | paasng.utils.notification_plugins (WeChatNotificationPlugin) |
| test_wecom | 49-51 | 1 | a9b6bcd6... | paasng.utils.notification_plugins (WeComNotificationPlugin) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_notifier.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 22-30 | 3 | b8a10ab4... | paasng.utils.notifier (DummyUserNotificationPlugin, UserNotificationBackend) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_patternmatcher.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_pattern | 23-90 | 1 | 078f51c0... | paasng.utils.patternmatcher (Pattern), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_rate_limit.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_UserActionRateLimiter | 33-47 | 3 | a70dfbc1... | paasng.core.core.storages.redisdb (get_default_redis), paasng.utils.rate_limit.constants (UserAction), paasng.utils.rate_limit.fixed_window (UserActionRateLimiter), paasng.utils.rate_limit.token_bucket (UserActionRateLimiter), pytest (pytest), tests.utils.auth (create_user), time (time) |
| test_rate_limits_on_view_func | 50-69 | 3 | 2e0ccfc1... | django.http (HttpRequest), paasng.utils.rate_limit.constants (UserAction), paasng.utils.rate_limit.fixed_window (rate_limits_by_user), rest_framework.response (Response), rest_framework.status (HTTP_200_OK, HTTP_429_TOO_MANY_REQUESTS), tests.utils.auth (create_user), time (time) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_serializers.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_to_internal_value | 33-46 | 1 | 4772ec93... | blue_krill.contextlib (nullcontext), pytest (pytest), rest_framework.exceptions (ValidationError) |
| test_to_representation | 48-62 | 1 | 5ce1e967... | blue_krill.contextlib (nullcontext), io (io), pytest (pytest) |
| test_config_var_reserved_key_validator | 65-80 | 0 | 9c2a0579... | blue_krill.contextlib (nullcontext), paasng.utils.serializers (ConfigVarReservedKeyValidator), pytest (pytest), rest_framework.exceptions (ValidationError) |
| test_to_internal_value | 88-100 | 1 | 718604e0... | pytest (pytest) |
| test_to_representation | 102-113 | 1 | 05fb6fd3... | pytest (pytest) |
| test_valid | 121-134 | 1 | f1b23b67... | pytest (pytest) |
| test_invalid | 136-151 | 1 | a2c3cd2c... | pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_text.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_normal | 31-41 | 1 | 8f5939e3... | paasng.utils.text (strip_html_tags), pytest (pytest) |
| test_remove_suffix | 44-53 | 1 | ecbc796a... | paasng.utils.text (remove_suffix), pytest (pytest) |
| test_camel_to_snake | 56-64 | 1 | 63fdad94... | paasng.utils.text (camel_to_snake), pytest (pytest) |
| test_calculate_percentage | 67-110 | 2 | 2f435ec1... | paasng.utils.text (calculate_percentage), pytest (pytest) |
| test_various_valid_patterns | 114-127 | 1 | 537838e4... | paasng.utils.text (BraceOnlyTemplate), pytest (pytest) |
| test_escaped_braces | 129-132 | 1 | 445bc58a... | paasng.utils.text (BraceOnlyTemplate) |
| test_no_substitution_needed | 134-136 | 1 | 3a577771... | paasng.utils.text (BraceOnlyTemplate) |
| test_missing_variable_raises_error | 138-141 | 1 | 75c255af... | paasng.utils.text (BraceOnlyTemplate), pytest (pytest) |
| test_basic | 145-146 | 1 | 7ad307e3... | paasng.utils.text (basic_str_format) |
| test_index_access_should_fail | 148-150 | 1 | 98c47f81... | paasng.utils.text (basic_str_format), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_time_tools.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_time_delta | 25-33 | 1 | 3c27149d... | datetime (timedelta), paasng.utils.datetime (get_time_delta), pytest (pytest) |
| test_humanize_timedelta | 36-51 | 1 | f215707c... | datetime (timedelta), paasng.utils.datetime (humanize_timedelta), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_validators.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_valid_input | 25-28 | 1 | fff4d52f... | paasng.utils.validators (ReservedWordValidator), pytest (pytest) |
| test_invalid_input | 30-35 | 2 | cfd022fa... | django.core.exceptions (ValidationError), paasng.utils.validators (ReservedWordValidator), pytest (pytest) |
| test_valid_input | 39-42 | 1 | 44878d55... | paasng.utils.validators (DnsSafeNameValidator), pytest (pytest) |
| test_negative_sample | 44-49 | 2 | 8daff064... | django.core.exceptions (ValidationError), paasng.utils.validators (DnsSafeNameValidator), pytest (pytest) |
| test_invalid_protocol | 53-59 | 1 | 855b4e06... | paasng.utils.validators (validate_repo_url), pytest (pytest) |
| test_invalid_port | 61-68 | 1 | 51c06ff4... | paasng.utils.validators (validate_repo_url), pytest (pytest) |
| test_invalid_url | 70-76 | 1 | a20cffc0... | paasng.utils.validators (validate_repo_url), pytest (pytest) |
| test_valid_url | 78-88 | 0 | b08930a7... | paasng.utils.validators (validate_repo_url), pytest (pytest) |
| test_invalid_port | 92-99 | 1 | d4021a6a... | paasng.utils.validators (validate_image_repo), pytest (pytest) |
| test_valid_repo | 101-110 | 0 | bba90ba8... | paasng.utils.validators (validate_image_repo), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/paasng/test_utils/test_view.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_one_line_error | 37-45 | 1 | e1c92897... | paasng.utils.views (one_line_error), pytest (pytest), rest_framework.exceptions (ErrorDetail, ValidationError) |
| test_hook_chain | 56-81 | 2 | 64714dd7... | paasng.utils.views (HookChain), pytest (pytest) |
| test_render | 85-113 | 1 | 310e2299... | json (json), paasng.utils.views (BkStandardApiJSONRenderer, ERROR_CODE_NUM_HEADER), pytest (pytest), rest_framework.response (Response) |
| test_permission_classes | 122-158 | 8 | c46176ed... | django.utils.decorators (method_decorator), paasng.utils.views (action_perms), rest_framework.response (Response), rest_framework.test (APIRequestFactory), rest_framework.viewsets (ViewSet) |

---


### 测试文件: apiserver/paasng/tests/test_settings.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_get_database_from_url | 39-45 | 3 | e4312bc5... | blue_krill.encrypt.utils (encrypt_string), os (os), paasng.settings.utils (get_database_conf), unittest (mock) |
| test_get_database_for_tests | 48-57 | 3 | edb01845... | paasng.settings.utils (get_database_conf), pytest (pytest) |
| test_get_paas_service_jwt_clients_simple | 60-65 | 1 | 107cbc01... | paasng.settings.utils (get_paas_service_jwt_clients) |
| test_get_paas_service_jwt_clients_mixed | 68-75 | 1 | 9816d7e4... | paasng.settings.utils (get_paas_service_jwt_clients) |
| test_get_service_remote_endpoints | 78-112 | 6 | 456fccbd... | paasng.settings.utils (NAME_FOR_SIMPLE_JWT, get_service_remote_endpoints) |
| test_is_in_celery_worker | 115-124 | 1 | 7bd667a3... | paasng.settings.utils (is_in_celery_worker), pytest (pytest) |

---


### 测试文件: apiserver/paasng/tests/test_sqlalchemy_transaction.py

| 测试名称 | 行数 | 断言数 | 主体MD5 | 目标 |
|---------|------|--------|---------|------|
| test_create_legacy_app_1 | 90-95 | 0 | c30869b9... | paasng.core.core.storages.sqlalchemy (legacy_db), tests.utils.helpers (configure_regions) |
| test_create_legacy_app_2 | 98-103 | 0 | c766e7b3... | paasng.core.core.storages.sqlalchemy (legacy_db), tests.utils.helpers (configure_regions) |

---

