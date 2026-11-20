# main.py
from rag import ask_rag

questions = [
    "How many days do I have to return a product?",
    "What happens if my laptop arrives damaged?",
    "How long does standard delivery take?",
    "What is the warranty period for laptops?",
    "Does the company offer free installation?"
]

for question in questions:

    print("\n" + "=" * 60)

    print("QUESTION:")
    print(question)

    print("\nANSWER:")
    print(ask_rag(question))

