
# File: tool_products_stock.py
from langchain_core.tools import tool

PRODUCTS = {
    "laptop": {
        "price": 12000,
        "stock": 5
    },
    "keyboard": {
        "price": 800,
        "stock": 12
    },
    "mouse": {
        "price": 350,
        "stock": 0
    }
}

@tool
def check_product_stock(product_name: str) -> dict:
    """
    Check the stock level of a product by its name.
    
    Args:
        product_name (str): The name of the product.
        
    Returns:
        dict: A dictionary containing the product details or an error message.
    """
    if product_name not in PRODUCTS:
        return {
            "found": False,
            "message": "Product not found."
        }

    return {
        "found": True,
        "product_name": product_name,
        "price": PRODUCTS[product_name]["price"],
        "stock": PRODUCTS[product_name]["stock"]
    }