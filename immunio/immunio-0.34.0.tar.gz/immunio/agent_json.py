"""
Utility module for JSON encoding and decoding for the agent. Handles
encoding and decoding UUID objects.
"""
import json
import uuid


class AgentEncoder(json.JSONEncoder):
    """
    Custom encoder. Encodes UUID objects as strings.
    """
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def object_hook(json_dict):
    """
    Custom decoder hook. Searches dict for values that look like UUIDs
    and parses them.
    """
    for key, value in json_dict.items():
        # Pre-screen for potential UUIDs
        if isinstance(value, basestring) and len(value) == 36:
            try:
                # Try to parse UUID, ignore if it fails.
                json_dict[key] = uuid.UUID(value)
            except ValueError:
                pass
    return json_dict


def dumps(obj):
    """
    Custom JSON encoder that handles UUID objects.
    """
    return json.dumps(obj, cls=AgentEncoder, separators=(',', ':',),
                      sort_keys=True)


def loads(string):
    """
    Custom JSON decoder that handles UUIDs.
    """
    return json.loads(string, object_hook=object_hook)
