"""Add a layer to the project."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance


@mcp_for_unity_tool(
    name="add_layer",
    description="Add a layer to the project. Use this to create custom layers for GameObjects."
)
async def add_layer(
    ctx: Context,
    layer_name: Annotated[str, "Layer name to add (required)"],
) -> dict[str, Any]:
    """Add a layer to the project."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Validate inputs
    if not layer_name:
        return {"success": False, "message": "layer_name parameter is required"}

    if not isinstance(layer_name, str) or len(layer_name.strip()) == 0:
        return {"success": False, "message": "layer_name must be a non-empty string"}

    # Transform simplified parameters to Unity bridge format (camelCase)
    params: dict[str, Any] = {
        "action": "add_layer",
        "layerName": layer_name,  # Map layer_name to layerName
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_editor",
        params,
    )

