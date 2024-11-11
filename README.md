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