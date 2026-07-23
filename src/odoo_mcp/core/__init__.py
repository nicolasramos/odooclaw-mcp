"""Core layer - Base technical components for Odoo RPC communication."""

from odoo_mcp.core.client import OdooClient
from odoo_mcp.core.exceptions import (
    OdooAuthError,
    OdooMCPError,
    OdooRPCError,
    OdooSecurityError,
)
from odoo_mcp.core.session import OdooSession

__all__ = [
    "OdooMCPError",
    "OdooAuthError",
    "OdooSecurityError",
    "OdooRPCError",
    "OdooSession",
    "OdooClient",
]
