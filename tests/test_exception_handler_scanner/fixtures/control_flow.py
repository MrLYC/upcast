# ruff: noqa
"""Various control flow patterns in exception handlers."""


def except_with_pass():
    """Exception handler with pass statement."""
    try:
        x = 1 / 0
    except ZeroDivisionError:
        pass


def except_with_return():
    """Exception handler with return statement."""
    try:
        x = 1 / 0
        return x
    except ZeroDivisionError:
        return None


def except_with_raise():
    """Exception handler with raise statement."""
    try:
        x = 1 / 0
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero")


def except_with_break():
    """Exception handler with break statement."""
    for i in range(10):
        try:
            x = 1 / i
        except ZeroDivisionError:
            break


def except_with_continue():
    """Exception handler with continue statement."""
    for i in range(10):
        try:
            x = 1 / i
        except ZeroDivisionError:
            continue
        print(x)
