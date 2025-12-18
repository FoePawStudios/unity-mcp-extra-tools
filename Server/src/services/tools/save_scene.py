"""Save the current scene."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_scene_path


@mcp_for_unity_tool(
    name="save_scene",
    description="Save the current scene. Use this to persist scene changes."
)
async def save_scene(
    ctx: Context,
    path: Annotated[str | None, "Optional: save with new path/name"] = None,
) -> dict[str, Any]:
    """Save the current scene."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate path if provided
    if path:
        is_valid, error_msg = validate_scene_path(path)
        if not is_valid:
            return {"success": False, "message": error_msg or "Invalid scene path"}

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "save",
    }

    if path:
        params["path"] = path

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_scene",
        params,
    )

