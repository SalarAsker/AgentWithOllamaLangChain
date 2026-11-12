# File: tool_check_order.py
from langchain_core.tools import tool

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