import json
import re

# actions used in the action space of our work
ALLOWED_ACTIONS = {
    "click",
    "double_click",
    "right_click",
    "type",
    "hotkey",
    "scroll",
    "drag",
    "wait",
    "done",
    "fail",
}


def extract_json(text: str) -> dict:
    text = text.strip()

    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))

    m = re.search(r"(\{.*\})", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))

    raise ValueError("Could not parse JSON action.")


def validate_action(obj: dict) -> dict:
    if "action" not in obj:
        raise ValueError("Missing 'action' field.")
    if obj["action"] not in ALLOWED_ACTIONS:
        raise ValueError(f"Unsupported action: {obj['action']}")
    return obj
