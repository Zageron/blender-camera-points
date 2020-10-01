from .add_camera_point import zag_op_AddCameraPoint

classes = (
    zag_op_AddCameraPoint,
)

def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
