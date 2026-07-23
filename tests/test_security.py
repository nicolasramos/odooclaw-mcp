from unittest.mock import MagicMock

import pytest

from odoo_mcp.core.exceptions import OdooSecurityError
from odoo_mcp.core.security import validate_model_access, validate_unlink, validate_write_fields


def test_allowlist_success():
    # Should not raise
    validate_model_access("res.partner")
    validate_model_access("sale.order")


def test_allowlist_failure():
    with pytest.raises(OdooSecurityError):
        validate_model_access("ir.config_parameter")

    with pytest.raises(OdooSecurityError):
        validate_model_access("account.payment.term")


def test_denylist_success():
    # Safe fields, should not raise
    validate_write_fields({"name": "New partner", "email": "test@test.com"})


def test_denylist_failure():
    with pytest.raises(OdooSecurityError):
        validate_write_fields({"name": "New partner", "state": "done"})

    with pytest.raises(OdooSecurityError):
        validate_write_fields({"company_id": 1})


def test_unlink_blocked():
    with pytest.raises(OdooSecurityError):
        validate_unlink("res.partner")


class TestGuardWiring:
    """Verify that tool functions actually call guard_model_access and reject disallowed models."""

    def _make_client(self):
        client = MagicMock()
        client.odoo_session.uid = 1
        return client

    def test_odoo_search_rejects_disallowed_model(self):
        from odoo_mcp.tools.records import odoo_search

        with pytest.raises(OdooSecurityError):
            odoo_search(self._make_client(), 1, "ir.config_parameter", [], 10)

    def test_odoo_read_rejects_disallowed_model(self):
        from odoo_mcp.tools.records import odoo_read

        with pytest.raises(OdooSecurityError):
            odoo_read(self._make_client(), 1, "ir.ui.menu", [1])

    def test_odoo_search_read_rejects_disallowed_model(self):
        from odoo_mcp.tools.records import odoo_search_read

        with pytest.raises(OdooSecurityError):
            odoo_search_read(self._make_client(), 1, "res.groups", [], ["name"], 10)

    def test_odoo_model_schema_rejects_disallowed_model(self):
        from odoo_mcp.tools.introspection import odoo_model_schema

        client = self._make_client()
        with pytest.raises(OdooSecurityError):
            odoo_model_schema(client, 1, "ir.attachment")
