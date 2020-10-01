from .main_menu import GEM_MT_MainMenu

classes = (
    GEM_MT_MainMenu,
)

def register_menus():
    from .add_menu_entry import register_menu_entry
    register_menu_entry()

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister_menus():
    from .add_menu_entry import unregister_menu_entry
    unregister_menu_entry()

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
