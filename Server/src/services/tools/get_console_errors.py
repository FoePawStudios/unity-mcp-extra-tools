"""Get errors and warnings from Unity console."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import coerce_bool, parse_json_payload
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance


@mcp_for_unity_tool(
    name="get_console_errors",
    description="Get errors and warnings from Unity console. Use this to check for compilation errors or runtime issues."
)
async def get_console_errors(
    ctx: Context,
    types: Annotated[list[Literal["error", "warning", "log"]] | str | None, "Message types to get (optional, default: ['error', 'warning'])"] = None,
    count: Annotated[int | str | None, "Max messages to return (optional, default: 10)"] = None,
    include_stacktrace: Annotated[bool | str | None, "Include stack traces (optional, default: false)"] = None,
) -> dict[str, Any]:
    """Get errors and warnings from Unity console."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Parse types parameter (default to ["error", "warning"])
    parsed_types = ["error", "warning"]
    if types:
        parsed_types = parse_json_payload(types) if isinstance(types, str) else types
        if not isinstance(parsed_types, list):
            return {"success": False, "message": "types must be a list"}
        # Validate types
        valid_types = {"error", "warning", "log"}
        if not all(t in valid_types for t in parsed_types):
            return {"success": False, "message": "types must contain only: 'error', 'warning', 'log'"}

    # Parse count parameter
    parsed_count = 10
    if count is not None:
        parsed_count = parse_json_payload(count) if isinstance(count, str) else count
        try:
            parsed_count = int(parsed_count)
            if parsed_count <= 0:
                return {"success": False, "message": "count must be greater than 0"}
        except (ValueError, TypeError):
            return {"success": False, "message": "count must be an integer"}

    parsed_include_stacktrace = coerce_bool(include_stacktrace, default=False)

    # Transform simplified parameters to Unity bridge format
    params: dict[str, Any] = {
        "action": "get",
        "types": parsed_types,
        "count": parsed_count,
        "includeStacktrace": parsed_include_stacktrace,
    }

    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "read_console",
        params,
    )

