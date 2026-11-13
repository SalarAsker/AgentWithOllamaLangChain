
# agent.py
# Import all the tools
from tools_all import tools, tools_by_name
from langchain_ollama import ChatOllama
from langchain_core.messages import (SystemMessage,HumanMessage,ToolMessage)



# Initialize the local language model
llm = ChatOllama(
        base_url="http://172.29.190.0:11434",
        # base_url="http://192.168.0.126:11434",
        # model= "llama3.2:3b",
        # model= "qwen3.5:9b",
        model = "qwen3.5:9b",
        # model = "qwen3.6:latest",
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
def run(user_question: str, max_tool_rounds: int=5) -> str:
    tool_call_stats  = []
    """
    Run the customer service assistant.

    The function repeatedly invokes the LLM,executes requested tools, and returns
    observations until the model produces a final answer or reaches the execution limit.

    Args:
        user_question:
            The customer's question.

        max_tool_rounds:
            Maximum number of tool execution
            rounds allowed.

    Returns:
        str:
            Final answer or stopping message.
    """
    # Add the user's question to the messages list.
    messages = [
    SystemMessage( content=SYSTEM_PROMPT),
    HumanMessage(content=user_question)
    ] 

    # Count completed tool execution rounds
    tool_rounds = 0

    while True:
        # Aske the llm to select the tools
        tools_req_response = llm_with_tools.invoke(messages)    
        # Save the tool request response AIMessage to the messges list. 
        messages.append(tools_req_response)

        # If there is no tool is requested. return the final response
        if not tools_req_response.tool_calls:
            return (tools_req_response.content, tool_call_stats)

        if tool_rounds >= max_tool_rounds:
            return(f"Maximum tool execution rounds ({max_tool_rounds}) reached. "
                    f"Stopping execution to prevent infinite loop.")

         # Count this tool round
        tool_rounds += 1

        # Execute a the tool request and get the tool response.
        if tools_req_response.tool_calls:
            
            for requested_tool in tools_req_response.tool_calls:
       
                # Retrieve the corresponding tool function based on the tool name.
                selected_tool = tools_by_name.get(requested_tool["name"])
                # print(selected_tool,"\n\n")
                tool_call_stats.append(selected_tool)
                if selected_tool is None:
                    tool_result = ToolMessage(
                        content=f"Unknown tool '{requested_tool['name']}', tool id '{requested_tool['id']}'." )
            
                else:
                    try:
                        # Invoking a tool with a full tool-call dict returns a ToolMessage
                        tool_result = selected_tool.invoke(requested_tool)
                        # print(requested_tool)
                        # print(tool_result)
                    except Exception as e:
                        tool_result = ToolMessage(
                            content=f"Tool execution failed: error: {str(e)}"
                        )
            
                # Save the ToolMessage result to the messages list.
                messages.append(tool_result)

  

