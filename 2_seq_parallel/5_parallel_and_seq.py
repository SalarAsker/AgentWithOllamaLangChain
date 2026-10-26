from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


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

# Prompt 1: Summarize
p_summarize = ChatPromptTemplate.from_template(
    """Summarize this customer feedback in one sentence.

Feedback:
{feedback}

Return only the summary.
"""
)

# Prompt 2: Sentiment
p_sentiment = ChatPromptTemplate.from_template(
    """Determine the overall sentiment of this feedback.

Return exactly one of:
Positive
Neutral
Negative

Feedback:
{feedback}
"""
)

# Prompt 3: Identify problems
p_problems = ChatPromptTemplate.from_template(
    """Identify the problems mentioned in this feedback.

Return a short bullet list.
If there are no problems, return 'None'.

Feedback:
{feedback}
"""
)

# Create individual chains
chain_summary = p_summarize | llm | StrOutputParser()

chain_sentiment = p_sentiment | llm | StrOutputParser()

chain_problems = p_problems | llm | StrOutputParser()

# Combine the three chains using RunnableParallel.
chain_final = RunnableParallel(
    summary=chain_summary,
    sentiment=chain_sentiment,
    problems=chain_problems
)

# Add after defining chain_final in Section 4.4

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

response_chain = ( p_response | llm   | StrOutputParser()
)

# Parallel analysis followed by response generation
# complete_chain = chain_final | response_chain

complete_chain = ( chain_final | RunnablePassthrough.assign( response=response_chain ) )


result = complete_chain.invoke({
    "feedback": feedback
})


print("\nSummary\n",result["summary"])
print("\nSentiment\n",result["sentiment"])
print("\nProblems\n",result["problems"])
print("\nResponse\n",result["response"])


# # Execute the workflow
# result = chain_final.invoke({
#     "feedback": feedback
# })

# print("Summary:")
# print(result["summary"])

# print("\nSentiment:")
# print(result["sentiment"])

# print("\nProblems:")
# print(result["problems"])