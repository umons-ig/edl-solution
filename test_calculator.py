"""
Test suite for the calculator module.
Your mission: Make all these tests pass!
"""

import pytest
from calculator import add, subtract, multiply, divide, power, factorial, average


class TestBasicOperations:
    """Tests for basic arithmetic operations"""
    
    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0
    
    def test_subtract(self):
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5
        assert subtract(-3, -3) == 0
    
    def test_multiply(self):
        assert multiply(3, 4) == 12
        assert multiply(-2, 3) == -6
        assert multiply(0, 100) == 0


class TestDivision:
    """Tests for division - including edge cases!"""
    
    def test_divide_normal_cases(self):
        assert divide(10, 2) == 5
        assert divide(9, 3) == 3
        assert divide(7, 2) == 3.5
    
    def test_divide_by_zero(self):
        """❌ This test is failing! Fix the divide function"""
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            divide(10, 0)


class TestPower:
    """Tests for power function"""
    
    def test_power_positive_exponent(self):
        assert power(2, 3) == 8
        assert power(5, 2) == 25
        assert power(10, 0) == 1
    
    def test_power_negative_exponent(self):
        """❌ This test is failing! Fix the power function"""
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
        """❌ These tests are failing! Implement factorial"""
        assert factorial(n) == expected
    
    def test_factorial_negative_input(self):
        """❌ This test is failing! Handle negative inputs"""
        with pytest.raises(ValueError, match="Factorial not defined for negative numbers"):
            factorial(-1)


class TestAverage:
    """Tests for average calculation"""
    
    def test_average_normal_cases(self):
        assert average([1, 2, 3, 4, 5]) == 3
        assert average([10, 20]) == 15
        assert average([5]) == 5
    
    def test_average_empty_list(self):
        """❌ This test is failing! Handle empty lists"""
        with pytest.raises(ValueError, match="Cannot calculate average of empty list"):
            average([])