from .add_camera_point import zag_op_AddCameraPoint
from .adjust_camera_point_orientation import ZAG_OP_AdjustCameraPointOrientation
from .add_orientation import zag_op_AddOrientation
from .remove_orientation import zag_op_RemoveOrientation

classes = (
    zag_op_AddCameraPoint,
    ZAG_OP_AdjustCameraPointOrientation,
    zag_op_AddOrientation,
    zag_op_RemoveOrientation
)

def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
