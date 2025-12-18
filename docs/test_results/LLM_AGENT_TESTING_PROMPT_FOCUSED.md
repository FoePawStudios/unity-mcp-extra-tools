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

Most tools have been fixed and are working correctly. The following tools need testing after recent fixes:

1. **`set_component_properties`**: Needs comprehensive testing to verify it works correctly
2. **`create_material`**: ✅ **FIXED** - Now requires parent folders to exist (created via `manage_asset`). Returns clear error if folder doesn't exist. **NEEDS TESTING** to verify the fix works correctly
3. **`load_scene`**: ✅ **COMPREHENSIVELY FIXED** - Fixed path parameter recognition, path duplication prevention, Windows path handling, and added extensive logging. **NEEDS TESTING** to verify all fixes work correctly
4. **`set_material_color`**: ✅ **FIXED** - Color parsing now correctly handles 0-255 range colors with zero components. **NEEDS TESTING** to verify the fix works correctly
5. **`assign_material`**: ✅ **UNBLOCKED** - Can now test since `create_material` has been fixed

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

## Phase 4: Scene Operations - Fixed Tool (Needs Testing)

### Tool: `load_scene`

**Note**: This tool has been **COMPREHENSIVELY FIXED** with extensive logging added for debugging. **NEEDS TESTING** to verify all fixes work correctly.

**Recent Fixes Applied**:
1. **Path parameter recognition**: Fixed issue where Unity didn't recognize `path` parameter even when explicitly provided
   - Added defensive checks to ensure path is never lost during normalization
   - Path is preserved even if normalization fails
   - Fixed Windows path handling by normalizing separators before `Path.GetDirectoryName()` calls

2. **Path duplication prevention**: Fixed issue where loading by name created duplicated paths like `"Assets/Scenes/TestScene_001.unity/TestScene_001.unity"`
   - Python tool now only sends `path` OR `name`, never both
   - When path is constructed from name, only `path` is sent (name is omitted)
   - Unity code ignores `name` parameter when `path` is provided

3. **Extensive logging**: Added comprehensive logging throughout the entire path transformation pipeline
   - Unity: Logs at entry, normalization, directory extraction, relativePath construction, fullPath construction, routing, and LoadScene method
   - Python: Logs parameter reception, path construction, parameter dictionary, and transport layer
   - All logs use structured format: `[ManageScene] [STEP_NAME] key='value'`
   - Logs include explicit null/empty indicators for debugging

**Prerequisites**: Create test scenes first using `create_scene`.

**Debugging**: If tests fail, check Unity Console for `[ManageScene]` log entries to trace the exact point of failure.

Test cases:
1. ✅ Load by path: `{"path": "Assets/Scenes/TestScene_001.unity"}`
   - **Expected**: Should load the scene successfully
   - **Previous issue**: Unity reported "Either 'name'/'path' or 'buildIndex' must be provided" even though path was sent
   - **Fix applied**: Defensive path normalization with preservation of original path if normalization fails

2. ✅ Load by path without extension: `{"path": "Assets/Scenes/TestScene_001"}`
   - **Expected**: Should automatically add `.unity` extension and load the scene
   - **Fix applied**: Extension is added automatically if missing during normalization

3. ✅ Load by name: `{"name": "TestScene_001"}`
   - **Expected**: Should find scene in Assets/Scenes/ directory and load successfully
   - **Previous issue**: Path duplication occurred - `"Assets/Scenes/TestScene_001.unity/TestScene_001.unity"`
   - **Fix applied**: Python only sends `name` (not both path and name), preventing duplication

4. ✅ Load by buildIndex: `{"buildIndex": 0}` (if scene is in build settings)
   - **Test**: Verify this works if scene is in build settings
   - **Note**: This path was already working, but verify it still works after fixes

5. ❌ Load non-existent (should fail gracefully): `{"name": "NonExistentScene"}`
   - **Expected**: Should return clear error message: "Scene file not found at 'Assets/Scenes/NonExistentScene.unity'"
   - **Check logs**: Verify logging shows correct path construction

6. ❌ Invalid path: `{"path": "Invalid/Path.unity"}`
   - **Expected**: Should return clear error message about file not found
   - **Check logs**: Verify path normalization and file existence check in logs

7. ❌ Invalid buildIndex: `{"buildIndex": 999}`
   - **Expected**: Should return clear error message about invalid build index

---

## Phase 5: Material Operations - Fixed Tool (Needs Testing)

### Tool: `create_material`

**Note**: This tool has been **FIXED**. It now requires parent folders to exist before creating materials (created via `manage_asset` with `action: create_folder`). **NEEDS TESTING** to verify the fix works correctly.

**Recent Fix**: 
- Removed recursive folder creation code
- Now checks if parent directory exists using `AssetDatabase.IsValidFolder()`
- Returns clear error message if folder doesn't exist, directing users to create folders first
- Tool description updated to set expectation that paths must exist

**Previous Error**: "Parent directory must exist before creating asset"

**IMPORTANT**: Before testing, ensure parent folders exist. Use `manage_asset` with `action: create_folder` to create folders if needed.

Test cases:
1. ✅ Create with existing folder: `{"materialPath": "Assets/Materials/TestMaterial_001.mat"}`
   - **Prerequisites**: Create `Assets/Materials/` folder first using `manage_asset` with `action: create_folder`
   - **Expected**: Should create material successfully
   - **Previous issue**: Failed with "Parent directory must exist before creating asset"
   - **Fix applied**: Clear error message now directs users to create folders first

2. ✅ Create with nested path: `{"materialPath": "Assets/Materials/SubFolder/TestMaterial_002.mat"}`
   - **Prerequisites**: Create `Assets/Materials/SubFolder/` folder structure first
   - **Expected**: Should create material successfully if folder exists
   - **Fix applied**: Returns clear error if folder doesn't exist

3. ✅ Create with shader: `{"materialPath": "Assets/Materials/TestMaterial_003.mat", "shader": "Standard"}`
   - **Expected**: Should create material with specified shader

4. ✅ Create with color: `{"materialPath": "Assets/Materials/TestMaterial_004.mat", "color": [1, 0, 0, 1]}`
   - **Expected**: Should create material with specified color

5. ✅ Create with properties: `{"materialPath": "Assets/Materials/TestMaterial_005.mat", "properties": {"_Metallic": 0.5}}`
   - **Expected**: Should create material with specified properties

6. ❌ Create without parent folder (should fail gracefully): `{"materialPath": "Assets/Materials/TestMaterial_006.mat"}`
   - **Prerequisites**: Ensure `Assets/Materials/` folder does NOT exist
   - **Expected**: Should return clear error message directing user to create folder first

7. ❌ Invalid path: `{"materialPath": "Invalid/Path.mat"}`
   - **Expected**: Should return clear error message

8. ❌ Invalid shader: `{"materialPath": "Assets/Materials/Test.mat", "shader": "NonExistentShader"}`
   - **Expected**: Should return clear error message about shader not found

---

### Tool: `set_material_color`

**Status**: ✅ **FIXED** - Color parsing now correctly handles 0-255 range colors with zero components. **NEEDS TESTING** to verify the fix works correctly.

**Recent Fix**: 
- Fixed color parsing heuristic to correctly detect 0-255 range colors even when some RGB components are zero
- Changed detection from `all(1.0 < val <= 255.0)` to `any(val > 1.0) and all(0.0 <= val <= 255.0)`
- Now correctly converts colors like `[128, 0, 0, 255]` to `[0.5, 0, 0, 1]` instead of incorrectly clamping

**Prerequisites**: Create a material first using `create_material` (with folder already created).

Test cases:
1. ✅ Set color (array 0-1): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [0, 1, 0, 1]}`
   - **Expected**: Should set color correctly

2. ✅ Set color (array 0-255): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [0, 255, 0, 255]}`
   - **Expected**: Should convert to [0, 1, 0, 1] automatically
   - **Previous issue**: Colors with zero components like `[128, 0, 0, 255]` were incorrectly clamped
   - **Fix applied**: Zero components are now correctly identified as being in 0-255 range

3. ✅ Set color with zero components (edge case): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [128, 0, 0, 255]}`
   - **Expected**: Should convert to [0.5, 0, 0, 1] (medium red with zero green and blue)
   - **This test verifies the zero-component fix**

4. ✅ Set color (JSON string): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": "[0,1,0,1]"}`
   - **Expected**: Should parse JSON string and set color correctly

5. ✅ Set color with alpha: `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [1, 1, 0, 0.5]}`
   - **Expected**: Should set color with alpha channel

6. ✅ Set HDR color (edge case): `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": [1.5, 0, 0, 1]}`
   - **Expected**: Should preserve 1.5 (not convert to 0-255 range since 1.5 is not <= 255.0)

7. ❌ Non-existent material: `{"materialPath": "Assets/Materials/NonExistent.mat", "color": [1, 0, 0, 1]}`
   - **Expected**: Should return clear error message

8. ❌ Invalid format: `{"materialPath": "Assets/Materials/TestMaterial_001.mat", "color": "invalid"}`
   - **Expected**: Should return clear error message

---

### Tool: `assign_material`

**Status**: ✅ **UNBLOCKED** - Can now test since `create_material` has been fixed.

**Prerequisites**: Create material using `create_material` and GameObject with MeshRenderer.

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

### Tools Needing Testing (Fixed but Not Verified):
1. **`set_component_properties`**: Needs comprehensive testing (parameter mapping fixed, but not fully tested)
2. **`create_material`**: ✅ **FIXED** - Now requires parent folders to exist (created via `manage_asset`). Returns clear error if folder doesn't exist. **NEEDS TESTING** to verify fix works
3. **`load_scene`**: ✅ **COMPREHENSIVELY FIXED** - Fixed path parameter recognition, path duplication prevention, Windows path handling, and added extensive logging. **NEEDS TESTING** to verify all fixes work
4. **`set_material_color`**: ✅ **FIXED** - Color parsing now correctly handles 0-255 range colors with zero components. **NEEDS TESTING** to verify fix works
5. **`assign_material`**: ✅ **UNBLOCKED** - Can now test since `create_material` is fixed

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

## Recent Fixes Applied

1. **`create_material` folder handling**: ✅ **FIXED**
   - Removed recursive folder creation code to simplify tool and avoid merge conflicts
   - Now requires parent folders to exist before creating materials
   - Uses `AssetDatabase.IsValidFolder()` to check folder existence
   - Returns clear error message directing users to create folders via `manage_asset` with `action: create_folder`
   - Tool description updated to set expectation that paths must exist

2. **`load_scene` path handling**: ✅ **COMPREHENSIVELY FIXED**
   - **Path parameter recognition**: Fixed critical bug where Unity didn't recognize `path` parameter even when explicitly provided
     - Added defensive checks to ensure path is never lost during normalization
     - Path is preserved even if `SanitizeAssetPath` returns null/empty
     - Fixed Windows path handling by normalizing separators BEFORE `Path.GetDirectoryName()` calls
   - **Path duplication prevention**: Fixed issue where loading by name created duplicated paths
     - Python tool now only sends `path` OR `name`, never both (prevents Unity from processing both)
     - When path is constructed from name, only `path` is sent to Unity
     - Unity code completely ignores `name` parameter when `path` is provided
   - **Extensive logging**: Added comprehensive logging throughout entire pipeline for debugging
     - Unity: 7 logging points (entry, normalize, dir_extract, rel_path, full_path, route, load)
     - Python: 4 logging points (entry, path_construct, params, transport)
     - Structured format: `[ManageScene] [STEP_NAME] key='value'` with explicit null/empty indicators
     - All logging wrapped in try-catch to prevent failures from breaking flow

3. **`set_material_color` color parsing**: ✅ **FIXED**
   - Fixed color parsing heuristic to correctly detect 0-255 range colors with zero components
   - Changed from `all(1.0 < val <= 255.0)` to `any(val > 1.0) and all(0.0 <= val <= 255.0)`
   - Now correctly converts colors like `[128, 0, 0, 255]` instead of incorrectly clamping

4. **`set_component_properties`**:
   - Needs comprehensive testing to verify it works correctly
   - Test edge cases (empty dict, invalid properties, etc.)

---

**START HERE**: First perform the Initial Cleanup steps described above, then begin testing with:
1. `set_component_properties` (should work, needs verification)
2. `create_material` (recently fixed - requires folders to exist, needs testing to verify)
3. `load_scene` (recently fixed, needs testing to verify)
4. `set_material_color` (recently fixed - color parsing improved, needs testing to verify)
5. `assign_material` (now unblocked, can test)

