from .camera import Camera
from .vector import Vector3


class DirectionalLight():
    def __init__(self, direction):
        self.direction = direction.normalize().A


class PointLight():
    def __init__(self, position, intensity=1.0):
        self.position = position
        self.intensity = intensity


class AmbientLight():
    def __init__(self, intensity=0.1):
        self.intensity = intensity


class Scene:
    def __init__(self, f=3, cx=0.5, cy=0.5):
        self.objects = dict()
        self.main_camera = Camera(f=f, cx=cx, cy=cy, position=Vector3(0,0,-10))
        self.main_camera.look_at(Vector3(0, 0, 0))
        self.lights = [
            DirectionalLight(direction=Vector3(1,-1,0)),
            AmbientLight(intensity=0.3),
        ]

    def add_object(self, obj, name=None):
        name = name or f'object-{len(self.objects)}'
        self.objects[name] = obj
        return name

    def update(self):
        for _, obj in self.objects.items():
            obj.update()