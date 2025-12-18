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
    path: Annotated[str | None, "Scene path, e.g., Assets/Scenes/MainMenu.unity (optional if name provided)"] = None,
    name: Annotated[str | None, "Scene name (optional if path provided)"] = None,
    buildIndex: Annotated[int | str | None, "Build index number (optional)"] = None,
) -> dict[str, Any]:
    """Load a scene."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs - at least one identifier must be provided
    if not path and not name and buildIndex is None:
        return {"success": False, "message": "At least one of path, name, or buildIndex must be provided"}

    # If only name is provided, construct the full path
    # Default to Assets/Scenes/ directory, matching create_scene behavior
    constructed_path = None
    if not path and name:
        # Construct full path: Assets/Scenes/{name}.unity
        # Check if name already includes .unity extension
        if not name.endswith(".unity"):
            constructed_path = f"Assets/Scenes/{name}.unity"
        else:
            constructed_path = f"Assets/Scenes/{name}"
        # Validate the constructed path
        is_valid, error_msg = validate_scene_path(constructed_path)
        if not is_valid:
            return {"success": False, "message": error_msg or "Invalid constructed scene path"}
    elif path:
        is_valid, error_msg = validate_scene_path(path)
        if not is_valid:
            return {"success": False, "message": error_msg or "Invalid scene path"}

    # Parse buildIndex if provided as string
    parsed_build_index = None
    if buildIndex is not None:
        parsed_build_index = parse_json_payload(buildIndex)
        if isinstance(parsed_build_index, str):
            try:
                parsed_build_index = int(parsed_build_index)
            except ValueError:
                return {"success": False, "message": "buildIndex must be an integer"}

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "load",
    }

    # Use constructed_path if we built one, otherwise use provided path
    if constructed_path:
        params["path"] = constructed_path
    elif path:
        params["path"] = path
    
    # Also include name for Unity's internal logic (it may use name or path)
    if name:
        params["name"] = name
    
    if parsed_build_index is not None:
        params["buildIndex"] = parsed_build_index

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_scene",
        params,
    )

