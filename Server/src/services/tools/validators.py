"""Input validation functions for simplified MCP tools."""

from __future__ import annotations

import re
from typing import Any


def validate_gameobject_name(name: str | None) -> tuple[bool, str | None]:
    """
    Validate GameObject identifier.
    
    Args:
        name: GameObject name or path
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "GameObject name cannot be empty"
    
    if not isinstance(name, str):
        return False, "GameObject name must be a string"
    
    # Basic validation: non-empty, reasonable length
    if len(name.strip()) == 0:
        return False, "GameObject name cannot be whitespace only"
    
    if len(name) > 256:  # Unity's reasonable limit
        return False, "GameObject name is too long (max 256 characters)"
    
    return True, None


def validate_component_type(component_type: str | None) -> tuple[bool, str | None]:
    """
    Validate component type name.
    
    Args:
        component_type: Component type name (e.g., "Rigidbody2D", "SpriteRenderer")
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not component_type:
        return False, "Component type cannot be empty"
    
    if not isinstance(component_type, str):
        return False, "Component type must be a string"
    
    component_type = component_type.strip()
    
    if len(component_type) == 0:
        return False, "Component type cannot be whitespace only"
    
    # Unity component names are typically PascalCase, but we'll be lenient
    # Just check for reasonable characters (alphanumeric, dots, underscores)
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_.]*$", component_type):
        return False, f"Component type '{component_type}' contains invalid characters. Must start with a letter and contain only letters, numbers, dots, and underscores."
    
    return True, None


def validate_scene_path(scene_path: str | None) -> tuple[bool, str | None]:
    """
    Validate scene path format.
    
    Args:
        scene_path: Scene path (e.g., "Assets/Scenes/Main.unity", "Assets/Scenes/Main", or "Main")
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not scene_path:
        return False, "Scene path cannot be empty"
    
    if not isinstance(scene_path, str):
        return False, "Scene path must be a string"
    
    scene_path = scene_path.strip()
    
    if len(scene_path) == 0:
        return False, "Scene path cannot be whitespace only"
    
    # Check if it's a path (starts with Assets/) or a scene name
    if scene_path.startswith("Assets/"):
        # Path format - Unity will automatically add .unity extension if missing
        # Validate path doesn't contain invalid characters
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        for char in invalid_chars:
            if char in scene_path:
                return False, f"Scene path contains invalid character: '{char}'"
        
        # If it ends with .unity, ensure it's a valid path format
        if scene_path.endswith(".unity"):
            if not re.match(r"^Assets/.*\.unity$", scene_path):
                return False, "Scene path must start with 'Assets/' and end with '.unity'"
        # Otherwise, it's a valid path without extension (Unity will add it)
    else:
        # Scene name only - validate it's a reasonable name
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", scene_path):
            return False, "Scene name contains invalid characters. Must start with a letter and contain only letters, numbers, and underscores."
    
    return True, None


def validate_prefab_path(prefab_path: str | None) -> tuple[bool, str | None]:
    """
    Validate prefab path format.
    
    Args:
        prefab_path: Prefab path (e.g., "Assets/Prefabs/Player.prefab")
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not prefab_path:
        return False, "Prefab path cannot be empty"
    
    if not isinstance(prefab_path, str):
        return False, "Prefab path must be a string"
    
    prefab_path = prefab_path.strip()
    
    if len(prefab_path) == 0:
        return False, "Prefab path cannot be whitespace only"
    
    # Prefab paths must start with Assets/ and end with .prefab
    if not prefab_path.startswith("Assets/"):
        return False, "Prefab path must start with 'Assets/'"
    
    if not prefab_path.endswith(".prefab"):
        return False, "Prefab path must end with '.prefab'"
    
    # Validate path doesn't contain invalid characters
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    for char in invalid_chars:
        if char in prefab_path:
            return False, f"Prefab path contains invalid character: '{char}'"
    
    return True, None


def validate_material_path(material_path: str | None) -> tuple[bool, str | None]:
    """
    Validate material path format.
    
    Args:
        material_path: Material path (e.g., "Assets/Materials/MyMaterial.mat")
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not material_path:
        return False, "Material path cannot be empty"
    
    if not isinstance(material_path, str):
        return False, "Material path must be a string"
    
    material_path = material_path.strip()
    
    if len(material_path) == 0:
        return False, "Material path cannot be whitespace only"
    
    # Material paths must start with Assets/ and end with .mat
    if not material_path.startswith("Assets/"):
        return False, "Material path must start with 'Assets/'"
    
    if not material_path.endswith(".mat"):
        return False, "Material path must end with '.mat'"
    
    # Validate path doesn't contain invalid characters
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    for char in invalid_chars:
        if char in material_path:
            return False, f"Material path contains invalid character: '{char}'"
    
    return True, None

