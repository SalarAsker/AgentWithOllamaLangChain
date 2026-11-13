
# File: tools.py
from langchain_core.tools import tool

# Simulated databases for products, orders, and deliveries
PRODUCTS = {
    "Laptop": {
        "price": 12000,
        "stock": 5
    },
    "Keyboard": {
        "price": 800,
        "stock": 12
    },
    "Mouse": {
        "price": 350,
        "stock": 0
    }
}

ORDERS = {
    1051: {
        "status": "Delivered",
        "product": "Keyboard"
    },
    1052: {
        "status": "Shipped",
        "product": "Laptop"
    },
    1053: {
        "status": "Processing",
        "product": "Mouse"
    }
}

DELIVERIES = {
    1051: "Delivered on 20 October",
    1052: "Expected delivery on 30 October",
    1053: "Not shipped yet. Expected delivery on 15 November"
}

# define a tool to check the stock level of a product using the tool decorator. This tool will be used by the LLM to fetch product details based on the provided product name.
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


# Define a tool to check the status of an order using the tool decorator. This tool will be used by the LLM to fetch order details based on the provided order ID.
@tool
def check_delivery_info(order_id: int) -> dict:
    """
    Get the delivery information of an order by its ID.
    
    Args:
        order_id (int): The ID of the order.
        
    Returns:
        dict: A dictionary containing the delivery information or an error message.
    """
    if order_id not in DELIVERIES:
        return {
            "found": False,
            "message": "Order not found."
        }

    return {
        "found": True,
        "order_id": order_id,
        "delivery_info": DELIVERIES[order_id]
    }


# Define a tool to check the status of an order using the tool decorator. This tool will be used by the LLM to fetch order details based on the provided order ID.
@tool
def check_order_status(order_id: int) -> dict:
    """
    Get the status of an order by its ID.
    
    Args:
        order_id (int): The ID of the order.
        
    Returns:
        dict: A dictionary containing the order details or an error message.
    """

    if order_id not in ORDERS:
        return {
            "found": False,
            "message": "Order not found."
           }

    return{
            "found": True,
            "order_id": order_id,
            "status": ORDERS[order_id]["status"],
            "product": ORDERS[order_id]["product"]  
         }



# Register the tools to be used by the LLM.
tools = [
    check_order_status, 
    check_product_stock, 
    check_delivery_info
    ]

# Tools dictionary
tools_by_name = {tool.name: tool for tool in tools}