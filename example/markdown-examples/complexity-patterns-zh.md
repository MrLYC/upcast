# 代码复杂度分析

## 元数据
暂无元数据。

## 概要信息
- **总数量**: 88
- **已扫描文件数**: 75

- **高复杂度函数数量**: 88

### 按严重程度统计函数数
- **acceptable**: 33 个函数
- **critical**: 2 个函数
- **high_risk**: 10 个函数
- **warning**: 43 个函数

## 结果详情

### 模块: apiserver/paasng/paas_wl/bk_app/cnative/specs/resource.py


#### detect_state

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 183-204 (共 22 行, 0 行注释)  
**描述**: Detect the final state from status.conditions

**函数签名**:
```python
def detect_state ( self ) -> ModelResState :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def detect_state(self) -> ModelResState:
    """Detect the final state from status.conditions"""
    if not self.mres.status.conditions:
        return ModelResState(DeployStatus.PENDING, 'Pending', 'state not initialized')
    if self.mres.status.phase == MResPhaseType.AppRunning:
        available = self._find_condition(MResConditionType.APP_AVAILABLE)
        if available and available.status == ConditionStatus.TRUE:
            return ModelResState(DeployStatus.READY, available.reason, available.message)
    if self.mres.status.phase == MResPhaseType.AppFailed:
        reasons: List[str] = []
        messages: List[str] = []
        for cond in self.mres.status.conditions:
            if cond.status == ConditionStatus.FALSE and cond.message:
                reasons.append(cond.reason)
                messages.append(cond.message)
        if messages:
            return ModelResState(DeployStatus.ERROR, '\n'.join(reasons), '\n'.join(messages))
        return ModelResState(DeployStatus.ERROR, 'Unknown', '')
    return ModelResState(DeployStatus.PROGRESSING, 'Progressing', 'progressing')
```
</details>

---


### 模块: apiserver/paasng/paas_wl/bk_app/dev_sandbox/kres_slzs/ingress.py


#### serialize

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 52-108 (共 57 行, 0 行注释)  
**描述**: serialize obj into Ingress(networking.k8s.io/v1)

**函数签名**:
```python
def serialize ( self, obj: 'DevSandboxIngress', original_obj: Optional[ResourceInstance] = None, **kwargs ) -> Dict :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def serialize(self, obj: 'DevSandboxIngress', original_obj: Optional[ResourceInstance] = None, **kwargs) -> Dict:
    """serialize obj into Ingress(networking.k8s.io/v1)"""
    nginx_adaptor = NginxRegexRewrittenProvider()
    annotations = {ANNOT_SSL_REDIRECT: 'false', ANNOT_SKIP_FILTER_CLB: 'true'}
    if obj.rewrite_to_root:
        annotations[ANNOT_REWRITE_TARGET] = nginx_adaptor.make_rewrite_target()
    if obj.set_header_x_script_name:
        annotations[ANNOT_CONFIGURATION_SNIPPET] = nginx_adaptor.make_configuration_snippet()
    if settings.APP_INGRESS_CLASS is not None:
        annotations['kubernetes.io/ingress.class'] = settings.APP_INGRESS_CLASS
    tls_group_by_secret_name: Dict[str, List] = defaultdict(list)
    for domain in obj.domains:
        if domain.tls_enabled:
            tls_group_by_secret_name[domain.tls_secret_name].append(domain.host)
    tls = []
    for (secret_name, hosts) in tls_group_by_secret_name.items():
        tls.append({'hosts': hosts, 'secretName': secret_name})
    rules = []
    for domain in obj.domains:
        paths = []
        for backend in domain.path_backends:
            paths.append({'path': nginx_adaptor.make_location_path(backend.path_prefix or '/') if obj.rewrite_to_root else backend.path_prefix, 'pathType': 'ImplementationSpecific', 'backend': {'service': {'name': backend.service_name, 'port': {'name': backend.service_port_name}}}})
        rules.append({'host': domain.host, 'http': {'paths': paths}})
    body: Dict[str, Any] = {'metadata': {'name': obj.name, 'annotations': annotations, 'labels': {'env': 'dev'}}, 'spec': {'rules': rules, 'tls': tls}, 'apiVersion': self.get_api_version_from_gvk(self.gvk_config), 'kind': 'Ingress'}
    if original_obj:
        body['metadata']['resourceVersion'] = original_obj.metadata.resourceVersion
    return body
```
</details>

---


### 模块: apiserver/paasng/paas_wl/bk_app/processes/kres_slzs.py


#### deserialize

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 194-246 (共 53 行, 0 行注释)  
**描述**: Generate a ProcInstance by given Pod object

**函数签名**:
```python
def deserialize ( self, app: WlApp, kube_data: ResourceInstance ) -> 'Instance' :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def deserialize(self, app: WlApp, kube_data: ResourceInstance) -> 'Instance':
    """Generate a ProcInstance by given Pod object"""
    pod = kube_data
    health_status = check_pod_health_status(parse_pod(kube_data))
    (instance_state, state_message) = self.parse_instance_state(pod.status.phase, health_status)
    c_status = None
    c_status_dict = {}
    if pod.status.get('containerStatuses'):
        c_status = pod.status.containerStatuses[0]
        c_status_dict = get_items(pod.to_dict(), 'status.containerStatuses', [{}])[0]
    process_type = self.get_process_type(pod)
    target_container = self._get_main_container(app, pod)
    envs = {}
    if target_container and hasattr(target_container, 'env'):
        for env in target_container.env:
            name = getattr(env, 'name', None)
            value = getattr(env, 'value', None)
            if name and value is not None:
                envs[name] = value
    if app.type == WlAppType.DEFAULT:
        labels = pod.metadata.labels or {}
        version = int(labels.get('release_version', 0))
    else:
        annotations = pod.metadata.annotations or {}
        version = int(annotations.get(BKPAAS_DEPLOY_ID_ANNO_KEY, 0))
    terminated_info = {}
    if c_status_dict:
        terminated_info = {'exit_code': get_items(c_status_dict, 'lastState.terminated.exitCode'), 'reason': get_items(c_status_dict, 'lastState.terminated.reason')}
    return self.entity_type(app=app, name=pod.metadata.name, process_type=process_type, host_ip=pod.status.get('hostIP', None), start_time=pod.status.get('startTime', None), state=instance_state, state_message=state_message, rich_status=self.extract_rich_status(pod.status.phase, c_status), image=target_container.image if target_container else '', envs=envs, ready=health_status.status == HealthStatusType.HEALTHY, restart_count=c_status.restartCount if c_status else 0, terminated_info=terminated_info, version=version)
```
</details>

---


### 模块: apiserver/paasng/paas_wl/bk_app/processes/models.py


#### process_spec_updator

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 181-199 (共 19 行, 0 行注释)  

**函数签名**:
```python
def process_spec_updator ( process: ProcessTmpl ) -> Tuple[bool, ProcessSpec] :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def process_spec_updator(process: ProcessTmpl) -> Tuple[bool, ProcessSpec]:
    process_spec = proc_specs.get(name=process.name)
    recorder = AttrSetter(process_spec)
    if process_spec.target_status != ProcessTargetStatus.START.value:
        recorder.setattr('target_status', ProcessTargetStatus.START.value)
    if command := process.command and command != process_spec.proc_command:
        recorder.setattr('proc_command', command)
    if plan_name := process.plan and plan := self.get_plan(plan_name, None):
        recorder.setattr('plan', plan)
    if process.autoscaling != process_spec.autoscaling:
        recorder.setattr('autoscaling', process.autoscaling)
    if scaling_config := process.scaling_config and scaling_config.dict() != process_spec.scaling_config:
        recorder.setattr('scaling_config', scaling_config.dict())
    if replicas := process.replicas and replicas != process_spec.target_replicas:
        recorder.setattr('target_replicas', replicas)
    return recorder.changed, process_spec
```
</details>

---


#### sync

**复杂度分数**: 17  
**严重程度**: high_risk  
**行数**: 129-213 (共 85 行, 0 行注释)  
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
    proc_type = 'process'
    proc_specs = ProcessSpec.objects.filter(engine_app=self.wl_app, type=proc_type)
    existed_procs_name = set(proc_specs.values_list('name', flat=True))
    removing_procs_name = list(existed_procs_name - processes_map.keys())
    if removing_procs_name:
        proc_specs.filter(name__in=removing_procs_name).delete()
    default_process_spec_plan = ProcessSpecPlan.objects.get_by_name(name=settings.DEFAULT_PROC_SPEC_PLAN)
    if self.wl_app.type == WlAppType.CLOUD_NATIVE:
        default_process_spec_plan = ProcessSpecPlan.objects.get_by_name(name=ResQuotaPlan.P_DEFAULT) or default_process_spec_plan
    adding_procs = [process for (name, process) in processes_map.items() if name not in existed_procs_name]
    
    def process_spec_builder(process: ProcessTmpl) -> ProcessSpec:
        target_replicas = process.replicas or self.get_default_replicas(process.name, environment)
        plan = default_process_spec_plan
        if plan_name := process.plan:
            plan = self.get_plan(plan_name, default_process_spec_plan)
        return ProcessSpec(type=proc_type, region=self.wl_app.region, name=process.name, engine_app_id=self.wl_app.pk, target_replicas=target_replicas, plan=plan, proc_command=process.command, autoscaling=process.autoscaling, scaling_config=process.scaling_config.dict() if process.scaling_config else None)
    self.bulk_create_procs(proc_creator=process_spec_builder, adding_procs=adding_procs)
    updating_proc_specs = [process for (name, process) in processes_map.items() if name in existed_procs_name]
    
    def process_spec_updator(process: ProcessTmpl) -> Tuple[bool, ProcessSpec]:
        process_spec = proc_specs.get(name=process.name)
        recorder = AttrSetter(process_spec)
        if process_spec.target_status != ProcessTargetStatus.START.value:
            recorder.setattr('target_status', ProcessTargetStatus.START.value)
        if command := process.command and command != process_spec.proc_command:
            recorder.setattr('proc_command', command)
        if plan_name := process.plan and plan := self.get_plan(plan_name, None):
            recorder.setattr('plan', plan)
        if process.autoscaling != process_spec.autoscaling:
            recorder.setattr('autoscaling', process.autoscaling)
        if scaling_config := process.scaling_config and scaling_config.dict() != process_spec.scaling_config:
            recorder.setattr('scaling_config', scaling_config.dict())
        if replicas := process.replicas and replicas != process_spec.target_replicas:
            recorder.setattr('target_replicas', replicas)
        return recorder.changed, process_spec
    self.bulk_update_procs(proc_updator=process_spec_updator, updating_procs=updating_proc_specs, updated_fields=['proc_command', 'plan', 'autoscaling', 'scaling_config', 'target_replicas', 'target_status', 'updated'])
```
</details>

---


### 模块: apiserver/paasng/paas_wl/infras/cluster/models.py


#### register_cluster

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 135-207 (共 73 行, 0 行注释)  
**描述**: Register a cluster to db, work Like update_or_create, but will validate some-attr

**函数签名**:
```python
def register_cluster ( self, region: str, name: str, type: str = ClusterType.NORMAL, is_default: bool = False, description: Optional[str] = None, ingress_config: Optional[Dict] = None, annotations: Optional[Dict] = None, ca_data: Optional[str] = None, cert_data: Optional[str] = None, key_data: Optional[str] = None, token_type: Optional[ClusterTokenType] = None, token_value: Optional[str] = None, default_node_selector: Optional[Dict] = None, default_tolerations: Optional[List] = None, feature_flags: Optional[Dict] = None, pk: Optional[str] = None, **kwargs ) -> 'Cluster' :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

@transaction.atomic(using='workloads')
def register_cluster(self, region: str, name: str, type: str = ClusterType.NORMAL, is_default: bool = False, description: Optional[str] = None, ingress_config: Optional[Dict] = None, annotations: Optional[Dict] = None, ca_data: Optional[str] = None, cert_data: Optional[str] = None, key_data: Optional[str] = None, token_type: Optional[ClusterTokenType] = None, token_value: Optional[str] = None, default_node_selector: Optional[Dict] = None, default_tolerations: Optional[List] = None, feature_flags: Optional[Dict] = None, pk: Optional[str] = None, **kwargs) -> 'Cluster':
    """Register a cluster to db, work Like update_or_create, but will validate some-attr

        Auth type: client-side cert
        ---------------------------

        :param cert_data: client cert data
        :param key_data: client key data

        Auth type: Bearer token
        -----------------------

        :param token_type: token type, use `SERVICE_ACCOUNT` by default
        :param token_value: value of token
        """
    default_cluster_qs = self.filter(region=region, is_default=True)
    if not default_cluster_qs.exists() and not is_default:
        raise NoDefaultClusterError('This region has not define a default cluster.')
    elif default_cluster_qs.filter(name=name).exists() and not is_default:
        raise SwitchDefaultClusterError("Can't change default cluster by calling `register_cluster`, please use `switch_default_cluster`")
    elif default_cluster_qs.exclude(name=name).exists() and is_default:
        raise DuplicatedDefaultClusterError('This region should have one and only one default cluster.')
    validate_ingress_config(ingress_config)
    defaults: Dict[str, Any] = {'type': type, 'is_default': is_default, 'description': description, 'ingress_config': ingress_config, 'annotations': annotations, 'ca_data': ca_data, 'cert_data': cert_data, 'key_data': key_data, 'default_node_selector': default_node_selector, 'default_tolerations': default_tolerations, 'feature_flags': feature_flags}
    if token_value:
        _token_type = token_type or ClusterTokenType.SERVICE_ACCOUNT
        defaults.update({'token_value': token_value, 'token_type': _token_type})
    defaults = {k: v for (k, v) in defaults.items() if v is not None}
    if pk:
        (cluster, _) = self.update_or_create(pk=pk, name=name, region=region, defaults=defaults)
    else:
        (cluster, _) = self.update_or_create(name=name, region=region, defaults=defaults)
    return cluster
```
</details>

---


### 模块: apiserver/paasng/paas_wl/infras/resources/base/kres.py


#### create_or_update

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 290-335 (共 46 行, 0 行注释)  
**描述**: Create or update a resource by name

**函数签名**:
```python
def create_or_update ( self, name: str, namespace: Namespace = None, body: Optional[Manifest] = None, update_method: str = 'replace', content_type: Optional[str] = None, auto_add_version: bool = False ) -> Tuple[ResourceInstance, bool] :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def create_or_update(self, name: str, namespace: Namespace = None, body: Optional[Manifest] = None, update_method: str = 'replace', content_type: Optional[str] = None, auto_add_version: bool = False) -> Tuple[ResourceInstance, bool]:
    """Create or update a resource by name

        :param content_type: content_type header for patch/replace requests
        :param auto_add_version: 当 update_method=replace 时，是否自动添加 metadata.resourceVersion 字段，默认为 False
        :returns: (instance, created)
        """
    assert update_method in ['replace', 'patch'], 'Invalid update_method {}'.format(update_method)
    if not body:
        body_dict: Dict = {'kind': self.kres.kind, 'metadata': {'name': name}}
    else:
        body_dict = self.client.serialize_body(body)
    body_dict.setdefault('kind', self.kres.kind)
    if body_dict and body_dict['metadata']['name'] != name:
        raise ValueError('name in args must match name in body')
    try:
        obj = self.resource.create(body=body_dict, namespace=namespace, **self.default_kwargs)
    except ApiException as e:
        if not (e.status == 409 and json.loads(e.body)['reason'] == 'AlreadyExists'):
            raise
    else:
        return obj, True
    if update_method == 'replace' and auto_add_version:
        self._add_resource_version(name, namespace, body_dict)
    logger.info(f'Create {self.kres.kind} {name} failed, already existed, continue update')
    _func = getattr(self.resource, update_method)
    update_kwargs = self.default_kwargs.copy()
    if content_type:
        update_kwargs['content_type'] = content_type
    obj = _func(name=name, body=body_dict, namespace=namespace, **update_kwargs)
    return obj, False
```
</details>

---


### 模块: apiserver/paasng/paas_wl/infras/resources/base/kube_client.py


#### __search

**复杂度分数**: 15  
**严重程度**: warning  
**行数**: 35-78 (共 44 行, 0 行注释)  

**函数签名**:
```python
def __search ( self, parts, resources, reqParams ) :
```

**消息**: Complexity 15 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def __search(self, parts, resources, reqParams):
    part = parts[0]
    if part != '*':
        resourcePart = resources.get(part)
        if not resourcePart:
            return []
        elif isinstance(resourcePart, ResourceGroup):
            if len(reqParams) != 2:
                raise ValueError('prefix and group params should be present, have %s' % reqParams)
            if not resourcePart.resources:
                (prefix, group, version) = (reqParams[0], reqParams[1], part)
                try:
                    resourcePart.resources = self.get_resources_for_api_version(prefix, group, part, resourcePart.preferred)
                except NotFoundError:
                    raise ResourceNotFoundError
                if resourcePart.resources:
                    self._cache['resources'][prefix][group][version] = resourcePart
                    self.__update_cache = True
            return self.__search(parts[1:], resourcePart.resources, reqParams)
        elif isinstance(resourcePart, dict):
            return self.__search(parts[1:], resourcePart, reqParams + [part])
        elif parts[1] != '*' and isinstance(parts[1], dict):
            for _resource in resourcePart:
                for (term, value) in parts[1].items():
                    if getattr(_resource, term) == value:
                        return [_resource]
            return []
        else:
            return resourcePart
    else:
        matches = []
        for key in resources.keys():
            matches.extend(self.__search([key] + parts[1:], resources, reqParams))
        return matches
```
</details>

---


### 模块: apiserver/paasng/paas_wl/infras/resources/kube_res/base.py


#### watch_by_app

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 463-509 (共 47 行, 0 行注释)  
**描述**: Get notified when resource changes

**函数签名**:
```python
def watch_by_app ( self, app: WlApp, labels: Optional[Dict] = None, ignore_unknown_objs: bool = False, **kwargs ) -> Iterator[WatchEvent[AET]] :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def watch_by_app(self, app: WlApp, labels: Optional[Dict] = None, ignore_unknown_objs: bool = False, **kwargs) -> Iterator[WatchEvent[AET]]:
    """Get notified when resource changes

        :param labels: labels for filtering results
        :param ignore_unknown_objs: whether skip watch event when deserialize can not handle the object
        """
    labels = labels or {}
    if 'resource_version' in kwargs and kwargs['resource_version'] is None:
        kwargs.pop('resource_version')
    if kwargs.get('namespace'):
        raise ValueError('"namespace" is not supported')
    deserializer = self._make_deserializer(app)
    with self.kres(app, api_version=deserializer.get_apiversion()) as kres_client:
        try:
            for raw_event in kres_client.ops_batch.create_watch_stream(namespace=self._get_namespace(app), labels=labels, **kwargs):
                if raw_event['type'] == 'ERROR':
                    raw_object = raw_event['raw_object']
                    msg = raw_object.get('message', 'Unknown')
                    yield WatchEvent(type='ERROR', error_message=msg)
                    return
                event = WatchEvent[AET](type=raw_event['type'])
                try:
                    event.res_object = deserializer.deserialize(app, raw_event['object'])
                except AppEntityDeserializeError as e:
                    if ignore_unknown_objs:
                        logger.warning('failed to deserialize k8s resource %s, skip.', e.res)
                        continue
                    yield WatchEvent(type='ERROR', error_message=e.msg)
                    return
                event.res_object._kube_data = raw_event['object']
                yield event
        except ApiException as exc:
            if self._exc_is_expired_rv(exc):
                yield WatchEvent(type='ERROR', error_message=exc.reason)
                return
            else:
                raise
```
</details>

---


### 模块: apiserver/paasng/paas_wl/utils/kubestatus.py


#### check_pod_health_status

**复杂度分数**: 16  
**严重程度**: high_risk  
**行数**: 89-150 (共 62 行, 0 行注释)  
**描述**: Check if the pod is healthy

**函数签名**:
```python
def check_pod_health_status ( pod: kmodels.V1Pod ) -> HealthStatus :
```

**消息**: Complexity 16 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def check_pod_health_status(pod: kmodels.V1Pod) -> HealthStatus:
    """Check if the pod is healthy

    For a Pod, healthy is meaning that the Pod is successfully complete or is Ready
               unhealthy is meaning that the Pod is restarting or is Failed
               progressing is meaning that the Pod is still running and condition `PodReady` is False.
    """
    pod_status: kmodels.V1PodStatus = pod.status
    healthy = HealthStatus(reason=pod_status.reason, message=pod_status.message, status=HealthStatusType.HEALTHY)
    unhealthy = HealthStatus(reason=pod_status.reason, message=pod_status.message, status=HealthStatusType.UNHEALTHY)
    progressing = HealthStatus(reason=pod_status.reason, message=pod_status.message, status=HealthStatusType.PROGRESSING)
    if pod_status.phase == 'Succeeded':
        return healthy
    elif pod_status.phase == 'Running':
        pod_spec: kmodels.V1PodSpec = pod.spec
        if pod_spec.restart_policy == 'Always':
            cond_ready = find_pod_status_condition(pod_status.conditions or [], cond_type='Ready')
            if cond_ready and cond_ready.status == 'True':
                return healthy
            if fail_message := get_any_container_fail_message(pod):
                return unhealthy.with_message(fail_message)
            return progressing
        return progressing
    elif pod_status.phase == 'Failed':
        if pod_status.message:
            return unhealthy
        if fail_message := get_any_container_fail_message(pod):
            return unhealthy.with_message(fail_message)
        return unhealthy.with_message('unknown')
    elif pod_status.phase == 'Pending':
        if fail_message := get_any_container_fail_message(pod) and fail_message not in ['ContainerCreating', 'PodInitializing']:
            return unhealthy.with_message(fail_message)
        scheduled_cond = find_pod_status_condition(pod_status.conditions or [], cond_type='PodScheduled')
        if scheduled_cond and scheduled_cond.status == 'False' and scheduled_cond.reason in ['Unschedulable', 'SchedulingGated']:
            return unhealthy.with_message(scheduled_cond.message)
        return progressing
    else:
        return HealthStatus(reason=pod_status.phase or 'unknown', message=pod_status.message, status=HealthStatusType.UNKNOWN)
```
</details>

---


### 模块: apiserver/paasng/paas_wl/utils/models.py


#### make_json_field

**复杂度分数**: 13  
**严重程度**: warning  
**行数**: 66-148 (共 83 行, 0 行注释)  
**描述**: 生成会自动进行类型转换为 `py_model` 的 JSONField

**函数签名**:
```python
def make_json_field ( cls_name: str, py_model: Type[M], decoder: Callable[[M], Dict] = cattr.unstructure, module: Optional[str] = None ) -> Type[JSONField] :
```

**消息**: Complexity 13 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def make_json_field(cls_name: str, py_model: Type[M], decoder: Callable[[M], Dict] = cattr.unstructure, module: Optional[str] = None) -> Type[JSONField]:
    """生成会自动进行类型转换为 `py_model` 的 JSONField

    :param cls_name: 自动生成的 JSONField 的类名, 在使用时, cls_name 必须与赋值的变量名一致！否则 migrations 会报错.
    :param py_model: Python 对象, 需要能被 decoder 转换成可序列化成 json serializable 的 dict 对象.
    :param decoder: 能将 py_model instance 反序列化为 json serializable 的 dict 对象
    :param module:

    >>> @dataclass
    ... class Dummy:
    ...   foo: str
    ...   bar: bool = False
    >>> DummyField = make_json_field('DummyField', Dummy)
    """
    if not isinstance(py_model, type):
        raise NotImplementedError(f'Unsupported type: {py_model}')
    
    def pre_init(self, value, obj):
        """Convert a dict/list to dataclass_model object"""
        loaded_value = super(JSONField, self).pre_init(value, obj)
        if isinstance(loaded_value, py_model) or loaded_value is None:
            return loaded_value
        return cattr.structure(loaded_value, py_model)
    
    def get_prep_value(self, value):
        """Convert dataclass_model object to a string"""
        if isinstance(value, py_model):
            value = decoder(value)
        return super(JSONField, self).get_prep_value(value)
    
    def dumps_for_display(self, value):
        """Convert dataclass_model object to a string, calling by jsonfield"""
        if isinstance(value, py_model):
            return decoder(value)
        return super(JSONField, self).dumps_for_display(value)
    
    def to_python(self, value):
        """The jsonfield.SubfieldBase metaclass calls pre_init instead of to_python, however to_python
        is still necessary for Django's deserializer"""
        loaded_value = super(JSONField, self).to_python(value)
        if isinstance(loaded_value, py_model) or loaded_value is None:
            return loaded_value
        return cattr.structure(loaded_value, py_model)
    
    def from_db_value(self, value, expression, connection):
        """Convert string-like value to dataclass_model object, calling by django"""
        loaded_value = super(JSONField, self).from_db_value(value, expression, connection)
        if isinstance(loaded_value, py_model) or loaded_value is None:
            return loaded_value
        return cattr.structure(loaded_value, py_model)
    
    def value_to_string(self, obj):
        """Convert dataclass_model object to a string, calling by django"""
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
    cls = type(cls_name, (JSONField, ), dict(pre_init=pre_init, get_prep_value=get_prep_value, dumps_for_display=dumps_for_display, to_python=to_python, from_db_value=from_db_value, value_to_string=value_to_string))
    try:
        module = sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        if module is None:
            raise RuntimeError("Can't detect the module name. please provide by func args.")
    finally:
        cls.__module__ = str(module)
    assert issubclass(cls, JSONField)
    return cls
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
    all_regions = set(Cluster.objects.values_list('region', flat=True))
    if options['region']:
        if options['region'] not in all_regions:
            print(f"{options['region']} is not a valid region name")
            sys.exit(1)
        regions = [options['region']]
    else:
        regions = list(all_regions)
    ignore_labels = options['ignore_labels']
    ignore_labels = [value.split('=') for value in ignore_labels]
    if any((len(label) != 2 for label in ignore_labels)):
        raise ValueError('Invalid label given!')
    if not options['include_masters']:
        ignore_labels.append(('node-role.kubernetes.io/master', 'true'))
    cluster_name = options.get('cluster_name')
    for region in regions:
        logger.debug(f'Make scheduler client from region: {region}')
        for cluster in Cluster.objects.filter(region=region):
            if cluster_name and cluster.name != cluster_name:
                continue
            logger.info(f'Will generate state for [{region}/{cluster.name}]...')
            if not options.get('no_input') and input('Confirm? (y/n, default: n) ').lower() != 'y':
                continue
            try:
                client = get_client_by_cluster_name(cluster_name=cluster.name)
                logger.info(f'Generating state for [{region} - {cluster.name}]...')
                state = generate_state(region, cluster.name, client, ignore_labels=ignore_labels)
                logger.info('Syncing the state to nodes...')
                sync_state_to_nodes(client, state)
            except Exception:
                logger.exception('Unable to generate state')
                continue
```
</details>

---


### 模块: apiserver/paasng/paas_wl/workloads/networking/ingress/kres_slzs/ingress.py


#### serialize

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 55-112 (共 58 行, 0 行注释)  
**描述**: serialize obj into Ingress(networking.k8s.io/v1beta1)

**函数签名**:
```python
def serialize ( self, obj: 'ProcessIngress', original_obj: Optional[ResourceInstance] = None, **kwargs ) -> Dict :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def serialize(self, obj: 'ProcessIngress', original_obj: Optional[ResourceInstance] = None, **kwargs) -> Dict:
    """serialize obj into Ingress(networking.k8s.io/v1beta1)"""
    nginx_adaptor = IngressNginxAdaptor(get_cluster_by_app(obj.app))
    annotations = {constants.ANNOT_SERVER_SNIPPET: obj.server_snippet, constants.ANNOT_CONFIGURATION_SNIPPET: obj.configuration_snippet, constants.ANNOT_SSL_REDIRECT: 'false', constants.ANNOT_SKIP_FILTER_CLB: 'true', **obj.annotations}
    if obj.rewrite_to_root:
        annotations[constants.ANNOT_REWRITE_TARGET] = nginx_adaptor.build_rewrite_target()
    if obj.set_header_x_script_name:
        annotations[constants.ANNOT_CONFIGURATION_SNIPPET] = ConfigurationSnippetPatcher().patch(obj.configuration_snippet, nginx_adaptor.make_configuration_snippet(fallback_script_name=obj.domains[0].primary_prefix_path)).configuration_snippet
    tls_group_by_secret_name: Dict[str, List] = defaultdict(list)
    for domain in obj.domains:
        if domain.tls_enabled:
            tls_group_by_secret_name[domain.tls_secret_name].append(domain.host)
    tls = []
    for (secret_name, hosts) in tls_group_by_secret_name.items():
        tls.append({'hosts': hosts, 'secretName': secret_name})
    rules = []
    for domain in obj.domains:
        paths = []
        for path_str in domain.path_prefix_list:
            paths.append({'path': nginx_adaptor.build_http_path(path_str or '/') if obj.rewrite_to_root else path_str, 'backend': {'serviceName': obj.service_name, 'servicePort': obj.service_port_name}})
        rules.append({'host': domain.host, 'http': {'paths': paths}})
    body: Dict[str, Any] = {'metadata': {'name': obj.name, 'namespace': obj.app.namespace, 'annotations': annotations}, 'spec': {'rules': rules, 'tls': tls}, 'apiVersion': self.get_api_version_from_gvk(self.gvk_config), 'kind': 'Ingress'}
    if original_obj:
        body['metadata']['resourceVersion'] = original_obj.metadata.resourceVersion
    return body
```
</details>

---


#### serialize

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 214-274 (共 61 行, 0 行注释)  
**描述**: serialize obj into Ingress(networking.k8s.io/v1)

**函数签名**:
```python
def serialize ( self, obj: 'ProcessIngress', original_obj: Optional[ResourceInstance] = None, **kwargs ) -> Dict :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def serialize(self, obj: 'ProcessIngress', original_obj: Optional[ResourceInstance] = None, **kwargs) -> Dict:
    """serialize obj into Ingress(networking.k8s.io/v1)"""
    nginx_adaptor = NginxRegexRewrittenProvider()
    annotations = {constants.ANNOT_SERVER_SNIPPET: obj.server_snippet, constants.ANNOT_CONFIGURATION_SNIPPET: obj.configuration_snippet, constants.ANNOT_SSL_REDIRECT: 'false', constants.ANNOT_SKIP_FILTER_CLB: 'true', **obj.annotations}
    if obj.rewrite_to_root:
        annotations[constants.ANNOT_REWRITE_TARGET] = nginx_adaptor.make_rewrite_target()
    if obj.set_header_x_script_name:
        annotations[constants.ANNOT_CONFIGURATION_SNIPPET] = ConfigurationSnippetPatcher().patch(obj.configuration_snippet, nginx_adaptor.make_configuration_snippet()).configuration_snippet
    tls_group_by_secret_name: Dict[str, List] = defaultdict(list)
    for domain in obj.domains:
        if domain.tls_enabled:
            tls_group_by_secret_name[domain.tls_secret_name].append(domain.host)
    tls = []
    for (secret_name, hosts) in tls_group_by_secret_name.items():
        tls.append({'hosts': hosts, 'secretName': secret_name})
    rules = []
    for domain in obj.domains:
        paths = []
        for path_str in domain.path_prefix_list:
            paths.append({'path': nginx_adaptor.make_location_path(path_str or '/') if obj.rewrite_to_root else path_str, 'pathType': 'ImplementationSpecific', 'backend': {'service': {'name': obj.service_name, 'port': {'name': obj.service_port_name}}}})
        rules.append({'host': domain.host, 'http': {'paths': paths}})
    body: Dict[str, Any] = {'metadata': {'name': obj.name, 'namespace': obj.app.namespace, 'annotations': annotations}, 'spec': {'rules': rules, 'tls': tls}, 'apiVersion': self.get_api_version_from_gvk(self.gvk_config), 'kind': 'Ingress'}
    if original_obj:
        body['metadata']['resourceVersion'] = original_obj.metadata.resourceVersion
    return body
```
</details>

---


### 模块: apiserver/paasng/paasng/accessories/log/filters.py


#### count_filters_options_from_logs

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 104-143 (共 40 行, 0 行注释)  
**描述**: 从日志样本(logs) 中统计 ES 日志的字段分布, 返回对应的 FieldFilters. 会忽略无可选 options 的 filters

**函数签名**:
```python
def count_filters_options_from_logs ( logs: List, properties: Dict[str, FieldFilter] ) -> Dict[str, FieldFilter] :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def count_filters_options_from_logs(logs: List, properties: Dict[str, FieldFilter]) -> Dict[str, FieldFilter]:
    """从日志样本(logs) 中统计 ES 日志的字段分布, 返回对应的 FieldFilters. 会忽略无可选 options 的 filters

    :param logs: 日志样本
    :param properties: 需要统计的ES 字段
    """
    field_counter: Dict[str, Counter] = defaultdict(Counter)
    log_fields = [(f, f.split('.')) for f in properties]
    for log in logs:
        for (log_field, split_log_field) in log_fields:
            try:
                value = get_attribute(log, split_log_field)
            except (AttributeError, KeyError):
                continue
            try:
                field_counter[log_field][value] += 1
            except TypeError:
                logger.warning('Field<%s> got an unhashable value: %s', log_field, value)
    result = {}
    for (title, values) in field_counter.items():
        f = properties[title]
        options = dict(f.options)
        total = sum(values.values())
        if total == 0 and len(options) == 0:
            continue
        for (value, count) in values.items():
            if value not in options:
                percentage = calculate_percentage(count, total)
                options[value] = percentage
        result[title] = FieldFilter(name=f.name, key=f.key, options=list(options.items()), total=total)
    return result
```
</details>

---


### 模块: apiserver/paasng/paasng/accessories/log/management/commands/batch_disable_mount_hostpath.py


#### handle

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 66-105 (共 40 行, 0 行注释)  

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
            for env in module.envs.all():
                env_can_use_bklog = self.check_env_status(env)
                if env_can_use_bklog:
                    if not dry_run:
                        wl_app = env.wl_app
                        latest_config = wl_app.latest_config
                        latest_config.mount_log_to_host = False
                        if edge_disable:
                            latest_config.save(update_fields=['mount_log_to_host', 'updated'])
                        else:
                            pending_latest_config.append(latest_config)
                    self.stdout.write(f'disable hostpath log collector for Application<{application.code}> Module<{module.name}>Env<{env.environment}>', style_func=style_func)
                can_use_bklog = can_use_bklog and env_can_use_bklog
        if can_use_bklog:
            if not dry_run:
                application.feature_flag.set_feature(AppFeatureFlagConst.ENABLE_BK_LOG_COLLECTOR, True)
                for cfg in pending_latest_config:
                    cfg.save(update_fields=['mount_log_to_host', 'updated'])
            self.stdout.write(f'switch log query to bk-log index for Application<{application.code}>', style_func=style_func)
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
            print(f'credentials of instance {i.pk} is None')
            continue
        credentials = json.loads(i.credentials)
        if not credentials:
            print(f'credentials of instance {i.pk} is empty')
            continue
        to_update = {}
        prefix = 'LEGACY_'
        for (k, v) in credentials.items():
            if not k.startswith(prefix):
                to_update[f'{prefix}{k}'] = v
        if not to_update:
            continue
        print(f'updating instance {i.pk}')
        credentials.update(to_update)
        if not dry_run:
            i.credentials = json.dumps(credentials)
            i.save(update_fields=['credentials'])
```
</details>

---


### 模块: apiserver/paasng/paasng/accessories/services/providers/sentry/client.py


#### _request

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 34-73 (共 40 行, 0 行注释)  

**函数签名**:
```python
def _request ( self, method, path, data, timeout = 10 ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def _request(self, method, path, data, timeout=10):
    url = '{base_url}{path}'.format(base_url=self.base_url, path=path)
    headers = self.headers
    try:
        if method == 'GET':
            resp = requests.get(url=url, headers=headers, params=data, timeout=timeout)
        elif method == 'HEAD':
            resp = requests.head(url=url, headers=headers, timeout=timeout)
        elif method == 'POST':
            resp = requests.post(url=url, headers=headers, json=data, timeout=timeout)
        elif method == 'DELETE':
            resp = requests.delete(url=url, headers=headers, json=data)
        elif method == 'PUT':
            resp = requests.put(url=url, headers=headers, json=data)
        else:
            return False, None
    except requests.exceptions.RequestException:
        logger.exception('Request sentry failed, connection exception')
        raise RequestSentryAPIFail('Request sentry failed, connection exception')
    resp_json = {}
    try:
        if resp.status_code != 204:
            resp_json = resp.json()
    except Exception:
        logger.exception('Failed to request sentry, failed to parse json')
    if resp.status_code not in (200, 201, 202, 204, 409):
        logger.exception('Request sentry failed, return status is not 20X/409[method=%s, url=%s, data=%s, status=%s, resp=%s]', method, url, data, resp.status_code, resp_json)
        return False, resp_json
    return True, resp_json
```
</details>

---


### 模块: apiserver/paasng/paasng/accessories/smart_advisor/tagging.py


#### dig_tags_local_repo

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 36-68 (共 33 行, 0 行注释)  
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
    req_file = p / 'requirements.txt'
    if req_file.exists() and not req_file.is_symlink():
        tags.append(force_tag('app-pl:python'))
        requirements_txt = req_file.read_text(encoding='utf-8', errors='ignore')
        for pkg_name in ('celery', 'django', 'gunicorn', 'blueapps'):
            if py_module_in_requirements(pkg_name, requirements_txt):
                tags.append(force_tag('app-sdk:{}'.format(pkg_name)))
    for fname in p.iterdir():
        if fname.name.endswith('.go'):
            tags.append(force_tag('app-pl:go'))
            break
        if fname.name.endswith('.php'):
            tags.append(force_tag('app-pl:php'))
            break
    if (p / 'package.json').exists() and (p / 'index.js').exists():
        tags.append(force_tag('app-pl:nodejs'))
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
        raise error_codes.CANNOT_ROLLBACK_CURRENT_STEP.f(_('当前发布流程已结束'))
    if not self.release.retryable:
        raise error_codes.CANNOT_ROLLBACK_CURRENT_STEP.f(_('当前插件类型不支持重置历史版本, 如需发布请创建新的版本'))
    current_stage = self.release.current_stage
    if current_stage.invoke_method == constants.ReleaseStageInvokeMethod.ITSM and current_stage.status in constants.PluginReleaseStatus.running_status():
        raise error_codes.CANNOT_ROLLBACK_CURRENT_STEP.f(_('请先撤回审批单据, 再返回上一步'))
    if current_stage.invoke_method == constants.ReleaseStageInvokeMethod.DEPLOY_API and current_stage.status in constants.PluginReleaseStatus.running_status():
        raise error_codes.CANNOT_ROLLBACK_CURRENT_STEP.f(_('请等待部署完成, 再返回上一步'))
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
**行数**: 480-554 (共 75 行, 0 行注释)  
**描述**: make a validator to validate ReleaseVersion object

**函数签名**:
```python
def make_release_validator ( plugin: PluginInstance, version_rule: PluginReleaseVersionRule, release_type: str, revision_policy: str, revision_type: str ) :
```

**消息**: Complexity 17 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def make_release_validator(plugin: PluginInstance, version_rule: PluginReleaseVersionRule, release_type: str, revision_policy: str, revision_type: str):
    """make a validator to validate ReleaseVersion object"""
    
    def validate_semver(version: str, previous_version_str: Optional[str], semver_type: SemverAutomaticType):
        try:
            parsed_version = semver.VersionInfo.parse(version)
            previous_version = semver.VersionInfo.parse(previous_version_str or '0.0.0')
        except ValueError as e:
            raise ValidationError(str(e))
        if semver_type == SemverAutomaticType.MAJOR:
            computational_revision = previous_version.bump_major()
        elif semver_type == SemverAutomaticType.MINOR:
            computational_revision = previous_version.bump_minor()
        else:
            computational_revision = previous_version.bump_patch()
        if computational_revision != parsed_version:
            raise ValidationError({'revision': _('版本号不符合，下一个 {label} 版本是 {revision}').format(label=SemverAutomaticType.get_choice_label(semver_type), revision=computational_revision)})
        return True
    
    def validate_release_policy(plugin: PluginInstance, release_type: str, revision_policy: str, source_version_name: str):
        """Plugin version release rules, e.g., cannot release already published versions."""
        policy = REVISION_POLICIES.get(revision_policy)
        if not policy:
            return True
        source_version_exists = PluginRelease.objects.filter(plugin=plugin, source_version_name=source_version_name, type=release_type, **policy['filter']).exists()
        if source_version_exists:
            raise policy['error']
        return True
    
    def validator(self, attrs: Dict):
        if revision_type == PluginRevisionType.TESTED_VERSION and not attrs['release_id']:
            raise ValidationError(_('使用测试版本发布时必须传参数: release_id'))
        version = attrs['version']
        source_version_type = attrs['source_version_type']
        source_version_name = attrs['source_version_name']
        source_hash = get_source_hash_by_plugin_version(plugin, source_version_type, source_version_name, revision_type, attrs['release_id'])
        if version_rule == PluginReleaseVersionRule.AUTOMATIC:
            validate_semver(version, self.context['previous_version'], SemverAutomaticType(attrs['semver_type']))
        elif version_rule == PluginReleaseVersionRule.REVISION and version != source_version_name:
            raise ValidationError(_('版本号必须与代码分支一致'))
        elif version_rule == PluginReleaseVersionRule.COMMIT_HASH and version != source_hash:
            raise ValidationError(_('版本号必须与提交哈希一致'))
        elif version_rule == PluginReleaseVersionRule.BRANCH_TIMESTAMP and not version.startswith(source_version_name):
            raise ValidationError(_('版本号必须以代码分支开头'))
        if revision_policy:
            validate_release_policy(plugin, release_type, revision_policy, source_version_name)
        attrs['source_hash'] = source_hash
        attrs.pop('release_id')
        return attrs
    return validator
```
</details>

---


#### validator

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 526-552 (共 27 行, 0 行注释)  

**函数签名**:
```python
def validator ( self, attrs: Dict ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def validator(self, attrs: Dict):
    if revision_type == PluginRevisionType.TESTED_VERSION and not attrs['release_id']:
        raise ValidationError(_('使用测试版本发布时必须传参数: release_id'))
    version = attrs['version']
    source_version_type = attrs['source_version_type']
    source_version_name = attrs['source_version_name']
    source_hash = get_source_hash_by_plugin_version(plugin, source_version_type, source_version_name, revision_type, attrs['release_id'])
    if version_rule == PluginReleaseVersionRule.AUTOMATIC:
        validate_semver(version, self.context['previous_version'], SemverAutomaticType(attrs['semver_type']))
    elif version_rule == PluginReleaseVersionRule.REVISION and version != source_version_name:
        raise ValidationError(_('版本号必须与代码分支一致'))
    elif version_rule == PluginReleaseVersionRule.COMMIT_HASH and version != source_hash:
        raise ValidationError(_('版本号必须与提交哈希一致'))
    elif version_rule == PluginReleaseVersionRule.BRANCH_TIMESTAMP and not version.startswith(source_version_name):
        raise ValidationError(_('版本号必须以代码分支开头'))
    if revision_policy:
        validate_release_policy(plugin, release_type, revision_policy, source_version_name)
    attrs['source_hash'] = source_hash
    attrs.pop('release_id')
    return attrs
```
</details>

---


### 模块: apiserver/paasng/paasng/infras/accounts/permissions/global_site.py


#### gen_site_role_perm_map

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 62-123 (共 62 行, 0 行注释)  
**描述**: 根据不同的用户角色，生成对应的权限映射表

**函数签名**:
```python
def gen_site_role_perm_map ( role: SiteRole ) -> Dict[SiteAction, bool] :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def gen_site_role_perm_map(role: SiteRole) -> Dict[SiteAction, bool]:
    """根据不同的用户角色，生成对应的权限映射表"""
    perm_map = {SiteAction.VISIT_SITE: True, SiteAction.VISIT_ADMIN42: False, SiteAction.SYSAPI_READ_APPLICATIONS: False, SiteAction.SYSAPI_MANAGE_APPLICATIONS: False, SiteAction.SYSAPI_READ_SERVICES: False, SiteAction.SYSAPI_MANAGE_ACCESS_CONTROL: False, SiteAction.SYSAPI_MANAGE_LIGHT_APPLICATIONS: False, SiteAction.SYSAPI_READ_DB_CREDENTIAL: False, SiteAction.SYSAPI_BIND_DB_SERVICE: False, SiteAction.MANAGE_PLATFORM: False, SiteAction.MANAGE_APP_TEMPLATES: False, SiteAction.OPERATE_PLATFORM: False}
    if role == SiteRole.BANNED_USER:
        perm_map[SiteAction.VISIT_SITE] = False
    elif role in [SiteRole.ADMIN, SiteRole.SUPER_USER]:
        perm_map[SiteAction.VISIT_ADMIN42] = True
        perm_map[SiteAction.MANAGE_PLATFORM] = True
        perm_map[SiteAction.MANAGE_APP_TEMPLATES] = True
        perm_map[SiteAction.OPERATE_PLATFORM] = True
    elif role == SiteRole.PLATFORM_MANAGER:
        perm_map[SiteAction.VISIT_ADMIN42] = True
        perm_map[SiteAction.MANAGE_PLATFORM] = True
    elif role == SiteRole.APP_TEMPLATES_MANAGER:
        perm_map[SiteAction.VISIT_ADMIN42] = True
        perm_map[SiteAction.MANAGE_APP_TEMPLATES] = True
    elif role == SiteRole.PLATFORM_OPERATOR:
        perm_map[SiteAction.VISIT_ADMIN42] = True
        perm_map[SiteAction.OPERATE_PLATFORM] = True
    elif role == SiteRole.SYSTEM_API_BASIC_READER:
        perm_map[SiteAction.SYSAPI_READ_APPLICATIONS] = True
        perm_map[SiteAction.SYSAPI_READ_SERVICES] = True
    elif role == SiteRole.SYSTEM_API_BASIC_MAINTAINER:
        perm_map[SiteAction.SYSAPI_READ_APPLICATIONS] = True
        perm_map[SiteAction.SYSAPI_MANAGE_APPLICATIONS] = True
        perm_map[SiteAction.SYSAPI_READ_SERVICES] = True
        perm_map[SiteAction.SYSAPI_MANAGE_ACCESS_CONTROL] = True
    elif role == SiteRole.SYSTEM_API_LIGHT_APP_MAINTAINER:
        perm_map[SiteAction.SYSAPI_READ_APPLICATIONS] = True
        perm_map[SiteAction.SYSAPI_READ_SERVICES] = True
        perm_map[SiteAction.SYSAPI_MANAGE_LIGHT_APPLICATIONS] = True
    elif role == SiteRole.SYSTEM_API_LESSCODE:
        perm_map[SiteAction.SYSAPI_READ_APPLICATIONS] = True
        perm_map[SiteAction.SYSAPI_MANAGE_APPLICATIONS] = True
        perm_map[SiteAction.SYSAPI_READ_SERVICES] = True
        perm_map[SiteAction.SYSAPI_READ_DB_CREDENTIAL] = True
        perm_map[SiteAction.SYSAPI_BIND_DB_SERVICE] = True
    return perm_map
```
</details>

---


### 模块: apiserver/paasng/paasng/infras/iam/members/management/commands/migrate_bkpaas3_perm.py


#### _migrate_single

**复杂度分数**: 20  
**严重程度**: high_risk  
**行数**: 144-264 (共 121 行, 0 行注释)  
**描述**: 迁移单个应用权限数据

**函数签名**:
```python
def _migrate_single ( self, idx: int, app: Dict ) -> List :
```

**消息**: Complexity 20 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def _migrate_single(self, idx: int, app: Dict) -> List:
    """迁移单个应用权限数据"""
    (app_code, app_name, creator) = (app['code'], app['name'], app['creator'])
    migrate_logs = []
    administrator_key = (app_code, ApplicationRole.ADMINISTRATOR)
    developer_key = (app_code, ApplicationRole.DEVELOPER)
    operator_key = (app_code, ApplicationRole.OPERATOR)
    all_role_keys = [administrator_key, developer_key, operator_key]
    migrate_logs.append(f'start migrate application [{app_name}/{app_code}] user roles... {idx}/{self.total_count}')
    administrators = self.members_map[administrator_key]
    if not administrators:
        raise ValueError("application hasn't administrators")
    first_grade_manager = creator
    if creator not in administrators:
        first_grade_manager = administrators[0]
        migrate_logs.append(f"creator not app's administrators, use first administrator {first_grade_manager}")
    grade_manager_id = self.grade_manager_map.get(app_code)
    if not grade_manager_id:
        migrate_logs.append('grade manager not exists, create...')
        if first_grade_manager in self.exclude_users:
            first_grade_manager = None
            migrate_logs.append(f'{first_grade_manager} in exclude users, skip add as members...')
        else:
            migrate_logs.append(f'add {first_grade_manager} as grade manager members...')
        grade_manager_id = self.cli.create_grade_managers(app_code, app_name, first_grade_manager)
        self.grade_manager_map[app_code] = grade_manager_id
        ApplicationGradeManager.objects.create(app_code=app_code, grade_manager_id=grade_manager_id)
    migrate_logs.append(f'add grade manager (id: {grade_manager_id}) members: count: {len(administrators)}, users: {administrators}')
    for username in administrators:
        if username in self.exclude_users:
            migrate_logs.append(f'user {username} in exclude user list, skip add as grade manager')
            continue
        try:
            self.cli.add_grade_manager_members(grade_manager_id, [username])
        except Exception as e:
            migrate_logs.append(f'failed to add grade manager: {username}, maybe was resigned: {str(e)}')
    exists_user_group_ids = [self.user_group_map[role_key] for role_key in all_role_keys if role_key in self.user_group_map]
    if len(exists_user_group_ids) < len(all_role_keys):
        if exists_user_group_ids:
            migrate_logs.append(f'user groups {exists_user_group_ids} exists, clean them and recreate...')
            self.cli.delete_user_groups(exists_user_group_ids)
            ApplicationUserGroup.objects.filter(app_code=app_code).delete()
        groups = self.cli.create_builtin_user_groups(grade_manager_id, app_code)
        for group in groups:
            (role, group_id, group_name) = (group['role'], group['id'], group['name'])
            migrate_logs.append(f'create user group id: {group_id}, role: {ApplicationRole(role).name}, name: {group_name}')
            self.user_group_map[app_code, role] = group_id
            ApplicationUserGroup.objects.create(app_code=app_code, role=role, user_group_id=group_id)
        self.cli.grant_user_group_policies(app_code, app_name, groups)
    user_group_id = self.user_group_map[administrator_key]
    migrate_logs.append(f'try add user_group (id: {user_group_id}, role: {ApplicationRole.ADMINISTRATOR.name}) members...count: {len(administrators)}, users: {administrators}')
    for username in administrators:
        try:
            self.cli.add_user_group_members(user_group_id, [username], NEVER_EXPIRE_DAYS)
        except Exception as e:
            migrate_logs.append(f'failed to add app administrator: {username}, maybe was resigned: {str(e)}')
    if developers := self.members_map[developer_key]:
        user_group_id = self.user_group_map[developer_key]
        migrate_logs.append(f'try add user_group (id: {user_group_id}, role: {ApplicationRole.DEVELOPER.name}) members...count: {len(developers)}, users: {developers}')
        for username in developers:
            try:
                self.cli.add_user_group_members(user_group_id, [username], NEVER_EXPIRE_DAYS)
            except Exception as e:
                migrate_logs.append(f'failed to add app developer: {username}, maybe was resigned: {str(e)}')
    if operators := self.members_map[operator_key]:
        user_group_id = self.user_group_map[operator_key]
        migrate_logs.append(f'try add user_group (id: {user_group_id}, role: {ApplicationRole.OPERATOR.name}) members...count: {len(operators)}, users: {operators}')
        for username in operators:
            try:
                self.cli.add_user_group_members(user_group_id, [username], NEVER_EXPIRE_DAYS)
            except Exception as e:
                migrate_logs.append(f'failed to add app operator: {username}, maybe was resigned: {str(e)}')
    migrate_logs.append(f'migrate application [{app_name}/{app_code}] user role success! {idx}/{self.total_count}')
    return migrate_logs
```
</details>

---


### 模块: apiserver/paasng/paasng/infras/perm_insure/views_perm.py


#### check_drf_view_perm

**复杂度分数**: 12  
**严重程度**: warning  
**行数**: 85-122 (共 38 行, 0 行注释)  
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
    if view_cls.__name__ in INSURE_CHECKING_EXCLUDED_VIEWS:
        return
    if issubclass(view_cls, ViewSetMixin):
        unprotected_actions = get_unprotected_actions(view_func)
        if view_func.actions and not unprotected_actions:
            return
    elif issubclass(view_cls, APIView):
        pass
    else:
        raise TypeError('not a valid DRF View')
    enabled_perm = view_cls.permission_classes
    if is_admin42:
        if not any((is_admin42_permission(p) for p in enabled_perm)):
            raise ImproperlyConfigured(f'The view class {view_cls} has no site_perm_class configured in permission_classes')
    if not enabled_perm or len(enabled_perm) == 1 and enabled_perm[0].__name__ == 'IsAuthenticated':
        name = view_cls if not unprotected_actions else f'{view_cls} - {unprotected_actions!r}'
        raise ImproperlyConfigured('The view class {} has no extra permission_classes configured other than `IsAuthenticated`, this may be a bug and lead to a permission leak error, add the view name to `perm_insure.conf.INSURE_CHECKING_EXCLUDED_VIEWS` if this is intended.'.format(name))
```
</details>

---


### 模块: apiserver/paasng/paasng/misc/audit/views.py


#### filter_queryset

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 50-77 (共 28 行, 0 行注释)  

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
    if target := query_params.get('target'):
        queryset = queryset.filter(target=target)
    if operation := query_params.get('operation'):
        queryset = queryset.filter(operation=operation)
    if access_type := query_params.get('access_type'):
        queryset = queryset.filter(access_type=access_type)
    if 'result_code' in query_params:
        result_code = query_params['result_code']
        queryset = queryset.filter(result_code=result_code)
    if module_name := query_params.get('module_name'):
        queryset = queryset.filter(module_name=module_name)
    if environment := query_params.get('environment'):
        queryset = queryset.filter(environment=environment)
    if start_time := query_params.get('start_time'):
        queryset = queryset.filter(created__gte=start_time)
    if end_time := query_params.get('end_time'):
        queryset = queryset.filter(created__lte=end_time)
    if operator := query_params.get('operator'):
        operator = user_id_encoder.encode(settings.USER_TYPE, operator)
        queryset = queryset.filter(user=operator)
    return queryset
```
</details>

---


### 模块: apiserver/paasng/paasng/plat_admin/numbers/app.py


#### get_results

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 353-401 (共 49 行, 0 行注释)  
**描述**: Return simple apps as result

**函数签名**:
```python
def get_results ( self ) -> Generator[SimpleApp, None, None] :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def get_results(self) -> Generator[SimpleApp, None, None]:
    """Return simple apps as result"""
    session = legacy_db.get_scoped_session()
    qs = self.get_default_qs(session)
    for app in qs.all():
        deploy_status = self.get_deploy_status(app)
        normalizer = LegacyAppNormalizer(app)
        region = normalizer.get_region()
        if not region:
            continue
        if app.code.startswith('collection_'):
            continue
        developers = normalizer.get_developers()
        if self.filter_app_codes_enabled and app.code not in self.filter_app_codes:
            continue
        if self.filter_developers_enabled and not self.filter_developers_devs & set(developers):
            continue
        if hasattr(app, 'svn_domain'):
            source_location = f'svn://{app.svn_domain}:80/apps/{app.code}'
        else:
            source_location = ''
        market_address = market_tag = None
        if self.include_market_info:
            market_address = self.get_market_address(region=region, app_code=app.code)
            market_tag = self.get_tag_display_name(app.tags_id)
        sim_app = SimpleApp(_source=SimpleAppSource.LEGACY, name=app.name, type='legacy', region=region, code=app.code, created=app.created_date, deploy_status=deploy_status, source_origin=SourceOrigin.AUTHORIZED_VCS.value, source_repo_type='bk_svn', source_location=source_location, engine_enabled=True, creator=normalizer.get_creator(), developers=developers, market_address=market_address, market_tag=market_tag)
        yield sim_app
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/applications/models.py


#### filter_queryset

**复杂度分数**: 12  
**严重程度**: warning  
**行数**: 141-180 (共 40 行, 0 行注释)  
**描述**: Filter applications by given parameters

**函数签名**:
```python
def filter_queryset ( cls, queryset: QuerySet, include_inactive = False, regions = None, languages = None, search_term = '', has_deployed: Optional[bool] = None, source_origin: Optional[SourceOrigin] = None, type_: Optional[ApplicationType] = None, order_by: Optional[List] = None, market_enabled: Optional[bool] = None ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

@classmethod
def filter_queryset(cls, queryset: QuerySet, include_inactive=False, regions=None, languages=None, search_term='', has_deployed: Optional[bool] = None, source_origin: Optional[SourceOrigin] = None, type_: Optional[ApplicationType] = None, order_by: Optional[List] = None, market_enabled: Optional[bool] = None):
    """Filter applications by given parameters"""
    if order_by is None:
        order_by = []
    if queryset.model is not Application:
        raise ValueError('BaseApplicationFilter only support to filter Application')
    if regions:
        queryset = queryset.filter_by_regions(regions)
    if languages:
        queryset = queryset.filter_by_languages(languages)
    if search_term:
        queryset = queryset.search_by_code_or_name(search_term)
    if has_deployed is not None:
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
**行数**: 71-124 (共 54 行, 0 行注释)  
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
    overlay_replicas: NotSetType | list = NOTSET
    overlay_res_quotas: NotSetType | list = NOTSET
    overlay_env_vars: NotSetType | list = NOTSET
    overlay_autoscaling: NotSetType | list = NOTSET
    overlay_mounts: NotSetType | list = NOTSET
    if not isinstance(spec_entity.env_overlay, NotSetType):
        eo = spec_entity.env_overlay
        if eo:
            overlay_replicas = [] if eo.replicas is None else eo.replicas
            overlay_res_quotas = [] if eo.res_quotas is None else eo.res_quotas
            overlay_env_vars = [] if eo.env_variables is None else eo.env_variables
            overlay_autoscaling = [] if eo.autoscaling is None else eo.autoscaling
            overlay_mounts = [] if eo.mounts is None else eo.mounts
    sync_processes(module, processes=spec_entity.processes, manager=manager)
    if build := spec_entity.build:
        sync_build(module, build)
    sync_hooks(module, spec_entity.hooks, manager)
    sync_env_vars(module, env_vars, overlay_env_vars)
    if addons := spec_entity.addons:
        sync_addons(module, addons)
    if mounts or overlay_mounts:
        sync_mounts(module, mounts, overlay_mounts, manager)
    sync_svc_discovery(module, spec_entity.svc_discovery, manager)
    sync_domain_resolution(module, spec_entity.domain_resolution, manager)
    sync_observability(module, spec_entity.observability)
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
**行数**: 204-247 (共 44 行, 0 行注释)  
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
    for proc_spec in ModuleProcessSpec.objects.filter(module=module).order_by('created'):
        for item in ProcessSpecEnvOverlay.objects.filter(proc_spec=proc_spec):
            if item.target_replicas is not None and item.target_replicas != proc_spec.target_replicas:
                overlay.append_item('replicas', crd.ReplicasOverlay(envName=item.environment_name, process=proc_spec.name, count=item.target_replicas))
            if item.scaling_config and item.autoscaling and item.scaling_config != proc_spec.scaling_config:
                overlay.append_item('autoscaling', crd.AutoscalingOverlay(envName=item.environment_name, process=proc_spec.name, minReplicas=item.scaling_config.min_replicas, maxReplicas=item.scaling_config.max_replicas, policy=item.scaling_config.policy))
            if item.plan_name and item.plan_name != proc_spec.plan_name:
                overlay.append_item('resQuotas', crd.ResQuotaOverlay(envName=item.environment_name, process=proc_spec.name, plan=self.get_quota_plan(item.plan_name)))
    model_res.spec.envOverlay = overlay
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/declarative/application/validations/v2.py


#### to_internal_value

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 131-160 (共 30 行, 0 行注释)  

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
    attrs['name_en'] = attrs.get('name_en') or attrs['name_zh_cn']
    has_default = False
    for module_desc in attrs['modules'].values():
        if module_desc.is_default:
            if has_default:
                raise serializers.ValidationError({'modules': _('一个应用只能有一个主模块')})
            has_default = True
    if not has_default:
        raise serializers.ValidationError({'modules': _('一个应用必须有一个主模块')})
    for (module_name, module_desc) in attrs['modules'].items():
        for svc in module_desc.services:
            if svc.shared_from and svc.shared_from not in attrs['modules']:
                raise serializers.ValidationError({f'modules[{module_name}].services': _('提供共享增强服务的模块不存在')})
    attrs.setdefault('plugins', [])
    if self.context.get('app_version'):
        attrs['plugins'].append({'type': AppDescPluginType.APP_VERSION, 'data': self.context.get('app_version')})
    if self.context.get('spec_version'):
        attrs['spec_version'] = self.context['spec_version']
    return ApplicationDesc(instance_existed=bool(self.instance), **attrs)
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/declarative/application/validations/v3.py


#### to_internal_value

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 122-155 (共 34 行, 0 行注释)  

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
    attrs['name_en'] = attrs.get('name_en') or attrs['name_zh_cn']
    modules_list = attrs.pop('modules')
    attrs['modules'] = {module_desc.name: module_desc for module_desc in modules_list}
    has_default = False
    for module_desc in modules_list:
        if module_desc.is_default:
            if has_default:
                raise serializers.ValidationError({'modules': _('一个应用只能有一个主模块')})
            has_default = True
    if not has_default:
        raise serializers.ValidationError({'modules': _('一个应用必须有一个主模块')})
    for (idx, module_desc) in enumerate(modules_list):
        for svc in module_desc.services:
            if svc.shared_from and svc.shared_from not in attrs['modules']:
                raise serializers.ValidationError({f'modules[{idx}].spec.addons': _('提供共享增强服务的模块不存在')})
    attrs.setdefault('plugins', [])
    if self.context.get('app_version'):
        attrs['plugins'].append({'type': AppDescPluginType.APP_VERSION, 'data': self.context.get('app_version')})
    if self.context.get('spec_version'):
        attrs['spec_version'] = self.context['spec_version']
    return ApplicationDesc(instance_existed=bool(self.instance), **attrs)
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/declarative/deployment/validations/v2.py


#### to_internal_value

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 80-153 (共 74 行, 0 行注释)  

**函数签名**:
```python
def to_internal_value ( self, data ) -> DeploymentDesc :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def to_internal_value(self, data) -> DeploymentDesc:
    attrs = super().to_internal_value(data)
    processes = []
    for (proc_type, process) in attrs['processes'].items():
        processes.append({'name': proc_type, 'replicas': process['replicas'], 'res_quota_plan': get_quota_plan(process['plan']) if process.get('plan') else None, 'proc_command': process['command'], 'command': None, 'args': shlex.split(process['command']), 'probes': process.get('probes')})
    hooks: NotSetType | dict = NOTSET
    if attrs['scripts'] and pre_release_hook := attrs['scripts'].get('pre_release_hook'):
        hooks = {'pre_release': {'command': [], 'args': shlex.split(pre_release_hook)}}
    global_vars = []
    env_vars = []
    for env_var in attrs.get('env_variables', []):
        if env_var['environment_name'] == ConfigVarEnvName.GLOBAL:
            global_vars.append({'name': env_var['key'], 'value': env_var['value']})
        else:
            env_vars.append({'env_name': env_var['environment_name'], 'name': env_var['key'], 'value': env_var['value']})
    env_overlay: NotSetType | dict
    if not env_vars:
        env_overlay = NOTSET
    else:
        env_overlay = {'env_variables': env_vars}
    _svc_discovery_value = attrs.get('svc_discovery')
    svc_discovery: NotSetType | dict[str, list[dict]]
    if _svc_discovery_value == NOTSET:
        svc_discovery = NOTSET
    else:
        svc_discovery = {}
        if bk_sass := _svc_discovery_value.get('bk_saas'):
            svc_discovery['bk_saas'] = [{'bk_app_code': item['bk_app_code'], 'module_name': item.get('module_name')} for item in bk_sass]
    spec = v1alpha2.BkAppSpec(processes=processes, hooks=hooks, configuration={'env': global_vars}, env_overlay=env_overlay, svc_discovery=svc_discovery)
    return cattr.structure({'language': attrs['language'], 'source_dir': attrs['source_dir'], 'bk_monitor': attrs.get('bk_monitor', None), 'spec_version': AppSpecVersion.VER_2, 'spec': spec}, DeploymentDesc)
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/declarative/handlers.py


#### _find_module_desc_data

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 367-415 (共 49 行, 0 行注释)  
**描述**: Find a module's desc data in the json data. This function can be used in both v2 and v3

**函数签名**:
```python
def _find_module_desc_data ( json_data: Dict, module_name: Optional[str], modules_data_type: Literal['list', 'dict'] ) -> Dict :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def _find_module_desc_data(json_data: Dict, module_name: Optional[str], modules_data_type: Literal['list', 'dict']) -> Dict:
    """Find a module's desc data in the json data. This function can be used in both v2 and v3
    because them have similar(but slightly different) structure.

    In the `json_data` 2 fields are used to store the module data:

    - "module": contains desc data of the default module.
    - "modules": contains desc data of multiple modules, use a list(v3) or dict(v2) format.

    :param modules_data_type: The data type that holds the modules data, v2 using dict, v3 using list.
    """
    if not module_name:
        desc_data = json_data.get('module')
        if not desc_data:
            raise DescriptionValidationError({'module': _('模块配置内容不能为空')})
        return desc_data
    desc_data = None
    if modules_data := json_data.get('modules'):
        if modules_data_type == 'dict':
            desc_data = modules_data.get(module_name)
            existed_modules = ', '.join(modules_data.keys())
        elif modules_data_type == 'list':
            desc_data = next((m for m in modules_data if m['name'] == module_name), None)
            existed_modules = ', '.join((m['name'] for m in modules_data))
        else:
            raise ValueError('Wrong modules data type')
        desc_data = desc_data or json_data.get('module')
        if not desc_data:
            raise DescriptionValidationError({'modules': _('未找到 {} 模块的配置，当前已配置模块为 {}').format(module_name, existed_modules)})
    if not desc_data:
        desc_data = json_data.get('module')
    if not desc_data:
        raise DescriptionValidationError({'module': _('模块配置内容不能为空')})
    return desc_data
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/engine/deploy/bg_build/executors.py


#### _start_following_logs

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 333-373 (共 41 行, 0 行注释)  
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
        self.stream.write_message('Pipeline is running, please wait patiently...')
        try:
            build_status = self.ctl.retrieve_build_status(pb)
        except BkCIGatewayServiceError:
            logger.exception(f'call bk_ci pipeline for build status and logs failed during deploy[{self.bp}]')
            raise
        if build_status.status in [PipelineBuildStatus.SUCCEED, PipelineBuildStatus.FAILED, PipelineBuildStatus.CANCELED]:
            logger.info('break poll loop with pipeline build status: %s', build_status.status)
            break
    start_following = False
    for log in self.ctl.retrieve_full_log(pb).logs:
        if not (log.tag.startswith('e-') and log.jobId == self.bk_ci_pipeline_job_id):
            continue
        if '[Output]' in log.message:
            break
        if '[Install plugin]' in log.message:
            start_following = True
        if start_following:
            self.stream.write_message(re.sub(self.bk_ci_log_level_tag_regex, '', log.message))
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/engine/deploy/bg_wait/wait_bkapp.py


#### get_status

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 164-213 (共 50 行, 0 行注释)  

**函数签名**:
```python
def get_status ( self ) -> PollingResult :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def get_status(self) -> PollingResult:
    deploy_id = self.params['deploy_id']
    dp = AppModelDeploy.objects.get(id=deploy_id)
    mres = get_mres_from_cluster(ModuleEnvironment.objects.get(application_id=dp.application_id, module_id=dp.module_id, environment=dp.environment_name))
    if not mres:
        return PollingResult.doing()
    if mres.metadata.annotations.get(BKPAAS_DEPLOY_ID_ANNO_KEY) != str(deploy_id):
        return PollingResult.done(data={'state': ModelResState(DeployStatus.UNKNOWN, 'Abandoned', 'deployment have been abandoned'), 'last_update': mres.status.lastUpdate})
    if mres.status.deployId != str(deploy_id):
        return PollingResult.doing(data={'bkapp.status.deployId': mres.status.deployId})
    state = MresConditionParser(mres).detect_state()
    if state.status == DeployStatus.READY:
        return PollingResult.done(data={'state': state, 'last_update': mres.status.lastUpdate})
    elif state.status == DeployStatus.ERROR:
        polling_failure_count = 1
        if self.metadata.last_polling_data and 'polling_failure_count' in self.metadata.last_polling_data:
            polling_failure_count = self.metadata.last_polling_data['polling_failure_count'] + 1
        if polling_failure_count > CNATIVE_DEPLOY_STATUS_POLLING_FAILURE_LIMITS:
            return PollingResult.done(data={'state': state, 'last_update': mres.status.lastUpdate})
        return PollingResult.doing(data={'polling_failure_count': polling_failure_count})
    elif state.status == DeployStatus.PROGRESSING:
        update_status(dp, state, last_transition_time=mres.status.lastUpdate)
    return PollingResult.doing()
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/engine/deploy/release/operator.py


#### release_by_k8s_operator

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 84-180 (共 97 行, 0 行注释)  
**描述**: Create a new release for given environment(which will be handled by k8s operator).

**函数签名**:
```python
def release_by_k8s_operator ( env: ModuleEnvironment, revision: AppModelRevision, operator: str, build: Optional[Build] = None, deployment: Optional[Deployment] = None ) -> str :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def release_by_k8s_operator(env: ModuleEnvironment, revision: AppModelRevision, operator: str, build: Optional[Build] = None, deployment: Optional[Deployment] = None) -> str:
    """Create a new release for given environment(which will be handled by k8s operator).
    this action will start an async waiting procedure which waits for the release to be finished.

    :param env: The environment to create the release for.
    :param revision: The revision to be released.
    :param operator: current operator's user_id
    :param deployment: the deployment of the release

    :raises: ValueError when image credential_refs is invalid  TODO: 抛更具体的异常
    :raises: UnprocessibleEntityError when k8s can not process this manifest
    :raises: other unknown exceptions...
    """
    application = env.application
    module = env.module
    default_name = f'{application.code}-{revision.pk}-{int(time.time())}'
    try:
        app_model_deploy = AppModelDeploy.objects.create(application_id=application.id, module_id=module.id, environment_name=env.environment, name=default_name, revision=revision, status=DeployStatus.PENDING.value, operator=operator)
    except IntegrityError:
        logger.warning('Name conflicts when creating new AppModelDeploy object, name: %s.', default_name)
        raise
    try:
        advanced_options = deployment.advanced_options if deployment else None
        bkapp_res = get_bkapp_resource_for_deploy(env, deploy_id=str(app_model_deploy.id), force_image=build.image if build else None, image_pull_policy=advanced_options.image_pull_policy if advanced_options else None, use_cnb=build.is_build_from_cnb() if build else False, deployment=deployment)
        ensure_namespace(env)
        svc_disc.apply_configmap(env, bkapp_res)
        deploy_addons_tls_certs(env)
        deploy_volume_source(env)
        deployed_manifest = apply_bkapp_to_k8s(env, bkapp_res.to_deployable())
        ensure_bk_log_if_need(env)
        sync_service_monitor(env)
    except Exception:
        app_model_deploy.status = DeployStatus.ERROR
        app_model_deploy.save(update_fields=['status', 'updated'])
        raise
    revision.deployed_value = deployed_manifest
    revision.has_deployed = True
    revision.save(update_fields=['deployed_value', 'has_deployed', 'updated'])
    if bkapp_res.spec.hooks and bkapp_res.spec.hooks.preRelease and deployment:
        exec_bkapp_hook.delay(bkapp_res.metadata.name, app_model_deploy.id, deployment.id)
    WaitAppModelReady.start({'env_id': env.id, 'deploy_id': app_model_deploy.id, 'deployment_id': deployment.id if deployment else None}, DeployStatusHandler)
    return str(app_model_deploy.id)
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/engine/utils/source.py


#### download_source_to_dir

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 237-307 (共 71 行, 0 行注释)  
**描述**: Download and extract the module's source files to local path, will generate Procfile if necessary

**函数签名**:
```python
def download_source_to_dir ( module: Module, operator: str, deployment: Deployment, root_path: Path ) -> tuple[str, Path] :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def download_source_to_dir(module: Module, operator: str, deployment: Deployment, root_path: Path) -> tuple[str, Path]:
    """Download and extract the module's source files to local path, will generate Procfile if necessary

    :param root_path: The local path to download the source files
    :return: (the configured source directory string, the source directory path), the path can be different
        with the `root_path` if source_dir is configured.
    :raise ValueError: If the configured source directory is invalid
    """
    spec = ModuleSpecs(module)
    if spec.source_origin_specs.source_origin in [SourceOrigin.AUTHORIZED_VCS, SourceOrigin.SCENE]:
        get_repo_controller(module, operator=operator).export(root_path, deployment.version_info)
    elif spec.deploy_via_package:
        PackageController.init_by_module(module, operator).export(root_path, deployment.version_info)
    else:
        raise NotImplementedError
    source_dir_str_deployment = str(deployment.get_source_dir())
    source_dir_str_desc = ''
    if ModuleSpecs(module).deploy_via_package:
        try:
            desc_obj = DeploymentDescription.objects.get(deployment=deployment)
        except DeploymentDescription.DoesNotExist:
            pass
        else:
            source_dir_str_desc = desc_obj.source_dir
    source_dir_str = source_dir_str_deployment
    if source_dir_str_desc and source_dir_str_desc != source_dir_str_deployment:
        logger.warning('The source_dir in deployment description is different from the one in deployment object: %s != %s', source_dir_str_desc, source_dir_str_deployment)
        source_dir_str = source_dir_str_desc
    source_dir = validate_source_dir_str(root_path, source_dir_str)
    if module.application.type == ApplicationType.CLOUD_NATIVE and module.build_config.build_method == RuntimeType.DOCKERFILE:
        logger.info('Skip Procfile patching for Dockerfile cnative application.')
        return source_dir_str, source_dir
    if reason := patch_source_dir_procfile(source_dir=source_dir, procfile=deployment.get_procfile()):
        logger.warning('skip the source patching process: %s', reason)
    return source_dir_str, source_dir
```
</details>

---


#### get_deploy_desc_handler_by_version

**复杂度分数**: 12  
**严重程度**: warning  
**行数**: 175-224 (共 50 行, 0 行注释)  
**描述**: Get the description handler for the given module and version.

**函数签名**:
```python
def get_deploy_desc_handler_by_version ( module: Module, operator: str, version_info: VersionInfo, source_dir: Path = _current_path ) -> DeployDescHandler :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def get_deploy_desc_handler_by_version(module: Module, operator: str, version_info: VersionInfo, source_dir: Path = _current_path) -> DeployDescHandler:
    """Get the description handler for the given module and version.

    :param module: The module object
    :param operator: The operator name
    :param version_info: The version info, will be used to read the description file
    :param source_dir: The source directory path to find the description file
    :return: The handler instance
    :raise InitDeployDescHandlerError: When fail to initialize the handler instance
    """
    try:
        metadata_reader = get_metadata_reader(module, operator=operator, source_dir=source_dir)
    except NotImplementedError:
        raise InitDeployDescHandlerError('Unsupported source type')
    (app_desc, app_desc_exc) = (None, None)
    if not _description_flag_disabled(module.application):
        try:
            app_desc = metadata_reader.get_app_desc(version_info)
        except GetAppYamlFormatError as e:
            raise InitDeployDescHandlerError(str(e))
        except GetAppYamlError as e:
            app_desc_exc = e
    (procfile_data, procfile_exc) = (None, None)
    try:
        procfile_data = metadata_reader.get_procfile(version_info)
    except GetProcfileFormatError as e:
        raise InitDeployDescHandlerError(str(e))
    except GetProcfileError as e:
        procfile_exc = e
    if not (app_desc or procfile_data):
        msg = []
        if app_desc_exc:
            msg.append(f'[app_desc] {app_desc_exc}')
        if procfile_exc:
            msg.append(f'[Procfile] {procfile_exc}')
        raise InitDeployDescHandlerError('; '.join(msg))
    try:
        return get_deploy_desc_handler(app_desc, procfile_data)
    except ValueError as e:
        raise InitDeployDescHandlerError(str(e))
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/evaluation/evaluators.py


#### _evaluate_by_user_visit

**复杂度分数**: 15  
**严重程度**: warning  
**行数**: 156-196 (共 41 行, 0 行注释)  

**函数签名**:
```python
def _evaluate_by_user_visit ( self ) :
```

**消息**: Complexity 15 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def _evaluate_by_user_visit(self):
    if not (self.report.pv and self.report.uv):
        self.result.issue_type = OperationIssueType.UNVISITED
        self.result.issues.append(f'应用最近 {self.visit_summary.time_range} 没有访问记录')
    for (mod_name, mod) in self.visit_summary.modules.items():
        for (env_name, env) in mod.envs.items():
            env_res_summary = self.res_summary.modules[mod_name].envs[env_name]
            if not (env_res_summary.cpu_requests and env_res_summary.mem_requests):
                continue
            if env.pv and env.uv:
                continue
            env_result = self.result.modules[mod_name].envs[env_name]
            env_result.issue_type = OperationIssueType.UNVISITED
            env_result.issues.append(f'该环境最近 {self.visit_summary.time_range} 没有访问记录')
            (is_low_cpu_usage, any_proc_running) = (True, False)
            for proc in self.res_summary.modules[mod_name].envs[env_name].procs:
                if not (proc.quota and proc.cpu):
                    continue
                any_proc_running = True
                if proc.cpu.max / proc.quota.limits.cpu > 0.01:
                    is_low_cpu_usage = False
                    break
            if is_low_cpu_usage and any_proc_running:
                env_result.issues.append(f'CPU 使用率低于 1% 且近 {self.res_summary.time_range} 使用量没有波动')
                env_result.issue_type = OperationIssueType.IDLE
                self.result.issue_type = OperationIssueType.IDLE
                self.result.issues.append(f'模块 {mod_name} 环境 {env_name} 近 {self.visit_summary.time_range} 没有访问记录' + f' 且 近 {self.res_summary.time_range} CPU 使用率低于 1%')
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/evaluation/tasks.py


#### _update_or_create_operation_report

**复杂度分数**: 17  
**严重程度**: high_risk  
**行数**: 52-124 (共 73 行, 0 行注释)  

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
    (cpu_requests, mem_requests, cpu_limits, mem_limits) = (0, 0, 0, 0)
    (cpu_usage_avg_val, mem_usage_avg_val) = (0.0, 0.0)
    for module in res_summary.modules.values():
        for procs in [module.envs[AppEnvName.STAG].procs, module.envs[AppEnvName.PROD].procs]:
            for proc in procs:
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
    (total_pv, total_uv) = (0, 0)
    visit_summary = AppUserVisitCollector(app).collect()
    for mod in visit_summary.modules.values():
        for env in [mod.envs[AppEnvName.STAG], mod.envs[AppEnvName.PROD]]:
            total_pv += env.pv
            total_uv += env.uv
    deploy_summary = AppDeploymentCollector(app).collect()
    latest_deployment = Deployment.objects.filter(app_environment__application=app).order_by('-created').first()
    latest_operation = Operation.objects.filter(application=app).order_by('-created').first()
    defaults = {'cpu_requests': cpu_requests, 'mem_requests': mem_requests, 'cpu_limits': cpu_limits, 'mem_limits': mem_limits, 'cpu_usage_avg': round(cpu_usage_avg_val / cpu_limits, 4) if cpu_limits else 0, 'mem_usage_avg': round(mem_usage_avg_val / mem_limits, 4) if mem_limits else 0, 'res_summary': asdict(res_summary), 'pv': total_pv, 'uv': total_uv, 'visit_summary': asdict(visit_summary), 'latest_deployed_at': latest_deployment.created if latest_deployment else None, 'latest_deployer': get_username_by_bkpaas_user_id(latest_deployment.operator) if latest_deployment else None, 'latest_operated_at': latest_operation.created if latest_operation else None, 'latest_operator': latest_operation.get_operator() if latest_operation else None, 'latest_operation': latest_operation.get_operate_display() if latest_operation else None, 'deploy_summary': asdict(deploy_summary), 'administrators': fetch_role_members(app.code, ApplicationRole.ADMINISTRATOR), 'developers': fetch_role_members(app.code, ApplicationRole.DEVELOPER), 'collected_at': timezone.now()}
    (report, _) = AppOperationReport.objects.update_or_create(app=app, defaults=defaults)
    evaluate_result = AppOperationEvaluator(report, res_summary, visit_summary, deploy_summary).evaluate()
    report.issue_type = evaluate_result.issue_type
    report.evaluate_result = asdict(evaluate_result)
    report.save(update_fields=['issue_type', 'evaluate_result'])
```
</details>

---


#### send_idle_email_to_app_developers

**复杂度分数**: 12  
**严重程度**: warning  
**行数**: 168-234 (共 67 行, 0 行注释)  
**描述**: 发送应用闲置模块邮件给应用管理员/开发者

**函数签名**:
```python
def send_idle_email_to_app_developers ( app_codes: List[str], only_specified_users: List[str], exclude_specified_users: List[str] ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

@shared_task
def send_idle_email_to_app_developers(app_codes: List[str], only_specified_users: List[str], exclude_specified_users: List[str]):
    """发送应用闲置模块邮件给应用管理员/开发者"""
    reports = AppOperationReport.objects.filter(issue_type=OperationIssueType.IDLE)
    if app_codes:
        reports = reports.filter(app__code__in=app_codes)
    if not reports.exists():
        logger.info('no idle app reports, skip current notification task')
        return
    waiting_notify_usernames = set()
    for r in reports:
        waiting_notify_usernames.update(r.administrators)
        waiting_notify_usernames.update(r.developers)
    if only_specified_users:
        waiting_notify_usernames &= set(only_specified_users)
    if exclude_specified_users:
        waiting_notify_usernames -= set(exclude_specified_users)
    (total_cnt, succeed_cnt) = (len(waiting_notify_usernames), 0)
    failed_usernames = []
    task = AppOperationEmailNotificationTask.objects.create(total_count=total_cnt, notification_type=EmailNotificationType.IDLE_APP_MODULE_ENVS)
    for (idx, username) in enumerate(waiting_notify_usernames):
        filters = ApplicationPermission().gen_develop_app_filters(username)
        app_codes = Application.objects.filter(is_active=True).filter(filters).values_list('code', flat=True)
        if just_leave_app_codes := JustLeaveAppManager(username).list():
            app_codes = [c for c in app_codes if c not in just_leave_app_codes]
        user_idle_app_reports = reports.filter(app__code__in=app_codes)
        if not user_idle_app_reports.exists():
            total_cnt -= 1
            logger.info('no idle app reports, skip notification to %s', username)
            continue
        try:
            AppOperationReportNotifier().send(user_idle_app_reports, EmailReceiverType.APP_DEVELOPER, [username])
        except Exception:
            failed_usernames.append(username)
            logger.exception('failed to send idle module envs email to %s', username)
        succeed_cnt += 1
        if idx % 20 == 0:
            task.succeed_count = succeed_cnt
            task.failed_count = len(failed_usernames)
            task.save(update_fields=['succeed_count', 'failed_count'])
    task.total_count = total_cnt
    task.succeed_count = succeed_cnt
    task.failed_count = len(failed_usernames)
    task.failed_usernames = failed_usernames
    task.status = BatchTaskStatus.FINISHED
    task.end_at = timezone.now()
    task.save(update_fields=['total_count', 'succeed_count', 'failed_count', 'failed_usernames', 'status', 'end_at'])
```
</details>

---


### 模块: apiserver/paasng/paasng/platform/modules/manager.py


#### initialize_app_model_resource

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 257-318 (共 62 行, 0 行注释)  

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
    if self.application.type != ApplicationType.CLOUD_NATIVE:
        return
    if not bkapp_spec or bkapp_spec['build_config'].build_method != RuntimeType.CUSTOM_IMAGE:
        return
    build_config = bkapp_spec['build_config']
    config_obj = BuildConfig.objects.get_or_create_by_module(self.module)
    build_params = {'image_repository': build_config.image_repository, 'image_credential_name': None}
    if image_credential := build_config.image_credential:
        build_params['image_credential_name'] = image_credential['name']
    update_build_config_with_method(config_obj, build_method=build_config.build_method, data=build_params)
    processes = [Process(name=proc_spec['name'], command=proc_spec['command'], args=proc_spec['args'], target_port=proc_spec.get('port', None), probes=proc_spec.get('probes', None), services=proc_spec.get('services', None)) for proc_spec in bkapp_spec['processes']]
    sync_processes(self.module, processes, manager=FieldMgrName.WEB_FORM)
    metrics = []
    for proc_spec in bkapp_spec['processes']:
        if env_overlay := proc_spec.get('env_overlay'):
            for (env_name, proc_env_overlay) in env_overlay.items():
                ProcessSpecEnvOverlay.objects.save_by_module(self.module, proc_spec['name'], env_name, **proc_env_overlay)
        if metric := get_items(proc_spec, ['monitoring', 'metric']):
            metrics.append({'process': proc_spec['name'], **metric})
    monitoring = Monitoring(metrics=metrics) if metrics else None
    ObservabilityConfig.objects.upsert_by_module(self.module, monitoring)
    if hook := bkapp_spec.get('hook'):
        self.module.deploy_hooks.enable_hook(type_=hook['type'], proc_command=hook.get('proc_command'), command=hook.get('command'), args=hook.get('args'))
```
</details>

---


### 模块: apiserver/paasng/paasng/utils/datetime.py


#### calculate_gap_seconds_interval

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 70-97 (共 28 行, 0 行注释)  

**函数签名**:
```python
def calculate_gap_seconds_interval ( gap_seconds, wide = False ) -> str :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def calculate_gap_seconds_interval(gap_seconds, wide=False) -> str:
    gap_minutes = abs(math.ceil(gap_seconds / 60))
    if not wide:
        interval_options = ['1s', '10s', '30s', '1m', '5m', '10m', '30m', '1h', '3h', '1d']
    else:
        interval_options = ['10s', '30s', '1m', '5m', '10m', '30m', '1h', '3h', '6h', '1d']
    if gap_minutes <= 1:
        index = 0
    elif gap_minutes <= 10:
        index = 1
    elif gap_minutes <= 30:
        index = 2
    elif gap_minutes <= 60:
        index = 3
    elif gap_minutes <= 360:
        index = 4
    elif gap_minutes <= 720:
        index = 5
    elif gap_minutes <= 1440:
        index = 6
    elif gap_minutes <= 4320:
        index = 7
    elif gap_minutes <= 10080:
        index = 8
    else:
        index = 9
    return interval_options[index]
```
</details>

---


### 模块: apiserver/paasng/paasng/utils/i18n/serializers.py


#### i18n

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 50-98 (共 49 行, 0 行注释)  
**描述**: `i18n` decorator will extend those fields wrapped by `I18NField` in the serializer.

**函数签名**:
```python
def i18n ( cls_or_languages: Optional[Union[Optional[List[str]], SerializerType]] = None ) -> Union[SerializerType, Callable[[SerializerType], SerializerType]] :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def i18n(cls_or_languages: Optional[Union[Optional[List[str]], SerializerType]] = None) -> Union[SerializerType, Callable[[SerializerType], SerializerType]]:
    """`i18n` decorator will extend those fields wrapped by `I18NField` in the serializer."""
    languages = [lang[0] for lang in settings.LANGUAGES]
    if isinstance(cls_or_languages, list):
        languages = cls_or_languages
    
    def decorator(cls: Type[serializers.Serializer]) -> Type[serializers.Serializer]:
        """Find all i18n fields, add with i18n suffix, finally extend modified fields to the `_declared_fields` attr.
        And The original field will be removed.
        """
        _declared_fields = getattr(cls, '_declared_fields')
        fields = {}
        for (attr, value) in cls.__dict__.items():
            if isinstance(value, I18NExtend):
                fields[attr] = value.field
        for (attr, field) in fields.items():
            delattr(cls, attr)
            for language_code in languages:
                i18n_field_name = to_translated_field(attr, language_code=language_code)
                _declared_fields[i18n_field_name] = copy.deepcopy(field)
        super_to_internal_value = getattr(cls, 'to_internal_value')
        
        def to_internal_value(self, data):
            with ExitStack() as stack:
                for raw_field_name in fields:
                    for language_code in languages:
                        i18n_field_name = to_translated_field(attr, language_code=language_code)
                        stack.enter_context(self.fields[i18n_field_name].override_field_name(raw_field_name))
                return super_to_internal_value(self, data)
        setattr(cls, 'to_internal_value', to_internal_value)
        return cls
    if cls_or_languages is None:
        return decorator
    elif isinstance(cls_or_languages, type) and issubclass(cls_or_languages, serializers.Serializer):
        return decorator(cls_or_languages)
    raise NotImplementedError
```
</details>

---


### 模块: apiserver/paasng/paasng/utils/models.py


#### _make_json_field

**复杂度分数**: 17  
**严重程度**: high_risk  
**行数**: 290-382 (共 93 行, 0 行注释)  
**描述**: 生成会自动进行类型转换为 `py_model` 的 `base_class`

**函数签名**:
```python
def _make_json_field ( base_class: Type[F], cls_name: str, py_model: Type[M], module: Optional[str] = None ) -> Type[F] :
```

**消息**: Complexity 17 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def _make_json_field(base_class: Type[F], cls_name: str, py_model: Type[M], module: Optional[str] = None) -> Type[F]:
    """生成会自动进行类型转换为 `py_model` 的 `base_class`

    :param base_class: 基础类型
    :param cls_name: 自动生成的 JSONField 的类名, 在使用时, cls_name 必须与赋值的变量名一致！否则 migrations 会报错.
    :param py_model: Python 模型, 需要能被 decoder 转换成可序列化成 json serializable object.
    :param module: Python 模块信息"""
    if not isinstance(py_model, type) and not (is_sequence(py_model) and not is_bare(py_model)) and not is_mapping(py_model):
        raise NotImplementedError(f'Unsupported type: {py_model}')
    
    def is_pymodel_instance(value):
        """should unstructured value to string?"""
        if is_sequence(py_model):
            elem_type = py_model.__args__[0]
            return all((isinstance(v, elem_type) for v in value))
        elif is_mapping(py_model):
            return isinstance(value, dict)
        else:
            return isinstance(value, py_model)
    
    def pre_init(self, value, obj):
        """Convert a dict/list to `py_model` object"""
        loaded_value = base_class.pre_init(self, value, obj)
        if loaded_value is None or is_pymodel_instance(value):
            return loaded_value
        return cattr.structure(loaded_value, py_model)
    
    def get_prep_value(self, value):
        """Convert `py_model` object to a string"""
        if hasattr(value, 'as_sql'):
            return value
        if value is not None and is_pymodel_instance(value):
            value = cattr.unstructure(value)
        return base_class.get_prep_value(self, value)
    
    def to_python(self, value):
        """The jsonfield.SubfieldBase metaclass calls pre_init instead of to_python, however to_python
        is still necessary for Django's deserializer"""
        loaded_value = base_class.to_python(self, value)
        if loaded_value is None:
            return loaded_value
        return cattr.structure(loaded_value, py_model)
    
    def from_db_value(self, value, expression, connection):
        """Convert string-like value to `py_model` object, calling by django"""
        loaded_value = base_class.from_db_value(self, value, expression, connection)
        if loaded_value is None:
            return loaded_value
        return cattr.structure(loaded_value, py_model)
    
    def value_to_string(self, obj):
        """Convert `py_model` object to a string, calling by django"""
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
    cls = type(cls_name, (base_class, ), dict(pre_init=pre_init, get_prep_value=get_prep_value, to_python=to_python, from_db_value=from_db_value, value_to_string=value_to_string))
    if module is None:
        module = __get_module_from_frame()
    if module is None:
        raise RuntimeError("Can't detect the module name. please provide by func args.")
    cls.__module__ = str(module)
    assert issubclass(cls, base_class)
    return cls
```
</details>

---


### 模块: apiserver/paasng/paasng/utils/patternmatcher.py


#### compile

**复杂度分数**: 16  
**严重程度**: high_risk  
**行数**: 66-133 (共 68 行, 0 行注释)  

**函数签名**:
```python
def compile ( self, sl: str ) :
```

**消息**: Complexity 16 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def compile(self, sl: str):
    reg_str = '^'
    pattern = self.cleaned_pattern
    esc_sl = sl
    if esc_sl == '\\':
        esc_sl += '\\'
    self.match_type = MatchType.Excat
    scan = Scanner(pattern)
    i = 0
    while not scan.is_eof():
        ch = scan.next()
        if ch == '*':
            if scan.peek() == '*':
                scan.next()
                if scan.peek() == sl:
                    scan.next()
                if scan.is_eof():
                    if self.match_type == MatchType.Excat:
                        self.match_type = MatchType.Prefix
                    else:
                        reg_str += '.*'
                        self.match_type = MatchType.Regexp
                else:
                    reg_str += '(.*' + esc_sl + ')?'
                    self.match_type = MatchType.Regexp
                if i == 0:
                    self.match_type = MatchType.Suffix
            else:
                reg_str += '[^' + esc_sl + ']*'
                self.match_type = MatchType.Regexp
        elif ch == '?':
            reg_str += '[^' + esc_sl + ']'
            self.match_type = MatchType.Regexp
        elif should_escape(ch):
            reg_str += '\\' + ch
        elif ch == '\\':
            if sl == '\\':
                reg_str += esc_sl
                i += 1
                continue
            if not scan.is_eof():
                reg_str += '\\' + scan.next()
                self.match_type = MatchType.Regexp
            else:
                reg_str += '\\'
        elif ch in ('[', ']'):
            reg_str += ch
            self.match_type = MatchType.Regexp
        else:
            reg_str += ch
        i += 1
    if self.match_type != MatchType.Regexp:
        return
    reg_str += '$'
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
    url = f'/api/bkapps/applications/{bk_cnative_app.code}/modules/{bk_module.name}/bkapp_model/process_specs/'
    resp = api_client.get(url)
    data = resp.json()
    metadata = data['metadata']
    proc_specs = data['proc_specs']
    assert metadata['allow_multiple_image'] is False
    assert len(proc_specs) == 2
    assert proc_specs[0]['name'] == 'web'
    assert proc_specs[0]['image'] == 'example.com/foo'
    assert proc_specs[0]['command'] == ['python']
    assert proc_specs[0]['args'] == ['-m', 'http.server']
    assert proc_specs[0]['env_overlay']['stag']['scaling_config'] == {'min_replicas': 1, 'max_replicas': 1, 'metrics': [{'type': 'Resource', 'metric': 'cpuUtilization', 'value': '85'}], 'policy': 'default'}
    assert proc_specs[0]['services'] is None
    assert proc_specs[1]['name'] == 'worker'
    assert proc_specs[1]['image'] == 'example.com/foo'
    assert proc_specs[1]['command'] == ['celery']
    assert proc_specs[1]['args'] == []
    assert proc_specs[1]['services'] is None
```
</details>

---


#### test_save

**复杂度分数**: 21  
**严重程度**: critical  
**行数**: 79-212 (共 134 行, 0 行注释)  

**函数签名**:
```python
def test_save ( self, api_client, bk_cnative_app, bk_module, web, celery_worker ) :
```

**消息**: Complexity 21 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def test_save(self, api_client, bk_cnative_app, bk_module, web, celery_worker):
    G(ProcessSpecEnvOverlay, proc_spec=web, environment_name='stag', autoscaling=True, scaling_config={'min_replicas': 1, 'max_replicas': 5, 'policy': 'default'})
    assert web.get_autoscaling('stag')
    url = f'/api/bkapps/applications/{bk_cnative_app.code}/modules/{bk_module.name}/bkapp_model/process_specs/'
    probes_cfg = {'liveness': {'exec': {'command': ['/bin/bash', '-c', 'echo hello']}, 'http_get': None, 'tcp_socket': None, 'initial_delay_seconds': 5, 'timeout_seconds': 5, 'period_seconds': 5, 'success_threshold': 1, 'failure_threshold': 3}, 'readiness': {'exec': None, 'tcp_socket': None, 'http_get': {'port': 8080, 'host': 'bk.example.com', 'path': '/healthz', 'http_headers': [{'name': 'XXX', 'value': 'YYY'}], 'scheme': 'HTTPS'}, 'initial_delay_seconds': 15, 'timeout_seconds': 60, 'period_seconds': 10, 'success_threshold': 1, 'failure_threshold': 5}, 'startup': {'exec': None, 'http_get': None, 'tcp_socket': {'port': 8080, 'host': 'bk.example.com'}, 'initial_delay_seconds': 5, 'timeout_seconds': 15, 'period_seconds': 2, 'success_threshold': 1, 'failure_threshold': 5}}
    request_data = [{'name': 'web', 'image': 'python:latest', 'command': ['python', '-m'], 'args': ['http.server'], 'port': 5000, 'env_overlay': {'stag': {'plan_name': 'default', 'target_replicas': 2, 'autoscaling': False}}, 'probes': probes_cfg}, {'name': 'beat', 'command': ['python', '-m'], 'args': ['celery', 'beat'], 'env_overlay': {'stag': {'plan_name': 'default', 'target_replicas': 1}, 'prod': {'plan_name': 'default', 'target_replicas': 1, 'autoscaling': True, 'scaling_config': {'min_replicas': 1, 'max_replicas': 5, 'metrics': [{'type': 'Resource', 'metric': 'cpuUtilization', 'value': '70'}]}}}, 'probes': {'liveness': None, 'readiness': None, 'startup': None}}]
    resp = api_client.post(url, data={'proc_specs': request_data})
    data = resp.json()
    proc_specs = data['proc_specs']
    assert ModuleProcessSpec.objects.filter(module=bk_module).count() == 2
    assert len(proc_specs) == 2
    assert proc_specs[0]['name'] == 'web'
    assert proc_specs[0]['image'] == 'example.com/foo'
    assert proc_specs[0]['command'] == ['python', '-m']
    assert proc_specs[0]['args'] == ['http.server']
    assert proc_specs[0]['port'] == 5000
    assert proc_specs[0]['env_overlay']['stag']['target_replicas'] == 2
    assert not proc_specs[0]['env_overlay']['stag']['autoscaling']
    assert proc_specs[0]['probes'] == probes_cfg
    assert proc_specs[1]['name'] == 'beat'
    assert proc_specs[1]['image'] == 'example.com/foo'
    assert proc_specs[1]['command'] == ['python', '-m']
    assert proc_specs[1]['args'] == ['celery', 'beat']
    assert proc_specs[1]['env_overlay']['prod']['scaling_config'] == {'min_replicas': 1, 'max_replicas': 5, 'metrics': [{'type': 'Resource', 'metric': 'cpuUtilization', 'value': '85'}], 'policy': 'default'}
    assert proc_specs[1]['probes'] == {'liveness': None, 'readiness': None, 'startup': None}
    spec_obj = ModuleProcessSpec.objects.get(module=bk_module, name='beat')
    assert spec_obj.get_scaling_config('prod') == AutoscalingConfig(min_replicas=1, max_replicas=5, policy='default')
    assert spec_obj.probes == {'liveness': None, 'readiness': None, 'startup': None}
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
    response = sys_api_client.post(f'/sys/api/plugins_center/bk_plugins/{bk_plugin_app.code}/configuration/', data=[{'key': 'FOO', 'value': 'foo'}, {'key': 'BAR', 'value': 'bar'}, {'key': 'BAZ', 'value': 'baz'}])
    assert response.status_code == 200
    assert ConfigVar.objects.filter(module=module).count() == 3
    assert ConfigVar.objects.get(module=module, key='FOO').value == 'foo'
    assert ConfigVar.objects.get(module=module, key='BAR').value == 'bar'
    assert ConfigVar.objects.get(module=module, key='BAZ').value == 'baz'
    response = sys_api_client.post(f'/sys/api/plugins_center/bk_plugins/{bk_plugin_app.code}/configuration/', data=[{'key': 'FOO', 'value': 'foo'}, {'key': 'BAR', 'value': 'BAR'}])
    assert response.status_code == 200
    assert ConfigVar.objects.filter(module=module).count() == 2
    assert ConfigVar.objects.get(module=module, key='FOO').value == 'foo'
    assert ConfigVar.objects.get(module=module, key='BAR').value == 'BAR'
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
    image_repository = 'strm/helloworld-http'
    response = api_client.post('/api/bkapps/cloud-native/', data={'region': settings.DEFAULT_REGION_NAME, 'code': f'uta-{random_suffix}', 'name': f'uta-{random_suffix}', 'bkapp_spec': {'build_config': {'build_method': 'custom_image', 'image_repository': image_repository, 'image_credential': {'name': image_credential_name, 'password': '123456', 'username': 'test'}}, 'processes': [{'name': 'web', 'command': ['bash', '/app/start_web.sh'], 'env_overlay': {'stag': {'environment_name': 'stag', 'target_replicas': 1, 'plan_name': '2C1G'}, 'prod': {'environment_name': 'prod', 'target_replicas': 2, 'plan_name': '2C1G'}}}]}, 'source_config': {'source_origin': SourceOrigin.CNATIVE_IMAGE, 'source_repo_url': image_repository}})
    assert response.status_code == 201, f"error: {response.json()['detail']}"
    app_data = response.json()['application']
    assert app_data['type'] == 'cloud_native'
    assert app_data['modules'][0]['web_config']['build_method'] == 'custom_image'
    assert app_data['modules'][0]['web_config']['artifact_type'] == 'none'
    module = Module.objects.get(id=app_data['modules'][0]['id'])
    cfg = BuildConfig.objects.get_or_create_by_module(module)
    assert cfg.image_repository == image_repository
    assert cfg.image_credential_name == image_credential_name
    process_spec = ModuleProcessSpec.objects.get(module=module, name='web')
    assert process_spec.command == ['bash', '/app/start_web.sh']
    assert process_spec.get_target_replicas('stag') == 1
    assert process_spec.get_target_replicas('prod') == 2
```
</details>

---


### 模块: apiserver/paasng/tests/api/test_configvar_by_key.py


#### test_configvar_by_key

**复杂度分数**: 12  
**严重程度**: warning  
**行数**: 32-92 (共 61 行, 0 行注释)  

**函数签名**:
```python
def test_configvar_by_key ( api_client, bk_module, init_env, init_value, update_env, update_value, expected_envs, expected_values ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

@pytest.mark.parametrize(('init_env', 'init_value', 'update_env', 'update_value', 'expected_envs', 'expected_values'), [(None, None, stag_env, 'v1', [stag_env], ['v1']), (stag_env, 'stag_v', prod_env, 'prod_v', [stag_env, prod_env], ['stag_v', 'prod_v']), (prod_env, 'old_prod', prod_env, 'new_prod', [prod_env], ['new_prod']), (global_env, 'global_v', prod_env, 'prod_v', [global_env, prod_env], ['global_v', 'prod_v'])])
def test_configvar_by_key(api_client, bk_module, init_env, init_value, update_env, update_value, expected_envs, expected_values):
    module = bk_module
    env_key = 'FOO'
    if init_env:
        if init_env == global_env:
            env_obj = -1
            ConfigVar.objects.create(module=module, key=env_key, environment_id=env_obj, value=init_value, description='desc', is_global=True)
        else:
            env_obj = ApplicationEnvironment.objects.get(module=module, environment=init_env)
            ConfigVar.objects.create(module=module, key=env_key, environment=env_obj, value=init_value, description='desc')
    path = f'/api/bkapps/applications/{bk_module.application.code}/modules/{bk_module.name}/config_vars/{env_key}/'
    resp = api_client.post(path, data={'environment_name': update_env, 'value': update_value, 'description': 'desc2'}, format='json')
    assert resp.status_code == 201
    resp = api_client.get(path)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == len(expected_envs)
    env_map = {d['environment_name']: d['value'] for d in data}
    for (env, val) in zip(expected_envs, expected_values):
        assert env_map[env] == val
    for item in data:
        if item['environment_name'] == global_env:
            assert item['is_global'] is True
        else:
            assert item['is_global'] is False
```
</details>

---


### 模块: apiserver/paasng/tests/api/test_market.py


#### test_update_market_app

**复杂度分数**: 14  
**严重程度**: warning  
**行数**: 113-164 (共 52 行, 0 行注释)  

**函数签名**:
```python
def test_update_market_app ( self, api_client, bk_app_full ) :
```

**消息**: Complexity 14 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def test_update_market_app(self, api_client, bk_app_full):
    if getattr(settings, 'BK_CONSOLE_DBCONF', None):
        from paasng.accessories.publish.sync_market.handlers import register_app_core_data
        register_app_core_data(sender=None, application=bk_app_full)
    Product.objects.create_default_product(bk_app_full)
    response = api_client.get(reverse('api.market.products.detail', args=(bk_app_full.code, )), format='json')
    data = response.json()
    target_name = uuid.uuid4().hex[:20]
    data['name'] = target_name
    data['width'] = 841
    data['contact'] = 'nobody;nobody1'
    data['open_mode'] = OpenMode.NEW_TAB.value
    data['visiable_labels'] = [{'id': 100, 'type': 'department', 'name': 'xx部门'}, {'id': 2001, 'type': 'user', 'name': 'user1'}]
    put_response = api_client.put(reverse('api.market.products.detail', args=(bk_app_full.code, )), data=data, format='json')
    assert put_response.status_code == 200
    product = Product.objects.get(code=bk_app_full.code)
    assert product.name == target_name
    assert product.displayoptions.width == 841
    assert product.displayoptions.contact == 'nobody;nobody1'
    assert product.displayoptions.open_mode == OpenMode.NEW_TAB.value
    if getattr(settings, 'BK_CONSOLE_DBCONF', None):
        from paasng.accessories.publish.sync_market.managers import AppManger
        from paasng.core.core.storages.sqlalchemy import console_db
        session = console_db.get_scoped_session()
        console_app = AppManger(session).get(bk_app_full.code)
        assert console_app.width == product.displayoptions.width == 841
        assert console_app.open_mode == product.displayoptions.open_mode
        try:
            assert json.loads(console_app.extra)['contact'] == product.displayoptions.contact
        except AttributeError:
            logger.info('The extra attribute of the application does not exist, skip verification')
        try:
            assert console_app.visiable_labels == product.transform_visiable_labels()
        except AttributeError:
            logger.info('The visiable_labels attribute of the application does not exist, skip verification')
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
    image_repository = 'strm/helloworld-http'
    response = api_client.post(f'/api/bkapps/cloud-native/{bk_cnative_app.code}/modules/', data={'name': f'uta-{random_suffix}', 'source_config': {'source_origin': SourceOrigin.CNATIVE_IMAGE, 'source_repo_url': 'strm/helloworld-http'}, 'bkapp_spec': {'build_config': {'build_method': 'custom_image', 'image_repository': image_repository}, 'processes': [{'name': 'web', 'command': ['bash', '/app/start_web.sh'], 'env_overlay': {'stag': {'environment_name': 'stag', 'target_replicas': 1, 'plan_name': '2C1G'}, 'prod': {'environment_name': 'prod', 'target_replicas': 2, 'plan_name': '2C1G'}}, 'port': 30000}], 'hook': {'type': 'pre-release-hook', 'enabled': True, 'command': ['/bin/bash'], 'args': ['-c', "echo 'hello world'"]}}})
    assert response.status_code == 201, f"error: {response.json()['detail']}"
    module_data = response.json()['module']
    assert module_data['web_config']['build_method'] == 'custom_image'
    assert module_data['web_config']['artifact_type'] == 'none'
    module = Module.objects.get(id=module_data['id'])
    cfg = BuildConfig.objects.get_or_create_by_module(module)
    assert cfg.image_repository == image_repository
    process_spec = ModuleProcessSpec.objects.get(module=module, name='web')
    assert process_spec.command == ['bash', '/app/start_web.sh']
    assert process_spec.port == 30000
    assert process_spec.get_target_replicas('stag') == 1
    assert process_spec.get_target_replicas('prod') == 2
    deploy_hook = ModuleDeployHook.objects.get(module=module, type=DeployHookType.PRE_RELEASE_HOOK)
    assert deploy_hook.command == ['/bin/bash']
    assert deploy_hook.args == ['-c', "echo 'hello world'"]
```
</details>

---


### 模块: apiserver/paasng/tests/paas_wl/bk_app/deploy/app_res/test_controllers.py


#### test_deploy_processes

**复杂度分数**: 11  
**严重程度**: warning  
**行数**: 142-170 (共 29 行, 0 行注释)  

**函数签名**:
```python
def test_deploy_processes ( self, wl_app, web_process ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

@pytest.mark.mock_get_structured_app()
def test_deploy_processes(self, wl_app, web_process):
    handler = ProcessesHandler.new_by_app(wl_app)
    with patch('paas_wl.infras.resources.base.kres.NameBasedOperations.replace_or_patch') as kd, patch('paas_wl.workloads.networking.ingress.managers.service.service_kmodel') as ks, patch('paas_wl.workloads.networking.ingress.managers.base.ingress_kmodel') as ki:
        ks.get.side_effect = AppEntityNotFound()
        ki.get.side_effect = AppEntityNotFound()
        handler.deploy([web_process])
        assert kd.called
        (deployment_args, deployment_kwargs) = kd.call_args_list[0]
        assert deployment_kwargs.get('name') == f'{region}-{wl_app.name}-web-python-deployment'
        assert deployment_kwargs.get('body')
        assert deployment_kwargs.get('namespace') == wl_app.namespace
        assert ks.get.called
        assert ks.create.called
        proc_service = ks.create.call_args_list[0][0][0]
        assert proc_service.name == f'{region}-{wl_app.name}-web'
        assert ks.get.called
        assert ki.save.called
        proc_ingress = ki.save.call_args_list[0][0][0]
        assert proc_ingress.name == f'{region}-{wl_app.name}'
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

@pytest.mark.usefixtures('_do_deploy')
def test_deploy_success(self, controller, bk_app, module_name, user_dev_wl_app):
    sandbox_entity_in_cluster = controller.sandbox_mgr.get(user_dev_wl_app, user_dev_wl_app.scheduler_safe_name)
    assert sandbox_entity_in_cluster.runtime.envs == {'FOO': 'test', 'SOURCE_FETCH_METHOD': 'BK_REPO', 'SOURCE_FETCH_URL': 'example.com', 'WORKSPACE': '/cnb/devsandbox/src'}
    assert sandbox_entity_in_cluster.status.replicas == 1
    assert sandbox_entity_in_cluster.status.ready_replicas in [0, 1]
    assert sandbox_entity_in_cluster.status.to_health_phase() in ['Progressing', 'Healthy']
    code_editor_entity_in_cluster = controller.code_editor_mgr.get(user_dev_wl_app, get_code_editor_name(user_dev_wl_app))
    assert code_editor_entity_in_cluster.runtime.envs == {'PASSWORD': '123456', 'START_DIR': '/home/coder/project'}
    assert code_editor_entity_in_cluster.status.replicas == 1
    assert code_editor_entity_in_cluster.status.ready_replicas in [0, 1]
    assert code_editor_entity_in_cluster.status.to_health_phase() in ['Progressing', 'Healthy']
    service_entity_in_cluster = controller.dev_sandbox_svc_mgr.get(user_dev_wl_app, get_dev_sandbox_service_name(user_dev_wl_app))
    assert service_entity_in_cluster.name == get_dev_sandbox_service_name(user_dev_wl_app)
    ingress_entity_in_cluster = controller.ingress_mgr.get(user_dev_wl_app, get_ingress_name(user_dev_wl_app))
    assert ingress_entity_in_cluster.name == get_ingress_name(user_dev_wl_app)
    assert ingress_entity_in_cluster.domains[0].host == get_sub_domain_host(bk_app.code, user_dev_wl_app, module_name)
```
</details>

---


### 模块: apiserver/paasng/tests/paas_wl/bk_app/processes/test_models.py


#### test_switch

**复杂度分数**: 16  
**严重程度**: high_risk  
**行数**: 57-102 (共 46 行, 0 行注释)  

**函数签名**:
```python
def test_switch ( self, wl_app ) :
```

**消息**: Complexity 16 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def test_switch(self, wl_app):
    mgr = ProcessSpecManager(wl_app)
    mgr.sync([ProcessTmpl(name='web', command='foo', replicas=2), ProcessTmpl(name='celery', command='foo')])
    web = ProcessSpec.objects.get(engine_app=wl_app, name='web')
    assert web.target_replicas == 2
    assert not web.autoscaling
    assert web.scaling_config is None
    mgr.sync([ProcessTmpl(name='web', command='foo', replicas=2, autoscaling=True, scaling_config=AutoscalingConfig(min_replicas=1, max_replicas=3, policy='default')), ProcessTmpl(name='celery', command='foo')])
    web.refresh_from_db()
    assert web.target_replicas == 2
    assert web.autoscaling
    assert web.scaling_config is not None
    assert web.scaling_config.min_replicas == 1
    assert web.scaling_config.max_replicas == 3
    assert web.scaling_config.policy == 'default'
    mgr.sync([ProcessTmpl(name='web', command='foo', replicas=2, autoscaling=False), ProcessTmpl(name='celery', command='foo')])
    web.refresh_from_db()
    assert web.target_replicas == 2
    assert not web.autoscaling
    assert web.scaling_config is not None
    assert web.scaling_config.min_replicas == 1
    assert web.scaling_config.max_replicas == 3
    assert web.scaling_config.policy == 'default'
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
    mgr.sync([ProcessTmpl(name='web', command='/bin/start.sh', probes=ProbeSet(liveness=Probe(exec=ExecAction(command=['/bin/healthz.sh'])), readiness=Probe(tcp_socket=TCPSocketAction(port=8080, host='127.0.0.1')))), ProcessTmpl(name='celery', command='/bin/start_celery.sh', probes=ProbeSet(startup=Probe(http_get=HTTPGetAction(port=8080, path='/healthz', host='127.0.0.1'))))])
    probes = ProcessProbe.objects.filter(app=wl_app)
    assert probes.count() == 3
    assert probes.filter(process_type='web').count() == 2
    assert probes.filter(process_type='celery').count() == 1
    mgr.sync([ProcessTmpl(name='web', command='foo', probes=ProbeSet(liveness=Probe(http_get=HTTPGetAction(port=8080, path='/healthz')), readiness=Probe(tcp_socket=TCPSocketAction(port=8080)), startup=Probe(exec=ExecAction(command=['/bin/healthz.sh']))))])
    probes = ProcessProbe.objects.filter(app=wl_app, process_type='web')
    assert probes.count() == 3
    probe = probes.filter(probe_type=ProbeType.LIVENESS).first()
    assert probe is not None
    assert probe.success_threshold == 1
    assert probe.failure_threshold == 3
    assert probe.probe_handler.http_get.port == 8080
    assert probe.probe_handler.http_get.path == '/healthz'
    mgr.sync([ProcessTmpl(name='web', command='foo', probes=None)])
    assert not ProcessProbe.objects.filter(app=wl_app).exists()
```
</details>

---


### 模块: apiserver/paasng/tests/paas_wl/bk_app/processes/test_processes.py


#### testlist_gen_cnative_process_specs

**复杂度分数**: 20  
**严重程度**: high_risk  
**行数**: 35-84 (共 50 行, 0 行注释)  

**函数签名**:
```python
def testlist_gen_cnative_process_specs (  ) :
```

**消息**: Complexity 20 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def testlist_gen_cnative_process_specs():
    specs = gen_cnative_process_specs(BkAppResource(metadata={'name': 'test'}, spec={'processes': [{'name': 'web', 'resQuotaPlan': '4C2G'}, {'name': 'worker', 'resQuotaPlan': 'default', 'autoscaling': {'minReplicas': 1, 'maxReplicas': 3, 'policy': 'default'}}], 'envOverlay': {'replicas': [{'process': 'worker', 'count': 0, 'envName': 'stag'}], 'autoscaling': [{'process': 'worker', 'minReplicas': 3, 'maxReplicas': 5, 'envName': 'stag', 'policy': 'default'}]}}), 'stag')
    assert specs[0].name == 'web'
    assert specs[0].plan_name == '4C2G'
    assert specs[0].target_replicas == 1
    assert specs[0].autoscaling is False
    assert specs[0].scaling_config is None
    assert specs[0].resource_limit == {'cpu': '4000m', 'memory': '2048Mi'}
    assert specs[0].resource_limit_quota == {'cpu': 4000, 'memory': 2048}
    assert specs[0].resource_requests == {'cpu': '200m', 'memory': '1024Mi'}
    assert specs[0].target_status == 'start'
    assert specs[1].name == 'worker'
    assert specs[1].plan_name == 'default'
    assert specs[1].target_replicas == 0
    assert specs[1].autoscaling is True
    assert specs[1].scaling_config['min_replicas'] == 3
    assert specs[1].scaling_config['max_replicas'] == 5
    assert specs[1].resource_limit == {'cpu': '4000m', 'memory': '1024Mi'}
    assert specs[1].resource_limit_quota == {'cpu': 4000, 'memory': 1024}
    assert specs[1].resource_requests == {'cpu': '200m', 'memory': '256Mi'}
    assert specs[1].target_status == 'stop'
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

@pytest.mark.usefixtures('_cluster_envs')
@pytest.mark.parametrize(('https_enabled', 'expect'), [('true', True), ('false', False)])
def test_init_cluster(https_enabled, expect):
    os.environ['PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT'] = https_enabled
    call_command('initial_default_cluster')
    cluster = Cluster.objects.get(name='default-main')
    ingress_config = cluster.ingress_config
    assert ingress_config.app_root_domains[0].https_enabled is expect
    assert ingress_config.sub_path_domains[0].https_enabled is expect
    assert ingress_config.app_root_domains[0].name == 'apps1.example.com'
    assert ingress_config.sub_path_domains[0].name == 'apps2.example.com'
    assert ingress_config.port_map.http == 880
    assert ingress_config.port_map.https == 8443
    assert cluster.default_tolerations == [{'effect': 'NoSchedule', 'key': 'dedicated', 'operator': 'Equal', 'value': 'bkSaas'}]
    assert cluster.default_node_selector == {'dedicated': 'bkSaas'}
    urls = APIServer.objects.filter(cluster=cluster).values_list('host', flat=True)
    assert set(urls) == {'https://kubernetes.default.svc.cluster.localroot', 'https://10.0.0.1'}
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
    ingress_config = {'app_root_domains': ['foo.com', {'name': 'bar.com'}, {'name': 'baz.com', 'reserved': True}]}
    c: Cluster = Cluster.objects.create(region=region, name='dft', is_default=True, ingress_config=ingress_config)
    c.refresh_from_db()
    assert isinstance(c.ingress_config, IngressConfig)
    assert len(c.ingress_config.app_root_domains) == 3
    assert all((isinstance(domain, Domain) for domain in c.ingress_config.app_root_domains))
    assert c.ingress_config.app_root_domains[0].name == 'foo.com'
    assert c.ingress_config.app_root_domains[0].reserved is False
    assert c.ingress_config.app_root_domains[1].name == 'bar.com'
    assert c.ingress_config.app_root_domains[1].reserved is False
    assert c.ingress_config.app_root_domains[2].name == 'baz.com'
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
    assert volume.name == 'secret'
    assert volume.secret
    assert volume.secret.secretName == 'the-secret'
    assert len(volume.secret.items) == 1
    assert volume.secret.items[0].key == 'a'
    assert volume.secret.items[0].path == 'secret/a'
    assert volume.secret.items[0].mode == 420
```
</details>

---


### 模块: apiserver/paasng/tests/paasng/accessories/servicehub/remote/test_manager.py


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

@pytest.mark.parametrize(('specs', 'ok'), [({}, True), ({'version': 'sth-wrong'}, False), ({'version': '1'}, True)])
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
                for (k, v) in specs.items():
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

@mock.patch('paasng.accessories.servicehub.services.get_application_cluster')
@pytest.mark.parametrize(('cluster_name', 'zone_name', 'plans', 'expected_zone_name', 'ok'), [(None, None, [gen_plan('r1', dict(app_zone='universal'), {})], 'universal', True), ('A', 'universal', [gen_plan('r1', dict(app_zone='universal'), {})], 'universal', True), ('A', 'ZA', [gen_plan('r1', dict(app_zone='ZA'), {})], 'ZA', True), ('A', 'ZA', [gen_plan('r1', dict(app_zone='ZB'), {}), gen_plan('r1', dict(app_zone='ZA'), {})], 'ZA', True), (None, None, [gen_plan('r1', dict(app_zone='sth-wrong'), {})], 'universal', False), ('A', 'universal', [gen_plan('r1', dict(app_zone='ZA'), {})], 'ZA', False), ('A', 'ZA', [gen_plan('r1', dict(app_zone='universal'), {})], 'universal', False), ('A', 'ZA', [gen_plan('r1', dict(app_zone='ZB'), {})], 'ZB', False)])
def test_bound_with_diff_app_zone(self, g_cluster, store, bk_module, bk_service_ver_zone, cluster_name, zone_name, plans, expected_zone_name, ok):
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
        with mock.patch.object(store, 'get') as get_svc:
            get_svc.return_value = asdict(bk_service_ver_zone)
            for env in bk_module.envs.all():
                for rel in mgr.list_unprovisioned_rels(env.engine_app, bk_service_ver_zone):
                    plan = rel.get_plan()
                    assert len(plan.specifications) > 0
                    assert plan.specifications['app_zone'] == expected_zone_name
```
</details>

---


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

@mock.patch('paas_wl.workloads.networking.egress.shim.get_cluster_egress_info')
@mock.patch('paasng.accessories.servicehub.remote.client.RemoteServiceClient.provision_instance')
@pytest.mark.parametrize('plans', [[gen_plan('r1', {'app_zone': 'universal'}, {})], [gen_plan('r1', {'app_zone': 'universal'}, {'restricted_envs': ['stag']}), gen_plan('r1', {'app_zone': 'universal'}, {'restricted_envs': ['prod']})]])
def test_provision(self, mocked_provision, get_cluster_egress_info, store, bk_module, bk_service_ver, plans):
    """Test service instance provision"""
    get_cluster_egress_info.return_value = {'egress_ips': ['1.1.1.1'], 'digest_version': 'foo'}
    mgr = RemoteServiceMgr(store=store)
    bk_service_ver.plans = plans
    mgr.bind_service(bk_service_ver, bk_module)
    with mock.patch.object(mgr, 'get') as get_service:
        get_service.return_value = bk_service_ver
        for env in bk_module.envs.all():
            expected_plan = plans[1] if env.environment == 'prod' and len(plans) == 2 else plans[0]
            for rel in mgr.list_unprovisioned_rels(env.engine_app):
                assert rel.is_provisioned() is False
                rel.provision()
                assert rel.is_provisioned() is True
                assert str(rel.db_obj.service_id) == bk_service_ver.uuid
                assert str(rel.db_obj.plan_id) == expected_plan.uuid
                assert mocked_provision.called
                assert len(mocked_provision.call_args[0]) == 3
                assert bool(all(mocked_provision.call_args[0]))
                assert mocked_provision.call_args[1]['params']['username'] == rel.db_engine_app.name
```
</details>

---


### 模块: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/release/test_executor.py


#### test_execute_current_stage

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 154-177 (共 24 行, 0 行注释)  

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
    assert release.current_stage.stage_id == 'stage1'
    executor.execute_current_stage('')
    assert release.current_stage.stage_id == 'stage1'
    assert release.current_stage.status == PluginReleaseStatus.PENDING
    with pytest.raises(APIError) as exc:
        executor.execute_current_stage('')
    assert exc.value.code == error_codes.EXECUTE_STAGE_ERROR.code
    assert exc.value.message == error_codes.EXECUTE_STAGE_ERROR.f(_('当前阶段已被执行, 不能重复触发已执行的阶段')).message
    release.current_stage.reset()
    stage_class_setter.return_value = build_stage_controller(PluginReleaseStatus.SUCCESSFUL)
    assert release.current_stage.stage_id == 'stage1'
    executor.execute_current_stage('')
    assert release.current_stage.stage_id == 'stage1'
    assert release.current_stage.status == PluginReleaseStatus.SUCCESSFUL
```
</details>

---


### 模块: apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/test_integration.py


#### test_release_version

**复杂度分数**: 18  
**严重程度**: high_risk  
**行数**: 182-312 (共 131 行, 0 行注释)  

**函数签名**:
```python
def test_release_version ( self, thirdparty_client, pd, plugin, api_client, iam_policy_client ) :
```

**消息**: Complexity 18 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

@pytest.mark.usefixtures('_setup_release_stages', '_setup_bk_user')
def test_release_version(self, thirdparty_client, pd, plugin, api_client, iam_policy_client):
    assert PluginRelease.objects.filter(plugin=plugin, type='prod', status__in=PluginReleaseStatus.running_status()).count() == 0
    with mock.patch('paasng.bk_plugins.pluginscenter.shim.get_plugin_repo_accessor') as get_plugin_repo_accessor:
        get_plugin_repo_accessor().extract_smart_revision.return_value = 'hash'
        resp = api_client.post(f'/api/bkplugins/{pd.identifier}/plugins/{plugin.id}/releases/', data={'type': 'prod', 'source_version_type': 'branch', 'source_version_name': 'foo', 'version': '0.0.1', 'comment': '...', 'semver_type': 'patch'})
        assert resp.status_code == 201
    release = PluginRelease.objects.get(plugin=plugin)
    assert release.current_stage.stage_id == 'market'
    assert release.current_stage.status == PluginReleaseStatus.PENDING
    resp = api_client.post(f'/api/bkplugins/{pd.identifier}/plugins/{plugin.id}/releases/{release.id}/next/')
    assert resp.status_code == 400
    assert resp.json() == {'code': error_codes.EXECUTE_STAGE_ERROR.code, 'detail': error_codes.EXECUTE_STAGE_ERROR.f(_('当前阶段未执行成功, 不允许进入下一阶段')).message}
    resp = api_client.post(f'/api/bkplugins/{pd.identifier}/plugins/{plugin.id}/market/', data={'category': '...', 'introduction': '...', 'description': '...', 'contact': '...'})
    assert resp.status_code == 200
    release.refresh_from_db()
    assert release.current_stage.status == PluginReleaseStatus.SUCCESSFUL
    counter = 0
    
    def deploy_action_side_effect(*args, **kwargs):
        nonlocal counter
        counter += 1
        if counter == 1:
            return {'deploy_id': '...', 'status': 'pending', 'detail': '', 'steps': [{'id': 'step-1', 'name': '步骤1', 'status': 'pending'}]}
        elif counter == 2:
            return {'deploy_id': '...', 'status': 'successful', 'detail': '', 'steps': [{'id': 'step-1', 'name': '步骤1', 'status': 'successful'}]}
        else:
            return {'logs': ['1', '2', '3'], 'finished': True}
    thirdparty_client.call.side_effect = deploy_action_side_effect
    resp = api_client.post(f'/api/bkplugins/{pd.identifier}/plugins/{plugin.id}/releases/{release.id}/next/')
    assert resp.status_code == 200
    release.refresh_from_db()
    release.current_stage.refresh_from_db()
    assert release.current_stage.stage_id == 'deploy'
    assert release.current_stage.api_detail == {'deploy_id': '...', 'status': 'pending', 'detail': '', 'steps': [{'id': 'step-1', 'name': '步骤1', 'status': 'pending'}]}
    resp = api_client.get(f'/api/bkplugins/{pd.identifier}/plugins/{plugin.id}/releases/{release.id}/stages/{release.current_stage.stage_id}/')
    assert resp.json() == {'stage_id': 'deploy', 'stage_name': '部署', 'status': 'pending', 'fail_message': '', 'invoke_method': 'deployAPI', 'status_polling_method': 'api', 'detail': {'steps': [{'id': 'step-1', 'name': '步骤1', 'status': 'successful'}], 'finished': True, 'logs': ['1', '2', '3']}}
    release.refresh_from_db()
    assert release.current_stage.status == PluginReleaseStatus.SUCCESSFUL
    assert release.status == PluginReleaseStatus.SUCCESSFUL
    release.current_stage.status = PluginReleaseStatus.FAILED
    release.current_stage.operator = 'xxxxxx'
    release.current_stage.save(update_fields=['status', 'operator'])
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
    scope = Scope.parse_from_str('group:v3-test-group')
    assert scope.type == ScopeType.GROUP
    assert scope.item == 'v3-test-group'
    scope = Scope.parse_from_str('project:admin/Skynet')
    assert scope.type == ScopeType.PROJECT
    assert scope.item == 'admin/Skynet'
    scope = Scope.parse_from_str('project:admin_yu/Sky-net')
    assert scope.type == ScopeType.PROJECT
    assert scope.item == 'admin_yu/Sky-net'
    scope = Scope.parse_from_str('user:user')
    assert scope.type == ScopeType.USER
    assert scope.item == 'user'
    scope = Scope.parse_from_str('api')
    assert scope.type == ScopeType.USER
    assert scope.item == 'user'
    scope = Scope.parse_from_str('')
    assert scope.type == ScopeType.USER
    assert scope.item == 'user'
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
    r1 = pr.get_raw_by_container_name('ieod-bkapp-career-stag')
    assert r1
    assert len(r1['values']) == 4
    r2 = pr.get_raw_by_container_name('cl5')
    assert r2
    assert len(r2['values']) == 3
    assert r1['metric'] == {'container_name': 'ieod-bkapp-career-stag'}
    assert r1['values'] == [[1590000844, '0.0003452615666667214'], [1590001444, '0.00040326460000083365'], [1590002044, '0.0003675630666667947'], [1590003044, '0.0003675630666667947']]
    r3 = pr.get_raw_by_container_name('cxxxx')
    assert r3 is None
    r4 = pr.get_raw_by_container_name()
    assert r4
    assert len(r4['values']) == 3
```
</details>

---


#### test_get_by_container_name

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 198-224 (共 27 行, 0 行注释)  
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
    r1 = pr.get_raw_by_container_name('celery-proc')
    assert r1
    assert len(r1['values']) == 4
    r2 = pr.get_raw_by_container_name('web-proc')
    assert r2
    assert len(r2['values']) == 3
    assert r1['metric'] == {'container_name': 'celery-proc'}
    assert r1['values'] == [[1673257280, '1073741824'], [1673257290, '1073741824'], [1673257300, '1073741824'], [1673257310, '1073741824']]
    r3 = pr.get_raw_by_container_name('xxx')
    assert r3 is None
    r4 = pr.get_raw_by_container_name()
    assert r4
    assert len(r4['values']) == 3
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

@pytest.mark.parametrize(('is_lapp', 'data', 'expected'), [(False, {}, {'bk_error_msg': '{code} not found', 'bk_error_code': '1301100', 'result': False, 'data': ''}), (True, {'app_name': 'Bar', 'introduction': 'introduction', 'developers': ['admin', 'blueking']}, {'bk_error_msg': '', 'bk_error_code': '0', 'result': True, 'data': {'light_app_code': '{light_app_code}', 'app_name': '{app_name}', 'introduction': 'introduction', 'developers': ['admin', 'blueking']}}), (True, {'app_name': 'Bar', 'introduction': 'introduction', 'developers': ['admin', 'blueking'], 'app_tag': ''}, {'bk_error_msg': '', 'bk_error_code': '0', 'result': True, 'data': {'light_app_code': '{light_app_code}', 'app_name': '{app_name}', 'introduction': 'introduction', 'developers': ['admin', 'blueking']}})])
def test_edit(self, legacy_tag, legacy_app, sys_light_api_client, is_lapp, data, expected):
    with legacy_db.session_scope() as session:
        AppAdaptor(session).update(code=legacy_app.code, data={'is_lapp': is_lapp})
    data = {'light_app_code': legacy_app.code, **data}
    if 'app_tag' in data:
        data['app_tag'] = legacy_tag.code
    response = sys_light_api_client.patch('/sys/api/light-applications/', data=data)
    assert response.status_code == 200
    result = response.json()
    result_data = result.pop('data')
    expected_data = expected.pop('data')
    assert result.pop('bk_error_msg') == expected.pop('bk_error_msg').format(code=legacy_app.code)
    if expected['result']:
        for (k, v) in expected_data.items():
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
**行数**: 69-98 (共 30 行, 0 行注释)  

**函数签名**:
```python
def test_integrated ( self, bk_module, proc_web, proc_celery ) :
```

**消息**: Complexity 11 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def test_integrated(self, bk_module, proc_web, proc_celery):
    ret = sync_env_overlays_replicas(bk_module, [ReplicasOverlay(env_name='prod', process='web', count=2), ReplicasOverlay(env_name='prod', process='worker', count=2)], manager=fieldmgr.FieldMgrName.APP_DESC)
    assert ret.updated_num == 1
    assert ret.created_num == 1
    assert ret.deleted_num == 1
    assert get_overlay_obj(proc_web, 'prod').target_replicas == 2
    assert get_overlay_obj(proc_celery, 'prod').target_replicas == 2
    assert get_overlay_obj(proc_web, 'stag').target_replicas is None
    fieldmgr.FieldManager(bk_module, fieldmgr.f_overlay_replicas(proc_web.name, 'prod')).set(fieldmgr.FieldMgrName.WEB_FORM)
    sync_env_overlays_replicas(bk_module, NOTSET, manager=fieldmgr.FieldMgrName.APP_DESC)
    assert get_overlay_obj(proc_web, 'prod').target_replicas == 2
    assert get_overlay_obj(proc_celery, 'prod').target_replicas is None
    assert get_overlay_obj(proc_web, 'stag').target_replicas is None
    sync_env_overlays_replicas(bk_module, [], manager=fieldmgr.FieldMgrName.APP_DESC)
    assert get_overlay_obj(proc_web, 'prod').target_replicas is None
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
    ret = sync_env_overlays_autoscalings(bk_module, [AutoscalingOverlay(env_name='prod', process='web', min_replicas=1, max_replicas=2, policy='default'), AutoscalingOverlay(env_name='prod', process='worker', min_replicas=2, max_replicas=5, policy='default')], manager=fieldmgr.FieldMgrName.APP_DESC)
    assert ret.updated_num == 1
    assert ret.created_num == 1
    assert ret.deleted_num == 1
    assert get_overlay_obj(proc_web, 'prod').autoscaling
    assert get_overlay_obj(proc_web, 'prod').scaling_config == AutoscalingConfig(min_replicas=1, max_replicas=2, policy='default')
    assert get_overlay_obj(proc_celery, 'prod').autoscaling
    assert get_overlay_obj(proc_celery, 'prod').scaling_config == AutoscalingConfig(min_replicas=2, max_replicas=5, policy='default')
    assert get_overlay_obj(proc_web, 'stag').autoscaling is None
    assert get_overlay_obj(proc_web, 'stag').scaling_config is None
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
    ret = sync_processes(bk_module, [Process(name=proc_web.name, replicas=1, command=['./start.sh'], res_quota_plan='4C1G', target_port=30000, probes=ProbeSet(liveness=Probe(http_get=HTTPGetAction(port='${PORT}', path='/healthz'), initial_delay_seconds=30, timeout_seconds=5, period_seconds=5, success_threshold=1, failure_threshold=3), readiness=Probe(tcp_socket=TCPSocketAction(port=30000))), services=[ProcService(name='web', target_port=30000, exposed_type={'name': 'bk/http'})]), Process(name='sleep', replicas=1, command=['bash'], res_quota_plan='4C2G', args=['-c', '100'], proc_command='sleep 100', autoscaling=AutoscalingConfig(min_replicas=2, max_replicas=10, policy='default'))], FieldMgrName.APP_DESC)
    assert ret.updated_num == 1
    assert ret.created_num == 1
    assert ret.deleted_num == 1
    assert ModuleProcessSpec.objects.filter(module=bk_module).count() == 2
    specs = ModuleProcessSpec.objects.filter(module=bk_module, name=proc_web.name)
    assert specs.count() == 1
    spec = specs.first()
    assert spec.port == 30000
    assert spec.probes.liveness.http_get.port == '${PORT}'
    assert spec.probes.liveness.initial_delay_seconds == 30
    assert spec.probes.liveness.period_seconds == 5
    assert spec.probes.readiness.tcp_socket.port == 30000
    assert spec.plan_name == '4C1G'
    assert spec.services[0].exposed_type.name == 'bk/http'
    spec = ModuleProcessSpec.objects.get(module=bk_module, name='sleep')
    assert spec.proc_command == 'sleep 100'
    assert spec.command is None
    assert spec.target_replicas == 1
    assert spec.scaling_config.max_replicas == 10
    assert spec.scaling_config.min_replicas == 2
    assert spec.plan_name == '4C2G'
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
    cache_path = f'{wl_app.region}/home/{wl_app.name}/cache'
    assert env_vars.pop('TAR_PATH') == f'{bucket}/{build_proc.source_tar_path}', 'TAR_PATH 与预期不符'
    assert env_vars.pop('PUT_PATH') == f'{bucket}/{generate_slug_path(build_proc)}', 'PUT_PATH 与预期不符'
    assert env_vars.pop('CACHE_PATH') == f'{bucket}/{cache_path}', 'CACHE_PATH 与预期不符'
    if settings.BUILD_EXTRA_ENV_VARS:
        for (k, v) in settings.BUILD_EXTRA_ENV_VARS.items():
            assert env_vars.pop(k) == v, f'{k} 与预期不符'
    if settings.PYTHON_BUILDPACK_PIP_INDEX_URL:
        for (k, v) in get_envs_from_pypi_url(settings.PYTHON_BUILDPACK_PIP_INDEX_URL).items():
            assert env_vars.pop(k) == v, f'{k} 与预期不符'
```
</details>

---


### 模块: apiserver/paasng/tests/paasng/platform/engine/deploy/test_building.py


#### test_start_build

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 157-198 (共 42 行, 0 行注释)  

**函数签名**:
```python
def test_start_build ( self, builder_class, bk_cnative_app, bk_module_full, bk_deployment_full, model_resource ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def test_start_build(self, builder_class, bk_cnative_app, bk_module_full, bk_deployment_full, model_resource):
    desc_handler = get_deploy_desc_handler(None, {'web': 'gunicorn'})
    with mock.patch('paasng.platform.engine.deploy.building.get_deploy_desc_handler_by_version', return_value=desc_handler), mock.patch('paasng.platform.engine.deploy.building.{}.compress_and_upload'.format(builder_class.__name__)), mock.patch('paasng.platform.engine.deploy.building.BuildProcessPoller') as mocked_poller, mock.patch('paasng.platform.engine.utils.output.RedisChannelStream') as mocked_stream, mock.patch('paasng.platform.engine.deploy.building.{}.launch_build_processes'.format(builder_class.__name__)) as launch_build_processes:
        faked_build_process_id = uuid.uuid4().hex
        launch_build_processes.return_value = faked_build_process_id
        attach_all_phases(sender=bk_deployment_full.app_environment, deployment=bk_deployment_full)
        builder = builder_class.from_deployment_id(bk_deployment_full.id)
        builder.start()
        deployment = Deployment.objects.get(pk=bk_deployment_full.id)
        assert deployment.status == JobStatus.PENDING.value
        assert deployment.build_process_id.hex == faked_build_process_id
        assert deployment.err_detail is None
        assert launch_build_processes.called
        (source_tar_path, bkapp_revision_id) = launch_build_processes.call_args[0]
        assert source_tar_path != ''
        assert bkapp_revision_id is not None
        assert mocked_stream().write_title.called
        assert mocked_poller.start.called
        assert mocked_poller.start.call_args[0][0] == {'build_process_id': deployment.build_process_id.hex, 'deployment_id': deployment.id}
```
</details>

---


#### test_start_normal

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 98-138 (共 41 行, 0 行注释)  

**函数签名**:
```python
def test_start_normal ( self, builder_class, bk_deployment_full ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def test_start_normal(self, builder_class, bk_deployment_full):
    with mock.patch('paasng.platform.engine.configurations.source_file.MetaDataFileReader.get_procfile') as mocked_get_procfile, mock.patch('paasng.platform.engine.deploy.building.{}.compress_and_upload'.format(builder_class.__name__)), mock.patch('paasng.platform.engine.deploy.building.BuildProcessPoller') as mocked_poller, mock.patch('paasng.platform.engine.utils.output.RedisChannelStream') as mocked_stream, mock.patch('paasng.platform.engine.deploy.building.{}.launch_build_processes'.format(builder_class.__name__)) as launch_build_processes:
        mocked_get_procfile.return_value = {'web': 'gunicorn'}
        faked_build_process_id = uuid.uuid4().hex
        launch_build_processes.return_value = faked_build_process_id
        attach_all_phases(sender=bk_deployment_full.app_environment, deployment=bk_deployment_full)
        builder = builder_class.from_deployment_id(bk_deployment_full.id)
        builder.start()
        deployment = Deployment.objects.get(pk=bk_deployment_full.id)
        assert deployment.status == JobStatus.PENDING.value
        assert deployment.build_process_id.hex == faked_build_process_id
        assert deployment.err_detail is None
        assert launch_build_processes.called
        (source_tar_path, bkapp_revision_id) = launch_build_processes.call_args[0]
        assert source_tar_path != ''
        assert bkapp_revision_id is None
        assert mocked_stream().write_title.called
        assert mocked_poller.start.called
        assert mocked_poller.start.call_args[0][0] == {'build_process_id': deployment.build_process_id.hex, 'deployment_id': deployment.id}
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

def test_migrate_and_rollback(self, bk_app, bk_module, image_repository_module, migration_process, cnb_builder, cnb_runner, buildpack, slugbuilder, slugrunner):
    BuildConfigMigrator(migration_process).migrate()
    config = BuildConfig.objects.get(module=bk_module)
    assert config.buildpacks.filter(id=buildpack.id).exists()
    assert config.buildpack_builder == cnb_builder
    assert config.buildpack_runner == cnb_runner
    image_config = BuildConfig.objects.get(module=image_repository_module)
    assert image_config.image_repository == 'https://example.com/image'
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
    assert legacy_image_repository_module.get_source_obj().get_repo_url() == 'https://example.com/image'
```
</details>

---


### 模块: apiserver/paasng/tests/paasng/platform/modules/test_helpers.py


#### test_bind_buildpack

**复杂度分数**: 12  
**严重程度**: warning  
**行数**: 72-121 (共 50 行, 0 行注释)  

**函数签名**:
```python
def test_bind_buildpack ( bk_module, slugbuilder, slugrunner, buildpack, slugbuilder_attrs, buildpack_attrs, linked, ok ) :
```

**消息**: Complexity 12 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

@pytest.mark.parametrize(('slugbuilder_attrs', 'buildpack_attrs', 'linked', 'ok'), [(dict(name=generate_random_string(12)), dict(name=generate_random_string(16)), False, False), (dict(region=generate_random_string()), dict(), False, False), (dict(), dict(region=generate_random_string()), False, False), (dict(name=generate_random_string(12)), dict(name=generate_random_string(16)), True, True), (dict(region=generate_random_string()), dict(), True, False), (dict(), dict(region=generate_random_string()), True, False), (dict(), dict(), True, True)])
def test_bind_buildpack(bk_module, slugbuilder, slugrunner, buildpack, slugbuilder_attrs, buildpack_attrs, linked, ok):
    for (k, v) in slugbuilder_attrs.items():
        setattr(slugbuilder, k, v)
        setattr(slugrunner, k, v)
    for (k, v) in buildpack_attrs.items():
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
        manager = ModuleRuntimeManager(bk_module)
        assert manager.get_slug_builder(raise_exception=True) == slugbuilder
        assert manager.list_buildpacks() == [buildpack]
        binder.bind_buildpack(buildpack)
        assert bk_module.build_config.buildpacks.count() == 1
    else:
        with pytest.raises(BindError):
            binder.bind_image(slugrunner=slugrunner, slugbuilder=slugbuilder)
            binder.bind_buildpack(buildpack)
```
</details>

---


#### test_bind_image

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 35-69 (共 35 行, 0 行注释)  

**函数签名**:
```python
def test_bind_image ( bk_module, slugbuilder, slugrunner, slugbuilder_attrs, slugrunner_attrs, ok ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

@pytest.mark.parametrize(('slugbuilder_attrs', 'slugrunner_attrs', 'ok'), [(dict(name=generate_random_string(12)), dict(name=generate_random_string(16)), False), (dict(region=generate_random_string()), dict(), False), (dict(), dict(region=generate_random_string()), False), (dict(), dict(), True)])
def test_bind_image(bk_module, slugbuilder, slugrunner, slugbuilder_attrs, slugrunner_attrs, ok):
    for (k, v) in slugbuilder_attrs.items():
        setattr(slugbuilder, k, v)
    for (k, v) in slugrunner_attrs.items():
        setattr(slugrunner, k, v)
    slugbuilder.save()
    slugrunner.save()
    binder = ModuleRuntimeBinder(bk_module)
    build_config = bk_module.build_config
    assert build_config.buildpack_builder is None
    assert build_config.buildpack_runner is None
    if ok:
        binder.bind_image(slugrunner, slugbuilder)
        manager = ModuleRuntimeManager(bk_module)
        assert manager.get_slug_builder(raise_exception=True) == slugbuilder
        assert manager.get_slug_runner(raise_exception=True) == slugrunner
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
        return [{'owner': {'login': 'octocat', 'avatar_url': 'https://github.com/images/error/octocat_happy.gif'}, 'name': 'Hello-World', 'description': 'This your first repo!', 'html_url': 'https://github.com/octocat/Hello-World', 'clone_url': 'https://github.com/octocat/Hello-World.git', 'ssh_url': 'git@github.com:octocat/Hello-World.git', 'created_at': '2011-01-26T19:01:12Z', 'updated_at': '2011-01-26T19:14:43Z'}, {'owner': {'login': 'octocat', 'avatar_url': 'https://github.com/images/error/octocat_happy.gif'}, 'name': 'hello-worId', 'description': 'My first repository on GitHub.', 'html_url': 'https://github.com/octocat/hello-worId', 'clone_url': 'https://github.com/octocat/hello-worId.git', 'ssh_url': 'git@github.com:octocat/hello-worId.git', 'created_at': '2014-01-26T19:01:12Z', 'updated_at': '2014-01-26T19:14:43Z'}]
    client.list_repo.side_effect = mock_list_repo
    ret = GitHubRepoController.list_all_repositories(api_url=github_repo_url, **user_credentials)
    assert len(ret) == 2
    assert ret[0].namespace == 'octocat'
    assert ret[0].project == 'Hello-World'
    assert ret[0].description == 'This your first repo!'
    assert ret[0].last_activity_at == datetime.datetime(2011, 1, 26, 19, 14, 43, tzinfo=tzutc())
    assert ret[1].web_url == 'https://github.com/octocat/hello-worId'
    assert ret[1].http_url_to_repo == 'https://github.com/octocat/hello-worId.git'
    assert ret[1].ssh_url_to_repo == 'git@github.com:octocat/hello-worId.git'
    assert ret[1].created_at == datetime.datetime(2014, 1, 26, 19, 1, 12, tzinfo=tzutc())
```
</details>

---


### 模块: operator/scripts/update_helm_chart.py


#### _remove_useless_newline

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 589-617 (共 29 行, 0 行注释)  
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
            if not src.endswith('yaml'):
                continue
            fp = self.chart_source_dir / TMPL_DIR / src
            try:
                contents = fp.read_text().splitlines()
            except FileNotFoundError:
                print(f'file {src} not exists, auto create...')
                fp.touch()
                continue
            for idx in range(len(contents)):
                if idx and contents[idx].count('}}') and contents[idx - 1].count('{{') - contents[idx - 1].count('}}') == 1:
                    contents[idx - 1] = contents[idx - 1].rstrip() + ' '
                    contents[idx - 1] += contents[idx].lstrip()
                    contents[idx] = ''
            fp.write_text('\n'.join([line for line in contents if line]) + '\n')
```
</details>

---


### 模块: svc-rabbitmq/tasks/management/commands/worker.py


#### guard

**复杂度分数**: 10  
**严重程度**: acceptable  
**行数**: 67-101 (共 35 行, 0 行注释)  

**函数签名**:
```python
def guard ( self ) :
```

**消息**: Complexity 10 exceeds threshold 10

<details>
<summary>查看源代码</summary>

```python

def guard(self):
    logger.info(_('{} guarding cluster at {}').format(self.name, self.pid))
    self.start_event.set()
    Stat(self).save()
    logger.info(_('Q Cluster-{} running.').format(self.parent_pid))
    self.schedule()
    counter = 0
    cycle = Conf.GUARD_CYCLE
    while not self.stop_event.is_set() or not counter:
        for p in self.pool:
            with p.timer.get_lock():
                if not p.is_alive() or p.timer.value == 0:
                    self.reincarnate(p)
                    continue
                if p.timer.value > 0:
                    p.timer.value -= cycle
        if not self.monitor.is_alive():
            self.reincarnate(self.monitor)
        if not self.pusher.is_alive():
            self.reincarnate(self.pusher)
        counter += cycle
        if counter >= 30:
            counter = 0
            self.schedule()
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

def run_once(self, client: Client, max_idle_seconds: int, safe_peer_host: typing.List[str], peer_host: typing.List[str], *args, **kwargs):
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
            print(f'list channels for connection {connection} failed: {err}, check in next time')
            rest_connections.append(connection)
            continue
        channels = [Channel(**i) for i in chs]
        if not self.has_consumer_channel(channels):
            print(f'connection {connection} is for publisher')
        elif not self.consumer_channels_idle(channels, timedelta(seconds=max_idle_seconds)):
            print(f'connection {connection} is activating, skipped')
            rest_connections.append(connection)
            continue
        else:
            print(f'idle connection {connection} is for consumer')
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
    if not ignore_consumer and channel['consumer_count'] > 0:
        return True
    if channel['acks_uncommitted'] > 0:
        return True
    if channel['messages_unacknowledged'] > 0:
        return True
    if channel['messages_uncommitted'] > 0:
        return True
    if channel['messages_unconfirmed'] > 0:
        return True
    message_stats = channel.get('message_stats')
    if not message_stats:
        return False
    if 'confirm_details' in message_stats and message_stats['confirm_details']['rate'] > 0:
        return True
    if 'publish_details' in message_stats and message_stats['publish_details']['rate'] > 0:
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

def handle(self, host: Optional[str], port: Optional[str], password: Optional[str], api_port: Optional[int], api_url: Optional[str], admin: Optional[str], dry_run: bool, **options):
    svc_objs = ServiceInstance.objects.all()
    for svc_obj in svc_objs:
        credentials = svc_obj.get_credentials()
        updated_credentials = credentials.copy()
        if api_url:
            updated_credentials['management_api'] = api_url
        elif host and api_port:
            updated_credentials['management_api'] = 'http://%s:%s' % (host, api_port)
        if host:
            updated_credentials['host'] = host
        if port:
            updated_credentials['port'] = port
        if password:
            updated_credentials['password'] = password
        if admin:
            updated_credentials['admin'] = admin
        if not dry_run and updated_credentials != credentials:
            svc_obj.credentials = json.dumps(updated_credentials)
            svc_obj.save(update_fields=['credentials'])
        self.stdout.write(self.style.NOTICE(f'实例配置变化：\n before:{credentials} \n after:{updated_credentials} \n'))
```
</details>

---


### 模块: svc-rabbitmq/vendor/management/commands/sync_user_policies.py


#### handle

**复杂度分数**: 12  
**严重程度**: warning  
**行数**: 86-122 (共 37 行, 0 行注释)  

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
        policies = {p['name']: p for p in client.user_policy.get(vhost)}
        if add:
            names = enabled_policies.keys() - policies.keys()
            print(f'policies will be add: {names}')
            if not dry_run:
                self.patch_policies(vhost, client, names, enabled_policies)
        if update:
            names = []
            for n in enabled_policies.keys() & policies.keys():
                if not self.compare_policies(enabled_policies[n].dict(), policies[n]):
                    names.append(n)
            print(f'policies will be update: {names}')
            if not dry_run:
                self.patch_policies(vhost, client, names, enabled_policies)
        if delete:
            names = disabled_policies & policies.keys()
            print(f'policies will be delete: {names}')
            if not dry_run:
                self.delete_policies(vhost, client, names)
```
</details>

---

