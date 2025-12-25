# exception-handlers 扫描报告

## 元数据
暂无元数据。

## 概要信息
- **总数量**: 1189
- **已扫描文件数**: 422
- **扫描耗时**: 6777 毫秒


### 异常处理器统计
根据 ExceptionHandlerSummary 字段的额外汇总统计信息。

## 结果详情


### 文件: `apiserver/paasng/manage.py`

#### 异常处理器 (行 23-37)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 25 行: ImportError (13 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 29-32)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 31 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/apis/admin/helpers/operator.py`

#### 异常处理器 (行 45-50)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 50 行 (1 行)

**Except 子句详情:**
- 第 47 行: ResourceMissing, ApiException (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/apis/admin/serializers/clusters.py`

#### 异常处理器 (行 31-34)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 33 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/apis/admin/views/clusters.py`

#### 异常处理器 (行 96-102)

- **Try 块**: 3 行
- **Except 子句数量**: 1
- **Finally 子句**: 第 102 行 (1 行)

**Except 子句详情:**
- 第 99 行: SwitchDefaultClusterError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 191-195)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 193 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 205-209)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 207 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 229-233)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 231 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 235-238)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 237 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/apis/admin/views/processes.py`

#### 异常处理器 (行 126-129)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 128 行: ProcessSpecPlan.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/applications/api.py`

#### 异常处理器 (行 127-130)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 129 行: Build.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/applications/handlers.py`

#### 异常处理器 (行 33-36)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 35 行: Config.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/applications/models/config.py`

#### 异常处理器 (行 46-49)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 48 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/cnative/specs/handlers.py`

#### 异常处理器 (行 44-49)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 48 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/cnative/specs/models/app_resource.py`

#### 异常处理器 (行 73-79)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 75 行: AppModelResource.DoesNotExist (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 241-245)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 244 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 247-250)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 249 行: PDValidationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 253-258)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 257 行: AppModelResource.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/cnative/specs/mounts.py`

#### 异常处理器 (行 309-314)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 314 行 (1 行)

**Except 子句详情:**
- 第 311 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/cnative/specs/procs/replicas.py`

#### 异常处理器 (行 145-148)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 147 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/cnative/specs/resource.py`

#### 异常处理器 (行 59-68)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 63 行: ResourceNotFoundError (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 66 行: ResourceMissing (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 74-90)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 90 行 (1 行)

**Except 子句详情:**
- 第 82 行: ApiException (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/cnative/specs/serializers.py`

#### 异常处理器 (行 141-149)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 148 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 155-163)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 162 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/cnative/specs/svc_disc.py`

#### 异常处理器 (行 112-118)

- **Try 块**: 3 行
- **Except 子句数量**: 1
- **Else 子句**: 第 118 行 (1 行)

**Except 子句详情:**
- 第 115 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/cnative/specs/views.py`

#### 异常处理器 (行 100-103)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 102 行: AppModelRevision.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 138-141)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 140 行: AppUserCredential.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 149-166)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 151 行: Exception (16 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 194-197)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 196 行: GetSourceConfigDataError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 211-222)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 221 行: IntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 235-238)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 237 行: GetSourceConfigDataError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 274-277)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 276 行: IntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 289-292)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 291 行: GetSourceConfigDataError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/deploy/actions/archive.py`

#### 异常处理器 (行 47-53)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 49 行: ScaleProcessError (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=1

---

### 文件: `apiserver/paasng/paas_wl/bk_app/deploy/actions/delete.py`

#### 异常处理器 (行 76-79)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 78 行: WlApp.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 82-85)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 84 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/deploy/actions/deploy.py`

#### 异常处理器 (行 67-73)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Finally 子句**: 第 73 行 (1 行)

**Except 子句详情:**
- 第 69 行: KubeException (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 79-82)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 81 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 87-91)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 90 行: KubeException, ResourceNotFoundError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 95-99)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 98 行: KubeException, ResourceNotFoundError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 125-136)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 128 行: Exception (9 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/deploy/actions/exec.py`

#### 异常处理器 (行 64-118)

- **Try 块**: 17 行
- **Except 子句数量**: 4
- **Else 子句**: 第 114 行 (2 行)
- **Finally 子句**: 第 117 行 (2 行)

**Except 子句详情:**
- 第 81 行: ResourceDuplicate (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 88 行: ReadTargetStatusTimeout (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 98 行: PodNotSucceededError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 108 行: Exception (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/deploy/app_res/controllers.py`

#### 异常处理器 (行 103-106)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 105 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 190-194)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 192 行: CreateServiceAccountTimeout (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 217-220)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 219 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 246-263)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 254 行 (10 行)

**Except 子句详情:**
- 第 248 行: ResourceMissing (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 292-295)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 294 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 341-360)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 347 行 (14 行)

**Except 子句详情:**
- 第 343 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 413-422)

- **Try 块**: 2 行
- **Except 子句数量**: 2
- **Else 子句**: 第 422 行 (1 行)

**Except 子句详情:**
- 第 415 行: ResourceMissing (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 418 行: ApiException (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 486-491)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 488 行: AppEntityNotFound (4 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 513-517)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 515 行: AppEntityNotFound (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 535-543)

- **Try 块**: 3 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 538 行: AppEntityNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 541 行: ApiException (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 556-559)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 558 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 630-636)

- **Try 块**: 3 行
- **Except 子句数量**: 1
- **Else 子句**: 第 636 行 (1 行)

**Except 子句详情:**
- 第 633 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/deploy/management/commands/delete_slug.py`

#### 异常处理器 (行 128-136)

- **Try 块**: 7 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 135 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/deploy/processes.py`

#### 异常处理器 (行 69-73)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 72 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 84-88)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 87 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 126-129)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 128 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 132-136)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 135 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 165-168)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 167 行: ProcessSpec.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 198-203)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 202 行: ProcNotFoundInRes (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 207-210)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 209 行: ProcNotFoundInRes (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 242-245)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 244 行: ProcNotFoundInRes (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 275-278)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 277 行: ProcNotFoundInRes (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 282-285)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 284 行: ModuleProcessSpec.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 336-339)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 338 行: ProcessSpec.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/dev_sandbox/controller.py`

#### 异常处理器 (行 82-87)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 87 行 (1 行)

**Except 子句详情:**
- 第 84 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 96-101)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 100 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 105-108)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 107 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 187-190)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 189 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 192-195)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 194 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 306-311)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 310 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 320-325)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 324 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 327-332)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 331 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/monitoring/app_monitor/managers.py`

#### 异常处理器 (行 89-92)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 91 行: AppMetricsMonitor.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 100-104)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 102 行: AppEntityNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 117-120)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 119 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/monitoring/app_monitor/utils.py`

#### 异常处理器 (行 28-31)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 30 行: AppMetricsMonitor.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/monitoring/bklog/kres_entities.py`

#### 异常处理器 (行 73-77)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 75 行: AppEntityNotFound (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/monitoring/bklog/managers.py`

#### 异常处理器 (行 59-63)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 61 行: AppEntityNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paas_wl/bk_app/processes/apps.py`

#### 异常处理器 (行 32-35)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 34 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/processes/controllers.py`

#### 异常处理器 (行 44-47)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 46 行: ProcessSpec.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 99-108)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 107 行: Release.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/processes/kres_slzs.py`

#### 异常处理器 (行 52-55)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 54 行: IndexError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 91-95)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 94 行: KeyError, Release.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/processes/migrations/0007_auto_20231127_1756.py`

#### 异常处理器 (行 25-33)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 27 行: json.JSONDecodeError, TypeError (7 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/processes/models.py`

#### 异常处理器 (行 53-56)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 55 行: ProcessSpecPlan.MultipleObjectsReturned (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 259-262)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 261 行: ProcessSpecPlan.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 329-334)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 332 行: ProcessSpecPlan.DoesNotExist (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 337-342)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 340 行: ProcessSpecPlan.DoesNotExist (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/processes/processes.py`

#### 异常处理器 (行 307-317)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 315 行: ApiException (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/processes/readers.py`

#### 异常处理器 (行 121-124)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 123 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 133-138)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 137 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/processes/serializers.py`

#### 异常处理器 (行 388-391)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 390 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 404-407)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 406 行: Release.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/processes/views.py`

#### 异常处理器 (行 115-118)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 117 行: ProcessOperationTooOften (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 123-129)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 128 行 (2 行)

**Except 子句详情:**
- 第 125 行: ProcessSpec.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 165-179)

- **Try 块**: 2 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 174 行: ProcessNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 176 行: ScaleProcessError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 178 行: AutoscalingUnsupported (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 333-336)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 335 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 454-457)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 456 行: PreviousInstanceNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 466-469)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 468 行: PreviousInstanceNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/bk_app/processes/watch.py`

#### 异常处理器 (行 194-204)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Finally 子句**: 第 203 行 (2 行)

**Except 子句详情:**
- 第 199 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 212-218)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 217 行 (2 行)

**Except 子句详情:**
- 第 214 行: queue.Empty (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/infras/cluster/loaders.py`

#### 异常处理器 (行 96-99)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 98 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/infras/cluster/management/commands/initial_default_cluster.py`

#### 异常处理器 (行 68-109)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 108 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/infras/cluster/models.py`

#### 异常处理器 (行 215-219)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 218 行: self.model.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 380-383)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 382 行: ValidationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/infras/cluster/utils.py`

#### 异常处理器 (行 26-29)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 28 行: Cluster.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 45-48)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 47 行: Cluster.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/infras/resource_templates/managers.py`

#### 异常处理器 (行 40-45)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 44 行: ProcessProbe.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 90-95)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 94 行: AppAddOn.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/infras/resources/base/base.py`

#### 异常处理器 (行 69-77)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 77 行 (1 行)

**Except 子句详情:**
- 第 73 行: HTTPError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/infras/resources/base/kres.py`

#### 异常处理器 (行 91-96)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 93 行: ApiException (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 197-205)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 199 行: ResourceNotFoundError (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 316-323)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 323 行 (1 行)

**Except 子句详情:**
- 第 318 行: ApiException (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 346-351)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 351 行 (1 行)

**Except 子句详情:**
- 第 348 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 399-407)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 401 行: ApiException (7 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=2, break=0, continue=0

---
#### 异常处理器 (行 590-593)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 592 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 605-608)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 607 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 647-652)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 652 行 (1 行)

**Except 子句详情:**
- 第 649 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/infras/resources/base/kube_client.py`

#### 异常处理器 (行 47-52)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 51 行: NotFoundError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 108-113)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 110 行: ResourceNotUniqueError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 127-131)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 129 行: DynamicApiError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 143-146)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 145 行: AttributeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=1, break=0, continue=0

---
#### 异常处理器 (行 146-149)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 148 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/infras/resources/generation/mapper.py`

#### 异常处理器 (行 115-123)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 119 行: Release.DoesNotExist, KeyError (5 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=1, break=0, continue=0

---
#### 异常处理器 (行 133-143)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 141 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/infras/resources/kube_res/base.py`

#### 异常处理器 (行 199-203)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 201 行: APIServerVersionIncompatible (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 301-304)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 303 行: NotAppScopedResource (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 336-365)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 364 行: ApiException (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=1, break=0, continue=0

---
#### 异常处理器 (行 348-351)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 350 行: NotAppScopedResource (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 354-361)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 356 行: AppEntityDeserializeError (6 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=1

---
#### 异常处理器 (行 427-430)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 429 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 482-505)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 504 行: ApiException (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=1, break=0, continue=0

---
#### 异常处理器 (行 494-501)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 496 行: AppEntityDeserializeError (6 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=1

---
#### 异常处理器 (行 593-599)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 596 行: AppEntityNotFound (4 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 620-629)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 628 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 683-686)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 685 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/utils/kubestatus.py`

#### 异常处理器 (行 200-203)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 202 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/utils/models.py`

#### 异常处理器 (行 139-145)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Finally 子句**: 第 145 行 (1 行)

**Except 子句详情:**
- 第 141 行: AttributeError, ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/utils/views.py`

#### 异常处理器 (行 28-38)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 37 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/configuration/configmap/kres_entities.py`

#### 异常处理器 (行 49-53)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 51 行: AppEntityNotFound (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/images/kres_entities.py`

#### 异常处理器 (行 94-98)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 96 行: AppEntityNotFound (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/images/views.py`

#### 异常处理器 (行 56-59)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 58 行: IntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/egress/cluster_state.py`

#### 异常处理器 (行 46-52)

- **Try 块**: 3 行
- **Except 子句数量**: 1
- **Else 子句**: 第 52 行 (1 行)

**Except 子句详情:**
- 第 49 行: RegionClusterState.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 94-97)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 96 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/egress/management/commands/create_rc_state_binding.py`

#### 异常处理器 (行 46-54)

- **Try 块**: 3 行
- **Except 子句数量**: 2
- **Else 子句**: 第 54 行 (1 行)

**Except 子句详情:**
- 第 49 行: RegionClusterState.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 51 行: IntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/egress/management/commands/region_gen_state.py`

#### 异常处理器 (行 113-123)

- **Try 块**: 8 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 121 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/egress/models.py`

#### 异常处理器 (行 134-139)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 139 行 (1 行)

**Except 子句详情:**
- 第 136 行: RCStateAppBinding.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/egress/views.py`

#### 异常处理器 (行 71-81)

- **Try 块**: 3 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 74 行: RegionClusterState.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 77 行: IntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 79 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 100-103)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 102 行: RCStateAppBinding.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/entrance/handlers.py`

#### 异常处理器 (行 38-43)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 42 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/config.py`

#### 异常处理器 (行 43-47)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 45 行: KeyError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/domains/independent.py`

#### 异常处理器 (行 40-45)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 42 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 63-73)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 73 行 (1 行)

**Except 子句详情:**
- 第 70 行: Domain.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 85-88)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 87 行: IntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 91-105)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 101 行: ValidCertNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 103 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 121-130)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 123 行: PersistentAppDomainRequired (5 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 128 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 146-150)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 148 行: Domain.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 157-160)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 159 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/domains/manager.py`

#### 异常处理器 (行 85-100)

- **Try 块**: 9 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 94 行: ValidCertNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 96 行: IntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 98 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 110-114)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 113 行: ReplaceAppDomainFailed (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 177-181)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 179 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 197-201)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 199 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 213-217)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 215 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/kres_slzs/service.py`

#### 异常处理器 (行 96-100)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 98 行: KeyError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/management/commands/patch_legacy_ingresses.py`

#### 异常处理器 (行 77-81)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 79 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 97-100)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 99 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/management/commands/patch_services.py`

#### 异常处理器 (行 46-49)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 48 行: ResourceMissing (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/management/commands/refresh_cert.py`

#### 异常处理器 (行 60-63)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 62 行: AppDomainSharedCert.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 156-160)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 158 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 165-169)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 167 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/management/commands/shared_cert_tool.py`

#### 异常处理器 (行 100-103)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 102 行: AppDomainSharedCert.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/managers/base.py`

#### 异常处理器 (行 130-134)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 133 行: PluginNotConfigured (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 192-234)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 213 行 (22 行)

**Except 子句详情:**
- 第 194 行: AppEntityNotFound (18 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 249-252)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 251 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/managers/misc.py`

#### 异常处理器 (行 56-64)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 64 行 (1 行)

**Except 子句详情:**
- 第 58 行: ModuleEnvironment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 72-75)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 74 行: EmptyAppIngressError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 88-95)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 95 行 (1 行)

**Except 子句详情:**
- 第 90 行: AppEntityNotFound (4 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 103-106)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 105 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/managers/service.py`

#### 异常处理器 (行 63-69)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 69 行 (1 行)

**Except 子句详情:**
- 第 65 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/plugins/ingress.py`

#### 异常处理器 (行 67-70)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 69 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/serializers.py`

#### 异常处理器 (行 72-75)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 74 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 87-90)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 89 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/ingress/views.py`

#### 异常处理器 (行 58-62)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 61 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 73-76)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 75 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 98-102)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 100 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/networking/sync.py`

#### 异常处理器 (行 29-32)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 31 行: DefaultServiceNameRequired, EmptyAppIngressError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paas_wl/workloads/tracing/instrumentor.py`

#### 异常处理器 (行 44-47)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 46 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 54-57)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 56 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paas_wl/workloads/volume/persistent_volume_claim/kres_entities.py`

#### 异常处理器 (行 49-53)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 51 行: AppEntityNotFound (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 57-61)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 59 行: AppEntityNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/__init__.py`

#### 异常处理器 (行 30-37)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 36 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/ci/apps.py`

#### 异常处理器 (行 33-38)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 37 行: ImportError (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/ci/clients/bk_ci.py`

#### 异常处理器 (行 57-60)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 59 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 72-75)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 74 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 85-88)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 87 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/ci/handlers.py`

#### 异常处理器 (行 61-77)

- **Try 块**: 5 行
- **Except 子句数量**: 4

**Except 子句详情:**
- 第 66 行: NotSupportedRepoType (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 69 行: RepoNotFoundError (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 72 行: Oauth2TokenHolder.DoesNotExist (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 75 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/ci/managers.py`

#### 异常处理器 (行 37-40)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 39 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/ci/serializers.py`

#### 异常处理器 (行 45-49)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 48 行: NotSupportedCIBackend (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/ci/views.py`

#### 异常处理器 (行 88-92)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 91 行: NotSupportedRepoType (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/cloudapi/components/http.py`

#### 异常处理器 (行 37-41)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 39 行: requests.exceptions.RequestException (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 45-56)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 47 行: Exception (10 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/cloudapi/views.py`

#### 异常处理器 (行 251-269)

- **Try 块**: 8 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 268 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/dev_sandbox/management/commands/renew_dev_sandbox_expired_at.py`

#### 异常处理器 (行 40-45)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 42 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 55-60)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 58 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/dev_sandbox/views.py`

#### 异常处理器 (行 68-71)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 70 行: DevSandboxAlreadyExists (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 86-89)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 88 行: DevSandboxResourceNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 151-181)

- **Try 块**: 16 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 173 行: DevSandboxAlreadyExists (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 177 行: Exception (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 191-194)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 193 行: DevSandbox.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 212-215)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 214 行: DevSandbox.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 223-226)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 225 行: DevSandboxResourceNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 244-247)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 246 行: DevSandbox.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 275-286)

- **Try 块**: 4 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 279 行: GitLabBranchNameBugError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 281 行: NotImplementedError (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 285 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/log/filters.py`

#### 异常处理器 (行 115-118)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 117 行: AttributeError, KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 119-122)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 121 行: TypeError (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/log/management/commands/batch_setup_bklog.py`

#### 异常处理器 (行 66-69)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 68 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/log/serializers.py`

#### 异常处理器 (行 140-147)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 146 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/log/shim/setup_bklog.py`

#### 异常处理器 (行 179-183)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 181 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 306-314)

- **Try 块**: 6 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 312 行: CustomCollectorConfigModel.DoesNotExist (3 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/log/shim/setup_elk.py`

#### 异常处理器 (行 125-132)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 131 行: IntegrityError (2 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/log/utils.py`

#### 异常处理器 (行 114-117)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 116 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 119-122)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 121 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 132-143)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 134 行: KeyError (10 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 143-147)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 145 行: KeyError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/log/views/config.py`

#### 异常处理器 (行 178-182)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 181 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/log/views/logs.py`

#### 异常处理器 (行 65-68)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 67 行: NoIndexError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 76-79)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 78 行: BkLogGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 135-139)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 137 行: ValidationError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 185-188)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 187 行: ProcessLogQueryConfig.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 215-227)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 221 行: RequestError, BkLogApiError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=1, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 225 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 260-277)

- **Try 块**: 2 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 267 行: ScanError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 271 行: RequestError, BkLogApiError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=1, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 275 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 307-317)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 311 行: RequestError, BkLogApiError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=1, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 315 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 406-409)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 408 行: ProcessLogQueryConfig.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/paas_analysis/clients.py`

#### 异常处理器 (行 40-54)

- **Try 块**: 2 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 42 行: requests.RequestException (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 49 行: json.decoder.JSONDecodeError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 52 行: PAResponseError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/paas_analysis/handlers.py`

#### 异常处理器 (行 30-33)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 32 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/paas_analysis/views.py`

#### 异常处理器 (行 54-61)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 56 行: PAClientException (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 59 行: ImproperlyConfigured (3 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/publish/entrance/preallocated.py`

#### 异常处理器 (行 44-48)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 47 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 94-104)

- **Try 块**: 9 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 103 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/publish/market/handlers.py`

#### 异常处理器 (行 27-32)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 31 行: MarketConfig.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/publish/market/legacy_client/misc.py`

#### 异常处理器 (行 72-75)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 74 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/publish/market/models.py`

#### 异常处理器 (行 234-253)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 236 行: MarketConfig.DoesNotExist (18 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 318-322)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 320 行: ImportError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/publish/market/serializers.py`

#### 异常处理器 (行 103-107)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 105 行: Tag.MultipleObjectsReturned (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 246-249)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 248 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 452-455)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 454 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/publish/market/status.py`

#### 异常处理器 (行 43-48)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 47 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/publish/sync_market/engine.py`

#### 异常处理器 (行 68-71)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 70 行: FieldNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 304-308)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 306 行: ObjectDoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 324-328)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 326 行: ObjectDoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 330-334)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 332 行: ObjectDoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/publish/sync_market/handlers.py`

#### 异常处理器 (行 55-58)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 57 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 117-138)

- **Try 块**: 20 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 137 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 158-162)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 161 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 167-173)

- **Try 块**: 3 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 170 行: NotImplementedError (2 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 172 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 211-214)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 213 行: SqlIntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=4, break=0, continue=0

---
#### 异常处理器 (行 241-244)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 243 行: SqlIntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 253-258)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 257 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 350-355)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 354 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 372-378)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 377 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 393-397)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 396 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 400-404)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 403 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 414-417)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 416 行: Product.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 420-423)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 422 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/publish/sync_market/managers.py`

#### 异常处理器 (行 28-41)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 40 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 77-87)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 85 行: TagMap.DoesNotExist (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/serializers.py`

#### 异常处理器 (行 34-37)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 36 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/apps.py`

#### 异常处理器 (行 34-37)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 36 行: ImproperlyConfigured (2 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/local/manager.py`

#### 异常处理器 (行 153-156)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 155 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 203-206)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 205 行: Service.DoesNotExist, ValidationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 214-217)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 216 行: Service.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 315-318)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 317 行: ServiceModuleAttachment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 342-347)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 346 行: ServiceEngineAppAttachment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 384-387)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 386 行: ServiceEngineAppAttachment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/management/commands/batch_unbind_svc.py`

#### 异常处理器 (行 80-88)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 82 行: SvcAttachmentDoesNotExist (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 91-99)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 93 行: Exception (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 131-135)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 133 行: ServiceObjNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 143-147)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 145 行: Application.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/management/commands/sync_instance_config.py`

#### 异常处理器 (行 50-53)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 52 行: ServiceObjNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/manager.py`

#### 异常处理器 (行 123-126)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 125 行: ServiceObjNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 131-136)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 135 行: ServiceObjNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 142-145)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 144 行: ServiceObjNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 153-156)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 155 行: ServiceObjNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 160-167)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 167 行 (1 行)

**Except 子句详情:**
- 第 162 行: SvcAttachmentDoesNotExist (4 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 270-273)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 272 行: SvcAttachmentDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/models.py`

#### 异常处理器 (行 179-182)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 181 行: db_props.model_module_rel.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/remote/client.py`

#### 异常处理器 (行 58-61)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 60 行: TypeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 101-109)

- **Try 块**: 3 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 104 行: RequestException (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 107 行: json.decoder.JSONDecodeError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/remote/collector.py`

#### 异常处理器 (行 46-49)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 48 行: RemoteClientError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 57-60)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 59 行: RemoteClientError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 73-77)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 75 行: ValidationError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 152-155)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 154 行: AttributeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 161-168)

- **Try 块**: 2 行
- **Except 子句数量**: 2
- **Else 子句**: 第 168 行 (1 行)

**Except 子句详情:**
- 第 163 行: FetchRemoteSvcError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 165 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 174-177)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 176 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/remote/manager.py`

#### 异常处理器 (行 180-184)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 182 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 232-239)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 237 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 275-278)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 277 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 283-287)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 285 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 394-397)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 396 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 410-418)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 416 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 484-487)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 486 行: ServiceNotFound, RuntimeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 592-595)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 594 行: RemoteServiceModuleAttachment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 619-624)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 623 行: RemoteServiceEngineAppAttachment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 668-671)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 670 行: exceptions.ServiceObjNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 680-683)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 682 行: RemoteServiceEngineAppAttachment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 816-819)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 818 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 829-832)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 831 行: exceptions.SvcInstanceNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/remote/store.py`

#### 异常处理器 (行 47-51)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 50 行: json.decoder.JSONDecodeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 93-97)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 95 行: ServiceNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 136-143)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 142 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/serializers.py`

#### 异常处理器 (行 74-80)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 80 行 (1 行)

**Except 子句详情:**
- 第 76 行: ServiceConfigNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/sharing.py`

#### 异常处理器 (行 70-73)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 72 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 117-120)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 119 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 172-175)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 174 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/tasks.py`

#### 异常处理器 (行 36-46)

- **Try 块**: 2 行
- **Except 子句数量**: 2
- **Else 子句**: 第 46 行 (1 行)

**Except 子句详情:**
- 第 38 行: NotImplementedError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1
- 第 41 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/urls.py`

#### 异常处理器 (行 141-146)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 145 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/servicehub/views.py`

#### 异常处理器 (行 131-140)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 133 行: BindServiceNoPlansError (5 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 138 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 236-240)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 238 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 243-247)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 245 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 302-306)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 304 行: ServiceObjNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 537-546)

- **Try 块**: 8 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 545 行: ServiceObjNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 634-637)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 636 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 643-652)

- **Try 块**: 2 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 645 行: RuntimeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 647 行: ReferencedAttachmentNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 651 行: SharedAttachmentAlreadyExists (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/services/providers/mysql/provider.py`

#### 异常处理器 (行 83-87)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 85 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 128-156)

- **Try 块**: 23 行
- **Except 子句数量**: 1
- **Finally 子句**: 第 156 行 (1 行)

**Except 子句详情:**
- 第 152 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 187-200)

- **Try 块**: 9 行
- **Except 子句数量**: 1
- **Finally 子句**: 第 200 行 (1 行)

**Except 子句详情:**
- 第 196 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/services/providers/sentry/client.py`

#### 异常处理器 (行 37-52)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 50 行: requests.exceptions.RequestException (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 55-59)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 58 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/services/providers/sentry/provider.py`

#### 异常处理器 (行 108-114)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 112 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 142-149)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 147 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 154-158)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 156 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/accessories/services/utils.py`

#### 异常处理器 (行 34-37)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 36 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/smart_advisor/tags.py`

#### 异常处理器 (行 157-161)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 160 行: ValueError, KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/accessories/views.py`

#### 异常处理器 (行 51-54)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 53 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/bk_plugins/apigw.py`

#### 异常处理器 (行 38-54)

- **Try 块**: 3 行
- **Except 子句数量**: 1
- **Else 子句**: 第 45 行 (10 行)

**Except 子句详情:**
- 第 41 行: PluginApiGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 47-51)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 50 行: PluginApiGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 59-63)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 62 行: PluginApiGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 92-96)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 95 行: PluginApiGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 100-104)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 103 行: PluginApiGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 163-177)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 176 行: RequestException, BKAPIError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 185-191)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 190 行: RequestException, BKAPIError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 198-206)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 205 行: RequestException, BKAPIError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 213-218)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 217 行: RequestException, BKAPIError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/bk_plugins/logging.py`

#### 异常处理器 (行 77-80)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 79 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/bk_plugins/models.py`

#### 异常处理器 (行 52-59)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 56 行: ObjectDoesNotExist (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 205-210)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 210 行 (1 行)

**Except 子句详情:**
- 第 207 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/bk_plugins/pluginscenter_views.py`

#### 异常处理器 (行 202-226)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 218 行: Exception (9 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 249-252)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 251 行: Deployment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 255-259)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 257 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 279-282)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 281 行: Deployment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/bk_plugins/tasks.py`

#### 异常处理器 (行 45-53)

- **Try 块**: 2 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 47 行: Deployment.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 50 行: OfflineOperationExistError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 52 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/bk_plugins/views.py`

#### 异常处理器 (行 191-195)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 193 行: RuntimeError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 201-204)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 203 行: TypeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 251-255)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 253 行: RuntimeError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/bk_devops/client.py`

#### 异常处理器 (行 65-68)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 67 行: APIGatewayResponseError, ResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 84-87)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 86 行: APIGatewayResponseError, ResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 113-116)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 115 行: APIGatewayResponseError, ResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 139-142)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 141 行: APIGatewayResponseError, ResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 163-166)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 165 行: APIGatewayResponseError, ResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 187-190)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 189 行: APIGatewayResponseError, ResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 224-227)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 226 行: APIGatewayResponseError, ResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 245-248)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 247 行: APIGatewayResponseError, ResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/bk_user/client.py`

#### 异常处理器 (行 36-39)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 38 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/iam_adaptor/management/client.py`

#### 异常处理器 (行 112-115)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 114 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 130-133)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 132 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 154-157)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 156 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 175-178)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 177 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 210-213)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 212 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 233-236)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 235 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 252-255)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 254 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 281-284)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 283 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 304-307)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 306 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 350-353)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 352 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/iam_adaptor/management/shim.py`

#### 异常处理器 (行 54-59)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 56 行: BKIAMApiError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 58 行: BKIAMGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/iam_adaptor/migrator.py`

#### 异常处理器 (行 39-42)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 41 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/itsm_adaptor/client.py`

#### 异常处理器 (行 64-69)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 68 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 114-119)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 118 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 130-135)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 134 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 160-165)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 164 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 191-196)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 195 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 207-214)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 213 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 236-241)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 240 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 254-259)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 258 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/management/commands/import_itsm_service.py`

#### 异常处理器 (行 40-45)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 42 行: ItsmCatalogNotExistsError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 55-66)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 60 行 (7 行)

**Except 子句详情:**
- 第 57 行: ItsmApiError, ItsmGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/models/instances.py`

#### 异常处理器 (行 105-110)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 107 行: SuspiciousOperation, RequestError (4 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 179-184)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 183 行: self.model.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 198-205)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 204 行: self.model.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 221-224)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 223 行: self.model.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 487-490)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 489 行: PluginVisibleRange.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 539-543)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 541 行: release.release_strategies.model.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/releases/stages.py`

#### 异常处理器 (行 155-162)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 160 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 282-289)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 287 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/serializers.py`

#### 异常处理器 (行 490-494)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 493 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 648-655)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 654 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/shim.py`

#### 异常处理器 (行 62-80)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 64 行: Exception (17 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 69-79)

- **Try 块**: 8 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 77 行: SourceAPIError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 102-109)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 104 行: StdAPIError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 107 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 141-147)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 143 行: PluginRepoNameConflict (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 145 行: SourceAPIError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 149-153)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 151 行: GitCommandExecutionError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/sourcectl/__init__.py`

#### 异常处理器 (行 60-63)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 62 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 68-71)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 70 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/sourcectl/tencent.py`

#### 异常处理器 (行 143-148)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 145 行: APIError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 209-212)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 211 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/thirdparty/utils.py`

#### 异常处理器 (行 117-120)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 119 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 130-133)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 132 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/bk_plugins/pluginscenter/views.py`

#### 异常处理器 (行 505-510)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 507 行: BkDevopsApiError, BkDevopsGatewayServiceError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 1075-1091)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 1085 行: RequestError, BkLogApiError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=1, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 1089 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 1111-1129)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 1123 行: RequestError, BkLogApiError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=1, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 1127 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 1149-1165)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 1159 行: RequestError, BkLogApiError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=1, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 1163 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 1187-1202)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 1196 行: RequestError, BkLogApiError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=1, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 1200 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 1224-1241)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 1235 行: RequestError, BkLogApiError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=1, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 1239 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/core/core/protections/base.py`

#### 异常处理器 (行 72-75)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 74 行: ConditionNotMatched (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/core/core/storages/redisdb.py`

#### 异常处理器 (行 39-42)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 41 行: AttributeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/core/core/storages/utils.py`

#### 异常处理器 (行 120-130)

- **Try 块**: 4 行
- **Except 子句数量**: 1
- **Finally 子句**: 第 129 行 (2 行)

**Except 子句详情:**
- 第 124 行: Exception (4 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 143-148)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 147 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/core/region/models.py`

#### 异常处理器 (行 57-62)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 62 行 (1 行)

**Except 子句详情:**
- 第 59 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/accounts/middlewares.py`

#### 异常处理器 (行 88-92)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 90 行: UserPrivateToken.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 179-187)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 187 行 (1 行)

**Except 子句详情:**
- 第 181 行: AuthenticatedAppAsUser.DoesNotExist (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=2, raise=0, break=0, continue=0

---
#### 异常处理器 (行 248-253)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 253 行 (1 行)

**Except 子句详情:**
- 第 250 行: json.decoder.JSONDecodeError (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/accounts/models.py`

#### 异常处理器 (行 147-153)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 149 行: self.model.DoesNotExist (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=1, break=0, continue=0

---
#### 异常处理器 (行 201-204)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 203 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 301-304)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 303 行: AccountFeatureFlag.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/accounts/oauth/backends.py`

#### 异常处理器 (行 190-193)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 192 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 194-198)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 196 行: KeyError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 239-253)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 252 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 260-272)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 271 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 277-284)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 283 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 294-308)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 307 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 315-327)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 326 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 332-339)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 338 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/accounts/oauth/models.py`

#### 异常处理器 (行 58-63)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 61 行: KeyError, ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/accounts/permissions/application.py`

#### 异常处理器 (行 138-141)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 140 行: AuthAPIError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/accounts/permissions/global_site.py`

#### 异常处理器 (行 54-57)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 56 行: UserProfile.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/accounts/utils.py`

#### 异常处理器 (行 30-35)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 34 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/accounts/views.py`

#### 异常处理器 (行 131-138)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 137 行: BKAppOauthError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 143-146)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 145 行: BkOauthClientDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 147-154)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 153 行: BKAppOauthError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 160-163)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 162 行: BkOauthClientDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 169-172)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 171 行: BKAppOauthError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 176-179)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 178 行: BkOauthClientDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 224-227)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 226 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 229-234)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 231 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 238-245)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 242 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 255-258)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 257 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 260-270)

- **Try 块**: 7 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 267 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/bk_ci/client.py`

#### 异常处理器 (行 36-39)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 38 行: APIGatewayResponseError, ResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/bk_log/client.py`

#### 异常处理器 (行 70-73)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 72 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 95-98)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 97 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 153-156)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 155 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 195-198)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 197 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/bkmonitorv3/client.py`

#### 异常处理器 (行 73-76)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 75 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 101-106)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 105 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 126-129)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 128 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 163-167)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 165 行: APIGatewayResponseError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 189-193)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 191 行: APIGatewayResponseError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 224-228)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 226 行: APIGatewayResponseError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 245-256)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 255 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 267-276)

- **Try 块**: 8 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 275 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/bkmonitorv3/params.py`

#### 异常处理器 (行 28-31)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 30 行: BKMonitorSpace.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/bkmonitorv3/shim.py`

#### 异常处理器 (行 35-39)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 38 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 73-76)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 75 行: BKMonitorSpace.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/iam/client.py`

#### 异常处理器 (行 90-95)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 94 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 114-119)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 118 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 135-145)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 144 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 164-169)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 168 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 195-201)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 200 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 220-226)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 225 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 258-269)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 263 行: HTTPResponseError (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 268 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 296-301)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 300 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 317-320)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 319 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 351-357)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 356 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 377-383)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 382 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 405-411)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 410 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 431-437)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 436 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 478-485)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 484 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 508-515)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 514 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 538-545)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 544 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/iam/legacy.py`

#### 异常处理器 (行 46-51)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 49 行: AuthAPIError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 60-63)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 62 行: AuthAPIError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/iam/members/management/commands/migrate_bkpaas3_perm.py`

#### 异常处理器 (行 124-137)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 137 行 (1 行)

**Except 子句详情:**
- 第 126 行: Exception (10 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 194-197)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 196 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 231-234)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 233 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 244-247)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 246 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 257-260)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 259 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/iam/members/management/commands/regrant_user_group_policies.py`

#### 异常处理器 (行 81-91)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 89 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/iam/members/management/commands/sync_app_admin_members.py`

#### 异常处理器 (行 110-125)

- **Try 块**: 3 行
- **Except 子句数量**: 1
- **Else 子句**: 第 125 行 (1 行)

**Except 子句详情:**
- 第 114 行: Exception (10 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 171-175)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 174 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/iam/open_apis/authentication.py`

#### 异常处理器 (行 30-35)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 34 行: RESTAuthenticationFailed (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/iam/permissions/perm.py`

#### 异常处理器 (行 164-168)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 166 行: PermissionDeniedError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/iam/permissions/resources/application.py`

#### 异常处理器 (行 217-221)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 219 行: AuthAPIError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/legacydb/adaptors.py`

#### 异常处理器 (行 167-171)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 170 行: SqlIntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=4, break=0, continue=0

---
#### 异常处理器 (行 183-188)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 188 行 (1 行)

**Except 子句详情:**
- 第 185 行: OAuth2Client.DoesNotExist (2 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 424-427)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 426 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/oauth2/api.py`

#### 异常处理器 (行 49-70)

- **Try 块**: 2 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 51 行: requests.RequestException (8 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 59 行: json.decoder.JSONDecodeError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 62 行: BkOauthApiResponseError (9 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/infras/oauth2/utils.py`

#### 异常处理器 (行 52-55)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 54 行: BkAppSecretInEnvVar.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 70-73)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 72 行: OAuth2Client.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/audit/service.py`

#### 异常处理器 (行 47-51)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 49 行: Application.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 69-84)

- **Try 块**: 8 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 83 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/changelog/query.py`

#### 异常处理器 (行 58-63)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 63 行 (1 行)

**Except 子句详情:**
- 第 60 行: InvalidChangelogError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 85-90)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 89 行: TypeError, ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/metrics/workloads/deployment.py`

#### 异常处理器 (行 50-54)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 52 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 56-60)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 58 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/healthz/probes.py`

#### 异常处理器 (行 133-136)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 135 行: AttributeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 147-159)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 149 行: FetchRemoteSvcError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 158 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/metrics/clients/bkmonitor.py`

#### 异常处理器 (行 43-51)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 48 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 71-77)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 76 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 84-89)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 87 行: BkMonitorGatewayServiceError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/metrics/clients/prometheus.py`

#### 异常处理器 (行 45-53)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 50 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 76-87)

- **Try 块**: 3 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 82 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 85 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/metrics/exceptions.py`

#### 异常处理器 (行 25-28)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 27 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/metrics/management/commands/deploy_stats_diagnoser.py`

#### 异常处理器 (行 77-81)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 79 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 85-88)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 87 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/metrics/models.py`

#### 异常处理器 (行 79-83)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 81 行: KeyError (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 152-155)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 154 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 174-178)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 177 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/metrics/shim.py`

#### 异常处理器 (行 37-45)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 44 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 57-61)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 60 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/ascode/client.py`

#### 异常处理器 (行 130-140)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 138 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/config/app_rule.py`

#### 异常处理器 (行 151-155)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 153 行: BKMonitorNotSupportedError (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 214-220)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 218 行: BKMonitorNotSupportedError (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/config/metric_label.py`

#### 异常处理器 (行 118-122)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 120 行: ServiceObjNotFound (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/monitor/alert_rules/tasks.py`

#### 异常处理器 (行 30-34)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 33 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 42-46)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 45 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/monitor/dashboards/handlers.py`

#### 异常处理器 (行 36-40)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 39 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/monitor/management/commands/init_alert_rules.py`

#### 异常处理器 (行 58-63)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 63 行 (1 行)

**Except 子句详情:**
- 第 60 行: exceptions.AsCodeAPIError, BKMonitorNotSupportedError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/monitor/management/commands/init_dashboards.py`

#### 异常处理器 (行 58-63)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 63 行 (1 行)

**Except 子句详情:**
- 第 60 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/monitor/service_monitor/controller.py`

#### 异常处理器 (行 56-59)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 58 行: ObservabilityConfig.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 76-80)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 78 行: AppEntityNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 90-93)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 92 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/monitoring/monitor/views.py`

#### 异常处理器 (行 250-255)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 252 行: BKMonitorNotSupportedError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 254 行: AsCodeAPIError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 273-276)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 275 行: BkMonitorGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 297-300)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 299 行: BkMonitorGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 333-339)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 335 行: BkMonitorSpaceDoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 338 行: BkMonitorGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 352-357)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 357 行 (1 行)

**Except 子句详情:**
- 第 354 行: BKMonitorSpace.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 362-365)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 364 行: BKMonitorSpace.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/operations/models.py`

#### 异常处理器 (行 132-135)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 134 行: TypeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 187-190)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 189 行: TypeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 229-232)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 231 行: TypeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 314-317)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 316 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/search/backends.py`

#### 异常处理器 (行 66-70)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 68 行: JSONDecodeError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 84-87)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 86 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 99-104)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 103 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/search/urls.py`

#### 异常处理器 (行 41-46)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 45 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/tools/views.py`

#### 异常处理器 (行 46-49)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 48 行: yaml.YAMLError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 51-54)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 53 行: ValueError, TypeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/misc/tracing/instrumentor.py`

#### 异常处理器 (行 44-47)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 46 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 54-57)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 56 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin42/serializers/accountmgr.py`

#### 异常处理器 (行 38-50)

- **Try 块**: 3 行
- **Except 子句数量**: 1
- **Else 子句**: 第 50 行 (1 行)

**Except 子句详情:**
- 第 46 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin42/serializers/engine.py`

#### 异常处理器 (行 57-60)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 59 行: ModuleEnvironmentOperations.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 64-69)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 68 行: ModuleEnvironmentOperations.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 73-76)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 75 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin42/serializers/services.py`

#### 异常处理器 (行 43-46)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 45 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin42/serializers/sourcectl.py`

#### 异常处理器 (行 53-56)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 55 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 58-61)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 60 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin42/utils/organization.py`

#### 异常处理器 (行 42-47)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 46 行: ComponentResponseInvalid (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin42/views/applications.py`

#### 异常处理器 (行 115-119)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 117 行: KeyError, ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 224-227)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 226 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 389-392)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 391 行: BKIAMGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 412-416)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 415 行: BKIAMGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin42/views/engine/runtime.py`

#### 异常处理器 (行 48-57)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 56 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 71-80)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 79 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 125-129)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 128 行: BPNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin42/views/operation/deploy.py`

#### 异常处理器 (行 211-216)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 215 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 229-235)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 234 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin42/views/services.py`

#### 异常处理器 (行 160-163)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 162 行: SvcAttachmentDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 234-237)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 236 行: UnsupportedOperationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 249-252)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 251 行: ServiceObjNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 263-266)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 265 行: UnsupportedOperationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 319-322)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 321 行: UnsupportedOperationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 343-346)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 345 行: UnsupportedOperationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 368-371)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 370 行: UnsupportedOperationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin42/views/sourcectl.py`

#### 异常处理器 (行 53-58)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 57 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin_cli/management/commands/adm_archive.py`

#### 异常处理器 (行 41-45)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 43 行: Application.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 69-77)

- **Try 块**: 3 行
- **Except 子句数量**: 2
- **Else 子句**: 第 77 行 (1 行)

**Except 子句详情:**
- 第 72 行: OfflineOperationExistError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 74 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin_cli/management/commands/adm_mapper_v1.py`

#### 异常处理器 (行 80-85)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 85 行 (1 行)

**Except 子句详情:**
- 第 82 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 105-109)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 107 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 166-173)

- **Try 块**: 3 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 173 行 (1 行)

**Except 子句详情:**

---

### 文件: `apiserver/paasng/paasng/plat_admin/admin_cli/mapper_version.py`

#### 异常处理器 (行 50-53)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 52 行: ModuleEnvironment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/plat_admin/initialization/management/commands/init_bkrepo.py`

#### 异常处理器 (行 67-75)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 69 行: RequestError (7 行)
  - 日志调用: debug=1, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/numbers/app.py`

#### 异常处理器 (行 55-58)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 57 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 60-64)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 62 行: ImportError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 522-526)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 525 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 753-760)

- **Try 块**: 4 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 757 行: Oauth2TokenHolder.DoesNotExist, UserProfile.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 759 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/system/applications.py`

#### 异常处理器 (行 38-43)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 41 行: ImportError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/system/legacy.py`

#### 异常处理器 (行 28-31)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 30 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/system/utils.py`

#### 异常处理器 (行 30-33)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 32 行: KeyError, ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/plat_admin/system/views.py`

#### 异常处理器 (行 170-174)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 172 行: ServiceObjNotFound (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 190-193)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 192 行: ServiceObjNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 195-202)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 197 行: SvcAttachmentDoesNotExist (6 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 202-206)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 204 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 288-291)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 290 行: SvcAttachmentDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 298-301)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 300 行: ServiceObjNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/platform/applications/handlers.py`

#### 异常处理器 (行 63-66)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 65 行: BKIAMGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 171-177)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 175 行: ClientError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 185-196)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 195 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/applications/management/commands/create_3rd_party_apps.py`

#### 异常处理器 (行 121-131)

- **Try 块**: 4 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 130 行 (2 行)

**Except 子句详情:**

---
#### 异常处理器 (行 138-152)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 150 行: DjangoIntegrityError (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 155-159)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 157 行: BKIAMGatewayServiceError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 165-173)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 167 行: IntegrityError (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=1, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/applications/management/commands/force_del_app.py`

#### 异常处理器 (行 79-87)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 84 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/applications/mixins.py`

#### 异常处理器 (行 75-78)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 77 行: Module.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 89-92)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 91 行: Module.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 93-96)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 95 行: ModuleEnvironment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 118-121)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 120 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/platform/applications/models.py`

#### 异常处理器 (行 220-224)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 223 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 227-230)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 229 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 390-393)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 392 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 425-430)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 427 行: SuspiciousOperation, RequestError (4 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 497-502)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 502 行 (1 行)

**Except 子句详情:**
- 第 499 行: Deployment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 561-564)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 563 行: ApplicationFeatureFlag.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/applications/operators.py`

#### 异常处理器 (行 82-85)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 84 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 102-107)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 106 行: ModuleEnvironmentOperations.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/applications/protections.py`

#### 异常处理器 (行 76-79)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 78 行: ConditionNotMatched (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 93-97)

- **Try 块**: 3 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 97 行 (1 行)

**Except 子句详情:**

---

### 文件: `apiserver/paasng/paasng/platform/applications/serializers/app.py`

#### 异常处理器 (行 137-141)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 139 行: IntegrityError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/applications/serializers/member_role.py`

#### 异常处理器 (行 33-36)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 35 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 37-40)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 39 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/applications/serializers/validators.py`

#### 异常处理器 (行 63-66)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 65 行: AppFieldValidationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/applications/specs.py`

#### 异常处理器 (行 74-80)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 79 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 87-90)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 89 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 124-127)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 126 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/applications/urls.py`

#### 异常处理器 (行 233-238)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 237 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/applications/utils.py`

#### 异常处理器 (行 223-226)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 225 行: AppModelDeploy.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 228-231)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 230 行: Deployment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/applications/views.py`

#### 异常处理器 (行 133-138)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 136 行: ImportError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 254-258)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 256 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 471-486)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 475 行: Exception (12 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 500-504)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 502 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 507-511)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 509 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 540-545)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 542 行: BkMonitorGatewayServiceError, BkMonitorApiError (2 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 544 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 581-590)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 585 行: DbIntegrityError (6 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 632-638)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 637 行: LessCodeApiError, LessCodeGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 680-683)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 682 行: LessCodeApiError, LessCodeGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 811-820)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 816 行: IndexError (5 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 892-901)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 896 行: DescriptionValidationError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 899 行: ControllerError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 916-919)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 918 行: DbIntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 946-950)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 949 行: BKIAMGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 965-969)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 968 行: BKIAMGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 980-983)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 982 行: BKIAMGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 998-1001)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 1000 行: BKIAMGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 1256-1281)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 1273 行: IntegrityError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 1279 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 1285-1291)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 1289 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 1310-1314)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 1312 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 1344-1348)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 1346 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 1353-1357)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 1355 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 1424-1429)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 1428 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/bk_lesscode/client.py`

#### 异常处理器 (行 74-81)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 79 行: APIGatewayResponseError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 93-98)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 95 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/bkapp_model/fieldmgr/fields.py`

#### 异常处理器 (行 84-89)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 89 行 (1 行)

**Except 子句详情:**
- 第 86 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/bkapp_model/importer.py`

#### 异常处理器 (行 62-65)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 64 行: ValidationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/bkapp_model/manifest.py`

#### 异常处理器 (行 124-128)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 126 行: ImportError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 179-183)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 181 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 252-255)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 254 行: ValueError (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 259-262)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 261 行: ProcessSpecPlan.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 419-422)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 421 行: SvcDiscConfig.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 432-435)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 434 行: DomainResolution.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 446-449)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 448 行: ObservabilityConfig.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 632-637)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 637 行 (1 行)

**Except 子句详情:**
- 第 634 行: RCStateAppBinding.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/bkapp_model/migrations/0010_auto_20231127_2039.py`

#### 异常处理器 (行 26-34)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 28 行: json.JSONDecodeError, TypeError (7 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 52-60)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 54 行: json.JSONDecodeError, TypeError (7 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/bkapp_model/models.py`

#### 异常处理器 (行 50-53)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 52 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 256-259)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 258 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 323-326)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 325 行: SvcDiscConfig.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 342-351)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 347 行 (5 行)

**Except 子句详情:**
- 第 344 行: ObservabilityConfig.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/bkapp_model/serializers/serializers.py`

#### 异常处理器 (行 86-91)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 88 行: ValueError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/bkapp_model/serializers/v1alpha2.py`

#### 异常处理器 (行 196-201)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 198 行: ValueError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/bkapp_model/views.py`

#### 异常处理器 (行 86-91)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 91 行 (1 行)

**Except 子句详情:**
- 第 88 行: ImportError (2 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 130-133)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 132 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 150-154)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 153 行: ObservabilityConfig.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/declarative/application/controller.py`

#### 异常处理器 (行 190-193)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 192 行: ModuleInitializationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 270-273)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 272 行: NotImplementedError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 298-302)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 300 行: ServiceObjNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/platform/declarative/application/resources.py`

#### 异常处理器 (行 45-50)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 47 行: Application.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 49 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 119-122)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 121 行: StopIteration (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/declarative/deployment/svc_disc.py`

#### 异常处理器 (行 85-93)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 92 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 120-123)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 122 行: Application.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 124-129)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 128 行: Module.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/declarative/handlers.py`

#### 异常处理器 (行 60-63)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 62 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 83-86)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 85 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 245-250)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 247 行: UnsupportedSpecVer (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=1, break=0, continue=0

---
#### 异常处理器 (行 265-268)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 267 行: UnsupportedSpecVer (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 279-283)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 281 行: UnsupportedSpecVer (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 305-308)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 307 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/declarative/serializers.py`

#### 异常处理器 (行 49-52)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 51 行: ValidationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 62-65)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 64 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 160-168)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 165 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 167 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/declarative/utils.py`

#### 异常处理器 (行 36-39)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 38 行: ValueError (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 41-44)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 43 行: ProcessSpecPlan.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/configurations/config_var.py`

#### 异常处理器 (行 118-121)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 120 行: BkOauthClientDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/configurations/image.py`

#### 异常处理器 (行 123-127)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 126 行: RepoBasicAuthHolder.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/configurations/source_file.py`

#### 异常处理器 (行 92-95)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 94 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 123-126)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 125 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 142-146)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 145 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 163-177)

- **Try 块**: 3 行
- **Except 子句数量**: 4

**Except 子句详情:**
- 第 166 行: exceptions.RequestTimeOutError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=1, continue=0
- 第 169 行: exceptions.ReadLinkFileOutsideDirectoryError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=1, continue=0
- 第 172 行: exceptions.ReadFileNotFoundError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1
- 第 175 行: Exception (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 215-218)

- **Try 块**: 2 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 218 行 (1 行)

**Except 子句详情:**

---
#### 异常处理器 (行 227-231)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 230 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/deploy/bg_build/executors.py`

#### 异常处理器 (行 84-145)

- **Try 块**: 27 行
- **Except 子句数量**: 3
- **Else 子句**: 第 144 行 (2 行)

**Except 子句详情:**
- 第 111 行: ReadTargetStatusTimeout (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 128 行: PodNotSucceededError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 140 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 149-167)

- **Try 块**: 4 行
- **Except 子句数量**: 1
- **Else 子句**: 第 164 行 (1 行)
- **Finally 子句**: 第 167 行 (1 行)

**Except 子句详情:**
- 第 157 行: Exception (6 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 183-188)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 185 行: ResourceDuplicate (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 233-237)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 235 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 268-303)

- **Try 块**: 19 行
- **Except 子句数量**: 4
- **Else 子句**: 第 302 行 (2 行)

**Except 子句详情:**
- 第 288 行: BkCIGatewayServiceError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 292 行: BkCIPipelineBuildNotSuccess (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 295 行: BkCITooManyEnvVarsError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 298 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 341-345)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 343 行: BkCIGatewayServiceError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/deploy/bg_command/bkapp_hook.py`

#### 异常处理器 (行 60-63)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 62 行: StepNotInPresetListError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 72-80)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 74 行: ReadTargetStatusTimeout (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 82-87)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 85 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 89-92)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 91 行: ReadTargetStatusTimeout (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 102-105)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 104 行: StepNotInPresetListError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/deploy/bg_command/pre_release.py`

#### 异常处理器 (行 81-85)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 83 行: KeyError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 98-101)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 100 行: StepNotInPresetListError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 105-108)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 107 行: StepNotInPresetListError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/deploy/bg_wait/wait_bkapp.py`

#### 异常处理器 (行 94-98)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 96 行: Deployment.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 243-247)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 246 行: StepNotInPresetListError (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 280-283)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 282 行: PyDanticValidationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/deploy/bg_wait/wait_deployment.py`

#### 异常处理器 (行 168-172)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 170 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 232-236)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 234 行: Deployment.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/deploy/building.py`

#### 异常处理器 (行 121-125)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 123 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 143-167)

- **Try 块**: 13 行
- **Except 子句数量**: 3
- **Else 子句**: 第 167 行 (1 行)

**Except 子句详情:**
- 第 159 行: InitDeployDescHandlerError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 161 行: DescriptionValidationError, ManifestImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 163 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 197-200)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 199 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 494-499)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 497 行: KeyError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/deploy/image_release.py`

#### 异常处理器 (行 125-147)

- **Try 块**: 13 行
- **Except 子句数量**: 2
- **Else 子句**: 第 147 行 (1 行)

**Except 子句详情:**
- 第 141 行: InitDeployDescHandlerError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 143 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 206-211)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 208 行: InvalidImageCredentials (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/deploy/interruptions.py`

#### 异常处理器 (行 53-58)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 55 行: DeployInterruptionFailed (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/deploy/release/legacy.py`

#### 异常处理器 (行 77-81)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 80 行: StepNotInPresetListError (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 94-98)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 97 行: StepNotInPresetListError (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 145-148)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 147 行: PyDanticValidationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 208-212)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 210 行: KubeException (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/deploy/release/operator.py`

#### 异常处理器 (行 75-81)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 80 行: StepNotInPresetListError (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 113-125)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 123 行: IntegrityError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 127-164)

- **Try 块**: 34 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 161 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 201-205)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 204 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 210-213)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 212 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/deploy/version.py`

#### 异常处理器 (行 53-58)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 56 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/logs.py`

#### 异常处理器 (行 121-124)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 123 行: OutputStream.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/management/commands/deploy_bkapp.py`

#### 异常处理器 (行 67-75)

- **Try 块**: 2 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 69 行: APIError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 71 行: DeployError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 73 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/management/commands/inject_engineapp_metadata.py`

#### 异常处理器 (行 42-48)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 44 行: Exception (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 52-60)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 56 行: Exception (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/platform/engine/management/commands/update_operations_pending_status.py`

#### 异常处理器 (行 70-81)

- **Try 块**: 10 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 80 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/models/config_var.py`

#### 异常处理器 (行 41-44)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 43 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/models/deployment.py`

#### 异常处理器 (行 210-215)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 212 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 221-230)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 228 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 235-244)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 242 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 283-286)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 285 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/models/managers.py`

#### 异常处理器 (行 132-140)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 139 行: ConfigVar.DoesNotExist (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/models/phases.py`

#### 异常处理器 (行 93-99)

- **Try 块**: 3 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 96 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 98 行: MultipleObjectsReturned (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/models/steps.py`

#### 异常处理器 (行 186-191)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 188 行: DeployStepMeta.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 190 行: DeployStepMeta.MultipleObjectsReturned (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/monitoring.py`

#### 异常处理器 (行 79-83)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 81 行: KeyError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/phases_steps/phases.py`

#### 异常处理器 (行 82-94)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 84 行: NoUnlinkedDeployPhaseError (11 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 86-92)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 91 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 100-105)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 102 行: DeployPhase.MultipleObjectsReturned (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 104 行: DeployPhase.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 111-115)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 113 行: StepNotInPresetListError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/platform/engine/phases_steps/steps.py`

#### 异常处理器 (行 106-110)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 108 行: StepNotInPresetListError, DuplicateNameInSamePhaseError (3 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/platform/engine/processes/events.py`

#### 异常处理器 (行 131-134)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 133 行: StopIteration (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 198-201)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 200 行: StopIteration (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/processes/handlers.py`

#### 异常处理器 (行 52-56)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 54 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/processes/views.py`

#### 异常处理器 (行 113-122)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 121 行: AppEntityNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/serializers.py`

#### 异常处理器 (行 301-304)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 303 行: yaml.YAMLError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 335-340)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 337 行: ModuleEnvironment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 339 行: TypeError, ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 649-652)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 651 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 663-666)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 665 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/utils/query.py`

#### 异常处理器 (行 35-38)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 37 行: Deployment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 42-45)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 44 行: Deployment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 63-66)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 65 行: OfflineOperation.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 70-73)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 72 行: OfflineOperation.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 80-83)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 82 行: OfflineOperation.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/utils/source.py`

#### 异常处理器 (行 91-98)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 95 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 97 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 108-116)

- **Try 块**: 3 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 111 行: GetDockerIgnoreError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 114 行: NotImplementedError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 161-164)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 163 行: NotImplementedError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 169-172)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 171 行: GetAppYamlError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 187-190)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 189 行: NotImplementedError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 195-201)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 197 行: GetAppYamlFormatError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 200 行: GetAppYamlError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 204-210)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 206 行: GetProcfileFormatError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 209 行: GetProcfileError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 221-224)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 223 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 279-284)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 284 行 (1 行)

**Except 子句详情:**
- 第 281 行: DeploymentDescription.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 328-335)

- **Try 块**: 6 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 334 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/views/deploy.py`

#### 异常处理器 (行 117-120)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 119 行: RoleNotAllowError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 142-154)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 153 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 182-193)

- **Try 块**: 4 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 186 行: GitLabBranchNameBugError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 188 行: NotImplementedError (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 192 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 292-295)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 294 行: DeployInterruptionFailed (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 315-318)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 317 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 321-325)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 323 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 340-343)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 342 行: Deployment.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/views/misc.py`

#### 异常处理器 (行 87-91)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 90 行: RoleNotAllowError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 93-108)

- **Try 块**: 2 行
- **Except 子句数量**: 3
- **Else 子句**: 第 105 行 (4 行)

**Except 子句详情:**
- 第 95 行: Deployment.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 98 行: OfflineOperationExistError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 101 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 120-126)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 125 行 (2 行)

**Except 子句详情:**
- 第 122 行: OfflineOperation.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 236-243)

- **Try 块**: 2 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 238 行: RequestMetricBackendError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 240 行: AppInstancesNotFoundError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 242 行: AppMetricNotSupportedError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/views/release.py`

#### 异常处理器 (行 138-143)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 142 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/workflow/flow.py`

#### 异常处理器 (行 125-129)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 127 行: StepNotInPresetListError (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 187-190)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 189 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 301-305)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 303 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 341-348)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 343 行: Exception (6 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/engine/workflow/protections.py`

#### 异常处理器 (行 75-99)

- **Try 块**: 3 行
- **Except 子句数量**: 4

**Except 子句详情:**
- 第 78 行: UserNotBindedToSourceProviderError (10 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 88 行: AccessTokenForbidden (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 92 行: BasicAuthError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 96 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 109-113)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 111 行: RoleNotAllowError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 143-148)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 148 行 (1 行)

**Except 子句详情:**
- 第 145 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 176-181)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 180 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/evaluation/collectors/resource.py`

#### 异常处理器 (行 161-183)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 182 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/evaluation/collectors/user_visit.py`

#### 异常处理器 (行 79-85)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 84 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/evaluation/providers.py`

#### 异常处理器 (行 29-32)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 31 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/evaluation/tasks.py`

#### 异常处理器 (行 142-146)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 144 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 215-219)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 217 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/base.py`

#### 异常处理器 (行 79-89)

- **Try 块**: 3 行
- **Except 子句数量**: 1
- **Finally 子句**: 第 88 行 (2 行)

**Except 子句详情:**
- 第 82 行: Exception (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 102-111)

- **Try 块**: 3 行
- **Except 子句数量**: 1
- **Finally 子句**: 第 110 行 (2 行)

**Except 子句详情:**
- 第 105 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/basic.py`

#### 异常处理器 (行 112-115)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 114 行: BKIAMGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/egress_gateway.py`

#### 异常处理器 (行 41-55)

- **Try 块**: 5 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 46 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 52 行: IntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 54 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 63-78)

- **Try 块**: 12 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 75 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 77 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/envs_base.py`

#### 异常处理器 (行 120-124)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 123 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/app_migrations/service.py`

#### 异常处理器 (行 65-72)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 72 行 (1 行)

**Except 子句详情:**
- 第 69 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 136-141)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 140 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/cnative_migrations/base.py`

#### 异常处理器 (行 56-60)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 59 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 62-65)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 64 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 69-73)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 71 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/cnative_migrations/build_config.py`

#### 异常处理器 (行 89-92)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 91 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/cnative_migrations/wl_app.py`

#### 异常处理器 (行 90-96)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 95 行: Release.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 106-112)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 111 行 (2 行)

**Except 子句详情:**
- 第 108 行: WlAppBackupRel.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/constants.py`

#### 异常处理器 (行 136-140)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 139 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/legacy_proxy.py`

#### 异常处理器 (行 146-151)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 150 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 154-160)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 159 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/management/commands/make_legacy_app_for_test.py`

#### 异常处理器 (行 197-203)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 201 行: TypeError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/migrate.py`

#### 异常处理器 (行 39-44)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 42 行: ImportError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 62-67)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 64 行: MigrationFailed (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 130-134)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 132 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 189-208)

- **Try 块**: 2 行
- **Except 子句数量**: 2
- **Else 子句**: 第 208 行 (1 行)

**Except 子句详情:**
- 第 191 行: PreCheckMigrationFailed, BackupLegacyDataFailed (9 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=1, continue=0
- 第 200 行: MigrationFailed (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=1, continue=0

---
#### 异常处理器 (行 226-231)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 231 行 (1 行)

**Except 子句详情:**
- 第 228 行: MigrationFailed, RollbackFailed (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 249-257)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 257 行 (1 行)

**Except 子句详情:**
- 第 251 行: RollbackFailed (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 268-279)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 277 行 (3 行)

**Except 子句详情:**
- 第 270 行: CNativeMigrationProcess.DoesNotExist (6 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=2, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/models.py`

#### 异常处理器 (行 40-43)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 42 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 50-67)

- **Try 块**: 7 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 57 行: MigrationProcess.DoesNotExist (11 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 297-300)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 299 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/tasks.py`

#### 异常处理器 (行 49-54)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 51 行: Exception (4 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=2, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 54-58)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 56 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 70-74)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 72 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 85-97)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 97 行 (1 行)

**Except 子句详情:**
- 第 89 行: Exception (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 104-114)

- **Try 块**: 6 行
- **Except 子句数量**: 1
- **Else 子句**: 第 114 行 (1 行)

**Except 子句详情:**
- 第 110 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/utils.py`

#### 异常处理器 (行 34-37)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 36 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 72-75)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 74 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 195-198)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 197 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 210-213)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 212 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 230-234)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 232 行: KeyError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/mgrlegacy/views.py`

#### 异常处理器 (行 51-54)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 53 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 315-321)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 320 行 (2 行)

**Except 子句详情:**
- 第 317 行: CNativeMigrationProcess.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 408-417)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 416 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 515-521)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 520 行 (2 行)

**Except 子句详情:**
- 第 517 行: RCStateAppBinding.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/modules/helpers.py`

#### 异常处理器 (行 158-162)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 161 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 260-269)

- **Try 块**: 4 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 264 行: AppSlugRunner.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 267 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 274-278)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 277 行: AppSlugRunner.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 279-282)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 281 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 287-291)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 290 行: AppSlugRunner.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 292-295)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 294 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/modules/management/commands/push_smart_image.py`

#### 异常处理器 (行 60-68)

- **Try 块**: 5 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 67 行 (2 行)

**Except 子句详情:**

---
#### 异常处理器 (行 107-117)

- **Try 块**: 7 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 114 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 122-133)

- **Try 块**: 9 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 132 行 (2 行)

**Except 子句详情:**

---

### 文件: `apiserver/paasng/paasng/platform/modules/manager.py`

#### 异常处理器 (行 93-99)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 98 行: Template.DoesNotExist, TmplRegionNotSupported (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 241-248)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 245 行: ObjectDoesNotExist (4 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 335-339)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 337 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 347-350)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 349 行: ModuleInitializationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 515-520)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 519 行: Template.DoesNotExist, TmplRegionNotSupported (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 525-529)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 527 行: ServiceObjNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/platform/modules/models/runtime.py`

#### 异常处理器 (行 46-49)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 48 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 119-122)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 121 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 215-219)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 217 行: KeyError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 220-223)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 222 行: self.model.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/modules/serializers.py`

#### 异常处理器 (行 96-101)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 101 行 (1 行)

**Except 子句详情:**
- 第 98 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 110-116)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 114 行: ObjectDoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 121-125)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 124 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 237-240)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 239 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 290-296)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 295 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/modules/specs.py`

#### 异常处理器 (行 125-128)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 127 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/modules/urls.py`

#### 异常处理器 (行 101-106)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 105 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/modules/views.py`

#### 异常处理器 (行 115-120)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 119 行: LessCodeApiError, LessCodeGatewayServiceError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 198-216)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 202 行: Exception (15 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 237-241)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 239 行: ObjectDoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 246-251)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 251 行 (1 行)

**Except 子句详情:**
- 第 248 行: MarketConfig.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 334-337)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 336 行: DbIntegrityError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 408-411)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 410 行: BPNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 501-508)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 507 行: BPNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 598-601)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 600 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/scene_app/initializer.py`

#### 异常处理器 (行 72-77)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 75 行: IOError, yaml.YAMLError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/smart_app/management/commands/smart_tool.py`

#### 异常处理器 (行 45-50)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 47 行: ControllerError, DescriptionValidationError, APIError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 49 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/smart_app/services/app_desc.py`

#### 异常处理器 (行 35-38)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 37 行: DescriptionValidationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/smart_app/services/detector.py`

#### 异常处理器 (行 91-97)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 95 行: RuntimeError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 118-122)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 120 行: YAMLError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 135-139)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 137 行: DescriptionValidationError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 160-165)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 162 行: PackageInvalidFileFormatError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 164 行: ReadLinkFileOutsideDirectoryError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 180-187)

- **Try 块**: 4 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 184 行: ReadFileNotFoundError (2 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 186 行: RuntimeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/smart_app/services/path.py`

#### 异常处理器 (行 97-102)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 102 行 (1 行)

**Except 子句详情:**
- 第 99 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 114-119)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 119 行 (1 行)

**Except 子句详情:**
- 第 116 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/smart_app/views.py`

#### 异常处理器 (行 132-136)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 134 行: PreparedPackageNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 149-153)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 151 行: ControllerError, DescriptionValidationError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 156-170)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 165 行: DescriptionValidationError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 168 行: RequestRegistryError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 184-188)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 187 行: tarfile.TarError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 286-290)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 288 行: PreparedPackageNotFound (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 304-308)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 306 行: ControllerError, DescriptionValidationError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 311-324)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 319 行: DescriptionValidationError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 322 行: RequestRegistryError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/client.py`

#### 异常处理器 (行 154-158)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 156 行: exceptions.AccessTokenError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 184-187)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 186 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 200-204)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 202 行: OAuth2Error (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=1, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/connector.py`

#### 异常处理器 (行 80-85)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 83 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 158-166)

- **Try 块**: 3 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 166 行 (1 行)

**Except 子句详情:**

---
#### 异常处理器 (行 171-180)

- **Try 块**: 4 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 180 行 (1 行)

**Except 子句详情:**

---
#### 异常处理器 (行 289-294)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 294 行 (1 行)

**Except 子句详情:**
- 第 291 行: CannotInitNonEmptyTrunk (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 359-364)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 362 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/controllers/bare_git.py`

#### 异常处理器 (行 61-65)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 63 行: ObjectDoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 81-92)

- **Try 块**: 3 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 84 行: GitCommandExecutionError (6 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0
- 第 90 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 160-163)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 162 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/controllers/bare_svn.py`

#### 异常处理器 (行 43-48)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 45 行: ObjectDoesNotExist (4 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/controllers/bk_svn.py`

#### 异常处理器 (行 53-60)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 60 行 (1 行)

**Except 子句详情:**
- 第 55 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 67-71)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 69 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/controllers/docker.py`

#### 异常处理器 (行 59-63)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 62 行: RepoBasicAuthHolder.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/controllers/gitee.py`

#### 异常处理器 (行 74-79)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 79 行 (1 行)

**Except 子句详情:**
- 第 76 行: exceptions.RemoteResourceNotFoundError, exceptions.AccessTokenForbidden (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 150-156)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 152 行: Exception (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/controllers/github.py`

#### 异常处理器 (行 74-79)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 79 行 (1 行)

**Except 子句详情:**
- 第 76 行: exceptions.RemoteResourceNotFoundError, exceptions.AccessTokenForbidden (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/controllers/gitlab.py`

#### 异常处理器 (行 48-55)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 50 行: GitlabGetError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0
- 第 54 行: GitlabAuthenticationError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 100-105)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 105 行 (1 行)

**Except 子句详情:**
- 第 102 行: exceptions.RemoteResourceNotFoundError, exceptions.AccessTokenForbidden (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 139-146)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 141 行: GitlabGetError (6 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 197-200)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 199 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/controllers/package.py`

#### 异常处理器 (行 61-64)

- **Try 块**: 2 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 64 行 (1 行)

**Except 子句详情:**

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/git/client.py`

#### 异常处理器 (行 196-200)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 198 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 231-235)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 233 行: GitCommandExecutionError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 339-343)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 341 行: subprocess.TimeoutExpired (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/gitlab/client.py`

#### 异常处理器 (行 65-68)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 67 行: GitlabGetError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/models.py`

#### 异常处理器 (行 203-207)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 205 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/package/cleaner.py`

#### 异常处理器 (行 37-45)

- **Try 块**: 4 行
- **Except 子句数量**: 1
- **Else 子句**: 第 45 行 (1 行)

**Except 子句详情:**
- 第 41 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/package/client.py`

#### 异常处理器 (行 98-101)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 100 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 108-117)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 112 行: tarfile.AbsoluteLinkError, tarfile.OutsideDestinationError, tarfile.LinkOutsideDestinationError (6 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 165-168)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 167 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 185-192)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 187 行: tarfile.AbsoluteLinkError, tarfile.OutsideDestinationError, tarfile.LinkOutsideDestinationError (6 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 262-265)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 264 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 343-347)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 345 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/package/uploader.py`

#### 异常处理器 (行 53-56)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 55 行: ObjectAlreadyExists (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/perm.py`

#### 异常处理器 (行 47-51)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 50 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/repo_controller.py`

#### 异常处理器 (行 134-137)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 136 行: UserProfile.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 140-144)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 143 行: PrivateTokenHolder.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 146-150)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 149 行: Oauth2TokenHolder.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/serializers.py`

#### 异常处理器 (行 58-62)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 61 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 67-73)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 72 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 77-81)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 80 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 181-189)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 189 行 (1 行)

**Except 子句详情:**
- 第 186 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/source_types.py`

#### 异常处理器 (行 265-270)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 269 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/svn/admin.py`

#### 异常处理器 (行 95-99)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 97 行: RuntimeError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 400-404)

- **Try 块**: 3 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 404 行 (1 行)

**Except 子句详情:**

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/svn/client.py`

#### 异常处理器 (行 120-123)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 122 行: AlreadyInitializedSvnRepo (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 138-146)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 143 行: SvnException (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 228-234)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 230 行: SvnException (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 374-377)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 376 行: SvnException (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 448-456)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 454 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 460-468)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 466 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 483-491)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 489 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/svn/server_config.py`

#### 异常处理器 (行 73-76)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 75 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/type_specs.py`

#### 异常处理器 (行 131-149)

- **Try 块**: 5 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 148 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/utils.py`

#### 异常处理器 (行 138-141)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 140 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 183-188)

- **Try 块**: 4 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 188 行 (1 行)

**Except 子句详情:**

---
#### 异常处理器 (行 197-202)

- **Try 块**: 4 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 202 行 (1 行)

**Except 子句详情:**

---

### 文件: `apiserver/paasng/paasng/platform/sourcectl/views.py`

#### 异常处理器 (行 220-240)

- **Try 块**: 2 行
- **Except 子句数量**: 3

**Except 子句详情:**
- 第 222 行: Oauth2TokenHolder.DoesNotExist (10 行)
  - 日志调用: debug=1, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0
- 第 232 行: AccessTokenForbidden (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 234 行: Exception (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 336-339)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 338 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 382-388)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 386 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 432-449)

- **Try 块**: 3 行
- **Except 子句数量**: 4
- **Else 子句**: 第 449 行 (1 行)

**Except 子句详情:**
- 第 439 行: UserNotBindedToSourceProviderError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 441 行: AccessTokenForbidden (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 443 行: SvnException (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 445 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 485-488)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 487 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 511-517)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 513 行: AccessTokenForbidden (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 515 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 541-547)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 545 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 565-568)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 567 行: NotImplementedError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 574-588)

- **Try 块**: 2 行
- **Except 子句数量**: 3
- **Else 子句**: 第 588 行 (1 行)

**Except 子句详情:**
- 第 576 行: UserNotBindedToSourceProviderError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 578 行: AccessTokenForbidden (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0
- 第 580 行: Exception (7 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/templates/manager.py`

#### 异常处理器 (行 41-49)

- **Try 块**: 6 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 47 行: ObjectDoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 84-88)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 87 行: Template.DoesNotExist, TmplRegionNotSupported (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/templates/templater.py`

#### 异常处理器 (行 53-58)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 58 行 (1 行)

**Except 子句详情:**
- 第 55 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/platform/templates/views.py`

#### 异常处理器 (行 54-58)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 57 行: ObjectDoesNotExist, TmplRegionNotSupported (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/settings/utils.py`

#### 异常处理器 (行 82-89)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 88 行: AttributeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/addons.py`

#### 异常处理器 (行 24-29)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 26 行: ImportError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 55-58)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 57 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/utils/api_middleware.py`

#### 异常处理器 (行 51-57)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 55 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 62-66)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 65 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 133-137)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 135 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/blobstore.py`

#### 异常处理器 (行 113-123)

- **Try 块**: 3 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 116 行: ClientError (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 122 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/configs.py`

#### 异常处理器 (行 35-38)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 37 行: TypeError, KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 55-60)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 57 行: KeyError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=1, break=0, continue=0

---
#### 异常处理器 (行 97-104)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 99 行: ValueError (6 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/datetime.py`

#### 异常处理器 (行 43-46)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 45 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 105-117)

- **Try 块**: 9 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 116 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 165-169)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 167 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/dictx.py`

#### 异常处理器 (行 37-40)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 39 行: KeyError, IndexError, TypeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/es_log/misc.py`

#### 异常处理器 (行 97-100)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 99 行: AttributeError, KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 104-107)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 106 行: TypeError (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 152-156)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 154 行: ValueError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/paasng/utils/es_log/time_range.py`

#### 异常处理器 (行 32-41)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 40 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/i18n/serializers.py`

#### 异常处理器 (行 180-186)

- **Try 块**: 4 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 185 行: KeyError, AttributeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 281-285)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 284 行: KeyError, AttributeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 291-299)

- **Try 块**: 7 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 299 行 (1 行)

**Except 子句详情:**

---

### 文件: `apiserver/paasng/paasng/utils/logging.py`

#### 异常处理器 (行 46-50)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 49 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/masked_curlify.py`

#### 异常处理器 (行 94-98)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 97 行: json.JSONDecodeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/middlewares.py`

#### 异常处理器 (行 87-91)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 89 行: LookupError (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/models.py`

#### 异常处理器 (行 420-424)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 423 行: AttributeError, ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/notification_plugins.py`

#### 异常处理器 (行 57-62)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 60 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/notifier.py`

#### 异常处理器 (行 64-67)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 66 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 85-90)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 88 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/serializers.py`

#### 异常处理器 (行 148-151)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 150 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 184-187)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 186 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 234-239)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 236 行: KeyError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 280-283)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 282 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 287-290)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 289 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/validators.py`

#### 异常处理器 (行 83-89)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 89 行 (1 行)

**Except 子句详情:**
- 第 85 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 95-98)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 97 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 179-182)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 181 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 194-197)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 196 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/paasng/utils/views.py`

#### 异常处理器 (行 40-44)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 42 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 142-148)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 147 行 (2 行)

**Except 子句详情:**
- 第 144 行: AttributeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/api/test_market.py`

#### 异常处理器 (行 157-160)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 159 行: AttributeError (2 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 161-164)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 163 行: AttributeError (2 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/conftest.py`

#### 异常处理器 (行 285-288)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 287 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 817-823)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 821 行: ModuleNotFoundError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/paas_wl/bk_app/monitoring/app_monitor/test_managers.py`

#### 异常处理器 (行 100-105)

- **Try 块**: 2 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 102 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 104 行: ApiException (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/paas_wl/conftest.py`

#### 异常处理器 (行 75-78)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 77 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 104-111)

- **Try 块**: 3 行
- **Except 子句数量**: 2

**Except 子句详情:**
- 第 107 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0
- 第 109 行: ApiException (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/paas_wl/e2e/ingress/utils.py`

#### 异常处理器 (行 159-165)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 161 行: ApiException (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=1

---

### 文件: `apiserver/paasng/tests/paas_wl/e2e/ingress/v0_21_0/conftest.py`

#### 异常处理器 (行 61-77)

- **Try 块**: 14 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 77 行 (1 行)

**Except 子句详情:**

---

### 文件: `apiserver/paasng/tests/paas_wl/e2e/ingress/v0_22_0/conftest.py`

#### 异常处理器 (行 61-77)

- **Try 块**: 14 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 77 行 (1 行)

**Except 子句详情:**

---

### 文件: `apiserver/paasng/tests/paas_wl/e2e/ingress/v1_0_0/conftest.py`

#### 异常处理器 (行 60-88)

- **Try 块**: 21 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 83 行 (6 行)

**Except 子句详情:**

---

### 文件: `apiserver/paasng/tests/paasng/accessories/publish/conftest.py`

#### 异常处理器 (行 33-43)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 41 行: TypeError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/paasng/accessories/publish/sync_market/test_sync_console.py`

#### 异常处理器 (行 77-80)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 79 行: NotImplementedError (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 98-101)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 100 行: NotImplementedError (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 118-121)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 120 行: NotImplementedError (2 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 132-135)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 134 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/paasng/platform/applications/test_lapp.py`

#### 异常处理器 (行 25-28)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 27 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/paasng/platform/engine/workflow/test_flow.py`

#### 异常处理器 (行 56-60)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 59 行: DeployShouldAbortError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 69-73)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 72 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/paasng/platform/mgrlegacy/conftest.py`

#### 异常处理器 (行 35-39)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 38 行: ValueError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `apiserver/paasng/tests/paasng/platform/mgrlegacy/test_envvar_migration.py`

#### 异常处理器 (行 27-30)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 29 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/paasng/platform/mgrlegacy/test_migration.py`

#### 异常处理器 (行 35-38)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 37 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/paasng/platform/mgrlegacy/utils.py`

#### 异常处理器 (行 36-39)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 38 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/paasng/test_utils/test_error_message.py`

#### 异常处理器 (行 46-49)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 48 行: DummyMsgError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 53-56)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 55 行: DummyMsgError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 60-63)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 62 行: DummyMsgError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 67-70)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 69 行: DummyMsgError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 84-87)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 86 行: DummyMsgError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/test_sqlalchemy_transaction.py`

#### 异常处理器 (行 26-29)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 28 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/utils/encrypt_cmd_base.py`

#### 异常处理器 (行 76-79)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 78 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/utils/helpers.py`

#### 异常处理器 (行 52-55)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 54 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 159-165)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 164 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 160-163)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 162 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 523-529)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 528 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 524-527)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 526 行: KeyError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `apiserver/paasng/tests/utils/mocks/cluster.py`

#### 异常处理器 (行 43-47)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 45 行: WlApp.DoesNotExist (3 行)
  - 日志调用: debug=0, info=0, warning=1, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `operator/scripts/update_helm_chart.py`

#### 异常处理器 (行 597-602)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 599 行: FileNotFoundError (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `svc-bkrepo/manage.py`

#### 异常处理器 (行 24-38)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 26 行: ImportError (13 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 30-33)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 32 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `svc-bkrepo/svc_bk_repo/monitoring/jobs.py`

#### 异常处理器 (行 51-65)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 65 行 (1 行)

**Except 子句详情:**
- 第 53 行: OSError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=2, raise=1, break=0, continue=0

---

### 文件: `svc-bkrepo/svc_bk_repo/vendor/helper.py`

#### 异常处理器 (行 35-38)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 37 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 40-44)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 42 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `svc-bkrepo/svc_bk_repo/vendor/provider.py`

#### 异常处理器 (行 70-74)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 72 行: RequestError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 77-81)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 79 行: RequestError (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `svc-bkrepo/svc_bk_repo/vendor/templatetags/tools.py`

#### 异常处理器 (行 27-32)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 29 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=1, break=0, continue=0

---

### 文件: `svc-bkrepo/svc_bk_repo/vendor/views.py`

#### 异常处理器 (行 104-121)

- **Try 块**: 2 行
- **Except 子句数量**: 4

**Except 子句详情:**
- 第 112 行: NoNeedToExtendQuota (3 行)
  - 日志调用: debug=0, info=1, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 115 行: ExtendQuotaMaxSizeExceeded (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 118 行: ExtendQuotaUsageTooLow (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0
- 第 120 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `svc-mysql/manage.py`

#### 异常处理器 (行 24-38)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 26 行: ImportError (13 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 30-33)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 32 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `svc-mysql/svc_mysql/vendor/helper.py`

#### 异常处理器 (行 81-92)

- **Try 块**: 4 行
- **Except 子句数量**: 1
- **Else 子句**: 第 90 行 (1 行)
- **Finally 子句**: 第 92 行 (1 行)

**Except 子句详情:**
- 第 85 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 98-105)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 100 行: DatabaseError (6 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=2, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---

### 文件: `svc-mysql/svc_mysql/vendor/tls.py`

#### 异常处理器 (行 54-57)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 56 行: FileNotFoundError, PermissionError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=1, return=0, raise=0, break=0, continue=0

---

### 文件: `svc-otel/manage.py`

#### 异常处理器 (行 24-38)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 26 行: ImportError (13 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 30-33)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 32 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `svc-otel/svc_otel/bkmonitorv3/client.py`

#### 异常处理器 (行 73-76)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 75 行: APIGatewayResponseError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `svc-rabbitmq/manage.py`

#### 异常处理器 (行 24-38)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 26 行: ImportError (13 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 30-33)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 32 行: ImportError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `svc-rabbitmq/svc_rabbitmq/utils.py`

#### 异常处理器 (行 28-31)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 30 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `svc-rabbitmq/tasks/__init__.py`

#### 异常处理器 (行 38-41)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 40 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `svc-rabbitmq/tasks/helper.py`

#### 异常处理器 (行 65-68)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 67 行: models.CronTask.DoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `svc-rabbitmq/tasks/monitor.py`

#### 异常处理器 (行 54-57)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 56 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 67-70)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 69 行: RuntimeError (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `svc-rabbitmq/tasks/scheduler.py`

#### 异常处理器 (行 93-99)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 96 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `svc-rabbitmq/tasks/tasks.py`

#### 异常处理器 (行 89-92)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 91 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 126-129)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 128 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 211-214)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 213 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---
#### 异常处理器 (行 239-242)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 241 行: ResourceNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 304-308)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 306 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---

### 文件: `svc-rabbitmq/vendor/client.py`

#### 异常处理器 (行 69-76)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 71 行: HTTPError (6 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=2, break=0, continue=0

---
#### 异常处理器 (行 294-298)

- **Try 块**: 3 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 298 行 (1 行)

**Except 子句详情:**

---

### 文件: `svc-rabbitmq/vendor/helper.py`

#### 异常处理器 (行 64-67)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 66 行: ObjectDoesNotExist (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---

### 文件: `svc-rabbitmq/vendor/management/commands/check_federation.py`

#### 异常处理器 (行 107-117)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 113 行: Exception (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `svc-rabbitmq/vendor/management/commands/consumer.py`

#### 异常处理器 (行 90-93)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 92 行: KeyboardInterrupt (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `svc-rabbitmq/vendor/management/commands/create_federation.py`

#### 异常处理器 (行 48-52)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 51 行: ResourceNotFound (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 121-135)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 131 行: Exception (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `svc-rabbitmq/vendor/management/commands/delete_federation.py`

#### 异常处理器 (行 43-54)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 50 行: Exception (5 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---

### 文件: `svc-rabbitmq/vendor/management/commands/evict_connections.py`

#### 异常处理器 (行 80-85)

- **Try 块**: 3 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 83 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 123-128)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 125 行: Exception (4 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 155-159)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 157 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=1

---
#### 异常处理器 (行 173-176)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 175 行: KeyboardInterrupt (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `svc-rabbitmq/vendor/management/commands/producer.py`

#### 异常处理器 (行 120-123)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 122 行: KeyboardInterrupt (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `svc-rabbitmq/vendor/management/commands/recovery_connections.py`

#### 异常处理器 (行 111-115)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 113 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=1, raise=0, break=0, continue=0

---
#### 异常处理器 (行 185-190)

- **Try 块**: 2 行
- **Except 子句数量**: 1
- **Else 子句**: 第 190 行 (1 行)

**Except 子句详情:**
- 第 187 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `svc-rabbitmq/vendor/management/commands/recovery_instances.py`

#### 异常处理器 (行 85-88)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 87 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=0, break=0, continue=0

---

### 文件: `svc-rabbitmq/vendor/models.py`

#### 异常处理器 (行 196-200)

- **Try 块**: 2 行
- **Except 子句数量**: 0
- **Finally 子句**: 第 199 行 (2 行)

**Except 子句详情:**

---

### 文件: `svc-rabbitmq/vendor/provider.py`

#### 异常处理器 (行 178-181)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 180 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 186-189)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 188 行: Exception (2 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=0, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 267-271)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 269 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
#### 异常处理器 (行 312-316)

- **Try 块**: 2 行
- **Except 子句数量**: 1

**Except 子句详情:**
- 第 314 行: Exception (3 行)
  - 日志调用: debug=0, info=0, warning=0, error=0, exception=1, critical=0
  - 控制流: pass=0, return=0, raise=1, break=0, continue=0

---
