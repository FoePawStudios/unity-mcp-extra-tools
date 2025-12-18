"""Find GameObject(s) in the current scene by name, tag, layer, or component."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import coerce_bool
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance


@mcp_for_unity_tool(
    name="find_gameobject",
    description="Find a GameObject in the current scene by name, tag, layer, or component. Use this before modifying or querying a GameObject to ensure it exists."
)
async def find_gameobject(
    ctx: Context,
    search_by: Annotated[Literal["name", "tag", "layer", "component"], "How to search (required)"],
    value: Annotated[str, "What to search for (required)"],
    find_all: Annotated[bool | str | None, "Return all matches (optional, default: false)"] = None,
    include_inactive: Annotated[bool | str | None, "Include inactive GameObjects (optional, default: false)"] = None,
    search_children: Annotated[bool | str | None, "Search in child objects (optional, default: false)"] = None,
) -> dict[str, Any]:
    """Find GameObject(s) in the current scene."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs
    if not search_by:
        return {"success": False, "message": "search_by parameter is required"}
    if not value:
        return {"success": False, "message": "value parameter is required"}

    # Map simplified search_by to Unity bridge search_method
    search_method_map = {
        "name": "by_name",
        "tag": "by_tag",
        "layer": "by_layer",
        "component": "by_component",
    }

    search_method = search_method_map.get(search_by)
    if not search_method:
        return {"success": False, "message": f"Invalid search_by value: {search_by}. Must be one of: name, tag, layer, component"}

    # Parse boolean parameters
    parsed_find_all = coerce_bool(find_all, default=False)
    parsed_include_inactive = coerce_bool(include_inactive, default=False)
    parsed_search_children = coerce_bool(search_children, default=False)

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "find",
        "search_method": search_method,
        "search_term": value,
    }

    if parsed_find_all:
        params["find_all"] = parsed_find_all
    if parsed_include_inactive:
        params["search_inactive"] = parsed_include_inactive
    if parsed_search_children:
        params["search_in_children"] = parsed_search_children

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_gameobject",
        params,
    )

