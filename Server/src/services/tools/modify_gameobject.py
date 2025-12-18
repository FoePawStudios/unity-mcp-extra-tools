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
    position: Annotated[list[float] | str | None, "New position [x, y, z] (optional)"] = None,
    rotation: Annotated[list[float] | str | None, "New rotation [x, y, z] in degrees (optional)"] = None,
    scale: Annotated[list[float] | str | None, "New scale [x, y, z] (optional)"] = None,
    parent: Annotated[str | None, "New parent name/path, or null to unparent (optional)"] = None,
    tag: Annotated[str | None, "New tag (optional)"] = None,
    layer: Annotated[str | None, "New layer (optional)"] = None,
    active: Annotated[bool | str | None, "New active state (optional)"] = None,
) -> dict[str, Any]:
    """Modify GameObject properties."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Validate inputs
    is_valid, error_msg = validate_gameobject_name(target)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid target GameObject name"}

    if name:
        is_valid, error_msg = validate_gameobject_name(name)
        if not is_valid:
            return {"success": False, "message": error_msg or "Invalid new GameObject name"}

    # Parse vector parameters
    parsed_position = parse_vector3(position)
    parsed_rotation = parse_vector3(rotation)
    parsed_scale = parse_vector3(scale)
    parsed_active = coerce_bool(active) if active is not None else None

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
    if parent is not None:  # Allow explicit None to unparent
        params["parent"] = parent
    if tag:
        params["tag"] = tag
    if layer:
        params["layer"] = layer
    if parsed_active is not None:
        params["set_active"] = parsed_active

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_gameobject",
        params,
    )

