"""Wait for Unity compilation to complete."""

from __future__ import annotations

import asyncio
from typing import Annotated, Any

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import coerce_bool, parse_json_payload
from transport.legacy.unity_connection import async_send_command_with_retry
from transport.unity_transport import send_with_unity_instance


@mcp_for_unity_tool(
    name="wait_for_compilation",
    description="Wait for Unity compilation to complete. Use this after script changes before operations requiring compiled code."
)
async def wait_for_compilation(
    ctx: Context,
    timeout_seconds: Annotated[int | str | None, "Maximum time to wait in seconds (optional, default: 60)"] = None,
    check_errors: Annotated[bool | str | None, "Check for compilation errors after completion (optional, default: true)"] = None,
) -> dict[str, Any]:
    """Wait for Unity compilation to complete."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}

    # Parse timeout
    parsed_timeout = 60
    if timeout_seconds is not None:
        parsed_timeout = parse_json_payload(timeout_seconds) if isinstance(timeout_seconds, str) else timeout_seconds
        try:
            parsed_timeout = int(parsed_timeout)
            if parsed_timeout <= 0:
                return {"success": False, "message": "timeout_seconds must be greater than 0"}
        except (ValueError, TypeError):
            return {"success": False, "message": "timeout_seconds must be an integer"}

    parsed_check_errors = coerce_bool(check_errors, default=True)

    # Poll get_editor_state until compilation completes
    start_time = asyncio.get_event_loop().time()
    while True:
        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed >= parsed_timeout:
            return {"success": False, "message": f"Timeout waiting for compilation to complete after {parsed_timeout} seconds"}

        # Check compilation status
        response = await send_with_unity_instance(
            async_send_command_with_retry,
            unity_instance,
            "get_editor_state",
            {},
        )

        if isinstance(response, dict):
            data = response.get("data", {})
            is_compiling = data.get("isCompiling", False)

            if not is_compiling:
                # Compilation complete
                if parsed_check_errors:
                    # Check for errors
                    has_errors = False
                    error_message = ""
                    if "message" in response and "error" in str(response.get("message", "")).lower():
                        has_errors = True
                        error_message = response.get("message", "")

                    return {
                        "success": True,
                        "completed": True,
                        "has_errors": has_errors,
                        "message": error_message if has_errors else "Compilation completed successfully",
                    }
                else:
                    return {
                        "success": True,
                        "completed": True,
                        "message": "Compilation completed",
                    }

        # Wait a bit before polling again
        await asyncio.sleep(0.5)

