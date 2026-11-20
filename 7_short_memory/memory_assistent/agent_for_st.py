# st_agent.py
from tools_all import tools_collection
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

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


def create_customer_service_agent():

    llm = ChatOllama(
        # base_url="http://172.29.190.0:11434",
        # model="qwen3.5:9b",
        base_url="http://192.168.9.145:11434",
        model ="llama3.2:3b",
        temperature=0.2,
        num_predict=256
    )

    checkpointer = InMemorySaver()

    return create_agent(
        model=llm,
        tools=tools_collection,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer
    )