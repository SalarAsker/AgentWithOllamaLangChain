
# customer_service_assistant.py
# Import all the tools
from tool_check_order import check_order_status
from tool_products_stock import check_product_stock
from tool_delivery_info import check_delivery_info

# Import the necessary classes from langchain_core
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import (SystemMessage,HumanMessage,ToolMessage)




# Initialize the local language model
llm = ChatOllama(
        base_url="http://172.29.190.0:11434",
        # model= "llama3.2:3b",
        model= "qwen3.5:9b",
        temperature=0.2,
        num_predict=256
        )

# Bind the tools to the LLM. 
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = (
    "You are a customer service assistant. "
    "Use the available tools to answer questions "
    "about orders, products, and deliveries. "
    "Never invent order or stock information. "
    "The database is simulated for this lesson."
)

# Define a function to run the customer service assistant with the provided user question.
def run(user_question: str) -> str:
    """
    Run the customer service assistant with the provided user question.
    
    Args:
        user_question (str): The question from the user.
        
    Returns:
        str
    """
    # Add the user's question to the messages list.
    messages = [
    SystemMessage( content=SYSTEM_PROMPT),
    HumanMessage(content=user_question)
    ] 

    # Aske the llm to select the tools
    tools_req_response = llm_with_tools.invoke(messages)
    
    # Save the tool request response AIMessage to the messges list. 
    messages.append(tools_req_response)

    # If there is no tool is requested. 
    # User asked a question that can be answered without any tool.
    # Tell me a joke about a cat.
    if not tools_req_response.tool_calls:
        return tools_req_response.content

    # Execute a the tool request and get the tool response.
    # Save the result as ToolMessage in the messages list. This allows for a complete conversation history.

    if tools_req_response.tool_calls:
        
        for requested_tool in tools_req_response.tool_calls:
            
            # tool_name = requested_tool["name"]
            # tool_args = requested_tool["args"]

            # Retrieve the corresponding tool function based on the tool name.
            selected_tool = tools_by_name.get(requested_tool["name"])

            if selected_tool is None:
                tool_result = ToolMessage(
                    content=f"Unknown tool '{requested_tool['name']}', tool id '{requested_tool['id']}'." )
        
            else:
                try:
                    # Invoking a tool with a full tool-call dict returns a ToolMessage
                    tool_result = selected_tool.invoke(requested_tool)
                    # print(tool_result)
                except Exception as e:
                    tool_result = ToolMessage(
                        content=f"Tool execution failed: error: {str(e)}"
                    )
        
            # Save the ToolMessage result to the messages list.
            messages.append(tool_result)

    # Generate the final response 
    final_response = llm_with_tools.invoke(messages)

    if final_response.tool_calls:
        return(f"The model requested additional tools: {final_response.tool_calls}. "
                f"We only implements the one tool call round only.")
    else:
        return final_response.content

# Prompt calling example
if __name__ == "__main__":
   print(run("What is the status of order 1051?"))
   print(run("Tell a joke about a customer service assistant."))
    