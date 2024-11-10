# p-ast

[![Release](https://img.shields.io/github/v/release/mrlyc/p-ast)](https://img.shields.io/github/v/release/mrlyc/p-ast)
[![Build status](https://img.shields.io/github/actions/workflow/status/mrlyc/p-ast/main.yml?branch=main)](https://github.com/mrlyc/p-ast/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/mrlyc/p-ast/branch/main/graph/badge.svg)](https://codecov.io/gh/mrlyc/p-ast)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mrlyc/p-ast)](https://img.shields.io/github/commit-activity/m/mrlyc/p-ast)
[![License](https://img.shields.io/github/license/mrlyc/p-ast)](https://img.shields.io/github/license/mrlyc/p-ast)

This project provides a series of tools to analyze Python projects. It does not actually execute code but only uses
static analysis methods. Therefore, it has a more universal application scenario.

- **Github repository**: <https://github.com/mrlyc/p-ast/>
- **Documentation** <https://mrlyc.github.io/p-ast/>

## Installation

```bash
pip install p-ast
```

## Usage

### find-env-vars

Infer the environment variables that a program depends on through code, including information such as default values and
types.

```bash
p-ast find-env-vars /path/to/your/python/project/**/*.py
```

The `-o` option can be used to output a csv file for further analysis.

```bash
p-ast find-env-vars /path/to/your/python/project/**/*.py -o env-vars.csv
```