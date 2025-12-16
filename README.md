# upcast

[![Release](https://img.shields.io/github/v/release/mrlyc/upcast)](https://img.shields.io/github/v/release/mrlyc/upcast)
[![Build status](https://img.shields.io/github/actions/workflow/status/mrlyc/upcast/main.yml?branch=main)](https://github.com/mrlyc/upcast/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/mrlyc/upcast/branch/main/graph/badge.svg)](https://codecov.io/gh/mrlyc/upcast)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mrlyc/upcast)](https://img.shields.io/github/commit-activity/m/mrlyc/upcast)
[![License](https://img.shields.io/github/license/mrlyc/upcast)](https://img.shields.io/github/license/mrlyc/upcast)

This project provides a series of tools to analyze Python projects. It does not actually execute code but only uses
static analysis methods. Therefore, it has a more universal application scenario.

- **Github repository**: <https://github.com/mrlyc/upcast/>
- **Documentation** <https://mrlyc.github.io/upcast/>

## Installation

```bash
pip install upcast
```

## Usage

### analyze-django-models

Analyze Django models in Python files and export structured information to YAML format. This command uses astroid for accurate type inference and supports abstract model inheritance, relationship fields, and Meta class options.

```bash
upcast analyze-django-models /path/to/django/project/
```

Output to a file:

```bash
upcast analyze-django-models /path/to/django/project/ -o models.yaml
```

Enable verbose output:

```bash
upcast analyze-django-models /path/to/django/project/ -o models.yaml --verbose
```

**Output Format:**

The command generates YAML output with the following structure:

```yaml
app.models.Author:
  module: app.models
  abstract: false
  meta:
    db_table: authors
    unique_together:
      - - first_name
        - last_name
  fields:
    first_name:
      type: CharField
      max_length: 100
    last_name:
      type: CharField
      max_length: 100
    email:
      type: EmailField
      unique: true
  relationships:
    books:
      type: ForeignKey
      to: app.models.Book
      related_name: author_books
```

**Features:**

- **Accurate Model Detection**: Uses astroid for type inference to detect Django models
- **Abstract Inheritance**: Automatically merges fields from abstract parent models
- **Relationship Fields**: Detects ForeignKey, OneToOneField, and ManyToManyField
- **Meta Class Options**: Extracts db_table, abstract, ordering, and other Meta options
- **YAML Output**: Human-readable structured output format

### find-env-vars

Infer the environment variables that a program depends on through code, including information such as default values and
types.

```bash
upcast find-env-vars /path/to/your/python/project/**/*.py
```

The `-o` option can be used to output a csv file for further analysis.

```bash
upcast find-env-vars /path/to/your/python/project/**/*.py -o env-vars.csv
```

Support the following output formats:

- csv
- html
