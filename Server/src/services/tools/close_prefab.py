"""Close the prefab isolation mode and return to scene view."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import coerce_bool
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance


@mcp_for_unity_tool(
    name="close_prefab",
    description="Close the prefab isolation mode and return to scene view. Use this after saving prefab changes."
)
async def close_prefab(
    ctx: Context,
    save_before_close: Annotated[bool | str | None, "Save prefab before closing (optional, default: true)"] = None,
) -> dict[str, Any]:
    """Close the prefab isolation mode and return to scene view."""
    unity_instance = get_unity_instance_from_context(ctx)

    # Parse boolean parameter (default True for save_before_close)
    parsed_save_before_close = coerce_bool(save_before_close, default=True)

    # Transform simplified parameters to Unity bridge format (camelCase)
    params: dict[str, Any] = {
        "action": "close_stage",
    }

    if parsed_save_before_close is not None:
        params["saveBeforeClose"] = parsed_save_before_close

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_prefabs",
        params,
    )

