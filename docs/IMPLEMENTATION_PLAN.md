# Complete Simplified Unity MCP Tools Implementation Plan

## Overview

This plan implements all 27 simplified MCP tools specified in `docs/UNITY_MCP_TOOL_PROPOSALS.md`. These tools replace complex action-based tools with focused, single-purpose tools that eliminate the `action` parameter requirement and use consistent naming conventions.

## Tools to Implement

### Phase 1: GameObject Operations (4 tools)

1. `create_gameobject` - Create new GameObject with optional transform, tag, layer, primitive type
2. `find_gameobject` - Find GameObject(s) by name, tag, layer, or component
3. `modify_gameobject` - Modify GameObject properties (transform, name, parent, tag, layer, active)
4. `delete_gameobject` - Delete a GameObject from scene

### Phase 2: Component Operations (5 tools)

5. `add_component` - Add component to GameObject with optional initial properties
6. `remove_component` - Remove component from GameObject
7. `set_component_property` - Set single component property (formerly SetComponentValue)
8. `set_component_properties` - Set multiple component properties at once
9. `get_component` - Get component information and properties

### Phase 3: Prefab Operations (4 tools)

10. `create_prefab` - Create prefab from scene GameObject
11. `open_prefab` - Open prefab in isolation mode
12. `save_prefab` - Save currently open prefab
13. `close_prefab` - Close prefab isolation mode

### Phase 4: Scene Operations (4 tools)

14. `create_scene` - Create new scene with optional camera/light
15. `load_scene` - Load scene by path, name, or build index
16. `save_scene` - Save current scene
17. `get_scene_hierarchy` - Get scene GameObject hierarchy

### Phase 5: Material Operations (3 tools)

18. `create_material` - Create new material asset with shader and properties
19. `set_material_color` - Set material color
20. `assign_material` - Assign material to renderer component

### Phase 6: Editor Control (7 tools)

21. `check_compilation_status` - Check if Unity is compiling
22. `wait_for_compilation` - Wait for compilation to complete
23. `get_console_errors` - Get console errors/warnings/logs
24. `clear_console` - Clear Unity console
25. `set_play_mode` - Control play mode (play/pause/stop)
26. `add_tag` - Add tag to project
27. `add_layer` - Add layer to project

## Architecture

```javascript
┌─────────────────┐
│   MCP Client    │  (Cursor, Claude Desktop, etc.)
│  (MCP Protocol) │
└────────┬────────┘
         │
         │ HTTP/Stdio
         │
┌────────▼─────────────────────────┐
│   Python MCP Server              │
│   (Server/src/main.py)           │
│   - Auto-discovery registration  │
│   - Tool definitions             │
│   - Value parsing/validation     │
└────────┬─────────────────────────┘
         │
         │ HTTP/Stdio
         │
┌────────▼─────────────────────────┐
│   Unity C# Bridge                │
│   (MCPForUnity/Editor/...)       │
│   - Unity API execution          │
└──────────────────────────────────┘
```



## Implementation Strategy

Use **direct Unity communication pattern** - simplified tools send commands directly to Unity via `send_with_unity_instance()` (same pattern as existing tools), rather than wrapping existing tool functions. This provides better isolation from upstream changes and cleaner separation.

**Key approach:**
- Tools use `@mcp_for_unity_tool` decorator for auto-discovery
- Tools send commands directly to Unity using `send_with_unity_instance(async_send_command_with_retry, unity_instance, tool_name, params)`
- Tools transform simplified parameters to match Unity bridge expectations
- Each tool is self-contained in its own file

**Benefits:**
- Upstream changes to existing tools won't affect simplified tools
- Clear separation between old and new tool systems
- Tools automatically registered via auto-discovery pattern
- No need for router or manual registration code



## File Structure

```javascript
UnityMCPExtraTools/
├── Server/
│   └── src/
│       ├── services/
│       │   └── tools/
│       │       ├── __init__.py
│       │       ├── value_parser.py                # Value parsing utilities
│       │       ├── validators.py                  # Input validation functions
│       │       ├── create_gameobject.py           # GameObject creation tool
│       │       ├── find_gameobject.py             # GameObject find tool
│       │       ├── modify_gameobject.py           # GameObject modification tool
│       │       ├── delete_gameobject.py           # GameObject deletion tool
│       │       ├── add_component.py               # Component addition tool
│       │       ├── remove_component.py            # Component removal tool
│       │       ├── set_component_property.py      # Single property setter
│       │       ├── set_component_properties.py    # Multiple properties setter
│       │       ├── get_component.py               # Component getter
│       │       ├── create_prefab.py               # Prefab creation tool
│       │       ├── open_prefab.py                 # Prefab open tool
│       │       ├── save_prefab.py                 # Prefab save tool
│       │       ├── close_prefab.py                # Prefab close tool
│       │       ├── create_scene.py                # Scene creation tool
│       │       ├── load_scene.py                  # Scene loading tool
│       │       ├── save_scene.py                  # Scene save tool
│       │       ├── get_scene_hierarchy.py         # Scene hierarchy tool
│       │       ├── create_material.py             # Material creation tool
│       │       ├── set_material_color.py          # Material color tool
│       │       ├── assign_material.py             # Material assignment tool
│       │       ├── check_compilation_status.py    # Compilation check tool
│       │       ├── wait_for_compilation.py        # Compilation wait tool
│       │       ├── get_console_errors.py          # Console errors tool
│       │       ├── clear_console.py               # Console clear tool
│       │       ├── set_play_mode.py               # Play mode control tool
│       │       ├── add_tag.py                     # Tag addition tool
│       │       └── add_layer.py                   # Layer addition tool
│       └── ... (existing server code)
└── MCPForUnity/
    └── Editor/
        └── (existing Unity bridge code)
```

**Note:** No manual registration needed - all tools use `@mcp_for_unity_tool` decorator and are auto-discovered by `register_all_tools()` in `services/tools/__init__.py`.



## Implementation Details

### 1. Core Infrastructure

**File**: `Server/src/services/tools/value_parser.py`

- `parse_value_string()` - Parse various value formats (JSON, comma-separated, numbers, booleans)
- `parse_vector3()` - Parse Vector3 from string/list
- `parse_color()` - Parse Color from string/list
- `parse_transform()` - Parse transform values

**File**: `Server/src/services/tools/validators.py`

- `validate_gameobject_name()` - Validate GameObject identifier
- `validate_component_type()` - Validate component type name
- `validate_scene_path()` - Validate scene path format
- `validate_prefab_path()` - Validate prefab path format
- `validate_material_path()` - Validate material path format

### 2. Tool Implementation Pattern

Each tool is implemented as a separate file using the auto-discovery pattern. All tools follow this structure:

**Template for each tool:**

```python
from fastmcp import Context
from typing import Annotated, Any
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from services.tools.utils import coerce_bool, parse_json_payload
from transport.unity_transport import send_with_unity_instance
from transport.legacy.unity_connection import async_send_command_with_retry
from .value_parser import parse_vector3, parse_value_string
from .validators import validate_gameobject_name

@mcp_for_unity_tool(
    name="create_gameobject",
    description="Create a new GameObject in the current scene. Use this when you need to add a new object to the scene hierarchy."
)
async def create_gameobject(
    ctx: Context,
    name: Annotated[str, "GameObject name (required)"],
    position: Annotated[list[float] | str | None, "Position [x, y, z]"] = None,
    rotation: Annotated[list[float] | str | None, "Rotation [x, y, z] in degrees"] = None,
    # ... other parameters
) -> dict[str, Any]:
    """Implementation that transforms parameters and sends to Unity."""
    unity_instance = get_unity_instance_from_context(ctx)
    if not unity_instance:
        return {"success": False, "message": "No active Unity instance"}
    
    # Validate inputs
    if not name:
        return {"success": False, "message": "name parameter is required"}
    
    # Parse vector parameters (handle both list and string formats)
    parsed_position = parse_vector3(position) if position else None
    parsed_rotation = parse_vector3(rotation) if rotation else None
    
    # Transform simplified parameters to Unity bridge format
    params = {
        "action": "create",
        "name": name,
    }
    if parsed_position:
        params["position"] = parsed_position
    if parsed_rotation:
        params["rotation"] = parsed_rotation
    # ... add other transformed parameters
    
    # Send directly to Unity
    return await send_with_unity_instance(
        async_send_command_with_retry,
        unity_instance,
        "manage_gameobject",
        params
    )
```

**Key points:**
- Each tool is in its own file (e.g., `create_gameobject.py`)
- Uses `@mcp_for_unity_tool` decorator for auto-discovery
- Return type is `dict[str, Any]` (matching existing tool pattern)
- No manual registration needed - `register_all_tools()` in `services/tools/__init__.py` auto-discovers them
- Tools send commands directly to Unity using `send_with_unity_instance()`
- Parameter transformation happens in the tool function itself
- Use `coerce_bool()` and `parse_json_payload()` from `services.tools.utils` for parameter parsing
- Always check for `unity_instance` and return early with error if None
- Validate required parameters before sending to Unity

### 3. Tool Categories

**GameObject Operations (4 tools):**
- `create_gameobject.py` - Sends to Unity bridge with `manage_gameobject` action="create"
- `find_gameobject.py` - Sends to Unity bridge with `manage_gameobject` action="find"
- `modify_gameobject.py` - Sends to Unity bridge with `manage_gameobject` action="modify"
- `delete_gameobject.py` - Sends to Unity bridge with `manage_gameobject` action="delete"

**Component Operations (5 tools):**
- `add_component.py` - Sends to Unity bridge with `manage_gameobject` action="add_component"
- `remove_component.py` - Sends to Unity bridge with `manage_gameobject` action="remove_component"
- `set_component_property.py` - Sends to Unity bridge with `manage_gameobject` action="set_component_property"
- `set_component_properties.py` - Sends to Unity bridge with `manage_gameobject` action="set_component_property"
- `get_component.py` - Sends to Unity bridge with `manage_gameobject` action="get_component"

**Prefab Operations (4 tools):**
- `create_prefab.py` - Sends to Unity bridge with `manage_prefabs` action="create_from_gameobject"
- `open_prefab.py` - Sends to Unity bridge with `manage_prefabs` action="open_stage"
- `save_prefab.py` - Sends to Unity bridge with `manage_prefabs` action="save_open_stage"
- `close_prefab.py` - Sends to Unity bridge with `manage_prefabs` action="close_stage"

**Scene Operations (4 tools):**
- `create_scene.py` - Sends to Unity bridge with `manage_scene` action="create"
- `load_scene.py` - Sends to Unity bridge with `manage_scene` action="load"
- `save_scene.py` - Sends to Unity bridge with `manage_scene` action="save"
- `get_scene_hierarchy.py` - Sends to Unity bridge with `manage_scene` action="get_hierarchy"

**Material Operations (3 tools):**
- `create_material.py` - Sends to Unity bridge with `manage_material` action="create"
- `set_material_color.py` - Sends to Unity bridge with `manage_material` action="set_material_color"
- `assign_material.py` - Sends to Unity bridge with `manage_material` action="assign_material_to_renderer"

**Editor Control (7 tools):**
- `check_compilation_status.py` - Sends `get_editor_state` command to Unity and returns compilation status from response
- `wait_for_compilation.py` - Polls `get_editor_state` command until compilation completes
- `get_console_errors.py` - Sends to Unity bridge with `read_console` action="get"
- `clear_console.py` - Sends to Unity bridge with `read_console` action="clear"
- `set_play_mode.py` - Sends to Unity bridge with `manage_editor` action="play"/"pause"/"stop"
- `add_tag.py` - Sends to Unity bridge with `manage_editor` action="add_tag"
- `add_layer.py` - Sends to Unity bridge with `manage_editor` action="add_layer"

### 4. Auto-Discovery Integration

**No server.py changes needed!** Tools are automatically registered via the existing `register_all_tools()` function in `Server/src/services/tools/__init__.py`, which:
1. Discovers all `.py` files in `services/tools/` directory
2. Imports modules with `@mcp_for_unity_tool` decorated functions
3. Automatically registers them with the MCP server

This means:
- **Zero modifications** to `server.py` or `main.py`
- Tools work immediately once files are created
- Follows existing project patterns
- Upstream changes won't affect tool registration

## Key Design Decisions

### Parameter Naming Consistency

- Always use `target` for GameObject identifier (not `name`, `gameobject_name`, etc.) - **consistent across all simplified tools**
- Always use `component_type` for component names (not `component_name`) - **consistent across all simplified tools**
- Use `search_by` and `value` for find operations - **consistent naming**
- Use `prefab_path`, `scene_path`, `material_path` consistently - **consistent naming**
- **Note:** Parameter names in simplified tools may differ from existing tools - this is intentional for consistency. Simplified tools use consistent naming internally and map to existing tool parameter names when communicating with Unity bridge.

### Value Parsing Strategy

- Accept arrays `[x, y, z]` OR strings `"[x,y,z]" `OR `"x,y,z"`
- JSON parsing first for complex types
- Fallback to comma-separated parsing
- Type coercion: string → number → boolean → string

### Error Handling

- Validate at Python layer before Unity call
- Provide clear error messages with suggestions
- Handle Unity-specific errors (GameObject not found, component missing, etc.)
- Include parameter hints in error messages

### Backward Compatibility

- All existing tools continue to work
- Simplified tools are additive only
- No breaking changes to existing API
- Gradual migration path

## Testing Strategy

### Phase 1: Unit Tests

- Value parser: JSON, comma-separated, type conversions
- Validators: All validation functions
- Handler logic: Parameter transformation

### Phase 2: Integration Tests

- End-to-end tool calls for each tool
- Error handling scenarios
- Unity bridge communication

### Phase 3: Validation Tests

- Real Unity scenes
- Common component types
- Edge cases (missing GameObjects, invalid paths, etc.)

### Phase 4: LLM Agent Tests

- Test with actual LLM agents (Claude, GPT)
- Verify tool selection accuracy
- Verify parameter correctness
- Compare error rates vs existing tools

## Implementation Phases

### Phase 1: Core Infrastructure + GameObject Tools (4 tools)

- Setup repository structure
- Implement value parser and validators
- Implement 4 GameObject operation tools
- Test GameObject operations

### Phase 2: Component Tools (5 tools)

- Implement 5 component operation tools
- Test component operations
- Verify property setting works correctly

### Phase 3: Prefab & Scene Tools (8 tools)

- Implement 4 prefab tools
- Implement 4 scene tools
- Test prefab and scene workflows

### Phase 4: Material & Editor Tools (10 tools)

- Implement 3 material tools
- Implement 7 editor control tools
- Test material and editor operations

### Phase 5: Documentation & Testing

- Complete documentation for all tools
- Full integration testing
- LLM agent testing
- Performance optimization

## Success Metrics

1. **All 27 tools implemented and functional**
2. **Zero breaking changes** to existing tools
3. **Reduced error rate** in LLM tool usage (target: 50% reduction)
4. **Improved tool selection** accuracy by LLMs
5. **Comprehensive test coverage** (target: 80%+)
6. **Complete documentation** with examples

## Pre-Implementation Checklist

Before starting implementation, verify the following:

### Environment & Setup
- [ ] Repository is cloned and up-to-date with upstream
- [ ] Python virtual environment is set up and activated
- [ ] All dependencies are installed (`pip install -r requirements.txt` or equivalent)
- [ ] Unity Editor is installed and accessible
- [ ] MCP for Unity package is installed in Unity test project
- [ ] Python MCP server can start successfully (`python -m Server.src.main` or equivalent)

### Code Understanding
- [ ] Reviewed existing tool patterns in `Server/src/services/tools/manage_gameobject.py`
- [ ] Reviewed existing tool patterns in `Server/src/services/tools/read_console.py`
- [ ] Reviewed existing tool patterns in `Server/src/services/tools/manage_editor.py`
- [ ] Reviewed `@mcp_for_unity_tool` decorator usage
- [ ] Reviewed `send_with_unity_instance()` function signature
- [ ] Reviewed helper utilities in `Server/src/services/tools/utils.py` (`coerce_bool`, `parse_json_payload`)
- [ ] Reviewed resource pattern in `Server/src/services/resources/editor_state.py`
- [ ] Understood auto-discovery mechanism in `Server/src/services/tools/__init__.py`

### Reference Documentation
- [ ] `docs/UNITY_MCP_TOOL_PROPOSALS.md` is available and reviewed
- [ ] All 27 tool specifications are understood
- [ ] Parameter mappings from simplified tools to Unity bridge actions are clear

### Unity Bridge Command Mapping
Verify understanding of Unity bridge commands:
- [ ] GameObject operations → `manage_gameobject` with appropriate `action` values
- [ ] Component operations → `manage_gameobject` with component-related `action` values
- [ ] Prefab operations → `manage_prefabs` with appropriate `action` values
- [ ] Scene operations → `manage_scene` with appropriate `action` values
- [ ] Material operations → `manage_material` with appropriate `action` values
- [ ] Editor operations → `manage_editor` or `read_console` with appropriate `action` values
- [ ] Compilation status → `get_editor_state` command (same as resource uses)

### Implementation Order
- [ ] Start with Phase 1: Core Infrastructure (value_parser.py, validators.py)
- [ ] Then Phase 1: GameObject Tools (4 tools)
- [ ] Follow with remaining phases in order

### Testing Setup
- [ ] Test Unity project is available
- [ ] Unity MCP server connection is verified
- [ ] Basic tool call testing workflow is understood
- [ ] Plan for incremental testing after each tool

## Notes

- **Repository**: This implementation is in the UnityMCPExtraTools repository (already forked and set up)
- **Auto-discovery**: All tools use the `@mcp_for_unity_tool` decorator and are automatically registered - no manual server.py changes needed
- **Isolation**: Simplified tools send commands directly to Unity, providing isolation from upstream changes to existing tools
- **Editor State Access**: For `check_compilation_status` and `wait_for_compilation`, send `get_editor_state` command to Unity (same pattern as the resource uses)
- **Helper Utilities**: Reuse `coerce_bool()` and `parse_json_payload()` from `services.tools.utils` for parameter handling
- **Parameter Transformation**: Tools must map simplified parameter names to Unity bridge parameter names (e.g., `component_type` → `component_name` for some operations)