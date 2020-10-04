import bpy
from bpy import context as Context, types as Types
import uuid

class zag_op_RemoveOrientation(Types.Operator):
    """ Try to remove an orientation from the camera point node. """

    bl_idname = "zag.remove_node_orientation"
    bl_label = "Remove Node Orientation"
    bl_options = {'REGISTER', 'UNDO'}

    uuidToRemove = bpy.props.StringProperty(
        name="UUID to Remove",
        description="Removes the orientation matching the UUID, if valid.",
        default="Invalid")

    @classmethod
    def poll(cls, context: Context):
        if (context.object is not None):
            selectedObject = context.active_object

            if selectedObject.get("zag.uuid"):
                return True

        return False

    def execute(self, context: Context):
        objs = bpy.data.objects
        objs.remove(objs[self.uuidToRemove], do_unlink=True)
        return {'FINISHED'}
