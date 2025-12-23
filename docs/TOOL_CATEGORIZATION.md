# Unity MCP Tools Categorization

This document categorizes all tools in `Server/src/services/tools/` into three groups:
1. **Added Tools** - New simplified wrapper tools created in this branch
2. **Modified Tools** - Existing tools that were refactored into simplified wrappers
3. **Original Tools** - Tools from upstream that remain unchanged

## Overview

The simplified tools implementation added **12 new tools** and refactored **15 existing tools** into focused, single-purpose wrappers. These simplified tools wrap the original complex `manage_*` tools, eliminating the need for an `action` parameter and providing consistent naming conventions.

---

## ✅ Added Tools (12)

These are **new simplified wrapper tools** created in this branch. They provide focused, single-purpose interfaces that wrap the original `manage_*` tools.

### Editor Control (4 tools)
1. **`clear_console.py`** - Clear the Unity console
   - Wraps: `read_console` with `action: "clear"`
   
2. **`check_compilation_status.py`** - Check if Unity is currently compiling scripts
   - Wraps: `get_editor_state` command
   
3. **`set_play_mode.py`** - Control Unity play mode (play, pause, stop)
   - Wraps: `manage_editor` with `action: "play"/"pause"/"stop"`
   
4. **`add_tag.py`** - Add a tag to the project
   - Wraps: `manage_editor` with `action: "add_tag"`
   
5. **`add_layer.py`** - Add a layer to the project
   - Wraps: `manage_editor` with `action: "add_layer"`

### Prefab Operations (2 tools)
6. **`open_prefab.py`** - Open a prefab in isolation mode for editing
   - Wraps: `manage_prefabs` with `action: "open_stage"`
   
7. **`close_prefab.py`** - Close the prefab isolation mode and return to scene view
   - Wraps: `manage_prefabs` with `action: "close_stage"`
   
8. **`save_prefab.py`** - Save changes made to the currently open prefab
   - Wraps: `manage_prefabs` with `action: "save_open_stage"`

### Scene Operations (1 tool)
9. **`get_scene_hierarchy.py`** - Get the hierarchy of GameObjects in the current scene
   - Wraps: `manage_scene` with `action: "get_hierarchy"`
   
10. **`save_scene.py`** - Save the current scene
    - Wraps: `manage_scene` with `action: "save"`

### GameObject Operations (1 tool)
11. **`delete_gameobject.py`** - Delete a GameObject from the scene
    - Wraps: `manage_gameobject` with `action: "delete"`

### Component Operations (1 tool)
12. **`remove_component.py`** - Remove a component from a GameObject
    - Wraps: `manage_gameobject` with `action: "remove_component"`

---

## 🔄 Modified Tools (15)

These tools **existed in upstream** but were **refactored into simplified wrappers** in this branch. They were transformed from complex action-based tools into focused, single-purpose tools.

### GameObject Operations (3 tools)
1. **`create_gameobject.py`** - Create new GameObject with optional transform, tag, layer, primitive type
   - Previously: Part of `manage_gameobject` with `action: "create"`
   - Now: Standalone simplified tool
   
2. **`find_gameobject.py`** - Find GameObject(s) by name, tag, layer, or component
   - Previously: Part of `manage_gameobject` with `action: "find"`
   - Now: Standalone simplified tool
   
3. **`modify_gameobject.py`** - Modify GameObject properties (transform, name, parent, tag, layer, active)
   - Previously: Part of `manage_gameobject` with `action: "modify"`
   - Now: Standalone simplified tool

### Component Operations (3 tools)
4. **`add_component.py`** - Add component to GameObject with optional initial properties
   - Previously: Part of `manage_gameobject` with `action: "add_component"`
   - Now: Standalone simplified tool
   
5. **`get_component.py`** - Get component information and properties
   - Previously: Part of `manage_gameobject` with `action: "get_component"`
   - Now: Standalone simplified tool
   
6. **`set_component_property.py`** - Set single component property
   - Previously: Part of `manage_gameobject` with `action: "set_component_property"`
   - Now: Standalone simplified tool
   
7. **`set_component_properties.py`** - Set multiple component properties at once
   - Previously: Part of `manage_gameobject` with `action: "set_component_property"` (multiple)
   - Now: Standalone simplified tool

### Prefab Operations (1 tool)
8. **`create_prefab.py`** - Create prefab from scene GameObject
   - Previously: Part of `manage_prefabs` with `action: "create_from_gameobject"`
   - Now: Standalone simplified tool

### Scene Operations (2 tools)
9. **`create_scene.py`** - Create new scene with optional camera/light
   - Previously: Part of `manage_scene` with `action: "create"`
   - Now: Standalone simplified tool
   
10. **`load_scene.py`** - Load scene by path, name, or build index
    - Previously: Part of `manage_scene` with `action: "load"`
    - Now: Standalone simplified tool

### Material Operations (3 tools)
11. **`create_material.py`** - Create new material asset with shader and properties
    - Previously: Part of `manage_material` with `action: "create"`
    - Now: Standalone simplified tool
    
12. **`set_material_color.py`** - Set material color
    - Previously: Part of `manage_material` with `action: "set_color"`
    - Now: Standalone simplified tool
    
13. **`assign_material.py`** - Assign material to renderer component
    - Previously: Part of `manage_material` with `action: "assign"`
    - Now: Standalone simplified tool

### Editor Control (2 tools)
14. **`get_console_errors.py`** - Get console errors/warnings/logs
    - Previously: Part of `read_console` with `action: "get"`
    - Now: Standalone simplified tool (focused on errors)
    
15. **`wait_for_compilation.py`** - Wait for compilation to complete
    - Previously: Existed but enhanced with better error handling
    - Now: Enhanced simplified tool

### Utility Files (2 files)
16. **`validators.py`** - Input validation functions
    - Previously: Existed with basic validation
    - Now: Enhanced with additional validators for new tools
    
17. **`value_parser.py`** - Value parsing utilities
    - Previously: Existed with basic parsing
    - Now: Enhanced with additional parsers for new tools

---

## 📦 Original Tools (20+)

These tools are **from upstream** and remain **unchanged**. They are the complex, multi-action tools that the simplified wrappers call internally.

### Core Management Tools (8 tools)
1. **`manage_gameobject.py`** - Performs CRUD operations on GameObjects and components
   - Actions: `create`, `modify`, `delete`, `find`, `add_component`, `remove_component`, `set_component_property`, `get_components`, `get_component`, `duplicate`, `move_relative`
   - **Note:** Most actions have simplified replacements, but `get_components`, `duplicate`, and `move_relative` do not
   
2. **`manage_scene.py`** - Performs CRUD operations on Unity scenes
   - Actions: `create`, `load`, `save`, `get_hierarchy`, `get_active`, `get_build_settings`, `screenshot`
   - **Note:** Most actions have simplified replacements, but `get_active`, `get_build_settings`, and `screenshot` do not
   
3. **`manage_prefabs.py`** - Performs CRUD operations on prefabs
   - Actions: `create_from_gameobject`, `open_stage`, `save_open_stage`, `close_stage`
   - **Note:** All actions have simplified replacements
   
4. **`manage_script.py`** - Manages C# script files (create, read, update, delete)
   - Complex tool for script management
   
5. **`manage_shader.py`** - Manages shader scripts (create, read, update, delete)
   - Complex tool for shader management
   
6. **`manage_material.py`** - Performs CRUD operations on materials
   - Actions: `create`, `set_color`, `assign`, etc.
   - **Note:** Most actions have simplified replacements
   
7. **`manage_asset.py`** - Performs CRUD operations on Unity assets
   - Actions: `import`, `create`, `modify`, `delete`, `duplicate`, `move`, `rename`, `search`, `get_info`, `create_folder`, `get_components`
   
8. **`manage_editor.py`** - Performs editor operations
   - Actions: `play`, `pause`, `stop`, `add_tag`, `add_layer`, etc.
   - **Note:** Some actions have simplified replacements

### Console & Debugging (2 tools)
9. **`read_console.py`** - Gets messages from or clears the Unity Editor console
   - Actions: `get`, `clear`
   - **Note:** Simplified replacements exist (`get_console_errors`, `clear_console`)
   
10. **`debug_request_context.py`** - Debug tool for request context inspection

### Testing & Execution (3 tools)
11. **`run_tests.py`** - Runs Unity tests for specified mode (EditMode/PlayMode)
    
12. **`execute_custom_tool.py`** - Execute a project-scoped custom tool registered by Unity
    
13. **`execute_menu_item.py`** - Execute a Unity menu item by path

### File Operations (1 tool)
14. **`find_in_file.py`** - Search for text patterns in files

### Script Management (1 tool)
15. **`script_apply_edits.py`** - Apply edits to C# scripts (large, complex tool ~1000 lines)

### Instance Management (1 tool)
16. **`set_active_instance.py`** - Set the active Unity instance for this client/session

### Batch Operations (1 tool)
17. **`batch_execute.py`** - Runs a list of MCP tool calls as one batch

### Utility Files (3 files)
18. **`utils.py`** - Utility functions for tools
    - Includes: `coerce_bool()`, `parse_json_payload()`, `to_camel_case()`, `convert_params_to_camel_case()`
    - **Note:** Enhanced with camelCase conversion functions for new tools
    
19. **`__init__.py`** - Package initialization and auto-discovery
    - Contains `register_all_tools()` function for automatic tool registration
    - **Note:** Enhanced to support auto-discovery of new simplified tools

---

## Summary Statistics

| Category | Count | Description |
|----------|-------|-------------|
| **Added Tools** | 12 | New simplified wrapper tools |
| **Modified Tools** | 15 | Existing tools refactored into simplified wrappers |
| **Original Tools** | 20+ | Unchanged tools from upstream |
| **Total Tools** | 47+ | All tools in the directory |

---

## Design Philosophy

### Simplified Tools
- **Single Purpose**: Each tool does one thing well
- **No Action Parameter**: Eliminates the need for an `action` parameter
- **Consistent Naming**: Uses consistent parameter names across all tools
- **Direct Unity Communication**: Sends commands directly to Unity bridge
- **Auto-Discovery**: Automatically registered via `@mcp_for_unity_tool` decorator

### Original Tools
- **Multi-Action**: Handle multiple operations via `action` parameter
- **Backward Compatible**: Maintained for existing integrations
- **Feature Complete**: Include operations not yet covered by simplified tools
- **Internal Use**: Called by simplified tools internally

---

## Migration Guide

For users migrating from original tools to simplified tools, see:
- **`docs/TOOL_REPLACEMENT_GUIDE.md`** - Maps old tools to new simplified tools
- **`docs/IMPLEMENTATION_PLAN.md`** - Implementation details and architecture

---

## Notes

- Simplified tools are **wrappers** around original tools - they don't duplicate functionality
- Original tools remain available for operations not yet covered by simplified tools
- Both tool types can coexist - choose based on your needs
- Simplified tools are recommended for new integrations due to their cleaner API

