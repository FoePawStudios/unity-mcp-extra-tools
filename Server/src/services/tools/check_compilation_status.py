"""Check if Unity is currently compiling scripts."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance


@mcp_for_unity_tool(
    name="check_compilation_status",
    description="Check if Unity is currently compiling scripts. Use this before operations that require compiled code."
)
async def check_compilation_status(
    ctx: Context,
) -> dict[str, Any]:
    """Check if Unity is currently compiling scripts."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Send get_editor_state command to Unity (same as resource uses)
    response = await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "get_editor_state",
        {},
    )

    # Extract compilation status from response
    if isinstance(response, dict):
        data = response.get("data", {})
        is_compiling = data.get("isCompiling", False)
        # Check for compilation errors by looking at the response
        has_errors = False
        if "message" in response and "error" in str(response.get("message", "")).lower():
            has_errors = True

        return {
            "success": True,
            "is_compiling": is_compiling,
            "has_errors": has_errors,
        }

    return response if isinstance(response, dict) else {"success": False, "message": "Failed to get compilation status"}

