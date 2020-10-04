import bpy

from bpy import context as Context, types as Types


class ZAG_OP_AdjustCameraPointOrientation(bpy.types.Operator):
    bl_idname = "zag.adjust_camera_point_orientation"
    bl_label = "ZAG Adjust Camera Point Orientation"
    bl_description = "Camera Point Adjustment Modal"
    bl_options = {"REGISTER", "UNDO", "BLOCKING"}

    uuid = bpy.props.StringProperty(
        name="Orientation UUID",
        description="UUID of the orientation we want to adjust..",
        default="Invalid")

    @classmethod
    def poll(cls, context: Context):
        if (context.object is not None):
            selectedObject = context.active_object

            if selectedObject.get("zag.type") == "CameraPoint":
                return True

        return False

    def invoke(self, context: Context, event: Types.Event):
        if uuid != "Invalid":
            context.window_manager.modal_handler_add(self)
            self.setup(context)
            return {"RUNNING_MODAL"}
        else:
            return {"CANCELLED"}

    def setup(self, context: Context):
        # Add a camera.
        # Place the camera at the OrientationPoint.
        # Position the camera to the rotation of the orientation object.
        # Frame to the camera.

        ## Mode / Button 1:
        ### Free orient
        ## Mode / Button 2:
        ### Place target for movement.

        pass

    def modal(self, context: Context, event: Types.Event):
        if event.type == "MIDDLEMOUSE":
            return {"PASS_THROUGH"}

        elif event.type == "LEFTMOUSE" and event.value == "PRESS":
            return {"FINISHED"}

        elif event.type == "RIGHTMOUSE" and event.value == "PRESS":
            return {"CANCELLED"}

        elif event.type == "MOUSEMOVE":
            delta = event.mouse_x - event.mouse_prev_x
            print(delta)

        return {"RUNNING_MODAL"}
