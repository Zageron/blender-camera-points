import bpy
import os

from bpy import context as Context, types as Types

from ..state import ExportFile


class zag_op_SerializePoints(Types.Operator):
    """ Try to add an orientation to the camera point node. """

    bl_idname = "zag.serialize_points"
    bl_label = "Save out the camera points and orientations"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context: Context):
        ExportFile()
        return {"FINISHED"}
