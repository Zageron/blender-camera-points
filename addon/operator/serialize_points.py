import bpy
from bpy import context as Context, types as Types


class zag_op_SerializePoints(Types.Operator):
    """ Try to add an orientation to the camera point node. """

    bl_idname = "zag.serialize_points"
    bl_label = "Save out the camera points and orientations"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context: Context):
        DATAPATH = "data/"

        if not os.path.exists(DATAPATH):
            os.mkdir(DATAPATH)

            filepath = bpy.data.filepath
            file = open(filepath + DATAPATH + "textfile", "w")
            file.write(json.dump(zagDataObject))
            file.close()

        return {"FINISHED"}
