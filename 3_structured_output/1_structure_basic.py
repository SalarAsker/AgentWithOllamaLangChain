import json

# Json text
json_text = """
{
    "summary": "Customer unhappy with delivery",
    "sentiment": "negative",
    "follow_up_required": true
}
"""
# Convert json to Python's dictionary
data = json.loads(json_text)

print(type(data))
print(data )
print(data["sentiment"])
print(data["follow_up_required"])

# Dictionar back to json
json_output = json.dumps(data, indent=4)

print(json_output)