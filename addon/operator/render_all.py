"""
Allows for queues rendering of sets of the CameraPoints and their orientations.
"""

import uuid

import bpy
from bpy import context as Context, types as Types
from bpy.props import BoolProperty

from .. import state


class _zag_op_RenderPrototype(Types.Operator):
    """ Parent operator type for scanning all camera points. """

    bl_options = {'REGISTER'}
    calculateScreenPoints: BoolProperty("Calculate Screen Points")
    skipRendering: BoolProperty("Skip Rendering")

    @classmethod
    def poll(cls, context: Context):
        return True

    def executeRender(self, _context: Context):
        """ Base call for activating the render pipeline. """

        return state.Render(self.skipRendering, self.calculateScreenPoints)


class zag_op_RenderAll(_zag_op_RenderPrototype):
    """ Render every orientation. """

    bl_idname = "zag.render_all"
    bl_label = "Render All"

    _timer: Types.Timer = None
    rendering: bool = False
    stop: bool = False

    def pre(self, _dummy):
        """ Handler for Blender's Pre Render callback. Marks as currently rendering. """

        self.rendering = True

    def post(self, _dummy):
        """ Handler for Blender's post Render callback. Marks as finished rendering. """

        self.rendering = False

    def cancelled(self, _dummy):
        """ Handler for Blender's cancelled Render callback. Marks render as stopped. """

        self.stop = True

    def execute(self, context: Context):

        if not state.IsSceneRenderable():
            print("Unable to render, no ProductionCamera.")
            return { "CANCELLED" }

        bpy.app.handlers.render_pre.append(self.pre)
        bpy.app.handlers.render_post.append(self.post)
        bpy.app.handlers.render_cancel.append(self.cancelled)

        self._timer = context.window_manager.event_timer_add(
            0.5, window=context.window)
        context.window_manager.modal_handler_add(self)

        self.skipRendering = False
        self.calculateScreenPoints = True

        return {"RUNNING_MODAL"}

    def modal(self, context: Context, event):
        if event.type == 'TIMER':
            if True in (not self.shots, self.stop is True):

                # We remove the handlers and the modal timer to clean everything
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)

                return {"FINISHED"}

            elif self.rendering is False:
                # We should move on to the next render item.
                self.executeRender(context)

            return {"PASS_THROUGH"}

class zag_op_CalculateAll(_zag_op_RenderPrototype):
    """ Calculate and save all of the camera points and their orientations. """

    bl_idname = "zag.calc_all"
    bl_label = "Calculate All"

    def execute(self, context: Context):
        """ Executes a calculation path, no rendering occurs. """

        self.skipRendering = True
        self.calculateScreenPoints = True
        return self.executeRender(context)
