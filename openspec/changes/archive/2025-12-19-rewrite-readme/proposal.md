# Proposal: Rewrite README

## Overview

Rewrite the project README.md to provide a comprehensive and up-to-date guide for all current scanner commands. The current README is outdated, contains references to deprecated commands, and doesn't cover all available scanners.

## Problem Statement

The current README has several issues:

1. **Incomplete Coverage**: Missing documentation for several scanners:

   - `scan-blocking-operations` - Not documented
   - `scan-concurrency-patterns` - Not documented
   - `scan-django-urls` - Not documented
   - `scan-exception-handlers` - Not documented
   - `scan-http-requests` - Not documented
   - `scan-signals` - Not documented
   - `scan-unit-tests` - Not documented

2. **Outdated Migration Guide**: Contains references to old deprecated commands that no longer exist

3. **Poor Organization**: Scanners are not grouped logically, making it hard to find related functionality

4. **Inconsistent Documentation**: Different scanners have varying levels of detail and examples

## Proposed Solution

Create a completely new README.md that:

1. **Comprehensive Scanner Coverage**: Document all 11 scanners with consistent format:

   - scan-env-vars
   - scan-django-models
   - scan-django-settings
   - scan-django-urls
   - scan-prometheus-metrics
   - scan-concurrency-patterns
   - scan-signals
   - scan-exception-handlers
   - scan-http-requests
   - scan-blocking-operations
   - scan-unit-tests

2. **Logical Organization**:

   - Quick Start section
   - Installation
   - Common Options (file filtering)
   - Scanner Groups:
     - Django Scanners (models, settings, urls, signals)
     - Code Analysis Scanners (concurrency, blocking-operations, unit-tests)
     - Infrastructure Scanners (env-vars, prometheus-metrics)
     - HTTP & Exception Scanners (http-requests, exception-handlers)

3. **Consistent Documentation Format** for each scanner:

   - Brief description
   - Basic usage example
   - Common use cases
   - Output format example
   - Key features

4. **Modern Structure**:
   - Remove migration guide (no longer needed)
   - Add quick reference table
   - Better examples
   - Clear feature highlights

## Requirements

### Requirement: Complete Scanner Documentation

The README SHALL document all 11 available scanner commands with consistent format and examples.

#### Scenario: Django URL Scanner Documentation

- **WHEN** users read the README
- **THEN** they SHALL find documentation for `scan-django-urls`
- **AND** see basic usage examples
- **AND** understand the output format
- **AND** see file filtering examples

#### Scenario: Blocking Operations Scanner Documentation

- **WHEN** users read the README
- **THEN** they SHALL find documentation for `scan-blocking-operations`
- **AND** understand what blocking operations are detected
- **AND** see examples of detected patterns
- **AND** understand async anti-pattern detection

#### Scenario: Unit Test Scanner Documentation

- **WHEN** users read the README
- **THEN** they SHALL find documentation for `scan-unit-tests`
- **AND** understand test framework support
- **AND** see output format examples
- **AND** understand coverage information

### Requirement: Logical Organization

The README SHALL organize scanners into logical groups for easy navigation.

#### Scenario: Scanner Grouping

- **WHEN** users browse the README
- **THEN** scanners SHALL be grouped by category
- **AND** Django-related scanners SHALL be together
- **AND** code analysis scanners SHALL be grouped
- **AND** each group SHALL have a clear heading

### Requirement: Consistent Format

Each scanner documentation SHALL follow the same structure for consistency.

#### Scenario: Uniform Documentation Structure

- **WHEN** viewing any scanner section
- **THEN** it SHALL have a brief description
- **AND** show basic usage command
- **AND** provide common use cases
- **AND** include output format example
- **AND** list key features

### Requirement: Remove Outdated Content

The README SHALL not contain references to deprecated or non-existent commands.

#### Scenario: Clean Migration Guide

- **WHEN** users read the README
- **THEN** there SHALL be no migration guide section
- **AND** no references to old command names
- **AND** no breaking change warnings

## Success Criteria

1. All 11 scanners are documented
2. Each scanner has consistent format
3. No references to deprecated commands
4. Clear logical grouping of scanners
5. Improved readability and navigation
6. Modern, professional appearance

## Out of Scope

- API documentation (belongs in separate docs)
- Detailed implementation details
- Architecture documentation beyond high-level overview
- Contribution guidelines (separate CONTRIBUTING.md)
