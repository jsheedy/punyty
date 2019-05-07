from math import sin, cos, tan
import time

from punyty.model import Model
from punyty.objects import Cube
from punyty.renderers import SDLRenderer
from punyty.scene import Scene
from punyty.vector import Vector3

def flyby():
    width = height = 800

    scene = Scene(f=2000, cx=width/2, cy=height/2)
    scene.main_camera.position = Vector3(0, 10, -5)
    scene.main_camera.look_at(Vector3.zero())
    cubes = [
        Cube(color=(0, 1, 0), position=Vector3(x, 0, z))
        for x in range(-10, 10, 2) for z in range(-10, 10, 2)
    ]
    cubes = [Cube(), Cube(position=Vector3(0, 0, 2))]

    renderer = SDLRenderer(width=width, height=height)

    for o in cubes:
        scene.add_object(o)

    t0 = time.time()
    while True:
        t = time.time()
        dt = t - t0
        # scene.main_camera.position = Vector3(50*sin(t/2), 30*tan(t/8), 50*cos(t/2))
        scene.main_camera.look_at(Vector3(0, 0, 0))
        # for o in cubes:
            # o.rotate(Vector3(-.2, 0.5*t, t/10))
        renderer.render(scene, draw_polys=True, draw_edges=True)

if __name__ == '__main__':
    flyby()
