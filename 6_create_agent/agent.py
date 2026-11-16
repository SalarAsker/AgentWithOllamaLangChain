
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from tools_calc import tools_collection  # Import the list directly


# Initialize the local language model
llm = ChatOllama(
    base_url="http://192.168.0.126:11434",
    model="llama3.2:3b",
    temperature=0.2
)

# Create an agent with the LLM and tools
agent = create_agent(
    model=llm, 
    tools=tools_collection,
    system_prompt= (
        "You are a calculator assistant. "
        "Use the available tools to perform calculations. "
        "Never invent calculation results. "
     )
    )  

# invoke the agent with a user question
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is 17 multiplied by 23 and then divided by 5 added to 10 and subtracted by 3?"
            }
        ]
    }
)

print(result["messages"][-1].content)


# # Invoke the agent with a user question
# def run(user_question: str) -> str:
#     """
#     Run the calculator assistant with the provided user question.
    
#     Args:
#         user_question (str): The question from the user.
        
#     Returns:
#         str
#     """
#     # Add the user's question to the messages list.
#     messages = [
#         {"role": "user", 
#          "content": user_question}
#     ]

#     # Invoke the agent with the messages
#     response = agent.invoke(messages)

#     # Return the final answer from the agent's response
#     return response["content"]
