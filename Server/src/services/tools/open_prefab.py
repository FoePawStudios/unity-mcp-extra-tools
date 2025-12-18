"""Open a prefab in isolation mode for editing."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_prefab_path


@mcp_for_unity_tool(
    name="open_prefab",
    description="Open a prefab in isolation mode for editing. Use this before modifying a prefab's structure or components."
)
async def open_prefab(
    ctx: Context,
    prefab_path: Annotated[str, "Prefab asset path, e.g., Assets/Prefabs/Enemy.prefab (required)"],
) -> dict[str, Any]:
    """Open a prefab in isolation mode for editing."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Validate inputs
    is_valid, error_msg = validate_prefab_path(prefab_path)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid prefab path"}

    # Transform simplified parameters to Unity bridge format (camelCase)
    params: dict[str, Any] = {
        "action": "open_stage",
        "prefabPath": prefab_path,
        "mode": "InIsolation",  # Default mode
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_prefabs",
        params,
    )

