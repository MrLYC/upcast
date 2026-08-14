## ADDED Requirements

### Requirement: Semantic Django View Discovery

The system SHALL provide a Django-view scanner that discovers request-handler candidates across eligible Python source files using framework semantics and confirmed route references.

#### Scenario: Confirm a class-based Django or DRF view

- **WHEN** a class has a resolved ancestor in the supported Django `View` or DRF view hierarchy
- **THEN** the scanner SHALL emit a view record with a canonical qualified identifier
- **AND** record the resolved ancestor and source location as recognition evidence

#### Scenario: Confirm a function view from a route reference

- **WHEN** a direct `path()` or `re_path()` target resolves to a function
- **THEN** the scanner SHALL emit that function as a confirmed view even when it lacks a known DRF decorator
- **AND** attach the route reference to the view record

#### Scenario: Preserve unconfirmed candidate evidence

- **WHEN** a potential framework base, decorator, or route target cannot be fully resolved
- **THEN** the scanner SHALL preserve its raw expression and source location with `partial` or `unknown` status
- **AND** SHALL NOT promote it to a confirmed view solely from a filename or short symbol name

### Requirement: ViewSet Action Analysis

The system SHALL represent DRF ViewSets with action-level findings in addition to the parent ViewSet record.

#### Scenario: Extract explicit action metadata

- **WHEN** a confirmed ViewSet method uses a resolved DRF `@action` decorator
- **THEN** the scanner SHALL record its action name, HTTP methods, detail scope, optional route metadata, and source location
- **AND** apply action-level security declarations as overrides of class-level declarations

#### Scenario: Mark framework-derived CRUD actions conservatively

- **WHEN** a ViewSet has a resolved DRF base with a known standard action contract
- **THEN** the scanner SHALL emit supported CRUD actions as `framework_derived`
- **AND** SHALL NOT derive actions from an unconfirmed or unsupported base

### Requirement: Route and Router References

The system SHALL provide reverse route references for resolved views without changing the public Django URL scanner output.

#### Scenario: Link a direct URL target

- **WHEN** a URLconf direct route resolves to a discovered view
- **THEN** the view record SHALL contain a confirmed route reference with URL source location and pattern evidence

#### Scenario: Confirm a mounted DRF Router registration

- **WHEN** a supported Router instance has a `register()` call whose ViewSet resolves
- **AND** that Router's `.urls` is mounted through `include()` or assigned directly to `urlpatterns`
- **THEN** the ViewSet record SHALL contain a confirmed Router route reference with prefix, basename, Router type, and source locations

#### Scenario: Retain an unmounted registration

- **WHEN** a supported Router registration is discovered but no matching Router URL mount is found
- **THEN** the scanner SHALL retain it as an unmounted candidate
- **AND** SHALL NOT report it as a confirmed endpoint

### Requirement: Security Evidence Separation

The system SHALL separately report authentication, authorization, and CSRF evidence for views and actions.

#### Scenario: Preserve local and inherited security declarations

- **WHEN** a view/action declares decorators, authentication classes, or permission classes
- **THEN** the scanner SHALL record raw expressions, resolved names when available, source locations, and declaration scope
- **AND** SHALL apply method/action, class, and statically resolvable default precedence without discarding overridden evidence

#### Scenario: Avoid unsafe equivalence claims

- **WHEN** authorization uses `AllowAny`, CSRF uses `csrf_exempt`, or a nonstandard decorator is encountered
- **THEN** the scanner SHALL NOT equate those signals with a Django login exemption
- **AND** SHALL report unclassified custom signals as raw evidence for downstream analysis

#### Scenario: Resolve permission implementations one hop

- **WHEN** a permission class/function referenced by a view can be resolved
- **THEN** the scanner SHALL record its definition location, inheritance, and `has_permission`/`has_object_permission` method evidence when present
- **AND** SHALL NOT recursively interpret arbitrary downstream service or IAM calls

### Requirement: Model Use Evidence

The system SHALL report statically supported model involvement without presenting inferred service behavior as direct model access.

#### Scenario: Report direct model evidence

- **WHEN** a view/action has a `queryset` or `model` declaration, direct recognized ORM access, or a resolvable serializer `Meta.model`
- **THEN** the scanner SHALL emit a model-use entry with source kind, location, resolution status, and operation classification where applicable

#### Scenario: Preserve unknown model expressions

- **WHEN** a model expression is dynamic, delegated to an unexamined service/manager, or cannot be resolved
- **THEN** the scanner SHALL retain the expression as unknown evidence
- **AND** SHALL NOT assign a concrete model or read/write/delete operation without proof

### Requirement: Typed and Stable View Output

The system SHALL expose results through validated scanner output models with stable ordering and canonical identifiers.

#### Scenario: Produce mergeable view records

- **WHEN** a scan completes
- **THEN** results SHALL be keyed by canonical qualified view identifiers
- **AND** route references SHALL use resolved module/symbol identities compatible with Django URL and Router target fields
- **AND** evidence collections SHALL be sorted deterministically by source location and identifier
