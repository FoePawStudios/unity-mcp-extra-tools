# LLM Agent Testing Prompt for Simplified Unity MCP Tools

Copy and paste this entire prompt into a fresh LLM agent session to begin comprehensive testing of all 27 simplified Unity MCP tools.

---

# Comprehensive Integration Testing of Simplified Unity MCP Tools

## Your Mission

You are tasked with performing comprehensive integration testing of 27 simplified Unity MCP tools. A Unity Editor instance is already running with the MCP server connected and ready to receive commands.

**Your goal**: Systematically test each tool, document all results (successes, failures, and workarounds) in a markdown file at `docs/test_results/simplified_tools_test_results.md`.

## Testing Guidelines

1. **Test Order**: Work through tools in the order listed below (by category)
2. **Test Each Tool Thoroughly**: 
   - Start with basic/happy path tests
   - Test parameter variations (arrays vs strings, optional params)
   - Test error scenarios (invalid inputs, missing prerequisites)
3. **Document Everything**: Create/update `docs/test_results/simplified_tools_test_results.md` with all results
4. **Clean Up**: After each test category, clean up created objects to avoid conflicts
5. **Workarounds**: If a simplified tool fails, try the equivalent legacy tool (e.g., `mcp_unityMCP_manage_gameobject`) and document if it succeeds

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
3. ✅ Creation with position (string): `{"name": "TestObject_003", "position": "10,2,0"}`
4. ✅ Creation with rotation: `{"name": "TestObject_004", "rotation": [0, 45, 0]}`
5. ✅ Creation with scale: `{"name": "TestObject_005", "scale": [2, 2, 2]}`
6. ✅ Creation with parent: Create parent first, then child with `{"name": "Child", "parent": "Parent"}`
7. ✅ Creation with tag: `{"name": "TestObject_006", "tag": "Untagged"}` (use existing tag)
8. ✅ Creation with layer: `{"name": "TestObject_007", "layer": "Default"}` (use existing layer)
9. ✅ Creation with primitive: `{"name": "TestCube", "primitive_type": "Cube"}`
10. ✅ Creation with active=false: `{"name": "TestObject_008", "active": false}`
11. ✅ All parameters combined
12. ❌ Invalid name (empty string): `{"name": ""}`
13. ❌ Invalid parent (non-existent): `{"name": "TestObject_009", "parent": "NonExistent"}`
14. ❌ Invalid primitive type: `{"name": "TestObject_010", "primitive_type": "InvalidType"}`

After testing, clean up all test objects.

### Tool 2: `find_gameobject`

Prerequisites: Create several test objects with different names, tags, and components first.

Test cases:
1. ✅ Find by name (single): `{"search_by": "name", "value": "TestObject_001"}`
2. ✅ Find by name (find_all=true): `{"search_by": "name", "value": "TestObject", "find_all": true}`
3. ✅ Find by tag: `{"search_by": "tag", "value": "Untagged"}`
4. ✅ Find by layer: `{"search_by": "layer", "value": "Default"}`
5. ✅ Find by component: `{"search_by": "component", "value": "Transform"}`
6. ✅ Include inactive: `{"search_by": "name", "value": "TestObject_008", "include_inactive": true}`
7. ✅ Search in children: Create parent with children, then search
8. ✅ Combination of options
9. ❌ Find non-existent: `{"search_by": "name", "value": "NonExistentObject"}`
10. ❌ Invalid search_by: `{"search_by": "invalid", "value": "Test"}`
11. ❌ Empty value: `{"search_by": "name", "value": ""}`

### Tool 3: `modify_gameobject`

Prerequisites: Create a test object first.

Test cases:
1. ✅ Modify position: `{"target": "TestObject_001", "position": [10, 5, 0]}`
2. ✅ Modify rotation: `{"target": "TestObject_001", "rotation": [0, 90, 0]}`
3. ✅ Modify scale: `{"target": "TestObject_001", "scale": [3, 3, 3]}`
4. ✅ Modify name: `{"target": "TestObject_001", "name": "RenamedObject"}`
5. ✅ Change parent: Create parent, then `{"target": "TestObject_001", "parent": "Parent"}`
6. ✅ Unparent: `{"target": "TestObject_001", "parent": null}`
7. ✅ Change tag: `{"target": "TestObject_001", "tag": "Untagged"}`
8. ✅ Change layer: `{"target": "TestObject_001", "layer": "Default"}`
9. ✅ Set active: `{"target": "TestObject_001", "active": false}`
10. ✅ Multiple properties: Combine position, rotation, and scale
11. ❌ Modify non-existent: `{"target": "NonExistent", "position": [0, 0, 0]}`
12. ❌ Invalid parent: `{"target": "TestObject_001", "parent": "NonExistent"}`

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

Prerequisites: Create test GameObject first.

Test cases:
1. ✅ Add Rigidbody2D: `{"target": "TestObject", "component_type": "Rigidbody2D"}`
2. ✅ Add Rigidbody: `{"target": "TestObject", "component_type": "Rigidbody"}`
3. ✅ Add SpriteRenderer: `{"target": "TestObject", "component_type": "SpriteRenderer"}`
4. ✅ Add MeshRenderer: `{"target": "TestObject", "component_type": "MeshRenderer"}`
5. ✅ Add BoxCollider2D: `{"target": "TestObject", "component_type": "BoxCollider2D"}`
6. ✅ Add BoxCollider: `{"target": "TestObject", "component_type": "BoxCollider"}`
7. ✅ Add with properties: `{"target": "TestObject", "component_type": "Rigidbody2D", "properties": {"mass": 2.5}}`
8. ✅ Add multiple components sequentially
9. ❌ Add to non-existent: `{"target": "NonExistent", "component_type": "Rigidbody2D"}`
10. ❌ Invalid component: `{"target": "TestObject", "component_type": "InvalidComponent"}`

### Tool 6: `remove_component`

Prerequisites: Create GameObject with components first.

Test cases:
1. ✅ Remove component: `{"target": "TestObject", "component_type": "Rigidbody2D"}`
2. ✅ Remove Transform (should fail - required): `{"target": "TestObject", "component_type": "Transform"}`
3. ✅ Remove multiple components sequentially
4. ❌ Remove non-existent: `{"target": "TestObject", "component_type": "NonExistentComponent"}`
5. ❌ Remove from non-existent: `{"target": "NonExistent", "component_type": "Rigidbody2D"}`

### Tool 7: `set_component_property`

Prerequisites: Create GameObject with Rigidbody2D component.

Test cases:
1. ✅ Set Rigidbody2D.mass: `{"target": "TestObject", "component_type": "Rigidbody2D", "property": "mass", "value": 2.5}`
2. ✅ Set Rigidbody2D.gravityScale: `{"target": "TestObject", "component_type": "Rigidbody2D", "property": "gravityScale", "value": 0.5}`
3. ✅ Set SpriteRenderer.color: `{"target": "TestObject", "component_type": "SpriteRenderer", "property": "color", "value": [1, 0, 0, 1]}`
4. ✅ Set Transform.position: `{"target": "TestObject", "component_type": "Transform", "property": "position", "value": [5, 0, 0]}`
5. ✅ Set nested property: `{"target": "TestObject", "component_type": "MeshRenderer", "property": "sharedMaterial.color", "value": [0, 1, 0, 1]}`
6. ✅ Set boolean: `{"target": "TestObject", "component_type": "BoxCollider2D", "property": "isTrigger", "value": true}`
7. ✅ Set string: Test with string property if available
8. ❌ Set on non-existent component: `{"target": "TestObject", "component_type": "NonExistent", "property": "mass", "value": 1}`
9. ❌ Invalid property: `{"target": "TestObject", "component_type": "Rigidbody2D", "property": "invalidProperty", "value": 1}`

### Tool 8: `set_component_properties`

Prerequisites: Create GameObject with Rigidbody2D component.

Test cases:
1. ✅ Set multiple Rigidbody2D properties: `{"target": "TestObject", "component_type": "Rigidbody2D", "properties": {"mass": 2.5, "gravityScale": 0.5, "drag": 0.1}}`
2. ✅ Set multiple SpriteRenderer properties: `{"target": "TestObject", "component_type": "SpriteRenderer", "properties": {"color": [1, 0, 0, 1], "sortingOrder": 5}}`
3. ✅ Set mixed property types
4. ❌ Set on non-existent component: `{"target": "TestObject", "component_type": "NonExistent", "properties": {"mass": 1}}`
5. ❌ Invalid property names: `{"target": "TestObject", "component_type": "Rigidbody2D", "properties": {"invalidProp": 1}}`

### Tool 9: `get_component`

Prerequisites: Create GameObject with components.

Test cases:
1. ✅ Get Transform: `{"target": "TestObject", "component_type": "Transform"}`
2. ✅ Get Rigidbody2D: `{"target": "TestObject", "component_type": "Rigidbody2D"}`
3. ✅ Get with include_private=false: `{"target": "TestObject", "component_type": "Rigidbody2D", "include_private": false}`
4. ✅ Get with include_private=true: `{"target": "TestObject", "component_type": "Rigidbody2D", "include_private": true}`
5. ✅ Verify returned properties match set values (set mass to 2.5, then get and verify)
6. ❌ Get non-existent component: `{"target": "TestObject", "component_type": "NonExistent"}`
7. ❌ Get from non-existent GameObject: `{"target": "NonExistent", "component_type": "Transform"}`

---

## Phase 3: Prefab Operations (4 tools)

### Tool 10: `create_prefab`

Prerequisites: Create test GameObject with components.

Test cases:
1. ✅ Create prefab from simple GameObject: `{"source_gameobject": "TestObject", "prefab_path": "Assets/Prefabs/TestPrefab.prefab"}`
2. ✅ Create prefab from GameObject with components
3. ✅ Create prefab from GameObject with children
4. ✅ Create with allow_overwrite=false (new prefab)
5. ✅ Create with allow_overwrite=true (overwrite existing)
6. ❌ Create from non-existent: `{"source_gameobject": "NonExistent", "prefab_path": "Assets/Prefabs/Test.prefab"}`
7. ❌ Invalid path: `{"source_gameobject": "TestObject", "prefab_path": "Invalid/Path.prefab"}`

### Tool 11: `open_prefab`

Prerequisites: Create a prefab first.

Test cases:
1. ✅ Open existing prefab: `{"prefab_path": "Assets/Prefabs/TestPrefab.prefab"}`
2. ✅ Verify prefab opens in isolation mode
3. ❌ Open non-existent: `{"prefab_path": "Assets/Prefabs/NonExistent.prefab"}`
4. ❌ Invalid path: `{"prefab_path": "Invalid/Path.prefab"}`

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
1. ✅ Close with save_before_close=true: `{"save_before_close": true}`
2. ✅ Close with save_before_close=false: `{"save_before_close": false}`
3. ✅ Close after save_prefab: Save first, then close
4. ❌ Close when no prefab open: Call `close_prefab` without opening prefab first

---

## Phase 4: Scene Operations (4 tools)

### Tool 14: `create_scene`

Test cases:
1. ✅ Create scene with name only: `{"scene_name": "TestScene_001"}`
2. ✅ Create scene with path: `{"scene_name": "TestScene_002", "scene_path": "Assets/Scenes/TestScene_002.unity"}`
3. ✅ Create with add_camera=true: `{"scene_name": "TestScene_003", "add_camera": true}`
4. ✅ Create with add_camera=false: `{"scene_name": "TestScene_004", "add_camera": false}`
5. ✅ Create with add_light=true: `{"scene_name": "TestScene_005", "add_light": true}`
6. ✅ Create with add_light=false: `{"scene_name": "TestScene_006", "add_light": false}`
7. ✅ Create with all options
8. ❌ Invalid path: `{"scene_name": "TestScene", "scene_path": "Invalid/Path.unity"}`
9. ❌ Duplicate name: Try creating scene with same name twice

### Tool 15: `load_scene`

Prerequisites: Create test scenes first.

Test cases:
1. ✅ Load by path: `{"scene_path": "Assets/Scenes/TestScene_001.unity"}`
2. ✅ Load by name: `{"scene_name": "TestScene_001"}`
3. ✅ Load by build_index: `{"build_index": 0}` (if scene is in build settings)
4. ✅ Load non-existent (should fail gracefully): `{"scene_name": "NonExistentScene"}`
5. ❌ Invalid path: `{"scene_path": "Invalid/Path.unity"}`
6. ❌ Invalid build_index: `{"build_index": 999}`

### Tool 16: `save_scene`

Test cases:
1. ✅ Save current scene: Call `save_scene` with no parameters
2. ✅ Save with new path: `{"scene_path": "Assets/Scenes/NewSceneName.unity"}`
3. ✅ Save after modifications: Make changes, then save
4. ❌ Invalid path: `{"scene_path": "Invalid/Path.unity"}`

### Tool 17: `get_scene_hierarchy`

Test cases:
1. ✅ Get hierarchy of empty scene
2. ✅ Get hierarchy with multiple GameObjects: Create objects, then get hierarchy
3. ✅ Get hierarchy with nested GameObjects: Create parent with children, then get hierarchy
4. ✅ Verify hierarchy structure matches created objects

---

## Phase 5: Material Operations (3 tools)

### Tool 18: `create_material`

Test cases:
1. ✅ Create with path only: `{"material_path": "Assets/Materials/TestMaterial_001.mat"}`
2. ✅ Create with shader: `{"material_path": "Assets/Materials/TestMaterial_002.mat", "shader": "Standard"}`
3. ✅ Create with color (array): `{"material_path": "Assets/Materials/TestMaterial_003.mat", "color": [1, 0, 0, 1]}`
4. ✅ Create with color (string): `{"material_path": "Assets/Materials/TestMaterial_004.mat", "color": "1,0,0,1"}`
5. ✅ Create with properties: `{"material_path": "Assets/Materials/TestMaterial_005.mat", "properties": {"_Metallic": 0.5}}`
6. ✅ Create with all options
7. ❌ Invalid path: `{"material_path": "Invalid/Path.mat"}`
8. ❌ Invalid shader: `{"material_path": "Assets/Materials/Test.mat", "shader": "NonExistentShader"}`

### Tool 19: `set_material_color`

Prerequisites: Create a material first.

Test cases:
1. ✅ Set color (array): `{"material_path": "Assets/Materials/TestMaterial_001.mat", "color": [0, 1, 0, 1]}`
2. ✅ Set color (string): `{"material_path": "Assets/Materials/TestMaterial_001.mat", "color": "0,1,0,1"}`
3. ✅ Set color with alpha: `{"material_path": "Assets/Materials/TestMaterial_001.mat", "color": [1, 1, 0, 0.5]}`
4. ✅ Set color multiple times
5. ❌ Non-existent material: `{"material_path": "Assets/Materials/NonExistent.mat", "color": [1, 0, 0, 1]}`
6. ❌ Invalid format: `{"material_path": "Assets/Materials/TestMaterial_001.mat", "color": "invalid"}`

### Tool 20: `assign_material`

Prerequisites: Create material and GameObject with MeshRenderer.

Test cases:
1. ✅ Assign to MeshRenderer: `{"target": "TestObject", "material_path": "Assets/Materials/TestMaterial_001.mat"}`
2. ✅ Assign to SpriteRenderer: Create object with SpriteRenderer, then assign
3. ✅ Assign to specific slot: `{"target": "TestObject", "material_path": "Assets/Materials/TestMaterial_001.mat", "slot": 0}`
4. ✅ Assign to multiple renderers
5. ❌ Non-existent GameObject: `{"target": "NonExistent", "material_path": "Assets/Materials/TestMaterial_001.mat"}`
6. ❌ GameObject without renderer: `{"target": "TestObject", "material_path": "Assets/Materials/TestMaterial_001.mat"}` (if object has no renderer)
7. ❌ Non-existent material: `{"target": "TestObject", "material_path": "Assets/Materials/NonExistent.mat"}`

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
1. ✅ Add new tag: `{"tag_name": "TestTag_001"}`
2. ✅ Add tag that already exists: Try adding same tag twice (should handle gracefully)
3. ✅ Verify tag appears: Check if tag is available in Unity
4. ❌ Invalid name: `{"tag_name": ""}` (empty string)

### Tool 27: `add_layer`

Test cases:
1. ✅ Add new layer: `{"layer_name": "TestLayer_001"}`
2. ✅ Add layer that already exists: Try adding same layer twice (should handle gracefully)
3. ✅ Verify layer appears: Check if layer is available in Unity
4. ❌ Invalid name: `{"layer_name": ""}` (empty string)

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

- **If a simplified tool fails**, try the equivalent legacy tool and document the workaround
- **Document all errors** with exact error messages
- **Use unique names** for all test objects to avoid conflicts
- **Clean up after each phase** to maintain test isolation
- **Be thorough** - test both success and failure scenarios

Begin testing now, starting with Phase 1: GameObject Operations.

