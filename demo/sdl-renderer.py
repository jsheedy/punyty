import time

from punyty.vector import Vector3
from punyty.objects import Cube
from punyty.renderers import SDLRenderer
from punyty.scene import Scene
import benchmark

if __name__ == '__main__':
    width = 1280
    height = 720

    scene = Scene()

    cube = Cube(color=Vector3(1, 1, 1))
    scene.add_object(cube)

    renderer = SDLRenderer(width=width, height=height)

    bench = benchmark.Benchmark(renderer)

    while True:
        scene.update()

        t = time.time()

        cube.rotate(Vector3(t, t, t))

        renderer.render(scene, draw_edges=False, draw_polys=True)

        fps = bench.update(t)
        if fps:
            print(fps)
