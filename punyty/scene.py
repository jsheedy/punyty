from .camera import Camera
from .vector import Vector3


class DirectionalLight():
    def __init__(self, direction):
        self.direction = direction.normalize().A


class Scene:
    def __init__(self, f=10, cx=0.5, cy=0.5, ambient_light=0.1):
        self.objects = dict()
        self.main_camera = Camera(f=f, cx=cx, cy=cy, position=Vector3(0,0,-40))
        self.main_camera.look_at(Vector3(0, 0, 0))
        self.main_light = DirectionalLight(direction=Vector3(0,0,-1))
        self.ambient_light = ambient_light

    def add_object(self, obj, name=None):
        name = name or f'object-{len(self.objects)}'
        self.objects[name] = obj
        return name

    def update(self):
        for _, obj in self.objects.items():
            obj.update()