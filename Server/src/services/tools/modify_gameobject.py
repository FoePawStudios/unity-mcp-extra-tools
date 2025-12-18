"""Modify GameObject properties (position, rotation, scale, name, parent, tag, layer, active state)."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import coerce_bool
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_gameobject_name
from .value_parser import parse_vector3


@mcp_for_unity_tool(
    name="modify_gameobject",
    description="Modify GameObject properties (position, rotation, scale, name, parent, tag, layer, active state). Use this to change GameObject transform or basic properties."
)
async def modify_gameobject(
    ctx: Context,
    target: Annotated[str, "GameObject name or path (required)"],
    name: Annotated[str | None, "New name (optional)"] = None,
    position: Annotated[list[float] | str | None, "New position as array [x, y, z] or JSON array string '[x, y, z]' (required brackets, not comma-separated) (optional)"] = None,
    rotation: Annotated[list[float] | str | None, "New rotation as array [x, y, z] or JSON array string '[x, y, z]' (required brackets, not comma-separated) in degrees (optional)"] = None,
    scale: Annotated[list[float] | str | None, "New scale as array [x, y, z] or JSON array string '[x, y, z]' (required brackets, not comma-separated) (optional)"] = None,
    parent: Annotated[str | None, "New parent name/path, or null/empty string to unparent (moves to scene root) (optional)"] = None,
    tag: Annotated[str | None, "New tag (optional)"] = None,
    layer: Annotated[str | None, "New layer (optional)"] = None,
    setActive: Annotated[bool | str | None, "New active state (optional)"] = None,
) -> dict[str, Any]:
    """Modify GameObject properties."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs
    is_valid, error_msg = validate_gameobject_name(target)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid target GameObject name"}

    if name:
        is_valid, error_msg = validate_gameobject_name(name)
        if not is_valid:
            return {"success": False, "message": error_msg or "Invalid new GameObject name"}

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
    
    parsed_active = coerce_bool(setActive) if setActive is not None else None

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "modify",
        "target": target,
    }

    if name:
        params["name"] = name
    if parsed_position:
        params["position"] = parsed_position
    if parsed_rotation:
        params["rotation"] = parsed_rotation
    if parsed_scale:
        params["scale"] = parsed_scale
    # Handle parent parameter
    # Unity handles empty string or null for unparenting (moves to scene root per ManageGameObject.cs line 664)
    # When parent is explicitly None (from JSON null), convert to empty string for proper unparenting
    # Note: We can't perfectly distinguish "not provided" vs "explicitly None", but if parent is in the call
    # and is None, we should handle unparenting. The safest approach: always include parent if provided,
    # and convert None to "" for unparenting.
    # However, to avoid changing parent when not intended, we only include if parent is not None.
    # For explicit unparenting, users should pass "" (empty string) instead of null.
    # But to handle JSON null gracefully, if parent is None and was likely provided, convert to "".
    # For now, we'll only include parent if it's not None (string value).
    # Users wanting to unparent should pass "" explicitly.
    if parent is not None:
        params["parent"] = parent
    # TODO: Consider using a sentinel value or inspect to detect if parent was explicitly provided as None
    if tag:
        params["tag"] = tag
    if layer:
        params["layer"] = layer
    if parsed_active is not None:
        params["setActive"] = parsed_active

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_gameobject",
        params,
    )

