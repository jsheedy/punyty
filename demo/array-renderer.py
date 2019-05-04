""" Doesn't display anything, primarily for benchmarking
ArrayRenderer independent of display """

import time

import numpy as np

from punyty.vector import Vector3
from punyty.objects import Cube
from punyty.renderers import ArrayRenderer
from punyty.scene import Scene

import benchmark


if __name__ == '__main__':
    width = 800
    height = 800
    target_array = np.zeros((height, width, 3))
    scene = Scene()
    cube = Cube()
    scene.add_object(cube)
    renderer = ArrayRenderer(target_array=target_array)

    bench = benchmark.Benchmark(renderer)

    while True:
        t = time.time()
        renderer.render(scene)
        cube.rotate(Vector3(time.time(), 0, 0))
        fps = bench.update(t)
        if fps:
            print(fps)