"""Tests for Redis key inference functionality."""

import tempfile
from pathlib import Path

import pytest

from upcast.scanners.redis_usage import RedisUsageScanner


@pytest.fixture
def scanner():
    """Create scanner instance."""
    return RedisUsageScanner()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_constant_key_inference(scanner, temp_dir):
    """Test inference of constant Redis keys."""
    test_file = temp_dir / "test_constant_key.py"
    test_file.write_text(
        """
from django.core.cache import cache

def test_func():
    cache.get("user:123")
    cache.set("user:456", "value", timeout=300)
"""
    )

    result = scanner.scan(test_file)
    usages = result.results.get("direct_client", [])

    assert len(usages) == 2
    assert usages[0].key == "user:123"
    assert usages[0].operation == "get"
    assert usages[1].key == "user:456"
    assert usages[1].operation == "set"


def test_variable_key_with_ellipsis(scanner, temp_dir):
    """Test inference of dynamic keys using ... for variable parts."""
    test_file = temp_dir / "test_dynamic_key.py"
    test_file.write_text(
        """
from django.core.cache import cache

def test_func(user_id):
    cache.get(user_id)
    cache.set(user_id, "value")
"""
    )

    result = scanner.scan(test_file)
    usages = result.results.get("direct_client", [])

    assert len(usages) == 2
    assert usages[0].key == "..."
    assert usages[1].key == "..."


def test_fstring_key_with_ellipsis(scanner, temp_dir):
    """Test inference of f-string keys with dynamic parts."""
    test_file = temp_dir / "test_fstring_key.py"
    test_file.write_text(
        """
from django.core.cache import cache

def test_func(user_id):
    cache.get(f"user:{user_id}")
    cache.set(f"user:{user_id}:profile", "value")
"""
    )

    result = scanner.scan(test_file)
    usages = result.results.get("direct_client", [])

    assert len(usages) == 2
    assert usages[0].key == "user:..."
    assert usages[1].key == "user:...:profile"  # ... replaces dynamic part


def test_format_method_key(scanner, temp_dir):
    """Test inference of keys using str.format()."""
    test_file = temp_dir / "test_format_key.py"
    test_file.write_text(
        """
from django.core.cache import cache

def test_func(user_id):
    cache.get("user:{}".format(user_id))
    cache.set("user:{0}:data".format(user_id), "value")
"""
    )

    result = scanner.scan(test_file)
    usages = result.results.get("direct_client", [])

    assert len(usages) == 2
    assert usages[0].key == "user:..."
    assert usages[1].key == "user:...:data"


def test_percent_formatting_key(scanner, temp_dir):
    """Test inference of keys using % formatting."""
    test_file = temp_dir / "test_percent_key.py"
    test_file.write_text(
        """
from django.core.cache import cache

def test_func(user_id):
    cache.get("user:%s" % user_id)
    cache.set("user:%d:profile" % user_id, "value")
"""
    )

    result = scanner.scan(test_file)
    usages = result.results.get("direct_client", [])

    assert len(usages) == 2
    assert usages[0].key == "user:..."
    assert usages[1].key == "user:...:profile"


def test_concatenation_key(scanner, temp_dir):
    """Test inference of keys using string concatenation."""
    test_file = temp_dir / "test_concat_key.py"
    test_file.write_text(
        """
from django.core.cache import cache

def test_func(user_id):
    cache.get("user:" + user_id)
    cache.set("prefix:" + user_id + ":suffix", "value")
"""
    )

    result = scanner.scan(test_file)
    usages = result.results.get("direct_client", [])

    assert len(usages) == 2
    assert usages[0].key == "user:..."
    assert usages[1].key == "prefix:...:suffix"


def test_attribute_access_key(scanner, temp_dir):
    """Test inference of keys using attribute access."""
    test_file = temp_dir / "test_attribute_key.py"
    test_file.write_text(
        """
from django.core.cache import cache
from django.conf import settings

def test_func():
    cache.get(settings.CACHE_KEY)
"""
    )

    result = scanner.scan(test_file)
    usages = result.results.get("direct_client", [])

    assert len(usages) == 1
    assert usages[0].key == "..."


def test_lock_key_inference(scanner, temp_dir):
    """Test key inference for distributed locks."""
    test_file = temp_dir / "test_lock_key.py"
    test_file.write_text(
        """
from django.core.cache import cache

def test_func(resource_id):
    with cache.lock("resource:lock"):
        pass

    with cache.lock(f"resource:{resource_id}:lock", timeout=10):
        pass
"""
    )

    result = scanner.scan(test_file)
    usages = result.results.get("distributed_lock", [])

    assert len(usages) == 2
    assert usages[0].key == "resource:lock"
    assert usages[1].key == "resource:...:lock"
    assert usages[1].timeout == 10


def test_variable_inference_to_literal(scanner, temp_dir):
    """Test that variables can be inferred to their literal values."""
    test_file = temp_dir / "test_var_inference.py"
    test_file.write_text(
        """
from django.core.cache import cache

def test_func():
    cache_key = "metrics:unavailable_deployments_total"
    cache.get(cache_key)
    cache.set(cache_key, "value", timeout=300)
"""
    )

    result = scanner.scan(test_file)
    usages = result.results.get("direct_client", [])

    assert len(usages) == 2
    # Both should infer the variable to its literal value
    assert usages[0].key == "metrics:unavailable_deployments_total"
    assert usages[1].key == "metrics:unavailable_deployments_total"


def test_uninferable_replaced_with_ellipsis(scanner, temp_dir):
    """Test that Uninferable is replaced with ... in all contexts."""
    test_file = temp_dir / "test_uninferable.py"
    test_file.write_text(
        """
from django.core.cache import cache

def test_func(obj):
    # Method call result - will be Uninferable
    cache.get(obj.get_key())

    # Complex expression - will be Uninferable
    cache.set(f"prefix:{obj.get_id()}", "value")
"""
    )

    result = scanner.scan(test_file)
    usages = result.results.get("direct_client", [])

    assert len(usages) == 2
    # Should be "..." not "Uninferable"
    assert usages[0].key == "..."
    assert usages[1].key == "prefix:..."
