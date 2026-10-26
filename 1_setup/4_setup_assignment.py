# File: main.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Create llm
llm = ChatOllama(
    base_url="http://192.168.0.126:11434",
    model="phi3:mini",  # or "llama3.2:3b"
    temperature=0.1
)


# Create prompt-template
prompt = ChatPromptTemplate.from_template(
    "Summarize this text in one sentence:\n{text_from_user}"
)

# Create chain (combine components)
chain = prompt | llm

# Run the chain. Fill the placeholder text_from_user with text
response = chain.invoke({"text_from_user": "LangChain was created to solve these issues. Langchain is a powerful framework designed to simplify the development of applications powered by large language models. It provides a set of tools, components, and interfaces that make it easy to build complex AI applications with features like memory, chains, and agents"})

print(response.content)




