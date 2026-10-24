# File: main.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st


# Model
models = {
    "Phi4Q4": "phi4:14b-q4_K_M",
    "Phi4Q8": "phi4:14b-q8_0"
}

selected_model = st.selectbox(
                "Select a model? default Phi4Q4",
                ("Phi4Q4","Phi4Q8"),
                index=0
)

# Create llm, model Phi4 is alwasy selected so can create the llm
# without controlling the selected_model.
llm = ChatOllama(
        base_url="http://172.29.190.0:11434",
        model= models[selected_model],
        temperature=0.1,
        num_predict=128
        )

# Create prompt
prompt = ChatPromptTemplate.from_template(
        "What is :{term}?"
         )

# Create chain (combine components)
chain = prompt | llm
        
#  User input
user_term = st.text_input("Enter a term to get its definition:")

if st.button("Get Definition") and user_term:
    with st.spinner("Thinking..."):
        try:
            # Run the chain. Fill the placeholder text_from_user with text
            response = chain.invoke({"term": user_term})
            st.markdown(response.content)  
        except Exception as e:
            st.error(f"An error occurred: {e}")

