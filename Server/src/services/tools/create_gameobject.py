"""Create a new GameObject in the current scene."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import coerce_bool, parse_json_payload
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_gameobject_name
from .value_parser import parse_vector3


@mcp_for_unity_tool(
    name="create_gameobject",
    description="Create a new GameObject in the current scene. Use this when you need to add a new object to the scene hierarchy."
)
async def create_gameobject(
    ctx: Context,
    name: Annotated[str, "GameObject name (required)"],
    position: Annotated[list[float] | str | None, "World position as array [x, y, z] or JSON array string '[x, y, z]' (required brackets, not comma-separated) (optional, default: [0, 0, 0])"] = None,
    rotation: Annotated[list[float] | str | None, "Euler rotation as array [x, y, z] or JSON array string '[x, y, z]' (required brackets, not comma-separated) in degrees (optional, default: [0, 0, 0])"] = None,
    scale: Annotated[list[float] | str | None, "Scale as array [x, y, z] or JSON array string '[x, y, z]' (required brackets, not comma-separated) (optional, default: [1, 1, 1])"] = None,
    parent: Annotated[str | None, "Parent GameObject name or path (optional)"] = None,
    tag: Annotated[str | None, "Tag name (optional)"] = None,
    layer: Annotated[str | None, "Layer name (optional)"] = None,
    setActive: Annotated[bool | str | None, "Set active state (optional, default: true)"] = None,
    primitiveType: Annotated[str | None, "Create primitive shape: Cube, Sphere, Capsule, Cylinder, Plane, Quad (optional)"] = None,
) -> dict[str, Any]:
    """Create a new GameObject in the current scene."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs
    is_valid, error_msg = validate_gameobject_name(name)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid GameObject name"}

    # Parse vector parameters with validation
    parsed_position = parse_vector3(position)
    if position is not None and parsed_position is None:
        return {"success": False, "message": "Position must be an array [x, y, z] or JSON array string '[x, y, z]', not a comma-separated string"}
    
    parsed_rotation = parse_vector3(rotation)
    if rotation is not None and parsed_rotation is None:
        return {"success": False, "message": "Rotation must be an array [x, y, z] or JSON array string '[x, y, z]', not a comma-separated string"}
    
    parsed_scale = parse_vector3(scale)
    if scale is not None and parsed_scale is None:
        return {"success": False, "message": "Scale must be an array [x, y, z] or JSON array string '[x, y, z]', not a comma-separated string"}
    
    # Parse active state - only use default if not explicitly provided
    parsed_active = coerce_bool(setActive) if setActive is not None else None
    
    # Validate primitive type if provided
    valid_primitive_types = {"Cube", "Sphere", "Capsule", "Cylinder", "Plane", "Quad"}
    if primitiveType and primitiveType not in valid_primitive_types:
        return {"success": False, "message": f"Invalid primitiveType '{primitiveType}'. Must be one of: {', '.join(valid_primitive_types)}"}

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "create",
        "name": name,
    }

    if parsed_position:
        params["position"] = parsed_position
    if parsed_rotation:
        params["rotation"] = parsed_rotation
    if parsed_scale:
        params["scale"] = parsed_scale
    if parent:
        params["parent"] = parent
    if tag:
        params["tag"] = tag
    if layer:
        params["layer"] = layer
    # Only send setActive if explicitly provided (not using default)
    if parsed_active is not None:
        params["setActive"] = parsed_active
    if primitiveType:
        params["primitiveType"] = primitiveType

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_gameobject",
        params,
    )

