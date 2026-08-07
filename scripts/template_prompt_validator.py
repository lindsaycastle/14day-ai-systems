from jsonschema import validate, ValidationError
import json

# schema = {'{'}
#     "type": "object",
#     "properties": {'{'}
#         "name": {'{'}"type": "string"{'}'},
#         "age": {'{'}"type": "integer", "minimum": 0{'}'}
#     {'}'},
#     "required": ["name", "age"]
# {'}'}

# data = {'{'}"name": "Alice", "age": 30{'}'}

schema = json.load(open("tests/prompt_library_schema.json"))

data = json.load(open("prompts/prompt_library.json"))

def validate_json(data, schema):
    try:
        validate(instance=data, schema=schema)
        print("Valid!")
    except ValidationError as e:
        print(f"Invalid: {e.message}")
