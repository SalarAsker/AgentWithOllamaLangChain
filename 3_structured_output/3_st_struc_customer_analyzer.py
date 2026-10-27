
import streamlit as st

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic_example import FeedbackAnalysis
from pydantic import ValidationError


# --------------------------------------------------
# 1. Streamlit page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Structured Feedback Analyzer",
    page_icon="📝",
    layout="centered"
)

st.title("Structured Customer Feedback Analyzer")

st.write(
    "Analyze customer feedback using Ollama, "
    "LangChain, and Pydantic."
)


# --------------------------------------------------
# 3. Initialize the LLM
# --------------------------------------------------

@st.cache_resource
def load_llm():
    return ChatOllama(
        base_url="http://172.29.190.0:11434",
        model="phi4:14b-q4_K_M",
        temperature=0.2,
        num_predict=256
    )

llm = load_llm()


# --------------------------------------------------
# 4. Configure structured output
# --------------------------------------------------

structured_llm = llm.with_structured_output(
    FeedbackAnalysis,
    method="json_schema"
)


# --------------------------------------------------
# 5. Create the prompt
# --------------------------------------------------

prompt = ChatPromptTemplate.from_template(
    """You are a customer feedback analyst.

Analyze the following customer feedback.

Instructions:
- Summarize the feedback concisely.
- Classify the overall sentiment.
- Identify only problems supported by the text.
- If no problems exist, return an empty list.
- Rate dissatisfaction severity from 1 to 5.
- Set follow_up_required to true when a
  customer service complaint needs attention.
- Do not invent information.

Customer feedback:
{feedback}"""
)


# --------------------------------------------------
# 6. Create the chain
# --------------------------------------------------

chain = prompt | structured_llm


# --------------------------------------------------
# 7. User interface
# --------------------------------------------------

feedback = st.text_area(
    "Enter customer feedback:",
    height=180,
    placeholder="Paste customer feedback here..."
)


# --------------------------------------------------
# 8. Execute the workflow
# --------------------------------------------------

if st.button("Analyze Feedback", type="primary"):

    if not feedback.strip():
        st.warning("Please enter customer feedback.")

    else:

        try:

            with st.spinner("Analyzing feedback..."):

                result = chain.invoke({
                    "feedback": feedback
                })

            st.success("Analysis completed!")

            # Summary
            st.subheader("Summary")
            st.write(result.summary)

            # Sentiment
            st.subheader("Sentiment")
            st.write(result.sentiment.capitalize())

            # Severity dissatisfaction
            st.subheader("Severity of Dissatisfaction")
            st.metric(
                label="Severity Score",
                value=f"{result.severity_dissatisfaction}/5"
            )

             # Severity satisfaction
            st.subheader("Severity of Satisfaction")
            st.metric(
                label="Severity Score",
                value=f"{result.severity_satisfaction}/5"
            )

            # Problems
            st.subheader("Identified Problems")

            if result.problems:
                for problem in result.problems:
                    st.write(f"- {problem}")
            else:
                st.write("No problems identified.")

            # Follow-up
            st.subheader("Follow-up Required")

            if result.follow_up_required:
                st.warning("Customer follow-up recommended.")
            else:
                st.info("No follow-up required.")

            # JSON output
            with st.expander("View Structured JSON"):
                st.json(result.model_dump())

        except ValidationError as error:
            st.error("The model output failed validation.")
            st.code(str(error))

        except Exception as error:
            st.error(f"Analysis failed: {error}")
