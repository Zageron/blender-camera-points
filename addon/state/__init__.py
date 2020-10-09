import bpy
import os
import json
from mathutils import Vector

from bpy import types

cameraPreviewIsActive: bool = False
cameraBeforePreview = None

# Should store some state data as an object.
# Then practice writing them out to a file.


DATAPATH = "data"
FILEPATH = "data\\CameraPoints.json"
TEXTNAME = "CameraPoints"

__activeDataInstance: dict = {}


def __RemoveAllChildren(obj: types.Object):
    ''' Removes the hierarchy of all objects under an onbject in the Camera Point hierarchy. '''
    if len(obj.children) > 0:
        for child in obj.children:
            __RemoveAllChildren(child)

    __RemoveObject(obj)


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


def __get_camera_points() -> dict:
    if __activeDataInstance is not None:
        return __activeDataInstance.get("camera_points")
    else:
        return {}


def __get_camera_point(cameraPoints: list, uuid: str) -> dict:
    for point in cameraPoints:
        if point.get("zag.uuid") == uuid:
            return point

    return None


def AddCameraPoint(uuid: str) -> bool:
    __load_internal_file()

    cameraPointData = {
        "possible_node_data": "blah",
        "orientations": {}
    }

    cameraPoints: dict = __get_camera_points()

    if not cameraPoints.get(uuid):
        cameraPoints[uuid] = cameraPointData

        __activeDataInstance.update(camera_points=cameraPoints)
        __save_internal_file()


def RemoveCameraPoint(uuid: str) -> bool:
    __load_internal_file()
    cameraPoints: list = __get_camera_points()
    if cameraPoints.get(uuid):
        del cameraPoints[uuid]
        __activeDataInstance.update(camera_points=cameraPoints)
        __save_internal_file()

    # Scene object removal
    objects = bpy.data.objects
    cameraPointToRemove = [obj for obj in objects if obj.get("zag.uuid") == uuid and obj.get("zag.type") == "CameraPoint"]
    if cameraPointToRemove is not None:
        cpr = cameraPointToRemove[0]
        __RemoveAllChildren(cpr)


def AddOrientation(orientationId: str, cameraPointId: str):
    __load_internal_file()

    cameraPoints: dict = __get_camera_points()
    cameraPoint: dict = cameraPoints[cameraPointId]
    cameraPoint["orientations"][orientationId] = { "location": { "x": -1, "y": -1 } }
    __activeDataInstance.update(camera_points=cameraPoints)
    __save_internal_file()

def UpdateOrientationTargets(orientationId: str, cameraPointId: str, point: Vector):
    cameraPoints: dict = __get_camera_points()
    cameraPoint: dict = cameraPoints[cameraPointId]
    orientation:dict = cameraPoint["orientations"][orientationId]
    orientation.update({"location": {  "x": point[0], "y": point[1] }})

def RemoveOrientation(orientationId: str, cameraPointId: str):
    objs = bpy.data.objects
    obj = [item for item in objs if item.get("zag.uuid") == orientationId]
    objs.remove(obj[0], do_unlink=True)

    # Data deletion
    __load_internal_file()
    cameraPoints: dict = __get_camera_points()
    cameraPoint: dict = cameraPoints[cameraPointId]
    del cameraPoint["orientations"][orientationId]
    __activeDataInstance.update(camera_points=cameraPoints)
    __save_internal_file()


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

def __CorrectCameraOrientation(rotation_euler: list) -> list:
    temp: list = list(rotation_euler)
    temp[2] += 3.14
    return temp

def MoveCameraToOrientation(orientation: types.Object, productionCamera: types.Object):
    productionCamera.rotation_euler = __CorrectCameraOrientation(orientation.rotation_euler)
    productionCamera.location = __GetWorldLocation(orientation)

def Render(skipRendering: bool, calculateScreenPoints: bool):
    # Grab "Production Camera"
    productionCamera: bpy.types.Object = None
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

    __load_internal_file()

    cp: types.Object
    for cp in cameraPoints:
        id: str = cp.get("zag.uuid")
        orientations: list = [obj for obj in bpy.data.objects if obj.get("zag.type") == "Orientation" and obj.parent.get("zag.uuid") == id]

        output_path = bpy.context.scene.render.filepath
        orientation: types.Object
        for orientation in orientations:
            MoveCameraToOrientation(orientation, productionCamera)

            if calculateScreenPoints:
                p = __GetWorldLocation(orientation.zagLinkNode1.children[0])

                from bpy_extras.object_utils import world_to_camera_view

                scene = bpy.context.scene

                # needed to rescale 2d coordinates
                render = scene.render
                res_x = render.resolution_x
                res_y = render.resolution_y

                cam = productionCamera
                coords_2d = world_to_camera_view(scene, cam, p)

                mirrored_2d: dict = { "x": abs(coords_2d.x), "y": abs(coords_2d.y - 1) }
                # 2d data printout:
                rnd = lambda i: round(i)

                coordinates: Vector = (rnd(res_x*mirrored_2d["x"]), rnd(res_y*mirrored_2d["y"]), 0)

                UpdateOrientationTargets(orientation.get("zag.uuid"), id, coordinates)

            if not skipRendering:
                bpy.context.scene.render.filepath = os.path.join(output_path, "{id}.png".format(id=orientation.get("zag.uuid")))
                bpy.ops.render.render(animation=False, write_still=True)

        __save_internal_file()
        bpy.context.scene.render.filepath = output_path

