"""A simple calculator module for testing"""

def add(a: int, b: int) -> int:
    """Add two numbers together
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract b from a
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Difference of a and b
    """
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product of a and b
    """
    return a * b

def divide(a: float, b: float) -> float:
    """Divide a by b
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Result of division
        
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(base: float, exponent: int) -> float:
    """Calculate base raised to exponent
    
    Args:
        base: The base number
        exponent: The exponent
        
    Returns:
        base ** exponent
    """
    return base ** exponent

class Calculator:
    """A calculator class with memory functionality"""
    
    def __init__(self):
        """Initialize calculator with zero memory"""
        self.memory = 0
        self.history = []
    
    def add_to_memory(self, value: float) -> None:
        """Add a value to memory
        
        Args:
            value: Number to add to memory
        """
        self.memory += value
        self.history.append(f"Added {value} to memory")
    
    def subtract_from_memory(self, value: float) -> None:
        """Subtract a value from memory
        
        Args:
            value: Number to subtract from memory
        """
        self.memory -= value
        self.history.append(f"Subtracted {value} from memory")
    
    def get_memory(self) -> float:
        """Get current memory value
        
        Returns:
            Current memory value
        """
        return self.memory
    
    def clear_memory(self) -> None:
        """Clear memory and reset to zero"""
        self.memory = 0
        self.history.append("Cleared memory")
    
    def get_history(self) -> list:
        """Get calculation history
        
        Returns:
            List of history entries
        """
        return self.history.copy()
    
    def calculate(self, operation: str, a: float, b: float) -> float:
        """Perform a calculation
        
        Args:
            operation: Operation to perform (+, -, *, /)
            a: First operand
            b: Second operand
            
        Returns:
            Result of calculation
            
        Raises:
            ValueError: If operation is invalid or division by zero
        """
        if operation == '+':
            result = add(a, b)
        elif operation == '-':
            result = subtract(a, b)
        elif operation == '*':
            result = multiply(a, b)
        elif operation == '/':
            result = divide(a, b)
        else:
            raise ValueError(f"Invalid operation: {operation}")
        
        self.history.append(f"{a} {operation} {b} = {result}")
        return result