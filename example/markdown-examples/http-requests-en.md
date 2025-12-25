# HTTP Requests Analysis

## Metadata
No metadata available.

## Summary
- **Total Count**: 56
- **Files Scanned**: 14
- **Scan Duration**: 10248 ms

- **Total Requests**: 56
- **Unique URLs**: 8

### Requests by Library
- **requests**: 56 requests

## Results

### ...

**Primary Method**: GET  
**Primary Library**: requests

#### Request Details

| File | Line | Method | Statement | Async | Session-Based | Timeout |
|------|------|--------|-----------|-------|---------------|---------|
| apiserver/paasng/paasng/accessories/cloudapi/components/http.py | 38 | REQUEST | `requests.request(method, url, **kwargs)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/dev_sandbox/management/commands/renew_dev_sandbox_expired_at.py | 56 | GET | `requests.get(url)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/paas_analysis/clients.py | 118 | GET | `requests.get(self.base_url + url, auth=self.auth)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/paas_analysis/clients.py | 128 | GET | `requests.get(self.base_url + url, params={'start_time': start_time.isoformat(), 'end_time': end_time.isoformat()}, auth=self.auth)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/paas_analysis/clients.py | 160 | GET | `requests.get(self.base_url + url, params=params, auth=self.auth)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/paas_analysis/clients.py | 185 | GET | `requests.get(self.base_url + url, params=params, auth=self.auth)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/paas_analysis/clients.py | 202 | GET | `requests.get(self.base_url + url, auth=self.auth)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/paas_analysis/clients.py | 212 | GET | `requests.get(self.base_url + url, params={'start_time': start_time.isoformat(), 'end_time': end_time.isoformat()}, auth=self.auth)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/paas_analysis/clients.py | 240 | GET | `requests.get(self.base_url + url, params=params, auth=self.auth)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/paas_analysis/clients.py | 271 | GET | `requests.get(self.base_url + url, params=params, auth=self.auth)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/paas_analysis/clients.py | 296 | GET | `requests.get(self.base_url + url, params=params, auth=self.auth)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 140 | GET | `requests.get(self.config.meta_info_url, auth=self.auth, timeout=self.REQUEST_LIST_TIMEOUT)` | No | No | 15 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 151 | GET | `requests.get(self.config.index_url, auth=self.auth, timeout=self.REQUEST_LIST_TIMEOUT)` | No | No | 15 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 162 | PUT | `requests.put(self.config.create_service_url, json=data, auth=self.auth, timeout=self.REQUEST_CREATE_TIMEOUT)` | No | No | 300 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 175 | PUT | `requests.put(url, json=data, auth=self.auth, timeout=self.REQUEST_CREATE_TIMEOUT)` | No | No | 300 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 187 | POST | `requests.post(url, json=data, auth=self.auth, timeout=self.REQUEST_CREATE_TIMEOUT)` | No | No | 300 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 199 | PUT | `requests.put(url, json=data, auth=self.auth, timeout=self.REQUEST_CREATE_TIMEOUT)` | No | No | 300 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 211 | POST | `requests.post(url, json=payload, auth=self.auth, timeout=self.REQUEST_CREATE_TIMEOUT)` | No | No | 300 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 223 | GET | `requests.get(url, auth=self.auth, timeout=self.REQUEST_LIST_TIMEOUT)` | No | No | 15 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 235 | GET | `requests.get(url, auth=self.auth, timeout=self.REQUEST_LIST_TIMEOUT)` | No | No | 15 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 250 | DELETE | `requests.delete(url, auth=self.auth, timeout=self.REQUEST_DELETE_TIMEOUT)` | No | No | 30 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 261 | PUT | `requests.put(url, json=config, auth=self.auth, timeout=self.REQUEST_CREATE_TIMEOUT)` | No | No | 300 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 268 | POST | `requests.post(url, json=params, auth=self.auth, timeout=self.REQUEST_CREATE_TIMEOUT)` | No | No | 300 |
| apiserver/paasng/paasng/accessories/servicehub/remote/client.py | 275 | DELETE | `requests.delete(url, auth=self.auth, timeout=self.REQUEST_DELETE_TIMEOUT)` | No | No | 30 |
| apiserver/paasng/paasng/accessories/services/providers/rabbitmq/provider.py | 64 | PUT | `requests.put(url=url, headers=self.headers, auth=self.auth, json=json)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/services/providers/rabbitmq/provider.py | 69 | DELETE | `requests.delete(url=url, headers=self.headers, auth=self.auth, json=json)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/services/providers/rabbitmq/provider.py | 73 | GET | `requests.get(url=url, headers=self.headers, auth=self.auth, json=json)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/services/providers/sentry/client.py | 39 | GET | `requests.get(url=url, headers=headers, params=data, timeout=timeout)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/services/providers/sentry/client.py | 41 | HEAD | `requests.head(url=url, headers=headers, timeout=timeout)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/services/providers/sentry/client.py | 43 | POST | `requests.post(url=url, headers=headers, json=data, timeout=timeout)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/services/providers/sentry/client.py | 45 | DELETE | `requests.delete(url=url, headers=headers, json=data)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/services/providers/sentry/client.py | 47 | PUT | `requests.put(url=url, headers=headers, json=data)` | No | No | N/A |
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 240 | POST | `requests.post(url=self.auth_url, json=dict(app_code=self.app_code, app_secret=self.app_secret, env_name=self.env_name, grant_type='authorization_code', rtx=username, **{self.COOKIE_KEY: user_credential}), headers=self.app_info_headers)` | No | No | N/A |
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 261 | POST | `requests.post(url=self.refresh_url, params=dict(app_code=self.app_code, env_name=self.env_name, grant_type='refresh_token', refresh_token=refresh_token), headers=self.app_info_headers)` | No | No | N/A |
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 278 | GET | `requests.get(url=self.validate_url, json={'access_token': access_token}, headers=self.app_info_headers)` | No | No | N/A |
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 295 | POST | `requests.post(url=self.auth_url, json=dict(app_code=self.app_code, app_secret=self.app_secret, env_name=self.env_name, grant_type='authorization_code', id_provider='bk_login', **{self.COOKIE_KEY: user_credential}), headers=self.app_info_headers)` | No | No | N/A |
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 316 | POST | `requests.post(url=self.refresh_url, json=dict(app_code=self.app_code, env_name=self.env_name, grant_type='refresh_token', refresh_token=refresh_token), headers=self.app_info_headers)` | No | No | N/A |
| apiserver/paasng/paasng/infras/accounts/oauth/backends.py | 333 | POST | `requests.post(url=self.validate_url, json={'access_token': access_token}, headers=self.app_info_headers)` | No | No | N/A |
| apiserver/paasng/paasng/misc/monitoring/metrics/clients/prometheus.py | 100 | REQUEST | `requests.request(method, url, **kwargs)` | No | No | N/A |
| apiserver/paasng/paasng/misc/search/backends.py | 83 | GET | `requests.get(self.BKDOC_SEARCH_BASE_URL.format(keyword))` | No | No | N/A |
| apiserver/paasng/paasng/platform/mgrlegacy/legacy_proxy.py | 147 | GET | `requests.get(logo_url, stream=True)` | No | No | N/A |
| apiserver/paasng/paasng/platform/mgrlegacy/legacy_proxy.py | 156 | GET | `requests.get(settings.APPLICATION_DEFAULT_LOGO, stream=True)` | No | No | N/A |
| apiserver/paasng/paasng/platform/sourcectl/package/downloader.py | 33 | GET | `requests.get(target_url, stream=True)` | No | No | N/A |
| apiserver/paasng/paasng/platform/sourcectl/svn/admin.py | 105 | GET | `requests.get(url, params=params, timeout=self.TIMEOUT, verify=self.SSL_VERIFY, **kwargs)` | No | No | 60 |



### .../api/overview

**Primary Method**: GET  
**Primary Library**: requests

#### Request Details

| File | Line | Method | Statement | Async | Session-Based | Timeout |
|------|------|--------|-----------|-------|---------------|---------|
| apiserver/paasng/paasng/accessories/services/providers/rabbitmq/provider.py | 54 | GET | `requests.get(url, auth=self.auth)` | No | No | N/A |



### .../api/v1/apps

**Primary Method**: POST  
**Primary Library**: requests

#### Request Details

| File | Line | Method | Statement | Async | Session-Based | Timeout |
|------|------|--------|-----------|-------|---------------|---------|
| apiserver/paasng/paasng/infras/oauth2/api.py | 101 | POST | `requests.post(url, json=data, headers=self.headers)` | No | No | N/A |



### .../api/v1/apps/.../access-keys

**Primary Method**: POST  
**Primary Library**: requests

#### Request Details

| File | Line | Method | Statement | Async | Session-Based | Timeout |
|------|------|--------|-----------|-------|---------------|---------|
| apiserver/paasng/paasng/infras/oauth2/api.py | 114 | POST | `requests.post(url, headers=self.headers)` | No | No | N/A |
| apiserver/paasng/paasng/infras/oauth2/api.py | 139 | GET | `requests.get(url, headers=self.headers)` | No | No | N/A |



### .../api/v1/apps/.../access-keys/...

**Primary Method**: DELETE  
**Primary Library**: requests

#### Request Details

| File | Line | Method | Statement | Async | Session-Based | Timeout |
|------|------|--------|-----------|-------|---------------|---------|
| apiserver/paasng/paasng/infras/oauth2/api.py | 122 | DELETE | `requests.delete(url, headers=self.headers)` | No | No | N/A |
| apiserver/paasng/paasng/infras/oauth2/api.py | 131 | PUT | `requests.put(url, json=data, headers=self.headers)` | No | No | N/A |



### .../sites/register

**Primary Method**: POST  
**Primary Library**: requests

#### Request Details

| File | Line | Method | Statement | Async | Session-Based | Timeout |
|------|------|--------|-----------|-------|---------------|---------|
| apiserver/paasng/paasng/accessories/paas_analysis/clients.py | 82 | POST | `requests.post(self.base_url + url, json={'site_type': 'app', 'extra_info': {'paas_app_code': app_code, 'module_name': module_name, 'environment': env}}, auth=self.auth)` | No | No | N/A |
| apiserver/paasng/paasng/accessories/paas_analysis/clients.py | 102 | POST | `requests.post(self.base_url + url, json={'site_type': 'custom', 'extra_info': {'site_name': site_name}}, auth=self.auth)` | No | No | N/A |



### https://example.com/api

**Primary Method**: POST  
**Primary Library**: requests

#### Request Details

| File | Line | Method | Statement | Async | Session-Based | Timeout |
|------|------|--------|-----------|-------|---------------|---------|
| apiserver/paasng/tests/paasng/test_utils/test_masked_curlify.py | 37 | POST | `Request('POST', 'https://example.com/api', json={'BK_PASSWORD': '123456', 'api_key': 'abcdef'})` | No | No | N/A |
| apiserver/paasng/tests/paasng/test_utils/test_masked_curlify.py | 47 | POST | `Request('POST', 'https://example.com/api', data={'BK_PASSWORD': '123456', 'api_key': 'abcdef'})` | No | No | N/A |
| apiserver/paasng/tests/paasng/test_utils/test_masked_curlify.py | 57 | POST | `Request('POST', 'https://example.com/api', headers={'BK_PASSWORD': '123456', 'api_key': 'abcdef'})` | No | No | N/A |

#### Additional Parameters
**JSON Body** (Line 37):
```
{'BK_PASSWORD': '123456', 'api_key': 'abcdef'}
```
**Form Data** (Line 47):
```
{'BK_PASSWORD': '123456', 'api_key': 'abcdef'}
```
**Headers** (Line 57):
```
{'BK_PASSWORD': '123456', 'api_key': 'abcdef'}
```


### https://example.com/api?BK_PASSWORD=123456&api_key=abcdef

**Primary Method**: GET  
**Primary Library**: requests

#### Request Details

| File | Line | Method | Statement | Async | Session-Based | Timeout |
|------|------|--------|-----------|-------|---------------|---------|
| apiserver/paasng/tests/paasng/test_utils/test_masked_curlify.py | 28 | GET | `Request('GET', 'https://example.com/api?BK_PASSWORD=123456&api_key=abcdef')` | No | No | N/A |


