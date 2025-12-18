# Proposed Simplified Unity MCP Tools

This document proposes new, simpler MCP tools designed specifically for LLM agents. These tools address common pain points with the current action-based tools by providing focused, single-purpose tools with clear descriptions and straightforward parameters.

## Design Principles

1. **One Purpose Per Tool** - No `action` parameter needed, reducing the #1 source of errors
2. **Consistent Naming** - Same parameter names across all tools (e.g., always `target` for GameObject identifier)
3. **Clear Descriptions** - Each tool description explains exactly when and how to use it
4. **Simplified Parameters** - Flatten nested structures where possible, use consistent types
5. **Workflow-Oriented** - Tools match common game development workflows

## Current Pain Points Addressed

- ❌ **Missing `action` parameter** → ✅ Each tool has a single, clear purpose
- ❌ **Inconsistent parameter names** (`search_term` vs `name`, `component_name` vs `components_to_add`) → ✅ Consistent naming across all tools
- ❌ **Complex nested structures** → ✅ Flattened, intuitive parameter structures
- ❌ **Type confusion** (arrays vs strings, booleans vs strings) → ✅ Clear type requirements in descriptions

---

## Proposed Tools

### GameObject Operations

#### `create_gameobject`

**Purpose:** Create a new GameObject in the current scene. Use this when you need to add a new object to the scene hierarchy.

**When to use:**
- Creating player, enemy, or NPC GameObjects
- Creating manager GameObjects (GameManager, AudioManager, etc.)
- Creating environment objects (platforms, obstacles, triggers)
- Creating UI containers or organizational GameObjects

**Parameters:**
```typescript
{
  name: string                    // GameObject name (required)
  position?: [number, number, number]  // World position [x, y, z] (optional, default: [0, 0, 0])
  rotation?: [number, number, number]  // Euler rotation [x, y, z] in degrees (optional, default: [0, 0, 0])
  scale?: [number, number, number]     // Scale [x, y, z] (optional, default: [1, 1, 1])
  parent?: string                 // Parent GameObject name or path (optional)
  tag?: string                    // Tag name (optional)
  layer?: string                  // Layer name (optional)
  active?: boolean                // Set active state (optional, default: true)
  primitive_type?: "Cube" | "Sphere" | "Capsule" | "Cylinder" | "Plane" | "Quad"  // Create primitive shape (optional)
}
```

**Example:**
```json
{
  "name": "Enemy",
  "position": [5, 0, 0],
  "tag": "Enemy",
  "active": true
}
```

**Prerequisites:**
- Scene must be loaded
- Unity must not be compiling (`editor_state.isCompiling` must be `false`)

---

#### `find_gameobject`

**Purpose:** Find a GameObject in the current scene by name, tag, layer, or component. Use this before modifying or querying a GameObject to ensure it exists.

**When to use:**
- Before modifying an existing GameObject
- Before adding components to a GameObject
- To verify a GameObject exists before operations
- To find GameObjects by tag or layer for batch operations

**Parameters:**
```typescript
{
  search_by: "name" | "tag" | "layer" | "component"  // How to search (required)
  value: string                                       // What to search for (required)
  find_all?: boolean                                  // Return all matches (optional, default: false)
  include_inactive?: boolean                         // Include inactive GameObjects (optional, default: false)
  search_children?: boolean                          // Search in child objects (optional, default: false)
}
```

**Example:**
```json
{
  "search_by": "name",
  "value": "Player",
  "find_all": false
}
```

**Returns:** GameObject identifier(s) that can be used with other tools

---

#### `modify_gameobject`

**Purpose:** Modify GameObject properties (position, rotation, scale, name, parent, tag, layer, active state). Use this to change GameObject transform or basic properties.

**When to use:**
- Moving, rotating, or scaling a GameObject
- Renaming a GameObject
- Changing parent-child relationships
- Setting tag or layer
- Activating/deactivating a GameObject

**Parameters:**
```typescript
{
  target: string                    // GameObject name or path (required)
  name?: string                    // New name (optional)
  position?: [number, number, number]  // New position [x, y, z] (optional)
  rotation?: [number, number, number]  // New rotation [x, y, z] in degrees (optional)
  scale?: [number, number, number]     // New scale [x, y, z] (optional)
  parent?: string | null           // New parent name/path, or null to unparent (optional)
  tag?: string                     // New tag (optional)
  layer?: string                    // New layer (optional)
  active?: boolean                 // New active state (optional)
}
```

**Example:**
```json
{
  "target": "Enemy",
  "position": [10, 2, 0],
  "rotation": [0, 45, 0],
  "active": true
}
```

---

#### `delete_gameobject`

**Purpose:** Delete a GameObject from the scene. Use this to remove unwanted objects.

**When to use:**
- Removing test objects
- Cleaning up temporary GameObjects
- Removing objects that are no longer needed

**Parameters:**
```typescript
{
  target: string  // GameObject name or path (required)
}
```

**Example:**
```json
{
  "target": "TestObject"
}
```

---

### Component Operations

#### `add_component`

**Purpose:** Add a component to a GameObject. Use this to add functionality like physics, rendering, or custom scripts to GameObjects.


**When to use:**
- Adding Rigidbody2D/Rigidbody for physics
- Adding SpriteRenderer/MeshRenderer for visuals
- Adding Colliders for collision detection
- Adding custom MonoBehaviour scripts (after scripts are compiled)

**Parameters:**
```typescript
{
  target: string                    // GameObject name or path (required)
  component_type: string           // Component type name, e.g., "Rigidbody2D", "SpriteRenderer" (required)
  properties?: Record<string, any>  // Initial component properties (optional)
}
```

**Example:**
```json
{
  "target": "Enemy",
  "component_type": "Rigidbody2D",
  "properties": {
    "mass": 1.5,
    "gravityScale": 1.0
  }
}
```

**Prerequisites:**
- Component type must be compiled (check `editor_state.isCompiling` is `false`)
- For custom scripts, ensure script is created and Unity has finished compiling

---

#### `remove_component`

**Purpose:** Remove a component from a GameObject. Use this to remove unwanted components.

**When to use:**
- Removing components that are no longer needed
- Cleaning up test components
- Replacing components (remove old, add new)

**Parameters:**
```typescript
{
  target: string        // GameObject name or path (required)
  component_type: string  // Component type name to remove (required)
}
```

**Example:**
```json
{
  "target": "Enemy",
  "component_type": "Rigidbody2D"
}
```

---

#### `set_component_property`

**Purpose:** Set a single property on a component. Use this to configure component values after creation.

**When to use:**
- Setting Rigidbody mass, gravity scale
- Setting SpriteRenderer color, sorting order
- Setting Collider size, offset, isTrigger
- Setting Transform position, rotation, scale
- Setting any component property value

**Parameters:**
```typescript
{
  target: string        // GameObject name or path (required)
  component_type: string  // Component type name (required)
  property: string     // Property name, use dot notation for nested (e.g., "sharedMaterial.color") (required)
  value: any           // Property value (required)
}
```

**Example:**
```json
{
  "target": "Enemy",
  "component_type": "Rigidbody2D",
  "property": "mass",
  "value": 2.5
}
```

**Nested Property Example:**
```json
{
  "target": "Enemy",
  "component_type": "MeshRenderer",
  "property": "sharedMaterial.color",
  "value": [1, 0, 0, 1]
}
```

---

#### `set_component_properties`

**Purpose:** Set multiple properties on a component at once. Use this when configuring multiple properties to avoid multiple calls.

**When to use:**
- Initializing a component with multiple properties
- Batch updating component settings
- More efficient than multiple `set_component_property` calls

**Parameters:**
```typescript
{
  target: string                    // GameObject name or path (required)
  component_type: string           // Component type name (required)
  properties: Record<string, any>  // Dictionary of property names to values (required)
}
```

**Example:**
```json
{
  "target": "Enemy",
  "component_type": "Rigidbody2D",
  "properties": {
    "mass": 2.5,
    "gravityScale": 0.5,
    "drag": 0.1
  }
}
```

---

#### `get_component`

**Purpose:** Get information about a component on a GameObject. Use this to read component properties or verify a component exists.

**When to use:**
- Reading component property values
- Verifying component configuration
- Checking if a component exists before operations

**Parameters:**
```typescript
{
  target: string        // GameObject name or path (required)
  component_type: string  // Component type name (required)
  include_private?: boolean  // Include private serialized fields (optional, default: false)
}
```

**Example:**
```json
{
  "target": "Enemy",
  "component_type": "Transform"
}
```

---

### Prefab Operations

#### `create_prefab`

**Purpose:** Create a prefab from a scene GameObject. Use this to save a GameObject as a reusable prefab asset.

**When to use:**
- Converting player/enemy GameObjects to prefabs
- Creating reusable UI elements
- Saving configured GameObjects for later use
- Creating prefab variants

**Parameters:**
```typescript
{
  source_gameobject: string  // Scene GameObject name or path (required)
  prefab_path: string        // Prefab asset path, e.g., "Prefabs/Enemy.prefab" (required)
  allow_overwrite?: boolean  // Allow replacing existing prefab (optional, default: false)
}
```

**Example:**
```json
{
  "source_gameobject": "Enemy",
  "prefab_path": "Prefabs/Enemy.prefab",
  "allow_overwrite": false
}
```

**Prerequisites:**
- Source GameObject must exist in scene
- Prefab folder should exist (create via filesystem if needed)

---

#### `open_prefab`

**Purpose:** Open a prefab in isolation mode for editing. Use this before modifying a prefab's structure or components.

**When to use:**
- Before modifying prefab GameObjects or components
- Before adding/removing components from a prefab
- Before changing prefab hierarchy

**Parameters:**
```typescript
{
  prefab_path: string  // Prefab asset path, e.g., "Prefabs/Enemy.prefab" (required)
}
```

**Example:**
```json
{
  "prefab_path": "Prefabs/Enemy.prefab"
}
```

**Note:** After opening, use GameObject/Component tools to modify. Then call `save_prefab` and `close_prefab`.

---

#### `save_prefab`

**Purpose:** Save changes made to the currently open prefab. Use this after modifying a prefab in isolation mode.

**When to use:**
- After modifying prefab in isolation mode
- Before closing prefab stage
- To persist prefab changes

**Parameters:**
```typescript
{}  // No parameters - saves the currently open prefab
```

**Example:**
```json
{}
```

**Prerequisites:**
- Prefab must be open (via `open_prefab`)

---

#### `close_prefab`

**Purpose:** Close the prefab isolation mode and return to scene view. Use this after saving prefab changes.

**When to use:**
- After finishing prefab edits
- To return to scene editing
- After saving prefab changes

**Parameters:**
```typescript
{
  save_before_close?: boolean  // Save prefab before closing (optional, default: true)
}
```

**Example:**
```json
{
  "save_before_close": true
}
```

---

### Scene Operations

#### `create_scene`

**Purpose:** Create a new scene. Use this to set up new game scenes (main menu, gameplay, settings, etc.).

**When to use:**
- Creating main menu scene
- Creating gameplay scenes
- Creating loading/transition scenes
- Creating settings/options scenes

**Parameters:**
```typescript
{
  scene_name: string              // Scene name (required)
  scene_path?: string             // Full path, e.g., "Scenes/MainMenu.unity" (optional)
  add_camera?: boolean            // Add main camera (optional, default: true)
  add_light?: boolean             // Add directional light (optional, default: true for 3D)
}
```

**Example:**
```json
{
  "scene_name": "MainMenu",
  "scene_path": "Scenes/MainMenu.unity",
  "add_camera": true,
  "add_light": false
}
```

---

#### `load_scene`

**Purpose:** Load a scene. Use this to switch between scenes or load a specific scene for editing.

**When to use:**
- Switching to a different scene
- Loading a scene for modification
- Loading scene by name or path

**Parameters:**
```typescript
{
  scene_path?: string    // Scene path, e.g., "Scenes/MainMenu.unity" (optional if name provided)
  scene_name?: string    // Scene name (optional if path provided)
  build_index?: number   // Build index number (optional)
}
```

**Example:**
```json
{
  "scene_path": "Scenes/MainMenu.unity"
}
```

---

#### `save_scene`

**Purpose:** Save the current scene. Use this to persist scene changes.

**When to use:**
- After making scene modifications
- Before switching scenes
- Before running tests
- Periodically during scene editing

**Parameters:**
```typescript
{
  scene_path?: string  // Optional: save with new path/name
}
```

**Example:**
```json
{}
```

---

#### `get_scene_hierarchy`

**Purpose:** Get the hierarchy of GameObjects in the current scene. Use this to see what objects exist in the scene.

**When to use:**
- Inspecting scene structure
- Finding GameObjects in scene
- Verifying scene setup
- Debugging scene issues

**Parameters:**
```typescript
{}  // No parameters - returns current scene hierarchy
```

**Example:**
```json
{}
```

---

### Material Operations

#### `create_material`

**Purpose:** Create a new material asset. Use this to create materials for rendering GameObjects.

**When to use:**
- Creating materials for sprites/meshes
- Creating UI materials
- Creating particle effect materials
- Setting up material presets

**Parameters:**
```typescript
{
  material_path: string           // Material asset path, e.g., "Materials/RedMaterial.mat" (required)
  shader?: string                 // Shader name, e.g., "Standard", "Unlit/Color" (optional, default: "Standard")
  color?: [number, number, number, number]  // Base color [r, g, b, a] (optional)
  properties?: Record<string, any>  // Additional shader properties (optional)
}
```

**Example:**
```json
{
  "material_path": "Materials/EnemyMaterial.mat",
  "shader": "Standard",
  "color": [1, 0, 0, 1]
}
```

---

#### `set_material_color`

**Purpose:** Set the color of a material. Use this to change material appearance.

**When to use:**
- Changing material color
- Creating material variants with different colors
- Updating material appearance

**Parameters:**
```typescript
{
  material_path: string                    // Material asset path (required)
  color: [number, number, number, number]  // Color [r, g, b, a] (required)
}
```

**Example:**
```json
{
  "material_path": "Materials/EnemyMaterial.mat",
  "color": [0, 1, 0, 1]
}
```

---

#### `assign_material`

**Purpose:** Assign a material to a renderer component on a GameObject. Use this to apply materials to GameObjects.

**When to use:**
- Applying materials to sprites/meshes
- Changing GameObject appearance
- Assigning materials to renderers

**Parameters:**
```typescript
{
  target: string        // GameObject name or path (required)
  material_path: string  // Material asset path (required)
  slot?: number        // Material slot index (optional, default: 0)
}
```

**Example:**
```json
{
  "target": "Enemy",
  "material_path": "Materials/EnemyMaterial.mat",
  "slot": 0
}
```

---

### Editor Control

#### `check_compilation_status`

**Purpose:** Check if Unity is currently compiling scripts. Use this before operations that require compiled code.

**When to use:**
- Before adding components (especially custom scripts)
- Before running tests
- Before operations that need compiled types
- To wait for compilation to complete

**Parameters:**
```typescript
{}  // No parameters - returns compilation status
```

**Returns:**
```typescript
{
  is_compiling: boolean  // True if Unity is compiling
  has_errors: boolean    // True if compilation has errors
}
```

**Example:**
```json
{}
```

---

#### `wait_for_compilation`

**Purpose:** Wait for Unity compilation to complete. Use this after script changes before operations requiring compiled code.

**When to use:**
- After creating/modifying scripts (via file editing)
- Before adding components that use custom scripts
- Before running tests
- To ensure Unity is ready for operations

**Parameters:**
```typescript
{
  timeout_seconds?: number  // Maximum time to wait (optional, default: 60)
  check_errors?: boolean    // Check for compilation errors after completion (optional, default: true)
}
```

**Example:**
```json
{
  "timeout_seconds": 30,
  "check_errors": true
}
```

---

#### `get_console_errors`

**Purpose:** Get errors and warnings from Unity console. Use this to check for compilation errors or runtime issues.

**When to use:**
- After script compilation
- After MCP operations
- To debug issues
- To verify no errors exist

**Parameters:**
```typescript
{
  types?: ("error" | "warning" | "log")[]  // Message types to get (optional, default: ["error", "warning"])
  count?: number                            // Max messages to return (optional, default: 10)
  include_stacktrace?: boolean              // Include stack traces (optional, default: false)
}
```

**Example:**
```json
{
  "types": ["error", "warning"],
  "count": 10
}
```

---

#### `clear_console`

**Purpose:** Clear the Unity console. Use this to clean up console output.

**When to use:**
- Before running tests
- To clear old messages
- For cleaner console output

**Parameters:**
```typescript
{}  // No parameters
```

**Example:**
```json
{}
```

---

#### `set_play_mode`

**Purpose:** Control Unity play mode (play, pause, stop). Use this to test gameplay.

**When to use:**
- Starting play mode to test game
- Pausing play mode
- Stopping play mode

**Parameters:**
```typescript
{
  mode: "play" | "pause" | "stop"  // Play mode action (required)
}
```

**Example:**
```json
{
  "mode": "play"
}
```

---

#### `add_tag`

**Purpose:** Add a tag to the project. Use this to create custom tags for GameObjects.

**When to use:**
- Creating game-specific tags (Player, Enemy, Pickup, etc.)
- Setting up tag system for collision detection
- Organizing GameObjects with tags

**Parameters:**
```typescript
{
  tag_name: string  // Tag name to add (required)
}
```

**Example:**
```json
{
  "tag_name": "Enemy"
}
```

---

#### `add_layer`

**Purpose:** Add a layer to the project. Use this to create custom layers for collision matrix.

**When to use:**
- Creating game-specific layers
- Setting up collision layers
- Organizing GameObjects by layer

**Parameters:**
```typescript
{
  layer_name: string  // Layer name to add (required)
}
```

**Example:**
```json
{
  "layer_name": "Enemies"
}
```

---

## Comparison: Current vs Proposed

### Current Tool (Complex)
```json
{
  "tool": "mcp_unityMCP_manage_gameobject",
  "params": {
    "action": "create",  // ❌ Easy to forget
    "name": "Enemy",
    "position": [0, 0, 0]
  }
}
```

### Proposed Tool (Simple)
```json
{
  "tool": "create_gameobject",
  "params": {
    "name": "Enemy",  // ✅ Clear purpose, no action needed
    "position": [0, 0, 0]
  }
}
```

### Current Tool (Inconsistent)
```json
{
  "tool": "mcp_unityMCP_manage_gameobject",
  "params": {
    "action": "find",
    "search_method": "by_name",
    "search_term": "Player"  // ❌ Why "search_term" not "name"?
  }
}
```

### Proposed Tool (Consistent)
```json
{
  "tool": "find_gameobject",
  "params": {
    "search_by": "name",  // ✅ Clear and consistent
    "value": "Player"
  }
}
```

### Current Tool (Confusing)
```json
{
  "tool": "mcp_unityMCP_manage_gameobject",
  "params": {
    "action": "add_component",
    "target": "Enemy",
    "component_name": "Rigidbody2D"  // ❌ Why not "component_type"?
  }
}
```

### Proposed Tool (Clear)
```json
{
  "tool": "add_component",
  "params": {
    "target": "Enemy",
    "component_type": "Rigidbody2D"  // ✅ Clear and consistent
  }
}
```

---

## Migration Strategy

1. **Keep existing tools** for backward compatibility
2. **Add new tools** alongside existing ones
3. **Update documentation** to prefer new tools
4. **Gradually deprecate** action-based tools once new tools are validated

---

## Benefits for LLM Agents

1. **No action parameter** - Eliminates #1 error source
2. **Consistent naming** - `target`, `component_type`, `search_by` used consistently
3. **Clear descriptions** - Each tool explains when and how to use it
4. **Workflow-oriented** - Tools match common game development tasks
5. **Simpler parameters** - Flattened structures, clear types
6. **Better tool selection** - LLMs can better match tasks to tools

---

## Next Steps

1. Review and refine tool proposals
2. Prioritize which tools to implement first
3. Create implementation plan
4. Test with LLM agents
5. Iterate based on feedback


