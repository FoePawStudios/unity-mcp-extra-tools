"""Set a single property on a component."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import parse_json_payload
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_component_type, validate_gameobject_name


@mcp_for_unity_tool(
    name="set_component_property",
    description="Set a single property on a component. Use this to configure component values after creation."
)
async def set_component_property(
    ctx: Context,
    target: Annotated[str, "GameObject name or path (required)"],
    component_type: Annotated[str, "Component type name (required)"],
    property: Annotated[str, "Property name, use dot notation for nested (e.g., sharedMaterial.color) (required)"],
    value: Annotated[Any, "Property value (required)"],
) -> dict[str, Any]:
    """Set a single property on a component."""
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

    if not property:
        return {"success": False, "message": "property parameter is required"}

    # Parse value if it's a string (might be JSON)
    parsed_value = parse_json_payload(value) if isinstance(value, str) else value

    # Transform simplified parameters to Unity bridge format
    # Unity bridge expects component_properties in format:
    # {"ComponentTypeName": {"property.path": value}}
    params: dict[str, Any] = {
        "action": "set_component_property",
        "target": target,
        "component_name": component_type,  # Map component_type to component_name
        "component_properties": {component_type: {property: parsed_value}},
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_gameobject",
        params,
    )

