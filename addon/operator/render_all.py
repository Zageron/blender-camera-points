import bpy
from bpy import context as Context, types as Types
import uuid

from ..state import Render

class zag_op_RenderAll(Types.Operator):
    """ Render every orientation. """

    bl_idname = "zag.render_all"
    bl_label = "Render All"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context: Context):
        return True

    def execute(self, context: Context):
        Render()
        return {"FINISHED"}

