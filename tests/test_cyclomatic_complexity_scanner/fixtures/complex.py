"""Complex functions with higher complexity values."""


def complex_function(x, y, z):
    """Function with multiple decision points - complexity 8."""
    if x > 0 and y > 0:  # +2 (if + and)
        if z > 0:  # +1
            return x + y + z
        else:  # elif/else doesn't add
            return x + y
    elif x < 0 or y < 0:  # +2 (elif + or)
        return -1

    for i in range(10):  # +1
        if i == 5:  # +1
            break

    return 0


def function_with_try_except(value):
    """Function with exception handling - complexity 3."""
    try:
        result = int(value)
        if result < 0:  # +1
            raise ValueError("Negative")
        return result
    except ValueError:  # +1
        return 0
    except TypeError:  # +1
        return -1


def function_with_ternary(x, y):
    """Function with ternary expressions - complexity 3."""
    result = x if x > 0 else 0  # +1
    result += y if y > 0 else 0  # +1
    return result


def function_with_comprehension(items):
    """Function with list comprehension - complexity 3."""
    # Comprehension with if adds +1
    positive = [x for x in items if x > 0]  # +1
    # Nested condition adds another +1
    even_positive = [x for x in items if x > 0 if x % 2 == 0]  # +2
    return positive, even_positive


def function_with_assert(value):
    """Function with assert - complexity 2."""
    assert value > 0, "Value must be positive"  # +1 for condition
    return value * 2


async def async_function_complex(x, y):
    """Async function with complexity 5."""
    if x > 0:  # +1
        if y > 0:  # +1
            return x + y

    for i in range(10):  # +1
        if i == x:  # +1
            return i

    return 0


class ComplexClass:
    """Class with complex methods."""

    def complex_method(self, items, threshold):
        """Method with complexity 7."""
        result = []
        for item in items:  # +1
            if item > threshold:  # +1
                if item % 2 == 0:  # +1
                    result.append(item * 2)
                elif item % 3 == 0:  # +1
                    result.append(item * 3)
            elif item < 0:  # +1
                result.append(0)

        return result if result else None  # +1
