
from odoo_mcp.config import DEFAULT_ALLOWED_MODELS, DEFAULT_DENIED_FIELDS


def get_allowed_models() -> set[str]:
    """Returns the set of models the MCP is authorized to interact with."""
    return DEFAULT_ALLOWED_MODELS


def get_denied_write_fields() -> set[str]:
    """Returns the set of fields that cannot be written directly by tools."""
    return DEFAULT_DENIED_FIELDS
