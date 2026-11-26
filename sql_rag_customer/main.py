
# main.py
from agent import run

if __name__ == "__main__":

    questions = [
        "What is the status of order 1001?",
        "When will it arrive? "
        "How long does standard delivery take?",
        "What product is included in order "
        "1006, and how many units are in stock?",
        "What is the warranty period for laptops?",
        "Does the company offer free installation?"
    ]

    for question in questions:

        print("\n" + "=" * 50)

        print("Customer:")
        print(question)

        print("\nAssistant:")
        print(run(question))