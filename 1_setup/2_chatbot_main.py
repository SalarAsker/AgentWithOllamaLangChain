# File: main.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Create llm
llm = ChatOllama(
        # base_url="http://172.29.190.0:11434",
        # model= "phi4:14b-q4_K_M",
        base_url="http://192.168.0.126:11434",
        model="phi3:mini",  # or "llama3.2:3b"
        temperature=0.1,
        num_predict=128
        )

# Create prompt-template
prompt = ChatPromptTemplate.from_template(
    """What is {term}?
    Answer in plain text only. Do NOT use markdown, bold, bullet points, or special formatting.
    """
)

# Create chain (combine components)
chain = prompt | llm 

while True:
    user_term = input("Write a term to get its definition. Exit 0: ")

    if user_term == "0":
        print("Exiting...")
        break
    
    if user_term:
        # Run the chain. Fill the placeholder text_from_user with text
        response = chain.invoke({"term": user_term})
        print(response.content)

    
