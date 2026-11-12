import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from ProductReviewSchema import ProductReviewAnalysis


# 2. Initialize the LLM 
llm = ChatOllama(
        base_url="http://172.29.190.0:11434",
        model= "phi4:14b-q4_K_M",
        temperature=0.2,
        num_predict=256
        )
# 3. Bind the Pydantic structure using with_structured_output
structured_llm = llm.with_structured_output(
    ProductReviewAnalysis,
    method="json_schema"
 )

# 4. Set up the Prompt Template
prompt = ChatPromptTemplate.from_template(
    """system", "You are an expert product review analyst. 
    Analyze the provided customer review and extract structured information 
    according to the requested schema.

    "human", "Product Review:\n{review}
    
    """
)

# Create chain
chain = prompt | structured_llm

# 5. Test with the 3 sample reviews
reviews = [
    {
        "id": 1,
        "text": "I recently picked up the SoundPulse Noise-Canceling Headphones and I'm really impressed. The active noise cancellation works like a charm on my daily commute, and the ear cushions are super comfortable even after hours of wear. The companion app also makes tweaking the EQ settings very easy. The only tiny downside is that the charging case feels a bit cheap and plasticky, but for under $150, I would definitely recommend these to anyone looking for great audio quality on a budget!"
    },
    {
        "id": 2,
        "text": "Purchased the KitchenPro Smart Espresso Maker two weeks ago. When it works, the espresso shots taste fantastic and the milk frother creates great microfoam. However, the setup was surprisingly frustrating because the Wi-Fi pairing kept dropping. It also takes almost 5 minutes to heat up in the morning, which is annoying when you're in a rush. Overall it's decent once you get used to its quirks, but I'm on the fence about whether it's worth the premium price tag."
    },
    {
        "id": 3,
        "text": "Avoid the FlexiDesk Ergonomic Wireless Mouse at all costs! The rubber grip started peeling off within three days of normal use. To make matters worse, the Bluetooth connection drops continuously while typing, causing huge lag spikes during work. Battery life is also nowhere near the advertised 30 days—I had to recharge it twice in one week. Requesting a full refund immediately."
    }
]

for review_item in reviews:
    print(f"\n==========================================")
    print(f" TESTING REVIEW #{review_item['id']}")
    print(f"==========================================")
    
    # Invoke the chain
    result: ProductReviewAnalysis = chain.invoke({"review": review_item["text"]})
    
    # Print individual fields
    print("\n--- Individual Fields ---")
    print(f"Product Name : {result.product_name}")
    print(f"Rating       : {result.rating} / 5")
    print(f"Sentiment    : {result.sentiment}")
    print(f"Advantages   : {', '.join(result.advantages)}")
    print(f"Disadvantages: {', '.join(result.disadvantages)}")
    print(f"Recommended  : {result.recommended}")
    
    # Display complete result as JSON
    # print("\n--- Complete JSON Output ---")
    # print(json.dumps(result.model_dump(), indent=4))