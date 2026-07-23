from typing import Any

from odoo_mcp.config import DEFAULT_SEARCH_LIMIT, MAX_SEARCH_LIMIT
from odoo_mcp.core.client import OdooClient
from odoo_mcp.core.domains import validate_domain
from odoo_mcp.core.serializers import serialize_records
from odoo_mcp.security.audit import audit_action
from odoo_mcp.security.guards import guard_model_access, guard_write_fields
from odoo_mcp.services.partner_service import find_existing_partner_id


def _clamp_limit(limit: int) -> int:
    """Clamp limit to MAX_SEARCH_LIMIT, treating <=0 as DEFAULT_SEARCH_LIMIT."""
    if limit <= 0:
        return DEFAULT_SEARCH_LIMIT
    return min(limit, MAX_SEARCH_LIMIT)


def odoo_search(
    client: OdooClient, user_id: int, model: str, domain: list[Any], limit: int
) -> list[int]:
    """Search for record IDs matching domain."""
    guard_model_access(model)
    validate_domain(domain)
    limit = _clamp_limit(limit)
    return client.call_kw(model, "search", args=[domain], kwargs={"limit": limit})


def odoo_read(
    client: OdooClient,
    user_id: int,
    model: str,
    ids: list[int],
    fields: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Read fields for a list of record IDs."""
    guard_model_access(model)
    kwargs = {"fields": fields} if fields else {}
    records = client.call_kw(model, "read", args=[ids], kwargs=kwargs)
    return serialize_records(records)


def odoo_search_read(
    client: OdooClient,
    user_id: int,
    model: str,
    domain: list[Any],
    fields: list[str] | None = None,
    limit: int = DEFAULT_SEARCH_LIMIT,
) -> list[dict[str, Any]]:
    """Search and read in a single call."""
    guard_model_access(model)
    validate_domain(domain)
    limit = _clamp_limit(limit)
    kwargs = {"limit": limit}
    if fields:
        kwargs["fields"] = fields
    records = client.call_kw(model, "search_read", args=[domain], kwargs=kwargs)
    return serialize_records(records)


def odoo_create(client: OdooClient, user_id: int, model: str, values: dict[str, Any]) -> int:
    """Create a new record after checking allowlist."""
    guard_model_access(model)
    audit_action("CREATE", user_id, model, [], values)

    if model == "res.partner":
        existing_partner_id = find_existing_partner_id(
            client,
            user_id,
            name=values.get("name"),
            vat=values.get("vat"),
            email=values.get("email"),
            allow_fuzzy_name=False,
        )
        if existing_partner_id:
            return existing_partner_id

    return client.call_kw(model, "create", args=[values])


def odoo_write(
    client: OdooClient, user_id: int, model: str, ids: list[int], values: dict[str, Any]
) -> bool:
    """Update records, respecting denylists and allowlists."""
    guard_model_access(model)
    guard_write_fields(values)
    audit_action("WRITE", user_id, model, ids, values)
    return client.call_kw(model, "write", args=[ids, values])
