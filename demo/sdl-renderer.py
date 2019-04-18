import time

import sdl2

from punyty.vector import Vector3
from punyty.objects import Cube
from punyty.renderers import SDLRenderer
from punyty.scene import Scene


if __name__ == '__main__':
    width = height =800

    scene = Scene(f=2000, cx=width/2, cy=height/2)
    cube = Cube()
    scene.add_object(cube)
    renderer = SDLRenderer(width=width, height=height)

    while True:
        t = time.time()
        renderer.render(scene)
        cube.rotate(Vector3(t, t, 0))
