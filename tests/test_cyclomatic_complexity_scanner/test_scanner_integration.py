"""Integration tests for complexity scanner."""

import pytest

from upcast.scanners.complexity import ComplexityScanner


class TestComplexityScanner:
    """Test complexity scanner integration."""

    def test_scan_simple_function(self, low_threshold_scanner: ComplexityScanner, tmp_path):
        """Test scanning simple function."""
        code = """
def simple_function(x):
    return x + 1
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = low_threshold_scanner.scan(tmp_path)

        assert result.summary.total_count == 1
        assert "test.py" in result.results
        assert result.results["test.py"][0].name == "simple_function"
        assert result.results["test.py"][0].complexity == 1

    def test_scan_function_with_if(self, low_threshold_scanner: ComplexityScanner, tmp_path):
        """Test scanning function with if statement."""
        code = """
def function_with_if(x):
    if x > 0:
        return x
    return 0
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = low_threshold_scanner.scan(tmp_path)

        assert result.summary.total_count == 1
        assert result.results["test.py"][0].complexity == 2  # Base 1 + if 1

    def test_scan_function_with_for_loop(self, low_threshold_scanner: ComplexityScanner, tmp_path):
        """Test scanning function with for loop."""
        code = """
def function_with_loop(items):
    total = 0
    for item in items:
        total += item
    return total
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = low_threshold_scanner.scan(tmp_path)

        assert result.summary.total_count == 1
        assert result.results["test.py"][0].complexity == 2  # Base 1 + for 1

    def test_scan_function_with_while(self, low_threshold_scanner: ComplexityScanner, tmp_path):
        """Test scanning function with while loop."""
        code = """
def function_with_while(n):
    i = 0
    while i < n:
        i += 1
    return i
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = low_threshold_scanner.scan(tmp_path)

        assert result.summary.total_count == 1
        assert result.results["test.py"][0].complexity == 2  # Base 1 + while 1

    def test_scan_complex_function(self, scanner: ComplexityScanner, tmp_path):
        """Test scanning function exceeding default threshold."""
        code = """
def complex_function(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                if x > y:
                    if y > z:
                        if x > z:
                            if x + y > 10:
                                if y + z > 5:
                                    if x + z > 8:
                                        if x + y + z > 20:
                                            return x + y + z
    for i in range(x):
        if i % 2 == 0:
            continue
    return 0
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_count == 1
        assert result.results["test.py"][0].complexity >= 11

    def test_scan_multiple_functions(self, scanner: ComplexityScanner, tmp_path):
        """Test scanning multiple functions."""
        code = """
def func1(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                if x > y:
                    if y > z:
                        if x > z:
                            if x + y > 10:
                                if y + z > 5:
                                    if x + z > 8:
                                        if x + y + z > 20:
                                            return x + y + z
    return 0

def func2(a, b, c):
    for i in range(a):
        if i % 2 == 0:
            if i > 10:
                if i < 50:
                    if i % 5 == 0:
                        if i % 7 == 0:
                            if i % 3 == 0:
                                if b > c:
                                    if a > b:
                                        if a > c:
                                            continue
    return a
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_count == 2
        assert len(result.results["test.py"]) == 2

    def test_scan_class_methods(self, scanner: ComplexityScanner, tmp_path):
        """Test scanning class methods."""
        code = """
class MyClass:
    def complex_method(self, x, y, z):
        if x > 0:
            if y > 0:
                if z > 0:
                    if x > y:
                        if y > z:
                            if x > z:
                                if x + y > 10:
                                    if y + z > 5:
                                        if x + z > 8:
                                            if x + y + z > 20:
                                                return x + y + z
        return 0
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_count == 1
        assert result.results["test.py"][0].name == "complex_method"

    def test_scan_async_function(self, scanner: ComplexityScanner, tmp_path):
        """Test scanning async function."""
        code = """
async def async_complex_function(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                if x > y:
                    if y > z:
                        if x > z:
                            if x + y > 10:
                                if y + z > 5:
                                    if x + z > 8:
                                        if x + y + z > 20:
                                            return x + y + z
    return 0
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_count == 1
        assert result.results["test.py"][0].name == "async_complex_function"

    def test_threshold_filtering(self, tmp_path):
        """Test that threshold filters results correctly."""
        code = """
def low_complexity(x):
    if x > 0:
        return x
    return 0

def high_complexity(x):
    if x > 0:
        if x > 10:
            if x > 20:
                if x > 30:
                    if x > 40:
                        if x > 50:
                            return x
    return 0
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        # With high threshold, should only get high_complexity function
        high_scanner = ComplexityScanner(threshold=5)
        result = high_scanner.scan(tmp_path)

        assert result.summary.total_count == 1
        assert result.results["test.py"][0].name == "high_complexity"

    def test_scan_empty_directory(self, scanner: ComplexityScanner, tmp_path):
        """Test scanning empty directory."""
        result = scanner.scan(tmp_path)

        assert result.summary.total_count == 0
        assert len(result.results) == 0

    def test_scan_no_complex_functions(self, scanner: ComplexityScanner, tmp_path):
        """Test scanning file without complex functions."""
        code = """
def simple1(x):
    return x + 1

def simple2(x):
    return x * 2
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_count == 0
        assert len(result.results) == 0

    def test_scan_multiple_files(self, scanner: ComplexityScanner, tmp_path):
        """Test scanning multiple files."""
        code1 = """
def complex1(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                if x > y:
                    if y > z:
                        if x > z:
                            if x + y > 10:
                                if y + z > 5:
                                    if x + z > 8:
                                        if x + y + z > 20:
                                            return x + y + z
    return 0
"""
        code2 = """
def complex2(a, b, c):
    for i in range(a):
        if i % 2 == 0:
            if i > 10:
                if i < 50:
                    if i % 5 == 0:
                        if i % 7 == 0:
                            if i % 3 == 0:
                                if b > c:
                                    if a > b:
                                        if a > c:
                                            continue
    return a
"""
        file1 = tmp_path / "module1.py"
        file1.write_text(code1)

        file2 = tmp_path / "module2.py"
        file2.write_text(code2)

        result = scanner.scan(tmp_path)

        assert result.summary.total_count == 2
        assert result.summary.files_scanned == 2
        assert "module1.py" in result.results
        assert "module2.py" in result.results

    def test_severity_assignment(self, low_threshold_scanner: ComplexityScanner, tmp_path):
        """Test severity levels are assigned correctly."""
        code = """
def healthy_func(x):
    return x

def acceptable_func(x):
    if x > 0:
        if x > 10:
            if x > 20:
                return x
    return 0

def warning_func(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                if x > y:
                    if y > z:
                        if x > z:
                            if x + y > 10:
                                if y + z > 5:
                                    if x + z > 8:
                                        return x
    return 0

def high_risk_func(a, b, c, d):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if a > b:
                        if b > c:
                            if c > d:
                                if a + b > 10:
                                    if b + c > 5:
                                        if c + d > 3:
                                            if a + c > 8:
                                                if a + d > 12:
                                                    if b + d > 7:
                                                        return a + b + c + d
    return 0
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = low_threshold_scanner.scan(tmp_path)

        assert result.summary.total_count >= 3
        severities = [r.severity for r in result.results["test.py"]]
        assert "warning" in severities or "high_risk" in severities or "critical" in severities
