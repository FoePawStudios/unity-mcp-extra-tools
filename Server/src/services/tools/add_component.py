"""Add a component to a GameObject."""

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
    name="add_component",
    description="Add a component to a GameObject. Use this to add functionality like physics, rendering, or custom scripts to GameObjects."
)
async def add_component(
    ctx: Context,
    target: Annotated[str, "GameObject name or path (required)"],
    componentName: Annotated[str, "Component type name, e.g., Rigidbody2D, SpriteRenderer (required)"],
    properties: Annotated[dict[str, Any] | str | None, "Initial component properties (optional)"] = None,
) -> dict[str, Any]:
    """Add a component to a GameObject."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs
    is_valid, error_msg = validate_gameobject_name(target)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid target GameObject name"}

    is_valid, error_msg = validate_component_type(componentName)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid component type"}

    # Parse properties if provided as string
    parsed_properties = None
    if properties:
        parsed_properties = parse_json_payload(properties)
        if parsed_properties is not None and not isinstance(parsed_properties, dict):
            return {"success": False, "message": "properties must be a JSON object (dict)"}

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "add_component",
        "target": target,
        "componentName": componentName,
    }

    # If properties provided, use componentProperties format expected by Unity bridge
    if parsed_properties:
        # Unity bridge expects componentProperties in format:
        # {"ComponentTypeName": {"property1": value1, "property2": value2}}
        params["componentProperties"] = {componentName: parsed_properties}

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_gameobject",
        params,
    )

