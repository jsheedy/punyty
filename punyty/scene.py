from .camera import Camera
from .lights import DirectionalLight, AmbientLight
from .vector import Vector3


class Scene:
    def __init__(self, f=3, cx=0.5, cy=0.5, lights=None):
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