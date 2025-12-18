"""Pytest configuration for unit test scanner tests."""


def pytest_configure(config):
    """Configure pytest to ignore fixture test files."""
    config.addinivalue_line(
        "python_files",
        "test_*.py",
    )


def pytest_collection_modifyitems(config, items):
    """Skip fixture test files from collection."""
    # Remove fixture files from collection
    skip_paths = [
        "fixtures/test_math.py",
        "fixtures/test_validators.py",
    ]

    items_to_keep = []
    for item in items:
        keep = True
        for skip_path in skip_paths:
            if skip_path in str(item.fspath):
                keep = False
                break
        if keep:
            items_to_keep.append(item)

    items[:] = items_to_keep
