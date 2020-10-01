from .main_menu import GEM_MT_MainMenu

classes = (
    GEM_MT_MainMenu,
)

def register_menus():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister_menus():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
