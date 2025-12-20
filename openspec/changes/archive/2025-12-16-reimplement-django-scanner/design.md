# Design Document: Django Model Scanner Reimplementation

## Context

The current implementation in `upcast/django_model/` uses ast-grep-py (605 lines total) for Django model analysis. While functional, it has limitations in accuracy and completeness.

The reference implementation in `django-model-scanner` uses Pylint's astroid library (1623 lines total) and provides:

- More accurate type inference for model detection
- Complete handling of abstract model inheritance
- Full relationship field parsing
- Meta class option extraction
- Better error handling and edge case coverage

**Current Stack:**

- ast-grep-py for AST pattern matching
- Custom plugin architecture
- JSON output format
- Limited field type and option extraction

**Target Stack:**

- astroid for semantic AST analysis
- Pylint checker architecture
- YAML output format
- Complete field, relationship, and Meta parsing

## Goals / Non-Goals

**Goals:**

- Accurate Django model detection through type inference
- Complete abstract model inheritance merging
- Full support for all Django field types and relationships
- Extract all Meta class options (db_table, abstract, indexes, etc.)
- Structured YAML output format
- Better error messages and edge case handling
- Maintain command-line interface simplicity

**Non-Goals:**

- Maintaining backward compatibility with existing output format
- Supporting non-Django Python models
- Runtime code execution or Django app loading
- Database schema introspection
- Migration file generation

## Decisions

### AST Library: astroid vs ast-grep-py

**Decision:** Use astroid for AST analysis.

**Rationale:**

- **Type Inference**: astroid can infer types through imports, crucial for detecting `models.Model` inheritance
- **Semantic Analysis**: Understands Python semantics beyond pattern matching
- **Proven Track Record**: Used by pylint, widely tested and maintained
- **Better Edge Cases**: Handles aliased imports, nested inheritance, dynamic bases

**Trade-offs:**

- ast-grep-py is faster but less accurate
- astroid adds ~5MB dependency
- astroid requires more complex code but provides better results

**Alternative Considered:**

- Continue with ast-grep-py: Would require complex heuristics that astroid provides out-of-box

### Architecture: Pylint Checker vs Standalone

**Decision:** Use Pylint checker architecture as the core, but provide standalone CLI.

**Rationale:**

- Pylint's visitor pattern is well-suited for AST traversal
- Can reuse checker in both standalone and pylint contexts
- Clear separation: detection → parsing → export
- Easier testing with isolated components

**Implementation:**

```python
# Core components
ast_utils.py      # Django model detection helpers
model_parser.py   # Field and relationship parsing
checker.py        # Pylint checker (visits AST)
export.py         # YAML formatting and output
main.py           # CLI wrapper
```

### Output Format: YAML vs JSON

**Decision:** Use YAML for structured output.

**Rationale:**

- More human-readable for manual inspection
- Better for documenting model schemas
- Supports comments (useful for documentation)
- Natural representation of nested structures
- Industry standard for config/schema files

**Output Structure:**

```yaml
app.models.User:
  module: app.models
  abstract: false
  table: auth_user
  fields:
    username:
      type: CharField
      max_length: 150
      unique: true
  relationships:
    groups:
      type: ManyToManyField
      to: auth.Group
      related_name: users
```

### Inheritance Handling: Two-Pass vs Single-Pass

**Decision:** Use two-pass processing.

**Rationale:**

- **Pass 1**: Parse all models independently
- **Pass 2**: Merge abstract model fields into concrete models

**Benefits:**

- Handles forward references (abstract model defined after concrete)
- Cleaner code separation
- Easier to debug inheritance issues

**Algorithm:**

```python
# Pass 1: Visit all ClassDef nodes
for class_node in ast:
    if is_django_model(class_node):
        model_data = parse_model(class_node)
        models[qname] = model_data

# Pass 2: Merge abstract inheritance
for model in models.values():
    merge_abstract_fields(model, models)
```

### Field Detection: Pattern Matching vs Type Checking

**Decision:** Combine both approaches.

**Rationale:**

- Use astroid type inference first (accurate)
- Fall back to pattern matching for edge cases
- Check for `models.Field` in ancestors

**Detection Logic:**

```python
def is_django_field(node):
    # 1. Try type inference
    for inferred in node.value.infer():
        if 'django.db.models.fields' in inferred.qname():
            return True

    # 2. Fall back to pattern matching
    if node.value.as_string().endswith('Field'):
        return True

    return False
```

### Meta Class Parsing: Literal Evaluation vs AST Walking

**Decision:** Use safe literal evaluation with ast.literal_eval.

**Rationale:**

- Safely evaluates simple Python literals (strings, numbers, lists, tuples, dicts)
- Avoids code execution security issues
- Handles most Meta class patterns (db_table, ordering, indexes)
- Falls back to string representation for complex values (like models.Index)

**Example:**

```python
def get_meta_option(meta_node, option_name):
    assign = find_assignment(meta_node, option_name)
    try:
        return ast.literal_eval(assign.value)
    except:
        return assign.value.as_string()  # fallback
```

## Technical Approach

### Module Structure

```
upcast/django_scanner/
├── __init__.py          # Package exports
├── ast_utils.py         # Model detection helpers
├── model_parser.py      # Field/relationship parsing
├── checker.py           # Pylint checker implementation
├── export.py            # YAML output formatting
└── cli.py               # Command-line interface
```

### Key Algorithms

**1. Model Detection**

```python
def is_django_model(class_node):
    # Check ancestors through astroid inference
    for base in class_node.ancestors():
        if base.qname() == 'django.db.models.base.Model':
            return True
    return False
```

**2. Field Parsing**

```python
def parse_field(assign_node):
    # Extract: name = models.CharField(max_length=100)
    field_name = assign_node.targets[0].as_string()
    call = assign_node.value
    field_type = call.func.attrname  # CharField

    # Parse kwargs
    options = {}
    for kw in call.keywords:
        options[kw.arg] = infer_literal_value(kw.value)

    return field_name, field_type, options
```

**3. Relationship Detection**

```python
REL_FIELDS = {'ForeignKey', 'OneToOneField', 'ManyToManyField'}

def parse_relationship(field_type, args, options):
    if field_type not in REL_FIELDS:
        return None

    return {
        'type': field_type,
        'to': args[0],  # Related model
        'on_delete': options.get('on_delete'),
        'related_name': options.get('related_name'),
    }
```

**4. Abstract Inheritance Merging**

```python
def merge_abstract_fields(model, all_models):
    for base_qname in model['bases']:
        base = all_models.get(base_qname)
        if base and base['abstract']:
            # Copy fields from abstract parent
            model['fields'].update(base['fields'])
            # Recursively merge grandparents
            merge_abstract_fields(base, all_models)
```

## Risks / Trade-offs

### Risk: astroid Inference Failures

**Risk:** astroid may fail to infer types for complex imports or dynamic code.

**Mitigation:**

- Implement pattern-matching fallbacks
- Test against real-world Django projects
- Provide verbose mode for debugging inference issues

### Risk: Pylint Dependency Weight

**Risk:** Adding pylint/astroid increases package size and complexity.

**Mitigation:**

- Only require astroid (not full pylint)
- Document as optional dependency for model scanning
- Keep checker standalone-usable without full pylint

### Risk: Breaking Changes for Users

**Risk:** Complete rewrite breaks existing integrations.

**Mitigation:**

- Clearly document breaking changes
- Provide migration guide
- Version bump to indicate major change
- Consider keeping old command with deprecation warning (optional)

### Trade-off: Completeness vs Performance

**Trade-off:** astroid analysis is slower than ast-grep-py pattern matching.

**Analysis:**

- Pro: More accurate results worth the extra time
- Pro: Model scanning is typically one-time or CI operation
- Con: Slower for very large codebases (1000+ models)
- Verdict: Accuracy is more important than speed for this use case

## Migration Plan

### Phase 1: Core Implementation

1. Add astroid and PyYAML dependencies
2. Implement ast_utils.py for model detection
3. Implement model_parser.py for field parsing
4. Add comprehensive unit tests

### Phase 2: Checker and Export

1. Implement checker.py with Pylint integration
2. Implement export.py for YAML output
3. Add cli.py command wrapper
4. Integration testing with real Django projects

### Phase 3: Integration

1. Update upcast/main.py command
2. Remove old django_model module
3. Update tests/test_django_model.py
4. Update documentation

### Phase 4: Validation

1. Test against example Django projects
2. Compare output with old implementation
3. Fix any regressions or missing features
4. Update README with new examples

## Open Questions

None at this time. All design decisions are resolved based on the proven django-model-scanner implementation.

## References

- [django-model-scanner GitHub](https://github.com/yourusername/django-model-scanner)
- [astroid Documentation](https://pylint.readthedocs.io/projects/astroid/)
- [Pylint Checker Tutorial](https://pylint.readthedocs.io/en/latest/how_tos/custom_checkers.html)
- [Django Model Reference](https://docs.djangoproject.com/en/stable/ref/models/)
