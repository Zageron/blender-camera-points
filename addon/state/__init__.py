import bpy
import os
import json

from bpy import types

cameraPreviewIsActive: bool = False
cameraBeforePreview = None

# Should store some state data as an object.
# Then practice writing them out to a file.


DATAPATH = "data"
FILEPATH = "data\\CameraPoints.json"
TEXTNAME = "CameraPoints"

__activeDataInstance: dict = {}


def __load_file():

    filepath = bpy.path.abspath("//")
    if os.path.exists(filepath + FILEPATH):
        with open(filepath + FILEPATH, "r") as infile:
            global __activeDataInstance
            __activeDataInstance = json.loads(infile.read())
    else:
        __init_file()


def ExportFile():
    filepath = bpy.path.abspath("//")
    if not os.path.exists(filepath + DATAPATH):
        os.mkdir(filepath + DATAPATH)

    with open(filepath + FILEPATH, "w") as outfile:
        text: types.Text = bpy.data.texts.get(TEXTNAME)
        outfile.write(text.as_string())


def __load_internal_file():
    text: types.Text = bpy.data.texts.get(TEXTNAME)
    if text is not None:
        global __activeDataInstance
        __activeDataInstance = json.loads(text.as_string())
    else:
        __init_internal_file()


def __save_internal_file():
    text: types.Text = bpy.data.texts.get(TEXTNAME)
    if text is None:
        text = bpy.data.texts.new(TEXTNAME)

    text.clear()
    text.write(json.dumps(__activeDataInstance, indent=4))


def __init_internal_file():
    global __activeDataInstance
    __activeDataInstance = {
        "camera_points": {},
    }
    __save_internal_file()
    __load_internal_file()


def __init_file():
    global __activeDataInstance

    __activeDataInstance = {
        "camera_points": {},
    }
    __save_file()
    __load_file()


def __get_camera_points() -> list:
    if __activeDataInstance is not None:
        return list(__activeDataInstance.get("camera_points"))
    else:
        return []


def __get_camera_point(cameraPoints: list, uuid: str) -> dict:
    for point in cameraPoints:
        if point.get("zag.uuid") == uuid:
            return point

    return None


def AddCameraPoint(uuid: str) -> bool:
    __load_internal_file()

    cameraPointData = {
        "camera_point": {
            "uuid": "{uuid}".format(uuid=uuid),
            "orientations": [],
            # Gonna need links to other nodes with directions and such...
        }
    }

    cameraPoints: list = __get_camera_points()
    for point in cameraPoints:
        if point.get("uuid") == uuid:
            return False

    cameraPoints.append(cameraPointData)

    __activeDataInstance.update(camera_points=cameraPoints)
    __save_internal_file()
    pass


def __RemoveAllChildren(obj: types.Object):
    if len(obj.children) > 0:
        for child in obj.children:
            __RemoveAllChildren(child)

    if obj.get("zag.type") == "Orientation":
        RemoveOrientation(obj["zag.uuid"])
    else:
        __RemoveObject(obj)


def RemoveCameraPoint(uuid: str) -> bool:
    __load_internal_file()
    cameraPoints: list = __get_camera_points()
    cameraPoints = [
        point for point in cameraPoints if point.get("zag.uuid") != uuid]
    __activeDataInstance.update(camera_points=cameraPoints)
    __save_internal_file()

    # Scene object removal
    objects = bpy.data.objects
    cameraPointToRemove = [obj for obj in objects if obj.get("zag.uuid") == uuid and obj.get("zag.type") == "CameraPoint"]
    if cameraPointToRemove is not None:
        cpr = cameraPointToRemove[0]
        __RemoveAllChildren(cpr)


def AddOrientation(uuid: str) -> bool:
    pass


def RemoveOrientation(uuid: str) -> bool:
    # TODO There's no json logic yet.
    objs = bpy.data.objects
    obj = [item for item in objs if item.get("zag.uuid") == uuid]
    objs.remove(obj[0], do_unlink=True)


def __RemoveObject(obj: types.Object):
    objs = bpy.data.objects
    objs.remove(obj, do_unlink=True)


def UpdateOrientation() -> bool:
    pass


def SetPreviewCamera(previewCameraState: bool = False):

    if previewCameraState and not cameraPreviewIsActive:
        # Enable the preview camera.
        cameraBeforePreview = bpy.context.scene.camera

        # Create and link Previewing collection if not present.
        previewCollection = bpy.data.collections.get("Previewing")
        if previewCollection is None:
            previewCollection = bpy.data.collections.new("Previewing")
            bpy.context.scene.collection.children.link(previewCollection)

        # Create and link camera object.
        previewCamera = bpy.data.cameras.new("PreviewCamera")
        previewCameraObject = bpy.data.objects.new(
            "PreviewCameraObj", previewCamera)
        previewCollection.objects.link(previewCameraObject)

        # Set new camera as active camera

    elif not previewCameraState and cameraPreviewIsActive:
        # Disable the preview camera.
        pass

    previewCollection = bpy.data.collections.get("Previewing")
    if previewCollection is None:
        previewCollection = bpy.data.collections.new("Previewing")
        bpy.context.scene.collection.children.link(previewCollection)


def __GetWorldLocation(obj: types.Object) -> types.Object:
    if obj.parent:
        return obj.location + __GetWorldLocation(obj.parent)

    return obj.location

def Render():
    #output_path = bpy.context.scene.render.filepath
    #bpy.context.scene.render.filepath = os.path.join(output_path, ".png")
    #bpy.ops.render.render(animation=False, write_still=True)

    # Grab "Production Camera"
    productionCamera: bpy.types.Object
    for camera in bpy.data.objects:
        if camera.get("zag.type") == "ProductionCamera":
            productionCamera = camera

    if productionCamera is None:
        print("Unable to render, no ProductionCamera.")
        return

    # Construct the hierarchy of objects.
    # GetAllCameraPoints
    objects: bpy.types.Object = bpy.data.objects
    cameraPoints: list = [obj for obj in objects if obj.get("zag.type") == "CameraPoint"]

    cp: types.Object
    for cp in cameraPoints:
        id: str = cp.get("zag.uuid")
        orientations: list = [obj for obj in bpy.data.objects if obj.get("zag.type") == "Orientation" and obj.parent.get("zag.uuid") == id]
        print(orientations)

        output_path = bpy.context.scene.render.filepath
        orientation: types.Object
        for orientation in orientations:
            productionCamera.rotation_euler = orientation.rotation_euler
            productionCamera.location = __GetWorldLocation(orientation)

            bpy.context.scene.render.filepath = os.path.join(output_path, "{id}.png".format(id=orientation.get("zag.uuid")))
            bpy.ops.render.render(animation=False, write_still=True)

        bpy.context.scene.render.filepath = output_path
