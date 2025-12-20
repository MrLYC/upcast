"""Edge cases for complexity calculation."""


def nested_function_outer():
    """Outer function - complexity 2."""
    x = 10

    def nested_function_inner(y):
        """Inner nested function - complexity 1 (independent)."""
        return y * 2

    if x > 0:  # +1
        return nested_function_inner(x)
    return 0


class MyClass:
    """Class with various method types."""

    def __init__(self, value):
        """Constructor with complexity 2."""
        if value < 0:  # +1
            value = 0
        self.value = value

    def instance_method(self, x):
        """Regular instance method - complexity 2."""
        if x > self.value:  # +1
            return x
        return self.value

    @staticmethod
    def static_method(x):
        """Static method - complexity 2."""
        if x > 0:  # +1
            return x
        return 0

    @classmethod
    def class_method(cls, x):
        """Class method - complexity 2."""
        if x > 0:  # +1
            return cls(x)
        return cls(0)

    async def async_method(self, x):
        """Async method - complexity 2."""
        if x > 0:  # +1
            return x
        return 0


def function_with_comments():
    """Function with comments - complexity 1."""
    # This is a comment
    x = 10  # inline comment
    # Another comment
    return x


def function_with_string_hash():
    """Function with hash in strings - complexity 1."""
    message = "This is #not a comment"
    code = "# This is also not a comment"
    return message + code


def function_with_multiline_string():
    """Function with multiline string - complexity 1."""
    text = """
    This is a multiline string
    # This looks like a comment but it's not
    It spans multiple lines
    """
    return text
