# Markdown Examples

This directory contains example markdown renderings of scanner outputs using the upcast render module.

## Overview

The render module (`upcast.render`) provides functionality to convert scanner outputs into readable markdown format with multi-language support.

## Available Examples

### English Examples (en)

- `http-requests-en.md` - HTTP request analysis
- `django-models-en.md` - Django model structure analysis
- `env-vars-en.md` - Environment variable usage
- `signals-en.md` - Django/Celery signal usage
- `complexity-patterns-en.md` - Code complexity analysis

### Chinese Examples (zh)

- `http-requests-zh.md` - HTTP 请求分析
- `django-models-zh.md` - Django 模型结构分析
- `env-vars-zh.md` - 环境变量使用
- `signals-zh.md` - Django/Celery 信号使用
- `complexity-patterns-zh.md` - 代码复杂度分析

## Usage

To generate markdown from scanner output:

```python
from upcast.models.http_requests import HttpRequestOutput
from upcast.render import render_to_markdown, render_to_file

# Create or load scanner output
output = HttpRequestOutput(...)

# Render to string
markdown = render_to_markdown(output, language='en', title='HTTP Requests')

# Or render directly to file
render_to_file(output, 'output.md', language='en', title='HTTP Requests')
```

## Supported Languages

- `en` - English
- `zh` - Chinese (Simplified)

## Template Structure

Templates are organized in `upcast/templates/{language}/`:

- `base.md.jinja2` - Base template for all scanner outputs
- `http_requests.md.jinja2` - Template for HTTP request analysis
- `django_models.md.jinja2` - Template for Django models
- `complexity.md.jinja2` - Template for complexity analysis
- `env_vars.md.jinja2` - Template for environment variables
- `signals.md.jinja2` - Template for signal analysis

## Features

- **Multi-language support**: Templates available in English and Chinese
- **Structured output**: Consistent structure with metadata, summary, and detailed results
- **Readable tables**: Field details presented in markdown tables
- **Modular design**: Each scanner type has its own template
- **Extensible**: Easy to add new templates for additional languages or scanner types
