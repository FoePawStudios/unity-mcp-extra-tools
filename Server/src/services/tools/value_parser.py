"""Value parsing utilities for simplified MCP tools."""

from __future__ import annotations

import json
import math
from typing import Any

from services.tools.utils import parse_json_payload


def parse_value_string(value: Any) -> Any:
    """
    Parse various value formats (JSON, comma-separated, numbers, booleans).
    
    Handles:
    - JSON strings: '{"key": "value"}' or '[1, 2, 3]'
    - Comma-separated strings: '1,2,3' or 'x,y,z'
    - Numbers: '123' or '45.6'
    - Booleans: 'true'/'false'
    - Arrays: [1, 2, 3]
    - Already parsed values: Returns as-is
    
    Args:
        value: Input value (can be string, list, dict, number, etc.)
        
    Returns:
        Parsed value in native Python type
    """
    if value is None:
        return None
    
    # If already a native type (not a string), return as-is
    if not isinstance(value, str):
        return value
    
    # Try JSON parsing first (handles JSON arrays and objects)
    parsed = parse_json_payload(value)
    if parsed != value:  # JSON parsing succeeded
        return parsed
    
    # Try comma-separated parsing for strings like "1,2,3"
    stripped = value.strip()
    if "," in stripped:
        parts = [p.strip() for p in stripped.split(",")]
        # Try to parse as numbers
        try:
            return [float(p) if "." in p else int(p) for p in parts]
        except ValueError:
            # Return as strings if can't parse as numbers
            return parts
    
    # Try boolean parsing
    lowered = stripped.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    
    # Try number parsing
    try:
        if "." in stripped:
            return float(stripped)
        return int(stripped)
    except ValueError:
        pass
    
    # Return as string if nothing else matches
    return value


def parse_vector3(value: list[float] | str | None, default: list[float] | None = None) -> list[float] | None:
    """
    Parse Vector3 from string or list.
    
    Accepts:
    - Lists: [1, 2, 3]
    - JSON array strings: '[1, 2, 3]' or '[1,2,3]' (must include brackets)
    
    Does NOT accept:
    - Comma-separated strings without brackets: '1,2,3' (will return None)
    
    Args:
        value: Input value to parse
        default: Default value if parsing fails or value is None
        
    Returns:
        List of 3 floats [x, y, z] or None
    """
    if value is None:
        return default
    
    def _to_vec3(parts: list[Any]) -> list[float] | None:
        """Convert list of parts to Vector3, validating values."""
        if len(parts) != 3:
            return default
        try:
            vec = [float(parts[0]), float(parts[1]), float(parts[2])]
            # Validate all values are finite
            if all(math.isfinite(n) for n in vec):
                return vec
        except (ValueError, TypeError, IndexError):
            pass
        return default
    
    # If already a list with 3 elements
    if isinstance(value, list):
        if len(value) == 3:
            return _to_vec3(value)
        return default
    
    # Parse as JSON first (handles '[1,2,3]' format)
    parsed = parse_json_payload(value)
    if isinstance(parsed, list) and len(parsed) == 3:
        return _to_vec3(parsed)
    
    # For strings, only accept JSON array format with brackets
    # Reject plain comma-separated strings like "10,2,0"
    if isinstance(value, str):
        stripped = value.strip()
        # Must start and end with brackets to be valid
        if not (stripped.startswith("[") and stripped.endswith("]")):
            # Reject comma-separated strings without brackets
            return default
        
        # Parse the content inside brackets
        content = stripped[1:-1].strip()
        if "," in content:
            parts = [p.strip() for p in content.split(",")]
        else:
            parts = content.split()
        
        if len(parts) == 3:
            return _to_vec3(parts)
    
    return default


def parse_color(value: list[float] | str | None, default: list[float] | None = None) -> list[float] | None:
    """
    Parse Color from string or list.
    
    Accepts:
    - RGBA lists: [r, g, b, a] where values are 0-1 (floats) or 0-255 (integers)
    - RGB lists: [r, g, b] (alpha defaults to 1.0)
    - JSON strings: '[1, 0, 0, 1]' or '[255, 0, 0]'
    - Comma-separated: '1,0,0,1' or '255,0,0'
    
    Automatically detects if values are 0-255 range and converts to 0-1.
    
    Args:
        value: Input value to parse
        default: Default value if parsing fails (defaults to [1, 1, 1, 1])
        
    Returns:
        List of 4 floats [r, g, b, a] in 0-1 range or None
    """
    if default is None:
        default = [1.0, 1.0, 1.0, 1.0]
    
    if value is None:
        return default
    
    def _to_color(parts: list[Any]) -> list[float] | None:
        """Convert parts to Color [r, g, b, a] in 0-1 range."""
        try:
            # Handle both 3 and 4 component colors
            if len(parts) == 3:
                r, g, b = float(parts[0]), float(parts[1]), float(parts[2])
                a = 1.0
            elif len(parts) == 4:
                r, g, b, a = float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])
            else:
                return default
            
            # Detect if values are in 0-255 range and convert to 0-1
            # Convert if ANY RGB component is > 1.0 AND all are within 0-255 range
            # This handles colors with zero components like [128, 0, 0, 255]
            # This avoids incorrectly converting edge cases like [1.5, 0, 0, 1] where
            # the user might want HDR colors or values outside normal 0-1 range
            rgb_values = [r, g, b]
            # Check if any component is > 1.0 (indicating 0-255 range) and all are within valid 0-255 range
            if any(val > 1.0 for val in rgb_values) and all(0.0 <= val <= 255.0 for val in rgb_values):
                # RGB components are in 0-255 range, convert them
                r, g, b = r / 255.0, g / 255.0, b / 255.0
                # Convert alpha only if it's also in 0-255 range
                if 0.0 <= a <= 255.0 and a > 1.0:
                    a = a / 255.0
            
            # Clamp to valid range (0-1 for Unity Color)
            r = max(0.0, min(1.0, r))
            g = max(0.0, min(1.0, g))
            b = max(0.0, min(1.0, b))
            a = max(0.0, min(1.0, a))
            
            return [r, g, b, a]
        except (ValueError, TypeError, IndexError):
            return default
    
    # If already a list
    if isinstance(value, list):
        if len(value) in (3, 4):
            return _to_color(value)
        return default
    
    # Parse as JSON first
    parsed = parse_json_payload(value)
    if isinstance(parsed, list) and len(parsed) in (3, 4):
        return _to_color(parsed)
    
    # Handle comma-separated strings
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            stripped = stripped[1:-1].strip()
        
        if "," in stripped:
            parts = [p.strip() for p in stripped.split(",")]
        else:
            parts = stripped.split()
        
        if len(parts) in (3, 4):
            return _to_color(parts)
    
    return default


def parse_transform(
    position: list[float] | str | None = None,
    rotation: list[float] | str | None = None,
    scale: list[float] | str | None = None
) -> dict[str, list[float]]:
    """
    Parse transform values (position, rotation, scale).
    
    Args:
        position: Position vector
        rotation: Rotation vector
        scale: Scale vector
        
    Returns:
        Dictionary with 'position', 'rotation', 'scale' keys (only includes provided values)
    """
    result: dict[str, list[float]] = {}
    
    parsed_position = parse_vector3(position)
    if parsed_position:
        result["position"] = parsed_position
    
    parsed_rotation = parse_vector3(rotation)
    if parsed_rotation:
        result["rotation"] = parsed_rotation
    
    parsed_scale = parse_vector3(scale)
    if parsed_scale:
        result["scale"] = parsed_scale
    
    return result

