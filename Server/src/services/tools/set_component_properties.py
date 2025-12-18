"""Set multiple properties on a component at once."""

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
    name="set_component_properties",
    description="Set multiple properties on a component at once. Use this when configuring multiple properties to avoid multiple calls."
)
async def set_component_properties(
    ctx: Context,
    target: Annotated[str, "GameObject name or path (required)"],
    component_type: Annotated[str, "Component type name (required)"],
    properties: Annotated[dict[str, Any] | str, "Dictionary of property names to values (required)"],
) -> dict[str, Any]:
    """Set multiple properties on a component at once."""
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

    # Parse properties if provided as string
    parsed_properties = parse_json_payload(properties)
    if not isinstance(parsed_properties, dict):
        return {"success": False, "message": "properties must be a JSON object (dict)"}

    if not parsed_properties:
        return {"success": False, "message": "properties dictionary cannot be empty"}

    # Transform simplified parameters to Unity bridge format
    # Unity bridge expects component_properties in format:
    # {"ComponentTypeName": {"property1": value1, "property2": value2}}
    params: dict[str, Any] = {
        "action": "set_component_property",
        "target": target,
        "component_name": component_type,  # Map component_type to component_name
        "component_properties": {component_type: parsed_properties},
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_gameobject",
        params,
    )

