"""Test fixture with module symbols."""

# Module-level variables
DEBUG = True
MAX_RETRIES = 3
API_URL = "https://api.example.com"
_private_var = "internal"

# Conditional variable
if DEBUG:
    LOG_LEVEL = "DEBUG"


def helper(arg1: int, arg2: str) -> bool:
    """A helper function."""
    return True


def _internal():
    """Private function."""
    pass


@decorator
@another_decorator(arg1, kwarg="value")
def decorated_func():
    """Decorated function."""
    pass


class MyClass:
    """A simple class."""

    attr1 = "value"

    def method1(self):
        """Method 1."""
        pass

    def method2(self):
        """Method 2."""
        pass


class _PrivateClass:
    """Private class."""

    pass


class Child(Parent1, Parent2):
    """Child class with multiple bases."""

    pass


from dataclasses import dataclass


@dataclass
class Config:
    """Configuration class."""

    name: str
    value: int
