"""Save changes made to the currently open prefab."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance


@mcp_for_unity_tool(
    name="save_prefab",
    description="Save changes made to the currently open prefab. Use this after modifying a prefab in isolation mode."
)
async def save_prefab(
    ctx: Context,
) -> dict[str, Any]:
    """Save changes made to the currently open prefab."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "save_open_stage",
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_prefabs",
        params,
    )

