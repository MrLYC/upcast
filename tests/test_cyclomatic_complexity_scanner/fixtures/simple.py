"""Simple functions with known complexity values."""


def simple_function():
    """A simple function with complexity 1."""
    return 42


def function_with_if(x):
    """Function with one if statement - complexity 2."""
    if x > 0:
        return x
    return -x


def function_with_if_elif(x):
    """Function with if-elif - complexity 3."""
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    return "zero"


def function_with_loop(items):
    """Function with a for loop - complexity 2."""
    total = 0
    for item in items:
        total += item
    return total


def function_with_while(n):
    """Function with a while loop - complexity 2."""
    count = 0
    while n > 0:
        count += 1
        n -= 1
    return count
