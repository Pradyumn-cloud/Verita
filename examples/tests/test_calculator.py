# tests/test_calculator.py
import pytest
from mypackage.calculator import Calculator, square

def test_add():
    """Test the add method."""
    calc = Calculator()
    assert calc.add(1, 2) == 3
    assert calc.add(-1, 1) == 0
    
def test_subtract():
    """Test the subtract method."""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(10, 10) == 0
    
def test_square():
    """Test the square function."""
    assert square(4) == 16
    assert square(-2) == 4