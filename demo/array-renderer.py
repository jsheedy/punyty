import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from punyty.vector import Vector3
from punyty.objects import Cube
from punyty.renderers import ArrayRenderer
from punyty.scene import Scene


if __name__ == '__main__':
    width = 800
    height = 800
    target_array = np.zeros((height, width, 3))
    scene = Scene()
    cube = Cube()
    scene.add_object(cube)
    renderer = ArrayRenderer(target_array=target_array)

    plt.show()
    matplotlib.interactive(False)

    for i in range(20):
        renderer.render(scene)
        plt.imshow(target_array)
        plt.show()
        cube.rotate(Vector3(time.time(), 0, 0))
        time.sleep(0.1)