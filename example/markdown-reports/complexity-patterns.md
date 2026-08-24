# complexity-patterns 扫描报告

## 元数据
- **scanner_name**: complexity-patterns

## 概要信息
- **总数量**: 64
- **已扫描文件数**: 2368
- **扫描耗时**: 46684 毫秒

- **高复杂度函数数量**: 64

### 按严重程度统计函数数
- **warning**: 34 个函数
- **high_risk**: 7 个函数
- **acceptable**: 21 个函数
- **critical**: 2 个函数

## 结果详情

### 模块: apiserver/paasng/paas_wl/bk_app/processes/kres_slzs.py


#### deserialize

**复杂度分数**: 11
**严重程度**: warning
**行数**: 194-246 (共 53 行, 1 行注释)
**描述**: Generate a ProcInstance by given Pod object

**函数签名**:
```python
def deserialize ( self, app: WlApp, kube_data: ResourceInstance ) -> 'Instance' :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def deserialize(self, app: WlApp, kube_data: ResourceInstance) -> "Instance":
        """Generate a ProcInstance by given Pod object"""
        pod = kube_data
        health_status = check_pod_health_status(parse_pod(kube_data))
        instance_state, state_message = self.parse_instance_state(pod.status.phase, health_status)

        # Use first container's status
        c_status = None
        c_status_dict = {}
        if pod.status.get("containerStatuses"):
            c_status = pod.status.containerStatuses[0]
            c_status_dict = get_items(pod.to_dict(), "status.containerStatuses", [{}])[0]

        process_type = self.get_process_type(pod)
        target_container = self._get_main_container(app, pod)

        envs = {}
        if target_container and hasattr(target_container, "env"):
            for env in target_container.env:
                name = getattr(env, "name", None)
                value = getattr(env, "value", None)
                if name and value is not None:
                    envs[name] = value

        if app.type == WlAppType.DEFAULT:
            labels = pod.metadata.labels or {}
            version = int(labels.get("release_version", 0))
        else:
            annotations = pod.metadata.annotations or {}
            version = int(annotations.get(BKPAAS_DEPLOY_ID_ANNO_KEY, 0))

        terminated_info = {}
        if c_status_dict:
            terminated_info = {
                "exit_code": get_items(c_status_dict, "lastState.terminated.exitCode"),
                "reason": get_items(c_status_dict, "lastState.terminated.reason"),
            }
        return self.entity_type(
            app=app,
            name=pod.metadata.name,
            process_type=process_type,
            host_ip=pod.status.get("hostIP", None),
            start_time=pod.status.get("startTime", None),
            state=instance_state,
            state_message=state_message,
            rich_status=self.extract_rich_status(pod.status.phase, c_status),
            image=target_container.image if target_container else "",
            envs=envs,
            ready=health_status.status == HealthStatusType.HEALTHY,
            restart_count=c_status.restartCount if c_status else 0,
            terminated_info=terminated_info,
            version=version,
        )

```
</details>

---


### 模块: apiserver/paasng/paas_wl/bk_app/processes/models.py


#### sync

**复杂度分数**: 17
**严重程度**: high_risk
**行数**: 129-213 (共 85 行, 6 行注释)
**描述**: Sync ProcessSpecs data with given processes.

**函数签名**:
```python
def sync ( self, processes: List[ProcessTmpl] ) :
```

**消息**: Complexity 17 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def sync(self, processes: List[ProcessTmpl]):
        """Sync ProcessSpecs data with given processes.

        :param processes: plain process spec structure,
                          such as [{"name": "web", "command": "foo", "replicas": 1, "plan": "bar"}, ...]
                          where 'replicas' and 'plan' is optional
        """
        processes_map: Dict[str, ProcessTmpl] = {process.name: process for process in processes}
        environment = get_metadata(self.wl_app).environment

        # Hardcode proc_type to "process" because no other values is supported at this moment.
        proc_type = "process"
        proc_specs = ProcessSpec.objects.filter(engine_app=self.wl_app, type=proc_type)
        existed_procs_name = set(proc_specs.values_list("name", flat=True))

        # remove proc spec objects which is already deleted via procfile
        removing_procs_name = list(existed_procs_name - processes_map.keys())
        if removing_procs_name:
            proc_specs.filter(name__in=removing_procs_name).delete()

        # add spec objects start
        default_process_spec_plan = ProcessSpecPlan.objects.get_by_name(name=settings.DEFAULT_PROC_SPEC_PLAN)
        if self.wl_app.type == WlAppType.CLOUD_NATIVE:
            default_process_spec_plan = (
                ProcessSpecPlan.objects.get_by_name(name=ResQuotaPlan.P_DEFAULT) or default_process_spec_plan
            )
        adding_procs = [process for name, process in processes_map.items() if name not in existed_procs_name]

        def process_spec_builder(process: ProcessTmpl) -> ProcessSpec:
            target_replicas = process.replicas or self.get_default_replicas(process.name, environment)
            plan = default_process_spec_plan
            if plan_name := process.plan:
                plan = self.get_plan(plan_name, default_process_spec_plan)

            return ProcessSpec(
                type=proc_type,
                region=self.wl_app.region,
                name=process.name,
                engine_app_id=self.wl_app.pk,
                target_replicas=target_replicas,
                plan=plan,
                proc_command=process.command,
                autoscaling=process.autoscaling,
                scaling_config=process.scaling_config.dict() if process.scaling_config else None,
            )

        self.bulk_create_procs(proc_creator=process_spec_builder, adding_procs=adding_procs)
        # add spec objects end

        # update spec objects
        updating_proc_specs = [process for name, process in processes_map.items() if name in existed_procs_name]

        def process_spec_updator(process: ProcessTmpl) -> Tuple[bool, ProcessSpec]:
            process_spec = proc_specs.get(name=process.name)
            recorder = AttrSetter(process_spec)

            # 目前 sync 方法都在部署阶段调用, 因此 target_status 需要设置为 start
            if process_spec.target_status != ProcessTargetStatus.START.value:
                recorder.setattr("target_status", ProcessTargetStatus.START.value)

            if (command := process.command) and command != process_spec.proc_command:
                recorder.setattr("proc_command", command)
            if (plan_name := process.plan) and (plan := self.get_plan(plan_name, None)):
                recorder.setattr("plan", plan)
            if process.autoscaling != process_spec.autoscaling:
                recorder.setattr("autoscaling", process.autoscaling)
            if (scaling_config := process.scaling_config) and scaling_config.dict() != process_spec.scaling_config:
                recorder.setattr("scaling_config", scaling_config.dict())
            if (replicas := process.replicas) and replicas != process_spec.target_replicas:
                recorder.setattr("target_replicas", replicas)
            return recorder.changed, process_spec

        self.bulk_update_procs(
            proc_updator=process_spec_updator,
            updating_procs=updating_proc_specs,
            updated_fields=[
                "proc_command",
                "plan",
                "autoscaling",
                "scaling_config",
                "target_replicas",
                "target_status",
                "updated",
            ],
        )

```
</details>

---


### 模块: apiserver/paasng/paas_wl/infras/resources/base/kube_client.py


#### __search

**复杂度分数**: 15
**严重程度**: warning
**行数**: 35-78 (共 44 行, 10 行注释)

**函数签名**:
```python
def __search ( self, parts, resources, reqParams ) :
```

**消息**: Complexity 15 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def __search(self, parts, resources, reqParams):  # noqa
        part = parts[0]
        if part != "*":
            resourcePart = resources.get(part)  # noqa
            if not resourcePart:
                return []
            elif isinstance(resourcePart, ResourceGroup):
                if len(reqParams) != 2:
                    raise ValueError("prefix and group params should be present, have %s" % reqParams)
                # Check if we've requested resources for this group
                if not resourcePart.resources:
                    prefix, group, version = reqParams[0], reqParams[1], part
                    try:
                        resourcePart.resources = self.get_resources_for_api_version(
                            prefix, group, part, resourcePart.preferred
                        )
                    except NotFoundError:
                        raise ResourceNotFoundError

                    # https://github.com/kubernetes-client/python/blob/master/kubernetes/base/dynamic/discovery.py#L271
                    # kubernetes python sdk will always update cache even if the resourcePart is not updated
                    # in order to avoid unnecessary disk writing, only update cache when resourcePart.resources is set
                    if resourcePart.resources:
                        self._cache["resources"][prefix][group][version] = resourcePart
                        self.__update_cache = True
                return self.__search(parts[1:], resourcePart.resources, reqParams)
            elif isinstance(resourcePart, dict):
                # In this case parts [0] will be a specified prefix, group, version
                # as we recurse
                return self.__search(parts[1:], resourcePart, reqParams + [part])
            else:  # noqa
                if parts[1] != "*" and isinstance(parts[1], dict):
                    for _resource in resourcePart:
                        for term, value in parts[1].items():
                            if getattr(_resource, term) == value:
                                return [_resource]
                    return []
                else:
                    return resourcePart
        else:
            matches = []
            for key in resources.keys():  # noqa: SIM118
                matches.extend(self.__search([key] + parts[1:], resources, reqParams))
            return matches

```
</details>

---


### 模块: apiserver/paasng/paas_wl/workloads/networking/egress/management/commands/region_gen_state.py


#### handle

**复杂度分数**: 12
**严重程度**: warning
**行数**: 82-123 (共 42 行, 0 行注释)

**函数签名**:
```python
def handle ( self, *args, **options ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def handle(self, *args, **options):
        all_regions = set(Cluster.objects.values_list("region", flat=True))
        if options["region"]:
            if options["region"] not in all_regions:
                print(f'{options["region"]} is not a valid region name')
                sys.exit(1)

            regions = [options["region"]]
        else:
            regions = list(all_regions)

        ignore_labels = options["ignore_labels"]
        ignore_labels = [value.split("=") for value in ignore_labels]
        if any(len(label) != 2 for label in ignore_labels):
            raise ValueError("Invalid label given!")

        if not options["include_masters"]:
            ignore_labels.append(("node-role.kubernetes.io/master", "true"))

        cluster_name = options.get("cluster_name")

        for region in regions:
            logger.debug(f"Make scheduler client from region: {region}")
            for cluster in Cluster.objects.filter(region=region):
                if cluster_name and cluster.name != cluster_name:
                    continue

                logger.info(f"Will generate state for [{region}/{cluster.name}]...")
                if not options.get("no_input") and input("Confirm? (y/n, default: n) ").lower() != "y":
                    continue

                try:
                    client = get_client_by_cluster_name(cluster_name=cluster.name)

                    logger.info(f"Generating state for [{region} - {cluster.name}]...")
                    state = generate_state(region, cluster.name, client, ignore_labels=ignore_labels)

                    logger.info("Syncing the state to nodes...")
                    sync_state_to_nodes(client, state)
                except Exception:
                    logger.exception("Unable to generate state")
                    continue

```
</details>

---


### 模块: apiserver/paasng/paasng/accessories/log/management/commands/batch_disable_mount_hostpath.py


#### handle

**复杂度分数**: 11
**严重程度**: warning
**行数**: 66-105 (共 40 行, 5 行注释)

**函数签名**:
```python
def handle ( self, app_code, region, cluster_name, all_clusters, edge_disable, dry_run, *args, **options ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def handle(self, app_code, region, cluster_name, all_clusters, edge_disable, dry_run, *args, **options):
        style_func = self.style.SUCCESS if not dry_run else self.style.NOTICE
        qs = self.validate_params(app_code, region, cluster_name, all_clusters)
        for application in qs:
            can_use_bklog = True
            pending_latest_config = []
            for module in application.modules.all():
                for env in module.envs.all():  # type: ModuleEnvironment
                    env_can_use_bklog = self.check_env_status(env)
                    if env_can_use_bklog:
                        if not dry_run:
                            # 日志平台采集配置已下发大于 14 天, 可停用平台日志采集链路
                            # Note: 需等待用户下次触发配置时，才会真正生效
                            wl_app = env.wl_app
                            # warning: latest_config 是 property, 必须拿出来后才能修改
                            latest_config = wl_app.latest_config
                            latest_config.mount_log_to_host = False
                            if edge_disable:
                                latest_config.save(update_fields=["mount_log_to_host", "updated"])
                            else:
                                pending_latest_config.append(latest_config)
                        self.stdout.write(
                            "disable hostpath log collector for "
                            f"Application<{application.code}> "
                            f"Module<{module.name}>"
                            f"Env<{env.environment}>",
                            style_func=style_func,
                        )
                    # 必须所有环境都满足条件, 才允许使用日志平台查询
                    can_use_bklog = can_use_bklog and env_can_use_bklog
            if can_use_bklog:
                if not dry_run:
                    application.feature_flag.set_feature(AppFeatureFlagConst.ENABLE_BK_LOG_COLLECTOR, True)
                    for cfg in pending_latest_config:
                        cfg.save(update_fields=["mount_log_to_host", "updated"])

                self.stdout.write(
                    f"switch log query to bk-log index for Application<{application.code}>",
                    style_func=style_func,
                )

```
</details>

---


### 模块: apiserver/paasng/paasng/accessories/servicehub/management/commands/update_legacy_rabbitmq.py


#### handle

**复杂度分数**: 11
**严重程度**: warning
**行数**: 37-76 (共 40 行, 0 行注释)

**函数签名**:
```python
def handle ( self, name, region, id, dry_run, *args, **options ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def handle(self, name, region, id, dry_run, *args, **options):
        services = models.Service.objects.all()
        if name:
            services = services.filter(name=name)

        if region:
            services = services.filter(region=region)

        if id:
            services = services.filter(pk=id)

        service = services.get()

        for i in models.ServiceInstance.objects.filter(service=service):
            if not i.credentials:
                print(f"credentials of instance {i.pk} is None")
                continue

            credentials = json.loads(i.credentials)

            if not credentials:
                print(f"credentials of instance {i.pk} is empty")
                continue

            to_update = {}
            prefix = "LEGACY_"

            for k, v in credentials.items():
                if not k.startswith(prefix):
                    to_update[f"{prefix}{k}"] = v

            if not to_update:
                continue

            print(f"updating instance {i.pk}")
            credentials.update(to_update)

            if not dry_run:
                i.credentials = json.dumps(credentials)
                i.save(update_fields=["credentials"])

```
</details>

---


### 模块: apiserver/paasng/paasng/accessories/services/providers/sentry/client.py


#### _request

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 34-73 (共 40 行, 1 行注释)

**函数签名**:
```python
def _request ( self, method, path, data, timeout = 10 ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def _request(self, method, path, data, timeout=10):
        url = "{base_url}{path}".format(base_url=self.base_url, path=path)
        headers = self.headers
        try:
            if method == "GET":
                resp = requests.get(url=url, headers=headers, params=data, timeout=timeout)
            elif method == "HEAD":
                resp = requests.head(url=url, headers=headers, timeout=timeout)
            elif method == "POST":
                resp = requests.post(url=url, headers=headers, json=data, timeout=timeout)
            elif method == "DELETE":
                resp = requests.delete(url=url, headers=headers, json=data)
            elif method == "PUT":
                resp = requests.put(url=url, headers=headers, json=data)
            else:
                return False, None
        except requests.exceptions.RequestException:
            logger.exception("Request sentry failed, connection exception")
            raise RequestSentryAPIFail("Request sentry failed, connection exception")

        resp_json = {}
        try:
            if resp.status_code != 204:
                resp_json = resp.json()
        except Exception:
            logger.exception("Failed to request sentry, failed to parse json")

        # 409, conflict means already created
        if resp.status_code not in (200, 201, 202, 204, 409):
            logger.exception(
                "Request sentry failed, return status is not 20X/409[method=%s, url=%s, data=%s, status=%s, resp=%s]",
                method,
                url,
                data,
                resp.status_code,
                resp_json,
            )
            return False, resp_json

        return True, resp_json

```
</details>

---


### 模块: apiserver/paasng/paasng/accessories/smart_advisor/tagging.py


#### dig_tags_local_repo

**复杂度分数**: 11
**严重程度**: warning
**行数**: 36-68 (共 33 行, 6 行注释)
**描述**: Dig a local repo to find proper tags for this module

**函数签名**:
```python
def dig_tags_local_repo ( local_path: str | PathLike ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
def dig_tags_local_repo(local_path: str | PathLike):
    """Dig a local repo to find proper tags for this module"""
    p = Path(local_path)
    if not p.exists():
        return []

    tags = []
    # Python detection
    req_file = p / "requirements.txt"

    # Because we will read the requirements.txt file later, we should ensure it exists
    # and is not a symlink because the file was created by the user.
    if req_file.exists() and not req_file.is_symlink():
        tags.append(force_tag("app-pl:python"))
        # Set `errors="ignore"` to ignore non-ascii characters when the file is using a
        # different encoding other than utf-8.
        requirements_txt = req_file.read_text(encoding="utf-8", errors="ignore")
        for pkg_name in ("celery", "django", "gunicorn", "blueapps"):
            if py_module_in_requirements(pkg_name, requirements_txt):
                tags.append(force_tag("app-sdk:{}".format(pkg_name)))

    # golang and other language detection is still naive, need improve
    for fname in p.iterdir():
        if fname.name.endswith(".go"):
            tags.append(force_tag("app-pl:go"))
            break
        if fname.name.endswith(".php"):
            tags.append(force_tag("app-pl:php"))
            break

    if (p / "package.json").exists() and (p / "index.js").exists():
        tags.append(force_tag("app-pl:nodejs"))
    return tags

```
</details>

---


### 模块: apiserver/paasng/paasng/bk_plugins/pluginscenter/releases/executor.py


#### back_to_previous_stage

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 121-157 (共 37 行, 0 行注释)
**描述**: 回滚当前发布阶段至上一阶段: 重置 release.current_stage, 并将 release.current_stage 设置成 previous_stage

**函数签名**:
```python
def back_to_previous_stage ( self, operator: str ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def back_to_previous_stage(self, operator: str):
        """回滚当前发布阶段至上一阶段: 重置 release.current_stage, 并将 release.current_stage 设置成 previous_stage
        ITSM 单据审批中不能返回上一步
        """
        if self.release.status == constants.PluginReleaseStatus.SUCCESSFUL:
            raise error_codes.CANNOT_ROLLBACK_CURRENT_STEP.f(_("当前发布流程已结束"))

        if not self.release.retryable:
            raise error_codes.CANNOT_ROLLBACK_CURRENT_STEP.f(
                _("当前插件类型不支持重置历史版本, 如需发布请创建新的版本")
            )

        current_stage = self.release.current_stage
        if (
            current_stage.invoke_method == constants.ReleaseStageInvokeMethod.ITSM
            and current_stage.status in constants.PluginReleaseStatus.running_status()
        ):
            raise error_codes.CANNOT_ROLLBACK_CURRENT_STEP.f(_("请先撤回审批单据, 再返回上一步"))
        if (
            current_stage.invoke_method == constants.ReleaseStageInvokeMethod.DEPLOY_API
            and current_stage.status in constants.PluginReleaseStatus.running_status()
        ):
            raise error_codes.CANNOT_ROLLBACK_CURRENT_STEP.f(_("请等待部署完成, 再返回上一步"))

        previous_stage_id = None
        for stage in self.release.stages_shortcut:
            if stage.id == current_stage.stage_id:
                break
            previous_stage_id = stage.id

        if previous_stage_id is None:
            raise error_codes.CANNOT_ROLLBACK_CURRENT_STEP
        previous_stage = self.release.all_stages.get(stage_id=previous_stage_id)
        current_stage.reset()
        self.release.current_stage = previous_stage
        self.release.status = constants.PluginReleaseStatus.PENDING
        self.release.save()

```
</details>

---


### 模块: apiserver/paasng/paasng/bk_plugins/pluginscenter/serializers.py


#### make_release_validator

**复杂度分数**: 17
**严重程度**: high_risk
**行数**: 480-554 (共 75 行, 4 行注释)
**描述**: make a validator to validate ReleaseVersion object

**函数签名**:
```python
def make_release_validator ( plugin: PluginInstance, version_rule: PluginReleaseVersionRule, release_type: str, revision_policy: str, revision_type: str ) :
```

**消息**: Complexity 17 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
def make_release_validator(  # noqa: C901
    plugin: PluginInstance,
    version_rule: PluginReleaseVersionRule,
    release_type: str,
    revision_policy: str,
    revision_type: str,
):
    """make a validator to validate ReleaseVersion object"""

    def validate_semver(version: str, previous_version_str: Optional[str], semver_type: SemverAutomaticType):
        try:
            parsed_version = semver.VersionInfo.parse(version)
            previous_version = semver.VersionInfo.parse(previous_version_str or "0.0.0")
        except ValueError as e:
            raise ValidationError(str(e))
        if semver_type == SemverAutomaticType.MAJOR:
            computational_revision = previous_version.bump_major()
        elif semver_type == SemverAutomaticType.MINOR:
            computational_revision = previous_version.bump_minor()
        else:
            computational_revision = previous_version.bump_patch()
        if computational_revision != parsed_version:
            raise ValidationError(
                {
                    "revision": _("版本号不符合，下一个 {label} 版本是 {revision}").format(
                        label=SemverAutomaticType.get_choice_label(semver_type), revision=computational_revision
                    )
                }
            )
        return True

    def validate_release_policy(
        plugin: PluginInstance, release_type: str, revision_policy: str, source_version_name: str
    ):
        """Plugin version release rules, e.g., cannot release already published versions."""
        policy = REVISION_POLICIES.get(revision_policy)
        if not policy:
            return True

        source_version_exists = PluginRelease.objects.filter(
            plugin=plugin, source_version_name=source_version_name, type=release_type, **policy["filter"]
        ).exists()
        if source_version_exists:
            raise policy["error"]  # type: ignore[misc]
        return True

    def validator(self, attrs: Dict):
        if revision_type == PluginRevisionType.TESTED_VERSION and (not attrs["release_id"]):
            raise ValidationError(_("使用测试版本发布时必须传参数: release_id"))

        version = attrs["version"]
        source_version_type = attrs["source_version_type"]
        source_version_name = attrs["source_version_name"]
        source_hash = get_source_hash_by_plugin_version(
            plugin, source_version_type, source_version_name, revision_type, attrs["release_id"]
        )

        if version_rule == PluginReleaseVersionRule.AUTOMATIC:
            validate_semver(version, self.context["previous_version"], SemverAutomaticType(attrs["semver_type"]))
        elif version_rule == PluginReleaseVersionRule.REVISION and version != source_version_name:
            raise ValidationError(_("版本号必须与代码分支一致"))
        elif version_rule == PluginReleaseVersionRule.COMMIT_HASH and version != source_hash:  # noqa: SIM102
            raise ValidationError(_("版本号必须与提交哈希一致"))
        elif version_rule == PluginReleaseVersionRule.BRANCH_TIMESTAMP and (
            not version.startswith(source_version_name)
        ):  # noqa: SIM102
            raise ValidationError(_("版本号必须以代码分支开头"))

        if revision_policy:
            validate_release_policy(plugin, release_type, revision_policy, source_version_name)
        attrs["source_hash"] = source_hash
        attrs.pop("release_id")
        return attrs

    return validator

```
</details>

---


#### validator

**复杂度分数**: 11
**严重程度**: warning
**行数**: 526-552 (共 27 行, 2 行注释)

**函数签名**:
```python
def validator ( self, attrs: Dict ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def validator(self, attrs: Dict):
        if revision_type == PluginRevisionType.TESTED_VERSION and (not attrs["release_id"]):
            raise ValidationError(_("使用测试版本发布时必须传参数: release_id"))

        version = attrs["version"]
        source_version_type = attrs["source_version_type"]
        source_version_name = attrs["source_version_name"]
        source_hash = get_source_hash_by_plugin_version(
            plugin, source_version_type, source_version_name, revision_type, attrs["release_id"]
        )

        if version_rule == PluginReleaseVersionRule.AUTOMATIC:
            validate_semver(version, self.context["previous_version"], SemverAutomaticType(attrs["semver_type"]))
        elif version_rule == PluginReleaseVersionRule.REVISION and version != source_version_name:
            raise ValidationError(_("版本号必须与代码分支一致"))
        elif version_rule == PluginReleaseVersionRule.COMMIT_HASH and version != source_hash:  # noqa: SIM102
            raise ValidationError(_("版本号必须与提交哈希一致"))
        elif version_rule == PluginReleaseVersionRule.BRANCH_TIMESTAMP and (
            not version.startswith(source_version_name)
        ):  # noqa: SIM102
            raise ValidationError(_("版本号必须以代码分支开头"))

        if revision_policy:
            validate_release_policy(plugin, release_type, revision_policy, source_version_name)
        attrs["source_hash"] = source_hash
        attrs.pop("release_id")
        return attrs

```
</details>

---


### 模块: apiserver/paasng/paasng/infras/perm_insure/views_perm.py


#### check_drf_view_perm

**复杂度分数**: 12
**严重程度**: warning
**行数**: 85-122 (共 38 行, 6 行注释)
**描述**: Check if a DRF view function has configured permission properly.

**函数签名**:
```python
def check_drf_view_perm ( view_func, is_admin42: bool ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
def check_drf_view_perm(view_func, is_admin42: bool):
    """Check if a DRF view function has configured permission properly.

    :raise ImproperlyConfigured: When the permission is not configured properly.
    """
    view_cls = view_func.cls
    # Skip if the view class is marked as excluded
    if view_cls.__name__ in INSURE_CHECKING_EXCLUDED_VIEWS:
        return

    if issubclass(view_cls, ViewSetMixin):
        # Some viewset doesn't configure `permission_classes`, them are protected by
        # decorators instead, make the check pass when all methods have been protected.
        unprotected_actions = get_unprotected_actions(view_func)
        if view_func.actions and not unprotected_actions:
            return
    elif issubclass(view_cls, APIView):
        # When the view class is a DRF APIView, only check the `permission_classes` property.
        pass
    else:
        raise TypeError("not a valid DRF View")

    enabled_perm = view_cls.permission_classes

    # When the view class is admin42 view, it should contain site_perm_class in permission_classes
    if is_admin42:  # noqa: SIM102
        if not any(is_admin42_permission(p) for p in enabled_perm):
            raise ImproperlyConfigured(
                f"The view class {view_cls} has no site_perm_class configured in permission_classes"
            )

    if not enabled_perm or (len(enabled_perm) == 1 and enabled_perm[0].__name__ == "IsAuthenticated"):
        name = view_cls if not unprotected_actions else f"{view_cls} - {unprotected_actions!r}"
        raise ImproperlyConfigured(
            "The view class {} has no extra permission_classes configured other than "
            "`IsAuthenticated`, this may be a bug and lead to a permission leak error, add "
            "the view name to `perm_insure.conf.INSURE_CHECKING_EXCLUDED_VIEWS` if this is intended.".format(name)
        )

```
</details>

---


### 模块: apiserver/paasng/paasng/misc/audit/views.py


#### filter_queryset

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 50-77 (共 28 行, 1 行注释)

**函数签名**:
```python
def filter_queryset ( self, queryset ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        slz = AppOperationRecordFilterSlZ(data=self.request.query_params)
        slz.is_valid(raise_exception=True)
        query_params = slz.validated_data

        if target := query_params.get("target"):
            queryset = queryset.filter(target=target)
        if operation := query_params.get("operation"):
            queryset = queryset.filter(operation=operation)
        if access_type := query_params.get("access_type"):
            queryset = queryset.filter(access_type=access_type)
        # result_code 的可选值包含 0，需要进行显式检查
        if "result_code" in query_params:
            result_code = query_params["result_code"]
            queryset = queryset.filter(result_code=result_code)
        if module_name := query_params.get("module_name"):
            queryset = queryset.filter(module_name=module_name)
        if environment := query_params.get("environment"):
            queryset = queryset.filter(environment=environment)
        if start_time := query_params.get("start_time"):
            queryset = queryset.filter(created__gte=start_time)
        if end_time := query_params.get("end_time"):
            queryset = queryset.filter(created__lte=end_time)
        if operator := query_params.get("operator"):
            operator = user_id_encoder.encode(settings.USER_TYPE, operator)
            queryset = queryset.filter(user=operator)
        return queryset

```
</details>

---


### 模块: apiserver/paasng/paasng/platform/applications/models.py


#### filter_queryset

**复杂度分数**: 12
**严重程度**: warning
**行数**: 141-180 (共 40 行, 1 行注释)
**描述**: Filter applications by given parameters

**函数签名**:
```python
def filter_queryset ( cls, queryset: QuerySet, include_inactive = False, regions = None, languages = None, search_term = '', has_deployed: Optional[bool] = None, source_origin: Optional[SourceOrigin] = None, type_: Optional[ApplicationType] = None, order_by: Optional[List] = None, market_enabled: Optional[bool] = None ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def filter_queryset(
        cls,
        queryset: QuerySet,
        include_inactive=False,
        regions=None,
        languages=None,
        search_term="",
        has_deployed: Optional[bool] = None,
        source_origin: Optional[SourceOrigin] = None,
        type_: Optional[ApplicationType] = None,
        order_by: Optional[List] = None,
        market_enabled: Optional[bool] = None,
    ):
        """Filter applications by given parameters"""
        if order_by is None:
            order_by = []
        if queryset.model is not Application:
            raise ValueError("BaseApplicationFilter only support to filter Application")

        if regions:
            queryset = queryset.filter_by_regions(regions)
        if languages:
            queryset = queryset.filter_by_languages(languages)
        if search_term:
            queryset = queryset.search_by_code_or_name(search_term)
        if has_deployed is not None:
            # When application has been deployed, it's `last_deployed_date` will not be empty.
            queryset = queryset.filter(last_deployed_date__isnull=not has_deployed)
        if not include_inactive:
            queryset = queryset.only_active()
        if order_by:
            queryset = cls.process_order_by(order_by, queryset)
        if source_origin:
            queryset = queryset.filter_by_source_origin(source_origin)
        if market_enabled is not None:
            queryset = queryset.filter(market_config__enabled=market_enabled)
        if type_ is not None:
            queryset = queryset.filter(type=type_)
        return queryset

```
</details>

---


### 模块: apiserver/paasng/paasng/platform/bkapp_model/importer.py


#### import_bkapp_spec_entity

**复杂度分数**: 13
**严重程度**: warning
**行数**: 71-124 (共 54 行, 6 行注释)
**描述**: Import a BkApp spec entity to the current module, will overwrite existing data.

**函数签名**:
```python
def import_bkapp_spec_entity ( module: Module, spec_entity: v1alpha2_entity.BkAppSpec, manager: FieldMgrName ) :
```

**消息**: Complexity 13 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
def import_bkapp_spec_entity(module: Module, spec_entity: v1alpha2_entity.BkAppSpec, manager: FieldMgrName):
    """Import a BkApp spec entity to the current module, will overwrite existing data.

    :param module: The module object.
    :param spec_entity: BkApp spec entity.
    :param manager: The manager performing this action.
    """
    env_vars = []
    mounts = spec_entity.mounts or []
    if configuration := spec_entity.configuration:
        env_vars = configuration.env or []

    # Initialize a bunch of overlay data
    overlay_replicas: NotSetType | list = NOTSET
    overlay_res_quotas: NotSetType | list = NOTSET
    overlay_env_vars: NotSetType | list = NOTSET
    overlay_autoscaling: NotSetType | list = NOTSET
    overlay_mounts: NotSetType | list = NOTSET
    if not isinstance(spec_entity.env_overlay, NotSetType):
        eo = spec_entity.env_overlay
        if eo:
            # Turn `None` value into empty list
            overlay_replicas = [] if eo.replicas is None else eo.replicas
            overlay_res_quotas = [] if eo.res_quotas is None else eo.res_quotas
            overlay_env_vars = [] if eo.env_variables is None else eo.env_variables
            overlay_autoscaling = [] if eo.autoscaling is None else eo.autoscaling
            overlay_mounts = [] if eo.mounts is None else eo.mounts

    # Run sync functions
    sync_processes(module, processes=spec_entity.processes, manager=manager)
    if build := spec_entity.build:
        sync_build(module, build)

    sync_hooks(module, spec_entity.hooks, manager)

    # sync_env_vars doesn't need to use manager parameter because the data will
    # only be manged by a single manger.
    sync_env_vars(module, env_vars, overlay_env_vars)

    if addons := spec_entity.addons:
        sync_addons(module, addons)
    if mounts or overlay_mounts:
        sync_mounts(module, mounts, overlay_mounts, manager)

    sync_svc_discovery(module, spec_entity.svc_discovery, manager)
    sync_domain_resolution(module, spec_entity.domain_resolution, manager)
    sync_observability(module, spec_entity.observability)

    # NOTE: Must import the processes first to create the ModuleProcessSpec objs
    sync_env_overlays_replicas(module, overlay_replicas, manager, spec_entity.processes)
    sync_env_overlays_res_quotas(module, overlay_res_quotas, manager, spec_entity.processes)
    sync_env_overlays_autoscalings(module, overlay_autoscaling, manager, spec_entity.processes)

    clean_empty_overlays(module)

```
</details>

---


### 模块: apiserver/paasng/paasng/platform/bkapp_model/manifest.py


#### apply_to_proc_overlay

**复杂度分数**: 11
**严重程度**: warning
**行数**: 204-247 (共 44 行, 1 行注释)
**描述**: Apply changes to the sub-fields in the 'envOverlay' field which is related

**函数签名**:
```python
def apply_to_proc_overlay ( self, model_res: crd.BkAppResource, module: Module ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def apply_to_proc_overlay(self, model_res: crd.BkAppResource, module: Module):
        """Apply changes to the sub-fields in the 'envOverlay' field which is related
        with process, fields list:

        - replicas
        - autoscaling
        - resQuotas
        """
        overlay = model_res.spec.envOverlay
        if not overlay:
            overlay = crd.EnvOverlay()

        for proc_spec in ModuleProcessSpec.objects.filter(module=module).order_by("created"):
            for item in ProcessSpecEnvOverlay.objects.filter(proc_spec=proc_spec):
                # Only include item that have different values
                if item.target_replicas is not None and item.target_replicas != proc_spec.target_replicas:
                    overlay.append_item(
                        "replicas",
                        crd.ReplicasOverlay(
                            envName=item.environment_name, process=proc_spec.name, count=item.target_replicas
                        ),
                    )
                if item.scaling_config and item.autoscaling and item.scaling_config != proc_spec.scaling_config:
                    overlay.append_item(
                        "autoscaling",
                        crd.AutoscalingOverlay(
                            envName=item.environment_name,
                            process=proc_spec.name,
                            minReplicas=item.scaling_config.min_replicas,
                            maxReplicas=item.scaling_config.max_replicas,
                            policy=item.scaling_config.policy,
                        ),
                    )
                if item.plan_name and item.plan_name != proc_spec.plan_name:
                    overlay.append_item(
                        "resQuotas",
                        crd.ResQuotaOverlay(
                            envName=item.environment_name,
                            process=proc_spec.name,
                            plan=self.get_quota_plan(item.plan_name),
                        ),
                    )

        model_res.spec.envOverlay = overlay

```
</details>

---


### 模块: apiserver/paasng/paasng/platform/declarative/application/validations/v3.py


#### to_internal_value

**复杂度分数**: 11
**严重程度**: warning
**行数**: 122-155 (共 34 行, 4 行注释)

**函数签名**:
```python
def to_internal_value ( self, data: Dict ) -> ApplicationDesc :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def to_internal_value(self, data: Dict) -> ApplicationDesc:
        attrs = super().to_internal_value(data)
        attrs["name_en"] = attrs.get("name_en") or attrs["name_zh_cn"]

        modules_list = attrs.pop("modules")
        # 调整 modules 字段格式从 list 到 dict
        attrs["modules"] = {module_desc.name: module_desc for module_desc in modules_list}
        # 验证至少有一个主模块
        has_default = False
        for module_desc in modules_list:
            if module_desc.is_default:
                if has_default:
                    raise serializers.ValidationError({"modules": _("一个应用只能有一个主模块")})
                has_default = True
        if not has_default:
            raise serializers.ValidationError({"modules": _("一个应用必须有一个主模块")})

        # 校验 shared_from 的模块是否存在
        for idx, module_desc in enumerate(modules_list):
            for svc in module_desc.services:
                if svc.shared_from and svc.shared_from not in attrs["modules"]:
                    raise serializers.ValidationError(
                        {f"modules[{idx}].spec.addons": _("提供共享增强服务的模块不存在")}
                    )

        # 处理额外字段
        attrs.setdefault("plugins", [])
        if self.context.get("app_version"):
            attrs["plugins"].append({"type": AppDescPluginType.APP_VERSION, "data": self.context.get("app_version")})

        if self.context.get("spec_version"):
            attrs["spec_version"] = self.context["spec_version"]

        return ApplicationDesc(instance_existed=bool(self.instance), **attrs)

```
</details>

---


### 模块: apiserver/paasng/paasng/platform/engine/deploy/bg_build/executors.py


#### _start_following_logs

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 333-373 (共 41 行, 7 行注释)
**描述**: 通过轮询，检查流水线是否执行完成，并逐批获取执行日志

**函数签名**:
```python
def _start_following_logs ( self, pb: entities.PipelineBuild ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def _start_following_logs(self, pb: entities.PipelineBuild):
        """通过轮询，检查流水线是否执行完成，并逐批获取执行日志"""
        time_started = time.time()

        while time.time() - time_started < _BUILD_PROCESS_TIMEOUT:
            time.sleep(self.polling_result_interval)
            self.stream.write_message("Pipeline is running, please wait patiently...")

            try:
                build_status = self.ctl.retrieve_build_status(pb)
            except BkCIGatewayServiceError:
                logger.exception(f"call bk_ci pipeline for build status and logs failed during deploy[{self.bp}]")
                raise

            # 到达稳定状态后，可以退出轮询
            if build_status.status in [
                PipelineBuildStatus.SUCCEED,
                PipelineBuildStatus.FAILED,
                PipelineBuildStatus.CANCELED,
            ]:
                logger.info("break poll loop with pipeline build status: %s", build_status.status)
                break

        # Q：为什么不在轮询过程中，按分块获取日志（做流式效果）
        # A：经测试，通过获取 log_num 再分块获取日志，会丢失部分日志，这是难以接受的，
        #    因此采用最后全量拉日志的方式，轮询过程中添加日志提示用户耐心等待流水线执行
        start_following = False
        for log in self.ctl.retrieve_full_log(pb).logs:
            # 注：丢弃流水线/构建机启动相关日志，只保留构建组件的日志
            if not (log.tag.startswith("e-") and log.jobId == self.bk_ci_pipeline_job_id):
                continue

            # 只保留 [Install plugin] 到 [Output] 之间的日志，不需要其他的
            if "[Output]" in log.message:
                break
            if "[Install plugin]" in log.message:
                start_following = True

            if start_following:
                # 移除蓝盾日志中的级别 Tag，如 ##[error], ##[info] 等
                self.stream.write_message(re.sub(self.bk_ci_log_level_tag_regex, "", log.message))

```
</details>

---


### 模块: apiserver/paasng/paasng/platform/evaluation/evaluators.py


#### _evaluate_by_user_visit

**复杂度分数**: 15
**严重程度**: warning
**行数**: 156-196 (共 41 行, 5 行注释)

**函数签名**:
```python
def _evaluate_by_user_visit ( self ) :
```

**消息**: Complexity 15 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def _evaluate_by_user_visit(self):
        # 无访问记录，说明是不活跃应用
        if not (self.report.pv and self.report.uv):
            self.result.issue_type = OperationIssueType.UNVISITED
            self.result.issues.append(f"应用最近 {self.visit_summary.time_range} 没有访问记录")

        # 环境纬度评估
        for mod_name, mod in self.visit_summary.modules.items():
            for env_name, env in mod.envs.items():
                # 这个环境没有运行中的进程的，跳过
                env_res_summary = self.res_summary.modules[mod_name].envs[env_name]
                if not (env_res_summary.cpu_requests and env_res_summary.mem_requests):
                    continue

                # 有访问记录，跳过
                if env.pv and env.uv:
                    continue

                env_result = self.result.modules[mod_name].envs[env_name]
                env_result.issue_type = OperationIssueType.UNVISITED
                env_result.issues.append(f"该环境最近 {self.visit_summary.time_range} 没有访问记录")

                # 如果没有访问量，且检测到资源使用率基本没有波动，则说明该环境闲置（没有后台任务）
                is_low_cpu_usage, any_proc_running = True, False
                for proc in self.res_summary.modules[mod_name].envs[env_name].procs:
                    if not (proc.quota and proc.cpu):
                        continue

                    any_proc_running = True
                    if proc.cpu.max / proc.quota.limits.cpu > 0.01:
                        is_low_cpu_usage = False
                        break

                if is_low_cpu_usage and any_proc_running:
                    env_result.issues.append(f"CPU 使用率低于 1% 且近 {self.res_summary.time_range} 使用量没有波动")
                    env_result.issue_type = OperationIssueType.IDLE
                    self.result.issue_type = OperationIssueType.IDLE
                    self.result.issues.append(
                        f"模块 {mod_name} 环境 {env_name} 近 {self.visit_summary.time_range} 没有访问记录"
                        + f" 且 近 {self.res_summary.time_range} CPU 使用率低于 1%"
                    )

```
</details>

---


### 模块: apiserver/paasng/paasng/platform/evaluation/tasks.py


#### _update_or_create_operation_report

**复杂度分数**: 17
**严重程度**: high_risk
**行数**: 52-124 (共 73 行, 11 行注释)

**函数签名**:
```python
def _update_or_create_operation_report ( app: Application ) :
```

**消息**: Complexity 17 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
def _update_or_create_operation_report(app: Application):
    res_summary = AppResQuotaCollector(app).collect()
    # 统计资源配额 & 实际使用情况
    cpu_requests, mem_requests, cpu_limits, mem_limits = 0, 0, 0, 0
    cpu_usage_avg_val, mem_usage_avg_val = 0.0, 0.0
    for module in res_summary.modules.values():
        for procs in [
            module.envs[AppEnvName.STAG].procs,
            module.envs[AppEnvName.PROD].procs,
        ]:
            for proc in procs:
                # 没有副本数量的忽略
                if not proc.replicas:
                    continue

                if proc.quota:
                    cpu_requests += proc.replicas * proc.quota.requests.cpu
                    mem_requests += proc.replicas * proc.quota.requests.memory
                    cpu_limits += proc.replicas * proc.quota.limits.cpu
                    mem_limits += proc.replicas * proc.quota.limits.memory
                if proc.cpu:
                    cpu_usage_avg_val += proc.replicas * proc.cpu.avg
                if proc.memory:
                    mem_usage_avg_val += proc.replicas * proc.memory.avg

    # 统计近 30 天总访问量 & 用户数
    total_pv, total_uv = 0, 0
    visit_summary = AppUserVisitCollector(app).collect()
    for mod in visit_summary.modules.values():
        for env in [mod.envs[AppEnvName.STAG], mod.envs[AppEnvName.PROD]]:
            total_pv += env.pv
            total_uv += env.uv

    # 统计部署情况
    deploy_summary = AppDeploymentCollector(app).collect()

    # 最近部署记录
    latest_deployment = Deployment.objects.filter(app_environment__application=app).order_by("-created").first()
    # 最新的操作记录
    latest_operation = Operation.objects.filter(application=app).order_by("-created").first()

    defaults = {
        # 资源使用
        "cpu_requests": cpu_requests,
        "mem_requests": mem_requests,
        "cpu_limits": cpu_limits,
        "mem_limits": mem_limits,
        "cpu_usage_avg": round(cpu_usage_avg_val / cpu_limits, 4) if cpu_limits else 0,
        "mem_usage_avg": round(mem_usage_avg_val / mem_limits, 4) if mem_limits else 0,
        "res_summary": asdict(res_summary),
        # 用户活跃度
        "pv": total_pv,
        "uv": total_uv,
        "visit_summary": asdict(visit_summary),
        # 部署情况
        "latest_deployed_at": latest_deployment.created if latest_deployment else None,
        "latest_deployer": get_username_by_bkpaas_user_id(latest_deployment.operator) if latest_deployment else None,
        "latest_operated_at": latest_operation.created if latest_operation else None,
        "latest_operator": latest_operation.get_operator() if latest_operation else None,
        "latest_operation": latest_operation.get_operate_display() if latest_operation else None,
        "deploy_summary": asdict(deploy_summary),
        # 应用开发者 / 管理员
        "administrators": fetch_role_members(app.code, ApplicationRole.ADMINISTRATOR),
        "developers": fetch_role_members(app.code, ApplicationRole.DEVELOPER),
        "collected_at": timezone.now(),
    }
    report, _ = AppOperationReport.objects.update_or_create(app=app, defaults=defaults)

    # 根据采集结果对应用运营情况进行评估
    evaluate_result = AppOperationEvaluator(report, res_summary, visit_summary, deploy_summary).evaluate()
    report.issue_type = evaluate_result.issue_type
    report.evaluate_result = asdict(evaluate_result)
    report.save(update_fields=["issue_type", "evaluate_result"])

```
</details>

---


#### send_idle_email_to_app_developers

**复杂度分数**: 12
**严重程度**: warning
**行数**: 168-234 (共 67 行, 4 行注释)
**描述**: 发送应用闲置模块邮件给应用管理员/开发者

**函数签名**:
```python
def send_idle_email_to_app_developers ( app_codes: List[str], only_specified_users: List[str], exclude_specified_users: List[str] ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
def send_idle_email_to_app_developers(
    app_codes: List[str], only_specified_users: List[str], exclude_specified_users: List[str]
):
    """发送应用闲置模块邮件给应用管理员/开发者"""
    reports = AppOperationReport.objects.filter(issue_type=OperationIssueType.IDLE)
    if app_codes:
        reports = reports.filter(app__code__in=app_codes)

    if not reports.exists():
        logger.info("no idle app reports, skip current notification task")
        return

    waiting_notify_usernames = set()
    for r in reports:
        waiting_notify_usernames.update(r.administrators)
        waiting_notify_usernames.update(r.developers)

    # 如果特殊指定用户，只发送给指定的用户
    if only_specified_users:
        waiting_notify_usernames &= set(only_specified_users)

    # 如果特别排除指定用户，则不发送给这些用户
    if exclude_specified_users:
        waiting_notify_usernames -= set(exclude_specified_users)

    total_cnt, succeed_cnt = len(waiting_notify_usernames), 0
    failed_usernames = []

    task = AppOperationEmailNotificationTask.objects.create(
        total_count=total_cnt, notification_type=EmailNotificationType.IDLE_APP_MODULE_ENVS
    )
    for idx, username in enumerate(waiting_notify_usernames):
        filters = ApplicationPermission().gen_develop_app_filters(username)
        app_codes = Application.objects.filter(is_active=True).filter(filters).values_list("code", flat=True)

        # 从缓存拿刚刚退出的应用 code exclude 掉，避免出现退出用户组，权限中心权限未同步的情况
        if just_leave_app_codes := JustLeaveAppManager(username).list():
            app_codes = [c for c in app_codes if c not in just_leave_app_codes]

        user_idle_app_reports = reports.filter(app__code__in=app_codes)

        if not user_idle_app_reports.exists():
            total_cnt -= 1
            logger.info("no idle app reports, skip notification to %s", username)
            continue

        try:
            AppOperationReportNotifier().send(user_idle_app_reports, EmailReceiverType.APP_DEVELOPER, [username])
        except Exception:
            failed_usernames.append(username)
            logger.exception("failed to send idle module envs email to %s", username)

        succeed_cnt += 1
        # 通知完所有用户需要较长时间，因此每隔一段时间更新下进度
        if idx % 20 == 0:
            task.succeed_count = succeed_cnt
            task.failed_count = len(failed_usernames)
            task.save(update_fields=["succeed_count", "failed_count"])

    task.total_count = total_cnt
    task.succeed_count = succeed_cnt
    task.failed_count = len(failed_usernames)
    task.failed_usernames = failed_usernames
    task.status = BatchTaskStatus.FINISHED
    task.end_at = timezone.now()
    task.save(update_fields=["total_count", "succeed_count", "failed_count", "failed_usernames", "status", "end_at"])

```
</details>

---


### 模块: apiserver/paasng/paasng/platform/modules/manager.py


#### initialize_app_model_resource

**复杂度分数**: 11
**严重程度**: warning
**行数**: 257-318 (共 62 行, 5 行注释)

**函数签名**:
```python
def initialize_app_model_resource ( self, bkapp_spec: Dict[str, Any] ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def initialize_app_model_resource(self, bkapp_spec: Dict[str, Any]):
        """
        Initialize the AppModelResource and import the bkapp_spec into the corresponding bkapp models

        :param bkapp_spec: validated_data from CreateBkAppSpecSLZ
        """
        # 只有云原生应用需要在创建模块后初始化 AppModelResource
        if self.application.type != ApplicationType.CLOUD_NATIVE:
            return

        if not bkapp_spec or bkapp_spec["build_config"].build_method != RuntimeType.CUSTOM_IMAGE:
            return

        # 镜像交付的应用需要将模块配置导入到 DB(bkapp model)
        # 导入 BuildConfig
        build_config = bkapp_spec["build_config"]
        config_obj = BuildConfig.objects.get_or_create_by_module(self.module)
        build_params = {
            "image_repository": build_config.image_repository,
            "image_credential_name": None,
        }
        if image_credential := build_config.image_credential:
            build_params["image_credential_name"] = image_credential["name"]
        update_build_config_with_method(config_obj, build_method=build_config.build_method, data=build_params)

        processes = [
            Process(
                name=proc_spec["name"],
                command=proc_spec["command"],
                args=proc_spec["args"],
                target_port=proc_spec.get("port", None),
                probes=proc_spec.get("probes", None),
                services=proc_spec.get("services", None),
            )
            for proc_spec in bkapp_spec["processes"]
        ]

        sync_processes(self.module, processes, manager=FieldMgrName.WEB_FORM)

        # 更新环境覆盖&更新可观测功能配置
        metrics = []
        for proc_spec in bkapp_spec["processes"]:
            if env_overlay := proc_spec.get("env_overlay"):
                for env_name, proc_env_overlay in env_overlay.items():
                    ProcessSpecEnvOverlay.objects.save_by_module(
                        self.module, proc_spec["name"], env_name, **proc_env_overlay
                    )

            if metric := get_items(proc_spec, ["monitoring", "metric"]):
                metrics.append({"process": proc_spec["name"], **metric})

        monitoring = Monitoring(metrics=metrics) if metrics else None
        ObservabilityConfig.objects.upsert_by_module(self.module, monitoring)

        # 导入 hook 配置
        if hook := bkapp_spec.get("hook"):
            self.module.deploy_hooks.enable_hook(
                type_=hook["type"],
                proc_command=hook.get("proc_command"),
                command=hook.get("command"),
                args=hook.get("args"),
            )

```
</details>

---


### 模块: apiserver/paasng/paasng/utils/patternmatcher.py


#### compile

**复杂度分数**: 16
**严重程度**: high_risk
**行数**: 66-133 (共 68 行, 12 行注释)

**函数签名**:
```python
def compile ( self, sl: str ) :
```

**消息**: Complexity 16 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def compile(self, sl: str):  # noqa: C901, PLR0915, PLR0912
        reg_str = "^"
        pattern = self.cleaned_pattern
        esc_sl = sl
        if esc_sl == "\\":
            esc_sl += "\\"

        self.match_type = MatchType.Excat
        scan = Scanner(pattern)
        i = 0
        while not scan.is_eof():
            ch = scan.next()
            if ch == "*":
                if scan.peek() == "*":
                    # is some flavor of "**"
                    scan.next()
                    # Treat **/ as ** so eat the "/"
                    if scan.peek() == sl:
                        scan.next()
                    if scan.is_eof():
                        # is "**EOF" - to align with .gitignore just accept all
                        if self.match_type == MatchType.Excat:
                            self.match_type = MatchType.Prefix
                        else:
                            reg_str += ".*"
                            self.match_type = MatchType.Regexp
                    else:
                        # is "**"
                        # Note that this allows for any # of /'s (even 0) because
                        # the .* will eat everything, even /'s
                        reg_str += "(.*" + esc_sl + ")?"
                        self.match_type = MatchType.Regexp
                    if i == 0:
                        self.match_type = MatchType.Suffix
                else:
                    reg_str += "[^" + esc_sl + "]*"
                    self.match_type = MatchType.Regexp
            elif ch == "?":
                # "?" is any char except "/"
                reg_str += "[^" + esc_sl + "]"
                self.match_type = MatchType.Regexp
            elif should_escape(ch):
                # Escape some regexp special chars that have no meaning in golang's filepath.Match
                reg_str += "\\" + ch
            elif ch == "\\":
                if sl == "\\":
                    # On windows map "\" to "\\", meaning an escaped backslash,
                    # and then just continue because filepath.Match on
                    # Windows doesn't allow escaping at all
                    reg_str += esc_sl
                    i += 1
                    continue
                if not scan.is_eof():
                    reg_str += "\\" + scan.next()
                    self.match_type = MatchType.Regexp
                else:
                    reg_str += "\\"
            elif ch in ("[", "]"):
                reg_str += ch
                self.match_type = MatchType.Regexp
            else:
                reg_str += ch
            i += 1
        if self.match_type != MatchType.Regexp:
            return
        reg_str += "$"
        self.regexp = re.compile(reg_str)
        return

```
</details>

---


### 模块: apiserver/paasng/tests/api/bkapp_model/test_bkapp_model.py


#### test_retrieve

**复杂度分数**: 14
**严重程度**: warning
**行数**: 53-77 (共 25 行, 0 行注释)

**函数签名**:
```python
def test_retrieve ( self, api_client, bk_cnative_app, bk_module, web, celery_worker ) :
```

**消息**: Complexity 14 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_retrieve(self, api_client, bk_cnative_app, bk_module, web, celery_worker):
        url = f"/api/bkapps/applications/{bk_cnative_app.code}/modules/{bk_module.name}/bkapp_model/process_specs/"
        resp = api_client.get(url)
        data = resp.json()
        metadata = data["metadata"]
        proc_specs = data["proc_specs"]
        assert metadata["allow_multiple_image"] is False
        assert len(proc_specs) == 2
        assert proc_specs[0]["name"] == "web"
        assert proc_specs[0]["image"] == "example.com/foo"
        assert proc_specs[0]["command"] == ["python"]
        assert proc_specs[0]["args"] == ["-m", "http.server"]
        assert proc_specs[0]["env_overlay"]["stag"]["scaling_config"] == {
            "min_replicas": 1,
            "max_replicas": 1,
            "metrics": [{"type": "Resource", "metric": "cpuUtilization", "value": "85"}],
            "policy": "default",
        }
        assert proc_specs[0]["services"] is None

        assert proc_specs[1]["name"] == "worker"
        assert proc_specs[1]["image"] == "example.com/foo"
        assert proc_specs[1]["command"] == ["celery"]
        assert proc_specs[1]["args"] == []
        assert proc_specs[1]["services"] is None

```
</details>

---


#### test_save

**复杂度分数**: 21
**严重程度**: critical
**行数**: 79-212 (共 134 行, 2 行注释)

**函数签名**:
```python
def test_save ( self, api_client, bk_cnative_app, bk_module, web, celery_worker ) :
```

**消息**: Complexity 21 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_save(self, api_client, bk_cnative_app, bk_module, web, celery_worker):
        G(
            ProcessSpecEnvOverlay,
            proc_spec=web,
            environment_name="stag",
            autoscaling=True,
            scaling_config={
                "min_replicas": 1,
                "max_replicas": 5,
                "policy": "default",
            },
        )
        assert web.get_autoscaling("stag")
        url = f"/api/bkapps/applications/{bk_cnative_app.code}/modules/{bk_module.name}/bkapp_model/process_specs/"
        probes_cfg = {
            "liveness": {
                "exec": {"command": ["/bin/bash", "-c", "echo hello"]},
                "http_get": None,
                "tcp_socket": None,
                "initial_delay_seconds": 5,
                "timeout_seconds": 5,
                "period_seconds": 5,
                "success_threshold": 1,
                "failure_threshold": 3,
            },
            "readiness": {
                "exec": None,
                "tcp_socket": None,
                "http_get": {
                    "port": 8080,
                    "host": "bk.example.com",
                    "path": "/healthz",
                    "http_headers": [{"name": "XXX", "value": "YYY"}],
                    "scheme": "HTTPS",
                },
                "initial_delay_seconds": 15,
                "timeout_seconds": 60,
                "period_seconds": 10,
                "success_threshold": 1,
                "failure_threshold": 5,
            },
            "startup": {
                "exec": None,
                "http_get": None,
                "tcp_socket": {"port": 8080, "host": "bk.example.com"},
                "initial_delay_seconds": 5,
                "timeout_seconds": 15,
                "period_seconds": 2,
                "success_threshold": 1,
                "failure_threshold": 5,
            },
        }
        request_data = [
            {
                "name": "web",
                # 设置 image 字段不会生效
                "image": "python:latest",
                "command": ["python", "-m"],
                "args": ["http.server"],
                "port": 5000,
                "env_overlay": {
                    "stag": {
                        "plan_name": "default",
                        "target_replicas": 2,
                        "autoscaling": False,
                    }
                },
                "probes": probes_cfg,
            },
            {
                "name": "beat",
                "command": ["python", "-m"],
                "args": ["celery", "beat"],
                "env_overlay": {
                    "stag": {
                        "plan_name": "default",
                        "target_replicas": 1,
                    },
                    "prod": {
                        "plan_name": "default",
                        "target_replicas": 1,
                        "autoscaling": True,
                        "scaling_config": {
                            "min_replicas": 1,
                            "max_replicas": 5,
                            # NOTE: The metrics field will be ignored by the backend
                            "metrics": [{"type": "Resource", "metric": "cpuUtilization", "value": "70"}],
                        },
                    },
                },
                "probes": {
                    "liveness": None,
                    "readiness": None,
                    "startup": None,
                },
            },
        ]
        resp = api_client.post(url, data={"proc_specs": request_data})
        data = resp.json()

        proc_specs = data["proc_specs"]

        assert ModuleProcessSpec.objects.filter(module=bk_module).count() == 2
        assert len(proc_specs) == 2

        assert proc_specs[0]["name"] == "web"
        assert proc_specs[0]["image"] == "example.com/foo"
        assert proc_specs[0]["command"] == ["python", "-m"]
        assert proc_specs[0]["args"] == ["http.server"]
        assert proc_specs[0]["port"] == 5000
        assert proc_specs[0]["env_overlay"]["stag"]["target_replicas"] == 2
        assert not proc_specs[0]["env_overlay"]["stag"]["autoscaling"]
        assert proc_specs[0]["probes"] == probes_cfg

        assert proc_specs[1]["name"] == "beat"
        assert proc_specs[1]["image"] == "example.com/foo"
        assert proc_specs[1]["command"] == ["python", "-m"]
        assert proc_specs[1]["args"] == ["celery", "beat"]
        assert proc_specs[1]["env_overlay"]["prod"]["scaling_config"] == {
            "min_replicas": 1,
            "max_replicas": 5,
            "metrics": [{"type": "Resource", "metric": "cpuUtilization", "value": "85"}],
            "policy": "default",
        }
        assert proc_specs[1]["probes"] == {"liveness": None, "readiness": None, "startup": None}

        spec_obj = ModuleProcessSpec.objects.get(module=bk_module, name="beat")
        assert spec_obj.get_scaling_config("prod") == AutoscalingConfig(
            min_replicas=1,
            max_replicas=5,
            policy="default",
        )
        assert spec_obj.probes == {"liveness": None, "readiness": None, "startup": None}
        assert spec_obj.probes.liveness is None

```
</details>

---


### 模块: apiserver/paasng/tests/api/extensions/test_bkplugins.py


#### test_sync

**复杂度分数**: 11
**严重程度**: warning
**行数**: 75-97 (共 23 行, 0 行注释)

**函数签名**:
```python
def test_sync ( self, bk_plugin_app, sys_api_client ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_sync(self, bk_plugin_app, sys_api_client):
        module = bk_plugin_app.get_default_module()
        assert ConfigVar.objects.filter(module=module).count() == 0
        response = sys_api_client.post(
            f"/sys/api/plugins_center/bk_plugins/{bk_plugin_app.code}/configuration/",
            data=[{"key": "FOO", "value": "foo"}, {"key": "BAR", "value": "bar"}, {"key": "BAZ", "value": "baz"}],
        )
        assert response.status_code == 200
        assert ConfigVar.objects.filter(module=module).count() == 3
        assert ConfigVar.objects.get(module=module, key="FOO").value == "foo"
        assert ConfigVar.objects.get(module=module, key="BAR").value == "bar"
        assert ConfigVar.objects.get(module=module, key="BAZ").value == "baz"
        response = sys_api_client.post(
            f"/sys/api/plugins_center/bk_plugins/{bk_plugin_app.code}/configuration/",
            data=[
                {"key": "FOO", "value": "foo"},
                {"key": "BAR", "value": "BAR"},
            ],
        )
        assert response.status_code == 200
        assert ConfigVar.objects.filter(module=module).count() == 2
        assert ConfigVar.objects.get(module=module, key="FOO").value == "foo"
        assert ConfigVar.objects.get(module=module, key="BAR").value == "BAR"

```
</details>

---


### 模块: apiserver/paasng/tests/api/test_applications.py


#### test_create_with_image

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 493-541 (共 49 行, 0 行注释)
**描述**: 托管方式：仅镜像

**函数签名**:
```python
def test_create_with_image ( self, api_client ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_create_with_image(self, api_client):
        """托管方式：仅镜像"""
        random_suffix = generate_random_string(length=6)
        image_credential_name = generate_random_string(length=6)
        image_repository = "strm/helloworld-http"
        response = api_client.post(
            "/api/bkapps/cloud-native/",
            data={
                "region": settings.DEFAULT_REGION_NAME,
                "code": f"uta-{random_suffix}",
                "name": f"uta-{random_suffix}",
                "bkapp_spec": {
                    "build_config": {
                        "build_method": "custom_image",
                        "image_repository": image_repository,
                        "image_credential": {"name": image_credential_name, "password": "123456", "username": "test"},
                    },
                    "processes": [
                        {
                            "name": "web",
                            "command": ["bash", "/app/start_web.sh"],
                            "env_overlay": {
                                "stag": {"environment_name": "stag", "target_replicas": 1, "plan_name": "2C1G"},
                                "prod": {"environment_name": "prod", "target_replicas": 2, "plan_name": "2C1G"},
                            },
                        }
                    ],
                },
                "source_config": {
                    "source_origin": SourceOrigin.CNATIVE_IMAGE,
                    "source_repo_url": image_repository,
                },
            },
        )
        assert response.status_code == 201, f'error: {response.json()["detail"]}'
        app_data = response.json()["application"]
        assert app_data["type"] == "cloud_native"
        assert app_data["modules"][0]["web_config"]["build_method"] == "custom_image"
        assert app_data["modules"][0]["web_config"]["artifact_type"] == "none"

        module = Module.objects.get(id=app_data["modules"][0]["id"])
        cfg = BuildConfig.objects.get_or_create_by_module(module)
        assert cfg.image_repository == image_repository
        assert cfg.image_credential_name == image_credential_name

        process_spec = ModuleProcessSpec.objects.get(module=module, name="web")
        assert process_spec.command == ["bash", "/app/start_web.sh"]
        assert process_spec.get_target_replicas("stag") == 1
        assert process_spec.get_target_replicas("prod") == 2

```
</details>

---


### 模块: apiserver/paasng/tests/api/test_configvar_by_key.py


#### test_configvar_by_key

**复杂度分数**: 12
**严重程度**: warning
**行数**: 32-92 (共 61 行, 5 行注释)

**函数签名**:
```python
def test_configvar_by_key ( api_client, bk_module, init_env, init_value, update_env, update_value, expected_envs, expected_values ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
def test_configvar_by_key(
    api_client, bk_module, init_env, init_value, update_env, update_value, expected_envs, expected_values
):
    module = bk_module
    env_key = "FOO"
    # 环境准备
    if init_env:
        if init_env == global_env:
            # global 环境的值是 -1
            env_obj = -1
            ConfigVar.objects.create(
                module=module,
                key=env_key,
                environment_id=env_obj,
                value=init_value,
                description="desc",
                is_global=True,
            )
        else:
            env_obj = ApplicationEnvironment.objects.get(module=module, environment=init_env)
            ConfigVar.objects.create(
                module=module, key=env_key, environment=env_obj, value=init_value, description="desc"
            )

    path = f"/api/bkapps/applications/{bk_module.application.code}/modules/{bk_module.name}/config_vars/{env_key}/"
    # 执行 upsert
    resp = api_client.post(
        path,
        data={"environment_name": update_env, "value": update_value, "description": "desc2"},
        format="json",
    )
    assert resp.status_code == 201

    # 查询
    resp = api_client.get(path)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == len(expected_envs)
    env_map = {d["environment_name"]: d["value"] for d in data}
    for env, val in zip(expected_envs, expected_values):
        assert env_map[env] == val

    # 添加对 is_global 的测试
    for item in data:
        if item["environment_name"] == global_env:
            assert item["is_global"] is True
        else:
            assert item["is_global"] is False

```
</details>

---


### 模块: apiserver/paasng/tests/api/test_market.py


#### test_update_market_app

**复杂度分数**: 14
**严重程度**: warning
**行数**: 113-164 (共 52 行, 6 行注释)

**函数签名**:
```python
def test_update_market_app ( self, api_client, bk_app_full ) :
```

**消息**: Complexity 14 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_update_market_app(self, api_client, bk_app_full):
        # 开启了应用市场配置，则测试数据同步
        if getattr(settings, "BK_CONSOLE_DBCONF", None):
            from paasng.accessories.publish.sync_market.handlers import (
                register_app_core_data,
            )

            # 单测为了提高性能, 禁用了 register_app_core_data, 需要主动触发
            register_app_core_data(sender=None, application=bk_app_full)

        # Get the origin product value
        Product.objects.create_default_product(bk_app_full)
        response = api_client.get(reverse("api.market.products.detail", args=(bk_app_full.code,)), format="json")
        data = response.json()

        # Change name to a new value
        target_name = uuid.uuid4().hex[:20]
        data["name"] = target_name
        data["width"] = 841
        data["contact"] = "nobody;nobody1"
        data["open_mode"] = OpenMode.NEW_TAB.value
        # 可见范围
        data["visiable_labels"] = [
            {"id": 100, "type": "department", "name": "xx部门"},
            {"id": 2001, "type": "user", "name": "user1"},
        ]
        put_response = api_client.put(
            reverse("api.market.products.detail", args=(bk_app_full.code,)), data=data, format="json"
        )
        assert put_response.status_code == 200
        product = Product.objects.get(code=bk_app_full.code)
        assert product.name == target_name
        assert product.displayoptions.width == 841
        assert product.displayoptions.contact == "nobody;nobody1"
        assert product.displayoptions.open_mode == OpenMode.NEW_TAB.value
        # 开启了应用市场配置，则测试数据同步
        if getattr(settings, "BK_CONSOLE_DBCONF", None):
            from paasng.accessories.publish.sync_market.managers import AppManger
            from paasng.core.core.storages.sqlalchemy import console_db

            session = console_db.get_scoped_session()
            console_app = AppManger(session).get(bk_app_full.code)
            assert console_app.width == product.displayoptions.width == 841
            assert console_app.open_mode == product.displayoptions.open_mode
            try:
                assert json.loads(console_app.extra)["contact"] == product.displayoptions.contact
            except AttributeError:
                logger.info("The extra attribute of the application does not exist, skip verification")
            try:
                assert console_app.visiable_labels == product.transform_visiable_labels()
            except AttributeError:
                logger.info("The visiable_labels attribute of the application does not exist, skip verification")

```
</details>

---


### 模块: apiserver/paasng/tests/api/test_modules.py


#### test_create_with_image

**复杂度分数**: 11
**严重程度**: warning
**行数**: 120-171 (共 52 行, 0 行注释)
**描述**: 托管方式：仅镜像

**函数签名**:
```python
def test_create_with_image ( self, bk_cnative_app, api_client ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_create_with_image(self, bk_cnative_app, api_client):
        """托管方式：仅镜像"""
        random_suffix = generate_random_string(length=6)
        image_repository = "strm/helloworld-http"
        response = api_client.post(
            f"/api/bkapps/cloud-native/{bk_cnative_app.code}/modules/",
            data={
                "name": f"uta-{random_suffix}",
                "source_config": {
                    "source_origin": SourceOrigin.CNATIVE_IMAGE,
                    "source_repo_url": "strm/helloworld-http",
                },
                "bkapp_spec": {
                    "build_config": {"build_method": "custom_image", "image_repository": image_repository},
                    "processes": [
                        {
                            "name": "web",
                            "command": ["bash", "/app/start_web.sh"],
                            "env_overlay": {
                                "stag": {"environment_name": "stag", "target_replicas": 1, "plan_name": "2C1G"},
                                "prod": {"environment_name": "prod", "target_replicas": 2, "plan_name": "2C1G"},
                            },
                            "port": 30000,
                        }
                    ],
                    "hook": {
                        "type": "pre-release-hook",
                        "enabled": True,
                        "command": ["/bin/bash"],
                        "args": ["-c", "echo 'hello world'"],
                    },
                },
            },
        )
        assert response.status_code == 201, f'error: {response.json()["detail"]}'
        module_data = response.json()["module"]
        assert module_data["web_config"]["build_method"] == "custom_image"
        assert module_data["web_config"]["artifact_type"] == "none"
        module = Module.objects.get(id=module_data["id"])

        cfg = BuildConfig.objects.get_or_create_by_module(module)
        assert cfg.image_repository == image_repository

        process_spec = ModuleProcessSpec.objects.get(module=module, name="web")
        assert process_spec.command == ["bash", "/app/start_web.sh"]
        assert process_spec.port == 30000
        assert process_spec.get_target_replicas("stag") == 1
        assert process_spec.get_target_replicas("prod") == 2

        deploy_hook = ModuleDeployHook.objects.get(module=module, type=DeployHookType.PRE_RELEASE_HOOK)
        assert deploy_hook.command == ["/bin/bash"]
        assert deploy_hook.args == ["-c", "echo 'hello world'"]

```
</details>

---


### 模块: apiserver/paasng/tests/paas_wl/bk_app/deploy/app_res/test_controllers.py


#### test_deploy_processes

**复杂度分数**: 11
**严重程度**: warning
**行数**: 142-170 (共 29 行, 3 行注释)

**函数签名**:
```python
def test_deploy_processes ( self, wl_app, web_process ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_deploy_processes(self, wl_app, web_process):
        handler = ProcessesHandler.new_by_app(wl_app)
        with patch("paas_wl.infras.resources.base.kres.NameBasedOperations.replace_or_patch") as kd, patch(
            "paas_wl.workloads.networking.ingress.managers.service.service_kmodel"
        ) as ks, patch("paas_wl.workloads.networking.ingress.managers.base.ingress_kmodel") as ki:
            ks.get.side_effect = AppEntityNotFound()
            ki.get.side_effect = AppEntityNotFound()

            handler.deploy([web_process])

            # Check deployment resource
            assert kd.called
            deployment_args, deployment_kwargs = kd.call_args_list[0]
            assert deployment_kwargs.get("name") == f"{region}-{wl_app.name}-web-python-deployment"
            assert deployment_kwargs.get("body")
            assert deployment_kwargs.get("namespace") == wl_app.namespace

            # Check service resource
            assert ks.get.called
            assert ks.create.called
            proc_service = ks.create.call_args_list[0][0][0]
            assert proc_service.name == f"{region}-{wl_app.name}-web"

            # Check ingress resource
            assert ks.get.called
            assert ki.save.called
            proc_ingress = ki.save.call_args_list[0][0][0]
            assert proc_ingress.name == f"{region}-{wl_app.name}"

```
</details>

---


### 模块: apiserver/paasng/tests/paas_wl/bk_app/dev_sandbox/test_controller.py


#### test_deploy_success

**复杂度分数**: 12
**严重程度**: warning
**行数**: 115-145 (共 31 行, 0 行注释)

**函数签名**:
```python
def test_deploy_success ( self, controller, bk_app, module_name, user_dev_wl_app ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_deploy_success(self, controller, bk_app, module_name, user_dev_wl_app):
        sandbox_entity_in_cluster = controller.sandbox_mgr.get(user_dev_wl_app, user_dev_wl_app.scheduler_safe_name)
        assert sandbox_entity_in_cluster.runtime.envs == {
            "FOO": "test",
            "SOURCE_FETCH_METHOD": "BK_REPO",
            "SOURCE_FETCH_URL": "example.com",
            "WORKSPACE": "/cnb/devsandbox/src",
        }
        assert sandbox_entity_in_cluster.status.replicas == 1
        assert sandbox_entity_in_cluster.status.ready_replicas in [0, 1]
        assert sandbox_entity_in_cluster.status.to_health_phase() in ["Progressing", "Healthy"]

        code_editor_entity_in_cluster = controller.code_editor_mgr.get(
            user_dev_wl_app, get_code_editor_name(user_dev_wl_app)
        )
        assert code_editor_entity_in_cluster.runtime.envs == {"PASSWORD": "123456", "START_DIR": "/home/coder/project"}
        assert code_editor_entity_in_cluster.status.replicas == 1
        assert code_editor_entity_in_cluster.status.ready_replicas in [0, 1]
        assert code_editor_entity_in_cluster.status.to_health_phase() in ["Progressing", "Healthy"]

        service_entity_in_cluster = controller.dev_sandbox_svc_mgr.get(
            user_dev_wl_app, get_dev_sandbox_service_name(user_dev_wl_app)
        )
        assert service_entity_in_cluster.name == get_dev_sandbox_service_name(user_dev_wl_app)

        ingress_entity_in_cluster = controller.ingress_mgr.get(user_dev_wl_app, get_ingress_name(user_dev_wl_app))
        assert ingress_entity_in_cluster.name == get_ingress_name(user_dev_wl_app)
        assert ingress_entity_in_cluster.domains[0].host == get_sub_domain_host(
            bk_app.code, user_dev_wl_app, module_name
        )

```
</details>

---


### 模块: apiserver/paasng/tests/paas_wl/bk_app/processes/test_models.py


#### test_switch

**复杂度分数**: 16
**严重程度**: high_risk
**行数**: 57-102 (共 46 行, 4 行注释)

**函数签名**:
```python
def test_switch ( self, wl_app ) :
```

**消息**: Complexity 16 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_switch(self, wl_app):
        # init data
        mgr = ProcessSpecManager(wl_app)
        mgr.sync([ProcessTmpl(name="web", command="foo", replicas=2), ProcessTmpl(name="celery", command="foo")])

        web = ProcessSpec.objects.get(engine_app=wl_app, name="web")
        assert web.target_replicas == 2
        assert not web.autoscaling
        assert web.scaling_config is None

        # switch to autoscaling
        mgr.sync(
            [
                ProcessTmpl(
                    name="web",
                    command="foo",
                    replicas=2,
                    autoscaling=True,
                    scaling_config=AutoscalingConfig(min_replicas=1, max_replicas=3, policy="default"),
                ),
                ProcessTmpl(name="celery", command="foo"),
            ]
        )
        web.refresh_from_db()
        assert web.target_replicas == 2
        assert web.autoscaling
        assert web.scaling_config is not None
        assert web.scaling_config.min_replicas == 1
        assert web.scaling_config.max_replicas == 3
        assert web.scaling_config.policy == "default"

        # rollback
        mgr.sync(
            [
                ProcessTmpl(name="web", command="foo", replicas=2, autoscaling=False),
                ProcessTmpl(name="celery", command="foo"),
            ]
        )
        web.refresh_from_db()
        assert web.target_replicas == 2
        assert not web.autoscaling
        # sync 时未提供 scaling_config, 不会设置为 None
        assert web.scaling_config is not None
        assert web.scaling_config.min_replicas == 1
        assert web.scaling_config.max_replicas == 3
        assert web.scaling_config.policy == "default"

```
</details>

---


#### test_sync

**复杂度分数**: 11
**严重程度**: warning
**行数**: 106-156 (共 51 行, 0 行注释)

**函数签名**:
```python
def test_sync ( self, wl_app ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_sync(self, wl_app):
        mgr = ProcessProbeManager(wl_app)
        mgr.sync(
            [
                ProcessTmpl(
                    name="web",
                    command="/bin/start.sh",
                    probes=ProbeSet(
                        liveness=Probe(exec=ExecAction(command=["/bin/healthz.sh"])),
                        readiness=Probe(tcp_socket=TCPSocketAction(port=8080, host="127.0.0.1")),
                    ),
                ),
                ProcessTmpl(
                    name="celery",
                    command="/bin/start_celery.sh",
                    probes=ProbeSet(
                        startup=Probe(http_get=HTTPGetAction(port=8080, path="/healthz", host="127.0.0.1")),
                    ),
                ),
            ]
        )

        probes = ProcessProbe.objects.filter(app=wl_app)
        assert probes.count() == 3
        assert probes.filter(process_type="web").count() == 2
        assert probes.filter(process_type="celery").count() == 1

        mgr.sync(
            [
                ProcessTmpl(
                    name="web",
                    command="foo",
                    probes=ProbeSet(
                        liveness=Probe(http_get=HTTPGetAction(port=8080, path="/healthz")),
                        readiness=Probe(tcp_socket=TCPSocketAction(port=8080)),
                        startup=Probe(exec=ExecAction(command=["/bin/healthz.sh"])),
                    ),
                )
            ]
        )
        probes = ProcessProbe.objects.filter(app=wl_app, process_type="web")
        assert probes.count() == 3
        probe = probes.filter(probe_type=ProbeType.LIVENESS).first()
        assert probe is not None
        assert probe.success_threshold == 1
        assert probe.failure_threshold == 3
        assert probe.probe_handler.http_get.port == 8080
        assert probe.probe_handler.http_get.path == "/healthz"

        mgr.sync([ProcessTmpl(name="web", command="foo", probes=None)])
        assert not ProcessProbe.objects.filter(app=wl_app).exists()

```
</details>

---


### 模块: apiserver/paasng/tests/paas_wl/bk_app/processes/test_processes.py


#### testlist_gen_cnative_process_specs

**复杂度分数**: 20
**严重程度**: high_risk
**行数**: 35-84 (共 50 行, 2 行注释)

**函数签名**:
```python
def testlist_gen_cnative_process_specs (  ) :
```

**消息**: Complexity 20 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
def testlist_gen_cnative_process_specs():
    specs = gen_cnative_process_specs(
        BkAppResource(
            metadata={"name": "test"},
            spec={
                "processes": [
                    {"name": "web", "resQuotaPlan": "4C2G"},
                    {
                        "name": "worker",
                        "resQuotaPlan": "default",
                        "autoscaling": {"minReplicas": 1, "maxReplicas": 3, "policy": "default"},
                    },
                ],
                "envOverlay": {
                    "replicas": [{"process": "worker", "count": 0, "envName": "stag"}],
                    "autoscaling": [
                        {
                            "process": "worker",
                            "minReplicas": 3,
                            "maxReplicas": 5,
                            "envName": "stag",
                            "policy": "default",
                        }
                    ],
                },
            },
        ),
        "stag",
    )

    assert specs[0].name == "web"
    assert specs[0].plan_name == "4C2G"
    assert specs[0].target_replicas == 1
    assert specs[0].autoscaling is False
    assert specs[0].scaling_config is None
    assert specs[0].resource_limit == {"cpu": "4000m", "memory": "2048Mi"}
    assert specs[0].resource_limit_quota == {"cpu": 4000, "memory": 2048}
    assert specs[0].resource_requests == {"cpu": "200m", "memory": "1024Mi"}
    assert specs[0].target_status == "start"

    assert specs[1].name == "worker"
    assert specs[1].plan_name == "default"
    assert specs[1].target_replicas == 0
    assert specs[1].autoscaling is True
    assert specs[1].scaling_config["min_replicas"] == 3  # type: ignore
    assert specs[1].scaling_config["max_replicas"] == 5  # type: ignore
    assert specs[1].resource_limit == {"cpu": "4000m", "memory": "1024Mi"}
    assert specs[1].resource_limit_quota == {"cpu": 4000, "memory": 1024}
    assert specs[1].resource_requests == {"cpu": "200m", "memory": "256Mi"}
    assert specs[1].target_status == "stop"

```
</details>

---


### 模块: apiserver/paasng/tests/paas_wl/infras/cluster/test_commands.py


#### test_init_cluster

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 47-74 (共 28 行, 0 行注释)

**函数签名**:
```python
def test_init_cluster ( https_enabled, expect ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
def test_init_cluster(https_enabled, expect):
    os.environ["PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT"] = https_enabled

    call_command("initial_default_cluster")

    cluster = Cluster.objects.get(name="default-main")

    ingress_config = cluster.ingress_config
    assert ingress_config.app_root_domains[0].https_enabled is expect
    assert ingress_config.sub_path_domains[0].https_enabled is expect
    assert ingress_config.app_root_domains[0].name == "apps1.example.com"
    assert ingress_config.sub_path_domains[0].name == "apps2.example.com"
    assert ingress_config.port_map.http == 880
    assert ingress_config.port_map.https == 8443
    assert cluster.default_tolerations == [
        {"effect": "NoSchedule", "key": "dedicated", "operator": "Equal", "value": "bkSaas"}
    ]
    assert cluster.default_node_selector == {"dedicated": "bkSaas"}
    urls = APIServer.objects.filter(cluster=cluster).values_list("host", flat=True)
    assert set(urls) == {"https://kubernetes.default.svc.cluster.localroot", "https://10.0.0.1"}

```
</details>

---


### 模块: apiserver/paasng/tests/paas_wl/infras/cluster/test_models.py


#### test_domains

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 130-143 (共 14 行, 0 行注释)

**函数签名**:
```python
def test_domains ( self, region ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_domains(self, region):
        ingress_config = {"app_root_domains": ["foo.com", {"name": "bar.com"}, {"name": "baz.com", "reserved": True}]}
        c: Cluster = Cluster.objects.create(region=region, name="dft", is_default=True, ingress_config=ingress_config)
        c.refresh_from_db()
        assert isinstance(c.ingress_config, IngressConfig)
        assert len(c.ingress_config.app_root_domains) == 3
        assert all(isinstance(domain, Domain) for domain in c.ingress_config.app_root_domains)

        assert c.ingress_config.app_root_domains[0].name == "foo.com"
        assert c.ingress_config.app_root_domains[0].reserved is False
        assert c.ingress_config.app_root_domains[1].name == "bar.com"
        assert c.ingress_config.app_root_domains[1].reserved is False
        assert c.ingress_config.app_root_domains[2].name == "baz.com"
        assert c.ingress_config.app_root_domains[2].reserved is True

```
</details>

---


### 模块: apiserver/paasng/tests/paas_wl/infras/resource_templates/test_addons.py


#### test_secret_volume

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 81-95 (共 15 行, 0 行注释)

**函数签名**:
```python
def test_secret_volume ( self, wl_app, secret_volume_addon_template ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_secret_volume(self, wl_app, secret_volume_addon_template):
        assert len(AddonManager(wl_app).get_volumes()) == 0

        secret_volume_addon_template.link_to_app(wl_app)
        volumes = AddonManager(wl_app).get_volumes()
        assert len(volumes) == 1
        volume = volumes[0]

        assert volume.name == "secret"
        assert volume.secret
        assert volume.secret.secretName == "the-secret"
        assert len(volume.secret.items) == 1
        assert volume.secret.items[0].key == "a"
        assert volume.secret.items[0].path == "secret/a"
        assert volume.secret.items[0].mode == 0o644

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/accessories/servicehub/remote/test_manager.py


#### test_provision

**复杂度分数**: 13
**严重程度**: warning
**行数**: 110-147 (共 38 行, 0 行注释)
**描述**: Test service instance provision

**函数签名**:
```python
def test_provision ( self, mocked_provision, get_cluster_egress_info, store, bk_module, bk_service_ver, plans ) :
```

**消息**: Complexity 13 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_provision(self, mocked_provision, get_cluster_egress_info, store, bk_module, bk_service_ver, plans):
        """Test service instance provision"""
        get_cluster_egress_info.return_value = {"egress_ips": ["1.1.1.1"], "digest_version": "foo"}
        mgr = RemoteServiceMgr(store=store)
        bk_service_ver.plans = plans

        mgr.bind_service(bk_service_ver, bk_module)
        with mock.patch.object(mgr, "get") as get_service:
            get_service.return_value = bk_service_ver

            for env in bk_module.envs.all():
                expected_plan = plans[1] if env.environment == "prod" and len(plans) == 2 else plans[0]
                for rel in mgr.list_unprovisioned_rels(env.engine_app):
                    assert rel.is_provisioned() is False
                    rel.provision()

                    assert rel.is_provisioned() is True
                    assert str(rel.db_obj.service_id) == bk_service_ver.uuid
                    assert str(rel.db_obj.plan_id) == expected_plan.uuid

                    assert mocked_provision.called
                    assert len(mocked_provision.call_args[0]) == 3
                    assert bool(all(mocked_provision.call_args[0]))
                    assert mocked_provision.call_args[1]["params"]["username"] == rel.db_engine_app.name

```
</details>

---


#### test_bind_with_specs

**复杂度分数**: 11
**严重程度**: warning
**行数**: 224-248 (共 25 行, 0 行注释)

**函数签名**:
```python
def test_bind_with_specs ( self, store, bk_module, bk_service_ver, specs, ok ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_bind_with_specs(self, store, bk_module, bk_service_ver, specs, ok):
        mgr = RemoteServiceMgr(store=store)
        assert mgr.module_is_bound_with(bk_service_ver, bk_module) is False
        if ok:
            mgr.bind_service(bk_service_ver, bk_module, specs=specs.copy())
        else:
            with pytest.raises(BindServiceNoPlansError):
                mgr.bind_service(bk_service_ver, bk_module, specs=specs.copy())
        assert mgr.module_is_bound_with(bk_service_ver, bk_module) is ok

        if ok and specs:
            for env in bk_module.envs.all():
                for rel in mixed_service_mgr.list_unprovisioned_rels(env.engine_app, bk_service_ver):
                    plan = rel.get_plan()
                    assert len(plan.specifications) > 0
                    for k, v in specs.items():
                        assert plan.specifications[k] == v

```
</details>

---


#### test_bound_with_diff_app_zone

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 334-396 (共 63 行, 0 行注释)
**描述**: 测试不同环境绑定不一样的 plan, 依赖 specifications[app_zone]

**函数签名**:
```python
def test_bound_with_diff_app_zone ( self, g_cluster, store, bk_module, bk_service_ver_zone, cluster_name, zone_name, plans, expected_zone_name, ok ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_bound_with_diff_app_zone(
        self,
        g_cluster,
        store,
        bk_module,
        bk_service_ver_zone,
        cluster_name,
        zone_name,
        plans,
        expected_zone_name,
        ok,
    ):
        """测试不同环境绑定不一样的 plan, 依赖 specifications[app_zone]"""
        g_cluster.return_value = Cluster(name=cluster_name, is_default=True)
        mgr = RemoteServiceMgr(store=store)
        bk_service_ver_zone.plans = plans

        assert mgr.module_is_bound_with(bk_service_ver_zone, bk_module) is False

        with override_settings(APP_ZONE_CLUSTER_MAPPINGS={cluster_name: zone_name} if zone_name else {}):
            if ok:
                mgr.bind_service(bk_service_ver_zone, bk_module, {})
            else:
                with pytest.raises(BindServiceNoPlansError):
                    mgr.bind_service(bk_service_ver_zone, bk_module, {})

        assert mgr.module_is_bound_with(bk_service_ver_zone, bk_module) is ok

        if ok:
            with mock.patch.object(store, "get") as get_svc:
                get_svc.return_value = asdict(bk_service_ver_zone)

                for env in bk_module.envs.all():
                    for rel in mgr.list_unprovisioned_rels(env.engine_app, bk_service_ver_zone):
                        plan = rel.get_plan()
                        assert len(plan.specifications) > 0
                        assert plan.specifications["app_zone"] == expected_zone_name

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/release/test_executor.py


#### test_execute_current_stage

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 154-177 (共 24 行, 2 行注释)

**函数签名**:
```python
def test_execute_current_stage ( self, release, stage_class_setter ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_execute_current_stage(self, release, stage_class_setter):
        executor = PluginReleaseExecutor(release)
        assert release.current_stage.status == PluginReleaseStatus.INITIAL
        assert release.current_stage.stage_id == "stage1"
        executor.execute_current_stage("")
        assert release.current_stage.stage_id == "stage1"
        assert release.current_stage.status == PluginReleaseStatus.PENDING

        # 已执行的步骤不能重试执行
        with pytest.raises(APIError) as exc:
            executor.execute_current_stage("")
        assert exc.value.code == error_codes.EXECUTE_STAGE_ERROR.code
        assert (
            exc.value.message
            == error_codes.EXECUTE_STAGE_ERROR.f(_("当前阶段已被执行, 不能重复触发已执行的阶段")).message
        )

        # 测试设置 status 为成功
        release.current_stage.reset()
        stage_class_setter.return_value = build_stage_controller(PluginReleaseStatus.SUCCESSFUL)
        assert release.current_stage.stage_id == "stage1"
        executor.execute_current_stage("")
        assert release.current_stage.stage_id == "stage1"
        assert release.current_stage.status == PluginReleaseStatus.SUCCESSFUL

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/test_integration.py


#### test_release_version

**复杂度分数**: 18
**严重程度**: high_risk
**行数**: 182-312 (共 131 行, 10 行注释)

**函数签名**:
```python
def test_release_version ( self, thirdparty_client, pd, plugin, api_client, iam_policy_client ) :
```

**消息**: Complexity 18 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_release_version(self, thirdparty_client, pd, plugin, api_client, iam_policy_client):
        # 当前插件没有正在执行的正式版本，可创建新的正式版本
        assert (
            PluginRelease.objects.filter(
                plugin=plugin, type="prod", status__in=PluginReleaseStatus.running_status()
            ).count()
            == 0
        )
        with mock.patch("paasng.bk_plugins.pluginscenter.shim.get_plugin_repo_accessor") as get_plugin_repo_accessor:
            get_plugin_repo_accessor().extract_smart_revision.return_value = "hash"
            # 创建正式版本发布
            resp = api_client.post(
                f"/api/bkplugins/{pd.identifier}/plugins/{plugin.id}/releases/",
                data={
                    "type": "prod",
                    "source_version_type": "branch",
                    "source_version_name": "foo",
                    "version": "0.0.1",
                    "comment": "...",
                    "semver_type": "patch",
                },
            )
            assert resp.status_code == 201

        release = PluginRelease.objects.get(plugin=plugin)
        assert release.current_stage.stage_id == "market"
        assert release.current_stage.status == PluginReleaseStatus.PENDING

        # 测试进入下一步(失败)
        resp = api_client.post(f"/api/bkplugins/{pd.identifier}/plugins/{plugin.id}/releases/{release.id}/next/")
        assert resp.status_code == 400
        assert resp.json() == {
            "code": error_codes.EXECUTE_STAGE_ERROR.code,
            "detail": error_codes.EXECUTE_STAGE_ERROR.f(_("当前阶段未执行成功, 不允许进入下一阶段")).message,
        }

        # 测试保存市场信息(完成当前阶段的操作)
        resp = api_client.post(
            f"/api/bkplugins/{pd.identifier}/plugins/{plugin.id}/market/",
            data={"category": "...", "introduction": "...", "description": "...", "contact": "..."},
        )
        assert resp.status_code == 200
        release.refresh_from_db()
        assert release.current_stage.status == PluginReleaseStatus.SUCCESSFUL

        counter = 0

        def deploy_action_side_effect(*args, **kwargs):
            nonlocal counter
            counter += 1
            if counter == 1:
                return {
                    "deploy_id": "...",
                    "status": "pending",
                    "detail": "",
                    "steps": [
                        {
                            "id": "step-1",
                            "name": "步骤1",
                            "status": "pending",
                        }
                    ],
                }
            elif counter == 2:
                return {
                    "deploy_id": "...",
                    "status": "successful",
                    "detail": "",
                    "steps": [
                        {
                            "id": "step-1",
                            "name": "步骤1",
                            "status": "successful",
                        }
                    ],
                }
            else:
                return {"logs": ["1", "2", "3"], "finished": True}

        thirdparty_client.call.side_effect = deploy_action_side_effect

        # 再次测试进入下一步(成功)
        resp = api_client.post(f"/api/bkplugins/{pd.identifier}/plugins/{plugin.id}/releases/{release.id}/next/")
        assert resp.status_code == 200
        release.refresh_from_db()
        release.current_stage.refresh_from_db()
        assert release.current_stage.stage_id == "deploy"
        assert release.current_stage.api_detail == {
            "deploy_id": "...",
            "status": "pending",
            "detail": "",
            "steps": [
                {
                    "id": "step-1",
                    "name": "步骤1",
                    "status": "pending",
                }
            ],
        }

        # 测试前端渲染 stage 的状态
        resp = api_client.get(
            f"/api/bkplugins/{pd.identifier}/plugins/{plugin.id}/releases/{release.id}"
            f"/stages/{release.current_stage.stage_id}/"
        )
        assert resp.json() == {
            "stage_id": "deploy",
            "stage_name": "部署",
            "status": "pending",
            "fail_message": "",
            "invoke_method": "deployAPI",
            "status_polling_method": "api",
            "detail": {
                "steps": [{"id": "step-1", "name": "步骤1", "status": "successful"}],
                "finished": True,
                "logs": ["1", "2", "3"],
            },
        }

        # 测试进入下一步(完成发布)
        # - 渲染 stage 时隐含了更新 status 的操作(后面需要重构成后台任务轮训更新状态)
        release.refresh_from_db()
        assert release.current_stage.status == PluginReleaseStatus.SUCCESSFUL
        # 最后一个步骤成功, 自动部署成功
        assert release.status == PluginReleaseStatus.SUCCESSFUL
        # release 已经成功完成后，再更新 stage 的信息时，不会再触发 release 状态的更新
        release.current_stage.status = PluginReleaseStatus.FAILED
        release.current_stage.operator = "xxxxxx"
        release.current_stage.save(update_fields=["status", "operator"])
        assert release.status == PluginReleaseStatus.SUCCESSFUL

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/infras/accounts/test_models.py


#### test_match_different_scope

**复杂度分数**: 13
**严重程度**: warning
**行数**: 25-48 (共 24 行, 0 行注释)

**函数签名**:
```python
def test_match_different_scope ( self ) :
```

**消息**: Complexity 13 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_match_different_scope(self):
        scope = Scope.parse_from_str("group:v3-test-group")
        assert scope.type == ScopeType.GROUP
        assert scope.item == "v3-test-group"

        scope = Scope.parse_from_str("project:admin/Skynet")
        assert scope.type == ScopeType.PROJECT
        assert scope.item == "admin/Skynet"

        scope = Scope.parse_from_str("project:admin_yu/Sky-net")
        assert scope.type == ScopeType.PROJECT
        assert scope.item == "admin_yu/Sky-net"

        scope = Scope.parse_from_str("user:user")
        assert scope.type == ScopeType.USER
        assert scope.item == "user"

        scope = Scope.parse_from_str("api")
        assert scope.type == ScopeType.USER
        assert scope.item == "user"

        scope = Scope.parse_from_str("")
        assert scope.type == ScopeType.USER
        assert scope.item == "user"

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/misc/monitoring/metrics/test_client.py


#### test_get_by_container_name

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 94-119 (共 26 行, 0 行注释)
**描述**: 测试 对象转换 dict

**函数签名**:
```python
def test_get_by_container_name ( self ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_get_by_container_name(self):
        """测试 对象转换 dict"""
        pr = PromResult.from_resp(raw_resp=self.fake_range_result)
        r1 = pr.get_raw_by_container_name("ieod-bkapp-career-stag")

        assert r1
        assert len(r1["values"]) == 4

        r2 = pr.get_raw_by_container_name("cl5")
        assert r2
        assert len(r2["values"]) == 3

        assert r1["metric"] == {"container_name": "ieod-bkapp-career-stag"}
        assert r1["values"] == [
            [1590000844, "0.0003452615666667214"],
            [1590001444, "0.00040326460000083365"],
            [1590002044, "0.0003675630666667947"],
            [1590003044, "0.0003675630666667947"],
        ]

        r3 = pr.get_raw_by_container_name("cxxxx")
        assert r3 is None

        r4 = pr.get_raw_by_container_name()
        assert r4
        assert len(r4["values"]) == 3

```
</details>

---


#### test_get_by_container_name

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 198-224 (共 27 行, 1 行注释)
**描述**: 测试对象转换为 dict

**函数签名**:
```python
def test_get_by_container_name ( self ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_get_by_container_name(self):
        """测试对象转换为 dict"""
        pr = BkPromResult.from_series(self.fake_range_series)
        r1 = pr.get_raw_by_container_name("celery-proc")

        assert r1
        assert len(r1["values"]) == 4

        r2 = pr.get_raw_by_container_name("web-proc")
        assert r2
        assert len(r2["values"]) == 3

        assert r1["metric"] == {"container_name": "celery-proc"}
        assert r1["values"] == [
            [1673257280, "1073741824"],
            [1673257290, "1073741824"],
            [1673257300, "1073741824"],
            [1673257310, "1073741824"],
        ]

        r3 = pr.get_raw_by_container_name("xxx")
        assert r3 is None

        # 不指定容器名称时，默认返回第一个
        r4 = pr.get_raw_by_container_name()
        assert r4
        assert len(r4["values"]) == 3

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/platform/applications/test_lapp.py


#### test_edit

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 175-244 (共 70 行, 0 行注释)

**函数签名**:
```python
def test_edit ( self, legacy_tag, legacy_app, sys_light_api_client, is_lapp, data, expected ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_edit(self, legacy_tag, legacy_app, sys_light_api_client, is_lapp, data, expected):
        with legacy_db.session_scope() as session:
            AppAdaptor(session).update(code=legacy_app.code, data={"is_lapp": is_lapp})

        data = {
            "light_app_code": legacy_app.code,
            **data,
        }
        if "app_tag" in data:
            data["app_tag"] = legacy_tag.code

        response = sys_light_api_client.patch(
            "/sys/api/light-applications/",
            data=data,
        )
        assert response.status_code == 200

        result = response.json()

        result_data = result.pop("data")
        expected_data = expected.pop("data")
        assert result.pop("bk_error_msg") == expected.pop("bk_error_msg").format(code=legacy_app.code)
        if expected["result"]:
            for k, v in expected_data.items():
                if isinstance(v, str):
                    assert result_data[k] == v.format(**data)
                else:
                    assert result_data[k] == v
        assert result == expected

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_proc_env_overlays.py


#### test_integrated

**复杂度分数**: 11
**严重程度**: warning
**行数**: 69-98 (共 30 行, 3 行注释)

**函数签名**:
```python
def test_integrated ( self, bk_module, proc_web, proc_celery ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_integrated(self, bk_module, proc_web, proc_celery):
        ret = sync_env_overlays_replicas(
            bk_module,
            [
                ReplicasOverlay(env_name="prod", process="web", count=2),
                ReplicasOverlay(env_name="prod", process="worker", count=2),
            ],
            manager=fieldmgr.FieldMgrName.APP_DESC,
        )
        assert ret.updated_num == 1
        assert ret.created_num == 1
        assert ret.deleted_num == 1

        assert get_overlay_obj(proc_web, "prod").target_replicas == 2
        assert get_overlay_obj(proc_celery, "prod").target_replicas == 2
        assert get_overlay_obj(proc_web, "stag").target_replicas is None

        # Set "web" process's field to be manged by a different manager and check if
        # the record should stay intact when getting an `NOTSET` input.
        fieldmgr.FieldManager(bk_module, fieldmgr.f_overlay_replicas(proc_web.name, "prod")).set(
            fieldmgr.FieldMgrName.WEB_FORM
        )
        sync_env_overlays_replicas(bk_module, NOTSET, manager=fieldmgr.FieldMgrName.APP_DESC)
        assert get_overlay_obj(proc_web, "prod").target_replicas == 2
        assert get_overlay_obj(proc_celery, "prod").target_replicas is None
        assert get_overlay_obj(proc_web, "stag").target_replicas is None

        # Manually pass an empty list should reset all records
        sync_env_overlays_replicas(bk_module, [], manager=fieldmgr.FieldMgrName.APP_DESC)
        assert get_overlay_obj(proc_web, "prod").target_replicas is None

```
</details>

---


#### test_normal

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 159-185 (共 27 行, 0 行注释)

**函数签名**:
```python
def test_normal ( self, bk_module, proc_web, proc_celery ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_normal(self, bk_module, proc_web, proc_celery):
        ret = sync_env_overlays_autoscalings(
            bk_module,
            [
                AutoscalingOverlay(env_name="prod", process="web", min_replicas=1, max_replicas=2, policy="default"),
                AutoscalingOverlay(
                    env_name="prod", process="worker", min_replicas=2, max_replicas=5, policy="default"
                ),
            ],
            manager=fieldmgr.FieldMgrName.APP_DESC,
        )
        assert ret.updated_num == 1
        assert ret.created_num == 1
        assert ret.deleted_num == 1

        assert get_overlay_obj(proc_web, "prod").autoscaling
        assert get_overlay_obj(proc_web, "prod").scaling_config == AutoscalingConfig(
            min_replicas=1, max_replicas=2, policy="default"
        )

        assert get_overlay_obj(proc_celery, "prod").autoscaling
        assert get_overlay_obj(proc_celery, "prod").scaling_config == AutoscalingConfig(
            min_replicas=2, max_replicas=5, policy="default"
        )

        assert get_overlay_obj(proc_web, "stag").autoscaling is None
        assert get_overlay_obj(proc_web, "stag").scaling_config is None

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_processes.py


#### test_integrated

**复杂度分数**: 21
**严重程度**: critical
**行数**: 37-99 (共 63 行, 0 行注释)

**函数签名**:
```python
def test_integrated ( self, bk_module, proc_web, proc_celery ) :
```

**消息**: Complexity 21 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_integrated(self, bk_module, proc_web, proc_celery):
        assert ModuleProcessSpec.objects.filter(module=bk_module).count() == 2

        ret = sync_processes(
            bk_module,
            [
                Process(
                    name=proc_web.name,
                    replicas=1,
                    command=["./start.sh"],
                    res_quota_plan="4C1G",
                    target_port=30000,
                    probes=ProbeSet(
                        liveness=Probe(
                            http_get=HTTPGetAction(port="${PORT}", path="/healthz"),
                            initial_delay_seconds=30,
                            timeout_seconds=5,
                            period_seconds=5,
                            success_threshold=1,
                            failure_threshold=3,
                        ),
                        readiness=Probe(tcp_socket=TCPSocketAction(port=30000)),
                    ),
                    services=[ProcService(name="web", target_port=30000, exposed_type={"name": "bk/http"})],
                ),
                Process(
                    name="sleep",
                    replicas=1,
                    command=["bash"],
                    res_quota_plan="4C2G",
                    args=["-c", "100"],
                    proc_command="sleep 100",
                    autoscaling=AutoscalingConfig(min_replicas=2, max_replicas=10, policy="default"),
                ),
            ],
            FieldMgrName.APP_DESC,
        )
        assert ret.updated_num == 1
        assert ret.created_num == 1
        assert ret.deleted_num == 1

        assert ModuleProcessSpec.objects.filter(module=bk_module).count() == 2

        specs = ModuleProcessSpec.objects.filter(module=bk_module, name=proc_web.name)
        assert specs.count() == 1

        spec = specs.first()
        assert spec.port == 30000
        assert spec.probes.liveness.http_get.port == "${PORT}"
        assert spec.probes.liveness.initial_delay_seconds == 30
        assert spec.probes.liveness.period_seconds == 5
        assert spec.probes.readiness.tcp_socket.port == 30000
        assert spec.plan_name == "4C1G"
        assert spec.services[0].exposed_type.name == "bk/http"

        spec = ModuleProcessSpec.objects.get(module=bk_module, name="sleep")
        assert spec.proc_command == "sleep 100"
        assert spec.command is None
        assert spec.target_replicas == 1
        assert spec.scaling_config.max_replicas == 10
        assert spec.scaling_config.min_replicas == 2
        assert spec.plan_name == "4C2G"
        assert spec.services is None

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/platform/engine/deploy/bg_build/test_utils.py


#### test_generate_env_vars_without_metadata

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 39-51 (共 13 行, 0 行注释)

**函数签名**:
```python
def test_generate_env_vars_without_metadata ( self, build_proc, wl_app ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_generate_env_vars_without_metadata(self, build_proc, wl_app):
        env_vars = generate_builder_env_vars(build_proc, {})
        bucket = settings.BLOBSTORE_BUCKET_APP_SOURCE
        cache_path = f"{wl_app.region}/home/{wl_app.name}/cache"
        assert env_vars.pop("TAR_PATH") == f"{bucket}/{build_proc.source_tar_path}", "TAR_PATH 与预期不符"
        assert env_vars.pop("PUT_PATH") == f"{bucket}/{generate_slug_path(build_proc)}", "PUT_PATH 与预期不符"
        assert env_vars.pop("CACHE_PATH") == f"{bucket}/{cache_path}", "CACHE_PATH 与预期不符"
        if settings.BUILD_EXTRA_ENV_VARS:
            for k, v in settings.BUILD_EXTRA_ENV_VARS.items():
                assert env_vars.pop(k) == v, f"{k} 与预期不符"
        if settings.PYTHON_BUILDPACK_PIP_INDEX_URL:
            for k, v in get_envs_from_pypi_url(settings.PYTHON_BUILDPACK_PIP_INDEX_URL).items():
                assert env_vars.pop(k) == v, f"{k} 与预期不符"

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/platform/engine/deploy/test_building.py


#### test_start_normal

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 98-138 (共 41 行, 4 行注释)

**函数签名**:
```python
def test_start_normal ( self, builder_class, bk_deployment_full ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_start_normal(self, builder_class, bk_deployment_full):
        with mock.patch(
            "paasng.platform.engine.configurations.source_file.MetaDataFileReader.get_procfile"
        ) as mocked_get_procfile, mock.patch(
            "paasng.platform.engine.deploy.building.{}.compress_and_upload".format(builder_class.__name__)
        ), mock.patch("paasng.platform.engine.deploy.building.BuildProcessPoller") as mocked_poller, mock.patch(
            "paasng.platform.engine.utils.output.RedisChannelStream"
        ) as mocked_stream, mock.patch(
            "paasng.platform.engine.deploy.building.{}.launch_build_processes".format(builder_class.__name__)
        ) as launch_build_processes:
            mocked_get_procfile.return_value = {"web": "gunicorn"}
            # Return a fake build_process ID
            faked_build_process_id = uuid.uuid4().hex
            launch_build_processes.return_value = faked_build_process_id

            attach_all_phases(sender=bk_deployment_full.app_environment, deployment=bk_deployment_full)
            builder = builder_class.from_deployment_id(bk_deployment_full.id)
            builder.start()

            # Validate deployment data
            deployment = Deployment.objects.get(pk=bk_deployment_full.id)
            assert deployment.status == JobStatus.PENDING.value
            assert deployment.build_process_id.hex == faked_build_process_id
            assert deployment.err_detail is None

            # Validate "start_build_process" arguments
            assert launch_build_processes.called
            (
                source_tar_path,
                bkapp_revision_id,
            ) = launch_build_processes.call_args[0]
            assert source_tar_path != ""
            assert bkapp_revision_id is None

            # Validate other arguments
            assert mocked_stream().write_title.called
            assert mocked_poller.start.called
            assert mocked_poller.start.call_args[0][0] == {
                "build_process_id": deployment.build_process_id.hex,
                "deployment_id": deployment.id,
            }

```
</details>

---


#### test_start_build

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 157-198 (共 42 行, 5 行注释)

**函数签名**:
```python
def test_start_build ( self, builder_class, bk_cnative_app, bk_module_full, bk_deployment_full, model_resource ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_start_build(self, builder_class, bk_cnative_app, bk_module_full, bk_deployment_full, model_resource):
        # Replace the deploy desc handler to skip the metadata reading action
        desc_handler = get_deploy_desc_handler(None, {"web": "gunicorn"})
        with mock.patch(
            "paasng.platform.engine.deploy.building.get_deploy_desc_handler_by_version", return_value=desc_handler
        ), mock.patch(
            "paasng.platform.engine.deploy.building.{}.compress_and_upload".format(builder_class.__name__)
        ), mock.patch("paasng.platform.engine.deploy.building.BuildProcessPoller") as mocked_poller, mock.patch(
            "paasng.platform.engine.utils.output.RedisChannelStream"
        ) as mocked_stream, mock.patch(
            "paasng.platform.engine.deploy.building.{}.launch_build_processes".format(builder_class.__name__)
        ) as launch_build_processes:
            # Return a fake build_process ID
            faked_build_process_id = uuid.uuid4().hex
            launch_build_processes.return_value = faked_build_process_id

            attach_all_phases(sender=bk_deployment_full.app_environment, deployment=bk_deployment_full)
            builder = builder_class.from_deployment_id(bk_deployment_full.id)
            builder.start()

            # Validate deployment data
            deployment = Deployment.objects.get(pk=bk_deployment_full.id)
            assert deployment.status == JobStatus.PENDING.value
            assert deployment.build_process_id.hex == faked_build_process_id
            assert deployment.err_detail is None

            # Validate "start_build_process" arguments
            assert launch_build_processes.called
            (
                source_tar_path,
                bkapp_revision_id,
            ) = launch_build_processes.call_args[0]
            assert source_tar_path != ""
            assert bkapp_revision_id is not None

            # Validate other arguments
            assert mocked_stream().write_title.called
            assert mocked_poller.start.called
            assert mocked_poller.start.call_args[0][0] == {
                "build_process_id": deployment.build_process_id.hex,
                "deployment_id": deployment.id,
            }

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/platform/mgrlegacy/cnative/test_migrators.py


#### test_migrate_and_rollback

**复杂度分数**: 13
**严重程度**: warning
**行数**: 103-136 (共 34 行, 0 行注释)

**函数签名**:
```python
def test_migrate_and_rollback ( self, bk_app, bk_module, image_repository_module, migration_process, cnb_builder, cnb_runner, buildpack, slugbuilder, slugrunner ) :
```

**消息**: Complexity 13 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_migrate_and_rollback(
        self,
        bk_app,
        bk_module,
        image_repository_module,
        migration_process,
        cnb_builder,
        cnb_runner,
        buildpack,
        slugbuilder,
        slugrunner,
    ):
        BuildConfigMigrator(migration_process).migrate()
        config = BuildConfig.objects.get(module=bk_module)
        assert config.buildpacks.filter(id=buildpack.id).exists()
        assert config.buildpack_builder == cnb_builder
        assert config.buildpack_runner == cnb_runner

        image_config = BuildConfig.objects.get(module=image_repository_module)
        assert image_config.image_repository == "https://example.com/image"
        assert image_config.build_method == RuntimeType.CUSTOM_IMAGE.value
        assert Module.objects.get(id=image_repository_module.id).source_origin == SourceOrigin.CNATIVE_IMAGE.value

        BuildConfigMigrator(migration_process).rollback()
        config = BuildConfig.objects.get(module=bk_module)
        assert config.buildpacks.filter(id=buildpack.id).exists()
        assert config.buildpack_builder == slugbuilder
        assert config.buildpack_runner == slugrunner

        image_config = BuildConfig.objects.get(module=image_repository_module)
        assert image_config.image_repository is None
        legacy_image_repository_module = Module.objects.get(id=image_repository_module.id)
        assert legacy_image_repository_module.source_origin == SourceOrigin.IMAGE_REGISTRY.value
        assert legacy_image_repository_module.get_source_obj().get_repo_url() == "https://example.com/image"

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/platform/modules/test_helpers.py


#### test_bind_image

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 35-69 (共 35 行, 2 行注释)

**函数签名**:
```python
def test_bind_image ( bk_module, slugbuilder, slugrunner, slugbuilder_attrs, slugrunner_attrs, ok ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
def test_bind_image(bk_module, slugbuilder, slugrunner, slugbuilder_attrs, slugrunner_attrs, ok):
    for k, v in slugbuilder_attrs.items():
        setattr(slugbuilder, k, v)
    for k, v in slugrunner_attrs.items():
        setattr(slugrunner, k, v)
    slugbuilder.save()
    slugrunner.save()

    binder = ModuleRuntimeBinder(bk_module)
    build_config = bk_module.build_config
    assert build_config.buildpack_builder is None
    assert build_config.buildpack_runner is None
    if ok:
        binder.bind_image(slugrunner, slugbuilder)
        # 必须绑定后再构造 ModuleRuntimeManager, 否则会因为 django 的查询缓存导致无法查询到对象
        manager = ModuleRuntimeManager(bk_module)
        assert manager.get_slug_builder(raise_exception=True) == slugbuilder
        assert manager.get_slug_runner(raise_exception=True) == slugrunner
        # 测试重复绑定
        binder.bind_image(slugrunner, slugbuilder)
        build_config.refresh_from_db()
        assert build_config.buildpack_builder == slugbuilder
        assert build_config.buildpack_runner == slugrunner
    else:
        with pytest.raises(BindError):
            binder.bind_image(slugrunner, slugbuilder)

```
</details>

---


#### test_bind_buildpack

**复杂度分数**: 12
**严重程度**: warning
**行数**: 72-121 (共 50 行, 3 行注释)

**函数签名**:
```python
def test_bind_buildpack ( bk_module, slugbuilder, slugrunner, buildpack, slugbuilder_attrs, buildpack_attrs, linked, ok ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
def test_bind_buildpack(bk_module, slugbuilder, slugrunner, buildpack, slugbuilder_attrs, buildpack_attrs, linked, ok):
    for k, v in slugbuilder_attrs.items():
        setattr(slugbuilder, k, v)
        setattr(slugrunner, k, v)

    for k, v in buildpack_attrs.items():
        setattr(buildpack, k, v)
    slugbuilder.buildpacks.clear()
    slugbuilder.save()
    slugrunner.save()
    buildpack.save()

    binder = ModuleRuntimeBinder(bk_module)
    build_config = bk_module.build_config

    assert build_config.buildpack_builder is None
    assert build_config.buildpack_runner is None
    assert slugbuilder.buildpacks.count() == 0

    if linked:
        slugbuilder.buildpacks.add(buildpack)
        assert slugbuilder.buildpacks.count() == 1

    if ok:
        binder.bind_image(slugrunner=slugrunner, slugbuilder=slugbuilder)
        binder.bind_buildpack(buildpack)
        # 必须绑定后再构造 ModuleRuntimeManager, 否则会因为 django 的查询缓存导致无法查询到对象
        manager = ModuleRuntimeManager(bk_module)
        assert manager.get_slug_builder(raise_exception=True) == slugbuilder
        assert manager.list_buildpacks() == [buildpack]
        # 测试重复绑定
        binder.bind_buildpack(buildpack)
        assert bk_module.build_config.buildpacks.count() == 1

    else:
        with pytest.raises(BindError):  # noqa: PT012
            binder.bind_image(slugrunner=slugrunner, slugbuilder=slugbuilder)
            binder.bind_buildpack(buildpack)

```
</details>

---


### 模块: apiserver/paasng/tests/paasng/platform/sourcectl/test_sourcectl_git.py


#### test_list_all_repositories

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 179-220 (共 42 行, 0 行注释)

**函数签名**:
```python
def test_list_all_repositories ( self, client, github_repo_url, user_credentials ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def test_list_all_repositories(self, client, github_repo_url, user_credentials):
        def mock_list_repo(*args, **kwargs):
            return [
                {
                    "owner": {
                        "login": "octocat",
                        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                    },
                    "name": "Hello-World",
                    "description": "This your first repo!",
                    "html_url": "https://github.com/octocat/Hello-World",
                    "clone_url": "https://github.com/octocat/Hello-World.git",
                    "ssh_url": "git@github.com:octocat/Hello-World.git",
                    "created_at": "2011-01-26T19:01:12Z",
                    "updated_at": "2011-01-26T19:14:43Z",
                },
                {
                    "owner": {
                        "login": "octocat",
                        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                    },
                    "name": "hello-worId",
                    "description": "My first repository on GitHub.",
                    "html_url": "https://github.com/octocat/hello-worId",
                    "clone_url": "https://github.com/octocat/hello-worId.git",
                    "ssh_url": "git@github.com:octocat/hello-worId.git",
                    "created_at": "2014-01-26T19:01:12Z",
                    "updated_at": "2014-01-26T19:14:43Z",
                },
            ]

        client.list_repo.side_effect = mock_list_repo
        ret = GitHubRepoController.list_all_repositories(api_url=github_repo_url, **user_credentials)
        assert len(ret) == 2
        assert ret[0].namespace == "octocat"
        assert ret[0].project == "Hello-World"
        assert ret[0].description == "This your first repo!"
        assert ret[0].last_activity_at == datetime.datetime(2011, 1, 26, 19, 14, 43, tzinfo=tzutc())
        assert ret[1].web_url == "https://github.com/octocat/hello-worId"
        assert ret[1].http_url_to_repo == "https://github.com/octocat/hello-worId.git"
        assert ret[1].ssh_url_to_repo == "git@github.com:octocat/hello-worId.git"
        assert ret[1].created_at == datetime.datetime(2014, 1, 26, 19, 1, 12, tzinfo=tzutc())

```
</details>

---


### 模块: operator/scripts/update_helm_chart.py


#### _remove_useless_newline

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 589-617 (共 29 行, 3 行注释)
**描述**: 去除 go-yaml unmarshal 中不需要的换行

**函数签名**:
```python
def _remove_useless_newline ( self ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def _remove_useless_newline(self):
        """去除 go-yaml unmarshal 中不需要的换行"""
        for src_files in filepath_conf.values():
            for src in src_files:
                if not src.endswith("yaml"):
                    continue

                fp = self.chart_source_dir / TMPL_DIR / src
                try:
                    contents = fp.read_text().splitlines()
                except FileNotFoundError:
                    print(f"file {src} not exists, auto create...")
                    fp.touch()
                    continue

                for idx in range(len(contents)):
                    # 忽略第一行，因为首行不会是被强制换行的
                    if (
                        idx
                        and contents[idx].count("}}")
                        and contents[idx - 1].count("{{") - contents[idx - 1].count("}}") == 1
                    ):
                        # 去掉上一行原来的换行符，拼接上当前行，把当前行设置为空字符串
                        contents[idx - 1] = contents[idx - 1].rstrip() + " "
                        contents[idx - 1] += contents[idx].lstrip()
                        contents[idx] = ""

                # 使用换行符号拼接每行的内容，并且在最后添加新空行
                fp.write_text("\n".join([line for line in contents if line]) + "\n")

```
</details>

---


### 模块: svc-rabbitmq/tasks/management/commands/worker.py


#### guard

**复杂度分数**: 10
**严重程度**: acceptable
**行数**: 67-101 (共 35 行, 9 行注释)

**函数签名**:
```python
def guard ( self ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def guard(self):
        logger.info(_("{} guarding cluster at {}").format(self.name, self.pid))
        self.start_event.set()
        Stat(self).save()
        logger.info(_("Q Cluster-{} running.").format(self.parent_pid))
        self.schedule()
        counter = 0
        cycle = Conf.GUARD_CYCLE  # guard loop sleep in seconds
        # Guard loop. Runs at least once
        while not self.stop_event.is_set() or not counter:
            # Check Workers
            for p in self.pool:
                with p.timer.get_lock():
                    # Are you alive?
                    if not p.is_alive() or p.timer.value == 0:
                        self.reincarnate(p)
                        continue
                    # Decrement timer if work is being done
                    if p.timer.value > 0:
                        p.timer.value -= cycle
            # Check Monitor
            if not self.monitor.is_alive():
                self.reincarnate(self.monitor)
            # Check Pusher
            if not self.pusher.is_alive():
                self.reincarnate(self.pusher)
            # Call scheduler once a minute (or so)
            counter += cycle
            if counter >= 30:
                counter = 0
                self.schedule()
            # Save current status
            Stat(self).save()
            sleep(cycle)
        self.stop()

```
</details>

---


### 模块: svc-rabbitmq/vendor/definitions.py


#### is_idle

**复杂度分数**: 15
**严重程度**: warning
**行数**: 64-96 (共 33 行, 0 行注释)

**函数签名**:
```python
def is_idle ( self, ignore_consumer: bool = False, max_idle: Optional[timedelta] = None ) :
```

**消息**: Complexity 15 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def is_idle(self, ignore_consumer: bool = False, max_idle: Optional[timedelta] = None):
        if not ignore_consumer and self.consumer_count > 0:
            return False

        if not self.idle_since:
            return False

        if self.acks_uncommitted > 0:
            return False

        if self.messages_unacknowledged > 0:
            return False

        if self.messages_uncommitted > 0:
            return False

        if self.messages_unconfirmed > 0:
            return False

        if max_idle and self.idle_since + max_idle > datetime.utcnow():
            return False

        message_stats = self.message_stats
        if not message_stats:
            return True

        if message_stats.confirm_details and message_stats.confirm_details.rate > 0:
            return False

        if message_stats.publish_details and message_stats.publish_details.rate > 0:
            return False

        return True

```
</details>

---


### 模块: svc-rabbitmq/vendor/management/commands/evict_connections.py


#### run_once

**复杂度分数**: 15
**严重程度**: warning
**行数**: 87-144 (共 58 行, 0 行注释)

**函数签名**:
```python
def run_once ( self, client: Client, max_idle_seconds: int, safe_peer_host: typing.List[str], peer_host: typing.List[str], *args, **kwargs ) :
```

**消息**: Complexity 15 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def run_once(
        self,
        client: Client,
        max_idle_seconds: int,
        safe_peer_host: typing.List[str],
        peer_host: typing.List[str],
        *args,
        **kwargs,
    ):
        vhost_set = self.get_vhost_set(*args, **kwargs)
        if vhost_set:
            print(f"evicting connections in vhosts: {', '.join(vhost_set)}")

        safe_peer_host_set = set()
        if safe_peer_host:
            safe_peer_host_set.update(safe_peer_host)
            print(f"safe peer hosts: {', '.join(safe_peer_host_set)}")

        peer_host_set = set()
        if peer_host:
            peer_host_set.update(peer_host)
            print(f"evicting connections for peer hosts: {', '.join(peer_host_set)}")

        rest_connections: typing.List[Connection] = []

        for i in client.connection.list():
            connection = Connection(**i)
            if vhost_set and connection.vhost not in vhost_set:
                continue

            if peer_host_set and connection.peer_host not in peer_host_set:
                continue

            if safe_peer_host_set and connection.peer_host in safe_peer_host_set:
                continue

            try:
                chs = client.connection.channels(connection.name)
            except Exception as err:
                print(f"list channels for connection {connection} failed: {err}, check in next time")
                rest_connections.append(connection)
                continue

            channels = [Channel(**i) for i in chs]

            if not self.has_consumer_channel(channels):
                print(f"connection {connection} is for publisher")
            elif not self.consumer_channels_idle(channels, timedelta(seconds=max_idle_seconds)):
                print(f"connection {connection} is activating, skipped")
                rest_connections.append(connection)
                continue
            else:
                print(f"idle connection {connection} is for consumer")

            if not self.close_connection(client, connection, *args, **kwargs):
                rest_connections.append(connection)

        return rest_connections

```
</details>

---


### 模块: svc-rabbitmq/vendor/management/commands/recovery_connections.py


#### channel_is_activated

**复杂度分数**: 12
**严重程度**: warning
**行数**: 117-143 (共 27 行, 0 行注释)

**函数签名**:
```python
def channel_is_activated ( self, channel, ignore_consumer ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def channel_is_activated(self, channel, ignore_consumer):
        if not ignore_consumer and channel["consumer_count"] > 0:
            return True

        if channel["acks_uncommitted"] > 0:
            return True

        if channel["messages_unacknowledged"] > 0:
            return True

        if channel["messages_uncommitted"] > 0:
            return True

        if channel["messages_unconfirmed"] > 0:
            return True

        message_stats = channel.get("message_stats")
        if not message_stats:
            return False

        if "confirm_details" in message_stats and message_stats["confirm_details"]["rate"] > 0:
            return True

        if "publish_details" in message_stats and message_stats["publish_details"]["rate"] > 0:
            return True

        return False

```
</details>

---


### 模块: svc-rabbitmq/vendor/management/commands/reset_ins_config.py


#### handle

**复杂度分数**: 11
**严重程度**: warning
**行数**: 44-83 (共 40 行, 0 行注释)

**函数签名**:
```python
def handle ( self, host: Optional[str], port: Optional[str], password: Optional[str], api_port: Optional[int], api_url: Optional[str], admin: Optional[str], dry_run: bool, **options ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def handle(
        self,
        host: Optional[str],
        port: Optional[str],
        password: Optional[str],
        api_port: Optional[int],
        api_url: Optional[str],
        admin: Optional[str],
        dry_run: bool,
        **options,
    ):
        svc_objs = ServiceInstance.objects.all()
        for svc_obj in svc_objs:
            credentials = svc_obj.get_credentials()
            updated_credentials = credentials.copy()

            if api_url:
                updated_credentials["management_api"] = api_url
            elif host and api_port:
                updated_credentials["management_api"] = "http://%s:%s" % (host, api_port)

            if host:
                updated_credentials["host"] = host

            if port:
                updated_credentials["port"] = port

            if password:
                updated_credentials["password"] = password

            if admin:
                updated_credentials["admin"] = admin

            if not dry_run and updated_credentials != credentials:
                svc_obj.credentials = json.dumps(updated_credentials)
                svc_obj.save(update_fields=["credentials"])

            self.stdout.write(
                self.style.NOTICE(f"实例配置变化：\n before:{credentials} \n after:{updated_credentials} \n")
            )

```
</details>

---


### 模块: svc-rabbitmq/vendor/management/commands/sync_user_policies.py


#### handle

**复杂度分数**: 12
**严重程度**: warning
**行数**: 86-122 (共 37 行, 1 行注释)

**函数签名**:
```python
def handle ( self, add, update, delete, dry_run, sleep, *args, **kwargs ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python
    def handle(self, add, update, delete, dry_run, sleep, *args, **kwargs):
        vhosts = self.get_vhost_set(*args, **kwargs)
        enabled_policies = {}
        disabled_policies = {}

        for p in self.get_policies(*args, **kwargs):
            if p.enable:
                enabled_policies[p.name] = p
            else:
                disabled_policies[p.name] = p

        client = self.get_client_by_cluster(*args, **kwargs)
        for vhost in vhosts:
            time.sleep(sleep)
            # policies which defined in the rabbitmq cluster
            policies = {p["name"]: p for p in client.user_policy.get(vhost)}

            if add:
                names = enabled_policies.keys() - policies.keys()
                print(f"policies will be add: {names}")
                if not dry_run:
                    self.patch_policies(vhost, client, names, enabled_policies)

            if update:
                names = []
                for n in enabled_policies.keys() & policies.keys():
                    if not self.compare_policies(enabled_policies[n].dict(), policies[n]):
                        names.append(n)
                print(f"policies will be update: {names}")
                if not dry_run:
                    self.patch_policies(vhost, client, names, enabled_policies)

            if delete:
                names = disabled_policies & policies.keys()
                print(f"policies will be delete: {names}")
                if not dry_run:
                    self.delete_policies(vhost, client, names)

```
</details>

---
