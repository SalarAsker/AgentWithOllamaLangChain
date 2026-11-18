# File: main.py
from agent import run

thread_id = "customer_session_001"


print("\nCUSTOMER:")
print("What is the status of order 1053?")

print("\nASSISTANT:")
print(run("What is the status of order 1053?",thread_id)
)


print("\nCUSTOMER:")
print("When will it arrive?")

print("\nASSISTANT:")
print(run("When will it arrive?",thread_id))


print("\nCUSTOMER:")
print("Which product did I order?")

print("\nASSISTANT:")
print(run("Which product did I order?",thread_id))

print("\nASSISTANT:")
print(run("Which product did I order?","customer_session_002"))