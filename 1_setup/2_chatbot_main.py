# File: main.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Create llm
llm = ChatOllama(
        base_url="http://172.29.190.0:11434",
        model= "phi4:14b-q4_K_M",
        temperature=0.1,
        num_predict=128
        )

# Create prompt-template
prompt = ChatPromptTemplate.from_template(
    "What is :{term}?"
)

# Create chain (combine components)
chain = prompt | llm

while True:
    user_term = input("Write a term to get its definition. Exit 0: ")
    
    if user_term and user_term != "0":
        # Run the chain. Fill the placeholder text_from_user with text
        response = chain.invoke({"term": user_term})
        print(response.content)
