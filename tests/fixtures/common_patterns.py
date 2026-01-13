"""Common code patterns for testing across all scanners."""

# Standard imports
STANDARD_IMPORTS = """
import os
import sys
from typing import Optional, List, Dict
"""

# Simple function
SIMPLE_FUNCTION = """
def example_function(x: int) -> int:
    '''Example function.'''
    return x * 2
"""

# Simple class
SIMPLE_CLASS = """
class ExampleClass:
    '''Example class.'''

    def __init__(self, value):
        self.value = value

    def method(self):
        return self.value
"""

# Async function
ASYNC_FUNCTION = """
import asyncio

async def async_example():
    '''Async example.'''
    await asyncio.sleep(1)
    return "done"
"""

# Async class method
ASYNC_METHOD = """
import asyncio

class AsyncExample:
    async def fetch_data(self):
        await asyncio.sleep(0.1)
        return "data"
"""

# Function with multiple parameters
FUNCTION_WITH_PARAMS = """
def complex_function(
    a: int,
    b: str = "default",
    *args,
    c: Optional[int] = None,
    **kwargs
) -> Dict:
    '''Function with multiple parameter types.'''
    return {"a": a, "b": b, "c": c}
"""

# Class with inheritance
CLASS_WITH_INHERITANCE = """
class BaseClass:
    def base_method(self):
        pass

class DerivedClass(BaseClass):
    def derived_method(self):
        pass
"""

# Decorator examples
SIMPLE_DECORATOR = """
@decorator
def decorated_function():
    pass
"""

DECORATOR_WITH_ARGS = """
@decorator(arg1="value", arg2=123)
def decorated_function():
    pass
"""

# Try-except pattern
TRY_EXCEPT_PATTERN = """
try:
    risky_operation()
except ValueError:
    handle_error()
"""

# Context manager
CONTEXT_MANAGER = """
with open("file.txt") as f:
    content = f.read()
"""

# Loop patterns
FOR_LOOP = """
for item in items:
    process(item)
"""

WHILE_LOOP = """
while condition:
    do_something()
"""

# Conditional
IF_ELSE = """
if condition:
    branch_a()
else:
    branch_b()
"""

# List comprehension
LIST_COMPREHENSION = """
result = [x * 2 for x in range(10) if x % 2 == 0]
"""

# Lambda
LAMBDA_FUNCTION = """
func = lambda x: x * 2
"""

# Nested function
NESTED_FUNCTION = """
def outer():
    def inner():
        return "nested"
    return inner()
"""

# Generator
GENERATOR_FUNCTION = """
def generator():
    for i in range(10):
        yield i
"""

# Property
PROPERTY_PATTERN = """
class MyClass:
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
"""

# Static and class methods
STATIC_CLASS_METHODS = """
class MyClass:
    @staticmethod
    def static_method():
        return "static"

    @classmethod
    def class_method(cls):
        return cls.__name__
"""

# Type hints
TYPE_HINTS = """
from typing import List, Dict, Optional, Union

def typed_function(
    items: List[str],
    mapping: Dict[str, int],
    optional: Optional[str] = None
) -> Union[str, int]:
    return items[0] if items else 0
"""

# Dataclass
DATACLASS_PATTERN = """
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    email: Optional[str] = None
"""

# Enum
ENUM_PATTERN = """
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
"""

# Abstract base class
ABC_PATTERN = """
from abc import ABC, abstractmethod

class AbstractBase(ABC):
    @abstractmethod
    def required_method(self):
        pass
"""
