"""Create a new material asset."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import parse_json_payload
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_material_path
from .value_parser import parse_color


@mcp_for_unity_tool(
    name="create_material",
    description="Create a new material asset. Use this to create materials for rendering GameObjects."
)
async def create_material(
    ctx: Context,
    material_path: Annotated[str, "Material asset path, e.g., Assets/Materials/RedMaterial.mat (required)"],
    shader: Annotated[str | None, "Shader name, e.g., Standard, Unlit/Color (optional, default: Standard)"] = None,
    color: Annotated[list[float] | str | None, "Base color [r, g, b, a] (optional)"] = None,
    properties: Annotated[dict[str, Any] | str | None, "Additional shader properties (optional)"] = None,
) -> dict[str, Any]:
    """Create a new material asset."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs
    is_valid, error_msg = validate_material_path(material_path)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid material path"}

    # Parse color if provided
    parsed_color = parse_color(color) if color else None

    # Parse properties if provided as string
    parsed_properties = None
    if properties:
        parsed_properties = parse_json_payload(properties)
        if parsed_properties is not None and not isinstance(parsed_properties, dict):
            return {"success": False, "message": "properties must be a JSON object (dict)"}

    # Transform simplified parameters to Unity bridge format (camelCase)
    params: dict[str, Any] = {
        "action": "create",
        "materialPath": material_path,
    }

    if shader:
        params["shader"] = shader
    if parsed_color:
        params["color"] = parsed_color
    if parsed_properties:
        params["properties"] = parsed_properties

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_material",
        params,
    )

