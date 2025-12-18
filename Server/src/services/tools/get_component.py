"""Get information about a component on a GameObject."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import coerce_bool
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance

from .validators import validate_component_type, validate_gameobject_name


@mcp_for_unity_tool(
    name="get_component",
    description="Get information about a component on a GameObject. Use this to read component properties or verify a component exists."
)
async def get_component(
    ctx: Context,
    target: Annotated[str, "GameObject name or path (required)"],
    componentName: Annotated[str, "Component type name (required)"],
    includeNonPublicSerialized: Annotated[bool | str | None, "Include private serialized fields (optional, default: false)"] = None,
) -> dict[str, Any]:
    """Get information about a component on a GameObject."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Validate inputs
    is_valid, error_msg = validate_gameobject_name(target)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid target GameObject name"}

    is_valid, error_msg = validate_component_type(componentName)
    if not is_valid:
        return {"success": False, "message": error_msg or "Invalid component type"}

    # Parse boolean parameter
    parsed_include_non_public = coerce_bool(includeNonPublicSerialized, default=False)

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "get_component",
        "target": target,
        "componentName": componentName,
    }

    if parsed_include_non_public:
        params["includeNonPublicSerialized"] = parsed_include_non_public

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_gameobject",
        params,
    )

