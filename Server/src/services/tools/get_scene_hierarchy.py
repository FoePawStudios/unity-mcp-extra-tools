"""Get the hierarchy of GameObjects in the current scene."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance


@mcp_for_unity_tool(
    name="get_scene_hierarchy",
    description="Get the hierarchy of GameObjects in the current scene. Use this to see what objects exist in the scene."
)
async def get_scene_hierarchy(
    ctx: Context,
) -> dict[str, Any]:
    """Get the hierarchy of GameObjects in the current scene."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "get_hierarchy",
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_scene",
        params,
    )

