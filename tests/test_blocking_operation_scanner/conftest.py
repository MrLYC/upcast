"""pytest configuration for blocking operation scanner tests."""


def pytest_configure(config):
    """Configure pytest to skip sample files."""
    config.addinivalue_line("python_files", "test_*.py")
