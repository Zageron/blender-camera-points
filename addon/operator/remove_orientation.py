import bpy
from bpy import context as Context, types as Types
import uuid

from ..state import RemoveOrientation
from bpy.props import StringProperty

class zag_op_RemoveOrientation(Types.Operator):
    """ Try to remove an orientation from the camera point node. """

    bl_idname = "zag.remove_node_orientation"
    bl_label = "Remove Node Orientation"
    bl_options = {'REGISTER', 'UNDO'}

    uuidToRemove: StringProperty(
        name="UUID to Remove",
        description="Removes the orientation matching the UUID, if valid.",
        default="Invalid")

    cameraPointId: StringProperty(
        name="UUID of Parent Camera Point",
        description="Id of the parent of the orientation to remove.",
        default="Invalid"
    )

    @classmethod
    def poll(cls, context: Context):
        if (context.object is not None):
            selectedObject = context.active_object

            if selectedObject.get("zag.uuid"):
                return True

        return False

    def execute(self, context: Context):
        if self.uuidToRemove != "Invalid" and self.cameraPointId != "Invalid":
            RemoveOrientation(self.uuidToRemove, self.cameraPointId)
            return {'FINISHED'}
        else:
            return {"CANCELED"}
