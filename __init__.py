# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.props import *
from bpy.types import Collection, CollectionObjects
from collections import defaultdict
import string

bl_info = {
    "name": "Move X Axis",
    "author": "Adam Bryant",
    "description": "",
    "blender": (2, 82, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Object"
}


class ObjectsToFaceCamera(bpy.types.Operator):
    """Education Arena Interactables Camera Setup"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "arena.face_camera"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Interactables Face Camera"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # execute() is called when running the operator.
    def execute(self, context):

        # The original script
        scene = context.scene
        for obj in scene.collections:
            obj.location.x += 1.0

        # Lets Blender know the operator finished successfully.
        return {'FINISHED'}


import bpy

class HelloWorldPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_options = {"DEFAULT_CLOSED"}


class HELLO_PT_World1(HelloWorldPanel, bpy.types.Panel):
    bl_idname = "HELLO_PT_World1"
    bl_label = "Panel 1"

    def draw(self, context):
        layout = self.layout
        metaCollection: Collection = bpy.context.scene.collection.children["Meta"]
        cameraPointsCollection: CollectionObjects = metaCollection.children["cp"]
        layout.label(text="Items in Collection")
        col = layout.column()
        col.label(text=cameraPointsCollection.objects["a"].name)
        col.label(text=cameraPointsCollection.objects["a"].location.__str__())


class HELLO_PT_World2(HelloWorldPanel, bpy.types.Panel):
    bl_parent_id = "HELLO_PT_World1"
    bl_label = "Panel 2"

    def draw(self, context):
        layout = self.layout
        layout.label(text="First Sub Panel of Panel 1.")


class HELLO_PT_World3(HelloWorldPanel, bpy.types.Panel):
    bl_parent_id = "HELLO_PT_World1"
    bl_label = "Panel 3"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Second Sub Panel of Panel 1.")


classes = (
    HELLO_PT_World1,
    HELLO_PT_World2,
    HELLO_PT_World3,
    ObjectsToFaceCamera
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()
