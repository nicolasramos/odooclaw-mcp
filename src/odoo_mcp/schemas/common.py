
from pydantic import BaseModel, Field


class BaseOdooRequest(BaseModel):
    """Base class providing optional caller context metadata."""

    sender_id: int | None = Field(
        None,
        description="Optional caller user ID for audit/context metadata. RPC execution runs as authenticated session user.",
    )
