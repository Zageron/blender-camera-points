import bpy
from bpy import context as Context, types as Types
import uuid

from bpy.props import BoolProperty

from ..state import Render

class _zag_op_RenderPrototype(Types.Operator):
    """ Render every orientation. """
    bl_options = {'REGISTER'}

    calculateScreenPoints: BoolProperty("Calculate Screen Points")
    skipRendering: BoolProperty("Skip Rendering")

    @classmethod
    def poll(cls, context: Context):
        return True

    def executeRender(self, context: Context):
        Render(self.skipRendering, self.calculateScreenPoints)
        return {"FINISHED"}

class zag_op_RenderAll(_zag_op_RenderPrototype):
    bl_idname = "zag.render_all"
    bl_label = "Render All"

    def execute(self, context: Context):
        self.skipRendering = False
        self.calculateScreenPoints = True
        return self.executeRender(context)

class zag_op_CalculateAll(_zag_op_RenderPrototype):
    bl_idname = "zag.calc_all"
    bl_label = "Calculate All"

    def execute(self, context: Context):
        self.skipRendering = True
        self.calculateScreenPoints = True
        return self.executeRender(context)
