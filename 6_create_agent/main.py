

# main.py

from agent import run

if __name__ == "__main__":

    questions = [
        "What is the status of order 1051?",

        "When will it arrive?"
    ]

    for question in questions:

        print("\n" + "=" * 50)

        print("Customer:")
        print(question)

        print("\nAssistant:")
        print(run(question))