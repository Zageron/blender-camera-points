import bpy
from bpy import context as Context, types as Types
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
    def poll(cls, context: Context):
        return (context.object is not None)


class ZAG_CameraPointPanel(View3DPanel, bpy.types.Panel):
    bl_idname = "ZAG_PT_Camera_Point"
    bl_label = "Camera Point Panel"
    bl_context = "objectmode"

    def draw_orientation(self, context: Context, selectedObject: Types.Object, objectUuid: str):
        layout = self.layout
        layout.label(text="Please select:")
        layout.label(text="    - An Orientation")
        layout.label(text="    - The parent Camera Point")
        pass

    def draw_camera_point(self, context: Context, selectedObject: Types.Object, objectUuid: str):
        layout = self.layout
        layout.label(text="UUID: " + objectUuid)

        layout.separator()

        # Location of the physical player point.
        layout.prop(data=selectedObject,
                    property="location", text="Location")

        ## Begin Section for Orientations
        layout.separator()

        ## Check for orientations.
        orientationPointObject = bpy.data.objects.get(
            "OrientationPoint-{id}".format(id=objectUuid))
        orientations = orientationPointObject.children
        layout.label(text="Orientations ({count}/{maximum})"
                        .format(
                            count=orientations.__len__(),
                            maximum=4))

        layout.operator(
            operator="view3d.view_selected", text="Focus on Point", icon="FORWARD"
        )

        layout.operator(
            operator="zag.serialize_points", text="Save", icon="FILE_TICK"
        )

        # Add Orientation
        layout.operator(
            "zag.add_node_orientation",
            text="Add New Orientation",
            icon="OUTLINER_OB_POINTCLOUD")

        for orientation in orientations:
            orientationId: str = orientation["zag.uuid"]

            subLayout = layout.box()
            subLayout.prop(
                data=orientation, property="rotation_euler", text="Orientation")
            adjustCameraProps = subLayout.operator(
                "zag.adjust_camera_point_orientation",
                text="Realtime Orientation Adjust",
                icon="CON_CAMERASOLVER")
            adjustCameraProps.uuid = orientationId

            subLayout.prop(data=orientation, property="zagLinkNode0", text="Linked Node")
            subLayout.prop(data=orientation, property="zagLinkNode1", text="Linked Node")

            removeProps = subLayout.operator(
                "zag.remove_node_orientation",
                text="Remove Orientation",
                icon="X"
            )
            removeProps.uuidToRemove = orientationId
            removeProps.cameraPointId = objectUuid

    def draw_general(self, context: Context):
        layout = self.layout
        pass


    def draw_error(self, context: Context):
        layout = self.layout
        subLayout = layout.box()
        subLayout.label(text="For more information, please select:")
        subLayout.label(text="    - An Orientation")
        subLayout.label(text="    - The parent Camera Point")

    def draw(self, context: Context):
        objectUuid: str = ""
        objectType: str = ""

        # General Tool Portion
        self.draw_general(context)

        # Active Object Acquisition
        if context.object is not None:
            selectedObject: Types.Object = bpy.context.view_layer.objects.active
            objectUuid: str = selectedObject.get("zag.uuid")
            objectType: str = selectedObject.get("zag.type")

        # Camera Point Specific Panel
        if objectType == "CameraPoint":
            self.draw_camera_point(context, selectedObject, objectUuid)

        # Specific Orientation Panel
        elif objectType == "Orientation":
            self.draw_error(context)

        elif objectType == "OrientationPoint":
            self.draw_orientation(context, selectedObject, objectUuid)
