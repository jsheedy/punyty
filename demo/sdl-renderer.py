from math import sin
import time

from punyty.vector import Vector3
from punyty.objects import Cube, Tetrahedron, Octahedron
from punyty.model import Model
from punyty.renderers import SDLRenderer
from punyty.scene import Scene
import benchmark

if __name__ == '__main__':
    width = height = 800

    scene = Scene(f=2000, cx=width/2, cy=height/2)
    scene.main_camera.position = Vector3(0, 0, -10)
    scene.main_camera.look_at(Vector3(0, 0, 0))
    cubes = (
        Tetrahedron(position=Vector3(-1, -1, 0), color=(1, 0, 0)),
        Cube(position=Vector3(-1, 1, 0), color=(0, 1, 0)),
        Octahedron(position=Vector3(1, -1, 0), color=(0, 0, 1)),
        Cube(position=Vector3(1, 1, 0), color=(1, 1, 1)),
    )
    # for cube in cubes:
    #     scene.add_object(cube)
    # bunny = Model.load_ply('/Users/velotron/Downloads/lucy.ply')
    bunny = Model.load_ply('models/bunny.ply')
    bunny.position = Vector3(0, -0.01, -9.5)
    scene.add_object(bunny)
    renderer = SDLRenderer(width=width, height=height)

    bench = benchmark.Benchmark(renderer)

    while True:
        t = time.time()
        # scene.main_camera.position = Vector3(0, 0, -10 + 5*sin(t/2))
        bunny.rotate(Vector3(renderer.joystick.y*6, renderer.joystick.x*6, 0))
        for cube in cubes:
            cube.rotate(Vector3(renderer.joystick.x*6, renderer.joystick.y*6, 0))
        renderer.render(scene, draw_edges=False, draw_polys=True, draw_axes=False)
        fps = bench.update(t)
        if fps:
            print(fps)
