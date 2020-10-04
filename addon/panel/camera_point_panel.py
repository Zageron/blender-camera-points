import bpy

from bpy.props import FloatVectorProperty

bl_info = {
    "name": "Camera Point Panel",
    "author": "Zageron",
    "description": "Panel for controlling the camera point properties on a node.",
    "blender": (2, 90, 0),
    "version": (0, 1, 0),
    "location": "",
    "warning": "",
    "category": "Generic"
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

        if context.object is not None:
            selectedObject = bpy.context.view_layer.objects.active
            id: str = selectedObject.get("zag.uuid")
            if selectedObject.get("zag.type") == "CameraPoint":
                layout.label(text="UUID: " + id)

                layout.separator()

                # Location of the physical player point.
                layout.prop(data=selectedObject,
                            property="location", text="Location")

                ## Begin Section for Orientations
                layout.separator()

                ## Check for orientations.
                orientationPointObject = bpy.data.objects.get(
                    "OrientationPoint" + id)
                orientations = orientationPointObject.children
                layout.label(text="Orientations ({count}/{maximum})"
                             .format(
                                 count=orientations.__len__(),
                                 maximum=4))

                layout.operator(
                    operator="view3d.view_selected", text="Focus on Point", icon="FORWARD")

                # Add Orientation
                layout.operator(
                    "zag.add_node_orientation",
                    text="Add New Orientation",
                    icon="OUTLINER_OB_POINTCLOUD")

                for orientation in orientations:
                    id: str = orientation["zag.uuid"]

                    subLayout = layout.box()
                    subLayout.prop(
                        data=orientation, property="rotation_euler", text="Orientation")
                    adjustCameraProps = subLayout.operator(
                        "zag.adjust_camera_point_orientation",
                        text="Realtime Orientation Adjust",
                        icon="CON_CAMERASOLVER")
                    adjustCameraProps.uuid = id

                    removeProps = subLayout.operator(
                        "zag.remove_node_orientation",
                        text="Remove Orientation",
                        icon="X"
                    )
                    removeProps.uuidToRemove = "Orientation" + id
            else:
                layout.label(text="No camera point selected.")
        else:
            layout.label(text="No object is selected.")

        # Preview Mode vs Edit Mode
        ## Preview Mode should stick the primary to the point, at the correct orientation.
        ## Edit Mode should just move to the object as normal viewport might.
