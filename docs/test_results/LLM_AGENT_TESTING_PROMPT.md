# LLM Agent Testing Prompt for Simplified Unity MCP Tools

Copy and paste this entire prompt into a fresh LLM agent session to begin comprehensive testing of all 27 simplified Unity MCP tools.

---

# Comprehensive Integration Testing of Simplified Unity MCP Tools

## Your Mission

You are tasked with performing comprehensive integration testing of 27 simplified Unity MCP tools. A Unity Editor instance is already running with the MCP server connected and ready to receive commands.

**Your goal**: Systematically test each tool, document all results (successes, failures, and workarounds) in a markdown file at `docs/test_results/simplified_tools_test_results.md`.

## Initial Cleanup - IMPORTANT FIRST STEP

**BEFORE STARTING ANY TESTS**, you must clean up any objects, scenes, prefabs, or materials created during previous test runs to avoid creation collisions and name conflicts.

1. **Get current scene hierarchy**: Use `get_scene_hierarchy` to see what GameObjects exist
2. **Delete test objects**: Use `delete_gameobject` to remove any objects with names matching test patterns (e.g., `TestObject_*`, `CompTest*`, `PrefabTest*`, `TestCube`, `TestMaterial*`, `TestScene*`, `TestTag*`, `TestLayer*`, `Child_*`, `Parent_*`, `RenamedObject*`)
3. **Check for test scenes**: Use scene management tools to identify and optionally clean up test scenes if needed
4. **Check for test materials**: If testing materials, check for and remove any test materials in `Assets/Materials/` that match test patterns
5. **Check for test prefabs**: If testing prefabs, check for and remove any test prefabs in `Assets/Prefabs/` that match test patterns

**Cleanup Pattern**: Look for objects with names that match these patterns:
- `TestObject_*` (any number)
- `CompTest*`
- `PrefabTest*`
- `TestCube`, `TestSphere`, `TestCapsule`, etc.
- `TestMaterial_*`
- `TestScene_*`
- `TestTag_*`
- `TestLayer_*`
- `Child_*`, `Parent_*`
- `RenamedObject*`

**Note**: Be careful not to delete actual project assets. Only delete objects that clearly match test naming patterns.

Once cleanup is complete, proceed with the testing plan below.

## Recent Fixes Applied

The following bugs have been fixed and should now work correctly:

1. **`find_gameobject`**: Fixed parameter name conversion (snake_case to camelCase) - should now find GameObjects correctly
2. **`add_component`**: Fixed parameter name conversion (`component_name` to `componentName`) - should now add components successfully
3. **`create_gameobject`**: 
   - Fixed parameter name conversion (`set_active` to `setActive`, `primitive_type` to `primitiveType`)
   - **Active parameter limitation**: The `active=false` parameter has limitations and may not work reliably during GameObject creation. **Workaround**: If you need to create an inactive GameObject, use a two-step approach: 1) Create the GameObject using `create_gameobject`, 2) Immediately follow with `modify_gameobject` to set `active=false`. This is the documented expected behavior.
   - Added primitive type validation - invalid types now return clear error messages
   - **Vector format**: Comma-separated strings without brackets (e.g., `"10,2,0"`) are now rejected with clear error - use array format `[10, 2, 0]` or JSON string `"[10, 2, 0]"`
4. **`modify_gameobject`**: 
   - Fixed parameter name conversion (`set_active` to `setActive`)
   - Fixed active state handling - now works correctly
   - **Vector format**: Same as create_gameobject - comma-separated strings without brackets are rejected
   - **Unparenting**: Use empty string `""` for explicit unparenting (moves to scene root)
5. **Component property/query tools**: ✅ **FIXED** - Parameter names now use camelCase directly (`componentName`, `includeNonPublicSerialized`) matching Unity's expectations. All component tools (`remove_component`, `set_component_property`, `get_component`, `set_component_properties`) should now work correctly.
6. **`create_material`**: ✅ **FIXED** - Parameter name now uses camelCase (`materialPath`) matching Unity's expectations. Folder creation logic exists in Unity C# backend.
7. **`load_scene`**: ✅ **FIXED** - Parameter names now use camelCase (`path`, `name`, `buildIndex`) matching Unity's expectations. Should now work correctly.
8. **`parse_color`**: Fixed heuristic to only convert 0-255 range when ALL RGB components are > 1.0 AND <= 255.0 (preserves edge cases like HDR colors)

## Testing Guidelines

1. **Test Order**: Work through tools in the order listed below (by category)
2. **Test Each Tool Thoroughly**: 
   - Start with basic/happy path tests
   - Test parameter variations (arrays vs strings, optional params)
   - Test error scenarios (invalid inputs, missing prerequisites)
3. **Document Everything**: Create/update `docs/test_results/simplified_tools_test_results.md` with all results
4. **Initial Cleanup**: **BEFORE starting tests**, clean up any objects from previous test runs (see "Initial Cleanup" section above)
5. **Clean Up**: After each test category, clean up created objects to avoid conflicts
6. **Workarounds**: If a simplified tool fails, try the equivalent legacy tool (e.g., `mcp_unityMCP_manage_gameobject`) and document if it succeeds

## Test Result Documentation Format

For each test, document in this format:

```markdown
## Tool: [tool_name]

### Test: [test_description]
- **Status**: ✅ PASS / ❌ FAIL / ⚠️ PARTIAL
- **Parameters**: `{parameter_json}`
- **Result**: `{result_json}`
- **Errors**: None / `Error message here`
- **Workaround**: If failed, document alternative command that succeeded (if any)
```

## Error Documentation

When a test fails:
1. Record the exact error message from the tool response
2. Try the equivalent legacy tool with the same operation
3. Document whether the legacy tool succeeded
4. Note any differences in parameter format required

## Test Isolation

- Use unique names for test objects (e.g., `TestObject_20241201_001`)
- Clean up test objects after each test category
- Use a dedicated test scene if needed
- Don't modify existing Unity project assets unless testing overwrite scenarios

---

## Phase 1: GameObject Operations (4 tools)

### Tool 1: `create_gameobject`

Test cases to perform:
1. ✅ Basic creation with name only: `{"name": "TestObject_001"}`
2. ✅ Creation with position (array): `{"name": "TestObject_002", "position": [5, 0, 0]}`
3. ✅ Creation with position (JSON string): `{"name": "TestObject_003", "position": "[10, 2, 0]"}`
4. ❌ Creation with position (comma-separated string - should fail): `{"name": "TestObject_003b", "position": "10,2,0"}` - Should return error: "Position must be an array [x, y, z] or JSON array string '[x, y, z]', not a comma-separated string"
5. ✅ Creation with rotation: `{"name": "TestObject_004", "rotation": [0, 45, 0]}`
6. ✅ Creation with scale: `{"name": "TestObject_005", "scale": [2, 2, 2]}`
7. ✅ Creation with parent: Create parent first, then child with `{"name": "Child", "parent": "Parent"}`
8. ✅ Creation with tag: `{"name": "TestObject_006", "tag": "Untagged"}` (use existing tag)
9. ✅ Creation with layer: `{"name": "TestObject_007", "layer": "Default"}` (use existing layer)
10. ✅ Creation with primitive: `{"name": "TestCube", "primitiveType": "Cube"}`
11. ⚠️ Creation with setActive=false: `{"name": "TestObject_008", "setActive": false}` - **LIMITATION**: This may not work reliably. Use workaround: create GameObject, then immediately use `modify_gameobject` with `setActive=false` to set the active state.
12. ✅ All parameters combined
13. ❌ Invalid name (empty string): `{"name": ""}`
14. ❌ Invalid parent (non-existent): `{"name": "TestObject_009", "parent": "NonExistent"}`
15. ❌ Invalid primitive type: `{"name": "TestObject_010", "primitiveType": "InvalidType"}` - Should now return clear error message (was silently failing before)

After testing, clean up all test objects.

### Tool 2: `find_gameobject`

**Note**: This tool was previously broken (could not find any GameObjects). It has been fixed and should now work correctly.

Prerequisites: Create several test objects with different names, tags, and components first.

Test cases:
1. ✅ Find by name (single): `{"search_by": "name", "value": "TestObject_001"}` - Should now work (was failing before)
2. ✅ Find by name (find_all=true): `{"search_by": "name", "value": "TestObject", "find_all": true}` - Should now work
3. ✅ Find by tag: `{"search_by": "tag", "value": "Untagged"}` - Should now work
4. ✅ Find by layer: `{"search_by": "layer", "value": "Default"}` - Should now work
5. ✅ Find by component: `{"search_by": "component", "value": "Transform"}` - Should now work
6. ✅ Include inactive: `{"search_by": "name", "value": "TestObject_008", "searchInactive": true}` - Should now work
7. ✅ Search in children: Create parent with children, then search
8. ✅ Combination of options
9. ❌ Find non-existent: `{"search_by": "name", "value": "NonExistentObject"}` - Should return empty results (not error)
10. ❌ Invalid search_by: `{"search_by": "invalid", "value": "Test"}`
11. ❌ Empty value: `{"search_by": "name", "value": ""}`

### Tool 3: `modify_gameobject`

Prerequisites: Create a test object first.

Test cases:
1. ✅ Modify position: `{"target": "TestObject_001", "position": [10, 5, 0]}`
2. ✅ Modify rotation: `{"target": "TestObject_001", "rotation": [0, 90, 0]}`
3. ✅ Modify scale: `{"target": "TestObject_001", "scale": [3, 3, 3]}`
4. ✅ Modify position (JSON string): `{"target": "TestObject_001", "position": "[15, 5, 0]"}`
5. ❌ Modify position (comma-separated - should fail): `{"target": "TestObject_001", "position": "20,5,0"}` - Should return error about array format
6. ✅ Modify name: `{"target": "TestObject_001", "name": "RenamedObject"}`
7. ✅ Change parent: Create parent, then `{"target": "TestObject_001", "parent": "Parent"}`
8. ✅ Unparent: `{"target": "TestObject_001", "parent": ""}` - Use empty string for explicit unparenting (moves to scene root). Note: `null` may not work due to Python/JSON serialization - use `""` instead.
9. ✅ Change tag: `{"target": "TestObject_001", "tag": "Untagged"}`
10. ✅ Change layer: `{"target": "TestObject_001", "layer": "Default"}`
11. ✅ Set active: `{"target": "TestObject_001", "setActive": false}` - Should now work correctly (was broken before)
12. ✅ Multiple properties: Combine position, rotation, and scale
13. ❌ Modify non-existent: `{"target": "NonExistent", "position": [0, 0, 0]}`
14. ❌ Invalid parent: `{"target": "TestObject_001", "parent": "NonExistent"}`

### Tool 4: `delete_gameobject`

Prerequisites: Create test objects first.

Test cases:
1. ✅ Delete existing: `{"target": "TestObject_001"}`
2. ✅ Delete with children: Create parent with children, delete parent, verify children deleted
3. ❌ Delete non-existent: `{"target": "NonExistent"}`
4. ❌ Delete twice: Try deleting same object twice (idempotency test)

---

## Phase 2: Component Operations (5 tools)

### Tool 5: `add_component`

**Note**: This tool was previously broken (parameter mapping issue). It has been fixed and should now work correctly.

Prerequisites: Create test GameObject first.

Test cases:
1. ✅ Add Rigidbody2D: `{"target": "TestObject", "componentName": "Rigidbody2D"}` - Should now work (was failing before)
2. ✅ Add Rigidbody: `{"target": "TestObject", "componentName": "Rigidbody"}` - Should now work
3. ✅ Add SpriteRenderer: `{"target": "TestObject", "componentName": "SpriteRenderer"}` - Should now work
4. ✅ Add MeshRenderer: `{"target": "TestObject", "componentName": "MeshRenderer"}` - Should now work
5. ✅ Add BoxCollider2D: `{"target": "TestObject", "componentName": "BoxCollider2D"}` - Should now work
6. ✅ Add BoxCollider: `{"target": "TestObject", "componentName": "BoxCollider"}` - Should now work
7. ✅ Add with properties: `{"target": "TestObject", "componentName": "Rigidbody2D", "properties": {"mass": 2.5}}`
8. ✅ Add multiple components sequentially
9. ❌ Add to non-existent: `{"target": "NonExistent", "componentName": "Rigidbody2D"}`
10. ❌ Invalid component: `{"target": "TestObject", "componentName": "InvalidComponent"}`

### Tool 6: `remove_component`

**Note**: This tool has been updated to use camelCase parameter names directly (`componentName`). It should now work correctly.

Prerequisites: Create GameObject with components first.

Test cases:
1. ✅ Remove component: `{"target": "TestObject", "componentName": "Rigidbody2D"}` - Should now work with camelCase parameter
2. ✅ Remove Transform (should fail - required): `{"target": "TestObject", "componentName": "Transform"}`
3. ✅ Remove multiple components sequentially
4. ❌ Remove non-existent: `{"target": "TestObject", "componentName": "NonExistentComponent"}`
5. ❌ Remove from non-existent: `{"target": "NonExistent", "componentName": "Rigidbody2D"}`

### Tool 7: `set_component_property`

**Note**: This tool has been updated to use camelCase parameter names directly (`componentName`). It should now work correctly.

Prerequisites: Create GameObject with Rigidbody2D component.

Test cases:
1. ✅ Set Rigidbody2D.mass: `{"target": "TestObject", "componentName": "Rigidbody2D", "property": "mass", "value": 2.5}` - Should now work with camelCase parameter
2. ✅ Set Rigidbody2D.gravityScale: `{"target": "TestObject", "componentName": "Rigidbody2D", "property": "gravityScale", "value": 0.5}`
3. ✅ Set SpriteRenderer.color: `{"target": "TestObject", "componentName": "SpriteRenderer", "property": "color", "value": [1, 0, 0, 1]}`
4. ✅ Set Transform.position: `{"target": "TestObject", "componentName": "Transform", "property": "position", "value": [5, 0, 0]}`
5. ✅ Set nested property: `{"target": "TestObject", "componentName": "MeshRenderer", "property": "sharedMaterial.color", "value": [0, 1, 0, 1]}`
6. ✅ Set boolean: `{"target": "TestObject", "componentName": "BoxCollider2D", "property": "isTrigger", "value": true}`
7. ✅ Set string: Test with string property if available
8. ❌ Set on non-existent component: `{"target": "TestObject", "componentName": "NonExistent", "property": "mass", "value": 1}`
9. ❌ Invalid property: `{"target": "TestObject", "componentName": "Rigidbody2D", "property": "invalidProperty", "value": 1}`

### Tool 8: `set_component_properties`

**Note**: This tool has been updated to use camelCase parameter names directly (`componentName`). It should now work correctly.

Prerequisites: Create GameObject with Rigidbody2D component.

Test cases:
1. ✅ Set multiple Rigidbody2D properties: `{"target": "TestObject", "componentName": "Rigidbody2D", "properties": {"mass": 2.5, "gravityScale": 0.5, "drag": 0.1}}` - Should now work with camelCase parameter
2. ✅ Set multiple SpriteRenderer properties: `{"target": "TestObject", "componentName": "SpriteRenderer", "properties": {"color": [1, 0, 0, 1], "sortingOrder": 5}}`
3. ✅ Set mixed property types
4. ❌ Set on non-existent component: `{"target": "TestObject", "componentName": "NonExistent", "properties": {"mass": 1}}`
5. ❌ Invalid property names: `{"target": "TestObject", "componentName": "Rigidbody2D", "properties": {"invalidProp": 1}}`

### Tool 9: `get_component`

**Note**: This tool has been updated to use camelCase parameter names directly (`componentName`, `includeNonPublicSerialized`). It should now work correctly.

Prerequisites: Create GameObject with components.

Test cases:
1. ✅ Get Transform: `{"target": "TestObject", "componentName": "Transform"}` - Should now work with camelCase parameter
2. ✅ Get Rigidbody2D: `{"target": "TestObject", "componentName": "Rigidbody2D"}` - Should now work with camelCase parameter
3. ✅ Get with includeNonPublicSerialized=false: `{"target": "TestObject", "componentName": "Rigidbody2D", "includeNonPublicSerialized": false}`
4. ✅ Get with includeNonPublicSerialized=true: `{"target": "TestObject", "componentName": "Rigidbody2D", "includeNonPublicSerialized": true}`
5. ✅ Verify returned properties match set values (set mass to 2.5, then get and verify)
6. ❌ Get non-existent component: `{"target": "TestObject", "componentName": "NonExistent"}`
7. ❌ Get from non-existent GameObject: `{"target": "NonExistent", "componentName": "Transform"}`

---

## Phase 3: Prefab Operations (4 tools)

### Tool 10: `create_prefab`

Prerequisites: Create test GameObject with components.

Test cases:
1. ✅ Create prefab from simple GameObject: `{"source_gameobject": "TestObject", "prefabPath": "Assets/Prefabs/TestPrefab.prefab"}`
2. ✅ Create prefab from GameObject with components
3. ✅ Create prefab from GameObject with children
4. ✅ Create with allowOverwrite=false (new prefab)
5. ✅ Create with allowOverwrite=true (overwrite existing)
6. ❌ Create from non-existent: `{"source_gameobject": "NonExistent", "prefabPath": "Assets/Prefabs/Test.prefab"}`
7. ❌ Invalid path: `{"source_gameobject": "TestObject", "prefabPath": "Invalid/Path.prefab"}`

### Tool 11: `open_prefab`

Prerequisites: Create a prefab first.

Test cases:
1. ✅ Open existing prefab: `{"prefabPath": "Assets/Prefabs/TestPrefab.prefab"}`
2. ✅ Verify prefab opens in isolation mode
3. ❌ Open non-existent: `{"prefabPath": "Assets/Prefabs/NonExistent.prefab"}`
4. ❌ Invalid path: `{"prefabPath": "Invalid/Path.prefab"}`

### Tool 12: `save_prefab`

Prerequisites: Open a prefab first.

Test cases:
1. ✅ Save prefab after modifications: Make changes, then call `save_prefab` with no parameters
2. ✅ Save prefab with new GameObject added
3. ✅ Save prefab with component changes
4. ❌ Save when no prefab open: Call `save_prefab` without opening prefab first

### Tool 13: `close_prefab`

Prerequisites: Open a prefab first.

Test cases:
1. ✅ Close with saveBeforeClose=true: `{"saveBeforeClose": true}`
2. ✅ Close with saveBeforeClose=false: `{"saveBeforeClose": false}`
3. ✅ Close after save_prefab: Save first, then close
4. ❌ Close when no prefab open: Call `close_prefab` without opening prefab first

---

## Phase 4: Scene Operations (4 tools)

### Tool 14: `create_scene`

Test cases:
1. ✅ Create scene with name only: `{"name": "TestScene_001"}`
2. ✅ Create scene with path: `{"name": "TestScene_002", "path": "Assets/Scenes/TestScene_002.unity"}`
3. ✅ Create with addCamera=true: `{"name": "TestScene_003", "addCamera": true}`
4. ✅ Create with addCamera=false: `{"name": "TestScene_004", "addCamera": false}`
5. ✅ Create with addLight=true: `{"name": "TestScene_005", "addLight": true}`
6. ✅ Create with addLight=false: `{"name": "TestScene_006", "addLight": false}`
7. ✅ Create with all options
8. ❌ Invalid path: `{"name": "TestScene", "path": "Invalid/Path.unity"}`
9. ❌ Duplicate name: Try creating scene with same name twice

### Tool 15: `load_scene`

**Note**: This tool has been updated to use camelCase parameter names directly (`path`, `name`, `buildIndex`). It should now work correctly.

Prerequisites: Create test scenes first.

Test cases:
1. ✅ Load by path: `{"path": "Assets/Scenes/TestScene_001.unity"}` - Should now work with camelCase parameter
2. ✅ Load by name: `{"name": "TestScene_001"}` - Should now work with camelCase parameter
3. ✅ Load by buildIndex: `{"buildIndex": 0}` (if scene is in build settings)
4. ✅ Load non-existent (should fail gracefully): `{"name": "NonExistentScene"}`
5. ❌ Invalid path: `{"path": "Invalid/Path.unity"}`
6. ❌ Invalid buildIndex: `{"buildIndex": 999}`

### Tool 16: `save_scene`

Test cases:
1. ✅ Save current scene: Call `save_scene` with no parameters
2. ✅ Save with new path: `{"path": "Assets/Scenes/NewSceneName.unity"}`
3. ✅ Save after modifications: Make changes, then save
4. ❌ Invalid path: `{"path": "Invalid/Path.unity"}`

### Tool 17: `get_scene_hierarchy`

Test cases:
1. ✅ Get hierarchy of empty scene
2. ✅ Get hierarchy with multiple GameObjects: Create objects, then get hierarchy
3. ✅ Get hierarchy with nested GameObjects: Create parent with children, then get hierarchy
4. ✅ Verify hierarchy structure matches created objects

---

## Phase 5: Material Operations (3 tools)

### Tool 18: `create_material`

**Note**: This tool has been updated to use camelCase parameter names directly (`materialPath`). Folder creation code exists in Unity C# backend. It should now work correctly.

Test cases:
1. ✅ Create with path only: `{"materialPath": "Assets/Materials/TestMaterial_001.mat"}` - Should now work with camelCase parameter
2. ✅ Create with shader: `{"materialPath": "Assets/Materials/TestMaterial_002.mat", "shader": "Standard"}`
3. ✅ Create with color (array): `{"materialPath": "Assets/Materials/TestMaterial_003.mat", "color": [1, 0, 0, 1]}`
4. ✅ Create with color (string): `{"materialPath": "Assets/Materials/TestMaterial_004.mat", "color": "1,0,0,1"}`
5. ✅ Create with properties: `{"materialPath": "Assets/Materials/TestMaterial_005.mat", "properties": {"_Metallic": 0.5}}`
6. ✅ Create with all options
7. ❌ Invalid path: `{"materialPath": "Invalid/Path.mat"}`
8. ❌ Invalid shader: `{"materialPath": "Assets/Materials/Test.mat", "shader": "NonExistentShader"}`

### Tool 19: `set_material_color`

**Note**: The `parse_color` function has been fixed to better handle edge cases. It now only converts 0-255 range when ALL RGB components are > 1.0 AND <= 255.0, preserving HDR colors and values outside normal 0-1 range.

Prerequisites: Create a material first.

Test cases:
1. ✅ Set color (array 0-1): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [0, 1, 0, 1]}`
2. ✅ Set color (array 0-255): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [0, 255, 0, 255]}` - Should convert to [0, 1, 0, 1]
3. ✅ Set color (JSON string): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": "[0,1,0,1]"}`
4. ✅ Set color with alpha: `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [1, 1, 0, 0.5]}`
5. ✅ Set HDR color (edge case): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [1.5, 0, 0, 1]}` - Should preserve 1.5 (not convert to 0-255 range)
6. ✅ Set mixed range (edge case): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [1.5, 0, 0, 1]}` - Should preserve values (not convert)
7. ✅ Set color multiple times
8. ❌ Non-existent material: `{"materialPath": "Assets/Materials/NonExistent.mat", "color": [1, 0, 0, 1]}`
9. ❌ Invalid format: `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": "invalid"}`

### Tool 20: `assign_material`

Prerequisites: Create material and GameObject with MeshRenderer.

Test cases:
1. ✅ Assign to MeshRenderer: `{"target": "TestObject", "materialPath": "Assets/Materials/TestMaterial_001.mat"}`
2. ✅ Assign to SpriteRenderer: Create object with SpriteRenderer, then assign
3. ✅ Assign to specific slot: `{"target": "TestObject", "materialPath": "Assets/Materials/TestMaterial_001.mat", "slot": 0}`
4. ✅ Assign to multiple renderers
5. ❌ Non-existent GameObject: `{"target": "NonExistent", "materialPath": "Assets/Materials/TestMaterial_001.mat"}`
6. ❌ GameObject without renderer: `{"target": "TestObject", "materialPath": "Assets/Materials/TestMaterial_001.mat"}` (if object has no renderer)
7. ❌ Non-existent material: `{"target": "TestObject", "materialPath": "Assets/Materials/NonExistent.mat"}`

---

## Phase 6: Editor Control (7 tools)

### Tool 21: `check_compilation_status`

Test cases:
1. ✅ Check when not compiling: Call with no parameters
2. ✅ Verify response structure: Should return `{"success": true, "is_compiling": false, "has_errors": false}`
3. ✅ Check when compiling: Create a script file to trigger compilation, then check status
4. ✅ Verify has_errors flag: Check if errors are detected

### Tool 22: `wait_for_compilation`

Test cases:
1. ✅ Wait when not compiling: Should return immediately
2. ✅ Wait during compilation: Create script, then wait
3. ✅ Wait with timeout: `{"timeout_seconds": 30}`
4. ✅ Wait with check_errors=true: `{"check_errors": true}`
5. ✅ Wait with check_errors=false: `{"check_errors": false}`
6. ❌ Very short timeout during compilation: `{"timeout_seconds": 1}` (while compiling)

### Tool 23: `get_console_errors`

Test cases:
1. ✅ Get errors only: `{"types": ["error"]}`
2. ✅ Get warnings only: `{"types": ["warning"]}`
3. ✅ Get logs only: `{"types": ["log"]}`
4. ✅ Get errors and warnings: `{"types": ["error", "warning"]}`
5. ✅ Get with count limit: `{"count": 5}`
6. ✅ Get with include_stacktrace=true: `{"include_stacktrace": true}`
7. ✅ Get with include_stacktrace=false: `{"include_stacktrace": false}`
8. ✅ Verify empty console: Should return empty array

### Tool 24: `clear_console`

Test cases:
1. ✅ Clear empty console: Call with no parameters
2. ✅ Clear console with errors: Generate errors, then clear
3. ✅ Clear console with warnings: Generate warnings, then clear
4. ✅ Verify console is empty after clear: Call `get_console_errors` after clear

### Tool 25: `set_play_mode`

Test cases:
1. ✅ Set to "play": `{"mode": "play"}`
2. ✅ Set to "pause" (while playing): `{"mode": "pause"}` (after play)
3. ✅ Set to "stop": `{"mode": "stop"}`
4. ✅ Verify play mode state changes: Check state after each change
5. ❌ Invalid mode: `{"mode": "invalid"}`

### Tool 26: `add_tag`

Test cases:
1. ✅ Add new tag: `{"tagName": "TestTag_001"}`
2. ✅ Add tag that already exists: Try adding same tag twice (should handle gracefully)
3. ✅ Verify tag appears: Check if tag is available in Unity
4. ❌ Invalid name: `{"tagName": ""}` (empty string)

### Tool 27: `add_layer`

Test cases:
1. ✅ Add new layer: `{"layerName": "TestLayer_001"}`
2. ✅ Add layer that already exists: Try adding same layer twice (should handle gracefully)
3. ✅ Verify layer appears: Check if layer is available in Unity
4. ❌ Invalid name: `{"layerName": ""}` (empty string)

---

## Workflow Tests

After testing all individual tools, test these multi-tool workflows:

### Workflow 1: GameObject Lifecycle
1. `create_gameobject` → Create test object
2. `find_gameobject` → Verify it exists
3. `add_component` → Add Rigidbody2D
4. `set_component_property` → Set mass
5. `get_component` → Verify mass was set
6. `modify_gameobject` → Change position
7. `delete_gameobject` → Clean up

### Workflow 2: Prefab Creation and Editing
1. `create_gameobject` → Create source object
2. `add_component` → Add components
3. `create_prefab` → Create prefab
4. `open_prefab` → Open for editing
5. `add_component` → Add component to prefab
6. `save_prefab` → Save changes
7. `close_prefab` → Close prefab stage
8. Verify prefab has new component

### Workflow 3: Scene Management
1. `create_scene` → Create test scene
2. `load_scene` → Load the scene
3. `create_gameobject` → Add objects
4. `get_scene_hierarchy` → Verify objects
5. `save_scene` → Save scene
6. `load_scene` → Reload and verify persistence

### Workflow 4: Material Assignment
1. `create_material` → Create material
2. `set_material_color` → Set color
3. `create_gameobject` → Create object with MeshRenderer
4. `assign_material` → Assign material
5. Verify material is applied

### Workflow 5: Compilation Workflow
1. `check_compilation_status` → Verify not compiling
2. Create script file (via filesystem or MCP script tool)
3. `check_compilation_status` → Verify compiling
4. `wait_for_compilation` → Wait for completion
5. `get_console_errors` → Check for errors
6. `add_component` → Add component using new script

---

## Final Steps

1. **Generate Summary**: Create summary statistics at the top of the test results file:
   - Total tests performed
   - Passed count
   - Failed count
   - Partial success count
   - Known issues list

2. **Review Documentation**: Ensure all tests are documented with proper format

3. **Clean Up**: Remove all test objects, scenes, prefabs, and materials created during testing

---

## Important Notes

- **Parameter Naming**: All simplified tools now use camelCase parameter names directly matching Unity's expectations. Use `componentName` (not `component_type`), `materialPath` (not `material_path`), `prefabPath` (not `prefab_path`), etc. This ensures Unity error messages reference parameter names that match what you see in the tool signatures.
- **Vector Format Requirements**: Position, rotation, and scale parameters must be:
  - Arrays: `[x, y, z]` (Python list)
  - JSON array strings: `"[x, y, z]"` or `'[x, y, z]'` (must include brackets)
  - **NOT supported**: Comma-separated strings like `"10,2,0"` (without brackets) - these will be rejected with clear error messages
- **Unparenting**: To unparent a GameObject, use empty string `""` instead of `null` (due to Python/JSON serialization)
- **If a simplified tool fails**, try the equivalent legacy tool and document the workaround
- **Document all errors** with exact error messages
- **Use unique names** for all test objects to avoid conflicts
- **Clean up after each phase** to maintain test isolation
- **Be thorough** - test both success and failure scenarios

- **All Tools Updated**: All simplified tools have been updated to use camelCase parameter names:
  - Component tools: `componentName`, `includeNonPublicSerialized` ✅
  - Scene tools: `name`, `path`, `buildIndex`, `addCamera`, `addLight` ✅
  - Prefab tools: `prefabPath`, `saveBeforeClose`, `allowOverwrite` ✅
  - Material tools: `materialPath` ✅
  - GameObject tools: `primitiveType`, `setActive`, `searchInactive` ✅
  - Editor tools: `tagName`, `layerName` ✅

**START HERE**: First perform the Initial Cleanup steps described above, then begin testing with Phase 1: GameObject Operations.

