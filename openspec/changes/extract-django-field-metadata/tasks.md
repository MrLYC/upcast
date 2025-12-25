# Tasks: Extract Django Field Metadata

## Task List

- [ ] 1. Update `DjangoField` model to add `help_text` and `verbose_name` fields

  - Add `help_text: str | None` field
  - Add `verbose_name: str | None` field
  - Update docstring

- [ ] 2. Update Django model scanner to extract metadata

  - Modify field parsing logic to extract `help_text` from parameters
  - Modify field parsing logic to extract `verbose_name` from parameters
  - Remove extracted fields from `parameters` dict

- [ ] 3. Update Markdown templates

  - Update `templates/zh/django_models.md.jinja2` to add "说明" and "显示名称" columns
  - Update `templates/en/django_models.md.jinja2` to add "Description" and "Verbose Name" columns
  - Ensure empty values display as "-" or similar placeholder

- [ ] 4. Update unit tests

  - Update test fixtures to include `help_text` and `verbose_name`
  - Add test cases for fields with metadata
  - Add test cases for fields without metadata
  - Verify YAML/JSON output format
  - Verify Markdown output format

- [ ] 5. Update integration test baseline

  - Regenerate example scan results with new format
  - Update README examples if needed

- [ ] 6. Run pre-commit checks and fix issues
  - Run `make lint`
  - Run `make test`
  - Fix any ruff/mypy issues

## Dependencies

- None

## Validation

- All unit tests pass with coverage ≥ 80%
- Integration tests pass
- Example output matches expected format
- Pre-commit checks pass
