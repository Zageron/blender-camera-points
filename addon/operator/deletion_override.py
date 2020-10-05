import bpy
import uuid

from bpy import context as Context, types as Types

from ..state import RemoveCameraPoint, RemoveOrientation

from bpy.props import BoolProperty

def __RemoveObject(obj: Types.Object):
    objs = bpy.data.objects
    objs.remove(obj, do_unlink=True)

def __RemoveObjectHierarchy(obj: Types.Object):
    if len(obj.children) > 0:
        for child in obj.children:
            __RemoveObjectHierarchy(child)

    __RemoveObject(obj)

def CheckTypeAndDelete(context: Types.Context, hierarchy: bool = False):
    count: int = len(context.selected_objects)
    obj: Types.Object
    for obj in context.selected_objects:
        type = obj.get("zag.type")

        if type is None:
            if hierarchy:
                __RemoveObjectHierarchy(obj)
            else:
                __RemoveObject(obj)
        elif type == "CameraPoint":
            RemoveCameraPoint(obj["zag.uuid"])
        elif type == "OrientationPoint":
            print(obj.name + ' is protected.')
        elif type == "Orientation":
            RemoveOrientation(obj["zag.uuid"])
        else:
            # Shouldn't ever get here.
            pass

    if count == 0:
        activeCollection = context.view_layer.active_layer_collection
        if activeCollection.name != "Points":
            if hierarchy:
                bpy.data.collections.remove(activeCollection.collection)
            else:
                print(activeCollection.name + 'Please delete hierarchy to delete collections.')
        else:
            print(activeCollection.name + ' collection is protected.')



class zag_op_DeletionOverride(Types.Operator):
    """ Check to see if the object being deleted is our custom object. """

    bl_idname = "object.delete"
    bl_label = "Delete Object"
    bl_options = {'REGISTER', 'UNDO'}

    use_global: BoolProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context: Types.Context):
        CheckTypeAndDelete(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class zag_op_CollectionDeletionOverride(Types.Operator):
    """ Check to see if the object being deleted in the collection is our custom object. """

    bl_idname = "outliner.delete"
    bl_label = "Delete Object"
    bl_options = {'REGISTER', 'UNDO'}

    hierarchy: BoolProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context: Types.Context):
        CheckTypeAndDelete(context, self.hierarchy)
        return {'FINISHED'}
