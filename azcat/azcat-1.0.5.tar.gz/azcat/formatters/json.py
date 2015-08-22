import json

def format (s):
    return "json", json.dumps(json.loads(s), indent=2)

