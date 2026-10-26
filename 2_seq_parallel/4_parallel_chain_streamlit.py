
import streamlit as st

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel


# Page configuration
st.set_page_config(
    page_title="Customer Feedback Analyzer",
    page_icon="📝",
    layout="centered"
)

st.title("Customer Feedback Analyzer")
st.write("Analyze customer feedback using Ollama and LangChain.")


# Initialize the local language model
@st.cache_resource
def load_llm():
    return ChatOllama(
        base_url="http://172.29.190.0:11434",
        model="phi4:14b-q4_K_M",
        temperature=0.2,
        num_predict=256
    )


llm = load_llm()


# Prompt 1: Summarize
p_summarize = ChatPromptTemplate.from_template(
    """Summarize this customer feedback in one sentence.

Feedback:
{feedback}

Return only the summary."""
)


# Prompt 2: Sentiment
p_sentiment = ChatPromptTemplate.from_template(
    """Determine the overall sentiment of this feedback.

Return exactly one of:
Positive
Neutral
Negative

Feedback:
{feedback}"""
)


# Prompt 3: Identify problems
p_problems = ChatPromptTemplate.from_template(
    """Identify the problems mentioned in this feedback.

Return a short bullet list.
If there are no problems, return 'None'.

Feedback:
{feedback}"""
)

p_response = ChatPromptTemplate.from_template(
    """Write a professional and empathetic response
to the customer using this analysis.

Summary:
{summary}

Sentiment:
{sentiment}

Problems:
{problems}

Acknowledge the concerns without inventing
refunds, promises, or company policies.

Return only the customer response."""
)

# Create individual chains
chain_summary = p_summarize | llm | StrOutputParser()
chain_sentiment = p_sentiment | llm | StrOutputParser()
chain_problems = p_problems | llm | StrOutputParser()


# User interface
feedback = st.text_area(
    "Enter customer feedback:",
    height=180,
    placeholder="Paste customer feedback here..."
)

st.subheader("Select analysis options")

col1, col2, col3 = st.columns(3)

with col1:
    summarize = st.checkbox("Summary", value=True)

with col2:
    sentiment = st.checkbox("Sentiment", value=True)

with col3:
    problems = st.checkbox("Problems", value=True)


btncol1, btncol2= st.columns(2)
# Button to execute the workflow
with btncol1:
    analyze = st.button("Analyze Feedback", type="primary", width=200)
with btncol2:
    generate = st.button("Generate Response", type="primary", width=200)

if analyze:

    if not feedback.strip():
        st.warning("Please enter customer feedback.")

    elif not any([summarize, sentiment, problems]):
        st.warning("Please select at least one analysis option.")

    else:
        # Build only the selected chains
        selected_chains = {}

        if summarize:
            selected_chains["summary"] = chain_summary

        if sentiment:
            selected_chains["sentiment"] = chain_sentiment

        if problems:
            selected_chains["problems"] = chain_problems

        # Combine selected chains in parallel
        # dictionary unpacking
        chain_final = RunnableParallel(selected_chains)

        # Execute workflow
        try:
            with st.spinner("Analyzing feedback..."):
                result = chain_final.invoke({
                    "feedback": feedback
                })

            st.success("Analysis completed!")

            # Display only selected results
            if "summary" in result:
                st.subheader("Summary")
                st.write(result["summary"])

            if "sentiment" in result:
                st.subheader("Sentiment")
                st.write(result["sentiment"])

            if "problems" in result:
                st.subheader("Identified Problems")
                st.write(result["problems"])

        except Exception as e:
            st.error(f"Analysis failed: {e}")

elif generate:
            
            response_chain = p_response | llm | StrOutputParser()
            with st.spinner("Generating response..."):


                chain_final = RunnableParallel(
                   summary=chain_summary,
                   sentiment=chain_sentiment,
                   problems=chain_problems
                   )
                
                complete_response_chain = chain_final | response_chain
              
                answer = complete_response_chain.invoke({
                    "feedback": feedback
                })
            st.markdown(f"**Response to customer :**\n\n{answer}")