## Why

`scan-django-urls` establishes where Django routes are declared, but URL references alone do not explain what a resolved view accesses or how it is protected.  In particular, users need an auditable, static report of view identity, DRF actions, model use, authentication and authorization evidence, and explicit uncertainty rather than a guessed security conclusion.

## What Changes

- Add a standalone `scan-django-views` command and typed Django-view output model without changing the public `scan-django-urls` output contract.
- Discover Django function views, class-based views, DRF API views, and ViewSets from semantic framework evidence across all Python source files.
- Add a shared, internal route-reference index for direct URL targets and DRF Router registrations/mounts, including an explicit distinction between mounted and unmounted registrations.
- Report view- and action-level security evidence separately for authentication, authorization, and CSRF. Preserve raw decorators and authentication/permission expressions when semantics cannot be proven.
- Resolve referenced permission classes one hop to show definition and check-method evidence, without attempting a general call-graph analysis.
- Report direct model evidence from queryset/model declarations, direct ORM calls, and serializer `Meta.model` resolution, including conservative operation labels.
- Add synthetic fixtures, scanner/CLI coverage, and scanner documentation. No external-project source, paths, snapshots, statistics, or project-specific mappings will be committed.

## Impact

- Affected specs: `django-view-scanner` (new), `cli-interface`, `common-utilities`.
- Affected code: new models/scanner/common Django analysis helpers; scanner registration in `upcast/main.py` and `upcast/scanners/__init__.py`.
- Affected tests/docs: a dedicated Django-view test package, CLI functional tests, README/documentation indexes, and `docs/scanners/django-views.md`.
- Compatibility: existing scanner commands, especially `scan-django-urls`, retain their public command and serialized output contracts.
