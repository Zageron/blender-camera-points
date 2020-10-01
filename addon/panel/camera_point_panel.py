import bpy

bl_info = {
    "name" : "Camera Point Panel",
    "author" : "Zageron",
    "description" : "Panel for controlling the camera point properties on a node.",
    "blender" : (2, 90, 0),
    "version" : (0, 1, 0),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Zageron"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

class ZAG_CameraPointPanel(View3DPanel, bpy.types.Panel):
    bl_idname = "ZAG_PT_Camera_Point"
    bl_label = "Camera Point Panel"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        # Buttom to snap to the selected point (say we grabbed it in the collections)
        # Preview Mode vs Edit Mode
        ## Preview Mode should stick the primary to the point, at the correct orientation.
        ## Edit Mode should just move to the object as normal viewport might.
