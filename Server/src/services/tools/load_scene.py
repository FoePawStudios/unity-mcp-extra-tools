"""Load a scene."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import parse_json_payload
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_scene_path


@mcp_for_unity_tool(
    name="load_scene",
    description="Load a scene. Use this to switch between scenes or load a specific scene for editing."
)
async def load_scene(
    ctx: Context,
    scene_path: Annotated[str | None, "Scene path, e.g., Assets/Scenes/MainMenu.unity (optional if name provided)"] = None,
    scene_name: Annotated[str | None, "Scene name (optional if path provided)"] = None,
    build_index: Annotated[int | str | None, "Build index number (optional)"] = None,
) -> dict[str, Any]:
    """Load a scene."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Validate inputs - at least one identifier must be provided
    if not scene_path and not scene_name and build_index is None:
        return {"success": False, "message": "At least one of scene_path, scene_name, or build_index must be provided"}

    if scene_path:
        is_valid, error_msg = validate_scene_path(scene_path)
        if not is_valid:
            return {"success": False, "message": error_msg or "Invalid scene path"}

    # Parse build_index if provided as string
    parsed_build_index = None
    if build_index is not None:
        parsed_build_index = parse_json_payload(build_index)
        if isinstance(parsed_build_index, str):
            try:
                parsed_build_index = int(parsed_build_index)
            except ValueError:
                return {"success": False, "message": "build_index must be an integer"}

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "load",
    }

    if scene_path:
        params["path"] = scene_path
    if scene_name:
        params["name"] = scene_name
    if parsed_build_index is not None:
        params["buildIndex"] = parsed_build_index

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_scene",
        params,
    )

