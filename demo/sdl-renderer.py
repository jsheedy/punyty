import math
import itertools
from random import random
import time

from punyty.vector import Vector3
from punyty.objects import Cube, Tetrahedron, Octahedron
from punyty.model import Model
from punyty.renderers import SDLRenderer
from punyty.scene import Scene, DirectionalLight
import benchmark

def sin(x):
    return math.sin(x)/2+0.5

def cos(x):
    return math.cos(x)/2+0.5

if __name__ == '__main__':
    width = 1280
    height = 720

    scene = Scene(f=2000, cx=width/2, cy=height/2)
    scene.main_camera.position = Vector3(0, 0, -10)
    scene.main_camera.look_at(Vector3(0, 0, 0))
    cubes = (
        Tetrahedron(position=Vector3(-1, -1, 0), color=Vector3(1, 0, 0)),
        Cube(position=Vector3(-1, 1, 0), color=Vector3(0, 1, 0)),
        Octahedron(position=Vector3(1, -1, 0), color=Vector3(0, 0, 1)),
        Cube(position=Vector3(1, 1, 0), color=Vector3(.8, .0, .0)),
    )
    # for cube in cubes:
    #     scene.add_object(cube)
    # bunny = Model.load_ply('models/bunny.ply')
    bunny = Model.load_ply('/Users/velotron/assets/stegs-low-poly.ply')
    bunny.color = Vector3(1,.5,.75)
    bunny.rotate(Vector3(0,1.1, 0))
    # bunny = Model.load_ply('/Users/velotron/assets/velotron_arise_eecc.ply')
    # bunny = Model.load_ply('/Users/velotron/assets/sphere.ply')
    # bunny.position = Vector3(0, -0.01, -9.5)
    scene.add_object(bunny)

    renderer = SDLRenderer(width=width, height=height, clear_color=Vector3(0, 0, 0))

    bench = benchmark.Benchmark(renderer)

    d=-10
    l=1.9
    keys = itertools.cycle([
        (l, Vector3(0,0,-d)),
        (l, Vector3(d,0,0)),
        (l, Vector3(0,0,d)),
        (l,  Vector3(-d,0,0)),
        (l,  Vector3(0.01,d,0)),
        (l,  Vector3(0,-d,0.01)),
    ])

    key, target = next(keys)
    t0 = time.time()
    p0 = scene.main_camera.position

    key = 1
    while True:
        scene.main_light = DirectionalLight(direction=Vector3(cos(0.2*time.time()),2, sin(0.13*time.time())).normalize())
        t = time.time() - t0
        bunny.color = Vector3(1,1,1)
        # bunny.color = Vector3(cos(0.2*time.time())/2+0.5, cos(.1*time.time())/2+0.5, sin(.4*time.time())/2+0.5)
        # if t > key:

        #     t0 = time.time()
        #     t = 0
        #     key = 10*random()
        #     pos = math.pi*2*random()
        #     target = Vector3(math.sin(pos), 1, math.cos(pos))
        #     p0 = scene.main_camera.position
            # key, target = next(keys)
        # scene.main_camera.position = Vector3(
        #     10 - renderer.joystick.y * 20,
        #     1,
        #     10 - renderer.joystick.x * 20
        # )
        scene.main_camera.position = Vector3(4*math.sin(10*renderer.joystick.x), 1, 4*math.cos(10*renderer.joystick.x)) # p0.lerp(target, t/key) # + Vector3(0, 0, .1*cos(time.time()))
        scene.main_camera.look_at(Vector3.zero())
        # for cube in cubes:
        #     cube.rotate(Vector3(t, t, 0))

        renderer.render(scene, draw_edges=False, draw_polys=True, draw_axes=False)
        fps = bench.update(t)
        if fps:
            print(fps)
