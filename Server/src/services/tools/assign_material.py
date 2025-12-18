"""Assign a material to a renderer component on a GameObject."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import parse_json_payload
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_gameobject_name, validate_material_path


@mcp_for_unity_tool(
    name="assign_material",
    description="Assign a material to a renderer component on a GameObject. Use this to apply materials to GameObjects."
)
async def assign_material(
    ctx: Context,
    target: Annotated[str, "GameObject name or path (required)"],
    material_path: Annotated[str, "Material asset path (required)"],
    slot: Annotated[int | str | None, "Material slot index (optional, default: 0)"] = None,
) -> dict[str, Any]:
    """Assign a material to a renderer component on a GameObject."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs
    is_valid, error_msg = validate_gameobject_name(target)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid target GameObject name"}

    is_valid, error_msg = validate_material_path(material_path)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid material path"}

    # Parse slot if provided as string
    parsed_slot = 0
    if slot is not None:
        parsed_slot = parse_json_payload(slot) if isinstance(slot, str) else slot
        try:
            parsed_slot = int(parsed_slot)
        except (ValueError, TypeError):
            return {"success": False, "message": "slot must be an integer"}

    # Transform simplified parameters to Unity bridge format (camelCase)
    params: dict[str, Any] = {
        "action": "assign_material_to_renderer",
        "target": target,
        "materialPath": material_path,
        "slot": parsed_slot,
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_material",
        params,
    )

