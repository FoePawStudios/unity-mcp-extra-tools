"""Add a tag to the project."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance


@mcp_for_unity_tool(
    name="add_tag",
    description="Add a tag to the project. Use this to create custom tags for GameObjects."
)
async def add_tag(
    ctx: Context,
    tag_name: Annotated[str, "Tag name to add (required)"],
) -> dict[str, Any]:
    """Add a tag to the project."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs
    if not tag_name:
        return {"success": False, "message": "tag_name parameter is required"}

    if not isinstance(tag_name, str) or len(tag_name.strip()) == 0:
        return {"success": False, "message": "tag_name must be a non-empty string"}

    # Transform simplified parameters to Unity bridge format (camelCase)
    params: dict[str, Any] = {
        "action": "add_tag",
        "tagName": tag_name,  # Map tag_name to tagName
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_editor",
        params,
    )

