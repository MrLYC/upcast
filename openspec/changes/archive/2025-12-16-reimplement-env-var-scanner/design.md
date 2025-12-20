# Design: Reimplement Environment Variable Scanner with Astroid

## Architecture Overview

```
upcast/env_var_scanner/
├── __init__.py           # Public API exports
├── ast_utils.py          # AST helper functions (like django_model_scanner)
├── env_var_parser.py     # Core parsing logic for env var patterns
├── checker.py            # Visitor pattern implementation
├── cli.py                # File scanning and orchestration
└── export.py             # YAML/JSON output formatting
```

## Key Design Decisions

### 1. Why Astroid?

**Chosen**: Use `astroid` for AST analysis

**Rationale**:

- **Type inference**: Astroid provides semantic analysis to infer types from default values
- **Import resolution**: Better handling of aliased imports and complex module structures
- **Consistency**: Same library as `django_model_scanner`, reducing learning curve
- **Expression evaluation**: Can evaluate constant expressions for variable name resolution

**Trade-offs**:

- **Learning curve**: More complex than ast-grep patterns
- **Performance**: Slightly slower than ast-grep for simple patterns
- **Benefit**: More accurate and maintainable long-term

### 2. Aggregation Strategy

**Chosen**: Aggregate by environment variable name (not by location)

**Rationale**:

- **User value**: Developers care about "what environment variables exist" not "where they're used"
- **Duplication removal**: Same variable used multiple times appears once
- **Type collection**: Can show all types a variable is used as
- **Default collection**: Can show all default values across codebase

**Example Output**:

```yaml
DATABASE_URL:
  types: [str]
  defaults: ["postgresql://localhost/db"]
  usages:
    - location: "config/settings.py:15"
      statement: "os.getenv('DATABASE_URL', 'postgresql://localhost/db')"
      type: str
      default: "postgresql://localhost/db"
      required: false
    - location: "config/database.py:8"
      statement: "env.str('DATABASE_URL')"
      type: str
      default: null
      required: true
  required: true # true if ANY usage is required

API_KEY:
  types: []
  defaults: []
  usages:
    - location: "api/client.py:23"
      statement: "os.environ['API_KEY']"
      type: null
      default: null
      required: true
  required: true
```

**Required Flag Logic**:

- **Variable level**: `required: true` if **ANY** usage has no default value
- **Usage level**: `required: true` for patterns without defaults:
  - `os.environ['KEY']` → required (no default, raises KeyError)
  - `env('KEY')` without default → required
  - `os.getenv('KEY')` → not required (implicit None default)
  - Any pattern with explicit default → not required

**Alternative Considered**: Location-based output (current implementation)

- **Rejected**: Less useful for configuration management, more duplication

### 3. Type Inference Strategy

**Chosen**: Multi-source type inference with priority

**Sources** (in priority order):

1. **Explicit type conversions**: `int(os.getenv(...))` → `int`
2. **Django-environ typed methods**: `env.bool(...)` → `bool`, `env.int(...)` → `int`
3. **Default value type inference**: `env('DEBUG') or False` → `bool`, `os.getenv('X', 123)` → `int`
4. **Fallback to string**: `os.getenv('X')` → `str` (default type when no conversion or default)

**Type Inference Rules**:

- **Explicit casts have highest priority**: Wrapper functions like `int()`, `float()`, `bool()`, `str()`
- **Method names indicate type**: Django-environ's `env.int()`, `env.bool()`, `env.str()`, etc.
- **Default value literal types**: Infer from the literal type of the default value
- **`or` expressions**: `env('X') or False` infers type from the right operand
- **No information**: Default to `str` for standard library getenv patterns

**Rationale**:

- **Accuracy**: Explicit type conversions are most reliable intent signals
- **Coverage**: Default values provide type hints when no cast exists
- **Flexibility**: List of types handles mixed usage patterns across the codebase

**Examples**:

```python
# Example 1: Explicit type conversion
max_connections = int(os.getenv('MAX_CONN', '10'))  # type: int

# Example 2: No conversion, default to str
database_url = os.getenv('DATABASE_URL')  # type: str

# Example 3: Type inference from default value
debug = env('DEBUG') or False  # type: bool

# Example 4: Mixed usage
# Usage 1: int(os.getenv('PORT', '8000')) → type: int
# Usage 2: os.getenv('PORT', '8000') → type: str
# Result: types = ['int', 'str']
```

### 4. Visitor Pattern Implementation

**Chosen**: Single-pass visitor with context tracking

```python
class EnvVarChecker:
    def __init__(self):
        self.env_vars = {}  # Aggregated by name

    def visit_call(self, node):
        if self.is_env_var_call(node):
            usage = self.parse_env_var_usage(node)
            self.aggregate_usage(usage)
```

**Rationale**:

- **Efficiency**: Single pass through AST
- **Context**: Can track imports and scope
- **Extensibility**: Easy to add new patterns

**Alternative Considered**: Multi-pass (one per pattern)

- **Rejected**: Less efficient, harder to maintain

### 5. Pattern Detection Architecture

**Chosen**: Pattern registry with priority

```python
PATTERNS = [
    # Priority 1: Required patterns (no default)
    Pattern("os.environ[{name}]", required=True, type_source="none"),

    # Priority 2: Standard library with defaults
    Pattern("os.getenv({name}, {default})", required=False, type_source="default"),

    # Priority 3: Django-environ with types
    Pattern("env.{type}({name})", required=True, type_source="method"),
]
```

**Rationale**:

- **Extensibility**: Easy to add custom patterns
- **Configuration**: Patterns can be user-configurable
- **Clarity**: Explicit pattern definitions vs. scattered logic

### 6. Default Value Extraction

**Chosen**: Astroid literal inference with fallback

**Strategy**:

1. Try `astroid.infer()` to evaluate constant expressions
2. Fall back to `.as_string()` for unevaluated expressions
3. Store as literal strings in output

**Rationale**:

- **Accuracy**: Resolves concatenated strings, constants
- **Safety**: Doesn't execute arbitrary code
- **Readability**: Preserves quotes and formatting

**Example**:

```python
# Code:
PREFIX = "DB_"
url = os.getenv(PREFIX + "URL", "postgresql://localhost")

# Inference:
# - Variable name: Resolves to "DB_URL"
# - Default value: Stored as '"postgresql://localhost"'
```

### 7. Error Handling Strategy

**Chosen**: Fail-safe with warnings

**Approach**:

- Continue scanning on parsing errors
- Log warnings for unresolved patterns
- Include partial results in output
- Report errors to stderr with `-v` flag

**Rationale**:

- **Robustness**: Don't fail entire scan for one bad file
- **Completeness**: Get as much info as possible
- **Debugging**: Verbose mode helps diagnose issues

## Integration with django_model_scanner

### Shared Utilities

Potential shared module: `upcast/ast_common/`

- `infer_literal_value()` - Extract literal values
- `safe_as_string()` - Safe AST to string conversion
- `resolve_import()` - Import resolution logic

**Decision**: Keep separate for now, consider extraction later

- **Rationale**: Avoid premature optimization, patterns may diverge

### Consistent Patterns

Both scanners follow:

1. **Module structure**: `ast_utils`, `parser`, `checker`, `cli`, `export`
2. **Visitor pattern**: Single-pass AST traversal
3. **YAML output**: Consistent formatting and style
4. **CLI interface**: Similar flags and options

## Performance Considerations

### Optimization Strategies

1. **Lazy imports**: Only import astroid when needed
2. **File filtering**: Skip non-Python files early
3. **Parallel scanning**: Future enhancement for large projects
4. **Caching**: Consider caching parsed ASTs for repeated scans

### Expected Performance

- **Small projects** (< 100 files): < 1 second
- **Medium projects** (100-1000 files): 1-5 seconds
- **Large projects** (> 1000 files): 5-30 seconds

**Benchmark**: Should be comparable to `django_model_scanner`

## Testing Strategy

### Unit Tests

- **AST utilities**: Test each helper function in isolation
- **Pattern detection**: Test each pattern with various inputs
- **Type inference**: Test inference from different sources
- **Aggregation**: Test merging multiple usages

### Integration Tests

- **Real codebases**: Test on actual Python projects
- **Edge cases**: Missing imports, syntax errors, dynamic code
- **Output format**: Verify YAML structure and content

### Test Fixtures

```python
# tests/fixtures/env_vars/
simple.py         # Basic os.getenv patterns
django_env.py     # Django-environ patterns
complex.py        # Mixed patterns, type inference
errors.py         # Syntax errors, edge cases
```

## Migration Path

### Phase 1: New Implementation

- Create `env_var_scanner` alongside old `env_var`
- New CLI command: `scan-env-vars`
- Old command still works

### Phase 2: Deprecation (Future Release)

- Add deprecation warning to `find_env_vars`
- Update documentation to recommend `scan-env-vars`

### Phase 3: Removal (Major Version Bump)

- Remove old `env_var` module
- Remove `find_env_vars` command

## Open Questions

1. **Output format**: YAML vs JSON vs both?

   - **Recommendation**: Support both, YAML as default

2. **Config file**: Support `.upcast.yml` for pattern configuration?

   - **Recommendation**: Start simple, add if needed

3. **IDE integration**: VSCode extension for env var highlighting?

   - **Recommendation**: Future enhancement, out of scope

4. **Type annotations**: Should we output Python type hints?
   - **Recommendation**: Yes, as comments in YAML output
