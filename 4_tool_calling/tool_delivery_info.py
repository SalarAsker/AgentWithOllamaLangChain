# File: tool_delivery_info.py
from langchain_core.tools import tool

DELIVERIES = {
    1051: "Delivered on 20 October",
    1052: "Expected delivery on 30 October",
    1053: "Not shipped yet"
}

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