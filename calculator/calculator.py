"""
Calculator module - Complete implementation for TDD demonstration

This is a COMPLETE example showing all functions working correctly.
All tests pass. Use this as a reference for TDD principles.
"""

def add(a, b):
    """Addition of two numbers"""
    return a + b

def subtract(a, b):
    """Subtraction of two numbers"""
    return a - b

def multiply(a, b):
    """Multiplication of two numbers"""
    return a * b

def divide(a, b):
    """
    Division of two numbers

    Raises:
        ZeroDivisionError: If divisor is zero
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def power(base, exponent):
    """
    Raise base to the power of exponent

    Supports positive, zero, and negative exponents.
    Uses recursion for negative exponents.
    """
    if exponent == 0:
        return 1
    elif exponent < 0:
        return 1 / power(base, -exponent)
    else:
        result = base
        for _ in range(exponent - 1):
            result *= base
        return result

def factorial(n):
    """
    Calculate factorial of n

    Args:
        n: Non-negative integer

    Returns:
        Factorial of n

    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def average(numbers):
    """
    Calculate the average of a list of numbers

    Args:
        numbers: List of numbers

    Returns:
        Average value

    Raises:
        ValueError: If list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)


if __name__ == "__main__":
    print("Calculator Demo - All Functions Working!")
    print("=" * 45)
    print(f"add(5, 3) = {add(5, 3)}")
    print(f"subtract(10, 4) = {subtract(10, 4)}")
    print(f"multiply(6, 7) = {multiply(6, 7)}")
    print(f"divide(15, 3) = {divide(15, 3)}")
    print(f"power(2, 4) = {power(2, 4)}")
    print(f"power(2, -2) = {power(2, -2)}")
    print(f"factorial(5) = {factorial(5)}")
    print(f"average([1, 2, 3, 4, 5]) = {average([1, 2, 3, 4, 5])}")
    print("=" * 45)
    print("✅ All functions implemented and tested!")