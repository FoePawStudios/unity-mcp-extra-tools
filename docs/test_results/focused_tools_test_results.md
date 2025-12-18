# Focused Tools Test Results

Generated: 2025-01-18

## Summary

- **Total Tests**: 8
- **Passed**: 4
- **Failed**: 3
- **Partial**: 1
- **Blocked**: 0
- **Known Issues**: 
  - `create_material`: Recursive folder creation has a bug - fails when parent folder doesn't exist. Workaround: Create folders manually first.
  - `load_scene`: Path handling issues when loading by path or name. Needs further investigation.

---

## Test Results by Tool

### Tool: create_material

**Status**: ⚠️ PARTIAL - Works when folder exists, but recursive folder creation fails

#### Test: Create with path only (folder exists)
- **Status**: ✅ PASS
- **Parameters**: `{"materialPath": "Assets/Materials/TestMaterial_001.mat"}`
- **Result**: `{"status":"success","message":"Created material at Assets/Materials/TestMaterial_001.mat with shader Standard"}`
- **Errors**: None
- **Note**: Folder was created manually first using `manage_asset` with `action: create_folder`

#### Test: Create with nested path (folder doesn't exist)
- **Status**: ❌ FAIL
- **Parameters**: `{"materialPath": "Assets/Materials/SubFolder/TestMaterial_002.mat"}`
- **Result**: `{"status":"error","message":"Creating asset at path Assets/Materials/SubFolder/TestMaterial_002.mat failed."}`
- **Errors**: Unity console shows: "Parent directory must exist before creating asset"
- **Issue**: The `EnsureFolderExists` method is not working correctly for recursive folder creation. The fix that was supposed to use `AssetDatabase.CreateFolder` recursively is not functioning as expected.

#### Test: Create with shader
- **Status**: ✅ PASS
- **Parameters**: `{"materialPath": "Assets/Materials/TestMaterial_003.mat", "shader": "Standard"}`
- **Result**: `{"status":"success","message":"Created material at Assets/Materials/TestMaterial_003.mat with shader Standard"}`
- **Errors**: None

#### Test: Create with color
- **Status**: ✅ PASS
- **Parameters**: `{"materialPath": "Assets/Materials/TestMaterial_004.mat", "color": [1, 0, 0, 1]}`
- **Result**: `{"status":"success","message":"Created material at Assets/Materials/TestMaterial_004.mat with shader Standard"}`
- **Errors**: None

---

### Tool: set_material_color

**Status**: ✅ PASS - Works correctly

#### Test: Set color (array 0-1)
- **Status**: ✅ PASS
- **Parameters**: `{"materialPath": "Assets/Materials/TestMaterial_004.mat", "color": [0, 1, 0, 1]}`
- **Result**: `{"status":"success","message":"Set color on _Color"}`
- **Errors**: None
- **Note**: Successfully changed material color from red [1,0,0,1] to green [0,1,0,1]

---

### Tool: assign_material

**Status**: ✅ PASS - Works correctly

#### Test: Assign to MeshRenderer
- **Status**: ✅ PASS
- **Parameters**: `{"target": "TestObject_Mat", "materialPath": "Assets/Materials/TestMaterial_004.mat"}`
- **Result**: `{"status":"success","message":"Assigned material TestMaterial_004 to TestObject_Mat slot 0"}`
- **Errors**: None
- **Note**: Successfully assigned material to a GameObject with MeshRenderer component

---

### Tool: load_scene

**Status**: ❌ FAIL - Multiple path handling issues

#### Test: Load by path (with .unity extension)
- **Status**: ❌ FAIL
- **Parameters**: `{"path": "Assets/Scenes/TestScene_001.unity"}`
- **Result**: `{"success":false,"code":"Either 'name'/'path' or 'buildIndex' must be provided for 'load' action."}`
- **Errors**: Unity reports that path/name/buildIndex wasn't provided, even though path was explicitly provided
- **Issue**: The path parameter might not be reaching Unity correctly, or there's an issue with parameter mapping

#### Test: Load by path (without .unity extension)
- **Status**: ❌ FAIL
- **Parameters**: `{"path": "Assets/Scenes/TestScene_001"}`
- **Result**: `{"success":false,"message":"Scene name contains invalid characters. Must start with a letter and contain only letters, numbers, and underscores."}`
- **Errors**: Path validation is incorrectly treating the path as a scene name
- **Issue**: Path validation logic is incorrectly processing paths without extensions

#### Test: Load by name
- **Status**: ❌ FAIL
- **Parameters**: `{"name": "TestScene_001"}`
- **Result**: `{"success":false,"code":"Scene file not found at 'Assets/Scenes/TestScene_001.unity/TestScene_001.unity'."}`
- **Errors**: Path duplication issue - the constructed path includes the scene name twice
- **Issue**: Path construction logic is duplicating the scene name when building paths from names

---

### Tool: set_component_properties

**Status**: ⚠️ NOT FULLY TESTED - Tool exists but couldn't test due to scene/object issues

#### Note
- Tool is registered and available in the MCP server
- Attempted to test but test objects were lost when scenes changed
- Tool signature accepts `properties` as `dict[str, Any] | str`
- Need to test with actual objects in scene to verify functionality
- Related tool `set_component_property` (single property) also exists but wasn't testable due to object availability

---

## Detailed Findings

### create_material - Recursive Folder Creation Bug

**Issue**: The `EnsureFolderExists` method in `ManageMaterial.cs` is not correctly creating nested folders recursively.

**Symptom**: When trying to create a material at a path like `Assets/Materials/SubFolder/TestMaterial.mat` where `SubFolder` doesn't exist, the creation fails with "Parent directory must exist before creating asset".

**Root Cause**: The recursive folder creation logic in `EnsureFolderExists` appears to have issues with path handling, possibly related to how `Path.GetDirectoryName` processes forward-slash paths on Windows.

**Workaround**: Manually create required folders using `manage_asset` with `action: create_folder` before creating materials.

**Recommendation**: Review and fix the `EnsureFolderExists` method in `ManageMaterial.cs` to properly handle recursive folder creation using `AssetDatabase.CreateFolder`.

### load_scene - Path Handling Issues

**Issue**: Multiple issues with path handling in the `load_scene` tool.

**Symptoms**:
1. Loading by path reports that no path/name/buildIndex was provided even when path is explicitly given
2. Loading by path without extension incorrectly validates the path as a scene name
3. Loading by name constructs incorrect paths with duplicated scene names

**Root Cause**: The path normalization and parameter mapping between Python tool and Unity C# handler appears to have issues. The Python tool sends `path` parameter, but Unity may be expecting `relativePath` or there's a mismatch in how parameters are processed.

**Recommendation**: Review the parameter mapping between `load_scene.py` and `ManageScene.cs` HandleCommand method to ensure paths are correctly normalized and passed through.

### Working Tools

The following tools are working correctly:
- ✅ `create_material` (when folders exist)
- ✅ `set_material_color`
- ✅ `assign_material`

These tools successfully handle their core functionality and can be used in production with the noted workarounds.

---

## Recommendations

1. **Fix recursive folder creation in `create_material`**: The `EnsureFolderExists` method needs to be reviewed and fixed to properly create nested folder structures.

2. **Fix path handling in `load_scene`**: Review parameter mapping and path normalization between Python tool and Unity C# handler to ensure consistent behavior.

3. **Test `set_component_properties`**: This tool needs comprehensive testing once test objects can be reliably maintained across scene operations.

4. **Consider adding integration tests**: Automated tests for these tools would help catch regressions and ensure fixes work correctly.

---

