# Reimplement Environment Variable Scanner with Astroid

## Why

The current `env_var` module uses `ast-grep-py` for parsing, which provides pattern-based matching but lacks the semantic understanding needed for:

1. **Type inference**: Cannot reliably infer types from default values or determine variable types through semantic analysis
2. **Variable resolution**: Limited ability to resolve concatenated environment variable names (e.g., `PREFIX + 'KEY'`)
3. **Context tracking**: Difficult to maintain scope and import context across complex codebases
4. **Code duplication**: Much of the scanning logic duplicates what `django_model_scanner` already does with astroid

By rewriting `env_var` to use `astroid` (like `django_model_scanner`), we gain:

- **Better type inference**: Leverage astroid's type inference to determine types from default values
- **Consistent architecture**: Both scanners share the same AST analysis approach
- **Improved accuracy**: Better handling of aliased imports, concatenated strings, and complex expressions
- **Maintainability**: Single AST library to maintain and understand

## What Changes

**Core Architecture**:

- Replace `ast-grep-py` with `astroid` for AST analysis
- Create `upcast/env_var_scanner/` module following `django_model_scanner` patterns
- Implement visitor pattern for environment variable detection
- Use astroid's type inference for default value analysis

**Output Format**:

- Aggregate results by environment variable name (not by location)
- For each environment variable, output:
  - **Name**: The environment variable name
  - **Types**: List of inferred types (from casts or default values)
  - **Default values**: List of all default values found (as literals)
  - **Locations**: List of file paths and line numbers where used
  - **Statements**: List of code statements that reference this variable
  - **Required**: Boolean indicating if any usage requires the variable

**Supported Patterns**:

- Standard library: `os.getenv()`, `os.environ[]`, `os.environ.get()`
- Django-environ: `env()`, `env.str()`, `env.int()`, etc.
- Custom patterns via configuration

## Impact

- **Affected specs**: Creates new `env-var-scanner` spec
- **Affected code**:
  - New module: `upcast/env_var_scanner/` (similar to `django_model_scanner/`)
  - Updated: `upcast/main.py` CLI command
  - Deprecated (but maintained): `upcast/env_var/` (old implementation)
- **Breaking change**: Output format changes from location-based to variable-aggregated
- **User impact**:
  - Users get more useful aggregated output
  - Old `find_env_vars` command maintained for backward compatibility
  - New `scan-env-vars` command uses new implementation
