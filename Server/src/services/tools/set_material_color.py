"""Set the color of a material."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_material_path
from .value_parser import parse_color


@mcp_for_unity_tool(
    name="set_material_color",
    description="Set the color of a material. Use this to change material appearance."
)
async def set_material_color(
    ctx: Context,
    material_path: Annotated[str, "Material asset path (required)"],
    color: Annotated[list[float] | str, "Color [r, g, b, a] (required)"],
) -> dict[str, Any]:
    """Set the color of a material."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Validate inputs
    is_valid, error_msg = validate_material_path(material_path)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid material path"}

    if not color:
        return {"success": False, "message": "color parameter is required"}

    # Parse color
    parsed_color = parse_color(color)
    if not parsed_color:
        return {"success": False, "message": "Invalid color format. Expected [r, g, b, a] or comma-separated string"}

    # Transform simplified parameters to Unity bridge format (camelCase)
    params: dict[str, Any] = {
        "action": "set_material_color",
        "materialPath": material_path,
        "color": parsed_color,
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_material",
        params,
    )

