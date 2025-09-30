"""
Test suite for the calculator module - Complete example

This is a COMPLETE test suite demonstrating TDD best practices.
All tests pass. Study these to understand:
- How to structure tests
- How to test exceptions
- How to use parameterized tests
- How to organize tests in classes
"""

import pytest
from calculator import add, subtract, multiply, divide, power, factorial, average


class TestBasicOperations:
    """Tests for basic arithmetic operations"""

    def test_add(self):
        """Test addition with various inputs"""
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0

    def test_subtract(self):
        """Test subtraction with various inputs"""
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5
        assert subtract(-3, -3) == 0

    def test_multiply(self):
        """Test multiplication with various inputs"""
        assert multiply(3, 4) == 12
        assert multiply(-2, 3) == -6
        assert multiply(0, 100) == 0


class TestDivision:
    """Tests for division - including edge cases!"""

    def test_divide_normal_cases(self):
        """Test division with valid inputs"""
        assert divide(10, 2) == 5
        assert divide(9, 3) == 3
        assert divide(7, 2) == 3.5

    def test_divide_by_zero(self):
        """✅ Test exception handling for division by zero"""
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            divide(10, 0)


class TestPower:
    """Tests for power function"""

    def test_power_positive_exponent(self):
        """Test power with positive exponents"""
        assert power(2, 3) == 8
        assert power(5, 2) == 25
        assert power(10, 0) == 1

    def test_power_negative_exponent(self):
        """✅ Test power with negative exponents"""
        assert power(2, -1) == 0.5
        assert power(4, -2) == 0.0625


class TestFactorial:
    """Tests for factorial function"""

    @pytest.mark.parametrize("n, expected", [
        (0, 1),      # Special case: 0! = 1
        (1, 1),
        (3, 6),
        (5, 120),
        (10, 3628800)
    ])
    def test_factorial_valid_inputs(self, n, expected):
        """✅ Test factorial with valid inputs using parametrization"""
        assert factorial(n) == expected

    def test_factorial_negative_input(self):
        """✅ Test exception handling for negative inputs"""
        with pytest.raises(ValueError, match="Factorial not defined for negative numbers"):
            factorial(-1)


class TestAverage:
    """Tests for average calculation"""

    def test_average_normal_cases(self):
        """Test average with valid lists"""
        assert average([1, 2, 3, 4, 5]) == 3
        assert average([10, 20]) == 15
        assert average([5]) == 5

    def test_average_empty_list(self):
        """✅ Test exception handling for empty list"""
        with pytest.raises(ValueError, match="Cannot calculate average of empty list"):
            average([])