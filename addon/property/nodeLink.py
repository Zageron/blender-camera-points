import bpy
from bpy.props import PointerProperty


def __isValidOrientationObject(self, otherObj):
    return otherObj is not None and otherObj.get("zag.type") == "Orientation"


def RegisterProperty():
    bpy.types.Object.zagLinkNode0 = PointerProperty(
        type=bpy.types.Object, poll=isValidOrientationObject)
    bpy.types.Object.zagLinkNode1 = PointerProperty(
        type=bpy.types.Object, poll=isValidOrientationObject)
