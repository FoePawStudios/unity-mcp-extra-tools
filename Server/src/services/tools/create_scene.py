"""Create a new scene."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import coerce_bool
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_scene_path


@mcp_for_unity_tool(
    name="create_scene",
    description="Create a new scene. Use this to set up new game scenes (main menu, gameplay, settings, etc.)."
)
async def create_scene(
    ctx: Context,
    scene_name: Annotated[str, "Scene name (required)"],
    scene_path: Annotated[str | None, "Full path, e.g., Assets/Scenes/MainMenu.unity (optional)"] = None,
    add_camera: Annotated[bool | str | None, "Add main camera (optional, default: true)"] = None,
    add_light: Annotated[bool | str | None, "Add directional light (optional, default: true for 3D)"] = None,
) -> dict[str, Any]:
    """Create a new scene."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Validate inputs
    if not scene_name:
        return {"success": False, "message": "scene_name parameter is required"}

    if scene_path:
        is_valid, error_msg = validate_scene_path(scene_path)
        if not is_valid:
            return {"success": False, "message": error_msg or "Invalid scene path"}

    # Parse boolean parameters
    parsed_add_camera = coerce_bool(add_camera, default=True)
    parsed_add_light = coerce_bool(add_light, default=True)

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "create",
        "name": scene_name,
    }

    if scene_path:
        params["path"] = scene_path
    if parsed_add_camera is not None:
        params["addCamera"] = parsed_add_camera  # Unity bridge may use this, check if needed
    if parsed_add_light is not None:
        params["addLight"] = parsed_add_light  # Unity bridge may use this, check if needed

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_scene",
        params,
    )

