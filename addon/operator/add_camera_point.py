import bpy
import uuid


class zag_op_AddCameraPoint(bpy.types.Operator):
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

    def execute(self, context):

        # uuid for the camera point
        id = str(uuid.uuid4())
        print(uuid)

        emptyObject = bpy.data.objects.new("CameraPoint", None)

        # Add the point to collection
        parent = bpy.data.collections.get("Points")
        if parent is None:
            parent = bpy.data.collections.new("Points")
            bpy.context.scene.collection.children.link(parent)

        # Position the point
        emptyObject.location = bpy.context.scene.cursor.location

        # set unique id
        emptyObject["uuid"] = id

        parent.objects.link(emptyObject)
        return {'FINISHED'}
