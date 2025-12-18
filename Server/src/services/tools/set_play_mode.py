"""Control Unity play mode (play, pause, stop)."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance


@mcp_for_unity_tool(
    name="set_play_mode",
    description="Control Unity play mode (play, pause, stop). Use this to test gameplay."
)
async def set_play_mode(
    ctx: Context,
    mode: Annotated[Literal["play", "pause", "stop"], "Play mode action (required)"],
) -> dict[str, Any]:
    """Control Unity play mode (play, pause, stop)."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs
    if not mode:
        return {"success": False, "message": "mode parameter is required"}

    if mode not in ("play", "pause", "stop"):
        return {"success": False, "message": f"Invalid mode: {mode}. Must be one of: play, pause, stop"}

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": mode,  # manage_editor expects action to be "play", "pause", or "stop"
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_editor",
        params,
    )

