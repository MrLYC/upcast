"""Test fixture: unittest style tests."""

import unittest

from app.validators import validate_email, validate_phone


class TestValidators(unittest.TestCase):
    """Test validation functions."""

    def test_email_valid(self):
        """Test valid email."""
        self.assertTrue(validate_email("test@example.com"))

    def test_email_invalid(self):
        """Test invalid email."""
        self.assertFalse(validate_email("invalid"))

    def test_phone(self):
        """Test phone validation."""
        self.assertTrue(validate_phone("+1234567890"))
        self.assertFalse(validate_phone("abc"))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""

    def test_empty_strings(self):
        """Test empty strings."""
        self.assertFalse(validate_email(""))
        self.assertFalse(validate_phone(""))
