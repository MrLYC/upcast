"""Test fixture: simple pytest tests."""

import pytest
from app.math_utils import add, is_even


def test_add_and_even():
    """
    测试 add 和 is_even 的基本行为
    """

    result = add(2, 3)
    assert result == 5

    assert is_even(result) is False
    assert is_even(4) is True


def test_add():
    """Test addition."""
    assert add(1, 2) == 3
    assert add(-1, 1) == 0


def test_exceptions():
    """Test exception handling."""
    with pytest.raises(ValueError):
        add("a", "b")
