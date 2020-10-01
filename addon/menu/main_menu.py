import bpy

class GEM_MT_MainMenu(bpy.types.Menu):
    bl_idname = "GEM_MT_MainMenu"
    bl_label = "Gemini Main Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = "INVOKE_DEFAULT"
        layout.label(text='Gemini Tools')
        layout.operator("gem.add_lights", text="Add Lights", icon="LIGHT")
