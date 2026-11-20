
# agent.py

from tools_all import tools_collection
from langchain_ollama import ChatOllama
from langchain.agents import create_agent


# -----------------------------------------
# 1. Initialize the language model
# -----------------------------------------

llm = ChatOllama(
    base_url="http://172.29.190.0:11434",
    model="qwen3.5:9b",
    temperature=0.2,
    num_predict=4000,
)

# -----------------------------------------
# 2. System instructions
# -----------------------------------------

SYSTEM_PROMPT = (
    "You are a customer service assistant. "
    "Use the available tools to answer questions "
    "about orders, products, and deliveries. "
    "Never invent order or stock information. "
    "When information from one tool is needed "
    "for another tool, retrieve it first. "
    "If information is unavailable, say so. "
    "The database is simulated for this lesson."
)

# -----------------------------------------
# 3. Create the LangChain agent
# -----------------------------------------

agent = create_agent(
    model=llm,
    tools=tools_collection,
    system_prompt=SYSTEM_PROMPT
)

# -----------------------------------------
# 4. Reusable run function
# -----------------------------------------

def run(user_question: str) -> str:
    from langgraph.errors import GraphRecursionError
    """
    Run the customer service agent.

    Args:
        user_question:
            The customer's question.

    Returns:
        str:
            The agent's final text answer.
    """

    if not user_question.strip():
        return "Please enter a question."
    try:
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_question
                    }
                ]
            },
            config={
                "recursion_limit": 12,
            }
        )
  
        final_message = result["messages"][-1]
        
        if isinstance(final_message.content, str):
            return final_message.content
        
        return str(final_message.content)
    
    except GraphRecursionError as e:
        return f"An error occurred: {e}"



    