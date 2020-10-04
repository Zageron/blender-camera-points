import bpy
import uuid
from bpy import context as Context, types as Types
import typing


class zag_op_AddOrientation(Types.Operator):
    """ Try to add an orientation to the camera point node. """

    bl_idname = "zag.add_node_orientation"
    bl_label = "Add Node Orientation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: Context):
        if (context.object is not None):
            selectedObject: Types.Object = context.active_object
            if selectedObject.get("zag.type") == "CameraPoint":
                id: str = selectedObject.get("zag.uuid")
                orientationPoint = bpy.data.objects.get("OrientationPoint" + id)
                if orientationPoint.children.__len__() < 4:
                    return True

        return False

    def execute(self, context: Context):
        selectedObject: Types.Object = context.active_object
        if selectedObject.get("zag.type") == "CameraPoint":

            # Initialize the orientation object.
            id: str = str(uuid.uuid4())
            orientationObject: Types.Object = bpy.data.objects.new("Orientation" + id, None)
            orientationObject.empty_display_size = 1.0
            orientationObject.empty_display_type = "SINGLE_ARROW"
            orientationObject.rotation_euler[0] = -1.570796

            # Lock up the object by default.
            orientationObject.lock_scale = [True, True, True]
            orientationObject.lock_location = [True, True, True]

            # Custom Properties
            orientationObject["zag.uuid"] = id
            orientationObject["zag.type"] = "Orientation"


            # Add object to scene and Points collection, set parent.
            pointsCollection: Types.Collection = bpy.data.collections.get("Points")
            pointsCollection.objects.link(orientationObject)

            parentId: str = selectedObject.get("zag.uuid")
            parent = bpy.data.objects.get("OrientationPoint" + parentId)
            orientationObject.parent = parent

        # Fixup
        #emptyObject["orientations"] = [[] for i in range(3)]
        #emptyObject["orientations"][0] = typing.List[float]
        #emptyObject["orientations"][1] = typing.List[float]
        #emptyObject["orientations"][2] = typing.List[float]
        return {"FINISHED"}
