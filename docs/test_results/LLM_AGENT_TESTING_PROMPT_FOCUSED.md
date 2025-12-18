# Focused LLM Agent Testing Prompt - Remaining Issues

Copy and paste this entire prompt into a fresh LLM agent session to test the remaining problematic tools that need attention.

---

# Focused Integration Testing of Remaining Unity MCP Tool Issues

## Your Mission

You are tasked with testing the remaining problematic Unity MCP tools that either failed or need additional verification. A Unity Editor instance is already running with the MCP server connected and ready to receive commands.

**Your goal**: Test the specific tools listed below, document all results (successes, failures, and workarounds) in a markdown file at `docs/test_results/focused_tools_test_results.md`.

## Initial Cleanup - IMPORTANT FIRST STEP

**BEFORE STARTING ANY TESTS**, you must clean up any objects, scenes, prefabs, or materials created during previous test runs to avoid creation collisions and name conflicts.

1. **Get current scene hierarchy**: Use `get_scene_hierarchy` to see what GameObjects exist
2. **Delete test objects**: Use `delete_gameobject` to remove any objects with names matching test patterns (e.g., `TestObject_*`, `CompTest*`, `TestMaterial*`, `TestScene*`)
3. **Check for test scenes**: Use scene management tools to identify and optionally clean up test scenes if needed
4. **Check for test materials**: Check for and remove any test materials in `Assets/Materials/` that match test patterns

**Cleanup Pattern**: Look for objects with names that match these patterns:
- `TestObject_*` (any number)
- `CompTest*`
- `TestMaterial_*`
- `TestScene_*`

**Note**: Be careful not to delete actual project assets. Only delete objects that clearly match test naming patterns.

Once cleanup is complete, proceed with the testing plan below.

## Recent Fixes Status

Most tools have been fixed and are working correctly. The following tools still need attention:

1. **`set_component_properties`**: Needs comprehensive testing to verify it works correctly
2. **`create_material`**: ❌ **STILL BROKEN** - Folder creation issue persists
3. **`load_scene`**: ❌ **STILL BROKEN** - Path parameter not being recognized
4. **`set_material_color`**: ❌ **BLOCKED** - Cannot test until `create_material` is fixed
5. **`assign_material`**: ❌ **BLOCKED** - Cannot test until `create_material` is fixed

## Testing Guidelines

1. **Test Each Tool Thoroughly**: 
   - Start with basic/happy path tests
   - Test parameter variations
   - Test error scenarios (invalid inputs, missing prerequisites)
2. **Document Everything**: Create/update `docs/test_results/focused_tools_test_results.md` with all results
3. **Clean Up**: After each test category, clean up created objects to avoid conflicts

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

## Important Notes

- **Parameter Naming**: All simplified tools use camelCase parameter names directly matching Unity's expectations. Use `componentName` (not `component_type`), `materialPath` (not `material_path`), `prefabPath` (not `prefab_path`), etc.
- **Vector Format Requirements**: Position, rotation, and scale parameters must be:
  - Arrays: `[x, y, z]` (Python list)
  - JSON array strings: `"[x, y, z]"` or `'[x, y, z]'` (must include brackets)
  - **NOT supported**: Comma-separated strings like `"10,2,0"` (without brackets)

---

## Phase 2: Component Operations - Remaining Tests

### Tool: `set_component_properties`

**Note**: This tool needs comprehensive testing to verify it works correctly. The parameter mapping has been fixed, but it hasn't been fully tested yet.

**Prerequisites**: Create a GameObject with Rigidbody2D component first.

Test cases:
1. ✅ Set multiple Rigidbody2D properties: `{"target": "TestObject", "componentName": "Rigidbody2D", "properties": {"mass": 2.5, "gravityScale": 0.5, "drag": 0.1}}`
2. ✅ Set multiple SpriteRenderer properties: `{"target": "TestObject", "componentName": "SpriteRenderer", "properties": {"color": [1, 0, 0, 1], "sortingOrder": 5}}`
3. ✅ Set mixed property types (float, bool, vector, etc.)
4. ✅ Verify properties were set: Use `get_component` to verify all properties were set correctly
5. ❌ Set on non-existent component: `{"target": "TestObject", "componentName": "NonExistent", "properties": {"mass": 1}}`
6. ❌ Invalid property names: `{"target": "TestObject", "componentName": "Rigidbody2D", "properties": {"invalidProp": 1}}`
7. ❌ Empty properties dict: `{"target": "TestObject", "componentName": "Rigidbody2D", "properties": {}}`
8. ❌ Properties as string: Test if properties can be passed as JSON string

---

## Phase 4: Scene Operations - Broken Tool

### Tool: `load_scene`

**Note**: This tool is still broken. Parameter names use camelCase (`path`, `name`, `buildIndex`), but Unity doesn't recognize the parameters correctly.

**Prerequisites**: Create test scenes first using `create_scene`.

Test cases:
1. ❌ Load by path: `{"path": "Assets/Scenes/TestScene_001.unity"}`
   - **Expected**: Should load the scene
   - **Current behavior**: Unity reports "Either 'name'/'path' or 'buildIndex' must be provided"
   - **Debug**: Check if parameter is reaching Unity C# code correctly

2. ❌ Load by name: `{"name": "TestScene_001"}`
   - **Expected**: Should find scene in Assets/Scenes/ directory
   - **Current behavior**: Looks in wrong location (`Assets/TestScene_001.unity` instead of `Assets/Scenes/TestScene_001.unity`)
   - **Debug**: Check path resolution logic in Unity C# code

3. ✅ Load by buildIndex: `{"buildIndex": 0}` (if scene is in build settings)
   - **Test**: Verify this works if scene is in build settings

4. ❌ Load non-existent (should fail gracefully): `{"name": "NonExistentScene"}`
   - **Expected**: Should return clear error message
   - **Current behavior**: May fail with wrong path error

5. ❌ Invalid path: `{"path": "Invalid/Path.unity"}`
   - **Expected**: Should return clear error message

6. ❌ Invalid buildIndex: `{"buildIndex": 999}`
   - **Expected**: Should return clear error message

**Debugging Steps**:
1. Check Unity C# code in `ManageScene.cs` to see how parameters are being processed
2. Verify parameter names match exactly (`path`, `name`, `buildIndex` - camelCase)
3. Check if path sanitization logic is interfering with parameter recognition
4. Compare with `create_scene` which works - what's different?

---

## Phase 5: Material Operations - Blocked by Broken Tool

### Tool: `create_material`

**Note**: This tool is still broken. Folder creation code exists in `ManageMaterial.cs` but doesn't work correctly.

**Current Error**: "Parent directory must exist before creating asset"

Test cases:
1. ❌ Create with path only: `{"materialPath": "Assets/Materials/TestMaterial_001.mat"}`
   - **Expected**: Should create Materials folder if it doesn't exist, then create material
   - **Current behavior**: Fails with "Parent directory must exist before creating asset"
   - **Debug**: Check folder creation logic in `ManageMaterial.cs` lines 505-523

2. ❌ Create with shader: `{"materialPath": "Assets/Materials/TestMaterial_002.mat", "shader": "Standard"}`
   - **Blocked** by folder creation issue

3. ❌ Create with color: `{"materialPath": "Assets/Materials/TestMaterial_003.mat", "color": [1, 0, 0, 1]}`
   - **Blocked** by folder creation issue

4. ❌ Create with properties: `{"materialPath": "Assets/Materials/TestMaterial_004.mat", "properties": {"_Metallic": 0.5}}`
   - **Blocked** by folder creation issue

5. ❌ Invalid path: `{"materialPath": "Invalid/Path.mat"}`
   - **Expected**: Should return clear error message

6. ❌ Invalid shader: `{"materialPath": "Assets/Materials/Test.mat", "shader": "NonExistentShader"}`
   - **Blocked** by folder creation issue

**Debugging Steps**:
1. Check `ManageMaterial.cs` folder creation code (lines 505-523)
2. Verify path resolution: `Application.dataPath` vs directory path
3. Check if `AssetDatabase.Refresh()` is called at the right time
4. Try alternative: Use `AssetDatabase.CreateFolder` instead of `Directory.CreateDirectory`
5. Check if directory actually gets created but Unity doesn't see it (timing issue)

**Possible Workaround**:
- Try creating the Materials folder manually first using Unity's asset management
- Then test if material creation works when folder exists

---

### Tool: `set_material_color`

**Status**: ❌ **BLOCKED** - Cannot test until `create_material` is fixed.

**Prerequisites**: Once `create_material` works, create a material first.

Planned test cases (when material creation works):
1. Set color (array 0-1): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [0, 1, 0, 1]}`
2. Set color (array 0-255): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [0, 255, 0, 255]}` - Should convert to [0, 1, 0, 1]
3. Set color (JSON string): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": "[0,1,0,1]"}`
4. Set color with alpha: `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [1, 1, 0, 0.5]}`
5. Set HDR color (edge case): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [1.5, 0, 0, 1]}` - Should preserve 1.5 (not convert to 0-255 range)
6. Non-existent material: `{"materialPath": "Assets/Materials/NonExistent.mat", "color": [1, 0, 0, 1]}`
7. Invalid format: `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": "invalid"}`

---

### Tool: `assign_material`

**Status**: ❌ **BLOCKED** - Cannot test until `create_material` is fixed.

**Prerequisites**: Once `create_material` works, create material and GameObject with MeshRenderer.

Planned test cases (when material creation works):
1. Assign to MeshRenderer: `{"target": "TestObject", "materialPath": "Assets/Materials/TestMaterial_001.mat"}`
2. Assign to SpriteRenderer: Create object with SpriteRenderer, then assign
3. Assign to specific slot: `{"target": "TestObject", "materialPath": "Assets/Materials/TestMaterial_001.mat", "slot": 0}`
4. Assign to multiple renderers
5. Non-existent GameObject: `{"target": "NonExistent", "materialPath": "Assets/Materials/TestMaterial_001.mat"}`
6. GameObject without renderer: `{"target": "TestObject", "materialPath": "Assets/Materials/TestMaterial_001.mat"}` (if object has no renderer)
7. Non-existent material: `{"target": "TestObject", "materialPath": "Assets/Materials/NonExistent.mat"}`

---

## Summary of Remaining Issues

### Tools Needing Testing:
1. **`set_component_properties`**: Needs comprehensive testing (parameter mapping fixed, but not fully tested)

### Tools Still Broken:
2. **`create_material`**: Folder creation logic not working correctly
3. **`load_scene`**: Path parameter not being recognized by Unity C# code

### Tools Blocked:
4. **`set_material_color`**: Blocked by `create_material` failure
5. **`assign_material`**: Blocked by `create_material` failure

---

## Final Steps

1. **Generate Summary**: Create summary statistics at the top of the test results file:
   - Total tests performed
   - Passed count
   - Failed count
   - Blocked count
   - Known issues list

2. **Review Documentation**: Ensure all tests are documented with proper format

3. **Clean Up**: Remove all test objects, scenes, prefabs, and materials created during testing

4. **Document Workarounds**: If any workarounds are found, document them clearly

---

## Recommendations for Fixes

1. **`create_material` folder creation**: 
   - Debug the directory creation logic in `ManageMaterial.cs`
   - Consider using `AssetDatabase.CreateFolder` instead of `Directory.CreateDirectory`
   - Check timing issues with `AssetDatabase.Refresh()`

2. **`load_scene` path resolution**:
   - Debug Unity C# path handling in `ManageScene.cs`
   - Verify parameter names match exactly (camelCase: `path`, `name`, `buildIndex`)
   - Check if path sanitization logic is interfering
   - Compare working `create_scene` implementation with `load_scene`

3. **`set_component_properties`**:
   - Verify it works correctly with all property types
   - Test edge cases (empty dict, invalid properties, etc.)

---

**START HERE**: First perform the Initial Cleanup steps described above, then begin testing with `set_component_properties` (since it should work), followed by debugging `load_scene` and `create_material`.

