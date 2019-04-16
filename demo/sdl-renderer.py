import time

import sdl2

from punyty.vector import Vector3
from punyty.objects import Cube
from punyty.renderers import SDLRenderer
from punyty.scene import Scene


if __name__ == '__main__':
    scene = Scene()
    cube = Cube()
    scene.add_object(cube)
    renderer = SDLRenderer(width=800, height=800)

    while True:
        t = time.time()
        renderer.render(scene)
        cube.rotate(Vector3(t, t, 0))
