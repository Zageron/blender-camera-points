bl_info = {
    "name": "Zageron's Camera Point Manager",
    "description": "Camera and perspective manager.",
    "author": "Zageron",
    "version": (1, 0),
    "blender": (2, 83, 0),
    "location": "View3D",
    "category": "3D View",
}

def register():
    from .addon.register import register_addon
    register_addon()

def unregister():
    from .addon.register import unregister_addon
    unregister_addon()
