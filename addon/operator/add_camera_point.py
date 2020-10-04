import bpy
import uuid
import types
import typing

from bpy import context as Context, types as Types


class zag_op_AddCameraPoint(Types.Operator):
    """ Add a camera point, with associated metadata, to the scene. """

    bl_idname = "zag.add_camera_point"
    bl_label = "Add Camera Point"
    bl_options = {'REGISTER', 'UNDO'}

    # from bpy.props import IntProperty, FloatProperty
    # radius: FloatProperty(name="Radius", default=1, min=1, max=100)
    # height: FloatProperty(name="Height", default=1, min=0, max=10)
    # count: IntProperty(name="Light Count", default=3, min=3, max=50)
    # energy: IntProperty(name="Light Energy", default=1000, min=500, max=2500)

    # def draw(self, context):
    #     layout = self.layout
    #     layout.prop(self, 'radius')
    #     layout.prop(self, 'height')
    #     layout.prop(self, 'count')
    #     layout.prop(self, 'energy')

    def execute(self, context: Context):

        # uuid for the camera point
        id: str = str(uuid.uuid4())

        emptyObject = bpy.data.objects.new("CameraPoint", None)

        # Add the point to collection
        parent = bpy.data.collections.get("Points")
        if parent is None:
            parent = bpy.data.collections.new("Points")
            bpy.context.scene.collection.children.link(parent)

        # Position the point
        emptyObject.location = bpy.context.scene.cursor.location

        # Lock up the rotation of the point by default.
        emptyObject.lock_rotation = [True, True, True]
        emptyObject.lock_rotation_w = True
        emptyObject.lock_rotations_4d = True
        emptyObject.lock_scale = [True, True, True]

        # set unique id
        emptyObject["zag.uuid"] = id
        emptyObject["zag.type"] = "CameraPoint"

        parent.objects.link(emptyObject)

        # Create orientation position container
        orientations = bpy.data.objects.new("OrientationPoint" + id, None)
        orientations.empty_display_type = "SPHERE"
        orientations.empty_display_size = .25
        orientations.location[2] = 1.7
        orientations["zag.uuid"] = id
        orientations["zag.type"] = "OrientationPoint"

        parent.objects.link(orientations)
        orientations.parent = emptyObject

        orientations.lock_location = [True, True, True]
        orientations.lock_rotation = [True, True, True]
        orientations.lock_rotation_w = True
        orientations.lock_rotations_4d = True
        orientations.lock_scale = [True, True, True]

        bpy.context.view_layer.objects.active = emptyObject
        return {'FINISHED'}
