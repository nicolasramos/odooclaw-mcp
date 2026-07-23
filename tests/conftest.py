"""Pytest configuration and fixtures for Odoo MCP Server tests."""

import os
from collections.abc import Generator
from unittest.mock import patch

import pytest

from odoo_mcp.config import DEFAULT_SEARCH_LIMIT
from odoo_mcp.core import OdooClient, OdooSession


@pytest.fixture
def mock_odoo_url() -> str:
    """Mock Odoo URL for testing."""
    return "https://test.odoo.com"


@pytest.fixture
def mock_odoo_db() -> str:
    """Mock Odoo database name for testing."""
    return "test_db"


@pytest.fixture
def mock_odoo_user() -> str:
    """Mock Odoo username for testing."""
    return "test_user"


@pytest.fixture
def mock_odoo_password() -> str:
    """Mock Odoo password for testing."""
    return "test_password"


@pytest.fixture
def mock_test_user_id() -> int:
    """Mock test user ID for testing."""
    return 42


@pytest.fixture
def mock_odoo_session(
    mock_odoo_url: str,
    mock_odoo_db: str,
    mock_odoo_user: str,
    mock_odoo_password: str,
) -> OdooSession:
    """Create a mock Odoo session for testing."""
    session = OdooSession(
        url=mock_odoo_url,
        db=mock_odoo_db,
        username=mock_odoo_user,
        password=mock_odoo_password,
    )
    # Mock authenticated state
    session.uid = 1
    session.session_id = "test_session_id"
    session.context = {"lang": "en_US", "tz": "UTC"}
    return session


@pytest.fixture
def mock_odoo_client(mock_odoo_session: OdooSession) -> OdooClient:
    """Create a mock Odoo client for testing."""
    return OdooClient(session=mock_odoo_session)


@pytest.fixture
def env_vars_mock(
    mock_odoo_url: str,
    mock_odoo_db: str,
    mock_odoo_user: str,
    mock_odoo_password: str,
) -> Generator[dict, None, None]:
    """Mock environment variables for Odoo connection."""
    env_vars = {
        "ODOO_URL": mock_odoo_url,
        "ODOO_DB": mock_odoo_db,
        "ODOO_USERNAME": mock_odoo_user,
        "ODOO_PASSWORD": mock_odoo_password,
        "ODOO_MCP_DEFAULT_LIMIT": str(DEFAULT_SEARCH_LIMIT),
        "ODOO_MCP_MAX_LIMIT": "80",
    }

    with patch.dict(os.environ, env_vars, clear=True):
        yield env_vars


@pytest.fixture
def mock_odoo_response() -> dict:
    """Mock a successful Odoo RPC response."""
    return {
        "jsonrpc": "2.0",
        "id": None,
        "result": [
            {
                "id": 1,
                "name": "Test Partner",
                "email": "test@example.com",
            }
        ],
    }


@pytest.fixture
def mock_search_result() -> list:
    """Mock a typical Odoo search result."""
    return [1, 2, 3]


@pytest.fixture
def mock_read_result() -> list:
    """Mock a typical Odoo read result."""
    return [
        {
            "id": 1,
            "name": "Test Record 1",
            "date": "2024-01-01",
        },
        {
            "id": 2,
            "name": "Test Record 2",
            "date": "2024-01-02",
        },
    ]
