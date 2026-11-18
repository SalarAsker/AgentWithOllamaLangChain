from langchain_core.tools import tool


# Tool for addition
@tool
def addition(a: float, b: float) -> float:
    """
    Add two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of the two numbers.
    """
    return a + b

# Tool for subtraction
@tool
def subtraction(a: float, b: float) -> float:
    """
    Subtract two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The difference of the two numbers.
    """
    return a - b

# Tool for multiplication
@tool
def multiplication(a: float, b: float) -> float:
    """
    Multiply two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of the two numbers.
    """
    return a * b

# Tool for division
@tool   
def division(a: float, b: float) -> float:
    """
    Divide two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The quotient of the two numbers.
    """
    if b == 0:
        return f"Error:Division by zero is not allowed."
    return a / b

# Tools collection
tools_collection = [
    addition,
    subtraction,
    multiplication,
    division
]


