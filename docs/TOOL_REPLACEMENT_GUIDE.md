# Tool Replacement Guide

This document maps old action-based tools to new simplified tools and identifies which old tools can be safely disabled in Cursor.

## ✅ Fully Replaced - Safe to Disable

These old tools are **completely replaced** by the new simplified tools:

### 1. `manage_gameobject`
**Actions that have replacements:**
- ✅ `create` → Use `create_gameobject`
- ✅ `find` → Use `find_gameobject`
- ✅ `modify` → Use `modify_gameobject`
- ✅ `delete` → Use `delete_gameobject`
- ✅ `add_component` → Use `add_component`
- ✅ `remove_component` → Use `remove_component`
- ✅ `get_component` → Use `get_component`
- ✅ `set_component_property` → Use `set_component_property` or `set_component_properties`

**Actions WITHOUT replacements (keep these):**
- ❌ `get_components` - Gets all components on a GameObject (plural)
- ❌ `duplicate` - Duplicates a GameObject
- ❌ `move_relative` - Moves GameObject relative to another object

**Recommendation:** ✅ **SAFE TO DISABLE** if you don't need `get_components`, `duplicate`, or `move_relative`.

### 2. `manage_scene`
**Actions that have replacements:**
- ✅ `create` → Use `create_scene`
- ✅ `load` → Use `load_scene`
- ✅ `save` → Use `save_scene`
- ✅ `get_hierarchy` → Use `get_scene_hierarchy`

**Actions WITHOUT replacements (keep these):**
- ❌ `get_active` - Gets the currently active scene
- ❌ `get_build_settings` - Gets scene build settings
- ❌ `screenshot` - Captures a screenshot

**Recommendation:** ✅ **SAFE TO DISABLE** if you don't need `get_active`, `get_build_settings`, or `screenshot`.

### 3. `manage_prefabs`
**Actions that have replacements:**
- ✅ `create_from_gameobject` → Use `create_prefab`
- ✅ `open_stage` → Use `open_prefab`
- ✅ `save_open_stage` → Use `save_prefab`
- ✅ `close_stage` → Use `close_prefab`

**Actions WITHOUT replacements:**
- None (all actions are covered)

**Recommendation:** ✅ **SAFE TO DISABLE** - Completely replaced!

### 4. `manage_material`
**Actions that have replacements:**
- ✅ `create` → Use `create_material`
- ✅ `set_material_color` → Use `set_material_color`
- ✅ `assign_material_to_renderer` → Use `assign_material`

**Actions WITHOUT replacements (keep these):**
- ❌ `ping` - Material ping operation
- ❌ `set_material_shader_property` - Set arbitrary shader properties (more flexible than color)
- ❌ `set_renderer_color` - Set renderer color directly
- ❌ `get_material_info` - Get material information

**Recommendation:** ⚠️ **PARTIALLY SAFE** - Can disable if you only need basic material operations (create, color, assign). Keep if you need advanced shader property manipulation.

### 5. `manage_editor`
**Actions that have replacements:**
- ✅ `play` → Use `set_play_mode("play")`
- ✅ `pause` → Use `set_play_mode("pause")`
- ✅ `stop` → Use `set_play_mode("stop")`
- ✅ `add_tag` → Use `add_tag`
- ✅ `add_layer` → Use `add_layer`

**Actions WITHOUT replacements (keep these):**
- ❌ `telemetry_status` - Check telemetry status
- ❌ `telemetry_ping` - Send telemetry ping
- ❌ `set_active_tool` - Set active Unity tool
- ❌ `remove_tag` - Remove a tag
- ❌ `remove_layer` - Remove a layer

**Recommendation:** ⚠️ **PARTIALLY SAFE** - Can disable if you don't need telemetry, tool switching, or tag/layer removal. The new tools only handle adding tags/layers, not removing them.

### 6. `read_console`
**Actions that have replacements:**
- ✅ `clear` → Use `clear_console`
- ✅ `get` → Use `get_console_errors` (though this is more limited - only gets errors/warnings)

**Actions WITHOUT replacements (keep these):**
- ❌ Advanced filtering (types, count, filter_text, since_timestamp, format, include_stacktrace) - `get_console_errors` is simpler and doesn't support all these options

**Recommendation:** ⚠️ **PARTIALLY SAFE** - Can disable if you only need basic console clearing and error checking. Keep if you need advanced console filtering/formatting.

## ❌ Keep These Tools

These tools have **NO replacements** and should be kept:

- `manage_asset` - Asset operations (not covered by new tools)
- `manage_script` - Script operations (not covered by new tools)
- `manage_shader` - Shader operations (not covered by new tools)
- `script_apply_edits` - Advanced script editing (not covered by new tools)
- `check_compilation_status` - ✅ This is actually a NEW tool (keep it!)
- `wait_for_compilation` - ✅ This is actually a NEW tool (keep it!)
- `run_tests` - Test execution (not covered by new tools)
- `execute_custom_tool` - Custom tool execution (not covered by new tools)
- `execute_menu_item` - Menu item execution (not covered by new tools)
- `find_in_file` - File search (not covered by new tools)
- `set_active_instance` - Instance management (not covered by new tools)
- `batch_execute` - Batch operations (not covered by new tools)
- `debug_request_context` - Debugging (not covered by new tools)

## Summary

### ✅ Completely Safe to Disable:
1. **`manage_prefabs`** - 100% replaced

### ✅ Mostly Safe to Disable (if you don't need advanced features):
2. **`manage_gameobject`** - 80% replaced (keep if you need `get_components`, `duplicate`, or `move_relative`)
3. **`manage_scene`** - 57% replaced (keep if you need `get_active`, `get_build_settings`, or `screenshot`)

### ⚠️ Partially Safe (disable only if you don't need advanced features):
4. **`manage_material`** - 60% replaced (keep if you need shader property manipulation or material info)
5. **`manage_editor`** - 50% replaced (keep if you need telemetry, tool switching, or tag/layer removal)
6. **`read_console`** - 50% replaced (keep if you need advanced console filtering)

## Recommended Cursor Configuration

If you want to keep things simple and only use the new simplified tools, disable:

```json
{
  "mcpServers": {
    "unityMCP": {
      "disabledTools": [
        "manage_prefabs",
        "manage_gameobject",  // Only if you don't need get_components, duplicate, move_relative
        "manage_scene",       // Only if you don't need get_active, get_build_settings, screenshot
        "manage_material",    // Only if you don't need advanced shader properties
        "manage_editor",      // Only if you don't need telemetry, tool switching, tag/layer removal
        "read_console"        // Only if you don't need advanced console filtering
      ]
    }
  }
}
```

**Note:** Cursor doesn't have a built-in `disabledTools` configuration option. You would need to manually remove these tools from the tool list, or create a wrapper/configuration to hide them. Check Cursor's MCP configuration documentation for the exact method to disable specific tools.

