
#File: simple_student.py
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


# 1. Initialize the model
llm = ChatOllama(
    base_url="http://172.29.190.0:11434",
    model="qwen3.5:9b",
    temperature=0.2
)

# 2. Create an in-memory checkpointer
checkpointer = InMemorySaver()

# 3. Create the agent
agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=(
        "You are a helpful assistant. "
        "Use the conversation history to "
        "answer follow-up questions."
    ),
    checkpointer=checkpointer
)


# 4. Define a conversation ID
config = {
    "configurable": {
        "thread_id": "student_001"
    }
}

# 5. First conversation turn
result1 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "My name is Alice. "
                    "My favorite programming "
                    "language is Python."
                )
            }
        ]
    },
    # same id to maintain the same conversation context
    config=config
)

print("First response:")
print(result1["messages"][-1].content)


# 6. Second conversation turn
result2 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "What is my favorite "
                    "programming language?"
                )
            }
        ]
    },
    # same id to maintain the same conversation context
    config=config
)

print("\nSecond response:")
print(result2["messages"][-1].content)

config = {
    "configurable": {
        "thread_id": "student_002"
    }
}


# 7. Third conversation turn
result3 = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "What is my name?"
                )
            }
        ]
    },
    # same id to maintain the same conversation context
    config=config 
)

print("\nThird response:")
print(result3["messages"][-1].content)
