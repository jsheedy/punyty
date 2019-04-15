from .camera import Camera
from .vector import Vector3


class Scene:
    def __init__(self):
        self.objects = dict()
        self.cameras = dict()
        self.main_camera = Camera(position=Vector3(0,0,-5))
        self.main_camera.look_at(Vector3(0, 0, 0))

    def add_object(self, obj, name=None):
        name = name or f'object-{len(self.objects)}'
        self.objects[name] = obj
        return name
