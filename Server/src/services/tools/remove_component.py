"""Remove a component from a GameObject."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_component_type, validate_gameobject_name


@mcp_for_unity_tool(
    name="remove_component",
    description="Remove a component from a GameObject. Use this to remove unwanted components."
)
async def remove_component(
    ctx: Context,
    target: Annotated[str, "GameObject name or path (required)"],
    component_type: Annotated[str, "Component type name to remove (required)"],
) -> dict[str, Any]:
    """Remove a component from a GameObject."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Validate inputs
    is_valid, error_msg = validate_gameobject_name(target)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid target GameObject name"}

    is_valid, error_msg = validate_component_type(component_type)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid component type"}

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "remove_component",
        "target": target,
        "component_name": component_type,  # Map component_type to component_name
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_gameobject",
        params,
    )

