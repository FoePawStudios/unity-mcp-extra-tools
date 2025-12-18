"""Delete a GameObject from the scene."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_gameobject_name


@mcp_for_unity_tool(
    name="delete_gameobject",
    description="Delete a GameObject from the scene. Use this to remove unwanted objects."
)
async def delete_gameobject(
    ctx: Context,
    target: Annotated[str, "GameObject name or path (required)"],
) -> dict[str, Any]:
    """Delete a GameObject from the scene."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs
    is_valid, error_msg = validate_gameobject_name(target)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid target GameObject name"}

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "delete",
        "target": target,
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_gameobject",
        params,
    )

