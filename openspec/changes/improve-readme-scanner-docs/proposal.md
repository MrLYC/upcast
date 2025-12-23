# Proposal: Improve README Scanner Documentation

## Status

- **State**: complete
- **Created**: 2025-12-23
- **Owner**: AI Agent
- **Completed**: 2025-12-23

## Why

The current README.md has scanner documentation scattered throughout without clear organization. Key issues:

1. **No dedicated scanners section** - Scanner docs are mixed with general content
2. **Inconsistent structure** - Different scanners have varying levels of detail
3. **Missing examples** - Not all scanners reference example outputs from `example/scan-results/`
4. **Hard to navigate** - Users struggle to find specific scanner information

This change will:

- Create a clear "Scanners" section with consistent subsection structure
- Ensure all 12 scanners have complete documentation
- Link each scanner to its example output file
- Improve discoverability and user experience

## What Changes

### Documentation Updates

Add a new `## Scanners` section to README.md with:

1. **Consistent subsection structure for each scanner**:

   - Brief description
   - Command-line usage
   - Output example (from `example/scan-results/`)
   - Key features list

2. **Complete coverage of all 12 scanners**:

   - Django scanners (4): models, settings, urls, signals
   - Code analysis (3): concurrency, blocking operations, unit tests
   - Infrastructure (2): env vars, prometheus metrics
   - HTTP & exceptions (2): http requests, exception handlers
   - Code quality (1): complexity patterns

3. **Cross-references**:
   - Link to example output files
   - Reference related scanners
   - Point to relevant specifications

### Example Integration

Each scanner section will include:

- Path to example output: `example/scan-results/<scanner>.yaml`
- Representative output snippet
- Explanation of output structure

## Success Criteria

- [x] README has clear `## Scanners` section
- [x] All 12 scanners documented with consistent structure
- [x] Each scanner links to example output
- [x] Documentation validated against actual scanner behavior
- [x] Navigation improved (table of contents, clear hierarchy)

## Out of Scope

- Changing scanner implementations
- Modifying example outputs
- Adding new scanners
- CLI interface changes
