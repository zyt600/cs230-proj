import json
import sys


def validate_json(data, output):
    try:
        json.loads(data)
        return True
    except Exception:
        return False
