"""Simple calculator module for testing smart-test."""

class Calculator:
    """A basic calculator with arithmetic operations."""
    
    def add(self, a, b):
        """Add two numbers."""
        return a + b
        
    def subtract(self, a, b):
        """Subtract b from a."""
        return a - b
        
    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b
        
    def divide(self, a, b):
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

def square(x):
    """Return the square of a number."""
    return x * x
    
def cube(x):
    """Return the cube of a number."""
    return x * x * x
    
def _internal_helper(value):
    """A private helper function."""
    return value * 2