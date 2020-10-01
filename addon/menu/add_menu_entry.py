import bpy

def menu_function(self, context):
    self.layout.operator("zag.add_camera_point", icon="CON_CAMERASOLVER")

def register_menu_entry():
    bpy.types.VIEW3D_MT_add.prepend(menu_function)

def unregister_menu_entry():
    bpy.types.VIEW3D_MT_add.remove(menu_function)
