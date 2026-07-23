from typing import Any


def serialize_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Clean up standard record reads."""
    res = []
    for r in records:
        cleaned = {}
        for k, v in r.items():
            # Example: clean up binary data or long html
            if isinstance(v, str) and len(v) > 2000 and "html" in k.lower():
                cleaned[k] = f"<{len(v)} bytes of HTML content omitted>"
            else:
                cleaned[k] = v
        res.append(cleaned)
    return res

def serialize_schema(schema: dict[str, Any]) -> str:
    """Minify the schema output so it does not overwhelm the LLM token context."""
    import json
    # You could filter out base fields (create_date etc.) if not requested
    return json.dumps(schema, indent=2)
