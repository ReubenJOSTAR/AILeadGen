import re
import json
from typing import Tuple, Dict, Any


def extract_from_reply(raw_reply: str) -> Tuple[str, Dict[str, Any]]:
    match = re.search(r'<extract>(.*?)</extract>', raw_reply, re.DOTALL)

    if not match:
        return raw_reply.strip(), {}

    clean_reply = raw_reply[:match.start()].strip()
    json_str = match.group(1).strip()

    try:
        extracted_data = json.loads(json_str)
    except json.JSONDecodeError:
        extracted_data = {}

    if not isinstance(extracted_data, dict):
        extracted_data = {}

    return clean_reply, extracted_data


def is_conversation_complete(extracted_data: Dict[str, Any]) -> bool:
    value = extracted_data.get("is_complete", False)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return False
