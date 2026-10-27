from pydantic_example import FeedbackAnalysis
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import ValidationError
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnableParallel


feedback = """
Honestly, this overall experience was really frustrating. The product itself seems decent enough, but getting it was an absolute nightmare. Delivery took way longer than estimated, and when I tried reaching out for updates, the customer support team took forever to respond and gave completely unhelpful answers. For this price, the terrible service completely ruined the purchase.
"""

# Initialize the local language model
llm = ChatOllama(
        base_url="http://172.29.190.0:11434",
        model= "phi4:14b-q4_K_M",
        temperature=0.2,
        num_predict=256
        )

#  Configure structured output
structured_llm = llm.with_structured_output(
    FeedbackAnalysis,
    method="json_schema"
)

# Create prompt
prompt = ChatPromptTemplate.from_template(
    """Analyze the following customer feedback.

Return a concise summary, overall sentiment,
problems mentioned, and whether follow-up
is required.

Return also the severity of dissatisfaction and satisfaction
on a scale of 1 to 5

Set follow_up_required to true when the
feedback contains a service complaint.

If no problems are mentioned, return
an empty list.

Feedback:
{feedback}"""
)

# Create individual chains
chain = prompt | structured_llm

# Execute the workflow
try:
    result = chain.invoke({
        "feedback": feedback
    })
except ValidationError as error:
    print(f"Validation error occurred: {error}")
except Exception as error:
    print(f"An error occurred: {error}")

# Access the fields
print("Summary:", result.summary)
print("\nSentiment:", result.sentiment)
print("\nProblems:", result.problems)
print("\nFollow-up required:", result.follow_up_required)
print("\nSeverity of dissatisfaction:", result.severity_dissatisfaction)
print("\nSeverity of satisfaction:", result.severity_satisfaction)
