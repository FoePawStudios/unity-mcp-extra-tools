"""Create a prefab from a scene GameObject."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import coerce_bool
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_gameobject_name, validate_prefab_path


@mcp_for_unity_tool(
    name="create_prefab",
    description="Create a prefab from a scene GameObject. Use this to save a GameObject as a reusable prefab asset."
)
async def create_prefab(
    ctx: Context,
    source_gameobject: Annotated[str, "Scene GameObject name or path (required)"],
    prefabPath: Annotated[str, "Prefab asset path, e.g., Assets/Prefabs/Enemy.prefab (required)"],
    allowOverwrite: Annotated[bool | str | None, "Allow replacing existing prefab (optional, default: false)"] = None,
) -> dict[str, Any]:
    """Create a prefab from a scene GameObject."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs
    is_valid, error_msg = validate_gameobject_name(source_gameobject)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid source GameObject name"}

    is_valid, error_msg = validate_prefab_path(prefabPath)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid prefab path"}

    # Parse boolean parameter
    parsed_allow_overwrite = coerce_bool(allowOverwrite, default=False)

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "create_from_gameobject",
        "target": source_gameobject,  # Map source_gameobject to target
        "prefabPath": prefabPath,
    }

    if parsed_allow_overwrite:
        params["allowOverwrite"] = parsed_allow_overwrite

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_prefabs",
        params,
    )

