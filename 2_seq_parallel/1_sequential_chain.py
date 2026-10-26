from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda


feedback = """
Honestly, this overall experience was really frustrating. The product itself seems decent enough, but getting it was an absolute nightmare. Delivery took way longer than estimated, and when I tried reaching out for updates, the customer support team took forever to respond and gave completely unhelpful answers. For this price, the terrible service completely ruined the purchase.
"""

# Create llm
llm = ChatOllama(
        base_url="http://172.29.190.0:11434",
        model= "phi4:14b-q4_K_M",
        temperature=0.2,
        num_predict=256
        )

# Step 1: Summarize
summary_prompt = ChatPromptTemplate.from_template(
    """Summarize this text. Feedback:\n
{feedback}
"""
)

# Step 2: Translate
translation_prompt = ChatPromptTemplate.from_template(
    """Translate this text into Swedish.Text:\n
{summary_prompt}
"""
)

# Step 3: Generate title
title_prompt = ChatPromptTemplate.from_template(
    """Generate a short Swedish title for this text.

    Your task is to generate ONE short title in Swedish.

Rules:
- Write ONLY in Swedish.
- Return ONLY the title.
- Do not translate into any other language.
- Do not include explanations or additional text.    

Text:\n
{translation}
"""
)

# Individual chains
summary_chain = summary_prompt | llm 
translation_chain = translation_prompt | llm
title_chain = title_prompt | llm

# Extract content between chains
get_content = RunnableLambda(lambda message: message.content)

# Connect sequentially
final_chain = summary_chain |get_content | translation_chain | get_content | title_chain

# Feedback is assign only to the first chain, i.e. summary_chain
result = final_chain.invoke({
    "feedback": feedback
})

print(result.content)
