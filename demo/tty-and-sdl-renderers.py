""" two renderers at once """
import time

from punyty.vector import Vector3
from punyty.objects import Cube, Tetrahedron
from punyty.renderers import TTYRenderer, SDLRenderer
from punyty.scene import Scene


if __name__ == '__main__':
    width = 800
    height = 800
    scene = Scene()
    cube = Cube()
    tetrahedron = Tetrahedron()
    scene.add_object(Tetrahedron)
    tty_renderer = TTYRenderer()
    sdl_renderer = SDLRenderer(width=width, height=height)

    while True:
        t = time.time()
        tty_renderer.render(scene)
        sdl_renderer.render(scene)
        tetrahedron.rotate(Vector3(t, 0, 0))
