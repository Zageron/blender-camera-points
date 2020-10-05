from .add_camera_point import zag_op_AddCameraPoint
from .adjust_camera_point_orientation import zag_op_AdjustCameraPointOrientation
from .add_orientation import zag_op_AddOrientation
from .remove_orientation import zag_op_RemoveOrientation
from .serialize_points import zag_op_SerializePoints
from .deletion_override import zag_op_DeletionOverride
from .deletion_override import zag_op_CollectionDeletionOverride

classes = (
    zag_op_AddCameraPoint,
    zag_op_AdjustCameraPointOrientation,
    zag_op_AddOrientation,
    zag_op_RemoveOrientation,
    zag_op_SerializePoints,
    zag_op_DeletionOverride,
    zag_op_CollectionDeletionOverride
)

def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
