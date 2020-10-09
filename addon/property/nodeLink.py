import bpy
from bpy.props import PointerProperty


def __isValidCameraPointObject(self, otherObj):
    if otherObj is None:
        return

    uuidOfTarget = otherObj.get("zag.uuid")
    if uuidOfTarget is None:
        return

    isCameraPoint = otherObj.get("zag.type") == "CameraPoint"
    notSelf: bool = self.get("zag.node_uuid") != uuidOfTarget

    notDuplicate = (
        (self.zagLinkNode0.get("zag.uuid") != uuidOfTarget if self.zagLinkNode0 else True)
        and
        (self.zagLinkNode1.get("zag.uuid") != uuidOfTarget if self.zagLinkNode1 else True)
    )

    return notSelf and isCameraPoint and notDuplicate

def __update(self, context):
    pass

def RegisterProperty():
    bpy.types.Object.zagLinkNode0 = PointerProperty(
        type=bpy.types.Object, poll=__isValidCameraPointObject, update=__update)
    bpy.types.Object.zagLinkNode1 = PointerProperty(
        type=bpy.types.Object, poll=__isValidCameraPointObject, update=__update)

def UnregisterProperty():
    del bpy.types.Object.zagLinkNode0
    del bpy.types.Object.zagLinkNode1
