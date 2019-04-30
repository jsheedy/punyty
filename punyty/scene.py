from .camera import Camera
from .object3d import Object3D
from .vector import Vector3


class Light(Object3D): pass

class Scene:
    def __init__(self, f=3.0, cx=0.5, cy=0.5):
        self.objects = dict()
        self.main_camera = Camera(f=f, cx=cx, cy=cy, position=Vector3(0,0,-5))
        self.main_camera.look_at(Vector3(0, 0, 0))
        self.main_light = Light(position=Vector3(1, 2, -5))

    def add_object(self, obj, name=None):
        name = name or f'object-{len(self.objects)}'
        self.objects[name] = obj
        return name
