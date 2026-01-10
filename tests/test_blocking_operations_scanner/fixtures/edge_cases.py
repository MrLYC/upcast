"""Edge cases fixture for blocking operations scanner tests."""

# Edge case: Aliased imports
ALIASED_IMPORTS = """
from time import sleep as tsleep
import asyncio as aio

def delayed_task():
    tsleep(1)
    aio.sleep(2)
"""

# Edge case: Nested function calls
NESTED_CALLS = """
import time

def outer():
    def inner():
        time.sleep(1)
        return nested_sleep()
    
    def nested_sleep():
        time.sleep(0.5)
    
    return inner()
"""

# Edge case: Lambda functions
LAMBDA_FUNCTIONS = """
import time

delay = lambda x: time.sleep(x)
quick_sleep = lambda: time.sleep(0.1)

def use_lambda():
    delay(1)
    quick_sleep()
"""

# Edge case: Dynamically called functions
DYNAMIC_CALLS = """
import time
import subprocess

def dynamic_call(operation):
    if operation == 'sleep':
        fn = time.sleep
        fn(1)
    elif operation == 'subprocess':
        cmd = subprocess.run
        cmd(['ls'])
"""

# Edge case: Attribute chains
ATTRIBUTE_CHAINS = """
import threading

class LockManager:
    def __init__(self):
        self.lock = threading.Lock()
    
    def acquire(self):
        self.lock.acquire()
        self.lock.release()

class NestedLocks:
    def __init__(self):
        self.manager = LockManager()
    
    def do_work(self):
        self.manager.lock.acquire()
"""

# Edge case: Multiple operations in one line
MULTIPLE_OPS_ONE_LINE = """
import time

def compact():
    time.sleep(1); time.sleep(2); time.sleep(3)
    result = time.sleep(0.5) or time.sleep(1)
"""

# Edge case: Operations in comprehensions
COMPREHENSIONS = """
import time

def in_comprehension():
    results = [time.sleep(0.1) for i in range(5)]
    dict_results = {i: time.sleep(0.1) for i in range(3)}
    set_results = {time.sleep(0.1) for i in range(2)}
"""

# Edge case: Operations in generators
GENERATORS = """
import time

def sleep_generator():
    for i in range(5):
        time.sleep(0.1)
        yield i

def generator_expr():
    gen = (time.sleep(0.1) for i in range(5))
    return list(gen)
"""

# Edge case: Conditional expressions (ternary)
CONDITIONAL_EXPRESSIONS = """
import time

def conditional():
    x = time.sleep(1) if True else time.sleep(2)
    result = time.sleep(0.5) if some_condition() else None

def some_condition():
    return True
"""

# Edge case: Decorated functions with blocking ops
DECORATED_FUNCTIONS = """
import time
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(0.1)
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def decorated_func():
    time.sleep(1)
    return "done"
"""

# Edge case: Operations in exception handlers
EXCEPTION_HANDLERS = """
import time
import subprocess

def error_handling():
    try:
        time.sleep(1)
    except Exception:
        time.sleep(0.5)
    else:
        time.sleep(0.2)
    finally:
        time.sleep(0.1)

def subprocess_error():
    try:
        subprocess.run(['false'])
    except subprocess.CalledProcessError:
        subprocess.run(['echo', 'error'])
"""

# Edge case: Class decorators and metaclasses
CLASS_DECORATORS = """
import time

def class_decorator(cls):
    original_init = cls.__init__
    
    def new_init(self, *args, **kwargs):
        time.sleep(0.1)
        original_init(self, *args, **kwargs)
    
    cls.__init__ = new_init
    return cls

@class_decorator
class DecoratedClass:
    def method(self):
        time.sleep(1)
"""

# Edge case: Operations in property getters/setters
PROPERTIES = """
import time

class PropertyExample:
    def __init__(self):
        self._value = 0
    
    @property
    def value(self):
        time.sleep(0.1)
        return self._value
    
    @value.setter
    def value(self, val):
        time.sleep(0.1)
        self._value = val
"""

# Edge case: Operations in context manager protocol
CONTEXT_MANAGERS = """
import time

class MyContextManager:
    def __enter__(self):
        time.sleep(0.1)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        time.sleep(0.1)
        return False

def use_context():
    with MyContextManager():
        time.sleep(1)
"""

# Edge case: Operations in __init__ and special methods
SPECIAL_METHODS = """
import time

class SpecialMethods:
    def __init__(self):
        time.sleep(0.1)
    
    def __call__(self):
        time.sleep(0.2)
    
    def __enter__(self):
        time.sleep(0.1)
        return self
    
    def __exit__(self, *args):
        time.sleep(0.1)
    
    def __del__(self):
        time.sleep(0.1)
"""

# Edge case: No blocking operations (negative case)
NO_BLOCKING_OPS = """
import math
import json

def pure_computation():
    result = math.sqrt(16)
    data = json.dumps({'key': 'value'})
    return result, data

class PureClass:
    def __init__(self):
        self.value = 42
    
    def compute(self):
        return self.value * 2
"""

# Edge case: Comments and strings containing blocking operation names
COMMENTS_AND_STRINGS = """
import time

def documented_function():
    # This function uses time.sleep for delay
    \"\"\"
    Example usage:
        time.sleep(1)  # Don't actually do this
    \"\"\"
    message = "Call time.sleep(1) for one second delay"
    actual_call = time.sleep(0.5)  # This should be detected
"""

# Edge case: Invalid or incomplete code (should not crash scanner)
INCOMPLETE_CODE = """
import time

def incomplete(
"""

# Edge case: Very long lines (truncation test)
LONG_LINES = """
import time

def long_statement():
    time.sleep(1)  # This is a very long comment that goes on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on and on
    very_long_variable_name_that_makes_the_line_extremely_long = time.sleep(2)
"""

# Edge case: Unicode and special characters
UNICODE_CODE = """
import time

def 测试函数():
    \"\"\"测试中文函数名\"\"\"
    time.sleep(1)

class Español:
    def método(self):
        time.sleep(0.5)
"""
