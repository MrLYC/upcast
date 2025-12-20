# Tasks: Enhance Signal Scanner with Send Detection and Usage Tracking

## Data Structures

- [ ] Create `SignalUsage` dataclass in `signal_parser.py`
- [ ] Add fields: file, line, column, pattern, code, sender (optional)
- [ ] Update `SignalChecker` to use new signal structure (receivers/senders/usages)

## Signal Send Detection

- [ ] Implement `_extract_signal_name()` helper in `signal_parser.py` - extract object name from Call node
- [ ] Implement `_is_signal_send_call()` in `signal_parser.py` - check if Call node is signal.send()
- [ ] Add signal name validation against known signals whitelist (django_imports, celery_imports, custom_signals, known_signal_names)
- [ ] Reject .send() calls on non-signal objects (mail.send, message.send, etc.)
- [ ] Implement `parse_signal_send()` - parse signal.send() calls with validation
- [ ] Implement `parse_signal_send_robust()` - parse signal.send_robust() calls with validation
- [ ] Add sender extraction for send calls
- [ ] Add Django signal send detection (post_save.send, etc.)
- [ ] Add Celery signal send detection (task_sent.send, etc.)
- [ ] Add custom signal send detection (order_paid.send, etc.)

## Checker Updates

- [ ] Add `_get_known_signal_names()` method to extract signal names from collected receivers
- [ ] Add `_collect_signal_sends()` method to `SignalChecker` - pass known_signal_names for validation
- [ ] Add `_register_send()` method to register send usages
- [ ] Update `visit_module()` to call `_collect_signal_sends()` (third pass)
- [ ] Update `_register_handler()` to add to receivers and usages
- [ ] Update signal structure initialization to include receivers/senders/usages dicts
- [ ] Add helper `_usage_to_receiver_dict()` to convert SignalUsage to receiver format
- [ ] Add helper `_usage_to_sender_dict()` to convert SignalUsage to sender format

## Parser Refactoring

- [ ] Update `parse_receiver_decorator()` to return list[SignalUsage]
- [ ] Update `parse_signal_connect_method()` to return SignalUsage
- [ ] Update `parse_celery_connect_decorator()` to return SignalUsage
- [ ] Add code snippet extraction helper `_extract_code_snippet()`
- [ ] Update all parse functions to include column offset

## Export Updates

- [ ] Update `format_signal_output()` to handle receivers/senders/usages structure
- [ ] Add `--simple` flag support for backward compatibility
- [ ] Update YAML output to include receivers, senders, usages sections
- [ ] Add sender filtering (optional, for --senders-only mode)
- [ ] Add receiver filtering (optional, for --receivers-only mode)

## CLI Enhancements

- [ ] Add `--simple` flag to cli.py for backward compatible output
- [ ] Add `--receivers-only` flag (optional, skip send detection)
- [ ] Add `--senders-only` flag (optional, skip receiver detection)
- [ ] Update help text to mention send detection
- [ ] Update summary output to show sender counts

## Test Fixtures

- [ ] Create `tests/test_signal_scanner/fixtures/signal_sends.py`
- [ ] Add Django signal send examples (post_save.send, etc.)
- [ ] Add Django signal send_robust examples
- [ ] Add custom signal send examples
- [ ] Create `tests/test_signal_scanner/fixtures/celery_sends.py`
- [ ] Add Celery signal send examples
- [ ] Create `tests/test_signal_scanner/fixtures/mixed_sends_receives.py`
- [ ] Add combined send and receive patterns

## Unit Tests

- [ ] Create `tests/test_signal_scanner/test_send_parser.py`
- [ ] Test `parse_signal_send()` with valid send calls
- [ ] Test `parse_signal_send_robust()` with valid calls
- [ ] Test send detection with sender parameter
- [ ] Test send detection without sender parameter
- [ ] Test custom signal send detection
- [ ] Test rejection of non-signal .send() calls (mail.send, message.send, etc.)
- [ ] Test validation against known signals whitelist
- [ ] Test send detection only for signals in django_imports/celery_imports/custom_signals
- [ ] Test negative cases (not a signal send)

## Integration Tests

- [ ] Update `test_integration.py` for new structure
- [ ] Add `test_detect_django_signal_sends()` - verify Django .send() detection
- [ ] Add `test_detect_django_send_robust()` - verify .send_robust() detection
- [ ] Add `test_detect_celery_signal_sends()` - verify Celery send detection
- [ ] Add `test_signal_usage_tracking()` - verify usages list completeness
- [ ] Add `test_separate_receivers_and_senders()` - verify receivers/senders separation
- [ ] Update existing integration tests for new output format

## CLI Tests

- [ ] Update `test_cli.py` for new output format
- [ ] Add `test_simple_flag()` - verify --simple backward compatibility
- [ ] Add `test_receivers_only_flag()` (optional)
- [ ] Add `test_senders_only_flag()` (optional)
- [ ] Update summary output tests for sender counts

## Documentation

- [ ] Update CLI help text with send detection examples
- [ ] Create migration guide in proposal.md or separate doc
- [ ] Add example outputs showing receivers/senders/usages
- [ ] Document SignalUsage dataclass
- [ ] Document pattern types (receiver_decorator, send_method, etc.)

## Validation & Quality

- [ ] Run `uv run pytest tests/test_signal_scanner/ -v` - ensure all tests pass
- [ ] Run `uv run ruff check upcast/signal_scanner/` - fix all issues
- [ ] Run `uv run ruff check tests/test_signal_scanner/` - fix all issues
- [ ] Manual test: scan django project with sends and receives
- [ ] Manual test: verify --simple flag produces old format
- [ ] Verify performance (should not be >50% slower)

## Completion Checklist

- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] All CLI tests passing
- [ ] Ruff checks passing
- [ ] Manual testing complete
- [ ] Documentation updated
- [ ] Migration guide available
- [ ] Performance acceptable
