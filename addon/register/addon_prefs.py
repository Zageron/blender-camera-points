import bpy

def update_panel(self, context):
    print("nope")

class CameraPointPanelPreferences(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__.split(".")[0]

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.label(text="Nothing")

def register_addon_preferences():
    bpy.utils.register_class(CameraPointPanelPreferences)

def unregister_addon_preferences():
    bpy.utils.unregister_class(CameraPointPanelPreferences)
